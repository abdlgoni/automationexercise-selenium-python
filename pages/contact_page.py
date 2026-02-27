from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

class ContactcusPage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
    
    CONTACT_US_TITLE = (By.XPATH, "//div[@class='col-sm-12']//h2[@class='title text-center']")
    
    GET_IN_TOUCH_TITLE = (By.XPATH, "//h2[normalize-space()='Get In Touch']")
    
    # form
    NAME_FIELD = (By.CSS_SELECTOR, "input[placeholder='Name']")
    EMAIL_FIELD = (By.CSS_SELECTOR, "input[placeholder='Email']")
    SUBJECT_FIELD = (By.CSS_SELECTOR, "input[placeholder='Subject']")
    MESSAGE_FIELD = (By.XPATH, "//textarea[@id='message']")
    
    UPLOAD_FILE = (By.CSS_SELECTOR, "input[name='upload_file']")
    
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "input[value='Submit']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[@class='status alert alert-success']")
    HOME_BUTTON = (By.CSS_SELECTOR, ".btn.btn-success")
    
    def is_contact_us_visible(self):
        return self.is_element_visible(self.CONTACT_US_TITLE)
    
    def get_in_touch_title(self):
        return self.get_text(self.GET_IN_TOUCH_TITLE)
    
    def enter_name(self, name):
        self.input_text(self.NAME_FIELD, name)
        
    def enter_email(self, email):
        self.input_text(self.EMAIL_FIELD, email)
        
    def enter_subject(self, subject):
        self.input_text(self.SUBJECT_FIELD, subject)
        
    def enter_message(self, message):
        self.input_text(self.MESSAGE_FIELD, message)
    
    def upload_file(self, file_path):
        self.input_text(self.UPLOAD_FILE, file_path)
        
    def click_submit(self):
        self.click(self.SUBMIT_BUTTON)

    def accept_alert(self):
        """Accept JavaScript alert if present"""
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            self.logger.info(f"Alert accepted: '{alert_text}'")
            return True
        except Exception as e:
            self.logger.debug(f"No alert present: {e}")
            return False

    def handle_ads(self, timeout=5):
        """
        Try several strategies to dismiss ads/popups that may appear after form submit.

        Strategies:
        - accept browser alert
        - click common overlay/modal close buttons
        - switch into iframes and try to click inner close buttons
        - close any extra windows/tabs opened by ads

        Returns:
            bool: True if an ad was detected and handled, False otherwise
        """
        handled = False

        # 1) Browser alert
        try:
            self.accept_alert()
            handled = True
        except Exception:
            pass

        # 2) Common close button selectors for overlays/modals
        close_locators = [
            (By.CSS_SELECTOR, "button[aria-label='Close']"),
            (By.CSS_SELECTOR, ".modal .close"),
            (By.CSS_SELECTOR, ".ads-close"),
            (By.CSS_SELECTOR, ".close-ad"),
            (By.XPATH, "//button[contains(@class,'close') or contains(normalize-space(.),'Close') or contains(normalize-space(.),'close') ]"),
            (By.XPATH, "//div[contains(@class,'ad')]/button")
        ]

        for loc in close_locators:
            try:
                if self.is_element_visible(loc, timeout=2):
                    try:
                        self.click(loc)
                        self.logger.debug(f"Closed ad using locator: {loc}")
                        return True
                    except Exception:
                        # try to click via JS if normal click fails
                        try:
                            el = self.find_element(loc)
                            self.driver.execute_script("arguments[0].click();", el)
                            self.logger.debug(f"Clicked ad close via JS: {loc}")
                            return True
                        except Exception:
                            continue
            except Exception:
                continue

        # 3) Try inside iframes (some ads live in iframes)
        try:
            frames = self.driver.find_elements(By.TAG_NAME, "iframe")
            for frame in frames:
                try:
                    self.driver.switch_to.frame(frame)
                    # attempt a few selectors inside iframe
                    try:
                        inner = self.driver.find_element(By.CSS_SELECTOR, ".close, .close-btn, button[aria-label='Close']")
                        inner.click()
                        self.logger.debug("Closed ad inside iframe")
                        self.driver.switch_to.default_content()
                        return True
                    except Exception:
                        self.driver.switch_to.default_content()
                        continue
                except Exception:
                    try:
                        self.driver.switch_to.default_content()
                    except Exception:
                        pass
        except Exception:
            pass

        # 4) Close any extra windows/tabs (ads sometimes open new windows)
        try:
            handles = self.driver.window_handles
            main = self.driver.current_window_handle
            if len(handles) > 1:
                for h in handles:
                    if h != main:
                        try:
                            self.driver.switch_to.window(h)
                            self.driver.close()
                        except Exception:
                            continue
                try:
                    self.driver.switch_to.window(main)
                except Exception:
                    pass
                self.logger.debug("Closed extra windows opened by ads")
                return True
        except Exception:
            pass

        if handled:
            return True

        self.logger.debug("No ads detected/handled")
        return False

    def is_success_message_visible(self):
        return self.is_element_visible(self.SUCCESS_MESSAGE)

    def get_success_message_text(self):
        return self.get_text(self.SUCCESS_MESSAGE)

    def click_home(self):
        self.click(self.HOME_BUTTON)
    