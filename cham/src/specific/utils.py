import pandas as pd
import streamlit as st


def charm_model_input_parameters(charm_model_input_dict, query_params_dict, local_flag, google_project, historical=None):
    st.subheader("Parameters")
    parameter_cols_position = st.columns(len(charm_model_input_dict))
    for i, (key, value) in enumerate(charm_model_input_dict.items()):
        with parameter_cols_position[i]:
            st.write(key.split("_")[0].title())
            edited_df = st.data_editor(
                data=pd.DataFrame([value]).rename(index={0: key}).T,
                hide_index=False,
                key=f"{key}_{str(historical)}"
            )
            charm_model_input_dict[key] = edited_df.T.to_dict(orient='records')[0]

    st.subheader("Data")
    data_cols_position = st.columns(len(query_params_dict))
    for i, query_name in enumerate(query_params_dict.keys()):
        df = st.session_state[query_name].copy()
        if historical:
            df = df[df[f'{query_name}_id'].isin(historical[f'{query_name}_id'])]

        df.insert(0, 'Select', True)
        with data_cols_position[i]:
            st.write(query_name.replace("_", " ").title())
            edited_df = st.data_editor(
                data=df[['Select', f'{query_name}_id', f'{query_name}_name']],
                disabled=df.columns[1:],
                hide_index=True,
                key=f"{query_name}_{str(historical)}"
            )

            Included_values = list(edited_df[edited_df["Select"] == True][f'{query_name}_id'])
            charm_model_input_dict[f'{query_name}_id'] = Included_values

    return charm_model_input_dict
