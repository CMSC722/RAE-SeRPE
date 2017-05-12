import map
import robot
import sys
sys.path.insert(0,'./../../src')
import planning_problem
import RAE
ppi = planning_problem.PlanningProblem('test_mot_plan.zip')
RAE(ppi.method_table, ppi.commands, ppi.domain, ppi.task_table, ('move', ('H',)))

# arena=map.map()
# robo=robot.robot('A',arena)
# print robo.naivePath('A','F')
# robo.move('G')
# robo.move('H')
# robo.currLoc()

#actionDict example, pass this into RAE when starting it
actionDict = {'move': robo.move, 'search': robo.search}
actionDict['move']('H')
