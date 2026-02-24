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
        logger.info("="*60)
        logger.info("TEST: Register User")
        logger.info("="*60)
        
        # ========== STEP 1: Navigate to home page ==========
        self.home_page.open()
        logger.debug("Navigated to home page")
        
        # ========== STEP 2: Click Signup/Login button ==========
        self.home_page.click_signup_login()
        logger.info("Clicked Signup/Login button")
        
        # ========== STEP 3-4: Verify signup section visible ==========
        assert self.login_page.is_signup_section_visible()
        logger.info("✓ Signup section is visible")
        
        # ========== STEP 5-6: Enter signup info and submit ==========
        self.login_page.signup(self.user_data['name'], self.user_data['email'])
        logger.debug(f"Entered name: {self.user_data['name']}")
        logger.debug(f"Entered email: {self.user_data['email']}")
        
        self.login_page.click_signup_button()
        logger.info("Clicked signup button")
        
        # ========== STEP 7: Verify account info page ==========
        assert self.signup_page.is_account_info_page_displayed()
        logger.info("✓ Account information page is displayed")
        # ========== STEP 8: Prepare account information ==========
        account_data = {
            'title': 'Mr',
            'password': self.user_data['password'],
            'day': self.birth_date['day'],
            'month': self.birth_date['month'],
            'year': self.birth_date['year']
        }
        logger.debug("Prepared account data (password, DOB)")
        
        # ========== STEP 9-11: Prepare address information ==========
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
        logger.debug("Prepared address data")
        
        # ========== STEP 8-11: Fill and submit registration form ==========
        self.signup_page.complete_registration(account_data, address_data)
        logger.info("Filled account and address information")
        
        # ========== STEP 12-13: Verify account created successfully ==========
        assert self.signup_page.is_account_created_successfully()
        logger.info("✓ Account created successfully")
        message_created = self.signup_page.get_account_created_message()
        assert 'ACCOUNT CREATED!' in message_created
        logger.debug(f"Verified message: {message_created}")
        
        # ========== STEP 14: Click Continue button ==========
        self.signup_page.click_continue()
        logger.info("Clicked Continue button")

        # ========== STEP 15: Verify logged in successfully ==========
        assert self.home_page.is_logged_in()
        username = self.home_page.get_logged_in_username()
        assert username == self.user_data['name']
        logger.info(f"✓ Successfully logged in as: {username}")
        
        # ========== STEP 16: Click Delete Account button ==========
        self.home_page.click_delete_account()
        logger.info("Clicked Delete Account button")
        
        # ========== STEP 17: Verify account deleted ==========
        assert self.signup_page.is_account_deleted_successfully()
        message_deleted = self.signup_page.get_account_deleted_message()
        assert 'ACCOUNT DELETED!' in message_deleted
        logger.info(f"✓ Verified message: {message_deleted}")
        
        self.signup_page.click_continue()
        logger.info("Clicked Continue button")
        logger.info("✓ Test PASSED: User registration and deletion successful")
        
    @pytest.mark.smoke
    def test_login_correct_email_and_password(self):
        """
        Test Case 2: Login with Correct Email and Password
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
        logger.info("="*60)
        logger.info("TEST: Login with Correct Email and Password")
        logger.info("="*60)
        
        # ========== STEP 1-3: Navigate to home page ==========
        self.home_page.open()
        logger.debug("Navigated to home page")
        
        # ========== STEP 4: Click Signup/Login button ==========
        self.home_page.click_signup_login()
        logger.info("Clicked Signup/Login button")
        
        # ========== STEP 5: Verify login section visible ==========
        assert self.login_page.is_login_section_visible()
        login_title = self.login_page.get_login_title()
        assert 'Login to your account' in login_title
        logger.info("✓ Login section is visible")
        
        # ========== STEP 6-7: Enter credentials and login ==========
        self.login_page.login("abdl@gmail.com", "12345678")
        logger.debug("Entered email and password")
        
        self.login_page.click_login_button()
        logger.info("Clicked login button")
        
        # ========== STEP 8: Verify login successful ==========
        assert self.home_page.is_logged_in()
        username = self.home_page.get_logged_in_username()
        logger.info(f"✓ Successfully logged in as: {username}")
        
        # ========== STEP 9: Click Delete Account button ==========
        self.home_page.click_delete_account()
        logger.info("Clicked Delete Account button")
        
        # ========== STEP 10: Verify account deleted ==========
        assert self.signup_page.is_account_deleted_successfully()
        message_deleted = self.signup_page.get_account_deleted_message()
        assert 'ACCOUNT DELETED!' in message_deleted
        logger.info(f"✓ Verified message: {message_deleted}")
        
        self.signup_page.click_continue()
        logger.info("Clicked Continue button")
        logger.info("✓ Test PASSED: Login and account deletion successful")
        
        
    def test_login_incorrect_email_and_password(self):
        """
        Test Case 3: Login with Incorrect Email and Password
        1. Launch browser
        2. Navigate to url 'http://automationexercise.com'
        3. Verify that home page is visible successfully
        4. Click on 'Signup / Login' button
        5. Verify 'Login to your account' is visible
        6. Enter incorrect email address and password
        7. Click 'login' button
        8. Verify error 'Your email or password is incorrect!' is visible
        """
        logger.info("="*60)
        logger.info("TEST: Login with Incorrect Email and Password")
        logger.info("="*60)
        
        # ========== STEP 1-3: Navigate to home page ==========
        self.home_page.open()
        logger.debug("Navigated to home page")
        
        # ========== STEP 4: Click Signup/Login button ==========
        self.home_page.click_signup_login()
        logger.info("Clicked Signup/Login button")
        
        # ========== STEP 5: Verify login section visible ==========
        assert self.login_page.is_login_section_visible()
        login_title = self.login_page.get_login_title()
        assert 'Login to your account' in login_title
        logger.info("✓ Login section is visible")
        
        # ========== STEP 6-7: Enter incorrect credentials and try to login ==========
        self.login_page.login("incorrect@example.com", "wrongpassword")
        logger.debug("Entered incorrect email and password")
        
        self.login_page.click_login_button()
        logger.info("Clicked login button")
        
        # ========== STEP 8: Verify error message displayed ==========
        error_message = self.login_page.get_login_error()
        assert 'Your email or password is incorrect!' in error_message
        logger.info(f"✓ Error message displayed: {error_message}")
        logger.info("✓ Test PASSED: Incorrect credentials properly rejected")
        
    @pytest.mark.smoke
    def test_logout_user(self):
        """
        Test Case 4: Logout User
        1. Launch browser
        2. Navigate to url 'http://automationexercise.com'
        3. Verify that home page is visible successfully
        4. Click on 'Signup / Login' button
        5. Verify 'Login to your account' is visible
        6. Enter correct email address and password
        7. Click 'login' button
        8. Verify that 'Logged in as username' is visible
        9. Click 'Logout' button
        10. Verify that user is navigated to login page
        """
        logger.info("="*60)
        logger.info("TEST: Logout User")
        logger.info("="*60)
        
        # ========== STEP 1-3: Navigate to home page ==========
        self.home_page.open()
        logger.debug("Navigated to home page")
        
        # ========== STEP 4: Click Signup/Login button ==========
        self.home_page.click_signup_login()
        logger.info("Clicked Signup/Login button")
        
        # ========== STEP 5: Verify login section visible ==========
        assert self.login_page.is_login_section_visible()
        login_title = self.login_page.get_login_title()
        assert 'Login to your account' in login_title
        logger.info("✓ Login section is visible")
        
        # ========== STEP 6-7: Enter credentials and login ==========
        self.login_page.login("abdl@gmail.com", "indomiegoreng123!")
        logger.debug("Entered email and password")
        
        self.login_page.click_login_button()
        logger.info("Clicked login button")
        
        # ========== STEP 8: Verify login successful ==========
        assert self.home_page.is_logged_in()
        username = self.home_page.get_logged_in_username()
        logger.info(f"✓ Successfully logged in as: {username}")
        
        # ========== STEP 9: Click Logout button ==========
        self.home_page.click_logout()
        logger.info("Clicked Logout button")
        
        # ========== STEP 10: Verify navigated to login page ==========
        assert self.login_page.is_login_section_visible()
        logger.info("✓ Successfully logged out and navigated to login page")
        logger.info("✓ Test PASSED: Logout functionality working correctly")
        
    def test_signup_existing_email(self):
        """
        Test Case 5: Signup with Already Existing Email
        1. Launch browser
        2. Navigate to url 'http://automationexercise.com'
        3. Verify that home page is visible successfully
        4. Click on 'Signup / Login' button
        5. Verify 'New User Signup!' is visible
        6. Enter name and already registered email address
        7. Click 'Signup' button
        8. Verify error 'Email Address already exist!' is visible
        """
        logger.info("="*60)
        logger.info("TEST: Signup with Already Existing Email")
        logger.info("="*60)
        
        # ========== STEP 1-3: Navigate to home page ==========
        self.home_page.open()
        logger.debug("Navigated to home page")
        
        # ========== STEP 4: Click Signup/Login button ==========
        self.home_page.click_signup_login()
        logger.info("Clicked Signup/Login button")
        
        # ========== STEP 5: Verify signup section visible ==========
        assert self.login_page.is_signup_section_visible()
        logger.info("✓ Signup section is visible")
        
        # ========== STEP 6: Enter name and existing email ==========
        self.login_page.signup("abdul", "abdl@gmail.com")
        logger.debug("Entered name: abdul")
        logger.debug("Entered existing email: abdl@gmail.com")
        
        # ========== STEP 7: Click Signup button ==========
        self.login_page.click_signup_button()
        logger.info("Clicked signup button")
        
        # ========== STEP 8: Verify error message ==========
        error_message = self.login_page.get_signup_error()
        assert 'Email Address already exist!' in error_message
        logger.info(f"✓ Error message displayed: {error_message}")
        logger.info("✓ Test PASSED: Duplicate email properly rejected")
        
        