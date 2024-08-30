import os
import pandas as pd
import numpy as np

def read_file(file_path, sep=';', encoding='utf-8'):
    """
    Read a file from the specified path.

    Parameters:
        file_path (str): Path to the file.
        sep (str, optional): Separator to use when reading CSV files. Defaults to ','.
        encoding (str, optional): Encoding to use when reading the file. Defaults to 'utf-8'.

    Returns:
        DataFrame: DataFrame containing the data from the file, or None if the file doesn't exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at the specified path: {file_path}")

    # Determine file type based on extension
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == ".csv":
        # Read CSV file
        data = pd.read_csv(file_path, sep=sep, encoding=encoding)
    elif file_ext in [".xls", ".xlsx"]:
        # Read Excel file
        data = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")
    
    return data

def add_metabolite_column(data):
    """
    Add a column called 'metabolite' to the DataFrame based on the values in the 'RT(min)' and 'MZ' columns.

    Parameters:
        data (DataFrame): Input DataFrame containing 'RT(min)' and 'MZ' columns.

    Returns:
        DataFrame: DataFrame with the 'metabolite' column added.
    """
    data['metabolite'] = 'M' + data['Mz'].astype(str) + 'T' + data['Rt(min)'].astype(str)
    return data


def filter_column(data, include=None, exclude=None):
    """
    Filter columns from a DataFrame based on included and excluded columns.

    Parameters:
        data (DataFrame): Input DataFrame.
        include(list, optional): List of column names to include. Default is None.
        exclude (list, optional): List of column names to exclude. Default is None.

    Returns:
        DataFrame: DataFrame containing filtered columns.
    """
    if include is None and exclude is None:
        raise ValueError("Either 'include' or 'exclude' must be provided.")

    if include is not None and exclude is not None:
        raise ValueError("Only one of 'include' or 'exclude' should be provided.")

    if include is not None:
        selected_columns = include
    else:
        selected_columns = [col for col in data.columns if col not in exclude]

    selected_data = data[selected_columns]
    return selected_data

def select_columns_with_metabolites_columns(data, list_columns=None):
    """
    Selects columns from a DataFrame that start with "M" and includes additional columns specified in the list.

    Parameters:
    - data: DataFrame
        The input DataFrame from which columns will be selected.
    - list_columns: list or None, optional
        A list of additional columns to include along with the columns starting with "M". If None, only columns starting with "M" will be selected. Default is None.

    Returns:
    - DataFrame
        A subset of the input DataFrame containing selected columns.
    """
    # Select columns that start with "M"
    m_columns = [col for col in data.columns if col.startswith("M")]
    
    # If list_columns is not provided, return only columns starting with "M"
    if list_columns is None:
        return data[m_columns]
    
    # Include additional columns specified in the list_columns list
    selected_columns = m_columns + list_columns
    
    # Return the subset of the DataFrame with selected columns
    return data[selected_columns]

def filter_rows(data, include=None, exclude=None):
    """
    Select and/or exclude rows based on specific conditions.

    Parameters:
        data (DataFrame): Input DataFrame.
        include (str or list): Condition(s) to include rows (optional) ex: list =["column1 == 'value'", "column2 <10"].
        exclude (str or list): Condition(s) to exclude rows (optional) ex: list =["column1 == 'value'", "column2 <10"].

    Returns:
        DataFrame: Filtered DataFrame.
    """
    if include is not None:
        if isinstance(include, str):
            include_condition = include
        elif isinstance(include, list):
            include_condition = ' or '.join(include)
        else:
            raise ValueError("Include parameter must be a string or a list of strings.")
    else:
        include_condition = None

    if exclude is not None:
        if isinstance(exclude, str):
            exclude_condition = exclude
        elif isinstance(exclude, list):
            exclude_condition = ' and '.join(['not (' + cond + ')' for cond in exclude])
        else:
            raise ValueError("Exclude parameter must be a string or a list of strings.")
    else:
        exclude_condition = None

    if include_condition is not None:
        selected_data = data.query(include_condition)
    else:
        selected_data = data

    if exclude_condition is not None:
        excluded_data = selected_data.query(exclude_condition)
    else:
        excluded_data = selected_data

    return excluded_data


def transpose_data(data, metabolite_column):
    """
    Transpose the data with specified column values as column names.

    Parameters:
        data (DataFrame): Input DataFrame.
        metabolite_column (str): Name of the column to use as column names.

    Returns:
        DataFrame: Transposed DataFrame with specified column values as column names.
    """
    transposed_data = data.set_index(metabolite_column).T
    transposed_data.index.name ='sample_name'
    return transposed_data

def merge_data(df1, df2):
    """
    Merge two datasets based on their indices.
    Make sue that the indices are the same in both datasets

    Parameters:
        df1 (DataFrame): First DataFrame.
        df2 (DataFrame): Second DataFrame.
    
    Returns:
        DataFrame: Merged DataFrame.
    """
    merged_data = pd.merge(df1, df2, left_index=True, right_index=True, how='outer')
    return merged_data


import pandas as pd

def blank_filter(data, condition_column='SampleType', condition_values=['blank'], operation='!=', threshold=0):
    """
    Filter columns from a DataFrame based on a condition applied to specific rows.

    Parameters:
    - data: DataFrame
        The input DataFrame from which columns will be removed.
    - condition_column: str
        The name of the column to use as the condition (default parameter = 'SampleType').
    - condition_values: list
        A list of values in the condition_column to consider for the condition (default parameter = ['blank']).
    - operation: str
        The comparison operation to apply. Supported operations are '!=', '<=', '>=', and '=' (default parameter = '!=').
    - threshold: int or float
        The threshold value for the condition (default parameter = 0).

    Returns:
    - DataFrame
        A modified DataFrame with columns removed based on the specified condition.
    """
    # Find rows where the condition is met
    rows_to_check = data[data[condition_column].isin(condition_values)].index
    special_rows = data.loc[rows_to_check]

    # Convert non-numeric values to numeric
    special_rows = special_rows.apply(pd.to_numeric, errors='coerce')

    # Get columns based on the specified operation and threshold
    if operation == '!=':
        filtered_columns = special_rows.loc[:, (special_rows != threshold).any()]
    elif operation == '<=':
        filtered_columns = special_rows.loc[:, (special_rows <= threshold).any()]
    elif operation == '>=':
        filtered_columns = special_rows.loc[:, (special_rows >= threshold).any()]
    elif operation == '=':
        filtered_columns = special_rows.loc[:, (special_rows == threshold).any()]
    else:
        raise ValueError("Unsupported operation. Supported operations are '!=', '<=', '>=', and '='")

    # Get column names
    column_names = filtered_columns.columns.tolist()

    # Remove columns from the DataFrame
    data_filtered = data.drop(column_names, axis=1)

    return data_filtered

def cv_filter(data, raw_list, threshold =20, operation = "<=" ):
    """
    Calculate the coefficient of variation (CV) for each column between given rows and filter based on threshold.

    Requirement:
    -  filter_rows function

    Parameters:
    - data: DataFrame
        The input DataFrame from which columns will be selected.
    - raw_list: list
        liste of rows to compare (ex: raw_list = ["sample_name == '240326NCE_Globale_neg_QC3-DIL8'", "sample_name == '240326NCE_Globale_neg_QC3'" , "sample_name == '240326NCE_Globale_neg_QC3-DIL2'"]).
    - threshold: int 
        cv threasholf of filtering (defolt = 20)
    - operation: "<=", ">="
        the fitration index: drop those how huer or less than threshold 

    Returns:
    - DataFrame
        A DataFrame data filtered based on the threshold given.
    """
    #filter QCDil2, QCDil8 and QC3 raws
    CV_data = filter_rows(data, include = raw_list)
    # Convert non-numeric values to numeric
    CV_data = CV_data.apply(pd.to_numeric, errors='coerce')
    # Calculate the mean and standard deviation for each column
    mean_values = CV_data.mean()
    std_values = CV_data.std()
    
    # Calculate the coefficient of variation (CV) for each column
    cvs = (std_values / mean_values) * 100

    # Identify columns with CV greater than the threshold
    if operation == '<=':
        columns_to_drop = cvs[cvs <= threshold].index.tolist()
    elif operation == '>=':
        columns_to_drop = cvs[cvs >= threshold].index.tolist()

    # Drop the identified columns from the DataFrame
    filtered_data = data.drop(columns_to_drop, axis=1)
    
    return filtered_data

def QC_filter(data, value_threshold=0):
    """
    Drop columns from a DataFrame where the value is 0 in at least 3/4 of the QCs.

    Parameters:
    - data: DataFrame
        The input DataFrame from which columns will be removed.
    - value_threshold: int
        The threshold value for the proportion (default parameter = 1000).

    Returns:
    - DataFrame
        A modified DataFrame with columns removed based on the specified condition.
    """
    # Select the last QC rows
    filtered_QC = data[data.index.to_series().str.contains(r'QC', regex=True, na=False)]

    # Exclude rows ending with 'DIL' followed by any number
    filtered_DIL = filtered_QC[~filtered_QC.index.to_series().str.contains(r'dil', regex=True, na=False)]
    filtered_rows = filtered_DIL.apply(pd.to_numeric, errors='coerce')
    
    # Calculate the proportion of zeros in each column
    QCthreshold_float = len (filtered_rows) * (3/4)
    QCthreshold = int(np.round(QCthreshold_float))
    zero_counts = (filtered_rows == value_threshold).sum()

    # Identify columns where the proportion of zeros exceeds the threshold
    columns_to_keep = []
    columns_to_drop = []
    for column, zero_count in zero_counts.items():
        if zero_count >= QCthreshold:
            columns_to_drop.append(column)
        else:
            columns_to_keep.append(column)

    # Drop identified columns from the DataFrame
    data_filtered = data.drop(columns=columns_to_drop)

    return data_filtered

def reading_alignData(output_path_POS, output_path_NEG, metadata_file_POS, metadata_file_NEG):
    # Validate input and output paths
    if not os.path.exists(output_path_POS) or not os.path.exists(output_path_NEG):
        print("Error: Output directories not found.")
        return None, None, None, None
    if not os.path.exists(metadata_file_POS) or not os.path.exists(metadata_file_NEG):
        print("Error: Metadata files not found.")
        return None, None, None, None

    # Read metadata for POS
    metadata_df_POS = pd.read_csv(metadata_file_POS, sep=";")

    # Read metadata for NEG
    metadata_df_NEG = pd.read_csv(metadata_file_NEG, sep=";")

    # Read and convert MSDIAL files to DataFrames for POS data
    pos_data = []
    for file_POS in os.listdir(output_path_POS):
        if file_POS.startswith("AlignResult-") and file_POS.endswith(".msdial"):
            msdial_file_POS = os.path.join(output_path_POS, file_POS)
            df_POS = pd.read_csv(msdial_file_POS, delimiter='\t')
            pos_data.append(df_POS)

    # Read and convert MSDIAL files to DataFrames for NEG data
    neg_data = []
    for file_NEG in os.listdir(output_path_NEG):
        if file_NEG.startswith("AlignResult-") and file_NEG.endswith(".msdial"):
            msdial_file_NEG = os.path.join(output_path_NEG, file_NEG)
            df_NEG = pd.read_csv(msdial_file_NEG, delimiter='\t')
            neg_data.append(df_NEG)

    if not pos_data:
        print("Error: No POS data found.")
        return None, None, None, None

    if not neg_data:
        print("Error: No NEG data found.")
        return None, None, None, None

    # Concatenate the list of DataFrames into single DataFrames
    pos_df = pd.concat(pos_data, axis=1)
    neg_df = pd.concat(neg_data, axis=1)

    print("Data loaded successfully.")
    return pos_df, neg_df, metadata_df_POS, metadata_df_NEG


def save_as_csv(data, output_dir, output_file, file_conflict="skip"):
    """
    Save DataFrame as a CSV file in the given directory.

    Parameters:
        data (DataFrame): DataFrame to be saved.
        output_dir (str): Directory where the CSV file will be saved.
        output_file (str): Name of the CSV file (without the extension).
        file_conflict (str): Behavior in case of a file conflict.
            - "skip": Skip saving the file (default).
            - "replace": Replace the existing file.
            - "append": Append to the existing file.

    Returns:
        str: Path to the saved CSV file, or None if saving is skipped.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct the full path to the output file
    output_path = os.path.join(output_dir, output_file + ".csv")
    
    # Check if a file with the same name already exists
    if os.path.exists(output_path):
        if file_conflict == "skip":
            print("Saving skipped.")
            return None
        elif file_conflict == "replace":
            # Replace the existing file
            data.to_csv(output_path, index=True, sep = ';')
            print("Existing file replaced.")
        elif file_conflict == "append":
            # Append to the existing file
            existing_data = pd.read_csv(output_path)
            combined_data = pd.concat([existing_data, data], ignore_index=True)
            combined_data.to_csv(output_path, index=True, sep = ';')
            print("Data appended to the existing file.")
        else:
            print("Invalid value for 'file_conflict'. Skipping saving.")
            return None
    else:
        # Save the DataFrame as a new CSV file
        data.to_csv(output_path, index=True, sep=';')
        print("CSV file saved.")
    
    return output_path