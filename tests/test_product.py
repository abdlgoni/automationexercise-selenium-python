import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.detail_product import DetailProductPage
import logging

logger = logging.getLogger(__name__)

class TestProduct:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.home_page = HomePage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.detail_product = DetailProductPage(self.driver)
        logger.info("Setup complete")
        
    @pytest.mark.smoke
    def test_verify_all_product_and_product_detail(self):
        """        
        Steps:
        1. Launch browser
        2. Navigate to url 'http://automationexercise.com'
        3. Verify that home page is visible successfully
        4. Click on 'Products' button
        5. Verify user is navigated to ALL PRODUCTS page successfully
        6. The products list is visible
        7. Click on 'View Product' of first product
        8. User is landed to product detail page
        9. Verify that detail is visible: product name, category, price, 
           availability, condition, brand
        """
        self.home_page.open()
        
        logger.info("Verifying home page is visible")
        assert self.home_page.is_homepage_visible(timeout=15),\
            "Homepage is not visible"
        logger.info("Home page visible successfully")
        
        logger.info("Clicking product button")
        self.home_page.click_products()
        logger.info("Clicked product button")
        
        logger.info("Verifying ALL PRODUCTS page")
        assert self.product_page.is_all_products_page_visible(timeout=10),\
            "ALL PRODUCTS Page is not visible"
            
        title = self.product_page.get_all_products_title()
        assert 'ALL PRODUCTS' in title.upper(),\
            f"Expected 'ALL PRODUCTS' in title got: '{title}'"
            
        logger.info("User navigated to ALL PRODUCTS page successfully")
        
        logger.info("Verifying Product list is visible")
        
        assert self.product_page.is_product_list_visible(timeout=10),\
            "Products List is not visible"
            
        products_count = self.product_page.get_product_count()
        logger.info(f"Products List is visible {products_count}")
        
        logger.info("Clicking view product of first product")
        assert self.product_page.click_view_product_by_index(0),\
            "Failed click view product button"
        logger.info("Clicked view product of first product")
        
        logger.info("Verifying user is on product detail page")
        assert self.detail_product.is_product_detail_page_visible(timeout=10),\
            "Product detail is not visible"
        logger.info("User landed to product detail page")
        
        logger.info("Verifying all product detail visible")
        verification_result = self.detail_product.verify_product_detail_visible()
        
        assert verification_result['all_visible'], \
            f"Not all product details are visible. Missing: {', '.join(verification_result['missing'])}"
            
        product_details = self.detail_product.get_all_product_details()
        
        logger.info(" All product details are visible:")
        logger.info(f"  - Name: {product_details['name']}")
        logger.info(f"  - Category: {product_details['category']}")
        logger.info(f"  - Price: {product_details['price']}")
        logger.info(f"  - Availability: {product_details['availability']}")
        logger.info(f"  - Condition: {product_details['condition']}")
        logger.info(f"  - Brand: {product_details['brand']}")
        
        assert product_details['name'], "Product name is empty"
        assert product_details['category'], "Product category is empty"
        assert product_details['price'], "Product price is empty"
        assert product_details['availability'], "Product availability is empty"
        assert product_details['condition'], "Product condition is empty"
        assert product_details['brand'], "Product brand is empty"
            
        