"""
Pytest configuration dan fixtures
"""

import pytest
import logging
import os
from datetime import datetime
from utils.driver_factory import DriverFactory
from utils.config import Config


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


@pytest.fixture(scope="class")
def driver(request):
    """
    Fixture untuk create dan quit WebDriver
    Scope: class - satu driver untuk satu test class
    """
    logger.info(f"Starting test class")
    
    browser = request.config.getoption("--browser") if hasattr(request.config, 'getoption') else Config.BROWSER
    driver = DriverFactory.get_driver(browser)
    
    # Assign driver ke class agar bisa diakses via self.driver
    if request.cls is not None:
        request.cls.driver = driver
    
    yield driver
    
    driver.quit()
    logger.info(f"Finished test class")

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


# ========== Fixture Examples untuk specific needs ==========

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