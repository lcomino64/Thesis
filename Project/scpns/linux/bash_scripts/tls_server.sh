# Generate a test cert/key if needed
if [ ! -f key.pem ] || [ ! -f cert.pem ]; then
    openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes
fi
# Start OpenSSL server 
openssl s_server -cert cert.pem -key key.pem -accept 8443 -cipher AES128-GCM-SHA256


