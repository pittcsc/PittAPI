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

from PittAPI import lab

@unittest.skip
class LabTest(unittest.TestCase):
    def test_get_status_alumni(self):
        results = lab.get_status("ALUMNI")
        self.assertIsInstance(results, dict)
        self.assertTrue("status" in results.keys())

    def test_get_status_benedum(self):
        results = lab.get_status("BENEDUM")
        self.assertIsInstance(results, dict)
        self.assertTrue("status" in results.keys())

    def test_get_status_cathg27(self):
        results = lab.get_status("CATH_G27")
        self.assertIsInstance(results, dict)
        self.assertTrue("status" in results.keys())

    def test_get_status_cathg62(self):
        results = lab.get_status("CATH_G62")
        self.assertIsInstance(results, dict)
        self.assertTrue("status" in results.keys())

    def test_get_status_lawrence(self):
        results = lab.get_status("LAWRENCE")
        self.assertIsInstance(results, dict)
        self.assertTrue("status" in results.keys())

    def test_get_status_hillman(self):
        results = lab.get_status("HILLMAN")
        self.assertIsInstance(results, dict)
        self.assertTrue("status" in results.keys())

    def test_get_status_sutherland(self):
        results = lab.get_status("SUTH")
        self.assertIsInstance(results, dict)
        self.assertTrue("status" in results.keys())

    def test_fetch_labs(self):
        self.assertIsInstance(lab._fetch_labs(), list)

    def test_lab_name_validation(self):
        valid, fake = lab.LOCATIONS[0].lower(), 'test'
        self.assertTrue(lab._validate_lab(valid), lab.LOCATIONS[0])
        self.assertRaises(ValueError, lab._validate_lab, fake)

    def test_make_status(self):
        keys = ['status', 'windows', 'mac', 'linux']
        closed = lab._make_status('closed')
        open = lab._make_status('open', 1, 1, 1)

        self.assertIsInstance(closed, dict)
        self.assertIsInstance(open, dict)

        self.assertEqual(closed[keys[0]], 'closed')
        self.assertEqual(open[keys[0]], 'open')

        for key in keys[1:]:
            self.assertEqual(closed[key], 0)
            self.assertEqual(open[key], 1)

    def test_extract_machines(self):
        data = '123 hello_world, 456 macOS, 789 cool, 3 nice'
        info = lab._extract_machines(data)
        self.assertIsInstance(info, list)
        self.assertEqual(info, [123, 456, 789, 3])
