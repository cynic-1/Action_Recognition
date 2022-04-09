import json
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from ball_prediction_common import *
import ball_predict_x

repair_throw_conventional_data = True
default_fill_range = 2
annotate_ball_data = True


# 返回各个帧的速度，不修改volley_position
# 速度从第1帧开始，因为第0帧之前的位置不存在，无法计算出第0帧的速度
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

    for i in range(total_num-1-2, -1, -1):
        if is_valid(i+1) and is_valid(i+2) and (not is_valid(i)):
            if find_nearest_extrema(extrema, i)[1] < default_fill_range:
                continue
            speed[i] = [0, float(2 * speed[i+1][1] - speed[i+2][1])]


# 这里的start和end是真实的图片id
def getLineFunc(speed_c, start, end):
    average = Average()
    for i in range(start, end-1):
        dist = (speed_c[i + 1][0] - speed_c[i][0]) / (speed_c[i + 1][1] - speed_c[i][1])
        average.add(dist)

    i = speed_c[start][1]
    pos = speed_c[start][0]
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
        return f"({self.left}, {self.right})"


def turning_point_fix(speed, extrema):
    speed_c = []
    for i in range(len(speed)):
        if len(speed[i]) != 0:
            speed_c.append([speed[i][1], i])

    _extrema = [Pair(0, 0)]
    i = 0
    j = 0
    while i < len(extrema) and j < len(speed_c):
        if speed_c[j][1] > extrema[i]:
            while i < len(extrema) and speed_c[j][1] > extrema[i]:
                i += 1

        if speed_c[j][1] == extrema[i]:
            _extrema.append(Pair(j, j))
            i += 1
        elif speed_c[j][1] < extrema[i] and (j+1 < len(speed_c) and speed_c[j+1][1] > extrema[i]):
            _extrema.append(Pair(j, j+1))
            i += 1

        j += 1
    _extrema.append(Pair(len(speed_c)-1, len(speed_c)-1))

    # 减3是为了防止尾部不规整点的出现
    for i in range(0, len(_extrema)-2-1):
        tri_set = _extrema[i:i+3]

        left = tri_set[0].right
        midl = tri_set[1].left
        midr = tri_set[1].right
        right = tri_set[2].left

        # 控制用于拟合的点的范围
        const_range = 2
        line_left = getLineFunc(speed_c, left+const_range, midl-const_range)
        line_right = getLineFunc(speed_c, midr+const_range, right-const_range)

        left_p = find_nearest_extrema(extrema, imageId=speed_c[left][1])[0]
        mid_p = find_nearest_extrema(extrema, imageId=speed_c[midl][1])[0]
        right_p = find_nearest_extrema(extrema, imageId=speed_c[right][1])[0]

        # 控制补全的范围
        const_range_1 = 0
        # range = [left_p+1, mid_p-1]
        for j in range(left_p+const_range_1, mid_p+1-const_range_1):
            if len(speed[j]) == 0:  # 未被补全
                speed[j] = [0, line_left(j)]

        for j in range(mid_p+const_range_1, right_p+1-const_range_1):
            if len(speed[j]) == 0:
                speed[j] = [0, line_right(j)]

    pass


def predict_y(volley_position, speed):
    interval = 1/30
    for i in range(1, len(volley_position)):
        if len(volley_position[i]) == 1:
            if len(volley_position[i-1]) == 2 and len(speed[i]) == 2:
                next_y = volley_position[i-1][1] + speed[i][1] * interval
                volley_position[i].append(next_y)


def interpolation(speed, extrema):
    for i in range(len(speed)):
        if len(speed[i]) == 0:
            left = i
            right = i
            while left >= 0:
                if len(speed[left]) != 0:
                    break
                left -= 1
            while right < len(speed):
                if len(speed[right]) != 0:
                    break
                right += 1

            is_interpolation = True
            # left, right中间有转折点时不插值
            for j in range(left+1, right):
                if j in extrema:
                    is_interpolation = False
                    break

            if not is_interpolation:
                continue

            # 可选建议：不要在接近转折点的地方插值
            # valid side result
            if left >= 0 and right < len(speed):
                _speed = speed[left][1] + ((i - left) / (right - left)) * (speed[right][1] - speed[left][1])
                speed[i] = [0, _speed]


def main():
    volley_position = get_volleyCenter("../volleyball_detect.json")
    _volley_position = deepcopy(volley_position)
    speed = predict_speed(volley_position)
    extrema, _ = ball_predict_x.predict_xAxis(volley_position)

    extrema.insert(0, 0)
    extrema.append(len(volley_position)-1)
    _speed = deepcopy(speed)

    interpolation(speed, extrema)
    turning_point_fix(speed, extrema)

    # # 利用传统方法修复未识别的点
    # conventional_speed_fix(_speed, extrema)
    # for i in range(len(speed)):
    #     if len(speed[i]) == 0:
    #         speed[i] = _speed[i]


    predict_y(volley_position, speed)

    not_predicted = 0
    for i in speed:
        if len(i) == 0:
            not_predicted += 1
    print("Not predicted: " + str(not_predicted))

    # ball_predict_x.annotate_image("../pose_images/", "predict_ball/",
    #                               volley_position, _volley_position, extrema)

    # 利用matplotlib作图
    fig = plt.figure(num=1)
    x, y = volley_position_to_plot(speed, axis=1)
    color = []
    for i in x:
        if len(_speed[i-1]) == 0:
            color.append("red")
        else:
            color.append("blue")
    x.extend(extrema)
    y.extend(len(extrema) * [0])
    color.extend(len(extrema) * ["purple"])
    plt.scatter(x, y, color=color)
    plt.show()
    # produceCSVTable("Vy.csv", x, y, xAxis_name="ImageID", yAxis_name="Vy")


# 为了避免Shadows name '' from outer place, 将主函数体安置在main中，以营造一个局部环境
if __name__ == "__main__":
    main()
    print("This is the end.")
