import logging
import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.checkout_page import CheckoutPage
from utils.data_generator import TestDataGenerator
import logging

logger = logging.getLogger(__name__)

class TestPlaceOrder:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.home_page = HomePage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.signup_page = SignupPage(self.driver)
        self.checkout_page = CheckoutPage(self.driver)
        self.data_generator = TestDataGenerator()
        self.user_data = self.data_generator.generate_user_data()
        self.birth_date = self.data_generator.generate_birth_date()
        self.payment_data = self.data_generator.generate_credit_card_data()
        logger.info("Setup Complete")

    def test_place_order_register_while_checkout(self):

        """
        1. Launch browser
        2. Navigate to url 'http://automationexercise.com'
        3. Verify that home page is visible successfully
        4. Add products to cart
        5. Click 'Cart' button
        6. Verify that cart page is displayed
        7. Click Proceed To Checkout
        8. Click 'Register / Login' button
        9. Fill all details in Signup and create account
        10. Verify 'ACCOUNT CREATED!' and click 'Continue' button
        11. Verify ' Logged in as username' at top
        12.Click 'Cart' button
        13. Click 'Proceed To Checkout' button
        14. Verify Address Details and Review Your Order
        15. Enter description in comment text area and click 'Place Order'
        16. Enter payment details: Name on Card, Card Number, CVC, Expiration date
        17. Click 'Pay and Confirm Order' button
        18. Verify success message 'Your order has been placed successfully!'
        19. Click 'Delete Account' button
        20. Verify 'ACCOUNT DELETED!' and click 'Continue' button
        """

        logger.info("Launched browser")
        self.home_page.open()
        logger.info("Browser launched")

        logger.info("Verifying home page is visible")
        assert self.home_page.is_homepage_visible(), \
            "Home page is not visible"
        logger.info("Home page visible successfully")

        logger.info("Clicking product button")
        self.home_page.click_products()
        logger.info("Clicked product button")

        logger.info("Verifying all product")
        assert self.product_page.is_all_products_page_visible(), \
            "All product page is not visible"
        logger.info("All product page visible")

        logger.info("Adding first product to cart")
        self.product_page.add_to_cart_by_index(0)
        logger.info("First product added to cart")

        # Verify modal appeared
        assert self.product_page.is_modal_content_visible(), \
            "Modal not visible after adding to cart"

        logger.info("Clicking view cart")
        self.product_page.click_view_cart_link()
        logger.info("View cart clicked")

        assert self.cart_page.is_cart_page_visible(), \
            "Cart page is not visible"
        logger.info("Cart page is visible")

        logger.info("Clicking proceed to checkout")
        self.cart_page.click_proceed_to_checkout()
        logger.info("Proceed to checkout clicked")

        assert self.cart_page.is_modal_checkout_visible(), \
            "Modal checkout is not visible"
        logger.info("Modal checkout is visible")

        self.cart_page.click_register_login_button()
        logger.info("Register / Login button clicked")

        self.login_page.wait_until_ready()
        assert self.login_page.is_signup_section_visible(), \
            "Signup section is not visible"
        logger.info("Signup section is visible")

        self.login_page.signup(self.user_data['name'], self.user_data['email'])
        logger.info("Signup form filled")

        self.login_page.click_signup_button()
        logger.info("Signup button clicked")

        assert self.signup_page.is_account_info_page_displayed()
        logger.info("Account info page displayed")

        account_data = {
            'title': 'Mr',
            'password': self.user_data['password'],
            'day': self.birth_date['day'],
            'month': self.birth_date['month'],
            'year': self.birth_date['year']
        }
        logger.debug("Prepared account data (password, DOB)")

        address_data = {
            'first_name': self.user_data['first_name'],
            'last_name': self.user_data['last_name'],
            'company': self.user_data['company'],
            'address1': self.user_data['address1'],
            'address2': self.user_data['address2'],
            'country': self.user_data['country'],
            'state': self.user_data['state'],
            'city': self.user_data['city'],
            'zipcode': self.user_data['zipcode'],
            'mobile': self.user_data['mobile']
        }
        logger.debug("Prepared address data")

        self.signup_page.complete_registration(account_data, address_data)
        logger.info("Filled account and address information")

        assert self.signup_page.is_account_created_successfully()
        logger.info("Account created successfully")
        message_created = self.signup_page.get_account_created_message()
        assert 'ACCOUNT CREATED!' in message_created
        logger.debug(f"Verified message: {message_created}")

        self.signup_page.click_continue()
        logger.info("Continue button clicked")

        assert self.home_page.is_logged_in()
        username = self.home_page.get_logged_in_username()
        assert username == self.user_data['name']
        logger.info(f"Successfully logged in as: {username}")

        self.home_page.click_cart()
        assert self.cart_page.is_cart_page_visible(),\
            "Cart page is not visible"
        logger.info("Cart page is visible")

        is_count_correct = self.cart_page.verify_products_count(1)

        assert is_count_correct, "Product count verification failed!"
        logger.info("Product count is verified successfully")

        logger.info("Clicking proceed to checkout")
        self.cart_page.click_proceed_to_checkout()
        logger.info("Proceed to checkout clicked")

        assert self.checkout_page.is_checkout_page_visible(),\
            "Checkout page is not visible"
        assert self.checkout_page.is_review_order_visible(),\
            "Review Your Order section is not visible"
        logger.info("Address Details and Review Your Order verified")

        self.checkout_page.enter_comment("Test order comment - automation exercise")
        self.checkout_page.click_place_order()
        logger.info("Comment entered and Place Order clicked")

        self.checkout_page.enter_payment_details(
            name=self.payment_data['name_on_card'],
            card_number=self.payment_data['card_number'],
            cvc=self.payment_data['cvc'],
            expiry_month=self.payment_data['expiry_month'],
            expiry_year=self.payment_data['expiry_year']
        )
        logger.info("Payment details entered")

        self.checkout_page.click_pay_and_confirm()
        logger.info("Pay and Confirm Order clicked")

        assert self.checkout_page.is_order_success_visible(),\
            "Order success page is not visible"
        success_message = self.checkout_page.get_order_success_message()
        assert 'Congratulations! Your order has been confirmed!' in success_message,\
            f"Unexpected success message: {success_message}"
        logger.info(f"Order placed successfully: {success_message}")

        self.home_page.click_delete_account()
        logger.info("Delete Account clicked")

        assert self.signup_page.is_account_deleted_successfully(),\
            "Account Deleted page is not visible"
        deleted_message = self.signup_page.get_account_deleted_message()
        assert 'ACCOUNT DELETED!' in deleted_message,\
            f"Unexpected delete message: {deleted_message}"
        logger.info(f"Account deleted: {deleted_message}")

        self.signup_page.click_continue()
        logger.info("Continue after account deletion clicked")

