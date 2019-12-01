from VectorClock.vectorClock import VectorClock
# key-value store class
class Store:
    dict

    # INIT FUNC
    def __init__(self):
        # first we need to initialize our dictionary
        self.dict = {}
        self.clock = {}
        self.timestamp = {}

    # INSERT
    # returns if it already existed -- server side should handle the errors
    #        technically server should stop errors before it is even placed
    #        in key value store
    # this function should be implemented for updates as well
    def upsertValue(self, key, value):
        # check to see if key exists
        exists = key in self.dict
        # place the value/new value
        self.dict[key] = value
        return exists

    # Grabs the vector clock
    def upsertVC(self, key, clock):
        self.clock[key] = clock
        return clock

    def upsertTime(self, key, stamp):
        self.timestamp[key] = stamp
        return timestamp

    # GET
    # returns a tuple (a,b,c)
    # a = if it exists or not
    #b = value
    # c = return code
    # Error handling
    #a = false
    #b = "Key does not exist"
    #c = 404
    def getValue(self, key):
        exists = key in self.dict
        # if it is present
        if(exists):
            code = 200
            value = self.dict[key]
        else:
            # if it isn't present
            code = 404
            value = "Key does not exist"

        return (exists, value, code)

    # Get the clock value
    def getClock(self, key):
        return self.clock[key]

    def getTime(self, key):
        return self.timestamp[key]
    # DELETE
    # returns a boolean -- true if exists -- false if not
    def deleteValue(self, key):
        exists = key in self.dict
        if(exists):
            self.dict.pop(key)
            return exists
        # if dne -- stop here
        return exists

    # return our kv-store
    def returnStore(self):
        l = []
        for key in self.dict.keys():
            l.append((key, self.dict[key]))
        return l

    def returnClock(self):
        l = []
        for key in self.clock.keys():
            l.append((key, self.clock[key]))
        return l

    def returnTables(self):
        return (self.returnStore(), self.returnClock())

    def returnTablesDict(self):
        return (self.dict, self.clock, self.timestamp)




    def comparison0(self,store,clock, timestamps):
        changeSelf = False
        changeStore = False
        if(self.dict == store): #later make it so you check if the clock is the same as well
            keys = store.keys()
            for i in keys:
                sum1 = sum(self.clock[i])
                sum2 = sum(clock[i])
                if sum1 > sum2:
                    store[i] = self.dict[i]
                    clock[i] = self.getClock(i)
                    timestamps[i] = self.getTime(i)
                    changeStore = True
            
                elif sum1 < sum2:
                    self.dict[i] = store[i]
                    self.upsertVC(i, clock[i])
                    self.upsertTime(i, timestamps[i])
                    changeSelf = True

            return changeSelf, changeStore

        else:#not up to date #we will bring our dictionary up to date
            keys = store.keys()
            for i in keys:
                if(self.dict.get(i) != store.get(i)):
                    if self.dict.get(i) == None:
                        self.dict[i] = store[i]
                        self.upsertVC(i, clock[i])
                        self.upsertTime(i, timestamps[i])
                        changeSelf = True
                        
                    else:
                        store[i] = self.dict[i]
                        clock[i] = self.getClock(i)
                        timestamps[i] = self.getTime(i)
                        changeStore = True

                    
                elif self.dict.get(i) == store.get(i):
                    sum1 = sum(self.clock[i])
                    sum2 = sum(clock[i])
                    if sum1 > sum2:
                        store[i] = self.dict[i]
                        clock[i] = self.getClock(i)
                        timestamps[i] = self.getTime(i)
                        changeStore = True
                
                    elif sum1 < sum2:
                        self.dict[i] = store[i]
                        self.upsertVC(i, clock[i])
                        self.upsertTime(i, timestamps[i])
                        changeSelf = True

            return changeSelf, changeStore

    def comparison(self, store, selfVCObj, storeVCObj, selfAddr, storeAddr):
        selfVC = selfVCObj.getClock()
        storeVC = storeVCObj.getClock()
        changeSelf = False
        changeStore = False
        if(self.dict == store):  # later make it so you check if the clock is the same as well
            keys = store.keys()
            for i in keys:
                selfClock = self.getClock(i)
                storeClock = store.getClock(i)
                sum1 = sum(selfClock)
                sum2 = sum(storeClock)
                if sum1 > sum2:
                    x, val, z = self.getValue(i)
                    t = self.getTime(i)
                    store.upsertValue(i, val)
                    store.upsertVC(selfClock)
                    store.upsertTime(t)
                    # storeVCObj.compClock(selfVCObj)
                    changeStore = True
             
                elif sum1 < sum2:
                    x, val, z = store.getValue(i)
                    t = store.getTime(i)
                    self.upsertValue(i, val)
                    self.upsertVC(selfClock)
                    self.upsertTime(t)
                    changeSelf = True
                    # selfVCObj.compClock(storeVCObj)
                    
                    
                else:
                    selfT = self.getTime(i)
                    storeT = store.getTime(i)
                    if selfT > storeT:
                        x, val, z = self.getValue(i)
                        t = self.getTime(i)
                        store.upsertValue(i, val)
                        store.upsertVC(selfClock)
                        store.upsertTime(t)
                        changeStore = True
                        # storeVCObj.compClock(selfVCObj)
                    elif storeT > selfT:
                        x, val, z = store.getValue(i)
                        t = store.getTime(i)
                        self.upsertValue(i, val)
                        self.upsertVC(selfClock)
                        self.upsertTime(t)
                        changeSelf = True
                        # selfVCObj.compClock(storeVCObj)
                    else:
                        print('all is well aha ha')

                
            if changeSelf == True:
                selfVCObj.compClock(storeVCObj)
            
            if changeStore == True:
                storeVCObj.compClock(selfVCObj)

                    

            return True  # means we are up to date
        else:  # not up to date
            # we will bring our dictionary up to date
            keys = store.keys()
            for i in keys:
                if(self.dict.get(i) != store.get(i)):
                    # update with clock
                    self.dict[i] = store[i]
                elif self.dict.get(i) == store.get(i):
                    selfClock = self.getClock(i)
                    storeClock = store.getClock(i)
                    sum1 = sum(selfClock)
                    sum2 = sum(storeClock)
                    if sum1 > sum2:
                        print('store outdated')
                    elif sum1 < sum2:
                        print('self outdated')
                    else:
                        print('uh oh timestamp time')
            return False
