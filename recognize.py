import face_recognition as frec
import cv2
import os, argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="Path to the video file")
parser.add_argument("-p", "--people", type=str, nargs='+', help="Set of people as image file path and name pairs")
parser.add_argument("-f", "--frame_step", default=1, type=int,  help="Frame step to look for faces")

args = vars(parser.parse_args())
VIDEO_PATH = args["input"]
PEOPLE = args["people"]
FRAME_STEP = args["frame_step"]

## Open the input movie file
input_movie = cv2.VideoCapture(VIDEO_PATH)
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

## Create face_db directory
if not os.path.exists("face_db/"):
	os.mkdir("face_db/")

## Load some sample pictures and learn how to recognize them.
known_faces = []
known_names = []
for person in PEOPLE:
	facePath = os.path.basename(person)
	name = os.path.basename(facePath).split(".")[0]
	image = frec.load_image_file(facePath)
	face_encoding = frec.face_encodings(image)[0]
	known_faces.append(face_encoding)
	known_names.append(name)

	if not os.path.exists("face_db/" + name):
		os.mkdir("face_db/" + name)

## Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_number = 0
current_path = os.getcwd()

while True:

	## Grab a single frame of video
	ret, frame = input_movie.read()
	frame_number += 1

	## Pass as the frame step count
	if frame_number % FRAME_STEP != 0:
		continue

	## Quit when the input video file ends
	if not ret:
		break

	## Find all the faces and face encodings in the current frame of video
	face_locations = frec.face_locations(frame)
	face_encodings = frec.face_encodings(frame, face_locations)

	## TODO Handle this part with a database.
	found = False
	for face_encoding in face_encodings:
		# See if the face is a match for the known face(s)
		matches = frec.compare_faces(known_faces, face_encoding, tolerance=0.50)
		print(matches)

		if all([not match for match in matches]):
			continue

		for i, match in enumerate(matches):
			if match:
				name = known_names[i]

				(top, right, bottom, left) = face_locations[0]
				crop_img = frame[top:bottom, left:right]
				personPath = os.path.join(current_path, "face_db", name)

				#	N = len(os.listdir(personPath))
				cv2.imwrite(os.path.join(personPath, str(frame_number) + ".png"), crop_img)

				# Write the resulting image to the output video file
				print("Writing frame {} / {}, face of {}".format(frame_number, length, name))
				found = True

				# Draw a box around the face
				cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

	if not found:
		print("No face found for frame {} / {}".format(frame_number, length))

	cv2.imshow('faces', frame)
	key = cv2.waitKey(1)
	if key == 27:
		break

input_movie.release()
cv2.destroyAllWindows()

## TODO Better csv format should be considered
#create_csv.CreateCsv(current_path + "/face_database/")
