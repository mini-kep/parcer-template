import sys
from pathlib import Path

class PathContext():
    def __init__(self):
        self.path = str(Path(__file__).parent)

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        sys.path.remove(self.path)

with PathContext():
    from parsers import PARSERS
    from parsers.dataset import update, Dataset 
    from parsers.helpers.markdown import as_markdown
    from parsers.helpers.timer import Timer

def save_reference_dataset(filename='test_data_2016H2.json'): 
    with Timer() as t: 
        dataset = Dataset(parsers=PARSERS, 
                          start_date='2016-06-01', 
                          end_date='2016-12-31',
                          silent=True)
        dataset.extract()
        dataset.save_json(filename)
    print(f'Saved reference dataset to {filename} ({t.elapsed} sec)')
    return filename

    
def markdown_descriptions(parsers=PARSERS):
    return '\n\n'.join([as_markdown(p) for p in parsers])


def update_all():
    for freq in 'aqmd':
        assert update(freq)   
    return True


if __name__ == '__main__':
    #assert save_reference_dataset() == 'test_data_2016H2.json'    
    #assert markdown_descriptions()
    assert update_all()