import requests
import pandas as pd
from copy import deepcopy

# Base url
base_url = "http://115.79.31.186:1096"

# Auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjM4MzkiLCJyb2xlIjoiQWRtaW4iLCJBY2NvdW50TmFtZSI6Imh1bmdxYiIsIkNsaWVudElwQWRkcmVzcyI6Ijo6MSIsIklzTG9jYWxJcCI6IlRydWUiLCJuYmYiOjE3MTUxODQ2NDIsImV4cCI6MTcxNTE4ODI0MiwiaWF0IjoxNzE1MTg0NjQyfQ.CihuC246iqFUos4MNZtNWs2q_SBOtmbXz4NRNuRQ4rg"


# Tạo thông tin dịch vụ
def create_patient_service():
    from Cận_lâm_sàng.GET import get_info_patient
    labEx_ids_and_patient_ids = get_info_patient()
    labEx_ids = [item["labExId"] for item in labEx_ids_and_patient_ids]

    # Kiểm tra xem danh sách labEx_ids có phần tử không
    if not labEx_ids:
        print("No labExId available.")
        return []

    # Tạo URL và headers cho request POST
    url = f"{base_url}/cis/LabExamItems/LabExamIds?ExcludedAttribute=&serviceTypeL0=&isLoadDelete=False"
    headers = {"Authorization": auth_token}

    # Tạo data từ danh sách labEx_ids
    data = labEx_ids

    try:
        # Thực hiện request POST
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        # Xử lý response data
        response_data = response.json()
        exItem_ids = []

        if isinstance(response_data, list):
            for item in response_data:
                exItem_id = item.get("exItemId")
                if exItem_id is not None:
                    exItem_ids.append(exItem_id)
                    print(exItem_id)
        elif isinstance(response_data, dict):
            exItem_id = response_data.get("exItemId")
            if exItem_id is not None:
                exItem_ids.append(exItem_id)
                print(exItem_id)
        else:
            print("Invalid response format")

        print("exItem_ids:", exItem_ids)
        return exItem_ids

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []


# Tạo bill
def create_bill():
    exItem_ids = create_patient_service()
    url = f"{base_url}/finance/BillLabExams/ExItemIds"
    headers = {"Authorization": auth_token}
    data = exItem_ids
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()


def create_information_patient():
    from Cận_lâm_sàng.GET import get_info_patient
    labEx_ids_and_patient_ids = get_info_patient()
    patient_ids = [item["patientId"] for item in labEx_ids_and_patient_ids]

    # Kiểm tra xem danh sách patient_ids có phần tử không
    if not patient_ids:
        print("No patientId available.")
        return []

    # Tạo URL và headers cho request POST
    url = f"{base_url}/pms/Patients/PatientIds"
    headers = {"Authorization": auth_token}
    # Tạo data từ danh sách labEx_ids
    data = patient_ids
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    # Xử lý response data
    response_data = response.json()
    return response_data


def create_visitIds(entry_ids):
    from Cận_lâm_sàng.GET import get_information_patient
    EntryIds = get_information_patient(entry_ids)
    url = f"{base_url}/cis/TxVisits/EntryIds"
    headers = {"Authorization": auth_token}
    # Tạo data từ danh sách labEx_ids
    data = EntryIds
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    # Xử lý response data
    response_data = response.json()
    print("response_data:", response_data)
    # Trích xuất txVisitId từ response_data nếu có
    txVisitIds = []
    for item in response_data:
        if "txVisitId" in item:
            txVisitIds.append(item["txVisitId"])

    return txVisitIds


def create_loadTxVisitIds(entry_ids):
    txVisitIds = create_visitIds(entry_ids)
    url = f"{base_url}/cis/TxVisitDX/LoadTxVisitIds"
    headers = {"Authorization": auth_token}
    # Tạo data từ danh sách labEx_ids
    data = txVisitIds
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    # Xử lý response data
    response_data = response.json()
    print("response_data:", response_data)
    return response_data


def generate_additional_data(original_data, num_records):
    new_data = []

    for _ in range(num_records):
        for _, row in original_data.iterrows():
            new_row = deepcopy(row)

            new_data.append(new_row)

    return pd.DataFrame(new_data)


def write_data_to_excel(file_path, sheet_name, data):
    # Ghi dữ liệu vào tệp Excel và ghi đè lên dữ liệu hiện có
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        data.to_excel(writer, sheet_name=sheet_name, index=False)


def process_CLS():
    from Cận_lâm_sàng.PUT import update_CLS_patient_from_excel
    file_path = "D://HIS api automation/DataTest/Data_API_CLS.xlsx"
    sheet_name = "Sheet1"

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Tạo dữ liệu bổ sung và ghi vào file Excel
    num_records_to_add = 2  # Số dòng dữ liệu bổ sung
    additional_data = generate_additional_data(excel_data.tail(1), num_records_to_add)
    write_data_to_excel(file_path, sheet_name, additional_data)

    # Đọc lại dữ liệu đã ghi vào file
    additional_data = pd.read_excel(file_path, sheet_name=sheet_name)
    # Thông tin
    for _ in range(num_records_to_add):
        for index, row in additional_data.iterrows():
            update_CLS_patient_from_excel(row)
