# 本程序用于以命令行方式调用OpenPoseDemo.exe，得到想要的JSON文件
# 目前暂时使用图像为材料，后期会考虑使用视频
from audioop import reverse
import json
import os

import cv2
import numpy as np

import graphics
import keypoints
import cut_video
import mathtools
import shutil

# 低分辨率开关
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



# 计算球与人之间的距离
def calc_distance(image_path, json_path, num, volley_position, distance1, distance2, horizontal_dist):
    img = cv2.imread(os.path.join(image_path, f"{num}.jpg"))
    # 读取和转化JSON文件
    with open(os.path.join(json_path, f"{num}_keypoints.json"), "r") as f:
        json_dict = json.load(f)
        mathtools.people_track(json_dict)

    # 获取球的信息，并在图像上标注球
    boxes = volley_position[num-1]
    # print(f"检测到{len(boxes)}个球。")

    people_cnt = len(json_dict["people"])

    # 目前只考虑一个球的情况
    if len(boxes) != 0:
        box = boxes[0]
        x1, y1, x2, y2 = box
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        # 以绿色边框描出球的位置
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        # print(f"球的长度是{x2-x1}")

        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        
        for people_id in range(people_cnt):
            pose_keypoints_2d = json_dict["people"][people_id]["pose_keypoints_2d"]
            elbow_pair = (6, 7)
            x1 = int(pose_keypoints_2d[elbow_pair[0]*3])
            y1 = int(pose_keypoints_2d[elbow_pair[0]*3+1])
            x2 = int(pose_keypoints_2d[elbow_pair[1]*3])
            y2 = int(pose_keypoints_2d[elbow_pair[1]*3+1])

            dist = mathtools.get_vertical_distance(x1, y1, x2, y2, center_x, center_y)
            # print(f"[image {num}] 距离Person{people_id} {int(dist)} pixel.")

            while num >= len(distance1): distance1.append([])
            distance1[num].append(int(dist))

            # distance1数组访问方式：
            # distance1[图片编号][people_id(人物编号，从0开始)] = 距离
            # 特点：可以直接用图片编号访问

            if people_id >= len(distance2): distance2.append([])
            distance2[people_id].append((num, int(dist)))
            # distance2数组访问方式：
            # distance2[people_id(人物编号，从0开始)] = tuple(图片编号, 距离)
            # 特点：图片编号是递增不连续的，便于在相邻下标位置访问到距离

            while num >= len(horizontal_dist): horizontal_dist.append([])
            dist2 = int(mathtools.get_horizontal_distance(x1, y1, x2, y2, center_x, center_y))
            horizontal_dist[num].append(dist2)
            # horizontal_dist存储球中心与人胳膊中垂线的距离
            # 存储方式与distance1完全相同




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

    # 生成排球识别信息的json文件
    volley_position_path = os.path.join(result_path, "volleyball_detect.json")
    if not os.path.exists(volley_position_path):
        # 引入排球识别
        print("排球识别信息不存在，将开始生成！")
        from detectron2_package import VolleyballDetect as Detect
        lst = []
        for i in range(total_num):
            img = cv2.imread(os.path.join(save_path, f"{i+1}.jpg"))
            boxes = Detect.detect_ball(img)
            boxes_new = []
            for box in boxes:
                box = list(map(lambda x: float(x), box))
                boxes_new.append(box)
            lst.append(boxes_new)
            print(f"[image {i+1}] completed.")
        str = json.dumps(lst)
        with open(volley_position_path, "w") as f:
            f.write(str)

    with open(volley_position_path, "r") as f:
        volley_position = json.load(f)

    
    distance1 = []
    distance2 = []
    horizontal_dist = []
    for i in range(total_num):
        calc_distance(save_path, json_path, i+1, volley_position, distance1, distance2, horizontal_dist)

    lst = distance2[0]
    min_imageID = []
    for i in range(len(lst)):
        # 某个点的距离距离胳膊已经足够近
        box = volley_position[lst[i][0]-1][0]
        ball_width = box[2]-box[0]
        imageID = lst[i][0]
        # 横向距离尽量放宽，避免误判
        if lst[i][1] - ball_width < 20 and horizontal_dist[imageID][0] < 4*ball_width:
            min_imageID.append(imageID)

    dynamic_info = {"min_imageID": min_imageID, \
                    "distance": distance1, "horizontal_dist": horizontal_dist, 
                    "volley_position": volley_position}
    print(min_imageID)

    for i in range(total_num):
        img = graphics.annotate_img(save_path, json_path, i+1, dynamic_info)
        # cv2.imshow("image", img)
        # cv2.waitKey()
        if (i+1) in min_imageID:
            cv2.imwrite(os.path.join(result_path, f"{i+1}.jpg"), img)

    # for id in min_imageID:
    #     shutil.copyfile(f"pose_results/{id}.jpg", f"pose_results/catch/{id}.jpg")