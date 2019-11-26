#key-value store class
class Store:
   dict

   #INIT FUNC
   def __init__(self):
      #first we need to initialize our dictionary
      self.dict = {}
      self.clock = {}


   #INSERT
   #returns if it already existed -- server side should handle the errors
   #        technically server should stop errors before it is even placed 
   #        in key value store
   #this function should be implemented for updates as well
   def upsertValue(self,key,value):
      #check to see if key exists
      exists = key in self.dict
      #place the value/new value
      self.dict[key] = value
      return exists
   
   #Grabs the vector clock
   def upsertVC(self,key,clock):
      self.clock[key] = clock
      return clock
   
   
   #GET
   #returns a tuple (a,b,c)
   #a = if it exists or not
   #b = value
   #c = return code
   #Error handling
   #a = false
   #b = "Key does not exist"
   #c = 404
   def getValue(self,key):
      exists = key in self.dict
      #if it is present
      if(exists):
         code = 200
         value = self.dict[key]
      else:
         #if it isn't present
         code = 404
         value = "Key does not exist"
      
      return (exists,value,code)
   
   #Get the clock value
   def getClock(self,key):
      return self.clock[key]

   #DELETE
   #returns a boolean -- true if exists -- false if not
   def deleteValue(self,key):
      exists = key in self.dict
      if(exists):
         self.dict.pop(key)
         return exists
      #if dne -- stop here
      return exists

   #return our kv-store
   def returnStore(self):
      l = []
      for key in self.dict.keys():
         l.append((key,self.dict[key]))
      return l

   def returnClock(self):
     l = []
     for key in self.clock.keys():
        l.append((key,self.clock[key]))
     return l 


   def returnTables(self):
      return (self.returnStore(),self.returnClock())
