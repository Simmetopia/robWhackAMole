import math
import unittest
import should_be.all

from nodes.game.inverse_kinematics import invkin


class TestInvKin(unittest.TestCase):
    def test_0_0_565_should_be_0_0_0_0(self):
        invkin(0, 0, 565).should_be([0, 0, 0, 0])

    def test_400_0_165_should_be_0_negativehalfpi_0_0(self):
        invkin(400, 0, 165).should_be([0, -math.pi / 2, 0, 0])


if __name__ == '__main__':
    unittest.main()
