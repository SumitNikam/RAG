import streamlit as st

@st.cache_data
def prepare_data_schema_context(
    df_info,
    cltv_df_info
):
    revenue_df_schema_info = """This dataset appears to contain information about telecommunication transactions, likely for a company operating in Romania. Here's a breakdown:

    Column name description Information:

    connectivity revenue refers to total_s15_revenue.
    The column names with "prev" as prefix refers to outflow activity.

    - Transaction Type: "INFLOW, BASE, RETENTION, OUTFLOW" transactions are present, indicating this dataset focuses on revenue-generating activities.

    - Products: The dataset covers various telecommunication products, including fixed lines, mobile voice, mobile data, M2M services, and potentially others.

    - Segments: Customer segments are categorized as SMB (Small and Medium Businesses), MLE, Strategic, Public, Wholesale, and "Other".

    - Channels: The data includes information on the sales channels used, including Direct Sales, Indirect Sales, BSA (Business Sales Associate), Digital, and several others.

    - Geography: County and Region level information is available.

    - Revenue and Subscribers: Data points include total revenue, ARPU (Average Revenue Per User), Inbundle/Outbundle revenue, and subscriber counts(volume), giving insight into revenue generation and customer behavior.

    - Time: Data is collected over a period of time, with monthly, quarterly, and yearly breakdowns.
    """ + str(df_info)

    cltv_df_schema_info = """This dataset appears to contain information about customer lifetime and customer lifetime value. Also dataset contain inflow count for combined segment, channel and product. Here's a breakdown:

    Column name description Information:

    - PRODUCT_TYPE: The dataset covers various telecommunication products, including fixed lines, mobile voice, mobile data, M2M services, and potentially others.

    - EBU SEGMENT: Customer segments are categorized as SMB (Small and Medium Businesses), MLE, Strategic, Public, Wholesale, and "Other".

    - ACQ CHANNEL: The data includes information on the sales channels used, including Direct Sales, Indirect Sales, BSA (Business Sales Associate), Digital, and several others.

    - CLT and CLTV: Data points include CLT and CLTV giving insight into Customer lifetime and customer lifetime value.

    - INFLOW_BASE: INFLOW_BASE(volume) is count of inflow 

    - Time: Data is collected over a period of time, with monthly, quarterly, and yearly breakdowns.
    """ + str(cltv_df_info)
    
    return revenue_df_schema_info, cltv_df_schema_info

@st.cache_data
def prepare_code_generation_prompt(
    df_end_date,
    df_info,
    cltv_df_info,
    df_desc,
    cltv_df_desc
):
    context_to_llm = f"""You are a top level python programmer.
    Your job is to convert the natural language questions related to the datasets into a python snippet.
    If the question is not related to below given datasets schemas,
    then generate a standard answer as
    "Sorry, I am trained to answer questions related to the importance data and customer lifetime value(CLTV) for Romania."
    Datasets information:
    revenue_df schema: {revenue_df_schema_info},
    revenue_df data column-wise descriptions: {revenue_df_desc},
    cltv schema: {cltv_df_schema_info},
    cltv data column-wise descriptions: {cltv_df_desc}
    If the question is related to the given datasets schemas,
    then convert the natural language questions into a python snippet.
    Only consider information available in the data schema for code generation.
    Here are some general instructions.
    - Combine segment, channel and product to calculate CLT and CLTV at a cohort level.
    - Revenue, ARPU and subscriber count(volume) are the key KPI's.
    - Consider all the KPI's mentioned above to analyse the performance, in case it is not given in the question.
    - YTD means year till date.
    - FY is financial year which starts from April to March next year.
    - CLT means Customer lifetime
    - CLTV means Customer lifetime value
    - churn means outflow
    - If date is not mention in question then take max date
    - Revenue is in euros.
    - Current date for revenue_df is {revenue_df_end_date}.
    - Current date for cltv_df is {cltv_df_end_date}.
    - Do not add any textual explaination while generating a python snippet.
    - Do not modify the dataframes.
    Only python code should be an output of every question.
    Follow the instructions carefully before generating a response.
    previous_answer:""
    """
    return context_to_llm

