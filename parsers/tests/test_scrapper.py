import pytest
import requests_mock
from parsers.scrapper import fetch, Scrapper

# def fetch(url):
#    """Fetch content from *url* from internet."""
#    content = requests.get(url).text
#    if "Error" in content:
#        raise ValueError(f"Cannot read from URL <{url}>")
#    if 'Error in parameters' in content:
#        raise Exception(f'Error in parameters: {url}')
#    return content


@pytest.fixture(scope='module')
def mocked_content():
    with requests_mock.mock() as m:
        yield m


class Test_fetch():
    # urls does not affect the test in this setup
    url = "http://example.com"

    def test_fetch_good_response(self, mocked_content):
        mocked_content.get(self.url, text='{value: 1}')
        assert fetch(self.url) == '{value: 1}'

    # TODO: must parametrise

    def test_fetch_with_non_readable_URL_raises_ValueError(
            self, mocked_content):
        mocked_content.get(self.url, text="Error reponse")
        with pytest.raises(ValueError):
            fetch(self.url)

    def test_fetch_on_Error_in_parameters(self, mocked_content):
        mocked_content.get(self.url, text="Error in parameters")
        with pytest.raises(ValueError):
            fetch(self.url)


def test_Scrapper():
    s = Scrapper(lambda x: x)
    assert '123' == s.get('123')
