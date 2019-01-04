import math


class FindClosest:
    def __init__(self, arm_mover):
        self.arm_mover = arm_mover

    def find(self, targets):
        position = self.arm_mover.current_position()
        closest = targets[0], self._distance_between(targets[0], position)
        for target in targets:
            distance_to_target = self._distance_between(target, position)
            if distance_to_target < closest[1]:
                closest = target, distance_to_target
        return closest[0]

    def _distance_between(self, p1, p2):
        x_diff = math.pow(p1.x - p2.x, 2)
        y_diff = math.pow(p1.y - p2.y, 2)
        z_diff = math.pow(p1.z - p2.z, 2)
        return math.sqrt(x_diff + y_diff + z_diff)
