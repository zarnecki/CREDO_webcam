/*
Modified from  webcam_opencv.cpp
downloaded from   https://gist.github.com/priteshgohil

g++ webcam_opencv.cpp -o webcam_opencv -I/usr/include/opencv4 -lopencv_core -lopencv_videoio -lopencv_highgui

More packages during compilation can be added from the list obtained by $ pkg-config --cflags --libs opencv4

*/
#include <opencv2/opencv.hpp>
#include <iostream>
#include <sstream>
#include <ctime>

int main(int argc, char** argv)
{
   if( argc !=  2 )
     {
       std::cout << " usage:  " << argv[0] << "  [device id]" << std::endl ;
      exit(1) ;
     }

   int devid = atoi(argv[1]);
   
   // open the first webcam plugged in the computer
   
   cv::VideoCapture  camera(devid); // in linux check $ ls /dev/video0

   if (!camera.isOpened())
     {
        std::cerr << "ERROR: Could not open camera" << std::endl;
        exit (2);
     }

    // create a window to display the images from the webcam
   
    cv::namedWindow("Webcam", cv::WINDOW_AUTOSIZE);

    // array to hold image
    cv::Mat frame;

    int Nframe = 0;
    std::time_t t_start = std::time(0); 
     
    // display the frame until you press a key
    while( camera.isOpened() )
      {
      
        // capture the next frame from the webcam
        camera >> frame;
	
        // show the image on the window
        cv::imshow("Webcam", frame);

	std::stringstream ftitle;
	ftitle << "WebCam event #" << Nframe;
	
        cv::setWindowTitle("Webcam",ftitle.str());
	Nframe++;
	
        // wait (10ms) for esc key to be pressed to stop
        if (cv::waitKey(10) == 'q')
            break;
       }

    std::time_t t_end = std::time(0);
    
    std::cout << Nframe << " frames read in " << t_end - t_start << " s " << std::endl;
    std::cout << " Average rate is " << Nframe/(t_end-t_start) << " Hz" << std::endl;
    return 0;
}


