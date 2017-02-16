import pprint
import unittest
import timeout_decorator

from PittAPI import people


class PittServerDownException(Exception):
    """Raise when a Pitt server is down or timing out"""


class PeopleTest(unittest.TestCase):
    @timeout_decorator.timeout(120, timeout_exception=PittServerDownException)
    def test_people_get_person(self):
        ans = people.get_person("dan", 19)
        self.assertIsInstance(ans, list)
        self.assertTrue(len(ans) == 19)
