import time

class InputBuffer:
    def __init__(self, max_time=0.7):
        self.buffer = []
        self.max_time = max_time

    def add(self, inputs):
        now = time.time()
        for i in inputs:
            self.buffer.append((i, now))
        self.cleanup()

    def cleanup(self):
        now = time.time()
        self.buffer = [(i, t) for i, t in self.buffer if now - t < self.max_time]

    def get(self):
        return [i for i, _ in self.buffer]