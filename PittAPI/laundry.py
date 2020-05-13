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

import requests
import re
from typing import Any, Dict, List, Union

from bs4 import BeautifulSoup

BASE_URL = 'https://www.laundryview.com/api/currentRoomData?school_desc_key=197&location={}'

LOCATION_LOOKUP = {
    "TOWERS": "2430136",
    "BRACKENRIDGE": "2430119",
    "HOLLAND": "2430137",
    "LOTHROP": "2430151",
    "MCCORMICK": "2430120",
    "SUTH_EAST": "2430135",
    "SUTH_WEST": "2430134",
    "FORBES_CRAIG": "2430142",
}


def _get_laundry_info(building_name: str) -> Any:
    """Returns BeautifulSoup object of laundry view webpage"""
    building_name = building_name.upper()
    url = BASE_URL.format(LOCATION_LOOKUP[building_name])
    response = requests.get(url)
    info = response.json()
    return info


def get_status_simple(building_name: str) -> Dict[str, str]:
    """
    :returns: a dictionary with free washers and dryers as well as total washers
              and dryers for given building

    :param: loc: Building name, case doesn't matter
        -> TOWERS
        -> BRACKENRIDGE
        -> HOLLAND
        -> LOTHROP
        -> MCCORMICK
        -> SUTH_EAST
        -> SUTH_WEST
    """
    laundry_soup = _get_laundry_info(building_name)
    re_format = re.compile(r'^([0-9]+) of ([0-9]+) available$')
    washer_text = laundry_soup.find('span', {'id': 'washer_available'}).text
    dryer_text = laundry_soup.find('span', {'id': 'dryer_available'}).text
    washer_match = re_format.match(washer_text)
    dryer_match = re_format.match(dryer_text)

    return {
        "building": building_name,
        "free_washers": int(washer_match.group(1)),
        "total_washers": int(washer_match.group(2)),
        "free_dryers": int(dryer_match.group(1)),
        "total_dryers": int(dryer_match.group(2)),
    }


def get_status_detailed(building_name: str) -> List[Dict[str, Union[str, int]]]:
    """
    :returns: A list of washers and dryers for the passed
              building location with their statuses

    :param building_name: (String) one of these:
        -> BRACKENRIDGE
        -> HOLLAND
        -> LOTHROP
        -> MCCORMICK
        -> SUTH_EAST
        -> SUTH_WEST
    """
    machines = []
    machine_type = "Unknown"
    laundry_soup = _get_laundry_info(building_name)

    for li in laundry_soup.findAll("li"):
        if "id" in li.attrs:
            machine_type = li.attrs["id"]
            continue

        machine_id = int(li.find("a").attrs["id"])
        machine_status = li.find("p").text
        machine_name = (
            li.text.split(machine_status)[0].encode("ascii", "ignore").decode("utf-8")
        )
        time_left = (
            int(machine_status[: machine_status.find(" ")])
            if "mins left" in machine_status
            else -1
        )

        machines.append(
            {
                "machine_id": machine_id,
                "machine_status": machine_status,
                "machine_name": machine_name,
                "machine_type": machine_type,
                "time_left": time_left,
            }
        )

    return machines
