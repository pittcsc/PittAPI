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
from enum import Enum

from bs4 import BeautifulSoup

BASE_URL = 'https://www.laundryview.com/api/currentRoomData?school_desc_key=197&location={}'
LOCATION_LOOKUP = {
    'TOWERS': '2430136',
    'BRACKENRIDGE': '2430119',
    'HOLLAND': '2430137',
    'LOTHROP': '2430151',
    'MCCORMICK': '2430120',
    'SUTH_EAST': '2430135',
    'SUTH_WEST': '2430134',
    'FORBES_CRAIG': '2430142'
}

class base_status(Enum):
    TOTALW = 0
    TOTALD = 0
    FREEW = 0
    FREED = 0
    INUSE = "In Use"
    AVAIL = "Available"
    OUT = "Out of Service"
    WASHER = "Washer"
    DRYER = "Dryer"

def _get_laundry_soup(building_name: str) -> Any:
    """Returns BeautifulSoup object of laundry view webpage"""
    building_name = building_name.upper()
    url = BASE_URL.format(LOCATION_LOOKUP[building_name])
    response = requests.get(url)
    laundry_soup = BeautifulSoup(response.text, 'lxml')
    return laundry_soup


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
    laundry_soup = _get_laundry_soup(building_name)
    total_washers = base_status.TOTALW.value
    total_dryers = base_status.TOTALD.value
    free_washers = base_status.FREEW.value
    free_dryers = base_status.FREED.value

    machine_dict = parse_soup(laundry_soup)
    # each building has a different system for washer vs dryer
    if(building_name == 'SUTH_EAST'):
        for machine in machine_dict.keys():
            num = int(machine)
            if num >= 5 and num <= 14:
                total_washers += 1
                if (machine_dict[machine] == 0 or machine_dict[machine] == 34):
                    free_washers += 1
            else:
                total_dryers += 1
                if (machine_dict[machine] == 0):
                    free_dryers += 1
    elif building_name == 'SUTH_WEST':
        for machine in machine_dict.keys():
            num = int(machine)
            if num <= 10:
                total_washers += 1
                if (machine_dict[machine] == 34 or machine_dict[machine] == 0 or machine_dict[machine] == 33):
                    free_washers += 1
            else:
                total_dryers += 1
                if (machine_dict[machine] == 0):
                    free_dryers += 1
    elif building_name == 'MCCORMICK':
        for machine in machine_dict.keys():
            num = int(machine)
            if num <= 5:
                total_washers += 1
                if (machine_dict[machine] == 34 or machine_dict[machine] == 0 or machine_dict[machine] == 33):
                    free_washers += 1
            else:
                total_dryers += 1
                if (machine_dict[machine] == 0):
                    free_dryers += 1
    elif building_name == 'BRACKENRIDGE':
        for machine in machine_dict.keys():
            num = int(machine)
            if num <= 8:
                total_washers += 1
                if (machine_dict[machine] == 34 or machine_dict[machine] == 60 or machine_dict[machine] == 33):
                    free_washers += 1
            else:
                total_dryers += 1
                if (machine_dict[machine] == 0):
                    free_dryers += 1
    elif building_name == 'HOLLAND':
        for machine in machine_dict.keys():
            num = int(machine[1:])
            if num <= 6 or num == 14 or num == 15:
                total_dryers += 1
                if (machine_dict[machine] == 0):
                    free_dryers += 1
            else:
                total_washers += 1
                if (machine_dict[machine] == 34 or machine_dict[machine] == 60 or machine_dict[machine] == 33):
                    free_washers += 1
    else:       # lothrop or towers
        for machine in machine_dict.keys():
            num_id = [char for char in machine]
            num = int(num_id[len(num_id) - 1]) % 2
            if (num == 0):  # it is an even code, so it is a washer
                total_washers += 1
                if (machine_dict[machine] == 22):
                    free_washers += 1
            else:  # it is an odd code, so it is a dryer
                total_dryers += 1
                if (machine_dict[machine] == 0):
                    free_dryers += 1

    return {
        'building': building_name,
        'free_washers': int(free_washers),
        'total_washers': int(total_washers),
        'free_dryers': int(free_dryers),
        'total_dryers': int(total_dryers)
    }


