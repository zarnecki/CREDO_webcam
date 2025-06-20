import numpy as np
import cv2
from datetime import datetime
from matplotlib import pyplot as plt

# For input arguments

import sys


### Default algorithm settings
#
#  Simple threshold requirement:
#  At least Nthr pixels with value Athr counts above  Mthr times maximum-mean from mean

Nthr =  3    # number of pixels required above threshold
Athr = 10    # threshold in pixel value
Mthr =  4    # threshold in maximum-mean distance for given pixel

# Averaging period for maximum and mean calculation

Nmax = 100

### Default input stream

mycam = 0    # webcam device id (0 for built-in webcam)

myfile = "signal.avi"

cor = 1    #  device (0) or file (1)

### Check input arguments

narg = len(sys.argv)   # including script name passed to python (!)

if narg == 1:
    print("\n Usage: ",sys.argv[0]," device/file  [Nthr] [Athr] [Mthr] [Nmax]\n")
    sys.exit()

if narg>1 :   #  device or file name given

    if len(sys.argv[1])>2 :
        myname = sys.argv[1]
        cor = 1
    else:
        mycam = int(sys.argv[1])
        cor = 0

# Read more arguments

if narg>2 :   # Number of pixels above threshold
    Nthr = int(sys.argv[2])

if narg>3 :   # Threshold in amplitude
    Athr = int(sys.argv[3])

if narg>4 :   # Threshold in maximum-mean distance
    Mthr = int(sys.argv[4])

if narg>5 :   # Averaging period
    Nmax = int(sys.argv[5])

    
### Actual code starts here

if cor == 0:
    cap = cv2.VideoCapture(mycam) 
    outname = 'cam_'+str(mycam)
else:
    cap = cv2.VideoCapture(myname)
    outname = 'file'

if not cap.isOpened() :
    print(f"Could not open video device {mycam}")
else :
    print(f"Streaming from device {mycam}")

print("Default resolution: ",cap.get(cv2.CAP_PROP_FRAME_WIDTH)," x ",
                             cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# print("Default frame rate: ",cap.get(cv2.CAP_PROP_FPS))
# print("Default gain: ",cap.get(cv2.CAP_PROP_GAIN))

# Modify image size

# imgsz = (640, 480)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, imgsz[0])
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, imgsz[1])

# Modify frame rate 

# imgrate = 30
# cap.set(cv2.CAP_PROP_FPS, imgrate)

# Running average, maximum

Vmax = 0.
Vmean = 0.

# Main loop    

Nframe = 0
t_start = datetime.now()
print(f"Data taking started at {t_start}  ({t_start.timestamp():.3f})")

# History of maximum counts
Nhist = 0
Hist_list = []
Max_list = []
Mean_list = []

# History of events

Nevt = 0

Tevt_list = []
Nevt_list = []
Sig_list = []
Val_list = []
Shape_list = []

frac = 1.0/Nmax
frac1 = 1.0 - frac

