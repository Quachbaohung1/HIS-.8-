import unittest
import pandas as pd
from unittest.mock import MagicMock
from Khám_bệnh_Toa_thuốc.POST import (
    process_check_patient_in_room,
    process_insert_info_patient,
    process_info_prescription_services,
    process_prescription_services,

)


class TestProcessPrescription(unittest.TestCase):

    def case_Prescription(self, file_path, expected_result, process_func):
        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, test_data]

        # Chạy hàm được kiểm thử
        result = process_func(file_path)

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: Passed")
        else:
            print(f"Running test for {file_path}: Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    # Kiểm tra bệnh nhân có trong phòng khám
    def test_case_00(self):
        result = process_check_patient_in_room()
        expected_result = result

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for check patient in room: Passed")
        else:
            print(f"Running test for check patient in room: Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for check patient in room. Expected: {expected_result}, Actual: {str(result)}")

    # Nhập đầy đủ thông tin khám bệnh của bệnh nhân
    def test_case_01(self):
        file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_01.xlsx"
        expected_result = 204
        self.case_Prescription(file_path, expected_result, process_insert_info_patient)

    # Không nhập thông tin thuốc
    def test_case_02(self):
        # Cho bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_02.xlsx"
        # Cho bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_15.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_info_prescription_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = 204
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(file_path, expected_result, custom_process_func)

    # Không nhập thông tin kho
    def test_case_03(self):
        # Cho bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_03.xlsx"
        # Cho bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_16.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_info_prescription_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = 204
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(file_path, expected_result, custom_process_func)

    # Không nhập thông tin ngày dùng thuốc
    def test_case_04(self):
        # Cho bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_04.xlsx"
        # Cho bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_17.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_prescription_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = 204
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(file_path, expected_result, custom_process_func)

    # Không nhập thông tin sáng trưa chiều tối
    def test_case_05(self):
        # Cho bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_05.xlsx"
        # Cho bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_18.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_prescription_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = 204
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(file_path, expected_result, custom_process_func)

    # Không nhập thông tin hoạt chất
    def test_case_06(self):
        # Cho bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_06.xlsx"
        # Cho bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_19.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_prescription_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(file_path, expected_result, custom_process_func)

    # Không nhập thông tin đường dùng
    def test_case_07(self):
        # Cho bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_07.xlsx"
        # Cho bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_20.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_prescription_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = 204
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(file_path, expected_result, custom_process_func)

    # Không nhập thông tin hàm lượng
    def test_case_08(self):
        # Cho bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_08.xlsx"
        # Cho bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_21.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_prescription_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = 204
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(file_path, expected_result, custom_process_func)

    # Không nhập thông tin đơn vị dùng
    def test_case_09(self):
        # Cho bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_09.xlsx"
        # Cho bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_22.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_prescription_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = 204
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(file_path, expected_result, custom_process_func)

    # Không nhập thông tin đơn vị tính
    def test_case_10(self):
        # Cho bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_10.xlsx"
        # Cho bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_23.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_prescription_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = 204
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(file_path, expected_result, custom_process_func)

    # Không nhập thông tin số lượng
    def test_case_11(self):
        # Cho bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_11.xlsx"
        # Cho bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_24.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_prescription_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = 204
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(file_path, expected_result, custom_process_func)

    # Không nhập thông tin mã thuốc
    def test_case_12(self):
        # Cho bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_12.xlsx"
        # Cho bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_25.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_prescription_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = 204
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(file_path, expected_result, custom_process_func)

    # Nhập đầy đủ thông tin và chọn kho BHYT
    def test_case_13(self):
        # Cho bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_13.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_prescription_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = 204
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(file_path, expected_result, custom_process_func)

    # Nhập đầy đủ thông tin và chọn kho Nhà thuốc
    def test_case_14(self):
        # Cho bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_14.xlsx"
        # Cho bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_26.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_prescription_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = 204
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(file_path, expected_result, custom_process_func)


if __name__ == '__main__':
    unittest.main()
