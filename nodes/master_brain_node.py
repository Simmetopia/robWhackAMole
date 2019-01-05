#!/usr/bin/env python
import uuid

import rospy
import cv2
import urllib
from rob_whack_a_mole.msg import Target
from rob_whack_a_mole.msg import Targets
from std_msgs.msg import Empty
import numpy as np
from brain.convert_to_robot_coords import ConverterNode
from configuration_loader import ConfigurationLoader
from vision import vision
from vision import app_constants


class MasterBrainNode:
    def __init__(self, target_topic, request_topic):
        self.target_publisher = rospy.Publisher(target_topic, Targets, queue_size=10)
        rospy.Subscriber(request_topic, Empty, self._get_vision_data)
        rospy.init_node("master_brain")

    def _get_vision_data(self, empty_msg):
        # get objects on table and game mode
        image = self._take_image()
        # image = cv2.imread("image.jpg")

        # Use vision node to identify all objects
        # interpret game mode and select targets
        filteredBricks = self._filter_objects(vision.Vision(False).findVisionNodes(image))

        # convert target coordinates to robot target coordinates
        converted = ConverterNode().convert(filteredBricks)

        targets = []
        for c in converted:
            targets.append(Target(c[0], c[1], 15))
        # publish targets with target_publisher
        rospy.loginfo("Publishing %s targets" % len(targets))
        self.target_publisher.publish(targets)

    def _take_image(self):
        """
        Fetches an image from the webcam
        """
        rospy.loginfo("Trying to fetch from webcam...")
        stream = urllib.urlopen('http://192.168.0.20/image/jpeg.cgi')
        bytes = stream.read(64500)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')

        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            return i
        else:
            rospy.loginfo("Failed to retrieve image!")

    def _filter_objects(self, detectedObjects):
        gameMode = 0
        bricks = []
        # Find modeObjects (white in area of Game Mode)
        rospy.loginfo("Detected %s objects" % len(detectedObjects))
        for i in detectedObjects:
            if i[0] == "white":
                if self._cordinateInArea(i[1], app_constants.gameModeZone):
                    gameMode += 1
            else:
                if self._cordinateInArea(i[1], app_constants.robotWorkZone):
                    bricks.append(i)
        return self._find_mode(gameMode, bricks)

    def _isInArea(self, coordinateToCheck, b):
        return coordinateToCheck > b[0] and coordinateToCheck < b[1]

    def _cordinateInArea(self, coord_set, boundrySet):
        xInRange = self._isInArea(coord_set[0], boundrySet.get(
            app_constants.robotWorkZoneGetX))
        yInRange = self._isInArea(coord_set[1], boundrySet.get(
            app_constants.robotWorkZoneGetY))
        return xInRange and yInRange

    def _find_mode(self, mode, bricks):
        rospy.loginfo("I am in mode %s" % mode)
        bik = []
        if mode == 1:
            bik = filter(lambda x: x[0] == app_constants.red, bricks)
        elif mode == 2:
            bik = filter(lambda x: x[0] == app_constants.red or x[0] == app_constants.yellow, bricks)
        else:
            bik = bricks
        print bik
        return bik


if __name__ == '__main__':
    config = ConfigurationLoader("config.json")
    brain = MasterBrainNode(config.game_subscribe(), config.game_publish())
    rospy.loginfo("Brain node is running")
    rospy.spin()
