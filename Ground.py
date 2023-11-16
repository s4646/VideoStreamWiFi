import cv2
import numpy as np
import socket
import struct

port = 12345
server_address = "localhost"

# Create a UDP socket
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp.bind((server_address, port))

while True:
    try:
        # Receive data length first
        data_len, addr = udp.recvfrom(struct.calcsize("<L"))

        # Then receive data
        data, addr = udp.recvfrom(struct.unpack("<L", data_len)[0])

        # Decode data as jpg
        frame = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            udp.close()
            break

    except Exception as e: 
        if type(e) == KeyboardInterrupt:     
            cv2.destroyAllWindows()
            udp.close()
        else:
            continue