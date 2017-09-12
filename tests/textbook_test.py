import responses
import json
import os
import unittest

from PittAPI import textbook

TERM = '1000'
SCRIPT_PATH = os.path.dirname(__file__)


class TextbookTest(unittest.TestCase):
    @responses.activate
    def setUp(self):
        self.validate_term = textbook._validate_term
        self.validate_course = textbook._validate_course

    @unittest.skip
    def test_term_validation(self):
        if len(TERM) != 0:
            self.assertEqual(self.validate_term(TERM), TERM)

        self.assertEqual(self.validate_term('2000'), '2000')
        self.assertRaises(ValueError, self.validate_term, '1')
        self.assertRaises(ValueError, self.validate_term, 'a')

        self.assertRaises(ValueError, self.validate, '100')

    def test_validate_course_correct_input(self):
        self.assertEqual(self.validate_course('0000'), '0000')
        self.assertEqual(self.validate_course('0001'), '0001')
        self.assertEqual(self.validate_course('0012'), '0012')
        self.assertEqual(self.validate_course('0123'), '0123')
        self.assertEqual(self.validate_course('1234'), '1234')
        self.assertEqual(self.validate_course('9999'), '9999')

    def test_validate_course_improper_input(self):
        self.assertEqual(self.validate_course('0'), '0000')
        self.assertEqual(self.validate_course('1'), '0001')
        self.assertEqual(self.validate_course('12'), '0012')
        self.assertEqual(self.validate_course('123'), '0123')

    def test_validate_course_incorrect_input(self):
        self.assertRaises(ValueError, self.validate_course, '')
        self.assertRaises(ValueError, self.validate_course, '00000')
        self.assertRaises(ValueError, self.validate_course, '11111')
        self.assertRaises(ValueError, self.validate_course, 'hi')

    def test_construct_query(self):
        construct = textbook._construct_query
        course_query = 'compare/courses/?id=9999&term_id=1111'
        book_query = 'compare/books?id=9999'

        self.assertEqual(construct('courses', '9999', '1111'), course_query)
        self.assertEqual(construct('books', '9999'), book_query)

    def test_find_item(self):
        find = textbook._find_item('id', 'key', 'test')
        test_data = [
            {'id': 1, 'key': 1},
            {'id': 2, 'key': 4},
            {'id': 3, 'key': 9},
            {'id': 4, 'key': 16},
            {'id': 5, 'key': 25}
        ]

        for i in range(1, 6):
            self.assertEqual(find(test_data, i), i ** 2)

        self.assertRaises(LookupError, find, test_data, 6)

    @responses.activate
    def test_get_textbook(self):
        with open(os.path.join(SCRIPT_PATH, 'samples/textbook_courses.json')) as f:
            responses.add(responses.GET, 'http://pitt.verbacompare.com/compare/courses/?id=22457&term_id=1000',
                          json=json.load(f), status=201)

        self.assertRaises(TypeError, textbook.get_textbook, '0000', 'CS', '401')


    @responses.activate
    def test_invalid_course_name(self):
        with open(os.path.join(SCRIPT_PATH, 'samples/textbook_courses.json')) as f:
            responses.add(responses.GET, 'http://pitt.verbacompare.com/compare/courses/?id=22457&term_id=1000',
                          json=json.load(f), status=201)

        self.assertRaises(LookupError, textbook.get_textbook, TERM, 'CS', '000', 'EXIST', None)

    @responses.activate
    def test_invalid_instructor(self):
        with open(os.path.join(SCRIPT_PATH, 'samples/textbook_courses.json')) as f:
            responses.add(responses.GET, 'http://pitt.verbacompare.com/compare/courses/?id=22457&term_id=1000',
                          json=json.load(f), status=201)

        self.assertRaises(LookupError, textbook.get_textbook, TERM, 'CS', '447', 'EXIST', None)

    @responses.activate
    def test_invalid_section(self):
        with open(os.path.join(SCRIPT_PATH, 'samples/textbook_courses.json')) as f:
            responses.add(responses.GET, 'http://pitt.verbacompare.com/compare/courses/?id=22457&term_id=1000',
                          json=json.load(f), status=201)

        self.assertRaises(LookupError, textbook.get_textbook, TERM, 'CS', '401', None, '9999')

    @responses.activate
    def test_get_textbook_no_section_or_instructor(self):
        with open(os.path.join(SCRIPT_PATH, 'samples/textbook_courses.json')) as f:
            responses.add(responses.GET, 'http://pitt.verbacompare.com/compare/courses/?id=22457&term_id=1000',
                          json=json.load(f), status=201)

        self.assertRaises(TypeError, textbook.get_textbook, TERM, 'CS', '401', None, None)

    def test_textbook_get_textbook(self):
        responses.add(responses.GET, 'http://pitt.verbacompare.com/compare/books?id=2096322',
                      json='[{"id":"2096322_9780133744057_0","isbn":"9780133744057","pf_id":null,"new_item_id":"1440565:N","used_item_id":null,"required":"Required","sort_order":["0","1","Data Struct.+Abstract.W/Java-W/Access"],"cover_image_url":"//coverimages.verbacompete.com/09aa6a70-fd2b-5a75-9d41-63a28c87de1a.jpg","title":"Data Struct.+Abstract.W/Java-W/Access","author":"Carrano","notes":null,"citation":"\u003Cem\u003EData Struct.+Abstract.W/Java-W/Access\u003C/em\u003E by Carrano. Pearson Education, 4th Edition, 2014. (ISBN: 9780133744057).","metadata":{"section_id":"2096322","section_code":"22768","term_name":"Fall 17"},"offers":[{"isbn":"9780133744057","retailer":"bookstore","item_id":"1440565:N","condition":"new","title":null,"currency":null,"merchant":"bookstore","rental_days":null,"retailer_name":"University Store","metadata":null,"in_cart":null,"selected":null,"total":"176.2","retailer_order":0,"comments":"Pick it up or ship it!","special_comment":"Pick it up or ship it!","store_branded":true,"data_source":"bookstore","description":"From University Store on Fifth","seller_rating":null,"fcondition":"New","fprice":"$176.20","discounted_shipping":null,"can_checkout":true,"feedback_count":null,"location":null,"price":"176.2","shipping":0,"variant":"new","id":"bookstore_9780133744057_new_1440565:N"},{"isbn":"9780133744057","retailer":"bookstore","item_id":"1440565:NR","condition":"new_rental","title":null,"currency":null,"merchant":"bookstore","rental_days":null,"retailer_name":"University Store","metadata":null,"in_cart":null,"selected":null,"total":"116.4","retailer_order":0,"comments":"Pick it up or ship it!","special_comment":"Pick it up or ship it!","store_branded":true,"data_source":"bookstore","description":"From University Store on Fifth","seller_rating":null,"fcondition":"New Rental","fprice":"$116.40","discounted_shipping":null,"can_checkout":true,"feedback_count":null,"location":null,"price":"116.4","shipping":0,"variant":"rental","id":"bookstore_9780133744057_new_rental_1440565:NR"},{"isbn":"9780133744057","retailer":"bookstore","item_id":"1440565:UR","condition":"used_rental","title":null,"currency":null,"merchant":"bookstore","rental_days":null,"retailer_name":"University Store","metadata":null,"in_cart":null,"selected":null,"total":"72.35","retailer_order":0,"comments":"Books Arriving Every Day-Check Frequently!","special_comment":"Pick it up or ship it!","store_branded":true,"data_source":"bookstore","description":"From University Store on Fifth","seller_rating":null,"fcondition":"Used Rental","fprice":"$72.35","discounted_shipping":null,"can_checkout":false,"feedback_count":null,"location":null,"price":"72.35","shipping":0,"variant":"rental","id":"bookstore_9780133744057_used_rental_1440565:UR"}],"section_id":null,"db_section_id":null,"inclusive_access":false,"catalog_id":23376,"edition":"4","copyright_year":"2015"}]',
                      status=200)

    @responses.activate
    def test_textbook_get_textbook(self):
        with open(os.path.join(SCRIPT_PATH, 'samples/textbook_courses.json')) as f:
            responses.add(responses.GET, 'http://pitt.verbacompare.com/compare/courses/?id=22457&term_id=1000',
                          json=json.load(f), status=201)
        instructor_test = textbook.get_textbook(
            term=TERM,
            department='CS',
            course='445',
            instructor='GARRISON III'
        )

        section_test = textbook.get_textbook(
            term=TERM,
            department='CS',
            course='445',
            section='1030'
        )
        self.assertIsInstance(instructor_test, list)
        self.assertIsInstance(section_test, list)

    @unittest.skip
    def test_textbook_get_textbooks(self):
        multi_book_test = textbook.get_textbooks(
            term=TERM,
            courses=[
                {'department': 'CS', 'course': '445', 'section': '1010'},
                {'department': 'STAT', 'course': '1000', 'instructor': 'YANG'}])
        self.assertIsInstance(multi_book_test, list)

    def test_invalid_department_code(self):
        self.assertRaises(ValueError, textbook.get_textbook, TERM, 'TEST', '000', 'EXIST', None)
