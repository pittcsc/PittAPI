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

Availability and machine status for Pitt residence-hall laundries.
"""

from dataclasses import dataclass
import re
from typing import Any, Literal

from pittapi.base_client import BaseClient

__all__ = ["BuildingStatus", "LaundryClient", "LaundryMachine"]

BASE_URL = "https://www.laundryview.com/api/currentRoomData?school_desc_key=197&location={location}"
LOCATION_IDS = {
    "TOWERS": "2430136",
    "BRACKENRIDGE": "2430119",
    "HOLLAND": "2430137",
    "LOTHROP": "2430151",
    "MCCORMICK": "2430120",
    "SUTH_EAST": "2430135",
    "SUTH_WEST": "2430134",
    "FORBES_CRAIG": "2430142",
}
NUMBER_PATTERN = re.compile(r"\d+")
MachineType = Literal["washer", "dryer"]


@dataclass(frozen=True, slots=True)
class BuildingStatus:
    building: str
    free_washers: int
    total_washers: int
    free_dryers: int
    total_dryers: int


@dataclass(frozen=True, slots=True)
class LaundryMachine:
    name: str
    id: str
    status: str
    type: MachineType
    time_left: int | None


class LaundryClient(BaseClient):
    """Fetch laundry information for Pitt residence halls."""

    def get_building_status(self, building_name: str) -> BuildingStatus:
        normalized_name = building_name.upper()
        machines = self.get_laundry_machine_statuses(normalized_name)
        free_washers = sum(machine.type == "washer" and machine.status == "Available" for machine in machines)
        free_dryers = sum(machine.type == "dryer" and machine.status == "Available" for machine in machines)
        total_washers = sum(machine.type == "washer" for machine in machines)
        total_dryers = sum(machine.type == "dryer" for machine in machines)
        return BuildingStatus(
            building=normalized_name,
            free_washers=free_washers,
            total_washers=total_washers,
            free_dryers=free_dryers,
            total_dryers=total_dryers,
        )

    def get_laundry_machine_statuses(self, building_name: str) -> tuple[LaundryMachine, ...]:
        normalized_name = building_name.upper()
        if normalized_name not in LOCATION_IDS:
            raise ValueError(f"invalid laundry building: {building_name}")

        url = BASE_URL.format(location=LOCATION_IDS[normalized_name])
        data = self.request("GET", url).json()
        try:
            machines = []
            for item in data["objects"]:
                machines.extend(parse_laundry_object(item))
            return tuple(machines)
        except (KeyError, TypeError) as error:
            raise ValueError("laundry response is missing required data") from error


def parse_laundry_object(data: dict[str, Any]) -> tuple[LaundryMachine, ...]:
    machine_type = data["type"]
    if machine_type == "washNdry":
        first_type = infer_combo_type(data["appliance_desc"])
        second_type = infer_combo_type(data["appliance_desc2"])
        return (
            parse_machine(data, first_type),
            parse_machine(data, second_type, suffix="2"),
        )
    if machine_type in ("washFL", "dry"):
        first_type: MachineType = "washer" if machine_type == "washFL" else "dryer"
        machines = [parse_machine(data, first_type)]
        if "type2" in data:
            second_type: MachineType = "washer" if data["type2"] == "washFL" else "dryer"
            machines.append(parse_machine(data, second_type, suffix="2"))
        return tuple(machines)
    return ()


def infer_combo_type(machine_name: str) -> MachineType:
    number = NUMBER_PATTERN.search(machine_name)
    if number is None:
        raise ValueError(f"combo machine has an invalid name: {machine_name}")
    return "washer" if int(number.group()) % 2 == 0 else "dryer"


def parse_machine(data: dict[str, Any], machine_type: MachineType, suffix: str = "") -> LaundryMachine:
    status = data[f"time_left_lite{suffix}"]
    time_left = None if status in ("Out of service", "Offline") else data[f"time_remaining{suffix}"]
    return LaundryMachine(
        name=data[f"appliance_desc{suffix}"],
        id=data[f"appliance_desc_key{suffix}"],
        status=status,
        type=machine_type,
        time_left=time_left,
    )
