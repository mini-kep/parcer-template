"""Parser classes to get datapoints for the database."""

import itertools

from helpers import DateHelper, Markdown, interpret_frequency

# individual parser modules
import getter.brent as brent
import getter.cbr_fx as cbr_fx
import getter.kep as kep


class ParserBase:

    def __repr__(self):
        start = DateHelper.as_string(self.start)
        return f'{self.__class__.__name__}(\'{start}\')'

    @classmethod
    def as_markdown(cls):
        url_str = Markdown.short_link(cls.source_url)
        freq_str = interpret_frequency(cls.freq)
        varname_str = ", ".join(cls.all_varnames)
        rows = [("Parser", cls.__name__),
                ("Description", cls.__doc__ or ''),
                ("URL", url_str or ''),
                ("Frequency", freq_str),
                ("Variables", varname_str or '')]
        return Markdown.table(rows)


class RosstatKEP_Base(ParserBase):
    """Sections of Rosstat Short-term economic indicators ('KEP') publication."""

    freq = '_'
    observation_start_date = DateHelper.make_date('1999-01-31')
    source_url = ("http://www.gks.ru/wps/wcm/connect/"
                  "rosstat_main/rosstat/ru/statistics/"
                  "publications/catalog/doc_1140080765391")
    all_varnames = ['CPI', 'GDP', 'etc']

    def __init__(self, start=None):
        if start is None:
            self.start = self.observation_start_date
        else:
            self.start = DateHelper.make_date(start)

    def sample(self):
        yield {"date": "2015-11-30", "freq": self.freq, "name": "CPI_rog", "value": 100.8}
        yield {"date": "2015-11-30", "freq": self.freq, "name": "RUR_EUR_eop", "value": 70.39}
        yield {"date": "2015-12-31", "freq": self.freq, "name": "CPI_rog", "value": 100.8}
        yield {"date": "2015-12-31", "freq": self.freq, "name": "RUR_EUR_eop", "value": 79.7}

    def yield_dicts(self):
        return kep.yield_dicts(self.freq)


class RosstatKEP_Monthly(RosstatKEP_Base):
    """Monthly indicators from Rosstat 'KEP' publication"""
    freq = 'm'


class RosstatKEP_Quarterly(RosstatKEP_Base):
    """Quarterly indicators from Rosstat 'KEP' publication"""
    freq = 'q'


class RosstatKEP_Annual(RosstatKEP_Base):
    """Annual indicators from Rosstat 'KEP' publication"""
    freq = 'a'


class CBR_USD(ParserBase):
    """Bank of Russia official USD to RUB exchange rate"""
    freq = 'd'
    observation_start_date = DateHelper.make_date('1992-01-01')  # '1991-07-01'
    source_url = "http://www.cbr.ru/scripts/Root.asp?PrtId=SXML"
    all_varnames = ['USDRUR_CB']

    def __init__(self, start=None):
        if start is None:
            self.start = self.observation_start_date
        else:
            self.start = DateHelper.make_date(start)
        self.end = DateHelper.today()

    def yield_dicts(self):
        return cbr_fx.get_cbr_er(self.start, self.end)

    def sample(self):
        """Yields dictionaries with sample datapoints."""
        return iter([{'date': '2017-09-15', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.7706},
                     {'date': '2017-09-16', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.5336},
                     {'date': '2017-09-19', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.6242},
                     {'date': '2017-09-20', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 58.0993},
                     {'date': '2017-09-21', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 58.129},
                     {'date': '2017-09-22', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 58.2242},
                     {'date': '2017-09-23', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.6527},
                     {'date': '2017-09-26', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.566}])


class BrentEIA(ParserBase):
    """Brent oil price from US EIA"""
    freq = 'd'
    observation_start_date = DateHelper.make_date('1987-05-15')
    source_url = "https://www.eia.gov/opendata/qb.php?category=241335"
    all_varnames = ['BRENT']

    def __init__(self, start=None):
        if start is None:
            self.start = self.observation_start_date
        else:
            self.start = DateHelper.make_date(start)

    def yield_dicts(self):
        for p in brent.yield_brent_dicts():
            if DateHelper.make_date(p['date']) >= self.start:
                yield p

    def sample(self):
        """Yield a few dictionaries with datapoints."""
        return iter([{'date': '2017-09-18', 'freq': 'd', 'name': 'BRENT', 'value': 55.5},
                     {'date': '2017-09-15', 'freq': 'd', 'name': 'BRENT', 'value': 56.18},
                     {'date': '2017-09-14', 'freq': 'd', 'name': 'BRENT', 'value': 56.76},
                     {'date': '2017-09-13', 'freq': 'd', 'name': 'BRENT', 'value': 55.52},
                     {'date': '2017-09-12', 'freq': 'd', 'name': 'BRENT', 'value': 55.06},
                     {'date': '2017-09-11', 'freq': 'd', 'name': 'BRENT', 'value': 54.2}]
                    )


class Dataset:
    """Operations related to all parsers."""

    parsers = [RosstatKEP_Monthly,
               RosstatKEP_Quarterly,
               RosstatKEP_Annual,
               CBR_USD,
               BrentEIA
               ]

    def get_sample():
        dataset_sample = []
        for cls in Dataset.parsers:
            parser = cls()
            gen = list(parser.sample())
            dataset_sample.extend(gen)
        return dataset_sample

    def yield_full_dataset():
        gen_list = [p().yield_dicts() for p in Dataset.parsers]
        return itertools.chain.from_iterable(gen_list)

    def as_markdown():
        tables = [cls.as_markdown() for cls in Dataset.parsers]
        return '\n\n'.join(tables)


if __name__ == "__main__":
    # to tests:
    assert CBR_USD().__repr__() == "CBR_USD('1992-01-01')"

    from pprint import pprint
    print('Sample dataset:')
    pprint(Dataset.get_sample())

    print('\nMarkdown descriptions:')
    print(Dataset.as_markdown())

    #fx = list(CBR_USD('2017-09-01').yield_dicts())
    #kep_m = list(RosstatKEP_Monthly('2017-06').yield_dicts())
    #oil = list(BrentEIA('2017-09-01').yield_dicts())

    # TODO: must put this generator into database
    #gen = Dataset.yield_full_dataset()

    # TODO: round/beautify 349.89999999999998
