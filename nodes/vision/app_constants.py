# create the hues for detecting colors in both regular game,
#  and the game mode leds. Look below for inspiration

red = "red"
yellow = "yellow"
blue = "blue"
white = "white"

redBounderies = (red, [50, 60, 180], [90, 80, 240])
yellowBounderies = (yellow, [40, 170, 200], [110, 200, 255])
blueBounderies = (blue, [100, 10, 10], [150, 50, 40])
whiteBounderies = (white, [200, 200, 205], [230, 240, 235])
allBounderies = [whiteBounderies, yellowBounderies,
                 redBounderies,  blueBounderies]

robotWorkZoneGetX = "boundriesX"
robotWorkZoneGetY = "boundriesY"

robotWorkZone = {
    "boundriesX": [3, 612],
    "boundriesY": [41, 225]
}

gameModeZone = {
    "boundriesX": [219, 615],
    "boundriesY": [342, 389]
}
