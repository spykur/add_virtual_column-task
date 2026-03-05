import pandas as pd
import re

def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    
    if new_column in df.columns:
        return pd.DataFrame()
    
    # Remove extra spaces from the role
    role = role.strip()
    
    # Check for the presence of a valid operator in the role
    matched_operators = re.findall(r'[+\-*]', role)

    if len(matched_operators) != 1:
        return pd.DataFrame()

    operator_found = matched_operators[0]
    
    # Split the role into components
    components = role.split(operator_found)
    
    if len(components) != 2:
        return pd.DataFrame()  # Return empty DataFrame if the rule does not have exactly two components
    
    col1, col2 = components[0].strip(), components[1].strip()
    
    if not all(re.fullmatch(r'[A-Za-z_]+', name) for name in (col1, col2, new_column)):
        return pd.DataFrame()
    # Check if the columns exist in the DataFrame
    if col1 not in df.columns or col2 not in df.columns:
        return pd.DataFrame()  # Return empty DataFrame if any of the columns do not exist
    
    df_copy = df.copy()  # Create a copy of the DataFrame to avoid modifying the original
    
    # Perform the operation based on the operator found
    if operator_found == '+':
        df_copy[new_column] = df_copy[col1] + df_copy[col2]
    elif operator_found == '-':
        df_copy[new_column] = df_copy[col1] - df_copy[col2]
    elif operator_found == '*':
        df_copy[new_column] = df_copy[col1] * df_copy[col2]
    
    return df_copy