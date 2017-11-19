#class Timer:
#    def __init__(self):
#        self.start()     
#        
#    def start(self):
#        self.start_time = time()
#        self.elapsed = 0
#
#    def stop(self):
#        self.elapsed = time() - self.start_time
#        return self
#
#    def __repr__(self):
#        return f'Time elapsed: {self.elapsed:.3} sec.'

def test_Timer_elapsed_property_retruns_expected_float():
    t = Timer()
    delay = 0.1
    sleep(delay)
    t.stop()
    assert isinstance(t.elapsed, float)
    assert t.elapsed >= delay  