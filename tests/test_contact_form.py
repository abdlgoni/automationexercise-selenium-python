import pytest
import os
from pages.home_page import HomePage
from pages.contact_page import ContactcusPage
import logging

logger = logging.getLogger(__name__)

class TestContactForm:
    """Test Suite for Contact Form Functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.home_page = HomePage(self.driver)
        self.contact_page = ContactcusPage(self.driver)
        logger.info("Setup Complete")
        
    def test_contact_form_submission(self):

        """
        1. Launch browser
        2. Navigate to url 'http://automationexercise.com'
        3. Verify that home page is visible successfully
        4. Click on 'Contact Us' button
        5. Verify 'GET IN TOUCH' is visible
        6. Enter name, email, subject and message
        7. Upload file
        8. Click 'Submit' button
        9. Click OK button
        10. Verify success message 'Success! Your details have been submitted successfully.' is visible
        11. Click 'Home' button and verify that landed to home page successfully
        """
 
        self.home_page.open()
        assert self.home_page.is_element_visible(self.home_page.CAROUSEL), "Homepage not visible"


        self.home_page.click_contact_us()
        logger.info("Navigated to Contact Us page")


        assert self.contact_page.get_in_touch_title().strip().lower() == 'get in touch', "Get In Touch title not found"

        self.contact_page.enter_name('Test User')
        self.contact_page.enter_email('testuser@example.com')
        self.contact_page.enter_subject('Automation Test')
        self.contact_page.enter_message('This is a test message sent by automated test.')
        logger.info("Filled contact form details")


        sample_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.txt'))
        self.contact_page.upload_file(sample_file)
        logger.info(f"Uploaded file:{sample_file}")


        self.contact_page.click_submit()
        logger.info("Clicked submit button")
        
        self.contact_page.accept_alert()

        assert self.contact_page.is_success_message_visible(), "Success message not visible"
        text = self.contact_page.get_success_message_text()
        assert 'Success! Your details have been submitted successfully.' in text or 'Success!' in text


        self.contact_page.click_home()
        assert self.home_page.homepage_loaded(), "Did not navigate back to homepage"


