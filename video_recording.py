# Just a script to play around with video recording
# Write something more formal when this code is working how we want

# CODE DOES NOT CURRENTLY WRITE BUTTON PRESS EVENTS

def writeEvent(f,timestamp,event):
    systime = time.localtime(time.time())
    systime = str(systime.tm_hour) + ":" + str(systime.tm_min) + ":" + str(systime.tim_sec)
    f.write(systime + "\t" + str(round(timestamp,3)) + "\t" + event)

import time
import numpy as np
import cv2
import serial
import glob

writeVideo = False
writeTiming = False
listenScan = False

scanTimeout = 6

Button1 = 49
Button2 = 50
Button3 = 51
Button4 = 52
TriggerKey=53

isScan = False
trigger = False
timeSinceLastTrigger = 0

if listenScan:
    allDevices = glob.glob('/dev/tty.USA*')
    deviceName = allDevices[0];
    BaudRate = 115200;
    ser = serial.Serial(deviceName,BaudRate,serial.EIGHTBITS,timeout=0)

if writeTiming:
    f = open('timing_output.txt','w')

# -1 works, but not sure what the argument is specifying
# 0 is the first camera (most likely webcam)
# 1 is the second camera (most likely scanner camera)
# Can also specify a filename
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
if writeVideo:
    # VideoWriter_fourcc argument specifies the type of codec to use when
    #   writing the video file
    # cap.get(propID) gets properties of the capture device
    # cap.set(propID,value) sets the property
    # cap.get(3) is width; cap.get(4) is height
    oFile = 'testWebcam.avi'
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    FPS = cap.get(cv2.CAP_PROP_FPS)
    Frame_Height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    Frame_Width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    Frame_Size = (int(Frame_Width),int(Frame_Height))
    out = cv2.VideoWriter(oFile,fourcc, FPS, Frame_Size)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:

        cv2.imshow('frame',frame)

        if listenScan:
            # 3 should be more than enough
            responses = ser.read(3)
            if TriggerKey in responses:
                trigger = True
                timeSinceLastTrigger = 0
            else if isScan:
                trigger = False
                timeSinceLastTrigger = time.time() - timeSinceLastTrigger
                if timeSinceLastTrigger > scanTimeout:
                    isScan = False
            else:
                trigger = False


        if writeVideo and out.isOpened():
            if trigger and not isScan:
                isScan = True
                oFile = 'scan_output.avi'
                outnew = cv2.VideoWriter(oFile,fourcc,FPS,Frame_Size)
                out.release()
                out = outnew
                tScanStart = time.time()
                if writeTiming:
                    writeEvent(f,0,"SCAN_STARTED")
            else if trigger and isScan and writeTiming:
                # Write to a file, the timestamp of the video and the trigger
                timestamp = time.time() - tScanStart
                writeEvent(f,timestamp,"TRIGGER")
            out.write(frame)

        if listenScan:
            trigger = False

        # if cv2.waitKey(5) & 0xFF == ord('q'):
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    else:
        break

# Release everything if job is finished
cap.release()
if writeVideo:
    out.release()
if listenScan:
    ser.close()
if writeTiming:
    f.close()
cv2.destroyAllWindows()
