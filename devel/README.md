*Cosmic ray detection with USB cameras, for the CREDO project (team project)*

### Code development

The catalog was created for codes created within the team project.

- **credo_webcam.py**

Initial code developed by Dominik and Tytus (copied from TLarcius fork).
Example algorithm for cosmic detection was extended by 
checking if enough pixels are grouped up together, doing
a basic impacts assessment (in form of deciding whether it was
perpendicular, vertical or horizontal) and some optimisation (by moving
some parts of the code around). 

Parsing of input arguments, some more optimization and minor changes in output added by AFZ.

- **credo_webcam_19_8.py**

Current code version. Recent developments:

- Simple user interface in the terminal window added. 
Allows to set observer's position (latitude, longitude) and select input device (or file).
More options still to come. 
- Simple check for poorly covered camera lenses: stops the program if too many events detected.

