import re

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures("setup_test")
class TestProductPage:
    """
    Test suite for checking product page
    """

    def convert_rgba_string_to_digits_list(self, rgba_string) -> list:
        """
        Convert rgba string to digits list
        :param rgba_string: RGBA string
        :return: digits list
        """
        digits_list = re.findall(r'\d+', rgba_string)
        return [int(item) for item in digits_list]

    def wait_for_page_with_title(self, page_title) -> bool:
        """
        Wait for page with title
        :param page_title: Page title
        :return: True/False based on page with title was opened or not
        """
        title = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
        return page_title == title.text

    def test_product_page(self):
        print("1. Open Main page")
        self.driver.get("http://localhost/litecart/en/")
        print("2. Wait for Main Page page")
        self.wait.until(EC.presence_of_element_located((By.ID, "slider")))
        print("3. Get first element in 'Campaigns' section")
        first_campaigns_product = self.driver.find_element_by_css_selector("#box-campaigns ul.products li:first-of-type")
        product_link = first_campaigns_product.find_element_by_xpath("./a[@class='link']")
        print("4. Get product name")
        product_name_element = product_link.find_element_by_xpath("./div[@class='name']")
        print("5. Get product campaigns price")
        campaigns_price_element = product_link.find_element_by_xpath(".//*[@class='campaign-price']")
        print("6. Get product regular price")
        regular_price_element = product_link.find_element_by_xpath(".//*[@class='regular-price']")
        product_name = product_name_element.text
        campaigns_price = campaigns_price_element.text
        regular_price = regular_price_element.text
        print("7. Check campaigns price is bold")
        assert campaigns_price_element.value_of_css_property("font-weight") >= "700", "Campaigns price is not bold"
        campaigns_price_color = self.convert_rgba_string_to_digits_list(campaigns_price_element.value_of_css_property("color"))
        print("8. Check campaigns price is red")
        assert campaigns_price_color[1] == 0 and campaigns_price_color[2] == 0, "Campaigns price color is not red"
        print("9. Check campaigns price is crossed out")
        assert campaigns_price_element.value_of_css_property("text-decoration-style") == 'solid'
        print("10. Check regular price font-weight is normal")
        assert regular_price_element.value_of_css_property("font-weight") == "400", "Regular price font-weight is not incorrect"
        regular_price_color = self.convert_rgba_string_to_digits_list(regular_price_element.value_of_css_property("color"))
        print("11. Check regular price is grey")
        assert regular_price_color[0] == regular_price_color[1] == regular_price_color[2], "Regular price color is not grey"
        assert float(campaigns_price_element.value_of_css_property("font-size").split("p")[0]) > float(regular_price_element.value_of_css_property("font-size").split("p")[0])
        print("12. Select product to open product details page")
        product_link.click()
        print("13. Wait for product details page")
        assert self.wait_for_page_with_title(product_name), "Page '{}' is not shown".format(product_name)
        campaigns_price_element_pdp = self.driver.find_element_by_css_selector(".campaign-price")
        regular_price_element_pdp = self.driver.find_element_by_css_selector(".regular-price")
        print("15. Check prices are equal on the main page and on the product details page")
        assert campaigns_price_element_pdp.text == campaigns_price, "Campaigns prices are not equal"
        assert regular_price_element_pdp.text == regular_price, "Regular prices are not equal"
        print("16. Check campaigns price is bold")
        assert campaigns_price_element_pdp.value_of_css_property("font-weight") >= "700", "Campaigns price is not bold"
        campaigns_price_color_pdp = self.convert_rgba_string_to_digits_list(campaigns_price_element_pdp.value_of_css_property("color"))
        print("17. Check campaigns price is red")
        assert campaigns_price_color_pdp[1] == 0 and campaigns_price_color_pdp[2] == 0, "Campaigns price color is not red"
        print("18. Check campaigns price is crossed out")
        assert campaigns_price_element_pdp.value_of_css_property("text-decoration-style") == 'solid'
        print("19. Check regular price font-weight is normal")
        assert regular_price_element_pdp.value_of_css_property("font-weight") == "400", "Regular price font-weight is not incorrect"
        regular_price_color_pdp = self.convert_rgba_string_to_digits_list(regular_price_element_pdp.value_of_css_property("color"))
        print("20. Check regular price is grey")
        assert regular_price_color_pdp[0] == regular_price_color_pdp[1] == regular_price_color_pdp[2], "Regular price color is not grey"
        print("21. Check campaigns price larger then regular price")
        assert float(campaigns_price_element_pdp.value_of_css_property("font-size").split("p")[0]) > float(regular_price_element_pdp.value_of_css_property("font-size").split("p")[0])
