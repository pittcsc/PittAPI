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
import unittest

import timeout_decorator

from PittAPI import course
from . import PittServerError, DEFAULT_TIMEOUT

TERM = '2177'
HEADER_DATA = ['<th width="9%">Subject</th>', '<th>Catalog #</th>', '<th>Credits/Units</th>']


class CourseTest(unittest.TestCase):
    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_get_courses(self):
        self.assertIsInstance(course.get_courses(TERM, 'CS'), list)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_get_courses_subject_query(self):
        self.assertIsInstance(course.get_courses(TERM, 'BIOSC'), list)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_get_courses_programs_query(self):
        self.assertIsInstance(course.get_courses(TERM, course.PROGRAMS[0]), list)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_get_courses_requirement_query(self):
        self.assertIsInstance(course.get_courses(TERM, course.REQUIREMENTS[0]), list)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_get_class_description(self):
        self.assertIsInstance(course.get_class_description(TERM, '10045'), str)


    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_invalid_subject(self):
        self.assertRaises(ValueError, course.get_courses, TERM, 'AAA')

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_invalid_term(self):
        self.assertRaises(ValueError, course.get_courses, '1', 'CS')

    def test_term_validation(self):
        # Test valid term
        self.assertEqual(course._validate_term('1', valid_terms=['1']), '1')
        # Test incorrect type of term
        self.assertEqual(course._validate_term(1, valid_terms=['1']), '1')
        # Test invalid term
        self.assertRaises(ValueError, course._validate_term, '2', valid_terms=['1'])

    def test_column_header_extraction(self):
        # column_titles = BeautifulSoup(HEADER_DATA, 'lxml')
        # self.assertEqual(course._extract_header(column_titles[0]), ['subject'])
        # self.assertEqual(course._extract_header(column_titles[1]), ['catalog_number'])
        # self.assertEqual(course._extract_header(column_titles[2]), ['credits'])
        # self.assertEqual(course._extract_header(column_titles), ['subject', 'catalog_number', 'credits'])
        pass
