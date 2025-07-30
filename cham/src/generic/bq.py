import google
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from typing import Any
import streamlit as st


@st.cache_data
def read_bq_cache(
    query: str,
    google_project: str
) -> Any:
    """
    Description:
    -----------
    Executes the query on BQ and returns the query output
    Parameters:
    -----------
    query : String
        Pass the BQ query
    table : String
        Pass full BQ table path i.e. 'project_name.dataset_name.table_name'
    google_project : String
        Pass the google_project. Default set to None which will pick current project
    Returns:
    -----------
    result : DataFrame
        Return query output in the form of a DataFrame or None if any error
    Examples:
    -----------
    df = bq_read(query=read_query, table=full_table_path)
    df = bq_read(query=read_query, table=full_table_path, google_project='vf-ca-inf-live')
    """
    # BQ client set up
    if google_project is not None:
        project_id = google_project
    else:
        _, project_id = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

    bqclient = bigquery.Client(project=project_id)

    try:
        result = bqclient.query(query).result().to_dataframe()
        return result
    except NotFound:
        print("Table is not found.")
        return None
    except Exception as e:
        print("Unexpected error:", e)
        return None


def read_bq(
    query: str,
    google_project: str
) -> Any:
    """
    Description:
    -----------
    Executes the query on BQ and returns the query output
    Parameters:
    -----------
    query : String
        Pass the BQ query
    table : String
        Pass full BQ table path i.e. 'project_name.dataset_name.table_name'
    google_project : String
        Pass the google_project. Default set to None which will pick current project
    Returns:
    -----------
    result : DataFrame
        Return query output in the form of a DataFrame or None if any error
    Examples:
    -----------
    df = bq_read(query=read_query, table=full_table_path)
    df = bq_read(query=read_query, table=full_table_path, google_project='vf-ca-inf-live')
    """
    # BQ client set up
    if google_project is not None:
        project_id = google_project
    else:
        _, project_id = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

    bqclient = bigquery.Client(project=project_id)

    try:
        result = bqclient.query(query).result().to_dataframe()
        return result
    except NotFound:
        print("Table is not found.")
        return None
    except Exception as e:
        print("Unexpected error:", e)
        return None
