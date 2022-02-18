import math

# 获取球到手臂两点连线的距离
def get_vertical_distance(x1: int, y1: int, x2: int, y2: int, cx: int, cy: int):
    # ax + by + c = 0
    if x2-x1 != 0:
        a = (y2-y1)/(x2-x1)
        b = -1
        c = -a*x1 + y1
        distance = abs(a*cx + b*cy + c) / math.sqrt(a**2 + b**2)
    else:
        # 防止除以0
        distance = abs(x1 - cx)
    return distance


# 获取球到手臂两点连线中垂线的距离
def get_horizontal_distance(x1: int, y1: int, x2: int, y2: int, cx: int, cy: int):
    # 求直线的中点
    x0 = (x1+x2) / 2
    y0 = (y1+y2) / 2

    if y2-y1 != 0:
        k = (x2-x1)/(y2-y1)

        a = k
        b = -1
        c = -k*x0 + y0

        distance = abs(a*cx + b*cy + c) / math.sqrt(a**2 + b**2)
    else:
        distance = abs(x0 - cx)
        
    return distance


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)