import socket             
import cv2
import time
import numpy as np

port = 12345
buffer_size = 1024
ip_address = "localhost"

###
# Ground Station
# Server
###

def main():

    # Initiate sockets
    udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    tcp = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    print("Sockets initiated")

    # Bind sockets
    udp.bind((ip_address, port))
    tcp.bind((ip_address, port))
    tcp.listen(1)

    # Accept client connection
    c, client_IP = tcp.accept()
    print(f"Client IP Address: {client_IP}")

    # Receive frame size from client 
    number_of_chunks = int(c.recv(buffer_size).decode())

    print("START STREAMING")
    while True:
        
        # Receive frame
        data = b''
        for i in range(number_of_chunks):
            msgFromServer = udp.recvfrom(buffer_size)
            data += msgFromServer[0]

        try:
            # Decode frame
            data = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(data, 1)

            # Display the resulting frame 
            cv2.imshow('frame', frame) 
        
        except Exception as e:
            print(f"ERROR: {e}")
            # cv2.destroyAllWindows()
            udp.settimeout(0.1) # need to be called for every exception
            continue

        # 'q' key is set to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            

    udp.close()
    c.close()
    tcp.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()