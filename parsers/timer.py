from time import time

class Timer:
    def __init__(self):
        self.start()     
        
    def start(self):
        self.start_time = time()
        self.elapsed = 0

    def stop(self):
        self.elapsed = time() - self.start_time
        return self

    def __repr__(self):
        return f'Time elapsed: {self.elapsed:.2f} sec'