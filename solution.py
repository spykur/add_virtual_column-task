import pandas as pd
import re

# I assume that if the command is correct, there will be only two columns in the role and only one operator between them,
# and the new column name will be valid when not exist in the df to avoid overwriting existing columns.

def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    
    # Check if the new column name already exists in the df
    if new_column in df.columns:
        return pd.DataFrame()
    
    # Remove whitespaces 
    role = role.strip()
    
    # Check for number of operators in the role
    matched_operators = re.findall(r'[+\-*]', role)

    # Check if there is exactly one operator in the role
    if len(matched_operators) != 1:
        return pd.DataFrame()

    operator_found = matched_operators[0]
    
    
    components = role.split(operator_found)
    
    #Check if there are exactly two components in the role 
    if len(components) != 2:
        return pd.DataFrame()  
    
    col1, col2 = components[0].strip(), components[1].strip()
    
    # Check if the column names are valid 
    if not all(re.fullmatch(r'[A-Za-z_]+', name) for name in (col1, col2, new_column)):
        return pd.DataFrame()
    
    # Check if the columns exist in the DataFrame
    if col1 not in df.columns or col2 not in df.columns:
        return pd.DataFrame()  
    
    df_copy = df.copy()  
    
    # Perform the operation and create the new column
    if operator_found == '+':
        df_copy[new_column] = df_copy[col1] + df_copy[col2]
    elif operator_found == '-':
        df_copy[new_column] = df_copy[col1] - df_copy[col2]
    elif operator_found == '*':
        df_copy[new_column] = df_copy[col1] * df_copy[col2]
    

    return df_copy
