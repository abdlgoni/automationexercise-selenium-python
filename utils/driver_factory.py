from requests import options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utils.config import Config

class DriverFactory:
    """factory class for create Webdriver Instance"""
    
    @staticmethod
    def get_driver(browser_name= None):
        """
        Create dan return WebDriver instance
        
        Args:
            browser_name (str): Name browser (chrome, firefox, edge)
            
        Returns:
            WebDriver: Instance dari WebDriver
        """
        
        if browser_name is None:
            browser_name = Config.BROWSER
            
        browser_name = browser_name.lower()
        
        if browser_name == "chrome":
            return DriverFactory._get_chrome_driver()
        elif browser_name == "firefox":
            return DriverFactory._get_firefox_driver()
        elif browser_name == "edge":
            return DriverFactory._get_edge_driver()
        else:
            raise ValueError(f"Browser '{browser_name}' tidak didukung. Gunakan: chrome, firefox, atau edge")
    
    @staticmethod
    def _get_chrome_driver():
        """Create Chrome Driver"""
        options = webdriver.ChromeOptions()
        
        if Config.HEADLESS:
            options.add_argument("--headless")
            
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument(f"--window-size={Config.WINDOW_WIDTH},{Config.WINDOW_HEIGHT}")
    #     options.add_argument("--disable-notifications")
    #     options.add_argument("--disable-popup-blocking")
    #     options.add_argument("--disable-infobars")
    #     options.add_argument("--disable-extensions")
    #     options.add_argument("--disable-blink-features=AutomationControlled")
    
    # # Disable various popup types via preferences
    #     options.add_experimental_option("prefs", {
    #         # Disable notification popups
    #         "profile.default_content_setting_values.notifications": 2,
    #         # Disable media stream popups (camera/mic)
    #         "profile.default_content_setting_values.media_stream": 2,
    #         # Disable popup windows
    #         "profile.default_content_settings.popups": 0,
    #         # Disable geolocation popups
    #         "profile.default_content_setting_values.geolocation": 2,
    #         # Disable download prompts
    #         "download.prompt_for_download": False,
    #         "download.directory_upgrade": True,
    #         "safebrowsing.enabled": True
    #     })
        
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        DriverFactory._configure_driver(driver)
        return driver
    
    @staticmethod
    def _get_firefox_driver():
        """Create Firefox WebDriver"""
        options = webdriver.FirefoxOptions()
        
        if Config.HEADLESS:
            options.add_argument("--headless")
        
        # Create driver
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        DriverFactory._configure_driver(driver)
        return driver
    
    @staticmethod
    def _get_edge_driver():
        """Create Edge WebDriver"""
        options = webdriver.EdgeOptions()
        
        if Config.HEADLESS:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Create driver
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        DriverFactory._configure_driver(driver)
        return driver
    
    @staticmethod
    def _configure_driver(driver):
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        driver.maximize_window()
    
    