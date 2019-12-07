import os
import datetime

def compareClocksPUT(clock1, clock2):
  clock1Win = 0
  clock2Win = 0
  l = list(set(clock1.keys()) | set(clock2.keys()))
  #take away the timestamp from our list
  l.remove("ts")
  for i in l:
    clock1Val = clock1.get(i)
    clock2Val = clock2.get(i)
    #now check if any values are none
    if(clock1Val == None):
      clock2Win += 1
    elif(clock2Val == None):
      clock1Win += 1
    elif(clock1Val > clock2Val):
      clock1Win += 1
    elif(clock1Val < clock2Val):
      clock2Win += 1
  #now lets figure out which clock should win
  if(clock1Win == clock2Win or (clock1Win > 0 and clock2Win > 0)):
    if(clock1["ts"] > clock2["ts"]):
      return True
    else:
      return False
  elif(clock1Win == 0):
    return False
  else:#clock2Win == 0"
    return True


def updateClock(clock,value):
  address = os.getenv("ADDRESS")
  clock[address] = value
  clock["ts"] = datetime.datetime.now().timestamp()
  return clock


def maxClock(clock1,clock2):
    l = list(set(clock1.keys()) | set(clock2.keys()))
    clock3 = {}
    for val in l:
        clock1Val = clock1.get(val) or 0
        clock2Val = clock2.get(val) or 0
        newVal = max(clock1Val,clock2Val)
        clock3[val] = newVal
    return clock3