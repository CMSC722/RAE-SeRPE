import map
import robot

arena=map.map()
robo=robot.robot('A',arena)
print robo.naivePath('A','F')
robo.move('G')
robo.move('H')
robo.currLoc()

#actionDict example, pass this into RAE when starting it
actionDict = {'move': robo.move, 'search': robo.search}
actionDict['move']('H')
