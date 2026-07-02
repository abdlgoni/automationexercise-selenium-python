from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging


class CheckoutPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    ADDRESS_DETAILS_HEADING = (By.XPATH, "//h2[contains(text(), 'Address Details')]")
    DELIVERY_ADDRESS = (By.CLASS_NAME, "address_delivery")
    BILLING_ADDRESS = (By.CLASS_NAME, "address_billing")

    REVIEW_ORDER_HEADING = (By.XPATH, "//h2[contains(text(), 'Review Your Order')]")

    COMMENT_TEXTAREA = (By.XPATH, "//textarea[@name='message']")
    PLACE_ORDER_BUTTON = (By.XPATH, "//a[contains(text(), 'Place Order')]")

    NAME_ON_CARD = (By.CSS_SELECTOR, "input[data-qa='name-on-card']")
    CARD_NUMBER = (By.CSS_SELECTOR, "input[data-qa='card-number']")
    CVC = (By.CSS_SELECTOR, "input[data-qa='cvc']")
    EXPIRY_MONTH = (By.CSS_SELECTOR, "input[data-qa='expiry-month']")
    EXPIRY_YEAR = (By.CSS_SELECTOR, "input[data-qa='expiry-year']")
    PAY_CONFIRM_BUTTON = (By.CSS_SELECTOR, "button[data-qa='pay-button']")

    ORDER_PLACED_TITLE = (By.CSS_SELECTOR, "h2[data-qa='order-placed']")
    ORDER_SUCCESS_MESSAGE = (By.XPATH, "//p[contains(., 'Congratulations! Your order has been confirmed!')]")
    CONFIRM_CONTINUE_BUTTON = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

    PAGE_READY_LOCATOR = ADDRESS_DETAILS_HEADING

    def is_checkout_page_visible(self):
        return self.is_element_visible(self.ADDRESS_DETAILS_HEADING)

    def get_delivery_address_text(self):
        return self.get_text(self.DELIVERY_ADDRESS)

    def get_billing_address_text(self):
        return self.get_text(self.BILLING_ADDRESS)

    def is_review_order_visible(self):
        return self.is_element_visible(self.REVIEW_ORDER_HEADING)

    def enter_comment(self, comment):
        self.input_text(self.COMMENT_TEXTAREA, comment)
        self.logger.info("Entered comment in checkout")

    def click_place_order(self):
        self.click(self.PLACE_ORDER_BUTTON)
        self.logger.info("Clicked Place Order button")

    def enter_payment_details(self, name, card_number, cvc, expiry_month, expiry_year):
        self.input_text(self.NAME_ON_CARD, name)
        self.input_text(self.CARD_NUMBER, card_number)
        self.input_text(self.CVC, cvc)
        self.input_text(self.EXPIRY_MONTH, expiry_month)
        self.input_text(self.EXPIRY_YEAR, expiry_year)
        self.logger.info("Entered payment details")

    def click_pay_and_confirm(self):
        self.click(self.PAY_CONFIRM_BUTTON)
        self.logger.info("Clicked Pay and Confirm Order button")

    def is_order_success_visible(self):
        return self.is_element_visible(self.ORDER_PLACED_TITLE)

    def get_order_success_message(self):
        if self.is_order_success_visible():
            return self.get_text(self.ORDER_SUCCESS_MESSAGE)
        return None

    def click_continue_after_order(self):
        self.click(self.CONFIRM_CONTINUE_BUTTON)
        self.logger.info("Clicked Continue after order")
