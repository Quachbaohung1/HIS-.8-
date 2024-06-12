import requests
import pandas as pd
from copy import deepcopy
from Cấu_hình.Setup import base_url_2, auth_token_2, base_url_5, auth_token_5
from Tiếp_nhận.POST import copy_sheet_values


# Lấy thông tin tất cả các bệnh nhân
def create_information_patient():
    from Khám_bệnh_Toa_thuốc.GET import check_patient_in_room
    patient_ids = check_patient_in_room()
    url = f"{base_url_2}/Patients/PatientIds"
    headers = {"Authorization": auth_token_2}
    data = patient_ids
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()


# Chọn bệnh nhân
def choose_patient(entry_id):
    from Khám_bệnh_Toa_thuốc.GET import check_visit_enty
    visit_ids = check_visit_enty(entry_id)
    visit_idas = []
    for visit_id in visit_ids:
        url = f"{base_url_2}/VisitEntries/VisitIds"
        headers = {"Authorization": auth_token_2}
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
    url = f"{base_url_5}/InvNowAvailables/GetInventoriesForBooking/?isInsurrance=False&name=&medAI=&fullName=&LengthLimit=20&fullNameOrCode=False&attribute=&isNoLoadItems=False"
    headers = {"Authorization": auth_token_5}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result_api = response.status_code
        return result_api
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"\nAn error occurred during patient creation: {e}")


