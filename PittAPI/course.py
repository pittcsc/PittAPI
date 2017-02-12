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

from PittAPI import SUBJECTS, HONORS, PROGRAMS, ONLINE_PROGRAMS, OFF_CAMPUS

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

strainer = SoupStrainer(['table', 'tr'])


def get_courses(term, subject):
    """Returns a list of dictionaries containing the data for all a subjects classes in a term"""
    subject = subject.upper()
    url = 'http://www.courses.as.pitt.edu/'

    if subject in SUBJECTS + HONORS + ONLINE_PROGRAMS:
        url += 'results-subja.asp?TERM={}&SUBJ={}'.format(term, subject)
    elif subject in PROGRAMS:
        url += 'results-subjspeciala.asp?TERM={}&SUBJ={}'.format(term, subject)
    elif subject in OFF_CAMPUS:
        url += '/results-offcamp.asp?TERM={}&CAMP={}'.format(term, subject)
    else:
        raise ValueError("Invalid subject")

    courses = _retrieve_courses_from_url(url)

    course_details = []

    for course in courses:
        details = [course_detail.string.replace('&nbsp;', '').strip()
                   for course_detail in course
                   if course_detail.string is not None]

        # Only append details if the list is not empty
        # If the subject code is incorrect, details will be NoneType
        if details:
            course_details.append(
                {
                    'subject': details[1] if details[1] else "Not Decided",
                    'catalog_number': details[3] if details[3] else "Not Decided",
                    'term': details[5].replace('\r\n\t', '') if details[5] else "Not Decided",
                    'class_number': course.find('a').contents[0] if course.find('a').contents[0] else "Not Decided",
                    'title': details[8] if details[8] else "Not Decided",
                    'instructor': details[10] if details[10] else "Not Decided",
                    'credits': details[12] if details[12] else "Not Decided"
                }
            )

    return course_details


def get_courses_by_req(term, req):
    """Returns a list of dictionaries containing the data for all SUBJECT classes in TERM"""

    req = req.upper()

    url = 'http://www.courses.as.pitt.edu/results-genedreqa.asp?REQ={}&TERM={}'.format(req, term)
    page = requests.get(url)
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


def _retrieve_courses_from_url(url):
    """Returns a list of all classes from and html table given a url"""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml', parse_only=strainer)
    courses = soup.findAll("tr", {"class": "odd"}) \
        + soup.findAll("tr", {"class": "even"})
    return courses
