import json
import os
import math
import numpy as np

import cv2
from detectron2_package import VolleyballDetect as Detect


def getboxes(imgpath, jsonpath):
    if os.path.exists(jsonpath + "/boxes.json"):
        return
    else:
        files = os.listdir(imgpath)  # 得到文件夹下的所有文件名称
        length = len(files)
        boxes = [length, 0, 0, 0]
        for i in range(1, length + 1):  # 遍历文件夹
            img = cv2.imread(imgpath + "/" + str(i) + ".jpg")
            # 获取球的位置
            box = Detect.detect_ball(img)
            if len(box) >= 1:
                boxes.extend(box[0].astype(float))
            else:
                boxes.extend([0, 0, 0, 0])
        # 把boxex信息写入json，避免多次使用detectron
        with open(jsonpath + "/boxes.json", 'w') as file_object:
            json.dump(boxes, file_object)

def find_distance(imgpath, jsonpath):
    getboxes(imgpath, jsonpath)  # 得到boxes信息的json文件
    files = os.listdir(imgpath)  # 得到图片文件夹下的所有文件名称
    ball_loc = [[0] for n in range(500)]  # 声明二维数组装每张图片的球信息——# x1, y1, x2, y2, diatance
    # 获取球的位置信息
    with open(jsonpath + "/boxes.json", "r") as f:  # 获取boxes信息
        json_dict = json.load(f)
    boxes = []
    for i in range(1, json_dict[0] + 1):
        boxes.append([json_dict[i * 4], json_dict[i * 4 + 1], json_dict[i * 4 + 2], json_dict[i * 4 + 3]])  # 从下标0开始
    # 获取distance信息
    for i in range(1, len(files) + 1):  # 遍历文件夹
        img = cv2.imread(imgpath + "/" + str(i) + ".jpg")
        # 获得humanpoints
        with open(jsonpath + "/" + str(i) + "_keypoints.json", "r") as f:
            json_dict = json.load(f)
        people_cnt = len(json_dict["people"])
        humanpoints = np.zeros((10, 25, 3))
        if people_cnt != 0:
            pose_keypoints_2d = json_dict["people"][0]["pose_keypoints_2d"]
            for j in range(25):
                humanpoints[0][j] = [pose_keypoints_2d[j * 3], pose_keypoints_2d[j * 3 + 1],
                                     pose_keypoints_2d[j * 3 + 2]]
        # 获取球的位置
        ball_loc[i] = boxes[i - 1] + [distance(humanpoints, boxes[i - 1])]  # x1, y1, x2, y2, diatance

    return ball_loc

def distance(humanpoints, ball):
    elbow = humanpoints[0][6]
    hand = humanpoints[0][7]
    center = (ball[0] + ball[2]) / 2, (ball[1] + ball[3]) / 2
    A = elbow[1] - hand[1] #A = y1 - y2
    B = elbow[0] - hand[0] #B = x1 - x2
    C = elbow[0]*(elbow[1] - hand[1]) - elbow[1]*(elbow[0] - hand[0]) #
    d = abs(A * center[0] + B * center[1] +C) / math.sqrt(A**2 + B**2)
    return d

def find_keypic(total, ball_loc):
    target = []
    last = 1000
    lastlast = 1000
    for j in range(1, total):
        if ((ball_loc[j][4] > last) and (last < lastlast)):  # 刚刚反弹——我们所需的计算速度的图片为该图片和其前一张图片
            target.append(j)
        lastlast = last
        last = ball_loc[j][4]
    return target

def speed(imgpath, jsonpath, interval):  # interval 是时间间隔
    ball_loc = find_distance(imgpath, jsonpath)
    files = os.listdir(imgpath)
    # 寻找所需的图片中的球位置——与手臂离得最近的2张
    target = find_keypic(len(files), ball_loc)
    # 求速度
    ratio = abs(21 / (ball_loc[1][0] - ball_loc[1][2]) * 0.01)  # 0.01为了化为米的单位
    speed_all = {}
    for j in target:
        center1 = (ball_loc[j - 1][0] + ball_loc[j - 1][2]) / 2, (ball_loc[j - 1][1] + ball_loc[j - 1][3]) / 2
        center2 = (ball_loc[j][0] + ball_loc[j][2]) / 2, (ball_loc[j][1] + ball_loc[j][3]) / 2
        speed_3d = math.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2) * ratio / interval
        speed_all.update({j: speed_3d})
        speed_all.update({j - 1: speed_3d})
        print(f"第{j-1}和{j}张图:速度{speed_3d}m/s")

    return speed_all

def direction(imgpath, jsonpath): #length是文件夹中的个数, ball_loc是计算好的球的x1y1x2y2distance数组
    ball_loc = find_distance(imgpath, jsonpath)
    files = os.listdir(imgpath)
    # 寻找所需的图片中的球位置——与手臂离得最近的2张
    target = find_keypic(len(files), ball_loc)
    #求方向
    direction_all = {}
    for i in range(1, len(files) + 1):  # 遍历文件夹
        if i in target:
            img = cv2.imread(imgpath + "/" + str(i) + ".jpg")
            # 获得humanpoints
            with open(jsonpath + "/" + str(i) + "_keypoints.json", "r") as f:
                json_dict = json.load(f)
            people_cnt = len(json_dict["people"])
            humanpoints = np.zeros((10, 25, 3))
            if people_cnt != 0:
                pose_keypoints_2d = json_dict["people"][0]["pose_keypoints_2d"]
                for j in range(25):
                    humanpoints[0][j] = [pose_keypoints_2d[j * 3], pose_keypoints_2d[j * 3 + 1],
                                         pose_keypoints_2d[j * 3 + 2]]
            #计算每张图中的方向——球的运动轨迹与关节6,7的夹角
            center1 = (ball_loc[i - 1][0] + ball_loc[i - 1][2]) / 2, (ball_loc[i - 1][1] + ball_loc[i - 1][3]) / 2
            center2 = (ball_loc[i][0] + ball_loc[i][2]) / 2, (ball_loc[i][1] + ball_loc[i][3]) / 2
            v1x = center2[0] - center1[0]
            v1y = center2[1] - center1[1]
            v2x = humanpoints[0][7][0] - humanpoints[0][6][0]
            v2y = humanpoints[0][7][1] - humanpoints[0][6][1]
            cos = (v1x*v2x+v1y*v2y)/((math.sqrt(v1x*v1x+v1y*v1y))*(math.sqrt(v2x*v2x+v2y*v2y)))
            theta = math.acos(cos)
            direction_all.update({i:theta})
            print(f"第{i-1}和{i}张图:球与小臂的夹角为{theta*(180.0/math.pi)}度")

    return direction_all





if __name__ == "__main__":
    imgpath = os.path.dirname(os.path.realpath(__file__)) + "/images/wrongSelfPadding1"
    jsonpath = os.path.dirname(os.path.realpath(__file__)) + "/images/json"
    interval = 1 / 12  # 两帧间隔——1/12秒
    speed(imgpath, jsonpath, interval)
    direction(imgpath, jsonpath)
