import numpy as np
import cv2
# from matplotlib import pyplot as plt

videoFile = "SamLocR3.mov"
cap = cv2.VideoCapture(videoFile)

# XML file located in opencv/data/haarcascades/ folder
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Canny edge detection
        # edges = cv2.Canny(gray,200,300)

        # HSV hue detection
        hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height = len(hsvframe)
        width = len(hsvframe[0])
        for x in range(width):
            for y in range(height):
                value = hsvframe[y,x,0]
                # if (x < 200 or x > 400) or (y < 200 or y > 300):
                    # hsvframe[y,x,2] = 0
                # else:
                if value < 100 or value > 105:
                    hsvframe[y,x,2] = 0
        newframe = cv2.cvtColor(hsvframe, cv2.COLOR_HSV2BGR)
        newframe = cv2.medianBlur(newframe,21)

        # newframe = cv2.cvtColor(newframe,cv2.COLOR_BGR2GRAY)
        # edges = cv2.Canny(newframe,300,400)

        # Sobel filtering
        # sobel = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=5)
        # abs_sobel = np.absolute(sobel)
        # sobel_8u = np.uint8(abs_sobel)

        # Finding coordinates for stuff (I forget what this was)
        # for i in range(len(gray[0])):
            # gray[:][i]
        # N = np.matrix(gray)
        # print(np.unravel_index(N.argmin(), N.shape))
        # print(N.argmin())
        # for i in range(len(gray)):
        #     print(gray[i][400])

        # Haar cascade eye detection
        # eyes = eye_cascade.detectMultiScale(gray,scaleFactor=1.5,minSize=(200,200))
        # for (ex,ey,ew,eh) in eyes:
        #     cv2.rectangle(frame,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        #     # print("eye found!")

        # cv2.rectangle(frame,(200,200),(400,300),(0,255,0),2)
        # cv2.rectangle(frame,(324,254),(326,256),(0,255,0),2)

        # print(hsvframe[255][325][0])

        # Display results
        cv2.imshow('frame',newframe)

        # edge_mask = cv2.bitwise_not(edges)
        # img = frame.putalpha(edge_mask)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cv2.destroyAllWindows()
