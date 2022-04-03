#!/bin/bash
echo "Creating our environment file"
bash generate_env.sh
echo "Finished creating our environment file"

echo "Creating blockchain network"
bash create_network.sh
echo "Done creating network"

# When we exit shut the network down.
trap "bash network/network.sh down" EXIT

echo "Starting rest server"
bash start_rest_server.sh
echo "Exiting rest server"

echo "Shutting network down"
