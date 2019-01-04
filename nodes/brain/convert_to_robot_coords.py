# Should be a function that takes input params as a single object
# below is a example of x,y coordinates that should be translated to
# coordinates that the robot can response to.




class ConverterNode:

    def convert(objects):
        convertedObj = []
        
        for obj in objects:
            robObjCenter = convertCenter(obj[1])
            convertedObj.append(obj[0], robCenter)
            
        return convertedObj

    
    def convertCenter(singleObject):
        #robot (0,0) = image (307,369) - OBS robot x-axis = image y-axis
        xZero = 369 
        yZero = 307

        x = xZero - singleObject[1] 
        y = yZero - singleObject[0]
        
        return [x,y]
            
    
    def findAngle():
        NotImplementedError


