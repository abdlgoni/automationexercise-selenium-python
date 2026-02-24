import pytest
from selenium import webdriver
from pages.login_page import LoginPage

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self):    
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        
        yield
        
        self.driver.quit()
    def test_login_with_valid_credential(self):
        self.login_page.open()
        self.login_page.login("tomsmith", "SuperSecretPassword!")
        succes_message = self.login_page.get_succes_message()
        assert "You logged into a secure area!" in succes_message
        
    def test_login_with_invalid_username(self):
        self.login_page.open()
        self.login_page.login("Azis", "SuperSecretPassword!")
        error_message = self.login_page.get_error_message()
        assert "Your username is invalid!" in error_message
        
    def test_login_with_invalid_password(self):
        self.login_page.open()
        self.login_page.login("Tomsmith", "Azis123")
        error_message = self.login_page.get_error_message()
        assert "Your password is invalid!" in error_message
        
            