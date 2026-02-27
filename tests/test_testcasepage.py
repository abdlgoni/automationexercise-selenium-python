import pytest
from pages.home_page import HomePage
from pages.test_case_page import TestCasePage
import logging

logger = logging.getLogger(__name__)

class TestTestCasePage:
    def test_test_case_page(self):
        """
        1. Launch browser
        2. Navigate to url 'http://automationexercise.com'
        3. Verify that home page is visible successfully
        4. Click on 'Test Cases' button
        5. Verify user is navigated to test cases page successfully
        """
        home_page = HomePage(self.driver)
        test_case_page = TestCasePage(self.driver)
        
        home_page.open()
        
        home_page.click_test_cases()
        assert test_case_page.is_test_case_page_displayed(), "Test Case page is not displayed"
    