#!/bin/bash

set -e

FILE_PATH="/Users/lachlancomino/Documents/Uniwork 2024/Thesis/Project/cluster_network/"
master_pi_password="user"
master_pi_user="user"
master_pi_ip="192.168.1.11"
master_pi="$master_pi_user"@"$master_pi_ip"


function delete_deployments() {
    # Delete all deployments
    ssh $master_pi "microk8s kubectl delete deployment --all"
}

function build_server() {
    docker build "$FILE_PATH"docker-images/server -t server-image:local || exit 1;
    docker save server-image > "$FILE_PATH"docker-images/server-image.tar    

    scp "$FILE_PATH"docker-images/server-image.tar $master_pi:~
    scp "$FILE_PATH"docker-images/server-deployment.yaml $master_pi:~
    scp "$FILE_PATH"docker-images/server-service.yaml $master_pi:~
    
    ssh $master_pi "microk8s ctr image import ~/server-image.tar"
    
    sleep 2
    
    ssh $master_pi "microk8s kubectl apply -f server-service.yaml" 
    ssh $master_pi "microk8s kubectl apply -f server-deployment.yaml"            

}

function build_client() {
    # Build images
    docker build "$FILE_PATH"docker-images/client -t client-image:local || exit 1
    docker save client-image > "$FILE_PATH"docker-images/client-image.tar

    # Transfer images, YAMLs and tools scripts to master Pi
    scp "$FILE_PATH"docker-images/client-image.tar $master_pi:~
    scp "$FILE_PATH"docker-images/client-deployment.yaml $master_pi:~

    # Import images into microk8s
    ssh $master_pi "microk8s ctr image import ~/client-image.tar"

    sleep 2

    # Apply deployment and config files on master Pi
    ssh $master_pi "microk8s kubectl apply -f ~/client-deployment.yaml"
}

while getopts ":s:c:d" opt; do
    case $opt in
      s) build_server ;;
      c) build_client ;;
      d) delete_deployments ;;
    esac
done


