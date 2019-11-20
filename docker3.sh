path_to_dockerfile="."



# example node addresses
addr1="10.10.0.2:13800"
addr2="10.10.0.3:13800"
addr3="10.10.0.4:13800"

# convenience variables
initial_full_view="${addr1},${addr2}"
full_view=${initial_full_view},${addr3}

# ------------------------------
# Now we start a new node and add it to the existing store

docker run --name="node3" --net=kv_subnet            \
           --ip=10.10.0.4  -p 13804:13800            \
           -e ADDRESS="${addr3}"                     \
           -e VIEW="${full_view}"                    \
           kv-store:3.0

curl --request PUT                                   \
     --header "Content-Type: application/json"       \
     --data '{"view": "${full_view}"}'               \
     --write-out "%{http_code}\n"                    \
     http://${addr2}/kv-store/view-change

curl --request GET                                   \
     --header "Content-Type: application/json"       \
     --write-out "%{http_code}\n"                    \
     http://${addr3}/kv-store/keys/sampleKey

<<'expected_response'
{
    "doesExist": "true",
    "message"  : "Retrieved successfully",
    "value"    : "sampleValue",
    "address"  : "10.10.0.2:13800"
}

status code: 200
expected_response
