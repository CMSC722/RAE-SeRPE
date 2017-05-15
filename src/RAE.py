import traceback
from interpreter import *
# from importlib import import_module
# import os,sys,inspect
import random

METHOD_RANDOM_ORDER = False


def Rae(method_lib, command_lib, state, task_table, task, debug_flag=False): #We'll need to remove 'task' when we're getting an input stream
    '''This is the main method for RAE, which will loop infinitely as it expects to receive tasks/events and refine a set
       of methods into a plan to complete these tasks/events with the Progress and Retry functions.
       task_event is a tuple of the form: (task_name, (arg1, arg2, ...))'''

    print "\n STARTING RAE\n"

    agenda = [] #making agenda a list instead of a set so we can have mutable stacks in the agenda (and don't have to return them from Progress/Retry)

    #Keep rae running indefinitely or add option for shutting down?
    # From Sunandita: Can do this based on the output of getTaskEvents(). RAE stops when its empty?
	#Can't it be given inputs at arbitrary times?
    te_inputs = [task]
    while len(agenda) > 0 or len(te_inputs) > 0:
        #te_inputs = getTasksEvents()

        #Here, we'll get task and event inputs and initialize them in the agenda
        print "\nRunning inputs loop..."
        while len(te_inputs) > 0:
            task_event = te_inputs.pop(0)
            candidates = getCandidates(method_lib, task_event, state, debug_flag)

            if not candidates:
                print "Failure: No methods found that address " + task_event[0] + " with " + str(task_event[1])

            else:
                print "Got candidates: " + str(candidates)
                #From Sunandita: Can try out different ways to choose the method in future instead of just poping the first one
                method = candidates.pop(0)
                tried = list()
                if [(task_event, method, None, tried)] not in agenda:
                    agenda.append([(task_event, method, None, tried)]) #Third element is 'i' normally, but we'll use an Interpreter generator object instead

        #Now we'll progress each stack in the agenda once and only add it back to the agenda if Progress succeeded
        #From Sunandita: We add a stack back only when stack is not empty and Progress has succeeded. Yes?
		#Return None if Progress does not succeed
        temp_agenda = []

        #Print stacks for debugging
        print "\nCurrent stacks in the agenda:\n"
        stack_num = 0
        for stack in agenda:
            instantiation = []
            print "Stack " + str(stack_num) + ":\n["
            for i in range(len(stack)):
                for key, value in stack[i][1][1].iteritems():
                    instantiation.append(str(key) + " = " + str(value['val']))
                print "(" + str(stack[i][0]) + ", (" + str(stack[i][1][0]) + ", {" + str(instantiation) + "}), Interpreter, " + str(stack[i][3]) + ")"
            print "]\n"

        #Progress stacks and only add back to agenda ones that haven't finished
        print "Running Progress loop..."
        for stack in agenda:
            Progress(method_lib, command_lib, task_table, state, stack, debug_flag)

            if stack:
                temp_agenda.append(stack)

        agenda = temp_agenda

    print "\nRAE finished"

def getTasksEvents():
    return [] #Need to get input stream here




def getCandidates(method_lib, task_event, state, debug_flag=False):
    '''returns a list of methods, which are tuples of the form -- (method name,  {arg1:{'v_type':v_type1, 'val':value1}, arg2:{'v_type':v_type2, 'val':value2}, ...})'''
    print "Starting getCandidates for " + task_event[0] + ":"

    candidates = []

    task_name = task_event[0]
    task_instantiation_tup = task_event[1]

    #Extract the relevant methods from the method_lib whose preconditions evaluate to True given the state
    method_names = []
    for method_name in method_lib:
        if method_lib[method_name]["task"]["id"] == task_name:
            method_names.append(method_name)
    if METHOD_RANDOM_ORDER:
        random.shuffle(method_names)

    for method_name in method_names:
        print "Trying method: " + method_name
        print "Trying to instantiate method: " + method_name + " for task: " + task_name
        #Need to try all permutations of variables to instantiate what was not given by the task.
        #Will be considered good method instantiation if precond_func evaluates to true
        method_arguments_list = method_lib[method_name]["parameters"]
        task_arguments_list = method_lib[method_name]["task"]["parameters"]
        if len(task_arguments_list) != len(task_instantiation_tup):
            print "ERROR: Task: " + task_name + " only given " + str(len(task_instantiation_tup)) + \
            " arguments, but expects " + str(len(task_arguments_list)) + " arguments in Method: " + method_name
            return []

        #Create a bunch of lists of what each argument could be
        #WE WILL NEED TO CHANGE THIS PART ONCE WE HAVE OBJECT TYPING IN METHODS
        poss_instantiation_queues = {}
        for argument in method_arguments_list:
            poss_instantiation_queues[argument] = []

            if argument not in task_arguments_list:
                for object_type, object_set in state["objects"].iteritems():
                    for object in object_set:
                        poss_instantiation_queues[argument].append(object)
            else: #argument already instantiated, so can get the one in the task instantiation tuple in the same position
                if debug_flag:
                    print "Task Arguments: " + str(task_arguments_list)
                    print "Task Instantiation: " + str(task_instantiation_tup)

                ndx = task_arguments_list.index(argument)
                poss_instantiation_queues[argument].append(task_instantiation_tup[ndx])

        #Create all permutations by keeping track of an index list that corresponds to the ordering of the arguments
        #in method_arguments_list.
        ndx_list = []
        for key in poss_instantiation_queues:
            ndx_list.append(0)

        #Then try to run the preconditions for each permutation in poss_instantiation_queues
        while ndx_list[0] < len(poss_instantiation_queues[method_arguments_list[0]]):
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

            #Print every tried instantiation if set to debug
            if debug_flag:
                printstr = "Trying instantiation: {"
                for key, value in poss_environment.iteritems():
                    printstr += key + " : " + str(value['val']) + ", "
                print printstr + "}"

            #Evaluate preconditions and store this instantiation in candidates if true
            try:
                precond_func = method_lib[method_name]["preconditions"]["preconditions"]
                if precond_func(state):
                    candidates.append((method_name, poss_environment))

                    printstr = "Success with trying instantiation: {"
                    for key, value in poss_environment.iteritems():
                        printstr += key + " : " + str(value['val']) + ", "
                    print printstr + "}"
            except Exception as e: #precondition function ran into undefined dictionary entries or something
                if debug_flag:
                    print 'Precondition Error: {}'.format(e)
                pass

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


