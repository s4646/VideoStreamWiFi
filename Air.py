import cv2
import pickle
import socket
import struct

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
    frame_size = len(pickle.dumps(frame))
    number_of_chunks = struct.pack("L", (frame_size) // buffer_size + 1)
    tcp.send(number_of_chunks)

    tcp.close()
    udp.close()
    video.release()

if __name__ == "__main__":
    main()