import pytest

from pittapi.sports import FOOTBALL_URL, MENS_BASKETBALL_URL, SportsClient
from pittapi.status import StatusClient

pytestmark = pytest.mark.live


@pytest.mark.parametrize("url", [FOOTBALL_URL, MENS_BASKETBALL_URL])
def test_espn_team_feed(url):
    with SportsClient() as sports:
        data = sports.get_team_data(url)

    assert data["team"]["id"]
    assert data["team"]["displayName"]


def test_pitt_service_status():
    with StatusClient() as status:
        summary = status.get_status()

    assert summary.components
    assert all(component.name and component.status for component in summary.components)
