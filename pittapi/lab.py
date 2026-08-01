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

Availability data for Pitt computing labs.
"""

from dataclasses import dataclass
from typing import Any

from pittapi.base_client import BaseClient

__all__ = ["Lab", "LabClient", "LabLocation"]

PITT_BASE_URL = "https://pitt-keyserve-prod.univ.pitt.edu/maps/std/"
LOCATIONS_URL = PITT_BASE_URL + "avail.json"


@dataclass(frozen=True, slots=True)
class LabLocation:
    """A computing lab published by Pitt's availability map."""

    id: str
    name: str
    title: str


@dataclass(frozen=True, slots=True)
class Lab:
    """Computer availability for one lab."""

    name: str
    is_closed: bool
    available_computers: int
    off_computers: int
    in_use_computers: int
    out_of_service_computers: int
    total_computers: int


class LabClient(BaseClient):
    """Fetch computing-lab availability."""

    def get_locations(self) -> tuple[LabLocation, ...]:
        """Return the labs currently published by Pitt."""
        data = self.request("GET", LOCATIONS_URL).json()
        try:
            maps = data["results"]["maps"]
            return tuple(
                LabLocation(id=item["ident"], name=item["pname"], title=item["title"]) for item in maps if item["publish"]
            )
        except (KeyError, TypeError) as error:
            raise ValueError("lab discovery response is missing required data") from error

    def get_status(self, location: LabLocation) -> Lab:
        """Return availability for a discovered lab location."""
        url = f"{PITT_BASE_URL}{location.id}/status.json?noredir=1"
        data = self.request("GET", url).json()
        return parse_lab(data)

    def get_all_statuses(self) -> tuple[Lab, ...]:
        """Discover every lab and return statuses in provider order."""
        return tuple(self.get_status(location) for location in self.get_locations())


def parse_lab(data: dict[str, Any]) -> Lab:
    """Convert one lab response into availability counts."""
    try:
        name = next(iter(data["hours"]))
        is_closed = data["hours"][name]["closed"]
        computers = data["state"].values()
    except (KeyError, StopIteration, TypeError) as error:
        raise ValueError("lab response is missing required data") from error

    counts = {0: 0, 1: 0, 2: 0, 3: 0}
    total_computers = 0
    for computer in computers:
        state = computer.get("up")
        if state not in counts:
            address = computer.get("addr", "unknown computer")
            raise ValueError(f"unknown computer state for {address}: {state}")
        counts[state] += 1
        total_computers += 1

    return Lab(
        name=name,
        is_closed=is_closed,
        available_computers=counts[1],
        off_computers=counts[0],
        in_use_computers=counts[2],
        out_of_service_computers=counts[3],
        total_computers=total_computers,
    )
