import numpy as np


def rectify(h):
    h = h.reshape((4, 2))
    hnew = np.zeros((4, 2), dtype=np.float32)
    add = h.sum(1)
    id_top_left = np.argmin(add)
    id_bottom_right = np.argmax(add)
    hnew[0] = h[id_top_left]
    hnew[2] = h[id_bottom_right]

    diff = np.diff(h, axis=1)
    diff[id_top_left] = 999
    diff[id_bottom_right] = 999
    id_top_right = np.argmin(diff)
    hnew[1] = h[id_top_right]

    diff[id_top_left] = -999
    diff[id_bottom_right] = -999
    id_bottom_left = np.argmax(diff)
    hnew[3] = h[id_bottom_left]

    # print("top_left"+str(hnew[0]))
    # print("bottom_right" + str(hnew[2]))
    # print("top_right" + str(hnew[1]))
    # print("bottom_left" + str(hnew[3]))
    return hnew
