"""
This module is named cal instead of calendar due to naming conflict occurring
inside of feedparser

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
"""

import feedparser
import re
from typing import List
from collections import namedtuple

content = re.compile(":&(.)*?<")
Event = namedtuple('Event', ['timestamp', 'timestamp_struct', 'content'])

ACADEMIC_CALENDAR_URL: str = "https://25livepub.collegenet.com/calendars/pitt-academic-calendar.xml"
GRADES_CALENDAR_URL: str = "https://25livepub.collegenet.com/calendars/pitt-grades-calendar.xml"
ENROLLMENT_CALENDAR_URL: str = "https://25livepub.collegenet.com/calendars/pitt-enrollment-calendar.xml"
COURSE_CALENDAR_URL: str = "https://25livepub.collegenet.com/calendars/pitt-courseclass-calendar.xml"
GRADUATION_CALENDAR_URL: str = "https://25livepub.collegenet.com/calendars/pitt-graduation-calendar.xml"


def _fetch_calendar_events(url: str) -> List[Event]:
    """"""
    d = feedparser.parse(url)
    events = []
    for entry in d.entries:
        event_content = content.search(entry.summary).group()[7:-2]
        event = Event(timestamp=entry.published, timestamp_struct=entry.published_parsed, content=event_content)
        events.append(event)
    return events


def get_academic_calendar() -> List[Event]:
    """"""
    return _fetch_calendar_events(ACADEMIC_CALENDAR_URL)


def get_grades_calendar() -> List[Event]:
    """"""
    return _fetch_calendar_events(GRADES_CALENDAR_URL)


def get_enrollment_calendar() -> List[Event]:
    """"""
    return _fetch_calendar_events(ENROLLMENT_CALENDAR_URL)


def get_course_calendar() -> List[Event]:
    """This is not a calendar about course schedule but rather
    when courses/class are being determined for the next semester"""
    return _fetch_calendar_events(COURSE_CALENDAR_URL)


def get_graduation_calendar() -> List[Event]:
    """"""
    return _fetch_calendar_events(GRADUATION_CALENDAR_URL)
