import pytest
import requests_mock
from parsers.mover.uploader import Uploader, Poster, yield_chunks
from parsers.config import UPLOAD_URL


@pytest.fixture(scope='module')
def mocked_content():
    with requests_mock.mock() as m:
        yield m


class MockPoster200(Poster):

    def __init__(self, data_chuck):
        super().__init__(data_chuck,
                         post_func=lambda data: 200,
                         delay=0.001)


# not used
class MockPoster400(Poster):
    def __init__(self, data_chuck):
        super().__init__(data_chuck,
                         post_func=lambda data: 400,
                         delay=0.001)


def test_yield_chunks_on_list_input_returns_chunks():
    # setup
    incoming_data = [1,2,3,4,5]
    chunk_size = 3
    # call
    result = yield_chunks(gen=incoming_data, chunk_size=chunk_size)
    # check
    assert list(result) == [[1, 2, 3], [4, 5]]


# recylcing setup
data_chunk_sample = [{
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


class TestPoster():

    def test_status_code_on_good_poster_equals_200(self, mocked_content):
        poster = Poster(data_chunk=data_chunk_sample)
        mocked_content.post(UPLOAD_URL, status_code=200)
        poster.post()
        assert poster.status_code == 200

    def test_status_code_on_bad_poster_equals_400(self, mocked_content):
        poster = Poster(data_chunk=data_chunk_sample,
                        delay=0.001)
        mocked_content.post(UPLOAD_URL, status_code=400)
        poster.post()
        assert poster.status_code == 400

    def test_attempts_on_bad_poster_equals_max_attempts(self, mocked_content):
        poster = Poster(data_chunk=data_chunk_sample,
                        delay=0.001)
        mocked_content.post(UPLOAD_URL, status_code=400)
        poster.post()
        # EP: we basically do not care about the message, but rather the status_code
        #     the status message is derived based on status_code
        # must check Poster.max_attempts = poster.attempts, this is much better
        # test
        assert poster.attempts == Poster.max_attempts

    def test_is_success_property_on_status_code_200_is_true(self):
        poster = Poster(data_chunk_sample)
        poster.status_code = 200
        assert poster.is_success is True

    def test_is_success_property_on_status_code_400_is_false(self):
        poster = Poster(data_chunk_sample)
        poster.status_code = 400
        assert poster.is_success is False


class TestUploader(object):

    def setup_method(self):
        self.long_data = data_chunk_sample * 1000 * 3
        self.uploader = Uploader(self.long_data, poster_class=MockPoster200)

    def test_repr_on_init_is_string(self):
        assert self.uploader.__repr__()
        
    def test_posters_attribute_on_init_is_list_(self):
        assert isinstance(self.uploader.posters, list)
        assert len(self.uploader.posters) == 6

    def test_post_method_returns_true(self):
        assert self.uploader.post() is True

    def test_is_success_after_calling_post_is_True(self):
        self.uploader.post()
        assert self.uploader.is_success is True


if __name__ == '__main__':
    pytest.main([__file__, "--durations=1"])
    u = Uploader(data_chunk_sample * 1000 * 3, poster_class=MockPoster200)
    z = u.posters[0]
    z.post()
    # WONTFIX: elapsed time will be zero for very short set of instructions
    #          may change to different time ing function
    # assert z.elapsed > 0
