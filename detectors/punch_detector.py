import time
import math

class PunchDetector:
    def __init__(self, threshold=8.0, cooldown=0.3):
        self.threshold = threshold
        self.cooldown = cooldown
        self.last_punch_time = 0

    def detect(self, lx, ly, lz):
        magnitude = math.sqrt(lx**2 + ly**2 + lz**2)
        current_time = time.time()

        if magnitude > self.threshold:
            if current_time - self.last_punch_time > self.cooldown:
                self.last_punch_time = current_time
                return True

        return False