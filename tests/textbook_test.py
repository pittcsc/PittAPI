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

from PittAPI import textbook
from . import PittServerError, DEFAULT_TIMEOUT


TERM = textbook.TERMS[0]

class TextbookTest(unittest.TestCase):
    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_textbook_get_books_data(self):
        ans = textbook.get_books_data([
        {'department_code': 'CHEM', 'course_name': 'CHEM0120', 'instructor': 'FORTNEY', 'term': TERM},
        {'department_code': 'CS', 'course_name': 'CS0445', 'instructor': 'GARRISON III','term': TERM}])
        self.assertIsInstance(ans, list)
        self.assertTrue(len(ans) == 6)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_textbook_get_books_data_past_22462(self):
        ans = textbook.get_books_data({'department_code': 'MATH', 'course_name': 'MATH0240', 'instructor': 'SYSOEVA', 'term': '2600'})
        self.assertIsInstance(ans, list)
        self.assertTrue(len(ans) == 2)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_textbook_get_books_data_many(self):
        ans = textbook.get_books_data([
        {'department_code': 'MATH', 'course_name': 'MATH0240', 'instructor': 'SYSOEVA', 'term': TERM},
        {'department_code': 'CS', 'course_name': 'CS0445', 'instructor': 'GARRISON III','term': TERM},
        {'department_code': 'CHEM', 'course_name': 'CHEM0120', 'instructor': 'FORTNEY', 'term': TERM},
        {'department_code': 'STAT', 'course_name': 'STAT1000', 'instructor': 'NELSON', 'term': TERM}])
        print(len(ans))
        self.assertIsInstance(ans, list)
        self.assertTrue(len(ans) == 9)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_invalid_department_code(self):
        self.assertRaises(ValueError, textbook.get_books_data, {'department_code': 'DOES', 'course_name': 'NOT', 'instructor': 'EXIST', 'term': TERM})

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_invalid_course_name(self):
        self.assertRaises(ValueError, textbook.get_books_data, {'department_code': 'CS', 'course_name': 'NOT', 'instructor': 'EXIST', 'term': TERM})

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_invalid_instructor(self):
        self.assertRaises(ValueError, textbook.get_books_data, {'department_code': 'CS', 'course_name': 'CS0447', 'instructor': 'EXIST', 'term': TERM})
