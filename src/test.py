import cv2
camera0 = 'http://192.168.0.16:4747/video'
camera1 = 'http://192.168.0.27:4747/video'

# Open the first camera
cap1 = cv2.VideoCapture(camera0)
# Open the second camera
cap2 = cv2.VideoCapture(camera1)

if not cap1.isOpened():
    print("Could not open camera 0")
    exit()

if not cap2.isOpened():
    print("Could not open camera 1")
    exit()

while True:
    # Capture frame-by-frame from both cameras
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1:
        print("Failed to grab frame from camera 0")
        break

    if not ret2:
        print("Failed to grab frame from camera 1")
        break

    # Resize frames to the same size (optional)
    frame1 = cv2.resize(frame1, (640, 480))
    frame2 = cv2.resize(frame2, (640, 480))

    # Combine frames horizontally
    combined_frame = cv2.hconcat([frame1, frame2])

    # Display the resulting frame
    cv2.imshow('Combined Frame', combined_frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap1.release()
cap2.release()
cv2.destroyAllWindows()
