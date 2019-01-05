import cv2
import argparse
import numpy as np
import app_constants
import uuid


def findBoxes(image, colorConstants):
    raise NotImplementedError


# should return something like
# returnType = {
#     "red":[[[x,y]]...],
#     "green":[[[x,y]]...],
#     "blue":[[[x,y]]...],
# }
# define the list of boundaries

class Vision:
    debug = False

    def threshold_image(self, image, debug=False):
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

    def contours(self, image, debug=False):
        """
        Extract the contours of the image by first
        converting it to grayscale and
        then call findContours
        """
        imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        im2, contours, hierarchy = cv2.findContours(
            imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return contours, hierarchy

    def get_bricks(self, contours, color):
        """
        For each contour in contours
            approximate the contours such that small variations are removed
            calulate the area of the contour
            if the area is within the desired range we append the box points
            to the bricks.
        """
        bricks = []
        centerBricks = []
        for cnt in contours:
            epsilon = 0.1 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            rect = cv2.minAreaRect(approx)
            area = cv2.contourArea(approx)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            lowerBoundry = 150
            if color == app_constants.white:
                lowerBoundry = 23

            if lowerBoundry < area < 2200:
                M = cv2.moments(cnt)
                cX = int(M["m10"]/M["m00"])
                cY = int(M["m01"]/M["m00"])
                bricks.append(box)
                centerBricks.append([color, (cX, cY)])
        return bricks, centerBricks

    def show_bricks(self, image, bricks, color):
        for b in bricks:
            cv2.drawContours(image, [b], 0, color, 2)

    def findVisionNodes(self, image):

        a = []
        # loop over the boundaries
        for (color, lower, upper) in app_constants.allBounderies:
            upperAsTuple = tuple(upper)
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")
            # find the colors within the specified boundaries and apply
            # the mask
            mask = cv2.inRange(image, lower, upper)
            output = cv2.bitwise_and(image, image, mask=mask)

            # extra shit to detect more things
            single_channel = self.threshold_image(output, self.debug)
            cont, hierarchy = self.contours(single_channel, self.debug)
            briks, centerBricks = self.get_bricks(cont, color)
            # a.append(self.get_bricks(cont))
            a.append(centerBricks)
            # if len(a) == 0:
            # else:
            #     b = np.concatenate([a, briks])
            self.show_bricks(image, briks, upperAsTuple)

            ab = np.hstack([image, output])
            # show the images
            if self.debug:
                cv2.imshow("images", ab)
                cv2.waitKey(0)
        cv2.imwrite(
            'result_'+str(uuid.uuid4())+'.jpg', image)

        flat_list = []
        for sublist in a:
            for item in sublist:
                flat_list.append(item)
        return flat_list

    """
    Initiates the program, and defaultly sets debug to false
    """

    def __init__(self, debug=False):
        self.debug = debug
