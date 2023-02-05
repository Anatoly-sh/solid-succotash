import pytest

from utils import get_data


def test_get_data(test_url):
    assert len(get_data(test_url)[0]) > 0

