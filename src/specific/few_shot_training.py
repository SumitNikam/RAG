import streamlit as st
from vertexai.language_models import InputOutputTextPair

######################################################
#    Few shot examples for within context            #
######################################################

# prepare training example list for the llm
# prepare training example list for the llm
train_example_list=[
    InputOutputTextPair(
        input_text="""For inflow, which is my top sales channel.""",
        output_text="""# Filter the data for inflow transaction type
inflow_rev_df = revenue_df[revenue_df['TRANSACTION_TYPE'] == 'INFLOW']
inflow_cltv_df = cltv_df[cltv_df['TRANSACTION_TYPE'] == 'INFLOW']

# Group the data by channel and calculate sum of subscriber count
channel_subs_count = inflow_rev_df.groupby('Channel')['Subs_Count'].sum()

# Group the data by channel and calculate sum of total/connectivity revenue
channel_revenue = inflow_rev_df.groupby('Channel')['Total_S15_Revenue'].sum()

# Filter the cltv data for ACQ_CHANNEL and PRODUCT_TYPE only for any and EBU_SEGMENT without any
cltv_without_any = current_month_cltv[(current_month_cltv['ACQ_CHANNEL']!='any') & (current_month_cltv['PRODUCT_TYPE']=='any') & (current_month_cltv['EBU_SEGMENT']=='any')]

# Group the data by channel and calculate sum of total/connectivity revenue
channel_cltv = cltv_without_any.groupby('ACQ_CHANNEL')['CLTV'].mean()

# Group the data by channel and calculate sum of total/connectivity revenue
channel_clt = cltv_without_any.groupby('ACQ_CHANNEL')['CLT'].mean()

# Calculate ARPU for each channel
channel_arpu = channel_revenue/channel_subs_count

# Get the channel with the highest subscriber count
top_channel_name_for_subs_count = channel_subs_count.idxmax()
top_channel_subs_count_value = channel_subs_count.max()

# Get the channel with the highest total revenue
top_channel_name_for_revenue = channel_revenue.idxmax()
top_channel_revenue_value = channel_revenue.max()

# Get the channel with the highest ARPU
top_channel_name_for_arpu = channel_arpu.idxmax()
top_channel_arpu_value = channel_arpu.max()

# Get the channel with the highest CLTV
top_channel_name_for_cltv = channel_cltv.idxmax()
top_channel_cltv_value = channel_cltv.max()

# Get the channel with the highest CLT
top_channel_name_for_clt = channel_clt.idxmax()
top_channel_clt_value = channel_clt.max()

# Print the top product information for volume, total revenue, ARPU, CLTV and CLT
print(f"top_channel in terms of volume {top_channel_name_for_subs_count} with value {top_channel_subs_count_value}")
print(f"top_channel in terms of total revenue {top_channel_name_for_revenue} with value {top_channel_revenue_value}")
print(f"top_channel in terms of ARPU {top_channel_name_for_arpu} with value {top_channel_arpu_value}")
print(f"top_channel in terms of CLTV {top_channel_name_for_cltv} with value {top_channel_cltv_value}")
print(f"top_channel in terms of CLT {top_channel_name_for_clt} with value {top_channel_clt_value}")
"""
    ),
    InputOutputTextPair(
        input_text="""Which sales channel contributes the most in the SMB segment""",
        output_text="""# Filter the dataset for the SMB segment
smb_df = revenue_df[revenue_df['Segment'] == 'SMB']

# Group the data by channel and calculate sum of subscriber count
channel_subs_count = smb_df.groupby('Channel')['Subs_Count'].sum()

# Group the data by channel and calculate sum of total/connectivity revenue
channel_revenue = smb_df.groupby('Channel')['Total_S15_Revenue'].sum()

# Filter the cltv data for PRODUCT_TYPE and EBU_SEGMENT only for any and ACQ_CHANNEL without any
cltv_without_any = cltv_df[(cltv_df['ACQ_CHANNEL']!='any') & (cltv_df['PRODUCT_TYPE']=='any') & (cltv_df['EBU_SEGMENT']=='any')]

# Group the data by channel and calculate sum of total/connectivity revenue
channel_cltv = cltv_without_any.groupby('ACQ_CHANNEL')['CLTV'].mean()

# Group the data by channel and calculate sum of total/connectivity revenue
channel_clt = cltv_without_any.groupby('ACQ_CHANNEL')['CLT'].mean()

# Calculate ARPU for each channel
channel_arpu = channel_revenue/channel_subs_count

# Get the channel with the highest subscriber count
top_channel_name_for_subs_count = channel_subs_count.idxmax()
top_channel_subs_count_value = channel_subs_count.max()

# Get the channel with the highest total revenue
top_channel_name_for_revenue = channel_revenue.idxmax()
top_channel_revenue_value = channel_revenue.max()

# Get the channel with the highest ARPU
top_channel_name_for_arpu = channel_arpu.idxmax()
top_channel_arpu_value = channel_arpu.max()

# Get the channel with the highest CLTV
top_channel_name_for_cltv = channel_cltv.idxmax()
top_channel_cltv_value = channel_cltv.max()

# Get the channel with the highest CLT
top_channel_name_for_clt = channel_clt.idxmax()
top_channel_clt_value = channel_clt.max()

# Print the top product information for volume, total revenue, ARPU, CLTV and CLT
print(f"top_channel in terms of volume {top_channel_name_for_subs_count} with value {top_channel_subs_count_value}")
print(f"top_channel in terms of total revenue {top_channel_name_for_revenue} with value {top_channel_revenue_value}")
print(f"top_channel in terms of ARPU {top_channel_name_for_arpu} with value {top_channel_arpu_value}")
print(f"top_channel in terms of CLTV {top_channel_name_for_cltv} with value {top_channel_cltv_value}")
print(f"top_channel in terms of CLT {top_channel_name_for_clt} with value {top_channel_clt_value}")
"""
    ),
    InputOutputTextPair(
        input_text="""Revenue generated by each product in last month?""",
        output_text="""# find the last month from data
last_month = revenue_df['year_month'].max()-1

# Filter the data for last month
last_month_df = revenue_df[revenue_df['year_month']==last_month]

# Group the data by product and calculate sum of total revenue
product_revenue = last_month_df.groupby('Product')['Total_S15_Revenue'].sum()

# Print the product with the highest revenue
print(f"Product with highest revenue {product_revenue.idxmax()} with value {product_revenue.max()}")

# Print the revenue generated by each product
for product, revenue in product_revenue.items():
    print(f"{product}: {revenue}")
"""
    ),
    InputOutputTextPair(
        input_text="""Which channel has worst ARPU?""",
        output_text="""# Calculate ARPU for each channel
channel_arpu = revenue_df.groupby('Channel')['ARPU'].mean()

# Get the channel with the lowest ARPU
worst_channel_arpu = channel_arpu.idxmin()

# Get the channel value with the lowest ARPU
worst_channel_arpu_value = channel_arpu.min()

# Print the worst channel with value
print(f"Channel with lowest ARPU: {worst_channel_arpu} with {worst_channel_arpu_value}")
"""
    ),
    InputOutputTextPair(
        input_text="""Which is the best performing Segment according to CLT?""",
        output_text="""# find the current month from cltv dataframe
current_month = cltv_df['year_month'].max()

# Filter the data for current month
current_month_cltv = cltv_df[cltv_df['year_month']==current_month]

# Filter the cltv data for ACQ_CHANNEL and PRODUCT_TYPE only for any and EBU_SEGMENT without any
clt_with_any = current_month_cltv[(current_month_cltv['ACQ_CHANNEL']=='any') & (current_month_cltv['PRODUCT_TYPE']=='any') & (current_month_cltv['EBU_SEGMENT']!='any')]

# Get the Segment with the highest CLTV
top_Segment_cltv = cltv_with_any['CLTV'].idxmax()

# Get the Segment value with the highest CLTV
top_Segment_cltv_value = cltv_with_any['CLTV'].max()

# Print the highest Segment with value
print(f"Segment with highest CLTV: {top_Segment_cltv} with {top_Segment_cltv_value}")
"""
    ),
    InputOutputTextPair(
        input_text="""Which product has the maximum CLTV for the month of 202403?""",
        output_text="""# Filter the data for the month of 202403
cltv_202403 = cltv_df[cltv_df['year_month']=='2024-03']

# Filter the cltv data for ACQ_CHANNEL and EBU_SEGMENT only for any and PRODUCT_TYPE without any
cltv_with_any = cltv_202403[(cltv_202403['ACQ_CHANNEL']=='any') & (cltv_202403['PRODUCT_TYPE']!='any') & (cltv_202403['EBU_SEGMENT']=='any')]

# Get the Segment with the highest CLTV
top_product_cltv = cltv_with_any['CLTV'].idxmax()

# Get the Segment value with the highest CLTV
top_product_cltv_value = cltv_with_any['CLTV'].max()

# Print the highest CLTV with value
print(f"Product with highest CLTV: {top_product_cltv} with {top_product_cltv_value} for month 202403")
"""
    ),
    InputOutputTextPair(
        input_text="""Which cohort has the maximum inflow count for the month of 202303?""",
        output_text="""# Filter the data for the month of 202303
cltv_202303 = cltv_df[cltv_df['year_month']=='2023-03']

# Ignore any from segment, channel and prduct
cltv_without_any = cltv_202303[(cltv_202303['ACQ_CHANNEL']!='any') & (cltv_202303['PRODUCT_TYPE']!='any') & (cltv_202303['EBU_SEGMENT']!='any')]

# Get the cohort with the maximum inflow count
max_inflow_cohort = cltv_without_any.loc[cltv_without_any['INFLOW_BASE'].idxmax()]

# Print the cohort with the maximum inflow count
print(f"Cohort with maximum inflow count: {max_inflow_cohort}")
"""
    ),
    InputOutputTextPair(
        input_text="""Which is the best performing channel as per clt for march 2024""",
        output_text="""# Filter the data for the month of 202403
clt_df_202403 = cltv_df[cltv_df['year_month']=='2024-03']

# Filter the clt data for ACQ_CHANNEL and PRODUCT_TYPE only for any and EBU_SEGMENT without any
clt_with_any = clt_df_202403[(clt_df_202403['EBU_SEGMENT']=='any') & (clt_df_202403['PRODUCT_TYPE']=='any') & (clt_df_202403['ACQ_CHANNEL']!='any')]

# Sort by Revenue in descending order and get top 3
top3_sales_channel_clt = clt_with_any.sort_values(by='CLT', ascending=False).reset_index(drop=True).head(3)

print("Top 3 Channel by CLT:")
print(top3_sales_channel_clt)
"""
    ),
    InputOutputTextPair(
        input_text="""Which is the best performing channel as per cltv?""",
        output_text="""# find the current month from cltv dataframe
current_month = cltv_df['year_month'].max()

# Filter the cltv data for current month
current_month_cltv = cltv_df[cltv_df['year_month']==current_month]

# Filter the cltv data for EBU_SEGMENT and PRODUCT_TYPE only for any and ACQ_CHANNEL without any
cltv_with_any = current_month_cltv[(current_month_cltv['EBU_SEGMENT']=='any') & (current_month_cltv['PRODUCT_TYPE']=='any') & (current_month_cltv['ACQ_CHANNEL']!='any')]

# Sort by Revenue in descending order and get top 3
top3_sales_channel_cltv = cltv_with_any.sort_values(by='CLTV', ascending=False).reset_index(drop=True).head(3)

print("Top 3 Channel by CLTV:")
print(top3_sales_channel_cltv)
"""
    ),
    InputOutputTextPair(
        input_text="""Which is the best performing segment for March-2024?""",
        output_text="""# Filter the data for the month of 202403
revenue_df_202403 = revenue_df[revenue_df['year_month']=='2024-03']

# Group the data by Segment and calculate sum of subscriber count
Segment_subs_count = revenue_df_202403.groupby('Segment')['Subs_Count'].sum()

# Group the data by Segment and calculate sum of total/connectivity revenue
Segment_revenue = revenue_df_202403.groupby('Segment')['Total_S15_Revenue'].sum()

# Calculate ARPu for each Segment
Segment_arpu = Segment_revenue/Segment_subs_count

# Get the Segment with the highest subscriber count
top_Segment_name_for_subs_count = Segment_subs_count.idxmax()
top_Segment_subs_count_value = Segment_subs_count.max()

# Get the Segment with the highest total revenue
top_Segment_name_for_revenue = Segment_revenue.idxmax()
top_Segment_revenue_value = Segment_revenue.max()

# Get the Segment with the highest arpu
top_Segment_name_for_arpu = Segment_arpu.idxmax()
top_Segment_arpu_value = Segment_arpu.max()

# Print the top Segment information for volume, total revenue and ARPU
print(f"top_Segment in terms of volume {top_Segment_name_for_subs_count} with value {top_Segment_subs_count_value}")
print(f"top_Segment in terms of total revenue {top_Segment_name_for_revenue} with value {top_Segment_revenue_value}")
print(f"top_Segment in terms of ARPU {top_Segment_name_for_arpu} with value {top_Segment_arpu_value}")
"""
    ),
    InputOutputTextPair(
        input_text="""Which sales channel contributes most in the SMB segment with respect rev?""",
        output_text="""# Filter for SMB segment
smb_df = revenue_df[revenue_df['Segment'] == 'SMB']

# find the current month from cltv dataframe
current_month = smb_df['year_month'].max()

# Filter the data for current month
current_month_revenue_df = smb_df[smb_df['year_month']==current_month]

# Group the data by channel and calculate sum of total/connectivity revenue
channel_revenue = current_month_revenue_df.groupby('Channel')['Total_S15_Revenue'].sum().reset_index()

# Sort by Revenue in descending order and get top 3
top3_sales_channel_rev = channel_revenue.sort_values(by='Total_S15_Revenue', ascending=False).reset_index(drop=True).head(3)

print("Top 3 Channel by CLTV:")
print(top3_sales_channel_rev)
"""
    ),
    InputOutputTextPair(
        input_text="""What is overall CLTV?""",
        output_text="""# Calculate the overall CLTV Filter the cltv data for ACQ_CHANNEL, PRODUCT_TYPE and EBU_SEGMENT only for any
cltv_only_any = cltv_df[(cltv_df['ACQ_CHANNEL']=='any') & (cltv_df['PRODUCT_TYPE']=='any') & (cltv_df['EBU_SEGMENT']=='any')]
overall_cltv = cltv_only_any.loc[cltv_only_any['CLTV'].idxmax()]

# Print the overall CLTV
print(f"Overall CLTV: {overall_cltv}")
"""
    ),
    InputOutputTextPair(
        input_text="""Tell me the top 10 channel by churn""",
        output_text="""# Filter the data for outflow transaction type
churn_df = revenue_df[revenue_df['TRANSACTION_TYPE'] == 'OUTFLOW']

# Group the data by channel and calculate sum of subscriber count
channel_subs_count = churn_df.groupby('Channel')['Subs_Count'].sum()

# Sort the channel_subs_count in descending order and get the top 10
top10_channel_churn = channel_subs_count.sort_values(ascending=False).head(10)

print("Top 10 channel by churn:")
print(top10_channel_churn)
"""
    ),
    InputOutputTextPair(
        input_text="""Which product contributes the most in the SMB segment""",
        output_text="""# Filter the dataset for the SMB segment
smb_df = revenue_df[revenue_df['Segment'] == 'SMB']

# Group the data by product and calculate sum of subscriber count
product_subs_count = smb_df.groupby('Product')['Subs_Count'].sum()

# Group the data by product and calculate sum of total/connectivity revenue
product_revenue = smb_df.groupby('Product')['Total_S15_Revenue'].sum()

# Filter the cltv data for ACQ_CHANNEL and EBU_SEGMENT only for any and PRODUCT_TYPE without any
cltv_without_any = cltv_df[(cltv_df['ACQ_CHANNEL']=='any') & (cltv_df['PRODUCT_TYPE']!='any') & (cltv_df['EBU_SEGMENT']=='any')]

# Group the data by product and calculate sum of total/connectivity revenue
product_cltv = cltv_without_any.groupby('PRODUCT_TYPE')['CLTV'].mean()

# Group the data by product and calculate sum of total/connectivity revenue
product_clt = cltv_without_any.groupby('PRODUCT_TYPE')['CLT'].mean()

# Calculate ARPU for each product
product_arpu = product_revenue/product_subs_count

# Get the product with the highest subscriber count
top_product_name_for_subs_count = product_subs_count.idxmax()
top_product_subs_count_value = product_subs_count.max()

# Get the product with the highest total revenue
top_product_name_for_revenue = product_revenue.idxmax()
top_product_revenue_value = product_revenue.max()

# Get the product with the highest ARPU
top_product_name_for_arpu = product_arpu.idxmax()
top_product_arpu_value = product_arpu.max()

# Get the product with the highest CLTV
top_product_name_for_cltv = product_cltv.idxmax()
top_product_cltv_value = product_cltv.max()

# Get the product with the highest CLT
top_product_name_for_clt = product_clt.idxmax()
top_product_clt_value = product_clt.max()

# Print the top product information for volume, total revenue, ARPU, CLTV and CLT
print(f"top_product in terms of volume {top_product_name_for_subs_count} with value {top_product_subs_count_value}")
print(f"top_product in terms of total revenue {top_product_name_for_revenue} with value {top_product_revenue_value}")
print(f"top_product in terms of ARPU {top_product_name_for_arpu} with value {top_product_arpu_value}")
print(f"top_product in terms of CLTV {top_product_name_for_cltv} with value {top_product_cltv_value}")
print(f"top_product in terms of CLT {top_product_name_for_clt} with value {top_product_clt_value}")
"""
    )
]

@st.cache_data
# Function to return training examples in app.py
def few_shot_examples(
    train_examples=train_example_list
):
    """
    Function to store and return the training
    examples for a code genration llm

    train_examples : List of training examples for code generation as per
    InputOutputTextPair format specified by
    chatbison requirements    
    """
    return train_examples
