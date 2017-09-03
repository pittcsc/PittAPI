import unittest

import timeout_decorator

from PittAPI import dining
from . import PittServerError

@unittest.skip
class DiningTest(unittest.TestCase):
    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_get_dining_locations(self):
        self.assertIsInstance(dining.get_locations(), list)
