import unittest
import timeout_decorator

from PittAPI import textbook
from . import PittServerError, DEFAULT_TIMEOUT

try:
    TERM = textbook.TERMS[0]
except IndexError:
    TERM = ''

@unittest.skip
class TextbookTest(unittest.TestCase):
    def test_term_validation(self):
        validate = textbook._validate_term

        if len(TERM) != 0:
            self.assertEqual(validate(TERM), TERM)
        else:
            self.assertEqual(validate('2000'), '2000')
            self.assertRaises(ValueError, validate, '1')
            self.assertRaises(ValueError, validate, 'a')

        self.assertRaises(ValueError, validate, '100')

    def test_validate_course(self):
        validate = textbook._validate_course

        # Testing correct input
        self.assertEqual(validate('0000'), '0000')
        self.assertEqual(validate('1234'), '1234')

        # Testing improper input
        self.assertEqual(validate('1'), '0001')
        self.assertEqual(validate('12'), '0012')
        self.assertEqual(validate('123'), '0123')

        # Testing incorrect input
        self.assertRaises(ValueError, validate, '00000')
        self.assertRaises(ValueError, validate, '11111')
        self.assertRaises(ValueError, validate, 'hi')

    def test_construct_query(self):
        construct = textbook._construct_query
        course_query = 'compare/courses/?id=9999&term_id=1111'
        book_query = 'compare/books?id=9999'

        self.assertEqual(construct('courses', '9999', '1111'), course_query)
        self.assertEqual(construct('books', '9999'), book_query)

    def test_find_item(self):
        find = textbook._find_item('id', 'key', 'test')
        test_data = [
            {'id': 1, 'key': 1},
            {'id': 2, 'key': 4},
            {'id': 3, 'key': 9},
            {'id': 4, 'key': 16},
            {'id': 5, 'key': 25}
        ]

        for i in range(1, 6):
            self.assertEqual(find(test_data, i), i ** 2)

        self.assertRaises(LookupError, find, test_data, 6)

    def test_get_textbook(self):
        self.assertRaises(TypeError, textbook.get_textbook, '0000', 'CS', '401')

@unittest.skip
@unittest.skipIf(len(TERM) == 0, 'Wasn\'t able to fetch correct terms to test with.')
class TextbookAPITest(unittest.TestCase):
    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_textbook_get_textbook(self):
        instructor_test = textbook.get_textbook(
            term=TERM,
            department='CS',
            course='445',
            instructor='GARRISON III'
        )

        section_test = textbook.get_textbook(
            term=TERM,
            department='CS',
            course='445',
            section='1010'
        )
        self.assertIsInstance(instructor_test, list)
        self.assertIsInstance(section_test, list)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_textbook_get_textbooks(self):
        multi_book_test = textbook.get_textbooks(
            term=TERM,
            courses=[
                {'department': 'CS', 'course': '445', 'section': '1010'},
                {'department': 'STAT', 'course': '1000', 'instructor': 'YANG'}])
        self.assertIsInstance(multi_book_test, list)

    @unittest.skip
    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_invalid_department_code(self):
        self.assertRaises(ValueError, textbook.get_textbook, TERM, 'TEST', '000', 'EXIST', None)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_invalid_course_name(self):
        self.assertRaises(LookupError, textbook.get_textbook, TERM, 'CS', '000', 'EXIST', None)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_invalid_instructor(self):
        self.assertRaises(LookupError, textbook.get_textbook, TERM, 'CS', '447', 'EXIST', None)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_invalid_section(self):
        self.assertRaises(LookupError, textbook.get_textbook, TERM, 'CS', '401',  None, '1060')
