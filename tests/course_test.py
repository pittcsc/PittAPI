import unittest

from bs4 import BeautifulSoup

from PittAPI import course

TERM = course.TERMS[0]
HEADER_DATA = '<th width="9%">Subject</th><th>Catalog #</th><th>Credits/Units</th>'

@unittest.skip
class CourseTest(unittest.TestCase):
    def test_get_courses(self):
        self.assertIsInstance(course.get_courses(TERM, 'CS'), list)

    def test_get_courses_subject_query(self):
        self.assertIsInstance(course.get_courses(TERM, 'BIOSC'), list)

    def test_get_courses_programs_query(self):
        self.assertIsInstance(course.get_courses(TERM, course.PROGRAMS[0]), list)

    def test_get_courses_requirement_query(self):
        self.assertIsInstance(course.get_courses(TERM, course.REQUIREMENTS[0]), list)

    def test_get_courses_day_query(self):
        self.assertIsInstance(course.get_courses(TERM, course.DAY_PROGRAM), list)

    def test_get_courses_sat_query(self):
        self.assertIsInstance(course.get_courses(TERM, course.SAT_PROGRAM), list)

    def test_get_class_description(self):
        self.assertIsInstance(course.get_class(TERM, '10045'), dict)

    def test_invalid_class_number(self):
        self.assertRaises(ValueError, course.get_class, TERM, '0')

    def test_invalid_subject(self):
        self.assertRaises(ValueError, course.get_courses, TERM, 'AAA')

    def test_invalid_term(self):
        self.assertRaises(ValueError, course.get_courses, '1', 'CS')
        self.assertRaises(ValueError, course.get_class, '1', '10045')

    def test_term_validation(self):
        self.assertEqual(course._validate_term(TERM), TERM)
        self.assertEqual(course._validate_term(int(TERM)), TERM)
        self.assertRaises(ValueError, course._validate_term, '1')

    def test_column_header_extraction(self):
        column_titles = BeautifulSoup(HEADER_DATA, 'lxml').findAll('th')
        self.assertEqual(course._extract_header(column_titles), ['subject', 'catalog_number', 'credits'])
