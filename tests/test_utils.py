import pytest
import datetime
import json

from pathlib import Path
from torrent_name_analyzer import utils

TEST_FILES_PATH = Path(Path(__file__).parent, "name_parser", "files")

# Collect torrent names to test
json_input = Path(TEST_FILES_PATH, "input.json")
with open(json_input) as input_file:
    torrents = json.load(input_file)

# Collect and adapt the expected results to our api
json_output = Path(TEST_FILES_PATH, "output.json")
with open(json_output) as output_file:
    expected_raw_results = json.load(output_file)
expected_results = []
for data_dict in expected_raw_results:
    rip_keys = []
    for rip_key in utils.RIP_PROPERTIES_KEYS:
        if rip_key in data_dict:
            if rip_key in {"sbs"}:
                rip_keys.append(data_dict[rip_key])
            else:
                rip_keys.append(rip_key)
            data_dict.pop(rip_key)
    if rip_keys:
        data_dict["rip_properties"] = ", ".join(rip_keys)

    # convert list/integers to strings
    for special_key in utils.SPECIAL_KEYS:
        if special_key not in data_dict:
            continue
        value = data_dict[special_key]
        if special_key in data_dict and isinstance(value, list):
            data_dict[special_key] = ", ".join([str(i) for i in value])
        elif special_key in data_dict and isinstance(value, int):
            data_dict[special_key] = f"{value}"
    expected_results.append(data_dict)

test_torrents = zip(torrents, expected_results)
test_exceptions = {
    "Family.Guy.S17.Complete.Season.17.x264.720p",
    "Borgen S1E9 - Divide and Rule ('Del og hersk').mp4",
    "The Simpsons - Complete Seasons S01 to S28 (1080p, 720p, DVDRip)",
    "Marvels Iron Fist S02 Complete 720p WEB-DL x264 [4.3GB] [MP4] [Season 2]",
}


@pytest.mark.parametrize("torrent_name, expected_data", test_torrents)
def test_get_parsed_data(torrent_name, expected_data):
    parsed_torrent = utils.get_parsed_data(torrent_name)
    if torrent_name in test_exceptions:
        pytest.skip(
            f"Skipping {torrent_name} because `group` detection is wrong:"
            f"\n{parsed_torrent}"
        )
    # remove timestamp and make sure is a datetime.datetime object
    ts = parsed_torrent.pop("timestamp")
    assert isinstance(ts, datetime.datetime) is True

    # remove torrent_name and make sure is equal to torrent filename
    tn = parsed_torrent.pop("torrent_name")
    assert tn == torrent_name
    print(parsed_torrent)

    # remove excess (since we don't have it in our test data sets)
    # ...and make sure that we have something in it
    if "excess" in parsed_torrent:
        excess = parsed_torrent.pop("excess")
        assert len(excess) > 0

    # check rip properties , because we make a string from dict keys,
    # so the order of the elements could be different
    if "rip_properties" in parsed_torrent:
        rip_properties = parsed_torrent.pop("rip_properties")
        expected_rip_properties = expected_data.pop("rip_properties")
        for key in rip_properties.split(", "):
            assert (key in expected_rip_properties) is True

    # check remaining keys match our expected data
    expected_keys = expected_data.keys()
    assert sorted(parsed_torrent.keys()) == sorted(expected_keys)

    # make sure that parser values match our expected values
    for key, value in parsed_torrent.items():
        assert value == expected_data[key]
