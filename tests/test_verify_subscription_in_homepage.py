import pytest
import time
from pages.home_page import HomePage
import logging

logger = logging.getLogger(__name__)

class TestVerifySubsciptionInHomepage:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.homepage = HomePage(self.driver)
        logger.info("Setup complete")
        
    def test_verify_subscription(self):
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

        email = f"test_{int(time.time())}@example.com"
        logger.info(f"Subscribing with email: {email}")
        assert self.homepage.subscribe_email(email), "Subscription did not succeed"

        success_text = self.homepage.get_text(self.homepage.SUBSCRIPTION_SUCCESS)
        assert "You have been successfully subscribed!" in success_text, \
            f"Unexpected subscription message: {success_text}"
