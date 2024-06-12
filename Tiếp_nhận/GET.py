import requests
import json
from Cấu_hình.Setup import base_url_3, auth_token_3

# Base url
base_url = base_url_3


# Auth token
auth_token = auth_token_3


# GET request
def CurrentServerDateTime():
    url = base_url + "/Masters/CurrentServerDateTime"
    headers = {
        "Authorization": auth_token
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    return json_str
