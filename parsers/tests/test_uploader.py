import pytest
from parsers.uploader import Uploader


#TODO: make test for poster

class MockPoster:
    status_message = ''
    is_success = True
    
    def __init__(self, x):
        pass
    
    def post(self):
        return 1 



def test_Uploader():
    u = Uploader(poster_class=MockPoster)
    assert u.post([])    

if __name__ == '__main__':
    pytest.main([__file__])
    u = Uploader(poster_class=MockPoster)
    assert u.post([1, 2, 3])   
    assert u.is_success
