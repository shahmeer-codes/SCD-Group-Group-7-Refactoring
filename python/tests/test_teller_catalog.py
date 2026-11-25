import unittest

from catalog import SupermarketCatalog
from model_objects import Product, ProductUnit
from teller import Teller
from tests.fake_catalog import FakeCatalog


class TellerCatalogContractTest(unittest.TestCase):
    def setUp(self):
        self.catalog = FakeCatalog()
        self.teller = Teller(self.catalog)
        self.rice = Product("rice", ProductUnit.EACH)
        self.catalog.add_product(self.rice, 2.49)

    def test_catalog_product_with_name_returns_product_or_none(self):
        self.assertIs(self.catalog.product_with_name("rice"), self.rice)
        self.assertIsNone(self.catalog.product_with_name("unknown"))

    def test_teller_delegates_product_lookup_to_catalog(self):
        self.assertIs(self.teller.product_with_name("rice"), self.rice)
        self.assertIsNone(self.teller.product_with_name("unknown"))

    def test_base_catalog_product_with_name_raises_exception(self):
        base_catalog = SupermarketCatalog()
        with self.assertRaises(Exception):
            base_catalog.product_with_name("rice")
