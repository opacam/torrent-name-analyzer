#!/usr/bin/env python
"""
Rest API to extract all possible media information from a torrent filename.

Run the app with one of these commands:
    $ PYTHONPATH=. ./torrent_name_analyzer/app.py
"""
import datetime
import connexion
import logging
import os

from flask import render_template

from torrent_name_analyzer.config import (
    config_by_name, DEFAULT_HOST, DEFAULT_PORT,
)
from torrent_name_analyzer import orm
from torrent_name_analyzer.utils import get_parsed_data

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger()

TORRENT_EXIST_IN_DB_MESSAGE = (
    "Torrent `{torrent_name}` already exists in database, "
    "please use `PUT` method to update it."
)
TORRENT_NOT_EXIST_IN_DB_MESSAGE = (
    "Torrent `{torrent_name}` doesnt exists in database,"
    "please use `POST` method to create it."
)

config_env = os.getenv("BOILERPLATE_ENV") or "dev"
log.info(f"Using configuration: {config_env}")

# Start database session
db_session = orm.init_db(config_env)


def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_torrents(limit):
    q = db_session.query(orm.Torrent)
    return [p.dump() for p in q][:limit]


def get_torrent(torrent_id):
    torrent = (
        db_session.query(orm.Torrent)
        .filter(orm.Torrent.torrent_id == torrent_id)
        .one_or_none()
    )
    return torrent.dump() if torrent is not None else ("Not found", 404)


def _get_torrent_by_name(torrent_name):
    """
    Private method to get a Torrent (or None) from the database given a
    torrent filename.
    """
    return (
        db_session.query(orm.Torrent)
        .filter(orm.Torrent.torrent_name == torrent_name)
        .one_or_none()
    )


def get_torrent_by_name(torrent_name):
    torrent = _get_torrent_by_name(torrent_name)
    return torrent.dump() if torrent is not None else ("Not found", 404)


def post_torrent(torrent_name):
    torrent = _get_torrent_by_name(torrent_name)
    if torrent is not None:
        msg = TORRENT_EXIST_IN_DB_MESSAGE.format(torrent_name=torrent_name)
        logging.warning(msg)
        return msg, 201
    logging.info(f"Creating torrent {torrent_name}...")
    parsed_torrent = get_parsed_data(torrent_name)
    db_session.add(orm.Torrent(**parsed_torrent))
    db_session.commit()
    return parsed_torrent, 200


def put_torrent(torrent_name):
    torrent = _get_torrent_by_name(torrent_name)
    if torrent is None:
        msg = TORRENT_NOT_EXIST_IN_DB_MESSAGE.format(torrent_name=torrent_name)
        logging.warning(msg)
        return msg, 201
    logging.info(f"Updating torrent {torrent_name}...")
    parsed_torrent = get_parsed_data(torrent_name)
    torrent.update(**parsed_torrent)
    db_session.commit()
    return parsed_torrent, 200


def remove_torrent(torrent_id):
    torrent = (
        db_session.query(orm.Torrent)
        .filter(orm.Torrent.torrent_id == torrent_id)
        .one_or_none()
    )
    if torrent is not None:
        logging.info("Deleting torrent %s..", torrent_id)
        db_session.query(orm.Torrent).filter(
            orm.Torrent.torrent_id == torrent_id
        ).delete()
        db_session.commit()
        return connexion.NoContent, 204
    else:
        return connexion.NoContent, 404


def create_app(config_name):
    config_cls = config_by_name[config_name]
    # initialize Flask app
    connexion_app = connexion.FlaskApp(__name__, specification_dir="swagger/")
    # Configure flask app
    flask_app = connexion_app.app
    flask_app.config.from_object(config_cls)
    # Add api
    connexion_app.add_api("swagger.yaml")

    @flask_app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # Create a URL route in our application for "/"
    @connexion_app.route("/")
    def home():
        """
        This function just responds to the browser ULR `localhost:5000/`
        """
        return render_template("home.html")

    return connexion_app


if __name__ == "__main__":
    app = create_app(config_env)
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT, use_reloader=True)
