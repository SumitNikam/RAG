import json
import sys
import google.auth
import pandas as pd
import streamlit as st

from src.generic import read_bq_cache

from app_pages.multi_page import MultiPage
from app_pages.simulation import simulation_body
from app_pages.upload_new_data import upload_new_data_body
from app_pages.download_results import download_results_body


def main(local_flag):

    app = MultiPage(app_name="CHARM-Dashboard")

    ##############################################
    #            LOAD PARAMETERS                 #
    ##############################################
    google_project = google.auth.default()[1]
    environment = google_project.split("-")[-1]

    with open(f'config/{environment}.json', encoding='utf8') as f:
        payloads = json.load(f)

    query_params_dict = payloads['query_params_dict']
    charm_model_input_dict = payloads['charm_model_input_dict']
    cloud_run_back_end = payloads['cloud_run_back_end']

    ##############################################
    #               LOAD DATA                    #
    ##############################################

    simulation_tables = query_params_dict["base_tables"] | query_params_dict["historical"]
    for query_name, query_param in simulation_tables.items():
        if local_flag:
            df = pd.read_csv(f'assets/data/{query_name}.csv', sep=';')
        else:
            with open(f'queries/{query_name}.sql', 'rb') as f:
                query_template = f.read()
            query = query_template.decode('utf-8').format(query_param)
            df = read_bq_cache(
                google_project=google_project,
                query=query
            )
            df[df.select_dtypes(include=['int64']).columns] = df.select_dtypes(include=['int64']).astype('int')

        st.session_state[query_name] = df

    ##############################################
    #                   PAGES                    #
    ##############################################

    app.app_page(
        "Upload New Data",
        upload_new_data_body,
        google_project,
        query_params_dict,
        cloud_run_back_end
    )

    app.app_page(
        "Simulation",
        simulation_body,
        google_project,
        query_params_dict["base_tables"],
        charm_model_input_dict,
        cloud_run_back_end,
        local_flag
    )

    app.app_page(
        "Download results",
        download_results_body,
        google_project,
        query_params_dict["output_tables"],
        local_flag
    )

    app.page_run()


if __name__ == "__main__":
    local_flag = False
    if len(sys.argv) > 1:
        local_flag = sys.argv[1]
        if local_flag == 'local_flag':
            print('### Running app in local env ###')
            local_flag = True

    main(local_flag)
