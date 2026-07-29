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

Vehicle, route, and arrival information for Pitt shuttles.
"""

from dataclasses import dataclass
from typing import Any, Callable, TypeVar

from pittapi.base_client import BaseClient

__all__ = [
    "MapPoint",
    "Route",
    "ScheduledTime",
    "ShuttleClient",
    "ShuttleStop",
    "StopArrival",
    "StopEstimate",
    "VehicleEstimate",
    "VehiclePoint",
    "VehicleStopEstimates",
]

API_KEY = "8882812681"
VEHICLE_POINTS_URL = "http://www.pittshuttle.com/Services/JSONPRelay.svc/GetMapVehiclePoints"
ARRIVAL_TIMES_URL = "http://www.pittshuttle.com/Services/JSONPRelay.svc/GetRouteStopArrivals"
STOP_ESTIMATES_URL = "http://www.pittshuttle.com/Services/JSONPRelay.svc/GetVehicleRouteStopEstimates"
ROUTES_URL = "http://www.pittshuttle.com/Services/JSONPRelay.svc/GetRoutesForMap"
Model = TypeVar("Model")


@dataclass(frozen=True, slots=True)
class VehiclePoint:
    vehicle_id: int
    name: str
    route_id: int
    latitude: float
    longitude: float
    heading: int
    ground_speed: float
    seconds: int
    timestamp: str
    is_delayed: bool
    is_on_route: bool


@dataclass(frozen=True, slots=True)
class ScheduledTime:
    arrival_time_utc: str
    departure_time_utc: str
    assigned_vehicle_id: int


@dataclass(frozen=True, slots=True)
class VehicleEstimate:
    vehicle_id: int
    seconds_to_stop: int
    on_route: bool


@dataclass(frozen=True, slots=True)
class StopArrival:
    route_id: int
    route_stop_id: int
    scheduled_times: tuple[ScheduledTime, ...]
    vehicle_estimates: tuple[VehicleEstimate, ...]


@dataclass(frozen=True, slots=True)
class StopEstimate:
    description: str
    estimate_time: str
    is_arriving: bool
    on_route: bool
    route_stop_id: int
    seconds: int
    text: str
    vehicle_id: int


@dataclass(frozen=True, slots=True)
class VehicleStopEstimates:
    vehicle_id: int
    estimates: tuple[StopEstimate, ...]


@dataclass(frozen=True, slots=True)
class MapPoint:
    heading: int
    latitude: float
    longitude: float


@dataclass(frozen=True, slots=True)
class ShuttleStop:
    route_stop_id: int
    route_id: int
    description: str
    latitude: float
    longitude: float
    city: str
    state: str
    zip_code: str
    map_points: tuple[MapPoint, ...]


@dataclass(frozen=True, slots=True)
class Route:
    route_id: int
    description: str
    map_latitude: float
    map_longitude: float
    map_line_color: str
    map_zoom: int
    stops: tuple[ShuttleStop, ...]


class ShuttleClient(BaseClient):
    """Fetch typed data from Pitt's shuttle tracking service."""

    def get_map_vehicle_points(self, api_key: str = API_KEY) -> tuple[VehiclePoint, ...]:
        return self.fetch_models(VEHICLE_POINTS_URL, {"ApiKey": api_key}, parse_vehicle_point)

    def get_route_stop_arrivals(self, api_key: str = API_KEY, times_per_stop: int = 1) -> tuple[StopArrival, ...]:
        params = {"ApiKey": api_key, "TimesPerStopString": str(times_per_stop)}
        return self.fetch_models(ARRIVAL_TIMES_URL, params, parse_stop_arrival)

    def get_vehicle_route_stop_estimates(
        self,
        vehicle_id: str,
        quantity: int = 2,
    ) -> tuple[VehicleStopEstimates, ...]:
        params = {"vehicleIdStrings": vehicle_id, "quantity": str(quantity)}
        return self.fetch_models(STOP_ESTIMATES_URL, params, parse_vehicle_stop_estimates)

    def get_routes(self, api_key: str = API_KEY) -> tuple[Route, ...]:
        return self.fetch_models(ROUTES_URL, {"ApiKey": api_key}, parse_route)

    def fetch_models(
        self,
        url: str,
        params: dict[str, str],
        parser: Callable[[dict[str, Any]], Model],
    ) -> tuple[Model, ...]:
        data = self.request("GET", url, params=params).json()
        if not isinstance(data, list):
            raise ValueError("shuttle response must contain a list")
        try:
            return tuple(parser(item) for item in data)
        except (KeyError, TypeError) as error:
            raise ValueError("shuttle response is missing required data") from error


def parse_vehicle_point(data: dict[str, Any]) -> VehiclePoint:
    return VehiclePoint(
        vehicle_id=data["VehicleID"],
        name=data["Name"],
        route_id=data["RouteID"],
        latitude=data["Latitude"],
        longitude=data["Longitude"],
        heading=data["Heading"],
        ground_speed=data["GroundSpeed"],
        seconds=data["Seconds"],
        timestamp=data["TimeStamp"],
        is_delayed=data["IsDelayed"],
        is_on_route=data["IsOnRoute"],
    )


def parse_stop_arrival(data: dict[str, Any]) -> StopArrival:
    scheduled_times = tuple(
        ScheduledTime(
            arrival_time_utc=item["ArrivalTimeUTC"],
            departure_time_utc=item["DepartureTimeUTC"],
            assigned_vehicle_id=item["AssignedVehicleId"],
        )
        for item in data["ScheduledTimes"]
    )
    vehicle_estimates = tuple(
        VehicleEstimate(
            vehicle_id=item["VehicleID"],
            seconds_to_stop=item["SecondsToStop"],
            on_route=item["OnRoute"],
        )
        for item in data["VehicleEstimates"]
    )
    return StopArrival(
        route_id=data["RouteID"],
        route_stop_id=data["RouteStopID"],
        scheduled_times=scheduled_times,
        vehicle_estimates=vehicle_estimates,
    )


def parse_vehicle_stop_estimates(data: dict[str, Any]) -> VehicleStopEstimates:
    estimates = tuple(
        StopEstimate(
            description=item["Description"],
            estimate_time=item["EstimateTime"],
            is_arriving=item["IsArriving"],
            on_route=item["OnRoute"],
            route_stop_id=item["RouteStopID"],
            seconds=item["Seconds"],
            text=item["Text"],
            vehicle_id=item["VehicleId"],
        )
        for item in data["Estimates"]
    )
    return VehicleStopEstimates(vehicle_id=data["VehicleID"], estimates=estimates)


def parse_route(data: dict[str, Any]) -> Route:
    stops = tuple(parse_stop(item) for item in data["Stops"])
    return Route(
        route_id=data["RouteID"],
        description=data["Description"],
        map_latitude=data["MapLatitude"],
        map_longitude=data["MapLongitude"],
        map_line_color=data["MapLineColor"],
        map_zoom=data["MapZoom"],
        stops=stops,
    )


def parse_stop(data: dict[str, Any]) -> ShuttleStop:
    map_points = tuple(
        MapPoint(heading=item["Heading"], latitude=item["Latitude"], longitude=item["Longitude"]) for item in data["MapPoints"]
    )
    return ShuttleStop(
        route_stop_id=data["RouteStopID"],
        route_id=data["RouteID"],
        description=data["Description"],
        latitude=data["Latitude"],
        longitude=data["Longitude"],
        city=data["City"],
        state=data["State"],
        zip_code=data["Zip"],
        map_points=map_points,
    )
