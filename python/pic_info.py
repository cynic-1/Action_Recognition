import json
import os
import sys
import time

import cv2
import numpy
import numpy as np

def ball_height(humanpoints, ballloc): #humanpoints 是关节坐标的三维数组：[人][关节][横/纵坐标]；balloc是球坐标的一维数组[左下x，左下y，右上x，右上y]
    x1, y1, x2, y2 = ballloc
    length = x2 - x1
    ball_center = (x1 + x2)/2, (y1 + y2)/2
    left_foot = humanpoints[0][14]
    right_foot = humanpoints[0][11]
    center = (left_foot+right_foot)/2
    # k1 = (left_foot[1]-right_foot[1])/(left_foot[0]-right_foot[0])
    # b1 = left_foot[1] - k1 * left_foot[0]
    # k2 = -1/k1
    # b2 = center[1] - k2 * center[0]
    height_2d = center[1] - ball_center[1]
    height_3d = height_2d * 21/length
    return height_3d

def person_height(humanpoints, ballloc): #humanpoints 是关节坐标的三维数组：[人][关节][横/纵坐标]
    x1, y1, x2, y2 = ballloc
    length = x2 - x1
    left_foot = humanpoints[0][14]
    right_foot = humanpoints[0][11]
    head = humanpoints[0][0]
    center = (left_foot + right_foot)/2
    return (center[1] - head[1])*21/length



if __name__ == "__main__":
    # produce_json()  # 先在output_json目录下输出json文件

    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)  # 切换回原来的路径

    img = cv2.imread("./images/3.jpg")  # numpy.ndarray类型
    img_origin = img.copy()
    print(img.shape)  # 输出 几行几列几维颜色

    # 读取和转化JSON文件
    with open("output_json/3_keypoints.json", "r") as f:
        json_dict = json.load(f)

    people_cnt = len(json_dict["people"])
    print(f"一共有{people_cnt}个人在画面中。")
    humanpoints = np.zeros((10, 25, 3))
    if people_cnt != 0:
        pose_keypoints_2d = json_dict["people"][0]["pose_keypoints_2d"]
        for i in range(25):
            humanpoints[0][i] = [pose_keypoints_2d[i * 3], pose_keypoints_2d[i * 3 + 1], pose_keypoints_2d[i * 3 + 2]]

    ballloc = [303.33194, 499.16248, 333.36005, 532.0776]
    ball_hei = ball_height(humanpoints, ballloc)
    print(ball_hei)