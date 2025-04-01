import pandas as pd

def clean_employee_data(data):
    """
    Cleans the employee data by handling missing values and formatting.
    :param data: List of dictionaries (JSON-like structure)
    :return: Cleaned data as a Pandas DataFrame
    """
    df = pd.DataFrame(data)

    # Handle missing values
    df.fillna('', inplace=True)

    # Format specific columns (example: standardize phone numbers)
    if 'phone' in df.columns:
        df['phone'] = df['phone'].astype(str).str.replace(r'\D', '', regex=True)

    return df
