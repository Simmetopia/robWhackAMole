class JointMover:
    N_JOINTS = 4
    NAMES = ["joint1", "joint2", "joint3", "joint4"]

    def __init__(self, joint_trajectory_facade, gripper_control):
        self.joint_trajectory = joint_trajectory_facade
        self.client = joint_trajectory_facade.get_client()
        self.gripper = gripper_control
        self.duration = self.joint_trajectory.duration(1)

    def go_to(self, joint_angles):
        joint_points = self._create_joint_trajectory_points(joint_angles)
        jt = self.joint_trajectory.create_trajectory(self.NAMES, joint_points)
        tolerance = self.duration + self.joint_trajectory.duration(2)
        goal = self.joint_trajectory.create_goal(jt, tolerance)
        self._send_goal_and_wait_for_result(goal)

    def _create_joint_trajectory_points(self, joint_angles):
        self.duration = self.joint_trajectory.duration(1)
        joint_points = []
        for a in joint_angles:
            jtp = self.joint_trajectory.create_point(a, self.N_JOINTS, self.duration)
            joint_points.append(jtp)
            self.duration += self.joint_trajectory.duration(2)
        return joint_points

    def _send_goal_and_wait_for_result(self, goal):
        self.client.wait_for_server()
        print goal
        self.client.send_goal(goal)
        self.client.wait_for_result()
        print self.client.get_result()

    def open_gripper(self):
        self.gripper.open()

    def close_gripper(self):
        self.gripper.close()
