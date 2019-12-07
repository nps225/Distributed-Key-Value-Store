"""
Course    : CSE 138 - Fall 2019
Author    : Elisabeth Oliver
Email     : elaolive@ucsc.edu
"""

import unittest
import requests


# ------------------------------
# Expected Responses
addResponse_Success = {
    'message'    : 'Added successfully',
    'replaced'   : False,
    'status_code': 201
}

addResponseError_NoKey = {
    'error'      : 'Value is missing',
    'message'    : 'Error in PUT',
    'status_code': 400
}

addResponseError_longKey = {
    'error'      : 'Key is too long',
    'message'    : 'Error in PUT',
    'status_code': 400
}

updateResponse_Success = {
    'message'    : 'Updated successfully',
    'replaced'   : True,
    'status_code': 200
}

updateResponseError_NoKey = addResponseError_NoKey

getResponse_Success = {
    'doesExist'  : True,
    'message'    : 'Retrieved successfully',
    'value'      : 'Default Value, should be changed based on input',
    'status_code': 200
}

getResponse_NoKey = {
    'doesExist'  : False,
    'error'      : 'Key does not exist',
    'message'    : 'Error in GET',
    'status_code': 404
}

delResponse_Success = {
    'doesExist'  : True,
    'message'    : 'Deleted successfully',
    'status_code': 200,
}

delResponse_NoKey = {
    'doesExist'  : False,
    'error'      : 'Key does not exist',
    'message'    : 'Error in DELETE',
    'status_code': 404
}


class TestHW2(unittest.TestCase):

    # ------------------------------
    # Helper Methods

    def keyOperation(self, fn_request, ip, port, key, **kwargs):
        return self.formatResult(fn_request(
            'http://{}:{}/kv-store/{}'.format(ip, port, key),
            headers={'Content-Type': 'application/json'},
            **kwargs
        ))

    def putKey(self, key, value, ip='localhost', port=13800):
        return self.keyOperation(requests.put, ip, port, key, json={'value': value})

    def getKey(self, key, ip='localhost', port=13800):
        return self.keyOperation(requests.get, ip, port, key)

    def deleteKey(self, key, ip='localhost', port=13800):
        return self.keyOperation(requests.delete, ip, port, key)

    def formatResult(self, result):
        """
        Reduce response to minimum JSON.
        """

        formatted_result = {'status_code': result.status_code}

        if result.json() is not None:
            for attr_name in ('message', 'replaced', 'error', 'doesExist', 'value'):
                if attr_name in result.json():
                    formatted_result[attr_name] = result.json()[attr_name]

        return formatted_result

    # ------------------------------
    # Tests

    # add a new key
    def test_add_1(self):
        self.assertEqual(self.putKey('Test', 'a friendly string'), addResponse_Success)

    # add and get
    def test_get_2(self):
        key    = 'AKey'
        value  = 'a different friendly string'

        result = self.putKey(key, value)
        self.assertEqual(
            result['status_code'],
            addResponse_Success['status_code'],
            msg='add key: failed add, cannot continue test\n{}\n'.format(result)
        )

        result            = self.getKey(key)
        expected          = getResponse_Success.copy()
        expected['value'] = value

        self.assertEqual(result, expected)

    # add then update
    def test_update_1(self):
        key    = 'AValueToUpdate!'

        result = self.putKey(key, 'one, one, one, one!')
        self.assertEqual(
            result['status_code'],
            addResponse_Success['status_code'],
            msg='add key: failed add, cannot continue test\n{}\n'.format(result)
        )

        self.assertEqual(self.putKey(key, 'two, three, four!'), updateResponse_Success)

    # add and delete
    def test_del_1(self):
        key    = 'keyToDelete'

        result = self.putKey(key, 'delete, delete, delete!')
        self.assertEqual(
            result['status_code'],
            addResponse_Success['status_code'],
            msg='add key: failed add, cannot continue test\n{}\n'.format(result)
        )

        self.assertEqual(self.deleteKey(key), delResponse_Success)


if __name__ == '__main__':
    unittest.main()
