from vectorClock import VectorClock
import os
val =  "\"10.10.0.2:13800\",\"10.10.0.3:13800\",\"10.10.0.4:13800\",\"10.10.0.5:13800\",\"10.10.0.6:13800\",\"10.10.0.7:13800\""
os.environ["VIEW"] = val
os.environ["ADDRESS"] = "10.10.0.6:13800"
os.environ["REPL_FACTOR"] = "3"

vc = VectorClock()
vc1 = VectorClock()
print(vc.getClock())
vc.incClock()
vc.incClock()
print(vc.getClock())
print(vc1.compClock(vc))
print(vc1.getClock())
