import copy
from interpreter import *
import planning_problem
import RAE

# None return used as failure representation (?)

def SeRPE(refine_methods, action_templates, state, task):
  print "Beginning SeRPE call..."
  candidates = RAE.getCandidates(refine_methods, task, state, True)
  print "Candidates were:\n"
  print candidates
  if len(candidates) == 0:
    return None
  # nondeterministic choice currently as DFS
  for m in candidates:
    state_copy = copy.deepcopy(state)
    result = progressToFinish(refine_methods, action_templates, state, task, m)
    if result != None:
      return result
    state = state_copy
    print "backtracking!\n"
  return None

def progressToFinish(refine_methods, action_templates, state, task, m):
  print "Progressing to finish..."
  plan = []
  print "Instantiating interpreter"
  interp = Interpreter(refine_methods[m[0]], m[1], state, pp.task_table, pp.commands)
  for (node_type, node_id, node_args) in interp:
    args = tuple()
    for arg in node_args:
      args = args + (arg['val'],)
    if node_type == "ACTION":
      print "Processing command " + str(node_id)
      action = action_templates[node_id]
      args = (state,) + args
      print("\n\nabout to execute \"" + node_id + "\"\n")
      print("state = " + state.__repr__() + "\n\n")
      succeeded = action(*args)
      if succeeded:
        print "Command \"" + node_id + "\" succeeded\n"
        print("state = " + state.__repr__() + "\n\n")
        plan.append(action)
      else:
        print "Command \"" + node_id + "\" failed\n"
        print("state = " + state.__repr__() + "\n\n")
        return None
    elif node_type == "TASK":
      print "Processing task" + str(node_id)
      plan_prime = SeRPE(refine_methods, action_templates, state, (node_id, args))
      if plan_prime != None:
        plan.append(plan_prime)
      else:
        return None
  return plan

pp = planning_problem.PlanningProblem("../domains/simple_domain2.zip")
print pp
result = SeRPE(pp.method_table, pp.action_models, pp.domain, ('backtrack', ('r1',)))
print result
