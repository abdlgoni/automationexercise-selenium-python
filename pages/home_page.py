"""
Page Object Model untuk automation exercise Homepage (automationexercise.com)
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException
from utils.config import Config
import logging
import time


class HomePage(BasePage):
    
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
    
    LOGO = (By.CSS_SELECTOR, ".logo ") 
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
    FEATURES_ITEMS = (By.CLASS_NAME, "features_items")
    PRODUCT_ITEMS = (By.CLASS_NAME, "product-image-wrapper")
    
    # View Product button (menggunakan text)
    VIEW_PRODUCT_BUTTONS = (By.CLASS_NAME, "choose")
    
    # Add to cart button
    ADD_TO_CART_BUTTON_OVERLAY = (By.CSS_SELECTOR,".product-overlay .add-to-cart")
    
    # View Cart link (muncul setelah add to cart)
    VIEW_CART_MODAL = (By.CSS_SELECTOR, ".modal-content")
    # Continue Shopping button (muncul setelah add to cart)
    CONTINUE_SHOPPING_BTN = (By.CSS_SELECTOR, ".btn.btn-success.close-modal.btn-block")
    VIEW_CART_LINK = (By.XPATH, "//body//section//p[2]")
    
    
    # ==================== SUBSCRIPTION SECTION ====================
    # Footer subscription form
    SUBSCRIPTION_TITLE = (By.XPATH, "//h2[contains(text(), 'Subscription')]")
    SUBSCRIPTION_EMAIL = (By.ID, "susbscribe_email")  
    SUBSCRIPTION_BUTTON = (By.ID, "subscribe")
    SUBSCRIPTION_SUCCESS = (By.XPATH, "//div[contains(@class, 'alert-success')]")
    
    # ==================== FOOTER ====================
    FOOTER = (By.ID, "footer")
    SCROLL_UP_BUTTON = (By.ID, "scrollUp")
    
    PAGE_READY_LOCATOR = LOGO
    
    # ========== Page Actions ==========
    
    def open(self):
        """
        Open automation exercise homepage
        """
        self.open_url(self.url)
        self.logger.info(f"Opened homepage: {self.url}")
    
    def is_homepage_visible(self, timeout=15):
        
        try:
            homepage_visible = self.is_element_visible(
                self.LOGO, timeout=timeout
            )
            
            if homepage_visible:
                self.logger.info("Homepage is visible")
                return True
            else:
                self.logger.error("Homepage not visible")
                
        except TimeoutException:
            self.logger.error("Timed out waiting for homepage visible")
    
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
        return self.is_element_visible(self.LOGGED_IN_AS)
    
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
        self.click(self.VIDEO_TUTORIALS_LINK)
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
            self.click(category_map[category_name])
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
            self.scroll_to_element(brand_map[brand_name])
            self.click(brand_map[brand_name])
            self.logger.info(f"Clicked {brand_name} brand")
            
        else:
            self.logger.error(f"Clicked {brand_name} Not Found")

    def is_product_list_visible(self, timeout=10):
        
        try:
            products_container = self.find_elements(self.FEATURES_ITEMS, timeout=timeout)

            products = self.get_all_products()
            products_count = len(products)
            
            if products_container and products_count > 0:
                self.logger.info(f"Products list visible with {products_count} products")
                return True
            else:
                self.logger.error("Product list not visible or empty")
                return False
            
        except Exception as e:
            self.logger.error(f"Error checking product list: {e}")
            return False

    def get_all_products(self):

        try:
            products = self.find_elements(self.PRODUCT_ITEMS)
            self.logger.info(f"Found {len(products)} products on page")
            return products
        except Exception as e:
            self.logger.error(f"No product found: {e}")
            return []
    
    def get_product_count(self):

        products = self.get_all_products()
        return len(products)
        
    def click_view_product_by_index(self, index=0):
        try:
            view_buttons = self.find_elements(self.VIEW_PRODUCT_BUTTONS)
            
            if index < len(view_buttons):
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true);",
                    view_buttons[index]
                )
                time.sleep(0.5)
                view_buttons[index].click()
                self.logger.info(f"Clicked View Product for product index {index}")
                return True
            else:
                self.logger.error(
                    f"Product index {index} out of range "
                    f"(only {len(view_buttons)} products available)"
                )
                return False
        except Exception as e:
            self.logger.error(f"Failed to click View Product: {e}")
            return False

    def add_to_cart_by_index(self, index=0):
        try:
            
            products = self.find_elements(
                self.PRODUCT_ITEMS
            )

            if index >= len(products):
                return False
            
            product = products[index]

            self.driver.execute_script(
                "argument[0].scrollintoview(true)",
                product
            )
            time.sleep(0.5)

            actions = ActionChains(self.driver)
            actions.move_to_element(product).perform()
            time.sleep(0.5)

            add_btn = product.find_element(*self.ADD_TO_CART_BUTTON_OVERLAY)
            add_btn.click()
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to add to cart: {e}")
            return False

    def is_modal_content_visible(self):
        return self.is_element_visible(self.VIEW_CART_MODAL)
    
    def click_continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BTN)
        self.logger.info("Clicked Continue Shopping button")
                      

    def click_view_cart(self):
        self.click(self.VIEW_CART_LINK)
        self.logger.info("Clicked View Cart link")


    def is_subscription_text_visible(self, timeout=5):
        """
        Check if subscription text is visible
        Returns: Boolean (True if visible, False otherwise)
        """
        return self.is_element_visible(self.SUBSCRIPTION_TITLE, timeout=timeout)
    
    def subscribe_email(self, email):
        """
        Subscribe dengan email di footer
        Args:
            email: Email address untuk subscribe
        Returns: Boolean (success atau tidak)
        """
        self.input_text(self.SUBSCRIPTION_EMAIL, email)
        self.click(self.SUBSCRIPTION_BUTTON)
        self.logger.info(f"Subscribed with email: {email}")

        return self.is_element_visible(self.SUBSCRIPTION_SUCCESS, timeout=3)

    def get_subscription_success_message(self):
        """
        Get subscription success message
        Returns: String (subscription success message)
        """
        return self.get_text(self.SUBSCRIPTION_SUCCESS)
    
    def scroll_to_footer(self):
        """Scroll ke bagian footer"""
        self.scroll_to_element(self.FOOTER)
        self.logger.info("Scrolled to footer")
    
    def click_scroll_up(self):
        """Click scroll up button untuk kembali ke top"""
        if self.is_element_visible(self.SCROLL_UP_BUTTON):
            self.click(self.SCROLL_UP_BUTTON)
            self.logger.info("Clicked scroll up button")
