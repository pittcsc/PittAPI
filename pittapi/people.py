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
"""
from requests_html import HTMLSession
from typing import List, Dict
from parse import compile

EMAIL_PATTERN = compile("Email{}")

PEOPLE_SEARCH_URL = "https://find.pitt.edu/Search"


def get_person(query: str) -> List[Dict[str, str]]:
    payload = {
        "search": query
    }
    session = HTMLSession()
    resp = session.post(PEOPLE_SEARCH_URL, data=payload)
    if resp.text.startswith("Too many people matched your criteria."):
        pass  # Return an exception
    elements = resp.html.xpath('/html/div/section')
    result = []
    for entry in elements:
        segments = entry.text.split('\n')
        person = {}
        if len(segments) <= 2:  # Only contains name
            name, _ = segments
            person['name'] = name
            person['type'] = "unknown"
        elif segments[2] == "Show More":  # Student
            name, email, _, *other = segments
            email = EMAIL_PATTERN.parse(email).fixed[0]
            person["name"] = name
            person["email"] = email
            person["type"] = "student"
        else:  # Employee
            name, *_ = segments
            person['name'] = name
            person['type'] = "employee"
        result.append(person)
    return result