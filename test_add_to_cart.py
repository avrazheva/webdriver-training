import pytest


@pytest.mark.usefixtures("setup_test")
class TestAddToCart:
    """
    Test suite for the cart page
    """

    def test_add_to_cart(self):
        print("1. Open Main page")
        assert self.main_page.open(), "Impossible to open Main page"
        print("2. Add 3 products to cart")
        for i in range(3):
            first_product = self.main_page.get_products_links_from_section(self.main_page.MOST_POPULAR_SECTION_ID)[0]
            first_product.click()
            assert self.pdp.wait_for_product_detail_page(), "Impossible to open Program Details Page"
            assert self.pdp.add_product_to_cart(), "Impossible to add product to cart"
            self.driver.back()
            assert self.main_page.wait_for_main_page(), "Impossible to open Main page"
        print("3. Open Cart page")
        assert self.main_page.click_checkout_hyperlink(), "Impossible to click Checkout hyperlink"
        print("4. Wait for Cart page")
        assert self.cart_page.wait_for_cart_page(), "Impossible to open Cart Page"
        print("5. Remove products")
        assert self.cart_page.clear_cart(), "Impossible to Clear Cart"
