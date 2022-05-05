import subprocess
import enum
import cv2
import base64
import numpy as np
import eel
import os
import sys
import contextvars
sys.path.append('/root/handtracker/')
from handtracker.HandTrackerEdge import HandTracker

tracker = HandTracker(stats=True)
LINE_PAIRS = [(0, 1), (1,2), (2,3), (3,4), (2,5), (0,5), (5,6), (6,7), (7,8), (5,9), (9,10), (10,11), (11,12), (9,13), (13,14), (14,15), (15,16), (13,17), (17,18), (18,19), (19,20), (0,17)]
handscaleavgpoints = 5

def drawFrame(canvas, hand, framescale):
    minx = np.min(hand.landmarks[:,0])
    maxx = np.max(hand.landmarks[:,0])
    miny = np.min(hand.landmarks[:,1])
    maxy = np.max(hand.landmarks[:,1])
    #framescale = framescale * ((handscaleavgpoints - 1) / handscaleavgpoints) + (1 / handscaleavgpoints) * max(maxx-minx, maxy-miny)
    framescale = max(maxx-minx, maxy-miny)
    points = []
    centerx = (minx + maxx)/2
    centery = (miny + maxy)/2
    for id, lm in enumerate(hand.landmarks):
        cx = int(((lm[0]-centerx) / (framescale))*25 + 25/2)
        cy = int(((lm[1]-centery) / (framescale))*24 + 24/2)
        points.append((cx,cy))
    eel.updateInfo(np.max(points[:][1]))
    for pair in LINE_PAIRS:
        cv2.line(canvas, points[pair[0]], points[pair[1]], (255,255,255), 1)

def cvloop():
    try:
        framescale = 1.0
        while True:
            canvas = np.zeros((24,24,3), np.uint8)
            frame, hands, bag = tracker.next_frame()
            if frame is not None:
#               resizeframe = cv2.resize(frame, (50,50))
                for hand in hands:
                    drawFrame(canvas=canvas, hand=hand, framescale=framescale)
                retval, buffer = cv2.imencode('.jpg', canvas)
                frame_as_text = base64.b64encode(buffer).decode("utf-8")
                eel.updateImageSrc(frame_as_text)
    except Exception:
        os.system('killall /root/browser')
        raise
        

@eel.expose
def startStream():
    eel.spawn(cvloop)

@eel.expose
def close():
    subprocess.call('killall /root/browser', shell=True)

eel.init('web')
eel.start('main.html', mode='custom', cmdline_args=['/root/browser'])

