import planning_problem

# None return used as failure representation (?)

def SeRPE(refine_methods, action_templates, state, task):
  candidates = instances(refine_methods, task, state)
  if len(candidates) == 0:
    return None
  # nondeterministic choice currently as DFS
  for m in candidates:
    result = progressToFinish(refine_methods, action_templates, state, task, m)
    if result != None:
      return result
  return None

def instances(refine_methods, task, state):
  # likely identical to RAE's getCandidates method?
  return []

def progressToFinish(refine_methods, action_templates, state, task, m):
  plan = []

  # how much of logic in SeRPE pseudocode is handled by interpreter?
  # TODO: fill in based on interpreter API

planningProblem = planning_problem.PlanningProblem("./parsing/trivial_pp.zip");
print(planningProblem)

SeRPE([], [], None, None)
