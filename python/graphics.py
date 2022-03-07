# 此文件用于放置绘图相关的函数
import cv2
import angle
import numpy as np
import os
import json
import keypoints
import mathtools
import calculation
from PIL import Image, ImageDraw, ImageFont
from mathtools import round_safe


# 支持绘制中文的绘图函数
def cv2ImgAddText(img, text, left, top, textColor, textSize):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


# 绘制骨骼连接和角度文字
def drawLineAndRadius(img, humanpoints, people_id):
    line_points_num = (
    (1, 5), (5, 6), (6, 7), (1, 2), (2, 3), (3, 4), (0, 1), (1, 8), (8, 9), (9, 10), (10, 11), (8, 12), (12, 13),
    (13, 14))
    line_points = []
    eps = 0.01
    for i in range(25):
        for j in range(i, 25):
            if ((i, j) in line_points_num) and (humanpoints[people_id][i][2] > eps) \
                 and (humanpoints[people_id][j][2] > eps):
                pt1 = (int(humanpoints[people_id][i][0]), int(humanpoints[people_id][i][1]))
                pt2 = (int(humanpoints[people_id][j][0]), int(humanpoints[people_id][j][1]))
                line_points.append((pt1, pt2))
    color = (0,255,0)  # BGR
    thickness = 1
    for k in range(len(line_points)):
        cv2.line(img, line_points[k][0], line_points[k][1], color, thickness, cv2.LINE_AA)

    radius_point = [5,6,13,2,3,10]
    radius = []
    radius.append(angle.angle_left_shoulder(humanpoints[people_id]))
    radius.append(angle.angle_left_elbow(humanpoints[people_id]))
    radius.append(angle.angle_left_knee(humanpoints[people_id]))
    radius.append(angle.angle_right_shoulder(humanpoints[people_id]))
    radius.append(angle.angle_right_elbow(humanpoints[people_id]))
    radius.append(angle.angle_right_knee(humanpoints[people_id]))
    # 在图像上注释角度,因为太眼花缭乱了，所以删去
    # for n in range(6):
    #     font = cv2.FONT_HERSHEY_SIMPLEX
    #     if radius[n] is not None:
    #         # cv2.putText(img,"%d"%radius[n],
    #         #     (int(humanpoints[people_id][radius_point[n]][0])-20, (int(humanpoints[people_id][radius_point[n]][1]))-20),
    #         #     font, 0.4, (255, 255, 255), 1)
    #         img = cv2ImgAddText(img, "%d" % radius[n] + chr(0x00b0), (int(humanpoints[people_id][radius_point[n]][0]) + 20),
    #                             (int(humanpoints[people_id][radius_point[n]][1]) - 40), (255, 255, 255), 20)
    #         cv2.line(img, (int(humanpoints[people_id][radius_point[n]][0]) + 8, (int(humanpoints[people_id][radius_point[n]][1])) - 3),
    #                  (int(humanpoints[people_id][radius_point[n]][0]) + 20, (int(humanpoints[people_id][radius_point[n]][1])) - 20),
    #                  (255, 255, 255), 2, cv2.LINE_AA)

    return img


def hcolor_to_bgr(hcolor):
    r = int(hcolor[1:3], 16)
    g = int(hcolor[3:5], 16)
    b = int(hcolor[5:7], 16)
    return (b, g, r)



# 将传入的源图像转化为标注图像
# 标注内容：关节、肢体连接、身体部位角度
# image_path: 原图像目录
# json_path:  图像转化成的JSON文件目录
# num:        图像的次序标号
# dynamic_info: 经过计算处理过的动态信息
# dynamic_info = {"min_imageID":  接球的图片编号
                # "distance":     球到手臂的距离
                # "horizontal_dist": 球到手臂的水平距离
                # "volley_position": 球的位置}
                # volley_position 访问方式：volley_position[num-1][第几个球]
def annotate_img(image_path, json_path, num, dynamic_info, arguments_json, annotate_people=False):
    img = cv2.imread(os.path.join(image_path, f"{num}.jpg"))
    # print(f"[image {num}] 图片的分辨率为：{img.shape}")  # 输出 几行几列几维颜色

    # 读取和转化JSON文件
    with open(os.path.join(json_path, f"{num}_keypoints.json"), "r") as f:
        json_dict = json.load(f)
        mathtools.people_track(json_dict)

    people_cnt = len(json_dict["people"])
    # print(f"[image {num}] 一共有{people_cnt}个人在画面中。")
    humanpoints = np.zeros((10, 25, 3))

    if people_cnt != 0:
        # 目前支持获取多个人的姿态数据，但还需要研究对单个人的追踪
        for people_id in range(people_cnt):
            pose_keypoints_2d = json_dict["people"][people_id]["pose_keypoints_2d"]
            for i in range(25):
                humanpoints[people_id][i] = [pose_keypoints_2d[i*3], pose_keypoints_2d[i*3+1], pose_keypoints_2d[i*3+2]]

            # 在图像上标注关节序号
            for i in range(25):
                x, y, confidence = pose_keypoints_2d[i*3], pose_keypoints_2d[i*3+1], pose_keypoints_2d[i*3+2]
                
                # 确保confidence参数不为0
                if abs(confidence) > 0.0001:
                    # 只标注有限的关键点
                    if(i < len(keypoints.color_table)):
                        color = hcolor_to_bgr(keypoints.color_table[i])
                        cv2.circle(img, (int(x), int(y)), 8, color, -1)  #在图中画出关键点
                else:
                    # print(f"[image {num}] keypoint {i} not exists.")
                    pass
            

            # 绘制人的编号
            if annotate_people:
                cv2.putText(img, f"Person {people_id}: ", (int(x), max(int(y)-100, 0)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)

            
            for i in range(25):
                x, y, confidence = pose_keypoints_2d[i*3], pose_keypoints_2d[i*3+1], pose_keypoints_2d[i*3+2]
                
                # 确保confidence参数不为0
                if abs(confidence) > 0.0001:
                    if(i < len(keypoints.color_table)):
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        # 绘制关键点数字标记
                        cv2.putText(img,str(i),(int(x)-2,int(y)+4),font,0.3,(255,255,255),1,cv2.LINE_AA)

            # 骨骼连接 & 标注角度数据
            img = drawLineAndRadius(img, humanpoints, people_id)


    # 打印手臂离球的距离
    distance = dynamic_info["distance"][num]
    for people_id in range(len(distance)):
        cv2.putText(img,f"Person{people_id}: {int(distance[people_id])} px.", \
                (0,(people_id+1)*40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),1,cv2.LINE_AA)

    # 描出球的位置
    boxes = dynamic_info["volley_position"][num-1]
    if len(boxes) != 0:
        box = boxes[0]
        x1, y1, x2, y2 = box
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        # 以绿色边框描出球的位置
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)


    # 获取横向距离,仅调试用
    pose_keypoints_2d = json_dict["people"][people_id]["pose_keypoints_2d"]
    elbow_pair = (6, 7)
    x1 = int(pose_keypoints_2d[elbow_pair[0]*3])
    y1 = int(pose_keypoints_2d[elbow_pair[0]*3+1])
    x2 = int(pose_keypoints_2d[elbow_pair[1]*3])
    y2 = int(pose_keypoints_2d[elbow_pair[1]*3+1])
    length = mathtools.get_distance(x1, y1, x2, y2)
    horizontal_dist = dynamic_info["horizontal_dist"][num]


    # 打印接到球的信息！
    # 接到球满足两个条件：1. 距离胳膊较近  2. 与胳膊中垂线距离不超过胳膊长度
    if num in dynamic_info["min_imageID"]:
        # 只考虑0号人
        people = json_dict["people"][0]
        ball = dynamic_info["volley_position"][num-1][0]
        print(f"[image {num}] 横向距离={horizontal_dist[0]}, 胳膊长度=" + "%.2f" % length)

        # 获取接球部位
        hitPosition = calculation.get_catch_part(people, ball)
        img = cv2ImgAddText(img, f"Person0 Catch ball! {hitPosition}", 0, 2*40, (0,0,255), 20)
        # cv2.putText(img,f"Person0 Catch ball! {hitPosition}", (0,3*40), \
        #     cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2,cv2.LINE_AA)
        arguments_json[num-1]["data"]["upper"]["hitPosition"] = hitPosition
    else:
        arguments_json[num-1]["data"]["upper"]["hitPosition"] = "未接球"

    people_id = 0
    arguments_json[num-1]["data"]["upper"]["hitAngle"] = round_safe(angle.angle_frontElbow_horizon(humanpoints[people_id]), 1)
    arguments_json[num-1]["data"]["upper"]["angleForearmArm"] = round_safe(angle.angle_left_elbow(humanpoints[people_id]), 1)
    arguments_json[num-1]["data"]["upper"]["angleArmTrunk"] = round_safe(angle.angle_rightElbow_trunk(humanpoints[people_id]), 1)

    arguments_json[num-1]["data"]["lower"]["angleCalfThigh"] = round_safe(angle.angle_left_knee(humanpoints[people_id]), 1)
    arguments_json[num-1]["data"]["lower"]["angleThighTrunk"] = round_safe(angle.angle_thigh_trunk(humanpoints[people_id]), 1)
    # 跳起的高度先默认为0
    arguments_json[num-1]["data"]["lower"]["jumpHeight"] = 0

    #打印角度 -1 代表不构成三角形
    # for i in range(people_cnt):
    #     angle.angle_left_shoulder(humanpoints[i])
    #     angle.angle_left_elbow(humanpoints[i])
    #     angle.angle_left_knee(humanpoints[i])
    #     angle.angle_left_ankle(humanpoints[i])
    #     angle.angle_right_shoulder(humanpoints[i])
    #     angle.angle_right_elbow(humanpoints[i])
    #     angle.angle_right_knee(humanpoints[i])
    #     angle.angle_right_ankle(humanpoints[i])

    # # 适应屏幕的尺寸调整
    # newW = W = img.shape[1]
    # newH = H = img.shape[0]
    # if W > 1600:
    #     newW = 1600
    #     newH = int(newW / (W / H))
    # elif H > 700:
    #     newH = 700
    #     newW = int(newH * (W / H))

    # cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("image", newW, newH) # 重设窗体宽高
    # cv2.imshow("image", img)
    # cv2.imwrite("img.jpg", img)
    return img
    # cv2.waitKey(0)