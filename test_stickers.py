import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures("setup_test")
class TestStickers:
    """
    Test suite for the http://localhost/litecart page
    """

    def test_stickers(self):
        print("1. Open Main page")
        self.driver.get("http://localhost/litecart")
        print("2. Wait for Main Page page")
        self.wait.until(EC.presence_of_element_located((By.ID, "slider")))
        print("3. Get All Products on the Main Page")
        products = self.driver.find_elements_by_css_selector(".product")
        print("4. Check stickers")
        for product in products:
            stickers = product.find_elements_by_xpath(".//div[contains(@class, 'sticker')]")
            assert len(stickers) == 1, "Count of stickers more then 1!"
