from ultralytics import YOLO
import cv2
import numpy as np

from tracker import Tracker
from speed_estimator import SpeedEstimator
from hazard_detector import HazardDetector
from lane_detector import LaneDetector


model = YOLO("yolov8s.pt")

tracker = Tracker()
speed_estimator = SpeedEstimator()
hazard_detector = HazardDetector()
lane_detector = LaneDetector()

road_classes = {0,1,2,3,5,7,15,16}
automobile_classes = {1,2,3,5,7}

cap = cv2.VideoCapture(
r"C:\Users\chinn\OneDrive\Desktop\traffic videos\object on road.mp4"
)

while True:

    ret,frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame,(1280,720))

    lane_edges = lane_detector.detect_lane(frame)

    results = model(frame)[0]

    detections = []

    for box in results.boxes:

        x1,y1,x2,y2 = box.xyxy[0].tolist()
        conf = float(box.conf)
        cls = int(box.cls)

        if cls not in road_classes:
            continue

        detections.append([x1,y1,x2,y2,conf,cls])

    tracks = tracker.update(detections)

    if len(tracks) > 0:

        for xyxy,track_id,class_id in zip(
            tracks.xyxy,tracks.tracker_id,tracks.class_id
        ):

            x1,y1,x2,y2 = xyxy
            track_id = int(track_id)
            class_id = int(class_id)

            cx = int((x1+x2)/2)
            cy = int((y1+y2)/2)

            speed_estimator.update(track_id,cx,cy)

            speed = speed_estimator.get_speed(track_id)

            slow,stopped = hazard_detector.detect(track_id,speed)

            label = f"ID {track_id} {speed:.1f} km/h"
            color = (0,255,0)

            is_vehicle = class_id in automobile_classes

            if is_vehicle:

                if stopped:
                    label += " STOPPED VEHICLE"
                    color = (0,0,255)

                elif slow:
                    label += " SLOW VEHICLE"
                    color = (0,255,255)

            else:

                label = "OBJECT HAZARD"
                color = (255,0,255)

            cv2.rectangle(
                frame,
                (int(x1),int(y1)),
                (int(x2),int(y2)),
                color,
                2
            )

            cv2.putText(
                frame,
                label,
                (int(x1),int(y1)-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )


    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)

    edges = cv2.Canny(blur,50,150)

    contours,_ = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if 500 < area < 5000:

            x,y,w,h = cv2.boundingRect(cnt)

            cx = x + w//2
            cy = y + h//2

            if lane_detector.inside_lane(cx,cy,frame.shape):

                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,255),2)

                cv2.putText(
                    frame,
                    "ROAD OBSTACLE",
                    (x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255,0,255),
                    2
                )

    cv2.imshow("Road Hazard Detection System",frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()