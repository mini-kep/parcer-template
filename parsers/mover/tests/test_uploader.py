import pytest
from parsers.mover.uploader import Uploader, Poster, yield_chunks

# TODO: review testing guidelines: https://github.com/mini-kep/guidelines/blob/master/testing.md
# with focus on test naming
# test name should substitute the comments in test + allow replicating the test by knowing its name 


def mock_post_returns_200_status_code(data):
    return 200


def mock_post_returns_400_status_code(data):
    return 400


class MockPoster200(Poster):
    def __init__(self, data_chuck):
        super().__init__(data_chuck,
                         post_func=mock_post_returns_200_status_code,
                         delay=0.001)


# not used in tests
# is it needed for some purpose?
class MockPoster400(Poster):
    def __init__(self, data_chuck):
        super().__init__(data_chuck,
                         post_func=mock_post_returns_400_status_code,
                         delay=0.001)


def test_yield_chunks_on_list_input_returns_chunks():
    gen = [1,2,3,4,5]
    chunk_size = 3
    assert list(yield_chunks(gen=gen, chunk_size=chunk_size)) == [[1, 2, 3], [4, 5]]


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

    def test_status_code_on_good_poster_equals_200(self):
        poster = Poster(data_chunk=data_chunk_sample,
                        post_func=mock_post_returns_200_status_code)
        poster.post()
        assert poster.status_code == 200

    def test_status_code_on_bad_poster_equals_400(self):
        poster = Poster(data_chunk=data_chunk_sample,
                        post_func=mock_post_returns_400_status_code,
                        delay=0.001)
        poster.post()
        assert poster.status_code == 400

    def test_attempts_on_bad_poster_equals_max_attempts(self):
        poster = Poster(data_chunk=data_chunk_sample,
                        post_func=mock_post_returns_400_status_code,
                        delay=0.001)
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


# FIXME (optinal): review how parsers.scrapper.fetch() is tested with
# 'requests_mock'.


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
