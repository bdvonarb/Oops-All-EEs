#!/usr/bin/env python
# -*- coding: utf-8 -*-

# set kwebhelper_settings.py values and create an HTML config page from it
# generate :command pages and more
# part of Minimal Kiosk Browser suite

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

import os,sys,shutil,urllib
global_vars = ['dldir', 'pdfprog', 'pdfoptions', 'pdfpathreplacements',
               'show_download_in_terminal', 'wget_options', 'uget_options', 'check_desktop', 'direct_commands', 'preferred_terminal', 'sudo_requires_password', 'run_as_script', 'config_path',
               'omxoptions', 'omx_livetv_options', 'live_tv', 'mimetypes', 'omxplayer_in_terminal_for_video', 'omxplayer_in_terminal_for_audio', 'audioextensions', 'streammode', 'videoextensions', 'useAudioplayer', 'omxaudiooptions', 'defaultaudiovolume', 'autoplay', 'autofinish', 'fontname', 'fontheight', 'maxlines', 'lwidth',
               'useVideoplayer', 'videoheight', 'screenmode', 'videomode', 'freeze_window', 'get_DAR', 'hide_controls', 'useVLC',
               'preferred_html5_video_format', 'html5_first', 'youtube_dl_options', 'youtube_omxoptions','use_ytdl_server'
               'ytdl_server_port','ytdl_server_host','ytdl_server_format']

methods = {'dldir':{'text': '', 'method': 'str', 'method_data': []},
'pdfprog':{'text': '', 'method': 'str', 'method_data': ['','evince','xpdf','mupdf']},
'pdfoptions':{'text': '', 'method': 'list', 'method_data': []},
'pdfpathreplacements':{'text': '', 'method': 'dict', 'method_data': []},
'show_download_in_terminal':{'text': '', 'method': 'bool', 'method_data': []},
'wget_options':{'text': '', 'method': 'list', 'method_data': []},
'uget_options':{'text': '', 'method': 'list', 'method_data': []},
'check_desktop':{'text': '', 'method': 'bool', 'method_data': []},
'direct_commands':{'text': '', 'method': 'list', 'method_data': []},
'preferred_terminal':{'text': '', 'method': 'str', 'method_data': []},
'sudo_requires_password':{'text': '', 'method': 'bool', 'method_data': []},
'run_as_script':{'text': '', 'method': 'bool', 'method_data': []},
'config_path':{'text': '', 'method': 'str', 'method_data': []},
'omxoptions':{'text': '', 'method': 'list', 'method_data': []},
'omx_livetv_options':{'text': '', 'method': 'list', 'method_data': []},
'live_tv':{'text': '', 'method': 'list', 'method_data': []},
'mimetypes':{'text': '', 'method': 'list', 'method_data': []},
'omxplayer_in_terminal_for_video':{'text': '', 'method': 'bool', 'method_data': []},
'omxplayer_in_terminal_for_audio':{'text': '', 'method': 'bool', 'method_data': []},
'audioextensions':{'text': '', 'method': 'list', 'method_data': []},
'streammode':{'text': '', 'method': 'str', 'method_data': ['audio','video']},
'videoextensions':{'text': '', 'method': 'list', 'method_data': []},
'useAudioplayer':{'text': '', 'method': 'bool', 'method_data': []},
'omxaudiooptions':{'text': '', 'method': 'list', 'method_data': []},
'defaultaudiovolume':{'text': '', 'method': 'int', 'method_data': range(-20,5)},
'autoplay':{'text': '', 'method': 'bool', 'method_data': []},
'autofinish':{'text': '', 'method': 'bool', 'method_data': []},
'fontname':{'text': '', 'method': 'str', 'method_data': []},
'fontheight':{'text': '', 'method': 'int', 'method_data': []},
'maxlines':{'text': '', 'method': 'int', 'method_data': range(5,26)},
'lwidth':{'text': '', 'method': 'int', 'method_data': range(40,81)},
'useVideoplayer':{'text': '', 'method': 'bool', 'method_data': []},
'videoheight':{'text': '', 'method': 'int', 'method_data': []},
'screenmode':{'text': '', 'method': 'str', 'method_data': ['min','max','full']},
'videomode':{'text': '', 'method': 'str', 'method_data': []},
'freeze_window':{'text': '', 'method': 'bool', 'method_data': []},
'get_DAR':{'text': '', 'method': 'bool', 'method_data': []},
'hide_controls':{'text': '', 'method': 'bool', 'method_data': []},
'useVLC':{'text': '', 'method': 'bool', 'method_data': []},
'preferred_html5_video_format':{'text': '', 'method': 'str', 'method_data': []},
'html5_first':{'text': '', 'method': 'bool', 'method_data': []},
'youtube_dl_options':{'text': '', 'method': 'list', 'method_data': []},
'youtube_omxoptions':{'text': '', 'method': 'list', 'method_data': []},
'use_ytdl_server':{'text': '', 'method': 'bool', 'method_data': []},
'ytdl_server_port':{'text': '', 'method': 'str', 'method_data': []},
'ytdl_server_host':{'text': '', 'method': 'str', 'method_data': []},
'ytdl_server_format':{'text': '', 'method': 'str', 'method_data': []} }

preset_patch = '''# Use youtube-dl-server, if possible; also required for autostart from the frontend
use_ytdl_server = True
# Port on which youtube-dl-server is running
# you should only change this, if the port is used by another application
ytdl_server_port = '9192'
# Host name or IP of youtube-dl-server.
# Only change this, if you want to use one server for many clients.
# If not 'localhost', this will also prevent autostart from the frontend
ytdl_server_host = 'localhost'
# Format string to be used by youtube-dl-server.In case of missing audio, you might change this to:
# best[protocol!=?m3u8][protocol!=?m3u8_native]
ytdl_server_format = 'best'
'''

default_template = u'''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html><head>
<meta content="text/html; charset=UTF-8" http-equiv="content-type">
<meta http-equiv="cache-control" content="max-age=0" />
<meta http-equiv="cache-control" content="no-cache" />
<meta http-equiv="expires" content="0" />
<meta http-equiv="expires" content="Tue, 01 Jan 1980 1:00:00 GMT" />
<meta http-equiv="pragma" content="no-cache" />
<!--forward-->
<!--title-->
<!--style-->
</head><body>
<!--content-->
</body></html>
'''

