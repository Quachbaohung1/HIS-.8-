import datetime
import sys
import requests
import json

# Base url
base_url = "http://115.79.31.186:1096"
# Auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjM4MzkiLCJyb2xlIjoiQWRtaW4iLCJBY2NvdW50TmFtZSI6Imh1bmdxYiIsIkNsaWVudElwQWRkcmVzcyI6Ijo6MSIsIklzTG9jYWxJcCI6IlRydWUiLCJuYmYiOjE3MTUxODQ2NDIsImV4cCI6MTcxNTE4ODI0MiwiaWF0IjoxNzE1MTg0NjQyfQ.CihuC246iqFUos4MNZtNWs2q_SBOtmbXz4NRNuRQ4rg"


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


# Lấy thông tin BN có CLS
def get_info_patient():
    print("Hàm check_patient_in_room được gọi")
    date = date_formatted()
    url = f"{base_url}/cis/LabExams/?fromDate={date}&toDate={date}&refNo=&patientCode=&patientName=&wardUnitId=&attribute=0&labExStatus=1&byProviderId=552&labExItemAttr=2&excludedLabExAttr=4&medRcdId=&qmsNo=&fromApproveDate=&toApproveDate=&fromLabDxOn=&toLabDxOn=&isLoadMissEntries=False&isStateForLab=False&isLoadItem=False"
    headers = {"Authorization": auth_token}

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

    labEx_ids_and_patient_ids = []

    if isinstance(response_data, list):
        for item in response_data:
            labEx_id = item.get("labExId")
            patient_id = item.get("patientId")
            if labEx_id is not None and patient_id is not None:
                labEx_ids_and_patient_ids.append({"labExId": labEx_id, "patientId": patient_id})
                print(f"labEx_id: {labEx_id}, patient_id: {patient_id}")
    elif isinstance(response_data, dict):
        labEx_id = response_data.get("labExId")
        patient_id = response_data.get("patientId")
        if labEx_id is not None and patient_id is not None:
            labEx_ids_and_patient_ids.append({"labExId": labEx_id, "patientId": patient_id})
            print(f"labEx_id: {labEx_id}, patient_id: {patient_id}")
    else:
        print("Invalid response format")

    print("labEx_ids_and_patient_ids:", labEx_ids_and_patient_ids)
    return labEx_ids_and_patient_ids


class frVisitEntryIdManager:
    def __init__(self):
        self.frVisitEntryIds = []
        self.all_datas = []
        self.current_index = 0
        self.current_index_data = 0

    def load_frVisitEntryIds_all_datas(self):
        from Khám_bệnh_CDDV.POST import process_kb_CDDV
        self.frVisitEntryIds, self.all_datas = process_kb_CDDV()
        self.current_index = 0  # Reset chỉ số
        self.current_index_data = 0  # Reset chỉ số
        print(f"Loaded frVisitEntryIds: {self.frVisitEntryIds}")
        print(f"Loaded all_datas: {self.all_datas}")

    def get_next_frVisitEntryId(self):
        if self.current_index >= len(self.frVisitEntryIds):
            print("No more frVisitEntryIds available.")
            sys.exit()

        frVisitEntryId = self.frVisitEntryIds[self.current_index]
        self.current_index += 1
        print(f"Returning frVisitEntryId: {frVisitEntryId}, current_index: {self.current_index}")
        return frVisitEntryId

    def get_next_all_data(self):
        if self.current_index_data >= len(self.all_datas):
            print("No more all_datas available.")
            sys.exit()

        all_data = self.all_datas[self.current_index_data]
        self.current_index_data += 1
        print(f"Returning all_data: {all_data}, current_index_data: {self.current_index_data}")
        return all_data


# Tạo instance của EntryIdManager và load danh sách entry_ids
entry_id_manager = frVisitEntryIdManager()
entry_id_manager.load_frVisitEntryIds_all_datas()


