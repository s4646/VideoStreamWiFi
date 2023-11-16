import cv2
import numpy as np
import socket
import struct

port = 12345
server_address = "localhost"

# Create a UDP socket
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Connect to server
udp.connect((server_address, port))

# Create video capture
cap = cv2.VideoCapture(0)  # 0 for webcam

try:
    while cap.isOpened():
        ret = False
        while not ret: ret, frame = cap.read()

        # Encode frame as jpg, then send it over UDP
        result, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        data = frame.tobytes()

        # Send data length first
        udp.sendto(struct.pack("L", len(data)), (server_address, port))

        # Then data
        udp.sendto(data, (server_address, port))

except KeyboardInterrupt:
    cap.release()
    udp.close()