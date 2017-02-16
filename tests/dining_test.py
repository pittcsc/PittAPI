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

from PittAPI import dining
from . import PittServerError


class DiningTest(unittest.TestCase):
    def test_encode_dining_location(self):
        self.assertEqual(dining._encode_dining_location('Cup & Chaucer - Hilman Library'), 'cup_&_chaucer-hillman')
        self.assertEqual(dining._encode_dining_location('Hill Top Grille - Sutherland Hall'), 'hill_top_grille-sutherland')
        self.assertEqual(dining._encode_dining_location('Market Central - Litchfield Towers'), 'market_central-towers')
        self.assertEqual(dining._encode_dining_location("Mato's - Sutherland Hall"), 'mato\'s-sutherland')
        self.assertEqual(dining._encode_dining_location('Quick Zone - Sutherland Hall'), 'quick_zone-sutherland')
        self.assertEqual(dining._encode_dining_location('Red Hot Chef - Sutherland Hall'), 'red_hot_chef-sutherland')
        self.assertEqual(dining._encode_dining_location(u'Bookstore Caf\xe9'), 'bookstore_cafe')
        self.assertEqual(dining._encode_dining_location('Bunsen Brewer - Chevron Science Center'), 'bunsen_brewer-chevron')
        self.assertEqual(dining._encode_dining_location('Burger King - Petersen Events Center Food Court'), 'burger_king-petersen')
        self.assertEqual(dining._encode_dining_location(u'Caf\xe9 at the Pete - Petersen Events Center Food Court'), 'cafe_at_the_pete-petersen')
        self.assertEqual(dining._encode_dining_location(u'Caf\xe9 Victoria'), 'cafe_victoria')
        self.assertEqual(dining._encode_dining_location(u'Cathedral Caf\xe9'), 'cathedral_cafe')
        self.assertEqual(dining._encode_dining_location('Cathedral Coffee'), 'cathedral_coffee')
        self.assertEqual(dining._encode_dining_location('Common Grounds - Litchfield Towers'), 'common_grounds-towers')
        self.assertEqual(dining._encode_dining_location('Culinary Classics - Schenley Cafe'), 'culinary_classics-schenley_cafe')
        self.assertEqual(dining._encode_dining_location('Einstein Bros Bagels - Benedum Hall'), 'einstein_bros_bagels-benedum')
        self.assertEqual(dining._encode_dining_location('Einstein Bros Bagels - Wesley W. Posvar, Second Floor'), 'einstein_bros_bagels-posvar')
        self.assertEqual(dining._encode_dining_location("Hill O' Beans - Sutherland Hall"), 'hill_o\'_beans-sutherland')
        self.assertEqual(dining._encode_dining_location("Nicola's Garden - Schenley Cafe"), 'nicola\'s_garden-schenley_cafe')
        self.assertEqual(dining._encode_dining_location('Oakland Bakery and Market - Amos Hall'), 'oakland_bakery_and_market-amos')
        self.assertEqual(dining._encode_dining_location('Pasta Plus - Petersen Events Center Food Court'), 'pasta_plus-petersen')
        self.assertEqual(dining._encode_dining_location('Pizza Hut Express - Schenley Cafe'), 'pizza_hut_express-schenley_cafe')
        self.assertEqual(dining._encode_dining_location('Salad Sensations - Petersen Events Center Food Court'), 'salad_sensations-petersen')
        self.assertEqual(dining._encode_dining_location('Simply To GO - Langley Hall'), 'simply_to_go-langley')
        self.assertEqual(dining._encode_dining_location('Strutters - Schenley Cafe'), 'strutters-schenley_cafe')
        self.assertEqual(dining._encode_dining_location('Sub Connection'), 'sub_connection')
        self.assertEqual(dining._encode_dining_location('Sub Connection - Schenley Cafe'), 'sub_connection-schenley_cafe')
        self.assertEqual(dining._encode_dining_location('Taco Bell - Schenley Cafe'), 'taco_bell-schenley_cafe')
        self.assertEqual(dining._encode_dining_location('The Pennsylvania Perk'), 'the_pennsylvania_perk')
        self.assertEqual(dining._encode_dining_location('The Side Bar - Barco Law Building'), 'the_side_bar-barco')
        self.assertEqual(dining._encode_dining_location('Thirst & Ten - Panther Hall'), 'thirst_&_ten-panther')

    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_get_dining_locations(self):
        self.assertIsInstance(dining.get_dining_locations(), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_get_location_menu(self):
        self.assertIsInstance(dining.get_dining_location_menu(), list)
