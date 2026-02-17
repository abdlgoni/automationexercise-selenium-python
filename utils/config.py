class Config:
    BASE_URL = "https://automationexercise.com/"
    
    BROWSER = "chrome"
    HEADLES = False
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 10
    PAGE_LOAD_TIMEOUT = 30
    
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080
    
    SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_PATH = "reports/screenshots/"
    
    REPORT_PATH = "reports/html_reports/"
    
    LOG_FILE = "logs/test_execution.log"
    LOG_LEVEL = "INFO"
    
    VALID_SEARCH_KEYWORDS = [
        "Python programming",
        "Artificial Intelligence",
        "Indonesia",
        "World War II"
    ]
    
    INVALID_SEARCH_KEYWORDS = [
        "xyzabcqwerty123notfound",
        "@@##$$%%"
    ]
    
    POPULAR_ARTICLES = [
        "United States",
        "Indonesia",
        "Python (programming language)",
        "World War II"
    ]
    
    