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

import unittest
import responses

from bs4 import BeautifulSoup

from PittAPI import course

TERM = 2001
HEADER_DATA = '<th width="9%">Subject</th><th>Catalog #</th><th>Credits/Units</th>'


class CourseTest(unittest.TestCase):
    def test_get_courses(self):
        self.assertIsInstance(course.get_courses(TERM, 'CS'), list)
        self.assertIsInstance(course.get_courses(TERM, 'BIOSC'), list)

    def test_get_courses_programs_query(self):
        self.assertIsInstance(course.get_courses(TERM, course.PROGRAMS[0]), list)

    def test_get_courses_requirement_query(self):
        self.assertIsInstance(course.get_courses(TERM, course.REQUIREMENTS[0]), list)

    def test_get_courses_day_query(self):
        self.assertIsInstance(course.get_courses(TERM, course.DAY_PROGRAM), list)

    def test_get_courses_sat_query(self):
        self.assertIsInstance(course.get_courses(TERM, course.SAT_PROGRAM), list)

    def test_get_course_invalid_class_number(self):
        self.assertRaises(ValueError, course.get_class, TERM, '0')

    def test_get_course_invalid_subject(self):
        self.assertRaises(ValueError, course.get_courses, TERM, 'AAA')

    def test_get_course_invalid_term(self):
        self.assertRaises(ValueError, course.get_courses, '1', 'CS')
        self.assertRaises(ValueError, course.get_class, '1', '10045')

    def test_get_class(self):
        self.assertIsInstance(course.get_class(TERM, '10045'), dict)

    def test_get_class_invalid_term(self):
        pass

    def test_get_class_invalid_class_number(self):
        pass

    def test_get_subject_query(self):
        pass

    def test_get_subject_query_invalid_code(self):
        pass

    def test_get_subject_query_invalid_term(self):
        pass

    def test_term_validation(self):
        self.assertEqual(course._validate_term(TERM), TERM)

    def test_term_validation_invalid_term(self):
        self.assertRaises(ValueError, course._validate_term, '1')

    def test_retrieve_courses_from_url(self):
        pass

    def test_extract_header(self):
        column_titles = BeautifulSoup(HEADER_DATA, 'lxml').findAll('th')
        self.assertEqual(course._extract_header(column_titles), ['subject', 'catalog_number', 'credits'])

    def test_extract_course_data(self):
        pass
