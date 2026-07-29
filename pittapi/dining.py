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

Dining locations, hours, and menus on Pitt's campus.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from pittapi.base_client import BaseClient

__all__ = [
    "DiningClient",
    "DiningLocation",
    "DiningStatus",
    "HoursInterval",
    "LocationHours",
    "Menu",
    "MenuCategory",
    "MenuItem",
    "MenuPeriod",
    "Nutrient",
]

REQUEST_HEADERS = {"User-Agent": "Chrome/103.0.5026.0"}
LOCATIONS_URL = "https://api.dineoncampus.com/v1/locations/status?site_id=5e6fcc641ca48e0cacd93b04&platform="
HOURS_URL = "https://api.dineoncampus.com/v1/locations/weekly_schedule?site_id=5e6fcc641ca48e0cacd93b04&date=%22{date}%22"
PERIODS_URL = "https://api.dineoncampus.com/v1/location/{location_id}/periods?platform=0&date={date}"
MENU_URL = "https://api.dineoncampus.com/v1/location/{location_id}/periods/{period_id}?platform=0&date={date}"


@dataclass(frozen=True, slots=True)
class DiningStatus:
    label: str
    message: str
    color: str


@dataclass(frozen=True, slots=True)
class DiningLocation:
    id: str
    name: str
    is_open: bool
    status: DiningStatus
    occupancy: str | None
    address: str | None


@dataclass(frozen=True, slots=True)
class HoursInterval:
    start_hour: int
    start_minutes: int
    end_hour: int
    end_minutes: int


@dataclass(frozen=True, slots=True)
class LocationHours:
    name: str
    date: str
    hours: tuple[HoursInterval, ...]


@dataclass(frozen=True, slots=True)
class Nutrient:
    name: str
    value: str
    unit: str
    numeric_value: str


@dataclass(frozen=True, slots=True)
class MenuItem:
    id: str
    name: str
    description: str | None
    portion: str | None
    ingredients: str | None
    nutrients: tuple[Nutrient, ...]
    filters: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MenuCategory:
    id: str
    name: str
    items: tuple[MenuItem, ...]


@dataclass(frozen=True, slots=True)
class MenuPeriod:
    id: str
    name: str
    categories: tuple[MenuCategory, ...]


@dataclass(frozen=True, slots=True)
class Menu:
    id: int
    date: str
    period: MenuPeriod


class DiningClient(BaseClient):
    """Fetch dining locations, hours, and menus."""

    def get_locations(self) -> tuple[DiningLocation, ...]:
        data = self.request("GET", LOCATIONS_URL, headers=REQUEST_HEADERS).json()
        try:
            return tuple(parse_location(item) for item in data["locations"])
        except (KeyError, TypeError) as error:
            raise ValueError("dining location response is missing required data") from error

    def get_location_hours(
        self,
        location_name: str | None = None,
        date: datetime | None = None,
    ) -> tuple[LocationHours, ...]:
        selected_date = date or datetime.now()
        date_text = selected_date.strftime("%Y-%m-%d")
        url = HOURS_URL.format(date=date_text)
        data = self.request("GET", url, headers=REQUEST_HEADERS).json()

        try:
            locations = data["the_locations"]
            matching_hours = []
            for location in locations:
                if location_name and location["name"].casefold() != location_name.casefold():
                    continue
                for day in location["week"]:
                    if day["date"] == date_text:
                        matching_hours.append(parse_location_hours(location["name"], day))
            if location_name and not matching_hours:
                raise LookupError(f"dining location not found: {location_name}")
            return tuple(matching_hours)
        except (KeyError, TypeError) as error:
            raise ValueError("dining hours response is missing required data") from error

    def get_location_menu(
        self,
        location_name: str,
        date: datetime | None = None,
        period_name: str | None = None,
    ) -> Menu:
        selected_date = date or datetime.today()
        date_text = selected_date.strftime("%y-%m-%d")
        location = self.find_location(location_name)

        periods_url = PERIODS_URL.format(location_id=location.id, date=date_text)
        periods_data = self.request("GET", periods_url, headers=REQUEST_HEADERS).json()
        try:
            period = select_period(periods_data["periods"], period_name)
        except (KeyError, TypeError) as error:
            raise ValueError("dining periods response is missing required data") from error

        menu_url = MENU_URL.format(location_id=location.id, period_id=period["id"], date=date_text)
        menu_data = self.request("GET", menu_url, headers=REQUEST_HEADERS).json()
        try:
            return parse_menu(menu_data["menu"])
        except (KeyError, TypeError) as error:
            raise ValueError("dining menu response is missing required data") from error

    def find_location(self, location_name: str) -> DiningLocation:
        for location in self.get_locations():
            if location.name.casefold() == location_name.casefold():
                return location
        raise LookupError(f"dining location not found: {location_name}")


def parse_location(data: dict[str, Any]) -> DiningLocation:
    status = data["status"]
    return DiningLocation(
        id=data["id"],
        name=data["name"],
        is_open=data["open"],
        status=DiningStatus(label=status["label"], message=status["message"], color=status["color"]),
        occupancy=data.get("occupancy"),
        address=data.get("address"),
    )


def parse_location_hours(name: str, data: dict[str, Any]) -> LocationHours:
    hours = tuple(HoursInterval(**interval) for interval in data["hours"])
    return LocationHours(name=name, date=data["date"], hours=hours)


def select_period(periods: list[dict[str, Any]], period_name: str | None) -> dict[str, Any]:
    if not periods:
        raise LookupError("no dining periods are available")
    if period_name is None or len(periods) == 1:
        return periods[0]
    for period in periods:
        if period["name"].casefold() == period_name.casefold():
            return period
    raise LookupError(f"dining period not found: {period_name}")


def parse_menu(data: dict[str, Any]) -> Menu:
    period_data = data["periods"]
    categories = []
    for category_data in period_data["categories"]:
        items = tuple(parse_menu_item(item) for item in category_data["items"])
        categories.append(MenuCategory(id=category_data["id"], name=category_data["name"], items=items))
    period = MenuPeriod(
        id=period_data["id"],
        name=period_data["name"],
        categories=tuple(categories),
    )
    return Menu(id=data["id"], date=data["date"], period=period)


def parse_menu_item(data: dict[str, Any]) -> MenuItem:
    nutrients = []
    for nutrient in data["nutrients"]:
        nutrients.append(
            Nutrient(
                name=nutrient["name"],
                value=nutrient["value"],
                unit=nutrient["uom"],
                numeric_value=nutrient["value_numeric"],
            )
        )
    filters = tuple(item["name"] for item in data["filters"])
    return MenuItem(
        id=data["id"],
        name=data["name"],
        description=data.get("desc"),
        portion=data.get("portion"),
        ingredients=data.get("ingredients"),
        nutrients=tuple(nutrients),
        filters=filters,
    )
