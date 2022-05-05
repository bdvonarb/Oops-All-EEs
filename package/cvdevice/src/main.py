import gevent
from gevent.queue import Queue, Empty
import settings
from cv import CV_Thread
from bt import BT_Thread
from PIL import ImageColor
import os
import eel


queue = Queue()

cvloop = CV_Thread()

btloop = BT_Thread()

def printReader():
    print("Print Loop Started")
    while True:
        print("Getting Frame")
        try:
            print(settings.frameQueue.peek(timeout=2))
            print("Frame Gotted")
        except Empty:
            print("Nothing Gotted")
        eel.sleep(0)

def previewUpdateLoop():
    print("Preview Update Loop Started")
    while True:
        try:
            eel.updateImageSrc(settings.frameQueue.peek(timeout=1))
        except Empty:
            eel.updateInfo("No Frame")
        eel.sleep(0.1)

def updatePreview(frame):
    eel.updateImageSrc(frame)

def frameEaterLoop():
    print("Frame Eater Loop Started")
    while True:
        try:
            settings.frameQueue.get(timeout=1)
        except Empty:
            print("Empty")
        eel.sleep(0)

def statusUpdateLoop():
    print("Status Update Loop Started", flush=True)
    while True:
        try:
            eel.updateStatus(settings.cvStatus, settings.btStatus, 1/(settings.currentFrameTime-settings.previousFrameTime))
        except Exception:
            raise
        eel.sleep(1)

@eel.expose
def startStream():
    eel.spawn(statusUpdateLoop)
    eel.spawn(cvloop.cvLoop)
    eel.spawn(btloop.btLoop)
    #eel.spawn(previewUpdateLoop)
    
@eel.expose
def close():
    eel.spawn(kill)

def kill():
    os.system('killall /root/browser')

@eel.expose
def setFGColor(value):
    print("Setting FG", flush=True)
    settings.FGColor = ImageColor.getcolor(value, "RGB")
    print(settings.FGColor, flush=True)

@eel.expose
def setBGColor(value):
    print("Setting BG", flush=True)
    settings.BGColor = ImageColor.getcolor(value, "RGB")
    print(settings.BGColor, flush=True)

print("Starting UI", flush=True)

eel.init('/root/web')
eel.start('main.html', mode='custom', cmdline_args=['/root/browser'])
