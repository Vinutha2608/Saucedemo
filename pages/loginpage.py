from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import get_logger


class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.action = ActionChains(self.driver)
        self.log = get_logger(__name__)

        self.username = (By.XPATH,"//input[@id='user-name']")
        self.password = (By.XPATH,"//input[@id='password']")
        self.login = (By.XPATH,"//input[@id='login-button']")

    def verify_login(self,Username,Password):
        uname = self.driver.find_element(*self.username)
        uname.send_keys(Username)
        self.log.info(f"Entered username: {uname.text}")
        passw = self.driver.find_element(*self.password)
        passw.send_keys(Password)
        self.log.info(f"Entered password: {passw.text}")
        self.driver.find_element(*self.login).click()
        self.log.info(f"Clicked Login button")
        assert "inventory" in self.driver.current_url
        # return True

    def handle_popup(self):
        try:
            # Try browser alert first
            alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert.dismiss()
            print("✅ Alert dismissed")
        except TimeoutException:
            pass

        try:
            # Press Escape to close any overlay
            from selenium.webdriver.common.keys import Keys
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except:
            pass





