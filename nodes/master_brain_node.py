#!/usr/bin/env python

import rospy
from rob_whack_a_mole.msg import Target
from rob_whack_a_mole.msg import Targets
from std_msgs.msg import Empty

from brain.convert_to_robot_coords import convert
from configuration_loader import ConfigurationLoader


class MasterBrainNode:
    def __init__(self, target_topic, request_topic):
        self.target_publisher = rospy.Publisher(target_topic, Targets, queue_size=10)
        rospy.Subscriber(request_topic, Empty, self._get_vision_data)
        rospy.init_node("master_brain")

    def _get_vision_data(self, empty):
        # get objects on table and game mode
        self._take_image()
        self._split_image()
        # interpret game mode and select targets
        # convert target cords to robot target cords
        convert()
        # publish targets with target_publisher
        targets = [Target(2, 3, 1), Target(4, 2, 1)]
        rospy.loginfo("Publishing targets")
        self.target_publisher.publish(targets)

    def _take_image(self):
        raise NotImplementedError

    def _split_image(self):
        raise NotImplementedError


if __name__ == '__main__':
    config = ConfigurationLoader("config.json")
    brain = MasterBrainNode(config.game_subscribe(), config.game_publish())
    rospy.loginfo("Brain node is running")
    rospy.spin()
