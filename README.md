1. Tải Fiddler (https://www.telerik.com/download/fiddler)
2. Tải Postman (https://www.postman.com/downloads/)
3. Thao tác trên ứng dung để lấy được API chính của chức năng cần viết và auth_token
4. Mẫu đoạn code API trên python:

import requests
import json


base_url = "..."

auth_token = "..."

def create_information_patient():
    url = f"{base_url}/pms/Patients/PatientIds"
    headers = {"Authorization": auth_token}
    data = {
                "PatientId": 123,
                "RefNo": 123,
                "OnDate": 123,
                "LabReqById": 123,
                "LabReqNotes": 23,
                "DxICD": 23,
                "DxText": 123,
                "Attribute": 123,
                "FrVisitEntryId": 23,
                "CreateOn": 23,
                "CreateById": 23,
                "Status": 23
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data
