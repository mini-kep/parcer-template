import pytest
from decimal import Decimal

from parsers.uploader import upload_datapoints, Uploader

       
def test_upload_to_database_returns_code_200():
    class MockResponse:
        status_code = 200
    
    def mock_post(*arg, **kwarg):        
        return MockResponse()
    
    test_data = [1,2,3]
    assert upload_datapoints(test_data, upload_func=mock_post)


def test_Uploader():
    u = Uploader(lambda x: True)
    assert u.post([])    
    
    
if __name__ == '__main__':
    pytest.main([__file__])
