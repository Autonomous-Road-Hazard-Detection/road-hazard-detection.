import math

class SpeedEstimator:

    def __init__(self, meter_per_pixel=0.02, fps=30):

        self.mpp = meter_per_pixel
        self.fps = fps
        self.track_history = {}

    def update(self, track_id, cx, cy):

        if track_id not in self.track_history:
            self.track_history[track_id] = []

        self.track_history[track_id].append((cx, cy))

        if len(self.track_history[track_id]) > 10:
            self.track_history[track_id].pop(0)

    def get_speed(self, track_id):

        history = self.track_history.get(track_id, [])

        if len(history) < 2:
            return 0

        x1, y1 = history[0]
        x2, y2 = history[-1]

        pixel_distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)

        meter_distance = pixel_distance * self.mpp

        time_elapsed = len(history) / self.fps

        speed_mps = meter_distance / time_elapsed

        speed_kmph = speed_mps * 3.6

        return speed_kmph