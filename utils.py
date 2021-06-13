import cv2 as cv
import numpy as np


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None,
                                               scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv.cvtColor(imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def getContours(img_dialation, actualImage):

    imageDimension = img_dialation.shape
    height = imageDimension[0]
    width = imageDimension[1]
    contours, hierarchy = cv.findContours(img_dialation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    store = []
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        store.append({'x': x, 'y': y, 'w': w, 'h': h})
        cv.drawContours(img_dialation, cnt, -1, (255, 255, 0), 10)

    actualScreenDimension = 900
    fullWidthDimension = removeHeader(store, width, actualScreenDimension)

    trimLeftSectionX, trimRightSectionY = removeLeftSection(store, width)
    height = actualImage.shape[0]
    croppedImage = cropImage(actualImage, fullWidthDimension[0]['y'] + fullWidthDimension[0]['h'], height,
                             trimLeftSectionX, trimRightSectionY - trimLeftSectionX)
    croppedDialationImage = cropImage(img_dialation, fullWidthDimension[0]['y'] + fullWidthDimension[0]['h'], height,
                             trimLeftSectionX, trimRightSectionY - trimLeftSectionX)

    return trimLeftSectionX, trimRightSectionY, croppedImage, croppedDialationImage


# Remove Left section of article
def removeHeader(store, width, actualScreenDimension):
    fullWidthDimension = []
    for shape in range(len(store)):
        if width == int(store[shape]['w']):
            fullWidthDimension.append(store[shape])

    return fullWidthDimension


# Remove Right section of article
def removeLeftSection(store, width):
    pixelCount = [0] * width
    for shape in store:
        pixelCount = countPixel(pixelCount, shape, width)

    sum = 0
    for pixel in pixelCount:
        sum += pixel

    average = sum/width
    for pixel in range(len(pixelCount)):
        if pixelCount[pixel] < average-1:
            pixelCount[pixel] = 0

    trimLeftSectionX = 0
    trimRightSectionY = 0
    for pixel in range(len(pixelCount)):
        if pixelCount[pixel] > 0 and trimLeftSectionX == 0:
            trimLeftSectionX = pixel - 30
        if trimLeftSectionX > 0 and pixelCount[pixel] == 0:
            trimRightSectionY = pixel
            break;

    return trimLeftSectionX, trimRightSectionY


def countPixel(pixelCount, shape, width):
    x, y, w, h = shape
    for path in range(shape['x'], shape['y']):
        # There are some cases where actual image width is smaller than dialation_image width
        if shape['y'] < width:
            pixelCount[path] = pixelCount[path] + 1

    return pixelCount


# Remove Footer
def removeAfterYFunc(store):
    return True


# Remove Header
def removeBeforeYFunc(store):
    return True


def detectImageFunc(store):
    return True


def cropImage(image, y, h, x, w):
    crop_img = image[y:y + h, x:x + w]
    return crop_img


def trimImage(imgDialation):
    TrimmedImage = 0
    return TrimmedImage
