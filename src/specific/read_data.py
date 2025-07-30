from google.cloud import storage
import pandas as pd
import io


# Function to generate the schema details
def read_data_gcs(
    bucket_name,
    file
):
    # Initialize a client
    client = storage.Client()

    # Get the bucket
    bucket = client.bucket('sumitbucket95')

    # Get the blob (file) from the bucket
    blob = bucket.blob('data/cltv.csv')

    # Download the blob as a string
    data = blob.download_as_string()

    # Read the CSV data into a pandas DataFrame
    df = pd.read_csv(io.StringIO(data.decode('utf-8')))

    return df
