from flask import Flask, request, jsonify, redirect,make_response
import logging
import requests
from KeyValueStore.store import Store
from Hash.hash import Hash
import json
import time
# from os import environ
import os
app = Flask(__name__)
### FIX keys/
# =========================================================

# app.config.from_envvar('APP_SETTINGS')
# app.config['FARQUADD'] = environ.get('FARQUADD_KEY')

# https://www.youtube.com/watch?v=7RWro4VF_9c
#  for the future if needed


# =========================================================
#first create our store
#val =  "\"10.10.0.2:13800\",\"10.10.0.3:13800\",\"10.10.0.4:13800\""
#os.environ["VIEW"] = val
#os.environ["ADDRESS"] = "10.10.0.3:13800"

store = Store()
#set up our hashing algorithm
view = os.getenv("VIEW").split(",")
address = os.getenv("ADDRESS")
#hash handles view + count + hashing algorithm
h = Hash()# you can check which shard you are in + it will return you a forwarding address if needed
timmmme = 0
#UPSERT
@app.route('/kv-store/keys/<key>', methods=['PUT'])
def upsertKey(key):
    #first step is to check if we need to forward our address
    data = request.get_json()
    
    if len(key) > 50:
        return jsonify(
            error="Key is too long",
            message="Error in PUT"
        ), 400
    if 'value' not in data:
        return jsonify(
            error="Value is missing",
            message="Error in PUT"
        ), 400
    else:  # else for readability?
        # make the request to the key value store
        # key
        #if the key is put in our key-value store
        addresses = h.checkHash(key)
        #handle the insert here
        if address in addresses:#if it is at this address

            value = data["value"]  # value
            res = store.upsertValue(key, value)
            if(not res):
                h.incCount()
                response = jsonify(
                    message='Added successfully',
                    replaced=res
                ), 201

            if(res):
                response = jsonify(
                    message="Updated successfully",
                    replaced=res
                ), 200
            #gossip here
            #gossipPUT(addresses,key,data)
            return response
        else:
            #we need to handle if we get a 503 here then we move onto the next request for replica
            y = addresses[0]
            url = 'http://' + y + '/kv-store/keys/' + key
            try:
                temp = (formatResult(requests.put(url,timeout=5, headers={
                    'Content-Type': 'application/json'}, json=request.get_json())))

                a, b = temp
                return jsonify(
                    message='Added successful',
                    replaced=a["replaced"],
                    address=y
                ),b
            except:  # return that main is down
                return jsonify(
                    error="instance is down",
                    message="Error in PUT",
                    address = y
                ), 503

# GET KEY IMPLEMENTATION
@app.route('/kv-store/keys/<key>', methods=['GET'])
def getKey(key):
    addresses = h.checkHash(key)
    if address in addresses:
        exists, val, code = store.getValue(key)
        if(exists):
            return jsonify(
                doesExist=exists,
                message="Retrieved successfully",
                value=val
            ), code
        else:
            return jsonify(
                doesExist=exists,
                error="Key does not exist",
                message=val
            ), code
    else:
        #handle if a node is down
        #this means we need to forward our request
        y = addresses[0]
        url = 'http://' + y + '/kv-store/keys/' + key
        # now let's grab make our request
        try:
            temp = (formatResult(requests.get(url= url,timeout=5, headers={
                'Content-Type': 'application/json'})))
            a,b = temp
            a.update({"address":y})
            return a,b
        except:
            return jsonify(
                error="Main instance is down",
                message="Error in GET",
                address = y
            ), 503

#Key-Count
@app.route('/kv-store/key-count', methods=['GET'])
def keyCount():
    count = h.getCount()
    temp = {
        "message": "Key count retrieved successfully",
        "key-count":count
        }
    return make_response(temp),200

#return entire store
@app.route('/kv-store/table', methods=['GET'])
def getStore():
    values,vectors = store.returnTablesDict()
    temp = {
        "message": "Key count retrieved successfully",
        "values":values,
        "vectors":vectors,
        "time":timmmme
        }
    return make_response(temp),200




#gossip protocol
#

def gossip():
    #I want to gossip every second to ensure I have the latest data
    while True:
        #first we must send a request that obtains the entire table from various nodes
        shard = h.getShard()
        for i in shard:
            app.logger.info(str(i))

        time.sleep(1)

#HELPER FUNCTIONS
def formatResult(result):
    status_code = result.status_code
    result = result.json()

    if result != None:
        jsonKeys = ["message", "replaced", "error", "doesExist", "value", "address", "key-count", "shards"]
        result = {k: result[k] for k in jsonKeys if k in result}

    else:
        result = {"status_code": status_code}


    return result, status_code

if __name__ == '__main__':
    num_keys = 0 #number of keys in our key-value store
    #app.config['JSON_SORT_KEYS'] = False
    #gossip()
    app.run(debug=True, threaded=True, host='0.0.0.0', port=13800)
    gossip()
# why 0.0.0.0?? https://stackoverflow.com/questions/20778771/what-is-the-difference-between-0-0-0-0-127-0-0-1-and-localhost
# it basically checks if there is anything being point to the network for the local IP
