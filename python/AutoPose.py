import json
import os
import subprocess

import cv2
from detectron2_package import VolleyballDetect as Detect
from tqdm import tqdm

if __name__ == "__main__":
    if not os.path.exists("infos"):
        os.mkdir("info")

    files = os.listdir("D:\\volley")
    for filename in files:
        if filename.endswith(".mp4"):
            os.system('chcp 65001')
            dir_name = "info\\" + filename[:-4]
            os.mkdir(dir_name)

            input_video = "D:\\volley\\" + filename
            image_path = os.path.join(dir_name, "pose_images")
            json_path = os.path.join(dir_name, "pose_images_json")

            subprocess.call(f"python video_process.py {image_path} {input_video} {json_path} None None None None")

            print(f"Finish {filename}.")
