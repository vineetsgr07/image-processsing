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


def getContours(imgDialation):
    imageDimension = imgDialation.shape
    height = imageDimension[0]
    width = imageDimension[1]
    contours, hierarchy = cv.findContours(imgDialation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    store = []
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        store.append({'x': x, 'y': y, 'w': w, 'h': h})
        cv.drawContours(imgDialation, cnt, -1, (255, 255, 0), 10)

    cropImage(imgDialation, store[1]['y'], store[0]['h'], store[0]['x'], store[0]['w'])

    removeAfterX = removeLeftSection(store, width/2)
    removeBeforeX = removeBeforeXFunc(store)
    removeAfterY = removeAfterYFunc(store)
    removeBeforeY = removeBeforeYFunc(store)
    detectImage = detectImageFunc(store)

    return {
        removeAfterX,
        removeBeforeX,
        removeAfterY,
        removeBeforeY,
        detectImage
    }


# Remove Right section of article
def removeLeftSection(store, centerPoint):
    remove = []
    for shape in store:
        x, y, w, h = shape
        if(y <= centerPoint):
            remove.append({'y': y})


    return True


# Remove Left section of article
def removeBeforeXFunc(store):
    return True


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
    cv.imshow("crop_img", crop_img)
    return crop_img

def trimImage(imgDialation):
    TrimmedImage = 0
    return TrimmedImage