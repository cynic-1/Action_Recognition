import os
import cv2



from tqdm import tqdm

# 函数功能：将某个目录下连续的*.jpg文件存为视频
# 参数img_root：目录路径，注意要以/结尾，不包含中文
# 参数video_name: 保存视频的名称
def save_video(img_root, video_name, fps=30):
    # # 获取到运行文件的路径，不是当前模块的路径
    # print(os.path.abspath(sys.argv[0]))
    frame = cv2.imread(os.path.join(img_root, "1.jpg"))
    size = (frame.shape[1], frame.shape[0])

    # 可以用(*'DVIX')或(*'X264'),如果都不行先装ffmepg: sudo apt-get install ffmepg
    # 不同视频编码对应不同视频格式（例：'I','4','2','0' 对应avi格式）
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    videoWriter = cv2.VideoWriter(video_name, fourcc, fps, size)  # 最后一个是保存图片的尺寸

    total_num = len(os.listdir(img_root))
    for i in tqdm(range(1, total_num + 1)):
        frame = cv2.imread(os.path.join(img_root, str(i) + '.jpg'))
        videoWriter.write(frame)

    videoWriter.release()


if __name__ == "__main__":
    img_root = "..\\info\\VID_20220420_110204(1)\\pose_results\\"  # 这里写你的文件夹路径，比如：/home/youname/data/img/,注意最后一个文件夹要有斜杠
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
