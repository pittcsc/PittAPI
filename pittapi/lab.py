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

__all__ = ["Lab", "LabClient"]

PITT_BASE_URL = "https://pitt-keyserve-prod.univ.pitt.edu/maps/std/"
AVAILABLE_LAB_IDS = {
    "THAW": "bba4a8796295ff6a8df116524b40e178",
    "LAWRENCE": "98a4759fc02ca3655d56cd58abed4e90",
    "CATH_LMC": "8b2a1c62ea8a23745101b998439310d2",
    "SUTH": "8adaaeb974aa38b2283c73532c095ca7",
    "CATH_G27": "6fd5a4e0dd0a32e3ccb441e25a1a2d78",
    "HILLMAN": "6638c1e72b9a56e5119ff9848b2bdc98",
    "CATH_G62": "04853e8d1453c90a910a0b803529a3a0",
}


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

    def get_one_lab_data(self, lab_name: str) -> Lab:
        if lab_name not in AVAILABLE_LAB_IDS:
            choices = ", ".join(AVAILABLE_LAB_IDS)
            raise ValueError(f"invalid lab name: {lab_name}. Valid options: {choices}")

        lab_id = AVAILABLE_LAB_IDS[lab_name]
        url = f"{PITT_BASE_URL}{lab_id}/status.json?noredir=1"
        data = self.request("GET", url).json()
        return parse_lab(data)

    def get_all_labs_data(self) -> tuple[Lab, ...]:
        return tuple(self.get_one_lab_data(lab_name) for lab_name in AVAILABLE_LAB_IDS)


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
