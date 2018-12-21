import rospy
from std_msgs.msg import Float64


class GripperControl:
    def __init__(self):
        self.gripper_cmd_pub = rospy.Publisher("/gripper/command", Float64, queue_size=10)

    def open(self):
        self.gripper_cmd_pub.publish_found_boxes(2)

    def close(self):
        self.gripper_cmd_pub.publish_found_boxes(0)
