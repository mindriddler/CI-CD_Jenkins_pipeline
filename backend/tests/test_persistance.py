import logging
from datetime import datetime

import pytest
from pingurl.models import WatchedUrl
from pingurl.persistance import add_watched_url, get_watched_url


def test_get_watched_url_input_string():
    url_id = "string"
    with pytest.raises(ValueError) as e:
        get_watched_url(url_id)
    assert str(e.value) == "url_id must be an integer"


def test_add_watched_url_input_string():
    watched_url = "string"
    with pytest.raises(ValueError) as e:
        add_watched_url(watched_url)
    assert str(e.value) == "watched_url must be a WatchedUrl instance"


def test_add_minimum_watched_url():
    watched_url = WatchedUrl(datetime.now(), True, 60, "https://www.example.com")
    url_id = add_watched_url(watched_url)
    assert get_watched_url(url_id) == watched_url


def test_add_multiple_watched_urls():
    watched_url1 = WatchedUrl(datetime.now(), True, 60, "https://www.example.com")
    watched_url2 = WatchedUrl(datetime.now(), False, 120, "https://www.example.org")
    url_id1 = add_watched_url(watched_url1)
    url_id2 = add_watched_url(watched_url2)
    assert get_watched_url(url_id1) == watched_url1
    assert get_watched_url(url_id2) == watched_url2
