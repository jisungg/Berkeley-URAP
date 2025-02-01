def convert_date_format(date_string):
    """
    Converts a date string from MM/DD/YYYY format to YYYYMMDD format.
    
    Args:
        date_string (str): The date string in MM/DD/YYYY format.
    
    Returns:
        str: The date string in YYYYMMDD format.
    """
    # Split the date string by '/'
    date_string = date_string.split('/')
    # Rearrange and zero-fill the date components
    new_date_string = date_string[2].zfill(2) + date_string[0].zfill(2) + date_string[1].zfill(2)
    return new_date_string


def convert_from_yyyymmdd(date_string):
    """
    Converts a date string from YYYYMMDD format to MM/DD/YYYY format.
    
    Args:
        date_string (str): The date string in YYYYMMDD format.
    
    Returns:
        str: The date string in MM/DD/YYYY format.
    """
    # Rearrange the date components to MM/DD/YYYY format
    new_date_string = date_string[4:6] + "/" + date_string[6:8] + "/" + date_string[0:4]
    return new_date_string