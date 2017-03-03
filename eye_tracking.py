import numpy as np
import cv2

videoFile = "SamHemiR1.mov"
cap = cv2.VideoCapture(videoFile)

# XML file located in opencv/data/haarcascades/ folder
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(frame,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            print("eye found!")
        cv2.imshow('frame',frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cv2.destroyAllWindows()
