import os

import requests

BASE_URL = os.getenv("HOST_IP")


def test_get_stats():
    response = requests.get(f"http://{BASE_URL}:5000/stats", timeout=60)
    assert response.status_code == 200
    assert "pings" in response.json()


def test_add_and_delete_watched_url():
    post_response = requests.post(
        f"http://{BASE_URL}:5000/watched-urls",
        json={
            "activateAt": "2023-11-06T01:36:28.610Z",
            "force": True,
            "periodSec": 30,
            "url": "https://example.com",
        },
        timeout=60,
    )
    assert post_response.status_code == 201
    url_id = post_response.json().get("urlId")
    delete_response = requests.delete(
        f"http://{BASE_URL}:5000/watched-urls/{url_id}", timeout=60
    )
    assert delete_response.status_code == 200
