from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from xbrl import process_file

import os

import time

from .utils import convert_date_format, convert_from_yyyymmdd

def init_download(browser, data_source, quarter, format, download_loc):
    """
    Initializes the download process for the specified data source and quarter.
    
    Args:
        browser (WebDriver): The Selenium WebDriver instance.
        data_source (str): The data source to download from ("UBPR" or "CDR").
        quarter (str): The quarter for which to download data in YYYYMMDD format.
        format (str): The format of the data to download.
        download_loc (str): The location to save the downloaded file.
    
    Returns:
        str: The JSON representation of the processed data.
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
   
    if data_source == 'UBPR':
        # Select the UBPR option from the list box
        for option in form_list_box.options:
            if option.text == 'UBPR Ratio -- Single Period':
                option.click()
                break
    
    elif data_source == 'CDR':
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


    # Convert the selection date to the format expected by the website
    selection_date = convert_from_yyyymmdd(quarter)

    print("selection date is ", selection_date)

    print("list box options are ", [d.text for d in list(year_list_box.options)])

    # Select the date in the list box
    for option in year_list_box.options:
        if option.text == selection_date:
            option.click()
            break


    # Click the XBRL button
    browser.find_element(By.ID, 'XBRLRadiobutton').click()

    # Wait a couple of seconds
    time.sleep(2)

    print("Downloading file...")

    # Download the file
    browser.find_element(By.ID, 'Download_0').click()

    file_downloaded = False
    # Wait until the file is downloaded
    while not file_downloaded:
        files = os.listdir(download_loc)

        print("found files ", files)

        # Check if there is a .ZIP file in the folder
        file_still_downloading = any(['part' in f for f in files])

        if not file_still_downloading:
            file_downloaded = True
            break
        print("Waiting for file to download...")
        time.sleep(1)

    print("File downloaded!")
    print("Processing file...", file_downloaded)

    # Process the downloaded file
    ret_str = process_file.process_xbrl_file(download_loc + "/" + files[-1])

    return ret_str