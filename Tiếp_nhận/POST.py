import math
import requests
import pandas as pd
import datetime
import re
from copy import deepcopy
from Tiếp_nhận import GET
from Cấu_hình.Setup import base_url_2, auth_token_2

# Base url
base_url = base_url_2


# Auth token
auth_token = auth_token_2


# POST request
def create_patient(data, verify_data):
    url = f"{base_url}/Patients"
    headers = {"Authorization": auth_token}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        patient_id = response_data.get("patientId")
        result = compare_data(response_data, verify_data)
        return patient_id, result
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"\nAn error occurred during patient creation: {e}")


def create_insurance(data, dob, verify_data):
    url = f"{base_url}/PatientInsurances/?dateOfBirth={dob}"
    headers = {"Authorization": auth_token}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        patient_id = response_data.get("patientId")
        result = compare_data(response_data, verify_data)
        return response_data, patient_id, result
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"\nAn error occurred during insurance creation: {e}")


def create_visit(data, visit_on, verify_data):
    url = f"{base_url}/Visits/?visitOn={visit_on}&noSetProcessingPending=False&isPassCreatePaymentTicket=False&isPassVisitOnSameDay=False"
    headers = {"Authorization": auth_token}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        result = compare_data(response_data, verify_data)
        # Kiểm tra và trích xuất entryId từ phản hồi JSON
        entry_id = None
        if response_data and "entry" in response_data and "entryId" in response_data["entry"]:
            entry_id = response_data["entry"]["entryId"]

        # Return các giá trị
        return response_data, entry_id, result
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"\nAn error occurred during insurance creation: {e}")


def create_patient_from_excel(row):
    full_name = None if pd.isna(row['LastName']) or pd.isna(row['FirstName']) else str(row['LastName']) + " " + str(row['FirstName'])
    IdCardNo = "0" + str(int(row['IdCardNo']))
    MobileNo = "0" + str(int(row['MobileNo']))
    RelativePhone = "0" + str(int(row['RelativePhone']))
    if pd.isna(row['FirstName']):
        FirstName = None  # hoặc tax_code = 'null' nếu bạn muốn lưu giá trị 'null' (dạng chuỗi)
    else:
        FirstName = str(int(row['FirstName']))

    if pd.isna(row['LastName']):
        LastName = None  # hoặc tax_code = 'null' nếu bạn muốn lưu giá trị 'null' (dạng chuỗi)
    else:
        LastName = row['LastName']
    # Kiểm tra nếu giá trị của cột TaxCode là NaN
    if pd.isna(row['TaxCode']):
        tax_code = None  # hoặc tax_code = 'null' nếu bạn muốn lưu giá trị 'null' (dạng chuỗi)
    else:
        tax_code = str(row['TaxCode'])

    if pd.isna(row['FullAddress']):
        FullAddress = None  # hoặc tax_code = 'null' nếu bạn muốn lưu giá trị 'null' (dạng chuỗi)
    else:
        FullAddress = str(row['FullAddress'])

    if pd.isna(row['Address']):
        Address = None  # hoặc tax_code = 'null' nếu bạn muốn lưu giá trị 'null' (dạng chuỗi)
    else:
        Address = str(row['Address'])

    Ethnic = "0" + str(int(row['Ethnic']))
    if pd.isna(row['Dob']):
        Dob = None  # hoặc tax_code = 'null' nếu bạn muốn lưu giá trị 'null' (dạng chuỗi)
    else:
        Dob = str(row['Dob'])
    patient_data = {
        "PatientCode": "SimulatedCode",
        "FullPatientCode": "SimulatedCode",
        "FirstName": FirstName,
        "LastName": LastName,
        "Dob": Dob,
        "Gender": int(row['Gender']),
        "IdCardNo": IdCardNo,
        "MobileNo": MobileNo,
        "Nationality": str(row['Nationality']),
        "Ethnic": Ethnic,
        "Country": str(row['Country']),
        "City": str(int(row['City'])),
        "District": str(int(row['District'])),
        "Ward": str(int(row['Ward'])),
        "Address": Address,
        "Occupation": row['Occupation'],
        "EmployerName": str(row['EmployerName']),
        "EmployerAddr": str(row['EmployerAddr']),
        "TaxCode": tax_code,
        "RelativeName": str(row['RelativeName']),
        "RelativeAddr": str(row['RelativeAddr']),
        "RelativePhone": RelativePhone,
        "RelativeType": row['RelativeType'],
        "Status": row['Status'],
        "FullName": full_name,
        "FullAddress": FullAddress
    }
    return patient_data


