"""
本文件展示了VolleyballDetect模块的使用方式：
先通过import引入，再使用detect_ball函数调用获得一个四元数组列表即可
"""

import cv2
import os
from detectron2_package import VolleyballDetect as Detect

if __name__ == "__main__":
    # 恢复默认路径为本文件所在路径
    file_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(file_path)

    # print(os.getcwd())
    img = cv2.imread("../images/1.jpg", cv2.IMREAD_COLOR)
    # print(img)
    box = Detect.detect_ball(img)
    print(box)