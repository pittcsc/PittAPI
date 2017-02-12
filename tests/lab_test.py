import pprint
import unittest
import timeout_decorator

from PittAPI import lab


pp = pprint.PrettyPrinter(indent=2)


class PittServerDownException(Exception):
    """Raise when a Pitt server is down or timing out"""


class LabTest(unittest.TestCase):
    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_lab_get_status_alumni(self):
        self.assertIsInstance(lab.get_status("ALUMNI"), dict)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_lab_get_status_benedum(self):
        self.assertIsInstance(lab.get_status("BENEDUM"), dict)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_lab_get_status_cathg26(self):
        self.assertIsInstance(lab.get_status("CATH_G26"), dict)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_lab_get_status_cathg27(self):
        self.assertIsInstance(lab.get_status("CATH_G27"), dict)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_lab_get_status_lawrence(self):
        self.assertIsInstance(lab.get_status("LAWRENCE"), dict)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_lab_get_status_hillman(self):
        self.assertIsInstance(lab.get_status("HILLMAN"), dict)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_lab_get_status_sutherland(self):
        self.assertIsInstance(lab.get_status("SUTH"), dict)
