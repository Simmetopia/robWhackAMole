from inverse_kinematics import invkin


class ArmMover:
    def __init__(self, joint_mover, dropzone, default_position):
        self.joint_mover = joint_mover
        self.position = default_position
        self.default_position = default_position
        self.go_to_default_position()
        self.dropzone = invkin(dropzone.x, dropzone.y, dropzone.z)

    def go_to_default_position(self):
        self._go_to_position(self.default_position)

    def _go_to_position(self, position):
        initial = invkin(self.position.x, self.position.y, self.default_position.z)
        self.joint_mover.go_to(initial)
        hover_above_target = invkin(position.x, position.y, self.default_position.z)
        self.joint_mover.go_to(hover_above_target)
        hit_target = invkin(position.x, position.y, position.z)
        self.joint_mover.go_to(hit_target)
        self.position = position

    def move_to_and_grab(self, target):
        self._go_to_position(target)
        self.joint_mover.close_gripper()

    def drop_in_dropzone(self):
        self._go_to_position(self.dropzone)
        self.joint_mover.open_gripper()

    def current_position(self):
        return self.position
