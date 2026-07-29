import json
from pathlib import Path

import pytest
import responses

from pittapi.laundry import (
    CURRENT_ROOM_URL,
    LOCATIONS_URL,
    SCHOOL_ID,
    BuildingStatus,
    LaundryClient,
    LaundryLocation,
    MachineStatus,
    infer_combo_type,
    parse_laundry_object,
    parse_machine,
)

SAMPLES = Path("tests/samples")
HOLLAND_DATA = json.loads((SAMPLES / "laundry_mock_response_holland.json").read_text())
TOWERS_DATA = json.loads((SAMPLES / "laundry_mock_response_towers.json").read_text())
HOLLAND = LaundryLocation("2430137", "Holland Hall", "Pittsburgh")
TOWERS = LaundryLocation("2430136", "Litchfield Towers", "Pittsburgh")


@pytest.mark.parametrize(
    ("location", "data", "expected"),
    [
        (HOLLAND, HOLLAND_DATA, BuildingStatus("Holland Hall", 0, 14, 15, 21)),
        (TOWERS, TOWERS_DATA, BuildingStatus("Litchfield Towers", 1, 54, 1, 55)),
    ],
)
@responses.activate
def test_building_status(location, data, expected):
    responses.add(responses.GET, CURRENT_ROOM_URL, json=data)
    assert LaundryClient().get_building_status(location) == expected


@responses.activate
def test_location_discovery_preserves_order_and_ignores_unknown_fields():
    data = {
        "room_data": [
            {
                "laundry_room_location": 2430137,
                "laundry_room_name": "Holland Hall",
                "campus_name": "Pittsburgh",
                "unknown": "ignored",
            },
            {
                "laundry_room_location": "2430136",
                "laundry_room_name": "Litchfield Towers",
                "campus_name": "Pittsburgh",
            },
        ]
    }
    responses.add(responses.GET, LOCATIONS_URL, json=data)
    assert LaundryClient().get_locations() == (HOLLAND, TOWERS)
    assert responses.calls[0].request.url.endswith(f"cui=1&loc={SCHOOL_ID}")


@responses.activate
def test_machine_statuses_are_models():
    responses.add(responses.GET, CURRENT_ROOM_URL, json=HOLLAND_DATA)
    machines = LaundryClient().get_machine_statuses(HOLLAND)
    assert len(machines) == 35
    assert any(machine.minutes_remaining is None for machine in machines)
    assert any(machine.minutes_remaining is not None for machine in machines)
    assert all(machine.model_number for machine in machines)


@pytest.mark.parametrize("payload", [{}, {"room_data": [{}]}])
@responses.activate
def test_malformed_location_discovery(payload):
    responses.add(responses.GET, LOCATIONS_URL, json=payload)
    with pytest.raises(ValueError, match="discovery response"):
        LaundryClient().get_locations()


@responses.activate
def test_malformed_payload():
    responses.add(responses.GET, CURRENT_ROOM_URL, json={})
    with pytest.raises(ValueError, match="missing required data"):
        LaundryClient().get_machine_statuses(HOLLAND)


def test_object_parsing_variants():
    available = {
        "type": "washFL",
        "appliance_desc": "Washer 2",
        "appliance_desc_key": "1",
        "model_number": "WASHER",
        "average_run_time": 30,
        "status_toggle": 0,
        "time_left_lite": "Available",
        "time_remaining": 0,
        "percentage": 0,
        "manualStack": True,
        "type2": "dry",
        "appliance_desc2": "Dryer 3",
        "appliance_desc_key2": "2",
        "model_number2": "DRYER",
        "average_run_time2": 60,
        "status_toggle2": 4,
        "time_left_lite2": "Offline",
        "time_remaining2": 4,
        "percentage2": 0,
    }
    machines = parse_laundry_object(available)
    assert machines[0].type == "washer"
    assert machines[0].status is MachineStatus.AVAILABLE
    assert machines[0].is_available
    assert machines[0].minutes_remaining is None
    assert machines[0].is_stacked
    assert machines[1].type == "dryer"
    assert machines[1].status is MachineStatus.OFFLINE
    assert not machines[1].is_available

    combo = available | {"type": "washNdry"}
    combo_machines = parse_laundry_object(combo)
    assert len(combo_machines) == 2
    assert all(machine.is_combo for machine in combo_machines)

    double_dryer = available | {"type": "dblDry", "stacked": True}
    assert tuple(machine.type for machine in parse_laundry_object(double_dryer)) == ("dryer", "dryer")
    assert parse_laundry_object({"type": "table"}) == ()


def test_infer_combo_type_rejects_bad_name():
    assert infer_combo_type("Dryer 3") == "dryer"
    with pytest.raises(ValueError, match="invalid name"):
        infer_combo_type("No number")


@pytest.mark.parametrize(
    ("status", "message"),
    [
        (MachineStatus.AVAILABLE, "Available"),
        (MachineStatus.IDLE, "Idle"),
        (MachineStatus.RUNNING, "15 min remaining"),
        (MachineStatus.OUT_OF_SERVICE, "Out of service"),
        (MachineStatus.OFFLINE, "Offline"),
    ],
)
def test_status_codes_are_the_source_of_truth(status, message):
    data = {
        "appliance_desc": "Machine 1",
        "appliance_desc_key": "1",
        "model_number": "MODEL",
        "average_run_time": 30,
        "status_toggle": status,
        "time_left_lite": message,
        "time_remaining": 15,
        "percentage": 50,
    }

    machine = parse_machine(data, "washer")

    assert machine.status is status
    assert machine.status_message == message
    expected_minutes = 15 if status is MachineStatus.RUNNING else None
    assert machine.minutes_remaining == expected_minutes
    expected_progress = 50 if status is MachineStatus.RUNNING else None
    assert machine.cycle_progress_percent == expected_progress


def test_running_machine_ignores_invalid_progress_and_unknown_status():
    data = {
        "appliance_desc": "Machine 1",
        "appliance_desc_key": "1",
        "average_run_time": 30,
        "status_toggle": MachineStatus.RUNNING,
        "time_left_lite": "Ext. Cycle",
        "time_remaining": 0,
        "percentage": 120,
    }
    assert parse_machine(data, "dryer").cycle_progress_percent is None

    data["status_toggle"] = 99
    with pytest.raises(ValueError, match="unknown laundry status code"):
        parse_machine(data, "dryer")
