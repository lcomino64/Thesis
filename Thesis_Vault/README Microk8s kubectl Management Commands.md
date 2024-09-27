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

# Private Repo
Build and upload to repo:
```

```