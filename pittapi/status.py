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

Operational status for Pitt technology services.
"""

from dataclasses import dataclass
from typing import Any

from pittapi.base_client import BaseClient

__all__ = [
    "AffectedComponent",
    "Component",
    "Incident",
    "IncidentUpdate",
    "StatusClient",
    "StatusSummary",
]

STATUS_URL = "https://status.pitt.edu/index.json"


@dataclass(frozen=True, slots=True)
class Component:
    status: str
    name: str
    updated_at: str
    description: str | None


@dataclass(frozen=True, slots=True)
class AffectedComponent:
    name: str
    new_status: str
    old_status: str


@dataclass(frozen=True, slots=True)
class IncidentUpdate:
    affected_components: tuple[AffectedComponent, ...]
    body: str
    status: str
    updated_at: str


@dataclass(frozen=True, slots=True)
class Incident:
    components: tuple[Component, ...]
    incident_updates: tuple[IncidentUpdate, ...]
    impact: str
    name: str
    status: str
    resolved_at: str | None
    updated_at: str


@dataclass(frozen=True, slots=True)
class StatusSummary:
    components: tuple[Component, ...]
    incidents: tuple[Incident, ...]


class StatusClient(BaseClient):
    """Fetch Pitt's current service status."""

    def get_status(self) -> StatusSummary:
        data = self.request("GET", STATUS_URL).json()
        try:
            components = tuple(parse_component(item) for item in data["components"])
            incidents = tuple(parse_incident(item) for item in data["incidents"])
        except (KeyError, TypeError) as error:
            raise ValueError("status response is missing required data") from error
        return StatusSummary(components=components, incidents=incidents)


def parse_component(data: dict[str, Any]) -> Component:
    return Component(
        status=data["status"],
        name=data["name"],
        updated_at=data["updated_at"],
        description=data["description"],
    )


def parse_affected_component(data: dict[str, Any]) -> AffectedComponent:
    return AffectedComponent(name=data["name"], new_status=data["new_status"], old_status=data["old_status"])


def parse_incident_update(data: dict[str, Any]) -> IncidentUpdate:
    affected_components = tuple(parse_affected_component(item) for item in data["affected_components"])
    return IncidentUpdate(
        affected_components=affected_components,
        body=data["body"],
        status=data["status"],
        updated_at=data["updated_at"],
    )


def parse_incident(data: dict[str, Any]) -> Incident:
    components = tuple(parse_component(item) for item in data["components"])
    updates = tuple(parse_incident_update(item) for item in data["incident_updates"])
    return Incident(
        components=components,
        incident_updates=updates,
        impact=data["impact"],
        name=data["name"],
        status=data["status"],
        resolved_at=data["resolved_at"],
        updated_at=data["updated_at"],
    )
