import requests
import pandas as pd
from Cấu_hình.Setup import base_url_2, auth_token_2


def clean_data(value):
    return str(value) if not pd.isna(value) else ''


def update_information_patient(all_info, data):
    headers = {"Authorization": auth_token_2}
    try:
        for info in all_info:
            entryId = info['entryId']
            url = f"{base_url_2}/VisitEntries/{entryId}?forceNull=True&ptFullAddress=5%2F49+Ntl%2C+Ph%C6%B0%E1%BB%9Dng+07%2C+Qu%E1%BA%ADn+B%C3%ACnh+Th%E1%BA%A1nh%2C+Th%C3%A0nh+ph%E1%BB%91+H%E1%BB%93+Ch%C3%AD+Minh&isPassMedAIValid=&isPassMedAIValidOtherPx=False&isPassInteraction=False&isRemoveAllConsulation=True&isUpdateEntryValOnly=False&isBackupStatus=True"
            response = requests.put(url, json=data, headers=headers)
            response.raise_for_status()
            result_api = response.status_code
            return result_api
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"\nAn error occurred during patient creation: {e}")


def prepare_information_data(row, info):
    MedRcdNo = clean_data(row['MedRcdNo'])
    NationalCode = "0" + clean_data(row['NationalCode'])
    ServiceGroupName = clean_data(row['ServiceGroupName'])
    LabExams = clean_data(row['LabExams'])
    CreatedBy = clean_data(row['CreatedBy'])
    # Đọc giá trị từ file Excel
    isPassOnWarning_excel = str(row['IsPassOnWarning'])
    # Chuyển đổi giá trị từ chuỗi sang Boolean
    isPassOnWarning = True if isPassOnWarning_excel.lower() == 'true' else False
    information_data = {
        "entryId": info["entryId"],
        "visitId": info["visitId"],
        "medServiceId": info["medServiceId"],
        "wardUnitId": info["wardUnitId"],
        "onDate": info["createOn"],
        "dxSymptom": clean_data(row['DxSymptom']),
        "initialDxICD": clean_data(row['InitialDxICD']),
        "initialDxText": clean_data(row['InitialDxText']),
        "dxICD": clean_data(row['DxICD']),
        "dxText": clean_data(row['DxText']),
        "dxByStaffId": int(row['DxByStaffId']),
        "txInstruction": 8,
        "createOn": info["createOn"],
        "createById": info["createById"],
        "status": info["status"],
        "insBenefitType": info['insBenefitType'],
        "insBenefitRatio": info["insBenefitRatio"],
        "priceId": info["priceId"],
        "qmsNo": info["qmsNo"],
        "ticketId": info["ticketId"],
        "medRcdNo": MedRcdNo,
        "createByWardUnitId": info["createByWardUnitId"],
        "visitDXList": [{"IcdCode": "A00", "ICDReason": "false"}, {"IcdCode": "A02.0", "ICDReason": "false"}],
        "txVisit": {"createOn": info["createOn"], "createByStaffName": row['CreateByStaffName']},
        "pxItems": [],
        "service": {
            "serviceId": int(row['ServiceId']),
            "code": clean_data(row['Code']),
            "typeL1": int(row['TypeL1']),
            "typeL2": int(row['TypeL2']),
            "typeL3": int(row['TypeL3']),
            "typeL4": int(row['TypeL4']),
            "category": int(row['Category']),
            "rank": int(row['Rank']),
            "unit": clean_data(row['Unit']),
            "description": clean_data(row['Description']),
            "insServiceName": clean_data(row['InsServiceName']),
            "attribute": int(row['Attribute2']),
            "nationalCode": NationalCode,
            "status": int(row['Status']),
            "insPrice": float(row['InsPrice']),
            "price": float(row['Price']),
            "priceId": int(row['PriceId']),
            "serviceGroupName": ServiceGroupName
        },
        "labExams": LabExams,
        "createdBy": CreatedBy,
        "contentHash": clean_data(row['ContentHash']),
        "isPassOnWarning": isPassOnWarning
    }
    return information_data, information_data["entryId"]


def update_information_patient_from_excel(row, entry_id):
    from Khám_bệnh_CDDV.GET import get_all_info, get_data_by_entry_id
    from Khám_bệnh_CDDV.POST import start_service_designation, data_of_create_service_designation, create_service_designation

    # Lấy tất cả thông tin bệnh nhân
    all_info = get_all_info(entry_id)
    print("all_info:", all_info)
    if len(all_info) == 0:
        print("No information about patients.")
        return []

    frVisitEntryIds = []
    all_datas = []

    # Lặp qua tất cả các thông tin bệnh nhân
    for info in all_info:
        # Chuẩn bị thông tin bệnh nhân và lấy entryId
        information_data, entryId = prepare_information_data(row, info)

        # Cập nhật thông tin bệnh nhân
        update_information_patient(all_info, information_data)

        # Lấy dữ liệu theo entryId
        entry_data = get_data_by_entry_id(entryId)

        # Bắt đầu chỉ định dịch vụ
        all_infoa = start_service_designation(entry_data)

        # Tạo chỉ định dịch vụ và lấy frVisitEntryId
        service_data = data_of_create_service_designation(row, all_infoa, all_info)

        frVisitEntryId, response_data = create_service_designation(service_data)

        # Thêm frVisitEntryId vào danh sách
        frVisitEntryIds.append(frVisitEntryId)
        all_datas.append(response_data)

    print("frVisitEntryIds:", frVisitEntryIds)
    print("all_datas:", all_datas)
    return frVisitEntryIds, all_datas
