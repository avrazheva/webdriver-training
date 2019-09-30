import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import NoSuchElementException

CREDENTIALS = "admin"


@pytest.mark.usefixtures("setup_test")
class TestLeftPanel:
    """
    Test suite for the http://localhost/litecart/admin/ page
    """

    def is_sub_menu_present(self) -> bool:
        """
        Search for sub menu element
        :return: True/False based on sub menu element present or not
        :rtype: bool
        """
        try:
            self.driver.find_element_by_css_selector(".docs")
        except NoSuchElementException:
            return False
        else:
            return True

    def test_left_panel(self):
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
        self.wait.until(EC.presence_of_element_located((By.ID, "widget-sales")))
        print("6. Search left panel elements")
        left_panel_elements = self.driver.find_elements_by_css_selector("#box-apps-menu li#app-")
        print("7. Click left panel elements in rotation")
        for index in range(len(left_panel_elements)):
            print("7.{}: Select left panel element".format(index))
            self.driver.find_elements_by_css_selector("#box-apps-menu li#app-")[index].click()
            if self.is_sub_menu_present():
                print("7.{}: Get all sub menu elements".format(index))
                child_elements = self.driver.find_elements_by_css_selector("ul.docs li")
                print("8. Click left panel sub menu elements in rotation")
                for sub_menu_index in range(len(child_elements)):
                    print("8.{}: Wait sub menu element".format(sub_menu_index))
                    sub_menu = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul.docs li:nth-child({})".format(sub_menu_index + 1))))
                    print("8.{}: Click on element".format(sub_menu_index))
                    sub_menu.click()
                    print("8.{}: Wait for title".format(sub_menu_index))
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
