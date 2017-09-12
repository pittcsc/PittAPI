import unittest

from PittAPI import people

@unittest.skip
class PeopleTest(unittest.TestCase):
    def test_people_get_person(self):
        ans = people.get_person("smith", 19)
        self.assertIsInstance(ans, list)
        self.assertTrue(len(ans) == 19)
