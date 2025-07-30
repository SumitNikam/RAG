import datetime

import pandas as pd


def extract_year_month(
    input_df,
    date_col,
    date_format='%Y%m',
):
    """
    This function helps to extract month and year from the date column.

    input:
    input_df (dataframe): pandas dataframe
    date_col (str): name of the date column
    date_format (str): the format to parse the date, default='%Y%m'

    output:
    input_df[date, year_col, month_col, quarter_col]
    """
    # Convert the REPORTING_DATE column to datetime
    input_df['date'] = pd.to_datetime(
        input_df[date_col],
        format=date_format
    )
    # Extract the year, month and quarter from the date column
    input_df['year'] = input_df['date'].dt.year
    input_df['month'] = input_df['date'].dt.month
    input_df['quarter'] = input_df['date'].dt.quarter
    input_df['year_month'] = pd.PeriodIndex(input_df.date, freq='M')
    input_df['year_quarter'] = pd.PeriodIndex(input_df.date, freq='Q')
    input_df.drop([date_col], axis=1, inplace=True)
    return input_df
