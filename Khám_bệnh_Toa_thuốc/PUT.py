import numpy as np
import requests
import pandas as pd
from Cấu_hình.Setup import base_url_2, auth_token_2
from Tiếp_nhận.POST import compare_data

# Base url
base_url = "http://115.79.31.186:1096"
# Auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjM4MzkiLCJyb2xlIjoiQWRtaW4iLCJBY2NvdW50TmFtZSI6Imh1bmdxYiIsIkNsaWVudElwQWRkcmVzcyI6Ijo6MSIsIklzTG9jYWxJcCI6IlRydWUiLCJuYmYiOjE3MTUxODQ2NDIsImV4cCI6MTcxNTE4ODI0MiwiaWF0IjoxNzE1MTg0NjQyfQ.CihuC246iqFUos4MNZtNWs2q_SBOtmbXz4NRNuRQ4rg"


def clean_data(value):
    if isinstance(value, pd.Series):
        return value.apply(clean_data)
    else:
        return str(value) if not pd.isna(value) else None


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


def sanitize_float(value):
    if pd.isna(value) or not np.isfinite(value):
        return 0.0
    return float(value)


def handle_null(value, default=None, to_type=int):
    return to_type(value) if not pd.isna(value) else default


def sanitize_nullable_decimal(value):
    try:
        if pd.isna(value):
            return None
        return float(value)
    except (ValueError, TypeError):
        return None


def prepare_medicine_data(row, info):
    MedRcdNo = clean_data(row['MedRcdNo'])
    NationalCode = "0" + clean_data(row['NationalCode'])
    ServiceGroupName = clean_data(row['ServiceGroupName'])
    LabExams = clean_data(row['LabExams'])
    CreatedBy = clean_data(row['CreatedBy'])
    isPassOnWarning_excel = str(row['IsPassOnWarning'])
    isPassOnWarning = True if isPassOnWarning_excel.lower() == 'true' else False

    IsInInsCat = False if str(row['IsInInsCat']).lower() == 'false' else True
    IsLocalPharmacy = False if str(row['IsLocalPharmacy']).lower() == 'false' else True
    IsPaid = False if str(row['IsPaid']).lower() == 'false' else True

    px_items = []

    px_item = {
        "ItemId": int(row['ItemIds']),
        "ItemName": str(row['ItemName']),
        "ItemUnit": str(row['ItemUnit']),
        "Qty": sanitize_nullable_decimal(row['Qty']),
        "Notes": clean_data(row['Notes']),
        "DoseNO": sanitize_nullable_decimal(row['DoseNO']),
        "DoseAN": sanitize_nullable_decimal(row['DoseAN']),
        "TxtDoseNO": clean_data(row['TxtDoseNO']),
        "TxtDoseAN": clean_data(row['TxtDoseAN']),
        "UseWeekDay": int(row['UseWeekDay']),
        "UseDays": handle_null(row['UseDays']),
        "Attribute": int(row['Attribute']),
        "IsPaid": IsPaid,
        "StoreId": int(row['StoreIds']),
        "InvSource": int(row['InvSource']),
        "MedStrenght": clean_data(row['MedStrenght']),
        "MedUseRoute": clean_data(row['MedUseRoute1']),
        "MedItem": {
            "ItemId": int(row['ItemIds']),
            "InsIndex": clean_data(row['InsIndex']),
            "Code": clean_data(row['Code2']),
            "Type": int(row['Type']),
            "ItemCat": int(row['ItemCat']),
            "ATC": clean_data(row['ATC']),
            "Name": str(row['Name']),
            "Description": clean_data(row['Description']),
            "NtlCode": clean_data(row['NtlCode']),
            "NtlName": str(row['NtlName']),
            "Unit": clean_data(row['Unit']),
            "PkgUnit": clean_data(row['PkgUnit']),
            "PkgUnitText": clean_data(row['PkgUnitText']),
            "UsageUnit": clean_data(row['UsageUnit']),
            "PPP": int(row['PPP']),
            "PPU": int(row['PPU']),
            "MedAI": clean_data(row['MedAI']),
            "MedUseRoute": clean_data(row['MedUseRoute']),
            "MedDosageForm": clean_data(row['MedDosageForm']),
            "MedStrenght": str(row['MedStrenght']),
            "MedGbCode": clean_data(row['MedGbCode']),
            "RegNo": str(row['RegNo']),
            "MfrCode": int(row['MfrCode']),
            "MfrName": str(row['MfrName']),
            "MfrAddr": str(row['MfrAddr']),
            "MfrCountry": str(row['MfrCountry']),
            "InsCode": clean_data(row['InsCode']),
            "InsName": str(row['InsName']),
            "InsPayRatio1": int(row['InsPayRatio1']),
            "Price": sanitize_float(row['Price']),
            "Attribute": int(row['Attribute']),
            "DrugWarnings": clean_data(row['DrugWarnings']),
            "StockCritLevel": int(row['StockCritLevel']),
            "Status": int(row['Status']),
            "BidGroupCode": int(row['BidGroupCode']),
            "BidPackageCode": int(row['BidPackageCode']),
            "BidDocNo": clean_data(row['BidDocNo']),
            "SysFullName": str(row['SysFullName']),
            "ProcessingMethodCode": clean_data(row['ProcessingMethodCode']),
            "Note": clean_data(row['Note']),
            "FullName": str(row['FullName']),
            "IsInInsCat": IsInInsCat,
            "Remaining": sanitize_float(row['Remaining']),
            "InsPrice": sanitize_float(row['InsPrice']),
            "AttributeDisplay": str(row['AttributeDisplay']),
            "IsLocalPharmacy": IsLocalPharmacy,
            "PlanCoefficient": sanitize_float(row['PlanCoefficient']),
            "PurchaseName": handle_null(row['PurchaseName'], default=None, to_type=int)
        },
        "Code": clean_data(row['Code']),
        "InsBenefitType": handle_null(row['InsBenefitType'], default=None, to_type=int),
        "OnVisit": handle_null(row['OnVisit'], default=None, to_type=int),
        "WardAdmId": handle_null(row['WardAdmId'], default=None, to_type=int),
        "TxVisitMedReturnId": handle_null(row['TxVisitMedReturnId'], default=None, to_type=int),
        "ApproveQty": handle_null(row['ApproveQty'], default=None, to_type=int),
        "Dosage": str(row['Dosage'])
    }
    px_items.append(px_item)

    medicine_data = {
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
        "txInstruction": 2,
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
        "PxItems": px_items,
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

    return medicine_data, medicine_data["entryId"]


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


def update_medicine_patient(all_info, data, verify_data):
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


def update_medicine_patient_from_excel(row, entry_id):
    from Khám_bệnh_Toa_thuốc.GET import get_all_info
    from Khám_bệnh_Toa_thuốc.POST import data_medicine

    # Lấy tất cả thông tin bệnh nhân
    all_info = get_all_info(entry_id)
    print("all_info:", all_info)
    if len(all_info) == 0:
        print("No information about patients.")
        return []

    # Lặp qua tất cả các thông tin bệnh nhân
    for info in all_info:
        # Chuẩn bị thông tin bệnh nhân và lấy entryId
        information_data, entryId = prepare_information_data(row, info)

        # Cập nhật thông tin bệnh nhân
        update_information_patient(all_info, information_data)

        # Chỉ định thuốc
        data_medicine(row)

        # Chuẩn bị thông tin bệnh nhân và lấy entryId
        medicine_data, entryId = prepare_medicine_data(row, info)

        # Cập nhật thông tin bệnh nhân
        update_information_patient(all_info, medicine_data)
