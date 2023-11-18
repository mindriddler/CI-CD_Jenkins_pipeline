from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest
from pingurl.business import AddWatchedUrlError, add_watched_url, delete_watched_url
from pingurl.models import PingData, WatchedUrl
from pingurl.persistance import watched_urls


@patch("pingurl.business.send_ping")
def test_add_watched_url_success(mock_send_ping):
    mock_ping_data = Mock(spec=PingData)
    mock_ping_data.ok.return_value = True
    mock_send_ping.return_value = mock_ping_data

    # Create an offset-aware datetime object
    watched_url = WatchedUrl(
        datetime.now(timezone.utc), False, 30, "http://example.com"
    )
    url_id = add_watched_url(watched_url)
    assert url_id is not None


@patch("pingurl.business.send_ping")
def test_add_watched_url_failure(mock_send_ping):
    mock_send_ping.return_value.ok = lambda: False
    watched_url = WatchedUrl(datetime.now(), False, 30, "http://example.com")
    with pytest.raises(AddWatchedUrlError):
        add_watched_url(watched_url)


@patch("pingurl.business.persistance")
def test_delete_watched_url(mock_persistance):
    url_id = 1
    mock_persistance.get_url_data.return_value = {
        "url_id": url_id,
        "activateAt": "2023-11-06T01:36:28.610Z",
        "force": True,
        "periodSec": 30,
        "url": "https://example.com",
    }

    # Now call the delete function
    delete_watched_url(url_id)
    mock_persistance.delete_watched_url.assert_called_with(url_id)
