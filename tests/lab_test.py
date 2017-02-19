import unittest
import timeout_decorator

from PittAPI import lab
from . import PittServerError, DEFAULT_TIMEOUT


class LabTest(unittest.TestCase):
    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_get_status_alumni(self):
        self.assertIsInstance(lab.get_status("ALUMNI"), dict)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_get_status_benedum(self):
        self.assertIsInstance(lab.get_status("BENEDUM"), dict)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_get_status_cathg27(self):
        self.assertIsInstance(lab.get_status("CATH_G27"), dict)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_get_status_cathg62(self):
        self.assertIsInstance(lab.get_status("CATH_G62"), dict)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_get_status_lawrence(self):
        self.assertIsInstance(lab.get_status("LAWRENCE"), dict)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_get_status_hillman(self):
        self.assertIsInstance(lab.get_status("HILLMAN"), dict)

    @timeout_decorator.timeout(DEFAULT_TIMEOUT, timeout_exception=PittServerError)
    def test_get_status_sutherland(self):
        self.assertIsInstance(lab.get_status("SUTH"), dict)

    def test_lab_validation(self):
        valid, fake = lab.LOCATIONS[0].lower(), 'test'
        self.assertTrue(lab._validate_lab(valid), lab.LOCATIONS[0])
        self.assertRaises(ValueError, lab._validate_lab, fake)

