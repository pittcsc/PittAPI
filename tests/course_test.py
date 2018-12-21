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
from unittest.mock import patch

import requests
from PittAPI import course


class CourseTest(unittest.TestCase):
    def test_validate_subject(self):
        for subject in course.SUBJECTS:
            self.assertEqual(course._validate_subject(subject), subject)
        self.assertRaises(ValueError, course._validate_subject, 'TEST')

    def test_validate_term(self):
        # If convert to string
        self.assertTrue(isinstance(course._validate_term(2191), str))

        self.assertEqual(course._validate_term(2191), '2191')
        self.assertEqual(course._validate_term('2191'), '2191')

        self.assertRaises(ValueError, course._validate_term, '214')
        self.assertRaises(ValueError, course._validate_term, '1111')
        self.assertRaises(ValueError, course._validate_term, '12345')

    def test_validate_course(self):
        self.assertEqual(course._validate_course(7), '0007')
        self.assertEqual(course._validate_course(449), '0449')
        self.assertEqual(course._validate_course(1501), '1501')

        self.assertEqual(course._validate_course('7'), '0007')
        self.assertEqual(course._validate_course('0007'), '0007')
        self.assertEqual(course._validate_course('449'), '0449')
        self.assertEqual(course._validate_course('1501'), '1501')

        self.assertRaises(ValueError, course._validate_course, -1)
        self.assertRaises(ValueError, course._validate_course, 0)
        self.assertRaises(ValueError, course._validate_course, '')
        self.assertRaises(ValueError, course._validate_course, 'A00')
        self.assertRaises(ValueError, course._validate_course, 'Hello')
        self.assertRaises(ValueError, course._validate_course, '10000')

    @responses.activate
    def test_get_payload(self):
        TRUE_PAYLOAD = {'CSRFToken': 'abc', 'term': '2194', 'campus': 'PIT', 'subject': 'CS', 'acad_career': '',
                        'catalog_nbr': '1501', 'class_nbr': '27740'}

        class MockSession:
            def __init__(self):
                self.cookies = {'CSRFCookie': 'abc'}

            def get(self, x):
                return None

        with patch('requests.Session') as mock:
            mock.return_value = MockSession()

            payload = course._get_payload('2194', subject='CS', course='1501', section='27740')[-1]
            for k, v in payload.items():
                self.assertEqual(v, TRUE_PAYLOAD[k])


class PittSubjectTest(unittest.TestCase):
    pass


class PittCourseTest(unittest.TestCase):
    pass


class PittSectionTest(unittest.TestCase):
    pass