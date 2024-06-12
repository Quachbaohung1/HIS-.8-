import logging
import unittest
import pandas as pd
from unittest.mock import MagicMock
from Khám_bệnh_CDDV.POST import (
    process_check_patient_in_room,
    process_insert_info_patient,
    process_examination_services,

)


class TestProcessExamination(unittest.TestCase):

    def case_Examination(self, file_path, expected_result, process_func):
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
        file_path = "E://HIS api automation/DataTest/Khám bệnh - CDDV/TC_01.xlsx"
        expected_result = 204
        self.case_Examination(file_path, expected_result, process_insert_info_patient)

    # Không nhập dịch vụ
    def test_case_02(self):
        file_path = "E://HIS api automation/DataTest/Khám bệnh - CDDV/TC_02.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_examination_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(file_path, expected_result, custom_process_func)

    # Không nhập bác sĩ
    def test_case_03(self):
        file_path = "E://HIS api automation/DataTest/Khám bệnh - CDDV/TC_03.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_examination_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(file_path, expected_result, custom_process_func)

    # Không nhập số lượng
    def test_case_04(self):
        file_path = "E://HIS api automation/DataTest/Khám bệnh - CDDV/TC_04.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_examination_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(file_path, expected_result, custom_process_func)

    # Nhập đầy đủ thông tin chỉ định dịch vụ thành công
    def test_case_05(self):
        file_path = "E://HIS api automation/DataTest/Khám bệnh - CDDV/TC_05.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_examination_services(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(file_path, expected_result, custom_process_func)


if __name__ == '__main__':
    unittest.main()
