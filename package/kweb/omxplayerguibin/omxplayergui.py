#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GUI for omxplayer
# as helper for Minimal Kiosk Browser
# or for standalone use
# Copyright 2013-2016 by Guenter Kreidl
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# version 1.7.0

import os,urllib,urllib2,sys,subprocess,threading,time,tkFileDialog,tkMessageBox,copy
import Tkinter as tk

# GLOBAL OPTIONS
settings = '/usr/local/bin/kwebhelper_settings.py'
scdir = os.path.expanduser('~')
preferred_terminal = 'lxterminal'
pdfprog = ''

# OMXPLAYER AUDIO VIDEO OPTIONS
omxoptions = []
omxaudiooptions = []
omx_livetv_options = ['--live']
live_tv = []
mimetypes = []
omxplayer_in_terminal_for_video = True
omxplayer_in_terminal_for_audio = True
audioextensions = ['mp3','aac','flac','wav','wma','cda','ogg','ogm','ac3','ape']
streammode = 'video'
videoextensions = ['asf','avi','mpg','mp4','mpeg','m2v','m1v','vob','divx','xvid','mov','m4v','m2p','mkv','m2ts','ts','mts','wmv','webm','flv']
useAudioplayer = True
useVideoplayer = True
defaultaudiovolume = 0
autoplay = True
autofinish = True
fontname = 'SansSerif'
fontheight = 12
maxlines = 8
lwidth = 40
videoheight = 288
screenmode = 'min'
videomode = '16:9'
freeze_window = False
get_DAR = False
hide_controls = False
useVLC = False 

# ONLINE VIDEO OPTIONS
preferred_html5_video_format = '.mp4'
html5_first = True
youtube_dl_options = ['-f','best']
youtube_omxoptions = []

## new
use_ytdl_server = True
ytdl_server_port = '9192'
ytdl_server_host = 'localhost'
ytdl_server_format = 'best'

### end of global settings

standalone = {'basedir':'','url':'','playlist':[],'open_settings':False,'root':None,'wcount':0}

# helper functions

def checkextensions(pl,extl):
    aonly = True
    for p in pl:
        if p.lower().split('.')[-1] not in extl:
            aonly = False
            break
    return aonly

def uriretrieve(uri):
    if not uri:
        return (False, '')
    if uri.startswith(os.sep):
        try:
            if os.path.exists(uri):
                f = file(uri,'rb')
                content = f.read()
                f.close()
                return (True, content)
            else:
                return (False, '')
        except:
            return (False, '')
    else:
        try:
            inp = urllib2.urlopen(uri)
            content = inp.read()
            if content:
                return (True, content)
            else:
                return (False, '')
        except:
            return (False, '')

def check_server():
    (flag, cont) = uriretrieve('http://'+ytdl_server_host+':'+ytdl_server_port+'/running')
    if flag and cont == 'OK':
        return True
    else:
        return False

def start_server():
    svr = None
    try:
        svr = subprocess.Popen(['ytdl_server.py','-p='+ytdl_server_port,'-f='+ytdl_server_format],stdin=subprocess.PIPE,stdout=file('/dev/null','wa'),stderr=file('/dev/null','wa'))
    except:
        pass
    return svr

def stop_server():
    (flag, cont) = uriretrieve('http://'+ytdl_server_host+':'+ytdl_server_port+'/stop')
    
def get_terminal():
    if os.path.exists('/usr/bin/xterm'):
        return 'xterm'
    else:
        return preferred_terminal

def get_opt(options):
    if '--win' in options:
        pos = options.index('--win')
        if pos < (len(options) -2):
            options[pos+1] = '"' + options[pos+1] + '"'
    return ' '.join(options)

def get_playlist(url,streammode,mimetype):
    playlist = []
    names = []
    audioonly = True
    go,pl = uriretrieve(url)
    if go and pl:
        pll = pl.split('\n')
        if url.lower().endswith('.m3u') or url.lower().endswith('.m3u8') or mimetype in  ['audio/mpegurl','audio/x-mpegurl','audio/m3u']:
            for s in pll:
                s = s.strip()
                if s != '' and not s.startswith('#'):
                    if s.split('.')[-1].lower() in audioextensions:
                        pass
                    elif streammode == 'audio' and s.split('.')[-1].lower() not in videoextensions:
                        pass
                    else:
                        audioonly = False
                    playlist.append(s)
                elif s.startswith('#EXTINF:'):
                    names.append(s.replace('#EXTINF:',''))
        elif url.lower().endswith('.pls') or mimetype in ['audio/x-scpls','audio/pls']:
            for s in pll:
                if s.startswith('File'):
                    aurl = s.split('=')[1].strip()
                    playlist.append(aurl)
                elif s.startswith('Title'):
                    name = s.split('=')[1].strip()
                    names.append(name)
        if names and len(names) != len(playlist):
            names = []
    return (audioonly, playlist, names)

def video_tag_extractor(url):
    result = []
    go,html = uriretrieve(url)
    if go and html and '<video ' in html:
        htl = html.split('<video')
        for ind in range(1,len(htl)):
            vtag = htl[ind].split('</video>')[0]
            if not 'src="' in vtag:
                continue
            vtl = vtag.split('src="')
            if len(vtl) > 2:
                links = []
                for l in vtl[1:]:
                    pos = l.find('"')
                    links.append(l[0:pos])
                link = links[0]
                for li in links:
                    if preferred_html5_video_format and li.lower().endswith(preferred_html5_video_format):
                        link = li
            else:
                vt = vtl[1]
                pos = vt.find('"')
                link = vt[0:pos]
            if link.startswith('http://')  or link.startswith('https://') or link.startswith('rtsp://') or link.startswith('rtmp://'):
                result.append(link)
            elif link.startswith('file://'):
                newlink = link.replace('file://','').replace('%20',' ')
                result.append(newlink)
            else:
                urll = url.split('/')
                if link.startswith('/'):
                    newlink = '/'.join(urll[0:3]+[link[1:]])
                else:
                    relcount = len(urll) - 1 - link.count('../')
                    newlink = '/'.join(urll[0:relcount]+[link.replace('../','')])
                if newlink.startswith('file://'):
                    newlink = newlink.replace('file://','').replace('%20',' ')
                result.append(newlink)
    return result

def play_ytdl(res):
    vlist = res.split('\n')
    playlist = []
    names = []
    for v in vlist:
        if v:
            if '://' in v:
                playlist.append(v)
            else:
                names.append(v)
    if len(playlist) != len(names):
        names = []
    if playlist:
        if useVideoplayer:
            if not standalone['root']:
                root = tk.Tk()
            else:
                root = tk.Toplevel(standalone['root'])

            standalone['wcount'] += 1
            player = omxplayergui(master=root, playlist=playlist,volume=defaultaudiovolume,omxaudiooptions=omxaudiooptions,
                                    omxvideooptions=youtube_omxoptions,mode='AV',streammode=streammode,vmode=videomode,vminheight=videoheight,
                                    autofinish=autofinish,fontheight=fontheight,fontname=fontname,screenmode=screenmode,
                                    autoplay=autoplay,audioextensions=audioextensions, get_DAR = get_DAR, hide_controls = hide_controls,
                                    videoextensions=videoextensions, freeze=freeze_window, namelist=names, standalone=standalone)
            if not standalone['root']:
                player.mainloop()
        else:
            terminal = get_terminal()
            if len(playlist) == 1:
                vurl = playlist[0]
                if not omxplayer_in_terminal_for_video:
                    pargs = ["omxplayer"] + youtube_omxoptions+[vurl]+['>', '/dev/null', '2>&1']
                elif terminal == 'xterm':
                    pargs = ["xterm","-fn","fixed","-fullscreen", "-maximized", "-bg", "black", "-fg", "black", "-e",'omxplayer']+youtube_omxoptions+[vurl]+['>', '/dev/null', '2>&1']
                else:
                    pargs = [terminal,"-e",'omxplayer']+youtube_omxoptions+[vurl]+['>', '/dev/null', '2>&1']
                dummy = subprocess.call(pargs)
            else:
                script = '#!/bin/bash\n'
                for vurl in playlist:
                    script += 'omxplayer ' + get_opt(youtube_omxoptions) + ' "' + vurl + '" > /dev/null 2>&1\n'
                script += 'rm ' + scdir+os.sep+'playall.sh\n'
                f = file(scdir+os.sep+'playall.sh','wb')
                f.write(script)
                f.close()
                os.chmod(scdir+os.sep+'playall.sh',511)
                if not omxplayer_in_terminal_for_video:
                    pargs = [scdir+os.sep+'playall.sh','>', '/dev/null', '2>&1']
                elif terminal == 'xterm':
                    pargs = ["xterm","-fn","fixed","-fullscreen", "-maximized", "-bg", "black", "-fg", "black", "-e",scdir+os.sep+'playall.sh']
                else:
                    pargs = [terminal,"-e",scdir+os.sep+'playall.sh']
                dummy = subprocess.call(pargs)

