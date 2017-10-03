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
import warnings

import grequests
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError as RequestsConnectionError
from typing import List, Dict, Any, Callable, Generator, Tuple

BASE_URL = 'http://pitt.verbacompare.com/'


def _fetch_term_codes() -> List[str]:
    """Fetches current valid term codes"""
    try:
        page = requests.get(BASE_URL)
    except RequestsConnectionError:
        return []
    script = BeautifulSoup(page.text, 'lxml').findAll('script')[-2].text
    data = json.loads(script[script.find('['):script.find(']') + 1])
    terms = [
        item['id']
        for item in data
    ]
    return terms


TERMS = _fetch_term_codes()
CODES = [
    'ADMJ', 'ADMPS', 'AFRCNA', 'AFROTC', 'ANTH', 'ARABIC', 'ARTSC', 'ASL', 'ASTRON', 'ATHLTR', 'BACC', 'BCHS', 'BECN',
    'BFIN', 'BHRM', 'BIND', 'BIOENG', 'BIOETH', 'BIOINF', 'BIOSC', 'BIOST', 'BMIS', 'BMKT', 'BOAH', 'BORG', 'BQOM',
    'BSEO', 'BSPP', 'BUS', 'BUSACC', 'BUSADM', 'BUSBIS', 'BUSECN', 'BUSENV', 'BUSERV', 'BUSFIN', 'BUSHRM', 'BUSMKT',
    'BUSORG', 'BUSQOM', 'BUSSCM', 'BUSSPP', 'CDACCT', 'CDENT', 'CEE', 'CGS', 'CHE', 'CHEM', 'CHIN', 'CLASS', 'CLRES',
    'CLST', 'CMMUSIC', 'CMPBIO', 'COE', 'COEA', 'COEE', 'COMMRC', 'CS', 'CSD', 'DENHYG', 'DENT', 'DIASCI', 'DSANE',
    'EAS', 'ECE', 'ECON', 'EDUC', 'ELI', 'EM', 'ENDOD', 'ENGCMP', 'ENGFLM', 'ENGLIT', 'ENGR', 'ENGSCI', 'ENGWRT',
    'ENRES', 'EOH', 'EPIDEM', 'FACDEV', 'FILMG', 'FILMST', 'FP', 'FR', 'FTADMA', 'FTDA', 'FTDB', 'FTDC', 'FTDR', 'GEOL',
    'GER', 'GERON', 'GREEK', 'GREEKM', 'GSWS', 'HAA', 'HIM', 'HINDI', 'HIST', 'HONORS', 'HPA', 'HPM', 'HPS', 'HRS',
    'HUGEN', 'IDM', 'IE', 'IL', 'IMB', 'INFSCI', 'INTBP', 'IRISH', 'ISB', 'ISSP', 'ITAL', 'JPNSE', 'JS', 'KOREAN',
    'LATIN', 'LAW', 'LCTL', 'LDRSHP', 'LEGLST', 'LING', 'LIS', 'LSAP', 'MATH', 'ME', 'MED', 'MEDEDU', 'MEMS', 'MILS',
    'MOLBPH', 'MSCBIO', 'MSCBMP', 'MSCMP', 'MSE', 'MSIMM', 'MSMBPH', 'MSMGDB', 'MSMPHL', 'MSMVM', 'MSNBIO', 'MUSIC',
    'NEURO', 'NPHS', 'NROSCI', 'NUR', 'NURCNS', 'NURNM', 'NURNP', 'NURSAN', 'NURSP', 'NUTR', 'ODO', 'OLLI', 'ORBIOL',
    'ORSUR', 'OT', 'PAS', 'PEDC', 'PEDENT', 'PERIO', 'PERS', 'PETE', 'PHARM', 'PHIL', 'PHYS', 'PIA', 'POLISH', 'PORT',
    'PROSTH', 'PS', 'PSY', 'PSYC', 'PSYED', 'PT', 'PUBHLT', 'PUBSRV', 'REHSCI', 'REL', 'RELGST', 'RESTD', 'RUSS', 'SA',
    'SERCRO', 'SLAV', 'SLOVAK', 'SOC', 'SOCWRK', 'SPAN', 'STAT', 'SWAHIL', 'SWBEH', 'SWCOSA', 'SWE', 'SWGEN', 'SWINT',
    'SWRES', 'SWWEL', 'TELCOM', 'THEA', 'TURKSH', 'UKRAIN', 'URBNST', 'VIET']
KEYS = ['isbn', 'citation', 'title', 'edition', 'author']
QUERIES = {
    'courses': 'compare/courses/?id={}&term_id={}',
    'books': 'compare/books?id={}'
}
LOOKUP_ERRORS = {
    1: 'instructor {1}.',
    2: 'section {2}.',
    3: 'instructor {1} or section {2}.'
}


