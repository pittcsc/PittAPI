import pprint
import unittest
import timeout_decorator

from PittAPI import course


pp = pprint.PrettyPrinter(indent=2)


class PittServerDownException(Exception):
    """Raise when a Pitt server is down or timing out"""


class CourseTest(unittest.TestCase):
    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_course_get_courses(self):
        self.assertIsInstance(course.get_courses("2177", "CS"), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_course_get_courses_by_req(self):
        self.assertIsInstance(course.get_courses_by_req("2177", "Q"), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_course_get_class_description(self):
        self.assertIsInstance(course.get_class_description("2177", "10045"), str)

