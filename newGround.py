import socket             
import cv2
import numpy as np

port = 12345
buffer_size = 1024
server_address = "localhost"

###
# Ground Station
# Client
###

def main():

    udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    tcp = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    udp.connect((server_address, port))
    tcp.connect((server_address, port))
    
    # Send a message to the server so your address will be known
    udp.sendto(" ".encode(), ("localhost", port))

    number_of_chunks = int(tcp.recv(buffer_size).decode())


    while True:
        
        # Receive frame
        data = b''
        for i in range(number_of_chunks):
            msgFromServer = udp.recvfrom(buffer_size)
            data += msgFromServer[0]

        
        # Decode frame
        data = np.fromstring(data, dtype=np.uint8)
        frame = cv2.imdecode(data, 1)

        try:
            # Display the resulting frame 
            cv2.imshow('frame', frame) 
        
        except Exception as e:
            continue
        
        # 'q' key is set to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            

    udp.close()
    tcp.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()