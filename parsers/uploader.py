"""Upload data from parsers to database."""
import requests
from time import sleep

from parsers.config import HEROKU_API_KEY as UPLOAD_API_TOKEN, UPLOAD_URL
from parsers.serialiser import to_json
from parsers.helpers import Logger, Timer


def post(data, token=UPLOAD_API_TOKEN, endpoint=UPLOAD_URL):
    """
    Post *data* as json to API endpoint.
    Returns: status_code
    """
    json_data = to_json(data)
    return requests.post(url=endpoint,
                         data=json_data,
                         headers={'API_TOKEN': token}).status_code


def yield_chunks(gen, chunk_size=1000):
    """Split generator or list into smaller parts.

    Args:
        gen - list or generator of datapoints to send
        chunk_size - number of datapoints to send at one time
    Yields:
        list of size *chunk_size* or smaller
    """
    gen = list(gen)
    for i in range(0, len(gen), chunk_size):
        yield gen[i:i + chunk_size]


class Poster():
    """Post to database:
     - attempts to post to db and delay between attempts (safe post mechanism)
     - collects response status
     - holds number of attempts
    """
    max_attempts = 3  # times
    delay = 5  # seconds
    timer = None

    def __init__(self, data_chunk, post_func=post, delay=None):
        self.data = list(data_chunk)
        self.post_func = post_func
        if delay:  # override default delay time
            self.delay = delay
        self.attempts = 0
        self.status_code = None
        self.elapsed = 0

    def post(self):
        """Posts chunk of data to database using self.post()."""
        with Timer() as t:
            for self.attempts in range(1, self.max_attempts + 1):
                self.status_code = self.post_func(data=self.data)
                if self.status_code == 200:
                    break
                sleep(self.delay)
        self.elapsed = t.elapsed

    @property
    def is_success(self):
        return self.status_code == 200

    def __len__(self):
        return len(self.data)

    @property
    def status_message(self):
        n = len(self)
        if self.is_success:
            return f'Uploaded {n} datapoints in {self.attempts} attempt(s)'
        else:
            return f'Failed to upload {n} datapoints in {self.attempts} attempt(s)'

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f'{cls_name}: {self.attempts} attempts, status code {self.status_code}'


class Uploader(object):
    """Post data to database.

    Handles:
    - separate incoming data to chunks
    - make a queue of Sender instances, one per chunk
    - invoke Senders' .post() methods
    - provide logging to console
    - provide collection of posting results (number of attempts of each sender)
    """

    def __init__(self, data, poster_class=Poster):
        self.posters = self.make_queue(data, poster_class)
        self.logger = Logger(silent=False)

    @staticmethod
    def make_queue(data, poster_class):
        return [poster_class(data_chunk) for data_chunk in yield_chunks(data)]

    def post(self):
        # Not todo: timer behaviour + logging
        with Timer() as t:
            for poster in self.posters:
                poster.post()
                self.logger.echo(poster.status_message)
        self.logger.echo('Finished upload', t)
        return self.is_success

    @property
    def is_success(self):
        return all([p.is_success for p in self.posters])


if __name__ == "__main__":
    data = [
        {
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

    p = Poster(data)
    p.post()
    assert p.status_code == 200

    u = Uploader(data)
    u.post()
    for sender in u.posters:
        assert sender.status_code == 200
