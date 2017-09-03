import unittest

import timeout_decorator

from PittAPI import shuttle
from . import PittServerError


class ShuttleTest(unittest.TestCase):
    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_get_map_vehicle_points(self):
        self.assertIsInstance(shuttle.get_map_vehicle_points(), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_get_route_stop_arrivals(self):
        self.assertIsInstance(shuttle.get_route_stop_arrivals(), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_vehicle_route_stop_estimates(self):
        self.assertIsInstance(shuttle.get_vehicle_route_stop_estimates(25), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_get_routes(self):
        self.assertIsInstance(shuttle.get_routes(), list)
