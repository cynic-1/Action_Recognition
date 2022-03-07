# 该模块对图像修改的方式是在原图像上增添内容，若已经增添过一次，
# 则会重复添加，可能会出现内容互相覆盖的情况
# 没有获取到球的帧球的位置会被标记为[0, 0]

import json
import os
import math
import numpy as np

import cv2
from PIL import Image, ImageDraw, ImageFont


def getboxes(imgpath, jsonpath, balljson):
    from detectron2_package import VolleyballDetect as Detect
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
        # 把boxes信息写入json，避免多次使用detectron
        with open(jsonpath + "/boxes.json", 'w') as file_object:
            json.dump(boxes, file_object)


def find_distance(imgpath, jsonpath, balljson):
    # getboxes(imgpath, jsonpath, balljson)  # 得到boxes信息的json文件
    files = os.listdir(imgpath)  # 得到图片文件夹下的所有文件名称
    ball_loc = [[0] for n in range(1000)]  # 声明二维数组装每张图片的球信息——# x1, y1, x2, y2, diatance
    # 获取球的位置信息
    with open(balljson, "r") as f:  # 获取boxes信息
        json_dict = json.load(f)
    boxes = []
    for i in range(0, len(json_dict)):
        if json_dict[i]:
            boxes.append(json_dict[i][0])  # 从下标0开始
        else:
            boxes.append([0, 0, 0, 0])
    # 获取distance信息
    for i in range(1, len(files) + 1):  # 遍历文件夹
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
    A = elbow[1] - hand[1]  # A = y1 - y2
    B = elbow[0] - hand[0]  # B = x1 - x2
    C = elbow[0] * (elbow[1] - hand[1]) - elbow[1] * (elbow[0] - hand[0])  #
    domi = math.sqrt(A ** 2 + B ** 2) if math.sqrt(A ** 2 + B ** 2) > 0 else 0.000000001
    d = abs(A * center[0] + B * center[1] + C) / domi
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


def cv2ImgAddText(img, text, left, top, textColor, textSize):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def height(imgpath, jsonpath, balljson):  # humanpoints 是关节坐标的三维数组：[人][关节][横/纵坐标]；balloc是球坐标的一维数组[左下x，左下y，右上x，右上y]
    ball_loc = find_distance(imgpath, jsonpath, balljson)
    files = os.listdir(imgpath)
    height_all = {}

    # 边计算高度边在图像上标记
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
        # 计算每张图中球的高度
        x1, y1, x2, y2, d = ball_loc[i]
        if x1 == 0 and y1 == 0 and x2 == 0 and y2 == 0:
            height_all.update({i: None})
        else:
            length = x2 - x1
            ball_center = (x1 + x2) / 2, (y1 + y2) / 2
            left_foot = humanpoints[0][14]
            right_foot = humanpoints[0][11]
            center = (left_foot + right_foot) / 2
            height_2d = center[1] - ball_center[1]
            height_3d = height_2d * 21 / length
            height_all.update({i: height_3d})
            # 画图
            img1 = cv2.imread(imgpath + "/" + str(i) + ".jpg")
            img1 = cv2ImgAddText(img1, "球离地面的高度：%.0f cm" % height_3d, ball_loc[i][2] + 20, ball_loc[i][3] - 50,
                                 (255, 255, 255), 20)
            cv2.imwrite(imgpath + "/" + str(i) + ".jpg", img1)
    return height_all


def speed(imgpath, jsonpath, balljson, interval):  # interval 是时间间隔
    # ball_loc的下标访问从1开始
    ball_loc = find_distance(imgpath, jsonpath, balljson)
    files = os.listdir(imgpath)
    # 不需要 寻找所需的图片中的球位置——与手臂离得最近的2张(target存放选中的连续两张图片中第二张的下标)
    # 直接对每两帧之间求速度
    # target = find_keypic(len(files), ball_loc)
    # 求速度转换因子
    ratio = abs(21 / (ball_loc[1][0] - ball_loc[1][2]) * 0.01)  # 0.01为了化为米的单位
    speed_all = {}

    # 求每两帧之间的速度
    for j in range(2, len(files)+1):
        center1 = (ball_loc[j - 1][0] + ball_loc[j - 1][2]) / 2, (ball_loc[j - 1][1] + ball_loc[j - 1][3]) / 2
        center2 = (ball_loc[j][0] + ball_loc[j][2]) / 2, (ball_loc[j][1] + ball_loc[j][3]) / 2
        speed_3d = math.sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2) * ratio / interval
        
        # 只需要标记一帧的速度即可
        speed_all.update({j: speed_3d})
        print(f"第{j - 1}和{j}张图:速度{speed_3d}m/s")

    # 在图中标注
    for j in range(2, len(files)+1):
        img2 = cv2.imread(imgpath + "/" + str(j) + ".jpg")
        img4 = cv2ImgAddText(img2, "球的速度：%.2f m/s" % speed_all.get(j), ball_loc[j][2] + 20, ball_loc[j][3] - 30,
                             (255, 255, 255), 20)
        cv2.imwrite(imgpath + "/" + str(j) + ".jpg", img4)
    return speed_all


