import pytest
import responses

from pittapi.gym import GYM_URL, Gym, GymClient

GYMS = [
    {
        "LocationId": 1,
        "LocationName": "Campus Recreation",
        "FacilityId": 10,
        "FacilityName": "Baierl Rec Center",
        "TotalCapacity": 200,
        "LastCount": 0,
        "PercetageCapacity": 0,
        "LastUpdatedDateAndTime": "07/09/2024 09:05 AM",
        "IsClosed": False,
        "Ignored": "provider extension",
    },
    {
        "LocationId": 2,
        "LocationName": "Trees Hall",
        "FacilityId": 20,
        "FacilityName": "Trees Fitness Center",
        "TotalCapacity": 100,
        "LastCount": 0,
        "PercetageCapacity": 0,
        "LastUpdatedDateAndTime": "07/09/2024 09:06 AM",
        "IsClosed": True,
    },
]


@responses.activate
def test_fetch_all_gyms_preserves_zero_and_closed_state():
    responses.add(responses.GET, GYM_URL, json=GYMS)

    gyms = GymClient().get_all_gyms_info()

    assert gyms[0] == Gym(
        location_id=1,
        location_name="Campus Recreation",
        facility_id=10,
        facility_name="Baierl Rec Center",
        total_capacity=200,
        current_count=0,
        percent_full=0,
        last_updated="07/09/2024 09:05 AM",
        is_closed=False,
    )
    assert gyms[1].current_count == 0
    assert gyms[1].is_closed


@responses.activate
def test_get_gym_info_and_unknown_gym():
    responses.add(responses.GET, GYM_URL, json=GYMS)
    assert GymClient().get_gym_info("Campus Recreation").facility_id == 10

    responses.add(responses.GET, GYM_URL, json=GYMS)
    with pytest.raises(LookupError, match="gym not found"):
        GymClient().get_gym_info("Missing Gym")


@pytest.mark.parametrize("payload", [{}, [{}]])
@responses.activate
def test_malformed_gym_response(payload):
    responses.add(responses.GET, GYM_URL, json=payload)
    with pytest.raises(ValueError, match="gym response"):
        GymClient().get_all_gyms_info()
