import unittest
import timeout_decorator

from PittAPI import textbook


class PittServerDownException(Exception):
    """Raise when a Pitt server is down or timing out"""


class TextbookTest(unittest.TestCase):
    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_textbook_get_books_data(self):
        ans = textbook.get_books_data([{'department_code': 'CHEM', 'course_name': 'CHEM0120', 'instructor': 'FORTNEY'}, {'department_code': 'CS', 'course_name': 'CS0445', 'instructor': 'GARRISON III'}])
        self.assertIsInstance(ans, list)
        self.assertTrue(len(ans) == 6)
        ans = textbook.get_books_data([{'department_code': 'MATH', 'course_name': 'MATH0220', 'instructor': 'HOCKENSMITH'}])
        self.assertIsInstance(ans, list)
        self.assertTrue(len(ans) == 2)
