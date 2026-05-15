import pytest

from pages.inventory_page import InventoryPage
from pages.loginpage import LoginPage
from utils.config_reader import get_config
# testing branch protection

class TestInventory:

    @pytest.fixture(autouse=True)
    def setup_class(self,setup):
        self.driver = setup
        self.ip = InventoryPage(self.driver)


    @pytest.mark.usefixtures("login")
    def test_products_displayed(self):
        self.ip.verify_products_displayed()

    @pytest.mark.parametrize("sort_type,verify_method", [
        ("az",   "verify_sort_az"),
        ("za",   "verify_sort_za"),
        ("lohi", "verify_sort_lohi"),
        ("hilo", "verify_sort_hilo"),
    ])
    def test_sort_products(self, sort_type, verify_method):
        self.ip.sort_products(sort_type)
        getattr(self.ip, verify_method)()


    def test_product_details(self):
        self.ip.verify_product_details()