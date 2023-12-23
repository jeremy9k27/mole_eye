import cv2   #include opencv library functions in python
import numpy as np


#Create an object to hold reference to camera video capturing
vidcap = cv2.VideoCapture(0)

#check if connection with camera is successfully
if vidcap.isOpened():
    ret, frame = vidcap.read()  #capture a frame from live video

    # define the contrast and brightness value
    contrast = 0.5 # Contrast control
    brightness = 15 # Brightness control 
    # Define 'blue' range in HSV colorspace
    lower = np.array([80,40,40])
    upper = np.array([100,255,255])

    # mu = np.array([235, 212, 50])
    # delta = np.array([20, 20, 20])

    # lower = mu-delta
    # upper = mu+delta

            

    #check whether frame is successfully captured
    if ret:
        # continue to display window until 'q' is pressed
        while(True):
            ret, frame = vidcap.read()  #capture a frame from live video
            
            # Adjust frame
            frame = cv2.addWeighted(frame, contrast, frame, 0, brightness)  
            
            # Find blue   
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            color_mask = cv2.inRange(hsv, lower, upper)
            # color_mask = cv2.inRange(frame, lower, upper)

            # print(color_mask)
            cv2.imshow("Frame", color_mask)
            cv2.imshow("Frame2", frame)
            # cv2.imshow("Frame", frame)
               
            if np.any(color_mask == 255) == True:
                print("detected")
            else:
                print("none")

            #press 'q' to break out of the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    #print error if frame capturing was unsuccessful
    else:
        print("Error : Failed to capture frame")

# print error if the connection with camera is unsuccessful
else:
    print("Cannot open camera")