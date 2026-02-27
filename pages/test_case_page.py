from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

class TestCasePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        
    TEST_CASE_CONTAINER = (By.CSS_SELECTOR, "section[id='form'] div[class='container']")
    
    def is_test_case_page_displayed(self):
        self.logger.info("Checking Test Case page visibility")
        return self.is_element_visible(self.TEST_CASE_CONTAINER)