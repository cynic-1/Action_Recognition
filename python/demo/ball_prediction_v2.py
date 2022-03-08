import json
import os
import cv2
import matplotlib.pyplot as plt

import numpy as np


def produceCSVTable(csv_name, x, y, xAxis_name, yAxis_name):
    num = min(len(x), len(y))
    with open(csv_name, "w") as f:
        f.write(f"{xAxis_name},{yAxis_name}\n")
        for i in range(num):
            f.write(f"{x[i]},{y[i]}\n")


def get_volleyCenter(ball_path):
    with open(ball_path, "r") as f:
        _volley_position = json.load(f)
    volley_position = []
    for i in range(len(_volley_position)):
        if len(_volley_position[i]) == 0:
            volley_position.append([])
        else:
            x1, y1, x2, y2 = _volley_position[i][0]
            volley_position.append([(x1 + x2) / 2, (y1 + y2) / 2])
    return volley_position


# 定义Average对象，实现动态添加数据求平均值
class Average:
    def __init__(self):
        self.__cnt = 0
        self.__total = 0

    def add(self, num):
        self.__cnt += 1
        self.__total += num

    def getAverage(self):
        if self.__cnt != 0:
            return self.__total / self.__cnt
        else:
            return 0

    def clear(self):
        self.__cnt = 0
        self.__total = 0

    def isEmpty(self):
        return self.__cnt == 0


# 深度拷贝层叠的列表结构
def deepcopy(obj):
    if type(obj) != list:
        return obj
    else:
        res = []
        for item in obj:
            res.append(deepcopy(item))
        return res


# 遍历从start到end的全段曲线，拟合一个直线方程
# 需要start到end近似要保持在一条直线上
def getLineFunc(vpc, start, end):
    average = Average()
    for i in range(start, end-1):
        dist = (vpc[i+1][0] - vpc[i][0]) / (vpc[i+1][1] - vpc[i][1])
        average.add(dist)
    id = vpc[start][1]
    pos = vpc[start][0]
    k = average.getAverage()

    def __line_f(imageID):
        # y - pos = k * (x - id)
        return pos + k * (imageID - id)
    return __line_f


def fill_curve(left, mid, right, volley_position, vpc, is_exist, is_start, is_end):
    f_left = getLineFunc(vpc, left+2, mid-2)
    f_right = getLineFunc(vpc, mid+2, right-2)
    shape = "^" if (vpc[left+1][0] - vpc[left][0] > 0) else "V"
    left_index = 1 if is_start else vpc[left][1]
    right_index = len(volley_position) if is_end else (vpc[right][1]-3)
    for i in range(left_index, right_index+1):
        if not is_exist[i]:
            is_exist[i] = True
            value = min(f_left(i), f_right(i)) if shape == "^" else \
                max(f_left(i), f_right(i))
            volley_position[i-1].append(value)


def annotate_image(input_path, output_path, volley_position, _volley_position):
    # 将x坐标预测值绘制到图像上
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    total_num = len(os.listdir(input_path))

    for i in range(1, total_num+1):
        img = cv2.imread(input_path + f"{i}.jpg")
        if len(_volley_position[i-1]) == 0:
            color = (0, 0, 100)
        else:
            color = (0, 0, 255)
        cv2.circle(img, (int(volley_position[i-1][0]), 40), 10, color, -1)
        # img = img.copy()
        cv2.imwrite(output_path + f"{i}.jpg", img)

        if i % 20 == 0:
            print(f"Finish annotate {i} images.")


def predict_speed_x(__volley_position: list):
    size = len(__volley_position)
    speed = np.zeros((size, 2))
    interval = 1 / 30
    valid_num = 0
    valid_list = [False for j in range(size)]
    for i in range(1, size):
        # 说明该帧和上一帧都检测到排球了
        if len(__volley_position[i - 1]) != 0 and len(__volley_position[i]) != 0:
            valid_num += 1
            v_x = (__volley_position[i][0] - __volley_position[i - 1][0]) / interval
            v_y = (__volley_position[i][1] - __volley_position[i - 1][1]) / interval
            speed[i][0] = v_x
            speed[i][1] = v_y
            valid_list[i] = True

    # 合格帧定义：该帧和上一帧都能检测到球的位置
    print("合格帧整体比例：%.2f%%" % (valid_num / size * 100))

    # 预测速度和坐标
    for i in range(1, size):
        # 位置未捕获，且上一帧没有问题，捕获到了速度
        if len(__volley_position[i]) == 0:
            # 预测x坐标
            __volley_position[i].append(__volley_position[i - 1][0] + speed[i - 1][0] * interval)
            speed[i][0] = (__volley_position[i][0] - __volley_position[i - 1][0]) / interval
            valid_list[i] = True
        else:
            if not valid_list[i]:
                speed[i][0] = (__volley_position[i][0] - __volley_position[i - 1][0]) / interval
                valid_list[i] = True
    return speed


if __name__ == "__main__":
    volley_position = get_volleyCenter("../volleyball_detect.json")
    _volley_position = deepcopy(volley_position)
    _volley_position1 = deepcopy(volley_position)

    # 传统的紧邻速度直接推算法预测
    predict_speed_x(_volley_position1)

    # volleyball_position_continual_version
    # vpc[index] = [x_pos, image_id]
    vpc = []
    for i, pos in enumerate(volley_position):
        if len(pos) != 0:
            vpc.append([pos[0], i + 1])

    # 先添加vpc中的第一项
    extrema = [0]
    for i in range(1, len(vpc)-1):
        if vpc[i][0] > vpc[i-1][0] and vpc[i][0] > vpc[i+1][0]:
            extrema.append(i)
        elif vpc[i][0] < vpc[i-1][0] and vpc[i][0] < vpc[i+1][0]:
            extrema.append(i)
    extrema.append(len(vpc)-1)

    # is_exist是从1开始的记录某张图片是否确实排球坐标的数组
    is_exist = [len(pos) != 0 for pos in volley_position]
    is_exist.insert(0, False)
    for i in range(0, len(extrema)-2):
        left = extrema[i]
        mid = extrema[i+1]
        right = extrema[i+2]
        fill_curve(left, mid, right, volley_position, vpc, is_exist,
                   is_start=(i == 0), is_end=(i == len(extrema)-2))

    # 265-276是变形最厉害的一段范围
    annotate_image("../pose_images/", "predict_ball/", volley_position, _volley_position)

    # # 利用matplot作图
    # fig = plt.figure(num=1)
    # plt.scatter(range(total_num), [i[0] for i in volley_position])
    # plt.show()

    print(volley_position)
    imageID = []
    pos_list = []
    for i, pos in enumerate(volley_position):
        if len(pos) != 0:
            imageID.append(i+1)
            pos_list.append(pos[0])
        else:
            print(f"found image {i} not predicted")

    fig = plt.figure(num=1)
    plt.scatter(imageID, pos_list)
    plt.show()

    # 将速度信息输出到csv文件
    # produceCSVTable("speed.csv", [(i+1) for i in range(total_num)], speed[:, 0],
    #                 xAxis_name="image_ID", yAxis_name="Speed")
    # produceCSVTable("position_x.csv", [(i+1) for i in range(total_num)],
    #                 [i[0] for i in volley_position], xAxis_name="image_ID",
    #                 yAxis_name="position_x")
