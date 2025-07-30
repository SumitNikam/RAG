import json
import requests
import google.oauth2.id_token
import google.auth.transport.requests
import numpy as np


def request(url, data):
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, url)
    data = {k: int(v) if isinstance(v, np.integer) else v for k, v in data.items()}
    response = requests.post(
        url,
        data=json.dumps(data).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {id_token}"
        }
    )
    return response
