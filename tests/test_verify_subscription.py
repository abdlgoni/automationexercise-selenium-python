import pytest
import time
from pages.home_page import HomePage
from pages.cart_page import CartPage
from pages.product_page import ProductPage
import logging

logger = logging.getLogger(__name__)

class TestVerifySubscription:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.homepage = HomePage(self.driver)
        self.cartpage = CartPage(self.driver)
        self.productpage = ProductPage(self.driver)
        logger.info("Setup complete")
        
    def test_verify_subscription_in_homepage(self):
        """Verify newsletter subscription works from homepage.

        Steps:
        1. Launch browser
        2. Navigate to url 'http://automationexercise.com'
        3. Verify that home page is visible successfully
        4. Scroll down to footer
        5. Verify text 'SUBSCRIPTION'
        6. Enter email address in input and click arrow button
        7. Verify success message 'You have been successfully subscribed!' is visible
        """
        self.homepage.open()

        logger.info("Verifying homepage is visible")
        assert self.homepage.is_homepage_visible(), "Homepage is not visible"

        logger.info("Scroll to footer")
        self.homepage.scroll_to_footer()
        
        logger.info("Verify text subscription")
        assert self.homepage.is_subscription_text_visible(), "Subscription text is not visible"

        email = f"test_{int(time.time())}@example.com"
        logger.info(f"Subscribing with email: {email}")
        assert self.homepage.subscribe_email(email), "Subscription did not succeed"

        logger.info("Verify success message")
        success_message = self.homepage.get_subscription_success_message()
        assert "You have been successfully subscribed!" in success_message, \
            f"Unexpected subscription message: {success_message}"
    
    def test_verify_subscription_in_cart_page(self):
        """
        1. Launch browser
        2. Navigate to url 'http://automationexercise.com'
        3. Verify that home page is visible successfully
        4. Click 'Cart' button
        5. Scroll down to footer
        6. Verify text 'SUBSCRIPTION'
        7. Enter email address in input and click arrow button
        8. Verify success message 'You have been successfully subscribed!' is visible
        """
        self.homepage.open()

        logger.info("Verifying homepage is visible")
        assert self.homepage.is_homepage_visible(), "Homepage is not visible"

        logger.info("Clicking on cart button")
        self.homepage.click_cart()
        self.cartpage.wait_until_ready()

        logger.info("Verifying cart page is visible")
        assert self.cartpage.is_cart_page_visible(), "Cart page is not visible"


        logger.info("Verifying subscription text")
        assert self.cartpage.is_subscription_text_visible(), "Subscription text is not visible"

        email = f"test_{int(time.time())}@example.com"
        logger.info(f"Subscribing with email: {email}")
        assert self.cartpage.subscribe_email(email), "Subscription did not succeed"

        logger.info("Verify success message")
        success_message = self.cartpage.get_subscription_success_message()
        assert "You have been successfully subscribed!" in success_message, \
            f"Unexpected subscription message: {success_message}"

    def test_verify_subscription_in_product_page(self):
        """
        1. Launch browser
        2. Navigate to url 'http://automationexercise.com'
        3. Verify that home page is visible successfully
        4. Click 'Products' button
        5. Scroll down to footer
        6. Verify text 'SUBSCRIPTION'
        7. Enter email address in input and click arrow button
        8. Verify success message 'You have been successfully subscribed!' is visible
        """
        self.homepage.open()

        logger.info("Verifying homepage is visible")
        assert self.homepage.is_homepage_visible(), "Homepage is not visible"

        logger.info("Clicking on products button")
        self.homepage.click_products()
        self.productpage.wait_until_ready()
        assert self.productpage.is_all_products_page_visible(), "Products page is not visible"

        logger.info("Scroll to footer")
        self.homepage.scroll_to_footer()

        logger.info("Verify text subscription")
        assert self.homepage.is_subscription_text_visible(), "Subscription text is not visible"

        email = f"test_{int(time.time())}@example.com"
        logger.info(f"Subscribing with email: {email}")
        assert self.homepage.subscribe_email(email), "Subscription did not succeed"

        logger.info("Verify success message")
        success_message = self.homepage.get_subscription_success_message()
        assert "You have been successfully subscribed!" in success_message, \
            f"Unexpected subscription message: {success_message}"
