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

Course catalog and section information from Pitt PeopleSoft.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from pittapi.base_client import BaseClient

__all__ = [
    "Attribute",
    "Component",
    "Course",
    "CourseClient",
    "CourseDetails",
    "Instructor",
    "Meeting",
    "Section",
    "SectionDetails",
    "Subject",
]

SUBJECTS_API = (
    "https://pitcsprd.csps.pitt.edu/psc/pitcsprd/EMPLOYEE/SA/s/"
    "WEBLIB_HCX_CM.H_COURSE_CATALOG.FieldFormula.IScript_CatalogSubjects?institution=UPITT"
)
SUBJECT_COURSES_API = (
    "https://pitcsprd.csps.pitt.edu/psc/pitcsprd/EMPLOYEE/SA/s/"
    "WEBLIB_HCX_CM.H_COURSE_CATALOG.FieldFormula.IScript_SubjectCourses?institution=UPITT&subject={subject}"
)
COURSE_DETAIL_API = (
    "https://pitcsprd.csps.pitt.edu/psc/pitcsprd/EMPLOYEE/SA/s/"
    "WEBLIB_HCX_CM.H_COURSE_CATALOG.FieldFormula.IScript_CatalogCourseDetails?institution=UPITT&course_id={id}"
    "&effdt=2018-06-30&crse_offer_nbr=1&use_catalog_print=Y"
)
COURSE_SECTIONS_API = (
    "https://pitcsprd.csps.pitt.edu/psc/pitcsprd/EMPLOYEE/SA/s/"
    "WEBLIB_HCX_CM.H_BROWSE_CLASSES.FieldFormula.IScript_BrowseSections?institution=UPITT&campus=&location="
    "&course_id={id}&institution=UPITT&term={term}&crse_offer_nbr=1"
)
SECTION_DETAILS_API = (
    "https://pitcsprd.csps.pitt.edu/psc/pitcsprd/EMPLOYEE/SA/s/"
    "WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassDetails?institution=UPITT&term={term}&class_nbr={id}"
)
VALID_TERM = re.compile(r"2\d\d[147]\Z")


@dataclass(frozen=True, slots=True)
class Instructor:
    name: str
    email: str | None = None


@dataclass(frozen=True, slots=True)
class Meeting:
    days: str
    start_time: str
    end_time: str
    start_date: str
    end_date: str
    instructors: tuple[Instructor, ...] = ()


@dataclass(frozen=True, slots=True)
class Attribute:
    attribute: str
    attribute_description: str
    value: str
    value_description: str


@dataclass(frozen=True, slots=True)
class Component:
    component: str
    required: bool


@dataclass(frozen=True, slots=True)
class SectionDetails:
    units: str
    class_capacity: str
    enrollment_total: str
    enrollment_available: str
    wait_list_capacity: str
    wait_list_total: str
    valid_to_enroll: str
    combined_section_numbers: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Section:
    term: str
    session: str
    section_number: str
    class_number: str
    section_type: str
    status: str
    instructors: tuple[Instructor, ...] = ()
    meetings: tuple[Meeting, ...] = ()
    details: SectionDetails | None = None


@dataclass(frozen=True, slots=True)
class Course:
    subject_code: str
    course_number: str
    course_id: str
    course_title: str


@dataclass(frozen=True, slots=True)
class CourseDetails:
    course: Course
    course_description: str | None = None
    credit_range: tuple[int, int] | None = None
    requisites: str | None = None
    components: tuple[Component, ...] = ()
    attributes: tuple[Attribute, ...] = ()
    sections: tuple[Section, ...] = ()


@dataclass(frozen=True, slots=True)
class Subject:
    subject_code: str
    courses: tuple[Course, ...]


