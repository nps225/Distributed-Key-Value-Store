import os
from datetime import datetime

class VectorClock:

    def __init__(self):
        self.view = os.getenv("VIEW").split(",")
        self.clock = [0 for i in range(len(self.view))]
        self.timeStamp = datetime.timestamp(datetime.now())

    def updateClock(self, newView):
        oldLen = len(self.view)
        view = newView.split(",")
        os.environ["VIEW"] = newView
        self.view = os.getenv("VIEW").split(",")
        counter = len(view) - oldLen
        print(counter)
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
        self.timeStamp = datetime.timestamp(datetime.now())
        
    def getClock(self):
        return self.clock

    def getView(self):
        return self.view

    def getTimeStamp(self):
        return self.timeStamp

#for doing a send/recieve
    def incClock(self, i):
        if i < len(self.view):
            self.clock[i]+=1
            self.timeStamp = datetime.timestamp(datetime.now())
        else:
            return 'Not allowed'
#for recieve, self is the recieving node and vClck is the one that did the send!
#if vc is same during gossip, compare the timestamps and set vc as so
    def compClock(self, vClck):
        clock0 = self.getClock()
        clock1 = vClck.getClock()
        if clock1 != clock0:
            for i in range(len(clock0)):
                clock0[i] = max(clock0[i], clock1[i])
        else:
            stamp0 = self.getTimeStamp()
            stamp1 = vClck.getTimeStamp()
            if stamp0 < stamp1:
                clock0 = clock1

        
        self.clock = clock0




    

        



