#!/bin/bash

master_pi="user@192.168.1.11"
FILE_PATH="/Users/lachlancomino/Documents/Uniwork 2024/Thesis/Project/cluster_network/"

function build_server() {
    docker build . -t docker-images/server-image:local

    scp "$FILE_PATH"docker-images/server-image.tar $master_pi
    scp "$FILE_PATH"docker-images/server-deployment.yaml $master_pi
    scp "$FILE_PATH"docker-images/server-service.yaml $master_pi

    ssh $master_pi "micrkok8s kubectl apply -f server-demployment.yaml"            
}

while getopts ":s" opt; do
    case $opt in
      s) build_server "$OPTARG" ;;
    esac
done


# Build images
docker build . -t docker-images/client-image:local

# Transfer images, YAMLs and tools scripts to master Pi
scp "$FILE_PATH"docker-images/client-image.tar $master_pi 
scp "$FILE_PATH"docker-images/client-deployment.yaml $master_pi
scp "$FILE_PATH"docker-images/client-config.yaml $master_pi
scp "$FILE_PATH"docker-images/kclient.sh $master_pi

# Import images into microk8s
ssh $master_pi "microk8s image import ~/client-image.tar"

# Give exec perms to client config script
ssh $master_pi "chmod +x kclient.sh"

# Apply deployment and config files on master Pi
ssh $master_pi "microk8s kubectl apply -f client-deployment"