def create_insurance_from_excel(row, patient_id):
    if pd.isna(row['InsZone']):
        InsZone = None  # hoặc tax_code = 'null' nếu bạn muốn lưu giá trị 'null' (dạng chuỗi)
    else:
        InsZone = int(row['InsZone'])
    if pd.isna(row['MedProviderId']):
        MedProviderId = None  # hoặc tax_code = 'null' nếu bạn muốn lưu giá trị 'null' (dạng chuỗi)
    else:
        MedProviderId = int(row['MedProviderId'])
    if pd.isna(row['Provider']):
        provider = None  # hoặc tax_code = 'null' nếu bạn muốn lưu giá trị 'null' (dạng chuỗi)
    else:
        provider = str(row['Provider'])
    if pd.isna(row['FullInsOn']):
        FullInsOn = None  # hoặc tax_code = 'null' nếu bạn muốn lưu giá trị 'null' (dạng chuỗi)
    else:
        FullInsOn = str(row['FullInsOn'])

    if pd.isna(row['StartDate']):
        StartDate = None  # hoặc tax_code = 'null' nếu bạn muốn lưu giá trị 'null' (dạng chuỗi)
    else:
        StartDate = str(row['StartDate'])

    if pd.isna(row['EndDate']):
        EndDate = None  # hoặc tax_code = 'null' nếu bạn muốn lưu giá trị 'null' (dạng chuỗi)
    else:
        EndDate = str(row['EndDate'])

    dob_value = row["Dob"]
    # Check if dob_value is NaN
    if isinstance(dob_value, float) and math.isnan(dob_value):
        dob_datetime = None
    else:
        # Convert the value to a string
        dob_str = str(dob_value)

        # Parse the string to datetime object
        dob_datetime = datetime.datetime.strptime(dob_str, "%Y-%m-%dT%H:%M:%S%z")
    if dob_datetime is not None:
        dob = dob_datetime.strftime("%Y%m%d")
    else:
        dob = None
    insurance_data = {
        "PatientId": patient_id,
        "InsCardNo": str(row['InsCardNo']),
        "InsName": str(row['InsName']),
        "StartDate": StartDate,
        "EndDate": EndDate,
        "MedProviderId": MedProviderId,
        "Address": str(row['Address']),
        "Country": str(row['Country']),
        "City": str(int(row['City'])),
        "District": str(int(row['District'])),
        "Ward": str(int(row['Ward'])),
        "InsZone": InsZone,
        "Status": row['Status'],
        "Attribute": int(row['Attribute']),
        "Provider": provider,
        "IsDisabled": str(row['IsDisabled']),
        "IsTemp": str(row['IsTemp']),
        "FullInsOn": FullInsOn
    }
    return insurance_data, dob


