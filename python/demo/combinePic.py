import os
import cv2

if __name__ == "__main__":
    img_root = '../pose_results/'  # 这里写你的文件夹路径，比如：/home/youname/data/img/,注意最后一个文件夹要有斜杠
    fps = 30  # 保存视频的FPS，可以适当调整
    frame = cv2.imread(img_root + "1.jpg")
    size = (frame.shape[1], frame.shape[0])

    # 可以用(*'DVIX')或(*'X264'),如果都不行先装ffmepg: sudo apt-get install ffmepg
    # 不同视频编码对应不同视频格式（例：'I','4','2','0' 对应avi格式）
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    videoWriter = cv2.VideoWriter(img_root + "video.avi", fourcc, fps, size)  # 最后一个是保存图片的尺寸

    total_num = len(os.listdir(img_root))
    for i in range(1, total_num + 1):
        frame = cv2.imread(img_root + str(i) + '.jpg')
        videoWriter.write(frame)

    videoWriter.release()
