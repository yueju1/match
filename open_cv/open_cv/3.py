import cv2 as cv 

 
if __name__ == "__main__":
 
    im = cv.imread("/home/pmlab/yueju3/robot/Greifer_Unterseitenkamera.bmp")    # 读图
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)    # 转灰度图
    #gray2 = cv.GaussianBlur(gray, (5, 5), 1)
    gray2 = cv.medianBlur(gray, 7)
    canny = cv.Canny(gray2, 460, 500) # (460,800)
    _, thresh = cv.threshold(canny, 140, 220, cv.THRESH_BINARY)  # 二值化 
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)  # 轮廓查找
         最小二乘法拟合椭圆  椭圆检测能检测圆吗 摄像机侧边拍真的是椭圆吗（不倾斜，相互平行）
         # 检测椭圆内圈？
    for i in contours:  sobel? kaolv geng fuza yidian
        if len(i) >= 5 :
            retval = cv.fitEllipse(i)  # 取其中一个轮廓拟合椭圆
            cv.ellipse(im, retval, (0, 0, 255), thickness=1) # 在原图画椭圆
            cv.circle(im, (int(retval[0][0]),int(retval[0][1])),3, (0, 0, 255), -2)
            col = cv.cvtColor(canny, cv.COLOR_GRAY2BGR)
            cv.drawContours(col, contours, -1, (0, 0, 255), 1)
            print(retval) # 这里可以查看下fitEllipse的返回值的结构
        # 还有别的方法画椭圆中心吗
cv.namedWindow('ellip',0)
cv.resizeWindow('ellip',1000,1000)
cv.imshow("ellip", im)

cv.namedWindow('ellips',0)
cv.resizeWindow('ellips',1000,1000)
cv.imshow("ellips", col)
1300.6314697265625, 967.3241577148438
cv.waitKey()


# main:  if 走到了特定位置:

#           执行此图像检测程序