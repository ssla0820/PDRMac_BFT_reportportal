import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import time, inspect, datetime, pytest, re, configparser

os.chdir(os.path.dirname(__file__))
from types import SimpleNamespace

from ATFramework import MyReport, logger
from ATFramework.drivers.driver_factory import DriverFactory
from pages.page_factory import PageFactory
from configs.app_config import *
from pages.locator import locator as L
from globals import *

# read PDR cap >>
app = SimpleNamespace(**PDR_cap)
# read PDR cap <<

# create driver & page >>
mwc = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mwc)
download_from_cl_dz_page = PageFactory().get_page_object('download_from_cl_dz_page', mwc)
upload_cloud_dz_page = PageFactory().get_page_object('upload_cloud_dz_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Download, Upload & Pack project to Cloud.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Download_Upload_&_Pack_Project_To_Cloud/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Download_Upload_&_Pack_Project_To_Cloud/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1


class Test_Download_Upload_Pack_Project_To_Cloud():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME * 3)
        yield mwc
        main_page.close_app()
        main_page.clear_cache()

    @classmethod
    def setup_class(cls):
        main_page.clear_cache()
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('Download_Upload_&_Pack_Project_To_Cloud')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"download/upload/pack project2cloud result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number,
                                                     report.get_ovinfo('na'),
                                                     report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        with uuid('c6e583bf-da3f-4424-a6bb-ffa77fac0896') as case:
            # 2. Upload Project to CyberLink Cloud...
            # 2.1 Enter project name dialog
            # 2.1.1. Input column > Unsaved project
            # Show "New Untitled Project
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.top_menu_bar_file_upload_project_to_cyberlink_cloud()
            time.sleep(DELAY_TIME)
            current_name = download_from_cl_dz_page.upload_project.get_project_name()
            case.result = False if not current_name == 'New Untitled Project' else True

        with uuid('31078a31-0cb8-4395-bc22-c4a2b2fc3760') as case:
            # 2.1 Enter project name dialog
            # 2.1.2. Input > Long file name
            # Input 142 chars limit and upload successfully
            download_from_cl_dz_page.upload_project.set_project_name(
                '1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
                '1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
                '123456789012345678901234567890123456789012345678901')
            # download_from_cl_dz_page.exist_click(L.download_from_cl_dz.upload_project.project_name)
            # download_from_cl_dz_page.input_text('a')
            current_name_length = len(download_from_cl_dz_page.upload_project.get_project_name())
            check_result_1 = False if not current_name_length == 251 else True

            download_from_cl_dz_page.upload_project.click_ok()
            project_is_existed = download_from_cl_dz_page.is_exist(L.download_from_cl_dz.upload_project.warning_msg.ok,timeout=30)
            if project_is_existed:
                download_from_cl_dz_page.upload_project.handle_warning_msg()

            check_result_2 = download_from_cl_dz_page.is_exist(
                L.download_from_cl_dz.upload_project.uploaded.link, timeout=30)

            case.result = check_result_1 and check_result_2

        with uuid('a9d666b1-4d95-4138-b997-65c767e1d8e5') as case:
            # 2.2. Final dialog
            # 2.2.2. Upload successfully > CL Cloud link
            # link to CL Cloud page
            case.result = download_from_cl_dz_page.upload_project.uploaded.click_link()

        with uuid('6ad29897-cba2-4438-a8a8-4a79ab0c9605') as case:
            # 2.2. Final dialog
            # 2.2.2. Upload successfully
            # show upload successfully msg
            image_full_path = Auto_Ground_Truth_Folder + 'DL_UL_project_to_cloud_2_2_2-1.png'
            ground_truth = Ground_Truth_Folder + 'DL_UL_project_to_cloud_2_2_2-1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_dialog, file_name=image_full_path)
            case.result = download_from_cl_dz_page.compare(ground_truth, current_preview)

        with uuid('0956225a-e070-4f26-bac2-70b9d71c405d') as case:
            # 2.2. Final dialog
            # 2.2.3. [OK]
            # Close Upload Project to CyberLink Cloud dialog
            check_result_1 = download_from_cl_dz_page.upload_project.uploaded.click_ok()
            check_result_2 = download_from_cl_dz_page.is_not_exist(L.upload_cloud_dz.upload_dialog)
            case.result = check_result_1 and check_result_2

        with uuid('b601866c-eca1-4695-86ab-8749c63cf5cd') as case:
            # 2.1 Enter project name dialog
            # 2.1.2. Input > Unicode name
            # Input unicode chars and upload successfully
            main_page.top_menu_bar_file_upload_project_to_cyberlink_cloud()
            time.sleep(DELAY_TIME)
            download_from_cl_dz_page.upload_project.set_project_name('許功蓋')
            current_name = download_from_cl_dz_page.upload_project.get_project_name()
            check_result_1 = False if not current_name == '許功蓋' else True

            download_from_cl_dz_page.upload_project.click_ok()
            project_is_existed = download_from_cl_dz_page.is_exist(L.download_from_cl_dz.upload_project.warning_msg.ok)
            if project_is_existed:
                download_from_cl_dz_page.upload_project.handle_warning_msg()

            check_result_2 = download_from_cl_dz_page.is_exist(
                L.download_from_cl_dz.upload_project.uploaded.link, timeout=30)

            case.result = check_result_1 and check_result_2

        with uuid('c497c623-dc87-4980-bde5-be04456842a7') as case:
            # 2.1 Enter project name dialog
            # 2.1.3. [OK]
            # start to upload the project
            case.result = check_result_2

        with uuid('f76f7b78-99e2-428d-8164-988d36bc9071') as case:
            # 2.2. Final dialog
            # 2.2.3. [OK] > Hotkey (Enter)
            # Close Upload Project to CyberLink Cloud dialog
            download_from_cl_dz_page.press_enter_key()
            check_result = download_from_cl_dz_page.is_not_exist(L.upload_cloud_dz.upload_dialog)
            case.result = check_result

        with uuid('941c73a2-d230-4c47-b3ef-56f4a8c0f955') as case:
            # 2.1 Enter project name dialog
            # 2.1.3. [OK] > The project has been uploaded
            # Pop out warning msg
            main_page.top_menu_bar_file_upload_project_to_cyberlink_cloud()
            time.sleep(DELAY_TIME)
            download_from_cl_dz_page.upload_project.set_project_name('許功蓋')
            download_from_cl_dz_page.upload_project.click_ok()

            check_result_1 = download_from_cl_dz_page.is_exist(L.download_from_cl_dz.upload_project.warning_msg.ok)
            check_result_2 = download_from_cl_dz_page.upload_project.handle_warning_msg()
            case.result = check_result_1 and check_result_2

        with uuid('e3a5224e-e9c7-4c8b-949f-b4bbe28f8f44') as case:
            # 2.2. Final dialog
            # 2.2.4. X
            # Close Upload Project to CyberLink Cloud dialog
            time.sleep(DELAY_TIME*3)
            check_result_1 = upload_cloud_dz_page.pack_project.click_Close()
            check_result_2 = download_from_cl_dz_page.is_not_exist(L.upload_cloud_dz.upload_dialog)
            case.result = check_result_1 and check_result_2

        with uuid('44f3e86a-ad82-458a-9302-1206bdb713ed') as case:
            # 2.1 Enter project name dialog
            # 2.1.1. Input column > Saved project
            # Show the saved name
            main_page.top_menu_bar_file_download_project_from_cyberlink_cloud()
            time.sleep(DELAY_TIME * 3)
            download_from_cl_dz_page.download_project.select_project('CloudTestPack')
            download_from_cl_dz_page.tap_download()
            download_from_cl_dz_page.download_project.select_download_folder(Test_Material_Folder + 'cloud_test/')
            time.sleep(30)
            download_from_cl_dz_page.download_project.downloaded.click_open()
            main_page.handle_merge_media_to_current_library_dialog(option='no')
            main_page.left_click()

            main_page.top_menu_bar_file_upload_project_to_cyberlink_cloud()
            time.sleep(DELAY_TIME)
            current_name = download_from_cl_dz_page.upload_project.get_project_name()
            case.result = False if not current_name == 'CloudTestPack' else True
            main_page.delete_folder(Test_Material_Folder + 'cloud_test/CloudTestPack/')

        with uuid('d36292ec-f2d6-4044-9232-255b207bba8c') as case:
            # 2.1 Enter project name dialog
            # 2.1.4. [Cancel]
            # close the dialog
            check_result_1 = download_from_cl_dz_page.upload_project.click_cancel()
            check_result_2 = download_from_cl_dz_page.is_not_exist(L.download_from_cl_dz.upload_project.project_name)
            case.result = check_result_1 and check_result_2

        with uuid('4d0cbbaa-03d9-4f05-afda-c4a9446f42b2') as case:
            # 2.2. Final dialog
            # 2.2.4. X > Hotkey (ESC)
            # Close Upload Project to CyberLink Cloud dialog
            main_page.top_menu_bar_file_upload_project_to_cyberlink_cloud()
            time.sleep(DELAY_TIME)
            download_from_cl_dz_page.upload_project.set_project_name('許功蓋')
            download_from_cl_dz_page.upload_project.click_ok()
            download_from_cl_dz_page.is_exist(L.download_from_cl_dz.upload_project.warning_msg.ok)
            download_from_cl_dz_page.upload_project.handle_warning_msg()

            download_from_cl_dz_page.press_esc_key()
            check_result = download_from_cl_dz_page.is_not_exist(L.upload_cloud_dz.upload_dialog)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid('e4385c2a-b3c6-41a0-972b-4d4f18cc2220') as case:
            # 1.1 General
            # 1.1.4. Caption Name
            # show "Download CyberLink Cloud Project"
            main_page.top_menu_bar_file_download_project_from_cyberlink_cloud()
            time.sleep(DELAY_TIME * 3)
            caption_name = download_from_cl_dz_page.download_project.caption_name()
            case.result = False if not caption_name == 'Download CyberLink Cloud Project' else True

            download_from_cl_dz_page.find(L.download_from_cl_dz.download_project.project_list_item, timeout=10)
            time.sleep(DELAY_TIME)

        with uuid('105f2780-d397-43ad-89f8-c824141788c4') as case:
            # 1.2. Sort
            # 1.2.1. Name > ▼
            # Sort from large to small
            check_result_1 = download_from_cl_dz_page.download_project.sort_by_name(increase=False)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_1-1.png'
            ground_truth = Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_1-1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download_project.sort_header, file_name=image_full_path)
            check_result_2 = download_from_cl_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('37f5d3bf-e0e0-4d53-8e9e-51dde39498d2') as case:
            # 1.2. Sort
            # 1.2.1. Name > ▲
            # Sort from small to large
            check_result_1 = download_from_cl_dz_page.download_project.sort_by_name(increase=True)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_1-2.png'
            ground_truth = Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_1-2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download_project.sort_header, file_name=image_full_path)
            check_result_2 = download_from_cl_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('8c1456da-a6e3-4d80-b7d8-b9063c128413') as case:
            # 1.2. Sort
            # 1.2.2. Date > ▲
            # Sort from small to large
            check_result_1 = download_from_cl_dz_page.download_project.sort_by_date(increase=True)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_2-1.png'
            ground_truth = Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_2-1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download_project.sort_header, file_name=image_full_path)
            check_result_2 = download_from_cl_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('4476179e-6c9c-41e0-ba3f-c62c60fb286b') as case:
            # 1.2. Sort
            # 1.2.2. Date > ▼
            # Sort from large to small
            check_result_1 = download_from_cl_dz_page.download_project.sort_by_date(increase=False)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_2-2.png'
            ground_truth = Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_2-2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download_project.sort_header, file_name=image_full_path)
            check_result_2 = download_from_cl_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('9429c54a-e7f6-498e-a83c-5e347026ca11') as case:
            # 1.2. Sort
            # 1.2.3. Size > ▲
            # Sort from small to large
            check_result_1 = download_from_cl_dz_page.download_project.sort_by_size(increase=True)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_3-1.png'
            ground_truth = Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_3-1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download_project.sort_header, file_name=image_full_path)
            check_result_2 = download_from_cl_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('c8e26d55-400c-4051-bec7-7678d78956bf') as case:
            # 1.2. Sort
            # 1.2.3. Size > ▼
            # Sort from large to small
            check_result_1 = download_from_cl_dz_page.download_project.sort_by_size(increase=False)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_3-2.png'
            ground_truth = Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_3-2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download_project.sort_header, file_name=image_full_path)
            check_result_2 = download_from_cl_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('3419a8f4-4c6b-43f7-b4ee-c1ec78b26368') as case:
            # 1.2. Sort
            # 1.2.4. Type > ▲
            # Sort from small to large
            check_result_1 = download_from_cl_dz_page.download_project.sort_by_type(increase=True)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_4-1.png'
            ground_truth = Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_4-1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download_project.sort_header, file_name=image_full_path)
            check_result_2 = download_from_cl_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('4c728048-6a00-476d-8ac6-2a387fbdd4a5') as case:
            # 1.2. Sort
            # 1.2.4. Type > ▼
            # Sort from large to small
            check_result_1 = download_from_cl_dz_page.download_project.sort_by_type(increase=False)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_4-2.png'
            ground_truth = Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_2_4-2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download_project.sort_header, file_name=image_full_path)
            check_result_2 = download_from_cl_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('4fb2fd89-2685-468b-966a-f1830c305341') as case:
            # 1.3. Delete
            # 1.3.1. Delete button > Warning msg
            # "Are you sure you want to delete the selected project from CL Cloud?"
            download_from_cl_dz_page.download_project.select_project(
                '1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
                '1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
                '123456789012345678901234567890123456789012345678901')
            check_result_1 = download_from_cl_dz_page.download_project.click_delete()
            time.sleep(DELAY_TIME * 2)
            image_full_path = Auto_Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_3_1-1.png'
            ground_truth = Ground_Truth_Folder + 'DL_UL_project_to_cloud_1_3_1-1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download_project.delete_window, file_name=image_full_path)
            check_result_2 = download_from_cl_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('96ac8bf9-459a-468d-9477-eba8d658423e') as case:
            # 1.3. Delete
            # 1.3.1. Delete button
            # Delete selected project
            check_result_1 = download_from_cl_dz_page.download_project.handle_warning_msg()
            time.sleep(DELAY_TIME)
            check_delete_project = download_from_cl_dz_page.download_project.select_project(
                '1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
                '1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
                '123456789012345678901234567890123456789012345678901')
            check_result_2 = True if not check_delete_project else False

            case.result = check_result_1 and check_result_2

        with uuid('1553e61e-a09a-49f2-a9df-f04e044551e5') as case:
            # 1.3. Delete
            # 1.3.1. Delete button
            # Button will be disabled after deletion
            case.result = not(download_from_cl_dz_page.download_project.get_del_status())

            download_from_cl_dz_page.download_project.select_project('許功蓋')
            download_from_cl_dz_page.download_project.click_delete()
            download_from_cl_dz_page.download_project.handle_warning_msg(option='ok')

        with uuid('9e7281e0-17f1-4006-a4f2-fcc999a8350d') as case:
            # 1.5. Download
            # 1.5.1. Download
            # download the selected project
            download_from_cl_dz_page.download_project.select_project('CloudTestPack')
            case.result = download_from_cl_dz_page.tap_download()

        with uuid('e4116969-699e-495f-a17a-3ed7d4df48c5') as case:
            # 1.5. Download
            # 1.5.2. Select Folder dialog
            # download to the selected folder
            check_result = download_from_cl_dz_page.download_project.select_download_folder(
                Test_Material_Folder + 'cloud_test/')
            case.result = check_result

        with uuid('b49f152e-e49a-4c34-860a-0d75a5429ba5') as case:
            # 1.5. Download
            # 1.5.3. Project Download process > Download process
            # The download process bar and percentage display normally
            check_result = download_from_cl_dz_page.is_exist(
                {'AXIdentifier': 'IDC_CLOUDPROGRESS_PROGRESS_BTN_CANCEL'}, timeout=5)
            # check_result = download_from_cl_dz_page.download_project.process_dialog.check_main_window()
            case.result = check_result

        with uuid('b811e900-0a94-4f9e-809b-840f239e1cd2') as case:
            # 1.5. Download
            # 1.5.3. Project Download process > Remain time
            # The remain time displays normally
            check_result = download_from_cl_dz_page.exist(
                L.download_from_cl_dz.download_project.process_dialog.remain_time, timeout=30).AXValue
            # check_result = download_from_cl_dz_page.download_project.process_dialog.check_remain_time()
            case.result = False if 'Remaining Time:' not in check_result else True

        with uuid('228bac05-eafe-4894-9743-56e54cea0b89') as case:
            # 1.5. Download
            # 1.5.3. Project Download process > Cancel
            # Cancel the download process
            check_result = download_from_cl_dz_page.exist_click(
                L.download_from_cl_dz.download_project.process_dialog.cancel)
            # case.result = download_from_cl_dz_page.download_project.process_dialog.click_cancel()
            case.result = check_result
            time.sleep(DELAY_TIME)
            main_page.delete_folder(Test_Material_Folder + 'cloud_test/CloudTestPack/')

        with uuid('0531284e-866c-4d5b-a03d-af768784215f') as case:
            # 1.5. Download
            # 1.5.4. Project Download dialog > Open
            # Open the downloaded project
            download_from_cl_dz_page.download_project.select_project('CloudTestPack')
            download_from_cl_dz_page.tap_download()
            download_from_cl_dz_page.download_project.select_download_folder(Test_Material_Folder + 'cloud_test/')
            time.sleep(30)
            case.result = download_from_cl_dz_page.download_project.downloaded.click_open()

            main_page.handle_merge_media_to_current_library_dialog(option='no')
            time.sleep(DELAY_TIME * 5)
            main_page.delete_folder(Test_Material_Folder + 'cloud_test/CloudTestPack/')

        with uuid('c5a3152a-c1b5-4cc1-bc0b-3a43b61eee20') as case:
            # 1.5. Download
            # 1.5.4. Project Download dialog > OK
            # Don't open the downloaded project
            main_page.top_menu_bar_file_download_project_from_cyberlink_cloud()
            time.sleep(DELAY_TIME * 2)
            download_from_cl_dz_page.download_project.select_project('CloudTestPack')
            download_from_cl_dz_page.tap_download()
            download_from_cl_dz_page.download_project.select_download_folder(Test_Material_Folder + 'cloud_test/')
            time.sleep(30)
            case.result = download_from_cl_dz_page.download_project.downloaded.click_ok()
            main_page.delete_folder(Test_Material_Folder + 'cloud_test/CloudTestPack/')

        with uuid('290b8027-eacb-4578-a3fb-891a2cb19c8f') as case:
            # 1.6. Cancel
            # 1.6.1. Cancel button
            # Close the Download Project from CyberLink Cloud dialog
            check_result_1 = download_from_cl_dz_page.download_project.click_cancel()
            check_result_2 = download_from_cl_dz_page.is_not_exist(L.download_from_cl_dz.download_project.caption)
            case.result = check_result_1 and check_result_2

        with uuid('38b80e2f-2468-4384-b1dd-391d84c42a5b') as case:
            # 1.6. Cancel
            # 1.6.1. Cancel button > Hotkey (Esc)
            # Close the Download Project from CyberLink Cloud dialog
            main_page.top_menu_bar_file_download_project_from_cyberlink_cloud()
            time.sleep(DELAY_TIME * 3)
            download_from_cl_dz_page.press_esc_key()
            check_result = download_from_cl_dz_page.is_not_exist(L.download_from_cl_dz.download_project.caption)
            case.result = check_result

        with uuid('a62b1be9-dc6f-4059-815d-f8d42b598680') as case:
            # 1. Download Project from CyberLink Cloud...
            # 1.1 General
            # 1.1.3. X
            # Close the dialog
            main_page.top_menu_bar_file_download_project_from_cyberlink_cloud()
            time.sleep(DELAY_TIME * 3)
            check_result_1 = download_from_cl_dz_page.download_project.click_close()
            check_result_2 = download_from_cl_dz_page.is_not_exist(L.download_from_cl_dz.download_project.caption)
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid('d4744997-2e71-4e05-8e9a-a652aa46d876') as case:
            # 3. Pack Project Materials and Upload to CyberLink Cloud...
            # 3.1. Enter project name dialog
            # 3.1.1. Input column > Unsaved project
            # show "New Untitled Project Pack"
            main_page.top_menu_bar_file_pack_project_and_upload_to_cyberlink_cloud()
            pack_name = download_from_cl_dz_page.pack_project_and_upload.get_project_name()
            case.result = False if not pack_name == 'New Untitled Project Pack' else True

        with uuid('1779368b-bb16-4bd1-bb4b-d5920aa1f9fd') as case:
            # 3.1. Enter project name dialog
            # 3.1.4. [Cancel]
            # close the dialog
            check_result_1 = download_from_cl_dz_page.pack_project_and_upload.click_cancel()
            check_result_2 = download_from_cl_dz_page.is_not_exist(L.download_from_cl_dz.pack_project_and_upload.window)
            case.result = check_result_1 and check_result_2

        with uuid('bdfbbc00-15af-4343-b924-ee51a991eb30') as case:
            # 3.1. Enter project name dialog
            # 3.1.1. Input column > Saved project
            # show the saved name
            main_page.top_menu_bar_file_pack_project_and_upload_to_cyberlink_cloud()
            download_from_cl_dz_page.exist(L.download_from_cl_dz.pack_project_and_upload.window, timeout=5)
            check_result_1 = download_from_cl_dz_page.pack_project_and_upload.set_project_name('cloud_test_pack')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'DL_UL_project_to_cloud_3_1_1-1.png'
            ground_truth = Ground_Truth_Folder + 'DL_UL_project_to_cloud_3_1_1-1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.pack_project_and_upload.window, file_name=image_full_path)
            check_result_2 = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result_1 and check_result_2

        with uuid('cc53b954-c864-478f-aa35-ffde428e91fe') as case:
            # 3.1. Enter project name dialog
            # 3.1.4. [OK]
            # start to upload the project
            download_from_cl_dz_page.pack_project_and_upload.click_ok()
            project_is_existed = download_from_cl_dz_page.is_exist(L.download_from_cl_dz.upload_project.warning_msg.ok,timeout=30)
            if project_is_existed:
                download_from_cl_dz_page.upload_project.handle_warning_msg()
            case.result = main_page.is_exist(L.download_from_cl_dz.pack_project_and_upload.ok, timeout=100)

        with uuid('22455426-4e08-4b9f-b100-8cfaa34571bc') as case:
            # 3.2. Final dialog
            # 3.2.2. Upload successfully
            # show upload successfully msg
            case.result = download_from_cl_dz_page.pack_project_and_upload.uploaded.check_main_window()

        with uuid('917e816c-9e86-4503-830e-56f078dbef8d') as case:
            # 3.2. Final dialog
            # 3.2.2. Upload successfully > CL Cloud link
            # link to CL Cloud page
            case.result = download_from_cl_dz_page.pack_project_and_upload.uploaded.click_link()

        with uuid('e5cfb1b0-87a0-42ea-b77c-c2763a74c2a8') as case:
            # 3.2. Final dialog
            # 3.2.3. [OK]
            # close upload project to CyberLink cloud dialog
            check_result_1 = download_from_cl_dz_page.pack_project_and_upload.uploaded.click_ok()
            check_result_2 = download_from_cl_dz_page.is_not_exist(
                L.download_from_cl_dz.pack_project_and_upload.uploaded.link, timeout=5)

            case.result = check_result_1 and check_result_2

        with uuid('16d0cd7a-3d4a-401b-97e6-570db2fc64a3') as case:
            # 3.1. Enter project name dialog
            # 3.1.4. [OK] > The project has been uploaded
            # pop out warning msg
            main_page.top_menu_bar_file_pack_project_and_upload_to_cyberlink_cloud()
            download_from_cl_dz_page.pack_project_and_upload.set_project_name('cloud_test_pack')
            download_from_cl_dz_page.pack_project_and_upload.click_ok()
            main_page.is_exist(L.download_from_cl_dz.upload_project.warning_msg.ok, timeout=10)
            case.result = download_from_cl_dz_page.pack_project_and_upload.handle_warning_msg(option='ok')

        with uuid('c8d268a6-12ce-4bb6-b654-7f2a6e38b276') as case:
            # 3.2. Final dialog
            # 3.2.3. [OK] > Hotkey (Enter)
            # close upload project to CyberLink cloud dialog
            download_from_cl_dz_page.exist(L.download_from_cl_dz.pack_project_and_upload.uploaded.link, timeout=10)
            download_from_cl_dz_page.press_enter_key()
            check_result = download_from_cl_dz_page.is_not_exist(
                L.download_from_cl_dz.pack_project_and_upload.uploaded.link, timeout=5)

            case.result = check_result

        with uuid('aae50c36-9de6-42cc-b7b4-4d041f74590a') as case:
            # 3.2. Final dialog
            # 3.2.4. X
            # close upload project to CyberLink cloud dialog
            main_page.top_menu_bar_file_pack_project_and_upload_to_cyberlink_cloud()
            download_from_cl_dz_page.pack_project_and_upload.set_project_name('cloud_test_pack')
            download_from_cl_dz_page.pack_project_and_upload.click_ok()
            download_from_cl_dz_page.pack_project_and_upload.handle_warning_msg(option='ok')
            download_from_cl_dz_page.exist(L.download_from_cl_dz.pack_project_and_upload.uploaded.link, timeout=10)

            check_result_1 = download_from_cl_dz_page.pack_project_and_upload.click_close()
            check_result_2 = download_from_cl_dz_page.is_not_exist(
                L.download_from_cl_dz.pack_project_and_upload.uploaded.link, timeout=5)

            case.result = check_result_1 and check_result_2

        with uuid('6deeb060-6e1e-4c57-aa0b-b44205d9ca98') as case:
            # 3.2. Final dialog
            # 3.2.4. X > Hotkey (ESC)
            # close upload project to CyberLink cloud dialog
            main_page.top_menu_bar_file_pack_project_and_upload_to_cyberlink_cloud()
            download_from_cl_dz_page.pack_project_and_upload.set_project_name('cloud_test_pack')
            download_from_cl_dz_page.pack_project_and_upload.click_ok()
            download_from_cl_dz_page.pack_project_and_upload.handle_warning_msg(option='ok')
            download_from_cl_dz_page.exist(L.download_from_cl_dz.pack_project_and_upload.uploaded.link, timeout=10)

            download_from_cl_dz_page.press_esc_key()
            check_result = download_from_cl_dz_page.is_not_exist(
                L.download_from_cl_dz.pack_project_and_upload.uploaded.link, timeout=5)

            case.result = check_result

            # delete uploaded project pack
            main_page.top_menu_bar_file_download_project_from_cyberlink_cloud()
            download_from_cl_dz_page.download_project.sort_by_date(0)
            download_from_cl_dz_page.download_project.select_project('cloud_test_pack')
            download_from_cl_dz_page.download_project.click_delete()
            download_from_cl_dz_page.download_project.handle_warning_msg(option='ok')
            download_from_cl_dz_page.download_project.click_close()

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    bb6d72a0-2e5e-464c-b266-064b0cc2bf95
                    12391ed9-15a6-48f4-9ce8-ee60ff8cc4da
                    f69de65e-e152-417f-874c-b406d4cbaf7e
                    9bf9ed44-0f4e-4374-a6a6-c088ec0358b5
                    3d4bfe3e-0d16-433c-a177-082af797acca
                    995506fc-9e4c-43e5-a858-ee4ad810410c
                    92ec5b08-5772-4ee0-9626-4e054ec80454
                    72d5f61f-3bb1-4fb3-a3dc-a48361dce0ef
                    f5fffe0a-1f04-4556-aa18-9dfff1fb3fc0
                    f69fe3c4-36ce-4d73-89d9-ce59941895e7
                    96c8be06-a261-4cc4-8ded-dae6ddaae9e3
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'
