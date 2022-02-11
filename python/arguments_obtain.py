import math


# 建立BODY_25的参数对应
# 序号均从0开始
body_dict = {
    "RShoulder": 2, "RElbow": 3, "RWrist": 4,
    "LShoulder": 5, "LElbow": 6, "LWrist": 7
}

global G_pose_keypoints
G_pose_keypoints = []


# 判断某个部位是否被识别到了
# part:数字
def exists(part):
    if G_pose_keypoints[part*3+2] > 0.001:
        return True
    else:
        return False


def setup_keypoints(pose_keypoints):
    G_pose_keypoints = pose_keypoints


# 获取某个部位的XY坐标
def get_partXY(part):
    return G_pose_keypoints[part*3+0], G_pose_keypoints[part*3+1]


def get_shoulder_angle(pose_keypoints):
    RElbow = body_dict["RElbow"]
    RWrist = body_dict["RWrist"]
    LElbow = body_dict["LElbow"]
    LWrist = body_dict["LWrist"]

    # 右前肢存在
    if(exists(RElbow) and exists(RWrist)):
        x_RElbow, y_RElbow = get_partXY(RElbow)
        x_RWrist, y_RWrist = get_partXY(RWrist)
        angle = math.atan2(x_RElbow-x_RWrist, y_RElbow-y_RWrist)
        angle = math.degrees(angle)
        return angle
    else if()
    
    x_LElbow, y_LElbow = get_partXY(LElbow)
    x_LWrist, y_LWrist = get_partXY(LWrist)


    