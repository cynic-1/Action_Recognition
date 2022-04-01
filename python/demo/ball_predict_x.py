import os
import cv2
import numpy as np
from tqdm import tqdm

from ball_prediction_common import *

repair_use_conventional_data = True
default_fill_range = 15


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


# 参数fill_range: 规定补全的位置区域，默认为10，越大，转折点处的拟合效果越好
# 建议不要超过30
def fill_curve(left, mid, right, volley_position, vpc, is_exist, is_start, is_end, fill_range=default_fill_range):
    # 适当与具体的left, mid, right有一些偏移，避免接触到坏点或者越界
    f_left = getLineFunc(vpc, left+2, mid-2)
    f_right = getLineFunc(vpc, mid+2, right-2)
    shape = "^" if (vpc[left+1][0] - vpc[left][0] > 0) else "V"
    # left_index = 1 if is_start else vpc[left][1]
    # right_index = len(volley_position) if is_end else (vpc[right][1]-3)
    for i in range(max(vpc[mid][1]-fill_range, 0),
                   min(vpc[mid][1]+fill_range, len(volley_position))):
        if not is_exist[i]:
            is_exist[i] = True
            value = min(f_left(i), f_right(i)) if shape == "^" else \
                max(f_left(i), f_right(i))
            volley_position[i-1].append(value)


