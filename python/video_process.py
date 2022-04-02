# 本程序用于以命令行方式调用OpenPoseDemo.exe，得到想要的JSON文件
# 本程序以视频为原料，输出视频中每帧的关键参数，并在图像上进行数据的标注
import codecs
import json
import os
import shutil

import cv2

import evaluate
import graphics
import cut_video
import mathtools
import keyImage

import ball_flight
from mathtools import round_safe
import demo.ball_prediction_new


# save_path = "pose_images"
#     mp4_path = "video/错误对垫姿势3.mp4"
#     json_path = "pose_images_json"
#     result_path = "pose_results"
#     keyimage_path = "pose_keyimages"
class VideoProcessor:
    def __init__(self, save_path, mp4_path, json_path, result_path, keyImage_path, volley_position_path, is_low_resolution):
        self.save_path = save_path
        self.mp4_path = mp4_path
        self.json_path = json_path
        self.result_path = result_path
        self.keyImage_path = keyImage_path
        self.is_low_resolution = is_low_resolution
        self.total_num = 0
        self.volley_position_path = volley_position_path
        self.volley_position = None
        self.extrema = []  # 转折点列表
        self.__prepare_source()

    # 获取VolleyPosition
    def getVolleyPosition(self):
        if self.volley_position is None:
            # 读取经过补全的排球位置
            self.volley_position, self.extrema = demo.ball_prediction_new.enhanced_volley_detect(self.volley_position_path)
        return self.volley_position

    def __prepare_source(self):
        # 定位系统路径到本文件的路径
        dir_path = os.path.dirname(os.path.realpath(__file__))  # 本文件当前的路径
        os.chdir(dir_path)

        if os.path.exists(self.save_path):
            print("检测到视频切片数据已经生成，就不再生成了。")
        else:
            print("正在生成视频切片数据。")
            cut_video.process_video(self.mp4_path, self.save_path, 1)
            print("视频切片数据生成完毕。")

        self.total_num = len(os.listdir(save_path))

        # 对视频里的所有图片生成json
        if not os.path.exists(self.json_path):
            print("图像的人体姿态json未生成，将开始生成。")
            self.__produce_json(self.save_path, self.json_path)
        else:
            print("图像的人体姿态JSON已生成，将不再生成。")

        if not os.path.exists(self.result_path):
            print("输出目录不存在，将自动创建。")
            os.makedirs(result_path)

        self.__produce_volley_json()

    # 命令行调用OpenPoseDemo程序，生成JSON
    # 具体就是将image_dir里的图片内容转化为姿态JSON
    # 执行方式是阻塞执行，即先执行完命令行，再执行下面的python代码
    def __produce_json(self, images_path, json_path):
        dir_path = os.path.dirname(os.path.realpath(__file__))  # 本文件当前的路径
        root_path = dir_path + "/../"  # 根路径，即为OpenPose主目录

        if not os.path.exists(json_path):
            os.makedirs(json_path)
            print("指定的json输出目录不存在，将新建一个")

        params = dict()
        # 这些路径都是相对于根路径而言的路径
        params["image_dir"] = "\"" + os.path.join(dir_path, images_path) + "\""
        # params["write_images"] = os.path.join(dir_path, "output_images")
        params["model_pose"] = "BODY_25"
        params["write_json"] = "\"" + os.path.join(dir_path, json_path) + "\""

        if self.is_low_resolution:
            params["net_resolution"] = "320x176"  # 调低分辨率，以让低显存电脑也能顺利运行

        os.chdir(root_path)  # 跳转到OpenPose根路径再执行
        print(os.getcwd())
        os.system('chcp 65001')  # 开启utf-8支持，否则输出乱码
        cmd = "bin\OpenPoseDemo" + self.__arg_constructor(params)
        print(cmd)
        information = os.popen(cmd)
        print(information.read())
        information.close()

        # 切换回原来的路径
        os.chdir(dir_path)

    # 用来将参数字典转化为命令行参数字符串
    def __arg_constructor(self, params: dict):
        arg = ""
        for key in params.keys():
            value = params[key]
            if type(value) == bool:
                arg = arg + f" --{key}"
            else:
                arg = arg + f" --{key} {value}"
        return arg

    def __produce_volley_json(self):
        # 生成排球识别信息的json文件
        if not os.path.exists(self.volley_position_path):
            # 引入排球识别
            print("排球识别信息不存在，将开始生成！")
            from detectron2_package import VolleyballDetect as Detect

            lst = []
            for i in range(self.total_num):
                img = cv2.imread(os.path.join(save_path, f"{i + 1}.jpg"))
                boxes = Detect.detect_ball(img)
                boxes_new = []
                for box in boxes:
                    box = list(map(lambda x: float(x), box))
                    boxes_new.append(box)
                lst.append(boxes_new)
                print(f"[image {i + 1}, total {self.total_num}] completed.")
            str = json.dumps(lst)
            with open(self.volley_position_path, "w") as f:
                f.write(str)
        else:
            print("排球位置信息JSON存在，不再生成")


