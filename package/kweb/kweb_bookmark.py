#!/usr/bin/env python
# -*- coding: utf-8 -*-

# kweb bookmark utility
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
import tkMessageBox
import Tkinter as tk

rooterror = '''kweb_bookmark.py must be run as root!

call it with:

gksudo kweb_bookmark.py url [title]'''

argumenterror = '''kweb_bookmark.py needs at least one argument!

call it with:

gksudo kweb_bookmark.py url [title]'''

installationerror = '''No kweb directory or data found!

You need to (re)install kweb to use this utility.'''

urinotvaliderror = '''The URL is not valid.

It must start with either

"http://", "https://" or "file://".'''

fullprompt = '''Do you want to add the following URL to kweb bookmarks?
$uri$

You can edit the name of the bookmark link below:'''

emptyprompt = '''Do you want to add the following URL to kweb bookmarks?
$uri$

You have to enter a name for the bookmark link below:'''

def checkinstallation():
    if os.path.exists('/usr/local/share/kweb/kweb_about_b.txt'):
        return True
    if not os.path.exists('/usr/local/share/kweb'):
        return False
    if not os.path.exists('/usr/local/share/kweb/kweb_about_b.txt'):
        if os.path.exists('/usr/local/bin/kwebhelper_set.py'):
            try:
                dummy = subprocess.call(['kwebhelper_set.py'])
            except:
                return False
        else:
            return False
    if os.path.exists('/usr/local/share/kweb/kweb_about_b.txt'):
        return True
    return False

def checkuri(uri):
        if uri.startswith('http://') or uri.startswith('https://') or uri.startswith('file://'):
            return True
        return False

class App(tk.Frame):              
    def __init__(self, master=None,uri='',name='',errmsg='',msg='',):
        tk.Frame.__init__(self, master)
        self.font = ('SansSerif','12','bold')
        self.root = master
        self.master.title('Minimal Kiosk Browser Bookmark Utility')
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)       
        top.columnconfigure(0, weight=1)
        top.minsize(480,240)
        self.name = tk.StringVar()
        self.name.set(name)
        self.uri = uri
        self.errmsg = errmsg
        self.msg = msg
        self.bmarr = []
        self.count = 0
        if not self.errmsg:
            self.load_bookmarks()
        self.root.protocol('WM_DELETE_WINDOW', self.quitapp)
        self.createWidgets()
        if not self.errmsg:
            self.rowconfigure(3, weight=1)
            self.columnconfigure(0, weight=1)
        if self.bmarr and not self.errmsg:
            self.bmlist.selection_set(self.count-1)
            self.bmlist.see(self.count-1)

    def createWidgets(self):
        if self.errmsg:
            self.mtext = tk.Label(self,text=self.errmsg,font=self.font,width=60)
            self.mtext.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W)
            self.quitbutton=tk.Button(self, takefocus=1, command=self.quitapp, font=self.font, text = 'Quit', justify = tk.CENTER)
            self.quitbutton.grid(row=1,column=0)
        else:
            if len(self.uri) > 60:
                suri = self.uri[0:56]+'...'
            else:
                suri = self.uri
            self.mtext = tk.Label(self,text=self.msg.replace('$uri$',suri),font=self.font,width = 60)
            self.mtext.grid(row=0,column=0,columnspan=2,sticky=tk.E+tk.W)
            self.nameentry = tk.Entry(self,width=60,textvariable=self.name,font=self.font)
            self.nameentry.grid(row=1,column=0,columnspan=2, sticky=tk.E+tk.W)
            self.mtext2 = tk.Label(self,text="Select the position in your bookmark list.\nThe bookmark will be inserted after the selected item.",font=self.font,width=60)
            self.mtext2.grid(row=2,column=0,columnspan=2,sticky=tk.N+tk.S+tk.E+tk.W)
            self.bmlist = tk.Listbox(self, bd=0, relief=tk.FLAT, exportselection=0, takefocus=0, selectmode = tk.SINGLE, width = 60, height = 8, font=self.font,activestyle='none',selectbackground='#000', selectforeground='#ffffd0')
            if self.bmarr:
                for line in self.bmarr:
                    if line:
                        if line[0] in ['&','@']:
                            continue
                        elif line.startswith('#!next'):
                            self.bmlist.insert(tk.END, line)
                            self.count += 1
                        elif line.startswith('#!'):
                            continue
                        elif '=' not in line:
                            continue
                        else:
                            self.bmlist.insert(tk.END, line)
                            self.count += 1
            self.yScroll = tk.Scrollbar(self, takefocus=0, orient=tk.VERTICAL)
            self.bmlist.configure(yscrollcommand=self.yScroll.set)
            self.yScroll['command'] = self.bmlist.yview
            self.yScroll.grid(row=3,column=2, sticky=tk.N+tk.S)
            self.bmlist.grid(row=3,column=0,columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
            self.quitbutton=tk.Button(self, takefocus=0, command=self.quitapp, font=self.font, text = 'Cancel', justify = tk.CENTER)
            self.quitbutton.grid(row=4,column=0,sticky=tk.W)
            self.savebutton=tk.Button(self, takefocus=0, command=self.savebm, font=self.font, text = 'Save', justify = tk.CENTER)
            self.savebutton.grid(row=4,column=1,sticky=tk.E)

    def quitapp(self):
        self.root.destroy()

    def load_bookmarks(self):
        f = file('/usr/local/share/kweb/kweb_about_b.txt','rb')
        bmtext = f.read().decode('utf-8').strip('\n')
        f.close()
        self.bmarr = bmtext.split('\n')

    def save_bookmark(self,uri,name):
        newbmark = name+'='+uri
        sel = self.bmlist.curselection()
        if not sel:
            self.bmarr.append(newbmark)
        elif sel[0] == self.count -1:
            self.bmarr.append(newbmark)
        else:
            txt = self.bmlist.get(sel[0])
            self.bmarr.insert(self.bmarr.index(txt)+1,newbmark)
        bmtext = '\n'.join(self.bmarr)
        f = file('/usr/local/share/kweb/kweb_about_b.txt','wb')
        f.write(bmtext.encode('utf-8'))
        f.close()
        try:
            dummy = subprocess.call(['kwebhelper_set.py','refreshabout','b'])
        except:
            return False
        if dummy != 0:
            return False
        return True

    def savebm(self):
        name = self.name.get()
        if not name:
            res = tkMessageBox.showerror('Bookmarker','You must enter a name first!')
            return
        res = self.save_bookmark(self.uri,name.strip())
        if not res:
            res = tkMessageBox.showerror('Bookmarker','UUPS, something went wrong!')
        self.quitapp()

uri = ''
name = ''
errmsg = ''
msg = ''
if os.geteuid() != 0:
    errmsg = rooterror
if not errmsg:
    if not checkinstallation():
        errmsg = installationerror
if not errmsg:
    if len(sys.argv) < 2:
        errmsg = argumenterror
if not errmsg:
    uri=sys.argv[1].decode('utf-8')
    if not checkuri(uri):
        errmsg = urinotvaliderror
if not errmsg:
    if len(sys.argv) > 2:
        name = sys.argv[2].decode('utf-8')
        msg = fullprompt
    else:
        msg = emptyprompt
try:
    root = tk.Tk()
    app = App(master=root,uri=uri,name=name,errmsg=errmsg,msg=msg)                       
    app.mainloop()
except:
    print "This program requires X-Org to run."
    sys.exit(0)
