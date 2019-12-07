#!/usr/bin/env python3
import requests
import time
#basic varables


#start off with empyt causal context
c1 = {}
c2 = {}



# #PUT REQUEST
# def simplePUT(port,value,data):
#    url = "http://localhost:"+ str(port) +"/kv-store/keys/" + value
#    temp = temp = (formatResult(requests.put(url, headers={
#                 'Content-Type': 'application/json'}, json=data)))
#    a,b = temp
# #    print(a)
# #    print(b)
#    return a.get("causal-context")

#GET REQUEST
def simpleGET(port,value,data):
   url = "http://localhost:"+ str(port) +"/kv-store/keys/" + value
   temp = temp = (formatResult(requests.get(url, headers={
                'Content-Type': 'application/json'}, json=data)))
   a,b = temp
#    print(a)
#    print(b)
   return a.get("causal-context")

#helper function
def formatResult(result):
    status_code = result.status_code
    result = result.json()

    if result != None:
        jsonKeys = ["message", "replaced", "error", "doesExist", "value", "address", "key-count", "shards","values","vectors","timestamps","VectorClock","Timestamp","View","replicas","id","shard-id","causal-context"]
        result = {k: result[k] for k in jsonKeys if k in result}

    else:
        result = {"status_code": status_code}


    return result, status_code


# ##HERE IS WHERE OUR TESTS WILL GO
# data = {"value":"2","causal-context":c1}
# c1 = simplePUT(13802,"a",data)
# print(c1)
# data = {"value":"1","causal-context":c1}
# c1 = simplePUT(13802,"b",data)
# print(c1)
# data = {"value":"1","causal-context":c1}
# c1 = simplePUT(13802,"a",data)
# print(c1)

data = {"value": "2", "causal-context":{'10.10.0.2:13800': 2, '10.10.0.4:13800': 4, 'ts': 1575705669.341587}}

c1 = simpleGET(13802, "b", data)
print(c1)
