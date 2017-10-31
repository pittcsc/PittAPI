'''
    File: laundry.py
    Author: Ankit Joshi
    Date Created: 9/1/2017
    Last Modified: 9/1/2017
'''


import requests
from bs4 import BeautifulSoup
import re

# ugh, update when codes change
location_lookup = {
    'TOWERS': '2430136',
    'BRACKENRIDGE': '2430119',
    'HOLLAND': '2430137',
    'LOTHROP': '2430151',
    'MCCORMICK': '2430120',
    'SUTH_EAST': '2430135',
    'SUTH_WEST': '2430134',
    'FORBES_CRAIG': '2430142'
}


def get_status_simple(building_name: str) -> Dict[str,str]:
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

    building_name = building_name.upper()
    url ='http://m.laundryview.com/submitFunctions.php?monitor=true&lr={}'.\
            format(location_lookup[building_name])
    response = requests.get(url)
    laundry_soup = BeautifulSoup(response.text, 'lxml')
    reFormat = re.compile(r'^([0-9]+) of ([0-9]+) available$')
    washer_text = laundry_soup.find('span',{'id': 'washer_available'}).text
    dryer_text = laundry_soup.find('span',{'id': 'dryer_available'}).text
    washer_match = reFormat.match(washer_text)
    dryer_match = reFormat.match(dryer_text)

    return  {
        'building': building_name,
        'free_washers': int(washer_match.group(1)),
        'total_washers': int(washer_match.group(2)),
        'free_dryers': int(dryer_match.group(1)),
        'total_dryers': int(dryer_match.group(2))
    }



def get_status_detailed(building_name: str) -> List[Dict[str,str]]:
    building_name = building_name.upper()
    """
    :returns: A list of washers and dryers for the passed
              building location with their statuses

              OR

              A dict of machine metadata if machine name
              is explicity passed

    :param building_name: (String) one of these:
        -> BRACKENRIDGE
        -> HOLLAND
        -> LOTHROP
        -> MCCORMICK
        -> SUTH_EAST
        -> SUTH_WEST
    :param machine: (String) specific machine to query
                    eg: machine='BA02'
    """
    building_name = building_name.upper()
    machines = []

    url = 'http://m.laundryview.com/submitFunctions.php?monitor=true&lr={}'.\
            format(location_lookup[building_name])
    response = requests.get(url)
    laundry_soup = BeautifulSoup(response.text, 'lxml')
    is_washer = False

    for li in laundry_soup.findAll('li'):
        if 'id' in li.attrs:
            is_washer = True if li.attrs['id'] == 'washer' \
                            else False
            continue

        machine_id = int(li.find('a').attrs['id'])
        machine_status = li.find('p').text
        machine_name = li.text.split(machine_status)[0].\
                           encode('ascii', 'ignore')
        machine_type = 'washer' if is_washer else 'dryer'


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

    di = [] # type: List[Dict[str,str]]
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
            'machine_name': machine_name,
            'machine_type': machine_type,
            'machine_status': machine_status,
            'machine_id': machine_id
        })

    if machine:
        try:
            machines = filter(lambda m: m['machine_name'] == machine, machines)[0]
        except IndexError:
            raise NoSuchMachineException(machine)

    return machines


class NoSuchMachineException(Exception):
    pass
