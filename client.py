import socket
import os.path as path
import sys

IP = '127.0.0.1'  # change to the IP address of the server
PORT = 14008  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size


def get_file_size(file_name: str) -> int:
    size = 0
    try:
        # print(file_name)
        size = path.getsize(file_name)
    except FileNotFoundError as fnfe:
        print(fnfe)
        sys.exit(1)
    return size


def send_file(filename: str, address: (str, int)):
    # get the file size in bytes
    # TODO: section 2 step 2
    file_size = get_file_size(filename)
    # convert file_size to an 8-byte byte string using big endian
    # TODO: section 2 step 3
    byte_size = file_size.to_bytes(8, byteorder='big')
    byte_name = filename.encode()  # bytes(filename, 'utf-8')
    # create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # TODO: section 2 step 5
        # send the file size in the first 8-bytes followed by the bytes
        # for the file name to server at (IP, PORT)
        client_socket.connect(address)
        # TODO: section 2 step 6
        client_socket.send(byte_size + byte_name)
        # TODO: section 2 step 7
        auth = client_socket.recv(8)
        if auth == b'go ahead':
            # open the file to be transferred
            with open(file_name, 'rb') as file:
                # read the file in chunks and send each chunk to the server
                is_done = False
                while not is_done:
                    # TODO: section 2 step 8a
                    chunk = file.read(16)
                    print(chunk)
                    # TODO: section 2 step 8b
                    if len(chunk) > 0:
                        client_socket.send(chunk)
                    else:
                        is_done = True
        else:
            raise OSError('Bad server response - was not go ahead!')

    except OSError as e:
        print(f'An error occurred while sending the file:\n\t{e}')
    finally:
        print('successfully closing')
        client_socket.close()


if __name__ == "__main__":
    # get filename from cmd line
    if len(sys.argv) < 2:
        print(f'SYNOPSIS: {sys.argv[0]} <filename> [IP address]')
        sys.exit(1)
    file_name = sys.argv[1]  # filename from cmdline argument
    # if an IP address is provided on cmdline, then use it
    if len(sys.argv) == 3:
        IP = sys.argv[2]

    send_file(file_name, (IP, PORT))


