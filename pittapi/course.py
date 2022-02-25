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

import json
import re
from datetime import datetime
from typing import List, Dict, Generator, NamedTuple, Optional, Tuple

import requests
from requests_html import HTMLSession, HTMLResponse
from parse import compile

import logging

logging.basicConfig(level=logging.DEBUG)

CLASS_SEARCH_URL = "https://psmobile.pitt.edu/app/catalog/classSearch"
CLASS_SEARCH_API_URL = "https://psmobile.pitt.edu/app/catalog/getClassSearch"
SECTION_DETAIL_URL = (
    "https://psmobile.pitt.edu/app/catalog/classsection/UPITT/{term}/{class_number}"
)

LABEL_MAP = {
    "Session": "session",
    "Career": "career",
    "Units": "units",
    "Grading": "grading",
    "Description": "description",
    "Enrollment Requirements": "preqs",
    "Class Attributes": "attributes",
    "Components": "components",
    "Status": "status",
    "Seats Taken": "seats_taken",
    "Seats Open": "seats_open",
    "Combined Section Capacity": "total_capacity",
    "Class Capacity": "total_capacity",
    "Unrestricted Seats": "unrestricted_seats",
    "Restricted Seats": "restricted_seats",
    "Wait List Total": "wait_list_total",
    "Wait List Capacity": "wait_list_capacity",
}

COMBINED_SECTION_PATTERN = compile(
    "{course_name}\n{subject_code} {course_number} - {section_number} ({class_number})\nStatus: {status}\nSeats Taken: {seats_taken:d}\nWait List Total: {wait_list_total:d}"
)
CREDIT_UNITS_PATTERN = compile("{:d} units")
SECTION_INFORMATION_PATTERN = compile(
    "Section: {section_number}-{section_type} ({class_number})\nSession: {session}\nDays/Times: {dt}\nRoom: {room}\nInstructor: {instructor}\nMeeting Dates: {meeting_dates}\nStatus: {status:w}{}"
)
COURSE_INFORMATION_PATTERN = compile("{subject_code} {course_number} - {course_title}")

SECTION_DETAIL_INT_FIELD = {
    "seats_taken",
    "seats_open",
    "total_capacity",
    "unrestricted_seats",
    "restricted_seats",
    "wait_list_total",
    "wait_list_capacity",
}


class CombinedSection(NamedTuple):
    term: str
    course_name: str
    subject_code: str
    course_number: str
    section_number: str
    class_number: str
    status: str
    seats_taken: int
    wait_list_total: int


class SectionDetails(NamedTuple):
    term: str
    session: str
    career: str
    units: int
    grading: str
    components: List[str]

    status: str
    seats_taken: int
    seats_open: int
    total_capacity: int
    unrestricted_seats: int
    restricted_seats: int
    wait_list_total: int
    wait_list_capacity: int

    preqs: str = ""
    description: str = ""
    attributes: Optional[List[str]] = None
    seat_restrictions: Optional[Dict[str, int]] = None
    combined_sections: Optional[List[CombinedSection]] = None


class SubjectCode(NamedTuple):
    subject_code: str
    description: str
    academic_group: str


class Section(NamedTuple):
    term: str
    session: str
    section_number: str
    class_number: str
    section_type: str
    instructor: str
    room: str
    status: str
    meetings_dates: Optional[List[Tuple[datetime, datetime]]] = None
    days: Optional[List[str]] = None
    times: Optional[List[str]] = None


class Course(NamedTuple):
    subject_code: str
    course_number: str
    course_title: str
    sections: Optional[List[Section]] = None


class Subject(NamedTuple):
    subject_code: str
    courses: Dict[str, Course]
    term: Optional[str] = None


def _get_subject_json() -> Generator[Dict, None, None]:
    text = requests.get(CLASS_SEARCH_URL).text
    s = re.search(r"(?=subjects\s*:\s).*,", text)
    text = s.group()[:-1]
    text = text[text.find(":") + 1 :]
    data = json.loads(text)

    for code in data:
        # Filter out subject codes for non main campuses
        if not any(v["campus"] == "PIT" for k, v in code["campuses"].items()):
            continue
        yield code


def get_subject_codes() -> List[str]:
    subjects = []
    for code in _get_subject_json():
        subjects.append(code["subject"])
    return subjects


def get_detailed_subject_codes() -> List[SubjectCode]:
    subjects = []
    for code in _get_subject_json():
        subjects.append(
            SubjectCode(
                subject_code=code["subject"],
                description=code["descr"],
                academic_group=code["acad_groups"]["group0"]["acad_group"],
            )
        )
    return subjects


