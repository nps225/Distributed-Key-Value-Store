from flask import Flask, request, jsonify, redirect,make_response
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
        x,y = h.checkHash(key)
        if(x):
            value = data["value"]  # value
            res = store.upsertValue(key, value)
            if(not res):
                h.incCount()
                return jsonify(
                    message='Added successfully',
                    replaced=res
                ), 201

            if(res):
                return jsonify(
                    message="Updated successfully",
                    replaced=res
                ), 200
        else:#we need to forward this request
            #we need to go to this shard
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
        #if not handle forwarding below here

# GET KEY IMPLEMENTATION
@app.route('/kv-store/keys/<key>', methods=['GET'])
def getKey(key):
    x, y = h.checkHash(key)    

    #key is in this node
    if(x): 
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
        #this means we need to forward our request
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

        

# DELETE KEY IMPLEMENTATION
@app.route('/kv-store/keys/<key>', methods=['DELETE'])
def deleteKey(key):
    # need condition here to see if value in storage already exists
    x, y = h.checkHash(key)

    #if the key is in this shard
    if(x):
        res = store.deleteValue(key)

        if(res):
            h.decCount()
            return jsonify(
                doesExist=res,
                message="Deleted successfully"
            ), 200

        if(not res):
            return jsonify(
                doesExist=res,
                error="Key does not exist",
                message="Error in DELETE"
            ), 404
    else:
        url = 'http://' + y + '/kv-store/keys/' + key
        try:
            a,b = (formatResult(requests.delete(url, timeout=5,headers={
                'Content-Type': 'application/json'})))
            a["address"] = y
            return a,b

        except:  # return that main is down
            # print(e)
            return jsonify(
                error="Main instance is down",
                message="Error in DELETE",
                address=y
            ), 503


@app.route('/kv-store/key-count', methods=['GET'])
def keyCount():
    count = h.getCount()
    temp = {
        "message": "Key count retrieved successfully",
        "key-count":count
        }
    return make_response(temp),200

@app.route('/kv-store/view-change',methods=['PUT'])
def viewChange():
    # let us begin the view change
    # had an idea for a view null check in another branch
    # assume that the view is always there since if no view, no access 
    data = request.get_json()#its our data!!!
    loc = h.getSelfAddress()
    # oldView = h.getView()
    #first we need to change the view of the current node
    # set the view
    # print('joe mama', flush = True)
    # print(data['view'], flush = True)
    forwarding = h.updateView(data["view"])#this should update the view, sends to the hash.py
    #now we need to reshard ....
    shards = []

    forward = [f for f in forwarding if f != loc]

    for v in forward:
        # if v is not loc:
        url = 'http://' + v + '/kv-store/view-change-forward' 
        temp = (formatResult(requests.put(url, timeout=5,headers={
                'Content-Type': 'application/json'}, json=data)))
        # res, b = requests.put(url, headers={
        #         'Content-Type': 'application/json'}, json=data)
        res, b = temp
        shards.append({
            "address": res["address"]
            # "key-count": res["key-count"]
        })

    # response = {
    #    "message":"View change successful",
    #    "shards": shards,
    #    "forwarding": forward
    # }
    
    # return make_response(response),200
    count = reshard(store.returnStore())
    shards.append({
        "address": loc
        # "key-count": h.getCount()
    })
    #get keycount, append to appropriate indexed shard address
    for i in range(len(shards)):
        val = shards[i]["address"]
        url = 'http://' + val + '/kv-store/key-count'
        temp = (formatResult(requests.get(url,timeout=5, headers={
                    'Content-Type': 'application/json'})))

        res, b = temp
        shards[i].update({"key-count": res["key-count"]})



    
    response = {
       "message":"View change successful",
       "shards": shards
    }

    return make_response(response),200




@app.route('/kv-store/view-change-forward',methods=['PUT'])
def viewChangeForward():
    data = request.get_json()#its our data!!!
    # #get original view
    sAddr = h.getSelfAddress()
    # #first we need to change the view of the current node
    # # set the view

    forwarding = h.updateView(data["view"])#this should update the view, sends to the hash.py
    c = reshard(store.returnStore())
    res = {
        "address": sAddr
        #"key-count": c
    }

    return make_response(res), 200

    





##HELPER FUNCTIONS
def formatResult(result):
    status_code = result.status_code
    result = result.json()

    if result != None:
        jsonKeys = ["message", "replaced", "error", "doesExist", "value", "address", "key-count", "shards"]
        result = {k: result[k] for k in jsonKeys if k in result}

    else:
        result = {"status_code": status_code}


    return result, status_code


def reshard(kv):
    for key,val in kv:
        x, y = h.checkHash(key)
        if not x:
            data = [{"value": val}]
          #we forward to insert
            try:
                url = 'http://' + y + '/kv-store/keys/' + key
                temp = (formatResult(requests.put(url,timeout=5, headers={
                    'Content-Type': 'application/json'}, json={"value":val})))
                res = store.deleteValue(key)
                h.decCount()
            except:
                pass
        
    return h.getCount()

          #if we get 200 from insert, we delete the key from current node and continue on


if __name__ == '__main__':
    num_keys = 0 #number of keys in our key-value store
    #app.config['JSON_SORT_KEYS'] = False
    app.run(debug=True, threaded=True, host='0.0.0.0', port=13800)
# why 0.0.0.0?? https://stackoverflow.com/questions/20778771/what-is-the-difference-between-0-0-0-0-127-0-0-1-and-localhost
# it basically checks if there is anything being point to the network for the local IP
