# key-value store class
import os
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

#    def comparison(self,store,clock):
#       if(self.dict == store): #later make it so you check if the clock is the same as well
#          return True#means we are up to date
#       else:#not up to date
#          #we will bring our dictionary up to date
#          keys = store.keys()
#          for i in keys:
#             if(self.dict.get(i) != store.get(i)):
#                self.dict[i] = store[i]
#          return False
   def comparison(self,store,clock,timestamps):
        if(self.dict == store and self.clock == clock):
            return True
        else:# we do not match so now check every key
            for i in store.keys():
                #all our reference variables
                clockVal = clock.get(i)
                timestamp = timestamps.get(i)
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
                           self.clock[i] = clockVal
                           self.timestamps[i] = timestamp
                     elif(self.dict.get(i) != value):
                           #values are different -> compare vector clocks
                           sum0 = sum(self.clock[i])
                           sum1 = sum(clockVal)
                           #now compare the clock values
                           #do nothing if we have the higher val
                           #else ...
                           if(sum0 < sum1):
                              self.dict[i] = value
                              self.clock[i] = clockVal
                              self.timestamps[i] = timestamp
                           else: # we must be even in our sums so compare the timestamps
                              #do nothing if we have the higher timestamp
                              #else...
                              ts0 = self.timestamps[i]
                              ts1 = timestamps[i]
                              if(ts0 < ts1):
                                 self.dict[i] = value
                                 self.clock[i] = clockVal
                                 self.timestamps[i] = timestamp
                  else:#if the values are equal compare the vector clocks and make sure we have the latest
                     sum0 = sum(self.clock[i])
                     sum1 = sum(clockVal)
                     #now compare the clock values
                     #do nothing if we have the higher val
                     #else ...
                     if(sum0 < sum1):
                           self.dict[i] = value
                           self.clock[i] = clockVal
                           self.timestamps[i] = timestamp
                     else: # we must be even in our sums so compare the timestamps
                           #do nothing if we have the higher timestamp
                           #else...
                           ts0 = self.timestamps[i]
                           ts1 = timestamps[i]
                           if(ts0 < ts1):
                              self.dict[i] = value
                              self.clock[i] = clockVal
                              self.timestamps[i] = timestamp

                        

        
        return self.returnTablesDict()
