'''
Created on Jul 16, 2016

@author: myths
'''

import matplotlib.pyplot as plt
import cv2, numpy as np

def showImage(img):
    plt.imshow(img)
    plt.show()

def otsu(img):
    _, im = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return im

def resize(img, width, height):
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

def bersen(img, blockSize=11, c=2):
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, c)

def opening(img, kernelSize=2):
    kernel = np.ones((kernelSize, kernelSize), np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return opening

def closing(img, kernelSize=2):
    kernel = np.ones((kernelSize, kernelSize), np.uint8)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return closing