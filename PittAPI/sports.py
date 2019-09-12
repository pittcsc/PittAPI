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

# temporary URL - need to do more reverse engineering for ESPN's more robust details, or at least figure out
# how the JS navigates different pages.
FOOTBALL_URL = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/pitt'

response = requests.get(FOOTBALL_URL)

data = json.loads(response.text)  # JSON for football data in an object


def get_football_record() -> str:
    record_summary = data['team']['record']['items'][0]['summary']
    return record_summary


def get_next_football_game(input : str) -> str:

    return_value = "Error: Input parameter"

    if input == "full_name":
        return_value = data['team']['nextEvent'][0]['name']
    if input == "short_name":
        return_value = data['team']['nextEvent'][0]['shortName']

    if input == "season_name":
        return_value = data['team']['nextEvent'][0]['seasonType']['name']

    if input == "week":
        return_value = data['team']['nextEvent'][0]['week']['text']

    if input == "field":
        return_value = data['team']['nextEvent'][0]['competitions'][0]['venue']['fullName']

    return return_value


def get_football_standings() -> str:
    return_value = data['team']['standingSummary']
    return return_value


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