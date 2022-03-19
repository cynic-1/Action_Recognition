import matplotlib.pyplot as plt
from ball_prediction_common import *
import ball_predict_x

annotate_ball_data = True


def main():
    volley_position = get_volleyCenter("../volleyball_detect.json")
    _volley_position = deepcopy(volley_position)
    extrema = ball_predict_x.predict_xAxis(volley_position)

    # 利用matplotlib作图
    fig = plt.figure(num=1)
    x, y = volley_position_to_plot(volley_position)
    plt.scatter(x, y)
    plt.show()

    # 265-276是变形最厉害的一段范围,应该重点检测
    if annotate_ball_data:
        ball_predict_x.annotate_image("../pose_images/", "predict_ball/", volley_position, _volley_position, extrema)

    # 将速度信息输出到csv文件
    # produceCSVTable("speed.csv", [(i+1) for i in range(total_num)], speed[:, 0],
    #                 xAxis_name="image_ID", yAxis_name="Speed")
    # produceCSVTable("position_x.csv", [(i+1) for i in range(total_num)],
    #                 [i[0] for i in volley_position], xAxis_name="image_ID",
    #                 yAxis_name="position_x")


# 为了避免Shadows name '' from outer place, 将主函数体安置在main中，以营造一个局部环境
if __name__ == "__main__":
    main()
