# create the hues for detecting colors in both regular game,

red = "red"
yellow = "yellow"
blue = "blue"
white = "white"

redBounderies = (red, [44, 61, 171], [119, 112, 200])
yellowBounderies = (yellow, [83, 190, 190], [161, 249, 240])
blueBounderies = (blue, [105, 37, 32], [171, 145, 140])
whiteBounderies = (white, [200, 200, 205], [230, 240, 235])
allBounderies = [whiteBounderies, yellowBounderies,
                 redBounderies,  blueBounderies]

robotWorkZoneGetX = "boundriesX"
robotWorkZoneGetY = "boundriesY"

robotWorkZone = {
    "boundriesX": [3, 612],
    "boundriesY": [41, 270]
}

gameModeZone = {
    "boundriesX": [219, 615],
    "boundriesY": [342, 389]
}
