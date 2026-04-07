class DirectionDetector:
    def detect(self, roll, pitch):
        if roll > 45:
            return "RIGHT"
        elif roll < -45:
            return "LEFT"
        elif pitch > 45:
            return "UP"
        elif pitch < -45:
            return "DOWN"
        return None