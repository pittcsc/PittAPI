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
from enum import IntEnum
import re
from typing import Any, Literal

from pittapi.base_client import BaseClient

__all__ = ["BuildingStatus", "LaundryClient", "LaundryMachine", "MachineStatus"]

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


class MachineStatus(IntEnum):
    """LaundryView's documented machine states."""

    AVAILABLE = 0
    IDLE = 1
    RUNNING = 2
    OUT_OF_SERVICE = 3
    OFFLINE = 4


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
    type: MachineType
    status: MachineStatus
    status_message: str
    minutes_remaining: int | None
    cycle_progress_percent: float | None
    model_number: str | None
    average_cycle_minutes: int
    is_combo: bool
    is_stacked: bool

    @property
    def is_available(self) -> bool:
        return self.status is MachineStatus.AVAILABLE


class LaundryClient(BaseClient):
    """Fetch laundry information for Pitt residence halls."""

    def get_building_status(self, building_name: str) -> BuildingStatus:
        normalized_name = building_name.upper()
        machines = self.get_laundry_machine_statuses(normalized_name)
        free_washers = sum(machine.type == "washer" and machine.is_available for machine in machines)
        free_dryers = sum(machine.type == "dryer" and machine.is_available for machine in machines)
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
    object_type = data["type"]
    is_combo = object_type == "washNdry"
    is_stacked = bool(data.get("stacked") or data.get("manualStack"))

    if is_combo:
        first_type = infer_combo_type(data["appliance_desc"])
    elif object_type == "washFL":
        first_type = "washer"
    elif object_type in ("dry", "dblDry"):
        first_type = "dryer"
    else:
        return ()

    machines = [parse_machine(data, first_type, is_combo=is_combo, is_stacked=is_stacked)]
    if "appliance_desc_key2" in data:
        if is_combo:
            second_type = infer_combo_type(data["appliance_desc2"])
        else:
            second_type = "washer" if data.get("type2") == "washFL" else "dryer"
        machines.append(
            parse_machine(
                data,
                second_type,
                suffix="2",
                is_combo=is_combo,
                is_stacked=is_stacked,
            )
        )
    return tuple(machines)


def infer_combo_type(machine_name: str) -> MachineType:
    number = NUMBER_PATTERN.search(machine_name)
    if number is None:
        raise ValueError(f"combo machine has an invalid name: {machine_name}")
    return "washer" if int(number.group()) % 2 == 0 else "dryer"


def parse_machine(
    data: dict[str, Any],
    machine_type: MachineType,
    suffix: str = "",
    is_combo: bool = False,
    is_stacked: bool = False,
) -> LaundryMachine:
    status_code = data[f"status_toggle{suffix}"]
    try:
        status = MachineStatus(status_code)
    except ValueError as error:
        raise ValueError(f"unknown laundry status code: {status_code}") from error

    minutes_remaining = None
    cycle_progress = None
    if status is MachineStatus.RUNNING:
        minutes_remaining = data[f"time_remaining{suffix}"]
        progress = data[f"percentage{suffix}"]
        if 0 <= progress <= 100:
            cycle_progress = progress

    return LaundryMachine(
        name=data[f"appliance_desc{suffix}"],
        id=data[f"appliance_desc_key{suffix}"],
        type=machine_type,
        status=status,
        status_message=data[f"time_left_lite{suffix}"],
        minutes_remaining=minutes_remaining,
        cycle_progress_percent=cycle_progress,
        model_number=data.get(f"model_number{suffix}", data.get("model_number")),
        average_cycle_minutes=data[f"average_run_time{suffix}"],
        is_combo=is_combo,
        is_stacked=is_stacked,
    )
