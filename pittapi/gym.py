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

Current occupancy for Pitt recreation facilities.
"""

from __future__ import annotations

from dataclasses import dataclass

from pittapi.base_client import BaseClient

__all__ = ["Gym", "GymClient"]

GYM_URL = "https://goboardapi.azurewebsites.net/api/FacilityCount/GetCountsByAccount"
PITT_ACCOUNT_KEY = "17c2cbcb-ec92-4178-a5f5-c4860330aea0"


@dataclass(frozen=True, slots=True)
class Gym:
    """Occupancy information for one recreation facility."""

    location_id: int
    location_name: str
    facility_id: int
    facility_name: str
    total_capacity: int
    current_count: int
    percent_full: int
    last_updated: str
    is_closed: bool


class GymClient(BaseClient):
    """Fetch recreation facility occupancy."""

    def get_all_gyms_info(self) -> tuple[Gym, ...]:
        data = self.request("GET", GYM_URL, params={"AccountAPIKey": PITT_ACCOUNT_KEY}).json()
        if not isinstance(data, list):
            raise ValueError("gym response must contain a list")
        try:
            return tuple(
                Gym(
                    location_id=item["LocationId"],
                    location_name=item["LocationName"],
                    facility_id=item["FacilityId"],
                    facility_name=item["FacilityName"],
                    total_capacity=item["TotalCapacity"],
                    current_count=item["LastCount"],
                    percent_full=item["PercetageCapacity"],
                    last_updated=item["LastUpdatedDateAndTime"],
                    is_closed=item["IsClosed"],
                )
                for item in data
            )
        except (KeyError, TypeError) as error:
            raise ValueError("gym response is missing required data") from error

    def get_gym_info(self, gym_name: str) -> Gym:
        for gym in self.get_all_gyms_info():
            if gym.location_name == gym_name:
                return gym
        raise LookupError(f"gym not found: {gym_name}")
