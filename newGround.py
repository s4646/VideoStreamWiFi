import socket             
 
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

    msg = ""
    while msg != b'exit':
        
        msgFromServer = udp.recvfrom(buffer_size)
        server_IP = msgFromServer[1]
        msg = msgFromServer[0]
        print(f"Message from Server {server_IP}: {msg.decode()}")

    udp.close()

if __name__ == "__main__":
    main()