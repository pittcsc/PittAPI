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

from typing import NamedTuple
import requests

FOOTBALL_URL = (
    "http://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/pitt"
)
BASKETBALL_URL = "http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/pittsburgh"


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


def get_next_mens_basketball_game() -> dict:
    """returns a dict containing details of the next scheduled men's basketball game."""
    basketball_response = requests.get(BASKETBALL_URL)
    basketball_data = basketball_response.json()
    next_game = None
    try:
        next_game = basketball_data["team"]["nextEvent"][0]
        opponent = None
        homeaway = None
        status = None
        if next_game["competitions"][0]["status"]["type"]["name"] == "STATUS_FINAL":
            status = "GAME_COMPLETE"
        elif next_game["competitions"][0]["status"]["type"]["name"] == "STATUS_IN_PROGRESS":
            status = "IN_PROGRESS"
        if next_game["competitions"][0]["competitors"][0]["id"] == 221:
            opponent = next_game["competitions"][0]["competitors"][0]
            homeaway = next_game["competitions"][0]["competitors"][0]["homeAway"]
        else:
            opponent = next_game["competitions"][0]["competitors"][1]
            homeaway = next_game["competitions"][0]["competitors"][1]["homeAway"]
        return {
            "Timestamp" : next_game["date"],
            "Oppponent" : {
                "id" : opponent["team"]["id"],
                "school" : opponent["team"]["nickname"],
                "name" : opponent["team"]["displayName"]
            },
            "HomeAway" : homeaway,
            "Location" : next_game["competitions"][0]["venue"],
            "Status" : status
        }
    except IndexError:
        return {
            "Status" : "OFFSEASON"
        }


def get_mens_basketball_standings() -> str:
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


def get_next_football_game() -> dict:
    football_response = requests.get(FOOTBALL_URL)
    football_data = football_response.json()
    next_game = None
    try:
        next_game = football_data["team"]["nextEvent"][0]
        opponent = None
        homeaway = None
        status = None
        if next_game["competitions"][0]["status"]["type"]["name"] == "STATUS_FINAL":
            status = "GAME_COMPLETE"
        elif next_game["competitions"][0]["status"]["type"]["name"] == "STATUS_IN_PROGRESS":
            status = "IN_PROGRESS"
        if next_game["competitions"][0]["competitors"][0]["id"] == 221:
            opponent = next_game["competitions"][0]["competitors"][1]
            homeaway = next_game["competitions"][0]["competitors"][0]["homeAway"]
        else:
            opponent = next_game["competitions"][0]["competitors"][0]
            homeaway = next_game["competitions"][0]["competitors"][1]["homeAway"]
        return {
            "Timestamp" : next_game["date"],
            "Oppponent" : {
                "id" : opponent["team"]["id"],
                "school" : opponent["team"]["nickname"],
                "name" : opponent["team"]["displayName"]
            },
            "HomeAway" : homeaway,
            "Location" : next_game["competitions"][0]["venue"],
            "Status" : status
        }
    except IndexError:
        return {
            "Status" : "OFFSEASON"
        }


def get_football_standings() -> str:
    """returns a string describing the placement of the football team. eg: '14th in ACC' """
    football_response = requests.get(FOOTBALL_URL)
    football_data = football_response.json()

    return_value = football_data["team"]["standingSummary"]
    return return_value
