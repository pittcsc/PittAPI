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

from pittapi import people

class PeopleTest(unittest.TestCase):
    def test_people_get_person(self):
        ans = people.get_person("John C Ramirez")
        self.assertIsInstance(ans, list)
        self.assertTrue(ans[0]['email'] == "ramirez@cs.pitt.edu")
        self.assertTrue(ans[0]['name'] == "Ramirez, John C")
        self.assertTrue(ans[0]['office_phone'] == "(412) 624-8441")

    def test_people_get_person_too_many(self):
        ans = people.get_person("Smith")
        self.assertIsInstance(ans,list)
        self.assertEquals(ans, [{"ERROR":"Too many people matched your criteria."}])

    def test_people_get_person_none(self):
        ans = people.get_person("Lebron Iverson Jordan Kobe")
        self.assertIsInstance(ans,list)
        self.assertEquals(ans, [{"ERROR":"No one found."}])