from logpy.facts import (Relation, fact)
from unification.variable import var
from logpy.core import (isvar, eq, EarlyGoalError, lany, everyg, lallgreedy, run)
from interpreter import *
# from importlib import import_module
# import os,sys,inspect

def Rae(method_lib, command_lib, state, task): #We'll need to remove 'task' when we're getting an input stream
    '''This is the main method for RAE, which will loop infinitely as it expects to receive tasks/events and refine a set
       of methods into a plan to complete these tasks/events with the Progress and Retry functions.
       task_event is a tuple of the form: (task_name, (arg1, arg2, ...))'''

    agenda = set()
    
    #Keep rae running indefinitely or add option for shutting down?
    # From Sunandita: Can do this based on the output of getTaskEvents(). RAE stops when its empty?
	#Can't it be given inputs at arbitrary times?
    te_inputs = [task]
    while True: 
        #te_inputs = getTasksEvents()
        
        agenda = set()
        
        #Here, we'll get task and event inputs and initialize them in the agenda
        while len(te_inputs) > 0:
            task_event = te_inputs.pop(0)
            candidates = getCandidates(method_lib, task_event, state)
            
            if not candidates:
                print "Failure: No methods found that address " + task_event[0] + " with " + str(task_event[1])
                
            else:
                #From Sunandita: Can try out different ways to choose the method in future instead of just poping the first one
                method = candidates.pop(0)
                tried = set()
                agenda.add([(task_event, method, None, tried)]) #Third element is 'i' normally, but we'll use an Interpreter generator object instead
        
        #Now we'll progress each stack in the agenda once and only add it back to the agenda if Progress succeeded
        #From Sunandita: We add a stack back only when stack is not empty and Progress has succeeded. Yes? 
		#Return None if Progress does not succeed
        temp_agenda = set()
        
        for stack in agenda:
            Progress(method_lib, command_lib, state, stack)
            
            if stack:
                temp_agenda.add(stack)
                
        agenda = temp_agenda
        
        
def getTasksEvents():
    return [] #Need to get input stream here

    
    
    
def getCandidates(method_lib, task_event, state):
    '''returns a list of methods, which are tuples of the form -- (method name,  {arg1:{'v_type':v_type1, 'val':value1}, arg2:{'v_type':v_type2, 'val':value2}, ...})'''

    candidates = []
    
    task_name = task_event[0]
    task_instantiation_tup = task_event[1]
    
    #Extract the relevant methods from the method_lib whose preconditions evaluate to True given the state
    for method_name in method_lib:
        print "Trying to instantiate method: " + method_name + " for task: " + task_name
        if method_lib[method_name]["task"]["id"] == task_name:
        
            #Need to try all permutations of variables to instantiate what was not given by the task.
            #Will be considered good method instantiation if precond_func evaluates to true
            method_arguments_list = method_lib[method_name]["parameters"]
            task_arguments_list = method_lib[method_name]["task"]["parameters"]
            
            #Create a bunch of lists of what each argument could be 
            #WE WILL NEED TO CHANGE THIS PART ONCE WE HAVE OBJECT TYPING IN METHODS
            poss_instantiation_queues = {}
            for argument in method_arguments_list:
                poss_instantiation_queues[argument] = []
                
                if argument not in task_arguments_list:
                    for object_type in state["objects"]:
                        for object in object_type:
                            poss_instantiation_queues[argument].append(object)
                else: #argument already instantiated, so can get the one in the task instantiation tuple in the same position
                    ndx = method_arguments_list.index(argument)
                    poss_instantiation_queues[argument].append(task_instantiation_tup[ndx])
                    
            #Create all permutations by keeping track of an index list that corresponds to the ordering of the arguments
            #in method_arguments_list. 
            ndx_list = []
            for key in poss_instantiation_queues:
                ndx_list.append(0)
                
            #Then try to run the preconditions for each permutation in poss_instantiation_queues
            while ndx_list[0] < len(method_arguments_list[0]):
                ndx_loc = 0
                meth_environment_dict = method_lib[method_name]["preconditions"]
                poss_environment = {}
                for argument in method_arguments_list:
                    poss_value = poss_instantiation_queues[argument][ndx_list[ndx_loc]]
                    ndx_loc += 1
                    
                    #Add argument:poss_value to meth_environment_dict
                    #We need to undo this later to not update our method library!
                    meth_environment_dict[argument] = poss_value
                    
                    #And also add it to environment dictionary that will be kept if preconditions evaluates to true
                    v_type = 'val_none'
                    if isinstance(poss_value, str):
                        v_type = 'val_str'
                    elif isinstance(poss_value, (int, float, long)):
                        v_type = 'val_num'
                    elif isinstance(poss_value, bool):
                        v_type = 'val_bool'
                    poss_environment[argument] = {'v_type':v_type, 'val':poss_value}
                  
                print meth_environment_dict
                #Evaluate preconditions and store this instantiation in candidates if true
                precond_func = method_lib[method_name]["preconditions"]["preconditions"]
                if precond_func(state):
                    candidates.append(method_name, poss_environment)
                
                
                #We need to undo the changes to teh meth_environment_dict so we can use different instantiations later
                for argument in method_arguments_list:
                    del meth_environment_dict[argument]
                
                #We're going to increment the index at the end of ndx_list by one and propogate this change toward the start
                #of the list so we go through every possible permutation
                rvrs_ndx = len(ndx_list) - 1
                ndx_list[rvrs_ndx] += 1
                while rvrs_ndx > 0 and ndx_list[rvrs_ndx] >= len(poss_instantiation_queues[method_arguments_list[rvrs_ndx]]):
                    ndx_list[rvrs_ndx] = 0
                    rvrs_ndx -= 1
                    ndx_list[rvrs_ndx] += 1
                
    return candidates
            

