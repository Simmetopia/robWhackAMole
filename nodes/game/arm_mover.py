from inverse_kinematics import invkin


class ArmMover:
    def __init__(self, joint_mover, dropzone, default_position):
        self.joint_mover = joint_mover
        self.position = default_position
        self.default_position = default_position
        self.go_to_default_position()
        self.dropzone = dropzone

    def go_to_default_position(self):
        self.joint_mover.sleep(2)
        self.joint_mover.open_gripper()
        self.joint_mover.sleep(1)
        self._go_to_position(self.default_position)

    def _go_to_position(self, position):
        initial = invkin(self.position.x, self.position.y, self.default_position.z)
        hover_above_target = invkin(position.x, position.y, self.default_position.z)
        positions = [initial, hover_above_target]
        self.joint_mover.go_to(positions)
        self.joint_mover.sleep(1)
        hit_target = invkin(position.x, position.y, position.z)
        self.joint_mover.go_to([hit_target])
        self.position = position

    def move_to_and_grab(self, target):
        self.joint_mover.open_gripper()
        self._go_to_position(target)
        self.joint_mover.sleep(1)
        self.joint_mover.close_gripper()
        self.joint_mover.sleep(2)

    def drop_in_dropzone(self):
        self._go_to_position(self.dropzone)
        self.joint_mover.sleep(1)
        self.joint_mover.open_gripper()
        self.joint_mover.sleep(2)
        self.dropzone.z += 15

    def current_position(self):
        return self.position
