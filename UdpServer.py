import socket

port = 12345
buffer_size = 1024

###
# Air Station
# Server
###

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Socket initiated")
    
    s.bind(("localhost", port))
    print("Socket binded to port", port)
    print("Waiting for client connection")
    
    # Receive a message from a client to get its IP
    bytesAddressPair = s.recvfrom(buffer_size)
    client_IP = bytesAddressPair[1]
    print(f"Client IP Address: {client_IP}")
    
    msg = ""
    while msg != "exit":
        
        msg = input()
        s.sendto(msg.encode(), client_IP)

    s.close()

if __name__ == "__main__":
    main()