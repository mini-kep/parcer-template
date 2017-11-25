# -*- coding: utf-8 -*-
import pytest

from parsers.helper.markdown import Markdown
from parsers.getter.base import ParserBase


def test_interpret_frequency():
    assert Markdown.interpret_frequency('d') == 'Daily'


class Test_Markdown:

    def test_add_dividers(self):
        assert Markdown._add_dividers(['Branch', 'Commit']) \
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
