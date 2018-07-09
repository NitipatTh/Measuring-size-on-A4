import numpy as np
from numpy import linalg as LA
import cv2
import rect
from cv2 import *

# initialize the camera

# cam = cv2.VideoCapture(0)  # 0 -> index of camera
# while(True):
#     # Capture frame-by-frame
#     s, img = cam.read()
#     cv2.imshow('frame', img)
#     if cv2.waitKey(1) & 0xFF == ord(' '):
#         imwrite("filename.jpg", img)
#         break
# # s, img = cam.read()
# # if s:  # frame captured without any errorss
# #     namedWindow("cam-test", True)
# #     imshow("cam-test", img)
# #     waitKey(0)
# #     destroyWindow("cam-test")
# #     imwrite("filename.jpg", img)  # save image
#
# cam.release()
# cv2.destroyAllWindows()

while True:
    try:
        num = int(input('Input image:'))
        break
    except ValueError:
        print("Not a number")

image = cv2.imread('img/' + str(num) + '.jpg')
# image = cv2.imread('filename.jpg')
# print(image.shape)
image = cv2.resize(image, (800, 469))
orig = image.copy()
cv2.imshow("orig.jpg", orig)
cv2.waitKey(0)
cv2.destroyAllWindows()

# convert to grayscale and blur to smooth
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# blurred = cv2.medianBlur(gray, 5)

# apply Canny Edge Detection
edged = cv2.Canny(blurred, 0, 50)
orig_edged = edged.copy()
edged = cv2.dilate(edged, None, iterations=1)
cv2.imshow("edge.jpg", edged)

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
im2, contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

# get approximate contour
target = None
for c in contours:
    p = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * p, True)
    # areaContour2 = cv2.contourArea(c)
    if len(approx) == 4:
        # print(str(areaContour2))
        target = approx
        break

# mapping target points to 800x800 quadrilateral
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

    # using thresholding on warped image to get scanned effect (If Required)
    ret2, th4 = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    cv2.imshow("Outline.jpg", image)
    # cv2.imshow("Otsu's.jpg", th4)
    # cv2.imshow("dst.jpg", dst)

    edged = th4.copy()
    ellipseKenel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (45, 45))
    th5 = cv2.morphologyEx(edged, cv2.MORPH_OPEN, ellipseKenel)
    imagem = cv2.bitwise_not(th5)
    # cv2.imshow("detect.jpg", imagem)

    im2, contours, hierarchy = cv2.findContours(imagem, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    check_detect = 0
    for c in contours:
        areaContour = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        areaRect = w * h
        aspectAre = areaRect / (568 * 800)
        if areaContour / areaRect > 0.1 and (
                x != 0 and y != 0 and (x + w - 1) != 567 and (y + h - 1) != 799) and aspectAre > 0.0001:
            roi = realDst[y:y + h, x:x + w]
            b, g, r, _ = np.uint8(cv2.mean(roi))
            # cv2.imshow("roi.jpg", roi)
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(realDst, [box], 0, (255, 0, 255), 2)
            w = LA.norm(box[0] - box[1])
            h = LA.norm(box[0] - box[3])
            realW = w * (8.3 / 568)
            realH = h * (11.7 / 800)
            cv2.rectangle(realDst, (box[2][0], box[2][1] - 55), (box[2][0] + 40, box[2][1] - 18),
                          (int(b), int(g), int(r)), -1)
            cv2.rectangle(realDst, (box[2][0] - 2, box[2][1] - 57), (box[2][0] + 42, box[2][1] - 17), (0, 0, 0), 2)
            cv2.putText(realDst, \
                        str("{0:.2f}".format(round(realW, 2))) + " x " + str(
                            "{0:.2f}".format(round(realH, 2))) + " inches", \
                        (box[2][0], box[2][1]), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 2)
            check_detect = 1

    if check_detect == 0:
        cv2.putText(realDst, "Marker can not be detected", \
                    (45, 390), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

    cv2.imshow("output.jpg", realDst)

    M_new = cv2.getPerspectiveTransform(pts2, approx)
    dst2 = cv2.warpPerspective(realDst, M_new, (800, 469))
    cv2.imshow("test.jpg", dst2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
