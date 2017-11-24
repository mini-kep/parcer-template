import pytest
from unittest import TestCase
from parsers.uploader import Uploader, Poster


class MockPoster:
    status_message = ''
    status_code = 200
    
    def __init__(self, x):
        pass
    
    def post(self):
        return 1

    @property
    def is_success(self):
        return self.status_code == 200


def mock_post_returns_200_status_code(data):
    return 200


def mock_post_returns_400_status_code(data):
    return 400


class TestUploader(TestCase):
    def setUp(self):
        self.data_chunk = [{
            "date": "1999-12-31",
            "freq": "a",
            "name": "GDP_yoy",
            "value": 106.4
        },
        {
            "date": "2000-12-31",
            "freq": "a",
            "name": "GDP_yoy",
            "value": 110.0
        }]
        self.uploader = Uploader(poster_class=MockPoster)

    def test_post_with_response_1(self):
        """
        MockPoster queued with data_chunk
        its method post called,
        returned 1
        """
        assert self.uploader.post(self.data_chunk)

    def test_is_success_true_if_poster_returned_200(self):
        """
        MockPoster's post resulted in status_code 200,
        is_success property set to true
        """
        assert self.uploader.is_success


class TestPoster(TestCase):
    def setUp(self):
        self.data_chunk = [{
            "date": "1999-12-31",
            "freq": "a",
            "name": "GDP_yoy",
            "value": 106.4
        },
            {
                "date": "2000-12-31",
                "freq": "a",
                "name": "GDP_yoy",
                "value": 110.0
            }]

    def test_is_success_property_is_true_if_post_returned_200(self):
        """
        post returns status_code 200
        property is_success set to True
        """
        self.poster = Poster(data_chunk=self.data_chunk,
                             post_func=mock_post_returns_200_status_code)
        self.poster.post()
        assert self.poster.is_success

    def test_status_message_if_post_returned_400(self):
        """
        post returns status_code 400, since failed to upload data_chunk
        status_message shows, that upload failed in max number of attempts
        """
        self.poster = Poster(data_chunk=self.data_chunk,
                             post_func=mock_post_returns_400_status_code)
        self.poster.post()
        assert self.poster.status_message == \
               f'Failed to upload {len(self.data_chunk)} datapoints in {Poster.max_attempts} attempt(s)'


if __name__ == '__main__':
    pytest.main([__file__])
