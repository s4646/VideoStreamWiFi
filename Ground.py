import pickle
import socket
import struct
import cv2

port = 12345
buffer_size = 1024
ip_address = "localhost"

def main():

    # Create socket objects
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket initiated")

    # Bind the sockets to a specific address and port
    udp.bind((ip_address, port))
    tcp.bind((ip_address, port))
    print("Sockets binded")

    # Listen to socket and accept tcp connection from client
    tcp.listen(1)
    client_socket, client_address = tcp.accept()

    # Receive frame size from client
    data = b""
    payload_size = struct.calcsize("L")
    while len(data) < payload_size:
        data += client_socket.recv(buffer_size)
    msg = struct.unpack("L", data)[0]

    print(msg)

    client_socket.close()
    tcp.close()
    udp.close()

if __name__ == "__main__":
    main()




    