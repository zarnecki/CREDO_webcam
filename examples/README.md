*Cosmic ray detection with USB cameras, for the CREDO project (team project)*

### Program example 

The following codes were prepared as examples of the [OpenCV](https://opencv.org/) library use 
for collecting and analysing of the webcam frames.

- webcam_opencv

Short code (in three versions: C++, Jupyter notebook and stand-alone Python)
showing how frames can be read from webcam and displayed in a OpenCV viewer.

- cosmic-trigger.ipynb

Python notebook implementing simple algorithm searching for "flashes" in the frames 
read from the (covered) webcam. The algorithm is based on two quantities which are calculated for
each pixel in the camera frame: mean pixel value (Vmean) and maximum pixel value (Vmax). 
Both values are "averaged" over the last 100 (parameter which can be adjusted) frames. 
The new frame is identified as a one containing "flash" if at least 3 pixels 
are found above the threshold given by:

`Vthr = Mthr*(Vmax-Vmean) + Athr`

where `Mthr` and `Athr` are parameters of the algorithm. Frame with the "flash" 
is displayed on screed (with small yellow frame indicating position of the flash)
and stored on file.

More documentation on OpenCV is available at [this link](https://docs.opencv.org/2.4/index.html).

