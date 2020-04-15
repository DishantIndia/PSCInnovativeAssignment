import cv2
import numpy as np
import time
import argparse

parser = argparse.ArgumentParser()
# argument
parser.add_argument("--video", help = "Path to input video file. Skip this argument to capture frames from a camera.")

args = parser.parse_args()

print("Move Away From Camera for Three Seconds.....")

# videocapture object
cap = cv2.VideoCapture(args.video if args.video else 0)

time.sleep(3)
count = 0
background=0

# background
for i in range(60):
	ret,background = cap.read()

while(cap.isOpened()):
	ret, img = cap.read()
	if not ret:
		break
	count+=1
	
	# bgr to hsv
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# red mask
	lower_red = np.array([0,120,70])
	upper_red = np.array([10,255,255])
	mask1 = cv2.inRange(hsv,lower_red,upper_red)

	lower_red = np.array([170,120,70])
	upper_red = np.array([180,255,255])
	mask2 = cv2.inRange(hsv,lower_red,upper_red)

	mask1 = mask1+mask2

	# refine mask
	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations=2)
	mask1 = cv2.dilate(mask1,np.ones((3,3),np.uint8),iterations = 1)
	mask2 = cv2.bitwise_not(mask1)

	# outpput
	res1 = cv2.bitwise_and(background,background,mask=mask1)
	res2 = cv2.bitwise_and(img,img,mask=mask2)
	final_output = cv2.addWeighted(res1,1,res2,1,0)
	
	final_output=cv2.resize(final_output,(1300,720))
	cv2.resizeWindow('final_output', 1300,720)
	cv2.imshow('Magic !!!',final_output)
	#cv2.imshow('Mask',mask2)
	k = cv2.waitKey(10)
	if k == 27:
		break
