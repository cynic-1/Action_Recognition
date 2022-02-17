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

from predictor import VisualizationDemo

# constants
WINDOW_NAME = "COCO detections"


def setup_cfg(args):
    # load config from file and command-line arguments
    cfg = get_cfg()
    # To use demo for Panoptic-DeepLab, please uncomment the following two lines.
    # from detectron2.projects.panoptic_deeplab import add_panoptic_deeplab_config  # noqa
    # add_panoptic_deeplab_config(cfg)
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    # Set score_threshold for builtin models
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.confidence_threshold
    cfg.freeze()
    return cfg


def get_parser():
    parser = argparse.ArgumentParser(description="Detectron2 demo for builtin configs")
    parser.add_argument(
        "--config-file",
        default="configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml",
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument("--webcam", action="store_true", help="Take inputs from webcam.")
    parser.add_argument("--video-input", help="Path to video file.")
    parser.add_argument(
        "--input",
        nargs="+",
        help="A list of space separated input images; "
        "or a single glob pattern such as 'directory/*.jpg'",
    )
    parser.add_argument(
        "--output",
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )

    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line 'KEY VALUE' pairs",
        default=["MODEL.WEIGHTS", "model_final_280758.pkl"],
        nargs=argparse.REMAINDER,
    )
    return parser


if __name__ == "__main__":
    file_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(file_path)

    mp.set_start_method("spawn", force=True)
    args = get_parser().parse_args()
    setup_logger(name="fvcore")
    logger = setup_logger()
    logger.info("Arguments: " + str(args))  # 以日志形式输出命令行参数

    cfg = setup_cfg(args)

    demo = VisualizationDemo(cfg)

    # 列出当前路径下的所有目录和文件
    now_path_dir = os.listdir(".")

    video_path = args.input[0]
    # input是args的一个对象,形式为列表，从列表中提取第一个参数，是视频
    print("输入视频的路径:", video_path)

    video_save_path = video_path.split(".")[0] + "_frames"


    # 如果目录不存在，就新建一个目录
    if video_save_path not in now_path_dir:
        logger.info(f"生成图片目录{video_save_path}不存在，自动建立一个。")
        os.mkdir(video_save_path)


    # 保存预测结果的目录
    video_prediction_path = video_path.split(".")[0] + "_prediction_frames"

    if video_prediction_path not in now_path_dir:
        logger.info(f"标记图片目录{video_prediction_path}不存在，自动建立一个新的。")
        os.mkdir(video_prediction_path)

    cap = cv2.VideoCapture(video_path)

    num_frames = cap.get(7)  # 获取帧总数
    print("frames: {}".format(num_frames))
    frame_count = 1

    while True:
        success, frame = cap.read()
        print("Read a New Frame: ", success, video_save_path + "{}.jpg".format(frame_count), frame is None)
        if frame is not None:
            # 保存帧图像到文件中
            cv2.imwrite(video_save_path + "/{}.jpg".format(frame_count), frame)
        frame_count += 1
        if(frame_count > num_frames): break
    cap.release()
    cv2.destroyAllWindows()


    # 逐个处理图片，并刷新进度条
    for index in tqdm.tqdm(list(range(1, int(num_frames)+1))):
        # use PIL, to be consistent with evaluation
        img = read_image(video_save_path + '/{}.jpg'.format(index), format="BGR")
        start_time = time.time()
        predictions, visualized_output = demo.run_on_image(img)
        # print(list(predictions.keys())) # 一般prediction中只有
        logger.info(
            "{}: {} in {:.2f}s".format(
                index,
                "detected {} instances".format(len(predictions["instances"]))
                if "instances" in predictions
                else "finished",
                time.time() - start_time,
            )
        )
        visualized_output.save(video_prediction_path + "/{}.jpg".format(index))