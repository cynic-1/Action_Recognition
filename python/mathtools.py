import math
from functools import cmp_to_key

# 获取球到手臂两点连线的距离
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


def is_part_in_people(people, part_id):
    confidence = people["pose_keypoints_2d"][part_id*3+2]
    return confidence > 0.1


def people_track(json_dict):
    # 如果人数大于3，则把远处的人（鼻子到腿最短）删去
    dist_pair = (0, 14)
    if(len(json_dict["people"]) >= 3):
        # 删去不含有上面两个部位对应的单人数据
        # 记住：删除列表中的特定元素或者保留列表中的特定元素需要用filter
        json_dict["people"] = list(filter(lambda people: (is_part_in_people(people, dist_pair[0]) \
            and is_part_in_people(people, dist_pair[0])), json_dict["people"]))

        def cmp(people1, people2):
            y1_1 = people1["pose_keypoints_2d"][dist_pair[0]*3+1]
            y1_2 = people1["pose_keypoints_2d"][dist_pair[1]*3+1]
            y2_1 = people2["pose_keypoints_2d"][dist_pair[0]*3+1]
            y2_2 = people2["pose_keypoints_2d"][dist_pair[1]*3+1]
            return abs(y1_2 - y1_1) - abs(y2_2 - y2_1)
        # 降序排序
        json_dict["people"].sort(key=cmp_to_key(cmp), reverse=True)

        # 删除其他的人
        if len(json_dict["people"]) > 2:
            del json_dict["people"][2:]

    def cmp2(people1, people2):
        part_id = 0
        x1 = people1["pose_keypoints_2d"][part_id*3]
        x2 = people2["pose_keypoints_2d"][part_id*3]
        return x1 - x2
    # 升序排列
    json_dict["people"].sort(key=cmp_to_key(cmp2))


if __name__ == "__main__":
    print(get_horizontal_distance(13, 15, 21, 56, 7, 7))
    pass