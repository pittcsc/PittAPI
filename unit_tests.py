from pittAPI import CourseAPI, LaundryAPI, LabAPI, DiningAPI
import pprint

pp = pprint.PrettyPrinter(indent=2)

dining = DiningAPI()
#medium_dict = dining.get_dining_locations(status="open")
#pp.pprint(medium_dict)
#medium_dict = dining.get_dining_locations(status="closed")
#pp.pprint(medium_dict)
#medium_dict = dining.get_dining_locations()
#pp.pprint(medium_dict)

assert DiningAPI._encode_dining_location('Cup & Chaucer - Hilman Library') == 'cup_&_chaucer-hillman'
assert DiningAPI._encode_dining_location('Hill Top Grille - Sutherland Hall') == 'hill_top_grille-sutherland'
assert DiningAPI._encode_dining_location('Market Central - Litchfield Towers') == 'market_central-towers'
assert DiningAPI._encode_dining_location("Mato's - Sutherland Hall") == 'mato\'s-sutherland'
assert DiningAPI._encode_dining_location('Quick Zone - Sutherland Hall') == 'quick_zone-sutherland'
assert DiningAPI._encode_dining_location('Red Hot Chef - Sutherland Hall') == 'red_hot_chef-sutherland'
assert DiningAPI._encode_dining_location(u'Bookstore Caf\xe9') == 'bookstore_cafe'
assert DiningAPI._encode_dining_location('Bunsen Brewer - Chevron Science Center') == 'bunsen_brewer-chevron'
assert DiningAPI._encode_dining_location('Burger King - Petersen Events Center Food Court') == 'burger_king-petersen'
assert DiningAPI._encode_dining_location(u'Caf\xe9 at the Pete - Petersen Events Center Food Court') == 'cafe_at_the_pete-petersen'
assert DiningAPI._encode_dining_location(u'Caf\xe9 Victoria') == 'cafe_victoria'
assert DiningAPI._encode_dining_location(u'Cathedral Caf\xe9') == 'cathedral_cafe'
assert DiningAPI._encode_dining_location('Cathedral Coffee') == 'cathedral_coffee'
assert DiningAPI._encode_dining_location('Common Grounds - Litchfield Towers') == 'common_grounds-towers'
assert DiningAPI._encode_dining_location('Culinary Classics - Schenley Cafe') == 'culinary_classics-schenley_cafe'
assert DiningAPI._encode_dining_location('Einstein Bros Bagels - Benedum Hall') == 'einstein_bros_bagels-benedum'
assert DiningAPI._encode_dining_location('Einstein Bros Bagels - Wesley W. Posvar, Second Floor') == 'einstein_bros_bagels-posvar'
assert DiningAPI._encode_dining_location("Hill O' Beans - Sutherland Hall") == 'hill_o\'_beans-sutherland'
assert DiningAPI._encode_dining_location("Nicola's Garden - Schenley Cafe") == 'nicola\'s_garden-schenley_cafe'
assert DiningAPI._encode_dining_location('Oakland Bakery and Market - Amos Hall') == 'oakland_bakery_and_market-amos'
assert DiningAPI._encode_dining_location('Pasta Plus - Petersen Events Center Food Court') == 'pasta_plus-petersen'
assert DiningAPI._encode_dining_location('Pizza Hut Express - Schenley Cafe') == 'pizza_hut_express-schenley_cafe'
assert DiningAPI._encode_dining_location('Salad Sensations - Petersen Events Center Food Court') == 'salad_sensations-petersen'
assert DiningAPI._encode_dining_location('Simply To GO - Langley Hall') == 'simply_to_go-langley'
assert DiningAPI._encode_dining_location('Strutters - Schenley Cafe') == 'strutters-schenley_cafe'
assert DiningAPI._encode_dining_location('Sub Connection') == 'sub_connection'
assert DiningAPI._encode_dining_location('Sub Connection - Schenley Cafe') == 'sub_connection-schenley_cafe'
assert DiningAPI._encode_dining_location('Taco Bell - Schenley Cafe') == 'taco_bell-schenley_cafe'
assert DiningAPI._encode_dining_location('The Pennsylvania Perk') == 'the_pennsylvania_perk'
assert DiningAPI._encode_dining_location('The Side Bar - Barco Law Building') == 'the_side_bar-barco'
assert DiningAPI._encode_dining_location('Thirst & Ten - Panther Hall') == 'thirst_&_ten-panther'