def play_html5(tags):
    if useVideoplayer:
        if not standalone['root']:
            root = tk.Tk()
        else:
            root = tk.Toplevel(standalone['root'])

        standalone['wcount'] += 1
        player = omxplayergui(master=root, playlist=tags,volume=defaultaudiovolume,omxaudiooptions=omxaudiooptions,
                                omxvideooptions=youtube_omxoptions,mode='AV',streammode=streammode,vmode=videomode,vminheight=videoheight,
                                autofinish=autofinish,fontheight=fontheight,fontname=fontname,screenmode=screenmode,
                                autoplay=autoplay,audioextensions=audioextensions, get_DAR = get_DAR, hide_controls = hide_controls,
                                videoextensions=videoextensions, freeze=freeze_window, namelist=[], standalone=standalone)
        if not standalone['root']:
            player.mainloop()
    else:
        terminal = get_terminal()
        if len(tags) == 1:
            if not omxplayer_in_terminal_for_video:
                pargs = ["omxplayer"] + youtube_omxoptions+[tags[0]]+['>', '/dev/null', '2>&1']
            elif terminal == 'xterm':
                pargs = ["xterm","-fn","fixed","-fullscreen", "-maximized", "-bg", "black", "-fg", "black", "-e",'omxplayer']+youtube_omxoptions+[tags[0]]+['>', '/dev/null', '2>&1']
            else:
                pargs = [terminal,"-e",'omxplayer']+youtube_omxoptions+[tags[0]]+['>', '/dev/null', '2>&1']
            dummy = subprocess.call(pargs)
        else:
            script = '#!/bin/bash\n'
            for t in tags:
                script += 'omxplayer ' + get_opt(youtube_omxoptions) + ' ' + t + ' > /dev/null 2>&1\n'
            script += 'rm ' + scdir+os.sep+'playall.sh\n'
            f = file(scdir+os.sep+'playall.sh','wb')
            f.write(script)
            f.close()
            os.chmod(scdir+os.sep+'playall.sh',511)
            if not omxplayer_in_terminal_for_video:
                pargs = [scdir+os.sep+'playall.sh','>', '/dev/null', '2>&1']
            elif terminal == 'xterm':
                pargs = ["xterm","-fn","fixed","-fullscreen", "-maximized", "-bg", "black", "-fg", "black", "-e",scdir+os.sep+'playall.sh']
            else:
                pargs = [terminal,"-e",scdir+os.sep+'playall.sh']
            dummy = subprocess.call(pargs)

# omxplayerGUI

