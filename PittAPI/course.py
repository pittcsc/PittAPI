'''
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
'''

import requests
from bs4 import BeautifulSoup, SoupStrainer
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from PittAPI import SUBJECTS, HONORS, PROGRAMS, ONLINE_PROGRAMS, OFF_CAMPUS, REQUIREMENTS

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

strainer = SoupStrainer(['table', 'tr', 'th'])

URL = 'http://www.courses.as.pitt.edu/'

def get_courses(term, subject):
    """Returns a list of dictionaries containing the data for all a subjects classes in a term"""
    col_headers, courses = _retrieve_courses_from_url(URL + _get_query(subject, term))
    return [_extract_course_data(col_headers, course) for course in courses]


def get_courses_by_req(term, req):
    """Returns a list of dictionaries containing the data for all SUBJECT classes in TERM"""

    page = requests.get(URL + _get_query(req, term))
    soup = BeautifulSoup(page.text, 'lxml', parse_only=strainer)
    courses = soup.findAll("tr", {"class": "odd"})
    courses_even = soup.findAll("tr", {"class": "even"})
    courses.extend(courses_even)

    course_details = []

    for course in courses:
        temp = []
        for i in course:
            try:
                if len(i.string.strip()) > 2:
                    temp.append(i.string.strip())
            except (TypeError, AttributeError) as e:
                pass

        temp = [x.replace('&nbsp;', '') for x in temp]

        if len(temp) == 6:
            course_details.append(
                {
                    'subject': temp[0].strip(),
                    'catalog_number': temp[1].strip(),
                    'term': temp[2].replace('\r\n\t', ' '),
                    'title': temp[3].strip(),
                    'instructor': 'Not decided' if len(temp[4].strip()) == 0 else temp[4].strip(),
                    'credits': temp[5].strip()
                }
            )
        else:
            course_details.append(
                {
                    'subject': 'Not available',
                    'catalog_number': temp[0].strip(),
                    'term': temp[1].strip().replace('\r\n\t', ' '),
                    'title': temp[2].replace('\r\n\t', ' '),
                    'instructor': 'Not decided' if len(temp[3].strip()) == 0 else temp[3].strip(),
                    'credits': temp[4].strip() if len(temp) == 5 else -1
                }
            )

    if len(course_details) == 0:
        raise ValueError("The TERM or REQ is invalid")

    return course_details


def get_class_description(term, class_number):
    """Return a string that is the description for class in a term"""

    url = 'http://www.courses.as.pitt.edu/detail.asp?CLASSNUM={}&TERM={}'.format(class_number, term)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml', parse_only=strainer)
    table = soup.findChildren('table')[0]
    rows = table.findChildren('tr')

    has_description = False
    for row in rows:
        cells = row.findChildren('td')
        for cell in cells:
            if has_description:
                return cell.string.strip()
            if len(cell.contents) > 0 and str(cell.contents[0]) == '<strong>Description</strong>':
                has_description = True


def _get_query(code, term):
    code = code.upper()
    if code in SUBJECTS + HONORS + ONLINE_PROGRAMS:
        return 'results-subja.asp?TERM={}&SUBJ={}'.format(term, code)
    elif code in PROGRAMS:
        return 'results-subjspeciala.asp?TERM={}&SUBJ={}'.format(term, code)
    elif code in OFF_CAMPUS:
        return 'results-offcamp.asp?TERM={}&CAMP={}'.format(term, code)
    elif code in REQUIREMENTS:
        return 'results-genedreqa.asp?TERM={}&REQ={}'.format(term, code)
    else:
        raise ValueError("Invalid subject")


def _extract_course_data(header, course):
    """Constructs a dictionary from column header labels(subject, class number, etc.) and course data."""
    data = {}
    for item, value in zip(header, course.findAll('td')):
        data[item] = value.text.strip().replace('\r\n\t', '')
        if not data[item]:
            data[item] = 'Not Decided'
    return data


def _extract_header(data):
    """Extracts table header and converts into keys for future dictionary"""
    header = []
    for tag in data:
        key = tag.text.strip().lower()
        key = key.replace(' ', '').replace('#', '_number')
        if key.find('/') != - 1:
            key = key[:key.index('/')]
        header.append(key)
    return header


def _retrieve_courses_from_url(url):
    """Returns a tuple of column header keys and list of course data"""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml', parse_only=strainer)
    header = _extract_header(soup.findAll('th'))
    courses = soup.findAll("tr", {"class": "odd"}) \
        + soup.findAll("tr", {"class": "even"})
    return header, courses
