"""
Search Result Page Object Model
Contains all locators and methods for search result page     
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

class SearchResultPage(BasePage):
    """Page Object for Search Results page"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
    
    # ==================== LOCATORS ====================
    SEARCHED_PRODUCTS_TITLE = (By.XPATH, "//h2[normalize-space()='Searched Products']")
    FEATURES_ITEMS = (By.CSS_SELECTOR, ".features_items")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".productinfo.text-center")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".productinfo p")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".productinfo h2")
    
    # ==================== VERIFICATION METHODS ====================
    
    def is_searched_products_page_visible(self, timeout=15):
        """Verify if 'SEARCHED PRODUCTS' title is visible"""
        return self.is_element_visible(self.SEARCHED_PRODUCTS_TITLE, timeout=timeout)
    
    def get_searched_products_title(self):
        """Get the 'SEARCHED PRODUCTS' title text"""
        try:
            return self.get_text(self.SEARCHED_PRODUCTS_TITLE)
        except Exception as e:
            self.logger.error(f"Failed to get title: {e}")
            return None
    
    def is_products_result_visible(self, timeout=15):
        """Verify container is visible and has at least one product"""
        try:
            container_visible = self.is_element_visible(self.FEATURES_ITEMS, timeout=timeout)
            products = self.get_all_search_results()
            
            if container_visible and len(products) > 0:
                self.logger.info(f"✓ Search results visible with {len(products)} product(s)")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error checking search results: {e}")
            return False
    
    def get_all_search_results(self):
        """Get all product elements from search results"""

        try:
            products = self.find_elements(self.PRODUCT_CARDS)
            self.logger.info(f"Found {len(products)} product(s) in search results")
            return products
        except Exception as e:
            self.logger.warning(f"No products found or error occurred: {e}")
            return []
    
    def get_search_results_count(self):
        """Get count of products in search results"""
        return len(self.get_all_search_results())
    
    def get_product_names_from_results(self):
        """Get all product names from search results"""
        product_names = []
        try:
            name_elements = self.find_elements(self.PRODUCT_NAMES)
            
            for element in name_elements:
                name = element.text.strip()
                if name:
                    product_names.append(name)
            
            self.logger.info(f"Extracted {len(product_names)} product names")
            return product_names
        except Exception as e:
            self.logger.error(f"Failed to get product names: {e}")
            return []
    
    def verify_search_results_contain_term(self, search_term):
        """Verify that at least one product name matches the search term"""
        product_names = self.get_product_names_from_results()
        
        if not product_names:
            return False
        
        search_term_lower = search_term.lower()
        matching_products = [name for name in product_names if search_term_lower in name.lower()]
        
        if matching_products:
            self.logger.info(f"Found {len(matching_products)} matching '{search_term}'")
            return True
        
        self.logger.error(f"No products matching '{search_term}' found")
        return False