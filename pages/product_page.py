"""
Product Page Object Model
Contains all locators and methods for product page    
 """
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException
import logging
import time

class ProductPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        
    ALL_PRODUCTS_TITLE = (By.XPATH, "//h2[@class='title text-center' and contains(text(), 'All Products')]")
    FEATURES_ITEMS = (By.CSS_SELECTOR, ".features_items")

    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".product-image-wrapper")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".productinfo.text-center")

    VIEW_PRODUCT_BUTTON = (By.XPATH, "//a[contains(text(),'View Product')]")
    
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")
    
    def is_all_products_page_visible(self, timeout=10):
        
        try:
            title_visible = self.is_element_visible(self.ALL_PRODUCTS_TITLE, timeout=timeout)
            
            if title_visible:
                self.logger.info("All Products page is visible")
                return True
            else:
                self.logger.error("All Products title is not visible")
                return False
            
        except TimeoutException:
            self.logger.error("Timed out waiting for All Products title to be visible")
            return False
        
    def get_all_products_title(self):
        return self.get_text(self.ALL_PRODUCTS_TITLE)
    
    
    def is_product_list_visible(self, timeout=10):
        
        try:
            container_visible = self.is_element_visible(self.FEATURES_ITEMS, timeout=timeout)
            
            products = self.get_all_products()
            products_count = len(products)
                        
            if container_visible and products_count > 0:
                self.logger.info(f"Products list visible with {products_count} products")
                return True
            else:
                self.logger.error("Product list not visible or empty")
                return False
            
        except Exception as e:
            self.logger.error(f"Error Checking product list: {e}")
            return False
        
    def get_all_products(self):
        
        try:
            products = self.find_elements(self.PRODUCT_CARDS)
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
            
            view_buttons = self.find_elements(
                self.VIEW_PRODUCT_BUTTON
            )
            
            if index < len(view_buttons):
                
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true);",
                    view_buttons[index]
                )
            
                time.sleep(0.5)
                
                view_buttons[index].click()
                self.logger.info(f"✓ Clicked View Product for product index {index}")
                return True
            
            else:
                self.logger.error(
                    f"❌ Product index {index} out of range "
                    f"(only {len(view_buttons)} products available)"
                )
                return False
            
        except Exception as e:
            self.logger.error(f"❌ Failed to click View Product: {e}")
            return False
        
    
    def search_product(self, search_term):
        """
        Search for products
        
        Args:
            search_term: Text to search for
            
        Returns:
            Boolean - True if search executed
        """
        try:
            self.input_text(self.SEARCH_INPUT, search_term)
            self.click(self.SEARCH_BUTTON)
            self.logger.info(f"✓ Searched for: {search_term}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Search failed: {e}")
            return False
        