import pprint
import unittest
import timeout_decorator

from PittAPI import shuttle


pp = pprint.PrettyPrinter(indent=2)


class PittServerDownException(Exception):
    """Raise when a Pitt server is down or timing out"""


class ShuttleTest(unittest.TestCase):
    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_shuttle_get_map_vehicle_points(self):
        self.assertIsInstance(shuttle.get_map_vehicle_points(), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_shuttle_get_route_stop_arrivals(self):
        self.assertIsInstance(shuttle.get_route_stop_arrivals(), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_shuttle_get_routes(self):
        self.assertIsInstance(shuttle.get_routes(), list)

