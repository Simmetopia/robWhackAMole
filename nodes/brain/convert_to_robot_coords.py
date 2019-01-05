# Should be a function that takes input params as a single object
# below is a example of x,y coordinates that should be translated to
# coordinates that the robot can response to.


class ConverterNode:
    def convert(self, objects):
        convertedObj = []
        for obj in objects:
            rob_obj_center = self.convertCenter(obj[1])
            convertedObj.append(rob_obj_center)
        return convertedObj

    def convertCenter(self, single_object):
        # robot (0,0) = image (307,369) - OBS robot x-axis = image y-axis
        xZero = 351
        yZero = 308

        x = xZero - single_object[1]
        y = yZero - single_object[0]

        return [x, y]
