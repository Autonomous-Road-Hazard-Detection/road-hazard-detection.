class HazardDetector:

    def __init__(self):

        self.slow_counter = {}
        self.stop_counter = {}

        self.slow_speed = 15
        self.stop_speed = 3

        self.slow_frames = 60
        self.stop_frames = 50

    def detect(self, track_id, speed):

        if track_id not in self.slow_counter:
            self.slow_counter[track_id] = 0

        if track_id not in self.stop_counter:
            self.stop_counter[track_id] = 0

        slow = False
        stopped = False

        if speed < self.slow_speed:
            self.slow_counter[track_id] += 1
        else:
            self.slow_counter[track_id] = 0

        if speed < self.stop_speed:
            self.stop_counter[track_id] += 1
        else:
            self.stop_counter[track_id] = 0

        if self.stop_counter[track_id] > self.stop_frames:
            stopped = True

        elif self.slow_counter[track_id] > self.slow_frames:
            slow = True

        return slow, stopped