def _construct_query(query: str, *args) -> str:
    """Constructs query based on which one is requested
    and fills the query in with the given arguments
    """
    return QUERIES[query].format(*args)


def _validate_term(term: str) -> str:
    """Validates term is a string and check if it is valid."""
    if len(TERMS) == 0:
        warnings.warn('Wasn\'t able to validate term. Assuming term code is valid.')
        if len(term) == 4 and term.isdigit():
            return term
        raise ValueError("Invalid term")
    if term in TERMS:
        return term
    raise ValueError("Invalid term")


def _validate_course(course: str) -> str:
    """Validates course is a four digit number,
     otherwise adds zero(s) to create four digit number or,
     raises an exception.
     """
    if len(course) > 4 or not course.isdigit():
        raise ValueError('Invalid course number')
    elif len(course) == 4:
        return course
    return '0' * (4 - len(course)) + course


def _filter_dictionary(d: Dict[Any,Any], keys: List[Any]) -> Dict[Any,Any]:
    """Creates new dictionary from selecting certain
    key value pairs from another dictionary
    """
    return dict(
        (k, d[k])
        for k in keys
        if k in d
    )


def _find_item(id_key, data_key, error_item) -> Callable[[Dict[Any,Any], Any], Any]:
    """Finds a dictionary in a list based on its id key, and
    returns a piece of data from the dictionary based on a data key.
    """
    def find(data, value):
        for item in data:
            if item[id_key] == value:
                return item[data_key]
        raise LookupError('Can\'t find {} {}.'.format(error_item, str(value)))
    return find


_find_sections = _find_item('id', 'sections', 'course')
_find_course_id_by_instructor = _find_item('instructor', 'id', 'instructor')
_find_course_id_by_section = _find_item('name', 'id', 'section')


def _extract_id(response, course: str, instructor: str, section: str) -> str:
    """Gathers sections from departments and finds course id by
     instructor name or section number.
     """
    sections = _find_sections(response.json(), course)
    error = 0
    try:
        if instructor is not None:
            return _find_course_id_by_instructor(sections, instructor.upper())
    except LookupError:
        error += 1
    try:
        if section is not None:
            return _find_course_id_by_section(sections, section)
    except LookupError:
        error += 2
    raise LookupError('Unable to find course by ' + LOOKUP_ERRORS[error].format(instructor, section))


def _extract_books(ids: List[str]) -> List[Dict[str,str]]:
    """Fetches a course's textbook information and returns a list
    of textbooks for the given course.
    """
    responses = grequests.imap([
        grequests.get(BASE_URL + _construct_query('books', section_id))
        for section_id in ids
    ])
    books = [
        _filter_dictionary(book, KEYS)
        for response in responses
        for book in response.json()
    ]
    return books


# Meant to force a return of None instead of raising a KeyError
# when using a nonexistent key
class DefaultDict(dict):
    def __missing__(self, key):
        return None


def _fetch_course(courses: List[Dict[str,str]], departments: Dict[str,str]) -> Generator[Tuple[str,str,str,str], None, None]:
    """Generator for fetching a courses information in order"""
    for course in courses:
        course = DefaultDict(course)
        yield (
            departments[course['department']],
            course['department'] + _validate_course(course['course']),
            course['instructor'],
            course['section']
        )


def _get_department_number(department_code: str) -> int:
    """Temporary solution to finding a department.
    There will be a new method to getting department information
    at a later time.
    """
    department_number = CODES.index(department_code) + 22399
    if department_number > 22462:
        department_number += 2  # between codes DSANE and EAS 2 id numbers are skipped.
    if department_number > 22580:
        department_number += 1  # between codes PUBSRV and REHSCI 1 id number is skipped.
    return department_number


def get_textbooks(term: str, courses: List[Dict[str,str]]) -> List[Dict[str,str]]:
    """Retrieves textbooks for multiple courses in the same term."""
    departments = {course['department'] for course in courses}
    responses = grequests.map(
        [
            grequests.get(BASE_URL + _construct_query('courses', _get_department_number(department), term), timeout=10)
            for department in departments
        ]
    )
    section_ids = [
        _extract_id(*course)
        for course in _fetch_course(courses, dict(zip(departments, responses)))
    ]
    return _extract_books(section_ids)


def get_textbook(term: str, department: str, course: str, instructor:str=None, section:str=None) -> List[Dict[str,str]]:
    """Retrieves textbooks for a given course."""
    has_section_or_instructor = (instructor is not None) or (section is not None)
    if not has_section_or_instructor:
        raise TypeError('get_textbook() is missing a instructor or section argument')
    response = requests.get(BASE_URL + _construct_query('courses', _get_department_number(department), term))
    section_id = _extract_id(response, department + _validate_course(course), instructor, section)
    return _extract_books([section_id])
