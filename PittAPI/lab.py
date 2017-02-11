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
from bs4 import BeautifulSoup, SoupStrainer
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

session = requests.session()
strainer = SoupStrainer('span')

location_dict = {
    'ALUMNI': 0,
    'BENEDUM': 1,
    'CATH_G26': 2,
    'CATH_G27': 3,
    'LAWRENCE': 4,
    'HILLMAN': 5,
    'SUTH': 6
}


def get_status(lab_name):
    """
    :returns: a dictionary with status and amount of OS machines.

    :param: lab_name: Lab name
    """

    lab_name = lab_name.upper()
    url = 'http://labinformation.cssd.pitt.edu/'
    page = session.get(url)
    soup = BeautifulSoup(page.text, 'lxml', parse_only=strainer)
    labs = soup.span.contents[0].strip().split("  ")

    lab = labs[location_dict[lab_name]].split(':')
    di = {}
    if len(lab) > 1:
        lab = [x.strip() for x in lab[1].split(',')]
        machines = [int(x[:x.index(' ')]) for x in lab]
        di = {
            'status': 'open',
            'windows': machines[0],
            'mac': machines[1],
            'linux': machines[2]
        }
    else:
        di = {
            'status': 'closed',
            'windows': 0,
            'mac': 0,
            'linux': 0
        }

    return di
