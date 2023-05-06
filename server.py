import socket
import os
import sys

IP = '127.0.0.1'  # default IP address of the server
PORT = 14008  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size


def get_file_info(data: bytes) -> (str, int):
    return data[8:].decode(), int.from_bytes(data[:8], byteorder='big')


def upload_file(conn_socket: socket, file_name: str, file_size: int):
    # create a new file to store the received data
    file_name += '.temp'
    # please do not change the above line!
    with open(file_name, 'wb') as file:
        retrieved_size = 0
        try:
            while retrieved_size < file_size:
                # TODO: section 1 step 6a
                retrieved_chunk = conn_socket.recv(BUFFER_SIZE)
                # TODO: section 1 stop 6b
                retrieved_size += len(retrieved_chunk)
                # TODO: section 1 stop 6c
                file.write(retrieved_chunk)
        except OSError as oe:
            print(oe)
            os.remove(file_name)


def start_server(ip, port):
    # create a TCP socket object
    print(IP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    print(f'Server ready and listening on {ip}:{port}')

    try:
        while True:
            (conn_socket, addr) = server_socket.accept()
            # TODO: section 1 step 2
            # expecting an 8-byte byte string for file size followed by file name
            data = conn_socket.recv(BUFFER_SIZE)

            # TODO: section 1 step 3
            (file_name, file_size) = get_file_info(data)
            print(f'Received: {file_name} with size = {file_size}')
            # TODO: section 1 step 4
            conn_socket.send(b'go ahead')
            upload_file(conn_socket, file_name, file_size)
            conn_socket.close()
    except KeyboardInterrupt as ki:
        pass
    finally:
        server_socket.close()


if __name__ == "__main__":
    # get IP address from cmd line
    if len(sys.argv) == 2:
        IP = sys.argv[1]  # IP from cmdline argument

    print('here')
    start_server(IP, PORT)
