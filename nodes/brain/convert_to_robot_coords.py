class ConverterNode:
    def convert(self, objects):
        convertedObj = []
        for obj in objects:
            rob_obj_center = self.convertCenter(obj[1])
            convertedObj.append(rob_obj_center)
        return convertedObj

    def convertCenter(self, single_object):
        xZero = 351
        yZero = 307

        x = xZero - single_object[1]
        y = yZero - single_object[0]

        return [x, y]
