import os
import pandas as pd

START_YR = 2001
END_YR = 2024
QUARTER = "0630"
DATA_DIR = "data"

VARIABLES = {
    "RC": {  # Balance Sheet (Form Type - 031)
        "variables": ["RCFD2170"],
        "description": "Balance Sheet"
    },
    "RCK": {  # Schedule RC-K – Quarterly Averages (Form Type - 031)
        "variables": ["RCON3387", "RCFD3368"],
        "description": "RC-K Quarterly Averages"
    },
    "RCCI": {  # Schedule RC-C Part I – Loans and Leases
        "variables": ["RCON1763"],
        "description": "RC-C Part I Loans and Leases"
    },
    "RCCII": {  # Schedule RC-C Part II – Loans to Small Businesses and Small Farms (Form Type - 031)
        "variables": ["RCON5570", "RCON5571", "RCON5572", "RCON5573", "RCON5574", "RCON5575"],
        "description": "RC-C Part II Loans to Small Businesses/Small Farms"
    }
}

def extract_yearly_vals(file_path: str, variables: list):
    """
    Extracts the specified variables from the file at the given path.
    Returns a DataFrame with the IDRSSD and the specified variables.
    """
    try:
        df = pd.read_csv(file_path, delimiter="\t", dtype=str)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
    
    if "IDRSSD" not in df.columns:
        print(f"IDRSSD column not found in file {file_path}.")
        return None
    
    # Keep only the columns we need.
    cols_to_keep = ["IDRSSD"] + variables
    available_cols = [col for col in cols_to_keep if col in df.columns]
    df = df[available_cols]

    for var in variables:
        if var in df.columns:
            # Replace missing or empty strings with 0 and convert to numeric.
            df[var] = pd.to_numeric(df[var].replace(["", " "], 0), errors='coerce')
        else:
            print(f"Variable {var} not found in file {file_path}.")

    return df

def write(yearly_tables: dict):
    """
    Writes the yearly tables to an Excel file with one sheet per year.
    """
    # Create a DataFrame from the results dictionary.
    # Rows are variables, columns are years.
    output_excel = "yearly_extracted_data.xlsx"
    with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
        for year, df in yearly_tables.items():
            # Each sheet is named after the year.
            sheet_name = str(year)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        
    print(f"Excel file with yearly tables written to {output_excel}")

"""
This script reads the FFIEC CDR Call data files for the years 2001-2024 and extracts
the specified variables from the specified schedules. It then writes the extracted
data to an Excel file with one sheet per year.

The script assumes the following directory structure:
- src/urap.py
- data/FFIEC CDR Call All Schedules {Quarter Year}/FFIEC CDR Call Schedule {Schedule} {Quarter Year (In Date Format)}.txt
  i.e. data/FFIEC CDR Call All Schedules Jun 30 2001/FFIEC CDR Call Schedule RC 06302001.txt
"""
def __main__():
    yearly_tables = {}

    # Loop over each year and each schedule.
    for year in range(START_YR, END_YR + 1):
        # Format the date portion. (Example: for 2001, file name uses "06302001")
        date_str = f"{QUARTER}{year}"
        merged_df = None
        print(f"Processing year {year} ...")
        
        for sched, sched_info in VARIABLES.items():
            # Construct the file path using the new structure:
            # data/FFIEC CDR Call All Schedules Jun 30 {year}/FFIEC CDR Call Schedule {sched} 0630{year}.txt
            dir_path = os.path.join(DATA_DIR, f"FFIEC CDR Call All Schedules Jun 30 {year}")
            file_name = f"FFIEC CDR Call Schedule {sched} {date_str}.txt"
            file_path = os.path.join(dir_path, file_name)
            
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}. Skipping.")
                continue

            # Extract the specified variables from the file.    
            df = extract_yearly_vals(file_path, sched_info["variables"])
        
            # Merge the current schedule's DataFrame with the merged_df for the year.
            # We perform an outer join to capture all banks.
            if merged_df is None:
                merged_df = df
            else:
                merged_df = pd.merge(merged_df, df, on="IDRSSD", how="outer")

        # If we managed to obtain data for this year, store it in the dictionary.
        if merged_df is not None:
            yearly_tables[year] = merged_df
        else:
            print(f"No data available for year {year}.")

    write(yearly_tables)

if __name__ == "__main__":
    __main__()