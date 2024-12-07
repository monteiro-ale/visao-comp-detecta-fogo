import cv2  # Library for openCV

# To access xml file which includes positive and negative images of fire
fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml')

# Start camera (use 0 for inbuilt or 1 for external USB camera)
vid = cv2.VideoCapture(0) 

# Uncomment to use a video file instead
# vid = cv2.VideoCapture("videos\\fire2.mp4")

while True:
    # Value in ret is True, ret = success of reading frame
    ret, frame = vid.read() 
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

    # Detect fire in the frame
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5) 

    # Highlight detected fire with rectangles
    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255, 0, 0), 2)
        print("Fire detected!")

    # Show the frame with rectangles
    cv2.imshow('Fire Detection', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the display window
vid.release()
cv2.destroyAllWindows()
#python fire-det-webcam.py