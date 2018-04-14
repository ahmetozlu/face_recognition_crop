# Recognize, Crop and Save Faces as Images From Video

## INSTALLATION

**1.) dlib**

Install dlib prerequisites

The dlib library only has four primary prerequisites:
Boost
Boost.Python
CMake
X11/XQuartx

Install CMake, Boost, Boost.Python, and X11 **apt-get** :

	$ sudo apt-get install build-essential cmake
	$ sudo apt-get install libgtk-3-dev
	$ sudo apt-get install libboost-all-dev

Install opencv3 with

	$ sudo pip3 install opencv-python

**2.) face_recognition 1.2.1**

In this project, [Adam Geitgey](https://github.com/ageitgey/face_recognition)'s face recognition system (*thanks a lot to Adam*) was used for face recognition and it can be installed by pypi using pip3 (or pip2 for Python 2):

	sudo pip3 install face_recognition

## USAGE

	$ python3 recognize.py -i <video-input> -p <face_image1> <face_image2> ... -f 5

- Give video file path with -i option
- Give people face images with -p option. You can give multiple face image at the same time.
- Give frame step rate with -f option e.g. go with 5 frame steps.

## LICENSE
This system is available under the MIT license. See the LICENSE file for more info.
