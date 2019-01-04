import math
import unittest

from nodes.game.arm_mover import ArmMover
from nodes.configuration_loader import ConfigurationLoader
from nodes.game.coordinate import Coordinate
from joint_mover_spy import JointMoverSpy
from nodes.game.target import Target


class TestArmMoverGivenJointMoverSpy(unittest.TestCase):
    def setUp(self):
        self.joint_mover = JointMoverSpy()
        config = ConfigurationLoader("testconfig.json")
        dropzone = config.dropzone()
        self.default_position = config.default_position()
        self.mover = ArmMover(self.joint_mover, dropzone, self.default_position)

    def test_grabbing_test_thing_joint_mover_should_receive_0_0_0_0(self):
        target = Target(Coordinate(80, 40, 0))
        self.mover.move_to_and_grab(target)
        self.joint_mover.received_angles().should_be(
            [(0, -math.pi / 2, 0, 0),
             (0, -math.pi / 2, 0, 0),
             (0, -math.pi / 2, 0, 0),
             (0, -math.pi / 2, 0, 0),
             (0.4636476090008061, 0.5540476301085788, -2.8045416450784777, 0),
             (0.4636476090008061, -1.250882880642002, -2.2087940595772633, 0)]
        )

    def test_grabbing_test_thing_joint_mover_should_close_grabber(self):
        target = Target(Coordinate(80, 40, 0))
        self.mover.move_to_and_grab(target)
        self.joint_mover.received_close().should_be_true()


if __name__ == '__main__':
    unittest.main()