import cv2   #include opencv library functions in python
import numpy as np

url = 'http://192.168.0.14:4747/video'

cap = cv2.VideoCapture(url)

while True:

    ret, frame = cap.read()

# Process the frame as desired

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):

        break

cap.release()

cv2.destroyAllWindows()