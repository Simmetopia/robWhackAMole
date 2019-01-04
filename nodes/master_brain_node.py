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
        image = self._take_image()
        
        #vision.FindObjects(image)
        
        self._filter_objects()
        # interpret game mode and select targets
        # convert target cords to robot target cords
        convert()
        # publish targets with target_publisher
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


    def _filter_object(self):
        raise NotImplementedError
    
    def _find_mode(self):
        raise NotImplementedError


if __name__ == '__main__':
    config = ConfigurationLoader("config.json")
    brain = MasterBrainNode(config.game_subscribe(), config.game_publish())
    rospy.loginfo("Brain node is running")
    rospy.spin()
