import cv2 as cv
import numpy as np
from utils import stackImages, getContours


path = 'images/1.jpg'
img = cv.imread(path)
imgContour = img.copy()

kernel = np.ones((5, 5), np.uint8)
imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
imgBlur = cv.GaussianBlur(imgGray, (7, 7), 0)
imgCanny = cv.Canny(img, 150, 200)
imgDialation = cv.dilate(imgCanny, kernel, iterations=20)
# cv.imshow("imgEroded Image", imgDialation)

# imgCanny_1 = cv.Canny(imgDialation, 50,50)

getContours(imgCanny, imgContour)

imgBlank = np.zeros_like(img)

imgStack = stackImages(0.6, ([img, imgGray, imgBlur],
                             [imgCanny, imgContour, imgBlank]))

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
