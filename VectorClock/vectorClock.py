import os
from datetime import datetime
from KeyValueStore.store import Store

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
    def incClock(self, address):
        i = 0
        res = None
        for adr in self.view:
            if adr is address:
                res = i
            else:
                i+=1

            
        if res:
            self.clock[res]+=1
            self.timeStamp = datetime.timestamp(datetime.now())
            return 'Succ'
        else:
            return 'Not allowed'

    def incClockIdx(self, i):
        if i < len(self.view):
            self.clock[i]+=1
            self.timeStamp = datetime.timestamp(datetime.now())
            return 'Succ'
        else:
            return 'Not Allowed'


    #should we change timestamp to new timestamp or newest nodes timestamp?
    def setClockidx(self, i, val):
        if i < len(self.view):
            self.clock[i] = val
            self.timeStamp = datetime.timestamp(datetime.now())
            return 'Succ'
        else:
            return 'Not Allowed'

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

        

        
    # #self being node on the recieving end of gossip, vClck for sending node of gossip, st1 for receiving and st2 for sending
    # def gossipClock(self, vClck, st1, st2):
    #     #1. if store is same as current dict (nuse Nikhils function in store)
    #     #2. iterate through every single key of the reciving node of the gossip
    #         #2a. check if key is in both and then check if vc is the same, if same then continue check
    #         #2b. check if non existent key, add it to our keystore
    #     #3. if it passed through 2 without doing shit, then check timestamps

    #     if st1.comparison 
    #     if clock0 != clock1:
    #         print('yeet')

    #     else:
    #         stamp0 = self.getTimeStamp()
    #         stamp1 = vClck.getTimeStamp()
    #         if stamp0 < stamp1:
    #             clock0 = clock1

        
    #     self.clock = clock0







    

        



