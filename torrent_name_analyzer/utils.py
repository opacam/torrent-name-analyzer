
import datetime
import logging

from sqlalchemy.inspection import inspect

from torrent_name_analyzer.orm import Torrent
from torrent_name_analyzer.name_parser import parse

SUPPORTED_KEYS = {column.name for column in inspect(Torrent).c}
RIP_PROPERTIES_KEYS = {
    # 3d: the film is encoded in 3d format
    "3d",
    # extended: is the extended version of the film
    "extended",
    # hardcoded: hardcoded caption (the caption is always there and
    # the person cannot turn it on or off)
    "hardcoded",
    # internal: it is only meant for release within the group because
    # it doesn't follow certain release standards.
    "internal",
    # proper: a previous release of this movie was poor
    # and this one is supposedly better.
    "proper",
    # readnfo: read an included info file to learn about
    # possible weaknesses or defects in the bootleg copy.
    "readnfo",
    # repack: repacked, similar to a PROPER.
    "repack",
    # sbs: Half Side-by-Side (SBS), means the left and right views of a 3D
    # video are subsampled at half resolution and you get a backwards
    # compatible full frame. ... Full SBS, means you transmit both views at
    # full resolution; better quality, but bigger file
    "sbs",
    # unrated: has content in it that could not be seen in
    # theaters – essentially, it is an uncensored version of the film
    "unrated",
    # widescreen: is encoded in wide screen format
    "widescreen",
}
# We can find these keys in our parsed torrent name. This keys could have
# different types of values, usually we will get an integer or an string but
# sometimes we could get a list.
SPECIAL_KEYS = {"season", "episode", "language", "excess"}
STANDARD_KEYS = SUPPORTED_KEYS - SPECIAL_KEYS - RIP_PROPERTIES_KEYS


def get_parsed_data(torrent_name: str) -> dict:
    """
    Given a torrent name, returns parsed data ready to be stored into database.
    """
    parsed_data = {"torrent_name": torrent_name}
    parsed_torrent = parse(torrent_name)
    parsed_keys_set = set(parsed_torrent.keys())
    logging.info(f"Parsed torrent: {parsed_torrent}")

    # collect standard keys, data is string
    for key in STANDARD_KEYS & parsed_keys_set:
        parsed_data[key] = parsed_torrent[key]

    # extract some rip properties, if any and set data
    rip_props = []
    for prop in RIP_PROPERTIES_KEYS & parsed_keys_set:
        value = parsed_torrent.pop(prop)
        if value is True:
            rip_props.append(prop)
        elif prop == "sbs":
            rip_props.append(value)
    if rip_props:
        parsed_data["rip_properties"] = ", ".join(rip_props)

    # make sure that we store strings for defined special keys,
    # since our parser returns as some lists
    for key in SPECIAL_KEYS & parsed_keys_set:
        if isinstance(parsed_torrent[key], list):
            parsed_data[key] = ", ".join(
                [str(i) for i in parsed_torrent[key]]
            )
            logging.info(
                f"{key} converted to string list: {parsed_data[key]}"
            )
        else:
            parsed_data[key] = parsed_torrent[key]

    # set/update timestamp
    parsed_data["timestamp"] = datetime.datetime.now()
    return parsed_data
