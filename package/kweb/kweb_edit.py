#!/usr/bin/env python
# -*- coding: utf-8 -*-

# kweb souce text editor
# This program is part of the Minimal Kiosk Browser (kweb) system.
# version 1.7.0

# Copyright 2016 by Guenter Kreidl
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import os,sys,subprocess
import Tkinter as tk
import tkMessageBox,tkFileDialog,tkSimpleDialog

default_text=u'''#!mode=mixed
#!spacer= 
#!target=top
#!pagetitle='''

abouterror = '''The name of kweb's user defined :Command pages may not
contain one of the following characters: /.&?"\''''

argumenterror = '''Wrong kind or number of arguments.'''

rooterror = '''To edit this file requires root access. Use
gksudo kweb_edit.py ...'''

textfileerror ='''Text files to be used by kweb_edit.py must use a ".txt" extension.'''

loaderror = '''Text file could not be opened.'''

emptyabouterror = '''You must give your new :Command page a name.'''

newtext = '''You are creating a new text file to compile to HTML.'''

edittext = '''You are editing the file:
$name$'''

newedit = '''You are creating the file:
$name$'''

installationerror = '''No kweb directory or data found!

You need to (re)install kweb to use this utility.'''

def checkinstallation():
    if not os.path.exists('/usr/local/share/kweb'):
        return False
    if not os.path.exists('/usr/local/bin/kwebhelper_set.py'):
        return False
    return True

def get_default_text(fname,about):
    if fname == 'kwebautoconfig.txt':
        txt = '=?#'
    else:
        txt = default_text
        if about or fname.startswith('kweb_about_'):
            txt += '\n#<h2>Untitled</h2>'
    return txt

def checkabout(aboutname):
    if aboutname in ['c','s','e','k','o','p','m']:
        return False
    forbidden = '/.&$=\\?"\''
    ret = True
    for ch in aboutname:
        if ch in forbidden:
            ret = False
            break
    return ret

