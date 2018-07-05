import numpy as np
from numpy import linalg as LA
import cv2
import rect

image = cv2.imread('img/36.jpg')
print(image.shape)
image = cv2.resize(image, (800, 469))
orig = image.copy()

# convert to grayscale and blur to smooth
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# blurred = cv2.medianBlur(gray, 5)

# apply Canny Edge Detection
edged = cv2.Canny(blurred, 0, 50)
orig_edged = edged.copy()

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
im2, contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

# get approximate contour
target = None
for c in contours:
    p = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * p, True)

    if len(approx) == 4:
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
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(realDst, [box], 0, (255, 0, 255), 2)
            w = LA.norm(box[0] - box[1])
            h = LA.norm(box[0] - box[3])
            realW = w * (8.3 / 568)
            realH = h * (11.7 / 800)
            cv2.putText(realDst, \
                        str("{0:.2f}".format(round(realW, 2))) + " x " + str("{0:.2f}".format(round(realH, 2))) + " inches", \
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
