'''
The Pitt API, to access workable football_data of the University of Pittsburgh
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
BASKETBALL_URL ='http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/pittsburgh'

football_response = requests.get(FOOTBALL_URL)
basketball_response = requests.get(BASKETBALL_URL)

football_data = json.loads(football_response.text)  # JSON for football football_data in an object
basketball_data = json.loads(basketball_response.text)

# basketball methods
def get_basketball_record() -> str:
    try:
        record_summary = basketball_data['team']['record']['items'][0]['summary']

    except KeyError:
        record_summary = "There's no record right now."
    return record_summary


# football methods
def get_football_record() -> str:
    record_summary = football_data['team']['record']['items'][0]['summary']
    return record_summary


def get_next_football_game(input : str) -> str:

    return_value = "Error: Input parameter"

    if input == "full_name":
        return_value = football_data['team']['nextEvent'][0]['name']
    if input == "short_name":
        return_value = football_data['team']['nextEvent'][0]['shortName']

    if input == "season_name":
        return_value = football_data['team']['nextEvent'][0]['seasonType']['name']

    if input == "week":
        return_value = football_data['team']['nextEvent'][0]['week']['text']

    if input == "field":
        return_value = football_data['team']['nextEvent'][0]['competitions'][0]['venue']['fullName']

    return return_value


def get_football_standings() -> str:
    return_value = football_data['team']['standingSummary']
    return return_value


print("_______________\nBASKETBALL")
print(get_basketball_record())
print("_______________\nFOOTBALL")

print("Record:")
print(get_football_record())
print("Next Game")
print(get_next_football_game("full_name"))
print(get_next_football_game("short_name"))
print(get_next_football_game("season_name"))
print(get_next_football_game("week"))
print("Location:")
print(get_next_football_game("field"))
print("Standings")
print(get_football_standings())