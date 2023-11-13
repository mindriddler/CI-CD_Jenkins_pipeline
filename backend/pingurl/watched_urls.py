from datetime import datetime

import validators
from flask import jsonify, request
from pingurl import app, business, persistance
from pingurl.models import WatchedUrl
from werkzeug.exceptions import BadRequest

MIN_PERIOD = 10


@app.route("/watched-urls", methods=["POST"])
def add_watched_url():
    data = request.get_json()

    try:
        if not "activateAt" in data:
            raise BadRequest("Missing parameter 'activateAt'")

        activate_at = None

        try:
            activate_at = datetime.fromisoformat(
                data["activateAt"].replace("Z", "+00:00")
            )
        except ValueError as e:
            raise BadRequest("The 'activateAt' parameter must an ISO 8601 date-time.")

        force = data.get("force", False)

        if not isinstance(force, bool):
            raise BadRequest("The 'force' parameter must be a boolean.")

        if not "periodSec" in data:
            raise BadRequest("Missing parameter 'periodSec'")

        period_sec = data["periodSec"]

        if not isinstance(period_sec, int) or period_sec < MIN_PERIOD:
            raise BadRequest(
                f"The 'periodSec' parameter must be an integer of {MIN_PERIOD} or more."
            )

        if not "url" in data:
            raise BadRequest("Missing parameter 'url'")

        url = data["url"]

        if not isinstance(url, str) or not validators.url(url):
            raise BadRequest(f"The 'url' parameter must be valid URL string.")

        try:
            watched_url = WatchedUrl(activate_at, force, period_sec, url)

            url_id = business.add_watched_url(watched_url)

            return jsonify({"message": "Watched URL added", "urlId": url_id}), 201

        except business.AddWatchedUrlError as e:
            raise BadRequest(str(e))

    except BadRequest as e:
        return jsonify({"error": "Bad request", "message": e.description}), 400


@app.route("/watched-urls/<int:url_id>", methods=["DELETE"])
def delete_url(url_id):
    try:
        business.delete_watched_url(url_id)
    except persistance.WatchedUrlNotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify({"message": f"Removed watched url with id {url_id}"}), 200


@app.route("/watched-urls/<int:url_id>", methods=["GET"])
def get_url_data(url_id):
    try:
        url_data = persistance.get_url_data(url_id)

        return jsonify(url_data), 200

    except persistance.WatchedUrlNotFoundError as e:
        return jsonify({"error": str(e)}), 404


@app.route("/watched-urls", methods=["GET"])
def get_url_ids():
    return jsonify({"urlIds": persistance.get_url_ids()}), 200


@app.route("/stats", methods=["GET"])
def get_total():
    return jsonify(persistance.get_stats()), 200
