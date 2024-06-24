### Applying image changes to local image

```shell
docker build . -t server-image:local
```

```shell
docker save server-image > server-image.tar
```

```shell
multipass transfer server-image.tar microk8s-vm:/tmp/server-image.tar
```

```shell
microk8s ctr image import /tmp/server-image.tar
```
### Applying YAML changes
```shell
microk8s kubectl apply -f <yaml-file>
```
### Delete pod completely
```shell
microk8s kubectl get deployments
```

```shell
microk8s kubectl delete deployment <deployment-name>
```
Check if pod still running
```shell
microk8s kubectl get pods
```
If it is still there
```shell
microk8s kubectl delete pod <pod-name>
```

### Viewing pod output
```shell
microk8s kubectl logs -f <pod-name>
```

### Custom Commands
```shell
microk8s kubectl patch configmap client-config -p '{"data":{"MESSAGE_FREQUENCY":"5"}}'
```

```shell
microk8s kubectl patch configmap client-config -p '{"data":{"MESSAGE":"New message"}}'
```

```shell
microk8s kubectl patch configmap client-config -p '{"data":{"MESSAGING_ENABLED":"false"}}'
```

```shell
microk8s kubectl patch configmap client-config -p '{"data"{"ENCRYPTION_ENABLED":"false"}}'
```

```shell
microk8s kubectl scale deployment client --replicas=$replicas
```
### For Raspberry Pis
Just run to transfer changes:
```shell
./build_and_transfer_images.sh
```
Make sure Docker is running

Then on home directory of master Pi:
```shell
user$ ./kclient.sh
```

Help for kclient.sh
```shell
Usage: kclient [options]

Options:
  -f <seconds>  Set the message frequency (in seconds)
  -m <text>     Set the message to send
  -s <on|off>   Toggle messaging on or off
  -e <on|off>   Toggle encryption on or off
  -h            Display this help message
```