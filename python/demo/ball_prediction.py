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


def predict_speed_x(__volley_position: list):
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


# 返回a，b中的最小值，但若其中之一接近ignore_num，则忽略该数字
def min_safe(a, b, ignore_num=0, eps=0.01):
    if abs(a-ignore_num) < eps and abs(b-ignore_num) < eps:
        return None
    elif abs(a-ignore_num) < eps:
        return b
    elif abs(b-ignore_num) < eps:
        return a
    else:
        return min(a, b)


def max_safe(a, b, ignore_num=0, eps=0.01):
    if abs(a-ignore_num) < eps and abs(b-ignore_num) < eps:
        return None
    elif abs(a-ignore_num) < eps:
        return b
    elif abs(b-ignore_num) < eps:
        return a
    else:
        return max(a, b)



def adjust_mid_point(volley_position, id1, id2):
    # 用于判断从id1到id2之间的坐标变化是呈V形还是^形
    shape_judge = 1

    average = Average()
    isPredictPoint = [len(volley_position[j]) == 0 for j in range(id2+3)]
    predict_num1 = np.zeros((id2+3, ))
    predict_num2 = np.zeros((id2+3, ))
    begin_track = False
    i = id1
    final_track = False
    while i < id2:
        if not begin_track:
            if len(volley_position[i]) != 0 and len(volley_position[i+1]) != 0:
                begin_track = True
                shape_judge = volley_position[i+1][0] - volley_position[i][0]

        if begin_track:
            x1 = predict_num1[i] if isPredictPoint[i] else volley_position[i][0]
            x2 = predict_num1[i+1] if isPredictPoint[i+1] else volley_position[i+1][0]
            dist = x2 - x1
            # 与之前的平均值相差过大
            if (not average.isEmpty()) and (abs( (dist-average.getAverage()) / average.getAverage()) > 0.5):
                final_track = True
            else:
                average.add(dist)

            if isPredictPoint[i+2]:
                if final_track:
                    predict_num1[i+2] = x2 + average.getAverage()
                else:
                    predict_num1[i+2] = x2 + dist

        i += 1

    j = id2
    begin_track = False
    final_track = False
    average.clear()
    while j > id1:
        if not begin_track:
            if len(volley_position[j]) != 0 and len(volley_position[j-1]) != 0:
                begin_track = True

        if begin_track:
            x1 = predict_num1[j] if isPredictPoint[j] else volley_position[j][0]
            x2 = predict_num1[j-1] if isPredictPoint[j-1] else volley_position[j-1][0]
            dist = x2 - x1
            if (not average.isEmpty()) and (abs((dist-average.getAverage()) / average.getAverage()) > 0.5):
                final_track = True
            else:
                average.add(abs(dist))
            if isPredictPoint[j-2]:
                if final_track:
                    predict_num2[j-2] = x2 + average.getAverage()
                else:
                    predict_num2[j-2] = x2 + dist

        j -= 1

    for i in range(id1, id2+1):
        if isPredictPoint[i]:
            if shape_judge > 0:
                value = min_safe(predict_num1[i], predict_num2[i])
            else:
                value = max_safe(predict_num1[i], predict_num2[i])
            if value is not None:
                volley_position[i].append(value)
                # print(f"fixed img={i}, value={value}")

    print(f"shape between {id1} and {id2} is " + ("V" if shape_judge < 0 else "^"))


# 深度拷贝层叠的列表结构
def deepcopy(obj):
    if type(obj) != list:
        return obj
    else:
        res = []
        for item in obj:
            res.append(deepcopy(item))
        return res


if __name__ == "__main__":
    volley_position = get_volleyCenter("../volleyball_detect.json")
    _volley_position = deepcopy(volley_position)
    size = len(volley_position)
    speed = predict_speed_x(_volley_position)
    turning_points = []
    # 寻找速度反向突变点
    for i in range(1, size):
        if (speed[i][0] * speed[i - 1][0]) < 0:
            turning_points.append(i)
    print(turning_points)

    # 寻找球在半程中的中间点
    mid_way = []
    for i in range(len(turning_points)):
        if i + 1 < len(turning_points):
            mid_way_pos = (turning_points[i] + turning_points[i + 1]) // 2
            mid_way.append(mid_way_pos)

    print(mid_way)

    # for i in range(0, len(mid_way)-1):
    #     id1 = mid_way[i]
    #     id2 = mid_way[i+1]
    #     adjust_mid_point(volley_position, id1, id2)
    #
    # for i in range(size):
    #     if len(volley_position[i]) == 0:
    #         volley_position[i].append(_volley_position[i][0])

    # 265-276是变形最厉害的一段范围
    # 将x坐标预测值绘制到图像上
    output_path = "predict_ball/"
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    input_path = "../pose_images/"
    total_num = len(os.listdir(input_path))
    # for i in range(1, total_num+1):
    #     img = cv2.imread(input_path + f"{i}.jpg")
    #     if len(_volley_position[i-1]) == 0:
    #         color = (0, 0, 100)
    #     else:
    #         color = (0, 0, 255)
    #     cv2.circle(img, (int(volley_position[i-1][0]), 40), 10, color, -1)
    #     # img = img.copy()
    #     cv2.imwrite(output_path + f"{i}.jpg", img)

    # 利用matplot作图
    fig = plt.figure(num=1)
    plt.scatter(range(total_num), [i[0] for i in _volley_position])
    plt.show()

    imageID = []
    poslist = []
    for i, pos in enumerate(volley_position):
        if len(pos) != 0:
            imageID.append(i+1)
            poslist.append(pos[0])

    # print(imageID)
    # print(poslist)
    # fig = plt.figure(num=1)
    # plt.scatter(imageID, poslist)
    # plt.show()

    # 将速度信息输出到csv文件
    # produceCSVTable("speed.csv", [(i+1) for i in range(total_num)], speed[:, 0],
    #                 xAxis_name="image_ID", yAxis_name="Speed")
    # produceCSVTable("position_x.csv", [(i+1) for i in range(total_num)],
    #                 [i[0] for i in volley_position], xAxis_name="image_ID",
    #                 yAxis_name="position_x")
