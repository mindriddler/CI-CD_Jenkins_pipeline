import pytest
from pingurl.persistance import get_watched_url


def test_get_watched_url_input_string():
    url_id = "string"
    with pytest.raises(ValueError) as e:
        get_watched_url(url_id)
    assert str(e.value) == "url_id must be an integer"
