import cv2
import base64
import numpy as np
import sys
sys.path.append('/root/handtracker/')
from handtracker.HandTrackerEdge import HandTracker
import eel
import settings
import time

class CV_Thread:
    LINE_PAIRS = [(0, 1), (1,2), (2,3), (3,4), (2,5), (0,5), (5,6), (6,7), (7,8), (5,9), (9,10), (10,11), (11,12), (9,13), (13,14), (14,15), (15,16), (13,17), (17,18), (18,19), (19,20), (0,17)]
    handscaleavgpoints = 5

    def __init__(self):
        self.tracker = HandTracker(stats=True)
        self.framescale = 1.0
        settings.cvStatus = 'Initialized'

    def createFrame(self, hand):
        canvas = np.zeros((24,25,3), np.uint8)
        cv2.rectangle(canvas, (0,0), (24,25), settings.BGColor, cv2.FILLED)
        minx = np.min(hand.landmarks[:,0])
        maxx = np.max(hand.landmarks[:,0])
        miny = np.min(hand.landmarks[:,1])
        maxy = np.max(hand.landmarks[:,1])
        self.framescale = self.framescale * ((self.handscaleavgpoints - 1) / self.handscaleavgpoints) + (1 / self.handscaleavgpoints) * max(maxx-minx, maxy-miny)
        points = []
        centerx = (minx + maxx)/2
        centery = (miny + maxy)/2
        for id, lm in enumerate(hand.landmarks):
            cx = int(((lm[0]-centerx) / (self.framescale))*25 + 25/2)
            cy = int(((lm[1]-centery) / (self.framescale))*24 + 24/2)
            points.append((cx,cy))
        for pair in self.LINE_PAIRS:
            cv2.line(canvas, points[pair[0]], points[pair[1]], settings.FGColor, 1)
        canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
        retval, buffer = cv2.imencode('.png', canvas)
        return base64.b64encode(buffer).decode("utf-8")

    def cvLoop(self):
        print("Starting CV Loop", flush=True)
        settings.cvStatus = 'Running'
        try:
            while True:
                frame, hands, bag = self.tracker.next_frame()
                if frame is not None:
                    for hand in hands:
                        image = self.createFrame(hand)
                        #print(image)
                        #print(len(image))
                        settings.frameQueue.put(image)
                        eel.updateImageSrc(image)
                        settings.newFrameTime(time.time())
                eel.sleep(0.05)
        except RuntimeError as err:
            settings.cvStatus = repr(err)
            raise



if __name__ == '__main__':
    cvloop = CV_Thread()
    cvloop.cvLoop()
    
    
    
        