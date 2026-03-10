"""
Detail Product Page Object Model
Contains all locators and methods for detail product page    
 """
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException
import logging

class DetailProductPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        
    PRODUCT_DETAIL_SECTION = (By.CSS_SELECTOR, "product-information")
    
    PRODUCT_NAME = (By.XPATH, "//div[@class='product-information']//h2")
    PRODUCT_CATEGORY = (By.XPATH, "//div[@class='product-information']//p[contains(text(), 'Category:')]")
    PRODUCT_PRICE = (By.XPATH, "//div[@class='product-information']//span/span")
    PRODUCT_AVAILABILITY = (By.XPATH, "//div[@class='product-information']//p[contains(text(), 'Availability:')]")
    PRODUCT_CONDITION = (By.XPATH, "//div[@class='product-information']//p[contains(text(), 'Condition:')]")
    PRODUCT_BRAND = (By.XPATH, "//div[@class='product-information']//p[contains(text(), 'Brand:')]")
    
    PRODUCT_MAIN_IMAGE = (By.XPATH, "//div[@class='view-product']//img")
    
    QUANTITY_INPUT = (By.ID, "quantity")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[@type='button' and contains(@class, 'cart')]")
   
    
    def is_product_detail_page_visible(self, timeout=10):
        
        try:
            detail_visible = self.is_element_visible(
                self.PRODUCT_DETAIL_SECTION, timeout=timeout)
             
            if detail_visible:
                self.logger.info("Product detail page is visible")
                return True
            else:
                self.logger.error("Product detail page not visible")
                 
        except TimeoutException:
            self.logger.error("Timed out waiting for All Products title to be visible")
            return False
        
    def get_product_name(self):
        
        try:
            name = self.get_text(self.PRODUCT_NAME, timeout=10)
            self.logger.info(f"Found Product name {name}")
            return name
        
        except Exception as e:
            self.logger.error(f"Failed to get product name {e}")
            return None
        
    def get_product_category(self):
        
        try:
            full_text = self.get_text(self.PRODUCT_CATEGORY)
            
            category = full_text.replace("Category:", "").strip()
            self.logger.info(f"Product category {category}")
            return category
        
        except Exception as e:
            self.logger.error(f"Failed to get category {e}")
            return None
        
    def get_product_price(self):
        
        try:
            price = self.get_text(self.PRODUCT_PRICE)
            self.logger.info(f"Product price: {price}")
            return price
        
        except Exception as e:
            self.logger.error(f"Failed to get price {e}")
            return None
        
    def get_product_avaibility(self):
        
        try:
            full_text = self.get_text(self.PRODUCT_AVAILABILITY)
            
            avaibility = full_text.replace("Avaibility:", "").strip()
            self.logger.info(f"Product Avaibility: {avaibility}")
            return avaibility
        
        except Exception as e:
            self.logger.error(f"Failed to get avaibility {e}")
            return None
        
    def get_product_condition(self):
        
        try:
            
            full_text = self.get_text(self.PRODUCT_CONDITION)
            
            condition = full_text.replace("Condition:", "").strip()
            self.logger.info(f"Product condition: {condition}")
            return condition
        except Exception as e:
            self.logger.error(f"Failed to get condition {e}")
            return None
        
    def get_product_brand(self):
        
        try:
            
            full_text = self.get_text(self.PRODUCT_BRAND)
            
            brand = full_text.replace("Brand:", "").strip()
            self.logger.info(f"Product brand {brand}")
            return brand
        
        except Exception as e:
            self.logger.error(f"Failed to get brand {e}")
            return None
        
    def get_all_product_detail(self):
        
        details={
            'name': self.get_product_name(),
            'category': self.get_product_category(),
            'price': self.get_product_price(),
            'avaibility': self.get_product_avaibility(),
            'condition': self.get_product_condition(),
            'brand': self.get_product_brand()
        }
        
        self.logger.info("Retrieved all product detail")
        return details
    
    def verify_product_detail_visible(self):
        
        details_check = {
            'name': self.is_element_visible(self.PRODUCT_NAME, timeout=5),
            'category': self.is_element_visible(self.PRODUCT_CATEGORY, timeout=5),
            'price': self.is_element_visible(self.PRODUCT_PRICE, timeout=5),
            'avaibility': self.is_element_visible(self.PRODUCT_PRICE, timeout=5),
            'condition': self.is_element_visible(self.PRODUCT_CONDITION, timeout=5),
            'brand': self.is_element_visible(self.PRODUCT_BRAND, timeout=5)
        }
        
        all_visible = all(details_check.values())
        
        # Log results
        for detail, visible in details_check.items():
            status = "✓" if visible else "❌"
            self.logger.info(f"{status} {detail.capitalize()}: {'Visible' if visible else 'NOT visible'}")
        
        if all_visible:
            self.logger.info("✓ All product details are visible")
        else:
            missing = [k for k, v in details_check.items() if not v]
            self.logger.error(f"Missing details: {', '.join(missing)}")
        
        return {
            'all_visible': all_visible,
            'details': details_check,
            'missing': [k for k, v in details_check.items() if not v]
        }
    
    def is_product_image_visible(self):
        """Check if product image is visible"""
        return self.is_element_visible(self.PRODUCT_MAIN_IMAGE, timeout=5)
    
    def add_to_cart(self, quantity=1):
        """
        Add product to cart
        
        Args:
            quantity: Quantity to add (default: 1)
            
        Returns:
            Boolean - True if added successfully
        """
        try:
            # Set quantity if not 1
            if quantity != 1:
                self.input_text(self.QUANTITY_INPUT, str(quantity))
            
            # Click add to cart
            self.click(self.ADD_TO_CART_BUTTON)
            self.logger.info(f"Added {quantity} to cart")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add to cart: {e}")
            return False