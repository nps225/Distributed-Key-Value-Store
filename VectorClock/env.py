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

v.incClock(1)
v.incClock(2)

print(v.getClock())
os.environ["VIEW"] = newView

v2 = VectorClock()
# print(v2.getClock())
v2.incClock(2)
print(v2.getClock())
v2.compClock(v)
print(v2.getClock())



