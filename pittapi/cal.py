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

Academic calendar data published by the University of Pittsburgh.
"""

from dataclasses import dataclass
from typing import Any

from pittapi.base_client import BaseClient

__all__ = ["CalendarClient", "Event"]

ACADEMIC_CALENDAR_URL = "https://25livepub.collegenet.com/calendars/pitt-academic-calendar.json"
GRADES_CALENDAR_URL = "https://25livepub.collegenet.com/calendars/pitt-grades-calendar.json"
ENROLLMENT_CALENDAR_URL = "https://25livepub.collegenet.com/calendars/pitt-enrollment-calendar.json"
COURSE_CALENDAR_URL = "https://25livepub.collegenet.com/calendars/pitt-courseclass-calendar.json"
GRADUATION_CALENDAR_URL = "https://25livepub.collegenet.com/calendars/pitt-graduation-calendar.json"


@dataclass(frozen=True, slots=True)
class Event:
    """One event from a Pitt calendar."""

    date: str
    title: str
    content: str
    categories: tuple[str, ...]


class CalendarClient(BaseClient):
    """Fetch events from Pitt's public calendars."""

    def get_academic_calendar(self) -> tuple[Event, ...]:
        return self.fetch_events(ACADEMIC_CALENDAR_URL)

    def get_grades_calendar(self) -> tuple[Event, ...]:
        return self.fetch_events(GRADES_CALENDAR_URL)

    def get_enrollment_calendar(self) -> tuple[Event, ...]:
        return self.fetch_events(ENROLLMENT_CALENDAR_URL)

    def get_course_calendar(self) -> tuple[Event, ...]:
        """Return dates on which courses for future terms are determined."""
        return self.fetch_events(COURSE_CALENDAR_URL)

    def get_graduation_calendar(self) -> tuple[Event, ...]:
        return self.fetch_events(GRADUATION_CALENDAR_URL)

    def fetch_events(self, url: str) -> tuple[Event, ...]:
        data = self.request("GET", url).json()
        if not isinstance(data, list):
            raise ValueError("calendar response must contain a list of events")

        events = []
        for raw_event in data:
            events.append(parse_event(raw_event))
        return tuple(events)


def parse_event(raw_event: dict[str, Any]) -> Event:
    """Convert one provider event into PittAPI's supported event model."""
    try:
        event_field = raw_event["customFields"][0]
        if event_field["label"] != "Event Title":
            raise ValueError("calendar event has an unexpected custom field")
        return Event(
            title=raw_event["title"],
            date=raw_event["startDateTime"][:10],
            content=event_field["value"],
            categories=tuple(raw_event["categoryCalendar"].split("|")),
        )
    except (KeyError, IndexError, TypeError) as error:
        raise ValueError("calendar event is missing required data") from error
