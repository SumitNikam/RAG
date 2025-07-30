import streamlit as st
import pandas as pd

from src.css import st_fixed_container, st_layout_style
from src.generic import read_bq_cache


def download_results_body(
    google_project: str,
    query_params_dict: dict,
    local_flag: bool
):
    ##############################################
    #                   LAYOUT                   #
    ##############################################
    st_layout_style()

    with st_fixed_container(mode="fixed", position="top", border=False):
        st.header("📈 Download Results")

    with st.container():
        ##############################################
        #               LOAD DATA                    #
        ##############################################
        data_cols_position = st.columns(len(query_params_dict))
        for i, (query_name, query_param) in enumerate(query_params_dict.items()):
            if local_flag:
                df = pd.read_csv(f'assets/data/{query_name}.csv', sep=',')
            else:
                with open(f'queries/{query_name}.sql', 'rb') as f:
                    query_template = f.read()
                query = query_template.decode('utf-8').format(query_param)

                df = read_bq_cache(
                    google_project=google_project,
                    query=query
                )

            with data_cols_position[i]:
                st.write(f"{query_name.replace('_', ' ').title()} output:")
                # display the dataframe on streamlit app
                st.dataframe(df.head(10), hide_index=True)

                # download button 1 to download dataframe as csv
                st.download_button(
                    label=f"Download {query_name.replace('_', ' ')} as CSV",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name=f'{query_name}.csv',
                    mime='text/csv'
                )
