
# Developer shreyas kapale


import cv2

import numpy as np

import imutils

from collections import deque

from pynput.mouse import Button, Controller
#pynput is a library for peripheral input devices.
#In this case i am using mouse controller
mouse = Controller()

mouse.position = (1024/2,1080/2)

greenLower = (29, 86, 6)

greenUpper = (64, 255, 255)

pts = deque(maxlen=64)

cam = cv2.VideoCapture(0)

while True:
	
	(grabbed, frame) = cam.read()
	#set the grabbed frame value in a frame var 

	frame = imutils.resize(frame, width=600)
    #frame resize 
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #blurr the frame to lose the noise and extract clean contours 
	mask = cv2.inRange(hsv, greenLower, greenUpper)
    #create a mask for get in only green colored area , taking in green max green and min green range values
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
    #filteration methods for clean contours
	con = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    #finding contour area's
		cv2.CHAIN_APPROX_SIMPLE)[-2]

	center = None

	if len(con) > 0:
		#if any contour is found ... then get the values of its area to get the radius value

		c = max(con, key=cv2.contourArea)

		((x, y), radius) = cv2.minEnclosingCircle(c)
		#get its coordinates  and radius

		M = cv2.moments(c)

		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		if radius > 10:
            # if radius is good enough , then draw circle around it till its visible
			mouse.position = (x*4, y*2)
            # move the mouse respect to the x , y multipy it by screen ratio and also respect to its tracking window size
			cv2.circle(frame, (int(x), int(y)), int(radius),
            # drawing circles till the contour is visible
 				(0, 255, 255), 2)

			cv2.circle(frame, center, 5, (0, 0, 255), -1)

	pts.appendleft(center)

	cv2.imshow("Frame", frame)

	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break


camera.release()
cv2.destroyAllWindows()
