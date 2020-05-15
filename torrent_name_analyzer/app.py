#!/usr/bin/env python
"""
Rest API to extract all possible media information from a torrent filename.

Run the app with one of these commands:
    $ PYTHONPATH=. ./torrent_name_analyzer/app.py
"""
import datetime
import connexion
import logging

from flask import render_template
from os.path import abspath, dirname, join

from torrent_name_analyzer import orm
from torrent_name_analyzer.name_parser import get_parsed_data


logging.basicConfig(level=logging.INFO)


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000
DB_FILE = abspath(join(dirname(__file__), "torrent_name.db"))

TORRENT_EXIST_IN_DB_MESSAGE = (
    "Torrent `{torrent_name}` already exists in database, "
    "please use `PUT` method to update it."
)

TORRENT_NOT_EXIST_IN_DB_MESSAGE = (
    "Torrent `{torrent_name}` doesnt exists in database,"
    "please use `POST` method to create it."
)


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
    print(torrent_id)
    print(torrent)
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


db_session = orm.init_db(f"sqlite:///{DB_FILE}")
app = connexion.FlaskApp(__name__, specification_dir="swagger/")
app.add_api("swagger.yaml")

application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR `localhost:5000/`
    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')


if __name__ == "__main__":
    app.run(
        host=DEFAULT_HOST,
        port=DEFAULT_PORT,
        use_reloader=True,
        threaded=False if ":memory:" in DB_FILE else True,
    )
