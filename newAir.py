import socket
import time
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
    number_of_chunks = (len(cv2.imencode('.jpg', frame)[1].tobytes()) // buffer_size) + 1
    # print("chunks:",number_of_chunks)
    c.send(str(number_of_chunks).encode())
    
    try:
        while True:
            
            # Encode frame
            ret, frame = video.read()
            data = cv2.imencode('.jpg', frame)[1].tobytes()

            # Send frame
            for i in range(number_of_chunks):
                udp.sendto(data[i*buffer_size : (i+1)*buffer_size], client_IP)

    except KeyboardInterrupt as e:    
        udp.close()
        c.close()
        tcp.close()
        video.release()
        print(f"\nError: {e}, Finished")

if __name__ == "__main__":
    main()