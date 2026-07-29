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

from bs4 import BeautifulSoup

from pittapi.base_client import BaseClient

__all__ = ["Gym", "GymClient"]

GYM_URL = "https://connect2concepts.com/connect2/?type=bar&key=17c2cbcb-ec92-4178-a5f5-c4860330aea0"
REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0"}


@dataclass(frozen=True, slots=True)
class Gym:
    """Occupancy information for one recreation facility."""

    name: str
    last_updated: str | None = None
    current_count: int | None = None
    percent_full: int | None = None

    @classmethod
    def from_text(cls, text: str) -> Gym:
        fields = text.split("|")
        if len(fields) < 4:
            return cls(name=fields[0])

        try:
            percent_full = int(fields[4].removesuffix("%"))
        except (IndexError, ValueError):
            percent_full = 0

        return cls(
            name=fields[0],
            current_count=int(fields[2].removeprefix("Last Count: ")),
            last_updated=fields[3].removeprefix("Updated: "),
            percent_full=percent_full,
        )


class GymClient(BaseClient):
    """Fetch recreation facility occupancy."""

    def get_all_gyms_info(self) -> tuple[Gym, ...]:
        response = self.request("GET", GYM_URL, headers=REQUEST_HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        gym_elements = soup.find_all("div", class_="barChart")
        return tuple(Gym.from_text(element.get_text("|", strip=True)) for element in gym_elements)

    def get_gym_info(self, gym_name: str) -> Gym:
        for gym in self.get_all_gyms_info():
            if gym.name == gym_name:
                return gym
        raise LookupError(f"gym not found: {gym_name}")
