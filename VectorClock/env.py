import vectorClock as Clock
import os
import datetime
# val =  "\"10.10.0.2:13800\",\"10.10.0.3:13800\",\"10.10.0.4:13800\",\"10.10.0.5:13800\",\"10.10.0.6:13800\",\"10.10.0.7:13800\""
# os.environ["VIEW"] = val
# os.environ["ADDRESS"] = "10.10.0.6:13800"
# os.environ["REPL_FACTOR"] = "3"
# print(datetime.datetime.now().timestamp())
# print(datetime.datetime.now().timestamp())
c1 = {'10.10.0.4:13800': 2, 'ts': 1575707999.138035}
c2 = {'10.10.0.2:13800': 1, 'ts': 1.168481}
c3 = {'10.10.0.2:13800': 1, 'ts': 1000000000000 }
print(c1)
print(c2)

# print(Clock.compareClocksPUT(c1,c2))
# print(Clock.maxClock(c1,c2))
print(Clock.compareClocksGET(c1,c3,"value"))