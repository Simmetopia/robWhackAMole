#!/usr/bin/env python

import rospy
import cv2
import urllib
from rob_whack_a_mole.msg import Target
from rob_whack_a_mole.msg import Targets
from std_msgs.msg import Empty
import numpy as np
from brain.convert_to_robot_coords import convert
from configuration_loader import ConfigurationLoader
from vision import vision


class MasterBrainNode:
    # TODO: Uncomment
    # def __init__(self, target_topic, request_topic):
    #     self.target_publisher = rospy.Publisher(
    #         target_topic, Targets, queue_size=10)
    #     rospy.Subscriber(request_topic, Empty, self._get_vision_data)
    #     rospy.init_node("master_brain")

    boundriesX = [3, 612]
    boundriesY = [41, 389]

    def _get_vision_data(self):
        # get objects on table and game mode
        # image = self._take_image()
        image = cv2.imread("image.jpg")

        # Use vision node to identify all objects
        # interpret game mode and select targets
        self._filter_objects(vision.Vision().findVisionNodes(image))

        # convert target coordinates to robot target coordinates
        convert()

        # publish targets with target_publisher
        # targets may be different than this
        targets = [Target(2, 3, 1), Target(4, 2, 1)]
        rospy.loginfo("Publishing targets")
        self.target_publisher.publish(targets)

    def _take_image(self):
        """
        Fetches an image from the webcam
        """
        print "try fetch from webcam..."
        stream = urllib.urlopen('http://192.168.0.20/image/jpeg.cgi')
        bytes = ''
        bytes += stream.read(64500)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')

        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),
                             cv2.CV_LOAD_IMAGE_COLOR)
            return i
        else:
            print "did not receive image, "
            print "try increasing the buffer size in line 13:"

    def _filter_objects(self, detectedObjects):
        gameMode = 0
        bricks = []
        # import areas from config
        # Find modeObjects (white in area of Game Mode)
        # return wanted colors = _find_mode(gameMode)
        for i in detectedObjects:
            if i[0] == "white":
                self.gameMode += 1
            else:
                if self._cordinateInArea(i[1]):
                    bricks.append(i)
        self._find_mode(gameMode)
        return bricks

    def _isInArea(self, coordinateToCheck, b):
        return coordinateToCheck > b[0] and coordinateToCheck < b[1]

    def _cordinateInArea(self, coord_set):
        xInRange = self._isInArea(coord_set[0], self.boundriesX)
        yInRange = self._isInArea(coord_set[1], self.boundriesY)
        return xInRange and yInRange

    def _find_mode(self, mode):
        if 1:
            # gamemode 1
            return 1
        elif 2:
            # gamemode 2
            return 2
        else:
            # gamemode 3
            return 3

# gamefield = [[6, 389], [612, 385],
#              [3, 46], [610, 41]]


MasterBrainNode()._get_vision_data()
# if __name__ == '__main__':
#     config = ConfigurationLoader("config.json")
#     brain = MasterBrainNode(config.game_subscribe(), config.game_publish())
#     rospy.loginfo("Brain node is running")
#     rospy.spin()
