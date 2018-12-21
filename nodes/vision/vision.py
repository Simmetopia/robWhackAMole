import cv2
import argparse
import numpy as np


def findBoxes(image, colorConstants):
    raise NotImplementedError


# should return something like
# returnType = {
#     "red":[[[x,y]]...],
#     "green":[[[x,y]]...],
#     "blue":[[[x,y]]...],
# }
# define the list of boundaries


def threshold_image(image, debug=False):
    """
    Thresholds the image within the desired range and 
    then dilates with a 3x3 matrix
    such that small holes are filled. Afterwards the
     'blobs' are closed using a
    combination of dilate and erode
    """
    ret, th1 = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY)
    resdi = cv2.dilate(th1, np.ones((3, 3), np.uint8))
    closing = cv2.morphologyEx(
        resdi, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    return closing


def contours(image, debug=False):
    """
    Extract the contours of the image by first converting it to grayscale and 
    then call findContours
    """
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    im2, contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return contours, hierarchy


def get_bricks(contours):
    """
    For each contour in contours
        approximate the contours such that small variations are removed
        calulate the area of the contour
        if the area is within the desired range we append the box points to the
        bricks.
    """
    bricks = []
    for cnt in contours:
        epsilon = 0.1 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        rect = cv2.minAreaRect(approx)
        area = cv2.contourArea(approx)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # if 20 < area < 380:
        bricks.append(box)
    return bricks


def show_bricks(image, bricks, color):
    for b in bricks:
        cv2.drawContours(image, [b], 0, color, 2)


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to the image")
args = vars(ap.parse_args())

# load the image
image = cv2.imread("leds.jpg")

debug = False

boundaries = [
    ([0, 15, 100], [100, 56, 240]),
    ([40, 175, 220], [60, 240, 255]),
    ([75, 140, 75], [130, 240, 130]),
]

# loop over the boundaries
for (lower, upper) in boundaries:
    upperAsTuple = tuple(upper)
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)

    # extra shit to detect more things
    single_channel = threshold_image(output, debug)
    cont, hierarchy = contours(single_channel, debug)

    show_bricks(image, get_bricks(cont), upperAsTuple)

    a = np.hstack([image, output])
    # show the images
    cv2.imshow("images", a)
    cv2.waitKey(0)
