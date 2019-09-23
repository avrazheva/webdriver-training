import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CREDENTIALS = "admin"


@pytest.mark.usefixtures("setup_test")
class TestLogin:
    """
    Test suite for the http://localhost/litecart/admin/ page
    """

    def test_login(self):
        print("1. Open Login page")
        self.driver.get("http://localhost/litecart/admin/")
        print("2. Enter Username")
        username = self.driver.find_element_by_name("username")
        username.clear()
        username.send_keys(CREDENTIALS)
        print("3. Enter Password")
        password = self.driver.find_element_by_name("password")
        password.clear()
        password.send_keys(CREDENTIALS)
        print("4. Click Login button")
        self.driver.find_element_by_name("login").click()
        print("5. Wait for admin page")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "widget-sales")))
