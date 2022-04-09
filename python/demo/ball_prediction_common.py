import json


# 生成一个CSV版本的数据文件，分别以x, y为两个字段
def produceCSVTable(csv_name, x, y, xAxis_name, yAxis_name):
    num = min(len(x), len(y))
    with open(csv_name, "w") as f:
        f.write(f"{xAxis_name},{yAxis_name}\n")
        for i in range(num):
            f.write(f"{x[i]},{y[i]}\n")


# 函数功能：求球的中心点
# 输入参数：ball_path
# 输出参数：volley_position = list[], 表示球的位置的列表
# 访问方式：volley_position[图片下标，从0开始] = [x, y]
# 若对应图片没有检测到球的位置，则volley_position[i] = []
def get_volleyCenter(ball_path):
    with open(ball_path, "r") as f:
        _volley_position = json.load(f)
    volley_position = []
    for i in range(len(_volley_position)):
        if len(_volley_position[i]) == 0:
            volley_position.append([])
        else:
            x1, y1, x2, y2 = _volley_position[i][0]
            volley_position.append([(x1 + x2) / 2, (y1 + y2) / 2])
    return volley_position


# 定义Average对象，实现动态添加数据求平均值
class Average:
    def __init__(self):
        self.__cnt = 0
        self.__total = 0

    # 在数字列表中新增一个数
    def add(self, num):
        self.__cnt += 1
        self.__total += num

    # 计算所添加的所有数的平均值
    def getAverage(self):
        if self.__cnt != 0:
            return self.__total / self.__cnt
        else:
            return 0

    # 清空对象中存储的所有数字
    def clear(self):
        self.__cnt = 0
        self.__total = 0

    # 返回对象中存储的用于求平均值的数的个数是否为0
    def isEmpty(self):
        return self.__cnt == 0


# 深度拷贝层叠的列表结构：类似[[], [], [[], []]]，只含有列表对象
def deepcopy(obj):
    if type(obj) != list:
        return obj
    else:
        res = []
        for item in obj:
            res.append(deepcopy(item))
        return res


def volley_position_to_plot(volley_position, axis=0):
    imageID = []
    positions = []
    for i in range(len(volley_position)):
        if len(volley_position[i]) >= (axis+1):
            imageID.append(i+1)
            positions.append(volley_position[i][axis])
    return imageID, positions
