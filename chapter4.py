"""Drawing shapes (lines, rectangles, circle) on image"""
import cv2
import numpy

img = numpy.zeros((512, 512, 3), numpy.uint8)
#print(img)
#

cv2.line(img, (0, 0), (img.shape[1], img.shape[0]), (0,255, 0), 3)
cv2.rectangle(img, (0, 0), (250, 350), (0, 0 , 255), 2) #replace 2 by cv2.FILLED to fill the rectangle
cv2.circle(img, (400, 50), 30,(255, 0, 0), 5)
cv2.putText(img, 'OPENCV', (300, 200), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 150, 0), 3)

cv2.imshow('Image', img)

cv2.waitKey(0)
