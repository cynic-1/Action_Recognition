import cv2
import argparse
import os
import time
import math
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser(description="从视频中截取图片")
    parser.add_argument("--input", help="需要截取的视频", dest="input", type=str)
    parser.add_argument("--output_path", help="输出图像的路径,若没有，自动创建", dest="output_path", type=str)
    parser.add_argument("--skip_frame", help="需要间隔多少帧截取图像,默认为1帧", dest="skip_frame", default=1, type=int)
    arg = parser.parse_args()
    return arg


def process_video(input_video, output_path, num):
    if not os.path.exists(output_path):
        print("指定的路径不存在，将自动建立路径。")
        os.makedirs(output_path)

    cap = cv2.VideoCapture(input_video)
    name = str(input_video)[0:str(input_video).rfind(".")]  # 截掉最后一个.及之后的内容
    name = name[name.rfind("/")+1:]
    name = name[name.rfind("\\")+1:]
    print("视频名称为 "+name)

    num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 获取视频的帧数
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # 视频宽度
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 高度
    fps = cap.get(cv2.CAP_PROP_FPS)  # 帧率

    if not cap.isOpened():
        print("视频无法打开，请检查路径。")
        return

    print("视频基本信息:")
    print(f"分辨率：{width}x{height}\n" + "帧率：%.2ffps" % fps)
    print(f"视频共有{num_frames}帧，每隔{num}帧截取一次图像。")
    frame_cnt = 0
    image_cnt = 0
    for _ in tqdm(range(int(num_frames))):
        # 读取帧
        ret, frame = cap.read()
        frame_cnt += 1
        # 如果达到视频的结尾，那么ret返回值就是False，这时将自动退出
        if not ret:
            break
        if frame_cnt % num == 0:
            image_cnt += 1
            path = os.path.join(output_path, f"{image_cnt}.jpg")
            success = cv2.imwrite(path, frame)  # 文件路径还不能出现中文！！！
            # print(path, "success" if success else "failure")


if __name__ == "__main__":
    arg = parse_args()
    process_video(arg.input, arg.output_path, arg.skip_frame)

# 推荐的命令行调用方式
# .\cut_video.py --input .\video\自垫球-横向.mp4 --output_path ./images/ --skip_frame 100
# 或者不明白的话也可以 .\cut_video.py --help来获取帮助
