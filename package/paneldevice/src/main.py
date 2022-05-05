import serial
from rpi_ws281x import PixelStrip, Color
import numpy as np
import time
import base64
import PIL
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import os
from os.path import exists
import io

testString = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAIBAQEBAQIBAQECAgICAgQDAgICAgUEBAMEBgUGBgYFBgYGBwkIBgcJBwYGCAsICQoKCgoKBggLDAsKDAkKCgr/2wBDAQICAgICAgUDAwUKBwYHCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgr/wAARCAAZABgDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD8fv8Ak/8A/wCzgP8A1av/AOEn/p6/7Cv/ACGvAKK9/wD+T/8A/s4D/wBWr/8AhJ/6ev8AsK/8hoA8AooooAKKKKAPf/8Ak/8A/wCzgP8A1av/AOEn/p6/7Cv/ACGivAKKAP/Z"

strip = PixelStrip(600, 18, 800000, 10, False, 255, 0)
strip.begin()

PANEL_WIDTH = 25
PANEL_HEIGHT = 24

def Pix2LED(x, y):
    if y%2 == 0:
        return y*PANEL_WIDTH + x
    else:
        return y*PANEL_WIDTH + PANEL_WIDTH - 1 - x

while True:
    try:
        imageStream = serial.Serial('/dev/rfcomm0')
        while True:
            base64String = imageStream.read_until()
            #base64String = testString
            jpgString = base64.b64decode(base64String)
            jpgBytes = io.BytesIO(jpgString)
            jpgimage = Image.open(jpgBytes)
            pixels = np.asarray(jpgimage)
            for y in range(0,PANEL_HEIGHT):
                for x in range(0,PANEL_WIDTH-1):
                    strip.setPixelColor(Pix2LED(x,y), int(Color(*pixels[y,x])))
            strip.show()
    except serial.serialutil.SerialException:
        os.system('killall rfcomm')
        os.system('rfcomm release all')
        os.system('rfcomm listen rfcomm0 &')
        time.sleep(10.0)
        
        
    

