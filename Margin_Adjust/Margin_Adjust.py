# encoding: utf-8

import cv2
import os
import numpy as np
import string
import time

def Margin_4_rect_center(filename):

    rects_center=[{}]*4
    img = cv2.imread(filename)
    Paper_width_mm=210
    Paper_length_mm=297
    Paper_width_dot=img.shape[1]
    Paper_length_dot=img.shape[0]
    x_mm_per_dot=Paper_width_mm/Paper_width_dot
    y_mm_per_dot=Paper_length_mm/Paper_length_dot

    target_rect_Side_length=5.8/x_mm_per_dot # cv2 get 5mm is about 5.8mm
    width_min=(5.8-0.6)/x_mm_per_dot
    width_max = (5.8 + 0.6)/x_mm_per_dot
    print(width_max,width_min)
    # 灰度图，滤波
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.medianBlur(gray, 1)
    # 边缘
    CANNY_THRESH_1 = 100
    CANNY_THRESH_2 = 200
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None, iterations=3)
    edges = cv2.erode(edges, None, iterations=1)

    # 查找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # print("Test image VC v2 get size and chanel：",img.shape)
    # 显示所有轮廓
    mask = np.zeros(img.shape)
    # print("cv2.findContours find object number:", len(contours))
    number = 0
    for c in contours:
        cv2.drawContours(mask, [c], 0, (0, 0, 255))
        rect = cv2.minAreaRect(c)
        # print(cv2.contourArea(c),rect,target_rect_Side_length)
        cv2.drawContours(mask, [c], 0, (0, 0, 255))
        # search 4 rectangle and get center X,Y
        if (rect[1][0] < width_max) and (rect[1][0] > width_min) and (rect[1][1] < width_max) and (rect[1][1] > width_min):
            rects_center[number]={"X":rect[0][0],"Y":rect[0][1]}
            number=number+1
            # print("number:",number,rect)
            print("number:",number,cv2.contourArea(c), rect, target_rect_Side_length)
            time.sleep(0.5)

    cv2.imwrite(filename.replace("jpg","bmp"), mask)

    # print(rects_center)
    Paper_center_X=img.shape[1]/2
    Paper_center_Y=img.shape[0]/2
    # print(Paper_center_X,Paper_center_Y)

    rects_sort_center=[{}]*4
    for rect in rects_center:
        if rect["X"]<Paper_center_X and rect["Y"]<Paper_center_Y:
            rects_sort_center[0]= {"X":rect["X"]*x_mm_per_dot,"Y":rect["Y"]*y_mm_per_dot}
        elif rect["X"]>Paper_center_X and rect["Y"]<Paper_center_Y:
            rects_sort_center[1]={"X":rect["X"]*x_mm_per_dot,"Y":rect["Y"]*y_mm_per_dot}
        elif rect["X"]<Paper_center_X and rect["Y"]>Paper_center_Y:
            rects_sort_center[2]={"X":rect["X"]*x_mm_per_dot,"Y":rect["Y"]*y_mm_per_dot}
        elif rect["X"]>Paper_center_X and rect["Y"]>Paper_center_Y:
            rects_sort_center[3]={"X":rect["X"]*x_mm_per_dot,"Y":rect["Y"]*y_mm_per_dot}
        else:
            pass
    # print(rects_sort_center)
    if product == "JiaoS":
        shift_X = -int((rects_sort_center[0]["X"]-x_target)*10+0.5)
        shift_Y = -int((rects_sort_center[0]["Y"] - y_target) * 10 + 0.5)
        scale= -int(((rects_sort_center[2]["Y"]-rects_sort_center[0]["Y"])-length_target)/length_target*1000+0.5)
        print(product,":",filename)
        print("shift_X:", shift_X)# +shift to left, - shift to right
        print("shift_Y:", shift_Y)# +shift to up, - shift to bottom
        print("scale:", scale)  #+enlarge, -reduce

    elif product == "Pro":
        shift_X = int((rects_sort_center[0]["X"]-x_target)*10+0.5)/10
        shift_Y = int((rects_sort_center[0]["Y"] - y_target) * 10 + 0.5)/10
        scale= int(((rects_sort_center[2]["Y"]-rects_sort_center[0]["Y"])-length_target)/length_target*1000+0.5)/10
        print(product,":",filename)
        print("shift_X(Main):", shift_X)# +shift to left, - shift to right
        print("shift_Y(Sub):", shift_Y)# +shift to up, - shift to bottom
        print("scale(Size adjust):", scale)  #+enlarge, -reduce
    else:
        pass


    return shift_X,shift_Y,scale



if __name__ == '__main__':


    # product = "JiaoS"
    product = "Pro"

    # front side
    x_target=7+2.5 #用尺子量， unit： mm
    y_target=9.3+2.5#用尺子量， unit： mm
    length_target=275.1#用尺子量， unit： mm
    shift_X,shift_Y, Scale = Margin_4_rect_center(r"2104131718030001_adjust.jpg")

    # # back side  duplex portrait+top to bottom
    # x_target=9.3+2.5
    # y_target=6.6+2.5
    # length_target=275.1
    # shift_X,shift_Y,Scale=Margin_4_rect_center("2104131542050001.jpg")