# Data thuốc
def data_medicine(row):
    # Tạo danh sách để lưu trữ thông tin về mỗi loại thuốc
    medicines = []

    def handle_null(value, default=None, to_type=int):
        if pd.isna(value):
            return default
        if value is None:
            return default
        return to_type(value)

    # Xác định các giá trị từ cột tương ứng cho mỗi loại thuốc
    store_ids = handle_null(row['StoreIds'], default=0, to_type=int)
    inv_sources = handle_null(row['InvSources'], default=None, to_type=int)
    lot_ids = handle_null(row['LotIds'], default=None, to_type=int)
    item_ids = handle_null(row['ItemIds'], default=0, to_type=int)
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
            store_ids
        ],
        "InvSources": None,
        "LotIds": None,
        "ItemIds": [
            item_ids
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
    return medicine_data


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


# Kiểm tra bệnh nhân có trong phòng khám
def process_check_patient_in_room():
    from Khám_bệnh_Toa_thuốc.GET import get_all_info
    # Thông tin
    entry_ids = [38392]
    for entry_id in entry_ids:
        all_info = get_all_info(entry_id)
        print("all_info:", all_info)
        if len(all_info) == 0:
            print("No information about patients.")
            return []
        return all_info


def process_insert_info_patient(file_path):
    from Khám_bệnh_Toa_thuốc.GET import get_all_info
    from Khám_bệnh_Toa_thuốc.PUT import prepare_information_data, update_information_patient
    sheet_name = "Data"

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Thông tin
    entry_ids = [38392]

    if len(entry_ids) != len(excel_data):
        raise ValueError("Số lượng entry_ids và số lượng hàng trong additional_data phải bằng nhau.")

    # Sử dụng một vòng lặp để xử lý từng hàng với từng entry_id tương ứng
    for entry_id, (index, row) in zip(entry_ids, excel_data.iterrows()):
        # Lấy tất cả thông tin bệnh nhân
        all_info = get_all_info(entry_id)
        print("all_info:", all_info)
        if len(all_info) == 0:
            print("No information about patients.")
            return []

        for info in all_info:
            # Chuẩn bị thông tin bệnh nhân và lấy entryId
            information_data, information_data["entryId"] = prepare_information_data(row, info)

            # Cập nhật thông tin bệnh nhân
            result_api = update_information_patient(all_info, information_data)
            return result_api


def process_info_prescription_services(file_path):
    from Khám_bệnh_Toa_thuốc.GET import get_all_info
    from Khám_bệnh_Toa_thuốc.PUT import prepare_information_data, update_information_patient
    sheet_name = "Data"
    check_sheet_name = "Check"
    columns_to_copy = ["ItemIds", "StoreIds", "Qty", "UseDays", "DoseNO", "DoseAN", "TxtDoseNO", "TxtDoseAN", "UseWeekDay"]

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Gọi hàm copy_sheet_values để sao chép các cột cần thiết sang sheet Verify
    copy_sheet_values(file_path, sheet_name, check_sheet_name, columns_to_copy)

    # Thông tin
    entry_ids = [38392]

    if len(entry_ids) != len(excel_data):
        raise ValueError("Số lượng entry_ids và số lượng hàng trong additional_data phải bằng nhau.")

    verify_data = pd.read_excel(file_path, sheet_name=check_sheet_name)

    # Sử dụng một vòng lặp để xử lý từng hàng với từng entry_id tương ứng
    for entry_id, (index, row) in zip(entry_ids, excel_data.iterrows()):
        # Lấy tất cả thông tin bệnh nhân
        all_info = get_all_info(entry_id)
        print("all_info:", all_info)
        if len(all_info) == 0:
            print("No information about patients.")
            return []

        for info in all_info:
            verify_row = verify_data.iloc[index]
            # Chuẩn bị thông tin bệnh nhân và lấy entryId
            information_data, information_data["entryId"] = prepare_information_data(row, info)

            # Cập nhật thông tin bệnh nhân
            update_information_patient(all_info, information_data)

            # Chuẩn bị thông tin chỉ định thuốc
            medicine_data = data_medicine(row)

            # Chỉ định thuốc
            result_api = choose_medicine(medicine_data, verify_row)
            return result_api


def process_prescription_services(file_path):
    from Khám_bệnh_Toa_thuốc.GET import get_all_info
    from Khám_bệnh_Toa_thuốc.PUT import prepare_information_data, prepare_medicine_data, update_information_patient, update_medicine_patient
    sheet_name = "Data"
    check_sheet_name = "Check"
    columns_to_copy = ["ItemIds", "StoreIds", "Qty", "UseDays", "DoseNO", "DoseAN", "TxtDoseNO", "TxtDoseAN",
                       "UseWeekDay"]

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Gọi hàm copy_sheet_values để sao chép các cột cần thiết sang sheet Verify
    copy_sheet_values(file_path, sheet_name, check_sheet_name, columns_to_copy)

    # Thông tin
    entry_ids = [38392]

    if len(entry_ids) != len(excel_data):
        raise ValueError("Số lượng entry_ids và số lượng hàng trong additional_data phải bằng nhau.")

    verify_data = pd.read_excel(file_path, sheet_name=check_sheet_name)

    # Sử dụng một vòng lặp để xử lý từng hàng với từng entry_id tương ứng
    for entry_id, (index, row) in zip(entry_ids, excel_data.iterrows()):
        # Lấy tất cả thông tin bệnh nhân
        all_info = get_all_info(entry_id)
        print("all_info:", all_info)
        if len(all_info) == 0:
            print("No information about patients.")
            return []

        for info in all_info:
            verify_row = verify_data.iloc[index]
            # Chuẩn bị thông tin bệnh nhân và lấy entryId
            information_data, information_data["entryId"] = prepare_information_data(row, info)

            # Cập nhật thông tin bệnh nhân
            update_information_patient(all_info, information_data)

            # Chuẩn bị thông tin chỉ định thuốc
            medicine_data = data_medicine(row)

            # Chỉ định thuốc
            choose_medicine(medicine_data)

            # Chuẩn bị thông tin bệnh nhân và lấy entryId
            medicine_data, medicine_data["entryId"] = prepare_medicine_data(row, info)

            # Cập nhật thông tin bệnh nhân
            result_api = update_medicine_patient(all_info, medicine_data, verify_row)
            return result_api
