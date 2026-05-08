import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import get_logger


class CheckoutPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.action = ActionChains(self.driver)
        self.log = get_logger(__name__)

        self.first_name = (By.XPATH,"//input[@id='first-name']")
        self.last_name = (By.XPATH,"//input[@id='last-name']")
        self.zip_code = (By.XPATH,"//input[@id='postal-code']")
        self.continue_btn = (By.XPATH,"//input[@id='continue']")

        self.overview_prices = (By.XPATH,"//div[@class='inventory_item_price']")
        self.item_total= (By.XPATH,"//div[@class='summary_subtotal_label']")
        self.tax_label = (By.XPATH,"//div[@class='summary_tax_label']")
        self.total_label = (By.XPATH,"//div[@class='summary_total_label']")

        self.finish_btn = (By.XPATH,"//button[@id='finish']")

        self.thankyou = (By.XPATH,"//h2[normalize-space()='Thank you for your order!']")

    def fill_form(self, first, last, zipcode):
        self.log.info(f"Filling form → {first} {last} | Zip: {zipcode}")
        self.driver.find_element(*self.first_name).send_keys(first)
        self.driver.find_element(*self.last_name).send_keys(last)
        self.driver.find_element(*self.zip_code).send_keys(zipcode)
        self.log.info("Form filled successfully")

    def click_continue(self):
        self.log.info("Clicking Continue")
        self.driver.find_element(*self.continue_btn).click()
        self.wait.until(EC.url_contains("checkout-step-two"))
        self.log.info("Order overview page loaded")

    def verify_overview(self):
        self.log.info("Verifying Overview")

        price_elements = self.driver.find_elements(*self.overview_prices)
        all_prices = [float(p.text.replace("$", "")) for p in price_elements]
        sum_of_prices = round(sum(all_prices), 2)
        self.log.info(f"Individual prices: {all_prices}")
        self.log.info(f"Sum of all prices: ${sum_of_prices}")

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        item_total_text = self.driver.find_element(*self.item_total).text
        item_total = round(float(item_total_text.split("$")[1]), 2)
        assert sum_of_prices == item_total, \
            f" Sum of prices '${sum_of_prices}' != Item total '${item_total}'"
        self.log.info(f"Item total verified: ${item_total} == sum of prices ${sum_of_prices}")

        tax_text = self.driver.find_element(*self.tax_label).text
        tax = round(float(tax_text.split("$")[1]), 2)
        self.log.info(f"Tax: ${tax}")
        # Item total + Tax should equal Final Total
        expected_total = round(item_total + tax, 2)
        total_text = self.driver.find_element(*self.total_label).text
        actual_total = round(float(total_text.split("$")[1]), 2)
        assert expected_total == actual_total, \
            f"Item total + Tax '${expected_total}' != Final total '${actual_total}'"
        self.log.info(f"Final total verified: ${item_total} + ${tax} = ${actual_total}")

    def click_finish(self):
        finish = self.wait.until(EC.element_to_be_clickable(self.finish_btn))
        finish.click()
        thank = self.wait.until(EC.visibility_of_element_located(self.thankyou))
        ty = thank.text.strip()
        assert ty == "Thank you for your order!"