class App(tk.Frame):              
    def __init__(self, master=None,fpath='',fname='',text='', errmsg='',msg='',fontsize='12'):
        tk.Frame.__init__(self, master)
        self.font = ('SansSerif',fontsize,'bold')
        self.root = master
        self.master.title('Kweb Editor for User Pages')
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.fpath = fpath
        self.fname = fname
        self.text = text
        self.modified = False
        self.about = ''
        if fname.startswith('kweb_about_'):
            self.about = self.fname.replace('kweb_about_','').replace('.txt','')
        self.errmsg = errmsg
        self.msg = msg
        self.root.protocol('WM_DELETE_WINDOW', self.quitapp)
        self.createWidgets()
        if not self.errmsg:
            top.minsize(480,240)
            self.rowconfigure(1, weight=1)
            self.columnconfigure(0, weight=1)
            self.textbox.insert('0.0',text)
            self.textbox.edit_reset()
            self.textbox.edit_modified(False)
            self.textbox.focus()

    def createWidgets(self):
        if self.errmsg:
            self.mtext = tk.Label(self,text=self.errmsg,font=self.font,width=60)
            self.mtext.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W)
            self.quitbutton=tk.Button(self, takefocus=1, command=self.quitapp, font=self.font, text = 'Quit', justify = tk.CENTER)
            self.quitbutton.grid(row=1,column=0)
        else:
            self.mtext = tk.Label(self,text=self.msg,font=self.font,width = 60)
            self.mtext.grid(row=0,column=0,columnspan=2,sticky=tk.E+tk.W)
            self.textbox = tk.Text(self, bd=0, takefocus=1, width = 60, height = 16, font=self.font, wrap=tk.NONE, undo=True, maxundo=-1)
            self.textbox.bind('<Button-3><ButtonRelease-3>',self.rClicker, add='')
            self.yScroll = tk.Scrollbar(self, takefocus=0, orient=tk.VERTICAL)
            self.textbox.configure(yscrollcommand=self.yScroll.set)
            self.yScroll['command'] = self.textbox.yview
            self.yScroll.grid(row=1,column=2, sticky=tk.N+tk.S)
            self.xScroll = tk.Scrollbar(self, takefocus=0, orient=tk.HORIZONTAL)
            self.textbox.configure(xscrollcommand=self.xScroll.set)
            self.xScroll['command'] = self.textbox.xview
            self.xScroll.grid(row=2,column=0, columnspan=2, sticky=tk.E+tk.W)
            self.textbox.grid(row=1,column=0,columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
            self.quitbutton=tk.Button(self, takefocus=0, command=self.quitapp, font=self.font, text = 'Cancel', justify = tk.CENTER)
            self.quitbutton.grid(row=3,column=0,sticky=tk.W)
            self.savebutton=tk.Button(self, takefocus=0, command=self.savecompile, font=self.font, text = 'Save & Create', justify = tk.CENTER)
            self.savebutton.grid(row=3,column=1,sticky=tk.E)

    def quitapp(self):
        if self.errmsg or self.textbox.get('0.0',tk.END) == self.text:
            self.root.destroy()
        elif self.modified or self.textbox.edit_modified():
            res = tkMessageBox.askyesno('Kweb Editor','Do you want to save your changes first?')
            if res:
                self.savecompile()
            else:
                self.root.destroy()
        else:
            self.root.destroy()

    def get_lines(self):
        lidx = []
        selection = self.textbox.tag_nextrange(tk.SEL, '0.0')
        if selection:
            first = selection[0]
            last = selection[1]
            start = int(first.split('.')[0])
            end = int(last.split('.')[0])
            for i in range(start,end+1):
                lidx.append(str(i)+'.0')
        return lidx

    def comment_out(self):
        index = ''
        positions = self.get_lines()
        if positions:
            index = positions[0]
            for p in positions:
                fc = self.textbox.get(p)
                if fc and fc not in '&@\n':
                    self.textbox.insert(p,'&')
            self.textbox.see(index)

    def uncomment(self):
        index = ''
        positions = self.get_lines()
        if positions:
            index = positions[0]
            for p in positions:
                fc = self.textbox.get(p)
                if fc and fc == '&':
                    while self.textbox.get(p) == '&':
                        self.textbox.delete(p)
            self.textbox.see(index)

    def rClicker(self,e):
        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')
            self.textbox.see(tk.INSERT)
        def rClick_Copy(e):
            e.widget.event_generate('<Control-c>')
        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')
            self.textbox.see(tk.INSERT)
        def rClick_Undo(e):
            try:
                self.textbox.edit_undo()
            except:
                pass
        def rClick_Redo(e):
            try:
                self.textbox.edit_redo()
            except:
                pass

        def insert(e,txt,gettext=False):
            if gettext:
                name = tkSimpleDialog.askstring("Enter Title", '')
                if name:
                    txt = txt.replace('Untitled',name)
            tind = self.textbox.index(tk.INSERT)
            if not tind:
                tind = self.textbox.index(tk.END)
            if tind.endswith('.0'):
                if self.textbox.get(tind,tind.replace('.0','.end')):
                    self.textbox.insert(tk.INSERT,txt+'\n')
                else:
                    self.textbox.insert(tk.INSERT,txt)
            else:
                self.textbox.insert('insert lineend ','\n'+txt)
            self.textbox.see(tind)

        e.widget.focus()
        rmenu = tk.Menu(None, tearoff=0, takefocus=0,font=self.font)
        rmenu.add_command(label='Cut', command=lambda e=e: rClick_Cut(e))
        rmenu.add_command(label='Copy', command=lambda e=e: rClick_Copy(e))
        rmenu.add_command(label='Paste', command=lambda e=e: rClick_Paste(e))
        rmenu.add_command(label='Undo', command=lambda e=e: rClick_Undo(e))
        rmenu.add_command(label='Redo', command=lambda e=e: rClick_Redo(e))
        rmenu.add_command(label='Comment Out', command=lambda e=e: self.comment_out())
        rmenu.add_command(label='Uncomment', command=lambda e=e: self.uncomment())
        imenu = tk.Menu(rmenu, tearoff=0, takefocus=0,font=self.font)
        imenu.add_command(label='#!template= (HTML file)', command=lambda e=e: insert(e,'#!template='))
        imenu.add_command(label='#!pagetitle= (Text)', command=lambda e=e: insert(e,'#!pagetitle='))
        imenu.add_command(label='#!css= (CSS file)', command=lambda e=e: insert(e,'#!css='))
        imenu.add_command(label='#!cssinclude', command=lambda e=e: insert(e,'#!cssinclude'))
        imenu.add_command(label='#!forward= (URL)', command=lambda e=e: insert(e,'#!forward='))
        imenu.add_command(label='#!fwtime= (seconds)', command=lambda e=e: insert(e,'#!fwtime='))
        imenu.add_separator()
        imenu.add_command(label='#!mode= [link,button,mixed]', command=lambda e=e: insert(e,'#!mode='))
        imenu.add_command(label='#!spacer=', command=lambda e=e: insert(e,'#!spacer='))
        imenu.add_command(label='#!target= [this,parent,top,blank]', command=lambda e=e: insert(e,'#!target='))
        imenu.add_command(label='#!title= (Text)', command=lambda e=e: insert(e,'#!title='))
        imenu.add_command(label='#!iframew= (px or %)', command=lambda e=e: insert(e,'#!iframew='))
        imenu.add_command(label='#!iframeh= (px or %)', command=lambda e=e: insert(e,'#!iframeh='))
        imenu.add_command(label='#!imgw= (px or %)', command=lambda e=e: insert(e,'#!imgw='))
        imenu.add_command(label='#!imgh= (px or %)', command=lambda e=e: insert(e,'#!imgh='))
        imenu.add_command(label='#!table=...', command=lambda e=e: insert(e,'#!table=1:1:0:0:4:top:center'))
        imenu.add_command(label='#!next', command=lambda e=e: insert(e,'#!next'))
        rmenu.add_cascade(label='Directives',menu=imenu)
        hmenu = tk.Menu(rmenu, tearoff=0, takefocus=0,font=self.font)
        hmenu.add_command(label='Line Break', command=lambda e=e: insert(e,'#<br>'))
        hmenu.add_command(label='Horizontal Line', command=lambda e=e: insert(e,'#<hr>'))
        hmenu.add_command(label='Headline', command=lambda e=e: insert(e,'#<h2>Untitled</h2>',True))
        hmenu.add_command(label='Category (large)', command=lambda e=e: insert(e,'#<h4>Untitled</h4>',True))
        hmenu.add_command(label='Category (smaller)', command=lambda e=e: insert(e,'#<h5>Untitled</h5>',True))
        hmenu.add_command(label='Category (smallest)', command=lambda e=e: insert(e,'#<h6>Untitled</h6>',True))
        hmenu.add_command(label='Bold Text Line', command=lambda e=e: insert(e,'#<br><b>Untitled</b><br>',True))
        hmenu.add_command(label='Small Text Line', command=lambda e=e: insert(e,'#<br><small>Untitled</small><br>',True))
        hmenu.add_command(label='Placeholder', command=lambda e=e: insert(e,'#<!--content-->'))
        rmenu.add_cascade(label='HTML',menu=hmenu)
        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")
        return "break"

    def get_filename(self):
        path = tkFileDialog.asksaveasfilename(parent=self.root,defaultextension='.txt',filetypes=[('Text File', '*.txt')],initialdir=self.fpath,title='Save Text')
        if path and path.endswith('.txt'):
            if path.startswith('/usr/local/share/kweb_about_'):
                about = path.replace('/usr/local/share/kweb_about_','').replace('.txt','')
                if not checkabout(about):
                    return
                self.about = about
            self.fpath = os.path.dirname(path)
            self.fname = os.path.basename(path)

    def savecompile(self):
        txt = self.textbox.get('0.0',tk.END)
        txt = txt.strip()
        succ = True
        if not self.fname:
            self.get_filename()
        if self.fname:
            try:
                f=file(os.path.join(self.fpath,self.fname),'wb')
                f.write(txt.encode('utf-8'))
                f.close()
            except:
                succ = False
            if succ:
                if self.about:
                    try:
                        dummy = subprocess.call(['kwebhelper_set.py','refreshabout',self.about])
                    except:
                        succ = False
                else:
                    try:
                        dummy = subprocess.call(['kwebhelper_set.py','createhtml',os.path.join(self.fpath,self.fname)])
                    except:
                        succ = False
            else:
                res = tkMessageBox.showerror('Kweb Editor','File could not be saved!')
            if succ:
                self.root.destroy()
            else:
                res = tkMessageBox.showerror('Kweb Editor','File could not be converted to HTML!')
        else:
            res = tkMessageBox.showerror('Kweb Editor','File name not selected or allowed!')
            
root = False
if os.geteuid() == 0:
    root = True
homedir = os.path.expanduser('~')
wdir = os.getcwd()
errmsg = ''
msg = ''
fontsize = '12'
fpath = ''
fname = ''
about = ''
text = ''
args = []
for arg in sys.argv:
    if not arg.startswith('-f='):
        args.append(arg)
    else:
        fn = arg.replace('-f=','').strip()
        if fn and fn in ['8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']:
            fontsize = fn

if len(args) == 1:
    if root:
        fpath = '/usr/local/share/kweb'
    else:
        fpath = wdir
    text = get_default_text(fname,about)
    msg = newtext
elif len(args) == 2:
    textpath = args[1]
    if textpath == 'about':
        errmsg = emptyabouterror
    else:
        if not textpath.startswith('/'):
            if root:
                textpath = os.path.join('/usr/local/share/kweb',textpath)
            else:
                textpath = os.path.join(wdir,textpath)
        fpath = os.path.dirname(textpath)
        fname = os.path.basename(textpath)
elif len(args) == 3 and args[1] == 'about':
    if checkabout(args[2]):
        about = args[2]
        textpath = '/usr/local/share/kweb/kweb_about_'+args[2]+'.txt'
        fpath = os.path.dirname(textpath)
        fname = os.path.basename(textpath)
    else:
        errmsg = abouterror
else:
    errmsg = argumenterror
if not checkinstallation():
    errmsg = installationerror
if fpath and fname and not errmsg:
    if not fname.endswith('.txt'):
        errmsg = textfileerror
if fpath and not errmsg:
    if not fpath.startswith(homedir):
        if not root:
            errmsg = rooterror
if fpath and fname and not errmsg:
    msgtxt = edittext
    if os.path.exists(textpath):
        try:
            f = file(textpath,'rb')
            text = f.read().decode('utf-8')
            f.close()
        except:
            errmsg = loaderror
    else:
        msgtxt = newedit
        text = get_default_text(fname,about)
    if about:
        msg = msgtxt.replace('$name$',textpath+ ' (:'+about+')')
    else:
        msg = msgtxt.replace('$name$',textpath)
try:
    root = tk.Tk()
    app = App(master=root,fpath=fpath,fname=fname,text=text,errmsg=errmsg,msg=msg,fontsize=fontsize)                       
    app.mainloop()
except:
    print "This program requires X-Org to run."
    sys.exit(0)
