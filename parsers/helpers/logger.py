class Logger(object):
    """Print comments to console."""    
    def __init__(self, silent=True):
        self.silent = silent
    
    def echo(self, msg='', t=None):
        if t:
            msg += f' in {t.elapsed:.2f} sec'        
        if not self.silent:
            print(msg) 