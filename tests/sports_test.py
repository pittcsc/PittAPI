import pytest
import responses

from pittapi.sports import (
    FOOTBALL_URL,
    MENS_BASKETBALL_URL,
    GameInfo,
    SportsClient,
    Team,
    find_competitors,
    parse_next_game,
    parse_record,
    parse_standings,
)


def team_data(status="STATUS_FINAL"):
    return {
        "team": {
            "id": "221",
            "record": {"items": [{"summary": "11-21"}]},
            "standingSummary": "12th in ACC",
            "nextEvent": [
                {
                    "date": "2022-03-08T19:00Z",
                    "competitions": [
                        {
                            "venue": {
                                "fullName": "Barclays Center",
                                "address": {"city": "Brooklyn", "state": "NY"},
                            },
                            "competitors": [
                                {
                                    "id": 221,
                                    "homeAway": "home",
                                    "team": {
                                        "id": 221,
                                        "nickname": "Pittsburgh",
                                        "displayName": "Pittsburgh Panthers",
                                    },
                                },
                                {
                                    "id": "103",
                                    "homeAway": "away",
                                    "team": {
                                        "id": "103",
                                        "nickname": "Boston College",
                                        "displayName": "Boston College Eagles",
                                    },
                                },
                            ],
                            "status": {"type": {"name": status}},
                        }
                    ],
                }
            ],
        }
    }


@responses.activate
def test_all_sports_client_methods():
    basketball = team_data()
    football = team_data("STATUS_IN_PROGRESS")
    for _ in range(3):
        responses.add(responses.GET, MENS_BASKETBALL_URL, json=basketball)
        responses.add(responses.GET, FOOTBALL_URL, json=football)

    client = SportsClient()
    assert client.get_mens_basketball_record() == "11-21"
    assert client.get_next_mens_basketball_game().status == "GAME_COMPLETE"
    assert client.get_mens_basketball_standings() == "12th in ACC"
    assert client.get_football_record() == "11-21"
    assert client.get_next_football_game().status == "IN_PROGRESS"
    assert client.get_football_standings() == "12th in ACC"


def test_scheduled_game_with_pitt_second():
    data = team_data("STATUS_SCHEDULED")
    data["team"]["nextEvent"][0]["competitions"][0]["competitors"].reverse()

    game = parse_next_game(data)

    assert game.status == "SCHEDULED"
    assert game.home_away == "home"
    assert game.opponent == Team(id="103", school="Boston College", name="Boston College Eagles")
    assert game.location.address.city == "Brooklyn"


def test_no_scheduled_game():
    assert parse_next_game({"team": {"nextEvent": []}}) == GameInfo(status="NO_GAME_SCHEDULED")


def test_record_fallback_and_standings_error():
    assert parse_record({"team": {"record": {}}}) == "There's no record right now."
    with pytest.raises(ValueError, match="missing standings"):
        parse_standings({})


@pytest.mark.parametrize(
    "competitors",
    [
        [],
        [{"id": "1"}, {"id": "2"}],
    ],
)
def test_invalid_competitors(competitors):
    with pytest.raises(ValueError):
        find_competitors(competitors, "221")


def test_malformed_game_data():
    with pytest.raises(ValueError, match="missing game data"):
        parse_next_game({"team": {"nextEvent": [{}]}})


@responses.activate
def test_sports_response_must_be_object():
    responses.add(responses.GET, FOOTBALL_URL, json=[])
    with pytest.raises(ValueError, match="must be an object"):
        SportsClient().get_team_data(FOOTBALL_URL)
