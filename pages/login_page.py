"""
Login Page Object Model
Contains all locators and methods for Login/Signup page
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    
    # CONTAINER_LOGIN_SIGNUP = (By.XPATH, "//section[@id='form']//div[@class='row']")
    # Login Form
    LOGIN_TITLE = (By.XPATH, "//h2[normalize-space()='Login to your account']")
    EMAIL_FORM_LOGIN =  (By.CSS_SELECTOR, "input[data-qa='login-email']")
    PASSWORD_FORM = (By.CSS_SELECTOR, "input[placeholder='Password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    LOGIN_ERROR_MESSAGE = (By.XPATH, "//p[normalize-space()='Your email or password is incorrect!']")
    # SUCCES_MESSAGE = (By.CSS_SELECTOR, ".flash.success")
    
    SIGNUP_TITLE = (By.XPATH, "//h2[normalize-space()='New User Signup!']")
    NAME_FORM = (By.CSS_SELECTOR, "input[placeholder='Name']")
    EMAIL_FORM_SIGNUP = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-qa='signup-button']")
    
    def is_login_section_visible(self):
        return self.is_element_visible(self.LOGIN_TITLE)
    
    def is_signup_section_visible(self):
        return self.is_element_visible(self.SIGNUP_TITLE)
    
    def login(self, email, password):
        self.input_text(self.EMAIL_FORM_LOGIN, email)
        self.input_text(self.PASSWORD_FORM, password)
        self.click(self.LOGIN_BUTTON)
        self.logger.info(f"Attempted with email {email}")
        
    def signup(self, name, email):
        self.input_text(self.NAME_FORM, name)
        self.input_text(self.EMAIL_FORM_SIGNUP, email)
        self.click(self.SIGNUP_BUTTON)
        self.logger.info(f"Attempted with name {name}, email {email}")
        
    def is_login_error_displayed(self):
        return self.is_element_visible(self.LOGIN_ERROR_MESSAGE)
    
    def get_login_error(self):
        if self.is_login_error_displayed():
            return self.get_text(self.LOGIN_ERROR_MESSAGE, timeout=3)
        return None
    
    def enter_username(self, username):
        self.input_text(self.USERNAME_INPUT, username)
        
    def enter_password(self, password):
        self.input_text(self.PASSWORD_INPUT, password)
        
    def click_login_button(self):
        self.click(self.LOGIN_BUTTON)
        
    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        
    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)
    
    def get_succes_message(self):
        return self.get_text(self.SUCCES_MESSAGE)
    
    
    