import math
from functools import cmp_to_key


# 获取球到手臂两点连线的距离
# assignable \nothing;
from typing import Optional


def get_vertical_distance(x1: int, y1: int, x2: int, y2: int, cx: int, cy: int):
    # ax + by + c = 0
    if x2-x1 != 0:
        a = (y2-y1)/(x2-x1)
        b = -1
        c = -a*x1 + y1
        distance = abs(a*cx + b*cy + c) / math.sqrt(a**2 + b**2)
        # print(a, b, c)
    else:
        # 防止除以0
        distance = abs(x1 - cx)
    return distance


# 获取球到手臂两点连线上(x0,y0)点的垂直距离（即平行于连线直线的距离）
# assignable \nothing;
def get_horizontal_distance_on(x1: int, y1: int, x2: int, y2: int, cx: int, cy: int, x0: int, y0: int):
    # 求过点(x0, y0)且与当前直线垂直的直线
    if y2-y1 != 0:
        k = -(x2-x1)/(y2-y1)

        a = k
        b = -1
        c = -k*x0 + y0

        distance = abs(a*cx + b*cy + c) / math.sqrt(a**2 + b**2)
    else:
        distance = abs(x0 - cx)

    return distance


# 获取球到手臂两点连线中垂线的距离
# assignable \nothing;
def get_horizontal_distance(x1: int, y1: int, x2: int, y2: int, cx: int, cy: int):
    # 求直线的中点
    x0 = (x1+x2) / 2
    y0 = (y1+y2) / 2

    if y2-y1 != 0:
        # 斜率应该是-1/k, 我傻了
        k = -(x2-x1)/(y2-y1)

        a = k
        b = -1
        c = -k*x0 + y0

        distance = abs(a*cx + b*cy + c) / math.sqrt(a**2 + b**2)
        # print(a, b, c)
    else:
        distance = abs(x0 - cx)

    return distance


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


# 判断某个部位被检测到
def is_part_in_people(people, part_id):
    confidence = people["pose_keypoints_2d"][part_id*3+2]
    return confidence > 0.1


# 安全的保留小数函数
def round_safe(num: Optional[float], accuracy: int):
    if num is None:
        return num
    else:
        return round(num, accuracy)


if __name__ == "__main__":
    print(get_horizontal_distance(13, 15, 21, 56, 7, 7))