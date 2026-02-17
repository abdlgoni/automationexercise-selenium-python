
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class SignupPage(BasePage):
    
    ACCOUNT_INFO_TITLE = (By.XPATH,"//b[normalize-space()='Enter Account Information']")
    
    # Title
    
    TITLE_MR = (By.ID, "id_gender1")
    TITLE_MRS = (By.ID, "id_gender2")
    
    # NAME
    NAME_FIELD = (By.ID, "name")
    
    # Email
    EMAIL_FIELD = (By.ID, "email")
    
    # Password
    PASSWORD_FIELD = (By.ID, "password")
    
    # Date of birth dropdown
    DAY_DROPDOWN = (By.ID, "days")
    MONTH_DROPDOWN = (By.ID, "months")
    YEAR_DROPDOWN = (By.ID, "years")
    
    NEWSLETTER_CHECKBOX = (By.ID, "uniform-newsletter")
    SPECIAL_OFFER_CHECKBOX = (By.ID, "uniform-optin")
    
    # Address information
    ADDRESS_INFORMATION_TITLE = (By.XPATH, "//b[normalize-space()='Address Information']")
    FIRST_NAME_FIELD = (By.ID, "first_name")
    LAST_NAME_FIELD = (By.ID, "last_name")
    COMPANY_FIELD = (By.ID, "company")
    ADDRESS1_FIELD = (By.ID, "address1")
    ADDRESS2_FIELD = (By.ID, "address2")
    COUNTRY_DROPDOWN = (By.ID, "country")
    STATE_FIELD = (By.ID, "state")
    CITY_FIELD = (By.ID, "city")
    ZIPCODE_FIELD = (By.ID, "zipcode")
    MOBILE_NUMBER_FIELD = (By.ID, "mobile_number")
    
    # CREATE ACCOUNT BUTTON
    CREATE_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[data-qa='create-account']")
    
    ACCOUNT_CREATED_TITLE = (By.XPATH, "//b[normalize-space()='Account Created!']")
    ACCOUNT_CREATED_MESSAGE = (By.XPATH, "//p[contains(text(),'You can now take advantage of member privileges to')]")
    CONTINUE_BUTTON = (By.XPATH, "//a[normalize-space()='Continue']")
    
    ACCOUNT_DELETE_TITLE = (By.XPATH, "//b[normalize-space()='Account Deleted!']") 
    ACCOUNT_DELETE_MESSAGE = (By.XPATH, "//p[contains(text(),'You can create new account to take advantage of me')]")
    CONTINUE_DELETE_BUTTON = ()
    
    def is_account_info_page_displayed(self):
        """
        Verify bahwa ada di halaman account information
        Return: Boolean
        """
        return self.is_element_visible(self.ACCOUNT_INFO_TITLE)
    
    def select_title(self, title):
        """
        Select gender title (Mr. atau Mrs.)
        Args:
            title: 'Mr' atau 'Mrs'
        """
        if title.lower() == 'mr':
            self.click(self.TITLE_MR)
            self.logger.info("Selected title Mr")
        elif title.lower() == 'mrs':
            self.click(self.TITLE_MRS)
            self.logger.info("Selected title Mrs")
        else:
            self.logger.error(f"Invalid: {title}. Use 'Mr' or 'Mrs' ")
            
    def enter_password(self, password):
        """
        Enter password
        Args:
            password: Password string
        """
        self.input_text(self.PASSWORD_FIELD, password)
        self.logger.info("Entered password")
        
    def select_date_of_birth(self, day, month, year):
        """
        Select date of birth dari dropdown
        Args:
            day: Day as string (e.g., '15')
            month: Month name as string (e.g., 'January')
            year: Year as string (e.g., '1990')
        """
        day_select = Select(self.find_element(self.DAY_DROPDOWN))
        day_select.select_by_value(day)
        
        month_select = Select(self.find_element(self.MONTH_DROPDOWN))
        month_select.select_by_visible_text(month)
        
        year_select = Select(self.find_element(self.YEAR_DROPDOWN))
        year_select.select_by_value(year)
        
        self.logger.info(f"Selcted date of birth {day}/{month}/{year}")
        
    def check_newsletter(self):
        newsletter = self.find_element(self.NEWSLETTER_CHECKBOX)
        if not newsletter.is_selected:
            self.click(self.NEWSLETTER_CHECKBOX)
            self.logger.info("Checked newsletter checkbox")
            
    def check_special_offer(self):
        offer = self.find_element(self.SPECIAL_OFFER_CHECKBOX)
        if not offer.is_selected:
            self.click(self.SPECIAL_OFFER_CHECKBOX)
            self.logger.info("Checked special info")
            
    def enter_first_name(self, first_name):
        """Enter First Name"""
        self.input_text(self.FIRST_NAME_FIELD, first_name)
        
    def enter_last_name(self, last_name):
        """Enter Last Name"""
        self.input_text(self.LAST_NAME_FIELD, last_name)
        
    def enter_company(self, company):
        """Enter Company"""
        self.input_text(self.COMPANY_FIELD, company)
        
    def enter_address1(self, address1):
        """Enter Address1"""
        self.input_text(self.ADDRESS1_FIELD, address1)
        
    def enter_address2(self, address2):
        """Enter Address2"""
        self.input_text(self.ADDRESS2_FIELD, address2)

    def select_country(self, country):
        """
        Select country dari dropdown
        Args:
            country: Country name (e.g., 'India', 'United States', 'Canada')
        """
        country_select = Select(self.find_element(self.COUNTRY_DROPDOWN))
        country_select.select_by_visible_text(country)
        self.logger.info(f"Selected country {country}")
        
    def enter_state(self, state):
        """Enter State"""
        self.input_text(self.STATE_FIELD, state)
        
    def enter_city(self, city):
        """Enter City"""
        self.input_text(self.CITY_FIELD, city)
        
    def enter_zipcode(self, zipcode):
        """Enter Zipcode"""
        self.input_text(self.ZIPCODE_FIELD, zipcode)
        
    def enter_mobile_number(self, number):
        """Enter Mobile Number"""
        self.input_text(self.MOBILE_NUMBER_FIELD, number)
        
    def click_create_account(self):
        """Click Create Account Button"""
        self.click(self.CREATE_ACCOUNT_BUTTON)
        self.logger.info("Clicked Create Account Button")
        
    def is_account_created_successfully(self):
        """
        Verify bahwa account berhasil dibuat
        Returns: Boolean
        """
        return self.is_element_visible(self.ACCOUNT_CREATED_TITLE)
    
    def get_account_created_message(self):
        """
        Get success message text
        Returns: Message string
        """
        if self.is_account_created_successfully():
            return self.get_text(self.ACCOUNT_CREATED_MESSAGE)
        return None
    
    def click_continue(self):
        """Click Continue button after account creation"""
        self.click(self.CONTINUE_BUTTON)
        self.logger.info("Clicked Continue Button")
        
    
        
    