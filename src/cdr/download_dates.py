from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

import time

from .utils import convert_date_format

def populate_download_options(browser, source_data="UBPR"):
    """
    Populates the download options for the specified data source.
    
    Args:
        browser (WebDriver): The Selenium WebDriver instance.
        source_data (str): The data source to check ("UBPR" or "CDR").
    
    Returns:
        list: A list of reformatted dates available for download.
    """
    # Navigate to the download page
    browser.get('https://cdr.ffiec.gov/public/PWS/DownloadBulkData.aspx')

    form_list_box = None
    attempt_nums = 0

    # Wait until the form list box is available
    while form_list_box is None:
        try:
            form_list_box = Select(browser.find_element(By.ID, "ListBox1"))
        except:
            attempt_nums += 1
            if attempt_nums > 10:
                raise Exception("Could not find form list box")
            time.sleep(1)
   
    if source_data == 'UBPR':
        # Select the UBPR option from the list box
        for option in form_list_box.options:
            if option.text == 'UBPR Ratio -- Single Period':
                option.click()
                break
    
    elif source_data == 'CDR':
        # Select the CDR option from the list box
        for option in form_list_box.options:
            if option.text == 'Call Reports -- Single Period':
                option.click()
                break

    attempt_nums = 0
    year_list_box = None

    # Wait until the year list box is available
    while year_list_box is None:
        try:
            year_list_box = Select(browser.find_element(By.ID, 'DatesDropDownList'))
        except:
            attempt_nums += 1
            if attempt_nums > 10:
                raise Exception("Could not find form list box")
            time.sleep(1)

    # Get the list of potential dates and reformat them
    potential_dates = [d.text for d in list(year_list_box.options)]
    reformatted_dates = [convert_date_format(d) for d in potential_dates]

    return reformatted_dates