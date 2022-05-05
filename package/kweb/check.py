#!/usr/bin/env python

# check for programs needed by Minimal Kiosk Browser
# version 1.7.0
import os

dependencies_fullfilled = True

print "... looking for programs needed by or recommended for Minimal Kiosk Browser"

# checking for lxterminal
if os.path.exists('/usr/bin/lxterminal'):
    print "found: lxterminal"
else:
    dependencies_fullfilled = False
    print "lxterminal not found. It is needed by Minimal Kiosk Browser. Install it with:"
    print "sudo apt-get install lxterminal"
    print

# checking for PDF support

pdfprograms = []
if os.path.exists('/usr/bin/mupdf'):
    pdfprograms.append('mupdf')
if os.path.exists('/usr/bin/xpdf'):
    pdfprograms.append('xpdf')
if os.path.exists('/usr/bin/evince'):
    pdfprograms.append('evince')

if not pdfprograms:
    dependencies_fullfilled = False
    print "No suitable PDF viewer found. Install evince (recommended) with:"
    print "sudo apt-get install evince"
elif 'mupdf' in pdfprograms and len(pdfprograms) == 1:
    print "minimal PDF support is found using mupdf."
    print "for better PDF support it is highly recommended to install either evince:"
    print "sudo apt-get install evince"
    print "or xpdf:"
    print "sudo apt-get install xpdf"
    print
else:
    if 'evince' in pdfprograms:
        print "found: evince for best PDF support"
    else:
        print "found: xpdf for better PDF support (recommended: evince!)"

#checking for omxplayer
if os.path.exists('/usr/bin/omxplayer'):
    print "found: omxplayer"
    print "for use with omxplayerGUI you should always get the latest version"
    print "from http://omxplayer.sconde.net/"
else:
    dependencies_fullfilled = False
    print "omxplayer not found. It is needed for audio and video support. Install it with:"
    print "sudo apt-get install omxplayer"
    print "for use with omxplayerGUI you should always get the latest version"
    print "from http://omxplayer.sconde.net/"
    print

#checking for youtube-dl
if os.path.exists('/usr/bin/youtube-dl'):
    print "found: youtube-dl"
    ytdldir = os.path.expanduser('~')+os.sep+'youtube-dl'
    if os.path.exists(ytdldir):
        print "found: youtube-dl from github (best solution and needed for youtube-dl-api-server)"
    else:
        print "for optimal use of youtube-dl you need the github version."
        print "you will be asked for automatic installation later on"
else:
    dependencies_fullfilled = False
    print "youtube-dl not found. It is needed for web video support."
    print "you will be asked for automatic installation of the optimal version later on"
    print

#checking for uget
if os.path.exists('/usr/bin/uget-gtk'):
    print "found: uget download manager"
else:
    dependencies_fullfilled = False
    print "uget download manager not found. It is highly recommended for downloads."
    print "Install it with:"
    print "sudo apt-get install uget"
    print 

#checking for tint2
if os.path.exists('/usr/bin/tint2'):
    print "found: tint2 task bar"
else:
    print "if you want to use Minimal Kiosk Browser without starting the desktop,"
    print "you need the light weight task bar tint2. Install it with:"
    print "sudo apt-get install tint2"
    print

#checking for xterm
if os.path.exists('/usr/bin/xterm'):
    print "found: xterm (as optional terminal variant and for playing video without GUI)"
else:
    print "xterm not found. It can be optionally used for playing video full screen without GUI."
    print "If you want to make use of this option, you must install it with:"
    print "sudo apt-get install xterm"
    print

if dependencies_fullfilled:
    print "All important programs needed by Minimal Kiosk Browser have been found."
else:
    print "Some programs needed to use all features of Minimal Kiosk Browser are not installed."
    print "Follow the install recommendations above."
