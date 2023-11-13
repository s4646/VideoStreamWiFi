import socket             
 
port = 12345
buffer_size = 1024

###
# Ground Station
# Client
###

def main():

    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send a message to the server so your address will be known
    s.sendto(" ".encode(), ("localhost", port))

    msg = ""
    while msg != b'exit':
        
        msgFromServer = s.recvfrom(buffer_size)
        server_IP = msgFromServer[1]
        msg = msgFromServer[0]
        print(f"Message from Server {server_IP}: {msg.decode()}")

    s.close()

if __name__ == "__main__":
    main()