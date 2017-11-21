# -*- coding: utf-8 -*-
import pytest

from parsers.markdown import Markdown, as_markdown, interpret_frequency
from parsers.getter.base import ParserBase

def test_interpret_frequency():
    assert interpret_frequency('d') == 'Daily'


@pytest.fixture
def mock_parser():
    MockParser = ParserBase
    MockParser.observation_start_date = '1965-01-01'
    MockParser.__doc__ = 'Short text'
    return MockParser


class Test_as_markdown:
    
    class Test_Formatter:

        def test_as_markdown_returns_string(self, mock_parser):
            result = as_markdown(mock_parser)
            expected = '\n'.join(['| Parser | ParserBase |',
                        '| ------ | ---------- |',
                        '| Description | Short text |',
                        '| Start date | 1965-01-01 |'])
            assert result == expected
             
class Test_Markdown:

    def test_add_dividers(self):
        assert Markdown.add_dividers(['Branch', 'Commit']) \
            == '| Branch | Commit |'


    def test_table(self):
        table1 = [
            ['Branch', 'Commit'],
            ['master', '0123456789abcdef'],
            ['staging', 'fedcba9876543210']
        ]
        md = Markdown.table(table1)
        assert md.startswith("|")
        assert 'Branch' in md
        assert 'fedcba9876543210' in md
        assert md == '| Branch | Commit |\n| ------ | ------ |\n| master | 0123456789abcdef |\n| staging | fedcba9876543210 |'

if __name__ == '__main__':
    pytest.main([__file__])
