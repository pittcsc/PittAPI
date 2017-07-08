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

BASE_URL = 'http://pitt.verbacompare.com/'


def _fetch_term_codes():
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


def _construct_query(query, *args):
    return QUERIES[query].format(*args)


def _validate_term(term):
    """Validates term is a string and check if it is valid."""
    if len(TERMS) == 0:
        warnings.warn('Wasn\'t able to validate term. Assuming term code is valid.')
        if len(term) == 4 and term.isdigit():
            return term
        raise ValueError("Invalid term")
    if term in TERMS:
        return term
    raise ValueError("Invalid term")


def _validate_course(course):
    if len(course) > 4 or not course.isdigit():
        raise ValueError('Invalid course number')
    elif len(course) == 4:
        return course
    return '0' * (4 - len(course)) + course


def _filter_dictionary(d, keys):
    return dict(
        (k, d[k])
        for k in keys
        if k in d
    )


def _find_item(id_key, data_key):
    def find(data, value):
        for item in data:
            if item[id_key] == value:
                return item[data_key]
        raise LookupError('Unable to find ' + value)

    return find


_find_sections = _find_item('id', 'sections')
_find_course_id_by_instructor = _find_item('instructor', 'id')
_find_course_id_by_section = _find_item('name', 'id')


def _extract_ids(response, course, instructor=None, section=None):
    sections = _find_sections(response.json(), course)
    print(sections)
    if instructor is not None:
        return _find_course_id_by_instructor(sections, instructor)
    elif section is not None:
        return _find_course_id_by_section(sections, section)
    raise ValueError('No instructor or section entered')


def _extract_books(ids):
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


class DefaultDict(dict):
    def __missing__(self, key):
        return None


def _fetch_course(courses, departments):
    for course in courses:
        course = DefaultDict(course)
        yield (
            departments[course['department']],
            course['department'] + _validate_course(course['course']),
            course['instructor'],
            course['section']
        )


def _get_department_number(department_code):
    department_number = CODES.index(department_code) + 22399
    if department_number > 22462:
        department_number += 2  # between codes DSANE and EAS 2 id numbers are skipped.
    if department_number > 22580:
        department_number += 1  # between codes PUBSRV and REHSCI 1 id number is skipped.
    return department_number


def get_textbooks(term, courses):
    departments = {course['department'] for course in courses}
    responses = grequests.map(
        [
            grequests.get(BASE_URL + _construct_query('courses', _get_department_number(department), term), timeout=10)
            for department in departments
        ]
    )
    section_ids = [
        _extract_ids(*course)
        for course in _fetch_course(courses, dict(zip(departments, responses)))
    ]
    return _extract_books(section_ids)


def get_textbook(term, department, course, instructor=None, section=None):
    response = requests.get(BASE_URL + _construct_query('courses', _get_department_number(department), term))
    section_id = _extract_ids(response, department + _validate_course(course), instructor, section)
    return _extract_books([section_id])
