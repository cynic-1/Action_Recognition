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
    # To use predictball for Panoptic-DeepLab, please uncomment the following two lines.
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
    parser = argparse.ArgumentParser(description="Detectron2 predictball for builtin configs")
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
    logger.info("Arguments: " + str(args))  # ????????????????????????????????????

    cfg = setup_cfg(args)

    demo = VisualizationDemo(cfg)

    # ?????????????????????????????????????????????
    now_path_dir = os.listdir(".")

    video_path = args.input[0]
    # input???args???????????????,???????????????????????????????????????????????????????????????
    print("?????????????????????:", video_path)

    video_save_path = video_path.split(".")[0] + "_frames"


    # ?????????????????????????????????????????????
    if video_save_path not in now_path_dir:
        logger.info(f"??????????????????{video_save_path}?????????????????????????????????")
        os.mkdir(video_save_path)


    # ???????????????????????????
    video_prediction_path = video_path.split(".")[0] + "_prediction_frames"

    if video_prediction_path not in now_path_dir:
        logger.info(f"??????????????????{video_prediction_path}???????????????????????????????????????")
        os.mkdir(video_prediction_path)

    cap = cv2.VideoCapture(video_path)

    num_frames = cap.get(7)  # ???????????????
    print("frames: {}".format(num_frames))
    frame_count = 1

    while True:
        success, frame = cap.read()
        print("Read a New Frame: ", success, video_save_path + "{}.jpg".format(frame_count), frame is None)
        if frame is not None:
            # ???????????????????????????
            cv2.imwrite(video_save_path + "/{}.jpg".format(frame_count), frame)
        frame_count += 1
        if(frame_count > num_frames): break
    cap.release()
    cv2.destroyAllWindows()


    # ???????????????????????????????????????
    for index in tqdm.tqdm(list(range(1, int(num_frames)+1))):
        # use PIL, to be consistent with evaluation
        img = read_image(video_save_path + '/{}.jpg'.format(index), format="BGR")
        start_time = time.time()
        predictions, visualized_output = demo.run_on_image(img)
        # print(list(predictions.keys())) # ??????prediction?????????
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