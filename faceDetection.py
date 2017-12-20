"""
This program detects face(s) in the video.
Video may be from webcam i.e. live from camera or can be pre-loaded.

"""

import cv2
from datetime import datetime as dt
import imutils

#Using Haar Cascade Classifier for face detection xml
cascade = cv2.CascadeClassifier("face_detection.xml")
video = cv2.VideoCapture(0) #initializes the first frame
a=0     #initial value of a set as 0, to count total frames
x1 = 0  #x1 used for determining position of face. Works on the delta (difference) between x ordinate of previous frame and current frame. 

"""
Main loop to run video.
Video is basically the continous capture of frames.
"""
while True:
    a =a+1
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converts color to greyscale image

    #Now to obtain the corner coordinates of face, we use cascade classifier.
    facePoints = cascade.detectMultiScale(gray_frame,
                                          scaleFactor=1.7, minNeighbors=10)
    """ Checks if the face has moved right, left or stayed in the same position"""
    for x, y, w, h in facePoints:
        if x-x1>50:
            print("Right")
        elif x-x1>0 and x-x1<50:
            print("Same")
        else:
            print("Left")
        cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 255, 0), 2) #makes rectangle around the face.
        
        x1 = x
    cv2.putText(frame, dt.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.imshow('Capture', cv2.resize(frame, (600, 500)))

    cv2.waitKey(1)
    if cv2.waitKey(1) == ord('q'):
        break
print(a)
video.release()
cv2.destroyAllWindows()
