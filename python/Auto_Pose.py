# ---------------------------
# 本程序作用：自动调用video_process进行测试
# requires video_path == "E:\\volleyball"
# ensures json_path == "info\\{filename[:-4]}\\pose_images_json"

import os
import subprocess


def createIfNotExist(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


if __name__ == "__main__":
    main_out_path = "E:\\volleyball\\info\\"
    createIfNotExist(main_out_path)

    video_path = "E:\\volleyball\\"
    files = os.listdir(video_path)
    folders = os.listdir(main_out_path)
    for filename in files:
        if filename.endswith(".mp4"):
            # print(f"file: {filename}")
            if filename[:-4] not in folders:
                # print("json数据未生成, 跳过此文件")
                continue

            os.system('chcp 65001')
            dir_name = main_out_path + filename[:-4]
            createIfNotExist(dir_name)

            input_video = video_path + filename
            image_path = os.path.join(dir_name, "pose_images")
            json_path = os.path.join(dir_name, "pose_images_json")
            result_path = os.path.join(dir_name, "pose_result")
            keyImage_path = os.path.join(dir_name, "pose_keyImage")
            volley_path = "volley_json\\" + filename[:-4] + ".json"
            print(volley_path)
            json_result = os.path.join(dir_name, "result.json")

            retCode = subprocess.call(f"python video_process.py {image_path} {input_video} {json_path} "
                                      f"{result_path} {keyImage_path} {volley_path} {json_result}")

            print(f"Return Code: {retCode}")
            if retCode != 0:
                print("出现异常！")

            print(f"Finish {filename}.")
