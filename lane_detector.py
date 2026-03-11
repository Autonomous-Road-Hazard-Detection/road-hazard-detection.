import cv2
import numpy as np

class LaneDetector:

    def detect_lane(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray,(5,5),0)

        edges = cv2.Canny(blur,50,150)

        height,width = edges.shape

        mask = np.zeros_like(edges)

        polygon = np.array([[
            (0,height),
            (width,height),
            (width,int(height*0.5)),
            (0,int(height*0.5))
        ]])

        cv2.fillPoly(mask,polygon,255)

        cropped = cv2.bitwise_and(edges,mask)

        return cropped


    def inside_lane(self,cx,cy,frame_shape):

        h,w = frame_shape[:2]

        lane_top = int(h*0.4)
        lane_bottom = h
        lane_left = int(w*0.2)
        lane_right = int(w*0.8)

        if lane_left < cx < lane_right and lane_top < cy < lane_bottom:
            return True

        return False