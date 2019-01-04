# Should be a function that takes input params as a single object
# below is a example of x,y coordinates that should be translated to
# coordinates that the robot can response to.

# This function should find the center of the square.

exampleInput = [[21, 32], [41, 42], [21, 32], [41, 42]]


class ConverterNode:

    def convert(objects):
        convertedObj = []
        
        for obj in objects:
            robCorners = convertSingleObject(obj[1])
            convertedObj.append(obj[0], robCorners)
            
        return convertedObj

    
    def convertSingleObject(singleObject):
        xbr = 100
        ybr = 50
        convertedCorners = []
        
        for so in singleObject:
            x = xbr - so[0]
            y = so[0] - ybr
            convertedCorners.append([x,y])
        
        return convertedCorners
            
    
    def findAngle():
        NotImplementedError

# find a logical return value that takes into account the angle of the block
