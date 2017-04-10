import map
import robot

arena=map.map()
robo=robot.robot('A',arena)
print robo.naivePath('A','F')
robo.move('G')
robo.move('H')
robo.currLoc()
