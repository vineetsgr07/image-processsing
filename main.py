import cv2 as cv
import numpy as np
from utils import stackImages, getContours

path = 'images/4.jpg'
img = cv.imread(path)
imgContour = img.copy()

imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
imgCanny = cv.Canny(imgGray, 150, 200)
imageBox = img.shape

imgBlank = np.zeros_like(imgGray)

kernel = np.ones((5,5),np.uint8)
imgDialation = cv.dilate(imgCanny, kernel, iterations=5)

getContours(imgDialation)

imgStack = stackImages(0.6, ([imgGray, imgContour, imgDialation],
                             [imgGray, imgContour, imgDialation]))

cv.imshow("stack", imgStack)
cv.waitKey(0)
