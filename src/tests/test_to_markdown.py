from to_markdown import add_dividers, to_markdown, Formatter

def test_add_dividers():
    assert add_dividers(['Branch', 'Commit']) == '| Branch | Commit |'
    # assert add_dividers([1, 2]) == ?
    # assert add_dividers([None]) == ?
    # assert add_dividers(['Branch', None]) == ?
    # also it can be parametrized with this different data

def test_to_markdown():        
    table1 = [
      ['Branch', 'Commit'],
      ['master', '0123456789abcdef'],
      ['staging', 'fedcba9876543210']
    ]        
    md = to_markdown(table1)
    assert md.startswith("|")
    assert 'Branch' in md
    assert 'fedcba9876543210' in md
    # here can be one assert with full result what we expecter. like: "| Branch | Commit | \n ..."
    # also what will happen if table1 will have not expected data. ex: to_markdown(None)

class MockParser:
    """A mock parser to test Table class"""
    info = dict(source_type='API')
    freq = 'a'
    source_url = 'http://some.url'
    all_varnames = ['data_1', 'data_2']

    
class Test_Formatter:
    
    def test_as_markdown_produces_correct_string_on_short_URL(self):
        expected = ('| Parser | MockParser |\n'
                    '| ------ | ---------- |\n'
                    '| Description | A mock parser to test Table class |\n'
                    '| URL | [http://some.url](http://some.url) |\n'
                    '| Frequency | Annual |\n'
                    '| Variables | data_1, data_2 |')
        assert Formatter(MockParser).as_markdown() == expected

    def test_as_markdown_valid_input_long_link(self):
        MockParser.source_url = ("http://www.gks.ru/wps/wcm/connect/"
                                 "rosstat_main/rosstat/ru/statistics/"
                                 "publications/catalog/"
                                 "doc_1140080765391")
        expected = 'http://www.gks.ru/wps/wcm/connect/rossta...'
        # is it works? probably should be without '...' ?
        # like: expected = 'http://www.gks.ru/wps/wcm/connect/rossta'
        assert expected in Formatter(MockParser).as_markdown()
        
if __name__ == '__main__':
    import pytest
    pytest.main([__file__])