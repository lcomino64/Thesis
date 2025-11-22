```shell
root@buildroot:~# sh tls_server.sh
Generating a RSA private key
............+++++
....................................................+++++
writing new private key to 'key.pem'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) []:AU
State or Province Name (full name) []:QLD
Locality Name (eg, city) []:Brisbane
Organization Name (eg, company) []:UQ
Organizational Unit Name (eg, section) []:Student
Common Name (eg, fully qualified host name) []:.
Email Address []:.
```

w/ AES Instructions enabled @ 150MHz:
```shell
❯ ./tls_benchmark.sh
Starting TLS throughput test to 192.168.1.50:8443
==================================================
Testing 64KB transfer...
Run 1:
Duration: 1.653 seconds
Throughput: 38.71 KB/s
------------------------
Run 2:
Duration: 6.747 seconds
Throughput: 9.48 KB/s
------------------------
Run 3:
Duration: 6.753 seconds
Throughput: 9.47 KB/s
------------------------
Testing 128KB transfer...
Run 1:
Duration: 6.733 seconds
Throughput: 19.01 KB/s
------------------------
Run 2:
Duration: 12.397 seconds
Throughput: 10.32 KB/s
------------------------
Run 3:
Duration: 12.314 seconds
Throughput: 10.39 KB/s
------------------------
Testing 256KB transfer...
Run 1:
Duration: 16.841 seconds
Throughput: 15.20 KB/s
------------------------
Run 2:
Duration: 20.436 seconds
Throughput: 12.52 KB/s
------------------------
Run 3:
Duration: 23.949 seconds
Throughput: 10.68 KB/s
------------------------
Testing 512KB transfer...
Run 1:
Duration: 31.266 seconds
Throughput: 16.37 KB/s
------------------------
Run 2:
Duration: 46.698 seconds
Throughput: 10.96 KB/s
------------------------
Run 3:
Duration: 41.291 seconds
Throughput: 12.39 KB/s
------------------------
Testing 1024KB transfer...
Run 1:
Duration: 53.064 seconds
Throughput: 19.29 KB/s
------------------------
Run 2:
Duration: 92.956 seconds
Throughput: 11.01 KB/s
------------------------
Run 3:
Duration: 93.393 seconds
Throughput: 10.96 KB/s
------------------------
```

w/ AES instructions disabled @ 150MHz
```shell
❯ ./tls_benchmark.sh
Starting TLS throughput test to 192.168.1.50:8443
==================================================
Testing 64KB transfer...
Run 1:
Duration: 1.492 seconds
Throughput: 42.89 KB/s
------------------------
Run 2:
Duration: 6.936 seconds
Throughput: 9.22 KB/s
------------------------
Run 3:
Duration: 6.941 seconds
Throughput: 9.22 KB/s
------------------------
Testing 128KB transfer...
Run 1:
Duration: 6.947 seconds
Throughput: 18.42 KB/s
------------------------
Run 2:
Duration: 12.885 seconds
Throughput: 9.93 KB/s
------------------------
Run 3:
Duration: 12.901 seconds
Throughput: 9.92 KB/s
------------------------
Testing 256KB transfer...
Run 1:
Duration: 13.130 seconds
Throughput: 19.49 KB/s
------------------------
Run 2:
Duration: 23.963 seconds
Throughput: 10.68 KB/s
------------------------
Run 3:
Duration: 31.090 seconds
Throughput: 8.23 KB/s
------------------------
Testing 512KB transfer...
Run 1:
Duration: 24.626 seconds
Throughput: 20.79 KB/s
------------------------
Run 2:
Duration: 46.329 seconds
Throughput: 11.05 KB/s
------------------------
Run 3:
Duration: 39.838 seconds
Throughput: 12.85 KB/s
------------------------
Testing 1024KB transfer...
Run 1:
Duration: 52.982 seconds
Throughput: 19.32 KB/s
------------------------
Run 2:
Duration: 87.624 seconds
Throughput: 11.68 KB/s
------------------------
Run 3:
Duration: 101.403 seconds
Throughput: 10.09 KB/s
------------------------
```


Output for one TLS1.3 stream transfer:
```
ACCEPT
bad gethostbyaddr
-----BEGIN SSL SESSION PARAMETERS-----
MCMCAQECAgMEBAITAgQABAChBAICBLCiBAICHCCkBgQEAQAAAA==
-----END SSL SESSION PARAMETERS-----
Shared ciphers:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256:AES128-GCM-SHA256
CIPHER is TLS_AES_256_GCM_SHA384
Secure Renegotiation IS supported
DONE
shutting down SSL
CONNECTION CLOSED
```