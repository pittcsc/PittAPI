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

from typing import List, NamedTuple

from requests_html import HTMLSession
from parse import compile

URL = "http://labinformation.cssd.pitt.edu/"

LAB_OPEN_PATTERN = compile(
    "{name} Lab is {status}: {windows:d} Windows, {macs:d} Macs, {linux:d} Linux"
)
LAB_CLOSED_PATTERN = compile("{name} Lab is currently {status}")


class Lab(NamedTuple):
    name: str
    status: str
    windows: int
    mac: int
    linux: int


def _fetch_labs() -> List[str]:
    """Fetches text of status/machines of all labs."""
    session = HTMLSession()
    resp = session.get(URL)
    data = resp.html.find("#lblTextMsg", first=True)
    return data.full_text.strip().split("  ")


def get_status() -> List[Lab]:
    """Returns a dictionary with status and amount of OS machines."""
    labs = []
    for lab_data in _fetch_labs():
        if "open" in lab_data:
            content = LAB_OPEN_PATTERN.parse(lab_data)
            computing_lab = Lab(**content.named)
        else:
            content = LAB_CLOSED_PATTERN.parse(lab_data)
            computing_lab = Lab(**content.named, windows=0, mac=0, linux=0)
        labs.append(computing_lab)
    return labs
