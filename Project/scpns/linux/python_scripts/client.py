import socket
import os
from tqdm import tqdm

CHUNK_SIZE = 1048576  # 64 KB, must match server's CHUNK_SIZE

def send_file(filename, operation):
    host = '192.168.1.50'
    port = 8080

    print(f"Checking file: {filename}")
    if not os.path.exists(filename):
        print(f"Error: File {filename} does not exist!")
        return

    file_size = os.path.getsize(filename)
    print(f"File size: {file_size} bytes")
    output_filename = f"{filename}.enc" if operation == 'encrypt' else filename[:-4]

    print(f"Connecting to {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4 * CHUNK_SIZE)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4 * CHUNK_SIZE)
        
        s.connect((host, port))
        print(f"Connected. Sending operation byte: {'0' if operation == 'encrypt' else '1'}")
        s.sendall(b'\x00' if operation == 'encrypt' else b'\x01')

        print("Waiting for acknowledgement")
        ack = s.recv(2)
        print(f"Received acknowledgement: {ack}")
        if ack != b'OK':
            print("Did not receive correct acknowledgement from server")
            return

        total_sent = 0
        total_received = 0

        print(f"Opening file: {filename}")
        try:
            with open(filename, 'rb') as f:
                print("File opened successfully")
                with open(output_filename, 'wb') as out_f:
                    with tqdm(total=file_size, unit='B', unit_scale=True, desc="Sending") as pbar_send, \
                         tqdm(total=None, unit='B', unit_scale=True, desc="Receiving") as pbar_recv:
                        
                        while True:
                            chunk = f.read(CHUNK_SIZE)
                            if not chunk:
                                print("Finished reading file")
                                break
                            chunk_size = len(chunk)
                            print(f"Read chunk of size: {chunk_size}")
                            print(f"Sending chunk size: {chunk_size}")
                            s.sendall(chunk_size.to_bytes(4, byteorder='big'))
                            print(f"Sending chunk of {chunk_size} bytes")
                            s.sendall(chunk)
                            total_sent += chunk_size
                            pbar_send.update(chunk_size)

                            print("Waiting for processed chunk size")
                            size_data = s.recv(4)
                            if not size_data:
                                print("Server closed connection")
                                break
                            chunk_size = int.from_bytes(size_data, byteorder='big')
                            if chunk_size == 0:
                                print("Server reported an error processing the chunk")
                                break
                            print(f"Receiving processed chunk of {chunk_size} bytes")
                            
                            processed_chunk = b''
                            while len(processed_chunk) < chunk_size:
                                data = s.recv(chunk_size - len(processed_chunk))
                                if not data:
                                    print("Server closed connection unexpectedly")
                                    break
                                processed_chunk += data
                            
                            out_f.write(processed_chunk)
                            total_received += len(processed_chunk)
                            pbar_recv.update(len(processed_chunk))
        except IOError as e:
            print(f"Error opening or reading file: {e}")
            return

    print(f"\nProcessed file saved as {output_filename}")
    print(f"Total sent: {total_sent} bytes, Total received: {total_received} bytes")

def main():
    filename = "test_files/2mb.txt"
    operation = "encrypt"  # or "encrypt"
    send_file(filename, operation)

if __name__ == "__main__":
    main()