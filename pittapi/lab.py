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
from bs4 import BeautifulSoup

import re
from collections import namedtuple
from typing import List

URL = "http://labinformation.cssd.pitt.edu/"

lab_name = re.compile(".*Lab")
Lab = namedtuple("Lab", ["name", "status", "windows", "mac", "linux"])


def _fetch_labs() -> List[str]:
    """Fetches text of status/machines of all labs."""
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "lxml")
    text = soup.span.text
    return text.strip().split("  ")


def _extract_machines(data: str) -> List[int]:
    """Gets available computer totals for each OS into a list."""
    _, data = data.split(":")
    return [int(i) for i in re.findall("\d+", data)]


def get_status() -> List[Lab]:
    """Returns a dictionary with status and amount of OS machines."""
    labs = []
    for lab_data in _fetch_labs():
        name = lab_name.search(lab_data).group()
        status = "open" if "open" in lab_data else "closed"
        machines = _extract_machines(lab_data) if status == "open" else [0, 0, 0]
        computing_lab = Lab(name, status, *machines)
        labs.append(computing_lab)
    return labs
