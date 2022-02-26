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
    'TOWERS': '2430136',
    'BRACKENRIDGE': '2430119',
    'HOLLAND': '2430137',
    'LOTHROP': '2430151',
    'MCCORMICK': '2430120',
    'SUTH_EAST': '2430135',
    'SUTH_WEST': '2430134',
    'FORBES_CRAIG': '2430142'
}


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

    total_machines = len(laundry_soup)     #total number of machines in the laundry room
    total_washers = 0
    total_dryers = 0
    free_washers = 0
    free_dryers = 0
    machine_dict = {}
    out_of_service_washers = []
    out_of_service_dryers = []
    for machine in laundry_soup:
        for machine1 in machine:
            for machine2 in machine1:
                for machine3 in machine2:
                    key_point = machine3.find('appliance_desc":')
                    end_point = machine3.rfind('appliance_desc":')
                    while(key_point<end_point):
                        key_end = key_point+17
                        machine4 = machine3[key_end:]
                        #print(machine4)
                        quotes = machine4.find('"')
                        machineid = machine4[:quotes]
                        #machineid = [char for char in machineid]
                        #machine_num = int(machineid[len(machineid)-1])
                        average_time_point = machine3.find('average_run_time":')
                        average_run_time = int(machine3[average_time_point+18:average_time_point+20])
                        time_remaining_point = machine3.find('time_remaining":')
                        find_comma = machine3[time_remaining_point+16:]
                        time_remaining = int(find_comma[:find_comma.find(',')])
                        in_use = average_run_time - time_remaining
                        machine_dict[machineid] = in_use
                        # find number 2
                        machine_id2 = machine3.find('appliance_desc2":')
                        machine_id2 = machine3[machine_id2+18:]
                        quotes2 = machine_id2.find('"')
                        machine_id2 = machine_id2[:quotes]
                        average_time_point2 = machine3.find('average_run_time2":')
                        average_run_time2 = int(machine3[average_time_point2 + 19:average_time_point2 + 21])
                        time_remaining_point2 = machine3.find('time_remaining2":')
                        find_comma2 = machine3[time_remaining_point2 + 17:]
                        time_remaining2 = int(find_comma2[:find_comma2.find(',')])
                        in_use2 = average_run_time2 - time_remaining2
                        machine_dict[machine_id2] = in_use2
                        machine3 = machine4
                        key_point = machine3.find('appliance_desc":')
                        end_point = machine3.rfind('appliance_desc":') + key_point
                    #print(machine_dict)
    for machine in machine_dict.keys():
        num_id = [char for char in machine]
        num = int(num_id[len(num_id) - 1]) % 2
        if (num == 0):  # it is an even code, so it is a washer
            total_washers += 1
            if (machine_dict[machine] == 22):
                free_washers += 1
            if(machine_dict[machine] == 60):
                out_of_service_washers.append(machine)
        else:  # it is an odd code, so it is a dryer
            total_dryers += 1
            if (machine_dict[machine] == 0):
                free_dryers += 1
            if(machine_dict[machine] == 60):
                out_of_service_dyers.append(machine)

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
        -> BRACKENRIDGE
        -> HOLLAND
        -> LOTHROP
        -> MCCORMICK
        -> SUTH_EAST
        -> SUTH_WEST
    """
    machines = []
    laundry_soup = _get_laundry_soup(building_name)

    total_machines = len(laundry_soup)  # total number of machines in the laundry room
    total_washers = 0
    total_dryers = 0
    free_washers = 0
    free_dryers = 0
    machine_dict = {}
    out_of_service_washers = []
    out_of_service_dryers = []
    for machine in laundry_soup:
        for machine1 in machine:
            for machine2 in machine1:
                for machine3 in machine2:
                    key_point = machine3.find('appliance_desc":')
                    end_point = machine3.rfind('appliance_desc":')
                    while (key_point < end_point):
                        key_end = key_point + 17
                        machine4 = machine3[key_end:]
                        # print(machine4)
                        quotes = machine4.find('"')
                        machineid = machine4[:quotes]
                        # machineid = [char for char in machineid]
                        # machine_num = int(machineid[len(machineid)-1])
                        average_time_point = machine3.find('average_run_time":')
                        average_run_time = int(machine3[average_time_point + 18:average_time_point + 20])
                        time_remaining_point = machine3.find('time_remaining":')
                        find_comma = machine3[time_remaining_point + 16:]
                        time_remaining = int(find_comma[:find_comma.find(',')])
                        in_use = average_run_time - time_remaining
                        machine_dict[machineid] = in_use
                        # find number 2
                        machine_id2 = machine3.find('appliance_desc2":')
                        machine_id2 = machine3[machine_id2 + 18:]
                        quotes2 = machine_id2.find('"')
                        machine_id2 = machine_id2[:quotes]
                        average_time_point2 = machine3.find('average_run_time2":')
                        average_run_time2 = int(machine3[average_time_point2 + 19:average_time_point2 + 21])
                        time_remaining_point2 = machine3.find('time_remaining2":')
                        find_comma2 = machine3[time_remaining_point2 + 17:]
                        time_remaining2 = int(find_comma2[:find_comma2.find(',')])
                        in_use2 = average_run_time2 - time_remaining2
                        machine_dict[machine_id2] = in_use2
                        machine3 = machine4
                        key_point = machine3.find('appliance_desc":')
                        end_point = machine3.rfind('appliance_desc":') + key_point
                    # print(machine_dict)
    for machine in machine_dict.keys():
        machine_id = machine
        num_id = [char for char in machine]
        num = int(num_id[len(num_id) - 1]) % 2
        if (num == 0):  # it is an even code, so it is a washer
            machine_type = "Washer"
            if (machine_dict[machine] == 22):
                machine_status = "Available"
                time_left = 60
            elif (machine_dict[machine] == 60):
                machine_status = "Out of Service"
                time_left = 0
            else:
                machine_status = "In use"
                time_left = 60 - machine_dict[machine]
        else:  # it is an odd code, so it is a dryer
            machine_type = "Dryer"
            if (machine_dict[machine] == 0):
                machine_status = "Available"
                time_left = 60
            elif (machine_dict[machine] == 60):
                machine_status = "Out of Service"
                time_left = 0
            else:
                machine_status = "In use"
                time_left = 60 - machine_dict[machine]

        machines.append({
            'machine_id': machine_id,
            'machine_status': machine_status,   #of out service, in use, or available
            'machine_type': machine_type,       # washer or dryer
            'time_left': time_left              # if free, time_left = 60, else some other number
        })

    return machines

def get_out_of_service(building_name: str) -> Dict[str, list]:
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

    total_machines = len(laundry_soup)  # total number of machines in the laundry room
    total_washers = 0
    total_dryers = 0
    free_washers = 0
    free_dryers = 0
    machine_dict = {}
    out_of_service_washers = []
    out_of_service_dryers = []
    for machine in laundry_soup:
        for machine1 in machine:
            for machine2 in machine1:
                for machine3 in machine2:
                    key_point = machine3.find('appliance_desc":')
                    end_point = machine3.rfind('appliance_desc":')
                    while (key_point < end_point):
                        key_end = key_point + 17
                        machine4 = machine3[key_end:]
                        # print(machine4)
                        quotes = machine4.find('"')
                        machineid = machine4[:quotes]
                        # machineid = [char for char in machineid]
                        # machine_num = int(machineid[len(machineid)-1])
                        average_time_point = machine3.find('average_run_time":')
                        average_run_time = int(machine3[average_time_point + 18:average_time_point + 20])
                        time_remaining_point = machine3.find('time_remaining":')
                        find_comma = machine3[time_remaining_point + 16:]
                        time_remaining = int(find_comma[:find_comma.find(',')])
                        in_use = average_run_time - time_remaining
                        machine_dict[machineid] = in_use
                        # find number 2
                        machine_id2 = machine3.find('appliance_desc2":')
                        machine_id2 = machine3[machine_id2 + 18:]
                        quotes2 = machine_id2.find('"')
                        machine_id2 = machine_id2[:quotes]
                        average_time_point2 = machine3.find('average_run_time2":')
                        average_run_time2 = int(machine3[average_time_point2 + 19:average_time_point2 + 21])
                        time_remaining_point2 = machine3.find('time_remaining2":')
                        find_comma2 = machine3[time_remaining_point2 + 17:]
                        time_remaining2 = int(find_comma2[:find_comma2.find(',')])
                        in_use2 = average_run_time2 - time_remaining2
                        machine_dict[machine_id2] = in_use2
                        machine3 = machine4
                        key_point = machine3.find('appliance_desc":')
                        end_point = machine3.rfind('appliance_desc":') + key_point
                    # print(machine_dict)
    for machine in machine_dict.keys():
        num_id = [char for char in machine]
        num = int(num_id[len(num_id) - 1]) % 2
        if (num == 0):  # it is an even code, so it is a washer
            total_washers += 1
            if (machine_dict[machine] == 22):
                free_washers += 1
            if (machine_dict[machine] == 60):
                out_of_service_washers.append(machine)
        else:  # it is an odd code, so it is a dryer
            total_dryers += 1
            if (machine_dict[machine] == 0):
                free_dryers += 1
            if (machine_dict[machine] == 60):
                out_of_service_dryers.append(machine)
    return{
        'Out of Service washers': out_of_service_washers,
        'Out of Service dryers': out_of_service_dryers
    }
