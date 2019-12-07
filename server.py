from flask import Flask, request, jsonify, redirect,make_response
import logging
import requests
from KeyValueStore.store import Store
import VectorClock.vectorClock as Clock
from Hash.hash import Hash
import json
import time
import threading
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

#init our VC

clock = 0
#UPSERT
@app.route('/kv-store/keys/<key>', methods=['PUT'])
def upsertKey(key):
    #first step is to check if we need to forward our address
    data = request.get_json()
    global clock
    causal = data["causal-context"]
    if len(key) > 50:
        response =  {
                        "error":"Key is too long",
                        "message":"Error in PUT",
                        "address":address,
                        "causal-context":causal
        }
        return make_response(response), 400
    if 'value' not in data:
        response =  {
                        "error":"Value is missing",
                        "message":"Error in PUT",
                        "address":address,
                        "causal-context":causal
        }
        return make_response(response), 400
    else:  # else for readability?
        #first check if there is a VectorClock attached
        # make the request to the key value store
        # key
        #if the key is put in our key-value store
        addresses = h.checkHash(key)
        #handle the insert here
        if address in addresses:#if it is at this address
            #here we should implement our incrementation of our clock
            clock = clock + 1
            value = data["value"]  # value
            causal = data["causal-context"]
            Clock.updateClock(causal,clock)
            res,clock3 = store.upsertValue(key, value, causal)
            # if(res == 404):
            #     return make_response({"causal-context":clock3}),404

            if(not res):
                #no previous value exists -> handled easily
                # h.incCount()
                response = {
                    "message":'Added successfully',
                    "replaced":res,
                    "address":address,
                    "causal-context":clock3
                }
                return make_response(response),201

            if(res):
                #we need to compare the clocks to ensure we have causality
                response = {
                    "message":'Update successfully',
                    "replaced":res,
                    "address":address,
                    "causal-context":clock3
                }
                return make_response(response),200

            #insert -> inc our clock
            #gossip here
            #gossipPUT(addresses,key,data)
        else:
            #we need to handle if we get a 503 here then we move onto the next request for replica
            # vc.incClock()
            for addr in addresses:
                y = addr
                url = 'http://' + y + '/kv-store/keys/' + key
                try:
                    data = request.get_json()
                    temp = (formatResult(requests.put(url,timeout=2, headers={
                        'Content-Type': 'application/json'}, json=data)))

                    a, b = temp
                    #on forward -> inc our clock
                    response =  {
                        "message":a["message"],
                        "replaced":a["replaced"],
                        "address":y,
                        "causal-context":a["causal-context"]
                    }
                    return make_response(response),b
                except:  # return that main is down
                    pass
                time.sleep(1)
            
            response =  {
                        "error":"instance is down",
                        "message":"Error in PUT",
                        "address":addresses,
                        "causal-context":causal
            }
            return make_response(response), 503

# GET KEY IMPLEMENTATION
@app.route('/kv-store/keys/<key>', methods=['GET'])
def getKey(key):
    data = request.get_json()
    addresses = h.checkHash(key)
    if address in addresses:
        exists, val, code = store.getValue(key)
        if(exists):
            response = {
                "doesExist":exists,
                "message":"Retrieved successfully",
                "value":val,
                "address":address,
                "causal-context":{}
            }
            return make_response(response), code
        else:
            response = {
                "doesExist":exists,
                "error":"Key does not exist",
                "message":val,
                "address":address,
                "causal-context":{}
            }
            return make_response(response),code
    else:
        #handle if a node is down
        #this means we need to forward our request
        y = addresses[0]
        url = 'http://' + y + '/kv-store/keys/' + key
        # now let's grab make our request
        try:
            temp = (formatResult(requests.get(url= url,timeout=2, headers={
                'Content-Type': 'application/json'})))
            a,b = temp
            # a.update({"address":y})
            #dont for get causal-context here
            return make_response(a),b
        except:
            response = {
                "error":"Main instance is down",
                "message":"Error in GET",
                "address":y,
                "causal-context":{}
            }
            return make_response(response), 503