header = u'''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html><head>
<meta content="text/html; charset=UTF-8" http-equiv="content-type">
<title>kweb :$title$</title>
<meta http-equiv="cache-control" content="max-age=0" />
<meta http-equiv="cache-control" content="no-cache" />
<meta http-equiv="expires" content="0" />
<meta http-equiv="expires" content="Tue, 01 Jan 1980 1:00:00 GMT" />
<meta http-equiv="pragma" content="no-cache" />
<link rel="stylesheet" type="text/css" href="file:///usr/local/share/kweb/about.css">
</head><body>
'''
header2=u'''<table widht="100%"><tr><td>
<h2>kwebhelper and omxplayerGUI settings</h2></td><td>
<form accept-charset="utf-8" enctype="application/x-www-form-urlencoded" method="get" action="file:///homepage.html" name="gksettings">
<input name="cmd" value="formdata" type="hidden">
<input name="gsudo" value="gksudo" type="hidden">
<input name="quotedset" value="kweb -ISAHMU0+-zbhrqfpok file:///usr/local/share/kweb/kweb_about_s.html" type="hidden">
<input value="Edit as root" type="submit"></form></td></tr></table>
<hr>
<b>Available Presets: </b> $presetlinks$
<hr>
Your current settings are shown below and you can modify every single one of them.<br>
All changes take effect immediately. Check the manual for a detailed explanation of all options.<br><br>
'''

formheader = u'''
<form accept-charset="utf-8" enctype="application/x-www-form-urlencoded" method="get" action="file:///homepage.html" name="$name$form">
<input name="cmd" value="formdata" type="hidden">
<input name="sudo" value="sudo" type="hidden">
<input name="set" value="kwebhelper_set.py" type="hidden">
<input name="name" value="$name$" type="hidden">
'''

editorfooter = u'''<b>You can create your own editable :command pages</b><br>
<form accept-charset="utf-8" enctype="application/x-www-form-urlencoded" method="get" action="file:///homepage.html" name="create">
<input name="cmd" value="formdata" type="hidden">
<input name="sudo" value="gksudo" type="hidden">
<input name="set" value="kweb_edit.py" type="hidden">
<input name="proc" value="about" type="hidden">
<input value="Create Command" type="submit"> Name: <input name="quoteds" type="text" size="10" value="">
</form>
Reload this page after creating or deleting a :command page.
<hr>
<h2>Keyboard Command Editor</h2>
<form accept-charset="utf-8" enctype="application/x-www-form-urlencoded"
method="get" action="file:///homepage.html" name="create">
<input name="cmd" value="formdata" type="hidden">
<input name="sudo" value="sudo" type="hidden">
<input name="set" value="kwebhelper_set.py" type="hidden">
<input name="proc" value="createkbd" type="hidden">
Select Keyboard Shortcut:
<select name="kbd">
<option>1</option>
<option>2</option>
<option>3</option>
<option>4</option>
<option>5</option>
<option>6</option>
<option>7</option>
<option>8</option>
<option>9</option>
<option>0</option>
<option>autoconfig</option>
</select>
<br>
Enter up to 4 URLs, keyboard or text commands or command lines:<br>
<input name="quoted1" size="40" value="" type="text"><br>
<input name="quoted2" size="40" value="" type="text"><br>
<input name="quoted3" size="40" value="" type="text"><br>
<input name="quoted4" size="40" value="" type="text"><br>
<input value="Create KBD Command" type="submit">
</form>
By sending an empty form the command will be disabled.<br>
The first URL will be used for redirection. All other URLs will be opened in a new window.<br>
<b>Keyboard commands:</b><br>
?value<br>
Value may be any combination of the following keyboard shortcuts: +-zfkmcqgteduwxy<br>
<b>Possible text commands:</b><br>
)URL&nbsp;&nbsp;&nbsp; (open URL in new window)<br>
))URL&nbsp;&nbsp;&nbsp; (open URL in new browser instance)<br>
$user agent string (no argument = default)<br>
!spellchecking language (e.g. "en_GB")<br>
@encoding (set default encoding, no argument = utf-8)<br>
<b>Command Lines:</b><br>
A command line should be entered like in a terminal. You may use it to start any external program.<br>
The autoconfig command will be executed when the browser starts.<br>
You'll find more information and some examples in the manual.<br>
<form accept-charset="utf-8" enctype="application/x-www-form-urlencoded"
method="get" action="file:///homepage.html" name="edit">
<input name="cmd" value="formdata" type="hidden">
<input name="sudo" value="gksudo" type="hidden">
<input name="set" value="kweb_edit.py" type="hidden">
You can also edit the commands manually: 
<select name="kbd">
<option value="kweb1.txt">1</option>
<option value="kweb2.txt">2</option>
<option value="kweb3.txt">3</option>
<option value="kweb4.txt">4</option>
<option value="kweb5.txt">5</option>
<option value="kweb6.txt">6</option>
<option value="kweb7.txt">7</option>
<option value="kweb8.txt">8</option>
<option value="kweb9.txt">9</option>
<option value="kweb0.txt">0</option>
<option value="kwebautoconfig.txt">autoconfig</option>
</select> 
<input value="Edit" type="submit">
</form>
Test your commands: <a href="file:///homepage.html?kbd=1"><button>1</button></a> &nbsp;&nbsp; 
<a href="file:///homepage.html?kbd=2"><button>2</button></a> &nbsp;&nbsp; 
<a href="file:///homepage.html?kbd=3"><button>3</button></a> &nbsp;&nbsp; 
<a href="file:///homepage.html?kbd=4"><button>4</button></a> &nbsp;&nbsp; 
<a href="file:///homepage.html?kbd=5"><button>5</button></a> &nbsp;&nbsp; 
<a href="file:///homepage.html?kbd=6"><button>6</button></a> &nbsp;&nbsp; 
<a href="file:///homepage.html?kbd=7"><button>7</button></a> &nbsp;&nbsp; 
<a href="file:///homepage.html?kbd=8"><button>8</button></a> &nbsp;&nbsp; 
<a href="file:///homepage.html?kbd=9"><button>9</button></a> &nbsp;&nbsp; 
<a href="file:///homepage.html?kbd=0"><button>0</button></a>
</body></html>
'''

presetform = u'''<big><b>Save and Load Presets</b></big><br>
You may save the currents settings as a named preset and load them again later on.<br>
After loading a preset, you should reload this page.<br>
<table><tr><td>
<form accept-charset="utf-8" enctype="application/x-www-form-urlencoded" method="get" action="file:///homepage.html" name="presetform">
<input name="cmd" value="formdata" type="hidden">
<input name="sudo" value="sudo" type="hidden">
<input name="set1" value="kwebhelper_set.py" type="hidden">
<input name="proc" value="savepreset" type="hidden">
<input value="Save Preset" type="submit"> Name: <input name="quoteds" type="text" size="20" value="">
</form><br>
<form accept-charset="utf-8" enctype="application/x-www-form-urlencoded" method="get" action="file:///homepage.html" name="presetform">
<input name="cmd" value="formdata" type="hidden">
<input name="sudo" value="sudo" type="hidden">
<input name="set2" value="kwebhelper_set.py" type="hidden">
<input name="proc" value="deletepreset" type="hidden">
<input value="Delete Preset" type="submit"> Name: <input name="quotedd" type="text" size="20" value="">
</form></td><td><b>Load Preset:</b> $presetlinks$</td></tr></table><hr>'''

