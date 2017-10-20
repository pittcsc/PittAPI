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

import grequests
from typing import Dict, List, Any


def _get_all_locations():
    """Creates generator of responses to fetch data on all dining locations"""
    request_objs = []
    for i in range(3):
        payload = {
            "_kgoui_object": "kgoui_Rcontent_I2",
            "feed": "dining_locations",
            "start": i * 10
        }
        request_objs.append(grequests.get("https://m.pitt.edu/dining/index.json", params=payload))
    resps = grequests.imap(request_objs)
    return resps


def get_locations():
    """Gets information about all dining locations"""
    return get_locations_by_status(None)


def get_locations_by_status(status: str) -> List[Dict[str, Any]]:
    """status can be nil, open, or closed
    None    - returns all dining locations
    'open'   - returns open dining locations
    'closed' - returns closed dining locations"""

    dining_locations = []
    resps = [
        r.json()["response"]['regions'][0]["contents"]
        for r in _get_all_locations()
    ]

    for location in resps:
        for content in location:
            data = {}
            fields = content["fields"]
            if fields["type"] == "loadMore":
                continue
            if status in ['open', 'closed']:
                if status != fields['status']:
                    continue

            if isinstance(fields["title"], dict):
                data["name"] = fields["title"]["value"]
            else:
                data["name"] = fields["title"]
            data["status"] = fields["status"]
            try:
                data["hours"] = fields["eventDate"]["formatted"]
            except TypeError:
                data["hours"] = "unavailable"

            dining_locations.append(data)

    return dining_locations


# def get_location_by_name(location):
#    try:
#        return get_locations()[location]
#    except:
#        raise ValueError('The dining location is invalid')

# def get_location_menu(location=None, date=None):
# location can only be market, market's subordinates, and cathedral cafe
# if location is none, return all menus, and date will be ignored
# date has to be a day of the week, or if empty will return menus for all days of the week
#
# https://www.pc.pitt.edu/dining/menus/flyingStar.php
# https://www.pc.pitt.edu/dining/menus/bellaTrattoria.php
# https://www.pc.pitt.edu/dining/menus/basicKneads.php
# https://www.pc.pitt.edu/dining/menus/basicKneads.php
# https://www.pc.pitt.edu/dining/menus/magellans.php
# https://www.pc.pitt.edu/dining/locations/cathedralCafe.php
#    return []
