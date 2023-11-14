import cv2
import socket

###
# Ground Station
# Client
###

port = 12345
buffer_size = 1024
server_address = "localhost"

def main():

    # Inititate camera connection
    print("Connecting to server")
    video = cv2.VideoCapture(f'udp://{server_address}:{port}')
    print("Connected!")
    
    while True:

        # Capture the video frame by frame 
        ret, frame = video.read()
        if ret:
            # Display the resulting frame
            cv2.imshow('frame', frame)
            # 'q' key is set to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()