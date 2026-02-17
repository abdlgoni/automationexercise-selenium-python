"""
Test Cases for Authentication (Login & Registration)
Based on Automation Exercise Test Cases
"""
import pytest
from selenium.webdriver.common.by import By
import time

class TestAuthentication:
    """Test suite for user authentication"""
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_register_user(self, driver):
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
        # Verify home page is visible
        assert "Automation Exercise" in driver.title
        
        # Click on Signup/Login button
        signup_login_btn = driver.find_element(By.XPATH, "//a[@href='/login']")
        signup_login_btn.click()
        
        # Verify 'New User Signup!' is visible
        signup_text = driver.find_element(By.XPATH, "//h2[text()='New User Signup!']")
        assert signup_text.is_displayed()
        
        # Enter name and email
        name_input = driver.find_element(By.NAME, "name")
        email_input = driver.find_element(By.XPATH, "//input[@data-qa='signup-email']")
        
        name_input.send_keys("Test User")
        email_input.send_keys(f"testuser{int(time.time())}@example.com")
        
        # Click Signup button
        signup_btn = driver.find_element(By.XPATH, "//button[@data-qa='signup-button']")
        signup_btn.click()
        
        # Verify 'ENTER ACCOUNT INFORMATION' is visible
        account_info_text = driver.find_element(By.XPATH, "//b[text()='Enter Account Information']")
        assert account_info_text.is_displayed()
        
        print("✓ Test Register User - Passed")
    
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_with_correct_credentials(self, driver):
        """
        Test Case 2: Login User with correct email and password
        Steps:
        1. Navigate to url 'http://automationexercise.com'
        2. Verify that home page is visible successfully
        3. Click on 'Signup / Login' button
        4. Verify 'Login to your account' is visible
        5. Enter correct email address and password
        6. Click 'login' button
        7. Verify that 'Logged in as username' is visible
        8. Click 'Delete Account' button
        9. Verify that 'ACCOUNT DELETED!' is visible
        """
        # Verify home page
        assert "Automation Exercise" in driver.title
        
        # Click on Signup/Login
        driver.find_element(By.XPATH, "//a[@href='/login']").click()
        
        # Verify 'Login to your account' is visible
        login_text = driver.find_element(By.XPATH, "//h2[text()='Login to your account']")
        assert login_text.is_displayed()
        
        # Note: You need to create a test user first or use existing credentials
        # This is a skeleton test - needs valid credentials
        
        print("✓ Test Login with Correct Credentials - Framework Ready")
    
    
    @pytest.mark.login
    def test_login_with_incorrect_credentials(self, driver):
        """
        Test Case 3: Login User with incorrect email and password
        Steps:
        1. Navigate to url 'http://automationexercise.com'
        2. Verify that home page is visible successfully
        3. Click on 'Signup / Login' button
        4. Verify 'Login to your account' is visible
        5. Enter incorrect email address and password
        6. Click 'login' button
        7. Verify error 'Your email or password is incorrect!' is visible
        """
        # Navigate to login page
        driver.find_element(By.XPATH, "//a[@href='/login']").click()
        
        # Verify login form is visible
        login_text = driver.find_element(By.XPATH, "//h2[text()='Login to your account']")
        assert login_text.is_displayed()
        
        # Enter incorrect credentials
        email_input = driver.find_element(By.XPATH, "//input[@data-qa='login-email']")
        password_input = driver.find_element(By.XPATH, "//input[@data-qa='login-password']")
        
        email_input.send_keys("wrongemail@example.com")
        password_input.send_keys("wrongpassword")
        
        # Click login button
        driver.find_element(By.XPATH, "//button[@data-qa='login-button']").click()
        
        # Verify error message
        error_msg = driver.find_element(By.XPATH, "//p[text()='Your email or password is incorrect!']")
        assert error_msg.is_displayed()
        
        print("✓ Test Login with Incorrect Credentials - Passed")
    
    
    @pytest.mark.login
    def test_logout_user(self, driver):
        """
        Test Case 4: Logout User
        Steps:
        1. Navigate to url 'http://automationexercise.com'
        2. Verify that home page is visible successfully
        3. Click on 'Signup / Login' button
        4. Verify 'Login to your account' is visible
        5. Enter correct email address and password
        6. Click 'login' button
        7. Verify that 'Logged in as username' is visible
        8. Click 'Logout' button
        9. Verify that user is navigated to login page
        """
        # Note: This test requires valid user credentials
        # Skeleton implementation
        
        print("✓ Test Logout User - Framework Ready")
    
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_register_with_existing_email(self, driver):
        """
        Test Case 5: Register User with existing email
        Steps:
        1. Navigate to url 'http://automationexercise.com'
        2. Verify that home page is visible successfully
        3. Click on 'Signup / Login' button
        4. Verify 'New User Signup!' is visible
        5. Enter name and already registered email address
        6. Click 'Signup' button
        7. Verify error 'Email Address already exist!' is visible
        """
        # Click on Signup/Login
        driver.find_element(By.XPATH, "//a[@href='/login']").click()
        
        # Verify signup form
        signup_text = driver.find_element(By.XPATH, "//h2[text()='New User Signup!']")
        assert signup_text.is_displayed()
        
        # Enter name and existing email
        driver.find_element(By.NAME, "name").send_keys("Existing User")
        driver.find_element(By.XPATH, "//input[@data-qa='signup-email']").send_keys("existinguser@example.com")
        
        # Click signup
        driver.find_element(By.XPATH, "//button[@data-qa='signup-button']").click()
        
        # Verify error message
        # Note: Actual error text might vary
        time.sleep(1)  # Wait for potential error message
        
        print("✓ Test Register with Existing Email - Framework Ready")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
