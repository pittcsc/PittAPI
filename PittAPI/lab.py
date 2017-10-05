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
from bs4 import BeautifulSoup
from typing import Dict, List, Union

from typing import List, Dict

session = requests.session()

LOCATIONS = ['ALUMNI', 'BENEDUM', 'CATH_G27', 'CATH_G62', 'LAWRENCE', 'HILLMAN', 'SUTH']
URL = 'http://labinformation.cssd.pitt.edu/'


def get_status(lab_name: str) -> Dict[str,Union[str,int]]:
    """Returns a dictionary with status and amount of OS machines."""
    lab_name, labs = _validate_lab(lab_name), _fetch_labs()
    status, *machines = labs[LOCATIONS.index(lab_name)].split(':')

    if 'open' in status:
        return _make_status('open', *_extract_machines(machines[0]))
    else:
        return _make_status('closed')


def _fetch_labs() -> List[str]:
    """Fetches text of status/machines of all labs."""
    text = ''
    while "Lab" not in text:
        page = session.get(URL)
        soup = BeautifulSoup(page.text, 'lxml')
        text = soup.span.text

    return text.strip().split('  ')


def _extract_machines(data: str) -> List[int]:
    """Gets available computer totals for each OS into a list."""
    machines = []
    for machine in data.split(','):
        machine = machine.strip()
        machines.append(int(machine[:machine.index(' ')]))
    return machines


def _make_status(state: str, win: int=0, mac: int=0, linux: int=0) -> Dict[str,Union[str,int]]:
    """Creates proper dictionary response for getting lab status."""
    return {
        'status': state,
        'windows': str(win),
        'mac': str(mac),
        'linux': str(linux)
    }


def _validate_lab(lab: str) -> str:
    """Corrects case of lab name and checks whether it's valid."""
    lab = lab.upper()
    if lab in LOCATIONS:
        return lab
    else:
        raise ValueError("Invalid lab name")