presetbutton=u'''
<a href="file:///homepage.html?cmd=sudo%20kwebhelper_set.py%20loadpreset%20$name$"><button>$name$</button></a>'''

encodingsdict = {'gb18030': ['gb18030'], 'euc-jp': ['cseucpkdfmtjapanese', 'euc-jp', 'x-euc-jp'], 'utf-16le': ['utf-16', 'utf-16le'], 'windows-1255': ['cp1255', 'windows-1255', 'x-cp1255'], 'iso-8859-8': ['csiso88598e', 'csisolatinhebrew', 'hebrew', 'iso-8859-8', 'iso-8859-8-e', 'iso-ir-138', 'iso8859-8', 'iso88598', 'iso_8859-8', 'iso_8859-8:1988', 'visual'], 'iso-8859-7': ['csisolatingreek', 'ecma-118', 'elot_928', 'greek', 'greek8', 'iso-8859-7', 'iso-ir-126', 'iso8859-7', 'iso88597', 'iso_8859-7', 'iso_8859-7:1987', 'sun_eu_greek'], 'iso-8859-6': ['arabic', 'asmo-708', 'csiso88596e', 'csiso88596i', 'csisolatinarabic', 'ecma-114', 'iso-8859-6', 'iso-8859-6-e', 'iso-8859-6-i', 'iso-ir-127', 'iso8859-6', 'iso88596', 'iso_8859-6', 'iso_8859-6:1987'], 'iso-8859-5': ['csisolatincyrillic', 'cyrillic', 'iso-8859-5', 'iso-ir-144', 'iso8859-5', 'iso88595', 'iso_8859-5', 'iso_8859-5:1988'], 'iso-8859-4': ['csisolatin4', 'iso-8859-4', 'iso-ir-110', 'iso8859-4', 'iso88594', 'iso_8859-4', 'iso_8859-4:1988', 'l4', 'latin4'], 'iso-8859-3': ['csisolatin3', 'iso-8859-3', 'iso-ir-109', 'iso8859-3', 'iso88593', 'iso_8859-3', 'iso_8859-3:1988', 'l3', 'latin3'], 'iso-8859-2': ['csisolatin2', 'iso-8859-2', 'iso-ir-101', 'iso8859-2', 'iso88592', 'iso_8859-2', 'iso_8859-2:1987', 'l2', 'latin2'], 'iso-2022-jp': ['csiso2022jp', 'iso-2022-jp'], 'x-user-defined': ['x-user-defined'], 'utf-16be': ['utf-16be'], 'utf-8': ['unicode-1-1-utf-8', 'utf-8', 'utf8'], 'windows-874': ['dos-874', 'iso-8859-11', 'iso8859-11', 'iso885911', 'tis-620', 'windows-874'], 'x-mac-cyrillic': ['x-mac-cyrillic', 'x-mac-ukrainian'], 'ibm866': ['866', 'cp866', 'csibm866', 'ibm866'], 'euc-kr': ['cseuckr', 'csksc56011987', 'euc-kr', 'iso-ir-149', 'korean', 'ks_c_5601-1987', 'ks_c_5601-1989', 'ksc5601', 'ksc_5601', 'windows-949'], 'iso-8859-16': ['iso-8859-16'], 'iso-8859-15': ['csisolatin9', 'iso-8859-15', 'iso8859-15', 'iso885915', 'iso_8859-15', 'l9'], 'iso-8859-14': ['iso-8859-14', 'iso8859-14', 'iso885914'], 'iso-8859-13': ['iso-8859-13', 'iso8859-13', 'iso885913'], 'windows-1258': ['cp1258', 'windows-1258', 'x-cp1258'], 'iso-8859-10': ['csisolatin6', 'iso-8859-10', 'iso-ir-157', 'iso8859-10', 'iso885910', 'l6', 'latin6'], 'windows-1256': ['cp1256', 'windows-1256', 'x-cp1256'], 'windows-1257': ['cp1257', 'windows-1257', 'x-cp1257'], 'windows-1254': ['cp1254', 'csisolatin5', 'iso-8859-9', 'iso-ir-148', 'iso8859-9', 'iso88599', 'iso_8859-9', 'iso_8859-9:1989', 'l5', 'latin5', 'windows-1254', 'x-cp1254'], 'iso-8859-8-i': ['csiso88598i', 'iso-8859-8-i', 'logical'], 'windows-1252': ['ansi_x3.4-1968', 'ascii', 'cp1252', 'cp819', 'csisolatin1', 'ibm819', 'iso-8859-1', 'iso-ir-100', 'iso8859-1', 'iso88591', 'iso_8859-1', 'iso_8859-1:1987', 'l1', 'latin1', 'us-ascii', 'windows-1252', 'x-cp1252'], 'windows-1253': ['cp1253', 'windows-1253', 'x-cp1253'], 'windows-1250': ['cp1250', 'windows-1250', 'x-cp1250'], 'windows-1251': ['cp1251', 'windows-1251', 'x-cp1251'], 'koi8-u': ['koi8-ru', 'koi8-u'], 'gbk': ['chinese', 'csgb2312', 'csiso58gb231280', 'gb2312', 'gb_2312', 'gb_2312-80', 'gbk', 'iso-ir-58', 'x-gbk'], 'koi8-r': ['cskoi8r', 'koi', 'koi8', 'koi8-r', 'koi8_r'], 'big5': ['big5', 'big5-hkscs', 'cn-big5', 'csbig5', 'x-x-big5'], 'shift_jis': ['csshiftjis', 'ms932', 'ms_kanji', 'shift-jis', 'shift_jis', 'sjis', 'windows-31j', 'x-sjis'], 'replacement': ['csiso2022kr', 'hz-gb-2312', 'iso-2022-cn', 'iso-2022-cn-ext', 'iso-2022-kr'], 'macintosh': ['csmacintosh', 'mac', 'macintosh', 'x-mac-roman']}

predefined_names = ['c','s','e','k','o','p','m']
predefined_editables = ['a','b','u']

