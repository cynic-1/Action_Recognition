import cv2
import VolleyballDetect as Detect
import os
import numpy as np

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    video_path = "correct_pose.mp4"
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("视频打开失败，请重试")
    
    num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 获取视频的帧数
    print(f"帧数：{num_frames} fps")
    cnt = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cnt += 1
        if frame is None:
            print(f"frame {cnt}: Failed to capture the frame.")
        else:
            volley_box = Detect.detect_ball(frame)
            print(f"frame {cnt}: Detect {len(volley_box)} balls. Details: {volley_box}")


    """
    for index in num_lst:
        path = os.path.join(input_dir, f"{index}.jpg")
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        volley_box = Detect.detect_ball(img)

        if len(volley_box) == 4:
            cv2.rectangle(img, (int(volley_box[0]), int(volley_box[1])), \
                (int(volley_box[2]), int(volley_box[3])), (0, 255, 0), 3)

        save_path = os.path.join(output_dir, f"{index}.jpg")
        cv2.imwrite(save_path, img)
        print("finished " + save_path)
    """

    cap.close()