"""
This program is able to detect any motion in any scenario.
Also, it is able to plot the time graph for the time, motion was detected.

"""

import cv2
import time
from datetime import datetime as dt
import pandas
import imutils

status_list = [None, None]
time_list = []
first_frame = None
time_dataFrame = pandas.DataFrame(columns=["Start Time", "End Time"])

capture = cv2.VideoCapture(0)
time.sleep(1)


while True:
    check, frame = capture.read()
    entry_status = 0 #entry status of 0 means the no motion is recorded and 1 is for object present in frame.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converts color frame to grayscale frame 
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    text= "Room occupied"

    if first_frame is None: #if there is no first_frame present then 'gray' is made the first_frame.
        first_frame = gray
        continue

    deltaFrame = cv2.absdiff(first_frame, gray) #gives the difference between the first frame recorded by the camera and the current running frame.
    resizedDeltaFrame = cv2.resize(deltaFrame, (600, 500))
    threshold_frame = cv2.threshold(resizedDeltaFrame, 55, 255, cv2.THRESH_BINARY)[1] #the delta frame is passed through threshold filter, which makes the image in just black or white.
    threshold_frame = cv2.dilate(threshold_frame, None, iterations=2)

    (_, cntr, _) = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #contours are extracted

"""
This loop makes the rectangle around the contour coordinates,
contours are the difference between first frame and the current frame.
"""
    for contour in cntr:
        if cv2.contourArea(contour) < 1000:
            continue
        entry_status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 255, 0), 2)
        text = "Occupied"

        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, dt.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

    """Further it adds the status of the room in the array, to make the time plot.
        It resets after it has got 1000 entries and entry status is 0.
        This enters the time stamp for the entry and exit of object in and from the frame.
    """
    status_list.append(entry_status)

    status_list[-10:]

    if status_list[-2] == 0 and status_list[-1] == 1: #entry time-stamp, if current entry status is 1 and the previous entry status is 0, then it means an object has entered the frame.
        time_list.append(dt.now())

    if status_list[-2] == 1 and status_list[-1] == 0: #exit time-stamp, if current entry status is 0 and the previous entry status is 1, then it means an object has left the frame.
        time_list.append(dt.now())

    if len(status_list) > 1000 and entry_status == 0:
        status_list[:] = [None, None]

    # cv2.imshow("Delta Frame", resizedDeltaFrame)
    cv2.imshow("Output", cv2.resize(frame,(600,500)))
    # cv2.imshow("Threshold Frame",threshold_frame)
    cv2.waitKey(1)

    if cv2.waitKey(1) == ord("q"):
        if entry_status == 1:
            time_list.append(dt.now())
        break

#enters the values from time_list into time_dataFrame for making the time graph
for i in range(0, len(time_list), 2):
    time_dataFrame = time_dataFrame.append({"Start Time": time_list[i], "End Time": time_list[i + 1]},
                                           ignore_index=True)

time_dataFrame.to_csv("Time Chart.csv")

capture.release()
cv2.destroyAllWindows()


