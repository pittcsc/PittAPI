"""
The Pitt API, to access workable data of the University of Pittsburgh
Copyright (C) 2015 Ritwik Gupta

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Pitt football and men's basketball information from ESPN.
"""

from dataclasses import dataclass
from typing import Any

from pittapi.base_client import BaseClient

__all__ = ["Address", "GameInfo", "SportsClient", "Team", "Venue"]

FOOTBALL_URL = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/pitt"
MENS_BASKETBALL_URL = "http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/pittsburgh"
PITT_TEAM_ID = "221"
NO_RECORD = "There's no record right now."


@dataclass(frozen=True, slots=True)
class Team:
    id: str
    school: str
    name: str


@dataclass(frozen=True, slots=True)
class Address:
    city: str
    state: str


@dataclass(frozen=True, slots=True)
class Venue:
    full_name: str
    address: Address


@dataclass(frozen=True, slots=True)
class GameInfo:
    timestamp: str | None = None
    opponent: Team | None = None
    home_away: str | None = None
    location: Venue | None = None
    status: str = "SCHEDULED"


class SportsClient(BaseClient):
    """Fetch Pitt football and men's basketball summaries."""

    def get_mens_basketball_record(self) -> str:
        return parse_record(self.get_team_data(MENS_BASKETBALL_URL))

    def get_next_mens_basketball_game(self) -> GameInfo:
        return parse_next_game(self.get_team_data(MENS_BASKETBALL_URL))

    def get_mens_basketball_standings(self) -> str:
        return parse_standings(self.get_team_data(MENS_BASKETBALL_URL))

    def get_football_record(self) -> str:
        return parse_record(self.get_team_data(FOOTBALL_URL))

    def get_next_football_game(self) -> GameInfo:
        return parse_next_game(self.get_team_data(FOOTBALL_URL))

    def get_football_standings(self) -> str:
        return parse_standings(self.get_team_data(FOOTBALL_URL))

    def get_team_data(self, url: str) -> dict[str, Any]:
        data = self.request("GET", url).json()
        if not isinstance(data, dict):
            raise ValueError("sports response must be an object")
        return data


def parse_record(data: dict[str, Any]) -> str:
    try:
        return data["team"]["record"]["items"][0]["summary"]
    except (KeyError, IndexError, TypeError):
        return NO_RECORD


def parse_standings(data: dict[str, Any]) -> str:
    try:
        return data["team"]["standingSummary"]
    except (KeyError, TypeError) as error:
        raise ValueError("sports response is missing standings") from error


def parse_next_game(data: dict[str, Any]) -> GameInfo:
    try:
        events = data["team"]["nextEvent"]
        if not events:
            return GameInfo(status="NO_GAME_SCHEDULED")
        event = events[0]
        competition = event["competitions"][0]
        pitt, opponent = find_competitors(competition["competitors"])
        opponent_team = opponent["team"]
        venue = competition["venue"]
        status_name = competition["status"]["type"]["name"]
        statuses = {
            "STATUS_FINAL": "GAME_COMPLETE",
            "STATUS_IN_PROGRESS": "IN_PROGRESS",
        }
        return GameInfo(
            timestamp=event["date"],
            opponent=Team(
                id=str(opponent_team["id"]),
                school=opponent_team["nickname"],
                name=opponent_team["displayName"],
            ),
            home_away=pitt["homeAway"],
            location=Venue(
                full_name=venue["fullName"],
                address=Address(city=venue["address"]["city"], state=venue["address"]["state"]),
            ),
            status=statuses.get(status_name, "SCHEDULED"),
        )
    except (KeyError, IndexError, TypeError) as error:
        raise ValueError("sports response is missing game data") from error


def find_competitors(competitors: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    if len(competitors) != 2:
        raise ValueError("a sports competition must contain two teams")
    first, second = competitors
    if str(first["id"]) == PITT_TEAM_ID:
        return first, second
    if str(second["id"]) == PITT_TEAM_ID:
        return second, first
    raise ValueError("Pitt is not present in the competition")
