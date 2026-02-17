"""
Page Object Model untuk automation exercise Homepage (automationexercise.com)
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import Config
import logging


class HomePage(BasePage):
    """Page Object untuk Wikipedia Homepage"""
    
    def __init__(self, driver):
        """
        Initialize HomePage
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        self.url = Config.BASE_URL
        self.logger = logging.getLogger(__name__)
    
    # ========== Locators ==========
    
    # ==================== NAVIGATION MENU ====================
    # Text-based locator untuk menu items (karena tidak ada ID/class unik)
    
    HOME_LINK = (By.XPATH, "//a[contains(@href, '/')]//i[@class='fa fa-home']/..")
    PRODUCTS_LINK = (By.XPATH, "//a[@href='/products']")
    CART_LINK = (By.XPATH, "//a[@href='/view_cart']")
    SIGNUP_LOGIN_LINK = (By.XPATH, "//a[@href='/login']")
    TEST_CASES_LINK = (By.XPATH, "//a[@href='/test_cases']")
    API_TESTING_LINK = (By.XPATH, "//a[@href='/api_list']")
    VIDEO_TUTORIALS_LINK = (By.XPATH, "//a[contains(@href, 'youtube')]")
    CONTACT_US_LINK = (By.XPATH, "//a[@href='/contact_us']")
    
    LOGGED_IN_AS = (By.XPATH, "//li[10]//a[1]")
    
    # Logout dan Delete Account (muncul setelah login)
    LOGOUT_LINK = (By.XPATH, "//a[@href='/logout']")
    DELETE_ACCOUNT_LINK = (By.XPATH, "//a[@href='/delete_account']")
    
    # Logged in as username (untuk verify login success)
    LOGGED_IN_AS = (By.XPATH, "//a[contains(text(), 'Logged in as')]")
    
    # ==================== HOMEPAGE SECTIONS ====================
    
    # Carousel/Slider
    CAROUSEL = (By.ID, "slider-carousel")
    
    # Features section
    FEATURES_ITEMS = (By.CLASS_NAME, "features_items")
    
    # Category section (left sidebar)
    CATEGORY_SECTION = (By.CLASS_NAME, "left-sidebar")
    WOMEN_CATEGORY = (By.XPATH, "//a[@href='#Women']")
    MEN_CATEGORY = (By.XPATH, "//a[@href='#Men']")
    KIDS_CATEGORY = (By.XPATH, "//a[@href='#Kids']")
    
    # Women subcategories (expand saat diklik)
    WOMEN_DRESS = (By.XPATH, "//a[@href='/category_products/1']")
    WOMEN_TOPS = (By.XPATH, "//a[@href='/category_products/2']")
    WOMEN_SAREE = (By.XPATH, "//a[@href='/category_products/7']")
    
    # Men subcategories
    MEN_TSHIRTS = (By.XPATH, "//a[@href='/category_products/3']")
    MEN_JEANS = (By.XPATH, "//a[@href='/category_products/6']")
    
    # Kids subcategories
    KIDS_DRESS = (By.XPATH, "//a[@href='/category_products/4']")
    KIDS_TOPS_SHIRTS = (By.XPATH, "//a[@href='/category_products/5']")
    
    # Brands section (left sidebar)
    BRANDS_SECTION = (By.CLASS_NAME, "brands_products")
    
    # Individual brands (menggunakan href karena tidak ada ID)
    POLO_BRAND = (By.XPATH, "//a[@href='/brand_products/Polo']")
    HM_BRAND = (By.XPATH, "//a[@href='/brand_products/H&M']")
    MADAME_BRAND = (By.XPATH, "//a[@href='/brand_products/Madame']")
    MAST_HARBOUR_BRAND = (By.XPATH, "//a[@href='/brand_products/Mast & Harbour']")
    BABYHUG_BRAND = (By.XPATH, "//a[@href='/brand_products/Babyhug']")
    ALLEN_SOLLY_BRAND = (By.XPATH, "//a[@href='/brand_products/Allen Solly Junior']")
    KOOKIE_KIDS_BRAND = (By.XPATH, "//a[@href='/brand_products/Kookie Kids']")
    BIBA_BRAND = (By.XPATH, "//a[@href='/brand_products/Biba']")
    
    # ==================== PRODUCTS SECTION ====================
    
    # Product items di homepage (recommended products)
    PRODUCT_ITEMS = (By.CLASS_NAME, "product-image-wrapper")
    
    # View Product button (menggunakan text)
    VIEW_PRODUCT_BUTTONS = (By.CLASS_NAME, "choose")
    
    # Add to cart button
    ADD_TO_CART_BUTTONS = (By.XPATH, "//a[@class='btn btn-default add-to-cart']")
    
    # Continue Shopping button (muncul setelah add to cart)
    CONTINUE_SHOPPING_BTN = (By.XPATH, "//button[contains(text(), 'Continue Shopping')]")
    
    # View Cart link (muncul setelah add to cart)
    VIEW_CART_MODAL = (By.XPATH, "//a[@href='/view_cart']//u[contains(text(), 'View Cart')]")
    
    # ==================== SUBSCRIPTION SECTION ====================
    # Footer subscription form
    SUBSCRIPTION_TITLE = (By.XPATH, "//h2[contains(text(), 'Subscription')]")
    SUBSCRIPTION_EMAIL = (By.ID, "susbscribe_email")  # Note: typo di website (susbscribe)
    SUBSCRIPTION_BUTTON = (By.ID, "subscribe")
    SUBSCRIPTION_SUCCESS = (By.XPATH, "//div[contains(@class, 'alert-success')]")
    
    # ==================== FOOTER ====================
    FOOTER = (By.ID, "footer")
    SCROLL_UP_BUTTON = (By.ID, "scrollUp")
    
    # ========== Page Actions ==========
    
    def open(self):
        """
        Open Wikipedia homepage
        """
        self.open_url(self.url)
        self.wait_for_page_load()
        self.logger.info(f"Opened homepage: {self.url}")
    
    def click_signup_login(self):
        """
        Navigate to Signup/login page
        """
        self.click(self.SIGNUP_LOGIN_LINK)
        self.logger.info("Clicked Signup/Login Link")
    
    def click_products(self):
        """
        Navigate to Products page
        """
        self.click(self.PRODUCTS_LINK)
        self.logger.info("Clicked Product Link")
        
    def click_cart(self):
        """
        Navigate to cart page
        """
        self.click(self.CART_LINK)
        self.logger.info("Clicked Cart Link")
    
    def click_logout(self):
        self.click(self.LOGOUT_LINK)
        self.logger.info("Clicked Logout Link")
        
    def click_delete_account(self):
        self.click(self.DELETE_ACCOUNT_LINK)
        self.logger.info("Clicked Delete Account")
        
    def is_logged_in(self):
        return self.is_element_visible(self.LOGGED_IN_AS, timeout=3)
    
    def get_logged_in_username(self):
        """
        Get username dari 'Logged in as' text
        Returns: Username string
        """
        if self.is_logged_in():
            full_text = self.get_text(self.LOGGED_IN_AS)
            # Extract username dari "Logged in as username"
            return full_text.replace("Logged in as ", "").strip()
        return None
        
    def click_test_cases(self):
        """
        Navigate to Test Cases page
        """
        self.click(self.TEST_CASES_LINK)
        self.logger.info("Clicked Test Cases Link")
        
    def click_api_testing(self):
        """
        Navigate to API Testing page
        """
        self.click(self.API_TESTING_LINK)
        self.logger.info("Clicked API Testing Link")
        
    def click_video_tutorial(self):
        """
        Navigate to Video Tutorial page
        """
        self.click(self.VIDEO_TUTORIAL_LINK)
        self.logger.info("Clicked Video Tutorial Link")
        
    def click_contact_us(self):
        """
        Navigate to Contact Us page
        """
        self.click(self.CONTACT_US_LINK)
        self.logger.info("Clicked Contact Us Link")
    
    def click_category(self, category_name):
        """
        Click pada category untuk expand subcategories
        Args:
            category_name: 'Women', 'Men', atau 'Kids'
        """
        category_map ={
            'Women': self.WOMEN_CATEGORY,
            'Men': self.MEN_CATEGORY,
            'Kids': self.KIDS_CATEGORY
        }
        
        if category_name in category_map:
            self.click(category_map[category_map])
            self.logger.info(f"clicked {category_name} Category")
        else:
            self.logger.error(f"Clicked {category_name} Not Found")
            
    def click_brand(self, brand_name):
        """
        Click pada brands untuk filter products
        Args:
            brand_name: Nama brand (e.g., 'Polo', 'H&M')
        """
        brand_map = {
            'Polo': self.POLO_BRAND,
            'HM': self.HM_BRAND,
            'Madame': self.MADAME_BRAND,
            'Mast & Harboutr': self.MAST_HARBOUR_BRAND,
            'Babyhug': self.BABYHUG_BRAND,
            'Allen Solly Junior': self.ALLEN_SOLLY_BRAND,
            'Kookie Kids': self.KOOKIE_KIDS_BRAND,
            'Biba': self.BIBA_BRAND
        }
        
        if brand_name in brand_map:
            self.scroll_to_element(brand_map[brand_map])
            self.click(brand_map[brand_map])
            self.logger.info(f"Clicked {brand_name} brand")
            
        else:
            self.logger.error(f"Clicked {brand_name} Not Found")
    
    def subscribe_email(self, email):
        """
        Subscribe dengan email di footer
        Args:
            email: Email address untuk subscribe
        Returns: Boolean (success atau tidak)
        """
        self.scroll_to_element(self.SUBSCRIPTION_EMAIL)
        self.input_text(self.SUBSCRIPTION_EMAIL, email)
        self.click(self.SUBSCRIPTION_BUTTON)
        self.logger.info(f"Subscribed with email: {email}")
        
        # Check success message
        return self.is_element_visible(self.SUBSCRIPTION_SUCCESS, timeout=3)
    
    def scroll_to_footer(self):
        """Scroll ke bagian footer"""
        self.scroll_to_element(self.FOOTER)
        self.logger.info("Scrolled to footer")
    
    def click_scroll_up(self):
        """Click scroll up button untuk kembali ke top"""
        if self.is_element_visible(self.SCROLL_UP_BUTTON):
            self.click(self.SCROLL_UP_BUTTON)
            self.logger.info("Clicked scroll up button")