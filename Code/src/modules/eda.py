# importing required libraries
import pandas as pd


def summarize_one(col:str, df:pd.DataFrame, enforce_counts:bool = False):

    # Check if the column is in the dataframe
    if col not in df.columns:
        raise ValueError(f"{col} is not a column in the dataframe.")
    

    
    # Calculate the number of unique values and missing values
    n_unique = df[col].nunique()
    n_missing = df[col].isna().sum()
    
    # Print the summary
    print("\n"*3)
    print("="*80)
    print(col + "\t"*4 + "type: " + str(df[col].dtype))
    print("="*80)
    
    if n_unique < 30 or enforce_counts:
        print(df[col].value_counts())
    else:
        print(f"There are {n_unique} unique values in the {col} column.")
    
    print(f"There are {n_missing} missing values in the {col} column.")

def summarize(df:pd.DataFrame, cols:list = [], enforce_counts:bool = False):
    """
    Summarize a dataframe or a list of columns in a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to summarize.
    cols : list, optional
        The columns to summarize.
    enforce_counts : bool, optional
        Whether to enforce the value counts for all columns. The default is False.
    """
    if cols == []:
        cols = df.columns
    
    for col in cols:
        summarize(df, col, enforce_counts)