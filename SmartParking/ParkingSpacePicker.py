import cv2
# import numpy as np
import pickle


width, height = 107, 48

#check whether a pickle object is there or not
try:
     with open("CarParkPos", "rb") as f:
          posList = pickle.load(f) #put contents of file f to posList

#Else create e new list
except:
     posList = []

def mouseClick(events,x,y,flags,params):
     if events == cv2.EVENT_LBUTTONDOWN:  #if are pressing left button, we will append to our list
          posList.append((x,y))
     if events == cv2.EVENT_RBUTTONDOWN:
          for i, pos in enumerate(posList):
               x1, y1 = pos
               if x1 <= x < x1 + width and y1 <= y < y1 + height:
                    posList.pop(i)

     #For each append and delete, we are going to add it to the pkl obj
     with open("CarParkPos","wb") as f: #wb :- read and write permission
          pickle.dump(posList,f) #dump posList in the file(f)


while True:
     img = cv2.imread('Resources/carParkImg.png')

     # cv2.rectangle(img, (51, 145), (157, 192), (255, 0, 255), 2)


     for pos in posList:
          cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255, 0, 255), 2)

     cv2.imshow("Image",img)
     cv2.setMouseCallback("Image",mouseClick)
     cv2.waitKey(1)