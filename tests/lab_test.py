import pytest
import responses

from pittapi.lab import LOCATIONS_URL, PITT_BASE_URL, Lab, LabClient, LabLocation, parse_lab

LOCATIONS = [
    {
        "ident": "first-id",
        "pname": "Thaw Hall M06",
        "name": "Pitt Digital Lab: Thaw Hall M06",
        "title": "Thaw Hall M06",
        "publish": True,
        "unknown": "ignored",
    },
    {
        "ident": "hidden-id",
        "pname": "Hidden Lab",
        "name": "Hidden Lab",
        "title": "Hidden Lab",
        "publish": False,
    },
    {
        "ident": "second-id",
        "pname": "Hillman",
        "name": "Hillman",
        "title": "Hillman",
        "publish": True,
    },
]


def lab_url(location):
    return f"{PITT_BASE_URL}{location.id}/status.json?noredir=1"


def lab_response(name):
    return {"hours": {name: {"closed": False}}, "state": {}}


@responses.activate
def test_discover_published_labs_in_provider_order():
    responses.add(responses.GET, LOCATIONS_URL, json={"results": {"maps": LOCATIONS}})

    locations = LabClient().get_locations()

    assert locations == (
        LabLocation("first-id", "Thaw Hall M06", "Thaw Hall M06"),
        LabLocation("second-id", "Hillman", "Hillman"),
    )


@responses.activate
def test_get_status():
    location = LabLocation("first-id", "Thaw Hall M06", "Thaw Hall M06")
    responses.add(responses.GET, lab_url(location), json=lab_response(location.title))

    result = LabClient().get_status(location)

    assert result == Lab(
        name="Thaw Hall M06",
        is_closed=False,
        available_computers=0,
        off_computers=0,
        in_use_computers=0,
        out_of_service_computers=0,
        total_computers=0,
    )


@responses.activate
def test_get_all_statuses_preserves_discovery_order():
    locations = (
        LabLocation("first-id", "Thaw Hall M06", "Thaw Hall M06"),
        LabLocation("second-id", "Hillman", "Hillman"),
    )
    responses.add(responses.GET, LOCATIONS_URL, json={"results": {"maps": LOCATIONS}})
    for location in locations:
        responses.add(responses.GET, lab_url(location), json=lab_response(location.title))

    labs = LabClient().get_all_statuses()
    assert tuple(lab.name for lab in labs) == ("Thaw Hall M06", "Hillman")


@pytest.mark.parametrize("payload", [{}, {"results": {"maps": [{}]}}])
@responses.activate
def test_malformed_location_discovery(payload):
    responses.add(responses.GET, LOCATIONS_URL, json=payload)
    with pytest.raises(ValueError, match="discovery response"):
        LabClient().get_locations()


def test_parse_all_machine_states():
    data = {
        "hours": {"Test Lab": {"closed": True}},
        "state": {
            "off": {"up": 0},
            "available": {"up": 1},
            "used": {"up": 2},
            "service": {"up": 3},
        },
    }
    result = parse_lab(data)
    assert result.is_closed
    assert result.off_computers == 1
    assert result.available_computers == 1
    assert result.in_use_computers == 1
    assert result.out_of_service_computers == 1


def test_parse_rejects_unknown_state():
    data = {"hours": {"Test": {"closed": False}}, "state": {"machine": {"up": 99}}}
    with pytest.raises(ValueError, match="unknown computer state for unknown computer"):
        parse_lab(data)


def test_parse_rejects_missing_data():
    with pytest.raises(ValueError, match="missing required data"):
        parse_lab({})
