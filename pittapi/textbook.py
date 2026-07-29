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

Textbook information from Pitt's bookstore comparison service.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import json
import re
from typing import Any

from bs4 import BeautifulSoup
import requests

from pittapi.base_client import BaseClient

__all__ = ["CourseInfo", "Textbook", "TextbookClient", "TextbookTerm"]

BASE_URL = "https://pitt.verbacompare.com/"
SUBJECTS_URL = BASE_URL + "compare/departments/?term={term_id}"
COURSES_URL = BASE_URL + "compare/courses/?id={department_id}&term_id={term_id}"
BOOKS_URL = BASE_URL + "compare/books?id={section_id}"
MAX_REQUEST_ATTEMPTS = 3
TERMS_PATTERN = re.compile(r"Collections\.Terms\((\[.*?\])\)", re.DOTALL)


@dataclass(frozen=True, slots=True)
class CourseInfo:
    """A normalized course lookup without any network side effects."""

    subject: str
    course_num: str
    instructor: str | None = None
    section_num: str | None = None

    def __post_init__(self) -> None:
        subject = self.subject.upper()
        course_num = self.course_num
        instructor = self.instructor.upper() if self.instructor else None

        if not course_num.isdigit() or len(course_num) > 4:
            raise ValueError("invalid course number")
        if self.section_num and (len(self.section_num) != 4 or not self.section_num.isdigit()):
            raise ValueError("invalid section number")

        object.__setattr__(self, "subject", subject)
        object.__setattr__(self, "course_num", course_num.zfill(4))
        object.__setattr__(self, "instructor", instructor)


@dataclass(frozen=True, slots=True)
class Textbook:
    title: str | None
    author: str | None
    edition: str | None
    isbn: str | None
    citation: str | None


@dataclass(frozen=True, slots=True)
class TextbookTerm:
    """A bookstore term available for textbook inquiries."""

    id: str
    name: str
    inquiry_enabled: bool
    ordering_enabled: bool