#Key-Count
@app.route('/kv-store/key-count', methods=['GET'])
def keyCount():
    data = request.get_json()
    count = len(store.returnStore())
    addresses = h.getShard()
    temp = {
            "message": "Key count retrieved successfully",
            "key-count":count,
            "shard-id":str(int(h.shard_id) + 1),
            "causal-context":data["causal-context"]
        }
    return make_response(temp),200

#return entire store
@app.route('/kv-store/table', methods=['GET'])
def getStore():
    values,vectors,timestamps = store.returnTablesDict()
    temp = {
        "message": "Returned table",
        "values":values,
        "vectors":vectors
        }
    return make_response(temp),200


@app.route('/kv-store/view', methods=['GET'])#for now this just returns my vector clock
def getView():
    # values,vectors,timestamps = store.returnTablesDict()
    temp = {
            "View":os.getenv("VIEW"),
            "REPL":os.getenv("REPL_FACTOR")
        }
    return make_response(temp),200


@app.route('/kv-store/shards/<id>',methods=['GET'])
def getShardId(id):
    data = request.get_json()
    val = h.getView().copy()
    repl = os.getenv("REPL_FACTOR")
    shardAddresses = val[(((int(id) - 1) * int(repl))):(((((int(id) - 1) * int(repl))  + int(repl))))]
    if not address in shardAddresses:
        for i in shardAddresses:
            #where i forward the the request to a member of that shard
            y = i
            url = 'http://' + y + '/kv-store/shards/' + id
            # now let's grab make our request
            try:
                temp = (formatResult(requests.get(url= url,timeout=2, headers={
                    'Content-Type': 'application/json'},json=data)))
                a,b = temp
                # a.update({"causal-context":data["causal-context"]})
                return make_response(a),b
            except:
                pass
        #handle if the shard is down
        #idk what to respond
        return make_response({}),503

    else:
        response = {
            "message":"Shard information retrieved successfully",
            "shard-id":id,
            "replicas":shardAddresses,
            "key-count":len(store.dict),
            "causal-context": data["causal-context"]
        }
        return make_response(response),200


@app.route('/kv-store/shards',methods=['GET'])
def getShard():
    data = request.get_json()
    response = {}
    response["message"] = "Shard membership retrieved successfully"
    response["causal-context"] = data["causal-context"]
    response["shards"] = []
    numOfShard = int(len(h.getView())/int(os.getenv("REPL_FACTOR")))
    for i in range(1,numOfShard+1):
        response["shards"].append(str(i))

    return make_response(response),200



@app.route('/kv-store/view-change',methods=['PUT'])
def viewChange():
    data = request.get_json()
    nodes = h.getView().copy()
    view = data["view"] #returns a list now :O
    repl = data["repl-factor"]
    viewString = ','.join(view)
    h.updateView(viewString)
    h.updateReplicationFactor(str(repl))
    nodes = list(set(nodes) | set(h.getView()))
    data["nodes2"] = nodes
    #alright now lets reshard
    #now lets forward our request to all nodes for the view change
    l = []
    for node in nodes:
        if not address == node:
            url = 'http://' + node + '/kv-store/view-change-forward'
            temp = (formatResult(requests.put(url,timeout=2, headers={
                'Content-Type': 'application/json'}, json=data)))
            l.append(temp)
    time.sleep(1)
    for node in nodes:
        if not address == node:
            url = 'http://' + node + '/kv-store/reshard'
            temp = (formatResult(requests.put(url,timeout=2, headers={
                'Content-Type': 'application/json'}, json=data)))
            l.append(temp)
    time.sleep(1)
    kv, vc, ts = store.returnTablesDict()
    data["length"] = len(l)
    res = reshard(kv,vc,ts)
    #now that reshard is done lets proceed to return the shard infos
    numOfShards = int(len(h.getView())/int(os.getenv("REPL_FACTOR")))
    #return shards
    l = []
    for i in range(1,numOfShards + 1):
        try:
                url = 'http://' + address + '/kv-store/shards/' + str(i)
                temp = (formatResult(requests.get(url,timeout=2, headers={
                            'Content-Type': 'application/json'}, json=data)))
                a,b = temp
                l.append(a)
        except:
                pass

    response = {
        "message":"View change successful",
        "causal-context":data["causal-context"],
        "shards":l
    }

    time.sleep(1)
    # data["count"] = count
    #now we need to update our view
    return make_response(response),200

