from pathlib import Path

import pytest
import responses
from bs4 import BeautifulSoup

from pittapi.people import PEOPLE_SEARCH_URL, PeopleClient, Person, PersonField, parse_segments

SAMPLES = Path("tests/samples")


@responses.activate
def test_people_search_returns_models():
    html = (SAMPLES / "people_ramirez_mock_response.html").read_text()
    responses.add(responses.POST, PEOPLE_SEARCH_URL, body=html)

    people = PeopleClient().get_person("John C Ramirez")

    assert isinstance(people[0], Person)
    assert people[0].name == "Ramirez, John C"
    assert PersonField("Office Phone", ("(412) 624-8441",)) in people[0].fields


@responses.activate
def test_too_many_and_no_people():
    too_many = (SAMPLES / "people_too_many_mock_response.html").read_text()
    responses.add(responses.POST, PEOPLE_SEARCH_URL, body=too_many)
    with pytest.raises(ValueError, match="too many people"):
        PeopleClient().get_person("Smith")

    none = (SAMPLES / "people_none_mock_response.html").read_text()
    responses.add(responses.POST, PEOPLE_SEARCH_URL, body=none)
    assert PeopleClient().get_person("Nobody") == ()


def test_segments_preserve_unknown_labels_and_collect_repeated_values():
    soup = BeautifulSoup(
        """
        <div>
          <span class="row-label"></span><span>Ignored</span>
          <span class="row-label">Unknown</span><span>Preserved</span>
          <span class="row-label">Email</span>
          <span></span><span>one@example.edu</span><span>two@example.edu</span>
        </div>
        """,
        "html.parser",
    )
    assert parse_segments(soup.select("span")) == (
        PersonField("Unknown", ("Preserved",)),
        PersonField("Email", ("one@example.edu", "two@example.edu")),
    )
