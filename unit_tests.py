from pittAPI import CourseAPI, LaundryAPI, LabAPI, PeopleAPI, DiningAPI
import pprint
import unittest

pp = pprint.PrettyPrinter(indent=2)

course = CourseAPI()
dining = DiningAPI()
#medium_dict = dining.get_dining_locations(status="open")
#pp.pprint(medium_dict)
#medium_dict = dining.get_dining_locations(status="closed")
#pp.pprint(medium_dict)
#medium_dict = dining.get_dining_locations()
#pp.pprint(medium_dict)

class UnitTest(unittest.TestCase):
    def test_courseapi_get_courses(self):
        terms = ["2171", "2174", "2177"]
        subjects = [
            "AFRCNA", "ANTH", "ARABIC", "ASL", "ARCH",
            "ARTSC", "ASTRON", "BIOETH", "BIOSC", "CHEM",
            "CHLIT", "CHIN", "CLASS", "COMMRC", "CS",
            "CLST", "EAS", "ECON", "ENGCMP", "ENGFLM",
            "ENGLIT", "ENGWRT", "ENV", "FILMST", "FP",
            "FR", "FTDA", "FTDB", "FTDC", "GEOL",
            "GER", "GREEK", "GREEKM", "GSWS", "HINDI",
            "HIST", "HPS", "HAA", "ISSP", "IRISH",
            "ITAL", "JPNSE", "JS", "KOREAN", "LATIN",
            "LCTL", "LING", "MATH", "MRST", "MUSIC",
            "NROSCI", "PERS", "PHIL", "PEDC", "PHYS",
            "POLISH", "PS", "PORT", "PSY", "QUECH",
            "REL", "RELGST", "RUSS", "SERCRO", "SLAV",
            "SLOVAK", "SOC", "SPAN", "STAT", "SA",
            "SWAHIL", "SWE", "THEA", "TURKSH", "UKRAIN",
            "URBNST", "VIET",
            "BUSACC", "BUSECN", "BUSENV", "BUSFIN", "BUSHRM",
            "BUSBIS", "BUSMIS", "BUSMKT", "BUSORG", "BUSQOM",
            "BUSERV", "BUSSPP", "BUSSCM",
            "WWW", "HYBRID", "SELF", "CGSDAY", "CGSSAT",
            "BCCC", "ADMJ", "BUSERV", "CDACCT", "CGS",
            "LDRSHP", "LEGLST", "NPHS", "PUBSRV",
            "AFROTC", "INFSCI", "MILS", "UHC",
            'BIOENG', 'CEE', 'CHE', 'COE', 'COEE',
            'ECE', 'EE', 'ENGR', 'ENGRPH', 'ENRES',
            'FTDH', 'IE', 'ME', 'MEMS', 'MSE',
            'MSEP', 'PETE', 'PWEA'
        ]
        for t in terms:
            for s in subjects:
                results = course.get_courses(term=t, subject=s)
                for result in results:
                    res1 = u'pass' if t in result[u'term'] else u'fail'
                    res2 = u'pass' if s in result[u'subject'] else u'fail'
                    self.assertEqual(res1, u'pass')
                    self.assertEqual(res2, u'pass')
    
    def test_diningapi_encode_dining_location(self):
        self.assertEqual(DiningAPI._encode_dining_location('Cup & Chaucer - Hilman Library'), 'cup_&_chaucer-hillman')
        self.assertEqual(DiningAPI._encode_dining_location('Hill Top Grille - Sutherland Hall'), 'hill_top_grille-sutherland')
        self.assertEqual(DiningAPI._encode_dining_location('Market Central - Litchfield Towers'), 'market_central-towers')
        self.assertEqual(DiningAPI._encode_dining_location("Mato's - Sutherland Hall"), 'mato\'s-sutherland')
        self.assertEqual(DiningAPI._encode_dining_location('Quick Zone - Sutherland Hall'), 'quick_zone-sutherland')
        self.assertEqual(DiningAPI._encode_dining_location('Red Hot Chef - Sutherland Hall'), 'red_hot_chef-sutherland')
        self.assertEqual(DiningAPI._encode_dining_location(u'Bookstore Caf\xe9'), 'bookstore_cafe')
        self.assertEqual(DiningAPI._encode_dining_location('Bunsen Brewer - Chevron Science Center'), 'bunsen_brewer-chevron')
        self.assertEqual(DiningAPI._encode_dining_location('Burger King - Petersen Events Center Food Court'), 'burger_king-petersen')
        self.assertEqual(DiningAPI._encode_dining_location(u'Caf\xe9 at the Pete - Petersen Events Center Food Court'), 'cafe_at_the_pete-petersen')
        self.assertEqual(DiningAPI._encode_dining_location(u'Caf\xe9 Victoria'), 'cafe_victoria')
        self.assertEqual(DiningAPI._encode_dining_location(u'Cathedral Caf\xe9'), 'cathedral_cafe')
        self.assertEqual(DiningAPI._encode_dining_location('Cathedral Coffee'), 'cathedral_coffee')
        self.assertEqual(DiningAPI._encode_dining_location('Common Grounds - Litchfield Towers'), 'common_grounds-towers')
        self.assertEqual(DiningAPI._encode_dining_location('Culinary Classics - Schenley Cafe'), 'culinary_classics-schenley_cafe')
        self.assertEqual(DiningAPI._encode_dining_location('Einstein Bros Bagels - Benedum Hall'), 'einstein_bros_bagels-benedum')
        self.assertEqual(DiningAPI._encode_dining_location('Einstein Bros Bagels - Wesley W. Posvar, Second Floor'), 'einstein_bros_bagels-posvar')
        self.assertEqual(DiningAPI._encode_dining_location("Hill O' Beans - Sutherland Hall"), 'hill_o\'_beans-sutherland')
        self.assertEqual(DiningAPI._encode_dining_location("Nicola's Garden - Schenley Cafe"), 'nicola\'s_garden-schenley_cafe')
        self.assertEqual(DiningAPI._encode_dining_location('Oakland Bakery and Market - Amos Hall'), 'oakland_bakery_and_market-amos')
        self.assertEqual(DiningAPI._encode_dining_location('Pasta Plus - Petersen Events Center Food Court'), 'pasta_plus-petersen')
        self.assertEqual(DiningAPI._encode_dining_location('Pizza Hut Express - Schenley Cafe'), 'pizza_hut_express-schenley_cafe')
        self.assertEqual(DiningAPI._encode_dining_location('Salad Sensations - Petersen Events Center Food Court'), 'salad_sensations-petersen')
        self.assertEqual(DiningAPI._encode_dining_location('Simply To GO - Langley Hall'), 'simply_to_go-langley')
        self.assertEqual(DiningAPI._encode_dining_location('Strutters - Schenley Cafe'), 'strutters-schenley_cafe')
        self.assertEqual(DiningAPI._encode_dining_location('Sub Connection'), 'sub_connection')
        self.assertEqual(DiningAPI._encode_dining_location('Sub Connection - Schenley Cafe'), 'sub_connection-schenley_cafe')
        self.assertEqual(DiningAPI._encode_dining_location('Taco Bell - Schenley Cafe'), 'taco_bell-schenley_cafe')
        self.assertEqual(DiningAPI._encode_dining_location('The Pennsylvania Perk'), 'the_pennsylvania_perk')
        self.assertEqual(DiningAPI._encode_dining_location('The Side Bar - Barco Law Building'), 'the_side_bar-barco')
        self.assertEqual(DiningAPI._encode_dining_location('Thirst & Ten - Panther Hall'), 'thirst_&_ten-panther')

    def test_diningapi_decode_dining_location(self):
        self.assertEqual(DiningAPI._decode_dining_location('cup_&_chaucer-hillman'), 'Cup & Chaucer - Hilman Library')
        self.assertEqual(DiningAPI._decode_dining_location('hill_top_grille-sutherland'), 'Hill Top Grille - Sutherland Hall')
        self.assertEqual(DiningAPI._decode_dining_location('market_central-towers'), 'Market Central - Litchfield Towers')
        self.assertEqual(DiningAPI._decode_dining_location('mato\'s-sutherland'), "Mato's - Sutherland Hall")
        self.assertEqual(DiningAPI._decode_dining_location('quick_zone-sutherland'), 'Quick Zone - Sutherland Hall')
        self.assertEqual(DiningAPI._decode_dining_location('red_hot_chef-sutherland'), 'Red Hot Chef - Sutherland Hall')
        self.assertEqual(DiningAPI._decode_dining_location('bookstore_cafe'), u'Bookstore Caf\xe9')
        self.assertEqual(DiningAPI._decode_dining_location('bunsen_brewer-chevron'), 'Bunsen Brewer - Chevron Science Center')
        self.assertEqual(DiningAPI._decode_dining_location('burger_king-petersen'), 'Burger King - Petersen Events Center Food Court')
        self.assertEqual(DiningAPI._decode_dining_location('cafe_at_the_pete-petersen'), u'Caf\xe9 at the Pete - Petersen Events Center Food Court')
        self.assertEqual(DiningAPI._decode_dining_location('cafe_victoria'), u'Caf\xe9 Victoria')
        self.assertEqual(DiningAPI._decode_dining_location('cathedral_cafe'), u'Cathedral Caf\xe9')
        self.assertEqual(DiningAPI._decode_dining_location('cathedral_coffee'), 'Cathedral Coffee')
        self.assertEqual(DiningAPI._decode_dining_location('common_grounds-towers'), 'Common Grounds - Litchfield Towers')
        self.assertEqual(DiningAPI._decode_dining_location('culinary_classics-schenley_cafe'), 'Culinary Classics - Schenley Cafe')
        self.assertEqual(DiningAPI._decode_dining_location('einstein_bros_bagels-benedum'), 'Einstein Bros Bagels - Benedum Hall')
        self.assertEqual(DiningAPI._decode_dining_location('einstein_bros_bagels-posvar'), 'Einstein Bros Bagels - Wesley W. Posvar, Second Floor')
        self.assertEqual(DiningAPI._decode_dining_location('hill_o\'_beans-sutherland'), "Hill O' Beans - Sutherland Hall")
        self.assertEqual(DiningAPI._decode_dining_location('nicola\'s_garden-schenley_cafe'), "Nicola's Garden - Schenley Cafe")
        self.assertEqual(DiningAPI._decode_dining_location('oakland_bakery_and_market-amos'), 'Oakland Bakery and Market - Amos Hall')
        self.assertEqual(DiningAPI._decode_dining_location('pasta_plus-petersen'), 'Pasta Plus - Petersen Events Center Food Court')
        self.assertEqual(DiningAPI._decode_dining_location('pizza_hut_express-schenley_cafe'), 'Pizza Hut Express - Schenley Cafe')
        self.assertEqual(DiningAPI._decode_dining_location('salad_sensations-petersen'), 'Salad Sensations - Petersen Events Center Food Court')
        self.assertEqual(DiningAPI._decode_dining_location('simply_to_go-langley'), 'Simply To GO - Langley Hall')
        self.assertEqual(DiningAPI._decode_dining_location('strutters-schenley_cafe'), 'Strutters - Schenley Cafe')
        self.assertEqual(DiningAPI._decode_dining_location('sub_connection'), 'Sub Connection')
        self.assertEqual(DiningAPI._decode_dining_location('sub_connection-schenley_cafe'), 'Sub Connection - Schenley Cafe')
        self.assertEqual(DiningAPI._decode_dining_location('taco_bell-schenley_cafe'), 'Taco Bell - Schenley Cafe')
        self.assertEqual(DiningAPI._decode_dining_location('the_pennsylvania_perk'), 'The Pennsylvania Perk')
        self.assertEqual(DiningAPI._decode_dining_location('the_side_bar-barco'), 'The Side Bar - Barco Law Building')
        self.assertEqual(DiningAPI._decode_dining_location('thirst_&_ten-panther'), 'Thirst & Ten - Panther Hall')

