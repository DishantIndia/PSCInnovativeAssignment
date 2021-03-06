import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
background=cv2.imread('black.jpg')
final=cv2.imread('white.jpg')
white=cv2.imread('white.jpg')
while(cap.isOpened()):
  ret, img = cap.read()

  img = np.flip(img,axis=1)
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  
  l1 = np.array([50,50,50])
  u1 = np.array([80,255,255])
  
  l2 = np.array([145,50,50])
  u2 = np.array([170,255,255])
 
  mask1 = cv2.inRange(hsv, l1, u1)
  mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
  
  mask2 = cv2.inRange(hsv, l2, u2)
  mask2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
    
  final[np.where(mask1==255)] = background[np.where(mask1==255)]
  final[np.where(mask2==255)] = white[np.where(mask2==255)]

  cv2.imshow('Display3',final)
  cv2.imshow('Display',img)
  
  close = cv2.waitKey(10)
  if close == 27:
    break