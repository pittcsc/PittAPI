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

session = requests.session()

LOCATIONS = ['ALUMNI', 'BENEDUM', 'CATH_G27', 'CATH_G62', 'LAWRENCE', 'HILLMAN', 'SUTH']
URL = 'http://labinformation.cssd.pitt.edu/'


def get_status(lab_name):
    """Returns a dictionary with status and amount of OS machines."""
    status = None
    machines = None
    while not status and not machines:
        lab_name, labs = _validate_lab(lab_name), _fetch_labs()
        status, *machines = labs[LOCATIONS.index(lab_name)].split(':')

    if 'open' in status:
        return _make_status('open', *_extract_machines(machines[0]))
    else:
        return _make_status('closed')


def _fetch_labs():
    """Fetches text of status/machines of all labs."""
    text = ''
    while not text:
        page = session.get(URL)
        soup = BeautifulSoup(page.text, 'lxml')
        text = soup.span.text

    return text.strip().split('  ')


def _extract_machines(data):
    """Gets available computer totals for each OS into a list."""
    machines = []
    for machine in data.split(','):
        machine = machine.strip()
        machines.append(int(machine[:machine.index(' ')]))
    return machines


def _make_status(state, win=0, mac=0, linux=0):
    """Creates proper dictionary response for getting lab status."""
    return {
        'status': state,
        'windows': win,
        'mac': mac,
        'linux': linux
    }


def _validate_lab(lab):
    """Corrects case of lab name and checks whether it's valid."""
    lab = lab.upper()
    if lab in LOCATIONS:
        return lab
    else:
        raise ValueError("Invalid lab name")
