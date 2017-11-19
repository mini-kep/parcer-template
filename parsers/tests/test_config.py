import pytest
from parsers import config


def test_config():
    assert isinstance(config.EIA_ACCESS_KEY, str)
    assert isinstance(config.HEROKU_API_KEY, str)


if __name__ == '__main__':
    pytest.main([__file__])
