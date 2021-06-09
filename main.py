import cv2 as cv
import numpy as np
from utils import stackImages

path = 'images/4.jpg'
img = cv.imread(path)
imgContour = img.copy()

imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
imgBlur = cv.GaussianBlur(imgGray, (7, 7), 10)
imgCanny = cv.Canny(imgGray, 150, 200)
imageBox = img.shape

def getContours(imgDialation):
    contours, hierarchy = cv.findContours(imgDialation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        print(x, w)
        cv.drawContours(imgContour, cnt, -1, (255, 255, 0), 10)

imgBlank = np.zeros_like(imgGray)

kernel = np.ones((5,5),np.uint8)
imgDialation = cv.dilate(imgCanny, kernel, iterations=5)

getContours(imgDialation)

imgStack = stackImages(0.6, ([imgGray, imgContour, imgDialation],
                             [imgGray, imgContour, imgDialation]))

cv.imshow("stack", imgStack)

# # cv.imshow("Grey Image", imgGray)
# # cv.imshow("Blur Image", imgBlur)
# # cv.imshow("Canny Image", imgGray)
# cv.imshow("Dialation Image", imgDialation)
#
# print(img.shape)
#
# # Height then width
# imgCropped = imgDialation[0:200, 200:500]
# cv.imshow("cropped Image", imgCropped)


# pts1 = np.float32([[111, 219], [287, 188], ])

cv.waitKey(0)
