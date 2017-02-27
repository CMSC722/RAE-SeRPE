def Rae(method_lib, facts):
    agenda = set()
    
    #Keep rae running indefinitely or add option for shutting down?
    while True: 
        te_inputs = getTasksEvents()
        
        #Here, we'll get task and event inputs and initialize them in the agenda
        while inputs:
            task_event = te_inputs.pop(0)
            candidates = getCandidates(method_lib, task_event, facts)
            
            if not candidates:
                print "No methods found that address " + task_event
                
            else:
                method = candidates.pop(0) '''Here is where we should decide how to choose candidates'''
                tried = set()
                agenda.add([(task_event, method, 0, tried)]) '''Third element is 'i', which we'll ignore for now'''
        
        #Now we'll progress each stack in the agenda once and only add it back to the agenda if Progress succeeded
        temp_agenda = set()
        
        for stack in agenda:
            stack = Progress(stack)
            
            if stack:
                temp_agenda.add(stack)
                
        agenda = temp_agenda
        
        
def getTasksEvents():
    return [] #Need to get input stream here

    
    
    
def getCandidates(method_lib, task_event, facts):
    return [] #Need to return a list of methods that match task/event and preconditions held in facts (probably by one-direction unifying)




def Progress(stack):
    top_tup = stack.pop()




def Retry(stack):