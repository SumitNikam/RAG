import json
import streamlit as st
import ast

from src.css import st_fixed_container, st_layout_style
from src.generic import request
from src.specific import charm_model_input_parameters


def simulation_body(
    google_project: str,
    query_params_dict: dict,
    charm_model_input_dict: dict,
    cloud_run_back_end: str,
    local_flag: str
):
    ##############################################
    #                   LAYOUT                   #
    ##############################################
    st_layout_style()

    with st_fixed_container(mode="fixed", position="top", border=False):
        st.header("📈 Run Simulation")

    with st.container():
        ##############################################
        #               LOAD DATA                    #
        ##############################################
        without_Historical_data_tab, Historical_data_tab = st.tabs(
            ["Without Historical data", "Historical data"]
        )
        charm_model_input = charm_model_input_dict.copy()

        with without_Historical_data_tab:
            parameters_input_dict = charm_model_input_parameters(
                charm_model_input_dict=charm_model_input_dict,
                query_params_dict=query_params_dict,
                local_flag=local_flag,
                google_project=google_project
            )

        with Historical_data_tab:
            # Date Input and Filtering
            st.subheader("Date Selection")
            historical = st.session_state["historical_parameters"]
            if historical is not None:
                quater = st.selectbox("Select a Quater", list(historical['quarter'].unique()), index=None, placeholder="Select Quater")
                if quater:
                    option = st.selectbox("Select a Execution Date", list(historical[historical['quarter'] == quater]['execution_date'].unique()), index=None, placeholder="Select Exeution Date")
                    if option:
                        historical_input_dict = ast.literal_eval(list(historical[(historical['quarter'] == quater) & (historical['execution_date'] == option)].reset_index(drop=True)['parameters_data'])[-1])
                        parameters_dict = {k: v for k, v in historical_input_dict.items() if k in charm_model_input}
                        data_dict = {k: v for k, v in historical_input_dict.items() if k in query_params_dict}

                        parameters_input_dict = charm_model_input_parameters(
                            charm_model_input_dict=parameters_dict,
                            query_params_dict=query_params_dict,
                            local_flag=local_flag,
                            google_project=google_project,
                            historical=data_dict
                        )
            else:
                st.info("There is no history generated yet. Please perform a first run to be able to access this feature.")
        st.divider()
        apply_submitted = st.button("Run Simulation")
        if apply_submitted:
            st.write("Running simulation...")
            request_response = request(
                f"{cloud_run_back_end}/simulation",
                parameters_input_dict
            )
            if request_response.status_code != 200:
                st.error(request_response.status_code, request_response.reason)
            else:
                request_status = json.loads(request_response.text)['status']
                if request_status == "Success":
                    st.info(f"{request_status}: New data loaded successfully")
                else:
                    request_message = json.loads(request_response.text)['message']
                    st.warning(f"{request_status}: {request_message}")