while(cap.isOpened()):
    # Debug output for threshold level
    if Nframe > 0 and Nframe%Nmax == 0 :
        print("Average pixel after {:d} frames: {:.2f} +/- {:.2f}  Max:  {:.2f} +/- {:.2f}".format(Nframe,np.mean(Vmean),np.std(Vmean),np.mean(Vmax),np.std(Vmax)),end="\r")

        Hist_list.append(t_frame)
        Max_list.append(np.mean(Vmax))
        Mean_list.append(np.mean(Vmean))
        Nhist+=1

    # Desplay flat frame after the initialization stage
    if Nframe == Nmax:
        fmean = Vmean.astype(np.uint8)
        cv2.imshow('WebCam',fmean)
        cv2.setWindowTitle('WebCam','WebCam mean frame')
    
    # Capture video stream frame-by-frame
    ret, frame = cap.read()

    if ret == True:

        t_frame = (datetime.now() - t_start).total_seconds()   # frame time from start of data taking [s]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    # output is 2D array
        
        if Nframe == 0 :             # Frist frame
            Vmax  = np.zeros_like(gray, dtype=np.float64)
            Vmean = np.zeros_like(gray, dtype=np.float64)
            
        if Nframe < Nmax :           # First Nmax frames - calibration
            Vmax   = np.maximum(Vmax,gray)
            Vmean += frac * gray

        else :         # After calibration, taking data
            
            # Threshold level for this frame (with mean frame as reference)
            
            Vthr = Mthr*(Vmax-Vmean) + Athr  

            # Significance: frame ratio to threshold frame (distance from mean)
            
            sigframe = (gray - Vmean)/Vthr

            abthr = np.transpose(np.nonzero(sigframe > 1)) #array of indexes of instances above treshold
            nabthr = np.size(abthr, 0) #size of the array
            next = 0 #0 if there are no 3 pixels above treshold next to each other and 1 it there are
            for x in range(nabthr):
                neathr = 0
                for y in range(nabthr) :   
                    if((abthr [x] [0] - 1 <= abthr [y] [0] <= abthr [x] [0] + 1) and (abthr [x] [1] - 1 <= abthr [y] [1] <= abthr [x] [1] +1)) :    
                        neathr += 1 #counting how many instances of pixels above threshold are in 3x3 squere
                if(neathr >= Nthr) :   
                    next = 1
                    xmax = abthr[x][1]   # Store location of the pixel which passes the condition
                    ymax = abthr[x][0]
                    break
                
            if next == 1 :

                #getting the area, a and b are x and y respectively

                amin,bmin = np.min(abthr,axis=0)
                amax,bmax = np.max(abthr,axis=0)

                square_size = np.sqrt (nabthr)
                
                #estimating the shape
                
                what_shape = -1
                if (amax - amin <= square_size and bmax - bmin <= square_size):
                    #impact was perpendicular
                    what_shape = 0
                else:
                    if (amax - amin <= square_size and bmax - bmin > square_size):
                        #impact was horizontal
                        what_shape = 1
                    if (amax - amin <= square_size and bmax - bmin > square_size):
                        #impact was vertical
                        what_shape = 2
                        
                #something has to be implemented for an occasion when there are lone pixels outside our "main" bunch TBD

                # Store frame parameters
                
                Tevt_list.append(t_frame)
                Nevt_list.append(Nframe)
                Val_list.append(gray[ymax,xmax])
                Sig_list.append(sigframe[ymax,xmax])
                Nevt += 1

                # flat corrected frame
                
                fcorr = np.maximum(gray - Vmean + np.mean(Vmean), 0.).astype(np.uint8)

                outname1 = outname+'_frame_'+str(Nframe)+'_unclassified.png'
                outname2 = outname+'_frame_'+str(Nframe)+'_unclassified_corr.png'
                hit = "unclassified"

                #perpendicular, horizontal, vertical
                if what_shape == 0:
                    outname1 = outname+'_frame_'+str(Nframe)+'_perpendicular_impact.png'
                    outname2 = outname+'_frame_'+str(Nframe)+'_perpendicular_impact_corr.png'
                    hit = "perpendicular"
                if what_shape == 1:
                    outname1 = outname+'_frame_'+str(Nframe)+'_horizontal_impact.png'
                    outname2 = outname+'_frame_'+str(Nframe)+'_horizontal_impact_corr.png'
                    hit = "horizontal"                  
                if what_shape == 2:
                    outname1 = outname+'_frame_'+str(Nframe)+'_vertical_impact.png'
                    outname2 = outname+'_frame_'+str(Nframe)+'_vertical_impact_corr.png'
                    hit = "vertical"

                Shape_list.append(what_shape)

                #saving original and corrected image
                cv2.imwrite (outname1, frame, [cv2.IMWRITE_PNG_COMPRESSION, 3])   # Default is 16 - poor quality !
                cv2.imwrite (outname2, fcorr, [cv2.IMWRITE_PNG_COMPRESSION, 3])

                cv2.drawMarker (frame,(xmax,ymax), (200,200,255), cv2.MARKER_SQUARE, 20, 1)     # Light red square. Color is (B,G,R) !
                cv2.imshow('WebCam',frame)
        
                cv2.setWindowTitle('WebCam','Event #'+str(Nframe)+' max at '+str(xmax)+':'+str(ymax)+" "+str(hit)+" "+str(nabthr)+" pixels")
        
                print("\nFrame # ",Nframe," : ",gray[ymax,xmax]," at (",xmax,",",ymax,")  S = ", sigframe[ymax,xmax],hit,nabthr," pixels")
            
            # Add to sum (also if event detected !)
            Vmax  = np.maximum(frac1*Vmax + frac*Vmean, gray)
            Vmean = frac1*Vmean  + frac*gray
         
        Nframe += 1

    # Could not read frame
    else:
        break
        
   # Break if 'q' pressed on display window
    if cv2.waitKey(20) & 0xFF  ==  ord('q'):
        break

# Loop completed

t_end = datetime.now()

tcap = (t_end - t_start).total_seconds()
frate = Nframe / tcap

print(f"{Nframe} frames captured in {tcap} s")
print(f"Average rate {frate} Hz")

# When everything done, release the capture

cap.release()
cv2.destroyAllWindows()

#note: we need to add something to close the program if the display window gets closed;

print(f"{Nevt} events found in {tcap} s")

if Nevt>0 and cor==0:
    tevt = tcap/Nevt
    print(f"Average time between events is {tevt} s")

# Print shape counts

shnames = ['Unknown','Perpendicular','Horizontal','Vertical']   # Shape values start at -1 (!)

shapes = np.array(Shape_list)

for ish in range(len(shnames)):
    print(shnames[ish]," : ",np.sum(shapes==ish-1))

    
