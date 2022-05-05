import os
from os.path import exists
import subprocess
import eel
import settings
import serial
import time



class BT_Thread:

    def __init__(self):
        os.system("/root/diagnoserfcomm")
        settings.btStatus = 'Initialized'
        

    def btLoop(self):
        print("Starting BT Loop", flush=True)
        try:
            while True:
                try: 
                    ser = serial.Serial('/dev/rfcomm0', baudrate=115200)
                    settings.btStatus = 'Connected'
                    while True:
                        print(time.perf_counter(), flush=True)
                        ser.write(bytes(settings.frameQueue.get() + "\n", 'utf-8'))
                        #ser.write(b"Hello\n")
                        eel.sleep(0.05)
                    eel.sleep(0)
                except (serial.serialutil.SerialException) as err:
                    settings.btStatus = "Communication Error, Attempting Reconnect"
                    eel.sleep(2)
                    os.system("/root/diagnoserfcomm")
                    try:
                        statusfile = open("bluetoothstatus.txt")
                        settings.btStatus = statusfile.read()
                        statusfile.close()
                    except FileNotFoundError as fileerr:
                        print(repr(fileerr))
                    eel.sleep(5)
                    

        except RuntimeError as err:
            settings.btStatus = "Fatal: " + repr(err)
            raise

if __name__ == '__main__':
    settings.frameQueue.put(settings.testImage)
    btloop = BT_Thread()
    btloop.btLoop()
        