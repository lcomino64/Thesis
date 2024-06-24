## FPGA Development
[[README FPGA Development Notes]]
Get stuff for running Scala Build Tools
> Install JAVA 8 SDK & SBT
```shell
# Using SDKMAN!
`curl -s "https://get.sdkman.io" | bash`

sdk install java $(sdk list java | grep -o "\b8\.[0-9]*\.[0-9]*\-tem" | head -1)

sdk install sbt
```
> Install Verilator (for FPGA simulation, for MacOS aarch64)
```shell
brew install git make autoconf gcc flex bison
git clone http://git.veripool.org/git/verilator   # Only first time
```

### Demo CPU Setup
> Clone VexRiscv
```shell
git clone https://github.com/SpinalHDL/VexRiscv.git
```
> Now in the root of the VexRiscv repo, run
```shell
sbt "runMain vexriscv.demo.GenSmallest"
```
This will compile the smallest possible CPU configuration
### From Litex Repo


## FPGA Software
Follow:
https://docs.zephyrproject.org/latest/develop/getting_started/index.html
## Kubernetes Cluster
[[README Microk8s kubectl Management Commands]]
Follow for setting up Raspberry Pis
https://ubuntu.com/tutorials/how-to-kubernetes-cluster-on-raspberry-pi#1-overview