class TextbookClient(BaseClient):
    """Fetch textbooks while keeping credentials and subjects per client."""

    def __init__(
        self,
        term: TextbookTerm | None = None,
        session: requests.Session | None = None,
        timeout: float = 10.0,
    ) -> None:
        super().__init__(session=session, timeout=timeout)
        self.term = term
        self.terms: tuple[TextbookTerm, ...] | None = None
        self.headers: dict[str, str] | None = None
        self.subject_ids: dict[str, str] | None = None

    def initialize_headers(self) -> None:
        last_error = None
        for _ in range(MAX_REQUEST_ATTEMPTS):
            try:
                response = self.request("GET", BASE_URL)
            except requests.HTTPError as error:
                last_error = error
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            csrf_element = soup.find("meta", attrs={"name": "csrf-token"})
            csrf_token = csrf_element.get("content") if csrf_element else None
            if not isinstance(csrf_token, str):
                raise requests.ConnectionError("textbook site did not provide valid request credentials")

            terms_match = TERMS_PATTERN.search(response.text)
            if terms_match is None:
                raise ValueError("textbook site did not provide available terms")
            try:
                terms_data = json.loads(terms_match.group(1))
                self.terms = tuple(
                    TextbookTerm(
                        id=str(item["id"]),
                        name=item["name"],
                        inquiry_enabled=item["inquiry"],
                        ordering_enabled=item["ordering"],
                    )
                    for item in terms_data
                )
            except (json.JSONDecodeError, KeyError, TypeError) as error:
                raise ValueError("textbook term response is missing required data") from error

            self.headers = {"X-CSRF-Token": csrf_token}
            return
        raise requests.ConnectionError(
            f"failed to connect to textbook site after {MAX_REQUEST_ATTEMPTS} attempts"
        ) from last_error

    def get_terms(self) -> tuple[TextbookTerm, ...]:
        """Return the terms currently published by the bookstore."""
        if self.terms is None:
            self.initialize_headers()
        return self.terms or ()

    def select_term(self, term: TextbookTerm) -> None:
        """Select a discovered term and clear term-specific subject state."""
        if term != self.term:
            self.term = term
            self.subject_ids = None

    def initialize_subjects(self) -> None:
        if self.term is None:
            raise ValueError("select a textbook term before requesting subjects")
        if self.headers is None:
            self.initialize_headers()

        url = SUBJECTS_URL.format(term_id=self.term.id)
        last_error = None
        for attempt in range(MAX_REQUEST_ATTEMPTS):
            try:
                response = self.request("GET", url, headers=self.headers)
            except requests.HTTPError as error:
                last_error = error
                if attempt < MAX_REQUEST_ATTEMPTS - 1:
                    self.initialize_headers()
                continue

            try:
                self.subject_ids = {item["name"]: item["id"] for item in response.json()}
            except (KeyError, TypeError) as error:
                raise ValueError("textbook subject response is missing required data") from error
            return
        raise requests.ConnectionError(f"failed to retrieve subjects after {MAX_REQUEST_ATTEMPTS} attempts") from last_error

    def get_textbooks_for_course(self, course: CourseInfo) -> tuple[Textbook, ...]:
        return self.get_textbooks_for_courses((course,))

    def get_textbooks_for_courses(self, courses: tuple[CourseInfo, ...] | list[CourseInfo]) -> tuple[Textbook, ...]:
        if self.term is None:
            raise ValueError("select a textbook term before requesting textbooks")
        if self.subject_ids is None:
            self.initialize_subjects()

        courses_by_subject = {}
        for course in courses:
            if course.subject not in self.subject_ids:
                raise LookupError(f"invalid textbook subject: {course.subject}")
            if course.subject not in courses_by_subject:
                courses_by_subject[course.subject] = self.get_courses(course.subject)

        section_ids = []
        for course in courses:
            section_ids.append(find_section_id(courses_by_subject[course.subject], course))

        with ThreadPoolExecutor() as executor:
            textbook_groups = executor.map(self.get_textbooks_for_section, section_ids)

        textbooks = []
        for group in textbook_groups:
            textbooks.extend(group)
        return tuple(textbooks)

    def get_courses(self, subject: str) -> list[dict[str, Any]]:
        if self.term is None:
            raise ValueError("select a textbook term before requesting courses")
        if self.headers is None:
            self.initialize_headers()
        if self.subject_ids is None or subject not in self.subject_ids:
            raise LookupError(f"invalid textbook subject: {subject}")

        url = COURSES_URL.format(department_id=self.subject_ids[subject], term_id=self.term.id)
        last_error = None
        for attempt in range(MAX_REQUEST_ATTEMPTS):
            try:
                response = self.request("GET", url, headers=self.headers)
            except requests.HTTPError as error:
                last_error = error
                if attempt < MAX_REQUEST_ATTEMPTS - 1:
                    self.initialize_headers()
                continue

            data = response.json()
            if not isinstance(data, list):
                raise ValueError("textbook course response must contain a list")
            return data
        raise requests.ConnectionError(f"failed to retrieve {subject} courses") from last_error

    def get_textbooks_for_section(self, section_id: str) -> tuple[Textbook, ...]:
        if self.term is None:
            raise ValueError("select a textbook term before requesting textbooks")
        if self.headers is None:
            self.initialize_headers()
        data = self.request("GET", BOOKS_URL.format(section_id=section_id), headers=self.headers).json()
        if not isinstance(data, list):
            raise ValueError("textbook response must contain a list")

        textbooks = []
        for item in data:
            textbook = parse_textbook(item)
            if textbook is not None:
                textbooks.append(textbook)
        return tuple(textbooks)


def find_section_id(courses: list[dict[str, Any]], course: CourseInfo) -> str:
    for course_data in courses:
        if course_data["id"] == course.subject + course.course_num:
            return find_section(course_data["sections"], course.instructor, course.section_num)
    raise LookupError(f"invalid textbook course: {course.subject} {course.course_num}")


def find_section(
    sections: list[dict[str, str]],
    instructor: str | None,
    section_num: str | None,
) -> str:
    if section_num:
        for section in sections:
            if section["name"] == section_num:
                return section["id"]
        raise LookupError(f"section not found: {section_num}")

    if instructor:
        for section in sections:
            if section["instructor"] == instructor:
                return section["id"]
        raise LookupError(f"instructor not found: {instructor}")

    instructors = {section["instructor"] for section in sections}
    if len(sections) == 1 or len(instructors) == 1:
        return sections[0]["id"]
    raise LookupError("provide an instructor or section number to identify the textbook section")


def parse_textbook(data: dict[str, Any]) -> Textbook | None:
    textbook = Textbook(
        title=data.get("title"),
        author=data.get("author"),
        edition=data.get("edition"),
        isbn=data.get("isbn"),
        citation=data.get("citation"),
    )
    values = (textbook.title, textbook.author, textbook.edition, textbook.isbn, textbook.citation)
    return textbook if any(values) else None