def Progress(method_lib, command_lib, task_table, state, stack, debug_flag=False):
    '''This method will refine the current stack.
       Stack is a bunch of method frames of the form: (task_event, method, Interpreter, tried)
       and method contains it's name and the current instantiation of its arguments: (method name,  {arg1:{'v_type':v_type1, 'val':value1}, arg2:{'v_type':v_type2, 'val':value2}, ...})'''

    print "Progressing stack:"

    top_tup = stack[len(stack) - 1]

    task_event = top_tup[0]
    method = top_tup[1]
    interp = top_tup[2]
    tried = top_tup[3]

    #Instead of using the line pointer 'i,' we'll keep track of the Interpreter object that
    #will lazily yield the branch nodes
    #TODO: from Sam -- you need to pass in ppi.task_table in the appropriate argument slot --
    #TODO: otherwise, the Interpreter won't be able to distinguish task invocations from
    #TODO: state variable reads and similar looking syntactic constructs
    if not interp:
        print "Instantiating Interpreter instance"
        interp = Interpreter(method_lib[method[0]], method[1], state, task_table, command_lib, 'RAE')

    # next_node = interp.next()

    #Try to get the next node from the interpreter, which will be a task or command
    try:
        next_node = interp.next()
        node_type = next_node[0]
        id = next_node[1]
        interp_args = next_node[2]
        args = tuple()

        #Need to process args from interpreter tuple type into useable tuple of action or task args
        for each in interp_args:
            args = args + (each['val'],)

        if node_type == "ACTION": #is command
            print "Performing command: " + str(id)
            command = command_lib[id]
            args = (state,) + args
            succeeded = command(*args)

            if succeeded:
                print "Command succeded"
                stack[len(stack) - 1] = (task_event, method, interp, tried)
                return
            else: #command failed
                print "Command failed"
                Retry(stack, debug_flag, method_lib, state)
                return

        elif node_type == "TASK": #is task
            print "Got task: " + str(id)
            candidates = getCandidates(method_lib, (id, args), state, debug_flag)
            if not candidates:
                Retry(stack, debug_flag, method_lib, state)
            else:
                method_primed = candidates.pop(0)
                tried_primed = set()
                stack.append(('task_event_primed', method_primed, None, tried_primed))
            return

        elif node_type == "FAIL": #Method returned failure
            print "Method failed"
            Retry(stack, debug_flag, method_lib, state)
            return

    except StopIteration: #Should have reached the end of the method if error raised
        print "Finished method: " + str(method[0])
        stack.pop()
        return


    #Should not get here
    print "ERROR: Unexpected node type: " + node_type
    return




def Retry(stack, debug_flag, method_lib, state):
    '''This method will retry other methods that applied to the task. It acts the backtracker'''

    print "Retrying stack: " + str(stack)

    top_tup = stack.pop()

    task_event = top_tup[0]
    method = top_tup[1]
    interp = top_tup[2]
    tried = top_tup[3]

    # sometimes tried is a set
    tried = list(tried)
    tried.append(method)

    candidates = getCandidates(method_lib, task_event, state, debug_flag)

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
            Retry(stack, debug_flag, method_lib, state)
        else:
            print "Failed to accomplish {}".format(task_event)

    return


# Set debug_flag to True when calling RAE if you want to see all the tried instantiations
# EXAMPLE USE:
# import planning_problem
# ppi = planning_problem.PlanningProblem('./../domains/simple_domain2.zip')
# Rae(ppi.method_table, ppi.commands, ppi.domain, ppi.task_table, ('backtrack', ('r1',)))
