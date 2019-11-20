#testing hash
from hash import Hash
import os
val =  "\"10.10.0.2:13800\",\"10.10.0.3:13800\",\"10.10.0.4:13800\""
os.environ["VIEW"] = val
os.environ["ADDRESS"] = "10.10.0.3:13800"
#print(os.getenv("VIEW"))

h = Hash()
#print(h.checkHash("a"))
val =  "\"10.10.0.2:13800\",\"10.10.0.3:138\",\"10.10.0.4:13800\""
os.environ["VIEW"] = val
os.environ["ADDRESS"] = "10.10.0.3:138"
address = "\""+ os.environ["ADDRESS"] + "\""
l = h.updateView(val)
l.remove(address)
for i in l:
   print(i)

print(h.getView())