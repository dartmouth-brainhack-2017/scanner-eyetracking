import numpy as np
import cv2
# from matplotlib import pyplot as plt

# Boolean to specify whether we want to write the video
writeVideo = True

videoFile = "SamLocR3.mov"
cap = cv2.VideoCapture(videoFile)

if writeVideo:
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    FPS = cap.get(cv2.CAP_PROP_FPS)
    Frame_Height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    Frame_Width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    # Frame_Size = (int(Frame_Width),int(Frame_Height))
    Frame_Size = (704,480)
    isColor = True
    out = cv2.VideoWriter('output.avi',fourcc, FPS, Frame_Size)

# while(cap.isOpened()):
#     ret, frame = cap.read()
#     if ret==True:
#         out.write(frame)
#     else:
#         break

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:

        # HSV hue detection
        hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height = len(hsvframe)
        width = len(hsvframe[0])
        for x in range(width):
            for y in range(height):
                value = hsvframe[y,x,0]
                saturation = hsvframe[y,x,1]
                brightness = hsvframe[y,x,2]
                # if (x < 200 or x > 400) or (y < 200 or y > 300):
                    # hsvframe[y,x,2] = 0
                # else:
                if (value < 95 or value > 110) or ((saturation < 120 or saturation > 160) and (brightness < 190 or brightness > 210)): # or :
                    hsvframe[y,x,2] = 0
        newframe = cv2.cvtColor(hsvframe, cv2.COLOR_HSV2BGR)
        newframe = cv2.medianBlur(newframe,21)

        edgeframe = cv2.cvtColor(newframe,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(edgeframe,300,400)
        final = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)

        # cv2.rectangle(frame,(200,200),(400,300),(0,255,0),2)
        # cv2.rectangle(newframe,(324,230),(326,232),(0,255,0),2)

        # print(hsvframe[230][325][2])

        if writeVideo:
            out.write(final)

        # Display results
        cv2.imshow('frame',final)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cv2.destroyAllWindows()
