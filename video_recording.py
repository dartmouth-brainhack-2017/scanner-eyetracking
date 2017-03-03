# Just a script to play around with video recording
# Write something more formal when this code is working how we want

import numpy as np
import cv2

# Boolean to specify whether we want to write the video
writeVideo = False

# -1 works, but not sure what the argument is specifying
# 0 is the first camera (most likely webcam)
# 1 is the second camera (most likely scanner camera)
# Can also specify a filename
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
if writeVideo:
    # VideoWriter_fourcc argument specifies the type of codec to use when
    #   writing the video file
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    FPS = 20.0
    Frame_Size = (640,480)
    isColor = True
    out = cv2.VideoWriter('output.avi',fourcc, FPS, Frame_Size, isColor)

# cap.isOpened() checks to make sure the capture is opened
# This should happen automatically and stay open
# If it isn't open, then we can't record anything
# In this case, we would need to call cap.open()
# cap.get(propID) gets properties of the capture device
# cap.set(propID,value) sets the property
# cap.get(3) is width; cap.get(4) is height
# The documentation on this is broken, so that's all I can say...
while(cap.isOpened()):
    ret, frame = cap.read()
    # ret is a boolean for whether the frame was read correctly
    # It can be used to check for the end of the video
    if ret==True:

        # write the flipped frame
        if writeVideo:
            out.write(frame)

        cv2.imshow('frame',frame)

        # if reading and displaying from a file, we want to read
        # argument for waitKey is milliseconds of delay (time to wait for ...
        #   user input)
        # delay <= 0 or no delay specified will result in infinite waiting
        # Keep in mind delay is minimum wait time, may be longer
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    else:
        # break if we reach the end of the file or cannot read any more ...
        #   frames for some other reason
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
