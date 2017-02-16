'''
The Pitt API, to access workable data of the University of Pittsburgh
Copyright (C) 2015 Ritwik Gupta

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

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
