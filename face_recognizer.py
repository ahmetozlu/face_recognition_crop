#----------------------------------------------
#--- Author         : Ahmet Ozlu
#--- Mail           : ahmetozlu93@gmail.com
#--- Date           : 21st September 2017
#----------------------------------------------

import face_recognition
import cv2
import os
from utils import create_csv

import standalone_DetectEmotion

# The output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_movie = cv2.VideoWriter('tbbt_output.avi', fourcc, 30, (1280, 720))

# Open the input movie file
input_movie = cv2.VideoCapture("tbbt.mp4")
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

# Load some sample pictures and learn how to recognize them.
lmm_image = face_recognition.load_image_file("sheldon.jpg")
lmm_face_encoding = face_recognition.face_encodings(lmm_image)[0]

al_image = face_recognition.load_image_file("penny.jpg")
al_face_encoding = face_recognition.face_encodings(al_image)[0]

known_faces = [
    lmm_face_encoding,
    al_face_encoding
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_number = 0

current_path = os.getcwd()

counter = 0
counter1 = 0
targeted_fer_image = "NAN"
fer = "NAN"
label = "NAN"
dataset_path = "NAN"
while True:
    # Grab a single frame of video
    ret, frame = input_movie.read()
    frame_number += 1

    # Quit when the input video file ends
    if not ret:
        break

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)

        # If you had more than 2 faces, you could make this logic a lot prettier
        # but I kept it simple for the demo
        name = None
        if match[0]:
            name = "Jim Parsons, 28, M"
        elif match[1]:
            name = "Kaley Cuoco, 29, F"

        face_names.append(name)

    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue

        crop_img = frame[top-100:bottom+100, left-100:right+100]

        if(name == "Jim Parsons, 28, M"):
            cv2.imwrite(current_path + "/face_database/Sheldon/" + "jim_parsons"+str(counter)+".png",crop_img)
            targeted_fer_image = current_path + "/face_database/Sheldon/" + "jim_parsons"+str(counter)+".png"
            counter = counter + 1
            label = "jim_parsons_28_m" + "_" + str(counter)
            dataset_path = current_path + "/face_database/Sheldon/"
        elif(name == "Kaley Cuoco, 29, F"):
            cv2.imwrite(current_path + "/face_database/Penny/" + "kaley_cuoco"+str(counter1)+".png",crop_img)
            targeted_fer_image = current_path + "/face_database/Penny/" + "kaley_cuoco"+str(counter1)+".png"
            counter1 = counter1 + 1
            label = "kaley_cuoco_29_f" + "_" + str(counter1)
            dataset_path = current_path + "/face_database/Penny/"
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

        if (targeted_fer_image != "NAN"):
            fer = standalone_DetectEmotion.fer(targeted_fer_image)

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name + ", " + fer, (left + 6, bottom - 6), font, 0.7, (0, 255, 255), 1)
        
        os.rename(targeted_fer_image, dataset_path + label + "_" + fer + ".png")

    # Write the resulting image to the output video file
    output_movie.write(frame)
    print("Writing frame {} / {}".format(frame_number, length))
    
    #cv2.imshow('face_recog_crop', frame)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# All done!
input_movie.release()
cv2.destroyAllWindows()
create_csv.CreateCsv(current_path + "/face_database/")
