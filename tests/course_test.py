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
import unittest
import responses
from unittest.mock import patch

from pathlib import Path

from pittapi import course, course_helper

SAMPLE_PATH = Path.cwd() / 'tests' / 'samples'


class RequestText:
    def __init__(self, text):
        self.text = text


class MockSession:

    def __init__(self, text=None):
        self.cookies = {'CSRFCookie': 'abc'}
        self.text = text

    def get(self, x):
        return None

    def post(self, *args, **kwargs):
        return RequestText(self.text)


class CourseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        with (SAMPLE_PATH / 'course_subject.html').open() as f:
            self.cs_subject_data = ''.join(f.readlines())
        with (SAMPLE_PATH / 'course_course.html').open() as f:
            self.cs_course_data = ''.join(f.readlines())
        with (SAMPLE_PATH / 'course_section.html').open() as f:
            self.cs_section_data = ''.join(f.readlines())
        with (SAMPLE_PATH / 'course_extra_1.html').open() as f:
            self.cs_extra_data_1 = ''.join(f.readlines())
        with (SAMPLE_PATH / 'course_extra_2.html').open() as f:
            self.cs_extra_data_2 = ''.join(f.readlines())
        with (SAMPLE_PATH / 'course_extra_3.html').open() as f:
            self.cs_extra_data_3 = ''.join(f.readlines())
        with (SAMPLE_PATH / 'course_extra_4.html').open() as f:
            self.cs_extra_data_4 = ''.join(f.readlines())

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

    def test_get_payload(self):
        TRUE_PAYLOAD = {'CSRFToken': 'abc', 'term': '2194', 'campus': 'PIT', 'subject': 'CS', 'acad_career': '',
                        'catalog_nbr': '1501', 'class_nbr': '27740'}
        with patch('requests.Session') as mock:
            mock.return_value = MockSession()

            payload = course._get_payload('2194', subject='CS', course='1501', section='27740')[-1]
            for k, v in payload.items():
                self.assertEqual(v, TRUE_PAYLOAD[k])

    def test_get_term_courses(self):
        with patch('requests.Session') as mock:
            mock.return_value = MockSession(self.cs_subject_data)
            cs_subject = course.get_courses('2194', 'CS')
            self.assertTrue('0004' in cs_subject.courses)
            self.assertTrue(cs_subject['0004'].number in cs_subject.courses)

            self.assertRaises(ValueError, cs_subject.__getitem__, '1111')
            self.assertRaises(ValueError, cs_subject.__getitem__, 4)

            self.assertIsInstance(cs_subject.to_dict(), dict)
            self.assertEqual(repr(cs_subject), json.dumps(cs_subject.to_dict()))
            for absolute in ['0004', '0007']:
                self.assertTrue(absolute in cs_subject.courses)
            self.assertEqual(str(cs_subject), 'PittSubject(2194, CS)')

    def test_get_term_courses_parent(self):
        with patch('requests.Session') as mock:
            mock.return_value = MockSession(self.cs_subject_data)
            cs_subject = course.get_courses('2194', 'CS')
            self.assertEqual(cs_subject['0004'].term, '2194')
            self.assertEqual(cs_subject['0004'].subject, 'CS')
            self.assertEqual(cs_subject['0004'][0].term, '2194')
            self.assertEqual(cs_subject['0004'][0].subject, 'CS')

    def test_get_course_sections(self):
        with patch('requests.Session') as mock:
            mock.return_value = MockSession(self.cs_course_data)
            cs_course = course.get_course_sections('2194', 'CS', '0007')
            self.assertEqual(cs_course.number, '0007')
            self.assertEqual(cs_course.term, '2194')
            self.assertEqual(cs_course.subject, 'CS')

            self.assertEqual(cs_course[0], cs_course.sections[0])
            self.assertEqual(len(cs_course[0:2]), 2)
            self.assertEqual(cs_course[0].course_number, cs_course.number)
            self.assertEqual(cs_course[0].course_title, cs_course.title)
            self.assertEqual(str(cs_course), 'PittCourse(2194, CS, 0007)')
            self.assertEqual(repr(cs_course), json.dumps(cs_course.to_dict()))

    @responses.activate
    def test_get_section_details_improper_section_type(self):
        responses.add(responses.GET, 'https://psmobile.pitt.edu/app/catalog/classsection/UPITT/2194/27469',
                      body=self.cs_extra_data_1, status=200)
        with patch('requests.Session') as mock:
            mock.return_value = MockSession(self.cs_section_data)
            cs_section = course.get_section_details('2194', 27469)
            self.assertEqual(cs_section.instructor, 'William Laboon')
            self.assertEqual(str(cs_section), 'PittSection(CS, 1632, LEC, 27469, William Laboon)')

    @responses.activate
    def test_get_section_details_no_class_attribute(self):
        responses.add(responses.GET, 'https://psmobile.pitt.edu/app/catalog/classsection/UPITT/2194/27469',
                      body=self.cs_extra_data_1, status=200)
        with patch('requests.Session') as mock:
            mock.return_value = MockSession(self.cs_section_data)
            cs_section = course.get_section_details('2194', '27469')
            self.assertEqual(cs_section.instructor, 'William Laboon')
            self.assertEqual(str(cs_section), 'PittSection(CS, 1632, LEC, 27469, William Laboon)')

            self.assertIsInstance(cs_section.extra_details, dict)
            self.assertIsInstance(cs_section.extra_details, dict)

    @responses.activate
    def test_get_section_details(self):
        responses.add(responses.GET, 'https://psmobile.pitt.edu/app/catalog/classsection/UPITT/2194/27469',
                      body=self.cs_extra_data_2, status=200)
        with patch('requests.Session') as mock:
            mock.return_value = MockSession(self.cs_section_data)
            cs_section = course.get_section_details('2194', '27469')
            self.assertEqual(cs_section.instructor, 'William Laboon')
            self.assertEqual(str(cs_section), 'PittSection(CS, 1632, LEC, 27469, William Laboon)')

            self.assertEqual(cs_section.term, '2194')
            self.assertEqual(cs_section.subject, 'CS')
            self.assertEqual(cs_section.course_number, '1632')
            self.assertEqual(cs_section.course_title, 'SOFTWARE QUALITY ASSURANCE')
            self.assertEqual(repr(cs_section), json.dumps(cs_section.to_dict()))

            self.assertIsInstance(cs_section.extra_details, dict)
            self.assertIsInstance(cs_section.extra_details, dict)

            self.assertIsInstance(cs_section.to_dict(), dict)
            self.assertIsInstance(cs_section.to_dict(extra_details=True), dict)

    @responses.activate
    def test_get_section_details_extra_details(self):
        responses.add(responses.GET, 'https://psmobile.pitt.edu/app/catalog/classsection/UPITT/2194/27469',
                      body=self.cs_extra_data_3, status=200)
        with patch('requests.Session') as mock:
            mock.return_value = MockSession(self.cs_section_data)
            cs_section = course.get_section_details('2194', '27469')
            self.assertIsInstance(cs_section.extra_details, dict)
            self.assertIsInstance(cs_section.extra_details, dict)

    @responses.activate
    def test_get_section_details_basic_extra_details(self):
        responses.add(responses.GET, 'https://psmobile.pitt.edu/app/catalog/classsection/UPITT/2194/27469',
                      body=self.cs_extra_data_4, status=200)
        with patch('requests.Session') as mock:
            mock.return_value = MockSession(self.cs_section_data)
            cs_section = course.get_section_details('2194', '27469')
            self.assertIsInstance(cs_section.extra_details, dict)
            self.assertIsInstance(cs_section.extra_details, dict)