@st.cache_data
def prepare_business_interpretation_prompt(
    df_info,
    cltv_df_info,
    df_desc,
    cltv_df_desc
):
    business_context = f"""
    You are a business analyst working with two datasets: `revenue_df` and `cltv_df`. 
    - `revenue_df` contains information about customer transactions for a telecommunications company.
    - `cltv_df` includes data on customer lifetime, inflow count, and customer lifetime value across various channels, segments, and products.

    Below are the schema and column details:
    - `revenue_df` schema: {revenue_df_info}
    - `cltv_df` schema: {cltv_df_info}
    - Column descriptions for `revenue_df`: {revenue_df_desc}
    - Column descriptions for `cltv_df`: {cltv_df_desc}

    Using the provided table information, the user's question, and the Python output (either text or plot table), frame a professional statement for a business reader. Ensure the statement:
    - Is based solely on the given data.
    - Includes numerical details.
    - Is brief and to the point.
    - Accurately describes the plot by referring to the `plot_table` and the date ranges.

    Take a deep breath and proceed.
    """
    return business_context_llm

# Instruction text to extract plot description
extraction_instruction_text = f"""You are an expert plot dataframe name extractor.
Refer the last python snippet to extract the dataframe object.
Extract the dataframe object names which are being plotted from the given python code.
Output should be the dataframe object names only,
returned as a string object in this format "plotted_object: plot object names"

#################
Example 1:
python_code: import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

# Group the sales_df by date and calculate the sum of sales
sales_df_monthly = sales_df.groupby('date')['SALE'].sum().reset_index();

# Group the costs_df by date and calculate the sum of costs
costs_df_monthly = costs_df.groupby('date')['COST'].sum().reset_index();

# Create a figure with two subplots
fig, axs = plt.subplots(2, 1, sharex=True);

# Plot the sales on the first subplot
axs[0].plot(sales_df_monthly['date'], sales_df_monthly['SALE'], color='blue', label='Sales');
axs[0].set_ylabel('Sales');
axs[0].legend();

# Plot the costs on the second subplot
axs[1].plot(costs_df_monthly['date'], costs_df_monthly['COST'], color='red', label='Costs');
axs[1].set_ylabel('Costs');
axs[1].legend();
plt.clf();
plt.xlabel('Date');
plt.ylabel('Amount');
plt.title('Sales and Cost Trend');
plt.legend();

# Save the plot to a buffer
buf = io.BytesIO();
plt.savefig(buf, format='png');

# Convert the buffer to a binary string
plot_binary = base64.b64encode(buf.getbuffer()).decode('ascii');

plotted_object: sales_df_monthly, costs_df_monthly
 
#################
Example 2:
python_code:
# Filter the costs_df to only include data for the year 2022
costs_df_2022 = costs_df[costs_df['year'] == 2022]

# Group the data by month and calculate the total cost
costs_df_2022_monthly = costs_df_2022.groupby('year_month')['COST'].sum()

plt.clf();
# Create a plot of the monthly cost trend
costs_df_2022_monthly.plot()
plt.xlabel('Month')
plt.ylabel('Cost')
plt.title('Cost Trend for 2022')

plotted_object: costs_df_2022_monthly

#################
Example 3:
python_code:
# Filter the sales_df to only include data for the year 2023
sales_df_2023 = sales_df[sales_df['year'] == 2023];

# Group the data by month and calculate the total sales
sales_by_month_2023 = sales_df_2023.groupby('month')['SALE'].sum().reset_index();

plt.clf();
# Create a line plot of the sales trend for 2023
plt.plot(sales_by_month_2023['month'], sales_by_month_2023['SALE']);
plt.xlabel('Month');
plt.ylabel('Sales');
plt.title('Sales Trend for 2023');

plotted_object: sales_by_month_2023

#################
"""

# @st.cache_data
def prepare_plot_extraction_instruction(
    instruction_text=extraction_instruction_text
):
    """
    Function to return instructions to describe the plot
    """

    return instruction_text
