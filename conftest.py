import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from pages.loginpage import LoginPage
from utils.config_reader import get_config
from utils.excel_reader import get_excel_data

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser: chrome, edge, firefox"
    )

@pytest.fixture(scope='session')
def setup(request):
    browser = request.config.getoption("--browser")
    if browser == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")

        chrome_options.add_argument("--incognito")  # ✅ no password saving in incognito
        chrome_options.add_argument("--disable-save-password-bubble")
        chrome_options.add_argument("--disable-features=PasswordLeakDetection,PasswordCheck")
        chrome_options.add_argument("--disable-password-generation")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "profile.default_content_setting_values.notifications": 2
        })
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
     )
    elif browser == "edge":
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    elif browser == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    else:
        raise Exception("browser not supported")
    driver.get(get_config("url"))
    driver.maximize_window()
    yield driver
    driver.close()

@pytest.fixture(scope='function')
def login(setup):
    driver = setup
    lp = LoginPage(driver)

    # take first row from excel
    data = get_excel_data("login")[0]
    Username = data[0]
    Password = data[1]

    lp.verify_login(Username, Password)
    return driver