from logpy.facts import (Relation, fact)
from unification.variable import var
from logpy.core import (isvar, eq, EarlyGoalError, lany, everyg, lallgreedy, run)

def Rae(method_lib, state):
    agenda = set()
    
    #Keep rae running indefinitely or add option for shutting down?
    while True: 
        te_inputs = getTasksEvents()
        
        #Here, we'll get task and event inputs and initialize them in the agenda
        while inputs:
            task_event = te_inputs.pop(0)
            candidates = getCandidates(method_lib, task_event, state)
            
            if not candidates:
                print "No methods found that address " + task_event
                
            else:
                method = candidates.pop(0)
                tried = set()
                agenda.add([(task_event, method, 0, tried)]) #Third element is 'i', which we'll ignore for now
        
        #Now we'll progress each stack in the agenda once and only add it back to the agenda if Progress succeeded
        temp_agenda = set()
        
        for stack in agenda:
            stack = Progress(stack)
            
            if stack:
                temp_agenda.add(stack)
                
        agenda = temp_agenda
        
        
def getTasksEvents():
    return [] #Need to get input stream here

    
    
    
def getCandidates(method_lib, task_event, state):
    task_name = task_event[0]
    task_tup = task_event[1]
    
    relevant_meths = method_lib[task_name][1:]
    task_arg_tup = method_lib[task_name][0]
    
    #Try to unify each relevant method with the state
    for meth in relevant_meths:
    
        meth_name = meth[0]
        meth_arg_tup = meth[1]
        meth_preconds = meth[2:]
        
        #set up vars we want unified
        meth_arg_vars = ();
        for each in meth_arg_tup:
            x = var(str(each))
            meth_arg_vars= meth_arg_vars + (x,)
            
        #Split state into arbitrary 'Relation' chunks based on relation
        # KB_dict = dict()
        # for key in state:
            # if key not in KB_dict:
                # KB_dict[key] = Relation()
            # fact(KB_dict[fct[0]], fct)
            
            
    
    return []




def Progress(stack):
    top_tup = stack.pop()
    pass




def Retry(stack):
    pass






#State stored as -- relationship name : [tuples that have this relationship]
state = {
    'dock' : [('d1',), ('d2',)],
    'robot' : [('r1',), ('r2',)],
    'cargo' : [('c1',), ('c2',), ('c3',)],
    'pile' : [('p1',), ('p2',), ('p3',), ('p4',)],
    'loc' : [('r1', 'd1'), ('r2', 'd2'), ('p1', 'd1'), ('p2', 'd1'), ('p3', 'd2'), ('p4', 'd2')],
    'in-pile' : [('c1', 'p1'), ('c2', 'p2'), ('c3', 'p3')],
    'on-robot' : [('r1', None), ('r2', None)],
    'adjacent' : [('d1', 'd2')],
    }

#Tasks stored as -- task name : [(arguments), (m1 name, (m1 args), (m1 precond as tups)), (m2 name, (m2 args), (m2 precond as tups)) ...]
method_lib = {
    'get-cargo' : [('r', 'c'), ('m1-get-cargo', ('r', 'c', 'd', 'p'), (('pile', ('p',)), ('dock', ('d',)), ('loc', ('r', 'd')), ('loc', ('p', 'd')), ('in-pile', ('c', 'p')), ('on-robot', ('r', None))))
                   ],
    }