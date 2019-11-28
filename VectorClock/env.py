from vectorClock import VectorClock

import os

val =  "\"10.10.0.2:13800\",\"10.10.0.3:13800\",\"10.10.0.4:13800\""
os.environ["VIEW"] = val
newView = "\"10.10.0.2:13800\",\"10.10.0.3:13800\",\"10.10.0.4:13800\",\"10.10.0.5:13800\""
v = VectorClock()

print('first view getter')
print(os.getenv("VIEW"))

v.updateClock(newView)

print(v.getClock())
print(v.getView())

v.incSelfClock(2)

print(v.getClock())



