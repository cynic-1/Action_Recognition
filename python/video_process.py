# 本程序用于以命令行方式调用OpenPoseDemo.exe，得到想要的JSON文件
# 本程序以视频为原料，输出视频中每帧的关键参数，并在图像上进行数据的标注
import codecs
import json
import os
import shutil
import sys
from functools import cmp_to_key
from typing import ClassVar

import cv2
from tqdm import tqdm

import ball_flight
import combinePic
import config
import evaluate
import graphics
import keyImage
import mathtools
import peopleTrack
from VideoInfoLoader import VideoInfoLoader
from mathtools import round_safe

global gl_config


# save_path = "pose_images"
#     mp4_path = "video/错误对垫姿势3.mp4"
#     json_path = "pose_images_json"
#     result_path = "pose_results"
#     keyimage_path = "pose_keyimages"



# 计算球与人之间的距离
# 此阶段原则：尽早抛出异常
def calc_distance(image_path, json_path, num, volley_position, distance1, distance2, horizontal_dist):
    img = cv2.imread(os.path.join(image_path, f"{num}.jpg"))

    # 读取和转化JSON文件
    with open(os.path.join(json_path, f"{num}_keypoints.json"), "r") as f:
        json_dict = json.load(f)
        # 无关人过滤算法
        peopleTrack.people_track(json_dict)

    # 获取球的信息，并在图像上标注球
    boxes = volley_position[num - 1]
    # print(f"检测到{len(boxes)}个球。")

    # TODO: 没检测到球的处理算法
    # assert(len(boxes) >= 1)  # 假定能检测到球

    people_cnt = len(json_dict["people"])

    # 目前选的是第一个球
    if len(boxes) != 0:
        if len(boxes) > 1:
            # 筛选体积最大的球
            def box_size_cmp(box1, box2):
                size1: int = int((box1[2] + box1[3] - box1[0] - box1[1]) / 2)
                size2: int = int((box2[2] + box2[3] - box2[0] - box2[1]) / 2)
                return size1 - size2
            boxes.sort(key=cmp_to_key(box_size_cmp), reverse=True)

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

            # TODO: 实现(6, 7)部位未检测到时的算法
            # 保证两个部位一定是出现的
            try:
                assert (mathtools.is_part_in_people(json_dict["people"][people_id], elbow_pair[0]))
                assert (mathtools.is_part_in_people(json_dict["people"][people_id], elbow_pair[1]))
            except AssertionError as e:
                print(f"关节不存在！第{num}张图像，第{people_id}个人。")

            x1 = int(pose_keypoints_2d[elbow_pair[0] * 3])
            y1 = int(pose_keypoints_2d[elbow_pair[0] * 3 + 1])
            x2 = int(pose_keypoints_2d[elbow_pair[1] * 3])
            y2 = int(pose_keypoints_2d[elbow_pair[1] * 3 + 1])

            dist = mathtools.get_vertical_distance(x1, y1, x2, y2, center_x, center_y)
            # print(f"[image {num}] 距离Person{people_id} {int(dist)} pixel.")

            while num >= len(distance1): distance1.append([])
            distance1[num].append(int(dist))

            # distance1数组访问方式：
            # distance1[图片编号][people_id(人物编号，从0开始)] = 距离
            # 特点：可以直接用图片编号访问
            # 没识别到球的位置默认为空数组，即distance1[图片编号][people_id] = []

            if people_id >= len(distance2): distance2.append([])
            distance2[people_id].append((num, int(dist)))
            # distance2数组访问方式：
            # distance2[people_id(人物编号，从0开始)] = tuple(图片编号, 距离)
            # 特点：图片编号是递增不连续的，便于在相邻下标位置访问到距离
            # 不递增原因：某些位置没有球

            while num >= len(horizontal_dist): horizontal_dist.append([])
            dist2 = int(mathtools.get_horizontal_distance(x1, y1, x2, y2, center_x, center_y))
            horizontal_dist[num].append(dist2)
            # horizontal_dist存储球中心与人胳膊中垂线的距离
            # 存储方式与distance1完全相同
    else:
        distance1.append([])
        horizontal_dist.append([])


def video_basic_info(videoProcessor: VideoInfoLoader):
    # 1. 检测到排球的帧的比例
    # 检测不到排球的两重原因：排球飞出视野；视野中有排球但未检测到
    total_frame = 0
    detected_frame = 0
    for positions in videoProcessor.getVolleyPosition():
        total_frame += 1
        if len(positions) != 0:
            detected_frame += 1

    valid_percent = int(detected_frame / total_frame * 100)
    print(f"排球帧总数:{total_frame}, 检测到帧的数目:{detected_frame}, 合格率: {valid_percent}%")

    # 2. 检查姿态json文件是否完整
    if not os.path.exists(os.path.join(videoProcessor.json_path, "2_keypoints.json")):
        raise Exception("姿态数据json不全!")


# 类的类型标注
class DistanceInfo:
    keyImages: ClassVar[list[int]]
    distance1: ClassVar[list]
    # distance1数组访问方式：
    # distance1[图片编号][people_id(人物编号，从0开始)] = 距离
    # 特点：可以直接用图片编号访问
    # 没识别到球的位置默认为空数组，即distance1[图片编号] = []
    horizontal_dist: ClassVar[list]
    volley_position: ClassVar[list]

    def __init__(self, keyImages, distance1, horizontal_dist, volley_position):
        self.keyImages = keyImages
        self.distance1 = distance1
        self.horizontal_dist = horizontal_dist
        self.volley_position = volley_position


