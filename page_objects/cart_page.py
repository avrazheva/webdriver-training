from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


class CartPage:
    """
    Utility class for Cart Page
    """

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def wait_for_cart_page(self) -> bool:
        """
        Wait for Cart Page
        :return: True/False based on Cart Page is opened opened or not
        """
        try:
            self.wait.until(EC.url_contains("/checkout"))
        except TimeoutException:
            print("Cart Page was not opened")
            return False
        else:
            return True

    def get_number_of_products_in_cart(self) -> int:
        """
        Get number of products in cart
        :return: number of products in cart
        """
        cart_products = self.driver.find_elements_by_css_selector("table.dataTable tr:not(.header):not(.footer) td:nth-child(1)")
        return sum([int(item.text) for item in cart_products if item.text.isdigit()])

    def is_product_removed(self, target_cart_products_count) -> bool:
        """
        Check if product is removed from cart
        :return: True/False based on product removed from cart or not
        """
        return self.get_number_of_products_in_cart() == target_cart_products_count

    def clear_cart(self) -> bool:
        """
        Remove all products from cart
        :return: True/False based on all products were removed from cart or not
        """
        try:
            print("Get count of products in cart")
            count_of_cart_products = self.get_number_of_products_in_cart()
            print("Count of products in card: {}".format(count_of_cart_products))
            for i in range(count_of_cart_products):
                remove_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name=remove_cart_item]")))
                remove_button.click()
                if i != count_of_cart_products - 1:
                    print("Wait for products count will updated")

                    def wait_for_condition(driver):
                        return self.is_product_removed(count_of_cart_products - i)

                    self.wait.until(wait_for_condition)
                else:
                    print("Wait for 'There are no items in your cart.' message")
                    self.wait.until(EC.presence_of_element_located((By.XPATH, "//em[text()='There are no items in your cart.']")))
        except (NoSuchElementException, TimeoutException):
            return False
        else:
            return True
