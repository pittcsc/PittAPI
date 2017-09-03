import unittest
import timeout_decorator

from PittAPI import people
from . import PittServerError


class PeopleTest(unittest.TestCase):
    @timeout_decorator.timeout(120, timeout_exception=PittServerError)
    def test_people_get_person(self):
        ans = people.get_person("smith", 19)
        self.assertIsInstance(ans, list)
        self.assertTrue(len(ans) == 19)