# Chọn BN để trả CLS
def choose_patient_to_start():
    count = 0  # Biến đếm số lần đã chạy
    entry_ids = []  # Danh sách entryIds sẽ được trả về
    while count < 2:  # Chỉ chạy 2 lần
        frVisitEntryId = entry_id_manager.get_next_frVisitEntryId()
        if frVisitEntryId is None:
            print("All frVisitEntryIds have been processed.")
            return []

        try:
            url = f"{base_url}/pms/Visits/EntryId/{frVisitEntryId[0]}"
            headers = {"Authorization": auth_token}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            # Kiểm tra xem "entry" có tồn tại trong response_data hay không
            if "entry" in response_data:
                entry = response_data["entry"]
                # Kiểm tra xem "entryId" có tồn tại trong "entry" hay không
                if "entryId" in entry:
                    entryId = entry["entryId"]
                    entry_ids.append(entryId)  # Thêm entryId vào danh sách entryIds
                    print(f"entryId for frVisitEntryId {frVisitEntryId}: {entryId}")
                    count += 1  # Tăng biến đếm sau mỗi lần chạy
                else:
                    print(f"Không tìm thấy entryId trong entry cho frVisitEntryId {frVisitEntryId}")
            else:
                print(f"Không tìm thấy entry cho frVisitEntryId {frVisitEntryId}")
            return entry_ids
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            return []
    else:
        print("Stopped after 2 runs.")


# Lấy thông tin BN lần 1
def get_information_patient(entry_ids):
    entryids = []

    url = f"{base_url}/pms/Visits/EntryId/{entry_ids}"
    headers = {"Authorization": auth_token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    print("response_data:", response_data)
    if "entry" in response_data:
        entry = response_data["entry"]
        # Kiểm tra xem "entryId" có tồn tại trong "entry" hay không
        if "entryId" in entry:
            entryId = entry["entryId"]
            entryids.append(entryId)  # Thêm entryId vào danh sách entryIds
        else:
            print(f"Không tìm thấy entryId")
    else:
        print(f"Không tìm thấy entry")

    return entryids


# Lấy thông tin BN lần 2
def get_information_patient_next(entry_ids):
    count = 0  # Biến đếm số lần đã chạy
    all_data_info_patient = []  # Danh sách entryIds sẽ được trả về
    while count < 2:  # Chỉ chạy 2 lần
        all_data_list = entry_id_manager.get_next_all_data()
        if all_data_list is None:
            print("All all_data have been processed.")
            return []

        for all_data in all_data_list:
            if not isinstance(all_data, dict):
                print("Expected each item in all_data to be a dictionary.")
                continue  # Bỏ qua phần tử không hợp lệ và tiếp tục

            try:
                url = f"{base_url}/pms/Visits/EntryId/{entry_ids}"
                headers = {"Authorization": auth_token}
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                response_data = response.json()
                print("response_data_entry_ids:", response_data)

                # Đảm bảo response_data là dictionary
                if isinstance(response_data, list) and len(response_data) == 1:
                    response_data = response_data[0]
                elif not isinstance(response_data, dict):
                    print("Expected response_data to be a dictionary or a list with a single dictionary element.")
                    return []

                # Chuyển all_data thành dictionary nếu cần thiết
                if not isinstance(all_data, dict):
                    try:
                        all_data = dict(all_data)
                    except (ValueError, TypeError):
                        print("Expected all_data to be convertible to a dictionary.")
                        return []

                # Merge dữ liệu từ all_data và response_data
                merged_data = all_data.copy()
                merged_data.update(response_data)

                # Kiểm tra nếu "attribute" không tồn tại trong response_data
                if "attribute" in response_data:
                    # Sử dụng giá trị của "attribute" từ all_data
                    merged_data["attribute"] = all_data.get("attribute")

                all_data_info_patient.append(merged_data)
                print("all_data_info_patient:", all_data_info_patient)
                count += 1  # Cập nhật biến đếm
                return all_data_info_patient
            except requests.RequestException as e:
                print(f"Request failed: {e}")
                return []
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
                return []
        else:
            print("Stopped after 2 runs.")


def load_report(patientId):
    url = f"{base_url}/cis/LabExams/LoadLabExByPatientId/{patientId}?isLoadEntry=True"
    headers = {"Authorization": auth_token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    print("response_data_report:", response_data)
    return response_data
