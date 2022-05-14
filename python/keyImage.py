def getCatchBallImage(distance2, volley_position, horizontal_dist) -> list[int]:
    lst = distance2[0]
    keyImages = []
    for i in range(len(lst)):
        # 某个点的距离距离胳膊已经足够近
        box = volley_position[lst[i][0]-1][0]
        ball_width = box[2]-box[0]
        imageID = lst[i][0]
        # 横向距离尽量放宽，避免误判
        if lst[i][1] - ball_width < 20 and horizontal_dist[imageID][0] < 4*ball_width:
            keyImages.append(imageID)
    return keyImages
