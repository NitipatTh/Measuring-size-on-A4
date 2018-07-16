import numpy as np


def rectify(h):
    h = h.reshape((4, 2))
    hnew = np.zeros((4, 2), dtype=np.float32)
    # add = h.sum(1)
    # id_top_left = np.argmin(add)
    # id_bottom_right = np.argmax(add)
    # hnew[0] = h[id_top_left]
    # hnew[2] = h[id_bottom_right]
    #
    # diff = np.diff(h, axis=1)
    # diff[id_top_left] = 999
    # diff[id_bottom_right] = 999
    # id_top_right = np.argmin(diff)
    # hnew[1] = h[id_top_right]
    #
    # diff[id_top_left] = -999
    # diff[id_bottom_right] = -999
    # id_bottom_left = np.argmax(diff)
    # hnew[3] = h[id_bottom_left]
    # print(hnew)
    hnew2 = hnew.copy()
    # print("top_left" + str(hnew[0]))
    # print("bottom_right" + str(hnew[2]))
    # print("top_right" + str(hnew[1]))
    # print("bottom_left" + str(hnew[3]))

    hnewCompare = sorted(h, key=lambda x: x[1])
    if hnewCompare[0][0] < hnewCompare[1][0]:
        # print("top_left" + str(hnewCompare[0]))
        # print("top_right" + str(hnewCompare[1]))
        hnew2[0] = hnewCompare[0]
        hnew2[1] = hnewCompare[1]
    else:
        # print("top_left" + str(hnewCompare[1]))
        # print("top_right" + str(hnewCompare[0]))
        hnew2[0] = hnewCompare[1]
        hnew2[1] = hnewCompare[0]

    if hnewCompare[2][0] < hnewCompare[3][0]:
        # print("bottom_left" + str(hnewCompare[2]))
        # print("bottom_right" + str(hnewCompare[3]))
        hnew2[3] = hnewCompare[2]
        hnew2[2] = hnewCompare[3]
    else:
        # print("bottom_left" + str(hnewCompare[3]))
        # print("bottom_right" + str(hnewCompare[2]))
        hnew2[3] = hnewCompare[3]
        hnew2[2] = hnewCompare[2]
    # print(hnew2)
    return hnew2
