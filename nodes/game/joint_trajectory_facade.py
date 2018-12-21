import actionlib
import rospy
from control_msgs.msg import FollowJointTrajectoryAction
from control_msgs.msg import FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint


class JointTrajectoryFacade:
    def __init__(self, server_name):
        self.server_name = server_name

    def get_client(self):
        return actionlib.SimpleActionClient(self.server_name, FollowJointTrajectoryAction)

    def create_trajectory(self, names, positions):
        return JointTrajectory(joint_names=names, points=positions)

    def create_goal(self, trajectory, tolerance):
        return FollowJointTrajectoryGoal(trajectory=trajectory, goal_time_tolerance=tolerance)

    def create_point(self, angles, n_joints, time_from_start):
        return JointTrajectoryPoint(positions=angles, velocities=[0.5] * n_joints, time_from_start=time_from_start)

    def duration(self, duration):
        return rospy.Duration(duration)
