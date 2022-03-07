from mathtools import round_safe


def evaluate(arguments_json):
    comment = ""
    mistake_count = 0
    if str(arguments_json["data"]["upper"]["hitPosition"]).startswith("后臂"):
        comment += "击球部位靠后，请用1/3处击球;\n"
        mistake_count += 1
    if arguments_json["data"]["upper"]["angleForearmArm"] is not None and arguments_json["data"]["upper"][
        "angleForearmArm"] <= 120:
        comment += "击球时注意不要弯曲手臂;\n"
        mistake_count += 1
    if arguments_json["data"]["upper"]["angleArmTrunk"] is not None and arguments_json["data"]["upper"][
        "angleArmTrunk"] > 100:
        comment += "击球时应保持手臂斜向下;\n"
        mistake_count += 1
    if arguments_json["data"]["lower"]["angleCalfThigh"] is not None and arguments_json["data"]["lower"][
        "angleCalfThigh"] > 160:
        comment += "击球时腿部应适当弯曲发力;\n"
        mistake_count += 1
    if arguments_json["data"]["lower"]["jumpHeight"] is not None and arguments_json["data"]["lower"]["jumpHeight"] > 10:
        comment += "击球时保持身体稳定，不要跳起;\n"
        mistake_count += 1
    # if arguments_json["data"]["ball"]["lastHeight"] is not None \
    #         and arguments_json["data"]["ball"]["lastHeight"] > 300:
    #     comment += "击球过高，请减小发力;\n"
    #     mistake_count += 1

    # arguments_json["data"]["comment"] = comment
    arguments_json["data"]["accuracy"] = round_safe(50 + (50 - mistake_count * 50 / 6), 1)
