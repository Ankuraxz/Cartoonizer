from cv2 import cv2
import numpy as np
import matplotlib.pyplot as plt

import os
import sys
#Params
num_down = 2 #DOWNSAMPLE STEPS
num_bi = 5 # BILATERAL FILTERING STEPS
print("Press q to capture and exit")
cam = cv2.VideoCapture(0)

while True:
    ret,frame = cam.read()
    if ret == False:
        print("Can't access camera, Something went wrong!")
        continue
    cv2.imshow("Original",frame)
    
    img = cv2.resize(frame,(800,800))

    # DOWNSAMPLING + BILATERIAL FILTER
    img_c = img
    for ix in range(num_down):
        img_c = cv2.pyrDown(img)# Pyramid Down : Downsampling
    # print(img_c.shape)
    for iy in range(num_bi):
        img_c = cv2.bilateralFilter(img_c,d=9,sigmaColor=9,sigmaSpace=7) #Filtering
    # print(img_c.shape)
    #UPSAMPLING
    for ix in range(num_down):
        img_c = cv2.pyrUp(img_c)# Pyramid Down : Downsampling
    # print(img_c.shape)
    #BLUR and Threshold
    img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) # GRAY SCALE
    img_blur = cv2.medianBlur(img_gray,7) #MEDIAN BLUR
    img_edge = cv2.adaptiveThreshold(img_blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,blockSize=9,C=2)

    img_c = cv2.resize(img_c,(800,800))
    #RGB CONVERSION + BITWISE &
    img_edge = cv2.cvtColor(img_edge,cv2.COLOR_GRAY2RGB)
    # print(img_c.shape)
    # print(img_edge.shape)
    img_cartoon = cv2.bitwise_and(img_c,img_edge)

    stack = np.hstack([img,img_cartoon])
    cv2.imshow("Cartoon",stack)

    key_pressed = cv2.waitKey(1)&0xFF #Bitmasking to get last 8 bits
    if key_pressed==ord('q'): #ord-->ASCII Value(8 bit)
        break


# plt.imsave("./cartoon.png",Cartoon)
cam.release()
cv2.destroyAllWindows()	

