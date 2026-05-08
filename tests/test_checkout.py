import pytest

from pages.addtocart_page import AddToCartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage


class TestCheckout:

    @pytest.fixture(autouse=True)
    def setup_class(self, setup):
        self.driver = setup
        self.atc = AddToCartPage(self.driver)
        self.ip = InventoryPage(self.driver)
        self.checkout = CheckoutPage(self.driver)

    @pytest.mark.usefixtures("login")
    def test_verify_add_product_to_cart(self):
        self.atc.add_product_to_cart()

    def test_verify_cart(self):
        self.atc.go_to_cart()

    def test_fill_form(self):
        first = "John"
        last = "Doe"
        zipcode = "564787"
        self.checkout.fill_form(first, last, zipcode)
        self.checkout.click_continue()

    def test_verify_order_overview(self):
        self.checkout.verify_overview()
        self.checkout.click_finish()



    # @pytest.mark.usefixtures("login")
    # def test_end_to_end(self):
    #     first = "John"
    #     last = "Doe"
    #     zipcode = "564787"
    #     self.atc.add_product_to_cart()
    #     self.atc.go_to_cart()
    #     self.checkout.fill_form(first,last,zipcode)
    #     self.checkout.click_continue()
    #     self.checkout.verify_overview()
    #     self.checkout.click_finish()



    


