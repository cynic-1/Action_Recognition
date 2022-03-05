import json
import numpy
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
    array = np.zeros((size, 3))
    inteval = 1/30
    valid_num = 0
    for i in range(1, size):
        # 说明该帧和上一帧都检测到排球了
        if len(volley_position[i-1]) != 0 and len(volley_position[i]) != 0:
            valid_num += 1
            array[i][0] = (volley_position[i][0] - volley_position[i-1][0]) / inteval
            array[i][1] = (volley_position[i][1] - volley_position[i-1][1]) / inteval
            array[i][2] = 1

    print("合格帧整体比例：%.2f%%" % (valid_num/size*100))

