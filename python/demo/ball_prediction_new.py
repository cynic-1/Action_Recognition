import json
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from ball_prediction_common import *
import ball_predict_x
from demo.参考的程序 import regression


def construct_array(_volley_position, begin, end):
    X = []
    Y = []
    for i in range(begin, end + 1):
        if len(_volley_position[i]) == 2:
            X.append(_volley_position[i][0])
            Y.append(_volley_position[i][1])
    X = np.array(X)
    Y = np.array(Y)
    return X, Y


def globalRegression(_volley_position, volley_position, extrema):
    extremaPos = 1
    for i in range(len(_volley_position)):
        if i == extrema[extremaPos]:
            begin = extrema[extremaPos - 1] + 1
            end = extrema[extremaPos]
            X, Y = construct_array(_volley_position, begin, end)
            a, b, c = regression.getRegression(X, Y)
            for j in range(begin, end + 1):
                if len(volley_position[j]) < 2:
                    x = volley_position[j][0]
                    y = a * x ** 2 + b * x + c
                    volley_position[j].append(y)
            extremaPos += 1

def local_regress(pos, _volley_position, extrema):
    max_ele_limit = 10

    X = []
    Y = []
    cnt = 0
    left = pos

    # 该点不是转折点
    if pos not in extrema:
        while left not in extrema:
            if len(_volley_position[left]) == 2:
                if cnt > max_ele_limit:
                    break
                X.append(_volley_position[left][0])
                Y.append(_volley_position[left][1])
                cnt += 1
            left -= 1

        right = pos
        while right not in extrema:
            if len(_volley_position[right]) == 2:
                if cnt > max_ele_limit:
                    break
                X.append(_volley_position[right][0])
                Y.append(_volley_position[right][1])
                cnt += 1
            right += 1
    else:
        # 该点是转折点，若是转折点，则两个while都不能执行
        if pos == 0:
            # 向右走
            right = pos+1
            while right not in extrema:
                if len(_volley_position[right]) == 2:
                    if cnt > max_ele_limit:
                        break
                    X.append(_volley_position[right][0])
                    Y.append(_volley_position[right][1])
                    cnt += 1
                right += 1
        else:
            # 向左走
            left = pos-1
            while left not in extrema:
                if len(_volley_position[left]) == 2:
                    if cnt > max_ele_limit:
                        break
                    X.append(_volley_position[left][0])
                    Y.append(_volley_position[left][1])
                    cnt += 1
                left -= 1

    X = np.array(X)
    Y = np.array(Y)
    try:
        return regression.getRegression(X, Y)
    except Exception as e:
        print(e)
        print(pos)
        print(X, Y)
        return 0, 0, 0



def localRegression(_volley_position, volley_position, extrema):
    for i in range(len(_volley_position)):
        if len(_volley_position[i]) < 2:
            a, b, c = local_regress(i, _volley_position, extrema)
            x = volley_position[i][0]
            y = a*x**2 + b*x + c
            volley_position[i].append(y)


def main():
    volley_position = get_volleyCenter("../volleyball_detect.json")
    _volley_position = deepcopy(volley_position)
    # 因为x坐标很好求，求出一些参数来做辅助
    extrema, _ = ball_predict_x.predict_xAxis(volley_position)

    # 这里的extrema是严格的交界点
    extrema.insert(0, 0)
    extrema.append(len(volley_position)-1)
    # globalRegression(_volley_position, volley_position, extrema)
    localRegression(_volley_position, volley_position, extrema)

    # ball_predict_x.annotate_image("../pose_images/", "predict_ball/",
    #                               volley_position, _volley_position, extrema)

    # ball_predict_x.annotate_image_each("../pose_images/", "predict_ball/",
    #                               volley_position, _volley_position, extrema)

    # 利用matplotlib作图
    plt.figure(figsize=(8, 6))
    x, y = volley_position_to_plot(_volley_position, axis=0)
    color = []
    for _ in x:
        color.append("red")
        # if len(_speed[i-1]) == 0:
        #     color.append("red")
        # else:
        #     color.append("blue")
    x.extend(extrema)
    y.extend(len(extrema) * [0])
    color.extend(len(extrema) * ["purple"])
    plt.scatter(x, y, color=color)
    plt.show()


# 为了避免Shadows name '' from outer place, 将主函数体安置在main中，以营造一个局部环境
if __name__ == "__main__":
    main()
    print("This is the end.")
