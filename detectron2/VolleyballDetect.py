# Copyright (c) Facebook, Inc. and its affiliates.
import argparse
import glob
import multiprocessing as mp
import numpy as np
import os
import tempfile
import time
import warnings
import cv2
import tqdm

from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
from detectron2.utils.logger import setup_logger
from detectron2.data import MetadataCatalog

from predictor import VisualizationDemo

# constants
WINDOW_NAME = "COCO detections"


# 设置的一些关于模型的常量
# config_file = "D:\迅雷下载\Canvas\detectron2-main\detectron2-main\configs\COCO-InstanceSegmentation\mask_rcnn_R_50_FPN_3x.yaml" # 配置文件位置
config_file = "configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
opts = ["MODEL.WEIGHTS", "detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl"]
confidence_threshold = 0.5  # 置信度阈值，超出阈值才显示


def setup_cfg():
    global labels  # 将labels发送到全局

    # load config from file and command-line arguments
    cfg = get_cfg()
    # To use demo for Panoptic-DeepLab, please uncomment the following two lines.
    # from detectron2.projects.panoptic_deeplab import add_panoptic_deeplab_config  # noqa
    # add_panoptic_deeplab_config(cfg)
    cfg.merge_from_file(config_file)
    cfg.merge_from_list(opts)
    # Set score_threshold for builtin models
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = confidence_threshold
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = confidence_threshold
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = confidence_threshold
    cfg.freeze()

    metadata = MetadataCatalog.get(
        cfg.DATASETS.TEST[0] if len(cfg.DATASETS.TEST) else "__unused"
    )
    labels = metadata.get("thing_classes", None)  # 表示事物的名称，与classes中的序号一一对应

    return cfg


#------------ 模块的初始化代码 -----------------------
# 恢复默认路径为本文件所在路径
file_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(file_path)

mp.set_start_method("spawn", force=True)
setup_logger(name="fvcore")
logger = setup_logger()

# 加载配置项
cfg = setup_cfg()
logger.info(f"使用模型{cfg.DATASETS.TEST[0]}")
logger.info("支持的识别对象有:" + ", ".join(labels))

# 生成图像识别核心
demo = VisualizationDemo(cfg)
# ---------------------------------------------------




# 通过predictions获取到排球的位置边框
def getBox(predictions):
    # 一般predictions中只有instances一个键
    instances = predictions["instances"]

    # 解析instances中的信息
    boxes = instances.pred_boxes if instances.has("pred_boxes") else None  # 边界取景框
    scores = instances.scores if instances.has("scores") else None  # 可信度列表
    classes = instances.pred_classes.tolist() if instances.has("pred_classes") else None  # 类别序号，对应labels的名称
    keypoints = instances.pred_keypoints if instances.has("pred_keypoints") else None  # 关键点，一般是没有
    masks = instances.pred_masks  # 指定物体的遮罩，是n*height*width的np布尔数组

    volley_box = []

    # 选出其中的排球
    for i in range(len(classes)):
        if(labels[classes[i]] == "sports ball"):
            # 获取物体的边界框
            box = boxes[i].tensor.to("cpu").numpy()[0]
            print(f"sports ball at {box}")
            # 将获取到的球添加进列表中
            volley_box = box
    return volley_box



# 函数作用：获取球的位置边框
# 参数img：Cv2读取的图像nparray，默认BGR格式
# 返回值：边框坐标，4元列表
def detect_ball(img, show=False):
    # use PIL, to be consistent with evaluation
    # img = read_image("1.jpg", format="BGR")  # 需要BGR格式
    img = img.copy()

    start_time = time.time()
    predictions, visualized_output = demo.run_on_image(img)  # 调用Detectron2识别图像

    volley_box = getBox(predictions)  # 获取边框信息

    # 以彩色模式读取图片，opencv2默认读取的图像都是BGR格式
    # img = cv2.imread("1.jpg", cv2.IMREAD_COLOR)

    if show == True:
        img = img.copy()  # opencv2的bug，需要拷贝一下才能在绘图函数中使用，原因未知
        cv2.rectangle(img, (int(volley_box[0]), int(volley_box[1])), \
            (int(volley_box[2]), int(volley_box[3])), (0, 255, 0), 3)
        cv2.imshow("image", img)
        cv2.waitKey(0)

    logger.info(
        "{}: {} in {:.2f}s".format(
            "当前",
            "detected {} instances".format(len(predictions["instances"]))
            if "instances" in predictions
            else "finished",
            time.time() - start_time,
        )
    )

    # 存储格式化标注的图像
    # visualized_output.save("output_1.jpg")
    return volley_box