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
from . import PittServerError


class CourseTest(unittest.TestCase):
    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_get_courses(self):
        self.assertIsInstance(course.get_courses('2177', 'CS'), list)

    @timeout_decorator.timeout(60, timeout_exception=PittServerError)
    def test_get_courses_subject_query(self):
        term = '2177'
        subjects = ['CS', 'BIOSC', 'ECON']

        for subject in subjects:
            try:
                results = course.get_courses(term, subject)
                self.assertIsInstance(results, list)
            except ValueError:
                self.fail(msg='Term {} and/or Subject {} is not valid.'.format(term, subject))

            for result in results:
                self.assertIn(term, result['term'])
                self.assertIn(subject, result['subject'])

    @timeout_decorator.timeout(60, timeout_exception=PittServerError)
    def test_get_courses_programs_query(self):
        term = '2177'
        programs = ['CLST', 'ENV', 'FILMST']

        for program in programs:
            try:
                self.assertIsInstance(course.get_courses(term, program), list)
            except ValueError:
                self.fail(msg='Term {} and/or Program {} is not valid.'.format(term, program))


    @timeout_decorator.timeout(60, timeout_exception=PittServerError)
    def test_get_courses_off_campus_query(self):
        term = '2177'
        off_camp = ['BCCC']

        for campus in off_camp:
            try:
                self.assertIsInstance(course.get_courses(term, campus), list)
            except ValueError:
                self.fail(msg='Term {} and/or Campus {} is not valid.'.format(term, campus))

    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_get_courses_by_req(self):
        self.assertIsInstance(course.get_courses_by_req('2177', 'Q'), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_get_class_description(self):
        self.assertIsInstance(course.get_class_description('2177', '10045'), str)

    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_invalid_subject(self):
        test_term, test_subjects = '2177', ['AAA', 'BBB', 'CCC']
        for subject in test_subjects:
            self.assertRaises(ValueError, course.get_courses, test_term, subject)
