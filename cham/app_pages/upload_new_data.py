import json
import streamlit as st
import pandas as pd

from src.css import st_fixed_container, st_layout_style
from src.generic import request


def upload_new_data_body(
    google_project: str,
    query_params_dict: dict,
    cloud_run_back_end: str
):
    ##############################################
    #                   LAYOUT                   #
    ##############################################
    st_layout_style()

    with st_fixed_container(mode="fixed", position="top", border=False):
        st.header("⬆️ Upload New Data")

    with st.container():
        ##############################################
        #           UPLOAD & DOWNLOAD FILE           #
        ##############################################

        projects_tab, controls_tab, mitre_techniques_tab, risks_tab, threat_scenarios_tab = st.tabs(
            ["Projects", "Controls", "Mitre Techniques", "Risks", "Threat Scenarios"]
        )

        with projects_tab:
            st.markdown("""
            #### Upload Projects Data
            Required columns for the Excel file: :blue-background[**project_id, project_name**]
            """)
            projects_file = st.file_uploader("Projects",
                                             type="xlsx",
                                             label_visibility="collapsed")

            if projects_file is not None:
                projects_df = pd.read_excel(projects_file)
                st.info("File received")

                if 'project' not in st.session_state:
                    st.session_state.project = {"input": projects_df}
                else:
                    st.session_state.project['input'] = projects_df.copy()

                if 'project' in st.session_state:
                    st.session_state.project_tab = 'project_tab'

            st.markdown("""
            #### Upload Controls Projects Mapping Data
            Required columns for the Excel file:
            :blue-background[**control_id, project_id, control_effectiveness**]
            """)
            controls_projects_file = st.file_uploader("Controls Projects Mapping",
                                                      type="xlsx",
                                                      label_visibility="collapsed",
                                                      key="button1")

            if controls_projects_file is not None:
                controls_projects_df = pd.read_excel(controls_projects_file)
                st.info("File received")

                if 'controls_project_mapping' not in st.session_state:
                    st.session_state.controls_project_mapping = {"input": controls_projects_df}
                else:
                    st.session_state.controls_project_mapping['input'] = controls_projects_df.copy()

        with controls_tab:
            st.markdown("""
            #### Upload Controls Data
            Required columns for the Excel file:
            :blue-background[**control_id, control_name, domain**]
            """)
            # download_project_template = st.button("Download Sample Excel File")
            controls_file = st.file_uploader("Controls",
                                             type="xlsx",
                                             label_visibility="collapsed")

            if controls_file is not None:
                controls_df = pd.read_excel(controls_file)
                st.info("File received")

                if 'control' not in st.session_state:
                    st.session_state.control = {"input": controls_df}
                else:
                    st.session_state.control['input'] = controls_df.copy()

                if 'control' in st.session_state:
                    st.session_state.control_tab = 'control_tab'

            st.markdown("""
            #### Upload Controls Projects Mapping Data
            Required columns for the Excel file:
            :blue-background[**control_id, project_id, control_effectiveness**]
            """)
            controls_projects_file = st.file_uploader("Controls Projects Mapping",
                                                      type="xlsx",
                                                      label_visibility="collapsed",
                                                      key="button2")

            if controls_projects_file is not None:
                controls_projects_df = pd.read_excel(controls_projects_file)
                st.info("File received")

                if 'controls_project_mapping' not in st.session_state:
                    st.session_state.controls_project_mapping = {"input": controls_projects_df}
                else:
                    st.session_state.controls_project_mapping['input'] = controls_projects_df.copy()

            st.markdown("""
            #### Upload Threat Scenario Controls Mapping Data
            Required columns for the Excel file:
            :blue-background[**ts_id, risk_id, control_id, weight**]
            """)
            ts_controls_file = st.file_uploader("Threat Scenario Controls Mapping",
                                                type="xlsx",
                                                label_visibility="collapsed")

            if ts_controls_file is not None:
                ts_controls_df = pd.read_excel(ts_controls_file)
                st.info("File received")

                if 'ts_controls_mapping' not in st.session_state:
                    st.session_state.ts_controls_mapping = {"input": ts_controls_df}
                else:
                    st.session_state.ts_controls_mapping['input'] = ts_controls_df.copy()

            st.markdown("""
            #### Upload Threat Scenario Controls Mitre Mapping Data
            Required columns for the Excel file:
            :blue-background[**ts_id, control_id, mitre_technique_id, control_weight_value**]
            """)
            ts_controls_mitre_file = st.file_uploader("Threat Scenario Controls Mitre Mapping",
                                                      type="xlsx",
                                                      label_visibility="collapsed",
                                                      key="button3")

            if ts_controls_mitre_file is not None:
                ts_controls_mitre_df = pd.read_excel(ts_controls_mitre_file)
                st.info("File received")

                if 'ts_controls_mitre_mapping' not in st.session_state:
                    st.session_state.ts_controls_mitre_mapping = {"input": ts_controls_mitre_df}
                else:
                    st.session_state.ts_controls_mitre_mapping['input'] = ts_controls_mitre_df.copy()

        with mitre_techniques_tab:
            st.markdown("""
            #### Upload Mitre Techniques Data
            Required columns for the Excel file:
            :blue-background[**mitre_technique_id, mitre_technique_name, lifecycle**]
            """)
            mitre_techniques_file = st.file_uploader("Mitre Techniques",
                                                     type="xlsx",
                                                     label_visibility="collapsed")

            if mitre_techniques_file is not None:
                mitre_techniques_df = pd.read_excel(mitre_techniques_file)
                st.info("File received")

                if 'mitre_technique' not in st.session_state:
                    st.session_state.mitre_technique = {"input": mitre_techniques_df}
                else:
                    st.session_state.mitre_technique['input'] = mitre_techniques_df.copy()

                if 'mitre_technique' in st.session_state:
                    st.session_state.mitre_technique_tab = 'mitre_technique_tab'

            st.markdown("""
            #### Upload Threat Scenario Controls Mitre Mapping Data
            Required columns for the Excel file:
            :blue-background[**ts_id, control_id, mitre_technique_id, control_weight_value**]
            """)
            ts_controls_mitre_file = st.file_uploader("Threat Scenario Controls Mitre Mapping",
                                                      type="xlsx",
                                                      label_visibility="collapsed",
                                                      key="button4")

            if ts_controls_mitre_file is not None:
                ts_controls_mitre_df = pd.read_excel(ts_controls_mitre_file)
                st.info("File received")

                if 'ts_controls_mitre_mapping' not in st.session_state:
                    st.session_state.ts_controls_mitre_mapping = {"input": ts_controls_mitre_df}
                else:
                    st.session_state.ts_controls_mitre_mapping['input'] = ts_controls_mitre_df.copy()

            st.markdown("""
            #### Upload Threat Scenario Mitre Mapping Data
            Required columns for the Excel file:
            :blue-background[**ts_id, mitre_technique_id, lifecycle, and_or, value**]
            """)
            ts_mitre_file = st.file_uploader("Threat Scenario Mitre Mapping",
                                             type="xlsx",
                                             label_visibility="collapsed")

            if ts_mitre_file is not None:
                ts_mitre_df = pd.read_excel(ts_mitre_file)
                st.info("File received")

                if 'ts_mitre_mapping' not in st.session_state:
                    st.session_state.ts_mitre_mapping = {"input": ts_mitre_df}
                else:
                    st.session_state.ts_mitre_mapping['input'] = ts_mitre_df.copy()

        with risks_tab:
            st.markdown("""
            #### Upload Risks Data
            Required columns for the Excel file: :blue-background[**risk_id, risk_name**]
            """)
            risks_file = st.file_uploader("Risks",
                                          type="xlsx",
                                          label_visibility="collapsed")

            if risks_file is not None:
                risks_df = pd.read_excel(risks_file)
                st.info("File received")

                if 'risk' not in st.session_state:
                    st.session_state.risk = {"input": risks_df}
                else:
                    st.session_state.risk['input'] = risks_df.copy()

                if 'risk' in st.session_state:
                    st.session_state.risk_tab = 'risk_tab'

            st.markdown("""
            #### Upload Threat Scenario Data
            Required columns for the Excel file:
            :blue-background[**risk_id, ts_id, ts_name, insider_flag, incident_data,
            future_threat_intensity_factor, median, stressed, stressed_percentile,
            potential_impact, flag**]
            """)
            threat_scenario_file = st.file_uploader("Threat Scenario",
                                                    type="xlsx",
                                                    label_visibility="collapsed")

            if threat_scenario_file is not None:
                threat_scenario_df = pd.read_excel(threat_scenario_file)
                st.info("File received")

                if 'ts' not in st.session_state:
                    st.session_state.ts = {"input": threat_scenario_df}
                else:
                    st.session_state.ts['input'] = threat_scenario_df.copy()

        with threat_scenarios_tab:
            st.markdown("""
            #### Upload Threat Scenario Data
            Required columns for the Excel file:
            :blue-background[**risk_id, ts_id, ts_name, insider_flag, incident_data,
            future_threat_intensity_factor, median, stressed, stressed_percentile,
            potential_impact, flag**]
            """)
            threat_scenario_file = st.file_uploader("Threat Scenario",
                                                    type="xlsx",
                                                    label_visibility="collapsed",
                                                    key="button5")

            if threat_scenario_file is not None:
                threat_scenario_df = pd.read_excel(threat_scenario_file)
                st.info("File received")

                if 'ts' not in st.session_state:
                    st.session_state.ts = {"input": threat_scenario_df}
                else:
                    st.session_state.ts['input'] = threat_scenario_df.copy()

                if 'ts' in st.session_state:
                    st.session_state.ts_tab = 'ts_tab'

            st.markdown("""
            #### Upload Risks Data
            Required columns for the Excel file: :blue-background[**risk_id, risk_name**]
            """)
            risks_file = st.file_uploader("Risks",
                                          type="xlsx",
                                          label_visibility="collapsed",
                                          key="button6")

            if risks_file is not None:
                risks_df = pd.read_excel(risks_file)
                st.info("File received")

                if 'risk' not in st.session_state:
                    st.session_state.risk = {"input": risks_df}
                else:
                    st.session_state.risk['input'] = risks_df.copy()

            st.markdown("""
            #### Upload Threat Scenario Controls Mapping Data
            Required columns for the Excel file:
            :blue-background[**ts_id, risk_id, control_id, weight**]
            """)
            ts_controls_file = st.file_uploader("Threat Scenario Controls Mapping",
                                                type="xlsx",
                                                label_visibility="collapsed",
                                                key="button7")

            if ts_controls_file is not None:
                ts_controls_df = pd.read_excel(ts_controls_file)
                st.info("File received")

                if 'ts_controls_mapping' not in st.session_state:
                    st.session_state.ts_controls_mapping = {"input": ts_controls_df}
                else:
                    st.session_state.ts_controls_mapping['input'] = ts_controls_df.copy()

            st.markdown("""
            #### Upload Threat Scenario Controls Mitre Mapping Data
            Required columns for the Excel file:
            :blue-background[**ts_id, control_id, mitre_technique_id, control_weight_value**]
            """)
            ts_controls_mitre_file = st.file_uploader("Threat Scenario Controls Mitre Mapping",
                                                      type="xlsx",
                                                      label_visibility="collapsed",
                                                      key="button8")

            if ts_controls_mitre_file is not None:
                ts_controls_mitre_df = pd.read_excel(ts_controls_mitre_file)
                st.info("File received")

                if 'ts_controls_mitre_mapping' not in st.session_state:
                    st.session_state.ts_controls_mitre_mapping = {"input": ts_controls_mitre_df}
                else:
                    st.session_state.ts_controls_mitre_mapping['input'] = ts_controls_mitre_df.copy()

            st.markdown("""
            #### Upload Threat Scenario Mitre Mapping Data
            Required columns for the Excel file:
            :blue-background[**ts_id, mitre_technique_id, lifecycle, and_or, value**]
            """)
            ts_mitre_file = st.file_uploader("Threat Scenario Mitre Mapping",
                                             type="xlsx",
                                             label_visibility="collapsed",
                                             key="button9")

            if ts_mitre_file is not None:
                ts_mitre_df = pd.read_excel(ts_mitre_file)
                st.info("File received")

                if 'ts_mitre_mapping' not in st.session_state:
                    st.session_state.ts_mitre_mapping = {"input": ts_mitre_df}
                else:
                    st.session_state.ts_mitre_mapping['input'] = ts_mitre_df.copy()

        st.divider()
        submit = st.button("SUBMIT")
        if submit:

            tabs = ["project_tab", "control_tab", "mitre_technique_tab", "risk_tab", "ts_tab"]

            if 'file_upload' not in st.session_state:
                st.session_state.file_upload = ''

            for tab in tabs:
                if tab in st.session_state:
                    files_to_upload = []

                    if tab == "control_tab":
                        if all(key in st.session_state for key in ['control', 'controls_project_mapping',
                                                                   'ts_controls_mapping',
                                                                   'ts_controls_mitre_mapping']):
                            if (
                                (set(st.session_state.control['input']['control_id'].unique()) ==
                                 set(st.session_state.controls_project_mapping['input']['control_id'].unique()) ==
                                 set(st.session_state.ts_controls_mapping['input']['control_id'].unique()) ==
                                 set(st.session_state.ts_controls_mitre_mapping['input']['control_id'].unique()))
                                and
                                (set(st.session_state.ts_controls_mapping['input']['ts_id'].unique()) ==
                                 set(st.session_state.ts_controls_mitre_mapping['input']['ts_id'].unique()))
                            ):
                                st.info("control_id and ts_id validated successfully")
                                st.success(f"Files ready for uploading in {tab}")
                                st.session_state.file_upload = 'success'
                                files_to_upload = ['control', 'controls_project_mapping', 'ts_controls_mapping',
                                                   'ts_controls_mitre_mapping']
                                break
                            else:
                                st.info("control_id's and ts_id's are different in uploaded files")
                        else:
                            st.write(f"Please upload all the required files in {tab}")

                    if tab == "project_tab":
                        if all(key in st.session_state for key in ['project', 'controls_project_mapping']):
                            if (
                                set(st.session_state.project['input']['project_id'].unique()) ==
                                set(st.session_state.controls_project_mapping['input']['project_id'].unique())
                            ):
                                st.info("project_id validated successfully")
                                st.success(f"Files ready for uploading in {tab}")
                                st.session_state.file_upload = 'success'
                                files_to_upload = ['project', 'controls_project_mapping']
                                break
                            else:
                                st.info("project_id's are different in uploaded files")
                        else:
                            st.write(f"Please upload all the required files in {tab}")

                    if tab == "mitre_technique_tab":
                        if all(key in st.session_state for key in ['mitre_technique', 'ts_controls_mitre_mapping',
                                                                   'ts_mitre_mapping']):
                            if (
                                (set(st.session_state.mitre_technique['input']['mitre_technique_id'].unique()) ==
                                 set(st.session_state.ts_controls_mitre_mapping['input']
                                     ['mitre_technique_id'].unique()) ==
                                 set(st.session_state.ts_mitre_mapping['input']['mitre_technique_id'].unique()))
                                and
                                (set(st.session_state.ts_controls_mitre_mapping['input']['ts_id'].unique()) ==
                                 set(st.session_state.ts_mitre_mapping['input']['ts_id'].unique()))
                            ):
                                st.info("mitre_technique_id and ts_id validated successfully")
                                st.success(f"Files ready for uploading in {tab}")
                                st.session_state.file_upload = 'success'
                                files_to_upload = ['mitre_technique', 'ts_controls_mitre_mapping', 'ts_mitre_mapping']
                                break
                            else:
                                st.info("mitre_technique_id's and ts_id's are different in uploaded files")
                        else:
                            st.write(f"Please upload all the required files in {tab}")

                    if tab == "risk_tab":
                        if all(key in st.session_state for key in ['risk', 'ts']):
                            if (
                                (set(st.session_state.risk['input']['risk_id'].unique()) ==
                                 set(st.session_state.ts['input']['risk_id'].unique()))
                            ):
                                st.info("risk_id validated successfully")
                                st.success(f"Files ready for uploading in {tab}")
                                st.session_state.file_upload = 'success'
                                files_to_upload = ['risk', 'ts']
                                break
                            else:
                                st.info("risk_id's are different in uploaded files")
                        else:
                            st.write(f"Please upload all the required files in {tab}")

                    if tab == "ts_tab":
                        if all(key in st.session_state for key in ['ts', 'risk', 'ts_controls_mapping',
                                                                   'ts_controls_mitre_mapping', 'ts_mitre_mapping']):
                            if (
                                (set(st.session_state.ts['input']['ts_id'].unique()) ==
                                 set(st.session_state.ts_controls_mapping['input']['ts_id'].unique()) ==
                                 set(st.session_state.ts_controls_mitre_mapping['input']['ts_id'].unique()) ==
                                 set(st.session_state.ts_mitre_mapping['input']['ts_id'].unique()))
                                and
                                (set(st.session_state.ts['input']['risk_id'].unique()) ==
                                 set(st.session_state.risk['input']['risk_id'].unique()) ==
                                 set(st.session_state.ts_controls_mapping['input']['risk_id'].unique()))
                                and
                                (set(st.session_state.ts_controls_mapping['input']['control_id'].unique()) ==
                                 set(st.session_state.ts_controls_mitre_mapping['input']['control_id'].unique()))
                            ):
                                st.info("ts_id, risk_id and control_id validated successfully")
                                st.success(f"Files ready for uploading in {tab}")
                                st.session_state.file_upload = 'success'
                                files_to_upload = ['ts', 'risk', 'ts_controls_mapping', 'ts_controls_mitre_mapping',
                                                   'ts_mitre_mapping']
                                break
                            else:
                                st.info("ts_id's, risk_id's and control_id's are different in uploaded files")
                        else:
                            st.write(f"Please upload all the required files in {tab}")

            if st.session_state.file_upload == 'success':

                upload_new_data_input = {}
                tables = query_params_dict["base_tables"] | query_params_dict["mapping_tables"]

                # Iterate through the list and write the shape if present in session state
                for df_name, table_path in tables.items():
                    # if df_name in st.session_state:
                    if df_name in files_to_upload:
                        upload_new_data_input[df_name] = {
                            "table_path": table_path,
                            "uploaded_new_data": st.session_state[df_name]['input'].to_dict()
                        }

                st.write("Uploading files...")
                request_response = request(
                    f"{cloud_run_back_end}/upload_new_data",
                    upload_new_data_input
                )

                if not request_response.status_code == 200:
                    st.error(request_response.status_code, request_response.reason)
                else:
                    request_status = json.loads(request_response.text)['status']
                    if request_status == "Success":
                        st.info(f"{request_status}: New data loaded successfully")
                    else:
                        request_message = json.loads(request_response.text)['message']
                        st.warning(f"{request_status}: {request_message}")
