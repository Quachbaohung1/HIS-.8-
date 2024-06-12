import requests
import pandas as pd


#Base url
base_url = "http://115.79.31.186:1096"
#Auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjM4MzkiLCJyb2xlIjoiQWRtaW4iLCJBY2NvdW50TmFtZSI6Imh1bmdxYiIsIkNsaWVudElwQWRkcmVzcyI6Ijo6MSIsIklzTG9jYWxJcCI6IlRydWUiLCJuYmYiOjE3MTUxODQ2NDIsImV4cCI6MTcxNTE4ODI0MiwiaWF0IjoxNzE1MTg0NjQyfQ.CihuC246iqFUos4MNZtNWs2q_SBOtmbXz4NRNuRQ4rg"


def clean_data(value):
    return str(value) if not pd.isna(value) else ''


def update_CLS_patient(data):
    headers = {"Authorization": auth_token}
    url = f"{base_url}/cis/LabExams/?ptFullAddress=&isUpdateItem=False&isUpdateOnlyItem=False"
    response = requests.put(url, json=data, headers=headers)
    response.raise_for_status()


def confirmed_CLS_patient(data):
    headers = {"Authorization": auth_token}
    url = f"{base_url}/cis/LabExams/?ptFullAddress=5%2F49+Ntl%2C+Ph%C6%B0%E1%BB%9Dng+07%2C+Qu%E1%BA%ADn+B%C3%ACnh+Th%E1%BA%A1nh%2C+Th%C3%A0nh+ph%E1%BB%91+H%E1%BB%93+Ch%C3%AD+Minh&isUpdateItem=False&isUpdateOnlyItem=False"
    response = requests.put(url, json=data, headers=headers)
    response.raise_for_status()


