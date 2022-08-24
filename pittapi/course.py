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

import datetime
import re
import requests
from typing import List, NamedTuple, Union

SUBJECTS_API = "https://prd.ps.pitt.edu/psc/pitcsprd/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_COURSE_CATALOG.FieldFormula.IScript_CatalogSubjects?institution=UPITT"
SUBJECT_COURSES_API = "https://prd.ps.pitt.edu/psc/pitcsprd/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_COURSE_CATALOG.FieldFormula.IScript_SubjectCourses?institution=UPITT&subject={subject}"
COURSE_DETAIL_API = "https://prd.ps.pitt.edu/psc/pitcsprd/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_COURSE_CATALOG.FieldFormula.IScript_CatalogCourseDetails?institution=UPITT&course_id={id}&effdt=2018-06-30&x_acad_career={career}&crse_offer_nbr=1&use_catalog_print=Y"
COURSE_SECTIONS_API = "https://prd.ps.pitt.edu/psc/pitcsprd/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_BROWSE_CLASSES.FieldFormula.IScript_BrowseSections?institution=UPITT&campus=&location=&course_id={id}&institution=UPITT&x_acad_career={career}&term={term}&crse_offer_nbr=1"
SECTION_DETAILS_API = "https://prd.ps.pitt.edu/psc/pitcsprd/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassDetails?institution=UPITT&term={term}&class_nbr={id}"
    # id -> unique course ID, not to be confused with course code (for instance, CS 0007 has code 105611)
    # career -> for example, UGRD (undergraduate)

VALID_TERMS = re.compile("2\d\d[147]")

ACADEMIC_CAREERS = ['UGRD', 'MEDS', 'LAW', 'GRAD', 'DMED', 'CNED']

class CombinedSection(NamedTuple):
    pass
#     term: str
#     course_name: str
#     subject_code: str
#     course_number: str
#     section_number: str
#     class_number: str
#     status: str
#     seats_taken: int
#     wait_list_total: int


class SectionDetails(NamedTuple):
    pass
#     term: str
#     session: str
#     career: str
#     units: int
#     grading: str
#     components: List[str]

#     status: str
#     seats_taken: int
#     seats_open: int
#     total_capacity: int
#     unrestricted_seats: int
#     restricted_seats: int
#     wait_list_total: int
#     wait_list_capacity: int

#     preqs: str = ""
#     description: str = ""
#     attributes: Optional[List[str]] = None
#     seat_restrictions: Optional[Dict[str, int]] = None
#     combined_sections: Optional[List[CombinedSection]] = None


class SubjectCode(NamedTuple):
    pass
#     subject_code: str
#     description: str
#     academic_group: str


class Section(NamedTuple):
    pass
#     term: str
#     session: str
#     section_number: str
#     class_number: str
#     section_type: str
#     instructor: str
#     room: str
#     status: str
#     meetings_dates: Optional[List[Tuple[datetime, datetime]]] = None
#     days: Optional[List[str]] = None
#     times: Optional[List[str]] = None


class Course(NamedTuple):
    pass
#     subject_code: str
#     course_number: str
#     course_title: str
#     sections: Optional[List[Section]] = None


class Subject(NamedTuple):
    pass
#     subject_code: str
#     courses: Dict[str, Course]
#     term: Optional[str] = None

def get_subject_courses(subject: str) -> Subject:
    pass

def get_term_courses(term: Union[str, int], subject: str) -> Subject:
    pass

def get_course_sections(term: Union[str, int], subject: str, course: Union[str, int]) -> Course:
    pass

def get_section_details(term: Union[str, int], section_number: int) -> Section:
    pass
    

def _validate_term(term: Union[str, int]) -> str:
    """Validates that the term entered follows the pattern that Pitt does for term codes."""
    if VALID_TERMS.match(str(term)):
        return str(term)
    raise ValueError("Term entered isn't a valid Pitt term, must match regex 2\d\d[147]")

def _validate_subject(subject: str) -> str:
    """Validates that the subject code entered is present in the API request."""
    if subject in _get_subject_codes():
        return subject
    raise ValueError("Subject code entered isn't a valid Pitt subject code.")

def _validate_course(course: Union[str, int]) -> str:
    """Validates that the course name entered is 4 characters long and in string form."""
    if course == "":
        raise ValueError("Invalid course number, please enter a non-empty string.")
    if (type(course) is str) and (not course.isdigit()):
        raise ValueError("Invalid course number, must be a number")
    if (type(course) is int) and (course <= 0):
        raise ValueError("Invalid course number, must be positive")
    course_length = len(str(course))
    if course_length < 4:
        return ("0" * (4 - course_length)) + str(course)
    elif course_length > 4:
        raise ValueError("Invalid course number, must be 4 characters long")
    return str(course)

def _validate_academic_career(academic_career: str) -> str:
    if academic_career not in ACADEMIC_CAREERS:
        raise ValueError("Invalid academic career, must be one of UGRD, MEDS, LAW, GRAD, DMED, CNED")
    return academic_career

def _get_subject_codes() -> List[str]:
    response = _get_subjects()
    codes = []
    for subject in response["subjects"]:
        codes.append(subject["subject"])
    return codes

def _get_internal_id_dict(subject: str) -> dict:
    response = _get_subject_courses(subject)
    internal_id_dict = {}
    for course in response["courses"]:
        if course["catalog_nbr"] not in internal_id_dict:
            internal_id_dict[course["catalog_nbr"]] = course["crse_id"]
    return internal_id_dict

def _get_subjects() -> dict:
    return requests.get(SUBJECTS_API).json()

def _get_subject_courses(subject: str) -> dict:
    subject = _validate_subject(subject)
    return requests.get(SUBJECT_COURSES_API.format(subject=subject)).json()

def _get_course_detail(course_id: Union[str, int], academic_career: str) -> dict:
    academic_career = _validate_academic_career(academic_career)
    response = requests.get(COURSE_DETAIL_API.format(id=course_id, career=academic_career)).json()
    if response["course_details"] == {}:
        raise ValueError("Invalid course ID; course with that ID does not exist")
    return response

def _get_course_sections(course_id: Union[str, int], academic_career: str, term: Union[str, int]) -> dict:
    term = _validate_term(term)
    academic_career = _validate_academic_career(academic_career)
    response = requests.get(COURSE_SECTIONS_API.format(id=course_id, career=academic_career, term=term)).json()
    if len(response["sections"]) == 0:
        raise ValueError("Invalid course ID; course with that ID does not exist")
    return response

def _get_section_details(term: Union[str, int], section_id: Union[str, int]) -> dict:
    term = _validate_term(term)
    response = requests.get(SECTION_DETAILS_API.format(term=term, id=section_id)).json()
    if error in response:
        raise ValueError("Invalid section ID; section with that ID does not exist")
    return response