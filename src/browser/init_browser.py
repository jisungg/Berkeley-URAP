from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

def return_browser(tmp_dir) -> dict:
    """
    Returns a Firefox browser instance with the specified download directory.
    
    Args:
        tmp_dir (str): The temporary directory to use for downloads.
    
    Returns:
        WebDriver: The configured Firefox WebDriver instance.
    """
    # Set up the Firefox WebDriver service
    s = Service('/usr/bin/geckodriver')

    # Configure Firefox options
    options = Options()
    options.set_preference("pdfjs.disabled", True)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.useWindow", False)
    options.set_preference("browser.download.dir", tmp_dir)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", 
                        "application/pdf, application/octet-string, application/force-download")
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')

    # Initialize the Firefox WebDriver with the configured options
    driver = webdriver.Firefox(service=s, options=options)

    return driver