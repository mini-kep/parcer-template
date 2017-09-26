from to_markdown import add_dividers, to_markdown, Formatter

def test_add_dividers():
    assert add_dividers(['Branch', 'Commit']) == '| Branch | Commit |'

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
    
class Test_Formatter:
    
    def setup_method(self):
        
        class MockParser:
            """A mock parser to test Table class"""
            info = dict(source_type='API')
            freqs = 'aqmwd'
            source_url = 'http://some.url'
            all_varnames = ['data_1', 'data_2']
        
        self.MockParser = MockParser

    def test_as_markdown_produces_correct_string_on_short_URL(self):
        expected = ('| Parser | MockParser |\n'
                    '| ------ | ---------- |\n'
                    '| Description | A mock parser to test Table class |\n'
                    '| URL | [http://some.url](http://some.url) |\n'
                    '| Source type | API |\n'
                    '| Frequency | Annual, quarterly, monthly, weekly, daily |\n'
                    '| Variables | data_1, data_2 |')
        assert Formatter(self.MockParser).as_markdown() == expected

    def test_as_markdown_valid_input_long_link(self):
        self.MockParser.source_url = ("http://www.gks.ru/wps/wcm/connect/"
                                      "rosstat_main/rosstat/ru/statistics/"
                                      "publications/catalog/"
                                      "doc_1140080765391")
        expected = 'http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/st...'
        assert expected in Formatter(self.MockParser).as_markdown()
