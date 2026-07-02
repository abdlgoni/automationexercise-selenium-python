from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from utils.config import Config
import logging

class BasePage:
    
    PAGE_READY_LOCATOR = None
    
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
    
    def _get_wait(self, timeout=None):
        if timeout is not None:
            return WebDriverWait(self.driver, timeout)
        return self.wait
        
    
    def _dismiss_ads(self):
        """Cleanup ads/vignette yang lolos dari blocking"""
        try:
            self.driver.execute_script("""
                const adSelectors = [
                    '#google_vignette',
                    'iframe[id*="google_ads"]',
                    'div[id*="google_ads"]',
                    '.adsbygoogle',
                    '#ad-overlay'
                ];
                adSelectors.forEach(sel => {
                    document.querySelectorAll(sel).forEach(el => el.remove());
                });
                // Restore scroll jika di-lock oleh vignette
                document.body.style.overflow = 'auto';
                document.body.style.position = 'static';
            """);
        except Exception:
            pass  # Silent fail, jangan sampai break test flow
        
    def find_element(self, locator, timeout=None):
        try:
            element = self._get_wait(timeout).until(EC.presence_of_element_located(locator))
            self.logger.debug(f"Element ditemukan {locator}")
            return element
        except TimeoutException as e:
            self.logger.error(f"element tidak ditemukan{locator}")
            raise e
            
    def find_elements(self, locator, timeout=None):
        try:
            elements = self._get_wait(timeout).until(EC.presence_of_all_elements_located(locator))
            self.logger.debug(f"Ditemukan {len(elements)} elements: {locator}")
            return elements
        except TimeoutException :
            self.logger.error(f"Elements tidak ditemukan: {locator}")
            return []
        
    def click(self, locator, timeout=None):
        try:
            element = self._get_wait(timeout).until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.debug(f"Clicked element {locator}")
        except (TimeoutException, ElementClickInterceptedException):
            try:
                element = self.find_element(locator, timeout=timeout)
                self.driver.execute_script("arguments[0].click();", element)
                self.logger.debug(f"Clicked via JS fallback: {locator}")
            except Exception as js_error:
                self.logger.error(f"Click failed (normal + JS): {locator} - {js_error}")
                raise
        
    def input_text(self, locator, text, timeout=None):
        element = self.find_element(locator, timeout=timeout)
        element.clear()
        element.send_keys(text)
        self.logger.debug(f"input text '{text}' ke element: {locator}")
        
    def get_text(self, locator, timeout=None):
        element = self.find_element(locator, timeout=timeout)
        text = element.text
        self.logger.debug(f"Get Text dari {locator}: {text}")
        return text
    
    def get_attribute(self, locator, attribute_name, timeout=None):
        element = self.find_element(locator, timeout=timeout)
        value = element.get_attribute(attribute_name)
        self.logger.debug(f"Get Atribute '{attribute_name}' dari {locator}: {value}")
        return value
    
    def is_element_visible(self, locator, timeout=None):
        try:
            self._get_wait(timeout).until(EC.visibility_of_element_located(locator))
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
        self._get_wait(timeout).until(EC.invisibility_of_element_located(locator))
        self.logger.debug(f"Element sudah hilang {locator}")
        
        
    # ========== Navigation Methods ==========
    
    def open_url(self, url):
        """
        Open URL
        
        Args:
            url (str): URL yang akan dibuka
        """
        self.driver.get(url)
        self._dismiss_ads()
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
        if timeout is None:
            timeout = Config.PAGE_LOAD_TIMEOUT
        self._get_wait(timeout).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        self.logger.debug("Page fully loaded")
        
    def wait_for_page_ready(self, locator, timeout=None):
        try:
            self._get_wait(timeout).until(EC.visibility_of_element_located(locator))
            self.logger.debug(f"Page ready — element visible: {locator}")
        except TimeoutException:
            self.logger.error(f"Page not ready — element not visible: {locator}")
            raise
    
    def wait_until_ready(self, timeout=None):
        if self.PAGE_READY_LOCATOR:
            self.wait_for_page_ready(self.PAGE_READY_LOCATOR, timeout)
    
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
