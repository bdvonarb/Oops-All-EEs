import cv2
import base64
import numpy as np


canvas = np.zeros((24,25,3), np.uint8)

cv2.line(canvas, (0,0), (23,24), (255,255,255), 1)

retval, buffer = cv2.imencode('.jpg', canvas)
print(base64.b64encode(buffer).decode("utf-8"))

