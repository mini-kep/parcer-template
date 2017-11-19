from time import time

class Timer:
    def __init__(self):
        self.start()
        
    def start(self):
        self.start_time = time()
        self.total_time = 0

    @property
    def elapsed(self):
        return time() - self.start_time
        
    def stop(self):
        self.total_time = self.elapsed
        return self

    def __repr__(self):
        return f'Time elapsed: {self.elapsed:.2f} sec'