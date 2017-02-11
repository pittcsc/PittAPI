import pprint
import unittest

from PittAPI import course, lab, laundry, people, dining

pp = pprint.PrettyPrinter(indent=2)

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


class UnitTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_courseapi_get_courses(self):
        # need to rewrite this test to accomodate the case where no courses are offered
        for t in terms:
            for s in subjects:
                pp.pprint(s)
                try:
                    results = course.get_courses(term=t, subject=s)
                    for result in results:
                        res1 = u'pass' if t in result[u'term']    else s + u'_' + t + u'_' + u'fail'
                        res2 = u'pass' if s in result[u'subject'] else s + u'_' + t + u'_' + u'fail'
                        self.assertEqual(res1, u'pass')
                        self.assertEqual(res2, u'pass')
                except ValueError:
                    pass

    def test_courseapi_retrieve_from_url(self):
        # staticmethod
        # need to rewrite this test to accomodate the case where no courses are offered
        for t in terms:
            for s in subjects:
                url = 'http://www.courses.as.pitt.edu/results-subja.asp?TERM={}&SUBJ={}'.format(t, s)
                courses = course._retrieve_from_url(url)
                res = u'pass' if len(courses) > 0 else u'empty course list: fail'
                self.assertEqual(res, u'pass')
                for c in courses:
                    res1 = u'pass' if t in unicode(str(c), u'utf-8') else s + u'_' + t + u'_' + u'fail'
                    res2 = u'pass' if s in unicode(str(c), u'utf-8') else s + u'_' + t + u'_' + u'fail'
                    self.assertEqual(res1, u'pass')
                    self.assertEqual(res2, u'pass')

    def test_courseapi_get_course_dict(self):
        # staticmethod
        self.assertTrue(True)

    def test_courseapi_get_courses_by_req(self):
        self.assertTrue(True)

    def test_courseapi_get_class_description(self):
        #staticmethod
        self.assertTrue(True)

    def test_labapi_get_status(self):
        self.assertTrue(True)

    def test_laundryapi_get_status_simple(self):
        self.assertTrue(True)

    def test_laundryapi_get_status_detailed(self):
        self.assertTrue(True)

    def test_peopleapi_get_person(self):
        self.assertTrue(True)

    def test_diningapi_get_dining_locations(self):
        self.assertTrue(True)

    def test_diningapi_get_dining_locations_by_status(self):
        self.assertTrue(True)

    def test_diningapi_get_dining_location_by_name(self):
        self.assertTrue(True)

    def test_diningapi_get_dining_location_menu(self):
        self.assertTrue(True)

    def test_diningapi_encode_dining_location(self):
        # staticmethod
        self.assertEqual(dining._encode_dining_location('Cup & Chaucer - Hilman Library'), 'cup_&_chaucer-hillman')
        self.assertEqual(dining._encode_dining_location('Hill Top Grille - Sutherland Hall'), 'hill_top_grille-sutherland')
        self.assertEqual(dining._encode_dining_location('Market Central - Litchfield Towers'), 'market_central-towers')
        self.assertEqual(dining._encode_dining_location("Mato's - Sutherland Hall"), 'mato\'s-sutherland')
        self.assertEqual(dining._encode_dining_location('Quick Zone - Sutherland Hall'), 'quick_zone-sutherland')
        self.assertEqual(dining._encode_dining_location('Red Hot Chef - Sutherland Hall'), 'red_hot_chef-sutherland')
        self.assertEqual(dining._encode_dining_location(u'Bookstore Caf\xe9'), u'bookstore_cafe')
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

    def test_diningapi_decode_dining_location(self):
        # staticmethod
        self.assertEqual(dining._decode_dining_location('cup_&_chaucer-hillman'), 'Cup & Chaucer - Hilman Library')
        self.assertEqual(dining._decode_dining_location('hill_top_grille-sutherland'), 'Hill Top Grille - Sutherland Hall')
        self.assertEqual(dining._decode_dining_location('market_central-towers'), 'Market Central - Litchfield Towers')
        self.assertEqual(dining._decode_dining_location('mato\'s-sutherland'), "Mato's - Sutherland Hall")
        self.assertEqual(dining._decode_dining_location('quick_zone-sutherland'), 'Quick Zone - Sutherland Hall')
        self.assertEqual(dining._decode_dining_location('red_hot_chef-sutherland'), 'Red Hot Chef - Sutherland Hall')
        self.assertEqual(dining._decode_dining_location(u'bookstore_cafe'), u'Bookstore Caf\xe9')
        self.assertEqual(dining._decode_dining_location('bunsen_brewer-chevron'), 'Bunsen Brewer - Chevron Science Center')
        self.assertEqual(dining._decode_dining_location('burger_king-petersen'), 'Burger King - Petersen Events Center Food Court')
        self.assertEqual(dining._decode_dining_location('cafe_at_the_pete-petersen'), u'Caf\xe9 at the Pete - Petersen Events Center Food Court')
        self.assertEqual(dining._decode_dining_location('cafe_victoria'), u'Caf\xe9 Victoria')
        self.assertEqual(dining._decode_dining_location('cathedral_cafe'), u'Cathedral Caf\xe9')
        self.assertEqual(dining._decode_dining_location('cathedral_coffee'), 'Cathedral Coffee')
        self.assertEqual(dining._decode_dining_location('common_grounds-towers'), 'Common Grounds - Litchfield Towers')
        self.assertEqual(dining._decode_dining_location('culinary_classics-schenley_cafe'), 'Culinary Classics - Schenley Cafe')
        self.assertEqual(dining._decode_dining_location('einstein_bros_bagels-benedum'), 'Einstein Bros Bagels - Benedum Hall')
        self.assertEqual(dining._decode_dining_location('einstein_bros_bagels-posvar'), 'Einstein Bros Bagels - Wesley W. Posvar, Second Floor')
        self.assertEqual(dining._decode_dining_location('hill_o\'_beans-sutherland'), "Hill O' Beans - Sutherland Hall")
        self.assertEqual(dining._decode_dining_location('nicola\'s_garden-schenley_cafe'), "Nicola's Garden - Schenley Cafe")
        self.assertEqual(dining._decode_dining_location('oakland_bakery_and_market-amos'), 'Oakland Bakery and Market - Amos Hall')
        self.assertEqual(dining._decode_dining_location('pasta_plus-petersen'), 'Pasta Plus - Petersen Events Center Food Court')
        self.assertEqual(dining._decode_dining_location('pizza_hut_express-schenley_cafe'), 'Pizza Hut Express - Schenley Cafe')
        self.assertEqual(dining._decode_dining_location('salad_sensations-petersen'), 'Salad Sensations - Petersen Events Center Food Court')
        self.assertEqual(dining._decode_dining_location('simply_to_go-langley'), 'Simply To GO - Langley Hall')
        self.assertEqual(dining._decode_dining_location('strutters-schenley_cafe'), 'Strutters - Schenley Cafe')
        self.assertEqual(dining._decode_dining_location('sub_connection'), 'Sub Connection')
        self.assertEqual(dining._decode_dining_location('sub_connection-schenley_cafe'), 'Sub Connection - Schenley Cafe')
        self.assertEqual(dining._decode_dining_location('taco_bell-schenley_cafe'), 'Taco Bell - Schenley Cafe')
        self.assertEqual(dining._decode_dining_location('the_pennsylvania_perk'), 'The Pennsylvania Perk')
        self.assertEqual(dining._decode_dining_location('the_side_bar-barco'), 'The Side Bar - Barco Law Building')
        self.assertEqual(dining._decode_dining_location('thirst_&_ten-panther'), 'Thirst & Ten - Panther Hall')

if __name__ == '__main__':
    unittest.main()
