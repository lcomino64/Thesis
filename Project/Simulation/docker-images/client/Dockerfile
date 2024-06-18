FROM debian:stable-slim

RUN apt-get update && apt-get install -y nmap && apt-get install -y ncat openssl 

COPY client.sh /app/client.sh
RUN chmod +x /app/client.sh

CMD ["/app/client.sh"]
