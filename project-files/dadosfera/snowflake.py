import os
import pandas as pd
from snowflake.snowpark import functions as F
import orchest as utils

connection_parameters = {
    "user": os.environ.get('SNOWFLAKE_USER'),
    "password": os.environ.get('SNOWFLAKE_PASSWORD'),
    "account": os.environ.get('SNOWFLAKE_ACCOUNT'), 
    "warehouse": 'COMPUTE_WH',
    "database": os.environ.get('SNOWFLAKE_DATABASE'),
    "schema": 'PUBLIC',
}


def create_pandas_df(snowpark_df):
    rows = snowpark_df.collect()
    
    data = []
    for row in rows:
        data.append(row.as_dict())
    
    df = pd.DataFrame(data)
    for column in df.columns:
        df = df.rename({column: column.lower()}, axis=1)
        
    return df

def remove_quotes_from_columns(df, columns):
    clean_function = [
        F.trim(F.replace(column, '"', ''))
        for column in columns
    ]
    
    df = df.with_columns(columns, clean_function)
    return df

def empty_string_as_null(df, columns):
    empty_string_as_null_columns = [
        f"nullif({column}, '') as {column}"
        for column in columns
    ]
    
    df = df.selectExpr(*empty_string_as_null_columns)
    return df