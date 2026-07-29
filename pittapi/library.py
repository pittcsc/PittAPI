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

Library catalog search and Hillman study-room reservations.
"""

from dataclasses import dataclass
from typing import Any

from pittapi.base_client import BaseClient

__all__ = ["Document", "LibraryClient", "QueryResult", "Reservation"]

LIBRARY_URL = "https://pitt.primo.exlibrisgroup.com/primaws/rest/pub/pnxs"
LIBRARY_PARAMS = {
    "acTriggered": "false",
    "blendFacetsSeparately": "false",
    "citationTrailFilterByAvailability": "true",
    "disableCache": "false",
    "getMore": "0",
    "inst": "01PITT_INST",
    "isCDSearch": "false",
    "lang": "en",
    "limit": "10",
    "newspapersActive": "false",
    "newspapersSearch": "false",
    "offset": "0",
    "otbRanking": "false",
    "pcAvailability": "false",
    "qExclude": "",
    "qInclude": "",
    "rapido": "false",
    "refEntryActive": "false",
    "rtaLinks": "true",
    "scope": "MyInst_and_CI",
    "searchInFulltextUserSelection": "false",
    "skipDelivery": "Y",
    "sort": "rank",
    "tab": "Everything",
    "vid": "01PITT_INST:01PITT_INST",
}
STUDY_ROOMS_URL = "https://pitt.libcal.com/spaces/bookings/search"
STUDY_ROOM_PARAMS = {
    "lid": "917",
    "gid": "1558",
    "eid": "0",
    "seat": "0",
    "d": "1",
    "customDate": "",
    "q": "",
    "daily": "0",
    "draw": "1",
    "order[0][column]": "1",
    "order[0][dir]": "asc",
    "start": "0",
    "length": "25",
    "search[value]": "",
}
DOCUMENT_FIELDS = (
    "title",
    "language",
    "subject",
    "format",
    "type",
    "isbns",
    "description",
    "publisher",
    "edition",
    "genre",
    "place",
    "creator",
    "version",
    "creationdate",
)


@dataclass(frozen=True, slots=True)
class Document:
    title: tuple[str, ...] = ()
    language: tuple[str, ...] = ()
    subject: tuple[str, ...] = ()
    format: tuple[str, ...] = ()
    type: tuple[str, ...] = ()
    isbns: tuple[str, ...] = ()
    description: tuple[str, ...] = ()
    publisher: tuple[str, ...] = ()
    edition: tuple[str, ...] = ()
    genre: tuple[str, ...] = ()
    place: tuple[str, ...] = ()
    creator: tuple[str, ...] = ()
    version: tuple[str, ...] = ()
    creationdate: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class QueryResult:
    num_results: int
    num_pages: int
    documents: tuple[Document, ...]


@dataclass(frozen=True, slots=True)
class Reservation:
    room: str
    reserved_from: str
    reserved_until: str


class LibraryClient(BaseClient):
    """Search Pitt's library catalog and study-room reservations."""

    def get_documents(self, query: str) -> QueryResult:
        params = {**LIBRARY_PARAMS, "q": f"any,contains,{query}"}
        return parse_query_result(self.request("GET", LIBRARY_URL, params=params).json())

    def get_document_by_bookmark(self, bookmark: str) -> QueryResult:
        params = {**LIBRARY_PARAMS, "bookMark": bookmark}
        data = self.request("GET", LIBRARY_URL, params=params).json()
        for error in data.get("errors", ()):
            if error.get("code") == "invalid.bookmark.format":
                raise ValueError("invalid bookmark")
        return parse_query_result(data)

    def hillman_total_reserved(self) -> int:
        data = self.request("GET", STUDY_ROOMS_URL, params=STUDY_ROOM_PARAMS).json()
        try:
            return data["recordsTotal"]
        except (KeyError, TypeError) as error:
            raise ValueError("reservation response is missing its total") from error

    def reserved_hillman_times(self) -> tuple[Reservation, ...]:
        data = self.request("GET", STUDY_ROOMS_URL, params=STUDY_ROOM_PARAMS).json()
        try:
            reservations = data["data"] or ()
            return tuple(
                Reservation(
                    room=item["itemName"],
                    reserved_from=item["from"],
                    reserved_until=item["to"],
                )
                for item in reservations
            )
        except (KeyError, TypeError) as error:
            raise ValueError("reservation response is missing required data") from error


def parse_query_result(data: dict[str, Any]) -> QueryResult:
    try:
        info = data["info"]
        documents = tuple(parse_document(item) for item in data["docs"])
        return QueryResult(num_results=info["total"], num_pages=info["last"], documents=documents)
    except (KeyError, TypeError) as error:
        raise ValueError("library response is missing required data") from error


def parse_document(data: dict[str, Any]) -> Document:
    display = data["pnx"]["display"]
    fields = {}
    for name in DOCUMENT_FIELDS:
        fields[name] = tuple(display.get(name, ()))
    return Document(**fields)
