from logpy.facts import (Relation, fact)
from unification.variable import var
from logpy.core import (isvar, eq, EarlyGoalError, lany, everyg, lallgreedy, run)

def Rae(method_lib, state):
    '''This is the main method for RAE, which will loop infinitely as it expects to receive tasks/events and refine a set
       of methods into a plan to complete these tasks/events with the Progress and Retry functions.'''

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
'''This method attempts to unify the given task/event with the state and method library and produces a list of 2 item tuples,
   which are all the possible methods and their associated instantiations that are consistent with the model'''
   
    candidates = []
    
    task_name = task_event[0]
    task_instantiation_tup = task_event[1]
    
    relevant_meths = method_lib[task_name][1:]
    task_arg_tup = method_lib[task_name][0]
    
    #Try to unify each relevant method with the state
    for meth in relevant_meths:
    
        meth_name = meth[0]
        meth_arg_tup = meth[1]
        meth_preconds_tup = meth[2]
        
        #Make dictionary of method arguments and their associated logpy vars
        args_to_vars = dict();
        for arg in meth_arg_tup:
            x = var(str(arg))
            args_to_vars[str(arg)] = x
            
        #Split state into arbitrary 'Relation' chunks based on relation name; store in logpy's facts and dict for future lookup
        rel_name_to_relation = dict()
        for relation_name in state:
        
            #Not sure about state representation here
            if relation_name not in rel_name_to_relation:
                rel_name_to_relation[relation_name] = Relation()
                
            for tup in state[relation_name]:
                fact(rel_name_to_relation[relation_name], (relation_name,) + tup)
            
        #Remake preconditions tuple with unification vars and relations from logpy
        goals_tup = tuple()
        for precond in meth_preconds_tup:
            relation_name = precond[0]
            
            if relation_name in rel_name_to_relation:
                relation = rel_name_to_relation[relation_name]
            else:
                print "ERROR: " + relation_name + " in " + meth_name + " preconditions is not in the state!"
                relation = None
                
            inner_inner_tup = (relation_name, )
            
            for variable in precond[1]:
            
                if str(variable) in args_to_vars:
                    inner_inner_tup = inner_inner_tup + (args_to_vars[str(variable)],)
                else:
                    inner_inner_tup = inner_inner_tup + (variable,)
            
            inner_tup = (relation, inner_inner_tup)
            goals_tup = goals_tup + (inner_tup,)
            
        #Create tuples for equals goal tup for partial instantiations -- (eq, (~a, ~b, ~c, ~d), (a, b, c, d))
        #We have a usage error if the instantiation isn't given enough variables, unless we've defined the same task with multiple inputs
        if len(task_instantiation_tup) != len(task_arg_tup):
            print "Possible error: " + task_name + " expected " + len(task_instantiation_tup) + " input arguments, but received " + len(task_arg_tup)
            continue
            
        partials_args1 = ()
        partials_args2 = ()
        for i in range(0, len(task_arg_tup)):
            arg1 = task_arg_tup[i]
            arg2 = task_instantiation_tup[i]
            
            if str(arg1) in args_to_vars:
                partials_args1 = partials_args1 + (args_to_vars[str(arg1)],)
                partials_args2 = partials_args2 + (arg2,)
            else:
                print "ERROR: " + str(arg1) + " appears in " + task_name + " arguments but not " + meth_name + " arguments!"
                
        #Put vars in tuple for logpy run method
        unify_tup = tuple()
        for key in args_to_vars:
            unify_tup = unify_tup + (args_to_vars[key],)
            
        #Run unification
        unifies = run(0, unify_tup, (lallgreedy,) + goals_tup, (eq, partials_args1, partials_args2))
        
        #Consider two different possible instantions for the same method different candidates
        for each_unify in unifies:
            candidates.append((meth_name, each_unify))
            
            
    return candidates




def Progress(stack):
    '''This method will refine the current stack.
       Stack is a bunch of method frames of the form: (task_event, method, 0, tried)
       and method contains it's name and the current instantiation of its arguments: (method_name, (a1, b1, c1, d1))'''

    top_tup = stack.pop()
    pass




def Retry(stack):
    '''This method will retry other methods that applied to the task. It acts the backtracker'''
    pass






#State stored as -- relationship name : [tuples that have this relationship]
state = {
    'dock' : [('d1',), ('d2',)],
    'robot' : [('r1',), ('r2',)],
    'cargo' : [('c1',), ('c2',), ('c3',)],
    'pile' : [('p1',), ('p2',), ('p3',), ('p4',)],
    'loc' : [('r1', 'd1'), ('r2', 'd2'), ('p1', 'd1'), ('p2', 'd1'), ('p3', 'd2'), ('p4', 'd2')],
    'in-pile' : [('c1', 'p1'), ('c2', 'p2'), ('c3', 'p3')],
    'on-robot' : [('r1', 'None'), ('r2', 'None')],
    'adjacent' : [('d1', 'd2')],
    }

#Tasks stored as -- task name : [(arguments), (m1 name, (m1 args), (m1 precond as tups)), (m2 name, (m2 args), (m2 precond as tups)) ...]
method_lib = {
    'get-cargo' : [('r', 'c'), ('m1-get-cargo', ('r', 'c', 'd', 'p'), (('pile', ('p',)), ('dock', ('d',)), ('loc', ('r', 'd')), ('loc', ('p', 'd')), ('in-pile', ('c', 'p')), ('on-robot', ('r', 'None'))))
                   ],
    }
    
task_event = ('get-cargo', ('r1', 'c1'))
    
print "Test Candidates: " + str(getCandidates(method_lib, task_event, state))