editable_defaults = {'b':u'''#!mode=link
#!spacer= &nbsp;&nbsp; 
#!target=top
#!pagetitle=Bookmarks
#<h2>Bookmarks</h2>
Raspberry Pi Forum=https://www.raspberrypi.org/forum
Omxplayer Download=http://omxplayer.sconde.net/
Youtube=https://www.youtube.com/
''',
'a':u'''#!mode=button
#!spacer= &nbsp;&nbsp; 
#!target=
#!pagetitle=Applications and Commands
#<h2>Applications and Commands</h2>
#<h6>Basic Applications</h6>
Terminal=lxterminal
Editor=leafpad
File Manager=pcmanfm
OmxplayerGUI=omxplayergui
Package Manager=pi-packages
Synaptic=gksudo synaptic
Taskmanager=lxtask
Appearance=lxappearance
OpenBox Configuration=obconf
Python Editor=idle
#<h6>Useful Commands</h6>
Top=top
Reboot=sudo reboot
Shutdown=sudo shutdown -h now
Update=sudo apt-get update
Upgrade=sudo apt-get upgrade
#<h6>Youtube-dl Tools</h6>
Install (Git)=ginstall-ytdl
Update (Git)=update-ytdl
Create Binary=makebin-ytdl
Start Server=ytdl_server.py
Start Server (no HLS)=ytdl_server.py -f=best[protocol!=?m3u8][protocol!=?m3u8_native]
Stop Server=http://localhost:9192/stop
Open Server=http://localhost:9192/
''','u':'''#!mode=button
#!spacer= &nbsp;&nbsp; 
#!target=
#!pagetitle=Browser Utilities
#<h2>Browser Utilities</h2>
#<h6>Themes</h6>
White=sudo cp /usr/local/share/kweb/white.css /usr/local/share/kweb/about.css
Black=sudo cp /usr/local/share/kweb/black.css /usr/local/share/kweb/about.css
Grey=sudo cp /usr/local/share/kweb/grey.css /usr/local/share/kweb/about.css
User=sudo cp /usr/local/share/kweb/user.css /usr/local/share/kweb/about.css
#<h6>User Agents</h6>
Default Kweb=$
Empty (-)=$-
Firefox Mobile=$Mozilla/5.0 (Android; Tablet; rv:36.0) Gecko/36.0 Firefox/36.0
Firefox Desktop=$Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:43.0) Gecko/20100101 Firefox/43.0
Chrome Desktop=$Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36
#<h6>Spell Checking Languages</h6>
English (UK)=!en_GB
English (US)=!en_US
German (DE)=!de_DE
#<h6>Default Encodings</h6>
UTF-8 (default)=@
Latin 1=#@windows-1252
#<h6>User Style Sheets</h6>
Default (none)=&
Color=&file:///usr/local/share/kweb/color.css
#<h6>Browser Commands</h6>
Toggle Fullscreen=?f
Show/Hide Toolbar=?k
Quit Browser=?q
#<h6>User Defined Keyboard Commands</h6>
1=?1
2=?2
3=?3
4=?4
5=?5
6=?6
7=?7
8=?8
9=?9
0=?0'''}
aboutheader = u'''#!mode=mixed
#!spacer=
#!target=top
#!pagetitle=
#<h2>Untitled</h2>
'''
about_delete_button = u'<a href="file:///homepage.html?cmd=sudo%20kwebhelper_set.py%20deleteabout%20$name$"><button>Delete</button></a>'
about_edit_button = u'<a href="file:///homepage.html?cmd=gksudo%20kweb_edit.py%20about%20$name$"><button>Edit</button></a>'
about_html_footer = u'<hr>' + about_edit_button + '</body></html>'

def create_form_body(name,value):
    output = u''
    output += '<b>'+name+':</b> '
    method = methods[name]['method']
    if methods[name]['text']:
        output += methods[name]['text'] + '<br>'
    if method == 'int':
        elem = '<input name="var$name$" type="text" size="4" value="$value$">'
        output += elem.replace('$name$',name).replace('$value$',value)
    elif method == 'str':
        evalue = value.strip('\'')
        if evalue:
            size = len(evalue)+4
        else:
            size = 25
        elem = '<input name="quotedvar$name$" type="text" size="$size$" value="$value$">'
        output += elem.replace('$name$',name).replace('$value$',evalue).replace('$size$',str(size))
    elif method == 'bool':
        elem = '<input type="radio" name="var$name$" value="True">True'
        elem += ' <input type="radio" name="var$name$" value="False">False'
        if value == 'True':
            elem = elem.replace('"True"','"True" checked')
        else:
            elem = elem.replace('"False"','"False" checked')            
        output += elem.replace('$name$',name)
    elif method == 'list':
        output += 'Enter one element per line!<br>'
        evalue = eval(value)
        if len(evalue) == 0:
            rows = 3
            cols = 25
        else:
            rows = max(min(8,len(evalue)),5)
            cols = 0
            for e in evalue:
                if len(e) > cols:
                    cols = len(e)
            cols = cols+4
        elem = '<textarea name="quoted$name$" cols="$cols$" rows="$rows$">'
        elem = elem.replace('$name$',name)
        elem = elem.replace('$rows$',str(rows))
        elem = elem.replace('$cols$',str(cols))
        txt  = ''
        if evalue:
            txt = '\n'.join(evalue)
        output += elem+txt+'</textarea>'
    elif method == 'dict':
        output += 'Enter one element per line in the form value1=value2<br>'
        evalued = eval(value)
        evalue = []
        for k,v in evalued.iteritems():
            evalue.append(k+'='+v)
        if len(evalue) == 0:
            rows = 3
            cols = 40
        else:
            rows = max(min(8,len(evalue)),5)
            cols = 0
            for e in evalue:
                if len(e) > cols:
                    cols = len(e)
            cols = cols+4
        elem = '<textarea name="quoted$name$" cols="$cols$" rows="$row$">'
        elem = elem.replace('$name$',name)
        elem = elem.replace('$rows$',str(rows))
        elem = elem.replace('$cols$',str(cols))
        txt  = ''
        if evalue:
            txt = '\n'.join(evalue)
        output += elem+txt+'</textarea>'
    return output

