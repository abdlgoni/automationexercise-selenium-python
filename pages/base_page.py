from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.config import Config
import logging

class BasePage:
    
    def __init__(self, driver):
        """
        Initialize BasePage
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.actions = ActionChains(driver)
        self.logger = logging.getLogger(__name__)
        
    def find_element(self, locator):
        """
        Find dan return single element
        
        Args:
            locator (tuple): Tuple of (By.TYPE, "value")
            
        Returns:
            WebElement: Element yang ditemukan
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.logger.debug(f"Element ditemukan {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"element tidak ditemukan{locator}")
            return []
            
    def find_elements(self, locator):
        """
        Find dan return multiple elements
        
        Args:
            locator (tuple): Tuple of (By.TYPE, "value")
            
        Returns:
            list: List of WebElements
        """
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            self.logger.debug(f"Ditemukan {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            self.logger.error(f"Elements tidak ditemukan: {locator}")
            return []
        
    def click(self, locator):
        """
        Click pada element
        
        Args:
            locator (tuple): Tuple of (By.TYPE, "value")
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.debug(f"Clicked element{locator}")
        except TimeoutException:
            self.logger.error(f"Element tidak Clickable: {locator}")
            raise
        
    def input_text(self, locator, text):
        """
        Input text ke element
        
        Args:
            locator (tuple): Tuple of (By.TYPE, "value")
            text (str): Text yang akan di-input
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        self.logger.debug(f"input text '{text}' ke element: {locator}")
        
    def get_text(self, locator):
        """
        Get text dari element
        
        Args:
            locator (tuple): Tuple of (By.TYPE, "value")
            
        Returns:
            str: Text dari element
        """
        element = self.find_element(locator)
        text = element.text
        self.logger.debug(f"Get Text dari {locator}: {text}")
        return text
    
    def get_attribute(self, locator, attribute_name):
        """
        Get attribute value dari element
        
        Args:
            locator (tuple): Tuple of (By.TYPE, "value")
            attribute_name (str): Nama attribute
            
        Returns:
            str: Value dari attribute
        """
        element = self.find_element(locator)
        value = element.get_attribute(attribute_name)
        self.logger.debug(f"Get Atribute '{attribute_name}' dari {locator}: {value}")
        return value
    
    def is_element_visible(self, locator, timeout=None):
        """
        Check apakah element visible
        
        Args:
            locator (tuple): Tuple of (By.TYPE, "value")
            timeout (int): Custom timeout
            
        Returns:
            bool: True jika visible, False jika tidak
        """
        try:
            wait_time = timeout if timeout else Config.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.visibility_of_element_located(locator))
            self.logger.debug(f"Element Visible: {locator}")
            return True
        except TimeoutException:
            self.logger.debug(f"Element tidak Visible {locator}")
            return False
    def is_element_present(self, locator):
        """
        Check apakah element present di DOM
        
        Args:
        locator (tuple): Tuple of (By.TYPE, "value")
            
        Returns:
            bool: True jika present, False jika tidak
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_element_disappear(self, locator, timeout=None):
        """
        Wait hingga element hilang
        
        Args:
            locator (tuple): Tuple of (By.TYPE, "value")
            timeout (int): Custom timeout
        """
        wait_time = timeout if timeout else Config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.invisibility_of_element_located(locator))
        self.logger.debug(f"Element sudah hilang {locator}")
        
    # ========== Navigation Methods ==========
    
    def open_url(self, url):
        """
        Open URL
        
        Args:
            url (str): URL yang akan dibuka
        """
        self.driver.get(url)
        self.logger.info(f"Opened URL {url}")
    
    def get_current_url(self):
        return self.driver.current_url
    
    def get_title(self):
        return self.driver.title
    
    def refresh_page(self):
        self.driver.refresh()
        self.logger.debug("Page refreshed")
        
    def go_back(self):
        self.driver.back()
        self.logger.debug("Navigated back")
        
    def scroll_to_element(self, locator):
        """
        Scroll ke element
        
        Args:
            locator (tuple): Tuple of (By.TYPE, "value")
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.debug(f"Scrolled to element: {locator}")
        
    def scroll_to_bottom(self):
        """Scroll ke bottom page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.logger.debug("Scrolled to bottom")
    
    def scroll_to_top(self):
        """Scroll ke top page"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.logger.debug("Scrolled to top")
    
    # ========== Wait Methods ==========
    
    def wait_for_page_load(self, timeout=None):
        """
        Wait hingga page fully loaded
        
        Args:
            timeout (int): Custom timeout
        """
        wait_time = timeout if timeout else Config.PAGE_LOAD_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        self.logger.debug("Page fully loaded")
        
    def wait_for_page_ready(self, locator):
        WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
        EC.visibility_of_element_located(locator)
    )
    
    # ========== Screenshot Methods ==========
    
    def take_screenshot(self, filename):
        """
        Take screenshot
        
        Args:
            filename (str): Nama file screenshot
        """
        filepath = f"{Config.SCREENSHOT_PATH}{filename}.png"
        self.driver.save_screenshot(filepath)
        self.logger.info(f"Screenshot saved: {filepath}")
        return filepath