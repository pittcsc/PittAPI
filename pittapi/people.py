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

Search Pitt's public people directory.
"""

from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag

from pittapi.base_client import BaseClient

__all__ = ["Person", "PersonField", "PeopleClient"]

PEOPLE_SEARCH_URL = "https://find.pitt.edu/Search"


@dataclass(frozen=True, slots=True)
class PersonField:
    name: str
    values: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Person:
    name: str
    fields: tuple[PersonField, ...]


class PeopleClient(BaseClient):
    """Search public Pitt directory records."""

    def get_person(self, query: str) -> tuple[Person, ...]:
        response = self.request("POST", PEOPLE_SEARCH_URL, data={"search": query})
        if "Too many people matched your criteria." in response.text:
            raise ValueError("too many people matched the search")

        soup = BeautifulSoup(response.text, "html.parser")
        people = []
        for entry in soup.select("#searchResults > section"):
            name, *segments = entry.find_all("span")
            people.append(Person(name=name.get_text(strip=True), fields=parse_segments(segments)))
        return tuple(people)


def parse_segments(segments: list[Tag]) -> tuple[PersonField, ...]:
    values_by_name: dict[str, list[str]] = {}
    current_name = None
    for segment in segments:
        text = segment.get_text(strip=True)
        if "row-label" in segment.get("class", ()):
            current_name = text or None
        elif current_name is not None and text:
            values_by_name.setdefault(current_name, []).append(text)

    return tuple(PersonField(name=name, values=tuple(values)) for name, values in values_by_name.items())
