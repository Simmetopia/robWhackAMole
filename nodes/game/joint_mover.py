import actionlib
import rospy
from control_msgs.msg import FollowJointTrajectoryAction
from control_msgs.msg import FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint


class JointMover:
    N_JOINTS = 4
    NAMES = ["joint1", "joint2", "joint3", "joint4"]

    def __init__(self, server_name, gripper_control):
        self.client = actionlib.SimpleActionClient(server_name, FollowJointTrajectoryAction)
        self.gripper = gripper_control
        self.last_moved_to = (0, 0, 0, 0)

    def sleep(self, duration):
        rospy.sleep(duration)

    def go_to(self, collection_of_angles):
        joint_points = self._create_joint_trajectory_points(collection_of_angles)
        jt = JointTrajectory(joint_names=self.NAMES, points=joint_points)
        tolerance = self.duration + rospy.Duration(2)
        goal = FollowJointTrajectoryGoal(trajectory=jt, goal_time_tolerance=tolerance)
        self._send_goal_and_wait_for_result(goal)

    def _create_joint_trajectory_points(self, collection_of_angles):
        self.duration = rospy.Duration(0)
        points = []
        for angles in collection_of_angles:
            self.duration += self._calculate_difference_between(angles)
            jtp = JointTrajectoryPoint(
                positions=angles, velocities=[0.5] * self.N_JOINTS, time_from_start=self.duration)
            points.append(jtp)
            self.last_moved_to = angles
        return points

    def _calculate_difference_between(self, angles):
        offset = 0.4
        weight = 0.1
        sum_of_differences = sum(abs(x) + abs(y) for x, y in zip(self.last_moved_to, angles))
        sum_of_differences = sum_of_differences if sum_of_differences > 4 else 4
        return rospy.Duration(offset + sum_of_differences * weight)

    def _send_goal_and_wait_for_result(self, goal):
        self.client.wait_for_server()
        self.client.send_goal(goal)
        self.client.wait_for_result()

    def open_gripper(self):
        self.gripper.open()

    def close_gripper(self):
        self.gripper.close()
