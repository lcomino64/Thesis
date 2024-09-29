#!/bin/bash
# Bash script to transfer images to raspberry Pis. Usually this is solved by using a private repo, but I couldn't get it working.

# Function to build and save images
build_images() {
    echo "Building server image..."
    docker build ./server -t server-image:local
    echo "Saving server image..."
    docker save server-image:local > server-image.tar

    echo "Building client image..."
    docker build ./client -t client-image:local
    echo "Saving client image..."
    docker save client-image:local > client-image.tar
}

# Check if --build flag is provided
if [[ "$1" == "--build" ]]; then
    build_images
fi

# List of Raspberry Pi addresses
PI_ADDRESSES=(
    "user@192.168.1.11"
    "user@192.168.1.12"
    "user@192.168.1.13"
    "user@192.168.1.14"
)

# SSH user and password
SSH_USER="user"
SSH_PASS="user"

# Directory on the Raspberry Pis where you want to store the YAML files and images
REMOTE_DIR="~"

# Loop through each Raspberry Pi
for PI in "${PI_ADDRESSES[@]}"; do
    echo "Transferring files to $PI..."
    
    # Transfer all YAML files from the current directory
    scp *.yaml $PI:$REMOTE_DIR

    if [[ "$1" == "--build" ]]; then
        # Transfer image tar files
        scp *.tar $PI:$REMOTE_DIR
    
        echo "Transfer complete for $PI"
    
        # Import images into containerd
        ssh $PI "for img in $REMOTE_DIR/*.tar; do sudo microk8s ctr image import \$img; done"
    
        echo "Images imported for $PI"
    fi

    echo "------------------------"
done

echo "All transfers and imports completed!"
