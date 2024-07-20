import cv2
import time
import numpy as np

camera0 = 'http://192.168.0.16:4747/video'
camera1 = 'http://192.168.0.28:4747/video'

cap1 = cv2.VideoCapture(camera0)
cap2 = cv2.VideoCapture(camera1)

if not cap1.isOpened() or not cap2.isOpened():
    print("Could not open one or both cameras")
    exit()

def get_frame(cap):
    ret, frame = cap.read()
    if ret and frame is not None and frame.size > 0:
        return frame, time.time()
    return None, 9999

while True:
    frame1, time1 = get_frame(cap1)
    frame2, time2 = get_frame(cap2)

    if frame1 is None or frame2 is None:
        print("Failed to grab frame from one or both cameras")
        continue  # Skip this iteration and try again

    # Ensure frames are within a small time window (e.g., 50ms)
    attempts = 0
    while abs(time1 - time2) > 0.05 and attempts < 10:
        if time1 < time2:
            frame1, time1 = get_frame(cap1)
        else:
            frame2, time2 = get_frame(cap2)
        
        if frame1 is None or frame2 is None:
            print("Failed to synchronize frames")
            break
        attempts += 1

    if frame1 is None or frame2 is None:
        continue  # Skip this iteration and try again

    # Resize frames to the same size (optional)
    try:
        if isinstance(frame1, np.ndarray) and frame1.size > 0:
            frame1 = cv2.resize(frame1, (640, 480))
        else:
            raise ValueError("Invalid frame1")
        
        if isinstance(frame2, np.ndarray) and frame2.size > 0:
            frame2 = cv2.resize(frame2, (640, 480))
        else:
            raise ValueError("Invalid frame2")
    except (cv2.error, ValueError) as e:
        print(f"Error resizing frames: {e}. Skipping this iteration.")
        continue

    # Combine frames horizontally
    try:
        combined_frame = cv2.hconcat([frame1, frame2])
    except cv2.error as e:
        print(f"Error combining frames: {e}. Skipping this iteration.")
        continue

    cv2.imshow('Combined Frame', combined_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap1.release()
cap2.release()
cv2.destroyAllWindows()