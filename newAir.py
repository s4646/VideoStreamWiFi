import socket
import pickle
import cv2

port = 12345
buffer_size = 1024
server_address = "localhost"

###
# Air Station
# Server
###

def main():

    # Define a video capture object 
    video = cv2.VideoCapture(0)
    
    # Initiate sockets
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Sockets initiated")
    
    # Bind sockets
    udp.bind(("localhost", port))
    tcp.bind(("localhost", port))
    tcp.listen(1)
    print("Sockets binded to port", port)
    print("Waiting for client connection")
    
    # Get client IP
    bytesAddressPair = udp.recvfrom(buffer_size)
    client_IP = bytesAddressPair[1]
    c, c_addr = tcp.accept()
    print(f"Client IP Address: {client_IP}")

    # Get frame size
    ret, frame = video.read()
    number_of_chunks = (len(pickle.dumps(frame)) // buffer_size) + 1
    print("chunks:",number_of_chunks)
    c.send(str(number_of_chunks).encode())
    
    msg = ""
    while msg != "exit":
        
        msg = input()
        udp.sendto(msg.encode(), client_IP)

    udp.close()
    c.close()
    tcp.close()

if __name__ == "__main__":
    main()