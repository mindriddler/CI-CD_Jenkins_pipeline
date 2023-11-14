from pingurl.models import PingData, WatchedUrl

watched_urls = {}
pings = {}
next_id = 0


def add_watched_url(watched_url: WatchedUrl): #hej alleammans HELLO
    if not isinstance(watched_url, WatchedUrl):
        raise ValueError("watched_url must be a WatchedUrl instance")

    if watched_url.url_id is not None:
        raise ValueError("url_id must be None")
    global next_id

    watched_url.url_id = next_id

    next_id += 1

    watched_urls[watched_url.url_id] = watched_url

    return watched_url.url_id


def get_watched_url(url_id):
    if not isinstance(url_id, int):
        raise ValueError("url_id must be an integer")

    if not url_id in watched_urls:
        raise WatchedUrlNotFoundError("url_id not found")

    return watched_urls[url_id]


def delete_watched_url(url_id):
    if not isinstance(url_id, int):
        raise ValueError("url_id must be an integer")

    if not url_id in watched_urls:
        raise WatchedUrlNotFoundError("url_id not found")

    del watched_urls[url_id]


def get_url_data(url_id):
    if not isinstance(url_id, int):
        raise ValueError("url_id must be an integer")

    if not url_id in watched_urls:
        raise WatchedUrlNotFoundError("url_id not found")

    watched_url_dict = watched_urls[url_id].to_dict()

    url_pings = pings.get(url_id, [])

    # turn the list of url pings into a list of dicts without the urlId key
    url_pings_result = [
        {k: v for k, v in ping.to_dict().items() if k != "urlId"} for ping in url_pings
    ]

    return {**watched_url_dict, "pings": url_pings_result}


def get_url_ids():
    return list(watched_urls.keys())


def add_ping_data(ping_data: PingData):
    if not isinstance(ping_data, PingData):
        raise ValueError("ping_data must be a PingData instance")

    if not ping_data.url_id in watched_urls:
        raise WatchedUrlNotFoundError("Watched URL with the given urlId was not found.")

    if not ping_data.url_id in pings:
        pings[ping_data.url_id] = []

    pings[ping_data.url_id].append(ping_data)


def get_stats():
    ping_count = 0
    for url_id in pings:
        ping_count += len(pings[url_id])

    return {"watchedUrls": len(watched_urls), "pings": ping_count}


class WatchedUrlNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)