def set_value(name,value):
    method = methods[name]['method']
    save_list = False
    for lnr in range(0,len(settingslist)):
        if settingslist[lnr].startswith(name+' ') or settingslist[lnr].startswith(name+'='):
            break
    if method == 'int':
        if value:
            try:
                val = int(value)
            except:
                val = ''
        if val and methods[name]['method_data']:
            if val not in methods[name]['method_data']:
                val = ''
        if val:
            settingslist[lnr] = name + ' = ' + str(val)
            save_list = True            
    elif method == 'str':
        save_list = True
        if methods[name]['method_data']:
            if value not in methods[name]['method_data']:
                save_list = False
        if value:
            val = '\''+value+'\''
        else:
            val = "''"
        if save_list:
            settingslist[lnr] = name + ' = ' + str(val)
    elif method == 'bool':
        if value and value in ['False','True']:
            settingslist[lnr] = name + ' = ' + value
            save_list = True
    elif method == 'list':
        if value:
            val = value.replace('%0A','').split('%0D')
        else:
            val = []
        val2 = []
        for v in val:
            nv = v.strip()
            if ' ' in nv and "'" not in nv and '"' not in nv:
                val2 = val2 + nv.split(' ')
            else:
                val2.append(nv)            
        save_list = True
        settingslist[lnr] = name + ' = ' + str(val2)        
    elif method == 'dict':
        if value:
            val = value.replace('%0A','').split('%0D')
            vad = {}
            for v in val:
                if '=' in v:
                    vd = v.strip().split('=')
                    vad[vd[0]] = vd[1]
        else:
            vad = {}
        save_list = True
        settingslist[lnr] = name + ' = ' + str(vad)
    if save_list:
        f = file(settingspath,'wb')
        f.write(('\n'.join(settingslist)).encode('utf-8'))
        f.close()
        os.chmod(settingspath,0755)
    return save_list

def create_presetlinks():
    res = ''
    presetfiles = os.listdir(spagepath)
    presetfiles.sort()
    for prf in presetfiles:
        name = prf.replace('.preset','')
        if prf.endswith('.preset'):
            res += presetbutton.replace('$name$',name)
    return res

def create_settings_page(settingslist):
    presetlinks = create_presetlinks()
    page = header.replace('$title$','settings')
    page += header2.replace('$presetlinks$',presetlinks)
    for line in settingslist[9:-1]:
        if line.startswith('#'):
            if line.startswith('# '):
                page += line.replace('#','').strip()+'<br>\n'
        elif '=' in line:
            ll = line.split('=')
            name = ll[0].strip()
            value = ll[1].strip()
            page += formheader.replace('$name$',name)
            page += create_form_body(name,value)
            page += ' <input value="save" type="submit">' 
            page += '</form><hr>'
    page += presetform.replace('$presetlinks$',presetlinks)
    page += '</body></html>'
    f = file(about_s_path,'wb')
    f.write(page.encode('utf-8'))
    f.close()
    os.chmod(about_s_path,0644)

def preset(cmd, name):
    global settingslist
    result = False
    presetpath = spagepath+'/'+name+'.preset'
    if cmd == 'savepreset':
        shutil.copy(settingspath,presetpath)
        result = True
    elif cmd == 'loadpreset':
        if os.path.exists(presetpath):
            shutil.copy(presetpath,settingspath)
            result = True
            settingslist = load_settings()
    elif cmd == 'deletepreset':
        if os.patch.exists(presetpath):
            os.remove(resetpath)
    return result

def get_command_names():
    fixed = [] + predefined_names
    editable = [] + predefined_editables
    basedir = '/usr/local/share/kweb'
    kwebcontent = os.listdir(basedir)
    for cont in kwebcontent:
        if cont.startswith('kweb_about_') and '.' in cont:
            name = cont.split('.')[0].replace('kweb_about_','')
            if cont.endswith('.txt'):
                if name not in editable:
                    editable.append(name)
            elif cont.endswith('.html'):
                if os.path.exists(basedir+'/'+cont.replace('.html','.txt')):
                    if name not in editable:
                        editable.append(name)
                else:
                    if name not in fixed:
                        fixed.append(name)
    return (fixed,editable)

def about_commands(cmd,name):
    sname = name.strip(' :')
    sname = sname.replace(' ','_')
    rlist = []
    refresh_editor = False
    fixed, editable = get_command_names()
    if cmd == 'deleteabout':
        if sname in editable and sname not in predefined_editables:
            bp = '/usr/local/share/kweb/kweb_about_'+sname
            if os.path.exists(bp+'.txt'):
                os.remove(bp+'.txt')
            if os.path.exists(bp+'.html'):
                os.remove(bp+'.html')
            refresh_editor = True
    elif cmd == 'refreshabout':
        if sname in editable:
            rlist.append(sname)
            if not os.path.exists('/usr/local/share/kweb/kweb_about_'+sname+'.html'):
                refresh_editor = True
    elif cmd == 'createabout':
        if sname not in editable and sname not in fixed:
            bp = '/usr/local/share/kweb/kweb_about_'+sname+'.txt'
            if not os.path.exists(bp):
                f = file(bp,'wb')
                f.write(aboutheader.encode('utf-8'))
                f.close()
                os.chmod(bp,0644)
                refresh_editor = True
                rlist.append(name)
    return refresh_editor,rlist

def create_about_pages(ablist):
    global editor_refresh
    for name in ablist:
        bp = '/usr/local/share/kweb/kweb_about_'+name+'.txt'
        if not os.path.exists(bp) and name in predefined_editables:
            f = file(bp,'wb')
            f.write(editable_defaults[name].encode('utf-8'))
            f.close()
            os.chmod(bp,0644)
        if os.path.exists(bp):
            template = default_template.replace('</body></html>',about_html_footer.replace('$name$',name))
            html = text2html(bp,template,css='file:///usr/local/share/kweb/about.css',pagetitle=':'+name)
            html.create()

def create_editor_page():
    epath = '/usr/local/share/kweb/kweb_about_e.html'
    linkform = u'<a href="file:///usr/local/share/kweb/kweb_about_$name$.html" target="_top">:$name$</a>'
    static,editable = get_command_names()
    spacer = u' &nbsp;&nbsp; '
    page = header.replace('$title$',':Command and Keyboard Command Editor')
    page += u'<h2>:command Editor</h2>'
    page += u'<b>Available Static :Command Pages</b><br>'+spacer
    for name in static:
        if name != 'c':
            page += linkform.replace('$name$',name)+spacer
        else:
            page += u'<a href="file://~/kweb_about_c.html" target="_top">:c</a>' +spacer
    page += u'<br><br><b>Available User Editable :Command Pages</b><br>'
    for name in editable:
        page += spacer+linkform.replace('$name$',name)+spacer
        page += about_edit_button.replace('$name$',name)+spacer
        if name not in predefined_editables:
            page += about_delete_button.replace('$name$',name)
        page += '<br>'
    page += editorfooter
    f = file(epath,'wb')
    f.write(page.encode('utf-8'))
    f.close()
    os.chmod(epath,0644)

def load_settings():
    if os.path.exists(settingspath):
        f = file(settingspath,'rb')
        settings = f.read().decode('utf-8')
        f.close()
        return settings.split('\n')
    else:
        return []

def checkspellings(spellings):
    return spellings

