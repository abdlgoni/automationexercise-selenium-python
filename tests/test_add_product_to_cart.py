import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
import logging

logger = logging.getLogger(__name__)

class TestAddPRoductToCart:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.home_page = HomePage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)

    @pytest.mark.smoke
    def test_add_product_to_cart(self):
        """
        1. Launch browser
        2. Navigate to url 'http://automationexercise.com'
        3. Verify that home page is visible successfully
        4. Click 'Products' button
        5. Hover over first product and click 'Add to cart'
        6. Click 'Continue Shopping' button
        7. Hover over second product and click 'Add to cart'
        8. Click 'View Cart' button
        9. Verify both products are added to Cart
        10. Verify their prices, quantity and total price
        """

        self.home_page.open()

        logger.info("Verifying homepage")
        assert self.home_page.is_homepage_visible(), \
            "Homepage is not visible"
        logger.info("Homepage is visible")

        logger.info("Clicking product button")
        self.home_page.click_products()
        logger.info("Clicked product button")
        self.product_page.wait_until_ready()

        logger.info("Verifying all product")
        assert self.product_page.is_all_products_page_visible(), \
            "All product page is not visible"
        logger.info("All product page visible")

        logger.info("Adding first product to cart")
        self.product_page.add_to_cart_by_index(0)
        logger.info("First product added to cart")

        # Verify modal appeared
        assert self.product_page.is_modal_content_visible(), \
            "Modal not visible after adding to cart"

        logger.info("Clicking continue shopping")
        self.product_page.click_continue_shopping()
        logger.info("Clicked continue shopping")

        logger.info("Adding second product to cart")
        self.product_page.add_to_cart_by_index(1)
        logger.info("Second product added to cart")

        assert self.product_page.is_modal_content_visible(), \
            "Modal not visible after adding to cart"

        logger.info("Clicking view cart")
        self.product_page.click_view_cart_link()
        logger.info("Clicked view cart")
        self.cart_page.wait_until_ready()

        assert self.cart_page.is_cart_page_visible(), \
            "Cart page is not visible"

        logger.info("Verifying both products are added to cart")
        assert self.cart_page.verify_products_count(2), \
            "Expected 2 products in cart"
        logger.info("Both products are in cart")

        logger.info("Verifying products details..")

        cart_details = self.cart_page.get_all_cart_details()



        assert len(cart_details) == 2,\
            f"Expected 2 products in cart, got {len(cart_details)}"

        # Verify first product details
        product1 = cart_details[0]
        logger.info(f"Product 1: {product1['name']}")
        logger.info(f"  Price: {product1['price']}")
        logger.info(f"  Quantity: {product1['quantity']}")
        logger.info(f"  Total: {product1['total']}")

        assert product1['name'], "Product 1 name is empty"
        assert product1['price'], "Product 1 price is empty"
        assert product1['quantity'], "Product 1 quantity is empty"
        assert product1['total'], "Product 1 total is empty"

        # Verify second product details
        product2 = cart_details[1]
        logger.info(f"Product 2: {product2['name']}")
        logger.info(f"  Price: {product2['price']}")
        logger.info(f"  Quantity: {product2['quantity']}")
        logger.info(f"  Total: {product2['total']}")

        assert product2['name'], "Product 2 name is empty"
        assert product2['price'], "Product 2 price is empty"
        assert product2['quantity'], "Product 2 quantity is empty"
        assert product2['total'], "Product 2 total is empty"

        assert product1['name'] != product2['name'], \
            "Product should be different"

        logger.info("All product detail verified")
