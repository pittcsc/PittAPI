import pytest
import responses

from pittapi.gym import GYM_URL, Gym, GymClient
from tests.mocks.gym_mocks import mock_gym_html


@responses.activate
def test_fetch_all_gyms():
    responses.add(responses.GET, GYM_URL, body=mock_gym_html)

    gyms = GymClient().get_all_gyms_info()

    assert len(gyms) == 8
    assert gyms[0] == Gym(
        name="Baierl Rec Center",
        last_updated="07/09/2024 09:05 AM",
        current_count=100,
        percent_full=50,
    )
    assert gyms[1].percent_full == 0
    assert gyms[2] == Gym(name="Bellefield Hall: Court & Dance Studio")


@responses.activate
def test_get_gym_including_zero_occupancy():
    html = '<div class="barChart">Test Gym|x|Last Count: 0|Updated: now|0%</div>'
    responses.add(responses.GET, GYM_URL, body=html)

    assert GymClient().get_gym_info("Test Gym").current_count == 0


@responses.activate
def test_unknown_gym_raises_lookup_error():
    responses.add(responses.GET, GYM_URL, body=mock_gym_html)
    with pytest.raises(LookupError, match="gym not found"):
        GymClient().get_gym_info("Missing Gym")


def test_missing_percentage_defaults_to_zero():
    gym = Gym.from_text("Test|unused|Last Count: 1|Updated: today")
    assert gym.percent_full == 0
