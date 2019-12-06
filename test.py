# # import unittest
# # import subprocess
# # import requests

# # PORT=8081
# # class TestHW1(unittest.TestCase):
# #  # from Peter Himself?
# #   # Make some sort of http request
# #   def test1(self):
# #     res = requests.get('http://localhost:'+str(PORT)+'/hello')
# #     self.assertEqual(res.text, 'Hello world!', msg='Incorrect response to /hello endpoint') 

# #   # Send a parameter with request to app, and access that parameter in app
# #   def test2(self):
# #     res = requests.post('http://localhost:'+str(PORT)+'/check?msg=HoorayAMessage123')
# #     self.assertEqual(res.text, 'POST message received: HoorayAMessage123', msg='Incorrect response to POST request to /test endpoint')

# #   # Set the status codes of responses
# #   def test4(self):
# #     res = requests.get('http://localhost:'+str(PORT)+'/hello')
# #     self.assertEqual(res.status_code, 200, msg='Did not return status 200 to GET request to /hello endpoint')

# #     res = requests.post('http://localhost:'+str(PORT)+'/hello')
# #     self.assertEqual(res.status_code, 405, msg='Did not return status 405 to POST request to /hello endpoint')

# #     res = requests.get('http://localhost:'+str(PORT)+'/check')
# #     self.assertEqual(res.status_code, 200, msg='Did not return status 200 to GET request to /test endpoint')   
    
# #     res = requests.post('http://localhost:'+str(PORT)+'/check')
# #     self.assertEqual(res.status_code, 200, msg='Did not return status 200 to POST request to /test endpoint')


# # if __name__ == '__main__':
# #   unittest.main()

# l = 5
# try:
#   for i in l:
#     print(i)
# except TypeError:
#   print("something went wrong")
#   pass

# except:
#   print("syntax error")
#   pass


# print("i am here")

import datetime

clock1 = {
  "node1":2,
  "node3":3,
  "node2":4,
  "ts": datetime.datetime.now()
}

clock2 = {
  "node2":2,
  "node1":3,
  "node3":2,
  "ts": datetime.datetime.now()
}

# print(clock1["ts"] < clock2["ts"])


def compareClocks(clock1, clock2):
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
  if(clock1Win == clock2Win or clock1Win > 0 and clock2Win > 0):
    if(clock1["ts"] > clock2["ts"]):
      return True
    else:
      return False
  elif(clock1Win == 0):
    return True
  else:#clock2Win == 0"
    return False





print(compareClocks(clock1,clock2))