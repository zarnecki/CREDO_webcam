/*
Modified from  webcam_opencv.cpp
downloaded from   https://gist.github.com/priteshgohil

g++ dialog_opencv.cpp -o dialog_opencv -I/usr/include/opencv4 -lopencv_core -lopencv_videoio -lopencv_highgui -lopencv_imgproc 

More packages during compilation can be added from the list obtained by $ pkg-config --cflags --libs opencv4

*/
#include <opencv2/opencv.hpp>
#include <iostream>
#include <sstream>
#include <ctime>


// Private dialog box based on OpenCV
//
// See:
// https://docs.opencv.org/3.1.0/d7/dfc/group__highgui.html
// https://docs.opencv.org/3.1.0/d6/d6e/group__imgproc__draw.html

std::string mydialog(std::string question, std::string ansmax = "0123456789", int allowText = 0, double fontScale = 1.0, int thickness=2)
{
  // For font selection see:
  //   https://docs.opencv.org/3.1.0/d0/de1/group__core.html#ga0f9314ea6e35f99bb23f29567fc16e11
  
  int fontFace = cv::FONT_HERSHEY_SIMPLEX;

  // Factor for empty space around text
  float gap = 1.0;

  // Text size estimate
  
  int baseline=0;
  cv::Size qSize = cv::getTextSize(question, fontFace, fontScale, thickness, &baseline);
  cv::Size aSize = cv::getTextSize(ansmax, fontFace, fontScale, thickness, &baseline);

  int dlrows =  (1 + gap) * (qSize.height + aSize.height);

  int dlcols = qSize.width;
  if(aSize.width > qSize.width) dlcols = aSize.width;
  dlcols += gap * qSize.height;
  
  // Dialog box background image (white)
  
  cv::Mat dlbg(dlrows,dlcols,CV_8UC3,cv::Scalar::all(255));

  // center of the question
  
  cv::Point qOrg((dlcols - qSize.width)/2, (1 + 0.5*gap)*qSize.height);
  cv::Point aOrg((dlcols - aSize.width)/2, dlrows - 0.5*gap*aSize.height);

  // Create dialog window
  
  cv::namedWindow("Dialog", cv::WINDOW_AUTOSIZE | cv::WINDOW_GUI_NORMAL);

  // Add question to background image
  
  cv::putText(dlbg,question, qOrg, fontFace, fontScale, cv::Scalar::all(0), thickness, 8);

  std::string answer = "";

  int akey = 0;

  while(1)
    {
    cv::Mat dlbox = dlbg.clone();
    
    cv::putText(dlbox, answer, aOrg, fontFace, fontScale, cv::Scalar::all(0), thickness, 8);
  
    cv::imshow("Dialog", dlbox);

    akey = cv::waitKey();

    // Debug line
    // std::cerr << akey << " : \'" << char(akey) << "\'" << std::endl;
    
    // Breake on NL/CR
    if (akey == '\n' || akey == '\r')
            break;

    // Backspace
    if (akey == '\b' && answer.length() > 0 )
      answer.pop_back();

    // Do not allow to exceed the maximum lenght

    if ( answer.length() == ansmax.length() ) continue;

    // Decode numbers
    
    if (akey >= '0' && akey <= '9')
      answer += char(akey);

    if (akey == '.' || akey == '-')
      answer += char(akey);

    // End of number parsing
    
    if( !allowText ) continue;

    // Only limited selection allowed

    if (akey >= 'a' && akey <= 'z')
      answer += char(akey);

    if (akey == '@' || akey == ' ')
      answer += char(akey);
    }

  // Close window
  
  cv::destroyWindow("Dialog");
  
  return answer;
}


int main(int argc, char** argv)
{
  // Dialog box


  std::string myans = mydialog("Your device ID:","00");

  std::cerr << "Your device ID: " << myans << std::endl;
  
  int devid = atoi(myans.c_str());


  std::string myans2 = mydialog("Window name:","xxxxxxxxxxxxxxxxxxxx",1);

  std::cerr << "Window title: " << myans2 << std::endl;
  


  
   // open the webcam with given ID
   
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
	ftitle << myans2 << " #" << Nframe;
	
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


