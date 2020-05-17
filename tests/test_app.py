import json
import pytest

from torrent_name_analyzer.config import DEFAULT_HOST, DEFAULT_PORT
from torrent_name_analyzer.app import (
    create_app,
    get_timestamp,
    TORRENT_EXIST_IN_DB_MESSAGE,
    TORRENT_NOT_EXIST_IN_DB_MESSAGE,
)
from torrent_name_analyzer.utils import SPECIAL_KEYS
from .test_utils import torrents, expected_results

api_version = "v1"
base_url = f"http://{DEFAULT_HOST}:{DEFAULT_PORT}"
torrents_end_point = f"{base_url}/{api_version}/torrents"


api_test_post = list(zip(torrents, expected_results))[:15]
api_test_put = api_test_post[:5]
api_test_get = api_test_post[0]
api_test_delete = api_test_post[-1]


def verify_result(response_data, expected_data):
    """A function to check that responses has the expected data."""
    avoid_keys = {"excess"}
    for k, v in response_data.items():
        if k in avoid_keys:
            continue
        if k == "timestamp":
            assert isinstance(v, str)
        else:
            assert v == expected_data[k]


@pytest.fixture(scope="session")
def client(request):
    """
    A client to perform session-wide tests for a `Flask` application
    created via `connexion`.
    """
    connexion_app = create_app("test")
    return connexion_app.app.test_client()


def test_get_timestamp():
    """Basic test for :meth:`~torrent_name_analyzer.app.get_timestamp`."""
    string_now = get_timestamp()
    assert isinstance(string_now, str) is True


def test_index_page(client):
    """
    Test that :meth:`~torrent_name_analyzer.app.create_app.home` returns a
    successful response code (200).
    """
    response = client.get(f"{base_url}/")
    assert response.status_code == 200


@pytest.mark.parametrize("torrent_name, expected_data", api_test_post)
@pytest.mark.run(order=1)
def test_post_success(client, torrent_name, expected_data):
    """
    Test that :meth:`~torrent_name_analyzer.app.post_torrent` returns a
    successful response code (200) and stores some parsed torrent names into
    database.
    """
    response = client.post(
        f"{torrents_end_point}/{torrent_name}", content_type="application/json"
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data.pop("torrent_name") == torrent_name
    verify_result(data, expected_data)


@pytest.mark.run(order=2)
def test_post_torrent_already_posted(client):
    """
    Test that :meth:`~torrent_name_analyzer.app.post_torrent` returns a
    response code of (200), which will mean that we cannot store a torrent that
    already exists in database.
    """
    torrent_name = api_test_post[0][0]
    response = client.post(
        f"{torrents_end_point}/{torrent_name}", content_type="application/json"
    )
    msg = json.loads(response.get_data(as_text=True))
    assert response.status_code == 201
    assert msg == TORRENT_EXIST_IN_DB_MESSAGE.format(torrent_name=torrent_name)


@pytest.mark.parametrize("torrent_name, expected_data", api_test_put)
@pytest.mark.run(order=3)
def test_put_success(client, torrent_name, expected_data):
    """
    Test that :meth:`~torrent_name_analyzer.app.put_torrent` returns a response
    code of (200), which will mean that we successfully updated an stored
    torrent of the database.
    """
    response = client.put(
        f"{torrents_end_point}/{torrent_name}", content_type="application/json"
    )
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data.pop("torrent_name") == torrent_name
    verify_result(data, expected_data)


@pytest.mark.run(order=4)
def test_put_torrent_not_posted(client):
    """
    Test that :meth:`~torrent_name_analyzer.app.put_torrent` returns a response
    code of (201), which will mean that we cannot update a torrent that doesnt
    exist in database.
    """
    fake_torrent = "Fake TvShow S01E01"
    response = client.put(
        f"{torrents_end_point}/{fake_torrent}", content_type="application/json"
    )
    msg = json.loads(response.get_data(as_text=True))
    assert response.status_code == 201
    assert msg == TORRENT_NOT_EXIST_IN_DB_MESSAGE.format(
        torrent_name=fake_torrent
    )


@pytest.mark.parametrize("get_by", (1, api_test_get[0]))
@pytest.mark.run(order=5)
def test_get_by_success(client, get_by):
    """
    Test that :meth:`~torrent_name_analyzer.app.get_torrent` and
    :meth:`~torrent_name_analyzer.app.get_torrent_by_name` returns a response
    code of (200), which will mean that we successfully got a response from the
    server alongside the corresponding json data.
    """
    torrent_name, expected_data = api_test_get
    expected_id = 1
    response = client.get(
        f"{torrents_end_point}/{get_by}", content_type="application/json"
    )
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data.pop("torrent_id") == expected_id
    assert data.pop("torrent_name") == torrent_name
    assert (len(data.pop("timestamp")) > 0) is True
    for k, v in data.items():
        if k in expected_data:
            expected_value = expected_data[k]
            if k in SPECIAL_KEYS:
                if isinstance(expected_value, int):
                    expected_value = str(expected_value)
                elif isinstance(expected_value, list):
                    expected_value = ", ".join(expected_value)
            assert v == expected_value
        else:
            assert v is None


@pytest.mark.run(order=6)
def test_get_torrents_success(client):
    """
    Test that :meth:`~torrent_name_analyzer.app.get_torrents`  returns a
    response code of (200), which will mean that we successfully got a response
    from the server alongside the corresponding json data (a list of torrent
    parsed items).
    """
    response = client.get(
        f"{torrents_end_point}", content_type="application/json"
    )
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert isinstance(data, list) is True
    assert len(data) == len(api_test_post)


@pytest.mark.parametrize("status_code", (204, 404))
@pytest.mark.run(order=7)
def test_delete_torrent(client, status_code):
    """
    Test :meth:`~torrent_name_analyzer.app.remove_torrent` that we are able to
    delete items from database (204) and also we make a test to check that the
    server returns an error status code in case that we try to remove a torrent
    that doesnt exists (404).
    """
    torrent_id = len(api_test_post)

    del_end_point = f"{torrents_end_point}/{torrent_id}"
    response = client.delete(del_end_point, content_type="application/json")
    assert response.status_code == status_code
