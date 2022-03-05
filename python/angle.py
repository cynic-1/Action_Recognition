import math

# {0,  "Nose"},
# {1,  "Neck"},
# {2,  "RShoulder"},
# {3,  "RElbow"},
# {4,  "RWrist"},
# {5,  "LShoulder"},
# {6,  "LElbow"},
# {7,  "LWrist"},
# {8,  "MidHip"},
# {9,  "RHip"},
# {10, "RKnee"},
# {11, "RAnkle"},
# {12, "LHip"},
# {13, "LKnee"},
# {14, "LAnkle"},
# {15, "REye"},
# {16, "LEye"},
# {17, "REar"},
# {18, "LEar"},
# {19, "LBigToe"},
# {20, "LSmallToe"},
# {21, "LHeel"},
# {22, "RBigToe"},
# {23, "RSmallToe"},
# {24, "RHeel"},
# {25, "Background"}

def angle_between_points( p0, p1, p2 ):
    # 计算角度
    a = (p1[0]-p0[0])**2 + (p1[1]-p0[1])**2
    b = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2
    c = (p2[0]-p0[0])**2 + (p2[1]-p0[1])**2
    if a * b == 0:
        return -1.0

    return  math.acos( (a+b-c) / math.sqrt(4*a*b) ) * 180 /math.pi

def get_angle_point(human, pos):  #human是每个人得到的json文件转化的二维数组
    # 返回各个部位的关键点
    pnts = []

    if pos == 'left_elbow':
        pos_list = (5,6,7)
    elif pos == 'left_shoulder':
        pos_list = (1,5,7)
    elif pos == 'left_knee':
        pos_list = (12,13,14)
    elif pos == 'left_ankle':
        pos_list = (5,12,14)
    elif pos == 'right_elbow':
        pos_list = (2,3,4)
    elif pos == 'right_shoulder':
        pos_list = (1,2,4)
    elif pos == 'right_knee':
        pos_list = (9,10,11)
    elif pos == 'right_ankle':
        pos_list = (2,9,11)
    elif pos == 'right_elbow_trunk':
        pos_list = (8,1,7)
    else:
        # print('Unknown  [%s]' % pos)
        return pnts

    for i in range(3):
        if human[pos_list[i]][2] <= 0.1:    #置信度过小
            # print('component [%d] incomplete'%(pos_list[i]))
            return pnts

        pnts.append((int( human[pos_list[i]][0]), int( human[pos_list[i]][1])))
    return pnts

# 大腿与躯干的夹角
def angle_thigh_trunk(human):
    trunk = (8,1)
    thigh = (12,13)
    # 计算两个向量之间的夹角
    V1 = (human[trunk[1]][0]-human[trunk[0]][0], human[trunk[1]][1]-human[trunk[0]][1])
    V2 = (human[thigh[1]][0]-human[thigh[0]][0], human[thigh[1]][1]-human[thigh[0]][1])
    d_V1 = math.sqrt(V1[0]**2 + V1[1]**2)
    d_V2 = math.sqrt(V2[0]**2 + V2[1]**2)
    if d_V1 == 0 or d_V2 == 0:
        return -1
    else:
        cos_theta = (V1[0] * V2[0] + V1[1] * V2[1]) / (d_V1 * d_V2)
        theta = math.acos(cos_theta)
        return theta / math.pi * 180.0


def angle_rightElbow_trunk(human):
    pnts = get_angle_point(human, 'right_elbow_trunk')
    if len(pnts) != 3:
        # print('component incomplete')
        return -1

    angle = 0
    if pnts is not None:
        angle = angle_between_points(pnts[0], pnts[1], pnts[2])
        # print('left shoulder angle: %f'%(angle))
    return angle


def angle_left_shoulder(human):
    pnts = get_angle_point(human, 'left_shoulder')
    if len(pnts) != 3:
        # print('component incomplete')
        return -1

    angle = 0
    if pnts is not None:
        angle = angle_between_points(pnts[0], pnts[1], pnts[2])
        # print('left shoulder angle: %f'%(angle))
    return angle

def angle_left_elbow(human):
    pnts = get_angle_point(human, 'left_elbow')
    if len(pnts) != 3:
        # print('component incomplete')
        return

    angle = 0
    if pnts is not None:
        angle = angle_between_points(pnts[0], pnts[1], pnts[2])
        # print('left elbow angle: %f'%(angle))
    return angle

def angle_left_knee(human):
    pnts = get_angle_point(human, 'left_knee')
    if len(pnts) != 3:
        # print('component incomplete')
        return

    angle = 0
    if pnts is not None:
        angle = angle_between_points(pnts[0], pnts[1], pnts[2])
        # print('left knee angle:%f'%(angle))
    return angle

def angle_left_ankle(human):
    pnts = get_angle_point(human, 'left_ankle')
    if len(pnts) != 3:
        # print('component incomplete')
        return

    angle = 0
    if pnts is not None:
        angle = angle_between_points(pnts[0], pnts[1], pnts[2])
        # print('left ankle angle:%f'%(angle))
    return angle

def angle_right_shoulder(human):
    pnts = get_angle_point(human, 'right_shoulder')
    if len(pnts) != 3:
        # print('component incomplete')
        return

    angle = 0
    if pnts is not None:
        angle = angle_between_points(pnts[0], pnts[1], pnts[2])
        # print('right shoulder angle:%f'%(angle))
    return angle

def angle_right_elbow(human):
    pnts = get_angle_point(human, 'right_elbow')
    if len(pnts) != 3:
        # print('component incomplete')
        return

    angle = 0
    if pnts is not None:
        angle = angle_between_points(pnts[0], pnts[1], pnts[2])
        # print('right elbow angle:%f'%(angle))
    return angle

# 获取前臂与水平方向的夹角
def angle_frontElbow_horizon(human):
    front_elbow = (3, 4)
    x1, y1 = human[front_elbow[0]][0], human[front_elbow[0]][1]
    x2, y2 = human[front_elbow[1]][0], human[front_elbow[1]][1]

    # 有不存在的关键点
    if human[front_elbow[0]][2] <= 0.1 or human[front_elbow[0]][2] <= 0.1:
        return -1
    else:
        radian = abs(math.atan2(y2-y1, x2-x1)) if x2-x1 != 0 else math.pi/2
        degree = radian / math.pi * 180.0
        return degree



def angle_right_knee(human):
    pnts = get_angle_point(human, 'right_knee')
    if len(pnts) != 3:
        # print('component incomplete')
        return

    angle = 0
    if pnts is not None:
        angle = angle_between_points(pnts[0], pnts[1], pnts[2])
        # print('right knee angle:%f'%(angle))
    return angle

def angle_right_ankle(human):
    pnts = get_angle_point(human, 'right_ankle')
    if len(pnts) != 3:
        # print('component incomplete')
        return

    angle = 0
    if pnts is not None:
        angle = angle_between_points(pnts[0], pnts[1], pnts[2])
        # print('right ankle angle:%f'%(angle))
    return angle