
import cv2
face_detect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_detect = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_detect = cv2.CascadeClassifier('haarcascade_smile.xml')

def detection(gray,frame):
    faces = face_detect.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_frame = frame[y:y+h, x:x+w]
        eye = eye_detect.detectMultiScale(roi_gray,1.1,20)
        for (ex,ey,ew,eh)in eye:
            cv2.rectangle(roi_frame,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        smile = smile_detect.detectMultiScale(roi_gray,1.7,22)
        for (sx,sy,sw,sh) in smile:
            cv2.rectangle(roi_frame,(sx,sy),(sx+sw,sy+sh),(0,0,255),2)
    return frame

video_capture = cv2.VideoCapture(0)
            

while True: # We repeat infinitely (until break):
    _, frame = video_capture.read() # We get the last frame.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # We do some colour transformations.
    canvas = detection(gray, frame) # We get the output of our detect function.
    cv2.imshow('Video', canvas) # We display the outputs.
    if cv2.waitKey(1) & 0xFF == ord('q'): # If we type on the keyboard:
        break # We stop the loop.

video_capture.release() # We turn the webcam off.
cv2.destroyAllWindows() #