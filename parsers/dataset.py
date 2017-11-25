import arrow
from pathlib import Path

from parsers.mover import to_json, Uploader
from parsers.helper import Markdown, Timer
from parsers import PARSERS, PARSERS_DICT


class ReadmeTable:
    def __init__(self, parsers=PARSERS):
        self.parsers = parsers

    def _yield_rows(self):
        yield ('Class', 'Description', 'Frequency', 'Start date')
        for p in self.parsers:
            yield (p.__name__,
                   p.__doc__,
                   p.freq,
                   p.observation_start_date)

    def __repr__(self):
        rows = list(self._yield_rows())
        return Markdown.table(rows)


class Dataset(object):
    def __init__(self, start_date, end_date=None, parsers=PARSERS):
        self.parsers = parsers
        self.start, self.end = start_date, end_date
        self.items = []

    def extract(self):
        self.items = []
        for parser_cls in self.parsers:
            parser = parser_cls(self.start, self.end)
            parser.extract()
            for datapoint in parser.items:
                self.items.append(datapoint)
        return self.items

    @property
    def json(self):
        fmt = {'separators': (',', ': '), 'indent': 4}
        return to_json(self.items, **fmt)

    def save_json(self, filename):
        Path(filename).write_text(self.json)

    def upload(self):
        return Uploader(self.items).post()


def save_reference_dataset(filename='test_data_2016H2.json'):
    with Timer() as t:
        dataset = Dataset(parsers=PARSERS,
                          start_date='2016-06-01',
                          end_date='2016-12-31',
                          silent=True)
        dataset.extract()
        dataset.save_json(filename)
    print(f'Saved reference dataset to {filename} in {t.elapsed} sec')
    return filename


def shift(**kwargs):
    return arrow.now().shift(**kwargs).format("YYYY-MM-DD")


def get_start_date(freq):
    d = dict(a=shift(years=-1),
             q=shift(quarters=-1),
             m=shift(months=-4),
             d=shift(weeks=-1))
    return d[freq]


def update(freq):
    dt = get_start_date(freq)
    parsers = PARSERS_DICT[freq]
    d = Dataset(start_date=dt, parsers=parsers)
    d.extract()
    return d.upload()


if __name__ == '__main__':  # pragma: no cover
    #    from parsers.getter.cbr_fx import USDRUR
    #    from parsers.getter.brent import Brent
    #    d = Dataset('2017-11-13', [USDRUR, Brent])
    #    #d.extract()
    #    assert d.items[0]['name'] == 'USDRUR_CB'
    #    assert isinstance(d.json, str)
    #    assert d.json
    #    #d.save_json('abc.txt')
    #    print()
    #    #d.upload()
    assert update('d')