def create_visit_from_excel(row, patient_id):
    full_name = None if pd.isna(row['LastName']) or pd.isna(row['FirstName']) else row['LastName'] + " " + str(int(row['FirstName']))
    Ethnic = "0" + str(int(row['Ethnic']))

    visit_on = str(GET.CurrentServerDateTime())
    visit_on_value_trimmed1 = visit_on.replace('"', '')
    visit_on_value_trimmed = visit_on[:20] + "+" + visit_on[-6:]
    isit_on_value_trimmed = visit_on_value_trimmed.replace('"', '')

    visit_on_datetime = datetime.datetime.strptime(isit_on_value_trimmed, "%Y-%m-%dT%H:%M:%S%z")
    Formated_visit_on = visit_on_datetime.strftime("%Y%m%d%H%M%S")
    if pd.isna(row['InsCheckedStatus']):
        InsCheckedStatus = None
    else:
        InsCheckedStatus = int(row['InsCheckedStatus'])
    if pd.isna(row['WardUnitId']):
        WardUnitId = None
    else:
        WardUnitId = int(row['WardUnitId'])
    if pd.isna(row['MedServiceId']):
        MedServiceId = None
    else:
        MedServiceId = int(row['MedServiceId'])
    visit_on = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    visit_data = {
        "ReceiveType": int(row['ReceiveType']),
        "RcvState": int(row['RcvState']),
        "RxTypeIn": int(row['RxTypeIn']),
        "VisitOn": visit_on_value_trimmed1,
        "PatientId": patient_id,
        "PtName": full_name,
        "PtAge": int(row['PtAge']),
        "PtGender": int(row['Gender']),
        "PtDob": str(row['Dob']),
        "PtAddress": str(row['Address']),
        "PtDistrict": str(int(row['District'])),
        "PtWard": str(int(row['Ward'])),
        "PtEthnic": Ethnic,
        "PtNationality": str(row['Nationality']),
        "PtOccupation": row['Occupation'],
        "InsCardNo": str(row['InsCardNo']),
        "InsBenefitType": int(row['InsBenefitType']),
        "InsBenefitRatio": int(row['InsBenefitRatio']),
        "Attribute": int(row['Attribute']),
        "FileStoreNo": "",
        "CreateById": int(row['CreateById']),
        "Status": row['Status'],
        "InsCheckedMessage": str(row['InsCheckedMessage']),
        "InsCheckedStatus": InsCheckedStatus,
        "Entry": {
            "MedServiceId": MedServiceId,
            "WardUnitId": WardUnitId,
            "OnDate": visit_on_value_trimmed1,
            "CreateById": int(row['CreateById']),
            "Status": row['Status'],
            "InsBenefitType": int(row['InsBenefitType']),
            "InsBenefitRatio": int(row['InsBenefitRatio']),
            "PriceId": int(row['PriceId']),
            "CreateByWardUnitId": int(row['CreateByWardUnitId']),
            "Service": None,
            "LabExams": None,
            "CreatedBy": None,
            "ContentHash": row['ContentHash']
        },
        "FullPatientCode": None,
        "InsBenefitTypeName": None,
        "WardUnitNames": None,
        "CreateByStaffName": None,
        "ContentHash": row['ContentHash1'],
        "LastUpdateByStaffName": None,
        "ModifiedOn": None
    }
    # Kiểm tra xem loại bảo hiểm có phải là BHYT hay không
    if int(row["InsBenefitType"]) == 2:
        # Nếu là BHYT, hiển thị "InsCheckedMessage" và "InsCheckedStatus"
        InsCheckedStatus = int(row['InsCheckedStatus']) if not pd.isna(row['InsCheckedStatus']) else None
        visit_data["InsCheckedMessage"] = str(row['InsCheckedMessage'])
        visit_data["InsCheckedStatus"] = InsCheckedStatus
    else:
        # Nếu không phải là BHYT, loại bỏ các trường "InsCheckedMessage" và "InsCheckedStatus"
        del visit_data["InsCheckedMessage"]
        del visit_data["InsCheckedStatus"]
        del visit_data["InsCardNo"]
    return visit_data, visit_on


def extract_numeric_suffix(s):
    """Extracts the numeric suffix from a string, if any."""
    if isinstance(s, str):  # Kiểm tra xem s có phải là một chuỗi không
        match = re.search(r'(\d+)$', s)
        return int(match.group(1))
    else:
        return None


def increment_string(prefix, counter):
    """Generates a new string by incrementing the counter."""
    return f"{prefix}{counter}"


def generate_sum_additional_data(original_data, num_records):
    new_data = []

    # Tạo các biến lưu trữ giá trị ban đầu cho mỗi cột
    max_first_name = original_data["FirstName"].max() if not original_data.empty else 0
    max_id_card_no = original_data["IdCardNo"].max() if not original_data.empty else 0
    ins_card_no_prefix = re.sub(r'\d+$', '', original_data["InsCardNo"].iloc[0]) if not original_data.empty else ""
    max_ins_card_no = int(original_data["InsCardNo"].apply(extract_numeric_suffix).max())

    for _ in range(num_records):
        for _ in range(2):  # Lặp qua hai dòng dữ liệu
            new_row = deepcopy(original_data.iloc[_])

            # Sử dụng các giá trị hiện tại cho mỗi dòng dữ liệu mới
            new_row["FirstName"] = max_first_name + 1 + _
            new_row["IdCardNo"] = max_id_card_no + 1 + _
            if not pd.isnull(new_row["InsCardNo"]):
                new_row["InsCardNo"] = increment_string(ins_card_no_prefix, max_ins_card_no + 1)

            new_data.append(new_row)

        # Cập nhật giá trị mới nhất của các biến
        max_first_name += 2
        max_id_card_no += 2
        max_ins_card_no += 2

    return pd.DataFrame(new_data)


def generate_additional_data(original_data, num_records):
    new_data = []

    # Tạo các biến lưu trữ giá trị ban đầu cho mỗi cột
    max_first_name = original_data["FirstName"].max() if not original_data.empty else 0
    max_id_card_no = original_data["IdCardNo"].max() if not original_data.empty else 0
    ins_card_no_prefix = re.sub(r'\d+$', '', original_data["InsCardNo"].iloc[0]) if not original_data.empty else ""
    max_ins_card_no = original_data["InsCardNo"].apply(extract_numeric_suffix).max() if not original_data.empty else 0

    for _ in range(num_records):
        for _, row in original_data.iterrows():
            new_row = deepcopy(row)

            # Sử dụng các giá trị hiện tại cho mỗi dòng dữ liệu mới
            new_row["FirstName"] = max_first_name + 1
            new_row["IdCardNo"] = max_id_card_no + 1
            new_row["InsCardNo"] = increment_string(ins_card_no_prefix, max_ins_card_no + 1)

            new_data.append(new_row)

        # Cập nhật giá trị mới nhất của các biến
        max_first_name += 1
        max_id_card_no += 1
        max_ins_card_no += 1

    return pd.DataFrame(new_data)


