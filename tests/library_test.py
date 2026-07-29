import json
from pathlib import Path

import pytest
import responses

from pittapi.library import LIBRARY_URL, QUERY_START, STUDY_ROOMS_URL, Document, LibraryClient

SAMPLES = Path("tests/samples")
QUERY_DATA = json.loads((SAMPLES / "library_mock_response_water.json").read_text())
ROOM_DATA = json.loads((SAMPLES / "hillman_study_room_mock_response.json").read_text())


@responses.activate
def test_get_documents():
    responses.add(responses.GET, LIBRARY_URL + QUERY_START + "water+cycle", json=QUERY_DATA)
    result = LibraryClient().get_documents("water cycle")
    assert result.num_pages == 10
    assert len(result.documents) == 10
    assert isinstance(result.documents[0], Document)
    assert isinstance(result.documents[0].title, tuple)


@responses.activate
def test_bookmark_success_unrelated_error_and_invalid():
    responses.add(responses.GET, LIBRARY_URL + "&bookMark=valid", json=QUERY_DATA)
    assert LibraryClient().get_document_by_bookmark("valid").num_pages == 10

    unrelated = QUERY_DATA | {"errors": [{"code": "other"}]}
    responses.add(responses.GET, LIBRARY_URL + "&bookMark=other", json=unrelated)
    assert LibraryClient().get_document_by_bookmark("other").num_pages == 10

    responses.add(
        responses.GET,
        LIBRARY_URL + "&bookMark=bad",
        json={"errors": [{"code": "invalid.bookmark.format"}]},
    )
    with pytest.raises(ValueError, match="invalid bookmark"):
        LibraryClient().get_document_by_bookmark("bad")


@responses.activate
def test_room_reservations_and_empty_data():
    responses.add(responses.GET, STUDY_ROOMS_URL, json=ROOM_DATA)
    responses.add(responses.GET, STUDY_ROOMS_URL, json=ROOM_DATA)
    responses.add(responses.GET, STUDY_ROOMS_URL, json={"data": None})
    client = LibraryClient()
    assert client.hillman_total_reserved() == 4
    assert len(client.reserved_hillman_times()) == 4
    assert client.reserved_hillman_times() == ()


@responses.activate
def test_malformed_library_responses():
    responses.add(responses.GET, LIBRARY_URL + QUERY_START + "bad", json={})
    with pytest.raises(ValueError, match="library response"):
        LibraryClient().get_documents("bad")

    responses.add(responses.GET, STUDY_ROOMS_URL, json={})
    with pytest.raises(ValueError, match="missing its total"):
        LibraryClient().hillman_total_reserved()

    responses.add(responses.GET, STUDY_ROOMS_URL, json={})
    with pytest.raises(ValueError, match="reservation response"):
        LibraryClient().reserved_hillman_times()
