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

import requests
import grequests
from bs4 import BeautifulSoup, SoupStrainer
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

sess = requests.session()


def _get_all_locations():
    request_objs = []
    for i in range(0,3):
        payload = (
            ("_region", "kgoui_Rcontent_I1_Ritems"),
            ("feed", "dining_locations"),
            ("start", i*10)
        )
        request_objs.append(grequests.get("https://m.pitt.edu/dining/index.json", params=payload))

    resps = grequests.imap(request_objs)
    return resps


def get_locations():
    return get_locations_by_status()


def get_locations_by_status(status=None):
    # status can be nil, open, or closed
    # None     - returns all dining locations
    # 'all'    - same as None (or anything else)
    # 'open'   - returns open dining locations
    # 'closed' - returns closed dining locations

    dining_locations = []

    resps = _get_all_locations()
    resps = [r.json()["response"]["contents"] for r in resps]

    for content in resps:
        for item in content:
            data = {}
            fields = item["fields"]
            if fields["type"] == "loadMore":
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

    dining_locations = [dict(t) for t in set([tuple(d.items()) for d in dining_locations])]
    return dining_locations


def get_location_by_name(location):
    try:
        return get_locations()[location]
    except:
        raise ValueError('The dining location is invalid')


def get_location_menu(location=None, date=None):
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
    return
