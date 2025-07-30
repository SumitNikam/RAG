import pandas as pd

# Function to generate the schema details
def get_schema_info(
    input_df
):
    """
    This function creates a basic schema for the given dataset.
    It creates a dictionaries with the unique values for categorical columns
    and percentiles of numeric columns

    input:
    input_df (dataframe): pandas dataframe

    output:
    numeric_dict (dict),  object_dict {dict}
    numeric_dict: dictionary with numeric data type information
    object_dict: dictionary with object data type informatio
    """
    numeric_dict = {}
    object_dict ={}
    for col in input_df:
        if input_df[col].dtype == 'O':
            object_dict[col] = input_df[col].unique()
        else:
            numeric_dict[col] = input_df.agg(
                {col:["min","max"]}
            )

    return (numeric_dict, object_dict)
