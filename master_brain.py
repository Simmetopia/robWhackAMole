
from convert_to_robot_coords import convert


def takeImage():
    NotImplementedError


def splitImage():
    NotImplementedError


def startNewCycle():
    takeImage()
    splitImage()
    # call some vision things
    # publish on game topic
    convert()
    NotImplementedError
