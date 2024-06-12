import logging
import unittest
import pandas as pd
from unittest.mock import MagicMock
from Tiếp_nhận.POST import (
    process_create_patient_from_excel,
    process_create_insurance_from_excel,
    process_patient_from_excel,
    process_generate_patient_from_excel,
    process_generate_sum_patient_from_excel
)


class CustomTestResult(unittest.TestResult):
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        super().__init__(stream, descriptions, verbosity)
        self.results = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.results.append((test, "Passed"))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.results.append((test, "Failed"))

    def addError(self, test, err):
        super().addError(test, err)
        self.results.append((test, "Error"))

    def get_results(self):
        return self.results

    def get_passed_results(self):
        return [result for result in self.results if result[1] == "Passed"]


class TestProcessPatient(unittest.TestCase):
    # Case nhập trùng họ tên với bệnh nhân cũ đã tiếp nhận trước đó trong cùng ngày
    def test_case_01(self):
        # bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_01.xlsx"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_13.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lầm 1)
        result_1 = process_create_patient_from_excel(file_path)
        expected_result_1 = result_1

        # Kiểm tra kết quả và in ra kết quả tương ứng (lần 1)
        if result_1 == expected_result_1:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result_1, expected_result_1,
                         f"Failed for {file_path}. Expected: {expected_result_1}, Actual: {str(result_1)}")

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lầm 2)
        result_2 = process_create_patient_from_excel(file_path)
        expected_result_2 = None

        # Kiểm tra kết quả và in ra kết quả tương ứng (lần 1)
        if result_2 == expected_result_2:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result_2, expected_result_2,
                         f"Failed for {file_path}. Expected: {expected_result_2}, Actual: {str(result_2)}")

    # Case nhập trùng số thẻ BHYT với bệnh nhân cũ
    def test_case_02(self):
        # bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_02.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lần 1)
        result_1 = process_create_insurance_from_excel(file_path)
        expected_result_1 = None

        # Kiểm tra kết quả và in ra kết quả tương ứng (lần 1)
        if result_1 == expected_result_1:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result_1, expected_result_1,
                         f"Failed for {file_path}. Expected: {expected_result_1}, Actual: {str(result_1)}")

    # Case nhập trùng số CCCD với bệnh nhân cũ
    def test_case_03(self):
        # bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_03.xlsx"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_14.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lần 1)
        result_1 = process_create_patient_from_excel(file_path)
        expected_result_1 = result_1

        # Kiểm tra kết quả và in ra kết quả tương ứng (lần 1)
        if result_1 == expected_result_1:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result_1, expected_result_1,
                         f"Failed for {file_path}. Expected: {expected_result_1}, Actual: {str(result_1)}")

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lần 2)
        result_2 = process_create_patient_from_excel(file_path)
        expected_result_2 = None

        # Kiểm tra kết quả và in ra kết quả tương ứng (lần 2)
        if result_2 == expected_result_2:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result_2, expected_result_2,
                         f"Failed for {file_path}. Expected: {expected_result_2}, Actual: {str(result_2)}")

    # Case không nhập họ tên
    def test_case_04(self):
        # bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_04.xlsx"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_15.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_create_patient_from_excel(file_path)
        expected_result = None

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    # Case không nhập ngày sinh
    def test_case_05(self):
        # bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_05.xlsx"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_16.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_create_patient_from_excel(file_path)
        expected_result = None

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    # Case không nhập địa chỉ
    def test_case_06(self):
        # bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_06.xlsx"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_17.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_create_patient_from_excel(file_path)
        expected_result = None

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    # Case không nhập thông tin phòng khám
    def test_case_07(self):
        # bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_07.xlsx"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_18.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_patient_from_excel(file_path)
        expected_result = [None]

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    # Case không nhập thông tin BHYT
    def test_case_08(self):
        # bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_08.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_create_insurance_from_excel(file_path)
        expected_result = None

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    # Case có nhập thông tin phòng khám nhưng không nhập thông tin dịch vụ khám
    def test_case_09(self):
        # bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_09.xlsx"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_19.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_patient_from_excel(file_path)
        expected_result = [None]

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    # Case nhập đầy đủ thông tin
    def test_case_10(self):
        # bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_10.xlsx"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_20.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_patient_from_excel(file_path)
        expected_result = result

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    # Case tạo thông tin bệnh nhân thành công
    def test_case_11(self):
        # bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_11.xlsx"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_21.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_create_patient_from_excel(file_path)
        expected_result = result

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    # Case tạo thông BHYT thành công
    def test_case_12(self):
        # bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_12.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_create_insurance_from_excel(file_path)
        expected_result = result

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    # Case tiếp nhận tự động từng loại bệnh nhân
    def test_case_13(self):
        # bệnh nhân BHYT
        file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_22.xlsx"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_23.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_generate_patient_from_excel(file_path)
        expected_result = result

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    # Case tiếp nhận thành công bệnh nhân BHYT + Thu phí (chạy tự động)
    def test_case_14(self):
        # bệnh nhân BHYT + Thu phí
        file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_24.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_generate_sum_patient_from_excel(file_path)
        expected_result = result

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")


def main():
    logging.basicConfig(filename='E:/HIS api automation/Result/TestResult_Tiếp_nhận.log', level=logging.INFO)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestProcessPatient)
    custom_result = CustomTestResult()
    suite.run(custom_result)

    successes = custom_result.testsRun - len(custom_result.failures) - len(custom_result.errors)
    with open("E:/HIS api automation/Result/TestResult_Tiếp_nhận.txt", "w", encoding="utf-8") as file:
        file.write("=== Test Report ===\n")
        file.write(f"Total tests run: {custom_result.testsRun}\n")
        file.write(f"Successes: {successes}\n")
        file.write(f"Failures: {len(custom_result.failures)}\n")
        file.write(f"Errors: {len(custom_result.errors)}\n")

        if successes > 0:
            file.write("\n=== Successes ===\n")
            for test, _ in custom_result.get_passed_results():
                file.write(f"{test}: Passed\n")

        if custom_result.failures:
            file.write("\n=== Failures ===\n")
            for test, fail_msg in custom_result.failures:
                file.write(f"{test}: {fail_msg}\n")

        if custom_result.errors:
            file.write("\n=== Errors ===\n")
            for test, err_msg in custom_result.errors:
                file.write(f"{test}: {err_msg}\n")

    logging.info("Test report generated.")


if __name__ == '__main__':
    main()
