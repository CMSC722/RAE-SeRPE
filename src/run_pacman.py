import planning_problem
import RAE

ppi = planning_problem.PlanningProblem('./../domains/pacman.zip')
RAE.METHOD_RANDOM_ORDER = True
RAE.Rae(ppi.method_table, ppi.commands, ppi.domain, ppi.task_table, ('play-game', ('',)), debug_flag=True)
