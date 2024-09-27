import socket
import subprocess
import threading

CHUNK_SIZE = 1048576  # 1 MB, adjust if needed

def process_data(data, operation, is_last_chunk):
    key = '00' * 16
    iv = '00' * 16
    
    if operation == 'encrypt':
        cmd = ['openssl', 'enc', '-aes-128-cbc', '-K', key, '-iv', iv, '-nosalt']
        if not is_last_chunk:
            cmd.append('-nopad')
    else:  # decrypt
        cmd = ['openssl', 'enc', '-d', '-aes-128-cbc', '-K', key, '-iv', iv, '-nosalt']
        if not is_last_chunk:
            cmd.append('-nopad')
    
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(input=data)
    
    if p.returncode != 0:
        raise Exception(f"OpenSSL error: {stderr.decode()}")
    
    return stdout

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4 * CHUNK_SIZE)
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4 * CHUNK_SIZE)

    print(f"[{addr}] Waiting for operation byte")
    op_byte = conn.recv(1)
    operation = 'encrypt' if op_byte == b'\x00' else 'decrypt'
    print(f"[{addr}] Operation: {operation}")

    print(f"[{addr}] Sending acknowledgement")
    conn.sendall(b'OK')

    total_received = 0
    total_sent = 0
    chunks_received = 0

    try:
        while True:
            print(f"[{addr}] Waiting for chunk size")
            size_data = conn.recv(4)
            if not size_data:
                print(f"[{addr}] Client closed connection")
                break
            chunk_size = int.from_bytes(size_data, byteorder='big')
            print(f"[{addr}] Expecting chunk of {chunk_size} bytes")
            
            chunk = b''
            while len(chunk) < chunk_size:
                data = conn.recv(chunk_size - len(chunk))
                if not data:
                    print(f"[{addr}] Client closed connection unexpectedly")
                    return
                chunk += data

            if not chunk:
                print(f"[{addr}] Received empty chunk, closing connection")
                break

            total_received += len(chunk)
            chunks_received += 1
            print(f"[{addr}] Received chunk of {len(chunk)} bytes. Total received: {total_received} bytes")

            try:
                is_last_chunk = (chunk_size < CHUNK_SIZE)
                processed_chunk = process_data(chunk, operation, is_last_chunk)
                print(f"[{addr}] Processed chunk, size: {len(processed_chunk)} bytes")
                conn.sendall(len(processed_chunk).to_bytes(4, byteorder='big'))
                conn.sendall(processed_chunk)
                total_sent += len(processed_chunk)
                print(f"[{addr}] Sent processed chunk of {len(processed_chunk)} bytes. Total sent: {total_sent} bytes")
            except Exception as e:
                print(f"[{addr}] Error processing chunk: {e}")
                conn.sendall((0).to_bytes(4, byteorder='big'))  # Send 0 to indicate error
                break

    finally:
        conn.close()
        print(f"[{addr}] Connection closed. Total received: {total_received} bytes, Total sent: {total_sent} bytes")
        print(f"[{addr}] Total chunks processed: {chunks_received}")

def main():
    host = 'localhost'
    port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()
