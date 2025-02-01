from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from .utils import convert_date_format

def get_last_updated(browser, source_data="UBPR") -> str:
    """
    Retrieves the last updated date for the specified data source.
    
    Args:
        browser (WebDriver): The Selenium WebDriver instance.
        source_data (str): The data source to check ("UBPR" or "CDR").
    
    Returns:
        str: The last updated date in YYYYMMDD format.
    """
    # Navigate to the download page
    browser.get('https://cdr.ffiec.gov/public/PWS/DownloadBulkData.aspx')
    form_list_box = Select(browser.find_element(By.ID, "ListBox1"))

    if source_data == 'UBPR':
        # Find the element containing the last updated date for UBPR
        el = browser.find_element(By.ID, 'UpdatedTextUBPR')
        print(el)
        el_text = el.text
        # Convert the date format to YYYYMMDD
        formatted_date = convert_date_format(el_text)
        return formatted_date
    
    elif source_data == 'CDR':
        # Find the element containing the last updated date for CDR
        el = browser.find_element(By.ID, 'UpdatedTextCDR')
        print(el)
        el_text = el.text
        el_text_split = el_text.split(' ')
        print(el_text_split)
        date_text = el_text_split[-1].strip()
        print(date_text)
        # Convert the date format to YYYYMMDD
        formatted_date = convert_date_format(date_text)
        return formatted_date