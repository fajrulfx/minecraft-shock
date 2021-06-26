from PIL import Image, ImageGrab
import cv2
import numpy as np
import time
import serial

ser = serial.Serial('COM11', 9800, timeout=1)
time.sleep(3)

i = 0
objects = [0]*100

while(True):
    im2 = ImageGrab.grab(bbox =(819, 1191, 1237, 1248)) 
    img = cv2.cvtColor(np.array(im2), cv2.COLOR_RGB2BGR)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,200,200])
    upper_red = np.array([8,255,255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

    objects[i] = len(contours)

    if i != 0:
        if objects[i] - objects[i-1] < 0:
            print("fire | from ", objects[i-1], " to ", objects[i])
            ser.write(b'H')
            time.sleep(0.5)
        else:
            ser.write(b'L')

    print(objects[i])

    i += 1
    if i == 100:
        i = 0
    time.sleep(0.2)

