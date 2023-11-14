import socket

port = 12345
buffer_size = 1024
server_address = "localhost"

###
# Air Station
# Server
###

def main():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Sockets initiated")
    
    udp.bind(("localhost", port))
    tcp.bind(("localhost", port))
    tcp.listen(1)
    print("Sockets binded to port", port)
    print("Waiting for client connection")
    
    # get client ip
    bytesAddressPair = udp.recvfrom(buffer_size)
    client_IP = bytesAddressPair[1]
    c, c_addr = tcp.accept()
    print(f"Client IP Address: {client_IP}")
    
    msg = ""
    while msg != "exit":
        
        msg = input()
        udp.sendto(msg.encode(), client_IP)

    udp.close()
    c.close()
    tcp.close()

if __name__ == "__main__":
    main()