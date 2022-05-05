#!/usr/bin/env python
# -*- coding: utf-8 -*-

# youtube-dl-server
# This program is part of the Minimal Kiosk Browser (kweb) system.
# It's main purpose is to supply a faster method to extract web video URLs
# for use with omxplayerGUI and kweb(3)
# version 1.7.0

# This program was inspired by
# https://github.com/jaimeMF/youtube-dl-api-server
# and uses a small part of it's code

# Copyright 2015-2016 by Guenter Kreidl
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import os,sys,time,BaseHTTPServer,signal,subprocess,threading
from SocketServer import ThreadingMixIn
from urllib import unquote
ytdldir = os.path.expanduser('~')+os.sep+'youtube-dl'
if os.path.exists(ytdldir):
    sys.path.insert(0,ytdldir)
try:
    import youtube_dl
except:
    print "No github youtube-dl version found."
    print "Use ginstall-ytdl to install it."
    sys.exit(0)

# overwritten by kwebhelper_settings:
ytdl_server_port = '9192'
ytdl_server_host = 'localhost'
ytdl_server_format = 'best'

settings = '/usr/local/bin/kwebhelper_settings.py'
ytdl_params = {'format': ytdl_server_format,'cachedir': False, 'quiet':True}
ydl = None
port = int(ytdl_server_port)

index_page = u'''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html><head><meta content="text/html; charset=UTF-8" http-equiv="content-type">
<meta http-equiv="cache-control" content="max-age=0" />
<meta http-equiv="cache-control" content="no-cache" />
<meta http-equiv="expires" content="0" />
<meta http-equiv="expires" content="Tue, 01 Jan 1980 1:00:00 GMT" />
<meta http-equiv="pragma" content="no-cache" />
<title>youtube-dl server</title></head><body>
<h3>Youtube-dl-Server</h3>
<form enctype="application/x-www-form-urlencoded"  method="get" action="/redir">Enter Video Website URL:<br>
  <input size="50" name="url"><br>
  <input value="Extract &amp; Play" type="submit"><br>
</form>
<a href="/"><button>Clear</button></a>
<br><br><a href="stop"><button>Stop Server</button></a>
</body></html>'''

play_page = u'''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html><head><meta content="text/html; charset=UTF-8" http-equiv="content-type">
<meta http-equiv="cache-control" content="max-age=0" />
<meta http-equiv="cache-control" content="no-cache" />
<meta http-equiv="expires" content="0" />
<meta http-equiv="expires" content="Tue, 01 Jan 1980 1:00:00 GMT" />
<meta http-equiv="pragma" content="no-cache" />
<title>youtube-dl server: play</title></head><body>
<h3>$$play$$</h3>
<a href="javascript:history.back()"><button>Go Back</button></a>
</body></html>'''

class SimpleYDL(youtube_dl.YoutubeDL):
    def __init__(self, *args, **kargs):
        super(SimpleYDL, self).__init__(*args, **kargs)
        self.add_default_info_extractors()

def flatten_result(result):
    r_type = result.get('_type', 'video')
    if r_type == 'video':
        videos = [result]
    elif r_type == 'playlist':
        videos = []
        for entry in result['entries']:
            videos.extend(flatten_result(entry))
    elif r_type == 'compat_list':
        videos = []
        for r in result['entries']:
            videos.extend(flatten_result(r))
    return videos

def  start_player(url):
    player = subprocess.call(['omxplayergui',url])

def play_video(url):
    t = threading.Timer(0,start_player,args=[url])
    t.daemon = True
    t.start()

def get_video(url,firsturi=False):
    global ydl
    res = u''
    try:
        info = ydl.extract_info(url, download=False)
        videos = flatten_result(info)
        if firsturi:
            if videos[0].has_key('url'):
                res = videos[0]['url']
        else:
            for v in videos:
                if v.has_key('title'):
                    res += v['title']+'\n' 
                if v.has_key('url'):
                    res += v['url']+'\n'
    except:
         pass
    return res.strip('\n')
    
def usage():
    print "ytdl_server.py [-p=port] [-f=formatstring]"

class ytdlHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    global server_running
    protocol_version = 'HTTP/1.1'
    def do_GET(s):
        rstring = u''
        redir = False
        stop = False
        path = s.path
        ctype = "text/plain"
        if not path:
            path = '/index'
        if path in ['/','/index','/index.html']:
            rstring = index_page
            ctype = "text/html"
        elif path == '/running':
           rstring = 'OK'
        elif path == '/stop':
            rstring = 'Shutting down server'
            stop = True
        elif path.startswith('/info?url='):
            url = unquote(path.replace('/info?url=','',1))
            if url and 'http' in url and '://' in url:
                rstring = get_video(url)
        elif path.startswith('/play?url='):
            url = unquote(path.replace('/play?url=','',1))
            if url and 'http' in url and '://' in url:
                uri = get_video(url,firsturi=True)
                if uri:
                    play_video(uri)
                    rstr = "Starting video ...."
                else:
                    rstr = "No video found!"
                rstring = play_page.replace('$$play$$',rstr).replace('$$uri$$',url)
                ctype = "text/html"
        elif path.startswith('/redir?url='):
            url = unquote(path.replace('/redir?url=','',1))
            if url and 'http' in url and '://' in url:
                rstring = get_video(url,firsturi=True)
                redir = True
        if rstring:
            if redir:
                s.send_response(302)
                s.send_header("Content-Length", "0")
                s.send_header("Location",rstring)
                s.end_headers()
                s.wfile.write('')
            else:
                s.send_response(200)
                s.send_header("Content-Type", ctype)
                out = rstring.encode('utf-8')
                s.send_header("Content-Length", str(len(out)))
                s.end_headers()
                s.wfile.write(out)
        else:
            s.send_response(404)
            s.send_header("Content-Type", ctype)
            s.send_header("Content-Length", '0')
            s.end_headers()
        if stop:
            time.sleep(0.5)
            print "Shutting down server"
            os.kill(os.getpid(), signal.SIGKILL)

class MultiThreadedHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass

if os.path.exists(settings):
    try:
        execfile(settings)
    except:
        pass
try:
    port = int(ytdl_server_port)
except:
    pass
if ytdl_server_format:
    ytdl_params['format'] = ytdl_server_format

if len(sys.argv) > 1:
    for opt in sys.argv[1:]:
        if opt in ['-h','--help']:
            usage()
            sys.exit(0)
        elif opt.startswith('-p='):
            pt = opt.replace('-p=','',1)
            if pt:
                try:
                    port = int(pt)
                except:
                    pass
        elif opt.startswith('-f='):
            fm = opt.replace('-f=','',1)
            if fm:
                ytdl_params['format'] = fm

print "Starting youtube-dl-server on port " + str(port)
ydl = SimpleYDL(ytdl_params)
server_address = ('', port)
try:
    httpd = MultiThreadedHTTPServer(server_address,ytdlHandler)
except:
    print 'There is already a server instance running'
    sys.exit(0)
httpd.serve_forever()
