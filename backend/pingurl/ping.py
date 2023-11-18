from datetime import datetime
from email.utils import parsedate_to_datetime

import requests
from pingurl import persistance
from pingurl.models import PingData, WatchedUrl

TIMEOUT = 10


def send_ping(watched_url: WatchedUrl) -> PingData:
    if not isinstance(watched_url, WatchedUrl):
        raise ValueError("watched_url must be a WatchedUrl instance")

    # Used only if a request exception occurs
    pinged_at = datetime.now()

    status_code = None
    response_time = None

    # Do some "rough" status code mapping for requests exceptions so that each
    # ping has a status code.
    try:
        response = requests.get(watched_url.url, timeout=TIMEOUT)
        pinged_at = parsedate_to_datetime(response.headers["Date"])
        response_time = response.elapsed
        status_code = response.status_code
    except requests.exceptions.Timeout:
        status_code = 503
    except requests.exceptions.ConnectionError:
        status_code = 503
    except requests.exceptions.TooManyRedirects:
        status_code = 508
    except requests.exceptions.RequestException:
        status_code = 500

    # Calculate response time if an exception occured
    if response_time is None:
        response_time = datetime.now() - pinged_at

    ping_data = PingData(
        pinged_at, response_time, status_code, url_id=watched_url.url_id
    )

    return ping_data


def send_ping_persist_data(url_id: int):
    try:
        watched_url = persistance.get_watched_url(url_id)
        persistance.add_ping_data(send_ping(watched_url))
    except WatchedUrlNotFoundError:
        pass
