import time

import pytest

from pages.loginpage import LoginPage
from utils.config_reader import get_config


class TestLogin:

    @pytest.mark.parametrize("Username,Password",[("standard_user","secret_sauce"),
                                             ("locked_out_user","secret_sauce"),
                                             ("",""),
                                             ("xyz","secret_sauce"),
                                             ("standard_user","hjk")])
    def test_login(self,setup,Username,Password):
        driver = setup
        driver.get(get_config("url"))
        lp = LoginPage(driver)
        lp.verify_login(Username,Password)
