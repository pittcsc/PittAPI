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
import responses

from pathlib import Path

from PittAPI import laundry

SAMPLE_PATH = Path.cwd() / 'tests' / 'samples'
TEST_BUILDING = list(laundry.LOCATION_LOOKUP.keys())[0]


class LaundryTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        with open(SAMPLE_PATH / 'laundry.htm') as f:
            self.laundry_data = ''.join(f.readlines())

    @responses.activate
    def test_get_status_simple(self):
        responses.add(
            responses.GET,
            'http://m.laundryview.com/submitFunctions.php?monitor=true&lr=' + laundry.LOCATION_LOOKUP[TEST_BUILDING],
            body=self.laundry_data,
            status=200
        )
        status = laundry.get_status_simple(TEST_BUILDING)
        self.assertIsInstance(status, dict)
        self.assertEqual(status['building'], TEST_BUILDING)
        self.assertEqual(status['free_washers'], 2)
        self.assertEqual(status['free_dryers'], 2)
        self.assertEqual(status['total_washers'], 4)
        self.assertEqual(status['total_dryers'], 4)

    @responses.activate
    def test_get_status_detailed(self):
        responses.add(
            responses.GET,
            'http://m.laundryview.com/submitFunctions.php?monitor=true&lr=' + laundry.LOCATION_LOOKUP[TEST_BUILDING],
            body=self.laundry_data,
            status=200
        )
        status = laundry.get_status_detailed(TEST_BUILDING)
        self.assertIsInstance(status, list)
