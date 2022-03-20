import json
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from ball_prediction_common import *
import ball_predict_x

repair_throw_conventional_data = True
default_fill_range = 15
annotate_ball_data = True


# 返回各个帧的速度，不修改volley_position
def predict_speed(volley_position: list):
    size = len(volley_position)
    speed = [[] for _ in range(size)]
    interval = 1 / 30
    valid_num = 0
    valid_list = [False for _ in range(size)]
    for i in range(1, size):
        # 说明该帧和上一帧都检测到排球了
        if len(volley_position[i - 1]) != 0 and len(volley_position[i]) != 0:
            valid_num += 1
            v_x = (volley_position[i][0] - volley_position[i - 1][0]) / interval
            v_y = (volley_position[i][1] - volley_position[i - 1][1]) / interval
            speed[i].append(v_x)
            speed[i].append(v_y)
            valid_list[i] = True
    return speed


# 查找该点离最近的极值点的距离
# 此函数需要优化
def find_nearest_extrema(extrema, imageId):
    dist = len(extrema)
    pos = 0
    for i in range(len(extrema)):
        if dist > abs(imageId - extrema[i]):
            dist = abs(imageId - extrema[i])
            pos = extrema[i]
    return pos, dist


def conventional_speed_fix(speed, extrema):
    def is_valid(_i):
        return len(speed[_i]) != 0
    total_num = len(speed)
    for i in range(3, total_num):
        if (is_valid(i-1) and is_valid(i-2)) and (not is_valid(i)):
            if find_nearest_extrema(extrema, i)[1] < default_fill_range:
                continue
            speed[i] = [0, float(2 * speed[i-1][1] - speed[i-2][1])]


# 这里的start和end是真实的图片id
def getLineFunc(vpc, start, end):
    average = Average()
    for i in range(start, end-1):
        try:
            dist = (vpc[i+1][0] - vpc[i][0]) / (vpc[i+1][1] - vpc[i][1])
        except Exception as e:
            print(e)
            print(i)
            exit(0)
        average.add(dist)
    i = vpc[start][1]
    pos = vpc[start][0]
    k = average.getAverage()

    def __line_f(imageID):
        # y - pos = k * (x - id)
        return pos + k * (imageID - i)
    return __line_f


class Pair:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        print(f"({self.left}, {self.right})")


def turning_point_fix(speed, extrema):
    speed_c = []
    for i in range(len(speed)):
        if len(speed[i]) != 0:
            speed_c.append([speed[i][1], i])

    _extrema = [Pair(0, 0)]
    i = 0
    j = 0
    while i < len(extrema) and j < len(speed_c):
        if speed_c[j][1] == extrema[i]:
            _extrema.append(Pair(j, j))
            i += 1
        elif speed_c[j][1] < extrema[i] and (j+1 < len(speed_c) and speed_c[j+1][1] > extrema[i]):
            _extrema.append(Pair(j, j+1))
            i += 1
        j += 1
    _extrema.append(Pair(len(speed_c)-1, len(speed_c)-1))

    for i in range(0, len(_extrema)-2):
        tri_set = _extrema[i:i+3]

        left = tri_set[0].right
        midl = tri_set[1].left
        midr = tri_set[1].right
        right = tri_set[2].left

        const_range = 2
        line_left = getLineFunc(speed_c, left+const_range, midl-const_range)
        line_right = getLineFunc(speed_c, midr+const_range, right-const_range)

        left_p = find_nearest_extrema(extrema, imageId=speed_c[left][1])[0]
        mid_p = find_nearest_extrema(extrema, imageId=speed_c[midl][1])[0]
        right_p = find_nearest_extrema(extrema, imageId=speed_c[right][1])[0]

        # range = [left_p+1, mid_p-1]
        for j in range(left_p+1, mid_p):
            if len(speed[j]) == 0:  # 未被补全
                speed[j] = [0, line_left(j)]

        for j in range(mid_p+1, right_p):
            if len(speed[j]) == 0:
                speed[j] = [0, line_right(j)]


def main():
    volley_position = get_volleyCenter("../volleyball_detect.json")
    speed = predict_speed(volley_position)
    extrema, _ = ball_predict_x.predict_xAxis(volley_position)

    turning_point_fix(speed, extrema)
    # conventional_speed_fix(speed, extrema)

    # 利用matplotlib作图
    fig = plt.figure(num=1)
    x, y = volley_position_to_plot(speed, axis=1)
    plt.scatter(x, y)
    plt.show()

    # produceCSVTable("Vy.csv", x, y, xAxis_name="ImageID", yAxis_name="Vy")


# 为了避免Shadows name '' from outer place, 将主函数体安置在main中，以营造一个局部环境
if __name__ == "__main__":
    main()
    print("This is the end.")