class CourseClient(BaseClient):
    """Fetch courses and sections from Pitt's PeopleSoft catalog."""

    def get_subject_courses(self, subject: str) -> Subject:
        normalized_subject = self.validate_subject(subject)
        data = self.get_subject_course_data(normalized_subject)
        try:
            courses = tuple(parse_course(item, normalized_subject) for item in data["courses"])
        except (KeyError, TypeError) as error:
            raise ValueError("subject course response is missing required data") from error
        return Subject(subject_code=normalized_subject, courses=courses)

    def get_course_details(self, term: str | int, subject: str, course: str | int) -> CourseDetails:
        normalized_term = validate_term(term)
        normalized_subject = self.validate_subject(subject)
        normalized_course = validate_course_number(course)
        course_id = self.find_course_id(normalized_subject, normalized_course)

        catalog_data = self.get_course_data(course_id)
        section_data = self.get_course_section_data(course_id, normalized_term)
        try:
            return parse_course_details(
                catalog_data["course_details"],
                section_data["sections"],
                normalized_term,
                normalized_subject,
                normalized_course,
                course_id,
            )
        except (KeyError, IndexError, TypeError) as error:
            raise ValueError("course response is missing required data") from error

    def get_section_details(self, term: str | int, class_number: str | int) -> Section:
        normalized_term = validate_term(term)
        data = self.get_section_data(normalized_term, class_number)
        try:
            return parse_section_details(data["section_info"], normalized_term, str(class_number))
        except (KeyError, IndexError, TypeError, ValueError) as error:
            raise ValueError("section response is missing required data") from error

    def validate_subject(self, subject: str) -> str:
        normalized_subject = subject.upper()
        data = self.request("GET", SUBJECTS_API).json()
        try:
            subject_codes = {item["subject"] for item in data["subjects"]}
        except (KeyError, TypeError) as error:
            raise ValueError("subject response is missing required data") from error
        if normalized_subject not in subject_codes:
            raise ValueError(f"invalid subject code: {subject}")
        return normalized_subject

    def find_course_id(self, subject: str, course_number: str) -> str:
        data = self.get_subject_course_data(subject)
        try:
            for course in data["courses"]:
                if course["catalog_nbr"] == course_number:
                    return course["crse_id"]
        except (KeyError, TypeError) as error:
            raise ValueError("subject course response is missing required data") from error
        raise LookupError(f"course not found: {subject} {course_number}")

    def get_subject_course_data(self, subject: str) -> dict[str, Any]:
        return self.request("GET", SUBJECT_COURSES_API.format(subject=subject)).json()

    def get_course_data(self, course_id: str) -> dict[str, Any]:
        data = self.request("GET", COURSE_DETAIL_API.format(id=course_id)).json()
        if not data.get("course_details"):
            raise LookupError(f"course ID not found: {course_id}")
        return data

    def get_course_section_data(self, course_id: str, term: str) -> dict[str, Any]:
        data = self.request("GET", COURSE_SECTIONS_API.format(id=course_id, term=term)).json()
        if not data.get("sections"):
            raise LookupError(f"no sections found for course ID {course_id} in term {term}")
        return data

    def get_section_data(self, term: str, class_number: str | int) -> dict[str, Any]:
        data = self.request("GET", SECTION_DETAILS_API.format(term=term, id=class_number)).json()
        if "error" in data:
            raise LookupError(f"section not found: {class_number}")
        return data


def validate_term(term: str | int) -> str:
    term_text = str(term)
    if not VALID_TERM.fullmatch(term_text):
        raise ValueError("term must be a four-digit Pitt term ending in 1, 4, or 7")
    return term_text


def validate_course_number(course: str | int) -> str:
    course_text = str(course)
    if not course_text.isdigit() or int(course_text) <= 0:
        raise ValueError("course number must be a positive number")
    if len(course_text) > 4:
        raise ValueError("course number cannot exceed four digits")
    return course_text.zfill(4)


def parse_course(data: dict[str, Any], subject: str) -> Course:
    return Course(
        subject_code=subject,
        course_number=data["catalog_nbr"],
        course_id=data["crse_id"],
        course_title=data["descr"],
    )


