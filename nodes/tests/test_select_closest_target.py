import unittest
import should_be.all

from nodes.game.coordinate import Coordinate
from nodes.game.find_closest import FindClosest
from joint_mover_position_0_0_0_stub import JointMoverPosition000Stub
from nodes.game.target import Target


class TestSelectClosestTarget(unittest.TestCase):
    def setUp(self):
        arm_mover = JointMoverPosition000Stub()
        self.closest = FindClosest(arm_mover)

    def test_selecting_between_three_should_return_closest(self):
        closest = Target(Coordinate(0, 4, 2))
        targets = [Target(Coordinate(5, 2, 2)), Target(Coordinate(12, 22, 7)), closest]
        [self.closest.find(targets)].should_be([closest])


if __name__ == '__main__':
    unittest.main()
