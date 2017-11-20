from time import time

#class Timer:
#    def __init__(self):
#        self.start()
#        
#    def start(self):
#        self.start_time = time()
#        self.total_time = 0
#        self.is_running = True
#
#    @property
#    def elapsed(self):
#        if self.is_running:
#            return time() - self.start_time
#        else:
#            return self.total_time
#        
#    def stop(self):
#        self.total_time = self.elapsed
#        self.is_running = False
#        
#    def __repr__(self):
#        return f'Time elapsed: {self.elapsed:.2f} sec'
#    
#    
def now():
    return time()
    
class Timer:
    def __enter__(self):
        self.t = now()
        return self

    def __exit__(self, type, value, traceback):
        self.e = now()

    @property
    def elapsed(self):
        return (self.e - self.t)

    def __repr__(self):
        return f'{self.elapsed:.3}'    