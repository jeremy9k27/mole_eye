import cv2   #include opencv library functions in python
import numpy as np

def avg_array(original_array):
    
    new_array = np.zeros_like(original_array, dtype=float)
   
    # Calculate averages based on specified conditions
    for m in [0,1]:
        for i in range(original_array.shape[1]):
            if i == 0:
                # For the first element, average with the next element
                new_array[m][i] = (original_array[m][i] + original_array[m][i + 1]) / 2
            elif i == (original_array.shape[1]) - 1:
                # For the last element, average with the previous element
                new_array[m][i] = (original_array[m][i] + original_array[m][i - 1]) / 2
            else:
                # For elements in the middle, average with the previous, current, and next elements
                new_array[m][i] = (original_array[m][i - 1] + original_array[m][i] + original_array[m][i + 1]) / 3

    return new_array.astype(int)

def classify(pitch):
   
    # i think the slope of the second half of the pitch is more informative of the pitch type
    #pitch = pitch[: , 0:int(pitch.shape[1]/2)]
    x = max(pitch[0]) - min(pitch[0])
    y = max(pitch[1]) - min(pitch[1])
    slope = y/x
    if slope < 0.5:
        type = "slider (sweeper)"
    elif slope < 1.1:
        type = "fastball"
    elif False:
        type = "slider (gyro)"
    else:
        type = "curveball"

    return [type, np.str_(x), np.str_(y)]
    

def disp_pitch(pitch_array, original):
    #print("successful")
    #black = np.zeros((480,640))
    onto = original
    
    for i in range(pitch_array.shape[1]):
        center = (pitch_array[0][i].astype(int), pitch_array[1][i].astype(int))
        #print(center)
        cv2.circle(onto, center, 5, 255, -1)

    text = classify(pitch_array)
    
    while True:
        cv2.putText(onto, text[0], (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(onto, "horiz", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(onto, text[1], (90, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(onto, "vert", (10, 430), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(onto, text[2], (90, 430), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    
        cv2.imshow("pitch map", onto)

        if cv2.waitKey(1) & 0xFF == ord('p'):
                original = original
                break
        

def process(pitch_array):
    print("before")
    print(pitch_array)
    i = 0
    limit = (pitch_array.shape[1])
    while i < limit -1:
        if ((abs(pitch_array[0][i+1] - pitch_array[0][i])) + (abs(pitch_array[1][i+1] - pitch_array[1][i])) < 60):
            i += 1
        else:
            pitch_array = np.delete(pitch_array, i+1, axis=1)
            limit += -1
    i = 0

    print("after")
    pitch_array = avg_array(pitch_array)
    print(pitch_array)
    return pitch_array
        
        
#Create an object to hold reference to camera video capturing
camera = 'http://192.168.0.17:4747/video'
#camera = 0

vidcap = cv2.VideoCapture(camera)

#check if connection with camera is successfully
if vidcap.isOpened():
    ret, frame = vidcap.read()  #capture a frame from live video

    # define the contrast and brightness value
    contrast = 0.6 # Contrast control
    brightness = 15 # Brightness control 
    # Define 'blue' range in HSV colorspace
    # center is 50?
    lower = np.array([31,22,30])
    upper = np.array([80,255,255])

    # mu = np.array([235, 212, 50])
    # delta = np.array([20, 20, 20])

    # lower = mu-delta
    # upper = mu+delta

    #i = 0
    i = 0
    k = 0
            
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
            ''''''
            if i == 0:
                hallucinations = np.zeros_like(color_mask)
                print(frame.shape)
                #num_rows = frame.shape[0]
                #num_cols = frame.shape[1]
                centroid_array = np.zeros((2,3))
                start = False
                stop = False
                onto1 = frame.copy()
                
                
            
            if i < 600:
                hallucinations = np.logical_or(hallucinations, color_mask).astype(int)
                
                i += 1 
                if i in [100,200,300,400,500,600,700,800,900,1000]:
                    print(i)
                

            if i == 600:
                #hallucinations = cv2.blur(hallucinations,(5,5))  
                #hallucinations[hallucinations > 0] = 1
                
                print("initialized")
                
                #print(color_mask.shape)
                i += 1  

            #cv2.imshow("hallucinations", 255 * hallucinations.astype(np.uint8))
           
            # calculate moments of binary image
            color_mask[hallucinations > 0] = 0
            frame_masked_gray[hallucinations > 0] = 0
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
                    #cv2.circle(frame, (cX, cY), 5, 255, -1)
                
                #cv2.circle(frame, (cX, cY), 5, 255, -1)
                    
                
                if k < 3:
                    centroid_array[0][k] = cX
                    centroid_array[1][k] = cY
                    k += 1

                else:
                    
                    start_con =  (centroid_array[0][0] > 480) & (centroid_array[1][0] < 240) & (centroid_array[0][1] > 480) & (centroid_array[1][1] < 240) & (((abs(centroid_array[0][-3] - centroid_array[0][-2])) + (abs(centroid_array[1][-3] - centroid_array[1][-2])) < 150) & ((abs(centroid_array[0][-2] - centroid_array[0][-1])) + (abs(centroid_array[1][-2] - centroid_array[1][-1])) < 150))
                    stop_con = ((abs(centroid_array[0][-3] - centroid_array[0][-2])) + (abs(centroid_array[1][-3] - centroid_array[1][-2])) > 60) & ((abs(centroid_array[0][-2] - centroid_array[0][-1])) + (abs(centroid_array[1][-2] - centroid_array[1][-1])) > 60) & ((abs(centroid_array[0][-3] - centroid_array[0][-1])) + (abs(centroid_array[1][-3] - centroid_array[1][-1])) > 60)

                    new_col = np.array([[cX], [cY]])
                    centroid_array = np.hstack((centroid_array, new_col))

                    if not start:
                        if start_con:
                            start = True
                            print("potential pitch detected")

                    if start:
                        if stop_con:
                            stop = True

                                                    
                    if not start:
                        centroid_array = centroid_array[: , 1:]
                    
                    if stop:
                        if centroid_array.shape[1] > 10:
                            print("pitch detected")
                            #print(centroid_array[:, :-1])

                            #process centroid array
                            centroid_array = process(centroid_array)
                            
                            #do math and display
                            disp_pitch(centroid_array, onto1)
                            
                        
                        else:
                            print("pitch not detected")


                        centroid_array = np.zeros((2,3))
                        start = False
                        stop = False
                        k = 0
                        onto1 = frame
                        #break




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





'''
4seam
[[451. 446. 441. 439. 436. 433. 432. 428. 427. 425. 304. 422. 423. 467.
  569.]
 [173. 177. 180. 184. 187. 190. 194. 199. 201. 204. 221. 210. 214. 207.
  152.]]
  
sweep
[[419. 418. 411. 411. 407. 401. 402. 400. 398. 397. 395. 397. 352. 279.]
 [149. 152. 152. 154. 162. 164. 165. 172. 174. 174. 173. 177. 168. 132.]]


 sink?
 [[431. 426. 422. 418. 414. 410. 409. 402. 402. 401. 397. 636. 563.]
 [ 93.  97. 101. 103. 105. 108. 108. 118. 120. 121. 124. 164. 143.]]


'''