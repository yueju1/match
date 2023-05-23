import cv2

asd = cv2.imread('/home/pmlab/yueju3/robot/Greifer_Unterseitenkamera.bmp')

cv2.namedWindow('camera', 0)
cv2.resizeWindow("camera", 1000, 1000)
    # cv2.namedWindow('asd', 0)
    # cv2.resizeWindow("asd", 1000, 1000)
    # Display image

cv2.imshow("camera", asd)
    # cv2.imshow('asd', part)
    # cv2.imshow('asd', casd)
cv2.waitKey()