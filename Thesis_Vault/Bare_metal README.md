## Demo:
Build
```shell
litex_bare_metal_demo --build-path=/home/lachlancomino/Thesis/Project/scpns/litex/build/arty_a7
```
Flash
```shell
litex_term /dev/ttyUSB1 --kernel=demo.bin
```
## Project:
Build
```shell
./make.py --build-path=/home/lachlancomino/Thesis/Project/scpns/litex/build/arty_a7
```
Flash
```shell
litex_term /dev/ttyUSB1 --kernel=scpns.bin
```