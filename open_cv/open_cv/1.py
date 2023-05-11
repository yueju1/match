import numpy as np
import cv2 as cv
img = cv.imread('/home/pmlab/Pictures/Screenshots/Screenshot from 2023-05-11 11-42-38.png', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
ret,thresh = cv.threshold(img,127,255,0)
contours,hierarchy = cv.findContours(thresh, 1, 2)
cnt = contours[0]
M = cv.moments(cnt)
print( M )