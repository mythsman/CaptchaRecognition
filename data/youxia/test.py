import cv2
import numpy as np

img=cv2.imread('1.png',cv2.IMREAD_GRAYSCALE)
res=cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
cv2.imshow('test.png',res)
cv2.waitKey(0)
cv2.destroyAllWindows()
