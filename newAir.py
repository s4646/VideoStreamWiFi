import socket
import time
import cv2


port = 12345
buffer_size = 1024
server_address = "localhost"

###
# Air Station
# Client
###

def main():

    # Define a video capture object 
    video = cv2.VideoCapture(0)
    
    # Initiate sockets
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Sockets initiated")
    
    # Bind sockets
    udp.connect((server_address, port))
    tcp.connect((server_address, port))

    print("Sockets connected to port", port)

    # Get frame size
    ret, frame = video.read()
    number_of_chunks = (len(cv2.imencode('.jpg', frame)[1].tobytes()) // buffer_size) + 1
    # print("chunks:",number_of_chunks)
    tcp.send(str(number_of_chunks).encode())
    
    print("START STREAMING")
    try:
        while True:
            
            # Encode frame
            ret, frame = video.read()
            data = cv2.imencode('.jpg', frame)[1].tobytes()

            # Send frame
            for i in range(number_of_chunks):
                udp.sendto(data[i*buffer_size : (i+1)*buffer_size], (server_address, port))

    except KeyboardInterrupt as e:    
        udp.close()
        tcp.close()
        video.release()
        print(f"\nFinished")

if __name__ == "__main__":
    main()