def checkencoding(encoding):
    if encoding in encodingsdict.keys():
        return encoding
    else:
        ret = ''
        for k,v in encodingsdict.iteritems():
            if encoding in v:
                ret = k
                break
        return ret

class text2html:
    def __init__(self,textpath,template,spacer=' ',mode='mixed',target='',css='',cssinclude=False,forward='',fwtime='0',pagetitle='',iframew='2',iframeh='2',imgw='',imgh=''):
        self.name = os.path.basename(textpath)
        self.path = os.path.dirname(textpath)
        self.template = template
        self.spacer = spacer
        self.mode = mode
        self.target = 'target="_'+target+'"'
        self.css = css
        self.cssinclude = cssinclude
        self.forward = forward
        self.fwtime = fwtime
        self.pagetitle = pagetitle
        self.iframew = iframew
        self.iframeh = iframeh
        self.imgw = imgw
        self.imgh = imgh
        self.title = ''
        self.output = ''
        self.collect = ''
        self.cmd_uri='file:///homepage.html?$type$='
        self.linkform = u'<a href="$link$" $target$ $title$">$name$</a>'
        self.cmdform = u'<a href="file:///homepage.html?cmd=$cmd$" $title$>$name$</a>'
        self.txtform = u'<a href="file:///homepage.html?txt=$cmd$" $title$>$name$</a>'
        self.kbdform = u'<a href="file:///homepage.html?kbd=$cmd$" $title$>$name$</a>'
        self.hiddenform = u'<iframe src="$uri$" width="$width$" height="$height$" name="$name$"></iframe>'
        self.text = self.load_file(os.path.join(self.path,self.name))

    def convert_name(self,name,mode):
        res = name
        if name.lower().split('.')[-1] in ['jpg','gif','png','ico']:
            if name.startswith('/'):
                name = 'file://'+name
            res = '<img src="' +name + '" style="'
            if self.imgw:
                res += 'width: '+self.imgw+';'
            if self.imgh:
                res += 'height: '+self.imgh+';'
            res += '"></img>'
        elif mode == 'button':
            res = '<button>'+name+'</button>'
        return res

    def cmd2uri(self,cmdline):
        quoter = ''
        newcmd = ''
        carr = []
        for c in cmdline:
            if not quoter:
                if c in ['"',"'"]:
                    quoter = c
                    newcmd += c
                elif c == ' ':
                    carr.append(urllib.quote_plus(newcmd))
                    newcmd = ''
                else:
                    newcmd += c
            else:
                if c == quoter:
                    quoter = ''
                    newcmd += c
                else:
                    newcmd += c
        if newcmd:
            carr.append(urllib.quote_plus(newcmd))
        return '%20'.join(carr)

    def load_file(self,path):
        res = ''
        if not path.startswith('/'):
            path = os.path.join(self.path,path)
        if os.path.exists(path):
            f = file(path,'rb')
            try:
                res = f.read().decode('utf-8')
            except:
                pass
            f.close()
        return res

    def check_link(self,link):
        if not link:
            return False
        if '://' in link and link.split('://',1)[0] in ['http','https','file','rtp','rtmp','rtsp','mmsh']:
            return True
        else:
            return False

    def create_kbd(self,name,value):
        res = ''
        kbds = ''
        if name:
            allowed_kbds = '+-zbhrqfpokgtjneduwxysacmv#0123456789'
        else:
            allowed_kbds = '+-zbhfpokgteduwxycm#q'
        if len(value) > 1:
            for ch in value[1:]:
                if ch in allowed_kbds:
                    kbds += ch
        if kbds:
            if name:
                res = self.kbdform.replace('$cmd$',kbds)
                if self.title:
                    res = res.replace('$title$','title="'+self.title+'"')
                    self.title = ''
                else:
                    res = res.replace(' $title$','')
                if self.mode == 'link':
                    mode = 'link'
                else:
                    mode = 'button'
                res = res.replace('$name$',self.convert_name(name,mode))
            else:
                uri = self.cmd_uri.replace('$type$','kbd')+kbds
                res = self.hiddenform.replace('$uri$',uri).replace('$width$',self.iframew).replace('$height$',self.iframeh).replace('$name$',self.title)
                self.title = ''
        return res

    def create_link(self,name,value):
        res = ''
        if name:
            res = self.linkform.replace('$link$',value)
            if self.target:
                res = res.replace('$target$',self.target)
            else:
                res = res.replace(' $target$','')
            if self.title:
                res = res.replace('$title$','title="'+self.title+'"')
                self.title = ''
            else:
                res = res.replace(' $title$','')
            if self.mode == 'button':
                mode = 'button'
            else:
                mode = 'link'
            res = res.replace('$name$',self.convert_name(name,mode))
        else:
            res = self.hiddenform.replace('$uri$',value).replace('$width$',self.iframew).replace('$height$',self.iframeh).replace('$name$',self.title)
            self.title = ''
        return res

    def create_cmd(self,name,value):
        res = ''
        cmd = self.cmd2uri(value)
        if name:
            res = self.cmdform.replace('$cmd$',cmd)
            if self.title:
                res = res.replace('$title$','title="'+self.title+'"')
                self.title = ''
            else:
                res = res.replace(' $title$','')
            if self.mode == 'link':
                mode = 'link'
            else:
                mode = 'button'
            res = res.replace('$name$',self.convert_name(name,mode))
        else:
            uri = self.cmd_uri.replace('$type$','cmd')+cmd
            res = self.hiddenform.replace('$uri$',uri).replace('$width$',self.iframew).replace('$height$',self.iframeh).replace('$name$',self.title)
            self.title = ''
        return res

    def create_txt(self,name,value):
        res = ''
        txt = ''
        if value.startswith('))'):
            if len(value) > 2 and self.check_link(value[2:]):
                txt = value
        elif value.startswith(')'):
            if len(value) > 1 and self.check_link(value[1:]):
                txt = value
        elif value.startswith('!'):
            if len(value)>5:
                spellings = checkspellings(value[1:])
                if spellings:
                    txt = '!' + spellings
        elif value.startswith('$'):
            if len(value) == 1:
                txt = value
            else:
                txt = '$' + urllib.quote(value[1:]).replace(' ','%20')
        elif value.startswith('@'):
            if len(value) == 1:
                txt = value
            else:
                enc = checkencoding(value[1:])
                if enc:
                    txt = '@'+enc
        elif name and value.startswith('&'):
            if len(value) == 1:
                txt = value
            else:
                cpath = value[1:]
                if cpath.startswith('file:///') and cpath.endswith('.css'):
                    txt = value.replace(' ','%20')
                elif cpath.startswith('/') and cpath.endswith('.css'):
                    txt = '&file://'+cpath.replace(' ','%20')
                elif cpath.endswith('.css'):
                    if os.path.exists(os.path.join(self.path,cpath)):
                        txt = '&file://'+os.path.join(self.path,cpath).replace(' ','%20')
        if txt:
            if name:
                res = self.txtform.replace('$cmd$',txt)
                if self.title:
                    res = res.replace('$title$','title="'+self.title+'"')
                    self.title = ''
                else:
                    res = res.replace(' $title$','')
                if self.mode == 'link':
                    mode = 'link'
                else:
                    mode = 'button'
                res = res.replace('$name$',self.convert_name(name,mode))
            else:
                uri = self.cmd_uri.replace('$type$','txt')+txt
                res = self.hiddenform.replace('$uri$',uri).replace('$width$',self.iframew).replace('$height$',self.iframeh).replace('$name$',self.title)
                self.title = ''
            return res

    def create_table(self,data):
        # data = "rows:columns:width:height:padding:valign:halign"
        tabletext =  ''
        if not ':' in data:
            return ''
        tdata = data.split(':')
        if len(tdata)== 7 and tdata[0].isdigit() and tdata[1].isdigit() and tdata[4].isdigit() and tdata[5] in ['top','middle','bottom'] and tdata[6] in ['left','center','right']:
            table = '\n<table border="0" cellspacing="0" cellpadding="' + tdata[4]+'"'
            if tdata[2] != '0':
                table += ' width="'+ tdata[2] +'"'
            if tdata[3] != '0':
                table += ' height="'+ tdata[3] +'"'
            table += '>\n'
            td = '<td style="text-align: '+tdata[6]+'; vertical-align: '+tdata[5]+'"><!--content--></td>\n'
            tabletext += table
            for rows in range(0,int(tdata[0])):
                tabletext += '<tr>\n'
                for columns in range(0,int(tdata[1])):
                    tabletext += td
                tabletext += '</tr>\n'
            tabletext += '</table>\n'
            return tabletext
        else:
            return ''
    def create(self):
        if not self.text:
            return
        for line in self.text.split('\n'):
            if not line:
                continue
            if line[0] in ['@','&']:
                continue
            if line.strip().startswith('#'):
                line = line.strip()
            if line.startswith('#!'):             
                if line.startswith('#!spacer='):
                    newspacer = line.replace('#!spacer=','')
                    self.spacer = newspacer
                elif line.startswith('#!mode='):
                    newmode = line.replace('#!mode=','').strip()
                    if newmode in ['mixed','link','button']:
                        self.mode = newmode
                elif line.startswith('#!target='):
                    newtarget = line.replace('#!target=','').strip()
                    if not newtarget or newtarget == 'this' or newtarget == 'self':
                        self.target = ''
                    elif newtarget in ['top','parent','blank']:
                         self.target = 'target="_'+newtarget+'"'
                    else:
                        self.target = 'target="'+newtarget+'"'
                elif line.startswith('#!forward='):
                    link = line.replace('#!forward=','').strip()
                    if link and self.check_link(link):
                        self.forward = link
                elif line.startswith('#!fwtime='):
                    fwtime = line.replace('#!fwtime=','').strip()
                    if fwtime:
                        try:
                            fw=float(fwtime)
                            self.fwtime = fwtime
                        except:
                            pass
                elif line.startswith('#!title='):
                    self.title = line.replace('#!title=','').strip()
                elif line.startswith('#!pagetitle='):
                    self.pagetitle = line.replace('#!pagetitle=','').strip()
                elif line.startswith('#!template='):
                    tpath = line.replace('#!template=','').strip()
                    if tpath and not self.output:
                        newtemplate = self.load_file(tpath)
                        if newtemplate:
                            self.template = newtemplate
                elif line.startswith('#!css='):
                    ncss = line.replace('#!css=','').strip()
                    if not ncss or line.lower().endswith('.css'):
                        self.css = ncss
                elif line.startswith('#!iframew='):
                    neww = line.replace('#!iframew=','').strip()
                    self.iframew = neww
                elif line.startswith('#!iframeh='):
                    newh = line.replace('#!iframeh=','').strip()
                    self.iframeh = newh
                elif line.startswith('#!imgw='):
                    nimgw = line.replace('#!imgw=','').strip()
                    if nimgw and nimgw[0] != '0':
                        self.imgw = nimgw
                    else:
                        self.imgw = ''
                elif line.startswith('#!imgh='):
                    nimgh = line.replace('#!imgh=','').strip()
                    if nimgh and nimgh[0] != '0':
                        self.imgh = nimgh
                    else:
                        self.imgh = ''
                elif line.startswith('#!cssinclude'):
                    self.cssinclude = True
                elif line.startswith('#!next'):
                    if not self.output:
                        self.output = self.template
                    self.output = self.output.replace('<!--content-->',self.collect,1)
                    self.collect = ''
                elif line.startswith('#!table='):
                    table = self.create_table(line.replace('#!table=',''))
                    if table:
                        self.collect += table
            elif line.startswith('#'):
                self.collect += line.replace('#','',1).strip() + '\n'
            elif '=' in line:
                larr = line.split('=',1)
                name = larr[0]
                value = larr[1]
                if value.startswith('#'):
                    value = value.replace('#','',1)
                newcmd = ''
                if not value:
                    continue
                if value.startswith('?'):
                    newcmd = self.create_kbd(name,value)
                elif value[0] in ['!','$','@',')','&']:
                    newcmd = self.create_txt(name,value)
                elif self.check_link(value):
                    newcmd = self.create_link(name,value)
                else:
                    newcmd = self.create_cmd(name,value)
                if newcmd:
                    self.collect += newcmd + self.spacer+'\n'
            else:
                continue
        if not self.output:
            self.output = self.template
        self.output = self.output.replace('<!--content-->',self.collect,1)
        if self.forward:
            repl = '<meta http-equiv="refresh" content="'+self.fwtime+';URL='+self.forward+'" />'
            self.output = self.output.replace('<!--forward-->',repl,1)
        else:
            self.output = self.output.replace('<!--forward-->','',1)
        if not self.pagetitle:
            self.pagetitle = self.name.split('.txt')[0]
        self.output = self.output.replace('<!--title-->','<title>'+self.pagetitle+'</title>')
        if self.css:
            if self.cssinclude:
                icss = self.load_file(self.css)
                if icss:
                    self.output = self.output.replace('<!--style-->','<style>\n'+icss+'\n</style>')
            else:
               self.output = self.output.replace('<!--style-->','<link rel="stylesheet" type="text/css" href="'+self.css+'">')
        else:
            self.output = self.output.replace('<!--style-->','',1)
        try:
            spath = os.path.join(self.path,self.name.replace('.txt','.html'))
            f = file(spath,'wb')
            f.write(self.output.encode('utf-8'))
            f.close()
        except:
            pass

