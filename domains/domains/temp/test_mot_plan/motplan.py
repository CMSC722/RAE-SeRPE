import map
import robot
import sys
sys.path.insert(0,'./../../src')
import planning_problem
from RAE import *
arena=map.map()
robo=robot.robot('A',arena)
ppi = planning_problem.PlanningProblem('Archive.zip')
rae=Rae(ppi.method_table, ppi.commands, ppi.domain, ppi.task_table, ('move-to-room', ('r1','A','H')), debug_flag=True)

# arena=map.map()
# robo=robot.robot('A',arena)
# print robo.naivePath('A','F')
# robo.move('G')
# robo.move('H')
# robo.currLoc()

# robo.move('G')
# robo.enter('Door A')