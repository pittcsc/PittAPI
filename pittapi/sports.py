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
"""

import json
from typing import Dict, NamedTuple
import requests

FOOTBALL_URL = (
    "http://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/pitt"
)
BASKETBALL_URL = "http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/pittsburgh"


class NextBasketballGame(NamedTuple):
    name: str
    short_name: str
    season_name: str
    week: int
    court: str


class NextFootballGame(NamedTuple):
    name: str
    short_name: str
    season_name: str
    week: int
    court: str


def get_mens_basketball_record() -> str:
    """returns the current record of the men's basketball team"""
    basketball_response = requests.get(BASKETBALL_URL)
    basketball_data = basketball_response.json()

    try:
        record_summary = basketball_data["team"]["record"]["items"][0]["summary"]

    except KeyError:
        record_summary = "There's no record right now."

    return record_summary


def get_next_mens_basketball_game() -> NextBasketballGame:
    """returns a dict containing details of the next scheduled men's basketball game."""
    basketball_response = requests.get(BASKETBALL_URL)
    basketball_data = basketball_response.json()

    next_game = NextBasketballGame(
        name=basketball_data["team"]["nextEvent"][0]["name"],
        short_name=basketball_data["team"]["nextEvent"][0]["shortName"],
        season_name=basketball_data["team"]["nextEvent"][0]["seasonType"]["name"],
        week=basketball_data["team"]["nextEvent"][0]["week"]["text"],
        court=basketball_data["team"]["nextEvent"][0]["competitions"][0]["venue"][
            "fullName"
        ],
    )

    return next_game


def get_mens_basketball_standings():
    """returns a string describing the placement of the men's basketball team. eg: '14th in ACC' """
    basketball_response = requests.get(BASKETBALL_URL)
    basketball_data = basketball_response.json()

    return_value = basketball_data["team"]["standingSummary"]
    return return_value


def get_football_record() -> str:
    """returns the current record of the men's football team"""
    football_response = requests.get(FOOTBALL_URL)
    football_data = football_response.json()

    try:
        record_summary = football_data["team"]["record"]["items"][0]["summary"]

    except KeyError:
        record_summary = "There's no record right now."

    return record_summary


def get_next_football_game() -> NextFootballGame:
    """returns a dict containing details of the next scheduled football game."""
    football_response = requests.get(FOOTBALL_URL)
    football_data = football_response.json()

    next_game = NextFootballGame(
        name=football_data["team"]["nextEvent"][0]["name"],
        short_name=football_data["team"]["nextEvent"][0]["shortName"],
        season_name=football_data["team"]["nextEvent"][0]["seasonType"]["name"],
        week=football_data["team"]["nextEvent"][0]["week"]["text"],
        field=football_data["team"]["nextEvent"][0]["competitions"][0]["venue"][
            "fullName"
        ],
    )

    return next_game


def get_football_standings() -> str:
    """returns a string describing the placement of the football team. eg: '14th in ACC' """
    football_response = requests.get(FOOTBALL_URL)
    football_data = football_response.json()

    return_value = football_data["team"]["standingSummary"]
    return return_value
