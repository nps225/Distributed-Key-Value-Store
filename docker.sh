# ------------------------------
# Run Docker containers

path_to_dockerfile="."

docker network create --subnet=10.10.0.0/16 kv_subnet
docker build -t kv-store:3.0 $path_to_dockerfile

# example node addresses
addr1="10.10.0.2:13800"
addr2="10.10.0.3:13800"
addr3="10.10.0.4:13800"
addr4="10.10.0.5:13800"
addr5="10.10.0.6:13800"
addr6="10.10.0.7:13800"

# convenience variables
initial_full_view="${addr1},${addr2}"
full_view=${initial_full_view},${addr3},${addr4}

nohup docker run --name="node1"        --net=kv_subnet     \
           --ip=10.10.0.2        -p 13802:13800      \
           -e ADDRESS="${addr1}"                     \
           -e VIEW=${full_view}              \
           -e REPL_FACTOR="2"                        \
           kv-store:3.0 &

nohup docker run --name="node2"        --net=kv_subnet     \
           --ip=10.10.0.3        -p 13803:13800      \
           -e ADDRESS="${addr2}"                     \
           -e VIEW=${full_view}              \
           -e REPL_FACTOR="2"                        \
           kv-store:3.0 &

nohup docker run --name="node3"        --net=kv_subnet     \
           --ip=10.10.0.4        -p 13804:13800      \
           -e ADDRESS="${addr3}"                     \
           -e VIEW="${full_view}"              \
           -e REPL_FACTOR="2"                        \
           kv-store:3.0 &

nohup docker run --name="node4"        --net=kv_subnet     \
           --ip=10.10.0.5        -p 13805:13800      \
           -e ADDRESS="${addr4}"                     \
           -e VIEW="${full_view}"              \
           -e REPL_FACTOR="2"                        \
           kv-store:3.0 &

nohup docker run --name="node5"        --net=kv_subnet     \
           --ip=10.10.0.6        -p 13806:13800      \
           -e ADDRESS="${addr5}"                     \
           -e VIEW="${addr5},${addr6}"             \
           -e REPL_FACTOR="2"                        \
           kv-store:3.0 &

docker run --name="node6"        --net=kv_subnet     \
           --ip=10.10.0.7        -p 13807:13800      \
           -e ADDRESS="${addr6}"                     \
           -e VIEW="${addr5},${addr6}"             \
           -e REPL_FACTOR="2"                        \
           kv-store:3.0 &

