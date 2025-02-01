from cdr import download_file
from browser import init_browser
from uuid import uuid4
import os
import shutil

QUARTER = 20090630

def download_from_data_source(data_source, quarter):
    """
    Downloads data from a specified data source for a given quarter.
    
    Args:
        data_source (str): The data source to download from.
        quarter (int): The quarter for which to download data.
    
    Returns:
        str: The result string from the download process.
    """
    # Create a temporary directory for the download process
    tmp_dir = '/tmp/' + str(uuid4())
    os.mkdir(tmp_dir)

    # Initialize the browser with the temporary directory
    browser = init_browser.return_browser(tmp_dir)

    # Start the download process
    ret_str = download_file.init_download(browser, data_source=data_source, quarter=quarter, format=format, download_loc=tmp_dir)

    # Clean up the temporary directory
    shutil.rmtree(tmp_dir)

    return ret_str


def return_cdr_file():
    """
    Downloads a quarterly CDR dataset, returning the JSON representation of the data.
    
    Returns:
        str: The JSON representation of the downloaded data.
    """
    if QUARTER is None:
        print("No quarter specified")
        return

    # Download the data for the specified quarter
    response = download_from_data_source("CDR", QUARTER)

    return response

