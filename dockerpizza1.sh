path_to_dockerfile="."


# example node addresses
addr1="10.10.0.2:13800"
addr2="10.10.0.3:13800"
addr3="10.10.0.4:13800"

# convenience variables
initial_full_view="${addr1},${addr2}"
full_view=${initial_full_view},${addr3}
curl --request   PUT                                 \
     --header    "Content-Type: application/json"    \
     --data      '{"value": "sampleValue"}'          \
     --write-out "%{http_code}\n"                    \
     http://10.10.0.3:13800/kv-store/keys/sampleKey


<<'expected_response'
{
    "message" : "Added successfully",
    "replaced": "false"
}
status code: 201
expected_response


curl --request GET                                   \
     --header "Content-Type: application/json"       \
     --write-out "%{http_code}\n"                    \
     http://${addr1}/kv-store/keys/sampleKey


<<'expected_response'
{
    "doesExist": "true",
    "message"  : "Retrieved successfully",
    "value"    : "sampleValue",
    "address"  : "10.10.0.3:13800"
}

status code: 200
expected_response
