import json
import os
import cv2
from detectron2_package import VolleyballDetect as Detect
from tqdm import tqdm

if __name__ == "__main__":
    if not os.path.exists("volley_json"):
        os.mkdir("volley_json")

    files = os.listdir("E:\\volleyball")
    for filename in files:
        if filename.endswith(".mp4"):
            os.system('chcp 65001')
            os.popen("rd /S /Q pose_images")

            fileID = int(filename.split("_")[0])
            input_video = "E:\\volleyball\\" + filename
            jsonPath = f"volley_json\\{fileID}.json"

            cap = cv2.VideoCapture(input_video)

            num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 获取视频的帧数
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # 视频宽度
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 高度
            fps = cap.get(cv2.CAP_PROP_FPS)  # 帧率

            if not cap.isOpened():
                print("视频无法打开，请检查路径。")
                continue

            print("视频基本信息:")
            print(f"分辨率：{width}x{height}\n" + "帧率：%.2ffps" % fps)
            frame_cnt = 0
            image_cnt = 0

            lst = []
            for _ in range(int(num_frames)):
                # 读取帧
                ret, frame = cap.read()
                frame_cnt += 1
                # 如果达到视频的结尾，那么ret返回值就是False，这时将自动退出
                if not ret:
                    break

                boxes = Detect.detect_ball(frame)
                boxes_new = []
                for box in boxes:
                    box = list(map(lambda x: float(x), box))
                    boxes_new.append(box)
                lst.append(boxes_new)
                print(f"[image {frame_cnt}, total {num_frames}] completed.")

            str = json.dumps(lst)
            with open(jsonPath, "w") as f:
                f.write(str)

            print(f"---------- Finish {fileID}: {filename} -----------------")
            os.remove("pose_images")
