import socket, cv2

port = 12345
buffer_size = 1024
ip_address = "localhost"

###
# Air Station
# Server
###

def main():

    # Inititate camera
    video = cv2.VideoCapture(0)
    print("Video initiated")

    # Initiate socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Socket initiated")

    # Bind and wait for client connection
    # s.bind((ip_address, port))
    # print("Socket binded to port", port)
    # print("Waiting for client connection")
    
    # # Receive a message from a client to get its IP
    # bytesAddressPair = s.recvfrom(buffer_size)
    # client_IP = bytesAddressPair[1]
    # print(f"Client IP Address: {client_IP}")
    
    try:
        while True:
            
            # Capture the video frame by frame and encode the frames
            ret, frame = video.read()
            frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

            # Divide frame to chunks 
            number_of_chunks = (len(frame_bytes)//buffer_size) + 1
            chunks = []
            for i in range(number_of_chunks):
                chunks.append(frame_bytes[i*buffer_size : (i+1)*buffer_size])

            # Send chunks to client
            for chunk in chunks:
                s.sendto(chunk, (ip_address, port))
    except KeyboardInterrupt:
        # After the loop release the cap object and close socket
        video.release()
        s.close()
        print("\nFinished")

if __name__ == "__main__":
    main()