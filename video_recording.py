# Just a script to play around with video recording
# Write something more formal when this code is working how we want

# CODE DOES NOT CURRENTLY WRITE BUTTON PRESS EVENTS

# def writeEvent(f,timestamp,event):
#     systime = time.localtime(time.time())
#     systime = str(systime.tm_hour) + ":" + str(systime.tm_min) + ":" + str(systime.tim_sec)
#     f.write(systime + "\t" + str(round(timestamp,3)) + "\t" + event)

import time
import numpy as np
import cv2
import serial
import glob
import os.path

# These variables can be used to control which sections of code are run
# Especially useful for testing when outside of the scanner (without a trigger)
writeVideo = True
writeTiming = False
listenScan = False

# Variables the user can change
scanTimeout = 6
studyID = '1010'
subjectID = 'TT'
runNumber = 1
breakNumber = 1

# Hardcoded variables (Don't change)
Button1 = 49
Button2 = 50
Button3 = 51
Button4 = 52
TriggerKey=53

# Initializing variables to be used later (Don't change)
isScan = False
trigger = False
timeSinceLastTrigger = 0

# Create a serial port connection to the scanner response box
if listenScan:
    allDevices = glob.glob('/dev/tty.USB0') # Standard for Linux (I think)
    if not allDevices:
        allDevices = glob.glob('/dev/tty.USA*') # Standard for MacOS (or for me,
                                                # at least)
    # if not allDevices:
        # Throw an error
    deviceName = allDevices[0]
    BaudRate = 115200;
    ser = serial.Serial(deviceName,BaudRate,serial.EIGHTBITS,timeout=0)

# Open a file for writing timing information
if writeTiming:
    f = open('timing_output.txt','w')

# Specify the capture device
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
    oFile = studyID + "_" + subjectID + "_break-" + str(breakNumber) + "_eyetracking.mov"
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    FPS = cap.get(cv2.CAP_PROP_FPS)
    Frame_Height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    Frame_Width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    Frame_Size = (int(Frame_Width),int(Frame_Height))
    out = cv2.VideoWriter(oFile,fourcc, FPS, Frame_Size)

while(cap.isOpened()):
    ret, frame = cap.read()
    # If a frame was returned...
    if ret==True:
        # Display the frame
        cv2.imshow('frame',frame)

        # Read from the scanner response box
        if listenScan:
            # 3 should be more than enough
            responses = ser.read(3)
            if TriggerKey in responses:
                trigger = True
                timeSinceLastTrigger = 0
            elif isScan:
                trigger = False
                # Fix timeSinceLastTrigger, doesn't work!!!
                timeSinceLastTrigger = time.time() - timeSinceLastTrigger
                if timeSinceLastTrigger > scanTimeout:
                    isScan = False
                    if writeVideo:
                        breakNumber += 1
                        oFile = studyID + "_" + subjectID + "_break-" + str(breakNumber) + "_eyetracking.mov"
                    if writeTiming:
                        timestamp = time.time() - tScanStart
                        # writeEvent(f,timestamp,"SCAN_ENDED")
                        systime = time.localtime(time.time())
                        systime = str(systime.tm_hour) + ":" + str(systime.tm_min) + ":" + str(systime.tim_sec)
                        f.write(systime + "\t" + str(round(timestamp,3)) + "\t" + "SCAN_ENDED")
            else:
                trigger = False

        if writeVideo and out.isOpened():
            if trigger and not isScan:
                isScan = True
                runNumber += 1
                oFile = studyID + "_" + subjectID + "_scan-" + str(runNumber) + "_eyetracking.mov"
                while os.path.isFile(oFile):
                    runNumber += 1
                    oFile = studyID + "_" + subjectID + "_scan-" + str(runNumber) + "_eyetracking.mov"
                outnew = cv2.VideoWriter(oFile,fourcc,FPS,Frame_Size)
                out.release()
                out = outnew
                tScanStart = time.time()
                if writeTiming:
                    # writeEvent(f,0,"SCAN_STARTED_"+str(runNumber))
                    systime = time.localtime(time.time())
                    systime = str(systime.tm_hour) + ":" + str(systime.tm_min) + ":" + str(systime.tim_sec)
                    f.write(systime + "\t" + str(round(timestamp,3)) + "\t" + "SCAN_STARTED_" + str(runNumber))
            elif trigger and isScan and writeTiming:
                # Write to a file, the timestamp of the video and the trigger
                timestamp = time.time() - tScanStart
                # writeEvent(f,timestamp,"TRIGGER")
                systime = time.localtime(time.time())
                systime = str(systime.tm_hour) + ":" + str(systime.tm_min) + ":" + str(systime.tim_sec)
                f.write(systime + "\t" + str(round(timestamp,3)) + "\t" + "TRIGGER")
            out.write(frame)

        if listenScan:
            trigger = False

    else:
        break

    if (cv2.waitKey(5) & 0xFF) == ord('q'):
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
