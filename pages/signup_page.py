
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
import logging


class SignupPage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
    
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
    
    ACCOUNT_CREATED_TITLE = (By.CSS_SELECTOR, "h2[data-qa='account-created']")
    ACCOUNT_CREATED_MESSAGE = (By.XPATH, "//p[contains(text(),'You can now take advantage of member privileges to')]")
    CONTINUE_BUTTON = (By.XPATH, "//a[normalize-space()='Continue']")
    
    ACCOUNT_DELETED_TITLE = (By.CSS_SELECTOR, "h2[data-qa='account-deleted']") 
    ACCOUNT_DELETED_MESSAGE = (By.XPATH, "//p[contains(text(),'You can create new account to take advantage of me')]")
    
    
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
            
    def check_special_offers(self):
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
            return self.get_text(self.ACCOUNT_CREATED_TITLE)
        return None
    
    def click_continue(self):
        """Click Continue button after account creation and deleted"""
        self.click(self.CONTINUE_BUTTON)
        self.logger.info("Clicked Continue Button")
        
    def is_account_deleted_successfully(self):
        """
        Verify bahwa account berhasil dibuat
        Returns: Boolean
        """
        return self.is_element_visible(self.ACCOUNT_DELETED_TITLE)
    
    def get_account_deleted_message(self):
        if self.is_account_deleted_successfully():
            return self.get_text(self.ACCOUNT_DELETED_TITLE)
        return None
        
    def fill_account_information(self, title, password, day, month, year, 
                                 newsletter=True, special_offers=True):
        """
        Fill semua Account Information section
        Args:
            title: 'Mr' atau 'Mrs'
            password: Password string
            day: Birth day (e.g., '15')
            month: Birth month (e.g., 'January')
            year: Birth year (e.g., '1990')
            newsletter: Boolean untuk newsletter checkbox
            special_offers: Boolean untuk special offers checkbox
        """
        self.select_title(title)
        self.enter_password(password)
        self.select_date_of_birth(day, month, year)
        
        if newsletter:
            self.check_newsletter()
        
        if special_offers:
            self.check_special_offers()
        
        self.logger.info("Filled account information section")
    
    def fill_address_information(self, first_name, last_name, company, 
                                 address1, address2, country, state, 
                                 city, zipcode, mobile):
        """
        Fill semua Address Information section
        Args:
            first_name: First name
            last_name: Last name
            company: Company name
            address1: Address line 1 (required)
            address2: Address line 2 (optional)
            country: Country name
            state: State name
            city: City name
            zipcode: Zipcode
            mobile: Mobile number
        """
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_company(company)
        self.enter_address1(address1)
        
        if address2:
            self.enter_address2(address2)
        
        self.select_country(country)
        self.enter_state(state)
        self.enter_city(city)
        self.enter_zipcode(zipcode)
        self.enter_mobile_number(mobile)
        
        self.logger.info("Filled address information section")
    
    def complete_registration(self, account_data, address_data):
        """
        Complete seluruh registration process
        Args:
            account_data: Dict dengan keys: title, password, day, month, year
            address_data: Dict dengan keys: first_name, last_name, company, 
                         address1, address2, country, state, city, zipcode, mobile
        
        Example:
            account_data = {
                'title': 'Mr',
                'password': 'Test@123',
                'day': '15',
                'month': 'January',
                'year': '1990'
            }
            
            address_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'company': 'ABC Corp',
                'address1': '123 Main St',
                'address2': 'Apt 4B',
                'country': 'United States',
                'state': 'California',
                'city': 'Los Angeles',
                'zipcode': '90001',
                'mobile': '+1234567890'
            }
        """
        # Fill account information
        self.fill_account_information(
            title=account_data.get('title', 'Mr'),
            password=account_data['password'],
            day=account_data['day'],
            month=account_data['month'],
            year=account_data['year'],
            newsletter=account_data.get('newsletter', True),
            special_offers=account_data.get('special_offers', True)
        )
        
        # Scroll to address section
        self.scroll_to_element(self.FIRST_NAME_FIELD)
        
        # Fill address information
        self.fill_address_information(
            first_name=address_data['first_name'],
            last_name=address_data['last_name'],
            company=address_data.get('company', ''),
            address1=address_data['address1'],
            address2=address_data.get('address2', ''),
            country=address_data['country'],
            state=address_data['state'],
            city=address_data['city'],
            zipcode=address_data['zipcode'],
            mobile=address_data['mobile']
        )
        
        # Scroll to and click Create Account button
        self.scroll_to_element(self.CREATE_ACCOUNT_BUTTON)
        self.click_create_account()
        
        self.logger.info("Completed full registration")
    
        
    