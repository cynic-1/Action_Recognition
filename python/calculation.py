# ---------------------------------------
# 此文件专用于接球部位的计算
# Author：张仁鹏
# Date：  2022-2-19
#-----------------------------------------

import mathtools

# 返回的是距离右关键点的百分比
def get_part_position(people, part_pair, cx, cy):
    x1 = int(people["pose_keypoints_2d"][part_pair[0]*3+0])
    y1 = int(people["pose_keypoints_2d"][part_pair[0]*3+1])
    x2 = int(people["pose_keypoints_2d"][part_pair[1]*3+0])
    y2 = int(people["pose_keypoints_2d"][part_pair[1]*3+1])
    dist = mathtools.get_distance(x1, y1, x2, y2)
    left_dist = mathtools.get_horizontal_distance_on(x1, y1, x2, y2, cx, cy, x1, y1)
    right_dist = mathtools.get_horizontal_distance_on(x1, y1, x2, y2, cx, cy, x2, y2)
    # 在part0->part1的射线延长线上
    print(f"[get_position] left: {left_dist}, right: {right_dist}, part: {part_pair}, length: {dist}")
    if left_dist > dist and right_dist < left_dist:
        return -right_dist/dist
    else:
        return right_dist/dist

# 获取接球部位
def get_catch_part(people, ball):
    front_elbow = (3,4)
    back_elbow = (2,3)
    cx = int((ball[0]+ball[2])/2)
    cy = int((ball[1]+ball[3])/2)
    front = get_part_position(people, front_elbow, cx, cy)
    back = get_part_position(people, back_elbow, cx, cy)
    return "front%.2f, back %.2f" % (front, back)
    if front < 1:
        return "front%.2f" % front
    else:
        return "back%.2f" % back