import numpy as np


def rectify(h):
    h = h.reshape((4, 2))
    h_new = np.zeros((4, 2), dtype=np.float32)
    hnewCompare = sorted(h, key=lambda x: x[1])
    if hnewCompare[0][0] < hnewCompare[1][0]:
        h_new[0] = hnewCompare[0]
        h_new[1] = hnewCompare[1]
    else:
        h_new[0] = hnewCompare[1]
        h_new[1] = hnewCompare[0]

    if hnewCompare[2][0] < hnewCompare[3][0]:
        h_new[3] = hnewCompare[2]
        h_new[2] = hnewCompare[3]
    else:
        h_new[3] = hnewCompare[3]
        h_new[2] = hnewCompare[2]
    return h_new
