import cv2
import socket

port = 12345
buffer_size = 1024
server_address = "localhost"

def main():
    
    # Capture video from the webcam
    video = cv2.VideoCapture(0)
    print("Video initiated")

    # Create socket objects
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket initiated")

    # Connect to the server
    udp.connect((server_address, port))
    tcp.connect((server_address, port))
    print("Connected to the server")

    # Send frame size to server
    ret = False
    while not ret: ret, frame = video.read()
    frame_size = len(cv2.imencode('.jpg', frame)[1].tobytes())
    number_of_chunks = ((frame_size) // buffer_size + 1)
    tcp.send(number_of_chunks.to_bytes(4, "big"))

    try:
        while video.isOpened():
            
            # Get frame from video capture
            ret = False
            while not ret: ret, frame = video.read()

            # Encode frame
            data = cv2.imencode('.jpg', frame)[1].tobytes()
            
            for i in range(number_of_chunks):
                
                # Send indexed frame segment
                index = i.to_bytes(4, "big")
                segment_size = buffer_size - len(index)
                if i == 0:
                    frame_segment = data[0 : segment_size]
                else:
                    frame_segment = data[i*segment_size : (i+1)*segment_size]
                
                udp.sendto(index + frame_segment, (server_address, port))
    
    except KeyboardInterrupt:
        tcp.close()
        udp.close()
        video.release()
        print("\nFinished")

if __name__ == "__main__":
    main()