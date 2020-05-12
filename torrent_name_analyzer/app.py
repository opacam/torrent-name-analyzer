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
from torrent_name_analyzer.name_parser import parse


logging.basicConfig(level=logging.INFO)


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000
DB_FILE = abspath(join(dirname(__file__), "torrent_name.db"))


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


def get_torrent_by_name(torrent_name):
    torrent = (
        db_session.query(orm.Torrent)
        .filter(orm.Torrent.torrent_name == torrent_name)
        .one_or_none()
    )
    return torrent.dump() if torrent is not None else ("Not found", 404)


def put_torrent(torrent_name):
    p = (
        db_session.query(orm.Torrent)
        .filter(orm.Torrent.torrent_name.like(torrent_name))
        .one_or_none()
    )
    parsed_torrent = parse(torrent_name)
    parsed_torrent["torrent_name"] = torrent_name
    logging.info(f"Parsed torrent: {parsed_torrent}")

    # extract some rip properties, if any
    rip_properties = {
        "3d",          # is 3d
        "extended",    # is the extended version of the film
        "hardcoded",   # hardcoded caption (the caption is always there and the person cannot turn it on or off)
        "internal",    # it is only meant for release within the group because it doesn't follow certain release standards.
        "proper",      # a previous release of this movie was poor and this one is supposedly better.
        "readnfo",     # read an included info file to learn about possible weaknesses or defects in the bootleg copy.
        "repack",      # repacked, similar to a PROPER.
        "sbs",         # Half Side-by-Side (SBS), means the left and right views of a 3D video are subsampled at half resolution and you get a backwards compatible full frame. ... Full SBS, means you transmit both views at full resolution; better quality, but bigger file
        "unrated",     # has content in it that could not be seen in theaters – essentially, it is an uncensored version of the film
        "widescreen",  # is wide screen
    }
    rip_props = []
    for prop in rip_properties:
        if prop in parsed_torrent:
            value = parsed_torrent.pop(prop)
            if value is True:
                rip_props.append(prop)
            elif prop == "sbs":
                rip_props.append(value)
    if rip_props:
        parsed_torrent["rip_properties"] = ", ".join(rip_props)

    # make sure that we store strings, since we parse some fields as lists
    special_keys = ["season", "episode", "language"]
    for key in special_keys:
        if key in parsed_torrent:
            if isinstance(parsed_torrent[key], list):
                parsed_torrent[key] = ", ".join(
                    [str(i) for i in parsed_torrent[key]]
                )
                logging.info(
                    f"{key} converted to string list: {parsed_torrent[key]}"
                )

    # store excess as a string using `||` as a separator
    if "excess" in parsed_torrent:
        parsed_torrent["excess"] = " || ".join(parsed_torrent["excess"])

    # set/update timestamp
    parsed_torrent["timestamp"] = datetime.datetime.now()

    if p is not None:
        logging.info(f"Updating torrent {torrent_name}..")
        p.update(**parsed_torrent)
    else:
        logging.info(f"Creating torrent {torrent_name}..")
        db_session.add(orm.Torrent(**parsed_torrent))
    db_session.commit()
    return connexion.NoContent, (200 if p is not None else 201)


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
