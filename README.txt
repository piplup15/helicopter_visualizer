A Simple Helicopter Visualizer in Python + OpenGL

By: Alvin Wong

========================================================================================

Requirements: This program was built using:
  - Python 2.7

This program also uses two dependencies:
  - PyOpenGL 3.0.2 (pyopengl.sourceforge.net)
  - Python Imaging Library (PIL)

Make sure to have these dependencies installed before proceeding.

========================================================================================

Description: This program takes in measurements from a helicopter flight and uses a 3D
visualizer to display the trajectory. The inputs to the program are:

(1) A file consisting of the relevant helicopter flight measurements, which must include:
    - Standard X, Y, and Z position coordinates.
    - Standard Qx, Qy, Qz, and Qw quaternions.
    - The time of the measurement (preferably starting at 0)

(2) An additional params file specifically for the flight, which must include:
    - Which columns to read the 8 parameters listed above, (indexed from 0)
    - The Z coordinate of the initial state of the flight.
    ** For more information, check out the file: default_params.txt

The files included in this program are:

(1) main.py - the main file for this program
(2) controls.py - specifies which keyboard controls are used for the program
(3) geometry.py - creates the required geometric objects for the visualizer
(4) shaders.py - includes standard vertex + fragment shaders for OpenGL
(5) textures.py - includes simple implementation for texturing
(6) model_helicopter.py - a simple helicopter created in OpenGL
(7) model_ground.py - a simple flat ground cretaed in OpenGL

=======================================================================================

The command to run the program is:

python main.py -f <datafilename> -p <paramsfilename>

Example, using the Stanford chaos dataset.

python main.py -f data/stanford_helicopter_data/chaos/smoother.txt -p default_params.txt

Alternatively, no specification of the params file defaults to the defaults_params.txt, so
the above can be simplified as:

python main.py -f data/stanford/helicopter_data/chaos/smoother.txt

======================================================================================

Safe flight!