#!/usr/bin/env python

# Helper settings file for kweb's (Minimal Kiosk Browser) helper scripts
# kwebhelper.py and omxplayergui.py
# Copyright 2013-2016 by Guenter Kreidl
# version 1.7.0

# <big><b>GLOBAL OPTIONS</b></big>
# Download directory, where the downloads including PDF files, playlists etc. go;
# if empty, a folder 'Downloads' in the user's home dir will be taken (and created, if it doesn't exist).
dldir = ''
#dldir = '/media/volume/Downloads'

# <br><big><b>PDF OPTIONS (kwebhelper)</b></big>
# Preferred pdf reader: either evince, xpdf or mupdf. If left empty, the program will try to find the best PDF reader
# Selecting an installed program of your choice will speed it up a bit
pdfprog = ''
#pdfprog = 'xpdf'
# Additional options for pdf program (must match the selected program!):
pdfoptions = []
#pdfoptions = ['-fullscreen']
# This will allow kweb to open pdf files on a local server as files instead of downloading them first;
# will only work with "http://localhost" links
pdfpathreplacements = {}
#pdfpathreplacements = {'http://localhost:8073/Ebooks1':'file:///var/www/Ebooks1'}

# <br><big><b>DOWNLOAD OPTIONS (kwebhelper)</b></big>
# Defines if wget will run in a terminal (visual control) or in the background:
show_download_in_terminal = True
#show_download_in_terminal = False
# Options for wget:
wget_options = ["--no-check-certificate","--no-clobber","--adjust-extension","--content-disposition"]
# Options for download manager uget:
uget_options = ['--quiet']

# <br><big><b>COMMAND EXECUTION OPTIONS (kwebhelper)</b></big>
# If this is set to "True", all Desktop (GUI) programs will be executed without starting a terminal first
check_desktop = True
#check_desktop = False
# Direct commands will be executed without starting a terminal first.
# Use it for background commands or programs with a GUI that are not desktop programs or if check_desktop is set to "False"
direct_commands = ['kwebhelper.py','omxplayergui','kwebhelper_set.py','omxplayer','gksudo','xterm','screen']
# Preferred terminal to run commands in, must be set ('xterm' or 'lxterminal')
preferred_terminal = 'lxterminal'
#preferred_terminal = 'xterm'
# Set the following to False if you don't want to run 'sudo' commands inside a terminal,
# but only if a password is not required (you may break command execution otherwise):
sudo_requires_password = True
#sudo_requires_password = False
# set the following to "True", if you want to run all commands from a script file.
# It may help with complex command links, but will require more disk accesses.
run_as_script = False
#run_as_script = True

# <br><a name="1"></a><big><b>GENERAL OMXPLAYER AUDIO VIDEO OPTIONS</b></big>
# Options for omxplayer to be used when playing video
omxoptions = []
#for selecting the sound output, uncomment one of these:
#omxoptions = ['-o','hdmi']
#omxoptions = ['-o','local']
#more options are also possible of course
# Options for omxplayer to be used when playing audio
omxaudiooptions = []
# Special options for watching live tv streams (omxplayer)
omx_livetv_options = ['--live']
# Add the start of your live tv stream links to this list to enable live tv options
live_tv = []
#like this:
#live_tv = ['http://192.168.0.5:9082']

# Mimetypes: if given, this will restrict what omxplayer will be given to play.
mimetypes = []
# If omxplayerGUI is not used omxplayer is started from a terminal (xterm) to clear the screen and get full keyboard control.
# Set the following to "False" to use omxplayer for video without starting a terminal first (if omxplayerGUI is not used)
omxplayer_in_terminal_for_video = True
#omxplayer_in_terminal_for_video = False
# Set the following to "False" to use omxplayer for audio without starting a terminal first (if omxaudioplayer is not used)
omxplayer_in_terminal_for_audio = True
#omxplayer_in_terminal_for_audio = False

# The following list will be used, to detect audio files, especially in m3u playlists
audioextensions = ['mp3','aac','flac','wav','wma','cda','ogg','ogm','ac3','ape']
# How unknown streams should be handled, must be either 'video' or 'audio'
streammode = 'video'
# If streammode is set to "video", the following list will be used for checking for video files
videoextensions = ['asf','avi','mpg','mp4','mpeg','m2v','m1v','vob','divx','xvid','mov','m4v','m2p','mkv','m2ts','ts','mts','wmv','webm','flv']
# If the following is set to "True" VLC will be used to play audio files and playlists (audio only)
useVLC = False
#useVLC = True

# <br><big><b>omxplayerGUI AUDIO & VIDEO OPTIONS</b></big>
# Play audio files or playlists that contain only audio files in omxaudioplayer 
useAudioplayer = True
# Use GUI for playing videos
useVideoplayer = True
# Volume setting when starting omxplayerGUI ranging from -20 to 4 ( -60 to +12 db)
defaultaudiovolume = 0
# Start playing the first (or only) file automatically
autoplay = True
# Close the GUI if the last (or only) file has been played to the end
autofinish = True
# Interface settings for omxaudioplayer and omxplayerGUI (video)
# The font to be used for playlist and buttons
fontname = 'SansSerif'
# Font size between 10 and 22, will also determine the size of the GUI window:
fontheight = 12
# Number of entries displayed in playlist window, between 5 and 25:
maxlines = 8
# Width of the window, value between 40 and 80, defines the minimum number of characters of the song name  displayed in the songlist (usually much more are shown!), not used for video mode
lwidth = 40
# Minimal height of video area (also depends on fontheight!), 288 or more:
videoheight = 288
# Default 'Lines:' mode, must be one of those: 'min','max', 'full'
screenmode = 'max'
# Default video mode: set this to 'full' or 'refresh' for full screen,
# to 'auto' (for automatic detection of the aspect ration) or to one of those:
# '4:3','16:9','16:10','2.21:1','2.35:1','2.39:1' to play in a window
# (you can also add one additional value here):
videomode = '16:9'
# Set the following to "True" for simple mode (no window resizing, moving etc. while playing video);
# must be set to "True" for older omxplayer versions
freeze_window = False
# Get aspect ratio in background, if True (if videomode not one of 'auto', 'full' or 'refresh').
# This costs some processing power and may even block or crash the system, especially with large AVI files.
# Therefore it disabled by default. Use it with care.
get_DAR = False
# If the following is set to "True", all control elements are hidden (can be enabled later on with ALT+h)
hide_controls = False

# <br><big><b>ONLINE VIDEO OPTIONS</b></big>
# Options for pages containing video, either HTML5 video tags or all websites supported by youtube-dl.
# If html5 video tags include more than one source format, select the preferred one here.
preferred_html5_video_format = '.mp4'
# Choose whether HTML5 URL extraction is tried first and youtube-dl extraction afterwards or vice versa.
html5_first = False
#html5_first = False
# Additional youtube-dl options, e. g. selecting a resolution or file format
youtube_dl_options = ['-f','best']
#youtube_dl_options = ['-f','37/22/18']
# Special omxplayer options for web video
youtube_omxoptions = []
# Use youtube-dl-server, if possible; also required for autostart from the frontend
use_ytdl_server = True
# Port on which youtube-dl-server is running.
# You should only change this, if the port is used by another application.
ytdl_server_port = '9192'
# Host name or IP of youtube-dl-server.
# Only change this, if you want to use one server for many clients.
# If not 'localhost', this will also prevent autostart from the frontend
ytdl_server_host = 'localhost'
# Format string to be used by youtube-dl-server. In case of missing audio, you might change this to:
# best[protocol!=?m3u8][protocol!=?m3u8_native]
ytdl_server_format = 'best'