def Progress(method_lib, command_lib, state, stack):
    '''This method will refine the current stack.
       Stack is a bunch of method frames of the form: (task_event, method, Interpreter, tried)
       and method contains it's name and the current instantiation of its arguments: (method name,  {arg1:{'v_type':v_type1, 'val':value1}, arg2:{'v_type':v_type2, 'val':value2}, ...})'''

    top_tup = stack[len(stack) - 1]
    
    task_event = top_tup[0]
    method = top_tup[1]
    interp = top_tup[2]
    tried = top_tup[3]
    
    #We're going to run the entire method for now instead of using the line pointer 'i'
	#We'll keep track of the Interpreter object that will lazily yield the branch nodes
    if not interp:
        interp = Interpreter(method_lib[method[0]], method[1], state) #This needs to be given the correct inputs when that's sorted
    
    #Try to get the next node from the interpreter, which will be a task or command
    try:
        next_node = interp.next()
        node_type = next_node[0]
        id = next_node[1]
        args = next_node[2]
        
        if node_type == "action": #is command
            command = command_lib[id]
            succeeded = command(*args)
            
            if succeeded:
                stack[len(stack) - 1] = (task_event, method, interp, tried)
                return
            else: #command failed
                Retry(stack)
                return
                
        elif node_type == "task": #is task
            candidates = getCandidates(method_lib, (id, args), state)
            if not candidates:
                Retry(stack)
            else:
                method_primed = candidates.pop(0)
                tried_primed = set()
                stack.append(('task_event_primed', method_primed, None, tried_primed))
            return
        
    except: #Should have reached the end of the method if error raised
        stack.pop()
        return
	
	
    #Should not get here
    print "ERROR: Unexpected node type: " + node_type
    return




def Retry(stack):
    '''This method will retry other methods that applied to the task. It acts the backtracker'''
    top_tup = stack.pop()
    
    task_event = top_tup[0]
    method = top_tup[1]
    interp = top_tup[2]
    tried = top_tup[3]
	
    tried.add(method)
	
    candidates = getCandidates(method_lib, task_event, state)
	
    #Can again choose better way to decide candidate here
    choice = None
    while candidates and not choice:
        choice = candidates.pop(0)
        if choice in tried:
            choice = None
	
    #Put this new method on the stack to be tried
    if choice:
        stack.append((task_event, choice, None, tried))
	
    #Retry underlying task if this one completely failed. If no stack left, let it disappear from agenda
    else:
        if stack:
            Retry(stack)
        else:
            print "Failed to accomplish " + task_event
            
    return






# #State stored as -- relationship name : [tuples that have this relationship]
# state = {
    # 'dock' : [('d1',), ('d2',)],
    # 'robot' : [('r1',), ('r2',)],
    # 'cargo' : [('c1',), ('c2',), ('c3',)],
    # 'pile' : [('p1',), ('p2',), ('p3',), ('p4',)],
    # 'loc' : [('r1', 'd1'), ('r2', 'd2'), ('p1', 'd1'), ('p2', 'd1'), ('p3', 'd2'), ('p4', 'd2')],
    # 'in-pile' : [('c1', 'p1'), ('c2', 'p2'), ('c3', 'p3')],
    # 'on-robot' : [('r1', 'None'), ('r2', 'None')],
    # 'adjacent' : [('d1', 'd2')],
    # }

# #Tasks stored as -- task name : [(arguments), (m1 name, (m1 args), (m1 precond as tups)), (m2 name, (m2 args), (m2 precond as tups)) ...]
# method_lib = {
    # 'get-cargo' : [('r', 'c'), ('m1-get-cargo', ('r', 'c', 'd', 'p'), (('pile', ('p',)), ('dock', ('d',)), ('loc', ('r', 'd')), ('loc', ('p', 'd')), ('in-pile', ('c', 'p')), ('on-robot', ('r', 'None'))))
                   # ],
    # }
    
# task_event = ('get-cargo', ('r1', 'c1'))
    
# print "Test Candidates: " + str(getCandidates(method_lib, task_event, state))


# #Example of importing and using actions here:
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0,parentdir) 

# file_path = 'domains.simple_domain'
# a_mod = import_module('.actions', file_path)

# #bool = a_mod.actionDict['pickupCargo']({}, None, None, None)

import planning_problem
ppi = planning_problem.PlanningProblem('./parsing/trivial_pp.zip')
Rae(ppi.method_table, ppi.commands, ppi.domain, ('t_start', (3,)))