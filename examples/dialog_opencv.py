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


# My openCV input dialog box

def mydialog(question, ansmax, allowText = False, fontScale = 1.0, thickness = 2):

    # Font selection
    fontFace = cv2.FONT_HERSHEY_SIMPLEX

    # Factor for empty space around text
    gap = 1.0

    # Text size estimate
  
    qSize = cv2.getTextSize(question, fontFace, fontScale, thickness)[0]
    aSize = cv2.getTextSize(ansmax, fontFace, fontScale, thickness)[0]

    dlrows =  int((1 + gap) * (qSize[1] + aSize[1]))

    dlcols = qSize[0]
    if aSize[0] > qSize[0]:
        dlcols = aSize[0]
        
    dlcols = int(dlcols + gap * qSize[1])
  
    # Dialog box background image (white)
  
    dlbg = 255*np.ones((dlrows, dlcols, 3), dtype = "uint8")
    
    # (cv2.Mat(dlrows,dlcols,cv2.CV_8UC3,(255,255,255))

    # position of the question and answer
  
    qOrg = ((dlcols - qSize[0])//2, int((1 + 0.5*gap)*qSize[1]) )
    aOrg = ((dlcols - aSize[0])//2, int(dlrows - 0.5*gap*aSize[1]) )

    # Create dialog window
  
    cv2.namedWindow("Dialog", cv2.WINDOW_AUTOSIZE | cv2.WINDOW_GUI_NORMAL)

    # Add question to background image
  
    cv2.putText(dlbg,question, qOrg, fontFace, fontScale, (0,0,0), thickness, 8)

    answer = ""

    akey = 0

    while(True):
    
        dlbox = np.array(dlbg)
    
        cv2.putText(dlbox, answer, aOrg, fontFace, fontScale, (0,0,0), thickness, 8)
  
        cv2.imshow("Dialog", dlbox)

        akey = cv2.waitKey() & 0xFF

        # Debug line
        # print(akey," : ",chr(akey))
    
        # Breake on NL/CR
        if akey == ord('\n') or akey == ord('\r') : 
            break

        # Backspace
        if akey == ord('\b') and len(answer) > 0 :
            answer = answer[:-1]

        # Do not allow to exceed the maximum lenght

        if  len(answer) == len(ansmax) : 
            continue

        # Decode numbers
    
        if akey >= 48 and akey <= 57 :  # '0'  to '9'
            answer += chr(akey)

        if akey == 45 or akey == 46:    #  '-'  and '.'
            answer += chr(akey)

        # End of number parsing
    
        if  not allowText: 
            continue

        # Only limited selection allowed

        if akey >= 97 and akey <= 122:    #  'a' to 'z'
            answer += chr(akey)

        if akey == 64 or akey == 32:       # '@'  and ' '
            answer += chr(akey)
    

    # Close window
  
    cv2.destroyWindow("Dialog")
  
    return answer
    


# In[3]:


# Input from dialog box (always returns a string)

mycam = int( mydialog("Your device ID:","00") )

mytitle = mydialog("Window name:","xxxxxxxxxxxxxxxxxxxx",True)

print("My device ID is ",mycam)
print("Window name is ",mytitle)


# In[4]:


# Open device

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
        cv2.setWindowTitle('Webcam',mytitle + ' #'+str(Nframe))

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




