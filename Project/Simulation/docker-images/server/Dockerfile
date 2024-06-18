FROM debian:stable-slim

RUN apt-get update && apt-get install -y nmap && apt-get install -y ncat openssl

COPY server.sh /app/server.sh
RUN chmod +x /app/server.sh

CMD ["/app/server.sh"]
