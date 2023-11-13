from pingurl import persistance, schedule
from pingurl.models import WatchedUrl
from pingurl.ping import send_ping


def add_watched_url(watched_url):
    if not isinstance(watched_url, WatchedUrl):
        raise ValueError("watched_url must be a WatchedUrl instance")

    ping_data = send_ping(watched_url)

    if not ping_data.ok() and not watched_url.force:
        raise AddWatchedUrlError("Ping failed and force is false")

    url_id = persistance.add_watched_url(watched_url)

    # Add the created url_id to the ping_data object
    ping_data.url_id = url_id

    persistance.add_ping_data(ping_data)

    schedule.add(watched_url)

    return url_id


def delete_watched_url(url_id):
    if not isinstance(url_id, int):
        raise ValueError("url_id must be an integer")

    schedule.remove(url_id)

    persistance.delete_watched_url(url_id)


class AddWatchedUrlError(Exception):
    def __init__(self, message):
        super().__init__(message)
