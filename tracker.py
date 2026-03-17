import supervision as sv
import numpy as np

class Tracker:

    def __init__(self):
        self.tracker = sv.ByteTrack()

    def update(self, detections):

        if len(detections) == 0:
            return sv.Detections(
                xyxy=np.empty((0, 4), dtype=np.float32),
                confidence=np.empty((0,), dtype=np.float32),
                class_id=np.empty((0,), dtype=np.int32),
            )

        detections = np.array(detections)

        sv_detections = sv.Detections(
            xyxy=detections[:, 0:4],
            confidence=detections[:, 4],
            class_id=detections[:, 5].astype(int)
        )

        tracks = self.tracker.update_with_detections(sv_detections)

        return tracks