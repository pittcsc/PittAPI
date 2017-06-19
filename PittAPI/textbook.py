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

# Future change to be implemented
from . import departments

session = requests.session()

# TODO(Alex Z.): Look into instructor names and whether they are useful
# TODO: Possibly make conversion between textbook term numbers and course term numbers
BASE_URL = 'http://pitt.verbacompare.com/'


def _fetch_term_codes():
    """Fetches current valid term codes"""
    try:
        page = requests.get(BASE_URL)
    except ConnectionError:
        return []
    script = BeautifulSoup(page.text, 'lxml').findAll('script')[-2].text
    data = json.loads(script[script.find('['):script.find(']') + 1])
    terms = [
        item['id']
        for item in data
    ]
    return terms


TERMS = _fetch_term_codes()


def _validate_term(term):
    """Validates term is a string and check if it is valid."""
    if len(TERMS) == 0:
        warnings.warn('Wasn\'t able to validate term. Assuming term code is valid.')
        return term
    if term in TERMS:
        return term
    raise ValueError("Invalid term")


def connection_exception(request, exception):
    pass


def get_books_data(courses_info):
    """Returns list of dictionaries of book information."""
    request_objs = []
    course_names = []  # need to save these
    instructors = []  # need to save these

    # TODO(Alex Z.): Validation that argument is a list, add warning and correction is not or raise exception
    for book_info in courses_info:
        # TODO(Alex Z.): Check what information is actually needed

        course_names.append(book_info['course_name'])
        instructors.append(book_info['instructor'])

        request_objs.append(
            grequests.get(
                _get_department_url(book_info['department_code'], book_info['term']),
                timeout=10
            )
        )

    responses = grequests.map(request_objs, exception_handler=connection_exception)  # parallel requests
    bundle = list(zip(responses, course_names, instructors))

    course_ids = _extract_course_ids(bundle)
    book_data = session.get(_construct_url(course_ids)).text

    return _extract_books(book_data)  # return list of dicts of books


def _construct_url(ids):
    return BASE_URL + 'comparison?id=' + '%2C'.join(ids)


def _extract_course_ids(bundle):
    ids = [
        _extract_course_id(
            sections=_extract_sections(
                response=response,
                course=course),
            instructor=instructor
        )
        for response, course, instructor in bundle
    ]
    return ids


def _extract_sections(response, course):
    for course_dict in response.json():
        if course_dict['id'] == course:
            sections = course_dict['sections']
            return sections


def _extract_course_id(sections, instructor):
    for section in sections:
        if section['instructor'] == instructor:
            course_id = section['id']
            return course_id


def _extract_books(data):
    keys = ['isbn', 'citation', 'title', 'edition', 'author']
    # TODO(Alex Z.): Added check for invalid response that return an empty json list
    start, end = data.find('Verba.Compare.Collections.Sections') + 35, data.find('}]}]);') + 4
    info = [json.loads(data[start:end])][0]  # TODO(Alex Z.) Look into whether it's needed to choose the first index
    books = [
        _filter_dictionary(book, keys)
        for data in info
        for book in data['books']
    ]
    return books


def _filter_dictionary(d, keys):
    return dict(
        (k, d[k])
        for k in keys
        if k in d
    )


def _get_department_url(department_code, term):
    """Returns url for given department code."""
    query = 'compare/courses/?id={}&term_id={}'.format(
        departments[department_code]['textbook'],
        _validate_term(term)
    )
    return BASE_URL + query