def prepare_information_data(row, entry_ids, fr_visit_entry_id_manager):
    from Cận_lâm_sàng.GET import get_information_patient_next

    Service = clean_data(row['Service'])
    LabExams = clean_data(row['LabExams'])
    CreatedBy = clean_data(row['CreatedBy'])
    FullPatientCode = clean_data(row['FullPatientCode'])
    InsBenefitTypeName = clean_data(row['InsBenefitTypeName'])
    WardUnitNames = clean_data(row['WardUnitNames'])
    CreateByStaffName = clean_data(row['CreateByStaffName'])
    LastUpdateByStaffName = clean_data(row['LastUpdateByStaffName'])
    ModifiedOn = clean_data(row['ModifiedOn'])
    TypeL0Code = clean_data(row['TypeL0Code'])
    ByProviderCode = clean_data(row['ByProviderCode'])
    ServiceTypeL3Name = clean_data(row['ServiceTypeL3Name'])
    ReqDate = clean_data(row['ReqDate'])
    MedItem = clean_data(row['MedItem'])
    Checked = clean_data(row['Checked'])
    TotalInvoiceAmtRound = clean_data(row['TotalInvoiceAmtRound'])
    TotalReceiptAmtRound = clean_data(row['TotalReceiptAmtRound'])
    ReqBy = clean_data(row['ReqBy'])

    all_data_info_patients = get_information_patient_next(entry_ids)
    print("all_data_info_patients:", all_data_info_patients)

    for all_data_info_patient in all_data_info_patients:
        entry = all_data_info_patient.get("entry", {})
        LabExamItems = all_data_info_patient.get("labExamItems", {})

        # Loop through LabExamItems
        for lab_exam_item in LabExamItems:

            information_data = {
                "LabExId": all_data_info_patient.get("labExId"),
                "Type": all_data_info_patient.get("type"),
                "PatientId": all_data_info_patient.get("patientId"),
                "RefNo": all_data_info_patient.get("refNo"),
                "OnDate": all_data_info_patient.get("onDate"),
                "LabReqById": all_data_info_patient.get("labReqById"),
                "LabReqNotes": all_data_info_patient.get("labReqNotes"),
                "DxICD": all_data_info_patient.get("dxICD"),
                "DxText": all_data_info_patient.get("dxText"),
                "Attribute": all_data_info_patient.get("attribute"),
                "FrVisitEntryId": all_data_info_patient.get("frVisitEntryId"),
                "LabDxConclusion": str(row['LabDxConclusion']),
                "LabDxConcludeById": int(row['LabDxConcludeById']),
                "LabDoneById": int(row['LabDoneById']),
                # "LabDxApproveById": int(row['LabDxApproveById']),
                "LabDxIssueOn": all_data_info_patient.get("createOn"),
                "CreateOn": all_data_info_patient.get("createOn"),
                "CreateById": all_data_info_patient.get("createById"),
                "LabDxDescription": "kwQAAB+LCAAAAAAABAClVM1u1DAQPheJd7CClJ6Sze6y2m2SRoJd4EDFAfECjuNNhk3syPZSQtUn4EKFekIceuBeruRa7XvkTXD+2hSEoDRSJHtmPs/3zSfbD3lUBA8f7PlSFSlFqsjpoaHoezUiUhp1Zs8m8rnzZLyazmcndcbCKcTMfbuVCtaF14SARZQp18mVl2ERA6uXaPB7KTBqJRTiRLlje3banTyeHownk+n0hPCUC/eR03xeiMkmFnzLIqtNKIGZzLHQXbw1Z8pa4wzSwt1/AxmV6BU9Rq95htl+m5Xwgbrjx3lXfNz2ZVxkOO0qar19pGdzMHu2mE9WzlBnStfqH0X2xywW8+VkNXv6v6KWunMoYCjFuYsUf9SEGl9zRFIs5aFx46IR+Loru0n0JhiBdVSVn1mMWFyV3wlKMKDQpAQE8XS9ibvV1VlVngGyXyYmb0MxUkn141uBVFWeM73ZXe4udFRjMNkq6hFEtnovd5dV+VUXiOtj8wQyW1PWlAJ/lAd3pbz8pYWCDG0GxGIwsYI0oh6z0dWnlkCMNia0MJZoubgDKsEbSFV+AaQVXTA9AIgFftcU1roa+H0I/31qLNmirCvS89FJuO3Ffdq/MHk/r96NhJv4WuNt04eTJD0SRVX5kSR/YtFfo99Y9BfDCEwWytwb4kfdU/QTDSCn/JMEAAA=",
                "LabDxTechnique": str(row['ServiceName']),
                "LabDxComment": str(row['LabDxComment']),
                "LabDxOn": all_data_info_patient.get("createOn"),
                # "LabDxApproveOn": all_data_info_patient.get("labDxApproveOn"),
                "OrdGrpId": all_data_info_patient.get("ordGrpId"),
                "Status": int(row['Status']),
                "IdToFiller": all_data_info_patient.get("idToFiller"),
                "WardUnitId": all_data_info_patient.get("wardUnitId"),
                "SysOrdGrpId": all_data_info_patient.get("sysOrdGrpId"),
                "AbbrId": int(row['AbbrId']),
                "DxInitial": str(row['DxInitial']),
                "LabDxDescriptionHtml": "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\r\n<html xmlns=\"http://www.w3.org/1999/xhtml\">\r\n\t<head>\r\n\t\t<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /><title>\r\n\t\t</title>\r\n\t\t<style type=\"text/css\">\r\n\t\t\t.csF0A1D375{text-align:justify;text-indent:0pt;margin:0pt 0pt 0pt 0pt;line-height:1.5}\r\n\t\t\t.cs13912233{color:#000000;background-color:transparent;font-family:'Times New Roman';font-size:14pt;font-weight:normal;font-style:normal;}\r\n\t\t\t.cs95E872D0{text-align:left;text-indent:0pt;margin:0pt 0pt 0pt 0pt}\r\n\t\t\t.cs887C2D5B{color:#000000;background-color:transparent;font-family:Calibri;font-size:10pt;font-weight:normal;font-style:normal;}\r\n\t\t</style>\r\n\t</head>\r\n\t<body>\r\n\t\t<p class=\"csF0A1D375\"><span class=\"cs13912233\">-Lồng ngực hai b&ecirc;n c&acirc;n đối .Kh&ocirc;ng thấy tổn thương c&aacute;c cung sườn tr&ecirc;n phim.</span></p><p class=\"csF0A1D375\"><span class=\"cs13912233\">-C&aacute;c cung tim kh&ocirc;ng gi&atilde;n. Đường k&iacute;nh ngang tim trong giới hạn b&igrave;nh thường.</span></p><p class=\"csF0A1D375\"><span class=\"cs13912233\">-Kh&ocirc;ng thấy tổn thương nhu m&ocirc; phổi hai b&ecirc;n.</span></p><p class=\"csF0A1D375\"><span class=\"cs13912233\">-G&oacute;c sườn ho&agrave;nh hai b&ecirc;n kh&ocirc;ng c&oacute; dịch.</span></p><p class=\"cs95E872D0\"><span class=\"cs887C2D5B\">&nbsp;</span></p></body>\r\n</html>\r\n",
                "Visit": {
                    "VisitId": all_data_info_patient.get("visitId"),
                    "VisitCode": all_data_info_patient.get("visitCode"),
                    "ReceiveType": all_data_info_patient.get("receiveType"),
                    "RcvState": all_data_info_patient.get("rcvState"),
                    "RxTypeIn": all_data_info_patient.get("rxTypeIn"),
                    "VisitOn": all_data_info_patient.get("visitOn"),
                    "PatientId": all_data_info_patient.get("patientId"),
                    "PtName": all_data_info_patient.get("ptName"),
                    "PtAge": all_data_info_patient.get("ptAge"),
                    "PtGender": all_data_info_patient.get("ptGender"),
                    "PtDob": all_data_info_patient.get("ptDob"),
                    "PtAddress": all_data_info_patient.get("ptAddress"),
                    "PtDistrict": all_data_info_patient.get("ptDistrict"),
                    "PtWard": all_data_info_patient.get("ptWard"),
                    "PtEthnic": all_data_info_patient.get("ptEthnic"),
                    "PtNationality": all_data_info_patient.get("ptNationality"),
                    "PtOccupation": all_data_info_patient.get("ptOccupation"),
                    "InsCardId": all_data_info_patient.get("insCardId"),
                    "InsCardNo": all_data_info_patient.get("insCardNo"),
                    "InsBenefitType": all_data_info_patient.get("insBenefitType"),
                    "InsBenefitRatio": all_data_info_patient.get("insBenefitRatio"),
                    "Attribute": all_data_info_patient.get("attribute"),
                    "FileStoreNo": all_data_info_patient.get("fileStoreNo"),
                    "QmsNo": all_data_info_patient.get("qmsNo"),
                    "TicketId": all_data_info_patient.get("ticketId"),
                    "CreateOn": all_data_info_patient.get("createOn"),
                    "CreateById": all_data_info_patient.get("createById"),
                    "Status": all_data_info_patient.get("status"),
                    "InsCheckedMessage": all_data_info_patient.get("insCheckedMessage"),
                    "InsCheckedStatus": all_data_info_patient.get("insCheckedStatus"),
                    "StmId": all_data_info_patient.get("stmId"),
                    "Entry": {
                        "EntryId": entry.get("entryId"),
                        "VisitId": entry.get("visitId"),
                        "MedServiceId": entry.get("medServiceId"),
                        "WardUnitId": entry.get("wardUnitId"),
                        "OnDate": entry.get("onDate"),
                        "DxSymptom": entry.get("dxSymptom"),
                        "InitialDxICD": entry.get("initialDxICD"),
                        "InitialDxText": entry.get("initialDxText"),
                        "DxICD": entry.get("dxICD"),
                        "DxText": entry.get("dxText"),
                        "DxByStaffId": entry.get("dxByStaffId"),
                        "TxInstruction": entry.get("txInstruction"),
                        "CreateOn": entry.get("createOn"),
                        "CreateById": entry.get("createById"),
                        "Status": entry.get("status"),
                        "InsBenefitType": entry.get("insBenefitType"),
                        "InsBenefitRatio": entry.get("insBenefitRatio"),
                        "PriceId": entry.get("priceId"),
                        "QmsNo": entry.get("qmsNo"),
                        "TicketId": entry.get("ticketId"),
                        "MedRcdNo": entry.get("medRcdNo"),
                        "LastDxOn": entry.get("lastDxOn"),
                        "CreateByWardUnitId": entry.get("createByWardUnitId"),
                        "Service": Service,
                        "LabExams": LabExams,
                        "CreatedBy": CreatedBy,
                        "ContentHash": str(row['ContentHash']),
                        "IsPassOnWarning": entry.get("isPassOnWarning")
                    },
                    "FullPatientCode": FullPatientCode,
                    "InsBenefitTypeName": InsBenefitTypeName,
                    "WardUnitNames": WardUnitNames,
                    "CreateByStaffName": CreateByStaffName,
                    "ContentHash": str(row['ContentHash1']),
                    "LastUpdateByStaffName": LastUpdateByStaffName,
                    "ModifiedOn": ModifiedOn
                },
                "ServiceName": str(row['ServiceName']),
                "LabExamItems": [
                    {
                        "ExItemId": lab_exam_item.get("exItemId"),
                        "LabExId": lab_exam_item.get("labExId"),
                        "MedServiceId": lab_exam_item.get("medServiceId"),
                        "PriceId": lab_exam_item.get("priceId"),
                        "InsBenefitType": lab_exam_item.get("insBenefitType"),
                        "InsBenefitRatio": lab_exam_item.get("insBenefitRatio"),
                        "InsCardId": lab_exam_item.get("insCardId"),
                        "Qty": lab_exam_item.get("qty"),
                        "Price": lab_exam_item.get("price"),
                        "InsPrice": lab_exam_item.get("insPrice"),
                        "InsPriceRatio": lab_exam_item.get("insPriceRatio"),
                        "Amt": lab_exam_item.get("amt"),
                        "EqptCode": "XQ.1.75009.LSS21610030",
                        "Attribute": int(row['Attribute']),
                        "ByProviderId": lab_exam_item.get("byProviderId"),
                        "Status": lab_exam_item.get("status"),
                        "DiscAmtSeq": int(row['DiscAmtSeq']),
                        "MedServiceTypeL0": lab_exam_item.get("medServiceTypeL0"),
                        "MedServiceTypeL2": lab_exam_item.get("medServiceTypeL2"),
                        "MedServiceTypeL3": lab_exam_item.get("medServiceTypeL3"),
                        "NonSubclinical": lab_exam_item.get("nonSubclinical"),
                        "TypeL0Code": TypeL0Code,
                        "ByProviderCode": ByProviderCode,
                        "ByProviderName": str(row['ByProviderName']),
                        "ServiceGroupName": str(row['ServiceGroupName.1']),
                        "ServiceTypeL3Name": ServiceTypeL3Name,
                        "ServiceCode": str(row['ServiceCode']),
                        "ServiceName": str(row['ServiceName']),
                        "InsBenefitTypeName": InsBenefitTypeName,
                        "ReqDate": ReqDate,
                        "AttrString": str(row['AttrString']),
                        "PaidAttrString": str(row['PaidAttrString']),
                        "ServiceTypeOrderIndex": int(row['ServiceTypeOrderIndex']),
                        "MedItemType": int(row['MedItemType']),
                        "MedItem": MedItem,
                        "Checked": Checked,
                        "OnDate": all_data_info_patient.get("onDate"),
                        "TotalInvoiceAmtRound": TotalInvoiceAmtRound,
                        "TotalReceiptAmtRound": TotalReceiptAmtRound,
                        "PtAmt": float(row['PtAmt']),
                        "PtAmtRound": float(row['PtAmtRound']),
                        "PtAmtPaid": float(row['PtAmtPaid']),
                        "PtCoPayAmt": float(row['PtCoPayAmt']),
                        "PtCoPayAmtRound": float(row['PtCoPayAmtRound']),
                        "InsAmt": float(row['InsAmt']),
                        "InsAmtRound": float(row['InsAmtRound']),
                        "DiscAmt": float(row['DiscAmt']),
                        "ReqBy": ReqBy
                    }
                ],
                "ItemI0": {
                    "ExItemId": lab_exam_item.get("exItemId"),
                    "LabExId": lab_exam_item.get("labExId"),
                    "MedServiceId": lab_exam_item.get("medServiceId"),
                    "PriceId": lab_exam_item.get("priceId"),
                    "InsBenefitType": lab_exam_item.get("insBenefitType"),
                    "InsBenefitRatio": lab_exam_item.get("insBenefitRatio"),
                    "InsCardId": lab_exam_item.get("insCardId"),
                    "Qty": lab_exam_item.get("qty"),
                    "Price": lab_exam_item.get("price"),
                    "InsPrice": lab_exam_item.get("insPrice"),
                    "InsPriceRatio": lab_exam_item.get("insPriceRatio"),
                    "Amt": lab_exam_item.get("amt"),
                    "EqptCode": "XQ.1.75009.EEYO110",
                    "Attribute": int(row['Attribute']),
                    "ByProviderId": lab_exam_item.get("byProviderId"),
                    "Status": lab_exam_item.get("status"),
                    "DiscAmtSeq": int(row['DiscAmtSeq']),
                    "MedServiceTypeL0": lab_exam_item.get("medServiceTypeL0"),
                    "MedServiceTypeL2": lab_exam_item.get("medServiceTypeL2"),
                    "MedServiceTypeL3": lab_exam_item.get("medServiceTypeL3"),
                    "NonSubclinical": lab_exam_item.get("nonSubclinical"),
                    "TypeL0Code": TypeL0Code,
                    "ByProviderCode": ByProviderCode,
                    "ByProviderName": str(row['ByProviderName']),
                    "ServiceGroupName": str(row['ServiceGroupName.1']),
                    "ServiceTypeL3Name": ServiceTypeL3Name,
                    "ServiceCode": str(row['ServiceCode']),
                    "ServiceName": str(row['ServiceName']),
                    "InsBenefitTypeName": InsBenefitTypeName,
                    "ReqDate": ReqDate,
                    "AttrString": str(row['AttrString']),
                    "PaidAttrString": str(row['PaidAttrString']),
                    "ServiceTypeOrderIndex": int(row['ServiceTypeOrderIndex']),
                    "MedItemType": int(row['MedItemType']),
                    "MedItem": MedItem,
                    "Checked": Checked,
                    "OnDate": all_data_info_patient.get("onDate"),
                    "TotalInvoiceAmtRound": TotalInvoiceAmtRound,
                    "TotalReceiptAmtRound": TotalReceiptAmtRound,
                    "PtAmt": float(row['PtAmt']),
                    "PtAmtRound": float(row['PtAmtRound']),
                    "PtAmtPaid": float(row['PtAmtPaid']),
                    "PtCoPayAmt": float(row['PtCoPayAmt']),
                    "PtCoPayAmtRound": float(row['PtCoPayAmtRound']),
                    "InsAmt": float(row['InsAmt']),
                    "InsAmtRound": float(row['InsAmtRound']),
                    "DiscAmt": float(row['DiscAmt']),
                    "ReqBy": ReqBy
                },
                "FullAddress": str(row['FullAddress'])
            }
            return information_data


