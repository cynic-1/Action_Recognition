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

# 引入排球识别
from detectron2_package import VolleyballDetect as Detect

is_low_resolution = False


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
def produce_json():
    dir_path = os.path.dirname(os.path.realpath(__file__))  # 本文件当前的路径
    root_path = dir_path + "/../" # 根路径，即为OpenPose主目录

    params = dict()
    # 这些路径都是相对于根路径而言的路径
    params["image_dir"] = "\"" + os.path.join(dir_path, "images") + "\""
    # params["write_images"] = os.path.join(dir_path, "output_images")
    params["model_pose"] = "BODY_25"
    params["write_json"] = "\"" + os.path.join(dir_path, "output_json") + "\""

    if is_low_resolution:
        params["net_resolution"] = "320x176"  # 调低分辨率，以让低显存电脑也能顺利运行

    os.chdir(root_path)  # 跳转到根路径再执行
    os.system('chcp 65001')  # 开启utf-8支持，否则输出乱码
    cmd = "bin\OpenPoseDemo" + arg_constructor(params)
    information = os.popen(cmd)
    print(information.read())
    information.close()


def hcolor_to_bgr(hcolor):
    r = int(hcolor[1:3], 16)
    g = int(hcolor[3:5], 16)
    b = int(hcolor[5:7], 16)
    return (b, g, r)


if __name__ == "__main__":
    # produce_json()  # 先在output_json目录下输出json文件

    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path) # 切换回原来的路径

    img = cv2.imread("./images/1.jpg")  # numpy.ndarray类型
    img_origin = img.copy()
    print(img.shape)  # 输出 几行几列几维颜色

    # 读取和转化JSON文件
    with open("output_json/1_keypoints.json", "r") as f:
        json_dict = json.load(f)

    people_cnt = len(json_dict["people"])
    print(f"一共有{people_cnt}个人在画面中。")
    humanpoints = np.zeros((10, 25, 3))
    if people_cnt != 0:
        pose_keypoints_2d = json_dict["people"][0]["pose_keypoints_2d"]
        for i in range(25):
            humanpoints[0][i] = [pose_keypoints_2d[i*3], pose_keypoints_2d[i*3+1], pose_keypoints_2d[i*3+2]]

        for i in range(25):
            x, y, confidence = pose_keypoints_2d[i*3], pose_keypoints_2d[i*3+1], pose_keypoints_2d[i*3+2]
            
            # 确保confidence参数不为0
            if abs(confidence) > 0.0001:
                if(i < len(keypoints.color_table)):
                    color = hcolor_to_bgr(keypoints.color_table[i])
                    cv2.circle(img, (int(x), int(y)), 8, color, -1)  #在图中画出关键点
            else:
                print(f"keypoint {i} not exists.")

        for i in range(25):
            x, y, confidence = pose_keypoints_2d[i*3], pose_keypoints_2d[i*3+1], pose_keypoints_2d[i*3+2]
            
            # 确保confidence参数不为0
            if abs(confidence) > 0.0001:
                if(i < len(keypoints.color_table)):
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img,str(i),(int(x)-2,int(y)+4),font,0.3,(255,255,255),1,cv2.LINE_AA)

    # 获取球的信息
    boxes = Detect.detect_ball(img_origin)
    print(f"检测到{len(boxes)}个球。")
    for box in boxes:
        x1, y1, x2, y2 = box
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        # 以绿色边框描出球的位置
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        print(f"球的长度是{x2-x1}")


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
    cv2.imwrite("img.jpg", img)
    # cv2.waitKey(0)
    pass