import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
SELENIUM_HUB = os.environ.get("SELENIUM_HUB", None)

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-allow-origins=*")
    chrome_options.add_argument("--window-size=1920,1080")

    if SELENIUM_HUB:
        driver = webdriver.Remote(command_executor=SELENIUM_HUB, options=chrome_options)
    else:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """Helper fixture to handle login before each functional test."""
    target_url = BASE_URL.rstrip('/')
    driver.get(f"{target_url}/login.php")
    driver.find_element("id", "inputUsername").send_keys("admin")
    driver.find_element("id", "inputPassword").send_keys("nimda666!")
    driver.find_element("xpath", "//button[@type='submit']").click()

    time.sleep(1)
    assert "Dashboard" in driver.title or "Howdy" in driver.page_source
    return driver
