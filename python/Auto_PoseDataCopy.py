import os

if __name__ == "__main__":
    folders = os.listdir("info")
    if not os.path.exists("poses"):
        os.mkdir("poses")
    for folder in folders:
        source = f"info\\{folder}\\pose_images_json\\"
        dst = f"poses\\{folder}\\pose_images_json\\"
        os.popen(f"xcopy {source} {dst} /E")