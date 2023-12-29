import cv2   #include opencv library functions in python
import numpy as np


#Create an object to hold reference to camera video capturing
camera = 'http://192.168.0.19:4747/video'
#camera = 0

vidcap = cv2.VideoCapture(camera)

#check if connection with camera is successfully
if vidcap.isOpened():
    ret, frame = vidcap.read()  #capture a frame from live video

    # define the contrast and brightness value
    contrast = 0.6 # Contrast control
    brightness = 15 # Brightness control 
    # Define 'blue' range in HSV colorspace
    lower = np.array([35,30,30])
    upper = np.array([65,255,255])

    # mu = np.array([235, 212, 50])
    # delta = np.array([20, 20, 20])

    # lower = mu-delta
    # upper = mu+delta

    #i = 0

    #halluncinations = np.zeros            

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

            # Bitwise-AND mask and original image
            frame_masked = cv2.bitwise_and(hsv,hsv, mask= color_mask)
            #cv2.imshow("frame masked", cv2.cvtColor(frame_masked, cv2.COLOR_HSV2BGR))

            # frame_masked = cv2.cvtColor(frame_masked, cv2.COLOR_BGR2GRAY)
            # print(frame_masked.mean())
            frame_masked_gray = (np.floor_divide(frame_masked[:, :, 1], 2)) + (np.floor_divide(frame_masked[:,:,2] ,2 ))
            # print(frame_masked_gray.max())

            
            #find hallucinations   
            i = 0
            
            if i == 0:
                hallucinations = np.zeros_like(color_mask)
                #num_rows = frame.shape[0]
                #num_cols = frame.shape[1]
                centroid_array = np.zeros(3,2)
                start = False
                stop = False
                
                
            
            if i < 2000:
                hallucinations = np.logical_or(hallucinations, color_mask).astype(int)
                i += 1 
                print(i)
                

            if i == 2000:
                print("initialized") 
                #print(color_mask.shape)
                i += 1  
           
            # calculate moments of binary image
            color_mask[hallucinations == 1] = 0
            frame_masked_gray[hallucinations == 1] = 0
            M = cv2.moments(frame_masked_gray)


            # calculate x,y coordinate of center
            if (M["m00"] > 0):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                '''#find distances to centroid
                for row in range(num_rows):
                    for col in range(num_cols):
                        if color_mask[row,col] == 1:
                            distance = 5
                            if distance > 10:
                                frame_masked_gray[row, col] = 0
                '''

                black_frame = np.zeros_like(color_mask)
                cv2.circle(black_frame, (cX, cY), 40, 255, -1)
                frame_masked_gray[black_frame == 0] = 0
                #cv2.imshow("black", black_frame)

                
                #recompute centroid
                M = cv2.moments(frame_masked_gray)
                if (M["m00"] > 0):
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                    #print(cX, cY)
                    cv2.circle(frame, (cX, cY), 5, 255, -1)
                
                #cv2.circle(frame, (cX, cY), 5, 255, -1)
                    
                
                for k in range(3):
                    fill centroid array

                if start == False:
                    if trigger:
                        start = True

                if start == True:
                    if trigger2:
                        stop = True

                if not start:
                    rewrite 3x2
                
                if start:
                    append into nx2

                if stop:
                    centroid_array = np.zeros(3,2)
                    start = False
                    stop = False


            cv2.imshow("Frame2", frame)
            cv2.imshow("frame_masked_gray", frame_masked_gray)
            #cv2.imshow("frame masked", cv2.cvtColor(frame_masked, cv2.COLOR_HSV2BGR))

            # if np.any(color_mask == 255) == True:
            #     print("detected")
            # else:
            #     print("none")

            #press 'q' to break out of the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    #print error if frame capturing was unsuccessful
    else:
        print("Error : Failed to capture frame")

# print error if the connection with camera is unsuccessful
else:
    print("Cannot open camera")

vidcap.release()

cv2.destroyAllWindows()