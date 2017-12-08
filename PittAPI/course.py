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
51 /Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
import warnings

import requests
import re
from typing import Any, Dict, List, Tuple
from bs4 import BeautifulSoup, SoupStrainer, Tag, ResultSet

URL = 'http://www.courses.as.pitt.edu/'

CODES = [
    'ADMPS', 'AFRCNA', 'ANTH', 'ARABIC', 'ASL', 'ARTSC', 'ASTRON', 'BIOETH', 'BIOSC', 'CHEM', 'CHLIT', 'CHIN', 'CLASS',
    'COMMRC', 'CS', 'EAS', 'ECON', 'ENGCMP', 'ENGFLM', 'ENGLIT', 'ENGWRT', 'FP', 'FR', 'FTDA', 'FTDB', 'FTDC', 'GEOL',
    'GER', 'GREEK', 'GREEKM', 'HINDI', 'HIST', 'HPS', 'HAA', 'ISSP', 'IRISH', 'ITAL', 'JPNSE', 'JS', 'KOREAN', 'LATIN',
    'LCTL', 'LING', 'MATH', 'MUSIC', 'NROSCI', 'PERS', 'PHIL', 'PEDC', 'PHYS', 'POLISH', 'PS', 'PORT', 'PSY', 'QUECH',
    'REL', 'RELGST', 'RUSS', 'SERCRO', 'SLAV', 'SLOVAK', 'SOC', 'SPAN', 'STAT', 'SA', 'SWAHIL', 'SWE', 'THEA', 'TURKSH',
    'UKRAIN', 'VIET', 'BUSACC', 'BUSECN', 'BUSENV', 'BUSFIN', 'BUSHRM', 'BUSBIS', 'BUSMIS', 'BUSMKT', 'BUSORG',
    'BUSQOM', 'BUSERV', 'BUSSPP', 'BUSSCM', 'ADMJ', 'BUSERV', 'CDACCT', 'CGS', 'LDRSHP', 'LEGLST', 'NPHS', 'PUBSRV',
    'AFROTC', 'INFSCI', 'MILS', 'BIOENG', 'CEE', 'CHE', 'COE', 'COEE', 'ECE', 'EE', 'ENGR', 'ENGRPH', 'ENRES', 'FTDH',
    'IE', 'ME', 'MEMS', 'MSE', 'MSEP', 'PETE', 'PWEA', 'WWW', 'HYBRID', 'UHC', 'BCCC']
REQUIREMENTS = ['G', 'W', 'Q', 'LIT', 'MA', 'EX', 'PH', 'SS', 'HS', 'NS', 'L', 'IF', 'IFN', 'I', 'A']
PROGRAMS = ['CLST', 'ENV', 'FILMST', 'MRST', 'URBNST', 'SELF', 'GSWS']
DAY_PROGRAM, SAT_PROGRAM = 'CGSDAY', 'CGSSAT'


def get_classes(term: str, code: str) -> List[Dict[str, str]]:
    """Returns a list of dictionaries containing all classes queried from code."""
    col_headers, course_data = _retrieve_courses_from_url(
        url=URL + _get_subject_query(code, term)
    )
    courses = [_extract_course_data(col_headers, course) for course in course_data]
    return courses


def get_courses(term: str, code: str) -> List[Dict[str,str]]:
    """Returns a list of dictionaries containing all class queried from code.
    This is now deprecated since the name of the function doesn't accurately reflect
    the data returned. Functionality will still be maintained till until a newer version
    of the API."""
    warnings.warn("Warning get_courses() is deprecated, please use get_classes() instead.")
    return get_classes(term, code)


def _get_subject_query(code: str, term: str) -> str:
    """Builds query based on code entered."""
    code, term = code.upper(), _validate_term(term)
    if code in CODES:
        return 'results-subja.asp?TERM={}&SUBJ={}'.format(term, code)
    elif code in PROGRAMS:
        return 'results-subjspeciala.asp?TERM={}&SUBJ={}'.format(term, code)
    elif code in REQUIREMENTS:
        return 'results-genedreqa.asp?TERM={}&REQ={}'.format(term, code)
    elif code in DAY_PROGRAM:
        return 'results-dayCGSa.asp?TERM={}'.format(term)
    elif code in SAT_PROGRAM:
        return 'results-satCGSa.asp?TERM={}'.format(term)
    raise ValueError("Invalid subject")


def _validate_term(term: str) -> str:
    """Validates term is a string and check if it is valid."""

    valid_terms = re.compile('2\d\d[147]')
    if valid_terms.match(str(term)):
        return term
    raise ValueError("Invalid term")


def _retrieve_courses_from_url(url: str) -> Tuple[List[str],ResultSet]:
    """Returns a tuple of column header keys and list of course data."""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml', parse_only=SoupStrainer(['table', 'tr', 'th']))
    courses = _extract_header(soup.findAll('th')), soup.findAll("tr", {"class": ["odd", "even"]})
    return courses


def _extract_header(data: List[Any]) -> List[str]:
    """Extracts column headers and converts it into keys for a future dictionary."""
    header = []
    for tag in data:
        key = tag.text.strip().lower() \
            .replace(' ', '').replace('#', '_number')
        if key.find('/') != - 1:
            key = key[:key.index('/')]
        header.append(key)
    return header


def _extract_course_data(header: List[str], course: Tag) -> Dict[str,str]:
    """Constructs a dictionary from column header labels(subject, class number, etc.) and course data."""
    data = {}
    for item, value in zip(header, course.findAll('td')):
        data[item] = value.text.strip().translate({'\r': '', '\n': '', '\t': ''}).replace('\xa0', '')
        if not data[item]:
            data[item] = 'Not Decided'
        print(data[item])
    try:
        # TODO(azharichenko): Look into why there is an empty column header
        del data['']
    finally:
        return data


def get_class(term: str, class_number: str) -> Dict[str,Any]:
    """Returns dictionary of details about a class."""
    payload = {
        'TERM': _validate_term(term),
        'CLASSNUM': class_number
    }
    page = requests.get(URL + 'detail.asp', params=payload)

    if 'no courses by' in page.text or 'Search by subject' in page.text:
        raise ValueError('Invalid class number.')

    class_details = dict(_extract_description(page.text), **_extract_details(page.text))
    return dict(class_details, **{'class_number': class_number, 'term': term})


def _extract_description(text: str) -> Dict[str,str]:
    """Extracts class description from web page"""
    soup = BeautifulSoup(text, 'lxml', parse_only=SoupStrainer(['td']))
    description = {
        'description': soup.findAll('td', {'colspan': '9'})[1].text.replace('\r\n', '')
    }

    return description


def _extract_details(text: str) -> Dict[str,Any]:
    """Extracts class number, classroom, section, date, and time from web page"""
    soup = BeautifulSoup(text, 'lxml', parse_only=SoupStrainer(['td']))
    row = soup.findAll('td', {'class': 'style1'})
    section = row[1]
    details = row[2]
    special_indicators = row[4]
    enroll_limit = row[7]
    instructor = row[8]
    days, time, classroom = details.text.split(' / ')
    return {
        'section': section.text.strip(),
        'days': days,
        'time': time.split('-'),
        'classroom': classroom.replace('\xa0', ' '),
        'special_indicators': special_indicators.text.split(),
        'enroll_limit': enroll_limit.text.strip(),
        'instructor': instructor.text.strip()
    }