def check_uri(link):
    if not link:
        return False
    if '://' in link and link.split('://',1)[0] in ['http','https','file']:
        return True
    else:
        return False

def check_kbd_args(arg):
    isuri = False
    allowed_kbds = '+-zfkqmcgteduwxy'
    if arg.startswith('#'):
        arg = arg.replace('#','',1)
    if not arg:
        return (False,'')
    if check_uri(arg):
        return (True,arg)
    elif arg.startswith('?') and len(arg) > 1:
        nk = ''
        for ch in arg[1:]:
            if ch in allowed_kbds:
                nk += ch
        if nk:
            return (False,'?'+nk)
        else:
            return (False,'')
    elif arg.startswith(')'):
        if check_uri(arg.lstrip(')')):
            return (False,arg)
        else:
            return (False,'')
    elif arg[0] == '$':
        return (False,arg)
    elif arg[0] == '!' and len(arg) > 5:
        spellings = checkspellings(value[1:])
        if spellings:
            return (False,arg)
        else:
            return (False,'')
    elif arg[0] == '@':
        if len(arg) > 0:
            enc = checkencoding(arg[1:])
            if enc:
                return (False,'@'+enc)
            else:
                return (False,'')
        else:
            return (False,arg)
    elif arg[0] not in ['!','$','@',')','&']:
        return (False,arg)
    else:
        return (False,'')

