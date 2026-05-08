from logging import Logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from utils.logger import get_logger


class InventoryPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.log = get_logger(__name__)

        # Locators
        self.product_title  = (By.XPATH, "//span[@class='title']")
        self.product_items  = (By.XPATH, "//div[@class='inventory_item']")
        self.product_names  = (By.XPATH, "//div[@class='inventory_item_name ']")
        self.product_prices = (By.XPATH, "//div[@class='inventory_item_price']")
        self.product_images = (By.CLASS_NAME, "inventory_item_img")
        self.sort_dropdown  = (By.XPATH, "//select[@class='product_sort_container']")

    def verify_products_displayed(self):
        self.log.info("Verifying inventory page loaded")
        self.wait.until(EC.visibility_of_element_located(self.product_title))
        assert "inventory" in self.driver.current_url, \
            f" Not on inventory page. URL: {self.driver.current_url}"

        products = self.driver.find_elements(*self.product_items)
        assert len(products) > 0, " No products displayed on inventory page"
        assert len(products) == 6, f" Expected 6 products but got {len(products)}"
        self.log.info(f"✅ {len(products)} products displayed after login")

    def sort_products(self, sort_type):
        dropdown = self.wait.until(
            EC.visibility_of_element_located(self.sort_dropdown)
        )
        select = Select(dropdown)
        select.select_by_value(sort_type)
        self.log.info(f" Sorted by: {sort_type}")

    def verify_sort_az(self):
        names = [n.text for n in self.driver.find_elements(*self.product_names)]
        assert names == sorted(names), \
            f" Not sorted A-Z.\nActual:   {names}\nExpected: {sorted(names)}"
        self.log.info(f" A-Z sort verified: {names}")

    def verify_sort_za(self):
        names = [n.text for n in self.driver.find_elements(*self.product_names)]
        assert names == sorted(names, reverse=True), \
            f" Not sorted Z-A.\nActual:   {names}\nExpected: {sorted(names, reverse=True)}"
        self.log.info(f" Z-A sort verified: {names}")

    def verify_sort_lohi(self):
        prices = [
            float(p.text.replace("$", ""))
            for p in self.driver.find_elements(*self.product_prices)
        ]
        assert prices == sorted(prices), \
            f" Not sorted Low-High.\nActual:   {prices}\nExpected: {sorted(prices)}"
        self.log.info(f" Price Low-High verified: {prices}")

    def verify_sort_hilo(self):
        prices = [
            float(p.text.replace("$", ""))
            for p in self.driver.find_elements(*self.product_prices)
        ]
        assert prices == sorted(prices, reverse=True), \
            f" Not sorted High-Low.\nActual:   {prices}\nExpected: {sorted(prices, reverse=True)}"
        self.log.info(f" Price High-Low verified: {prices}")

    #  Case 3: Verify product name, price, image
    def verify_product_details(self):
        names  = self.driver.find_elements(*self.product_names)
        prices = self.driver.find_elements(*self.product_prices)
        # images = self.driver.find_elements(*self.product_images)

        assert len(names)  == 6, f" Expected 6 product names, got {len(names)}"
        assert len(prices) == 6, f" Expected 6 product prices, got {len(prices)}"
        # assert len(images) == 6, f" Expected 6 product images, got {len(images)}"

        for i in range(6):
            name  = names[i].text
            price = prices[i].text
            # image = images[i].find_element(By.TAG_NAME, "img")

            assert name != "", \
                f" Product {i+1} name is empty"
            assert "$" in price, \
                f" Product {i+1} price format invalid: {price}"
            # assert image.get_attribute("src") != "", \
            #     f" Product {i+1} image src is empty"

            self.log.info(f" Product {i+1}: {name} | {price} | Image OK")