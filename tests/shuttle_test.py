import unittest

from PittAPI import shuttle

@unittest.skip
class ShuttleTest(unittest.TestCase):
    def test_get_map_vehicle_points(self):
        self.assertIsInstance(shuttle.get_map_vehicle_points(), list)

    def test_get_route_stop_arrivals(self):
        self.assertIsInstance(shuttle.get_route_stop_arrivals(), list)

    def test_vehicle_route_stop_estimates(self):
        self.assertIsInstance(shuttle.get_vehicle_route_stop_estimates(25), list)

    def test_get_routes(self):
        self.assertIsInstance(shuttle.get_routes(), list)
