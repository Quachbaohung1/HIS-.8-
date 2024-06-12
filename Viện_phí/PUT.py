import datetime
import sys
import requests
import json
import pandas as pd

# Base url
base_url = "http://115.79.31.186:1096"
# Auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjM4MzkiLCJyb2xlIjoiQWRtaW4iLCJBY2NvdW50TmFtZSI6Imh1bmdxYiIsIkNsaWVudElwQWRkcmVzcyI6Ijo6MSIsIklzTG9jYWxJcCI6IlRydWUiLCJuYmYiOjE3MTUxODQ2NDIsImV4cCI6MTcxNTE4ODI0MiwiaWF0IjoxNzE1MTg0NjQyfQ.CihuC246iqFUos4MNZtNWs2q_SBOtmbXz4NRNuRQ4rg"


def clean_data(value):
    return str(value) if not pd.isna(value) else ''


def update_information_patient(entryId, data):
    headers = {"Authorization": auth_token}
    url = f"{base_url}/pms/VisitEntries/{entryId}?forceNull=True&ptFullAddress=5%2F49+Ntl%2C+Ph%C6%B0%E1%BB%9Dng+07%2C+Qu%E1%BA%ADn+B%C3%ACnh+Th%E1%BA%A1nh%2C+Th%C3%A0nh+ph%E1%BB%91+H%E1%BB%93+Ch%C3%AD+Minh&isPassMedAIValid=&isPassMedAIValidOtherPx=False&isPassInteraction=False&isRemoveAllConsulation=True&isUpdateEntryValOnly=False&isBackupStatus=True"
    response = requests.put(url, json=data, headers=headers)
    response.raise_for_status()


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
    for item in info:
        information_data = {
            "entryId": item["entryId"],
            "visitId": item["visitId"],
            "medServiceId": item["medServiceId"],
            "wardUnitId": item["wardUnitId"],
            "onDate": item["createOn"],
            "dxSymptom": clean_data(row['DxSymptom']),
            "initialDxICD": clean_data(row['InitialDxICD']),
            "initialDxText": clean_data(row['InitialDxText']),
            "dxICD": clean_data(row['DxICD']),
            "dxText": clean_data(row['DxText']),
            "dxByStaffId": int(row['DxByStaffId']),
            "txInstruction": 3,
            "createOn": item["createOn"],
            "createById": item["createById"],
            "status": item["status"],
            "insBenefitType": item['insBenefitType'],
            "insBenefitRatio": item["insBenefitRatio"],
            "priceId": item["priceId"],
            "qmsNo": item["qmsNo"],
            "ticketId": item["ticketId"],
            "medRcdNo": MedRcdNo,
            "createByWardUnitId": item["createByWardUnitId"],
            "visitDXList": [{"IcdCode": "A00", "ICDReason": "false"}, {"IcdCode": "A02.0", "ICDReason": "false"}],
            "txVisit": {"createOn": item["createOn"], "createByStaffName": row['CreateByStaffName']},
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
        return information_data["entryId"], information_data
