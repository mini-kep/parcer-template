from parsers.getter.kep import (make_url,
                                read_csv,
                                get_dataframe_from_repo,
                                yield_all_dicts,
                                is_valid,
                                yield_kep_dicts)

url ='https://raw.githubusercontent.com/mini-kep/parser-rosstat-kep/master/data/processed/latest/dfa.csv'

def test_make_url():
    assert make_url('a') == url

def test_get_dataframe_from_repo():
    return get_dataframe_from_repo('a') == read_csv(url)

def test_read_csv():
    pass#assert isistance (read_csv(".\parsers\getter\tests\test_read_csv.csv"),pd.DataFrame) 
