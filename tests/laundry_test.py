import json
from pathlib import Path

import pytest
import responses

from pittapi.laundry import (
    BASE_URL,
    LOCATION_IDS,
    BuildingStatus,
    LaundryClient,
    infer_combo_type,
    parse_laundry_object,
)

SAMPLES = Path("tests/samples")
HOLLAND_DATA = json.loads((SAMPLES / "laundry_mock_response_holland.json").read_text())
TOWERS_DATA = json.loads((SAMPLES / "laundry_mock_response_towers.json").read_text())


@pytest.mark.parametrize(
    ("building", "data", "expected"),
    [
        ("HOLLAND", HOLLAND_DATA, BuildingStatus("HOLLAND", 0, 14, 15, 21)),
        ("towers", TOWERS_DATA, BuildingStatus("TOWERS", 1, 54, 1, 55)),
    ],
)
@responses.activate
def test_building_status(building, data, expected):
    responses.add(responses.GET, BASE_URL.format(location=LOCATION_IDS[building.upper()]), json=data)
    assert LaundryClient().get_building_status(building) == expected


@responses.activate
def test_machine_statuses_are_models():
    responses.add(responses.GET, BASE_URL.format(location=LOCATION_IDS["HOLLAND"]), json=HOLLAND_DATA)
    machines = LaundryClient().get_laundry_machine_statuses("HOLLAND")
    assert len(machines) == 35
    assert any(machine.time_left is None for machine in machines)
    assert any(machine.time_left is not None for machine in machines)


def test_invalid_building_and_payload():
    with pytest.raises(ValueError, match="invalid laundry building"):
        LaundryClient().get_laundry_machine_statuses("Missing")


@responses.activate
def test_malformed_payload():
    responses.add(responses.GET, BASE_URL.format(location=LOCATION_IDS["HOLLAND"]), json={})
    with pytest.raises(ValueError, match="missing required data"):
        LaundryClient().get_laundry_machine_statuses("HOLLAND")


def test_object_parsing_variants():
    available = {
        "type": "washFL",
        "appliance_desc": "Washer 2",
        "appliance_desc_key": "1",
        "time_left_lite": "Available",
        "time_remaining": 0,
        "type2": "dry",
        "appliance_desc2": "Dryer 3",
        "appliance_desc_key2": "2",
        "time_left_lite2": "Offline",
        "time_remaining2": 4,
    }
    machines = parse_laundry_object(available)
    assert machines[0].type == "washer"
    assert machines[1].type == "dryer"
    assert machines[1].time_left is None

    combo = available | {"type": "washNdry"}
    assert len(parse_laundry_object(combo)) == 2
    assert parse_laundry_object({"type": "table"}) == ()


def test_infer_combo_type_rejects_bad_name():
    assert infer_combo_type("Dryer 3") == "dryer"
    with pytest.raises(ValueError, match="invalid name"):
        infer_combo_type("No number")
