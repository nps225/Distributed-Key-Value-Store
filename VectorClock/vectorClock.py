import os

class VectorClock:

    def __init__(self):
        self.view = os.getenv("VIEW").split(",")
        self.clock = [0 for i in range(len(self.view))]

    def updateClock(self, newView):
        oldLen = len(self.view)
        view = newView.split(",")
        os.environ["VIEW"] = newView
        self.view = os.getenv("VIEW").split(",")
        counter = len(view) - oldLen
        print(counter)
        # print(len(view))
        if self.clock != None:
            newClock = []
            for val in self.clock:
                newClock.append(val)
            
            while counter != 0:
                newClock.append(0)
                counter-=1
        else:
            while counter != 0:
                newClock.append(0)
                counter-=1
        
        self.clock = newClock
        
    def getClock(self):
        return self.clock

    def getView(self):
        return self.view


    def incClock(self, i):
        if i < len(self.view):
            self.clock[i]+=1
        else:
            return 'Not allowed'

        



