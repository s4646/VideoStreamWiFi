import cv2
import socket
import numpy as np

port = 12345
buffer_size = 1024
ip_address = "localhost"
index_length = 4

def main():

    # Create socket objects
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket initiated")

    # Bind the sockets to a specific address and port
    udp.bind((ip_address, port))
    tcp.bind((ip_address, port))
    print("Sockets binded")

    # Listen to socket and accept tcp connection from client
    tcp.listen(1)
    client_socket, client_address = tcp.accept()

    # Receive frame size from client
    data = b""
    data += client_socket.recv(buffer_size)
    number_of_chunks = int.from_bytes(data, "big")

    try:
        while True:
            
            # Get unsorted indexed data from client
            unorganised_data = []
            for i in range(number_of_chunks):
                packet = udp.recvfrom(buffer_size)[0]
                index = int.from_bytes(packet[:index_length], "big")
                data = packet[index_length:]
                unorganised_data.append((index, data))
                # if i != index: print("NOT ORGANISED!!!")
            
            # Sort frame's data
            data = sorted(unorganised_data)

            # Build and decode the frame
            frame = b''
            for segment in data:
                frame += segment[1]
            
            frame = np.frombuffer(frame, dtype=np.uint8)
            frame = cv2.imdecode(frame, 1)

            # Display the resulting frame 
            cv2.imshow('frame', frame)

            # 'q' key is set to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except Exception:
        cv2.destroyAllWindows()
        client_socket.close()
        tcp.close()
        udp.close()
        print("\nFinished")


if __name__ == "__main__":
    main()




    