def write_data_to_excel(file_path, sheet_name, data):
    # Ghi dữ liệu vào tệp Excel và ghi đè lên dữ liệu hiện có
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        data.to_excel(writer, sheet_name=sheet_name, index=False)


def copy_sheet_values(file_path, sheet_name, verify_sheet_name, columns_to_copy):
    # Đọc dữ liệu từ sheet 1
    df_sheet1 = pd.read_excel(file_path, sheet_name=sheet_name)

    # Chọn các cột cần thiết
    df_to_copy = df_sheet1[columns_to_copy]

    # Ghi dữ liệu vào sheet 2, thay thế sheet nếu nó đã tồn tại
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df_to_copy.to_excel(writer, sheet_name=verify_sheet_name, index=False)


def compare_data(json_data, excel_row):
    for key, value in json_data.items():
        if key in excel_row and str(value) != str(excel_row[key]):
            return "Failed"
    return "Passed"


def process_create_patient_from_excel(file_path):
    sheet_name = "Data"
    check_sheet_name = "Check"
    columns_to_copy = ["FirstName", "LastName", "InsCardNo", "CreateById", "InsBenefitRatio", "InsBenefitType"]

    # Đọc dữ liệu từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Gọi hàm copy_sheet_values để sao chép các cột cần thiết sang sheet Verify
    copy_sheet_values(file_path, sheet_name, check_sheet_name, columns_to_copy)

    verify_data = pd.read_excel(file_path, sheet_name=check_sheet_name)

    for index, row in excel_data.iterrows():
        verify_row = verify_data.iloc[index]
        patient_data = create_patient_from_excel(row)
        abc = create_patient(patient_data, verify_row)
        if abc is None:  # Check if response_data is None, indicating failure
            patient_id, patient_result = None, "Failed"
        else:
            patient_id, patient_result = abc
        print(f"\nCreate patient result {index}: {patient_result}")
        return abc


def process_create_insurance_from_excel(file_path):
    sheet_name = "Data"
    check_sheet_name = "Check"
    columns_to_copy = ["FirstName", "LastName", "InsCardNo", "CreateById", "InsBenefitRatio", "InsBenefitType"]

    # Đọc dữ liệu từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Gọi hàm copy_sheet_values để sao chép các cột cần thiết sang sheet Verify
    copy_sheet_values(file_path, sheet_name, check_sheet_name, columns_to_copy)

    verify_data = pd.read_excel(file_path, sheet_name=check_sheet_name)

    entry_ids = []  # Danh sách để lưu các entry_id
    for index, row in excel_data.iterrows():
        verify_row = verify_data.iloc[index]
        patient_data = create_patient_from_excel(row)
        patient_id, patient_result = create_patient(patient_data, verify_row)
        print(f"\nCreate patient result {index}: {patient_result}")

        if int(row["InsBenefitType"]) == 2:
            insurance_data, dob = create_insurance_from_excel(row, patient_id)
            check = create_insurance(insurance_data, dob, verify_data)
            if check is None:  # Check if response_data is None, indicating failure
                response_data, patient_id, insurance_result = None, None, "Failed"
            else:
                response_data, patient_id, insurance_result = check
            print(f"Create insurance result {index}: {insurance_result}")
            return check


def process_patient_from_excel(file_path):
    sheet_name = "Data"
    check_sheet_name = "Check"
    columns_to_copy = ["FirstName", "LastName", "InsCardNo", "CreateById", "InsBenefitRatio", "InsBenefitType"]

    # Đọc dữ liệu từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Gọi hàm copy_sheet_values để sao chép các cột cần thiết sang sheet Verify
    copy_sheet_values(file_path, sheet_name, check_sheet_name, columns_to_copy)

    verify_data = pd.read_excel(file_path, sheet_name=check_sheet_name)

    entry_ids = []  # Danh sách để lưu các entry_id
    for index, row in excel_data.iterrows():
        verify_row = verify_data.iloc[index]
        patient_data = create_patient_from_excel(row)
        patient_id, patient_result = create_patient(patient_data, verify_row)
        print(f"\nCreate patient result {index}: {patient_result}")

        if int(row["InsBenefitType"]) == 2:
            insurance_data, dob = create_insurance_from_excel(row, patient_id)
            response_data, patient_id, insurance_result = create_insurance(insurance_data, dob, verify_data)
            print(f"Create insurance result {index}: {insurance_result}")

        visit_data, visit_on = create_visit_from_excel(row, patient_id)
        result = create_visit(visit_data, visit_on, verify_data)
        if result is None:  # Check if response_data is None, indicating failure
            response_data, entry_id, visit_result = None, None, "Failed"
        else:
            response_data, entry_id, visit_result = result
        print(f"Create visit result {index}: {result}")
        entry_ids.append(entry_id)  # Lưu entry_id vào danh sách
    print("entry_ids", entry_ids)
    return entry_ids


