"""
Pytest configuration dan fixtures
"""

import pytest
import logging
import os
from datetime import datetime
from utils.driver_factory import DriverFactory
from utils.config import Config
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from utils.data_generator import TestDataGenerator


# Setup logging
def setup_logging():
    """Setup logging configuration"""
    os.makedirs("logs", exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler()
        ]
    )


setup_logging()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="function", autouse=True)
def driver(request):
    """
    Fixture untuk create dan quit WebDriver
    Scope: function + autouse - satu driver BARU untuk setiap test method
    Browser akan di-close setelah test selesai, kemudian di-buka lagi untuk test berikutnya
    
    autouse=True memastikan fixture ini selalu berjalan untuk SETIAP test
    tanpa perlu tambahan di class atau method level
    """
    logger.info(f"Starting test: {request.node.name}")
    
    browser = request.config.getoption("--browser") if hasattr(request.config, 'getoption') else Config.BROWSER
    driver = DriverFactory.get_driver(browser)
    
    # Assign driver ke instance test agar bisa diakses via self.driver
    if request.instance is not None:
        request.instance.driver = driver
    
    yield driver
    
    driver.quit()
    logger.info(f"Finished test: {request.node.name} - Browser closed")

# @pytest.fixture(scope="session")
# def driver_session(request):
#     """
#     Fixture untuk create WebDriver dengan session scope
#     Scope: session - reuse driver untuk semua tests
#     Gunakan ini jika ingin lebih cepat, tapi kurang isolated
#     """
#     logger.info("Creating session-scoped driver")
    
#     browser = request.config.getoption("--browser") if hasattr(request.config, 'getoption') else Config.BROWSER
#     driver = DriverFactory.get_driver(browser)
    
#     yield driver
    
#     driver.quit()
#     logger.info("Session-scoped driver closed")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook untuk capture test result (untuk screenshot on failure)
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
    
    # Capture screenshot jika test failed
    if rep.when == "call" and rep.failed:
        # Get driver dari test instance
        if hasattr(item, "instance") and hasattr(item.instance, "driver"):
            driver = item.instance.driver
            if driver and Config.SCREENSHOT_ON_FAILURE:
                screenshot_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                try:
                    os.makedirs(Config.SCREENSHOT_PATH, exist_ok=True)
                    filepath = f"{Config.SCREENSHOT_PATH}{screenshot_name}.png"
                    driver.save_screenshot(filepath)
                    logger.error(f"Screenshot captured on failure: {filepath}")
                    # Attach screenshot path ke report untuk bisa dilihat di laporan
                    rep.screenshot_path = filepath
                except Exception as e:
                    logger.error(f"Gagal capture screenshot: {str(e)}")


def pytest_addoption(parser):
    """
    Add custom command line options
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    
    parser.addoption(
        "--count",
        action="store",
        default=1,
        type=int,
        help="Number of times to repeat each test"
    )


def pytest_configure(config):
    """
    Pytest configuration hook
    """
    # Create directories if not exist
    os.makedirs(Config.SCREENSHOT_PATH, exist_ok=True)
    os.makedirs(Config.REPORT_PATH, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Set headless from command line
    if config.getoption("--headless"):
        Config.HEADLESS = True
    
    # Add custom markers
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "search: mark test as search functionality test")
    config.addinivalue_line("markers", "article: mark test as article page test")
    
    config.addinivalue_line(
        "markers", 
        "flaky: mark test as flaky (may fail intermittently)"
    )


# ========== Fixture untuk setup akun ==========

@pytest.fixture(scope="function")
def registered_account():
    """
    Fixture function: register akun baru sebelum test,
    yield credentials, cleanup setelah test selesai.

    Gunakan di test yang butuh akun sudah terdaftar (e.g., test_login_correct_email_and_password).
    """
    logger = logging.getLogger(__name__)
    driver = None
    user_data = None
    try:
        # Setup: register new account via browser terpisah
        driver = DriverFactory.get_driver()
        home_page = HomePage(driver)
        login_page = LoginPage(driver)
        signup_page = SignupPage(driver)
        data_gen = TestDataGenerator()
        user_data = data_gen.generate_user_data()
        birth_date = data_gen.generate_birth_date()

        home_page.open()
        home_page.click_signup_login()
        login_page.wait_until_ready()
        login_page.signup(user_data['name'], user_data['email'])
        login_page.click_signup_button()

        account_data = {
            'title': 'Mr',
            'password': user_data['password'],
            'day': birth_date['day'],
            'month': birth_date['month'],
            'year': birth_date['year'],
        }
        address_data = {
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'company': user_data['company'],
            'address1': user_data['address1'],
            'address2': user_data['address2'],
            'country': user_data['country'],
            'state': user_data['state'],
            'city': user_data['city'],
            'zipcode': user_data['zipcode'],
            'mobile': user_data['mobile'],
        }
        signup_page.complete_registration(account_data, address_data)
        assert signup_page.is_account_created_successfully()
        signup_page.click_continue()
        home_page.wait_until_ready()

        # Logout agar bisa test login
        home_page.click_logout()
        login_page.wait_until_ready()

        logger.info(f"Registered account for test: {user_data['email']}")

        # Yield credentials ke test
        yield {
            'email': user_data['email'],
            'password': user_data['password'],
            'name': user_data['name'],
        }
    except Exception as e:
        logger.error(f"Gagal setup registered_account: {e}")
        # Pastikan yield tetap berjalan agar pytest tidak error
        yield None
    finally:
        # Teardown: cleanup akun (fallback jika test tidak sempat delete)
        if user_data and driver:
            try:
                home_page = HomePage(driver)
                login_page = LoginPage(driver)
                signup_page = SignupPage(driver)

                home_page.open()
                home_page.click_signup_login()
                login_page.wait_until_ready()
                login_page.login(user_data['email'], user_data['password'])
                login_page.click_login_button()
                home_page.wait_until_ready()

                if home_page.is_logged_in():
                    home_page.click_delete_account()
                    if signup_page.is_account_deleted_successfully():
                        signup_page.click_continue()
                        logger.info(f"Cleaned up account: {user_data['email']}")
            except Exception:
                logger.warning(f"Account {user_data['email']} already deleted or cleanup skipped")
            finally:
                driver.quit()
        elif driver:
            driver.quit()


@pytest.fixture
def base_url():
    """Return base URL"""
    return Config.BASE_URL


# @pytest.fixture
# def valid_search_keywords():
#     """Return list of valid search keywords"""
#     return Config.VALID_SEARCH_KEYWORDS


# @pytest.fixture
# def invalid_search_keywords():
#     """Return list of invalid search keywords"""
#     return Config.INVALID_SEARCH_KEYWORDS