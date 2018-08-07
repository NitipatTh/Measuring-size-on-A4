import numpy as np
from numpy import linalg as LA
import cv2
import math
import rect
import colorExtraction
from cv2 import *

# initialize the camera

while True:
    try:
        num = int(input('Input image:'))
        break
    except ValueError:
        print("Not a number")

image = cv2.imread('img/' + str(num) + '.jpg')
image = cv2.resize(image, (800, 469))
orig = image.copy()
cv2.imshow("orig.jpg", orig)
cv2.waitKey(0)
cv2.destroyAllWindows()

# convert to grayscale and blur to smooth
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)

# apply Canny Edge Detection
edged = cv2.Canny(blurred, 0, 50)
edged = cv2.dilate(edged, None, iterations=1)

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
_, contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

# get approximate contour
target = None
for c in contours:
    p = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * p, True)
    # areaContour2 = cv2.contourArea(c)
    if len(approx) == 4 and cv2.contourArea(c)/(800 * 469) > 0.1:
        # print(str(areaContour2))
        target = approx
        print(cv2.contourArea(c))
        print(800*469)
        print(cv2.contourArea(c)/(800 * 469))
        break

# mapping target point
# ts to 800x800 quadrilateral3

# scale A4 is 0.709402 (567.5214x800)
if target is None:
    print("Marker can not be detected")
    blank_image = np.zeros((800, 568, 3), np.uint8)
    cv2.putText(blank_image, "Marker can not be detected", \
                (45, 390), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
    cv2.imshow("output.jpg", blank_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    wA4scale = 568
    approx = rect.rectify(target)
    pts2 = np.float32([[0, 0], [wA4scale, 0], [wA4scale, 800], [0, 800]])
    M = cv2.getPerspectiveTransform(approx, pts2)
    dst = cv2.warpPerspective(orig, M, (wA4scale, 800))

    cv2.drawContours(image, [target], -1, (0, 255, 0), 2)
    realDst = dst.copy()
    dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

    tophatKenel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 40))
    tophat = cv2.morphologyEx(dst, cv2.MORPH_TOPHAT, tophatKenel)

    # using thresholding on warped image to get scanned effect
    minThd = math.floor(8 + np.std(tophat))
    _, th_tophat = cv2.threshold(tophat, minThd, 255, cv2.THRESH_BINARY_INV)
    _, thOtsu = cv2.threshold(dst, 0, 255, cv2.THRESH_OTSU)

    ellipseKenel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    th_final = cv2.bitwise_not(th_tophat) + cv2.bitwise_not(thOtsu)
    imagem = cv2.morphologyEx(th_final, cv2.MORPH_OPEN, ellipseKenel)
    imagem = cv2.erode(imagem, None, iterations=1)

    _, contours, hierarchy = cv2.findContours(imagem, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    check_detect = 0
    idcontour = 0
    for c in contours:
        areaContour = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        areaRect = w * h
        aspectAre = areaRect / (568 * 800)
        if areaContour / areaRect > 0.1 and (
                x != 0 and y != 0 and (x + w - 1) != 567 and (y + h - 1) != 799) and aspectAre > 0.005 \
                and hierarchy[0][idcontour][3] == -1:
            roi = realDst[y:y + h, x:x + w]
            color_set = colorExtraction.clustering(roi)
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            w = LA.norm(box[0] - box[1])
            h = LA.norm(box[0] - box[3])
            realW = w * (21.0 / 568)
            realH = h * (29.7 / 800)

            # Color Extaction
            for k in range(0, len(color_set)):
                colorTmp = roi.copy()
                b, g, r = color_set[k]

                cv2.rectangle(realDst,  (box[2][0] + (30*k)-50, box[2][1] - 55),\
                              (box[2][0] + 30 + (30*k)-50, box[2][1] - 18), \
                              (int(round(b)), int(round(g)), int(round(r))), -1)

            cv2.drawContours(realDst, [box], 0, (255, 0, 255), 2)
            cv2.putText(realDst, \
                        str("{0:.2f}".format(round(realW, 2))) + " x " + str(
                            "{0:.2f}".format(round(realH, 2))) + " cm", \
                        (box[2][0], box[2][1]-5), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 2)
            check_detect = 1
        idcontour = idcontour + 1

    if check_detect == 0:
        cv2.putText(realDst, "Object can not be detected", \
                    (45, 390), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

    cv2.imshow("output.jpg", realDst)

    cv2.imwrite("pic_result.jpg", realDst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