# 命令行参数：
# 1. save_path: 保存raw图片文件的路径
# 2. mp4_path: 源图片文件的路径
# 3. json_path: 保存json文件的路径
# 4. result_path: 保存标记后图片的路径
# 5. keyImage_path: 关键帧路径
# 6. volley_position_path: 排球位置json路径
# 7. json_result: result.json保存路径
def main():
    # 在pose_images文件夹生成视频的全切片
    # 1. save_path = "pose_images"
    # 2. mp4_path = "video/错误对垫姿势1.mp4"
    # 3. json_path = "pose_images_json"
    # 4. result_path = "pose_results"
    # 5. keyImage_path = "pose_keyimages"
    # 6. volley_position_path = "volleyball_detect.json"
    # 7. json_result = "result.json"
    save_path = sys.argv[1]  # folder
    mp4_path = sys.argv[2]
    json_path = sys.argv[3]  # folder
    result_path = sys.argv[4]
    keyImage_path = sys.argv[5]
    volley_position_path = sys.argv[6]  # if exists, use; else, create
    json_result = sys.argv[7]

    # # 3. 检查当前项目是否已生成
    # if os.path.exists(result_path):
    #     raise Exception("此项目已经生成!")

    videoInfo = VideoInfoLoader(save_path, mp4_path, json_path, result_path,
                                keyImage_path, volley_position_path,
                                is_low_resolution=False, is_produce_motion_data=False)

    video_basic_info(videoInfo)

    volley_position = videoInfo.getVolleyPosition()
    total_num = videoInfo.total_num

    distance1 = []
    distance2 = []
    horizontal_dist = []
    for i in range(total_num):
        calc_distance(save_path, json_path, i + 1, volley_position, distance1, distance2, horizontal_dist)

    keyImages = keyImage.getCatchBallImage(distance2, volley_position, horizontal_dist)
    distanceInfo = DistanceInfo(keyImages, distance1, horizontal_dist, volley_position)
    print(f"图像关键帧列表： {keyImages}")

    # 输出的信息json
    arguments_json = [
        {
            "imgLoc": f"{i + 1}.jpg",
            "data": {
                "upper": {}, "lower": {}, "ball": {}
            }
        } for i in range(total_num)]

    if not os.path.exists(result_path):
        print(f"结果存放目录不存在，已自动生成：{result_path}")
        os.mkdir(result_path)

    print("开始绘制基础信息... (level=1)")
    # 绘制信息
    for i in tqdm(range(total_num)):
        img = graphics.annotate_img(save_path, json_path, i + 1, distanceInfo, arguments_json)
        if config.gl_config["keyImageOnly"]:
            if (i+1) in keyImages:
                cv2.imwrite(os.path.join(result_path, f"{i + 1}.jpg"), img)
        else:
            cv2.imwrite(os.path.join(result_path, f"{i + 1}.jpg"), img)

    print("已完成pose_result的写入")

    # 球的信息标注属于第3级渲染
    if config.gl_config["render_level"] >= 3:
        inteval = 1 / 30  # 设置间隔两帧的时间为1/30 s
        height_all = ball_flight.height(result_path, json_path, volley_position)
        print("[info] 已成功获取全部图像中球的高度。")
        speed_all = ball_flight.speed(result_path, json_path, volley_position, inteval)
        print("[info] 已成功获取到全部图像中球的速度。")
        direction_all = ball_flight.direction(result_path, json_path, volley_position)
        print("[info] 已成功获取到全部图像中球的方向。")
        for i in range(1, total_num + 1):
            arguments_json[i - 1]["data"]["ball"]["lastHeight"] = round_safe(height_all.get(i), 2)
            arguments_json[i - 1]["data"]["ball"]["initialAngle"] = round_safe(direction_all.get(i), 2)
            arguments_json[i - 1]["data"]["ball"]["initialVelocity"] = round_safe(speed_all.get(i), 2)

            arguments_json[i - 1]["data"]["coordination"] = 90
            arguments_json[i - 1]["data"]["accuracy"] = 80
            arguments_json[i - 1]["data"]["rate"] = 85

            if i in keyImages:
                try:
                    evaluate.evaluate(arguments_json[i - 1])
                except Exception as e:
                    print(f"Exception when processing image {i}", e)
            else:
                arguments_json[i - 1]["data"]["isKeyImage"] = False

    # 只生成关键帧的json
    final_json = []
    for i in range(0, total_num):
        if (i+1) in keyImages:
            final_json.append(arguments_json[i])

    # 导出json文件
    with codecs.open(json_result, "w", encoding="utf-8") as f:
        s = json.dumps(final_json, ensure_ascii=False) # 以UTF-8格式写入文件
        f.write(s)
        print("数据json生成完毕！")

    # 创建一个存放排球接球关键帧的目录
    specific_image_path = os.path.join(keyImage_path)
    if not os.path.exists(specific_image_path):
        os.makedirs(specific_image_path)

    # 将接球的关键帧复制到result_path的catch目录中
    for i in keyImages:
        shutil.copyfile(os.path.join(result_path, f"{i}.jpg"), os.path.join(specific_image_path, f"{i}.jpg"))

    if config.gl_config["combinePic"]:
        print("开始将结果合成视频！")
        combinePic.save_video(videoInfo.result_path, video_name=os.path.join(videoInfo.keyImage_path, "video.mp4"))
        print("合成完毕！")


if __name__ == "__main__":
    main()
