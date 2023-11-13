import cv2

def main():
    # define a video capture object 
    video = cv2.VideoCapture(0)

    while True: 
	
        # Capture the video frame by frame 
        ret, frame = video.read() 

        # Display the resulting frame 
        cv2.imshow('frame', frame) 
        
        # 'q' key is set to quit
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    # After the loop release the cap object 
    video.release()
    # Destroy all the windows 
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()