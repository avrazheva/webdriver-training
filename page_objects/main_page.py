from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    """
    Utility class for Main Page
    """

    MOST_POPULAR_SECTION_ID = "box-most-popular"

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open(self) -> bool:
        """
        Open Main page
        :return: True/False based on Main page was successfully opened or not
        """
        self.driver.get("http://litecart.stqa.ru/ru/")
        return self.wait_for_main_page()

    def wait_for_main_page(self) -> bool:
        """
        Wait for Main page
        :return: True/False based on Main page is opened opened or not
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//h3[text()='Most Popular']")))
        except TimeoutException:
            print("Main page was not opened")
            return False
        else:
            return True

    def get_products_links_from_section(self, section_id) -> list:
        """
        Get all products from provided section on the main page
        :param section_id: Products section id
        :return: list on web elements
        """
        return self.driver.find_elements_by_css_selector("#" + section_id + " ul.products li a.link")

    def click_checkout_hyperlink(self) -> bool:
        """
        Click checkout hyperlink
        :return: True/False base on hyperlink was successfully selected or not
        """
        try:
            self.driver.find_element_by_css_selector("a.link[href*=checkout]").click()
        except NoSuchElementException:
            print("Impossible to find Checkout hyperlink")
            return False
        else:
            return True