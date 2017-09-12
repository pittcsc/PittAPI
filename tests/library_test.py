import unittest

from PittAPI import library

@unittest.skip
class LibraryTest(unittest.TestCase):
    def test_get_documents(self):
        self.assertIsInstance(library.get_documents("water"), dict)

    def test_get_document_by_bookmark(self):
        bookmark_test = library.get_document_by_bookmark("ePnHCXMw42LgT" +
            "QStzc4rAe_hSmEGbaYyt7QAHThpwMYgouGcGJDo6hSkCezyGQI7SJYmZgacDKzhQ" +
            "LXAWkDazTXE2UMXdOZRPHT8Ih50Ha6hBehic_yyKlhkYVM48RbmFiamxibGAFlyLRc")
        self.assertIsInstance(bookmark_test, dict)

    def test_invalid_bookmark(self):
        self.assertRaises(ValueError, library.get_document_by_bookmark, "abcd")
