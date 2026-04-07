import time

class InputBuffer:
    def __init__(self, max_time=0.5):
        self.buffer = []
        self.max_time = max_time

    def add(self, input):
        now = time.time()
        self.buffer.append((input, now))
        self.cleanup()

    def cleanup(self):
        now = time.time()
        self.buffer = [
            (i, t) for i, t in self.buffer
            if now - t < self.max_time
        ]

    def get_inputs(self):
        return [i for i, _ in self.buffer]