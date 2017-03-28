import meth_parser
import pprint

# Q about SeRPE and DFS: should first valid solution be used? Current use of DFS tends toward this

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

# Later to be python script parameters instead of hardcoded
table = meth_parser.load_methods("../domains/test_domain1/test_domain1.meth")
#table = meth_parser.load_methods("../domains/simple_domain/simple_domain.meth")
pp = pprint.PrettyPrinter()
pp.pprint(table)

SeRPE([], [], None, None)