# 计算球与人之间的距离
def calc_distance(image_path, json_path, num, volley_position, distance1, distance2, horizontal_dist):
    img = cv2.imread(os.path.join(image_path, f"{num}.jpg"))
    # 读取和转化JSON文件
    with open(os.path.join(json_path, f"{num}_keypoints.json"), "r") as f:
        json_dict = json.load(f)
        mathtools.people_track(json_dict)

    # 获取球的信息，并在图像上标注球
    boxes = volley_position[num - 1]
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
    mp4_path = "video/错误对垫姿势1.mp4"
    json_path = "pose_images_json"
    result_path = "pose_results"
    keyImage_path = "pose_keyimages"
    volley_position_path = "volleyball_detect.json"

    videoProcessor = VideoProcessor(save_path, mp4_path, json_path, result_path,
                                    keyImage_path, volley_position_path,
                                    is_low_resolution=True)

    volley_position = videoProcessor.getVolleyPosition()
    total_num = videoProcessor.total_num

    distance1 = []
    distance2 = []
    horizontal_dist = []
    for i in range(total_num):
        calc_distance(save_path, json_path, i + 1, volley_position, distance1, distance2, horizontal_dist)

    catch_images = keyImage.getCatchBallImage(distance2, volley_position, horizontal_dist)
    dynamic_info = {"min_imageID": catch_images,
                    "distance": distance1, "horizontal_dist": horizontal_dist,
                    "volley_position": volley_position}
    print(f"图像关键帧： {catch_images}")

    # 输出的信息json
    arguments_json = [
        {
            "imgLoc": f"{i + 1}.jpg",
            "data": {
                "upper": {}, "lower": {}, "ball": {}
            }
        } for i in range(total_num)]

    # 绘制信息
    for i in range(total_num):
        img = graphics.annotate_img(save_path, json_path, i + 1, dynamic_info, arguments_json)
        cv2.imwrite(os.path.join(result_path, f"{i + 1}.jpg"), img)

    inteval = 1 / 30  # 设置间隔两帧的时间为1/30 s
    height_all = ball_flight.height(result_path, volley_position, volley_position_path)
    print("[info] 已成功获取全部图像中球的高度。")
    speed_all = ball_flight.speed(result_path, volley_position, volley_position_path, inteval)
    print("[info] 已成功获取到全部图像中球的速度。")
    direction_all = ball_flight.direction(result_path, volley_position, volley_position_path)
    print("[info] 已成功获取到全部图像中球的方向。")
    for i in range(1, total_num + 1):
        arguments_json[i - 1]["data"]["ball"]["lastHeight"] = round_safe(height_all.get(i), 2)
        arguments_json[i - 1]["data"]["ball"]["initialAngle"] = round_safe(direction_all.get(i), 2)
        arguments_json[i - 1]["data"]["ball"]["initialVelocity"] = round_safe(speed_all.get(i), 2)

        arguments_json[i - 1]["data"]["coordination"] = 90
        arguments_json[i - 1]["data"]["accuracy"] = 80
        arguments_json[i - 1]["data"]["rate"] = 85

        if i in catch_images:
            try:
                evaluate.evaluate(arguments_json[i - 1])
            except Exception as e:
                print(f"Exception when processing image {i}", e)
        else:
            arguments_json[i - 1]["data"]["isKeyImage"] = False


    # 只生成关键帧的json
    final_json = []
    for i in range(0, total_num):
        if (i+1) in catch_images:
            final_json.append(arguments_json[i])

    with codecs.open("result.json", "w", encoding="utf-8") as f:
        str = json.dumps(final_json, ensure_ascii=False) # 以UTF-8格式写入文件
        f.write(str)
        print("数据json生成完毕！")

    # 创建一个存放排球接球关键帧的目录
    specific_image_path = os.path.join(keyImage_path)
    if not os.path.exists(specific_image_path):
        os.makedirs(specific_image_path)

    # 将接球的关键帧复制到result_path的catch目录中
    for id in catch_images:
        shutil.copyfile(os.path.join(result_path, f"{id}.jpg"), os.path.join(specific_image_path, f"{id}.jpg"))
