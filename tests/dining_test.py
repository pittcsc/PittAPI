import unittest

from PittAPI import dining

@unittest.skip
class DiningTest(unittest.TestCase):
    def test_get_dining_locations(self):
        self.assertIsInstance(dining.get_locations(), list)
