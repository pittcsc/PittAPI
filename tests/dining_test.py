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

import json
import unittest
import responses

from pathlib import Path

from PittAPI import dining

SAMPLE_PATH = Path('.') / 'samples'


class DiningTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        with open(SAMPLE_PATH / 'dining.json') as f:
            self.dining_data = json.load(f)

    @responses.activate
    def test_get_dining_locations(self):
        responses.add(responses.GET,
                      'https://m.pitt.edu/dining/index.json?feed=dining_locations&_kgoui_object=kgoui_Rcontent_I2&start=0',
                      json=self.dining_data, status=200)
        responses.add(responses.GET,
                      'https://m.pitt.edu/dining/index.json?feed=dining_locations&_kgoui_object=kgoui_Rcontent_I2&start=10',
                      json=self.dining_data, status=200)
        responses.add(responses.GET,
                      'https://m.pitt.edu/dining/index.json?feed=dining_locations&_kgoui_object=kgoui_Rcontent_I2&start=20',
                      json=self.dining_data, status=200)
        self.assertIsInstance(dining.get_locations(), list)

    @responses.activate
    def test_get_dining_locations_by_status_open(self):
        responses.add(responses.GET,
                      'https://m.pitt.edu/dining/index.json?feed=dining_locations&_kgoui_object=kgoui_Rcontent_I2&start=0',
                      json=self.dining_data, status=200)
        responses.add(responses.GET,
                      'https://m.pitt.edu/dining/index.json?feed=dining_locations&_kgoui_object=kgoui_Rcontent_I2&start=10',
                      json=self.dining_data, status=200)
        responses.add(responses.GET,
                      'https://m.pitt.edu/dining/index.json?feed=dining_locations&_kgoui_object=kgoui_Rcontent_I2&start=20',
                      json=self.dining_data, status=200)
        locations = dining.get_locations_by_status('open')
        self.assertIsInstance(locations, list)
        for location in locations:
            self.assertEquals(location['status'], 'open')

    @responses.activate
    def test_get_dining_locations_by_status_closed(self):
        responses.add(responses.GET,
                      'https://m.pitt.edu/dining/index.json?feed=dining_locations&_kgoui_object=kgoui_Rcontent_I2&start=0',
                      json=self.dining_data, status=200)
        responses.add(responses.GET,
                      'https://m.pitt.edu/dining/index.json?feed=dining_locations&_kgoui_object=kgoui_Rcontent_I2&start=10',
                      json=self.dining_data, status=200)
        responses.add(responses.GET,
                      'https://m.pitt.edu/dining/index.json?feed=dining_locations&_kgoui_object=kgoui_Rcontent_I2&start=20',
                      json=self.dining_data, status=200)
        locations = dining.get_locations_by_status('closed')
        self.assertIsInstance(locations, list)
        for location in locations:
            self.assertEquals(location['status'], 'closed')
