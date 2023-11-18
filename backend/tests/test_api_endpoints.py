import requests

BASE_URL = "http://127.0.0.1:5000"


def test_get_stats():
    response = requests.get(f"{BASE_URL}/stats")
    assert response.status_code == 200
    assert "pings" in response.json()


def test_add_and_delete_watched_url():
    post_response = requests.post(
        f"{BASE_URL}/watched-urls",
        json={
            "activateAt": "2023-11-06T01:36:28.610Z",
            "force": True,
            "periodSec": 30,
            "url": "https://example.com",
        },
    )
    assert post_response.status_code == 201
    url_id = post_response.json().get("urlId")
    delete_response = requests.delete(f"{BASE_URL}/watched-urls/{url_id}")
    assert delete_response.status_code == 200
