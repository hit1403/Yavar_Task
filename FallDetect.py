# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YbMJ2WMsp7WHU6N9MvYnvsZR4URLJI-0
"""

import cv2
import cvzone
import math
from ultralytics import YOLO

cap = cv2.VideoCapture("/content/fatboysf.mp4")

# Initialize YOLO model
model = YOLO('yolov8s-pose.pt')

classnames = ["person"]

# Define output video properties
output_width = 980
output_height = 740
output_fps = cap.get(cv2.CAP_PROP_FPS)
output_fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter('output_fall_detection.mp4', output_fourcc, output_fps, (output_width, output_height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (output_width, output_height))

    # Perform object detection
    results = model(frame)

    for info in results:
        parameters = info.boxes
        for box in parameters:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            confidence = box.conf[0]
            class_detect = box.cls[0]
            class_detect = int(class_detect)
            class_detect = classnames[class_detect]
            conf = math.ceil(confidence * 100)

            # Implement fall detection using the coordinates x1,y1,x2
            height = y2 - y1
            width = x2 - x1
            threshold = height - width

            # Bounding box and label
            if conf > 40 and class_detect == 'person':
                cvzone.cornerRect(frame, [x1, y1, width, height], l=30, rt=6)
                cvzone.putTextRect(frame, f'{class_detect}', [x1 + 8, y1 - 12], thickness=2, scale=2)

            # Fall detection message
            if threshold < 0:
                cvzone.putTextRect(frame, 'Fall Detected', [height, width], thickness=2, scale=2)

    # Write the processed frame to the output video
    output_video.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
output_video.release()
cv2.destroyAllWindows()
