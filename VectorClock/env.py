import vectorClock as Clock
import os
import datetime
# val =  "\"10.10.0.2:13800\",\"10.10.0.3:13800\",\"10.10.0.4:13800\",\"10.10.0.5:13800\",\"10.10.0.6:13800\",\"10.10.0.7:13800\""
# os.environ["VIEW"] = val
# os.environ["ADDRESS"] = "10.10.0.6:13800"
# os.environ["REPL_FACTOR"] = "3"
# print(datetime.datetime.now().timestamp())
# print(datetime.datetime.now().timestamp())
c1 = {'10.10.0.4:13800': 1, 'ts': datetime.datetime.now().timestamp()}
c2 = {'10.10.0.2:13800': 1, '10.10.0.4:13800': 1, 'ts': datetime.datetime.now().timestamp()}
print(c1)
print(c2)


print(Clock.compareClocksPUT(c1,c2))