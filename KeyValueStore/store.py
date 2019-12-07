# key-value store class
import os
import VectorClock.vectorClock as Clock
class Store:
   dict

   # INIT FUNC
   def __init__(self):
      # first we need to initialize our dictionary
      self.dict = {}
      self.clock = {}
      self.timestamps = {}

   #checkHash to make sure we are in the right shard
   def checkHash(self,key):
      #get latest copy of our view
      view = os.getenv("VIEW").split(",")
      #obtain our nodes address
      address = os.getenv("ADDRESS")
      replication = int(os.getenv("REPL_FACTOR"))#gets the number of replicas that are present
      
      #obtain our shard - we get a check of a new hash everytime by getting the
      # value and the hashing it, then divide by the current view length
      # this should stay the same when we do a get, it doesnt reshard
      # only reshards when we have a viewChange with the modulo
      val_ascii = sum([ord(c) for c in key])
      # shard = (val_ascii).encode().hex() % (len(view))
      #we are going to check
      shard = int((val_ascii) % (len(view)/replication))
      addresses = []
      for i in range(replication):
         addresses.append(view[shard * replication + i].replace("\"",""))
   
      return addresses

   # INSERT
   # returns if it already existed -- server side should handle the errors
   #        technically server should stop errors before it is even placed
   #        in key value store
   # this function should be implemented for updates as well
   def upsertValue(self, key, value,newClock):
      # check to see if key exists
      exists = key in self.dict
      # place the value/new value
      if not exists:
         self.dict[key] = value
         self.clock[key] = newClock
         return exists,newClock
      else: #must exist
         currentClock = self.clock[key]
         e = Clock.compareClocksPUT(currentClock,newClock)
         if e:
            clock3 = Clock.maxClock(currentClock,newClock)
            return 404,clock3
         else:
            self.dict[key] = value
            clock3 = Clock.maxClock(currentClock,newClock)
            return exists,clock3


   # Grabs the vector clock
   def upsertVC(self, key, clock):
      self.clock[key] = clock
      return clock

   def upsertTimestamp(self,key,timestamp):
      self.timestamps[key] = timestamp
      return timestamp

   # GET
   # returns a tuple (a,b,c)
   # a = if it exists or not
   # b = value
   # c = return code
   # Error handling
   # a = false
   # b = "Key does not exist"
   # c = 404
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

   # DELETE
   # returns a boolean -- true if exists -- false if not
   def deleteValue(self, key):
      exists = key in self.dict
      if(exists):
         self.dict.pop(key)
         self.timestamps.pop(key)
         self.clock.pop(key)
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
      return (self.dict, self.clock, self.timestamps)


   def comparison(self,store,clock):
        if(self.dict == store and self.clock == clock):
            return True
        else:# we do not match so now check every key
            for i in store.keys():
                #all our reference variables
               #  clockVal = clock.get(i)
               #  timestamp = timestamps.get(i)
                value = store.get(i)
                ##COMPARISON STARTS HERE
                #first check if the key is supposed to be here or not
                #use this code when we need to reshard
                addresses = self.checkHash(i)
                address = os.getenv("ADDRESS")
                if(address in addresses):
                  #only time we care is if the values are different
                  if((self.dict.get(i) != value)):
                     #check first if the value exists
                     #if not we must add it in
                     if(self.dict.get(i) == None):
                           self.dict[i] = value
                           self.clock[i] = clock.get(i)
                     elif(self.dict.get(i) != value):
                           #values are different -> compare vector clocks
                           clock1 = self.clock.get(i)
                           clock2 = clock.get(i)
                           res = Clock.compareClocksPUT(clock1,clock2)
                           if(not res):#true means new value higher than last so replace
                              self.dict[i] = value
                              clock3 = Clock.maxClock(clock1,clock2)
                              self.clock[i] = clock3
                  else:
                     self.dict[i] = value
                     self.clock[i] = clock.get(i)

                        

        
        return self.returnTablesDict()
