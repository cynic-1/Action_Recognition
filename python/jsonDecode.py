import codecs

if __name__ == "__main__":
    resultPath = "info\\VID_20220420_110204(1)\\result.json"
    with open(resultPath, "r") as f:
        import json
        dict = json.load(f)

    with open("data.csv", "w") as f:
        for d in dict:
            s = f"{d['data']['upper']['hitPosition']}," \
                f"{d['data']['upper']['hitAngle']}," \
                f"{d['data']['upper']['angleForearmArm']}," \
                f"{d['data']['upper']['angleArmTrunk']}," \
                f"{d['data']['lower']['angleCalfThigh']}," \
                f"{d['data']['lower']['angleThighTrunk']}," \
                f"{d['data']['ball']['lastHeight']}," \
                f"{d['data']['ball']['initialAngle']}," \
                f"{d['data']['ball']['initialVelocity']}\n"
            f.write(s)
