################### 
# Course: CMPS128
# Date: Fall 2019
# Assignment: #1
# Author: Elisabeth Oliver
# Email: elaolive@ucsc.edu
###################

import unittest
import subprocess
import requests

PORT=8081
localhost = "localhost" # Docker Toolbox users should use Docker's ip address here

class TestHW1(unittest.TestCase):

  # Make basic GET http request
  def test1(self):
    res = requests.get('http://'+localhost+':'+str(PORT)+'/hello')
    self.assertEqual(res.text, 'Hello, world!', msg='Incorrect response to /hello endpoint')

  # Send a POST request to app with a parameter, and access that parameter in app
  def test2(self):
    res = requests.post('http://'+localhost+':'+str(PORT)+'/check?msg=Hooray!AMessage!123')
    self.assertEqual(res.text, 'POST message received: Hooray!AMessage!123', msg='Incorrect response to POST request to /check endpoint')

  # Check the status codes of hello
  def test4(self):
    res = requests.get('http://'+localhost+':'+str(PORT)+'/hello')
    self.assertEqual(res.status_code, 200, msg='Did not return status 200 to GET request to /hello endpoint')

    res = requests.post('http://'+localhost+':'+str(PORT)+'/hello')
    self.assertEqual(res.status_code, 405, msg='Did not return status 405 to POST request to /hello endpoint')


if __name__ == '__main__':
  unittest.main()
