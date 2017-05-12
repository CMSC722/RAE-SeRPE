import map
import robot
import sys
sys.path.insert(0,'./../../src')
import planning_problem
from RAE import *
arena=map.map()
robo=robot.robot('A',arena)
ppi = planning_problem.PlanningProblem('test_mot_plan.zip')
rae=Rae(ppi.method_table, ppi.commands, ppi.domain, ppi.task_table, ('move-to-room', ('H',)))




