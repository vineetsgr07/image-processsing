import cv2 as cv
import numpy as np
from utils import stackImages, getContours, trimImage
from PIL import Image
from pytesseract import image_to_string, image_to_boxes

path = 'images/4.jpg'
img = cv.imread(path)
actualImage = img.copy()

imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
imgCanny = cv.Canny(imgGray, 150, 200)
imageBox = img.shape

imgBlank = np.zeros_like(imgGray)

kernel = np.ones((5, 5), np.uint8)
imgDialation = cv.dilate(imgCanny, kernel, iterations=10)

trimLeftSectionX, trimRightSectionY, croppedImage, croppedDialationImage = getContours(imgDialation, actualImage)

tripImageDimension = trimImage(imgDialation)

imgStack = stackImages(0.6, ([imgDialation, croppedDialationImage, croppedImage], [imgGray, actualImage, croppedImage]))

im_pil = Image.fromarray(croppedImage)
im_np = np.asarray(im_pil)
characterWithText = image_to_boxes(im_pil)
imageWithText = image_to_string(im_pil)



cv.imshow("stack", imgStack)
cv.waitKey(0)
