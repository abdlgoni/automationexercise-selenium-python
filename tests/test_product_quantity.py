import pytest
from pages.home_page import HomePage
from pages.detail_product import DetailProductPage
from pages.cart_page import CartPage
import logging

logger = logging.getLogger(__name__)

class TestProductQuantity:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.home_page = HomePage(self.driver)
        self.detail_product = DetailProductPage(self.driver)
        self.cart_page = CartPage(self.driver)
        logger.info("Setup complete")

    @pytest.mark.smoke
    def test_product_quantity(self):

        """
        1. Launch browser
        2. Navigate to url 'http://automationexercise.com'
        3. Verify that home page is visible successfully
        4. Click 'View Product' for any product on home page
        5. Verify product detail is opened
        6. Increase quantity to 4
        7. Click 'Add to cart' button
        8. Click 'View Cart' button
        9. Verify that product is displayed in cart page with exact quantity
        """

        logger.info("Launching browser")
        self.home_page.open()
        logger.info("Browser launched")

        logger.info("Verifying home page is visible")
        assert self.home_page.is_homepage_visible(), \
            "Home page is not visible"
        logger.info("Home page visible successfully")

        logger.info("Clicking view product of first product")
        assert self.home_page.click_view_product_by_index(0), \
            "Failed to click view product button"
        logger.info("Clicked view product of first product")
        self.detail_product.wait_until_ready()

        logger.info("Verifying user is on product detail page")
        assert self.detail_product.is_product_detail_page_visible(), \
            "Product detail is not visible"
        logger.info("User landed to product detail page")

        logger.info("Increasing quantity to 4")
        assert self.detail_product.set_quantity(4), \
            "Failed to set quantity"
        logger.info("Quantity increased to 4")

        logger.info("Clicking add to cart button")
        assert self.detail_product.click_add_to_cart(), \
            "Failed to click add to cart button"
        logger.info("Clicked add to cart button")

        logger.info("Verifying modal content is visible")
        assert self.detail_product.is_modal_content_visible(), \
            "Modal content is not visible"
        logger.info("Modal content visible")

        logger.info("Clicking view cart")
        self.detail_product.click_view_cart_link()
        logger.info("Clicked view cart")
        self.cart_page.wait_until_ready()

        logger.info("Verifying product is displayed in cart page with exact quantity")
        assert self.cart_page.is_cart_page_visible(), \
            "Cart page is not visible"
        logger.info("Cart page visible")

        cart_quantity = self.cart_page.get_product_quantities_from_cart()
        logger.info(f"Cart quantity: {cart_quantity}")

        cart_quantity = int(cart_quantity[0])
        assert cart_quantity == 4, \
            f"Expected quantity 4, got {cart_quantity}"
        logger.info("Product is displayed in cart page with exact quantity")

        logger.info("Test product quantity completed successfully")