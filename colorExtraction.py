import numpy as np
from numpy import linalg as LA
from cv2 import *


def clustering(obj):
    height, width, _ = obj.shape
    class_color = 0

    color_set = list()
    for i in range(0, 20):
        for j in range(0, 20):
            roi = obj[0 + (round(height * 0.05) * i):(round(height * 0.05) + (round(height * 0.05) * i)) \
                , 0 + (round(width * 0.05) * j):(round(width * 0.05)) + (round(width * 0.05) * j)]
            b, g, r, _ = np.uint8(cv2.mean(roi))
            if class_color == 0:
                color_set.append([b, g, r])
                class_color = class_color + 1
                continue
            check_class = 0
            for k in range(0, len(color_set)):
                norm_color = LA.norm(np.asarray(color_set[k]) - [int(b), int(g), int(r)])
                if norm_color < 50:
                    tmp = (np.asarray(color_set[k]) + [int(b), int(g), int(r)]) / 2
                    color_set[k] = list(tmp)
                    check_class = 1
                    break

            if check_class == 0:
                color_set.append([b, g, r])

    return color_set
