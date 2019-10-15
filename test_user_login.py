import random
import string

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

MESSAGE_ACCOUNT_CREATED = "Your customer account has been created."
MESSAGE_LOGOUT = "You are now logged out."
MESSAGE_LOGIN = "You are now logged in as {} {}."


@pytest.mark.usefixtures("setup_test")
class TestSorting:
    """
    Test suite for the http://localhost/litecart/admin/?app=countries&doc=countries page
    """

    @staticmethod
    def generate_random_string(length=8, digits=False) -> str:
        """
        Generate random digits or letters string with provided length
        :param length: string length
        :param digits: If true generates digits sequence otherwise letters
        :return: string
        """
        letters = string.ascii_letters if not digits else string.digits
        return ''.join(random.choice(letters) for i in range(length))

    def is_message_shown(self, message) -> bool:
        """
        Check message is shown
        :param message: Message
        :return: True/False based on message is shown or not
        """
        message_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".notice.success")))
        return message_element.text == message and message_element.is_displayed()

    def wait_for_page_with_title(self, page_title) -> bool:
        """
        Wait for page with title
        :param page_title: Page title
        :return: True/False based on page with title was opened or not
        """
        print("Wait for page with title '{}'".format(page_title))
        title = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
        return page_title == title.text

    def test_countries_sorting(self):
        print("1. Open Countries page")
        # self.driver.get("http://localhost/litecart")
        self.driver.get("http://litecart.stqa.ru/ru/")
        print("2. Wait for Main Page page")
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h3[text()='Most Popular']")))
        print("3. Select 'New customers click here' hyperlink")
        self.driver.find_element_by_xpath("//a[text()='New customers click here']").click()
        print("4. Wait for 'Create Account' page")
        assert self.wait_for_page_with_title("Create Account"), "Impossible to open page with title 'Create Account'"
        email = self.generate_random_string(length=12) + "@litecart.com"
        password = self.generate_random_string()
        first_name = self.generate_random_string(4)
        last_name = self.generate_random_string(5)
        print("5. Enter first name")
        self.driver.find_element_by_css_selector("input[name=firstname]").send_keys(first_name)
        print("6. Enter last name")
        self.driver.find_element_by_css_selector("input[name=lastname]").send_keys(last_name)
        print("7. Enter address one")
        self.driver.find_element_by_css_selector("input[name=address1]").send_keys(self.generate_random_string(5))
        print("8. Enter postal code")
        self.driver.find_element_by_css_selector("input[name=postcode]").send_keys(self.generate_random_string(5, True))
        print("9. Enter City")
        self.driver.find_element_by_css_selector("input[name=city]").send_keys(self.generate_random_string(6))
        print("10. Select 'United States' from country drop-down")
        country_select = Select(self.driver.find_element_by_name("country_code"))
        country_select.select_by_visible_text("United States")
        print("11. Select first state from 'Zone/State/Province' drop-down")
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name=zone_code]")))
        zone_select = Select(self.driver.find_element_by_css_selector("select[name=zone_code]"))
        zone_select.select_by_visible_text("Arizona")
        print("12. Enter email")
        self.driver.find_element_by_css_selector("input[name=email]").send_keys(email)
        print("13. Enter phone")
        self.driver.find_element_by_css_selector("input[name=phone]").send_keys(Keys.HOME + self.generate_random_string(12, True))
        print("14. Enter password")
        self.driver.find_element_by_css_selector("input[name=password]").send_keys(password)
        print("15. Enter confirm password")
        self.driver.find_element_by_css_selector("input[name=confirmed_password]").send_keys(password)
        print("16. Select 'Create Account' button")
        self.driver.find_element_by_css_selector("button[name=create_account]").click()
        print("17. Wait for Main Page page")
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h3[text()='Most Popular']")))
        print("18. Check 'Your customer account has been created.' message is shown")
        assert self.is_message_shown(MESSAGE_ACCOUNT_CREATED), "'' message is not shown".format(MESSAGE_ACCOUNT_CREATED)
        print("19. Click 'Logout' button")
        self.driver.find_element_by_xpath("//a[text()='Logout']").click()
        print("20. Check 'You are now logged out.' message is shown")
        assert self.is_message_shown(MESSAGE_LOGOUT), "'' message is not shown".format(MESSAGE_LOGOUT)
        print("21. Enter email")
        self.driver.find_element_by_css_selector("input[name=email]").send_keys(email)
        print("22. Enter password")
        self.driver.find_element_by_css_selector("input[name=password]").send_keys(password)
        print("23. Click 'Login' button")
        self.driver.find_element_by_css_selector("button[name=login]").click()
        print("24. Check 'You are now logged in as " + first_name + " " + last_name + ".' message is shown")
        assert self.is_message_shown(MESSAGE_LOGIN.format(first_name, last_name)), "'' message is not shown".format(MESSAGE_LOGIN.format(first_name, last_name))
        print("25. Click 'Logout' button")
        self.driver.find_element_by_xpath("//a[text()='Logout']").click()
        print("26. Check 'You are now logged out.' message is shown")
        assert self.is_message_shown(MESSAGE_LOGOUT), "'' message is not shown".format(MESSAGE_LOGOUT)
