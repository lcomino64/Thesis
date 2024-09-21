#!/bin/bash

PORT=8080

while true; do
  socat TCP-LISTEN:$PORT,fork EXEC:'bash -c "
    while IFS= read -r line; do
      op=${line:0:1}
      data=${line:1}
      if [ "$op" = "0" ]; then
        echo "Encrypting: $data"
        echo "$data" | openssl enc -aes-256-cbc -base64 -k mysecretkey
      elif [ "$op" = "1" ]; then
        echo "Decrypting: $data"
        echo "$data" | openssl enc -d -aes-256-cbc -base64 -k mysecretkey
      else
        echo "Invalid operation"
      fi
    done
  "'
done
