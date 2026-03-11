import supervision as sv
import numpy as np

class Tracker:

    def __init__(self):
        self.tracker = sv.ByteTrack()

    def update(self, detections):

        if len(detections) == 0:
            return []

        detections = np.array(detections)

        sv_detections = sv.Detections(
            xyxy=detections[:, 0:4],
            confidence=detections[:, 4],
            class_id=detections[:, 5].astype(int)
        )

        tracks = self.tracker.update_with_detections(sv_detections)

        return tracks