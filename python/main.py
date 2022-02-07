# 本程序用于以命令行方式调用OpenPoseDemo.exe，得到想要的JSON文件
# 目前暂时使用图像为材料，后期会考虑使用视频

import json
import os
import sys
import time

import cv2
import numpy

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
def produce_json():
    dir_path = os.path.dirname(os.path.realpath(__file__))  # 本文件当前的路径
    root_path = dir_path + "/../" # 根路径，即为OpenPose主目录

    params = dict()
    # 这些路径都是相对于根路径而言的路径
    params["image_dir"] = os.path.join(dir_path, "images")
    # params["write_images"] = os.path.join(dir_path, "output_images")
    params["model_pose"] = "BODY_25"
    params["write_json"] = os.path.join(dir_path, "output_json")

    if is_low_resolution:
        params["net_resolution"] = "320x176"  # 调低分辨率，以让低显存电脑也能顺利运行

    os.chdir(root_path)  # 跳转到根路径再执行
    os.system('chcp 65001')  # 开启utf-8支持，否则输出乱码
    cmd = "bin\OpenPoseDemo" + arg_constructor(params)
    information = os.popen(cmd)
    print(information.read())
    information.close()


if __name__ == "__main__":
    produce_json()  # 先在output_json目录下输出json文件

    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path) # 切换回原来的路径

    img = cv2.imread("./images/1.jpg")  # numpy.ndarray类型
    print(img.shape)  # 输出 几行几列几维颜色

    # 读取和转化JSON文件
    with open("output_json/1_keypoints.json", "r") as f:
        json_dict = json.load(f)

    people_cnt = len(json_dict["people"])
    print(f"一共有{people_cnt}个人在画面中。")
    if people_cnt != 0:
        pose_keypoints_2d = json_dict["people"][0]["pose_keypoints_2d"]
        for i in range(25):
            x, y, confidence = pose_keypoints_2d[i*3], pose_keypoints_2d[i*3+1], pose_keypoints_2d[i*3+2]
            if abs(confidence) > 0.00001:
                cv2.circle(img, (int(x), int(y)), 10, (0, 0, int(255*confidence)), -1)


    # 适应屏幕的尺寸调整
    newW = W = img.shape[1]
    newH = H = img.shape[0]
    if W > 1600:
        newW = 1600
        newH = int(newW / (W / H))
    elif H > 700:
        newH = 700
        newW = int(newH * (W / H))

    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("image", newW, newH) # 重设窗体宽高
    cv2.imshow("image", img)
    cv2.waitKey(0)
    pass