def prepare_confirmed_information_data(row, information_data):
    visit = information_data.get("Visit", {})
    entry = visit.get("Entry", {})
    itemI0 = information_data.get("ItemI0", {})
    LabExamItems = information_data.get("LabExamItems", {})
    # Loop through LabExamItems
    for lab_exam_item in LabExamItems:
        confirmed_data = {
            "LabExId": information_data.get("LabExId"),
            "Type": information_data.get("Type"),
            "PatientId": information_data.get("PatientId"),
            "RefNo": information_data.get("RefNo"),
            "OnDate": information_data.get("OnDate"),
            "LabReqById": information_data.get("LabReqById"),
            "LabReqNotes": information_data.get("LabReqNotes"),
            "DxICD": information_data.get("DxICD"),
            "DxText": information_data.get("DxText"),
            "Attribute": information_data.get("Attribute"),
            "FrVisitEntryId": information_data.get("FrVisitEntryId"),
            "LabDxConclusion": information_data.get("LabDxConclusion"),
            "LabDxConcludeById": information_data.get("LabDxConcludeById"),
            "LabDoneById": information_data.get("LabDoneById"),
            "LabDxApproveById": int(row['LabDxApproveById']),
            "LabDxIssueOn": information_data.get("LabDxIssueOn"),
            "CreateOn": information_data.get("CreateOn"),
            "CreateById": information_data.get("CreateById"),
            "LabDxDescription": information_data.get("LabDxDescription"),
            "LabDxTechnique": information_data.get("LabDxTechnique"),
            "LabDxComment": information_data.get("LabDxComment"),
            "LabDxOn": information_data.get("CreateOn"),
            "LabDxApproveOn": information_data.get("CreateOn"),
            "OrdGrpId": information_data.get("OrdGrpId"),
            "Status": information_data.get("Status"),
            "IdToFiller": information_data.get("IdToFiller"),
            "WardUnitId": information_data.get("WardUnitId"),
            "SysOrdGrpId": information_data.get("SysOrdGrpId"),
            "AbbrId": information_data.get("AbbrId"),
            "DxInitial": information_data.get("DxInitial"),
            "LabDxDescriptionHtml": information_data.get("LabDxDescriptionHtml"),
            "Visit": {
                "VisitId": visit.get("VisitId"),
                "VisitCode": visit.get("VisitCode"),
                "ReceiveType": visit.get("ReceiveType"),
                "RcvState": visit.get("RcvState"),
                "RxTypeIn": visit.get("RxTypeIn"),
                "VisitOn": visit.get("VisitOn"),
                "PatientId": visit.get("PatientId"),
                "PtName": visit.get("PtName"),
                "PtAge": visit.get("PtAge"),
                "PtGender": visit.get("PtGender"),
                "PtDob": visit.get("PtDob"),
                "PtAddress": visit.get("PtAddress"),
                "PtDistrict": visit.get("PtDistrict"),
                "PtWard": visit.get("PtWard"),
                "PtEthnic": visit.get("PtEthnic"),
                "PtNationality": visit.get("PtNationality"),
                "PtOccupation": visit.get("PtOccupation"),
                "InsCardId": visit.get("InsCardId"),
                "InsCardNo": visit.get("InsCardNo"),
                "InsBenefitType": visit.get("InsBenefitType"),
                "InsBenefitRatio": visit.get("InsBenefitRatio"),
                "Attribute": visit.get("Attribute"),
                "FileStoreNo": visit.get("FileStoreNo"),
                "QmsNo": visit.get("QmsNo"),
                "TicketId": visit.get("TicketId"),
                "CreateOn": visit.get("CreateOn"),
                "CreateById": visit.get("CreateById"),
                "Status": visit.get("Status"),
                "InsCheckedMessage": visit.get("InsCheckedMessage"),
                "InsCheckedStatus": visit.get("InsCheckedStatus"),
                "StmId": visit.get("StmId"),
                "Entry": {
                    "EntryId": entry.get("EntryId"),
                    "VisitId": entry.get("VisitId"),
                    "MedServiceId": entry.get("MedServiceId"),
                    "WardUnitId": entry.get("WardUnitId"),
                    "OnDate": entry.get("OnDate"),
                    "DxSymptom": entry.get("DxSymptom"),
                    "InitialDxICD": entry.get("InitialDxICD"),
                    "InitialDxText": entry.get("InitialDxText"),
                    "DxICD": entry.get("DxICD"),
                    "DxText": entry.get("DxText"),
                    "DxByStaffId": entry.get("DxByStaffId"),
                    "TxInstruction": entry.get("TxInstruction"),
                    "CreateOn": entry.get("CreateOn"),
                    "CreateById": entry.get("CreateById"),
                    "Status": entry.get("Status"),
                    "InsBenefitType": entry.get("InsBenefitType"),
                    "InsBenefitRatio": entry.get("InsBenefitRatio"),
                    "PriceId": entry.get("PriceId"),
                    "QmsNo": entry.get("QmsNo"),
                    "TicketId": entry.get("TicketId"),
                    "MedRcdNo": entry.get("MedRcdNo"),
                    "LastDxOn": entry.get("LastDxOn"),
                    "CreateByWardUnitId": entry.get("CreateByWardUnitId"),
                    "Service": entry.get("Service"),
                    "LabExams": entry.get("LabExams"),
                    "CreatedBy": entry.get("CreatedBy"),
                    "ContentHash": entry.get("ContentHash"),
                    "IsPassOnWarning": entry.get("isPassOnWarning")
                },
                "FullPatientCode": information_data.get("FullPatientCode"),
                "InsBenefitTypeName": information_data.get("InsBenefitTypeName"),
                "WardUnitNames": information_data.get("WardUnitNames"),
                "CreateByStaffName": information_data.get("CreateByStaffName"),
                "ContentHash": information_data.get("ContentHash"),
                "LastUpdateByStaffName": information_data.get("LastUpdateByStaffName"),
                "ModifiedOn": information_data.get("ModifiedOn")
            },
            "ServiceName": information_data.get("ServiceName"),
            "LabExamItems": [
                {
                    "ExItemId": lab_exam_item.get("ExItemId"),
                    "LabExId": lab_exam_item.get("LabExId"),
                    "MedServiceId": lab_exam_item.get("MedServiceId"),
                    "PriceId": lab_exam_item.get("PriceId"),
                    "InsBenefitType": lab_exam_item.get("InsBenefitType"),
                    "InsBenefitRatio": lab_exam_item.get("InsBenefitRatio"),
                    "InsCardId": lab_exam_item.get("InsCardId"),
                    "Qty": lab_exam_item.get("Qty"),
                    "Price": lab_exam_item.get("Price"),
                    "InsPrice": lab_exam_item.get("InsPrice"),
                    "InsPriceRatio": lab_exam_item.get("InsPriceRatio"),
                    "Amt": lab_exam_item.get("Amt"),
                    "EqptCode": lab_exam_item.get("EqptCode"),
                    "Attribute": lab_exam_item.get("Attribute"),
                    "ByProviderId": lab_exam_item.get("ByProviderId"),
                    "Status": lab_exam_item.get("Status"),
                    "DiscAmtSeq": lab_exam_item.get("DiscAmtSeq"),
                    "MedServiceTypeL0": lab_exam_item.get("MedServiceTypeL0"),
                    "MedServiceTypeL2": lab_exam_item.get("MedServiceTypeL2"),
                    "MedServiceTypeL3": lab_exam_item.get("MedServiceTypeL3"),
                    "NonSubclinical": lab_exam_item.get("NonSubclinical"),
                    "TypeL0Code": lab_exam_item.get("TypeL0Code"),
                    "ByProviderCode": lab_exam_item.get("ByProviderCode"),
                    "ByProviderName": lab_exam_item.get("ByProviderName"),
                    "ServiceGroupName": lab_exam_item.get("ServiceGroupName"),
                    "ServiceTypeL3Name": lab_exam_item.get("ServiceTypeL3Name"),
                    "ServiceCode": lab_exam_item.get("ServiceCode"),
                    "ServiceName": lab_exam_item.get("ServiceName"),
                    "InsBenefitTypeName": lab_exam_item.get("InsBenefitTypeName"),
                    "ReqDate": lab_exam_item.get("ReqDate"),
                    "AttrString": lab_exam_item.get("AttrString"),
                    "PaidAttrString": lab_exam_item.get("PaidAttrString"),
                    "ServiceTypeOrderIndex": lab_exam_item.get("ServiceTypeOrderIndex"),
                    "MedItemType": lab_exam_item.get("MedItemType"),
                    "MedItem": lab_exam_item.get("MedItem"),
                    "Checked": lab_exam_item.get("Checked"),
                    "OnDate": lab_exam_item.get("OnDate"),
                    "TotalInvoiceAmtRound": lab_exam_item.get("TotalInvoiceAmtRound"),
                    "TotalReceiptAmtRound": lab_exam_item.get("TotalReceiptAmtRound"),
                    "PtAmt": lab_exam_item.get("PtAmt"),
                    "PtAmtRound": lab_exam_item.get("PtAmtRound"),
                    "PtAmtPaid": lab_exam_item.get("PtAmtPaid"),
                    "PtCoPayAmt": lab_exam_item.get("PtCoPayAmt"),
                    "PtCoPayAmtRound": lab_exam_item.get("PtCoPayAmtRound"),
                    "InsAmt": lab_exam_item.get("InsAmt"),
                    "InsAmtRound": lab_exam_item.get("InsAmtRound"),
                    "DiscAmt": lab_exam_item.get("DiscAmt"),
                    "ReqBy": lab_exam_item.get("ReqBy")
                }
            ],
            "ItemI0": {
                "ExItemId": itemI0.get("ExItemId"),
                "LabExId": itemI0.get("LabExId"),
                "MedServiceId": itemI0.get("MedServiceId"),
                "PriceId": itemI0.get("PriceId"),
                "InsBenefitType": itemI0.get("InsBenefitType"),
                "InsBenefitRatio": itemI0.get("InsBenefitRatio"),
                "InsCardId": itemI0.get("InsCardId"),
                "Qty": itemI0.get("Qty"),
                "Price": itemI0.get("Price"),
                "InsPrice": itemI0.get("InsPrice"),
                "InsPriceRatio": itemI0.get("InsPriceRatio"),
                "Amt": itemI0.get("Amt"),
                "EqptCode": itemI0.get("EqptCode"),
                "Attribute": itemI0.get("Attribute"),
                "ByProviderId": itemI0.get("ByProviderId"),
                "Status": itemI0.get("Status"),
                "DiscAmtSeq": itemI0.get("DiscAmtSeq"),
                "MedServiceTypeL0": itemI0.get("MedServiceTypeL0"),
                "MedServiceTypeL2": itemI0.get("MedServiceTypeL2"),
                "MedServiceTypeL3": itemI0.get("MedServiceTypeL3"),
                "NonSubclinical": itemI0.get("NonSubclinical"),
                "TypeL0Code": itemI0.get("TypeL0Code"),
                "ByProviderCode": itemI0.get("ByProviderCode"),
                "ByProviderName": itemI0.get("ByProviderName"),
                "ServiceGroupName": itemI0.get("ServiceGroupName"),
                "ServiceTypeL3Name": itemI0.get("ServiceTypeL3Name"),
                "ServiceCode": itemI0.get("ServiceCode"),
                "ServiceName": itemI0.get("ServiceName"),
                "InsBenefitTypeName": itemI0.get("InsBenefitTypeName"),
                "ReqDate": itemI0.get("ReqDate"),
                "AttrString": itemI0.get("AttrString"),
                "PaidAttrString": itemI0.get("PaidAttrString"),
                "ServiceTypeOrderIndex": itemI0.get("ServiceTypeOrderIndex"),
                "MedItemType": itemI0.get("MedItemType"),
                "MedItem": itemI0.get("MedItem"),
                "Checked": itemI0.get("Checked"),
                "OnDate": itemI0.get("OnDate"),
                "TotalInvoiceAmtRound": itemI0.get("TotalInvoiceAmtRound"),
                "TotalReceiptAmtRound": itemI0.get("TotalReceiptAmtRound"),
                "PtAmt": itemI0.get("PtAmt"),
                "PtAmtRound": itemI0.get("PtAmtRound"),
                "PtAmtPaid": itemI0.get("PtAmtPaid"),
                "PtCoPayAmt": itemI0.get("PtCoPayAmt"),
                "PtCoPayAmtRound": itemI0.get("PtCoPayAmtRound"),
                "InsAmt": itemI0.get("InsAmt"),
                "InsAmtRound": itemI0.get("InsAmtRound"),
                "DiscAmt": itemI0.get("DiscAmt"),
                "ReqBy": itemI0.get("ReqBy")
            },
            "FullAddress": information_data.get("FullAddress")
        }

    return confirmed_data, confirmed_data["PatientId"]

def update_CLS_patient_from_excel(row):
    from Cận_lâm_sàng.GET import choose_patient_to_start, frVisitEntryIdManager, load_report
    from Cận_lâm_sàng.POST import create_bill, create_information_patient, create_loadTxVisitIds
    # Load danh sách frVisitEntryIds và all_datas
    frVisitEntryIdManager()
    entry_ids = choose_patient_to_start()
    print("entry_ids:", entry_ids)
    if len(entry_ids) == 0:
        print("No entry_ids.")
        return
    for entry_id in entry_ids:
        create_bill()
        create_information_patient()
        create_loadTxVisitIds(entry_id)
        information_data = prepare_information_data(row, entry_id, frVisitEntryIdManager())
        update_CLS_patient(information_data)
        confirmed_data, patientId = prepare_confirmed_information_data(row, information_data)
        confirmed_CLS_patient(confirmed_data)
        load_report(patientId)


