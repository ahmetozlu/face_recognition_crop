# Single-View Face Recognition Database Creator

<p align="center">
  <img src="https://user-images.githubusercontent.com/22610163/30775206-0d959a3c-a098-11e7-965e-add626987376.gif">
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/22610163/30774902-978f4d56-a092-11e7-9860-536fdfb990f1.png">
</p>

Once we have acquired some data, we’ll need to read it in our program. In the demo applications I have decided to read the images from a very simple CSV file. Why? Because it’s the simplest platform-independent approach I can think of. However, if you know a simpler solution please ping me about it. Basically all the CSV file needs to contain are lines composed of a filename followed by a ; followed by the label (as integer number), making up a line like this:

    /path/to/image.ext;0

You don’t really want to create the CSV file by hand. I have prepared you a little Python script create_csv.py (you find it at src/create_csv.py coming with this tutorial) that automatically creates you a CSV file. If you have your images in hierarchie like this (/basepath/<subject>/<image.ext>):

    . 
    |-- s1     
    |   |-- 1.pgm
    |   |-- ...
    |   |-- 10.pgm
    |-- s2
    |   |-- 1.pgm 
    |   |-- ...
    |   |-- 10.pgm
    ...
    |-- s40
    |   |-- 1.pgm
    |   |-- ...    
    |   |-- 10.pgm
    
face_recognizer.py calls create_csv.py with the path to the folder, and it could save the output as a csv file.
