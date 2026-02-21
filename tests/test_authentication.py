"""
Test Cases for Authentication (Login & Registration)
Based on Automation Exercise Test Cases
"""
import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from utils.data_generator import TestDataGenerator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.usefixtures("driver")
class TestAuthentication:
    """Test suite for user authentication"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.home_page = HomePage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.signup_page = SignupPage(self.driver)
        self.data_generator = TestDataGenerator()
        self.user_data = self.data_generator.generate_user_data()
        self.birth_date = self.data_generator.generate_birth_date()
        logger.info("Setup Complete")
    
    @pytest.mark.smoke
    def test_register_user(self):
        """
        Test Case 1: Register User
        Steps:
        1. Navigate to url 'http://automationexercise.com'
        2. Verify that home page is visible successfully
        3. Click on 'Signup / Login' button
        4. Verify 'New User Signup!' is visible
        5. Enter name and email address
        6. Click 'Signup' button
        7. Verify that 'ENTER ACCOUNT INFORMATION' is visible
        8. Fill details: Title, Name, Email, Password, Date of birth
        9. Select checkbox 'Sign up for our newsletter!'
        10. Select checkbox 'Receive special offers from our partners!'
        11. Fill details: First name, Last name, Company, Address, Address2, Country, State, City, Zipcode, Mobile Number
        12. Click 'Create Account button'
        13. Verify that 'ACCOUNT CREATED!' is visible
        14. Click 'Continue' button
        15. Verify that 'Logged in as username' is visible
        16. Click 'Delete Account' button
        17. Verify that 'ACCOUNT DELETED!' is visible and click 'Continue' button
        """
        
        logger.info("Starting test register user")
        self.home_page.open()
        
        self.home_page.click_signup_login()
        logger.info("Clicked Signup/Login")
        
        assert self.login_page.is_signup_section_visible()
        logger.info("Signup section is visible")
        
        self.login_page.signup(self.user_data['name'], self.user_data['email'])
        self.login_page.click_signup_button()
        logger.info("Filled signup form and clicked signup button")
        
        assert self.signup_page.is_account_info_page_displayed()
        logger.info("Account information page is visible")
        # Fill account info
        account_data = {
            'title': 'Mr',
            'password': self.user_data['password'],
            'day': self.birth_date['day'],
            'month': self.birth_date['month'],
            'year': self.birth_date['year']
        }
        
        # Fill address info
        address_data = {
            'first_name': self.user_data['first_name'],
            'last_name': self.user_data['last_name'],
            'company': self.user_data['company'],
            'address1': self.user_data['address1'],
            'address2': self.user_data['address2'],
            'country': self.user_data['country'],
            'state': self.user_data['state'],
            'city': self.user_data['city'],
            'zipcode': self.user_data['zipcode'],
            'mobile': self.user_data['mobile']
        }
        
        self.signup_page.complete_registration(account_data, address_data)
        logger.info("Completed registration form")
        # Submit
        # Verify success
        assert self.signup_page.is_account_created_successfully()
        logger.info("Acconut created successfully")
        message_created = self.signup_page.get_account_created_message()
        assert 'ACCOUNT CREATED!' in message_created
        self.signup_page.click_continue()

        assert self.home_page.is_logged_in()
        
        username = self.home_page.get_logged_in_username()
        assert username == self.user_data['name'] 
        logger.info(f"Successfully registered user: {username}")
        
        self.home_page.click_delete_account()
        assert self.signup_page.is_account_deleted_successfully()
        message_deleted = self.signup_page.get_account_deleted_message()
        assert 'ACCOUNT DELETED!' in message_deleted
        
        self.signup_page.click_continue()
        logger.info("Successfully deleted account")
        
    @pytest.mark.smoke
    def test_login_correct_email_and_password(self):
        """
        1. Launch browser
        2. Navigate to url 'http://automationexercise.com'
        3. Verify that home page is visible successfully
        4. Click on 'Signup / Login' button
        5. Verify 'Login to your account' is visible
        6. Enter correct email address and password
        7. Click 'login' button
        8. Verify that 'Logged in as username' is visible
        9. Click 'Delete Account' button
        10. Verify that 'ACCOUNT DELETED!' is visible
        """
        
        logger.info("Starting test login with correct email and password")
        self.home_page.open()
        
        self.home_page.click_signup_login()
        logger.info("Clicked Signup/Login")
        
        self.login_page.is_login_section_visible()
        login_title = self.login_page.get_login_title()
        assert 'Login to your account' in login_title
        logger.info("Login section is visible")
        
        self.login_page.login("abdl@gmail.com", "12345678")
        self.login_page.click_login_button()
        logger.info("Entered credentials and clicked login button")
        assert self.home_page.is_logged_in()
        username = self.home_page.get_logged_in_username()
        logger.info(f"Successfully logged in as: {username}")
        self.home_page.click_delete_account()
        assert self.signup_page.is_account_deleted_successfully()
        message_deleted = self.signup_page.get_account_deleted_message()
        assert 'ACCOUNT DELETED!' in message_deleted
        self.signup_page.click_continue()
        logger.info("Successfully deleted account")
        
            
        
        