def move(self, state,loc):
    print 'Moved from location: ' + self.location + ' to location : ' + loc
    self.location=loc
    return True

def search(self, state, loc):
    if(self.temp.observeable(self.location,loc)):
        print 'Searched for Location: ' +loc + ' from location : ' + self.location + ' and found it!'
        return True
    else:
        print 'Searched for Location: ' + loc + ' from location : ' + self.location + ' and did not find it!'
        return False

def enter(self, state, door):
    loc=self.temp.doors[door][0]
    print 'Exited Hallway : ' + self.location + ' and Entered Room : ' + loc
    self.location=loc
    return True

def exit(self, state, door):
    loc=self.temp.doors[door][1]
    print 'Exited Room : ' + self.location + ' and Entered Hallway : ' +  loc
    self.location=loc
    return True

def naivePath(self,state,start,goal):
    return min(list(self.naivePathHelper(start, goal)), key=len)
