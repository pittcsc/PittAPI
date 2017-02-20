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

import re

import requests
from bs4 import BeautifulSoup

session = requests.session()

location_dict = {
    'TOWERS': '2430136',
    'BRACKENRIDGE': '2430119',
    'HOLLAND': '2430137',
    'LOTHROP': '2430151',
    'MCCORMICK': '2430120',
    'SUTH_EAST': '2430135',
    'SUTH_WEST': '2430134',
    'FORBES_CRAIG': '2430142'
}


def get_status_simple(building_name):
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

    session.hash_bits_per_character = 5
    """

    building_name = building_name.upper()
    url = 'http://classic.laundryview.com/appliance_status_ajax.php?lr={}'.format(location_dict[building_name])
    page = session.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    # What was I doing...
    re1 = ['(\\d+)', '(\\s+)', '(of)', '(\\s+)', '(\\d+)', '(\\s+)', '((?:[a-z][a-z]+))']

    rg = re.compile(''.join(re1), re.IGNORECASE | re.DOTALL)
    search = rg.findall(str(soup))

    di = {
        u'building': building_name,
        u'free_washers': search[0][0],
        u'total_washers': search[0][4],
        u'free_dryers': search[1][0],
        u'total_dryers': search[1][4]
    }

    return di


def get_status_detailed(building_name):
    building_name = building_name.upper()

    # Get a cookie
    response = requests.get("http://www.laundryview.com/laundry_room.php?view=c&lr={}".format(location_dict[building_name]))
    cookie = response.headers["Set-Cookie"]
    cookie = cookie[cookie.index("=") + 1:cookie.index(";")]

    # Get the weird laundry data
    headers = {"Cookie": "PHPSESSID={}".format(cookie)}
    response = requests.get("http://www.laundryview.com/dynamicRoomData.php?location={}".format(
        location_dict[building_name]), headers=headers).text
    resp_split = response.split('&')[3:]

    cleaned_resp = []
    for status_string in resp_split:
        if "machine" not in status_string:
            continue
        machine_name = status_string[:status_string.index('=')].replace('Status', '')
        status_string = status_string[status_string.index('=') + 1:].strip()

        machine_split = status_string.split("\n")
        machine_split[0] += machine_name

        try:
            machine_split[1] += machine_name
        except IndexError:
            pass

        machine_split = [x.split(':') for x in machine_split]
        cleaned_resp.append(machine_split[0])
        try:
            cleaned_resp.append(machine_split[1])
        except IndexError:
            pass

    cleaned_resp = [x for x in cleaned_resp if len(x) == 10]

    di = []
    for machine in cleaned_resp:
        time_left = -1
        machine_name = "{}_{}".format(machine[9], machine[3])
        machine_status = ""

        if machine[0] is '1':
            machine_status = u'Free'
        else:
            if machine[6] is '':
                machine_status = u'Out of service'
            else:
                machine_status = u'In use'

        if machine_status is u'In use':
            time_left = int(machine[1])
        else:
            time_left = -1 if machine[6] is '' else machine[6]
        di.append({
            u'machine_name': machine_name,
            u'machine_status': machine_status,
            u'time_left': time_left
        })

    return di
