import requests
import pandas as pd
from copy import deepcopy

# Base url
base_url = "http://115.79.31.186:1096"

# Auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjM4MzkiLCJyb2xlIjoiQWRtaW4iLCJBY2NvdW50TmFtZSI6Imh1bmdxYiIsIkNsaWVudElwQWRkcmVzcyI6Ijo6MSIsIklzTG9jYWxJcCI6IlRydWUiLCJuYmYiOjE3MTUxODQ2NDIsImV4cCI6MTcxNTE4ODI0MiwiaWF0IjoxNzE1MTg0NjQyfQ.CihuC246iqFUos4MNZtNWs2q_SBOtmbXz4NRNuRQ4rg"


# Lấy thông tin tất cả các bệnh nhân
def create_information_patient():
    from Khám_bệnh_CDDV.GET import check_patient_in_room
    patient_ids = check_patient_in_room()
    url = f"{base_url}/pms/Patients/PatientIds"
    headers = {"Authorization": auth_token}
    data = patient_ids
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()


# Chọn bệnh nhân
def choose_patient():
    from Khám_bệnh_Toa_thuốc.GET import check_visit_enty
    visit_ids = check_visit_enty()
    visit_idas = []
    for visit_id in visit_ids:
        url = f"{base_url}/pms/VisitEntries/VisitIds"
        headers = {"Authorization": auth_token}
        data = [visit_id]
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        # Lặp qua danh sách các đối tượng JSON trong response.json()
        for item in response.json():
            visit_ida = item["visitId"]  # Trích xuất visitId từ mỗi đối tượng
            visit_idas.append(visit_ida)
    print("visit_idas", visit_idas)
    return visit_idas


# Chọn thuốc
def choose_medicine(data):
    url = f"{base_url}/ims/InvNowAvailables/GetInventoriesForBooking/?isInsurrance=False&name=&medAI=&fullName=&LengthLimit=20&fullNameOrCode=False&attribute=&isNoLoadItems=False"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    return response_json


# Data thuốc
def data_medicine(row):
    # Tạo danh sách để lưu trữ thông tin về mỗi loại thuốc
    medicines = []

    # for _, row in row.iterrows():
    def handle_null(value, default=None, to_type=int):
        return to_type(value) if not pd.isna(value) else default

    # Xác định các giá trị từ cột tương ứng cho mỗi loại thuốc
    store_ids = handle_null(row['StoreIds'])
    inv_sources = handle_null(row['InvSources'], default=None, to_type=int)
    lot_ids = handle_null(row['LotIds'], default=None, to_type=int)
    item_ids = handle_null(row['ItemIds'])
    ignore_item_ids = handle_null(row['IgnoreItemIds'], default=None, to_type=int)
    vou_status = handle_null(row['VouStatus'], default=None, to_type=int)
    ignore_store_id = False if str(row['IgnoreStoreId']).lower() == 'false' else True
    ignore_lot_id = False if str(row['IgnoreLotId']).lower() == 'false' else True
    ignore_inv_source = False if str(row['IgnoreInvSource']).lower() == 'false' else True
    item_cat_ids = handle_null(row['ItemCatIds'], default=None, to_type=int)
    item_types = handle_null(row['ItemTypes'], default=None, to_type=int)
    bid_ids = handle_null(row['BidIds'], default=None, to_type=int)
    provider_ids = handle_null(row['ProviderIds'], default=None, to_type=int)
    ignore_item_cat_ids = handle_null(row['IgnoreItemCatIds'], default=None, to_type=int)
    take_only_group_in_store_hospital = handle_null(row['TakeOnlyGroupInStoreHospital'], default=None, to_type=int)
    take_only_item_ins = handle_null(row['TakeOnlyItemIns'], default=None, to_type=int)

    # medicine_data = {
    #     "StoreIds": [
    #         store_ids
    #     ],
    #     "InvSources": inv_sources,
    #     "LotIds": lot_ids,
    #     "ItemIds": [
    #         item_ids
    #     ],
    #     "IgnoreItemIds": ignore_item_ids,
    #     "VouStatus": vou_status,
    #     "IgnoreStoreId": ignore_store_id,
    #     "IgnoreLotId": ignore_lot_id,
    #     "IgnoreInvSource": ignore_inv_source,
    #     "ItemCatIds": item_cat_ids,
    #     "ItemTypes": item_types,
    #     "BidIds": bid_ids,
    #     "ProviderIds": provider_ids,
    #     "IgnoreItemCatIds": ignore_item_cat_ids,
    #     "TakeOnlyGroupInStoreHospital": take_only_group_in_store_hospital,
    #     "TakeOnlyItemIns": take_only_item_ins
    # }
    medicine_data = {
        "StoreIds": [
            36
        ],
        "InvSources": None,
        "LotIds": None,
        "ItemIds": [
            4
        ],
        "IgnoreItemIds": None,
        "VouStatus": None,
        "IgnoreStoreId": ignore_store_id,
        "IgnoreLotId": ignore_lot_id,
        "IgnoreInvSource": ignore_inv_source,
        "ItemCatIds": None,
        "ItemTypes": None,
        "BidIds": None,
        "ProviderIds": None,
        "IgnoreItemCatIds": None,
        "TakeOnlyGroupInStoreHospital": None,
        "TakeOnlyItemIns": None
    }

    # Chọn loại thuốc từ thông tin được cung cấp
    medicine = choose_medicine(medicine_data)
    medicines.append(medicine)
    return medicines


def generate_additional_data(original_data, num_records):
    new_data = []

    for _ in range(num_records):
        for i in range(0, len(original_data), 2):
            if i + 1 < len(original_data):
                new_row1 = deepcopy(original_data.iloc[i])
                new_row2 = deepcopy(original_data.iloc[i + 1])
                new_data.append(new_row1)
                new_data.append(new_row2)
    return pd.DataFrame(new_data)


def write_data_to_excel(file_path, sheet_name, data):
    # Ghi dữ liệu vào tệp Excel và ghi đè lên dữ liệu hiện có
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        data.to_excel(writer, sheet_name=sheet_name, index=False)


# Call
def process_kb_ketoa():
    from Khám_bệnh_Toa_thuốc.PUT import update_medicine_patient_from_excel
    # from Khám_bệnh.GET import get_information_patient
    file_path = "D://HIS api automation/DataTest/Data_API_Thuốc.xlsx"
    sheet_name = "Sheet1"

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # # Tạo dữ liệu bổ sung và ghi vào file Excel
    # num_records_to_add = 2  # Số dòng dữ liệu bổ sung
    # additional_data = generate_additional_data(excel_data.tail(1), num_records_to_add)
    # write_data_to_excel(file_path, sheet_name, additional_data)
    #
    # # Đọc lại dữ liệu đã ghi vào file
    # additional_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Thông tin cần thiết cho get_information_patient
    # for i in range(0, len(excel_data), 2):
    #     if i + 1 < len(excel_data):
    #         rows = excel_data.iloc[i:i + 2]
    for index, row in excel_data.iterrows():
        update_medicine_patient_from_excel(row)


process_kb_ketoa()