def parse_course_details(
    catalog: dict[str, Any],
    sections: list[dict[str, Any]],
    term: str,
    subject: str,
    course_number: str,
    course_id: str,
) -> CourseDetails:
    course = Course(
        subject_code=subject,
        course_number=course_number,
        course_id=course_id,
        course_title=sections[0]["descr"],
    )
    offerings = catalog.get("offerings", ())
    requisites = offerings[0].get("req_group") if offerings else None
    components = tuple(
        Component(component=item["descr"], required=item["optional"] == "N") for item in catalog.get("components", ())
    )
    attributes = tuple(
        Attribute(
            attribute=item["crse_attribute"],
            attribute_description=item["crse_attribute_descr"],
            value=item["crse_attribute_value"],
            value_description=item["crse_attribute_value_descr"],
        )
        for item in catalog.get("attributes", ())
    )
    parsed_sections = tuple(parse_catalog_section(item, term) for item in sections)
    return CourseDetails(
        course=course,
        course_description=catalog.get("descrlong"),
        credit_range=(catalog["units_minimum"], catalog["units_maximum"]),
        requisites=requisites,
        components=components,
        attributes=attributes,
        sections=parsed_sections,
    )


def parse_catalog_section(data: dict[str, Any], term: str) -> Section:
    instructors = parse_instructors(data.get("instructors", ()))
    meetings = []
    for item in data.get("meetings", ()):
        meeting_instructors = ()
        if item.get("instructor"):
            meeting_instructors = (Instructor(name=item["instructor"]),)
        meetings.append(
            Meeting(
                days=item["days"],
                start_time=item["start_time"],
                end_time=item["end_time"],
                start_date=item["start_dt"],
                end_date=item["end_dt"],
                instructors=meeting_instructors,
            )
        )
    return Section(
        term=term,
        session=data["session"],
        section_number=data["class_section"],
        class_number=str(data["class_nbr"]),
        section_type=data["section_type"],
        status=data["enrl_stat_descr"],
        instructors=instructors,
        meetings=tuple(meetings),
    )


def parse_section_details(section_info: dict[str, Any], term: str, class_number: str) -> Section:
    details_data = section_info["class_details"]
    enrollment = section_info["class_availability"]
    combined_numbers = ()
    if section_info["is_combined"]:
        combined_numbers = tuple(str(item["class_nbr"]) for item in section_info["combined_sections"])

    details = SectionDetails(
        units=details_data["units"],
        class_capacity=enrollment["class_capacity"],
        enrollment_total=enrollment["enrollment_total"],
        enrollment_available=str(enrollment["enrollment_available"]),
        wait_list_capacity=enrollment["wait_list_capacity"],
        wait_list_total=enrollment["wait_list_total"],
        valid_to_enroll=section_info["valid_to_enroll"],
        combined_section_numbers=combined_numbers,
    )
    meetings = tuple(parse_detailed_meeting(item) for item in section_info["meetings"])
    return Section(
        term=term,
        session=details_data["session"],
        section_number=details_data["class_section"],
        class_number=class_number,
        section_type=details_data["component"],
        status=details_data["status"],
        meetings=meetings,
        details=details,
    )


def parse_detailed_meeting(data: dict[str, Any]) -> Meeting:
    start_date, end_date = data["date_range"].split(" - ")
    return Meeting(
        days=data["days"],
        start_time=data["meeting_time_start"],
        end_time=data["meeting_time_end"],
        start_date=start_date,
        end_date=end_date,
        instructors=parse_instructors(data["instructors"]),
    )


def parse_instructors(instructors: list[dict[str, Any]] | tuple[Any, ...]) -> tuple[Instructor, ...]:
    if not instructors or instructors[0] == "To be Announced":
        return ()
    parsed = []
    for instructor in instructors:
        if instructor["name"] in ("To be Announced", "-"):
            continue
        parsed.append(Instructor(name=instructor["name"], email=instructor.get("email")))
    return tuple(parsed)