def _parse_class_search_page(resp: HTMLResponse, term: str) -> Dict:
    if resp.html.search("No classes found matching your criteria"):
        raise ValueError("Criteria didn't find any classes")
    if resp.html.search(
        "The search took too long to respond, please try selecting additional search criteria."
    ):
        raise ValueError("Search response took too long.")
    if resp.status_code != 200:
        raise ValueError()

    courses = {}
    elements = resp.html.find("div")

    course: Optional[Course] = None
    for element in elements:
        logging.debug(element.text)
        if "secondary-head" in element.attrs["class"]:
            content = COURSE_INFORMATION_PATTERN.parse(element.text).named
            course = Course(**content, sections=list())
            courses[content["course_number"]] = course
        elif "section-content" in element.attrs["class"]:
            content = SECTION_INFORMATION_PATTERN.parse(element.text).named
            del content["dt"]
            del content["meeting_dates"]
            section = Section(**content, term=term)
            logging.debug(section)
            course.sections.append(section)
    return courses


def get_extra_section_details(
    *, section: Section = None, term=None, class_number=None
) -> SectionDetails:
    if section is None and (term is None or class_number is None):
        raise ValueError()
    if section is not None:
        term = section.term
        class_number = section.class_number

    data = {"term": term}
    session = HTMLSession()

    url = SECTION_DETAIL_URL.format(term=term, class_number=class_number)
    resp = session.get(url)
    elements = resp.html.xpath("/html/body/section/section/div")
    heading = ""
    for element in elements:
        logging.debug(element.text, end="\n\n")
        if "role" in element.attrs:
            heading = element.text
            continue

        if heading == "Combined Section":
            if "combined_sections" not in data:
                data["combined_sections"] = []
            content = COMBINED_SECTION_PATTERN.parse(element.text)
            combined_section = CombinedSection(**content.named, term=term)
            data["combined_sections"].append(combined_section)
            continue

        if "\n" not in element.text:
            continue

        label, content, *extra = element.text.split("\n")

        if heading == "Enrollment Restrictions":
            if "seat_restrictions" not in data:
                data["seat_restrictions"] = {}
            data["seat_restrictions"][label] = int(re.search("\d+", content).group())
            continue

        if label in LABEL_MAP:
            label = LABEL_MAP[label]
            if label == "components":
                content = content.split(", ")
            elif label == "units":
                content = CREDIT_UNITS_PATTERN.parse(content)[0]
            elif label == "attributes":
                content = [content] + extra
            elif label in SECTION_DETAIL_INT_FIELD:
                content = int(content)

            data[label] = content
    return SectionDetails(**data)


def _validate_term(term: str) -> str:
    """Validates that the term entered follows the pattern that Pitt does for term codes."""
    valid_terms = re.compile("2\d\d[147]")
    if valid_terms.match(term):
        return term
    raise ValueError("Term entered isn't a valid Pitt term.")


def _validate_course(course: str) -> str:
    """Validates that the course name entered is 4 characters long and in string form."""
    if course == "":
        raise ValueError("Invalid course number.")
    if not course.isdigit():
        raise ValueError("Invalid course number.")
    course_length = len(course)
    if course_length < 4:
        return ("0" * (4 - course_length)) + course
    elif course_length > 4:
        raise ValueError("Invalid course number.")
    return course


def _get_payload(
    term, *, subject="", course="", section=""
) -> Tuple[HTMLSession, Dict[str, str]]:
    """Make payload for request and generates CSRFToken for the request"""

    # Generate new CSRFToken
    session = HTMLSession()
    session.get(CLASS_SEARCH_URL)

    payload = {
        "CSRFToken": session.cookies["CSRFCookie"],
        "term": term,
        "campus": "PIT",
        "subject": subject,
        "acad_career": "",
        "catalog_nbr": course,
        "class_nbr": section,
    }
    return session, payload


def get_courses(term: str, subject: str) -> Subject:
    """Returns a list of courses available in term for a particular subject."""
    term = _validate_term(term)
    session, payload = _get_payload(term, subject=subject)
    response = session.post(CLASS_SEARCH_API_URL, data=payload)
    courses = _parse_class_search_page(response, term)
    subject = Subject(subject_code=subject, term=term, courses=courses)
    return subject


def get_course_sections(term: str, subject: str, course: str) -> Section:
    """Return details on all sections taught in a certain course"""
    term = _validate_term(term)
    course = _validate_course(course)
    session, payload = _get_payload(term, subject=subject, course=course)
    response = session.post(CLASS_SEARCH_API_URL, data=payload)
    course, *_ = _parse_class_search_page(response, term).values()
    return course


def get_section_details(term: str, section_number: str) -> Course:
    """Returns information pertaining to a certain section."""
    term = _validate_term(term)
    if isinstance(section_number, int):
        section_number = str(section_number)
    session, payload = _get_payload(term, section=section_number)
    response = session.post(CLASS_SEARCH_API_URL, data=payload)
    course, *_ = _parse_class_search_page(response, term).values()
    return course
