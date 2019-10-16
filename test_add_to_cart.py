import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


@pytest.mark.usefixtures("setup_test")
class TestAddToCart:
    """
    Test suite for the cart page
    """

    def select_product_size(self):
        """
        Select product size
        """
        try:
            size = self.driver.find_element_by_css_selector("select[name='options[Size]']")
            Select(size).select_by_index(1)
        except NoSuchElementException:
            print("Size drop-down is not shown for the product")

    def add_product_to_cart(self):
        """
        Add product to cart
        :return: True/False based on product was successfully added to cart or not
        """
        try:
            print("Select product")
            first_product = self.driver.find_element_by_css_selector("#box-most-popular ul.products li:first-of-type")
            product_link = first_product.find_element_by_xpath("./a[@class='link']")
            product_link.click()
            print("Wait for product details page")
            add_to_cart_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[name=add_cart_product]")))
            self.select_product_size()
            print("Select 'Add To Cart' button")
            current_cart_items_count = int(self.driver.find_element_by_css_selector("span.quantity").text)
            add_to_cart_button.click()
            print("Wait for count of items in cart will increase")
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "span.quantity"), str(current_cart_items_count + 1)))
        except (NoSuchElementException, TimeoutException):
            return False
        else:
            return True

    def get_number_of_products_in_cart(self):
        """
        Get number of products in cart
        :return: number of products in cart
        """
        cart_products = self.driver.find_elements_by_css_selector("table.dataTable tr:not(.header):not(.footer) td:nth-child(1)")
        return sum([int(item.text) for item in cart_products if item.text.isdigit()])

    def is_product_removed(self, target_cart_products_count):
        """
        Check if product is removed from cart
        :return: True/False based on product removed from cart or not
        """
        return self.get_number_of_products_in_cart() == target_cart_products_count

    def clear_cart(self):
        """
        Remove all products from cart
        :return: True/False based on all products were removed from cart or not
        """
        try:
            print("Get count of products in cart")
            count_of_cart_products = self.get_number_of_products_in_cart()
            print("Count of products in card: {}".format(count_of_cart_products))
            for i in range(count_of_cart_products):
                remove_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name=remove_cart_item]")))
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

    def test_add_to_cart(self):
        print("1. Open Main page")
        self.driver.get("http://litecart.stqa.ru/ru/")
        print("2. Wait for Main Page page")
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h3[text()='Most Popular']")))
        print("3. Add 3 products to cart")
        for i in range(3):
            assert self.add_product_to_cart(), "Impossible to add product to cart"
            self.driver.back()
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//h3[text()='Most Popular']")))
        print("4. Open Cart page")
        self.driver.find_element_by_css_selector("a.link[href*=checkout]").click()
        print("5. Wait for Cart page")
        self.wait.until(EC.url_contains("/checkout"))
        print("6. Remove products")
        assert self.clear_cart(), "Impossible to clear cart"
