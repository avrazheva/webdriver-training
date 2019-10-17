import pytest


@pytest.mark.usefixtures("login")
class TestBrowserLogging:
    """
    Test suite for the browser log
    """

    def test_browser_logging(self):
        print("1. Open Catalog page")
        self.driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
        print("2. Wait for Catalog page")
        assert self.utils.wait_for_page_with_title("Catalog"), "Page with title 'Catalog' is not open"
        print("3. Get all products from catalog")
        products = self.driver.find_elements_by_css_selector("table.dataTable tr.row td:nth-child(3) a[href*=product_id]")
        for index in range(len(products)):
            product = self.driver.find_elements_by_css_selector("table.dataTable tr.row td:nth-child(3) a[href*=product_id]")[index]
            product_name = product.text
            product.click()
            print("{}.1. Wait for Edit Product page".format(index + 1))
            assert self.utils.wait_for_page_with_title("Edit Product: {}".format(product_name)), "Page with title 'Catalog' is not open"
            print("{}.2. Check browser log".format(index + 1))
            assert len(self.driver.get_log("browser")) == 0, "There are some errors in browser log"
            print("{}.3. Return to Catalog page".format(index + 1))
            self.driver.back()
            assert self.utils.wait_for_page_with_title("Catalog"), "Page with title 'Catalog' is not open"
