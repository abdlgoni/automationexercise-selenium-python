import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.detail_product import DetailProductPage
from pages.search_result import SearchResultPage
import logging

logger = logging.getLogger(__name__)

class TestSearchProduct:
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.homepage = HomePage(driver)
        self.product_page = ProductPage(driver)
        self.detail_product_page = DetailProductPage(driver)
        self.search_result = SearchResultPage(driver)
        
    @pytest.mark.smoke
    def test_search_product(self):
        """
        Steps:
        1. Launch browser
        2. Navigate to url 'http://automationexercise.com'
        3. Verify that home page is visible successfully
        4. Click on 'Products' button
        5. Verify user is navigated to ALL PRODUCTS page successfully
        6. Enter product name in search input and click search button
        7. Verify 'SEARCHED PRODUCTS' is visible
        8. Verify all the products related to search are visible
        """
        
        self.homepage.open()
        
        logger.info("Verifying Homepage")
        assert self.homepage.is_homepage_visible(), \
            "Homepage is not visible"
        logger.info("Homepage visible")
        
        logger.info("Clicking product button")
        self.homepage.click_products()
        logger.info("Clicked product button")
        
        logger.info("Verifying all product")
        assert self.product_page.is_all_products_page_visible(), \
            "All product page is not visible"
            
        logger.info("ALL product page visible")
        
        logger.info("Searching product")
        search_term = "jeans"
        
        assert self.product_page.search_product(search_term), \
            f"Failed to search for {search_term}"
        logger.info(f"Searched for {search_term}")
        
        logger.info("Verifying 'SEARCHED PRODUCTS' title")
        assert self.search_result.is_searched_products_page_visible(), \
            "'SEARCHED PRODUCTS' title is not visible"
            
        title = self.search_result.get_searched_products_title()
        assert 'SEARCHED PRODUCTS' in title.upper(), \
            f"Expected 'SEARCHED PRODUCTS', got {title}"
        logger.info("'SEARCHED PRODUCTS' title visible")
        
        logger.info("verifying search result")
        assert self.search_result.is_products_result_visible(), \
            "Search result is not visible"
        
        results_count = self.search_result.get_search_results_count()
        assert results_count > 0, \
            f"Expected > 0 result count, got {results_count}"
        logger.info(f"{results_count} search result(s) visible")
        
        assert self.search_result.verify_search_results_contain_term(search_term), \
            f"Search result don't contain '{search_term}'"
        logger.info(f"Result match search term {search_term}")
        
        product_names = self.search_result.get_product_names_from_results()
        logger.info(f"Products found: {', '.join(product_names[:5])}")
        