def get_status_detailed(building_name: str) -> List[Dict[str, Union[str, int]]]:
    """
    :returns: A list of washers and dryers for the passed
              building location with their statuses

    :param building_name: (String) one of these:
        -> TOWERS
        -> BRACKENRIDGE
        -> HOLLAND
        -> LOTHROP
        -> MCCORMICK
        -> SUTH_EAST
        -> SUTH_WEST
    """
    laundry_soup = _get_laundry_soup(building_name)

    total_washers = base_status.TOTALW.value
    total_dryers = base_status.TOTALD.value
    free_washers = base_status.FREEW.value
    free_dryers = base_status.FREED.value
    in_use_tag = base_status.INUSE.value
    available_tag = base_status.AVAIL.value
    out_of_service_tag = base_status.OUT.value
    washer_tag = base_status.WASHER.value
    dryer_tag = base_status.DRYER.value
    machines = []

    machine_dict = parse_soup(laundry_soup)

    def findWasher():
        machine_type = washer_tag
        if (machine_dict[machine] == 34 or machine_dict[machine] == 60 or machine_dict[machine] == 33):
            machine_status = available_tag
            time_left = 60
        elif (machine_dict[machine] == 60):
            machine_status = out_of_service_tag
            time_left = 0
        else:
            machine_status = in_use_tag
            time_left = 60 - machine_dict[machine]
        machines.append({
            'machine_id': machine,
            'machine_status': machine_status,   #of out service, in use, or available
            'machine_type': machine_type,       # washer or dryer
            'time_left': time_left              # if free, time_left = 60, else some other number
        })
    def findDryer():
        machine_type = dryer_tag
        if (machine_dict[machine] == 0):
            machine_status = available_tag
            time_left = 60
        elif (machine_dict[machine] == 60):
            machine_status = out_of_service_tag
            time_left = 0
        else:
            machine_status = in_use_tag
            time_left = 60 - machine_dict[machine]
        machines.append({
            'machine_id': machine,
            'machine_status': machine_status,   #of out service, in use, or available
            'machine_type': machine_type,       # washer or dryer
            'time_left': time_left              # if free, time_left = 60, else some other number
        })
    # every building has a different system for washer/dryer id, so this accounts for them all
    if(building_name == 'SUTH_EAST'):
        for machine in machine_dict.keys():
            num = int(machine)
            if num >= 5 and num <= 14:
                findWasher()
            else:
                findDryer()
    elif building_name == 'SUTH_WEST':
        for machine in machine_dict.keys():
            num = int(machine)
            if num <= 10:
                findWasher()
            else:
                findDryer()
    elif building_name == 'MCCORMICK':
        for machine in machine_dict.keys():
            num = int(machine)
            if num <= 5:
                findWasher()
            else:
                findDryer()
    elif building_name == 'BRACKENRIDGE':
        for machine in machine_dict.keys():
            num = int(machine)
            if num <= 8:
                findWasher()
            else:
                findDryer()
    elif building_name == 'HOLLAND':
        for machine in machine_dict.keys():
            num = int(machine[1:])
            if num <= 6 or num == 14 or num == 15:
                findDryer()
            else:
                findWasher()
    else:       # it is lothrop or towers
        for machine in machine_dict.keys():
            machine_id = machine
            num_id = [char for char in machine]
            num = int(num_id[len(num_id) - 1]) % 2
            if (num == 0):  # it is an even code, so it is a washer
               findWasher()
            else:  # it is an odd code, so it is a dryer
               findDryer()

    return machines


# used to go through the data on website and get important info
def parse_soup(laundry_soup: str) -> List[Dict[str, Union[str, int]]]:
    laundry_soup = laundry_soup.p.getText() # Get all the text inside <p> brackets
    machine = laundry_soup
    machine_dict = {}                       # this will hold all the info to return
    toFind = 'appliance_desc":'             # this the id of the machine -- first thing to find
    length = len(toFind) + 1
    key_point = machine.find(toFind)  # find first occurance of string
    end_point = machine.rfind(toFind)  # find the last example of this string
    while (key_point < end_point):
        key_end = key_point + length  ## start of string plus string length
        machineInfo = machine[key_end:]
        quotes = machineInfo.find('"')
        machineid = machineInfo[:quotes]    # find the id up until the quotes
        time_key = 'average_run_time":'     # find avg run time keys next
        time_key_length = len(time_key)
        average_time_point = machineInfo.find(time_key) + time_key_length
        average_run_time = int(machineInfo[average_time_point:average_time_point + 2])  # the +2 is the two digits of the runtime
        remaining_key = 'time_remaining":'  # find time remaining on the machine
        remaining_length = len(remaining_key)
        time_remaining_point = machineInfo.find(remaining_key)
        find_comma = machineInfo[time_remaining_point + remaining_length:]
        time_remaining = int(find_comma[:find_comma.find(',')])     # time remaining can vary in number of digits, so we take it up until a comma
        in_use = average_run_time - time_remaining      # how much time is left will tell us if it is in use or not
        machine_dict[machineid] = in_use    # add the id and its time left to the dictionary
        # find number 2 (some machines are duel, so there will be double of all info)
        machine_id2_key = 'appliance_desc2":'
        machine_id2_length = len(machine_id2_key) + 1
        machine_id2 = machineInfo.find(machine_id2_key)
        if(machine_id2 != -1):      # if a second machine DOES exist then do this code
            machine_id2 = machineInfo[machine_id2 + machine_id2_length:]
            quotes2 = machine_id2.find('"')
            machine_id2 = machine_id2[:quotes]
            time2_key = 'average_run_time2":'
            time2_key_length = len(time2_key)
            average_time_point2 = machineInfo.find(time2_key) + time2_key_length
            average_run_time2 = int(machineInfo[(average_time_point2):(average_time_point2 + 2)])
            remaining2_key = 'time_remaining2":'
            remaining2_length = len(remaining2_key)
            time_remaining_point2 = machineInfo.find(remaining2_key)
            find_comma2 = machineInfo[time_remaining_point2 + remaining2_length:]
            time_remaining2 = int(find_comma2[:find_comma2.find(',')])
            in_use2 = average_run_time2 - time_remaining2
            machine_dict[machine_id2] = in_use2
        machine = machineInfo        # update the string so now it searches from end of first example to the end of the string
        key_point = machine.find('appliance_desc":')    # find next id
        end_point = machine.rfind('appliance_desc":') + key_point
    return machine_dict