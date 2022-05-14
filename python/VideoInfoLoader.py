import json
import predictball.ball_prediction_new
import os
import cut_video
import cv2
import config


# 生成并存储视频的基本信息，包括：视频位置、视频切片位置、保存路径、姿态json位置、排球位置json等等
class VideoInfoLoader:
    def __init__(self, save_path: str, mp4_path: str, json_path: str,
                 result_path: str, keyImage_path: str, volley_position_path: str, is_low_resolution: bool,
                 is_produce_motion_data: bool = True):
        self.save_path = save_path
        self.mp4_path = mp4_path
        self.json_path = json_path
        self.result_path = result_path
        self.keyImage_path = keyImage_path
        self.is_low_resolution = is_low_resolution
        self.is_produce_motion_data = is_produce_motion_data

        self.total_num = 0
        self.volley_position_path = volley_position_path
        self.volley_position = None
        self.extrema = []  # 转折点列表
        self.__prepare_source()

    # 获取VolleyPosition
    def getVolleyPosition(self) -> list:
        if self.volley_position is None:
            # 读取经过补全的排球位置
            if config.gl_config["use_volley_pos_fill"]:
                self.volley_position, self.extrema = predictball.ball_prediction_new.enhanced_volley_detect(
                    self.volley_position_path)
            else:
                with open(self.volley_position_path, "r") as f:
                    self.volley_position = json.load(f)

            print("排球位置补全完成！")
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

        self.total_num = len(os.listdir(self.save_path))
        self.__produce_volley_json()  # 生成排球位置数据：前置要求：视频已经切片

        if self.is_produce_motion_data:
            # 对视频里的所有图片生成json
            if not os.path.exists(self.json_path):
                print("图像的人体姿态json未生成，将开始生成。")
                self.__produce_json(self.save_path, self.json_path)
            else:
                print("图像的人体姿态JSON已生成，将不再生成。")

            if not os.path.exists(self.result_path):
                print("输出目录不存在，将自动创建。")
                os.makedirs(self.result_path)


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
                img = cv2.imread(os.path.join(self.save_path, f"{i + 1}.jpg"))
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