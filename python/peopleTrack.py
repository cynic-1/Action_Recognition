from functools import cmp_to_key

from mathtools import is_part_in_people


# 无关人物过滤算法
# assignable json_dict;
def people_track(json_dict):
    # 如果人数大于3，则把远处的人（鼻子到腿最短）删去
    dist_pair = (0, 14)
    if len(json_dict["people"]) >= 3:
        # 删去不含有上面两个部位对应的单人数据
        # 记住：删除列表中的特定元素或者保留列表中的特定元素需要用filter
        json_dict["people"] = list(filter(lambda people: is_part_in_people(people, dist_pair[0])
                                                         and is_part_in_people(people, dist_pair[0]),
                                          json_dict["people"]))

        # 依照身高判断谁是主人物
        def cmp(people1, people2):
            y1_1 = people1["pose_keypoints_2d"][dist_pair[0] * 3 + 1]
            y1_2 = people1["pose_keypoints_2d"][dist_pair[1] * 3 + 1]
            y2_1 = people2["pose_keypoints_2d"][dist_pair[0] * 3 + 1]
            y2_2 = people2["pose_keypoints_2d"][dist_pair[1] * 3 + 1]
            return abs(y1_2 - y1_1) - abs(y2_2 - y2_1)

        # 降序排序
        json_dict["people"].sort(key=cmp_to_key(cmp), reverse=True)

        # 删除其他的人
        if len(json_dict["people"]) > 2:
            del json_dict["people"][2:]

    def cmp2(people1, people2):
        part_id = 0
        x1 = people1["pose_keypoints_2d"][part_id * 3]
        x2 = people2["pose_keypoints_2d"][part_id * 3]
        return x1 - x2

    # 升序排列
    json_dict["people"].sort(key=cmp_to_key(cmp2))
