import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime


images = [] # contains current images after the loop
names = [] # contains name of the image
path = 'Images'
list = os.listdir(path)
#print (list)

for name in list:
    current_img = cv2.imread(f'{path}/{name}')
    images.append(current_img)
    names.append(os.path.splitext(name)[0])
#print(names)

def findencodings(images):
    known_encodes = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        known_encodes.append(encode)
    return known_encodes

def entry(name):
    with open('Entry_names.csv', 'r+') as f:
        name_list = []
        my_data = f.readlines()
        for line in my_data:
            entry = line.split(',')
            name_list.append(entry[0])
        if name not in name_list:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')


ecodes_faces = findencodings(images) # finds ecodings for all known faces
print("encodings completed")
capture = cv2.VideoCapture(0)

while True:
    _,frame = capture.read()  # capture frame from web cam
    img = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # changing its color

    facelocation = face_recognition.face_locations(img) # finding its location
    img_encode = face_recognition.face_encodings(img,facelocation) # findings its encoding based on its location

    for check_encoding, location in zip(img_encode,facelocation):# comparing the encodings of loaded images & live images
        matches = face_recognition.compare_faces(ecodes_faces,check_encoding)
        face_distance = face_recognition.face_distance(ecodes_faces,check_encoding)
        #print(face_distance)
        match_index = np.argmin(face_distance)

        if matches[match_index]:
            name = names[match_index].upper()
            print("Identified face of",name)
            y1, x2, y2, x1 = location
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2 - 30), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1 + 4, y2 - 4), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            entry(name) # stored the names and time in csv file
        else:
            print('face not registered')

    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) == ord('q'):
        break






