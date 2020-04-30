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

ACADEMIC_CALENDAR_URL = "https://25livepub.collegenet.com/calendars/pitt-academic-calendar.xml"


def get_academic_calendar_events(include_summary=False):
    """"""
    d = feedparser.parse(ACADEMIC_CALENDAR_URL)
    events = [(entry.published_parsed, entry.title.upper()) for entry in d.entries]
    return events
