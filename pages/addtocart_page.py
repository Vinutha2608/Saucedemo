import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger


class AddToCartPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.action = ActionChains(self.driver)
        self.log = get_logger(__name__)

        self.add_to_cart_btn = (By.XPATH,"//button[@id='add-to-cart-sauce-labs-backpack']")
        self.cart_icon = (By.XPATH,"//a[@class='shopping_cart_link']")
        self.cart_count = (By.CSS_SELECTOR, ".shopping_cart_badge")
        self.checkout = (By.XPATH,"//button[@id='checkout']")

    def add_product_to_cart(self):
        self.log.info("Verifying cart icon")
        count_elements = self.driver.find_elements(*self.cart_count)
        count_before = int(count_elements[0].text) if count_elements else 0
        self.log.info(f"Cart count before: {count_before}")

        self.log.info("Adding product to cart")
        self.driver.find_element(*self.add_to_cart_btn).click()
        self.log.info("Product added to cart")

        count_after_element = self.wait.until(
            EC.visibility_of_element_located(self.cart_count)
        )
        count_after = int(count_after_element.text)
        self.log.info(f"Cart count after: {count_after}")

        assert count_after == count_before + 1
        self.log.info(f"Cart count increased from {count_before} → {count_after}")

    def go_to_cart(self):
        self.log.info(f"Clicking cart icon")
        cart = self.wait.until(EC.element_to_be_clickable(self.cart_icon))
        cart.click()
        checkout_btn = self.wait.until(EC.element_to_be_clickable(self.checkout))
        checkout_btn.click()
        self.log.info(f"Clicked checkout button")
