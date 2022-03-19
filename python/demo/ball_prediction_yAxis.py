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

    # 合格帧定义：该帧和上一帧都能检测到球的位置
    print("合格帧整体比例：%.2f%%" % (valid_num / size * 100))
    return speed


def main():
    volley_position = get_volleyCenter("../volleyball_detect.json")
    speed = predict_speed(volley_position)
    extrema = ball_predict_x.predict_xAxis(volley_position)

    # 利用matplotlib作图
    fig = plt.figure(num=1)
    x, y = volley_position_to_plot(speed, axis=1)
    plt.scatter(x, y)
    plt.show()

    produceCSVTable("Vy.csv", x, y, xAxis_name="ImageID", yAxis_name="Vy")


# 为了避免Shadows name '' from outer place, 将主函数体安置在main中，以营造一个局部环境
if __name__ == "__main__":
    main()
