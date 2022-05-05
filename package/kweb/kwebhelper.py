#!/usr/bin/env python
# -*- coding: utf-8 -*-

# helper script for kweb Minimal Kiosk Browser
# Copyright 2013-2016 by Guenter Kreidl
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import os,urllib,sys,shutil

version = '1.7.0'
software_path = 'http://steinerdatenbank.de/software/'
config_path = ''
scdir = os.path.expanduser('~')

# GLOBAL OPTIONS
settings = '/usr/local/bin/kwebhelper_settings.py'
dldir = ''

# PDF OPTIONS
pdfprog = ''
pdfoptions = []
pdfpathreplacements = {}

# DOWNLOAD OPTIONS
show_download_in_terminal = True
wget_options = ["--no-check-certificate","--no-clobber","--adjust-extension","--content-disposition"]
use_uget = True
uget_options = ['--quiet']

#COMMAND EXECUTION OPTIONS
check_desktop = True
direct_commands = ['kwebhelper.py','omxplayergui','kwebhelper_set.py','omxplayer','gksudo','xterm','screen']
preferred_terminal = 'lxterminal'
sudo_requires_password = True
run_as_script = False

### end of global settings

class internalcommands():
    def __init__(self,url,config_path):
        self.settings = {'proc':'','gopts':'','copts':'','sopts':'','kopts':'','url':''}
        self.gopts = 'ZJEWYITSXAHLGVMKNRPBFOQ'
        self.copts = 'UD'
        self.sopts = '0123456789'
        self.kopts = '+-zbhrqfpoklgtjneduwxyavcsmi#?!.,'
        self.config_path = config_path
        self.homedir = os.path.expanduser('~')
        self.upgradescript = '''#!/bin/bash
echo "New version §version§ is available"
read -n 1 -p "Do you want to install it? (y)" KWEBINSTALL
if [ "$KWEBINSTALL" == "y" ]; then
echo
cd ''
wget --no-clobber §url§kweb-§version§.tar.gz
tar -xzf kweb-§version§.tar.gz
cd kweb-§version§
echo "installing ..."
./debinstall
echo
echo "If no errors were reported kweb version §version§ has been successfully installed"
read -n 1 -p "Delete all downloaded files? (y)" ANSWER
if [ "$ANSWER" == "y" ]; then
rm *
cd ../
rmdir kweb-§version§
rm kweb-§version§.tar.gz
fi
else
echo "Nothing was installed"
fi
echo
rm §scdir§/upgradekweb.sh
'''
        self.messagescript = '''#!/bin/bash
echo
read -t 10 -n 1 -p "§msg§"
rm §scdir§/kwebmessage.sh
'''
        self.eval_url(url)

    def eval_url(self,url):
        cmd = urllib.unquote_plus(url.split('formdataintern&')[1])
        if cmd:
            cmdl = cmd.split('&')
            for cm in cmdl:
                cml = cm.split('=',1)
                if len(cml) == 2:
                    cm1 = cml[0].strip()
                    cm2 = cml[1].strip()
                    if cm1 in self.settings.keys():
                        if cm2 not in self.settings[cm1]:
                            self.settings[cm1] += cm2

    def execute(self):
        if self.settings['proc']:
            proc = self.settings['proc']
            if proc == 'update':
                if not self.get_config():
                    self.settings['kopts'] = self.kopts
                self.update_page()
            elif proc == 'delete':
                if os.path.exists(self.homedir+'/.kweb.conf'):
                    os.remove(self.homedir+'/.kweb.conf')
                self.settings['kopts'] = self.kopts
                self.update_page()
            elif proc == 'set':
                self.save_config()
                self.update_page()
            elif proc == 'upgrade':
                escript = ''
                scpath = scdir+'/kwebmessage.sh'
                newversion =self.getversion()
                if newversion:
                    if newversion == version:
                        msg = 'Your version '+version+' is up to date'
                        escript = self.messagescript.replace('§msg§', msg).replace('§scdir§',scdir)
                    else:
                        scpath = scdir+'/kwebupgrade.sh'
                        escript = self.upgradescript.replace('§version§',newversion).replace('§scdir§',scdir).replace('§url§',software_path)
                else:
                    escript = self.messagescript.replace('§msg§','Could not connect to server').replace('§scdir§',scdir)
                if escript:
                    f = file(scpath,'wb')
                    f.write(escript.encode('utf-8'))
                    f.close()
                    os.chmod(scpath, 511)
                    os.execlp(preferred_terminal,preferred_terminal,'-e',scpath)

    def getversion(self):
        res = ''
        try:
            fn,h = urllib.urlretrieve(software_path+'kweb_version_jessie.txt')
            if os.path.exists(fn):
                f = file(fn,'ra')
                res = f.read()
                f.close()
        except:
            pass
        if len(res) > 12:
            res = ''
        return res.strip()

    def get_config(self):
        if os.path.exists(self.homedir+'/.kweb.conf'):
            f = file(self.homedir+'/.kweb.conf','rb')
            conf = f.read()
            f.close()
            confl = conf.split('\n')
            if len(confl[0]) > 1 and confl[0].startswith('-'):
                for ch in confl[0][1:len(confl[0])]:
                    if ch in self.gopts:
                       self.settings['gopts'] += ch 
                    elif ch in self.copts:
                       self.settings['copts'] += ch 
                    elif ch in self.sopts:
                       self.settings['sopts'] += ch 
                    elif ch in self.kopts:
                       self.settings['kopts'] += ch
            if len(confl) > 1 and confl[1]:
                self.settings['url'] = confl[1].strip()
            return True
        return False

    def save_config(self):
        opts = '-' + self.settings['gopts']
        if len(self.settings['copts']) > 1:
            opts += self.settings['copts'][-1]
        else:
            opts += self.settings['copts']
        if len(self.settings['sopts']) > 1:
            opts += self.settings['sopts'][-1]
        else:
            opts += self.settings['sopts']
        opts += self.settings['kopts']
        opts += '\n' + self.settings['url']
        if opts in ['-\n','-'+self.kopts+'\n']:
            opts = ''
        if opts:
            if opts.startswith('-\n'):
                opts = opts[1:len(opts)]
            f = file(self.homedir+'/.kweb.conf','wb')
            f.write(opts)
            f.close()
        else:
            if os.path.exists(self.homedir+'/.kweb.conf'):
                os.remove(homedir+'/.kweb.conf')

    def update_page(self):
        if not os.path.exists(self.config_path):
            try:
                shutil.copy('/usr/local/share/kweb/kweb_about_c.html',self.config_path)
            except:
                pass
        if os.path.exists(self.config_path):
            f = file(self.config_path,'rb')
            page = f.read().decode('utf-8')
            f.close()
            pagel = page.split('<!--splitter-->')
            gopts = pagel[1].replace(' checked','')
            for ch in self.settings['gopts']:
                gopts = gopts.replace('value="'+ch+'"','value="'+ch+'" checked')
            pagel[1] = gopts
            copts = pagel[2].replace(' checked','')
            if not self.settings['copts']:
                nopt = ''
            elif len(self.settings['copts']) > 1:
                nopt = self.settings['copts'][-1]
            else:
                nopt = self.settings['copts']
            copts = copts.replace('value="'+nopt+'"','value="'+nopt+'" checked')
            pagel[2] = copts
            sopts = pagel[3].replace(' checked','')
            if not self.settings['sopts']:
                nopt = ''
            elif len(self.settings['sopts']) > 1:
                nopt = self.settings['sopts'][-1]
            else:
                nopt = self.settings['sopts']
            sopts = sopts.replace('value="'+nopt+'"','value="'+nopt+'" checked')
            pagel[3] = sopts
            kopts = pagel[4].split('value="')[0]
            kopts += 'value="'+self.settings['kopts']+'">'
            pagel[4] = kopts
            uri = pagel[5].split('value="')[0]
            uri += 'value="'+self.settings['url']+'">'
            pagel[5] = uri
            newpage = '<!--splitter-->'.join(pagel)
            f = file(self.config_path,'wb')
            f.write(newpage.encode('utf-8'))
            f.close()

