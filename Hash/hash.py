import os
class Hash:
   #this will include our hashing algorithm as well as returning the port to forward to
   #Hashing Algorithm
   # (ascii value) % n (where n is the number of computers)
   def __init__(self):
      self.count = 0
      self.shard_id = str(int((os.getenv("VIEW").replace("\"","").split(",").index(os.getenv("ADDRESS")))/int(os.getenv("REPL_FACTOR"))))
   
   # check the hash if its in use
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
   
   def getShard(self):
     f = int(self.shard_id)
     rep = int(os.getenv("REPL_FACTOR"))
     index = f * rep
     shard = os.getenv("VIEW").replace("\"","").split(",")[index:index+rep]
     return shard

      

   # increasing the count of shards/the items that go into the nodes
   def incCount(self):
      self.count += 1
      return self.count

   # decreasing the count of shards/the items that go into the nodes
   def decCount(self):
      self.count -= 1
      return self.count

   # gets the count of shards/the items that go into the nodes
   def getCount(self):
      return self.count

   # get the latest copy of our view 
   def getView(self):
      return os.getenv("VIEW").split(",")

   #get address key is in
   def getSelfAddress(self):
      return os.getenv("ADDRESS")

   # change the view
   def updateView(self,updateView):
      # gets the view that the user inputted in the user
      # assume the views are not wrong and durable from the user
      os.environ["VIEW"] = updateView
      return os.environ["VIEW"].split(",")