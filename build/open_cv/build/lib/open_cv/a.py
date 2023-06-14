import numpy as np
import cv2


# # 生成一组随机点
# points = np.random.randint(0, 300, (100, 2))
# print(points)
# # 计算拟合的椭圆
# center = cv2.fitEllipse(points)

# # 画出拟合的椭圆
# img = np.zeros((300, 300, 3), dtype=np.uint8)
# cv2.ellipse(img, center, (255, 0, 0), 2)
# print(points.shape)
# # # 画出原始点
# # for point in points:
# #     cv2.circle(img, tuple(point), 2, (0, 0, 255), -1)

# cv2.imshow("Fit Circle to Points", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

print(cv2.__version__)