def scan_cmd(cmdline):
    # must be utf-8 decoded!
    quoter = ''
    newcmd = ''
    carr = []
    for c in cmdline.strip():
        if not quoter:
            if c in ['"',"'"]:
                quoter = c
            elif c == ' 'and newcmd:
                carr.append(newcmd.encode('utf-8'))
                newcmd = ''
            else:
                newcmd += c
        else:
            if c == quoter:
                quoter = ''
            else:
                newcmd += c
    if newcmd:
        carr.append(newcmd.encode('utf-8'))
    return carr

# main script function

def run(args):
    # arg0 = ignore, arg1 = mode, arg2 = URL
    # possible modes = 'pdf','dl','dlw','dlu', 'dlp', 'cmd'
    if len(args) > 2:
        mode = args[1]
        url = args[2]

    # pdf section (download - if needed - and open pdf file)
        if mode == 'pdf':
            global pdfprog
            if not pdfprog:
                if os.path.exists('/usr/bin/evince'):
                    pdfprog = 'evince'
                elif os.path.exists('/usr/bin/xpdf'):
                    pdfprog = 'xpdf'
                else:
                    pdfprog = 'mupdf'
            go = False
            # option to open pdf as local file copies instead of downloading them first
            if pdfpathreplacements:
                for k,v in pdfpathreplacements.iteritems():
                    if url.startswith(k):
                        nurl = url.replace(k,v)
                        if os.path.exists(urllib.unquote(nurl.replace('file://','').replace('%20',' ').split('#')[0])):
                            url = nurl
                        break
            if url.startswith('file://'):
                url = url.replace('file://','').replace('%20',' ')
                url = urllib.unquote(url)
                urll = url.split('#page=')
                f = urll[0]
                if os.path.exists(f):
                    if len(urll) > 1:
                        page = urll[1].split('&')[0]
                        if pdfprog in ['evince','evince-gtk']:
                            os.execvp(pdfprog,[pdfprog]+pdfoptions+['-i',page,f])
                        else:
                            os.execvp(pdfprog,[pdfprog]+pdfoptions+[f,page])
                    else:
                        os.execvp(pdfprog,[pdfprog]+pdfoptions+[f])
            else:
                lower = url.lower()
                if lower.endswith('.pdf') or '.pdf#page' in lower:
                    urll = url.split('#page=')
                    f = dldir+os.sep+urllib.unquote(urll[0].split('/')[-1].replace('%20',' '))
                    if os.path.exists(f):
                        go = True
                    else:
                        try:
                            fn,h = urllib.urlretrieve(urll[0],f)
                            go = True
                        except:
                            pass
                if go:
                    if len(urll) > 1:
                        page = urll[1].split('&')[0]
                        if pdfprog in ['evince','evince-gtk']:
                            os.execvp(pdfprog,[pdfprog]+pdfoptions+['-i',page,f])
                        else:
                            os.execvp(pdfprog,[pdfprog]+pdfoptions+[f,page])
                    else:
                        os.execvp(pdfprog,[pdfprog]+pdfoptions+[f])

    # end of pdf section

    # download section
        elif mode in ['dl','dlw','dlu','dlp'] and not url.startswith('file://'):
            # download page or file using uget or wget
            addargs = []
            if mode == 'dlp':
                if "-p" not in wget_options and "--page-requisites" not in wget_options:
                    addargs.append("-p")
                if "-k" not in wget_options and "--convert-links" not in wget_options:
                    addargs.append("-k")
            if mode == 'dlu' and os.path.exists('/usr/bin/uget-gtk'):
                pargs = ["uget-gtk",'--http-cookie-file='+homedir + "/.web_cookie_jar",'--folder='+dldir]+uget_options+[url]
                os.execvp("uget-gtk",pargs)
            else:
                if show_download_in_terminal:
                    pargs = [preferred_terminal,'-e', "wget", "--directory-prefix="+dldir,"--load-cookies="+homedir + "/.web_cookie_jar"]+wget_options+addargs+[url]
                    os.execvp(preferred_terminal,pargs)
                else:
                    pargs = ["wget", "--directory-prefix="+dldir,"--load-cookies="+homedir + "/.web_cookie_jar"]+wget_options+addargs+[url]
                    os.execvp("wget",pargs)

    #end of download section

    # command execution section
        elif mode == 'cmd':
            cmd = ''
            cmdarray = []
            terminal_required = False
            cpage = 'file:///homepage.html?cmd='
            url = url.decode('utf-8')
            if url.startswith('#'):
                cmd = url[1:]
            elif url.startswith(cpage):
                cmd = url.replace(cpage,'')
                if not cmd.startswith('formdata'):
                    cmd = urllib.unquote_plus(cmd).replace('%20',' ')
            elif url.startswith('http://localhost') and ('/homepage.html?cmd=' in url):
                cmd = url.split('/homepage.html?cmd=')[1]
                if not cmd.startswith('formdata'):
                    cmd = urllib.unquote_plus(cmd).replace('%20',' ')
            if cmd:
                if cmd.startswith('formdataintern'):
                    icmd = internalcommands(url,config_path)
                    icmd.execute()
                else:
                    if cmd.startswith('formdata'):
                        cmd = cmd.split('formdata')[1].strip()
                        if '&' in cmd:
                            cmdargs = cmd.split('&')
                            for ind in range(0,len(cmdargs)):
                                if '=' in cmdargs[ind]:
                                    cargl = cmdargs[ind].split('=')
                                    if cargl[0].startswith('quoted') and cargl[1] != '':
                                        cmdargs[ind] = (" '" + urllib.unquote_plus(cargl[1]) + "'").replace('\n','%0D').replace('\r','%0A')
                                    elif cargl[0].startswith('dquoted') and cargl[1] != '':
                                        cmdargs[ind] = (' "' + urllib.unquote_plus(cargl[1]) + '"').replace('\n','%0D').replace('\r','%0A')
                                    elif cargl[1] != '':
                                        cmdargs[ind] = ' ' + urllib.unquote_plus(cargl[1])
                                    else:
                                        cmdargs[ind] = ''
                                else:
                                    cmdargs[ind] = ' ' + urllib.unquote_plus(cmdargs[ind]).strip()
                            cmd = ''.join(cmdargs).strip()
                        else:
                            cmd = urllib.unquote_plus(cmd).strip()
                    cmdarray = scan_cmd(cmd)
                    cmdline = cmd.encode('utf-8')
                    if len(cmdarray)>1 and cmdarray[0] in ['sudo']:
                        realname = cmdarray[1]
                        if os.geteuid() != 0:
                            terminal_required = sudo_requires_password
                    else:
                        realname = cmdarray[0]
                    desktop_app = False
                    if not realname in direct_commands:
                        if check_desktop and '/' not in realname:
                            if os.path.exists('/usr/share/applications/'+realname+'.desktop'):
                                desktop_app = True
                    if not (desktop_app or realname in direct_commands):
                        terminal_required = True
                    if terminal_required:
                        cmdarray = [preferred_terminal,'-e'] + cmdarray
                        if not run_as_script:
                            cmdline = preferred_terminal + ' -e '+cmdline
                    if run_as_script:
                        dmcount = 0
                        scpath = scdir+os.sep+'temp'+str(dmcount)+'.sh'
                        while os.path.exists(scpath):
                            dmcount += 1
                            scpath = scdir+os.sep+'temp'+str(dmcount)+'.sh'
                        f = file(scpath,'wb')
                        f.write('#!/bin/bash\n'+cmdline+'\nrm '+scpath+'\n')
                        f.close()
                        os.chmod(scpath,511)
                        if terminal_required:
                            try:
                                os.execlp(preferred_terminal,preferred_terminal,'-e',scpath)
                            except:
                                pass
                        else:
                            try:
                                os.execl(scpath,scpath)
                            except:
                                pass
                    else:
                        try:
                            os.execvp(cmdarray[0],cmdarray)
                        except:
                            try:
                                dummy = os.system(cmdline)
                            except:
                                pass                    
    # end of command execution section

if __name__ == '__main__':
    # take settings from separate file:
    if settings:
        try:
            execfile(settings)
        except:
            pass
    homedir = os.path.expanduser('~')
    if not config_path:
        config_path = homedir + '/kweb_about_c.html'
    if not dldir:
        dldir = homedir +'/Downloads'
    if not os.path.exists(dldir):
        os.mkdir(dldir)
    if dldir.startswith(homedir):
        scdir = dldir
    args = sys.argv
    run(args)
