"""
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
"""

import unittest

from PittAPI import laundry

@unittest.skip
class LaundryTest(unittest.TestCase):
    def test_laundry_get_status_simple_towers(self):
        self.assertIsInstance(laundry.get_status_simple("TOWERS"), dict)

    def test_laundry_get_status_simple_brackenridge(self):
        self.assertIsInstance(laundry.get_status_simple("BRACKENRIDGE"), dict)

    def test_laundry_get_status_simple_holland(self):
        self.assertIsInstance(laundry.get_status_simple("HOLLAND"), dict)

    def test_laundry_get_status_simple_lothrop(self):
        self.assertIsInstance(laundry.get_status_simple("LOTHROP"), dict)

    def test_laundry_get_status_simple_mccormick(self):
        self.assertIsInstance(laundry.get_status_simple("MCCORMICK"), dict)

    def test_laundry_get_status_simple_sutheast(self):
        self.assertIsInstance(laundry.get_status_simple("SUTH_EAST"), dict)

    def test_laundry_get_status_simple_suthwest(self):
        self.assertIsInstance(laundry.get_status_simple("SUTH_WEST"), dict)

    def test_laundry_get_status_simple_forbescraig(self):
        self.assertIsInstance(laundry.get_status_simple("FORBES_CRAIG"), dict)

    def test_laundry_get_status_detailed_towers(self):
        self.assertIsInstance(laundry.get_status_detailed("TOWERS"), list)

    def test_laundry_get_status_detailed_brackenridge(self):
        self.assertIsInstance(laundry.get_status_detailed("BRACKENRIDGE"), list)

    def test_laundry_get_status_detailed_holland(self):
        self.assertIsInstance(laundry.get_status_detailed("HOLLAND"), list)

    def test_laundry_get_status_detailed_lothrop(self):
        self.assertIsInstance(laundry.get_status_detailed("LOTHROP"), list)

    def test_laundry_get_status_detailed_mccormick(self):
        self.assertIsInstance(laundry.get_status_detailed("MCCORMICK"), list)

    def test_laundry_get_status_detailed_sutheast(self):
        self.assertIsInstance(laundry.get_status_detailed("SUTH_EAST"), list)

    def test_laundry_get_status_detailed_suthwest(self):
        self.assertIsInstance(laundry.get_status_detailed("SUTH_WEST"), list)

    def test_laundry_get_status_detailed_forbescraig(self):
        self.assertIsInstance(laundry.get_status_detailed("FORBES_CRAIG"), list)
