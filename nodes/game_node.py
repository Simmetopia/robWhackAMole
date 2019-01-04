#!/usr/bin/env python
import rospy
from rob_whack_a_mole.msg import Targets
from std_msgs.msg import Empty

from game.coordinate import Coordinate
from game.target import Target
from configuration_loader import ConfigurationLoader
from game.arm_mover import ArmMover
from game.gripper_control import GripperControl
from game.joint_mover import JointMover
from game.find_closest import FindClosest


class GameNode:
    def __init__(self, mover, find_closest,
                 request_target_topic, new_target_topic):
        self.mover = mover
        self.find_closest = find_closest
        self.pub = rospy.Publisher(request_target_topic, Empty, queue_size=10)
        rospy.Subscriber(new_target_topic, Targets, self.grab_and_drop)

    def start(self):
        while True:
            if raw_input("Press enter to request another target\n") == "":
                self._request_new_target()
            else:
                break

    def _request_new_target(self):
        self.pub.publish()

    def grab_and_drop(self, msg):
        if len(msg.targets) == 0:
            self.mover.go_to_default_position()
            return
        target = self._get_target(msg)
        self.mover.move_to_and_grab(target)
        self.mover.drop_in_dropzone()
        self._request_new_target()

    def _get_target(self, msg):
        targets = []
        for msg_target in msg.targets:
            coordinate = Coordinate(msg_target.x, msg_target.y, msg_target.z)
            targets.append(Target(coordinate))
        target = self.find_closest.find(targets)
        rospy.loginfo("Closest target is at [{0}, {1}, {2}]".format(
            target.x, target.y, target.z))  # debugging
        return target


if __name__ == "__main__":
    rospy.init_node("game_node")
    joint_mover = JointMover("/arm_controller/follow_joint_trajectory", GripperControl())
    config = ConfigurationLoader("config.json")
    dropzone = config.dropzone()
    default_position = config.default_position()
    arm_mover = ArmMover(joint_mover, dropzone, default_position)
    node = GameNode(arm_mover, FindClosest(arm_mover),
                    config.game_publish(), config.game_subscribe())
    rospy.loginfo("Game node is running")
    node.start()
