import cv2
import numpy
from numpy.ma.testutils import approx


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range (0,rows):
            for y in range (0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = numpy.zeros((height, width, 3), numpy.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range (0, rows):
            hor[x] = numpy.hstack(imgArray[x])
        ver = numpy.vstack(hor)
    else:
        for x in range (0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
                if len(imgArray[x].shape) == 2:
                    imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = numpy.hstack(imgArray)
        ver = hor
    return ver

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area > 500:
            cv2.drawContours(imgContours, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            #print(peri)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print(len(approx))
            objCor = len(approx)
            x, y, width, height = cv2.boundingRect(approx)

            if objCor == 3:
                 objectType = 'Tri'
            elif objCor == 4:
                aspRatio = width / float(height)
                if aspRatio > 0.95 and aspRatio < 1.05:
                    objectType = 'Square'
                else:
                    objectType = 'Rectangle'
            elif objCor > 4:
                objectType = 'Circle'
            else:
                objectType = 'None'

            cv2.rectangle(imgContours, (x, y), (x + width, y + height), (0, 255, 0), 2)
            cv2.putText(imgContours, objectType, ((x + (width // 2) - 10), (y + (height // 2))), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 2)

path = 'Resources/shapes.png'

img = cv2.imread(path)
imgContours = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
imgCanny = cv2.Canny(imgBlur, 50, 50)
imgBlank = numpy.zeros_like(img)
getContours(imgCanny)

imgStack = stackImages(0.5, ([img, imgGray, imgBlur], [imgCanny, imgContours, imgBlank]))
cv2.imshow('Stacked Images', imgStack)
cv2.waitKey(0)