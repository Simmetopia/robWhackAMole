class JointMoverSpy:
    def __init__(self):
        self.angles = []
        self.closed_gripper = False

    def go_to(self, angles):
        self.angles.append(angles)

    def received_angles(self):
        return self.angles

    def open_gripper(self):
        pass

    def sleep(self, duration):
        pass

    def close_gripper(self):
        self.closed_gripper = True

    def received_close(self):
        return self.closed_gripper
