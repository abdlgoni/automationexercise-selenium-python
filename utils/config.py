import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = "https://automationexercise.com/"
    
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 15
    PAGE_LOAD_TIMEOUT = 30
    
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080
    
    SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_PATH = "reports/screenshots/"
    
    REPORT_PATH = "reports/html_reports/"
    
    LOG_FILE = "logs/test_execution.log"
    LOG_LEVEL = "INFO"
    
    TEST_EMAIL = os.getenv("TEST_EMAIL", "")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "")
    
    
    
