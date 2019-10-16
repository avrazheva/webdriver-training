import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


@pytest.mark.usefixtures("login")
class TestAddProduct:
    """
    Test suite for the add product
    """

    def test_add_product(self):
        print("1. Open Catalog page")
        self.driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog")
        print("2. Wait for Countries page")
        assert self.utils.wait_for_page_with_title("Catalog"), "Page with title 'Catalog' is not open"
        print("3. Select 'Add New Product' button")
        self.driver.find_element_by_xpath("//a[@class='button' and text()=' Add New Product']").click()
        print("4. Wait for 'Add New Product' page")
        assert self.utils.wait_for_page_with_title("Add New Product"), "Page with title 'Add New Product' is not open"
        print("5. Select 'Enabled' Status")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='radio' and @value='1']"))).click()
        print("6. Input name")
        product_name = self.utils.generate_random_string(6)
        self.driver.find_element_by_css_selector("input[name*=name]").send_keys(product_name)
        print("7. Input code")
        self.driver.find_element_by_css_selector("input[name=code]").send_keys(self.utils.generate_random_string(6, digits=True))
        print("8. Select Category")
        self.driver.find_element_by_xpath("//input[@type='checkbox' and @value='1-1']").click()
        print("9. Select Quantity")
        self.driver.find_element_by_css_selector("input[name=quantity]").send_keys(self.utils.generate_random_string(1, digits=True))
        print("10. Upload Product image")
        self.driver.find_element_by_css_selector("input[type=file]").send_keys(os.getcwd() + "/resources/product_image.png")
        print("11. Select 'Valid From' date")
        self.driver.find_element_by_css_selector("input[name=date_valid_from]").send_keys("12-12-2018")
        print("12. Select 'Valid To' date")
        self.driver.find_element_by_css_selector("input[name=date_valid_to]").send_keys("12-12-2019")
        print("13. Select 'Information'")
        self.driver.find_element_by_css_selector("a[href*=tab-information]").click()
        print("14. Wait for 'Information' tab to be open")
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#tab-information[style*='block']")))
        print("15. Select Manufacturer")
        manufacturer = self.driver.find_element_by_css_selector("select[name=manufacturer_id]")
        Select(manufacturer).select_by_visible_text("ACME Corp.")
        print("16. Enter Keywords")
        self.driver.find_element_by_css_selector("input[name=keywords]").send_keys(self.utils.generate_random_string(5))
        print("17. Enter Short Description")
        self.driver.find_element_by_css_selector("input[name*=short_description]").send_keys(self.utils.generate_random_string(10))
        print("18. Enter Description")
        text_area = self.driver.find_element_by_css_selector("div.trumbowyg-editor")
        self.driver.execute_script("arguments[0].textContent = arguments[1];", text_area, self.utils.generate_random_string(25))
        print("20. Enter Head Title")
        self.driver.find_element_by_css_selector("input[name*=head_title]").send_keys(self.utils.generate_random_string(6))
        print("21. Enter Meta Description")
        self.driver.find_element_by_css_selector("input[name*=meta_description]").send_keys(self.utils.generate_random_string(6))
        print("22. Select 'Prices'")
        self.driver.find_element_by_css_selector("a[href*=tab-prices]").click()
        print("23. Wait for 'Prices' tab to be open")
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#tab-prices[style*='block']")))
        print("24. Enter Purchase Price")
        self.driver.find_element_by_css_selector("input[name=purchase_price]").send_keys(self.utils.generate_random_string(1, digits=True))
        print("25. Select Currency")
        currency = self.driver.find_element_by_css_selector("select[name=purchase_price_currency_code]")
        Select(currency).select_by_visible_text("Euros")
        print("26. Enter Price USD")
        self.driver.find_element_by_css_selector("input[name='prices[USD]']").send_keys(self.utils.generate_random_string(1, digits=True))
        print("27. Enter Price USD Tax")
        self.driver.find_element_by_css_selector("input[name='gross_prices[USD]']").send_keys(self.utils.generate_random_string(1, digits=True))
        print("28. Enter Price EUR")
        self.driver.find_element_by_css_selector("input[name='prices[EUR]']").send_keys(self.utils.generate_random_string(1, digits=True))
        print("29. Enter Price EUR Tax")
        self.driver.find_element_by_css_selector("input[name='gross_prices[EUR]']").send_keys(self.utils.generate_random_string(1, digits=True))
        print("30. Select Save button")
        self.driver.find_element_by_css_selector("button[name=save]").click()
        print("31. Wait for Countries page")
        assert self.utils.wait_for_page_with_title("Catalog"), "Page with title 'Catalog' is not open"
        assert self.utils.is_success_message_shown("Changes saved"), "Changes were not saved successfully"
        print("32. Get All Product Names hyperlinks from table")
        names_links = self.driver.find_elements_by_css_selector("table.dataTable tr.row td:nth-child(3) a")
        names = [name_link.text for name_link in names_links]
        assert product_name in names, "Product with name '{}' was not found it table".format(product_name)
