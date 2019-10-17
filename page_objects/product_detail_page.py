from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


class ProductDetailPage:
    """
    Utility class for Product Detail Page
    """

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def wait_for_product_detail_page(self) -> bool:
        """
        Wait for Product Detail Page
        :return: True/False based on Product Detail Page is opened opened or not
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#box-product")))
        except TimeoutException:
            print("Product Detail Page was not opened")
            return False
        else:
            return True

    def select_product_size(self):
        """
        Select product size
        """
        try:
            size = self.driver.find_element_by_css_selector("select[name='options[Size]']")
            Select(size).select_by_index(1)
        except NoSuchElementException:
            print("Size drop-down is not shown for the product")

    def add_product_to_cart(self) -> bool:
        """
        Add product to cart
        :return: True/False based on product was successfully added to cart or not
        """
        try:
            button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name=add_cart_product]")))
            self.select_product_size()
            current_cart_items_count = int(self.driver.find_element_by_css_selector("span.quantity").text)
            button.click()
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "span.quantity"), str(current_cart_items_count + 1)))
        except (TimeoutException, NoSuchElementException):
            return False
        else:
            return True
