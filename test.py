# coding: utf-8
import numpy as np
import cv2
from imutils.perspective import four_point_transform
import imutils
# 注意：请先安装opencv-python
# 参考教程 https://www.cnblogs.com/lclblack/p/6377710.html

photo = cv2.imread("4.jpg")  # 待处理的文件名在这里
rows, cols, channels = photo.shape
# 如果图片过大，可以缩小一下
# photo = cv2.resize(photo,(cols//2, rows//2))
cv2.imshow("raw",photo)

# 以下是对于圈涂颜色的限制 ：HSV 绿色
# 参考 https://www.cnblogs.com/wangyblzu/p/5710715.html
#      http://blog.csdn.net/jkwwwwwwwwww/article/details/53401149
color1 = np.array([35, 50, 50])
color2 = np.array([78, 255, 255])
hsv = cv2.cvtColor(photo, cv2.COLOR_BGR2HSV)  # 转换为HSV模式的图片
mask = cv2.inRange(hsv, color1, color2)  # 获得遮罩mask
mask = cv2.dilate(mask, None, iterations=2)
mask = cv2.erode(mask, None, iterations=2)
# 开运算 先腐蚀 后膨胀
cv2.imshow("mask", mask)
cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # 寻找圈画区域矩形
mistakset = []
if len(cnts) > 0:
    cnts = filter(lambda a:cv2.contourArea(a)>300,cnts)  # 过滤面积较小区域
    for c in cnts:
        s = cv2.minAreaRect(c)  # 最小外接矩形轮廓
        box=cv2.boxPoints(s)  # 获得矩形顶点
        mistakset.append(four_point_transform(photo, box)) # 添加到错题集合
    i = 0
    for mis in mistakset:
        i=i+1
        gray = cv2.cvtColor(mis,cv2.COLOR_BGR2GRAY)  # 转成灰度模式
        # cv2.imshow("gray", gray)
        m = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,27, 20)  # 进行二值化
        cv2.imshow(u'mistake%d'%i,m)
        cv2.imwrite(u'mistake%d.png'%i,m)  # 保存
cv2.waitKey()