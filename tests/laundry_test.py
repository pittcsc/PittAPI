import pprint
import unittest
import timeout_decorator

from PittAPI import laundry


pp = pprint.PrettyPrinter(indent=2)


class PittServerDownException(Exception):
    """Raise when a Pitt server is down or timing out"""


class LaundryTest(unittest.TestCase):
    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_simple_towers(self):
        self.assertIsInstance(laundry.get_status_simple("TOWERS"), dict)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_simple_brackenridge(self):
        self.assertIsInstance(laundry.get_status_simple("BRACKENRIDGE"), dict)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_simple_holland(self):
        self.assertIsInstance(laundry.get_status_simple("HOLLAND"), dict)
    
    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_simple_lothrop(self):
        self.assertIsInstance(laundry.get_status_simple("LOTHROP"), dict)
    
    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_simple_mccormick(self):
        self.assertIsInstance(laundry.get_status_simple("MCCORMICK"), dict)
    
    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_simple_sutheast(self):
        self.assertIsInstance(laundry.get_status_simple("SUTH_EAST"), dict)
    
    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_simple_suthwest(self):
        self.assertIsInstance(laundry.get_status_simple("SUTH_WEST"), dict)
    
    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_simple_forbescraig(self):
        self.assertIsInstance(laundry.get_status_simple("FORBES_CRAIG"), dict)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_detailed_towers(self):
        self.assertIsInstance(laundry.get_status_detailed("TOWERS"), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_detailed_brackenridge(self):
        self.assertIsInstance(laundry.get_status_detailed("BRACKENRIDGE"), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_detailed_holland(self):
        self.assertIsInstance(laundry.get_status_detailed("HOLLAND"), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_detailed_lothrop(self):
        self.assertIsInstance(laundry.get_status_detailed("LOTHROP"), list)
    
    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_detailed_mccormick(self):
        self.assertIsInstance(laundry.get_status_detailed("MCCORMICK"), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_detailed_sutheast(self):
        self.assertIsInstance(laundry.get_status_detailed("SUTH_EAST"), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_detailed_suthwest(self):
        self.assertIsInstance(laundry.get_status_detailed("SUTH_WEST"), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerDownException)
    def test_laundry_get_status_detailed_forbescraig(self):
        self.assertIsInstance(laundry.get_status_detailed("FORBES_CRAIG"), list)
