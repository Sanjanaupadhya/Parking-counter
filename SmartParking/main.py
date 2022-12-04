import cv2
import pickle
import cvzone
import numpy as np
import pandas as pd

#video feed
cap = cv2.VideoCapture("Resources/carPark.mp4")

width, height = 107, 48

y1, y2 = 60, 95
dic = {}

def checkParkingSpace(imgpro):
    spaceCounter = 0

    seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    #Getting pos from poslist and display rectangles
    # for i, pos in posList:
    for i, pos in enumerate(posList):
        x, y = pos
        imgCrop = imgpro[y:y+height, x:x+width]
        # cv2.imshow(str(x*y), imgCrop)3

        #To count no of pixels
        count = cv2.countNonZero(imgCrop)

        if count < 860:
            color = (0, 255, 0) #Green
            thickness = 5
            spaceCounter += 1
            # cvzone.putTextRect(vid, {x}, (x, y + height - 3), scale=1, thickness=1, offset=0, colorR=color)

        else:
            color =  (0, 0, 255) #Red
            thickness = 2


        cv2.rectangle(vid, pos, (pos[0] + width, pos[1] + height), color, thickness)
        # To write pixel count on img
        cvzone.putTextRect(vid, str(count), (x, y + height - 3), scale=1, thickness=1, offset=0, colorR=color)  # (img, name, pos, scale, thickness, offset, clr)

        y1, y2 = 60, 95




        if 50<=x<=55 and color == (0, 255, 0):
            cvzone.putTextRect(vid, f'Free: col 1', (x, y+15), scale=1, thickness=1, offset=0, colorR=color)
            for s in seq:
                if y1 + (50 * s) <= y <= y2 + (50 * s) and color == (0, 255, 0):
                    cvzone.putTextRect(vid, f'row {s + 1}', (x, y + 27), scale=1, thickness=1, offset=1, colorR=color)


        if 157<=x<=162 and color == (0, 255, 0):
            cvzone.putTextRect(vid, f'Free: col 2', (x, y+15), scale=1, thickness=1, offset=0, colorR=color)
            for s in seq:
                if y1 + (50 * s) <= y <= y2 + (50 * s) and color == (0, 255, 0):
                    cvzone.putTextRect(vid, f'row {s + 1}', (x, y + 27), scale=1, thickness=1, offset=1, colorR=color)

        if 400<=x<=403 and color == (0, 255, 0):
            cvzone.putTextRect(vid, f'Free: col 3', (x, y+15), scale=1, thickness=1, offset=0, colorR=color)
            for s in seq:
                if y1 + (50 * s) <= y <= y2 + (50 * s) and color == (0, 255, 0):
                    cvzone.putTextRect(vid, f'row {s + 1}', (x, y + 27), scale=1, thickness=1, offset=1, colorR=color)

        if 508<=x<=511 and color == (0, 255, 0):
            cvzone.putTextRect(vid, f'Free: col 4' , (x, y+15), scale=1, thickness=1, offset=0, colorR=color)
            for s in seq:
                if y1 + (50 * s) <= y <= y2 + (50 * s) and color == (0, 255, 0):
                    cvzone.putTextRect(vid, f'row {s + 1}', (x, y + 27), scale=1, thickness=1, offset=1, colorR=color)

        if 748<=x<=751 and color == (0, 255, 0):
            cvzone.putTextRect(vid, f'Free: col 5', (x, y+15), scale=1, thickness=1, offset=0, colorR=color)
            for s in seq:
                if y1 + (50 * s) <= y <= y2 + (50 * s) and color == (0, 255, 0):
                    cvzone.putTextRect(vid, f'row {s + 1}', (x, y + 27), scale=1, thickness=1, offset=1, colorR=color)

        if 906<=x<=909 and color == (0, 255, 0):
            cvzone.putTextRect(vid, f'Free: col 6', (x, y+15), scale=1, thickness=1, offset=0, colorR=color)
            for s in seq:
                if y1 + (50 * s) <= y <= y2 + (50 * s) and color == (0, 255, 0):
                    cvzone.putTextRect(vid, f'row {s + 1}', (x, y + 27), scale=1, thickness=1, offset=1, colorR=color)





    #Displaying remaining spaces
    # cvzone.putTextRect(vid, str(spaceCounter), (100, 50), scale=2, thickness=3, offset=9, colorR=(0, 255, 0))
    cvzone.putTextRect(vid, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3, thickness=3, offset=9, colorR=(0, 255, 0))


with open("CarParkPos", "rb") as f:
    posList = pickle.load(f)

while True:
    #To loop the video
    #current position(frame) == total no of frames of the video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        #Reset the frame(to zero), if they reach the total amount of frame of the video
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, vid = cap.read()

    imgGray = cv2.cvtColor(vid, cv2.COLOR_RGB2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

    #convert to binary image
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16) #(img, max value, method, binary inverse, blocksize)

    #to remove noise
    imgMedian = cv2.medianBlur(imgThreshold, 5)

    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    cv2.imshow("Parking Video", vid)
    cv2.waitKey(10)