assert DiningAPI._decode_dining_location('cup_&_chaucer-hillman') == 'Cup & Chaucer - Hilman Library'
assert DiningAPI._decode_dining_location('hill_top_grille-sutherland') == 'Hill Top Grille - Sutherland Hall'
assert DiningAPI._decode_dining_location('market_central-towers') == 'Market Central - Litchfield Towers'
assert DiningAPI._decode_dining_location('mato\'s-sutherland') == "Mato's - Sutherland Hall"
assert DiningAPI._decode_dining_location('quick_zone-sutherland') == 'Quick Zone - Sutherland Hall'
assert DiningAPI._decode_dining_location('red_hot_chef-sutherland') == 'Red Hot Chef - Sutherland Hall'
assert DiningAPI._decode_dining_location('bookstore_cafe') == u'Bookstore Caf\xe9'
assert DiningAPI._decode_dining_location('bunsen_brewer-chevron') == 'Bunsen Brewer - Chevron Science Center'
assert DiningAPI._decode_dining_location('burger_king-petersen') == 'Burger King - Petersen Events Center Food Court'
assert DiningAPI._decode_dining_location('cafe_at_the_pete-petersen') == u'Caf\xe9 at the Pete - Petersen Events Center Food Court'
assert DiningAPI._decode_dining_location('cafe_victoria') == u'Caf\xe9 Victoria'
assert DiningAPI._decode_dining_location('cathedral_cafe') == u'Cathedral Caf\xe9'
assert DiningAPI._decode_dining_location('cathedral_coffee') == 'Cathedral Coffee'
assert DiningAPI._decode_dining_location('common_grounds-towers') == 'Common Grounds - Litchfield Towers'
assert DiningAPI._decode_dining_location('culinary_classics-schenley_cafe') == 'Culinary Classics - Schenley Cafe'
assert DiningAPI._decode_dining_location('einstein_bros_bagels-benedum') == 'Einstein Bros Bagels - Benedum Hall'
assert DiningAPI._decode_dining_location('einstein_bros_bagels-posvar') == 'Einstein Bros Bagels - Wesley W. Posvar, Second Floor'
assert DiningAPI._decode_dining_location('hill_o\'_beans-sutherland') == "Hill O' Beans - Sutherland Hall"
assert DiningAPI._decode_dining_location('nicola\'s_garden-schenley_cafe') == "Nicola's Garden - Schenley Cafe"
assert DiningAPI._decode_dining_location('oakland_bakery_and_market-amos') == 'Oakland Bakery and Market - Amos Hall'
assert DiningAPI._decode_dining_location('pasta_plus-petersen') == 'Pasta Plus - Petersen Events Center Food Court'
assert DiningAPI._decode_dining_location('pizza_hut_express-schenley_cafe') == 'Pizza Hut Express - Schenley Cafe'
assert DiningAPI._decode_dining_location('salad_sensations-petersen') == 'Salad Sensations - Petersen Events Center Food Court'
assert DiningAPI._decode_dining_location('simply_to_go-langley') == 'Simply To GO - Langley Hall'
assert DiningAPI._decode_dining_location('strutters-schenley_cafe') == 'Strutters - Schenley Cafe'
assert DiningAPI._decode_dining_location('sub_connection') == 'Sub Connection'
assert DiningAPI._decode_dining_location('sub_connection-schenley_cafe') == 'Sub Connection - Schenley Cafe'
assert DiningAPI._decode_dining_location('taco_bell-schenley_cafe') == 'Taco Bell - Schenley Cafe'
assert DiningAPI._decode_dining_location('the_pennsylvania_perk') == 'The Pennsylvania Perk'
assert DiningAPI._decode_dining_location('the_side_bar-barco') == 'The Side Bar - Barco Law Building'
assert DiningAPI._decode_dining_location('thirst_&_ten-panther') == 'Thirst & Ten - Panther Hall'

print("All tests complete!")