def direction(imgpath, jsonpath, balljson):  # length是文件夹中的个数, ball_loc是计算好的球的x1,y1,x2,y2,distance数组
    ball_loc = find_distance(imgpath, jsonpath, balljson)
    files = os.listdir(imgpath)
    # 寻找所需的图片中的球位置——与手臂离得最近的2张
    # target = find_keypic(len(files), ball_loc)
    # 求方向
    direction_all = {}
    for i in range(2, len(files) + 1):  # 遍历文件夹
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
        # 计算每张图中的方向——球的运动轨迹与关节6,7的夹角
        center1 = (ball_loc[i - 1][0] + ball_loc[i - 1][2]) / 2, (ball_loc[i - 1][1] + ball_loc[i - 1][3]) / 2
        center2 = (ball_loc[i][0] + ball_loc[i][2]) / 2, (ball_loc[i][1] + ball_loc[i][3]) / 2

        # 球的速度矢量
        v1x = center2[0] - center1[0]
        v1y = center2[1] - center1[1]

        # 小臂骨骼(6,7)矢量
        v2x = humanpoints[0][7][0] - humanpoints[0][6][0]
        v2y = humanpoints[0][7][1] - humanpoints[0][6][1]

        domi = math.sqrt(v1x * v1x + v1y * v1y) * math.sqrt(v2x * v2x + v2y * v2y) if math.sqrt(v1x * v1x + v1y * v1y) * math.sqrt(v2x * v2x + v2y * v2y)>0 else 0.0000000001
        cos = (v1x * v2x + v1y * v2y) / domi
        # 球与小臂的夹角，暂时先不用了
        theta = math.acos(cos)

        # 只关心角的大小，不关心角的方向
        theta_ball_horizon = abs(math.atan2(v1y, v1x)) if v1x != 0 else math.pi/2

        # 求的不是球与小臂的夹角（虽然也有用），而是球飞行过程中与水平线的夹角
        # direction_all.update({i: theta * (180.0 / math.pi)})
        direction_all.update({i: theta_ball_horizon * (180.0 / math.pi)})

        # print(f"第{i - 1}和{i}张图:球与小臂的夹角为{theta * (180.0 / math.pi)}度")
        print(f"第{i - 1}和{i}张图:球飞行方向与水平线的夹角为{theta_ball_horizon * (180.0 / math.pi)}度")

        # 在图中标注
        img1 = cv2.imread(imgpath + "/" + str(i) + ".jpg")
        img2 = cv2ImgAddText(img1, "球方向与水平线的夹角：%.0f" % direction_all.get(i) + chr(0x00b0), ball_loc[i][2] + 20,
                             ball_loc[i][3] - 10, (255, 255, 255), 20)

        v = math.sqrt(v1x**2 + v1y**2)
        std_x = v1x / v * 50 if v != 0 else 0
        std_y = v1y / v * 50 if v != 0 else 0

        # 画一条球的方向指示线
        img3 = cv2.arrowedLine(img2, (int(center2[0]), int(center2[1])),
                                (int(center2[0] + std_x), int(center2[1] + std_y)), (179, 113, 60), 2, 8)

        cv2.imwrite(imgpath + "/" + str(i) + ".jpg", img3)

    return direction_all


if __name__ == "__main__":
    # imgpath = os.path.dirname(os.path.realpath(__file__)) + "/images/rightPadding"
    # jsonpath = os.path.dirname(os.path.realpath(__file__)) + "/pose_images_json"
    # balljson = os.path.dirname(os.path.realpath(__file__)) + "/volleyball_detect.json"
    imgpath = "pose_results"
    jsonpath = "pose_images_json"
    balljson = "volleyball_detect.json"
    interval = 1 / 30  # 两帧间隔——1/12秒
    height(imgpath, jsonpath, balljson)
    speed(imgpath, jsonpath, balljson, interval)
    direction(imgpath, jsonpath, balljson)