def process_generate_patient_from_excel(file_path):
    sheet_name = "Data"
    verify_sheet_name = "Check"
    columns_to_copy = ["FirstName", "LastName", "InsCardNo", "CreateById", "InsBenefitRatio", "InsBenefitType"]

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Tạo dữ liệu bổ sung và ghi vào file Excel
    num_records_to_add = 2  # Số dòng dữ liệu bổ sung
    additional_data = generate_additional_data(excel_data.tail(1), num_records_to_add)
    write_data_to_excel(file_path, sheet_name, additional_data)

    # Đọc lại dữ liệu đã ghi vào file
    additional_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Gọi hàm copy_sheet_values để sao chép các cột cần thiết sang sheet Verify
    copy_sheet_values(file_path, sheet_name, verify_sheet_name, columns_to_copy)

    # Đọc dữ liệu từ sheet Verify để so sánh
    verify_data = pd.read_excel(file_path, sheet_name=verify_sheet_name)

    entry_ids = []  # Danh sách để lưu các entry_id
    for index, row in additional_data.iterrows():
        verify_row = verify_data.iloc[index]
        patient_data = create_patient_from_excel(row)
        patient_id, patient_result = create_patient(patient_data, verify_row)
        print(f"\nCreate patient result {index}: {patient_result}")

        if int(row["InsBenefitType"]) == 2:
            insurance_data, dob = create_insurance_from_excel(row, patient_id)
            response_data, patient_id, insurance_result = create_insurance(insurance_data, dob, verify_data)
            print(f"Create insurance result {index}: {insurance_result}")

        visit_data, visit_on = create_visit_from_excel(row, patient_id)
        response_data, entry_id, visit_result = create_visit(visit_data, visit_on, verify_data)
        print(f"Create visit result {index}: {visit_result}")
        entry_ids.append(entry_id)  # Lưu entry_id vào danh sách

    print("entry_ids", entry_ids)
    return entry_ids  # Trả về danh sách các entry_id


def process_generate_sum_patient_from_excel(file_path):
    sheet_name = "Data"
    verify_sheet_name = "Check"
    columns_to_copy = ["FirstName", "LastName", "InsCardNo", "CreateById", "InsBenefitRatio", "InsBenefitType"]

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Tạo dữ liệu bổ sung và ghi vào file Excel
    num_records_to_add = 2  # Số dòng dữ liệu bổ sung
    additional_data = generate_sum_additional_data(excel_data.tail(2), num_records_to_add)
    write_data_to_excel(file_path, sheet_name, additional_data)

    # Đọc lại dữ liệu đã ghi vào file
    additional_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Gọi hàm copy_sheet_values để sao chép các cột cần thiết sang sheet Verify
    copy_sheet_values(file_path, sheet_name, verify_sheet_name, columns_to_copy)

    # Đọc dữ liệu từ sheet Verify để so sánh
    verify_data = pd.read_excel(file_path, sheet_name=verify_sheet_name)

    entry_ids = []  # Danh sách để lưu các entry_id
    for index, row in additional_data.iterrows():
        verify_row = verify_data.iloc[index]
        patient_data = create_patient_from_excel(row)
        patient_id, patient_result = create_patient(patient_data, verify_row)
        print(f"\nCreate patient result {index}: {patient_result}")

        if int(row["InsBenefitType"]) == 2:
            insurance_data, dob = create_insurance_from_excel(row, patient_id)
            response_data, patient_id, insurance_result = create_insurance(insurance_data, dob, verify_data)
            print(f"Create insurance result {index}: {insurance_result}")

        visit_data, visit_on = create_visit_from_excel(row, patient_id)
        response_data, entry_id, visit_result = create_visit(visit_data, visit_on, verify_data)
        print(f"Create visit result {index}: {visit_result}")
        entry_ids.append(entry_id)  # Lưu entry_id vào danh sách

    print("entry_ids", entry_ids)
    return entry_ids  # Trả về danh sách các entry_id