def create_kbd(kbd,args):
    allowed_kbds = ['0','1','2','3','4','5','6','7','8','9']
    pathst = '/usr/local/share/kweb/kweb'
    if kbd == 'default':
        for ch in allowed_kbds:
            p = pathst+ch+'.txt'
            if not os.path.exists(p):
                f = file(p,'wb')
                f.write(u'=?b')
                f.close()
                html = text2html(p,default_template)
                html.create()
    elif kbd == 'autoconfig':
        atxt = ''
        p = pathst+kbd+'.txt'
        p2 = pathst+kbd+'.html'
        if not args:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except:
                    pass
            if os.path.exists(p2):
                try:
                    os.remove(p2)
                except:
                    pass
        else:
            for arg in args:
                isuri,value = check_kbd_args(arg)
                if value:
                    if isuri:
                        atxt += '=)' + value + '\n'
                    else:
                        atxt += '=' + value + '\n'
            if atxt:
                atxt += '=?#'
                f = file(p,'wb')
                f.write(atxt.encode('utf-8'))
                f.close()
                html = text2html(p,default_template)
                html.create()
    elif kbd in allowed_kbds:
        p = pathst+kbd+'.txt'
        ktext = ''
        forward = ''
        for arg in args:
            isuri,value = check_kbd_args(arg)
            if value:
                if isuri:
                    if not forward:
                        forward=value
                        ktext += '#!forward='+value+'\n'
                    else:
                        ktext += '=)'+value+'\n'
                else:
                    ktext += '='+value+'\n'
        if not forward:
            ktext += '=?b'
        f = file(p,'wb')
        f.write(ktext.encode('utf-8'))
        f.close()
        html = text2html(p,default_template)
        html.create()

def create_html(path):
    fpath = ''
    if path.endswith('.txt'):
        if path.startswith('/') and os.path.exists(path):
            fpath = path
        else:
            tpath = os.path.join(os.getcwd(),path)
            if os.path.exists(tpath):
                fpath = tpath
            else:
                if os.geteuid() == 0 and os.path.exists(os.path.join('/usr/local/share/kweb',path)):
                        fpath = os.path.join('/usr/local/share/kweb',path)
        if fpath:
            html = text2html(fpath,default_template)
            html.create()

def patch_presets():
    if os.path.exists('/usr/local/share/kweb'):
        kfiles = os.listdir('/usr/local/share/kweb')
        presets = []
        for t in kfiles:
            if t.endswith('.preset') and t not in ['nogui.preset','default.preset','trueaspect.preset']:
                presets.append(t)
        for t in presets:
            f = file('/usr/local/share/kweb/'+t,'rb')
            preset = f.read()
            f.close()
            if not 'Helper settings file for kweb\'s (Minimal Kiosk Browser) helper scripts' in preset:
                continue
            if not 'use_ytdl_server' in preset:
                preset = preset.strip()+'\n'+preset_patch
            preset = preset.replace("'omxplayergui.py'","'omxplayergui'")
            try:
                f = file('/usr/local/share/kweb/'+t,'wb')
                template = f.write(preset)
                f.close()
                os.chmod('/usr/local/share/kweb/'+t,0755)
            except:
                pass
def create_usercss():
    if not os.path.exists('/usr/local/share/kweb/user.css'):
        if os.path.exists('/usr/local/share/kweb/white.css'):
            shutil.copy('/usr/local/share/kweb/white.css','/usr/local/share/kweb/user.css')
                
if __name__ == '__main__':
    settingspath = '/usr/local/bin/kwebhelper_settings.py'
    settingslist = load_settings()
    spagepath = '/usr/local/share/kweb'
    if not os.path.exists(spagepath):
        os.mkdir(spagepath)
    about_s_path = spagepath+'/kweb_about_s.html'
    createsettingspage = False
    aboutlist = []
    editor_refresh = False
    args = sys.argv
    if len(args) == 2 and args[1] == 'patchpresets':
        patch_presets()
    if len(args) == 3 and args[1] == 'createkbd':
        create_kbd(args[2],[])
    elif len(args) > 3 and args[1] == 'createkbd':
        create_kbd(args[2],args[3:])
    elif len(args) == 3 and args[1] == 'createhtml':
        create_html(args[2])
    elif len(args) == 3 and args[1] in ['savepreset','loadpreset','deletepreset']:
        createsettingspage = preset(args[1],args[2])
    elif len(args) == 3 and args[1] in ['createabout','deleteabout','refreshabout']:
        editor_refresh,aboutlist = about_commands(args[1],args[2])
    elif len(args) == 2 and args[1] == 'refresheditor':
        editor_refresh = True
    elif len(args) == 2 and args[1] in global_vars:
        createsettingspage = set_value(args[1],'')
    elif len(args) == 3 and args[1] in global_vars:
        createsettingspage = set_value(args[1],args[2])
    elif len(args) == 1:
        create_usercss()
        create_kbd('default',[])
        createsettingspage = True
        dummy,aboutlist = get_command_names()
        editor_refresh = True
    if settingslist and createsettingspage:
        create_settings_page(settingslist)
    if aboutlist:
        create_about_pages(aboutlist)
    if editor_refresh:
        create_editor_page()
