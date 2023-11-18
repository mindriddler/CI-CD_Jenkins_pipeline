import pytest
from flask import Flask
from pingurl import app, watched_urls


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_add_watched_url(client):
    response = client.post(
        "/watched-urls",
        json={
            "activateAt": "2023-11-06T01:36:28.610Z",
            "force": True,
            "periodSec": 30,
            "url": "https://example.com",
        },
    )
    assert response.status_code == 201


def test_delete_watched_url(client):
    # Add a URL first and then delete it
    response = client.delete("/watched-urls/0")
    assert response.status_code == 200
