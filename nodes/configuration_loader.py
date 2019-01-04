import json

from game.coordinate import Coordinate


class ConfigurationLoader:
    def __init__(self, filename):
        with open(filename) as f:
            self.config = json.load(f)

    def game_subscribe(self):
        return self._extract_topic("game_subscribe")

    def game_publish(self):
        return self._extract_topic("game_publish")

    def _extract_topic(self, topic):
        return self.config["topics"][topic]

    def dropzone(self):
        return self._extract_position("dropzone")

    def default_position(self):
        return self._extract_position("default")

    def _extract_position(self, position):
        return Coordinate(
            self.config["positions"][position]["x"],
            self.config["positions"][position]["y"],
            self.config["positions"][position]["z"])
