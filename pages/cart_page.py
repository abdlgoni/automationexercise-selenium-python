"""
Cart Page Object Model
Contains all locator and methods for cart page
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import logging


class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        
    CART_INFO_TABLE = (By.ID, "cart_info_table")
    SHOPPING_CART_TITLE = (By.CSS_SELECTOR, ".active")
    
    CART_ITEMS = (By.XPATH, "//tbody//tr")
    CART_PRODUCTS = (By.CSS_SELECTOR, "tr[id^='product-']")
    
    EMPTY_CART_MESSAGE = (By.ID, "empty_cart")
    
    PRODUCT_IMAGES = (By.XPATH, "//td[@class='cart_product']//img")
    PRODUCT_NAMES = (By.XPATH, "//td[@class='cart_description']//h4/a")
    PRODUCT_PRICES = (By.XPATH, "//td[@class='cart_price']//p")
    PRODUCT_QUANTITIES = (By.XPATH, "//td[@class='cart_quantity']//button")
    PRODUCT_TOTALS = (By.XPATH, "//td[@class='cart_total']//p")
    
    DELETE_BUTTONS = (By.XPATH, "//td[@class='cart_delete']//a")
    
    PROCEED_TO_CHECKOUT = (By.XPATH, "//a[contains(text(), 'Proceed To Checkout')]")

    CHECKOUT_MODAL = (By.CLASS_NAME, "modal-content")
    REGISTER_LOGIN_BUTTON = (By.LINK_TEXT, "Register / Login")
    CONTINUE_ON_CART = (By.CLASS_NAME, "modal-footer")

    SUBSCRIPTION_TITLE = (By.XPATH, "//h2[contains(text(), 'Subscription')]")
    SUBSCRIPTION_EMAIL = (By.ID, "susbscribe_email")
    SUBSCRIPTION_BUTTON = (By.ID, "subscribe")
    SUBSCRIPTION_SUCCESS = (By.XPATH, "//div[contains(@class, 'alert-success')]")

    FOOTER = (By.ID, "footer")
    
    PAGE_READY_LOCATOR = SHOPPING_CART_TITLE
    
    def is_cart_page_visible(self):
        
        try:
            table_visible = self.is_element_visible(self.SHOPPING_CART_TITLE)
            
            if table_visible:
                self.logger.info("Cart page is visible")
                return True
            else:
                self.logger.error("Cart page is not visible")
                return False
            
        except TimeoutException:
            self.logger.error("Timeout waiting for cart page")
            return False
        
    def is_cart_empty(self):
        
        try:
            empty_msg = self.is_element_present(self.EMPTY_CART_MESSAGE)
            if empty_msg:
                self.logger.info("Cart is empty")
                return True
            
            # Alternative Check if no products
            products = self.get_all_cart_products()
            if len(products) == 0:
                self.logger.info("Cart is empty (no products)")
                return True
            
            return False
            
        except Exception as e:
            self.logger.debug(f"Cart not empty: {e}")
            return False
        
    def get_all_cart_products(self):
        
        products = self.find_elements(self.CART_PRODUCTS)
        self.logger.info(f"Found {len(products)} in cart")
        return products
        
    def get_cart_products_count(self):
        
        products = self.get_all_cart_products()
        count = len(products)
        self.logger.info(f"Cart has {count} product(s)")
        return count
    
    def verify_products_count(self, expected_count):
        
        actual_count = self.get_cart_products_count()
        
        if actual_count == expected_count:
            self.logger.info(f"Cart has {expected_count} products(s) as expected")
            return True
        
        else:
            self.logger.error(
                f"Expected {expected_count} products."
                f"but found {actual_count}"
            )
        return False
    
    def get_product_names_from_cart(self):
        
        product_names = []
        
        try:
            
            name_element = self.find_elements(self.PRODUCT_NAMES)
            
            for element in name_element:
                try:
                    name = element.text.strip()
                    if name:
                        product_names.append(name)
                except:
                    continue
            
            self.logger.info(f"Extracted {len(product_names)} product names")
            return product_names
            
        except Exception as e:
            self.logger.error(f"Failed to get product names {e}")
            return []
        
    def get_product_price_from_cart(self):
        
        prices = []
        
        try:
            
            price_element = self.find_elements(self.PRODUCT_PRICES)
            
            for element in price_element:
                try:
                    price = element.text.strip()
                    if price:
                        prices.append(price)
                    
                except:
                    continue
                
            self.logger.info(f"Extracte {len(prices)} prices")
            return prices
        
        except Exception as e:
            self.logger.error(f"Failed to get prices: {e}")
            return []

    def get_product_quantities_from_cart(self):
        
        quantities = []
        
        try:
            
            quantity_element = self.find_elements(self.PRODUCT_QUANTITIES)
            
            for element in quantity_element:
                try:
                    quantity = element.text.strip()
                    if quantity:
                        quantities.append(quantity)
                    
                except:
                    continue
                
            self.logger.info(f"Extracte {len(quantities)} quantities")
            return quantities
        
        except Exception as e:
            self.logger.error(f"Failed to get quantities: {e}")
            return []

    def get_product_totals_from_cart(self):
        
        totals = []
        
        try:
            
            total_element = self.find_elements(self.PRODUCT_TOTALS)
            
            for element in total_element:
                try:
                    total = element.text.strip()
                    if total:
                        totals.append(total)
                    
                except:
                    continue
                
            self.logger.info(f"Extracte {len(totals)} totals")
            return totals
        
        except Exception as e:
            self.logger.error(f"Failed to get totals: {e}")
            return []

    def get_all_cart_details(self):
        
        cart_details = []
        
        try:
            names = self.get_product_names_from_cart()
            prices = self.get_product_price_from_cart()
            quantities = self.get_product_quantities_from_cart()
            totals = self.get_product_totals_from_cart()
            
            # Combine all data
            for i in range(len(names)):
                product = {
                    'name': names[i] if i < len(names) else 'Unknown',
                    'price': prices[i] if i < len(prices) else 'Unknown',
                    'quantity': quantities[i] if i < len(quantities) else 0,
                    'total': totals[i] if i < len(totals) else 'Unknown'
                }
                cart_details.append(product)
            
            self.logger.info(f"Extracted details for {len(cart_details)} products")
            return cart_details
            
        except Exception as e:
            self.logger.error(f"Failed to get cart details: {e}")
            return []
        
    def verify_product_in_cart(self, product_name):

        product_names = self.get_product_names_from_cart()
        
        for name in product_names:
            if product_name.lower() in name.lower():
                self.logger.info(f"Product '{product_name}' found in cart")
                return True
        
        self.logger.error(f"Product '{product_name}' not found in cart")
        return False
    
    def verify_product_price(self, index, expected_price):
        
        prices = self.get_product_price_from_cart()

        if index >= len(prices):
            self.logger.error(f"product index {index} out of range")
            return False
        
        actual_price = prices[index]
        
        if actual_price == expected_price:
            self.logger.info(f"Price {actual_price} matches expected price {expected_price}")
            return True
        
        else:
            self.logger.error(f"Price {actual_price} does not match expected price {expected_price}")
            return False

    def verify_product_quantity(self, index, expected_quantity):

        quantities = self.get_product_quantities_from_cart()

        if index >= len(quantities):
            self.logger.error(f"product index {index} out of range")
            return False
        
        actual_quantity = quantities[index]
        
        if actual_quantity == expected_quantity:
            self.logger.info(f"Quantity {actual_quantity} matches expected quantity {expected_quantity}")
            return True
        
        else:
            self.logger.error(f"Quantity {actual_quantity} does not match expected quantity {expected_quantity}")
            return False

    def verify_product_total(self, index, expected_total):

        totals = self.get_product_totals_from_cart()

        if index >= len(totals):
            self.logger.error(f"product index {index} out of range")
            return False
        
        actual_total = totals[index]
        
        if actual_total == expected_total:
            self.logger.info(f"Total {actual_total} matches expected total {expected_total}")
            return True
        
        else:
            self.logger.error(f"Total {actual_total} does not match expected total {expected_total}")
            return False

    def verify_all_product_details(self, index, expected_details):

        cart_details = self.get_all_cart_details()

        if index >= len(cart_details):
            self.logger.error(f"product index {index} out of range")
            return {
                'all_correct': False,
                'errors': [f'Index {index} out of range']
            }
        
        actual = cart_details[index]
        errors = []

        # Verify name
        if 'name' in expected_details:
            if expected_details['name'].lower() not in actual['name'].lower():
                errors.append(
                    f"Name mismatch: expected '{expected_details['name']}', "
                    f"got '{actual['name']}'"
                )
        
        if 'price' in expected_details:
            if expected_details['price'] != actual['price']:
                errors.append(
                    f"Price mismatch: expected '{expected_details['price']}', "
                    f"got '{actual['price']}'"
                )
        
        if 'quantity' in expected_details:
            if expected_details['quantity'] != actual['quantity']:
                errors.append(
                    f"Quantity mismatch: expected '{expected_details['quantity']}', "
                    f"got '{actual['quantity']}'"
                )
        
        if 'total' in expected_details:
            if expected_details['total'] != actual['total']:
                errors.append(
                    f"Total mismatch: expected '{expected_details['total']}', "
                    f"got '{actual['total']}'"
                )
        
        all_correct = len(errors) == 0

        if all_correct:
            self.logger.info(f"Product {index}: All detail correct")
        else:
            self.logger.error(f"Product {index}: verification failed")
            for error in errors:
                self.logger.error(f" -{error}")
        
        return {
            'all_correct': all_correct,
            'actual': actual,
            'expected': expected_details,
            'errors': errors
        }
        
    def delete_product_by_index(self, index=0):

        try:
            delete_button = self.find_elements(self.DELETE_BUTTONS)

            if index >= len(delete_button):
                self.logger.error(f"product index {index} out of range")
                return False
            
            self.click(delete_button[index])
            self.logger.info(f"Deleted product at index {index}")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to delete product at index {index}: {e}")
            return False

    def click_proceed_to_checkout(self):
        self.click(self.PROCEED_TO_CHECKOUT)
        self.logger.info("Clicked Proceed checkout button")

    def is_modal_checkout_visible(self):
        return self.is_element_visible(self.CHECKOUT_MODAL)

    def click_register_login_button(self):
        self.click(self.REGISTER_LOGIN_BUTTON)

    def is_subscription_text_visible(self, timeout=5):
        """
        Check if subscription text is visible
        Returns: Boolean (True if visible, False otherwise)
        """
        return self.is_element_visible(self.SUBSCRIPTION_TITLE, timeout=timeout)
    
    def subscribe_email(self, email):
    
        self.input_text(self.SUBSCRIPTION_EMAIL, email)
        self.click(self.SUBSCRIPTION_BUTTON)
        self.logger.info(f"Subscribed with email: {email}")
        
        return self.is_element_visible(self.SUBSCRIPTION_SUCCESS)

    def get_subscription_success_message(self):
        """
        Get subscription success message
        Returns: String (subscription success message)
        """
        return self.get_text(self.SUBSCRIPTION_SUCCESS)
    

    
        
    
        
    
