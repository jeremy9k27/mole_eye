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
   
    pitch = pitch[: , 0:int(pitch.shape[1]/3)]
    x = max(pitch[0]) - min(pitch[0])
    y = max(pitch[1]) - min(pitch[1])
    slope = y/x

    if y > 50:
        type = 'curveball'
    elif y > 35:
      
        type = 'fastball'
    else:
        type = 'slider (sweeper)'

    '''
    if slope < 0.45:
        type = "slider (sweeper)"
    elif slope < 0.9:
        type = "fastball"
    elif False:
        type = "slider (gyro)"
    else:
        type = "curveball"
    '''

    return [type, np.str_(x), np.str_(y)]

def disp_pitch(pitch_array, original):
    #print("successful")
    #black = np.zeros((480,640))
    onto = original
    
    for i in range(pitch_array.shape[1]):
        center = (pitch_array[0][i].astype(int), pitch_array[1][i].astype(int))
        #print(center)
        cv2.circle(onto, center, 5, (255,255,255), -1)

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

curveball1 = [[617, 610, 597, 586, 575, 565, 555, 546, 537, 529, 523, 518, 515, 511, 506, 503, 499, 496, 492, 489, 486, 484, 480, 475, 470, 466, 465, 465, 465, 465, 465, 465, 466, 467], [55, 59, 68, 76, 84, 91, 99, 108, 116, 123, 129, 134, 139, 144, 149, 152, 157, 162, 167, 169, 174, 179, 185, 191, 200, 207, 209, 210, 211, 213, 214, 216, 218, 220]]
fastball1 = [[611, 599, 578, 561, 547, 534, 525, 517, 510, 504, 499, 494, 490, 487, 484, 482, 477, 474, 472, 473, 471, 470, 470, 469, 469, 468], [153, 157,165,171,175,179,182,185,188,199,193,196,198,200,202,203,207,211,214,215,216,217,218,220,221,222]]
sweeper1 = [[624,617,604,591,580,569,559,550,542,533,524,516,510,503,496,488,482,478,475,473], [167,168,171,174,177,180,183,186,189,193,197,201,204,208,213,218,223,226,229,231]]

def disp_pitch_test(pitch_array):
    #print("successful")
    black = np.zeros((480,640))
    
    for i in range(pitch_array.shape[1]):
        cv2.circle(black, (pitch_array[0][i], pitch_array[1][i]), 5, (255,255,255), -1)

    text = classify(pitch_array)
    
    while True:
        cv2.putText(black, text[0], (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(black, "horiz", (10, 430), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(black, text[1], (90, 430), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(black, "vert", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(black, text[2], (90, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        cv2.imshow("pitch map", black)

        if cv2.waitKey(1) & 0xFF == ord('p'):
                break

disp_pitch_test(avg_array(process(np.array(curveball1))))
#disp_pitch(avg_array(process(np.array(fastball1)))) 
#disp_pitch(avg_array(process(np.array(sweeper1))))
