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
    def test_term_validation(self):
        pass

    def test_validate_course(self):
        pass

    def test_construct_query(self):
        pass

    def test_find_item(self):
        pass

    def test_extract_ids(self):
        pass


@unittest.skipIf(len(TERM) == 0, 'Wasn\'t able to fetch correct terms to test with.')
class TextbookAPITest(unittest.TestCase):
    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_textbook_get_textbooks(self):
        ans = textbook.get_textbooks(
            term=TERM,
            courses=[
                {'department': 'CHEM', 'course': '120', 'instructor': 'FORTNEY'},
                {'department': 'CS', 'course': '445', 'instructor': 'GARRISON III'}])
        self.assertIsInstance(ans, list)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_textbook_get_books_data_many(self):
        ans = textbook.get_textbooks(
            term=TERM,
            courses=[
                {'department': 'MATH', 'course': '240', 'instructor': 'SYSOEVA'},
                {'department': 'CS', 'course': '445', 'instructor': 'GARRISON III'},
                {'department': 'CHEM', 'course': '120', 'instructor': 'FORTNEY'},
                {'department': 'STAT', 'course': '1000', 'instructor': 'NELSON'}])
        self.assertIsInstance(ans, list)

    @unittest.skip
    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_invalid_department_code(self):
        self.assertRaises(ValueError, textbook.get_textbook, TERM, 'TEST', 'Not', 'EXIST', None)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_invalid_course_name(self):
        self.assertRaises(ValueError, textbook.get_textbook, TERM, 'CS', 'Not', 'EXIST', None)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_invalid_instructor(self):
        self.assertRaises(ValueError, textbook.get_textbook, TERM, 'CS', '447', 'EXIST', None)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_invalid_section(self):
        self.assertRaises(ValueError, textbook.get_textbook, TERM, 'CS', '401',  None, '1060')