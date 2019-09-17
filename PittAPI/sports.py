'''
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
'''

import json
import requests

FOOTBALL_URL = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/pitt'
BASKETBALL_URL = 'http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/pittsburgh'

football_response = requests.get(FOOTBALL_URL)
basketball_response = requests.get(BASKETBALL_URL)

football_data = json.loads(football_response.text)
basketball_data = json.loads(basketball_response.text)


# basketball methods

# get_basketball_record() is a method designed to get the current record of the Men's basketball team via string.
#   - During the off-season this data should return "There's no record right now".

# get_next_basketball_game(input_parameter: str) is a method to get specific info on the next matchup via string.
#   - in the off-season, this will return info on the latest game played.
#   input_parameter specifies which type of information to get depending on what is entered.
#   - full_name is something like "Pittsburgh Panthers vs.  Penn State Nittany Lions"
#   - short_name is something like "PITT vs. PSU"
#   - season_name is something like "Regular Season", "Playoffs", "Pre-season", etc.
#   - week is something like "Week 19"
#   - court returns the location of the game being played.

# get_basketball_standings simply returns a string resembling something like "14th in ACC"


def get_basketball_record() -> str:
    try:
        record_summary = basketball_data['team']['record']['items'][0]['summary']

    except KeyError:
        record_summary = "There's no record right now."

    return record_summary


def get_next_basketball_game(input_parameter: str) -> str:

    return_value = "Error: Input parameter"

    if input_parameter == "full_name":
        return_value = basketball_data['team']['nextEvent'][0]['name']
    if input_parameter == "short_name":
        return_value = basketball_data['team']['nextEvent'][0]['shortName']

    if input_parameter == "season_name":
        return_value = basketball_data['team']['nextEvent'][0]['seasonType']['name']

    if input_parameter == "week":
        return_value = basketball_data['team']['nextEvent'][0]['week']['text']

    if input_parameter == "court":
        return_value = basketball_data['team']['nextEvent'][0]['competitions'][0]['venue']['fullName']

    return return_value


def get_basketball_standings() -> str:
    return_value = basketball_data['team']['standingSummary']
    return return_value


# end basketball methods


# football methods
# get_football_record() is a method designed to get the current record of the Men's basketball team.
#   - During the off-season this data should return "There's no record right now" TODO: ADD THIS EXCEPTION CATCH

# get_next_football_game(input_parameter: str) is a method to get specific info on the next matchup.
#   - in the off-season, this will return info on the latest game played.
# input_parameter specifies which type of information to get depending on what is entered.
#   - full_name is something like "Pittsburgh Panthers vs.  Penn State Nittany Lions"
#   - short_name is something like "PITT vs. PSU"
#   - season_name is something like "Regular Season", "Playoffs", "Pre-season", etc.
#   - week is something like "Week 19"
#   - field returns the location of the game being played.

# get_basketball_standings simply returns a string resembling something like "14th in ACC"


def get_football_record() -> str:
    record_summary = football_data['team']['record']['items'][0]['summary']
    return record_summary


def get_next_football_game(input_parameter: str) -> str:

    return_value = "Error: Input parameter"

    if input_parameter == "full_name":
        return_value = football_data['team']['nextEvent'][0]['name']
    if input_parameter == "short_name":
        return_value = football_data['team']['nextEvent'][0]['shortName']

    if input_parameter == "season_name":
        return_value = football_data['team']['nextEvent'][0]['seasonType']['name']

    if input_parameter == "week":
        return_value = football_data['team']['nextEvent'][0]['week']['text']

    if input_parameter == "field":
        return_value = football_data['team']['nextEvent'][0]['competitions'][0]['venue']['fullName']

    return return_value


def get_football_standings() -> str:
    return_value = football_data['team']['standingSummary']
    return return_value
