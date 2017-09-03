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
import timeout_decorator

from PittAPI import library
from . import PittServerError, DEFAULT_TIMEOUT

class LibraryTest(unittest.TestCase):
    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_get_documents(self):
        self.assertIsInstance(library.get_documents("water"), dict)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_get_document_by_bookmark(self):
        bookmark_test = library.get_document_by_bookmark("ePnHCXMw42LgT" +
            "QStzc4rAe_hSmEGbaYyt7QAHThpwMYgouGcGJDo6hSkCezyGQI7SJYmZgacDKzhQ" +
            "LXAWkDazTXE2UMXdOZRPHT8Ih50Ha6hBehic_yyKlhkYVM48RbmFiamxibGAFlyLRc")
        self.assertIsInstance(bookmark_test, dict)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_invalid_bookmark(self):
        self.assertRaises(ValueError, library.get_document_by_bookmark(), "abcd")
