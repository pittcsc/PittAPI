import unittest
import timeout_decorator

from PittAPI import textbook


class PittServerDownException(Exception):
    """Raise when a Pitt server is down or timing out"""


class TextbookTest(unittest.TestCase):
    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_textbook_get_books_data(self):
        ans = textbook.get_books_data([{'department_code': 'CHEM', 'course_name': 'CHEM0120', 'instructor': 'FORTNEY', 'term': '2600'}, {'department_code': 'CS', 'course_name': 'CS0445', 'instructor': 'GARRISON III','term': '2600'}])
        self.assertIsInstance(ans, list)
        self.assertTrue(len(ans) == 6)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_textbook_get_books_data_past_22462(self):
        ans = textbook.get_books_data([{'department_code': 'MATH', 'course_name': 'MATH0220', 'instructor': 'HOCKENSMITH', 'term': '2600'}])
        self.assertIsInstance(ans, list)
        self.assertTrue(len(ans) == 2)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_invalid_department_code(self):
        self.assertRaises(ValueError, textbook.get_books_data, [{'department_code': 'DOES', 'course_name': 'NOT', 'instructor': 'EXIST', 'term': '2600'}])

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_invalid_course_name(self):
        self.assertRaises(ValueError, textbook.get_books_data, [{'department_code': 'CS', 'course_name': 'NOT', 'instructor': 'EXIST', 'term': '2600'}])

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_invalid_instructor(self):
        self.assertRaises(ValueError, textbook.get_books_data, [{'department_code': 'CS', 'course_name': 'CS0447', 'instructor': 'EXIST', 'term': '2600'}])
