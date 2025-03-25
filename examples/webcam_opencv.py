#!/usr/bin/env python
# coding: utf-8

# Code modified from:
# 
# https://github.com/codingforentrepreneurs/OpenCV-Python-Series/blob/master/src/camera-test.py
# 
# Video capture settings described on:
# 
# https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-set
# 

# In[1]:


import numpy as np
import cv2
from datetime import datetime


# In[2]:


# Open device

mycam = 5    # Device number for my external Logitech WebCam

cap = cv2.VideoCapture(mycam) 

if not cap.isOpened() :
    print(f"Could not open video device {mycam}")
else :
    print(f"Streaming from device {mycam}")

print("Default resolution: ",cap.get(cv2.CAP_PROP_FRAME_WIDTH)," x ",
                             cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("Default frame rate: ",cap.get(cv2.CAP_PROP_FPS))

# Modify image size

# imgsz = (320, 240)
# imgsz = (640, 480)
# imgsz = (800, 600)
# imgsz = (1280, 960)
# imgsz = (1920, 1080)

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, imgsz[0])
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, imgsz[1])

# Modify frame rate 

# imgrate = 30
# cap.set(cv2.CAP_PROP_FPS, imgrate)


# Main loop    

Nframe = 0
t_start = datetime.now()

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret == True:

        cv2.imshow('Webcam',frame)
        cv2.setWindowTitle('Webcam','WebCam event #'+str(Nframe))

        Nframe += 1
        
    if cv2.waitKey(20) & 0xFF  ==  ord('q'):
        break


# Loop completed

t_end = datetime.now()

tcap = (t_end-t_start).total_seconds()
frate = Nframe/tcap

print(f"{Nframe} frames captured in {tcap} s")
print(f"Average rate {frate} Hz")

# When everything done, release the capture

cap.release()
cv2.destroyAllWindows()


# In[ ]:




