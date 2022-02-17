# 本程序用于以命令行方式调用OpenPoseDemo.exe，得到想要的JSON文件
# 目前暂时使用图像为材料，后期会考虑使用视频
import json
import os
import sys
import time

import cv2
import numpy
import numpy as np

import angle
import keypoints
import cut_video

# 引入排球识别
from detectron2_package import VolleyballDetect as Detect

is_low_resolution = True


# 用来将参数字典转化为命令行参数字符串
def arg_constructor(params: dict):
    arg = ""
    for key in params.keys():
        value = params[key]
        if type(value) == bool:
            arg = arg + f" --{key}"
        else:
            arg = arg + f" --{key} {value}"
    return arg


# 命令行调用OpenPoseDemo程序，生成JSON
# 具体就是将image_dir里的图片内容转化为姿态JSON
# 执行方式是阻塞执行，即先执行完命令行，再执行下面的python代码
def produce_json(images_path="images", json_path="output_json"):
    dir_path = os.path.dirname(os.path.realpath(__file__))  # 本文件当前的路径
    root_path = dir_path + "/../" # 根路径，即为OpenPose主目录

    if not os.path.exists(json_path):
        os.makedirs(json_path)
        print("指定的json输出目录不存在，将新建一个")

    params = dict()
    # 这些路径都是相对于根路径而言的路径
    params["image_dir"] = "\"" + os.path.join(dir_path, images_path) + "\""
    # params["write_images"] = os.path.join(dir_path, "output_images")
    params["model_pose"] = "BODY_25"
    params["write_json"] = "\"" + os.path.join(dir_path, json_path) + "\""

    if is_low_resolution:
        params["net_resolution"] = "320x176"  # 调低分辨率，以让低显存电脑也能顺利运行

    os.chdir(root_path)  # 跳转到OpenPose根路径再执行
    print(os.getcwd())
    os.system('chcp 65001')  # 开启utf-8支持，否则输出乱码
    cmd = "bin\OpenPoseDemo" + arg_constructor(params)
    print(cmd)
    information = os.popen(cmd)
    print(information.read())
    information.close()

    # 切换回原来的路径
    os.chdir(dir_path)


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
    lineType = 4
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
    for n in range(6):
        font = cv2.FONT_HERSHEY_SIMPLEX
        if radius[n] is not None:
            cv2.putText(img,"%d"%radius[n],
                (int(humanpoints[people_id][radius_point[n]][0])-20, (int(humanpoints[people_id][radius_point[n]][1]))-20),
                font, 0.4, (255, 255, 255), 1)


def hcolor_to_bgr(hcolor):
    r = int(hcolor[1:3], 16)
    g = int(hcolor[3:5], 16)
    b = int(hcolor[5:7], 16)
    return (b, g, r)


# 将传入的源图像转化为标注图像
# image_path: 原图像目录
# json_path:  图像转化成的JSON文件目录
# num:        图像的次序标号
def process_img(image_path, json_path, num):
    img = cv2.imread(os.path.join(image_path, f"{num}.jpg"))
    img_origin = img.copy()
    print(f"[image {num}] 图片的分辨率为：{img.shape}")  # 输出 几行几列几维颜色

    # 读取和转化JSON文件
    with open(os.path.join(json_path, f"{num}_keypoints.json"), "r") as f:
        json_dict = json.load(f)

    people_cnt = len(json_dict["people"])
    print(f"[image {num}] 一共有{people_cnt}个人在画面中。")
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
                    print(f"[image {num}] keypoint {i} not exists.")

            # 参照位置：鼻子
            keypoint_id = 0
            x, y = pose_keypoints_2d[keypoint_id*3], pose_keypoints_2d[keypoint_id*3+1]
            cv2.putText(img, f"Person {people_id}", (int(x), max(int(y)-100, 0)), 
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
            drawLineAndRadius(img, humanpoints, people_id)


    # 获取球的信息，并在图像上标注球
    boxes = Detect.detect_ball(img_origin)
    print(f"检测到{len(boxes)}个球。")
    for box in boxes:
        x1, y1, x2, y2 = box
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        # 以绿色边框描出球的位置
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        print(f"球的长度是{x2-x1}")

        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        

    #打印角度 -1 代表不构成三角形
    for i in range(people_cnt):
        angle.angle_left_shoulder(humanpoints[i])
        angle.angle_left_elbow(humanpoints[i])
        angle.angle_left_knee(humanpoints[i])
        angle.angle_left_ankle(humanpoints[i])
        angle.angle_right_shoulder(humanpoints[i])
        angle.angle_right_elbow(humanpoints[i])
        angle.angle_right_knee(humanpoints[i])
        angle.angle_right_ankle(humanpoints[i])

    # 适应屏幕的尺寸调整
    newW = W = img.shape[1]
    newH = H = img.shape[0]
    if W > 1600:
        newW = 1600
        newH = int(newW / (W / H))
    elif H > 700:
        newH = 700
        newW = int(newH * (W / H))

    # cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("image", newW, newH) # 重设窗体宽高
    # cv2.imshow("image", img)
    # cv2.imwrite("img.jpg", img)
    return img
    # cv2.waitKey(0)


if __name__ == "__main__":
    # 在pose_images文件夹生成视频的全切片
    save_path = "pose_images"
    mp4_path = "video/正确对垫姿势.mp4"
    json_path = "pose_images_json"
    result_path = "pose_results"

    # 定位系统路径到本文件的路径
    dir_path = os.path.dirname(os.path.realpath(__file__))  # 本文件当前的路径
    os.chdir(dir_path)

    if os.path.exists(save_path):
        print("检测到视频切片数据已经生成，就不再生成了")
    else:
        print("正在生成视频切片数据")
        cut_video.process_video(mp4_path, save_path, 1)
        print("视频切片数据生成完毕")

    # 对视频里的所有图片生成json
    if not os.path.exists(json_path):
        produce_json(save_path, json_path)
    
    if not os.path.exists(result_path):
        print("输出目录不存在，将自动创建。")
        os.makedirs(result_path)

    total_num = len(os.listdir(save_path))
    for i in range(total_num):
        img = process_img(save_path, json_path, i+1)
        # cv2.imshow("image", img)
        # cv2.waitKey()
        cv2.imwrite(os.path.join(result_path, f"{i+1}.jpg"), img)