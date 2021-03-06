# ------------------------------
# Run Docker containers

path_to_dockerfile="."

docker network create --subnet=10.10.0.0/16 kv_subnet
docker build -t kv-store:4.0 $path_to_dockerfile

# example node addresses
addr1="10.10.0.2:13800"
addr2="10.10.0.3:13800"
addr3="10.10.0.4:13800"
rep= "1"

# convenience variables
initial_full_view="${addr1},${addr2}"
full_view=${initial_full_view},${addr3}

nohup docker run --name="node1"        --net=kv_subnet     \
           --ip=10.10.0.2        -p 13802:13800      \
           -e ADDRESS="${addr1}"                     \
           -e VIEW=${initial_full_view}              \
           -e REPL_FACTOR=${rep}                     \
           kv-store:4.0 &

nohup docker run --name="node2"        --net=kv_subnet     \
           --ip=10.10.0.3        -p 13803:13800      \
           -e ADDRESS="${addr2}"                     \
           -e VIEW=${initial_full_view}              \
           -e REPL_FACTOR=${rep}                     \
           kv-store:4.0 &