# volley_position: 填充好的数据
# _volley_position: 原始的数据
# extrema: 极值点
def annotate_image_each(input_path, output_path,  # fixed parameters
                   volley_position, _volley_position, extrema):  # 待变参数
    # 将x坐标预测值绘制到图像上
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    total_num = len(os.listdir(input_path))
    print(f"开始在图像上标记排球横坐标位置，输出目录在{output_path}，总数为{total_num}")

    for i in tqdm(range(1, total_num+1)):
        img = cv2.imread(input_path + f"{i}.jpg")
        if len(_volley_position[i-1]) == 0:
            color = (0, 0, 100)
        else:
            color = (0, 0, 255)
        if len(volley_position[i-1]) >= 2:
            cv2.circle(img, (int(volley_position[i-1][0]), int(volley_position[i-1][1])), 10, color, -1)
        # img = img.copy()
        if (i-1) in extrema:
            cv2.putText(img, "catch ball", (20, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imwrite(output_path + f"{i}.jpg", img)


# volley_position: 填充好的数据
# _volley_position: 原始的数据
# extrema: 极值点
def annotate_image(input_path, output_path,  # fixed parameters
                   volley_position, _volley_position, extrema):  # 待变参数
    # 将x坐标预测值绘制到图像上
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    total_num = len(os.listdir(input_path))
    print(f"开始在图像上标记排球横坐标位置，输出目录在{output_path}，总数为{total_num}")
    img = cv2.imread(input_path + "1.jpg")

    for i in tqdm(range(1, total_num+1)):
        # 缺失帧
        if len(_volley_position[i-1]) == 0:
            color = (0, 200, 0)

        # 非缺失帧
        else:
            color = (0, 0, 255)
        if len(volley_position[i-1]) >= 2:
            cv2.circle(img, (int(volley_position[i-1][0]), int(volley_position[i-1][1])), 10, color, -1)
        # img = img.copy()
        if (i-1) in extrema:
            cv2.putText(img, "catch ball", (20, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.imwrite(output_path + f"{i}.jpg", img)
            img = cv2.imread(input_path + f"{i}.jpg")


# 函数 predict_speed_x()
# 参数 __volley_position: 排球位置原始数组
# 预测速度和坐标——传统，根据前一个点计算的数据去相应地推算后一个点
# 用途：用于非反弹情况下拟合排球位置
def predict_speed_x(volley_position: list):
    size = len(volley_position)
    speed = np.zeros((size, 2))
    interval = 1 / 30
    valid_num = 0
    valid_list = [False for j in range(size)]
    for i in range(1, size):
        # 说明该帧和上一帧都检测到排球了
        if len(volley_position[i - 1]) != 0 and len(volley_position[i]) != 0:
            valid_num += 1
            v_x = (volley_position[i][0] - volley_position[i - 1][0]) / interval
            v_y = (volley_position[i][1] - volley_position[i - 1][1]) / interval
            speed[i][0] = v_x
            speed[i][1] = v_y
            valid_list[i] = True

    # 合格帧定义：该帧和上一帧都能检测到球的位置
    print("合格帧整体比例：%.2f%%" % (valid_num / size * 100))

    # 预测速度和坐标
    for i in range(1, size):
        # 位置未捕获，且上一帧没有问题，捕获到了速度
        if len(volley_position[i]) == 0:
            # 预测x坐标
            volley_position[i].append(volley_position[i - 1][0] + speed[i - 1][0] * interval)
            speed[i][0] = (volley_position[i][0] - volley_position[i - 1][0]) / interval
            valid_list[i] = True
        else:
            if not valid_list[i]:
                speed[i][0] = (volley_position[i][0] - volley_position[i - 1][0]) / interval
                valid_list[i] = True
    return speed


def turning_point_predict(volley_position):
    # volleyball_position_continual_version
    # vpc[index] = [x_pos, image_id]
    # 构建一个连续的，没有间断点的排球位置集合
    # 其中排球的图像编号有可能中断，因为某些位置的排球可能未被识别到
    vpc = []
    for i, pos in enumerate(volley_position):
        if len(pos) != 0:
            vpc.append([pos[0], i + 1])

    # 先添加vpc中的第一项
    extrema = [0]
    for i in range(1, len(vpc) - 1):
        if vpc[i][0] > vpc[i - 1][0] and vpc[i][0] > vpc[i + 1][0]:
            extrema.append(i)
        elif vpc[i][0] < vpc[i - 1][0] and vpc[i][0] < vpc[i + 1][0]:
            extrema.append(i)
    # 再添加vpc中最后一项
    extrema.append(len(vpc) - 1)

    # is_exist 是从1开始的记录某张图片是否确实排球坐标的数组
    # 拟合曲线，进行转折点附近的预测
    is_exist = [len(pos) != 0 for pos in volley_position]
    is_exist.insert(0, False)
    for i in range(0, len(extrema) - 2):
        left = extrema[i]
        mid = extrema[i + 1]
        right = extrema[i + 2]
        fill_curve(left, mid, right, volley_position, vpc, is_exist,
                   is_start=(i == 0), is_end=(i == len(extrema) - 2))

    return extrema


# 返回的extrema：从0开始
def get_new_turning_point(vp):
    extrema = []
    const_range = 10
    for i in range(1, len(vp) - 1):
        if vp[i][0] > vp[i - 1][0] and vp[i][0] > vp[i + 1][0]:
            is_local_max = True
            for j in range(max(0, i-const_range), min(len(vp), i+const_range)):
                if vp[j][0] > vp[i][0]:
                    is_local_max = False

            if is_local_max:
                extrema.append(i)

        elif vp[i][0] < vp[i - 1][0] and vp[i][0] < vp[i + 1][0]:
            is_local_min = True
            for j in range(max(0, i - const_range), min(len(vp), i + const_range)):
                if vp[j][0] < vp[i][0]:
                    is_local_min = False

            if is_local_min:
                extrema.append(i)

    return extrema


# 在volley_position基础上进行增添，补全未检测到帧的x坐标
def predict_xAxis(volley_position):
    _volley_position = deepcopy(volley_position)

    # 传统的紧邻速度直接推算法预测
    predict_speed_x(_volley_position)
    _extrema = turning_point_predict(volley_position)

    # 经过这一步，所有位置都被补全
    if repair_use_conventional_data:
        # 利用传统方法补全未预测的帧
        for i, pos in enumerate(volley_position):
            if len(pos) == 0:
                pos.append(_volley_position[i][0])

    return get_new_turning_point(volley_position), _extrema