class omxplayergui(tk.Frame):

    def __init__(self, master=None, playlist=[],mode='audio',autofinish=True,autoplay=True,volume=0,
                 omxaudiooptions=[],omxvideooptions=[],vminheight=288,vmode='full',streammode='video',screenmode='min',
                 audioextensions = [], videoextensions = [],freeze=True, namelist=[],
                 fontheight=14,fontname='SansSerif',maxlines=8,width=40, get_DAR = False, hide_controls = False, standalone={'wcount':0}):
        tk.Frame.__init__(self, master)
        self.mode = mode
        self.standalone = standalone
        self.set_defaults()
        self.frozen = ''
        self.root = master
        self.fontheight = min([max([fontheight,10]),22])
        self.fontname = fontname
        try:
            self.font = (self.fontname,str(self.fontheight),'bold')
        except:
            self.font = ('SansSerif',str(self.fontheight),'bold')
        self.maxlines = min([max([maxlines,5]),25])
        self.defaultwidth = min([max([width,40]),80])
        self.omxaudiooptions = self.filteroptions(omxaudiooptions)
        self.omxvideooptions = self.filteroptions(omxvideooptions)
        self.autofinish = autofinish
        self.dbuscontrol = not freeze
        self.playlist = playlist
        self.namelist = namelist
        self.autoplay = autoplay
        self.get_DAR = get_DAR
        self.audioextensions = audioextensions
        self.videoextensions = videoextensions
        self.scalefactor = 1.0
        self.videomode = tk.StringVar()
        if vmode in self.videomodes:
            self.videomode.set(vmode)
        elif self.checkvideomode(vmode):
            self.videomodes.append(vmode)
            self.videomode.set(vmode)
        else:
            self.videomode.set('full')
        dummy = self.videomode.trace('w',self.trace_videomode)
        self.streammode = tk.StringVar()
        if streammode in self.streammodes:
            self.streammode.set(streammode)
        else:
            self.streammode.set('video')
        self.vminheight = min(max((vminheight,288,self.fontheight*28)),self.root.winfo_screenheight()-self.fontheight*10)
        self.vminwidth = self.getwidth(self.vminheight,self.videomode.get())

        self.screenmodes = ['Lines:','min']
        self.screenmode = tk.StringVar()
        for sm in [320,384,432,480,512,576,720,800,900]:
            if sm > self.vminheight and sm < self.root.winfo_screenheight()-self.fontheight*10:
                self.screenmodes.append(str(sm))
        self.screenmodes = self.screenmodes + ['max','full']
        if screenmode in ['min','max','full']:
            self.screenmode.set(screenmode)
        else:
            self.screenmode.set('min')
        dummy = self.screenmode.trace('w',self.trace_screenmode)
        self.status = 'stopped'
        self.omxprocess = None
        self.omxwatcher = None
        self.durwatcher = None
        self.songpointer = 0
        self.listpointer = 0
        self.currentmode = 'audio'
        self.resize = True
        self.visible = True
        self.layer = 0
        self.seekable = True
        self.controls_hidden = hide_controls
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.root.bind("<<finished>>",self.on_finished)
        self.root.bind("<Unmap>",self.check_visible,'+')
        self.root.bind("<Configure>",self.check_window,'+')
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.screenwidth = self.root.winfo_screenwidth()
        self.set_title()
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)        
        for keysym in self.keybindings:
            self.root.bind(keysym,self.keyp_handler)
        self.volume_after = None
        self.volume_after_running = False
        self.currentvolume = min([max([volume,-20]),4])*3
        self.changedvolume = tk.IntVar()
        self.changedvolume.set(self.currentvolume)
        self.playcontent = tk.StringVar()
        self.playcontent.set(self.playstring)
        self.seekposition = tk.DoubleVar()
        self.seekposition.set(0)
        self.seek_after = None
        self.resize_after = None
        self.video_duration = 0
        self.dbus_dest = 'org.mpris.MediaPlayer2.omxplayer' + str(int(time.time()*10))
        self.yScroll = None
        self.createwidgets()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(6, weight=1)
        if self.controls_hidden and self.mode == 'AV':
            self.hide_control()
        dummy = self.after(200, self.on_activate_first)
        self.root.update_idletasks()

    def set_defaults(self):
        self.playstring = '>'
        self.pausestring = '||'
        self.stopstring = '[]'
        self.rewstring = '←'
        self.fwdstring = '→'
        self.prevstring = '↑'
        self.nextstring = '↓'
        self.vchdelay = 0.05
        self.videomodes = ['Mode:','full','refresh','auto','4:3','16:9','16:10','2.21:1','2.35:1','2.39:1']
        self.streammodes = ['Stream:','audio','video']
        self.keybindings = ['<KeyPress>','<Alt-KeyPress>']

    def set_title(self):
        if self.mode == 'audio':
            flags = ''
            if not self.dbuscontrol:
                flags += 'f'
            if flags:
                flags = ' (' + flags + ')'
            self.root.title("omxaudioplayer"+flags)
        else:
            flags = ''
            if not self.dbuscontrol or not self.seekable:
                flags += 'f'
            if self.get_DAR:
                flags += 'a'
            if self.layer > 0:
                flags += str(self.layer)
            if flags:
                flags = ' (' + flags + ')'
            self.root.title("omxplayerGUI"+flags)        

    def get_scalefactor(self,url):
        self.scalefactor = 1.0
        res = ''
        try:
            db = subprocess.Popen(['omxplayer','-i',url],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            (res,err) = db.communicate()
        except:
            res = ''
        if res and 'DAR' in res:
            pos1 = res.find('DAR')
            pos2 = res.find(']',pos1)
            dar = res[pos1+4:pos2]
            if ':' in dar:
                darl = dar.split(':')
                if len(darl) == 2:
                    try:
                        width = float(darl[0])
                    except:
                        width = None
                    try:
                        height = float(darl[1])
                    except:
                        height = None
                    if width and height:
                        self.scalefactor = width / height

    def get_duration(self):
        dur = 0
        canseek = ''
        url = self.playlist[self.songpointer]
        if self.dbuscontrol:
            count = 0
            while self.omxprocess and count < 9:
                if dur == 0:
                    res = self.send_dbus(['duration'])
                    if res:
                        try:
                            dur = int(res.strip())
                        except:
                            pass
                if not canseek:
                    res = self.send_dbus(['canseek'])
                    if res and res.strip() in ['true','false']:
                            canseek = res.strip()
                if self.scalefactor == 1.0:
                    res = self.send_dbus(['aspect'])
                    if res:
                        try:
                            self.scalefactor = float(res.strip())
                        except:
                            pass
                if dur != 0 and canseek:
                    break
                count += 1
                time.sleep(2)
            if self.omxprocess and dur != 0 and canseek == 'true':
                try:
                    scdur = (dur/30000000)/2.0
                    self.seekbar['to'] = scdur
                    self.seekbar['state'] = tk.NORMAL
                    self.seekable = True
                    self.root.resizable(True, True)
                    self.frozen = ''
                    self.resize = True
                    self.vmodeoption['state'] = tk.NORMAL
                    self.lmodeoption['state'] = tk.NORMAL
                    self.set_title()
                except:
                    pass
        self.video_duration = dur
        if self.dbuscontrol and self.omxprocess and self.get_DAR and self.scalefactor == 1.0 and self.videomode.get() not in ['auto','full','refresh']:
            self.get_scalefactor(url)
        try:
            self.reset_pnbuttons()
        except:
            pass

    def goto_pos(self):
        self.seek_after = None
        newpos = int(self.seekposition.get()*60000000)           
        if newpos < self.video_duration:
            dummy = self.send_dbus(['setposition',str(newpos)])

    def seekinvideo(self, position):
        if self.omxprocess and self.dbuscontrol and self.video_duration > 0:
            if self.seek_after:
                self.root.after_cancel(self.seek_after)
            self.seek_after = self.root.after(500, self.goto_pos)

    def vol_changed(self, volume):
        vol = int(volume)
        if self.status != 'stopped':
            if self.volume_after:
                self.root.after_cancel(self.volume_after)
            if self.mode == 'AV' and self.dbuscontrol and self.videomode.get() in ['full','refresh']:
                self.volume_after = self.root.after(500, self.set_volume)
            elif self.dbuscontrol:
                self.volume_after = self.root.after(500, self.set_volume_dbus)
            else:
                self.volume_after = self.root.after(500, self.set_volume)
        else:
            self.currentvolume = vol

    def set_volume_dbus(self):
        self.volume_after = None
        vol = self.changedvolume.get()
        if vol == self.currentvolume:
            return
        vval = "{0:11.10f}".format(pow(10,vol*100/2000.0))
        res = self.send_dbus(['volume',(vval)])
        if self.omxprocess and not res:
            self.volume_after = self.root.after(500, self.set_volume_dbus)
        self.currentvolume = vol

    def set_volume(self):
        self.volume_after = None
        vol = self.changedvolume.get()
        url = self.playlist[self.songpointer]
        delfact = 1.0
        if not url.startswith('file://') and self.currentmode == 'video':
            delfact = 10.0
        if self.status != 'stopped':
            while self.volume_after_running:
                time.sleep(0.1)
            self.volume_after_running = True
            if vol > self.currentvolume:
                diff = vol - self.currentvolume
                self.currentvolume = vol
                for k in range(0,diff/3):
                    self.sendcommand('+')
                    time.sleep(self.vchdelay*delfact)
            elif vol < self.currentvolume:
                diff = self.currentvolume - vol
                self.currentvolume = vol
                for k in range(0,diff/3):
                    self.sendcommand('-')
                    time.sleep(self.vchdelay*delfact)
            self.volume_after_running = False
        self.currentvolume = vol

    def trace_screenmode(self, *args):
        mode = self.screenmode.get()
        if mode == 'max':
            self.maximize()
            self.un_fullscreen()
            self.maximize()
        elif mode == 'full':
            self.fullscreen()
            self.un_maximize()
        else:
            self.un_fullscreen()
            self.un_maximize()
            if mode == 'min':
                self.screen_resize(self.vminheight)
            else:
                self.screen_resize(int(mode))

    def trace_videomode(self, *args):
        mode = self.videomode.get()
        if mode not in ['full','refresh']:
            if self.screenmode.get() in ['full','max']:
                self.check_window()
            else:
                geo = self.bgframe.winfo_geometry()
                geol = geo.split('+')
                sgeol = geol[0].split('x')
                self.screen_resize(int(sgeol[1]))

    def screen_resize(self,height):
        self.bgframe['width'] = self.getwidth(height,self.videomode.get())
        self.bgframe['height'] = height
        self.bgframe.grid_propagate(True)        
        top=self.winfo_toplevel()
        top.update_idletasks()
        top.geometry(str(top.winfo_reqwidth())+'x'+str(top.winfo_reqheight()))

    def save_playlist(self):
        path = tkFileDialog.asksaveasfilename(defaultextension='.m3u',filetypes=[('M3U Playlist', '*.m3u')],title='Save Playlist')
        if path:
            f = file(path,'wb')
            f.write('\n'.join(self.playlist))
            f.close()

    def checkaudio(self,url):
        ext = url.split('.')[-1].lower()
        if ext in self.audioextensions:
            return True
        elif ext in self.videoextensions:
            return False
        elif self.streammode.get() == 'audio':
            return True
        else:
            return False

    def checkvideomode(self,vmode):
        res = True
        if ':' in vmode:
            vmlist = vmode.split(':')
            if len(vmlist) == 2:
                try:
                    f = float(vmlist[0])
                except:
                    res = False
                try:
                    f = float(vmlist[1])
                except:
                    res = False
            else:
                res = False
        else:
            res = False
        return res

    def getheight(self,width,mode):
        if mode == 'auto' and self.scalefactor != 1.0:
            return int(round(width / self.scalefactor))
        elif mode in ['full','refresh','16:9','auto'] or mode not in self.videomodes:
            return int(round(width * 9.0 / 16))
        else:
            wl = mode.split(':')
            wf = float(wl[0])
            hf = float(wl[1])
            return int(round(width * hf / wf))

    def getwidth(self,height,mode):
        if mode == 'auto' and self.scalefactor != 1.0:
            return int(round(height * self.scalefactor))
        elif mode in ['full','refresh','16:9','auto'] or mode not in self.videomodes:
            return int(round(height * 16.0 / 9))
        else:
            wl = mode.split(':')
            wf = float(wl[0])
            hf = float(wl[1])
            return int(round(height * wf / hf))

    def videowinsize(self, screenoffset=0):
        geo = self.bgframe.winfo_geometry()
        geol = geo.split('+')
        sgeol = geol[0].split('x')
        vw = int(sgeol[0])
        vh = int(sgeol[1])
        xpos = self.bgframe.winfo_rootx()
        ypos = self.bgframe.winfo_rooty()
        
        vidh = self.getheight(vw,self.videomode.get())
        if vidh <= vh:
            offset = int(round((vh-vidh)/2.0))
            varr = [str(xpos+screenoffset),str(ypos+offset),str(xpos+vw+screenoffset),str(ypos+offset+vidh)]
        else:
            vidw  = self.getwidth(vh,self.videomode.get())
            offset = int(round((vw-vidw)/2.0))
            varr = [str(xpos+offset+screenoffset),str(ypos),str(xpos+offset+vidw+screenoffset),str(ypos+vh)]
        return ' '.join(varr)

    def filteroptions(self,optlist):
        res = []
        ignore = False
        for opt in optlist:
            if ignore:
                ignore = False
            elif opt in ['-b','--blank','-r','--refresh','-g','--genlog','-k','--keys', '-i', '--info','-s', '--stats','--no-keys']:
                pass
            elif opt in ['--win','--vol','--amp','--dbus_name','--key-config','-l','--pos','--layer']:
                ignore = True
            else:
                res.append(opt)
        return res         

    def on_activate_first(self):
        top=self.winfo_toplevel()
        if self.mode == 'audio':
            top.minsize(int(top.winfo_reqwidth()),int(top.winfo_reqheight()))
        else:
            hoffset = 0
            top.minsize(self.getwidth(self.vminheight,'4:3'),self.vminheight+hoffset)
        if self.playlist and self.autoplay:
            self.playsong(0)

    def freeze_screen(self,mode):
        if mode in ['full','refresh']:
            self.root.lift()
            self.root.grab_set_global()
        self.resize = False
        self.root.resizable(False, False)
        self.frozen = self.root.geometry()
        self.playlistwindow.grid_remove()
        self.video_duration = 0
        self.vmodeoption['state'] = tk.DISABLED
        self.lmodeoption['state'] = tk.DISABLED
        if self.yScroll:
            self.yScroll.grid_remove()
        self.seekbar['state'] = tk.DISABLED
        self.smodeoption['state'] = tk.DISABLED
        if self.dbuscontrol:
            self.seekable = False
        self.set_title()

    def unfreeze_screen(self,mode):
        if mode in ['full','refresh']:
            self.root.grab_release()
        self.root.resizable(True, True)
        self.frozen = ''
        self.playlistwindow.grid()
        self.vmodeoption['state'] = tk.NORMAL
        self.lmodeoption['state'] = tk.NORMAL
        self.smodeoption['state'] = tk.NORMAL
        self.seekbar['to'] = 180
        self.seekbar['state'] = tk.NORMAL
        if self.yScroll:
            self.yScroll.grid()
        self.video_duration = 0
        self.scalefactor = 1.0
        self.reset_pnbuttons()
        self.resize = True
        self.seekable = True
        self.set_title()

    def maximize(self):
        self.root.attributes('-zoomed', True)

    def un_maximize(self):
        self.root.attributes('-zoomed', False)

    def fullscreen(self):
        self.root.attributes('-fullscreen', True)

    def un_fullscreen(self):
        self.root.attributes('-fullscreen', False)

    def transparency_off(self):
        if self.dbuscontrol and self.omxprocess and self.resize and self.visible and self.currentmode == 'video':
            dummy = self.send_dbus(['setalpha','255'])

    def half_transparent(self):
        if self.dbuscontrol and self.omxprocess and self.resize and self.visible and self.currentmode == 'video':
            dummy = self.send_dbus(['setalpha','128'])
            dummy = self.root.after(2000,self.transparency_off)

    def check_visible(self, evt = None):
        if self.dbuscontrol and self.omxprocess and self.resize and self.visible and self.currentmode == 'video':
            url = self.playlist[self.songpointer]
            if '--live' not in self.omxvideooptions:
                self.visible = False
                dummy = self.send_dbus(['hidevideo'])
            else:
                dummy = self.send_dbus(['setvideopos']+self.videowinsize(self.screenwidth).split(' '))
        elif not self.dbuscontrol and self.omxprocess and self.currentmode == 'video':
            self.root.deiconify()

    def check_window(self,evt=None):
        if self.frozen:
            if self.root.geometry() != self.frozen:
                self.root.geometry(self.frozen)
        elif self.dbuscontrol and self.omxprocess and self.resize and self.currentmode == 'video':
            if self.resize_after:
                self.root.after_cancel(self.resize_after)
            self.resize_after = self.root.after(20, self.resize_videoarea, 0)

    def resize_videoarea(self, *args):
        if not self.visible:
            self.visible = True
            dummy = self.send_dbus(['unhidevideo'])
        else:
            dummy = self.send_dbus(['setvideopos']+self.videowinsize(args[0]).split(' '))
            self.resize_after = None

    def keyp_handler(self, event):
        st = event.state & 141
        if st == 0:
            if event.keysym in ['space','Return','KP_Enter','p']:
                self.playpause()
            elif event.keysym in ['q','Escape']:
                self.stop()
            elif event.keysym == 'Down' and self.nextbutton['state'] != tk.DISABLED:
                self.nextsong()
            elif event.keysym == 'Up' and self.prevbutton['state'] != tk.DISABLED:
                self.prevsong()
            elif event.keysym == 'Left' and self.seekable:
                self.sendcommand('\x1b\x5b\x44')
            elif event.keysym == 'Right' and self.seekable:
                self.sendcommand('\x1b\x5b\x43')
            elif event.keysym == 'less':
                self.sendcommand('<')
            elif event.keysym == 'greater':
                self.sendcommand('>')
            elif event.keysym in ['Next','comma'] and self.seekable:
                self.sendcommand('\x1b\x5b\x42')
            elif event.keysym in ['Prior','period'] and self.seekable:
                self.sendcommand('\x1b\x5b\x41')
            elif event.keysym in ['1','2','z','j','k','i','o','n','m','s','w','x','d','f']:
                self.sendcommand(event.keysym)
            else:
                av = 0
                if event.keysym in ['plus','KP_Add']:
                    av = 3
                elif event.keysym in ['minus','KP_Subtract']:
                    av = -3
                if av != 0:
                    nv = self.changedvolume.get() + av
                    if nv in range(-60,13):
                        self.changedvolume.set(nv)
                        self.vol_changed(nv) 
        elif st == 8:
            if event.keysym in ['c','q']:
                self.on_close()
            elif event.keysym == 'k':
                os.system('killall dbus-send')
                os.system('killall omxplayer.bin')
            elif event.keysym == 'm' and not self.frozen:
                if self.mode == 'audio':
                    if self.root.attributes('-zoomed'):
                        self.un_maximize()
                    else:
                        self.maximize()
                elif self.running_in_window():
                    if self.screenmode.get() == 'max' or self.root.attributes('-zoomed'):
                        self.screenmode.set('min')
                    else:
                        self.screenmode.set('max')
            elif event.keysym == 'f' and not self.frozen:
                if self.mode == 'audio':
                    if self.root.attributes('-fullscreen'):
                        self.un_fullscreen()
                    else:
                        self.fullscreen()
                elif self.running_in_window():
                    if self.screenmode.get() == 'full' or self.root.attributes('-fullscreen'):
                        self.screenmode.set('max')
                    else:
                        self.screenmode.set('full')
            elif event.keysym == 's'and not (self.omxprocess and self.mode == 'AV'):
                self.save_playlist()
            elif event.keysym == 'u' and not self.omxprocess:
                if self.dbuscontrol:
                    self.dbuscontrol = False
                else:
                    self.dbuscontrol = True
                self.set_title()
            elif event.keysym == 'a' and self.mode == 'AV' and self.resize:
                if self.omxprocess and self.videomode.get() in ['full','refresh','auto']:
                    return
                if self.videomode.get() != 'auto':
                    self.videomode.set('auto')
            elif event.keysym in ['KP_Add','KP_Subtract','Next','Prior'] and self.mode == 'AV' and not self.omxprocess:
                if event.keysym in ['KP_Subtract','Next'] and self.layer > 0:
                    self.layer -= 1
                elif event.keysym in ['KP_Add','Prior']:
                    self.layer += 1
                self.set_title()
            elif self.mode == 'AV' and not self.frozen and self.running_in_window():
                if event.keysym == 'h':
                    if self.controls_hidden:
                        self.unhide_control()
                    else:
                        self.hide_control()
                elif event.keysym in ['0','1','2','3','4','5','6','7','8','9']:
                    ind = min(int(event.keysym),len(self.screenmodes)-4)
                    self.screenmode.set(self.screenmodes[ind+1])
                elif event.keysym in ['plus','minus'] and self.videomode.get() not in ['full','refresh']:
                    mode = self.videomode.get()
                    pos = self.videomodes.index(mode)
                    if event.keysym == 'plus' and pos < len(self.videomodes)-1:
                        self.videomode.set(self.videomodes[pos+1])                        
                    elif event.keysym == 'minus' and pos > 3:
                        self.videomode.set(self.videomodes[pos-1]) 

    def running_in_window(self):
        if self.omxprocess and self.mode == 'AV' and self.videomode.get() in ['full','refresh']:
            return False
        else:
            return True
            
    def playsong(self, index):
        if not self.omxprocess:
            self.prevbutton['state'] = tk.DISABLED
            self.nextbutton['state'] = tk.DISABLED
            self.songpointer = index
            vopts = ['--vol',str(self.currentvolume*100)]
            pos = self.seekposition.get()
            if pos != 0:
                sec = int(pos * 60)
                h = sec/3600
                m = (sec-(h*3600))/60
                s = sec%60
                seekstr = ':'.join([str(h).rjust(2,'0'),str(m).rjust(2,'0'),str(s).rjust(2,'0')])
                sopts = ['--pos',seekstr]
            else:
                sopts = []

            if self.dbuscontrol:
                dbopts = ['--dbus_name',self.dbus_dest]
            else:
                dbopts = []

            if self.mode == 'audio' or self.checkaudio(self.playlist[index]):
                options = self.omxaudiooptions + vopts + sopts + dbopts
                self.currentmode = 'audio'
            else:
                mode = self.videomode.get()
                if mode == 'auto':
                    self.get_scalefactor(self.playlist[index])
                self.freeze_screen(mode)
                self.currentmode = 'video'
                if mode == 'full':
                    bopts = ['-b']
                elif mode == 'refresh':
                    bopts = ['-b','-r']
                else:
                    bopts = ['--win',self.videowinsize()]
                if self.layer != 0:
                    lopts = ['--layer',str(self.layer)]
                elif self.standalone['wcount'] > 1:
                    lopts = ['--layer',str(self.standalone['wcount'])]
                else:
                    lopts = []
                options = self.omxvideooptions + vopts + sopts + bopts + dbopts + lopts
            pargs = ['omxplayer'] + options + [self.playlist[index]]
            self.omxprocess = subprocess.Popen(pargs,stdin=subprocess.PIPE,stdout=file('/dev/null','wa'),stderr=file('/dev/null','wa'))
            self.omxwatcher = threading.Timer(0,self.watch)
            self.omxwatcher.daemon = True
            self.omxwatcher.start()
            if self.durwatcher:
                try:
                    self.durwatcher.cancel()
                    self.durwatcher = None
                except:
                    pass
            if self.currentmode == 'video':
                self.durwatcher = threading.Timer(2,self.get_duration)
                self.durwatcher.daemon = True
                self.durwatcher.start()
            else:
                dummy = self.root.after(200,self.reset_pnbuttons)
            self.status = 'playing'
            self.playcontent.set(self.pausestring)
            selection = self.playlistwindow.curselection()
            if not selection or index != int(selection[0]):
                self.listpointer = index
                self.playlistwindow.selection_clear(0, len(self.playlist)-1)
                self.playlistwindow.selection_set(index)
            self.playlistwindow.see(index)

    def reset_pnbuttons(self):
        self.prevbutton['state'] = tk.NORMAL
        self.nextbutton['state'] = tk.NORMAL

    def on_close(self):
        if self.omxprocess:
            self.status='closing'
            self.sendcommand('q')
            dummy = self.after(200,self.on_close2)
        else:
            self.standalone['wcount'] += -1
            self.root.destroy()

    def on_close2(self):
        if self.omxprocess:
            self.omxprocess.terminate()
            dummy = self.after(200,self.on_close3)
        else:
            self.standalone['wcount'] += -1
            self.root.destroy()

    def on_close3(self):
        if self.omxprocess:
            self.omxprocess.kill()
        self.standalone['wcount'] += -1
        self.root.destroy()

    def on_finished(self, *args):
        stat = self.status
        self.status = 'stopped'
        self.playcontent.set(self.playstring)
        if self.currentmode == 'video':
            mode = self.videomode.get()
            self.unfreeze_screen(mode)
        self.seekposition.set(0)
        if stat != 'finished':
            if self.songpointer == self.listpointer:
                if self.listpointer < len(self.playlist)-1:
                    self.nextsong()
                elif self.autofinish:
                    self.on_close()
            else:
                self.songpointer = self.listpointer
                self.playsong(self.songpointer)

    def watch(self):
        if self.omxprocess:
            try:
                dummy = self.omxprocess.wait()
            except:
                pass
        self.omxprocess = None
        if self.durwatcher:
            try:
                self.durwatcher.cancel()
                self.durwatcher = None
            except:
                pass
        if self.status != 'closing':
            self.root.event_generate("<<finished>>")

    def sendcommand(self, cmd):
        if self.omxprocess:
            try:
                self.omxprocess.stdin.write(cmd)
            except:
                pass

    def send_dbus(self,args):
        res = ''
        err = ''
        if self.omxprocess:
            try:
                db = subprocess.Popen(['dbuscontrolm.sh']+[self.dbus_dest]+args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                (res,err) = db.communicate()
            except:
                res = ''
            if err:
                res = ''
        return res

    def playpause(self):
        if self.status in ['stopped','finished']:
            self.songpointer = self.listpointer
            self.playsong(self.songpointer)

        elif self.status == 'paused':
            self.sendcommand('p')
            self.status = 'playing'
            self.playcontent.set(self.pausestring)

        elif self.status == 'playing':
            self.sendcommand('p')
            self.status = 'paused'
            self.playcontent.set(self.playstring)

    def stop(self,stat='finished'):
        if self.omxprocess:
            self.status = stat
            self.sendcommand('q')
        else:
            self.playcontent.set(self.playstring)
            self.status = 'stopped'

    def rewind(self):
        if self.seekable:
            self.sendcommand('\x1b\x5b\x44')

    def forward(self):
        if self.seekable:
            self.sendcommand('\x1b\x5b\x43')

    def prevsong(self):
        if self.listpointer != self.songpointer and self.status != 'stopped':
            self.stop('stopped')
        elif self.listpointer > 0:
            self.listpointer = self.listpointer - 1
            self.playlistwindow.selection_clear(0, len(self.playlist)-1)
            self.playlistwindow.selection_set(self.listpointer)
            if self.status == 'stopped':
                self.playsong(self.listpointer)
            else:
                self.stop('stopped')

    def nextsong(self):
        if self.listpointer != self.songpointer and self.status != 'stopped':
            self.stop('stopped')
        elif self.listpointer < len(self.playlist)-1:
            self.listpointer = self.listpointer + 1
            self.playlistwindow.selection_clear(0, len(self.playlist)-1)
            self.playlistwindow.selection_set(self.listpointer)
            if self.status == 'stopped':
                self.playsong(self.listpointer)
            else:
                self.stop('stopped')

    def on_listbox_select(self,event):
        sel = self.playlistwindow.curselection()
        if sel:
            self.listpointer = int(sel[0])

    def on_listbox_double(self,event):
        self.on_listbox_select(event)
        if self.status != 'stopped':
            if self.songpointer == self.listpointer:
                self.stop()
                self.playsong(self.listpointer)
            else:
                self.stop('stopped')
        else:
            self.playsong(self.listpointer)

    def focus_out(self, event):
        self.root.focus_set()

    def createwidgets(self):
        hg = min(self.maxlines,len(self.playlist))
        self.bgframe = tk.Frame(self, bg = '#000')            
        self.playlistwindow = tk.Listbox(self, bd=0, relief=tk.FLAT, exportselection=0, takefocus=0, selectmode = 'single', width = self.defaultwidth, height = hg, font=self.font,activestyle='none',bg='#000', fg = '#ddd', selectbackground='#60c', selectforeground='#ffffd0')
        if self.namelist:
            for song in self.namelist:
                self.playlistwindow.insert(tk.END, song)
        else:
            for url in self.playlist:
                slist = url.split('/')
                song = slist[-1]
                if not song:
                    if len(slist) > 1:
                        song = slist[-2]
                    else:
                        song = url
                self.playlistwindow.insert(tk.END, urllib.unquote(song).replace('%20',' '))
        self.playlistwindow.selection_set(self.songpointer)
        self.playlistwindow.bind("<<ListboxSelect>>", self.on_listbox_select)
        self.playlistwindow.bind("<Double-Button-1>",self.on_listbox_double)
        self.playlistwindow.bind("<FocusIn>",self.focus_out)
        if len(self.playlist) > self.maxlines:
            self.bgframe.grid(row=0,column=0,columnspan=8, sticky=tk.N+tk.S+tk.E+tk.W)
            self.yScroll = tk.Scrollbar(self, takefocus=0, orient=tk.VERTICAL)
            self.yScroll['width'] = int(self.yScroll['width']) + (self.fontheight-10)
            self.playlistwindow.configure(yscrollcommand=self.yScroll.set)
            self.yScroll['command'] = self.playlistwindow.yview
            self.yScroll.grid(row=0,column=7, sticky=tk.N+tk.S)
        else:
            self.bgframe.grid(row=0,column=0,columnspan=7, sticky=tk.N+tk.S+tk.E+tk.W)
        self.playlistwindow.grid(row=0,column=0,columnspan=7, sticky=tk.N+tk.S+tk.E+tk.W)

        self.playbutton = tk.Button(self, takefocus=0, command=self.playpause, font=self.font, textvariable = self.playcontent, width = 3, justify = tk.CENTER)
        self.playbutton.grid(row=1,column=0)
        self.stopbutton = tk.Button(self, takefocus=0, command=self.stop, font=self.font, text = self.stopstring, width = 3, justify = tk.CENTER)
        self.stopbutton.grid(row=1,column=1)

        self.rewbutton = tk.Button(self, takefocus=0, command=self.rewind, font=self.font, text = self.rewstring, width = 3, justify = tk.CENTER)
        self.rewbutton.grid(row=1,column=2)
        self.fwdbutton = tk.Button(self, takefocus=0, command=self.forward, font=self.font, text = self.fwdstring, width = 3, justify = tk.CENTER)
        self.fwdbutton.grid(row=1,column=3)

        self.prevbutton = tk.Button(self, takefocus=0, command=self.prevsong, font=self.font, text = self.prevstring, width = 3, justify = tk.CENTER)
        self.prevbutton.grid(row=1,column=4)
        self.nextbutton = tk.Button(self, takefocus=0, command=self.nextsong, font=self.font, text = self.nextstring, width = 3, justify = tk.CENTER)
        self.nextbutton.grid(row=1,column=5)
        self.volume = tk.Scale(self, takefocus=0, font = (self.fontname,str((self.fontheight+4)/2),'bold'), command=self.vol_changed, width=str((self.fontheight+4)/2)+'p',length=str((self.fontheight-2)*10)+'p', from_ = -60, to=12, variable=self.changedvolume ,orient=tk.HORIZONTAL, resolution=3, showvalue=1)
        self.volume.grid(row=1,column=6, sticky=tk.E)

        if self.mode == 'AV':
            mode = self.screenmode.get()
            if mode == 'max':
                self.maximize()
            elif mode == 'full':
                self.fullscreen()
            if mode == 'min':
                self.bgframe['width'] = self.vminwidth
                self.bgframe['height'] = self.vminheight
            else:
                self.bgframe['width'] = self.root.winfo_screenwidth()
                self.bgframe['height'] = self.root.winfo_screenheight()
            self.vmodeoption = tk.OptionMenu(self, self.videomode, *self.videomodes)
            self.vmodeoption.configure(font=(self.fontname,str(self.fontheight-2),'bold'))
            self.vmodeoption['menu'].configure(font=(self.fontname,str(self.fontheight-2),'bold'),disabledforeground='#44f', postcommand = self.half_transparent)
            self.vmodeoption['menu'].entryconfigure(0,state=tk.DISABLED)
            self.vmodeoption.grid(row=2,column=0,columnspan=2,sticky="WE")

            self.lmodeoption = tk.OptionMenu(self, self.screenmode, *self.screenmodes)
            self.lmodeoption.configure(font=(self.fontname,str(self.fontheight-2),'bold'))
            self.lmodeoption['menu'].configure(font=(self.fontname,str(self.fontheight-2),'bold'),disabledforeground='#44f', postcommand = self.half_transparent)
            self.lmodeoption['menu'].entryconfigure(0,state=tk.DISABLED)
            self.lmodeoption.grid(row=2,column=2,columnspan=2,sticky="WE")

            self.smodeoption = tk.OptionMenu(self, self.streammode, *self.streammodes)
            self.smodeoption.configure(font=(self.fontname,str(self.fontheight-2),'bold'))
            self.smodeoption['menu'].configure(font=(self.fontname,str(self.fontheight-2),'bold'),disabledforeground='#44f')
            self.smodeoption['menu'].entryconfigure(0,state=tk.DISABLED)
            self.smodeoption.grid(row=2,column=4,columnspan=2, sticky="WE")
            self.seekbar = tk.Scale(self, takefocus=0, command=self.seekinvideo, font = (self.fontname,str((self.fontheight+4)/2),'bold'),width=str((self.fontheight+4)/2)+'p', from_ = 0, to=180, variable=self.seekposition ,orient=tk.HORIZONTAL, resolution=0.05, showvalue=1)
            self.seekbar.grid(row=2,column=6, sticky="WE")

    def hide_control(self):
        self.controls_hidden = True
        self.playbutton.grid_remove()
        self.stopbutton.grid_remove()
        self.rewbutton.grid_remove()
        self.fwdbutton.grid_remove()
        self.prevbutton.grid_remove()
        self.nextbutton.grid_remove()
        self.volume.grid_remove()
        self.vmodeoption.grid_remove()
        self.lmodeoption.grid_remove()
        self.smodeoption.grid_remove()
        self.seekbar.grid_remove()
        self.root.grid_propagate(True)
        top=self.winfo_toplevel()
        top.update_idletasks()
        top.geometry(str(top.winfo_reqwidth())+'x'+str(top.winfo_reqheight()))            
        
    def unhide_control(self):
        self.playbutton.grid()
        self.stopbutton.grid()
        self.rewbutton.grid()
        self.fwdbutton.grid()
        self.prevbutton.grid()
        self.nextbutton.grid()
        self.volume.grid()
        self.vmodeoption.grid()
        self.lmodeoption.grid()
        self.smodeoption.grid()
        self.seekbar.grid()
        self.controls_hidden = False
        self.root.grid_propagate(True)        
        top=self.winfo_toplevel()
        top.update_idletasks()
        top.geometry(str(top.winfo_reqwidth())+'x'+str(top.winfo_reqheight()))

# main script function

def run(args):
    # arg0 = ignore, arg1 = mode, arg2 = URL, arg3 (optional, only for mode 'av') = mimetype
    # possible modes = 'av', 'ytdl'
    if len(args) > 2:
        mode = args[1]
        url = args[2]
        mimetype = ''

    # av section: play audio, video, m3u playlists and streams
        if mode in ['av','-av','pl']:
            mtflag = True
            if len(args) > 3:
                mimetype = args[3]
                if mimetypes and mimetype not in mimetypes:
                    mtflag = False
            url_extension = url.lower().split('.')[-1]
            if (url_extension in ['m3u','m3u8','pls'] or mode == 'pl' or 'mimetype' in ['audio/mpegurl','audio/x-mpegurl','audio/m3u','audio/x-scpls','audio/pls']) and mtflag:
                if mode == 'pl':
                    playlist = copy.copy(standalone['playlist'])
                    names = []
                    audioonly = checkextensions(playlist,audioextensions)
                else:
                    audioonly, playlist, names = get_playlist(url,streammode,mimetype)
                if playlist:
                    if audioonly and useVLC:
                        dummy = subprocess.call(['vlc',url])
                    elif audioonly and useAudioplayer:
                        if not standalone['root']:
                            root = tk.Tk()
                        else:
                            root = tk.Toplevel(standalone['root'])
                        standalone['wcount'] += 1
                        player = omxplayergui(master=root, playlist=playlist,namelist=names,volume=defaultaudiovolume,omxaudiooptions=omxaudiooptions,
                                                autofinish=autofinish,fontheight=fontheight,fontname=fontname,maxlines=maxlines,
                                                autoplay=autoplay,width=lwidth,audioextensions=audioextensions,videoextensions=videoextensions,
                                                freeze=freeze_window, standalone=standalone)
                        if not standalone['root']:
                            player.mainloop()
                    elif useVideoplayer:
                        if not standalone['root']:
                            root = tk.Tk()
                        else:
                            root = tk.Toplevel(standalone['root'])
                        standalone['wcount'] += 1
                        player = omxplayergui(master=root, playlist=playlist,namelist=names,volume=defaultaudiovolume,omxaudiooptions=omxaudiooptions,
                                                omxvideooptions=omxoptions,mode='AV',streammode=streammode,vmode=videomode,vminheight=videoheight,
                                                autofinish=autofinish,fontheight=fontheight,fontname=fontname,screenmode=screenmode,
                                                autoplay=autoplay,audioextensions=audioextensions, get_DAR = get_DAR, hide_controls = hide_controls,
                                                videoextensions=videoextensions, freeze=freeze_window, standalone=standalone)
                        if not standalone['root']:
                            player.mainloop()
                    else:
                        if audioonly:
                            options = omxaudiooptions
                        else:
                            options = omxoptions
                        script = '#!/bin/bash\n'
                        for s in playlist:
                            if audioonly and omxplayer_in_terminal_for_audio:
                                script += 'echo "now playing: '+ urllib.unquote(s.split('/')[-1]) +'"\n'
                            script += 'omxplayer ' + get_opt(options) + ' "' + s + '" > /dev/null 2>&1\n'
                        script += 'rm ' + scdir+os.sep+'playall.sh\n'
                        f = file(scdir+os.sep+'playall.sh','wb')
                        f.write(script)
                        f.close()
                        os.chmod(scdir+os.sep+'playall.sh',511)
                        if omxplayer_in_terminal_for_audio and audioonly:
                            dummy = subprocess.call([preferred_terminal,"-e",scdir+os.sep+'playall.sh'])
                        elif omxplayer_in_terminal_for_video and not audioonly:
                            terminal = get_terminal()
                            if terminal == 'xterm':
                                dummy = subprocess.call(["xterm","-fn","fixed","-fullscreen", "-maximized", "-bg", "black", "-fg", "black", "-e",scdir+os.sep+'playall.sh'])
                            else:
                                dummy = subprocess.call([terminal,'-e',scdir+os.sep+'playall.sh'])
                        else:
                            dummy = subprocess.call([scdir+os.sep+'playall.sh','>', '/dev/null', '2>&1'])
                
            elif mtflag:
                url_valid = True
                if url.startswith('file://'):
                    url = url.replace('file://','').replace('%20',' ')
                    url = urllib.unquote(url)
                    if not os.path.exists(url):
                        url_valid = False
                elif url.startswith('/'):
                    if not os.path.exists(url):
                        url_valid = False
                if url_valid:
                    if url_extension in audioextensions or (streammode == 'audio' and not url_extension in videoextensions):
                        if useVLC:
                            dummy = subprocess.call(['vlc',url])
                        elif useAudioplayer:
                            if not standalone['root']:
                                root = tk.Tk()
                            else:
                                root = tk.Toplevel(standalone['root'])
                            standalone['wcount'] += 1
                            player = omxplayergui(master=root, playlist=[url],volume=defaultaudiovolume,omxaudiooptions=omxaudiooptions,
                                                    autofinish=autofinish,fontheight=fontheight,fontname=fontname,maxlines=maxlines,
                                                    autoplay=autoplay,width=lwidth,audioextensions=audioextensions,videoextensions=videoextensions,
                                                    freeze=freeze_window, standalone=standalone)
                            if not standalone['root']:
                                player.mainloop()
                        else:
                            if omxplayer_in_terminal_for_audio:
                                pargs = [preferred_terminal,'-e','omxplayer'] + omxaudiooptions + [url]
                                dummy = subprocess.call(pargs)
                            else:
                                pargs = ['omxplayer'] + omxaudiooptions + [url]
                                dummy = subprocess.call(pargs)
                                
                    else:
                        options = omxoptions
                        if live_tv:
                            for lt in live_tv:
                                if url.startswith(lt):
                                    options = omx_livetv_options
                                    break
                        if useVideoplayer:
                            if not standalone['root']:
                                root = tk.Tk()
                            else:
                                root = tk.Toplevel(standalone['root'])
                            standalone['wcount'] += 1
                            player = omxplayergui(master=root, playlist=[url],volume=defaultaudiovolume,omxaudiooptions=omxaudiooptions,
                                                    omxvideooptions=options,mode='AV',streammode=streammode,vmode=videomode,vminheight=videoheight,
                                                    autofinish=autofinish,fontheight=fontheight,fontname=fontname,screenmode=screenmode,
                                                    autoplay=autoplay,audioextensions=audioextensions,get_DAR = get_DAR, hide_controls = hide_controls,
                                                    videoextensions=videoextensions,freeze=freeze_window, standalone=standalone)
                            if not standalone['root']:
                                player.mainloop()
                        elif omxplayer_in_terminal_for_video:
                            terminal = get_terminal()
                            if terminal == 'xterm':
                                pargs = ["xterm","-fn","fixed","-fullscreen", "-maximized", "-bg", "black", "-fg", "black", "-e",'omxplayer']+options+[url]+['>', '/dev/null', '2>&1']
                            else:
                                pargs = [terminal,"-e",'omxplayer']+options+[url]+['>', '/dev/null', '2>&1']
                            dummy = subprocess.call(pargs)
                        else:
                            pargs = ['omxplayer'] + options + [url,'>', '/dev/null', '2>&1']
                            dummy = subprocess.call(pargs)
                            
    # end of media section

    # web video section (HTML5 and all websites supported by youtube-dl)
        elif mode in ['ytdl','-ytdl']: #youtube and HTML5 videos
            if html5_first:
                tags = video_tag_extractor(url)
                if tags: #extract embedded html5 video
                    play_html5(tags)
                elif use_ytdl_server and check_server():
                    (flag, res) = uriretrieve('http://'+ytdl_server_host+':'+ytdl_server_port+'/info?url='+urllib.quote(url))
                    if flag and res:
                        play_ytdl(res)
                elif os.path.exists('/usr/bin/youtube-dl'):
                    yta = ['youtube-dl', '-g', '-e']+youtube_dl_options+[url]
                    yt = subprocess.Popen(yta,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    (res,err) = yt.communicate()
                    if res:
                        play_ytdl(res)
            else:
                res = ''
                flag = True
                if use_ytdl_server and check_server():
                    (flag, res) = uriretrieve('http://'+ytdl_server_host+':'+ytdl_server_port+'/info?url='+urllib.quote(url))
                elif os.path.exists('/usr/bin/youtube-dl'):
                    yta = ['youtube-dl', '-g', '-e']+youtube_dl_options+[url]
                    yt = subprocess.Popen(yta,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    (res,err) = yt.communicate()
                if flag and res:
                    play_ytdl(res)
                else:
                    tags = video_tag_extractor(url)
                    if tags: #extract embedded html5 video
                        play_html5(tags)
        if os.path.exists(homedir+'/.omxplayergui.run'):
            os.remove(homedir+'/.omxplayergui.run')

    # end of web video section

def usage():
    print 'usage: omxplayergui.py [--config=/path/to/config.py] [--preset=presetname] [mode] [url] [mimetype]'
    print 'mode = av or ytdl'
    print 'url = http or file:// link or file path'
    print 'mimetype must start with audio/ or video/'
    print 'if run without argument a simple frontend will be used'
    sys.exit(0)

class entryApp(tk.Frame):
    def __init__(self, master,standalone,fontheight=12,fontname="SansSerif"):
        tk.Frame.__init__(self, master)
        self.fontheight = min([max([fontheight,10]),22])
        self.fontname = fontname
        try:
            self.font = (self.fontname,str(self.fontheight),'bold')
        except:
            self.font = ('SansSerif',str(self.fontheight),'bold')
        self.root = master
        self.master.title('OmxplayerGUI Frontend 1.7.0')
        self.standalone = standalone
        self.help = None
        self.grid()
        self.url = tk.StringVar()
        self.url.set(self.standalone['url'])
        self.root.protocol('WM_DELETE_WINDOW', self.quitapp)
        self.createWidgets()
        top=self.winfo_toplevel()
        top.resizable(False, False)

    def createWidgets(self):
        self.urlentry = tk.Entry(self,width=60,textvariable=self.url,font=self.font)
        self.urlentry.grid(row=0,column=0,columnspan=7, sticky=tk.N+tk.S+tk.E+tk.W)
        self.urlentry.bind('<Button-3><ButtonRelease-3>',self.rClicker, add='')
        self.openbutton = tk.Button(self, takefocus=0, command=self.get_file, font=self.font, text = 'Open', width = 7, justify = tk.CENTER)
        self.openbutton.grid(row=1,column=0)
        self.streambutton = tk.Button(self, takefocus=0, command=self.stream, font=self.font, text = 'Play/Stream', width = 12, justify = tk.CENTER)
        self.streambutton.grid(row=1,column=1)
        self.extractbutton = tk.Button(self, takefocus=0, command=self.extract, font=self.font, text = 'Extract', width = 10, justify = tk.CENTER)
        self.extractbutton.grid(row=1,column=2)
        self.quitbutton = tk.Button(self, takefocus=0, command=self.quitapp, font=self.font, text = 'Quit', width = 7, justify = tk.CENTER)
        self.quitbutton.grid(row=1,column=3)
        self.helpbutton = tk.Button(self, takefocus=0, command=self.showmanual, font=self.font, text = 'Help', width = 7, justify = tk.CENTER)
        self.helpbutton.grid(row=1,column=4)
        if os.path.exists('/usr/bin/kweb') and os.path.exists('/usr/local/share/kweb/kweb_about_s.html'):
            self.configurebutton = tk.Button(self, takefocus=0, command=self.configure, font=self.font, text = 'Edit Settings', width = 14, justify = tk.CENTER)
            self.configurebutton.grid(row=1,column=5)
        else:
            self.text = tk.Label(self, text=u'© 2014 by Günter Kreidl',font=('SansSerif',str(self.fontheight-2),'bold'))
            self.text.grid(row=1,column=5)           

        self.playlistwindow = tk.Listbox(self, bd=0, relief=tk.FLAT, exportselection=0, takefocus=0, selectmode = tk.EXTENDED, width = 60, height = 12, font=self.font,activestyle='none',bg='#112', fg = '#ddd', selectbackground='#60c', selectforeground='#ffffd0')
        if self.standalone['playlist']:
            for url in self.standalone['playlist']:
                slist = url.split('/')
                song = slist[-1]
                if not song:
                    if len(slist) > 1:
                        song = slist[-2]
                    else:
                        song = url
                self.playlistwindow.insert(tk.END, song.replace('%20',' '))
        self.playlistwindow.bind("<Double-Button-1>",self.on_listbox_double)
        self.yScroll = tk.Scrollbar(self, takefocus=0, orient=tk.VERTICAL)
        self.yScroll['width'] = int(self.yScroll['width']) + (self.fontheight-10)
        self.playlistwindow.configure(yscrollcommand=self.yScroll.set)
        self.yScroll['command'] = self.playlistwindow.yview
        self.yScroll.grid(row=2,column=6, sticky=tk.N+tk.S)
        self.playlistwindow.grid(row=2,column=0,columnspan=6, sticky=tk.N+tk.S+tk.E+tk.W)

        self.loadbutton = tk.Button(self, takefocus=0, command=self.load, font=self.font, text = 'Load', width = 7, justify = tk.CENTER)
        self.loadbutton.grid(row=3,column=0)
        self.savebutton = tk.Button(self, takefocus=0, command=self.save, font=self.font, text = 'Save List', width = 12, justify = tk.CENTER)
        self.savebutton.grid(row=3,column=1)
        self.addbutton = tk.Button(self, takefocus=0, command=self.add, font=self.font, text = 'Add Files', width = 10, justify = tk.CENTER)
        self.addbutton.grid(row=3,column=2)
        self.folderbutton = tk.Button(self, takefocus=0, command=self.folders, font=self.font, text = 'Folder', width = 7, justify = tk.CENTER)
        self.folderbutton.grid(row=3,column=3)
        self.deletebutton = tk.Button(self, takefocus=0, command=self.delete, font=self.font, text = 'Delete', width = 7, justify = tk.CENTER)
        self.deletebutton.grid(row=3,column=4)
        self.playbutton = tk.Button(self, takefocus=0, command=self.play, font=self.font, text = 'Play All', width = 14, justify = tk.CENTER)
        self.playbutton.grid(row=3,column=5)

    def load(self):
        extlist = ['m3u','m3u8','pls']
        filetypes = []
        pl = []
        for extension in extlist:
            filetypes.append((extension.upper(),'*.'+extension))
        filetypes.append(('ALL','*.*'))
        url = tkFileDialog.askopenfilename(parent=self.root,filetypes=filetypes,title='Select a Playlist',initialdir=self.standalone['basedir'])
        if url:
            self.standalone['basedir'] = os.path.dirname(url)
            ext = url.split('.')[-1].lower()
            if ext in extlist:
                ao,pl,names = get_playlist(url,'video','')
            if pl:
                self.standalone['playlist'] = pl
                if self.playlistwindow.get(0,tk.END):
                    self.playlistwindow.delete(0,tk.END)
                for url in self.standalone['playlist']:
                    slist = url.split('/')
                    song = slist[-1]
                    if not song:
                        if len(slist) > 1:
                            song = slist[-2]
                        else:
                            song = url
                    self.playlistwindow.insert(tk.END, song.replace('%20',' '))

    def save(self):
        if self.standalone['playlist']:
            path = tkFileDialog.asksaveasfilename(parent=self.root,defaultextension='.m3u',filetypes=[('M3U Playlist', '*.m3u')],initialdir=self.standalone['basedir'],title='Save Playlist')
            if path:
                if not path.endswith('.m3u'):
                    path += '.m3u'
                self.standalone['basedir'] = os.path.dirname(path)
                f = file(path,'wb')
                f.write('\n'.join(self.standalone['playlist']))
                f.close()

    def add(self):
        extlist = audioextensions + videoextensions
        filetypes = [('ALL','*.*')]
        for extension in extlist:
            filetypes.append((extension.upper(),'*.'+extension))
        flist = tkFileDialog.askopenfilenames(parent=self.root,filetypes=filetypes,title='Add File(s)',initialdir=self.standalone['basedir'])
        if flist:
            self.standalone['basedir'] = os.path.dirname(flist[0])
            for p in flist:
                if p.lower().split('.')[-1] in extlist:
                    self.standalone['playlist'].append(p)
                    self.playlistwindow.insert(tk.END, p.split('/')[-1])

    def folders(self):
        pl = []
        extlist = audioextensions + videoextensions
        path = tkFileDialog.askdirectory(parent=self.root,title='Add Directories',initialdir=self.standalone['basedir'])
        if path and os.path.isdir(path):
            self.standalone['basedir'] = path
            for root, dirs, files in os.walk(path):
                for f in files:
                    if f.lower().split('.')[-1] in extlist:
                        pl.append(os.path.join(root, f))
            pl.sort(key=str.lower)
            self.standalone['playlist'] += pl
            for p in pl:
                self.playlistwindow.insert(tk.END, p.split('/')[-1])
        
    def delete(self):
        sel = self.playlistwindow.curselection()
        if sel:
            sl = list(sel)
            sl.reverse()
            for s in sl:
                del self.standalone['playlist'][s]
                self.playlistwindow.delete(s)
        else:
            self.message('Nothing Selected','You must first select the items you want to delete.')

    def on_listbox_double(self,event):
        sel = self.playlistwindow.curselection()
        if sel:
            self.url.set(self.standalone['playlist'][sel[0]])
            self.stream()

    def play(self):
        if not self.standalone['playlist'] :
            self.message('Playlist Empty','You must add something to your paylist first!')
        else:
            run(['','pl',self.standalone['url']])

    def openmanual(self):
        global pdfprog
        self.help = subprocess.Popen([pdfprog,'/usr/local/share/kweb/omxplayerGUI_manual.pdf'])
        dummy = self.help.wait()
        self.help = None

    def showmanual(self):
        if self.help:
            return
        global pdfprog
        if not pdfprog:
            if os.path.exists('/usr/bin/evince'):
                pdfprog = 'evince'
            elif os.path.exists('/usr/bin/evince-gtk'):
                pdfprog = 'evince-gtk'
            elif os.path.exists('/usr/bin/xpdf'):
                pdfprog = 'xpdf'
            elif os.path.exists('/usr/bin/xpdf'):
                pdfprog = 'mupdf'
        if pdfprog:
            ti = threading.Timer(0,self.openmanual)
            ti.start()
        else:
            self.message('Missing Program','No PDF program found to open the manual.')

    def configure(self):
        if self.standalone['wcount'] == 0:
            self.standalone['open_settings'] = True
            self.root.destroy()
        else:
            self.message('Not Allowed','You must first close all player windows.')
        
    def quitapp(self):
        if self.standalone['wcount'] == 0:
            self.standalone['url'] = ''
            self.standalone['playlist'] = []
            if self.help:
                try:
                    self.help.terminate()
                except:
                    pass
            self.root.destroy()
        else:
            self.message('Not Allowed','You must first close all player windows.')

    def message(self,title,msg):
        res = tkMessageBox.showerror(title,msg )

    def stream(self):
        url = self.url.get()
        if not url and not (url.startswith('http') or url.startswith('file://') or url.startswith('/')):
            self.message('No Valid URL','You must enter a valid URL\nor file path!')
        else:
            self.standalone['url'] = url
            run(['','av',self.standalone['url']])

    def extract(self):
        url = self.url.get()
        if url and url.startswith('?'):
            searchstr = url[1:len(url)].strip().replace(' ','+')
            while '++' in searchstr:
                searchstr = searchstr.replace('++','+')
            if '+' in searchstr:
                last = searchstr.split('+')[-1]
                page = None
                try:
                    page = int(last)
                    searchstr = searchstr[0:searchstr.rfind('+'+last)]
                except:
                    pass
            if searchstr:
                self.standalone['url'] = 'http://www.youtube.com/results?search_query='+searchstr
                if page:
                    self.standalone['url'] += '&page=' + last
                run(['','ytdl',self.standalone['url']])
            else:
                self.message('No Valid Entry','You must enter a valid search request!')
        elif not url or not url.startswith('http'):
            self.message('No Valid URL','You must enter a valid URL!')
        else:
            self.standalone['url'] = url
            run(['','ytdl',self.standalone['url']])

    def get_file(self):
        extlist = audioextensions + videoextensions + ['m3u','m3u8','pls']
        filetypes = [('ALL','*.*')]
        for extension in extlist:
            filetypes.append((extension.upper(),'*.'+extension))
        url = tkFileDialog.askopenfilename(parent=self.root,filetypes=filetypes,title='audio,video,playlist',initialdir=self.standalone['basedir'])
        if url:
            ext = url.split('.')[-1].lower()
            if ext in extlist:
                self.standalone['url'] = url
                self.standalone['basedir'] = os.path.dirname(url)
                self.url.set(url)
                self.stream()

    def rClicker(self,e):
        def rClick_Paste(e):
            self.url.set('')
            e.widget.event_generate('<Control-v>')
        def rClick_Clear(e):
            self.url.set('')
        e.widget.focus()
        rmenu = tk.Menu(None, tearoff=0, takefocus=0,font=self.font)
        rmenu.add_command(label=' Clear&Paste', command=lambda e=e: rClick_Paste(e))
        rmenu.add_command(label=' Clear', command=lambda e=e: rClick_Clear(e))
        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")
        return "break"

if __name__ == '__main__':
    checkstr = ' '.join(sys.argv)
    if '--config=' in checkstr or '--preset=' in checkstr:
        args = []
        for arg in sys.argv:
            if arg.startswith('--config='):
                spath = arg.split('--config=')[1]
                if spath and os.path.exists(spath) and spath.endswith('.py'):
                    settings = spath
            elif arg.startswith('--preset='):
                pname = arg.split('--preset=')[1]
                if pname and os.path.exists('/usr/local/share/kweb/' + pname + '.preset'):
                    settings = '/usr/local/share/kweb/' + pname + '.preset'
            else:
                args.append(arg)
    else:
        args = sys.argv
    # take settings from separate file:
    if settings and os.path.exists(settings):
        try:
            execfile(settings)
        except:
            pass
    homedir = os.path.expanduser('~')
    standalone['basedir'] = homedir
    if len(args) > 2 and args[1] in ['av','-av','ytdl','-ytdl']:
        run(args)
    elif len(args) == 2:
        url = args[1]
        if ':' in url or url.startswith('/'):
            run([args[0],'av',url])
        elif url in ['-h','--help']:
            usage()
        else:
            url = os.getcwd()+os.sep +url
            if os.path.exists(url):
                run([args[0],'av',url])
    elif len(args) == 1:
        server = None
        if use_ytdl_server and ytdl_server_host == 'localhost' and os.path.exists(os.path.join(homedir,'youtube-dl')) and not check_server():
            server = start_server()
        while True:
            useAudioplayer = True
            useVideoplayer = True
            useVLC = False
            try:
                root = tk.Tk()
                standalone['root'] = root
                app = entryApp(master=root,standalone=standalone,fontheight=fontheight,fontname=fontname)                       
                app.mainloop()
            except:
                print 'X-Windows must be running!'
                usage()
            if standalone['open_settings']:
                try:
                    kweb = subprocess.Popen(['gksudo','kweb -ISAHMCU0+-zbhrqfpok file:///usr/local/share/kweb/kweb_about_s.html'])
                    (res,err) = kweb.communicate()
                except:
                    pass
                standalone['open_settings'] = False
                if settings and os.path.exists(settings):
                    try:
                        execfile(settings)
                    except:
                        pass
            else:
                break
        if server:
            stop_server()
        try:
            sys.exit(0)
        except:
            pass
    else:
       usage() 
