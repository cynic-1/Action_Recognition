import json
import os
import cv2

import numpy as np

if __name__ == "__main__":
    ball_path = "../volleyball_detect.json"
    with open(ball_path, "r") as f:
        _volley_position = json.load(f)
    volley_position = []
    for i in range(len(_volley_position)):
        if len(_volley_position[i]) == 0:
            volley_position.append([])
        else:
            x1, y1, x2, y2 = _volley_position[i][0]
            volley_position.append([(x1+x2)/2, (y1+y2)/2])
    size = len(volley_position)
    array = np.zeros((size, 2))
    inteval = 1/30
    valid_num = 0
    valid_list = [False for i in range(size)]
    for i in range(1, size):
        # 说明该帧和上一帧都检测到排球了
        if len(volley_position[i-1]) != 0 and len(volley_position[i]) != 0:
            valid_num += 1
            v_x = (volley_position[i][0] - volley_position[i-1][0]) / inteval
            v_y = (volley_position[i][1] - volley_position[i-1][1]) / inteval
            array[i][0] = v_x
            array[i][1] = v_y
            valid_list[i] = True

    # error发生在第50帧
    for i in range(1, size):
        # 位置未捕获，且上一帧没有问题，捕获到了速度
        if len(volley_position[i]) == 0:
            # 预测x坐标
            volley_position[i].append(volley_position[i-1][0] + array[i-1][0] * inteval)
            array[i][0] = (volley_position[i][0] - volley_position[i-1][0]) / inteval
            valid_list[i] = True
        else:
            if not valid_list[i]:
                array[i][0] = (volley_position[i][0] - volley_position[i-1][0]) / inteval
                valid_list[i] = True
        print(f"{i}: {volley_position[i]}")

    output_path = "predict_ball/"
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    input_path = "../pose_images/"
    total_num = len(os.listdir(input_path))
    for i in range(1, total_num+1):
        img = cv2.imread(input_path + f"{i}.jpg")
        if len(_volley_position[i-1]) == 0:
            color = (0, 0, 100)
        else:
            color = (0, 0, 255)
        cv2.circle(img, (int(volley_position[i-1][0]), 40), 10, color, -1)
        # img = img.copy()
        cv2.imwrite(output_path + f"{i}.jpg", img)

    print("合格帧整体比例：%.2f%%" % (valid_num/size*100))