@app.route('/kv-store/reshard',methods=['PUT'])
def reshardForward():
    kv,vc,ts = store.returnTablesDict()
    res = reshard(kv,vc,ts)
    return make_response({"lol":res},200)

@app.route('/kv-store/view-change-forward',methods=['PUT'])
def viewChangeForward():
    data = request.get_json()
    view = data["view"] #returns a list now :O
    repl = data["repl-factor"]
    viewString = ','.join(view)
    h.updateView(viewString)
    h.updateReplicationFactor(str(repl))
    # kv, vc, ts = store.returnTablesDict()
    # reshard(kv,vc,ts)
    return make_response(data),200

@app.route('/kv-store/view-change/<key>',methods=['PUT'])
def reshardInsert(key):
    data = request.get_json()
    if(address in h.checkHash(key)):
        res = store.upsertValue(key, data["value"],data["causal-context"])
    return make_response({"value":res},200)


def reshard(kv,vc,ts):
    a = kv.copy()
    b = vc.copy()
    c = ts.copy()
    l = []
    for key in a:
        addresses = h.checkHash(key)
        if not address in addresses:
            #now forward the value to the address
            try:
                l.append(addresses[0])
                store.deleteValue(key)
                h.decCount()
                url = 'http://' + addresses[0] + '/kv-store/view-change/' + key
                temp = (formatResult(requests.put(url,timeout=2, headers={
                            'Content-Type': 'application/json'}, json={"value":a[key],"causal-context":b[key]})))
            except:
                pass
                
    return l

#gossip protocol
#DONT MESS WITH CLOCKS HERE
def gossip():
    #I want to gossip every second to ensure I have the latest data
    
    while True:
        #first we must send a request that obtains the entire table from various nodes
        global store
        shard = h.getShard()
        addresses = os.getenv("VIEW").replace("\"","").split(",")
        for i in addresses:
            if i in shard and i != address:
                try:
                    # print(i)
                    url = 'http://' + i + '/kv-store/table'
                    temp = (formatResult(requests.get(url,timeout=2, headers={
                    'Content-Type': 'application/json'})))
                    res,b = temp
                    store.comparison(res["values"],res["vectors"])
                    #now update our vector clock with the correct values
                    # res, b = temp
                except:
                    print("something bad happened and weeeee don't care!!!")
                    pass
            else:#not in our shard
                #we need to update our clock value
                try:
                    # print(i)
                    url = 'http://' + i + '/kv-store/view'
                    temp = (formatResult(requests.get(url,timeout=2, headers={
                    'Content-Type': 'application/json'})))
                    res,b = temp
                    
                except:
                    print("kinda bad happened!!!")
                    pass

                    
        # for i in shard:
        #     app.logger.info(str(i))

        time.sleep(1)


#HELPER FUNCTIONS
def formatResult(result):
    status_code = result.status_code
    result = result.json()

    if result != None:
        jsonKeys = ["message", "replaced", "error", "doesExist", "value", "address", "key-count", "shards","values","vectors","timestamps","VectorClock","Timestamp","View","replicas","id","shard-id","causal-context"]
        result = {k: result[k] for k in jsonKeys if k in result}

    else:
        result = {"status_code": status_code}


    return result, status_code


if __name__ == '__main__':
    num_keys = 0 #number of keys in our key-value store
    #app.config['JSON_SORT_KEYS'] = False
    threading = threading.Thread(target=gossip)
    threading.start()
    #second thread to handle the view sync? -- try in regular gossip -> try here if it is too laggy
    # threading2 = threading.Thread(target=gossip2)
    # threading2.start()
    app.run(debug=True, threaded=True, host='0.0.0.0', port=13800)
# why 0.0.0.0?? https://stackoverflow.com/questions/20778771/what-is-the-difference-between-0-0-0-0-127-0-0-1-and-localhost
# it basically checks if there is anything being point to the network for the local IP
