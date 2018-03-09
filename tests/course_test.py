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

import os
import unittest
import responses

from bs4 import BeautifulSoup

from PittAPI import course

TERM = 2001
SCRIPT_PATH = os.path.dirname(__file__)
HEADER_DATA = '<th width="9%">Subject</th><th>Catalog #</th><th>Credits/Units</th>'


class CourseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        with open(os.path.join(SCRIPT_PATH, 'samples', 'course_cs.html')) as f:
            self.cs_data = ''.join(f.readlines())
        with open(os.path.join(SCRIPT_PATH, 'samples', 'course_class_cs.html')) as f:
            self.cs_class_data = ''.join(f.readlines())

    @responses.activate
    def test_get_classes(self):
        responses.add(responses.GET, 'http://www.courses.as.pitt.edu/results-subja.asp?TERM=2001&SUBJ=CS',
                      body=self.cs_data, status=200)
        self.assertIsInstance(course.get_classes(TERM, 'CS'), list)

    @responses.activate
    def test_get_courses(self):
        responses.add(responses.GET, 'http://www.courses.as.pitt.edu/results-subja.asp?TERM=2001&SUBJ=CS',
                      body=self.cs_data, status=200)
        self.assertIsInstance(course.get_courses(TERM, 'CS'), list)

    def test_get_class_invalid_class_number(self):
        self.assertRaises(ValueError, course.get_class, TERM, '0')

    def test_get_classes_invalid_subject(self):
        self.assertRaises(ValueError, course.get_classes, TERM, 'AAA')

    def test_get_classes_invalid_term(self):
        self.assertRaises(ValueError, course.get_classes, '1', 'CS')

    @responses.activate
    def test_get_class(self):
        responses.add(responses.GET, 'http://www.courses.as.pitt.edu/detail.asp?TERM=2001&CLASSNUM=10001',
                      body=self.cs_class_data, status=200)
        self.assertIsInstance(course.get_class(TERM, '10001'), dict)

    def test_get_class_invalid_term(self):
        self.assertRaises(ValueError, course.get_class, '1', '10045')

    def test_get_subject_query(self):
        self.assertEquals(course._get_subject_query(course.CODES[0], TERM), 'results-subja.asp?TERM=2001&SUBJ=ADMPS')
        self.assertEquals(course._get_subject_query(course.PROGRAMS[0], TERM),
                          'results-subjspeciala.asp?TERM=2001&SUBJ=CLST')
        self.assertEquals(course._get_subject_query(course.REQUIREMENTS[0], TERM),
                          'results-genedreqa.asp?TERM=2001&REQ=G')
        self.assertEquals(course._get_subject_query(course.DAY_PROGRAM, TERM), 'results-dayCGSa.asp?TERM=2001')
        self.assertEquals(course._get_subject_query(course.SAT_PROGRAM, TERM), 'results-satCGSa.asp?TERM=2001')

    def test_get_subject_query_invalid_code(self):
        self.assertRaises(ValueError, course._get_subject_query, 'AAA', TERM)

    def test_get_subject_query_invalid_term(self):
        self.assertRaises(ValueError, course._get_subject_query, course.CODES[0], '0000')

    def test_term_validation(self):
        self.assertEqual(course._validate_term(TERM), TERM)

    def test_term_validation_invalid_term(self):
        self.assertRaises(ValueError, course._validate_term, '1')

    def test_extract_header(self):
        column_titles = BeautifulSoup(HEADER_DATA, 'lxml').findAll('th')
        self.assertEqual(course._extract_header(column_titles), ['subject', 'catalog_number', 'credits'])

    def test_extract_course_data(self):
        pass
