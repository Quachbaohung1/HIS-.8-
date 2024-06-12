import datetime
import requests
import json
from Cấu_hình.Setup import base_url_2, auth_token_2


# Lấy ngày tháng từ hàm GET ở file Tiếp nhận
def date_formatted():
    from Tiếp_nhận.GET import CurrentServerDateTime
    date = str(CurrentServerDateTime())
    date_value_trimmed = date[:20] + "+" + date[-6:]
    isit_on_value_trimmed = date_value_trimmed.replace('"', '')

    date_datetime = datetime.datetime.strptime(isit_on_value_trimmed, "%Y-%m-%dT%H:%M:%S%z")
    date_fomatted = date_datetime.strftime("%Y%m%d")
    print("Formated_visit_on: ", date_fomatted)
    return date_fomatted


# Kiểm tra danh sách bệnh nhân ở Phòng khám
def check_patient_in_room():
    print("Hàm check_patient_in_room được gọi")
    date = date_formatted()
    url = f"{base_url_2}/Visits/VisitFullEntries/149?fromDate={date}&TxEntryStatus=1&ExcludedVisitAttr=Empty"
    headers = {"Authorization": auth_token_2}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return []
    patient_ids = []
    if isinstance(response_data, list):
        for item in response_data:
            patient_id = item.get("patientId")
            if patient_id is not None:
                patient_ids.append(patient_id)
                print(patient_id)
    elif isinstance(response_data, dict):
        patient_id = response_data.get("patientId")
        if patient_id is not None:
            patient_ids.append(patient_id)
            print(patient_id)
    else:
        print("Invalid response format")

    print("patient_ids", patient_ids)
    return patient_ids


# Hiển thị entry_visit
def check_visit_enty(entry_id):
    try:
        url = f"{base_url_2}/VisitEntries/{entry_id}"
        headers = {"Authorization": auth_token_2}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        visit_id = response.json()["visitId"]
        print(f"\nvisit_id for entry_id {entry_id}: {visit_id}")
        return [visit_id]
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return []


# Lấy thông tin bệnh nhân GetDeleted
def check_information_patient_initial(entry_id):
    visit_ids = check_visit_enty(entry_id)
    visit_idas = []
    for visit_id in visit_ids:
        url = f"{base_url_2}/Visits/Id/{visit_id}?isGetDeleted=False"
        headers = {"Authorization": auth_token_2}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            visit_json = response.json()
            visit_id = visit_json["visitId"]
            insBenefitType = int(visit_json.get("insBenefitType", 0))
            if insBenefitType != 2:
                print(f"Visit with visit_id {visit_id} does not have insBenefitType equal to 2.")
                continue
            visit_idas.append(visit_id)
        except requests.RequestException as e:
            print(f"Request failed: {e}")
    print("visit_ids", visit_idas)
    return visit_idas


def check_information_patient_subsequent(all_info):
    visit_info_list = []  # Khởi tạo danh sách để lưu thông tin các lượt thăm
    visitIds = get_visit_ids(all_info)
    if visitIds:
        # Duyệt qua các visit_id trong danh sách thông tin
        for visit_id in visitIds:
            url = f"{base_url_2}/Visits/Id/{visit_id}?isGetDeleted=False"
            headers = {"Authorization": auth_token_2}

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                response_json = response.json()
                print("response_json: ", response_json)

                # Kiểm tra xem response_json có phải là một danh sách JSON hay không
                visit_items = response_json if isinstance(response_json, list) else [response_json]

                for item in visit_items:
                    visit_info = {
                        "visitId": int(item.get("visitId", 0)),
                        "patient_id": int(item.get("patientId", 0)),
                        "insBenefitType": int(item.get("insBenefitType", 0)),
                        "insBenefitRatio": int(item.get("insBenefitRatio", 0)),
                        "insCardId": int(item.get("insCardId", 0)) if item.get("insCardId") else None
                    }
                    visit_info_list.append(visit_info)  # Thêm thông tin vào danh sách
                    print("visit_info_dict:", visit_info_list)

            except requests.RequestException as e:
                print(f"Request failed: {e}")
    else:
        print("Danh sách visitIds rỗng.")

    # Trả về danh sách thông tin các lượt thăm dưới dạng JSON
    return visit_info_list


# Lấy thông tin bệnh nhân để update
def get_all_info(entry_id):
    all_info = []
    visit_idas = check_information_patient_initial(entry_id)

    for visit_id in visit_idas:
        url = f"{base_url_2}/VisitEntries/VisitId/{visit_id}"
        headers = {"Authorization": auth_token_2}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()

            all_info.extend(
                {
                    "entryId": int(item.get("entryId")),
                    "visitId": int(item.get("visitId")),
                    "medServiceId": int(item.get("medServiceId")),
                    "wardUnitId": int(item.get("wardUnitId")),
                    "createOn": item.get("createOn"),
                    "createById": int(item.get("createById")),
                    "status": int(item.get("status")),
                    "insBenefitType": int(item.get("insBenefitType", 0)),
                    "insBenefitRatio": int(item.get("insBenefitRatio", 0)),
                    "priceId": int(item.get("priceId")),
                    "qmsNo": item.get("qmsNo"),
                    "ticketId": int(item.get("ticketId")),
                    "createByWardUnitId": int(item.get("createByWardUnitId")),
                    "dxByStaffId": item.get("dxByStaffId"),
                    "dxICD": item.get("dxICD"),
                    "dxText": item.get("dxText"),
                    "patient_id": int(item.get("patientId", 0)),
                    "insCardId": int(item.get("insCardId", 0))
                }
                for item in response_json
            )

        except requests.RequestException as e:
            print(f"Lỗi khi thực hiện yêu cầu: {e}")

    print("all_info:", all_info)
    return all_info


def get_visit_ids(all_info):
    for info in all_info:
        visit_id = info.get("visitId")
        url = f"{base_url_2}/Visits/Id/{visit_id}?isGetDeleted=False"
        headers = {"Authorization": auth_token_2}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()

            all_info.extend([
                {
                    "entryId": int(item.get("entryId")),
                    "visitId": int(item.get("visitId")),
                    "medServiceId": int(item.get("medServiceId")),
                    "wardUnitId": int(item.get("wardUnitId")),
                    "createOn": item.get("createOn"),
                    "createById": int(item.get("createById")),
                    "status": int(item.get("status")),
                    "insBenefitType": int(item.get("insBenefitType", 0)),
                    "insBenefitRatio": int(item.get("insBenefitRatio", 0)),
                    "priceId": int(item.get("priceId")),
                    "qmsNo": item.get("qmsNo"),
                    "ticketId": int(item.get("ticketId")),
                    "createByWardUnitId": int(item.get("createByWardUnitId")),
                    "dxByStaffId": item.get("dxByStaffId"),
                    "dxICD": item.get("dxICD"),
                    "dxText": item.get("dxText"),
                    "patient_id": int(item.get("patientId", 0)),
                    "insCardId": int(item.get("insCardId", 0))
                }
                for item in response_json
            ])

        except requests.RequestException as e:
            print(f"Lỗi khi thực hiện yêu cầu: {e}")

    print("all_info:", all_info)
    return all_info
