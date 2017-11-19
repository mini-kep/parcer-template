import arrow
from parsers import PARSERS
from parsers import PARSERS_DICT
from parsers.timer import Timer
from parsers.dataset import Dataset 
from parsers.markdown import as_markdown

def shift(**kwargs):
    return arrow.now().shift(**kwargs).format("YYYY-MM-DD")

JOBS = dict(a=shift(years=-1),
            q=shift(quarters=-1), 
            m=shift(months=-4),
            d=shift(weeks=-1))  


def save_reference_dataset(filename='test_data_2016H2.json'): 
    t = Timer()
    dataset = Dataset(parsers=PARSERS, 
                      start_date='2016-06-01', 
                      end_date='2016-12-31',
                      silent=True)
    dataset.extract()
    dataset.save_json(filename)
    print('Saved reference dataset:', filename)
    print(t)
    return filename

    
def markdown_descriptions(parsers=PARSERS):
    return '\n\n'.join([as_markdown(p) for p in parsers])


def upload_latest(freq):
    dt = JOBS[freq]
    d = Dataset(PARSERS_DICT[freq], dt)
    d.extract()
    return d.upload()
    
if __name__ == '__main__':
    #assert save_reference_dataset() == 'test_data_2016H2.json'    
    assert markdown_descriptions()
    for freq in 'aqmd':
        print('\nLoading latest values for frequency:', freq)
        print()
        assert upload_latest(freq)
