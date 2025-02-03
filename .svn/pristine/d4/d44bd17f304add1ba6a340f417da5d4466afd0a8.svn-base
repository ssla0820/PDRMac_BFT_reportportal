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
upload_cloud_dz_page = PageFactory().get_page_object('upload_cloud_dz_page', mwc)
download_from_cl_dz_page = PageFactory().get_page_object('download_from_cl_dz_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
pip_designer_page = PageFactory().get_page_object('pip_designer_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
title_designer_page = PageFactory().get_page_object('title_designer_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
mask_designer_page = PageFactory().get_page_object('mask_designer_page', mwc)
video_collage_designer_page = PageFactory().get_page_object('video_collage_designer_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)
produce_page = PageFactory().get_page_object('produce_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page', mwc)
particle_designer_page = PageFactory().get_page_object('particle_designer_page', mwc)
import_media_from_cloud_page = PageFactory().get_page_object('import_downloaded_media_from_cl_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Upload Cloud or DZ.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Upload_Cloud_DZ/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Upload_Cloud_DZ/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1


class Test_Upload_Cloud_DZ():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        # delete Material "cloud_test" folder
        temp_dir = os.path.abspath(Test_Material_Folder + 'cloud_test')
        logger(temp_dir)
        main_page.delete_folder(temp_dir)

        main_page.start_app()
        media_room_page.find(L.media_room.library_listview.unit_collection_view_item, timeout=10)
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
            google_sheet_execution_log_init('Upload_Cloud_DZ')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"upload cloud/dz result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        with uuid('782128fd-5df9-414d-8e58-dd9e0d1338e5') as case:
            # 1. Entry Point
            # 1.1. File Menu > Upload Project to CyberLink Cloud
            # Enter Upload dialog
            check_result_1 = upload_cloud_dz_page.tap_Filemenu_UploadProject_ToCL()
            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_1_1-1.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_1_1-1.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2
            download_from_cl_dz_page.upload_project.click_close()

        with uuid('406ebb61-8047-4a6c-8672-029ee880b2ee') as case:
            # 1. Entry Point
            # 1.1. File Menu > Pack Project Materials and Upload to CyberLink Cloud
            # Enter Upload dialog
            check_result_1 = upload_cloud_dz_page.tap_Filemenu_PackProject_UploadCL()

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_1_1-2.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_1_1-2.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2
            download_from_cl_dz_page.upload_project.click_cancel()

        with uuid('26eeb147-8f73-4c0e-98d0-5719710d7e69') as case:
            # 1. Entry Point
            # 1.3. Context Menu of Library: Share and Upload to the Internet > PiP Room
            # Enter Upload dialog
            main_page.enter_room(4)  # enter pip room
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.click_ok()
            pip_designer_page.input_template_name_and_click_ok('cloud_test')
            pip_room_page.hover_library_media('cloud_test')
            case.result = pip_room_page.select_RightClickMenu_ShareUploadToInternet()

            time.sleep(DELAY_TIME)

        with uuid('f8981740-951a-4aa7-8ef0-897ff891810f') as case:
            # 1. Entry Point
            # 1.3. Context Menu of Library: Share and Upload to the Internet > Title Room
            # Enter Upload dialog
            main_page.enter_room(1)  # enter title room
            title_room_page.click_CreateNewTitle_btn()
            title_designer_page.click_ok()
            title_designer_page.click_custom_name_ok('cloud_test')
            title_room_page.hover_library_media('cloud_test')
            case.result = title_room_page.select_RightClickMenu_ShareUploadToInternet()

            time.sleep(DELAY_TIME)

        with uuid('34e6d8e1-1862-4a17-b523-180b29c6e8bd') as case:
            # 1. Entry Point
            # 1.4. Designer Dialog > PiP Designer
            # Enter Upload dialog
            main_page.enter_room(4)  # enter pip room
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.click_share()
            pip_designer_page.save_as_name('cloud_test')
            pip_designer_page.exist(L.pip_designer.save_as_ok).press()
            login_dz_confirm_dialog = pip_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_1_4-1.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_1_4-1.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            case.result = upload_cloud_dz_page.compare(ground_truth, current_preview)

            pip_designer_page.press_esc_key()
            pip_designer_page.click_cancel()

        with uuid('3df36155-cd79-4e6d-bc30-afbd0be1f8e3') as case:
            # 1. Entry Point
            # 1.4. Designer Dialog > Title Designer
            # Enter Upload dialog
            main_page.enter_room(1)  # enter title room
            title_room_page.click_CreateNewTitle_btn()
            title_designer_page.click_share()
            title_designer_page.exist(
                L.title_designer.save_as_template.edittext_save_as_template).sendKeys('cloud_test')
            title_designer_page.exist(L.title_designer.save_as_template.btn_ok).press()
            login_dz_confirm_dialog = title_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_1_4-2.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_1_4-2.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            case.result = upload_cloud_dz_page.compare(ground_truth, current_preview)

            title_designer_page.press_esc_key()
            title_designer_page.click_cancel()

        with uuid('24f9cf33-3cbf-445b-91b7-50c55d590690') as case:
            # 1. Entry Point
            # 1.4. Designer Dialog > Mask Designer
            # Enter Upload dialog
            main_page.enter_room(0)  # enter media room
            main_page.insert_media('Food.jpg')
            tips_area_page.tools.select_Mask_Designer()
            mask_designer_page.Edit_MaskDesigner_ClickShare()
            mask_designer_page.exist(L.mask_designer.save_as_dlg.name).sendKeys('cloud_test')
            mask_designer_page.exist(L.mask_designer.save_as_dlg.ok).press()
            login_dz_confirm_dialog = mask_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_1_4-3.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_1_4-3.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            case.result = upload_cloud_dz_page.compare(ground_truth, current_preview)

            mask_designer_page.press_esc_key()
            mask_designer_page.Edit_MaskDesigner_ClickCancel(option=None)

        with uuid('97bb1b00-d416-48d9-bdfc-b6c161df10cb') as case:
            # 1. Entry Point
            # 1.4. Designer Dialog > Video Collage Designer
            # Enter Upload dialog
            main_page.top_menu_bar_plugins_video_collage_designer()
            video_collage_designer_page.click_share()
            video_collage_designer_page.exist(L.video_collage_designer.save_as.input_name).sendKeys('cloud_test')
            video_collage_designer_page.exist(L.video_collage_designer.save_as.btn_ok).press()
            login_dz_confirm_dialog = video_collage_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_1_4-4.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_1_4-4.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            case.result = upload_cloud_dz_page.compare(ground_truth, current_preview)

            video_collage_designer_page.press_esc_key()
            video_collage_designer_page.click_cancel()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid('bbefd7af-1c52-43bb-8ec5-57bce4ae1c0a') as case:
            # 1. Entry Point
            # 1.5. Upload a copy to CyberLink Cloud in Produce page > 2D > H.264 AVC
            # Display checkbox of Upload a copy to CyberLink Cloud
            main_page.insert_media('Skateboard 02.mp4')
            main_page.click_produce()
            in_produce_page = produce_page.check_enter_produce_page()
            if in_produce_page:
                produce_page.local.select_file_format('avc')
                produce_page.local.set_check_upload_copy_to_cyberlink_cloud()
                main_page.delete_folder(Test_Material_Folder + 'cloud_test/Produce.mp4')
                time.sleep(DELAY_TIME)
                produce_page.select_output_folder(Test_Material_Folder + 'cloud_test/Produce')
                produce_page.exist_click(L.produce.btn_start_produce)
                produce_page.local.click_option_convert_cyberlink_cloud_copy_to_mp4_dialog(option=1)
                produce_finish = produce_page.is_exist(L.produce.btn_back_to_edit_after_upload_cl, timeout=30)
                if produce_finish:
                    check_result_1 = produce_page.is_exist(L.produce.txt_produce_and_upload_complete)
                    check_result_2 = produce_page.is_exist(L.produce.btn_view_on_cloud_hyperlink)
                else:
                    logger('produce & upload to cloud fail')
            else:
                logger('did not enter produce page')

            case.result = check_result_1 and check_result_2
            # back to edit mode and delete produced file
            produce_page.exist_click(L.produce.btn_back_to_edit_after_upload_cl)
            time.sleep(2)
            media_room_page.hover_library_media('Produce.mp4')
            main_page.right_click()
            main_page.select_right_click_menu('Move to Trash Can')

        with uuid('42eef3dc-8ab4-419b-ab3c-4152f321e140') as case:
            # 1. Entry Point
            # 1.5. Upload a copy to CyberLink Cloud in Produce page > 2D > H.265 HEVC
            # Display checkbox of Upload a copy to CyberLink Cloud
            main_page.click_produce()
            in_produce_page = produce_page.check_enter_produce_page()
            if in_produce_page:
                produce_page.local.select_file_format('hevc')
                produce_page.local.set_check_upload_copy_to_cyberlink_cloud()
                produce_page.select_output_folder(Test_Material_Folder + 'cloud_test/Produce')
                produce_page.exist_click(L.produce.btn_start_produce)
                produce_page.local.click_option_convert_cyberlink_cloud_copy_to_mp4_dialog(option=1)
                produce_finish = produce_page.is_exist(L.produce.btn_back_to_edit_after_upload_cl, timeout=30)
                if produce_finish:
                    check_result_1 = produce_page.is_exist(L.produce.txt_produce_and_upload_complete)
                    check_result_2 = produce_page.is_exist(L.produce.btn_view_on_cloud_hyperlink)
                else:
                    logger('produce & upload to cloud fail')
            else:
                logger('did not enter produce page')

            case.result = check_result_1 and check_result_2
            # back to edit mode and delete produced file
            produce_page.exist_click(L.produce.btn_back_to_edit_after_upload_cl)
            time.sleep(2)
            media_room_page.hover_library_media('Produce.mp4')
            main_page.right_click()
            main_page.select_right_click_menu('Move to Trash Can')

        with uuid('aaf8a9da-0ba9-4fe1-a01c-65aa368901e1') as case:
            # 1. Entry Point
            # 1.5. Upload a copy to CyberLink Cloud in Produce page > 2D > XAVC S
            # Display checkbox of Upload a copy to CyberLink Cloud
            main_page.click_produce()
            in_produce_page = produce_page.check_enter_produce_page()
            time.sleep(DELAY_TIME*2)
            if in_produce_page:
                produce_page.local.select_file_format('xavc_s')
                produce_page.local.set_check_upload_copy_to_cyberlink_cloud()
                produce_page.select_output_folder(Test_Material_Folder + 'cloud_test/Produce')
                produce_page.exist_click(L.produce.btn_start_produce)
                produce_page.local.click_option_convert_cyberlink_cloud_copy_to_mp4_dialog(option=1)
                produce_finish = produce_page.is_exist(L.produce.btn_back_to_edit_after_upload_cl, timeout=30)
                if produce_finish:
                    check_result_1 = produce_page.is_exist(L.produce.txt_produce_and_upload_complete)
                    check_result_2 = produce_page.is_exist(L.produce.btn_view_on_cloud_hyperlink)
                else:
                    logger('produce & upload to cloud fail')
            else:
                logger('did not enter produce page')

            case.result = check_result_1 and check_result_2
            # back to edit mode and delete produced file
            produce_page.exist_click(L.produce.btn_back_to_edit_after_upload_cl)
            time.sleep(2)
            media_room_page.hover_library_media('Produce.mp4')
            main_page.right_click()
            main_page.select_right_click_menu('Move to Trash Can')

            # remove uploaded content
            time.sleep(DELAY_TIME)
            media_room_page.import_media_from_cyberlink_cloud()

            download_from_cl_dz_page.set_search_text('powerdirector')
            time.sleep(DELAY_TIME)
            import_media_from_cloud_page.tap_select_deselect_all_btn()
            time.sleep(DELAY_TIME)
            delete_btn_enabled = import_media_from_cloud_page.exist(
                L.import_downloaded_media_from_cl.delete_btn).AXEnabled
            if delete_btn_enabled:
                download_from_cl_dz_page.exist_click(L.import_downloaded_media_from_cl.delete_btn)
                download_from_cl_dz_page.download_project.handle_warning_msg(option='ok')
                delete_btn_status = import_media_from_cloud_page.exist(
                    L.import_downloaded_media_from_cl.delete_btn, timeout=10).AXEnabled
                if not delete_btn_status:
                    download_from_cl_dz_page.tap_close_button()
            else:
                download_from_cl_dz_page.tap_close_button()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid('0462b5a1-378b-4255-ab68-183edeff9cfc') as case:
            # 2. Upload Cloud Project
            # 2.1. Enter a Name > Default
            # Add in Custom & check saved template display as settings
            main_page.top_menu_bar_file_upload_project_to_cyberlink_cloud()
            upload_cloud_dz_page.upload_project.edit_ClickOK()
            time.sleep(DELAY_TIME * 2)
            overwrite_confirm_dialog = upload_cloud_dz_page.is_exist(L.base.confirm_dialog.main_window, timeout=10)
            if overwrite_confirm_dialog:
                upload_cloud_dz_page.click(L.base.confirm_dialog.btn_ok)
            upload_cloud_dz_page.upload_project.check_Complete()
            main_page.top_menu_bar_file_download_project_from_cyberlink_cloud()
            time.sleep(DELAY_TIME * 5)

            check_result = download_from_cl_dz_page.download_project.find_project('New Untitled Project')
            case.result = check_result

            # delete uploaded project
            download_from_cl_dz_page.download_project.select_project('New Untitled Project')
            download_from_cl_dz_page.download_project.click_delete()
            download_from_cl_dz_page.download_project.handle_warning_msg(option='ok')
            download_from_cl_dz_page.download_project.click_close()

        with uuid('87974730-5a2a-41a4-99e1-3e6cc1698631') as case:
            # 2. Upload Cloud Project
            # 2.1. Enter a Name > Custom
            # Add in Custom & check saved template display as settings
            main_page.top_menu_bar_file_upload_project_to_cyberlink_cloud()
            upload_cloud_dz_page.upload_project.edit_InputProjectName('cloud_test_project')
            upload_cloud_dz_page.upload_project.edit_ClickOK()
            upload_cloud_dz_page.upload_project.check_Complete()
            main_page.top_menu_bar_file_download_project_from_cyberlink_cloud()
            time.sleep(DELAY_TIME * 3)

            check_result = download_from_cl_dz_page.download_project.find_project('cloud_test_project')
            case.result = check_result

        with uuid('19f8687e-d50d-4952-94d9-860078830767') as case:
            # 2. Upload Cloud Project
            # 2.3. Upload Progress > Success
            # upload correctly
            have_new_upload_project = download_from_cl_dz_page.download_project.find_project('cloud_test_project')
            case.result = False if not have_new_upload_project else True

            # delete uploaded project
            download_from_cl_dz_page.download_project.select_project('cloud_test_project')
            download_from_cl_dz_page.download_project.click_delete()
            download_from_cl_dz_page.download_project.handle_warning_msg(option='ok')
            download_from_cl_dz_page.download_project.click_close()

        with uuid('a6a644c7-0d81-42cc-a06c-157ab8c8b8cc') as case:
            # 2. Upload Cloud Project
            # 2.3. Upload Progress > Cancel
            # Cancel Progress & exit upload  -> AT limitation, skip this case

            # main_page.top_menu_bar_file_upload_project_to_cyberlink_cloud()
            # upload_cloud_dz_page.upload_project.edit_ClickOK()
            # upload_cloud_dz_page.upload_project.edit_Uploading_ClickCancel()
            # upload_cloud_dz_page.upload_project.handle_ConfirmCancel_ClickYes()
            #
            # main_page.top_menu_bar_file_download_project_from_cyberlink_cloud()
            # time.sleep(DELAY_TIME * 3)
            # have_new_upload_project = download_from_cl_dz_page.download_project.find_project('New Untitled Project')
            # case.result = True if not have_new_upload_project else False
            #
            # download_from_cl_dz_page.download_project.click_close()
            case.result = None
            case.fail_log = 'AT limition'

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid('405adb30-19ed-4b9c-9378-36ee3a6f8f46') as case:
            # 3. Pack Project Materials and Upload to CyberLink Cloud
            # 3.1. Enter a Name > Default
            # Add in Custom & check saved template display as settings
            main_page.top_menu_bar_file_pack_project_and_upload_to_cyberlink_cloud()
            upload_cloud_dz_page.pack_project.edit_ClickOK()
            project_exist = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.btn_warning_ok)
            if project_exist:
                upload_cloud_dz_page.upload_project.handle_OverwriteIt()
            upload_cloud_dz_page.pack_project.check_Complete()

            main_page.top_menu_bar_file_download_project_from_cyberlink_cloud()
            time.sleep(DELAY_TIME * 3)
            have_new_upload_project = download_from_cl_dz_page.download_project.find_project(
                'New Untitled Project Pack')
            check_result = False if not have_new_upload_project else True
            case.result = check_result

            # delete uploaded project
            download_from_cl_dz_page.download_project.select_project('New Untitled Project Pack')
            download_from_cl_dz_page.download_project.click_delete()
            download_from_cl_dz_page.download_project.handle_warning_msg(option='ok')
            download_from_cl_dz_page.download_project.click_close()

        with uuid('28554bdd-35a8-4a32-b6ee-8621ebd28fc9') as case:
            # 3. Pack Project Materials and Upload to CyberLink Cloud
            # 3.1. Enter a Name > Custom
            # Add in Custom & check saved template display as settings
            main_page.top_menu_bar_file_pack_project_and_upload_to_cyberlink_cloud()
            upload_cloud_dz_page.pack_project.edit_InputProjectName('test_project_pack')
            upload_cloud_dz_page.pack_project.edit_ClickOK()
            project_exist = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.btn_warning_ok)
            if project_exist:
                upload_cloud_dz_page.upload_project.handle_OverwriteIt()
            upload_cloud_dz_page.pack_project.check_Complete()

            main_page.top_menu_bar_file_download_project_from_cyberlink_cloud()
            time.sleep(DELAY_TIME * 3)
            have_new_upload_project = download_from_cl_dz_page.download_project.find_project('test_project_pack')
            check_result = False if not have_new_upload_project else True
            case.result = check_result

        with uuid('29ae8688-52bc-4086-bf9f-da79049be5fd') as case:
            # 3. Pack Project Materials and Upload to CyberLink Cloud
            # 3.5. Upload Progress > Success
            # upload correctly
            case.result = check_result

            # delete uploaded project
            download_from_cl_dz_page.download_project.select_project('test_project_pack')
            download_from_cl_dz_page.download_project.click_delete()
            download_from_cl_dz_page.download_project.handle_warning_msg(option='ok')
            download_from_cl_dz_page.download_project.click_close()

        with uuid('e8f62e4a-ee45-491d-a195-b4b914da3bc1') as case:
            # 3. Pack Project Materials and Upload to CyberLink Cloud
            # 3.5. Upload Progress > Cancel
            # cancel progress & exit upload -> AT limitation, skip this case

            # main_page.insert_media('Skateboard 02.mp4')
            # main_page.top_menu_bar_file_pack_project_and_upload_to_cyberlink_cloud()
            # upload_cloud_dz_page.pack_project.edit_ClickOK()
            # project_exist = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.btn_warning_ok)
            # if project_exist:
            #     upload_cloud_dz_page.upload_project.handle_OverwriteIt()
            # upload_cloud_dz_page.pack_project.edit_Uploading_ClickCancel()
            # upload_cloud_dz_page.pack_project.handle_ConfirmCancel_ClickYes()
            #
            # main_page.top_menu_bar_file_download_project_from_cyberlink_cloud()
            # time.sleep(DELAY_TIME * 3)
            # have_new_upload_project = download_from_cl_dz_page.download_project.find_project(
            #     'New Untitled Project Pack')
            # case.result = True if not have_new_upload_project else False
            #
            # download_from_cl_dz_page.download_project.click_close()
            case.result = None
            case.fail_log = 'AT limition'

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid('6bb1826f-4b1c-4723-8185-c0e440e56791') as case:
            # 4.2. Step1: Describe Template
            # 4.2.5. Close > [X] button
            # close dialog correctly

            # enter pip room
            main_page.enter_room(4)

            # Select category "General"
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME * 2)

            # Select template "Dialog_03"
            main_page.select_library_icon_view_media("Dialog_03")

            pip_room_page.click_ModifyAttribute_btn(strType='PiP')
            pip_designer_page.click_share()
            pip_designer_page.save_as_name('cloud_test')
            pip_designer_page.exist(L.pip_designer.save_as_ok).press()
            login_dz_confirm_dialog = pip_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)
            upload_template_dialog = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.upload_description)
            if upload_template_dialog:
                check_result = upload_cloud_dz_page.designer_upload_template.tap_CloseWindow()
            case.result = check_result

        with uuid('1977b26c-aefa-4933-bbc7-2074ad7cf623') as case:
            # 4. PiP Designer
            # 4.1. Save As Template
            # 4.1.1. Enter a Name
            # Add in Custom & check saved template display as settings
            pip_designer_page.click_share()
            check_result_1 = pip_designer_page.save_as_name('cloud_test')
            current_slider_value = pip_designer_page.exist(L.pip_designer.save_as_slider).AXValue
            check_result_2 = False if not current_slider_value == 0.5 else True
            pip_designer_page.exist(L.pip_designer.save_as_ok).press()
            login_dz_confirm_dialog = pip_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)

            current_title = upload_cloud_dz_page.designer_upload_template.get_TitleField()
            check_result_3 = False if not current_title == ' cloud_test' else True

            case.result = check_result_1 and check_result_3

        with uuid('2606afd5-1d8e-49c8-8993-99f8355a6cd8') as case:
            # 4.1. Save As Template
            # 4.1.2. Use the Slider > Middle (Default)
            # Add in Custom & check saved template display as settings
            case.result = check_result_2

        with uuid('cbf0771e-8536-406d-a7ea-2fce6e5281d7') as case:
            # 4.2. Step1: Describe Template
            # 4.2.1. Upload > CyberLink Cloud & DirectorZone
            # Upload template correctly & check upload display as settings
            current_upload_to_setting = upload_cloud_dz_page.exist(L.upload_cloud_dz.upload_to).AXTitle
            case.result = False if not current_upload_to_setting == 'CyberLink Cloud and Dir...' else True

            upload_cloud_dz_page.designer_upload_template.edit_Upload_To(upload_option=1)  # upload to CL Cloud

        with uuid('162b76b0-91c6-4f08-8a10-b6a289c679b3') as case:
            # 4.2. Step1: Describe Template
            # 4.2.2. Cloud > Space Display
            # check display correctly
            case.result = upload_cloud_dz_page.designer_upload_template.check_UsedSpaceInfo()

        with uuid('46d102d8-2f46-4921-bff8-83ee56b27a21') as case:
            # 4.2. Step1: Describe Template
            # 4.2.3. Info > Details
            # link to related account webpage correctly
            case.result = upload_cloud_dz_page.designer_upload_template.check_DetailsLink()
            time.sleep(DELAY_TIME * 3)

        with uuid('36c7e2e1-0072-4185-8971-f3e68932df27') as case:
            # 4.2. Step1: Describe Template
            # 4.2.3. Info > Title
            # check template info display as settings
            case.result = check_result_3

        with uuid('b0d94f7f-5dd6-4ee2-8d54-0abbab807e99') as case:
            # 4.2. Step1: Describe Template
            # 4.2.3. Info > Empty info (SPACE)
            # next button should disable
            upload_cloud_dz_page.designer_upload_template.edit_InputTags(' ')
            upload_cloud_dz_page.designer_upload_template.edit_InputCollection(' ')
            upload_cloud_dz_page.designer_upload_template.edit_InputDescription(' ')

            check_next_btn_status = upload_cloud_dz_page.exist(L.upload_cloud_dz.upload_btn_next).AXEnabled
            case.result = True if not check_next_btn_status else False

        with uuid('22e9bded-8a6d-4233-a7dc-44b88421f8f7') as case:
            # 4.2. Step1: Describe Template
            # 4.2.3. Info > Style
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_ApplyStyle(style=12)  # style: Pets
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_4_2_3-1.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_4_2_3-1.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('2c339a51-8947-49dd-905b-6dc0102089be') as case:
            # 4.2. Step1: Describe Template
            # 4.2.3. Info > Tags
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_InputTags('bubble')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_4_2_3-2.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_4_2_3-2.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('a991a109-780c-4a3a-8f33-d94d44dd543d') as case:
            # 4.2. Step1: Describe Template
            # 4.2.3. Info > Collection
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_InputCollection('cartoon')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_4_2_3-3.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_4_2_3-3.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('63f3caed-3582-4c69-9e9e-39a7fc04b4bb') as case:
            # 4.2. Step1: Describe Template
            # 4.2.3. Info > Description
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_InputDescription('for upload test')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_4_2_3-4.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_4_2_3-4.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('d5ba38f9-ad14-4215-baa5-8bd733018072') as case:
            # 4.3. Confirm Copyright Disclaimer
            # 4.3.1. Copyright Display
            # check display correctly
            upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            check_result_1 = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.upload_tick_confirm, timeout=5)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_4_3_1-1.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_4_3_1-1.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('45ed5b4d-2e91-47a8-98ad-b1fa0926403e') as case:
            # 4.3. Confirm Copyright Disclaimer
            # 4.3.2. I have Confirmed > Untick (Default)
            # disable Next
            check_result = not upload_cloud_dz_page.find(L.upload_cloud_dz.upload_btn_next).AXEnabled
            case.result = check_result

        with uuid('71effa2f-0677-4ecb-9f00-6d11cb57de85') as case:
            # 4.3. Confirm Copyright Disclaimer
            # 4.3.2. I have Confirmed > Tick
            # continue Next
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_TickConfirm()
            check_result_2 = upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            case.result = check_result_1 and check_result_2

            time.sleep(DELAY_TIME * 3)

        with uuid('aa077bdd-7fed-41fa-9bf6-2e3b4aeedb0e') as case:
            # 4.4. Step2: Upload Progress
            # 4.4.3. Upload Progress > Cancel
            # cancel progress & exit upload
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_ClickCancel()
            check_result_2 = upload_cloud_dz_page.is_not_exist(L.upload_cloud_dz.upload_template_dialog)
            case.result = check_result_1 and check_result_2

        with uuid('d9e65971-16af-43c3-8940-1f390be3bdc9') as case:
            # 4.4. Step2: Upload Progress
            # 4.4.3. Upload Progress > Success
            # upload correctly
            pip_designer_page.click_share()
            pip_designer_page.save_as_name('cloud_test')
            pip_designer_page.exist(L.pip_designer.save_as_ok).press()
            login_dz_confirm_dialog = pip_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)
            upload_cloud_dz_page.designer_upload_template.edit_Upload_To(upload_option=1)  # upload to CL Cloud
            upload_cloud_dz_page.designer_upload_template.edit_ApplyStyle(style=12)  # style: Pets
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_InputTags('bubble')
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_InputCollection('cartoon')
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_InputDescription('for upload test')
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            # upload_cloud_dz_page.designer_upload_template.edit_TickConfirm()
            # upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            time.sleep(DELAY_TIME)
            check_result_1 = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.upload_view_CL, timeout=60)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_4_4_3-1.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_4_4_3-1.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)
            check_result_3 = upload_cloud_dz_page.designer_upload_template.edit_ClickFinish()

            case.result = check_result_1 and check_result_2 and check_result_3
            pip_designer_page.click_close_btn()

        # kill uploaded template
        time.sleep(DELAY_TIME)
        # main_page.enter_room(4)
        pip_room_page.exist_click(L.pip_room.btn_import_media)
        pip_room_page.exist_click(L.pip_room.btn_download_from_DZ_cloud)
        download_from_cl_dz_page.find(L.download_from_cl_dz.template, timeout=20)
        download_from_cl_dz_page.select_template('cloud_test')
        time.sleep(DELAY_TIME)
        download_from_cl_dz_page.tap_delete_button()
        main_page.press_enter_key()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid('6188f7ee-d3be-4c3f-bf3b-4a709a9fb13f') as case:
            # 5.2. Step1: Describe Template
            # 5.2.5. Close > [X] button
            # close dialog correctly
            main_page.enter_room(5)  # enter particle room
            particle_room_page.click_ModifySelectedParticle_btn()
            particle_designer_page.click_Share()
            particle_designer_page.save_as_name('cloud_test')
            particle_designer_page.save_as_ok()
            login_dz_confirm_dialog = pip_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)
            upload_template_dialog = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.upload_description)
            if upload_template_dialog:
                check_result = upload_cloud_dz_page.designer_upload_template.tap_CloseWindow()
            case.result = check_result

        with uuid('e18c2419-32a7-45a9-b278-965fb9f4871f') as case:
            # 5. Particle Designer
            # 5.1. Save As Template
            # 5.1.1. Enter a Name
            # Add in Custom & check saved template display as settings
            particle_designer_page.click_Share()
            check_result_1 = particle_designer_page.save_as_name('cloud_test')
            current_slider_value = particle_designer_page.exist(
                L.particle_designer.save_as_template_dialog.slider).AXValue
            check_result_2 = False if not current_slider_value == 0.5 else True
            particle_designer_page.save_as_ok()
            login_dz_confirm_dialog = pip_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)

            current_title = upload_cloud_dz_page.designer_upload_template.get_TitleField()
            check_result_3 = False if not current_title == ' cloud_test' else True

            case.result = check_result_1 and check_result_3

        with uuid('4e36e298-c89e-4eca-87a5-c6d0a0423b02') as case:
            # 5.1. Save As Template
            # 5.1.2. Use the Slider > Middle (Default)
            # Add in Custom & check saved template display as settings
            case.result = check_result_2

        with uuid('af32813c-36e6-4028-a7d0-71345bd26265') as case:
            # 5.2. Step1: Describe Template
            # 5.2.1. Upload > CyberLink Cloud & DirectorZone
            # Upload template correctly & check upload display as settings
            current_upload_to_setting = upload_cloud_dz_page.exist(L.upload_cloud_dz.upload_to).AXTitle
            case.result = False if not current_upload_to_setting == 'CyberLink Cloud and Dir...' else True

            upload_cloud_dz_page.designer_upload_template.edit_Upload_To(upload_option=1)  # upload to CL Cloud

        with uuid('7e639c7a-6131-4ca3-b814-96aab22f7fd7') as case:
            # 5.2. Step1: Describe Template
            # 5.2.2. Cloud > Space Display
            # check display correctly
            case.result = upload_cloud_dz_page.designer_upload_template.check_UsedSpaceInfo()

        with uuid('8e36dea6-ed83-4682-84a3-ac156a927528') as case:
            # 5.2. Step1: Describe Template
            # 5.2.3. Info > Details
            # link to related account webpage correctly
            case.result = upload_cloud_dz_page.designer_upload_template.check_DetailsLink()
            time.sleep(DELAY_TIME * 3)

        with uuid('49cfdce3-8421-4eef-8dc4-dc373dd8a5c8') as case:
            # 5.2. Step1: Describe Template
            # 5.2.3. Info > Title
            # check template info display as settings
            case.result = check_result_3

        with uuid('9506b221-bda8-4c4d-bb6b-b8e1f2c5ce69') as case:
            # 5.2. Step1: Describe Template
            # 5.2.3. Info > Empty info (SPACE)
            # next button should disable
            upload_cloud_dz_page.designer_upload_template.edit_InputTags(' ')
            upload_cloud_dz_page.designer_upload_template.edit_InputCollection(' ')
            upload_cloud_dz_page.designer_upload_template.edit_InputDescription(' ')

            check_next_btn_status = upload_cloud_dz_page.exist(L.upload_cloud_dz.upload_btn_next).AXEnabled
            case.result = True if not check_next_btn_status else False

        with uuid('26d6db54-4df6-4b64-8266-7042ccbf89a0') as case:
            # 5.2. Step1: Describe Template
            # 5.2.3. Info > Style
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_ApplyStyle(style=12)  # style: Pets
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_5_2_3-1.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_5_2_3-1.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('b3ae1e30-0882-4dfd-a796-febfbadf2dc9') as case:
            # 5.2. Step1: Describe Template
            # 5.2.3. Info > Tags
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_InputTags('bubble')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_5_2_3-2.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_5_2_3-2.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('a1427bc9-c1af-43e1-826c-5a661dc4d827') as case:
            # 5.2. Step1: Describe Template
            # 5.2.3. Info > Collection
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_InputCollection('cartoon')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_5_2_3-3.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_5_2_3-3.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('6332f43c-4947-4657-a03d-a9b1dac75fc5') as case:
            # 5.2. Step1: Describe Template
            # 5.2.3. Info > Description
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_InputDescription('for upload test')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_5_2_3-4.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_5_2_3-4.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('2ed97a2c-28a3-4bc9-83e7-c8cacc37774b') as case:
            # 5.3. Confirm Copyright Disclaimer
            # 5.3.1. Copyright Display
            # check display correctly
            upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            check_result_1 = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.upload_tick_confirm, timeout=5)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_5_3_1-1.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_5_3_1-1.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('f889d0ad-5846-4f15-ab0f-90c02b34b1dd') as case:
            # 5.3. Confirm Copyright Disclaimer
            # 5.3.2. I have Confirmed > Untick (Default)
            # disable Next
            check_result = not upload_cloud_dz_page.find(L.upload_cloud_dz.upload_btn_next).AXEnabled
            case.result = check_result

        with uuid('fb44a5c0-c35c-49f9-9dac-c78821ed98ce') as case:
            # 5.3. Confirm Copyright Disclaimer
            # 5.3.2. I have Confirmed > Tick
            # continue Next
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_TickConfirm()
            check_result_2 = upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            case.result = check_result_1 and check_result_2

            time.sleep(DELAY_TIME * 3)

        with uuid('70f4ddae-9b80-40fd-8bf2-e996187c6776') as case:
            # 5.4. Step2: Upload Progress
            # 5.4.3. Upload Progress > Cancel
            # cancel progress & exit upload
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_ClickCancel()
            check_result_2 = upload_cloud_dz_page.is_not_exist(L.upload_cloud_dz.upload_template_dialog)
            case.result = check_result_1 and check_result_2

            time.sleep(DELAY_TIME)

        with uuid('80f18791-85f1-4a20-81db-56cd5b0a5243') as case:
            # 5.4. Step2: Upload Progress
            # 5.4.3. Upload Progress > Success
            # upload correctly
            particle_designer_page.click_Share()
            particle_designer_page.save_as_name('cloud_test')
            particle_designer_page.save_as_ok()
            login_dz_confirm_dialog = pip_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)
            upload_cloud_dz_page.designer_upload_template.edit_Upload_To(upload_option=1)  # upload to CL Cloud
            upload_cloud_dz_page.designer_upload_template.edit_ApplyStyle(style=12)  # style: Pets
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_InputTags('bubble')
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_InputCollection('cartoon')
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_InputDescription('for upload test')
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            # upload_cloud_dz_page.designer_upload_template.edit_TickConfirm()
            # upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            time.sleep(DELAY_TIME)
            check_result_1 = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.upload_view_CL, timeout=60)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_5_4_3-1.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_5_4_3-1.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)
            check_result_3 = upload_cloud_dz_page.designer_upload_template.edit_ClickFinish()

            case.result = check_result_1 and check_result_2 and check_result_3
            particle_designer_page.click_close_btn()

            # kill uploaded template
        time.sleep(DELAY_TIME)
        # main_page.enter_room(4)
        particle_room_page.exist_click(L.particle_room.btn_import_media)
        particle_room_page.exist_click(L.particle_room.btn_download_from_DZ_cloud)
        download_from_cl_dz_page.find(L.download_from_cl_dz.template, timeout=20)
        download_from_cl_dz_page.select_template('cloud_test')
        time.sleep(DELAY_TIME)
        download_from_cl_dz_page.tap_delete_button()
        main_page.press_enter_key()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        with uuid('9f96b018-fc00-40ad-b730-9afbc8b7907f') as case:
            # 6.2. Step1: Describe Template
            # 6.2.5. Close > [X] button
            # close dialog correctly
            main_page.enter_room(1)  # enter title room
            title_room_page.click_CreateNewTitle_btn()
            title_designer_page.click_share()
            title_designer_page.save_as_name('cloud_test')
            title_designer_page.exist(L.title_designer.save_as_template.btn_ok).press()
            login_dz_confirm_dialog = title_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)
            upload_template_dialog = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.upload_description)
            if upload_template_dialog:
                check_result = upload_cloud_dz_page.designer_upload_template.tap_CloseWindow()
            case.result = check_result

        with uuid('19460447-374e-46e2-9f98-08954aa00034') as case:
            # 6. Title Designer
            # 6.1. Save As Template
            # 6.1.1. Enter a Name
            # Add in Custom & check saved template display as settings
            title_designer_page.click_share()
            check_result_1 = title_designer_page.save_as_name('cloud_test')
            title_designer_page.save_as_set_slider(value=0)
            current_slider_value = title_designer_page.exist(L.title_designer.save_as_template.slider).AXValue
            check_result_2 = False if not current_slider_value == 0 else True
            title_designer_page.exist(L.title_designer.save_as_template.btn_ok).press()
            login_dz_confirm_dialog = title_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)

            current_title = upload_cloud_dz_page.designer_upload_template.get_TitleField()
            check_result_3 = False if not current_title == ' cloud_test' else True

            case.result = check_result_1 and check_result_3

        with uuid('799a497e-289d-4a7c-b535-4193411f803d') as case:
            # 6.1. Save As Template
            # 6.1.2. Use the Slider > Min
            # Add in Custom & check saved template display as settings
            case.result = check_result_2

        with uuid('67c85d98-4608-4261-8b0b-425df4070716') as case:
            # 6.2. Step1: Describe Template
            # 6.2.1. Upload > CyberLink Cloud & DirectorZone
            # Upload template correctly & check upload display as settings
            current_upload_to_setting = upload_cloud_dz_page.exist(L.upload_cloud_dz.upload_to).AXTitle
            case.result = False if not current_upload_to_setting == 'CyberLink Cloud and Dir...' else True

            upload_cloud_dz_page.designer_upload_template.edit_Upload_To(upload_option=1)  # upload to CL Cloud

        with uuid('b9aec7f6-1278-4328-bb5b-8b50182b6df5') as case:
            # 6.2. Step1: Describe Template
            # 6.2.2. Cloud > Space Display
            # check display correctly
            case.result = upload_cloud_dz_page.designer_upload_template.check_UsedSpaceInfo()

        with uuid('90faf620-dffd-45a4-86ab-30d39678012c') as case:
            # 6.2. Step1: Describe Template
            # 6.2.3. Info > Details
            # link to related account webpage correctly
            case.result = upload_cloud_dz_page.designer_upload_template.check_DetailsLink()
            time.sleep(DELAY_TIME * 3)

        with uuid('efc8017e-47d0-476f-811c-851f5d433c18') as case:
            # 6.2. Step1: Describe Template
            # 6.2.3. Info > Title
            # check template info display as settings
            case.result = check_result_3

        with uuid('cf3ee9a2-a3ce-421a-8982-430daaed7995') as case:
            # 6.2. Step1: Describe Template
            # 6.2.3. Info > Empty info (SPACE)
            # next button should disable
            upload_cloud_dz_page.designer_upload_template.edit_InputTags(' ')
            upload_cloud_dz_page.designer_upload_template.edit_InputCollection(' ')
            upload_cloud_dz_page.designer_upload_template.edit_InputDescription(' ')

            check_next_btn_status = upload_cloud_dz_page.exist(L.upload_cloud_dz.upload_btn_next).AXEnabled
            case.result = True if not check_next_btn_status else False

        with uuid('e31e1069-9dc9-4b79-ba97-9eb9395437ef') as case:
            # 6.2. Step1: Describe Template
            # 6.2.3. Info > Style
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_ApplyStyle(style=12)  # style: Pets
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_6_2_3-1.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_6_2_3-1.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('d6f4f906-4756-4fb4-9d02-fe63ed37c251') as case:
            # 6.2. Step1: Describe Template
            # 6.2.3. Info > Tags
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_InputTags('bubble')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_6_2_3-2.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_6_2_3-2.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('98fcf99e-4214-4721-b9a7-a9657e3c6afa') as case:
            # 6.2. Step1: Describe Template
            # 6.2.3. Info > Collection
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_InputCollection('cartoon')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_6_2_3-3.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_6_2_3-3.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('739a851d-44ab-4b26-a5bc-3101bd948797') as case:
            # 6.2. Step1: Describe Template
            # 6.2.3. Info > Description
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_InputDescription('for upload test')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_6_2_3-4.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_6_2_3-4.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('c1f743f2-a6c3-4f6f-9478-8c59db6694ab') as case:
            # 6.3. Confirm Copyright Disclaimer
            # 6.3.1. Copyright Display
            # check display correctly
            upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            check_result_1 = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.upload_tick_confirm, timeout=5)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_6_3_1-1.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_6_3_1-1.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('a9f1da7d-35e1-482c-8e28-199ee47618c2') as case:
            # 6.3. Confirm Copyright Disclaimer
            # 6.3.2. I have Confirmed > Untick (Default)
            # disable Next
            check_result = not upload_cloud_dz_page.find(L.upload_cloud_dz.upload_btn_next).AXEnabled
            case.result = check_result

        with uuid('24468b81-0147-4054-981d-022121636286') as case:
            # 6.3. Confirm Copyright Disclaimer
            # 6.3.2. I have Confirmed > Tick
            # continue Next
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_TickConfirm()
            check_result_2 = upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            case.result = check_result_1 and check_result_2

            time.sleep(DELAY_TIME * 3)

        with uuid('59d32abd-ff48-450f-975d-b2f9dd78530c') as case:
            # 6.4. Step2: Upload Progress
            # 6.4.3. Upload Progress > Cancel
            # cancel progress & exit upload
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_ClickCancel()
            check_result_2 = upload_cloud_dz_page.is_not_exist(L.upload_cloud_dz.upload_template_dialog)
            case.result = check_result_1 and check_result_2

        with uuid('acbd308f-0076-4ac7-a1e7-821022b16089') as case:
            # 6.4. Step2: Upload Progress
            # 6.4.3. Upload Progress > Success
            # upload correctly
            title_designer_page.click_share()
            title_designer_page.save_as_name('cloud_test')
            title_designer_page.exist(L.title_designer.save_as_template.btn_ok).press()
            login_dz_confirm_dialog = title_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)
            upload_cloud_dz_page.designer_upload_template.edit_Upload_To(upload_option=1)  # upload to CL Cloud
            upload_cloud_dz_page.designer_upload_template.edit_ApplyStyle(style=12)  # style: Pets
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_InputTags('bubble')
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_InputCollection('cartoon')
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_InputDescription('for upload test')
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            # upload_cloud_dz_page.designer_upload_template.edit_TickConfirm()
            # upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            time.sleep(DELAY_TIME)
            check_result_1 = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.upload_view_CL, timeout=60)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_6_4_3-1.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_6_4_3-1.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)
            check_result_3 = upload_cloud_dz_page.designer_upload_template.edit_ClickFinish()

            case.result = check_result_1 and check_result_2 and check_result_3
            title_designer_page.click_close_btn()

        # kill uploaded template
        time.sleep(DELAY_TIME)
        # main_page.enter_room(1)
        title_room_page.exist_click(L.title_room.btn_import_media)
        title_room_page.exist_click(L.title_room.btn_download_from_DZ_cloud)
        download_from_cl_dz_page.find(L.download_from_cl_dz.template, timeout=20)
        download_from_cl_dz_page.select_template('cloud_test')
        time.sleep(DELAY_TIME)
        download_from_cl_dz_page.tap_delete_button()
        main_page.press_enter_key()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        with uuid('ed8d8bf1-5a3b-4e79-8b0f-c059c5330bdb') as case:
            # 7.2. Step1: Describe Template
            # 7.2.5. Close > [X] button
            # close dialog correctly
            main_page.insert_media('Food.jpg')
            tips_area_page.tools.select_Mask_Designer()
            mask_designer_page.Edit_MaskDesigner_ClickShare()
            mask_designer_page.save_as.input_name('cloud_test')
            mask_designer_page.save_as.click_ok()
            login_dz_confirm_dialog = mask_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)
            upload_template_dialog = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.upload_description)
            if upload_template_dialog:
                check_result = upload_cloud_dz_page.designer_upload_template.tap_CloseWindow()
            case.result = check_result

        with uuid('5b1e4fd2-4b3e-4072-9dff-23d08c4ed617') as case:
            # 7. Mask Designer
            # 7.1. Save As Template
            # 7.1.1. Enter a Name
            # Add in Custom & check saved template display as settings
            mask_designer_page.Edit_MaskDesigner_ClickShare()
            mask_designer_page.save_as.input_name('cloud_test')
            default_slider_value = mask_designer_page.exist(L.mask_designer.save_as_dlg.slider).AXValue
            check_result_2 = False if not default_slider_value == 0.5 else True
            mask_designer_page.save_as.set_slider(value=1)
            current_slider_value = mask_designer_page.exist(L.mask_designer.save_as_dlg.slider).AXValue
            check_result_3 = False if not current_slider_value == 1 else True
            mask_designer_page.save_as.click_ok()
            login_dz_confirm_dialog = mask_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)

            current_title = upload_cloud_dz_page.designer_upload_template.get_TitleField()
            check_result_4 = False if not current_title == ' cloud_test' else True

            case.result = check_result_4

        with uuid('34e79435-e9fa-4be7-a441-a8c7ffd4ca93') as case:
            # 7.1. Save As Template
            # 7.1.2. Use the Slider > Middle (Default)
            # Add in Custom & check saved template display as settings
            case.result = check_result_2

        with uuid('3171226b-78a1-40a1-b66e-44f0d06368bd') as case:
            # 7.1. Save As Template
            # 7.1.2. Use the Slider > Max
            # Add in Custom & check saved template display as settings
            case.result = check_result_3

        with uuid('f14af12b-7da6-4572-a1af-b7664097e33e') as case:
            # 7.2. Step1: Describe Template
            # 7.2.1. Upload > CyberLink Cloud & DirectorZone
            # Upload template correctly & check upload display as settings
            current_upload_to_setting = upload_cloud_dz_page.exist(L.upload_cloud_dz.upload_to).AXTitle
            case.result = False if not current_upload_to_setting == 'CyberLink Cloud and Dir...' else True

            upload_cloud_dz_page.designer_upload_template.edit_Upload_To(upload_option=1)  # upload to CL Cloud

        with uuid('1970d435-6f41-469d-b7bc-998b766c62ba') as case:
            # 7.2. Step1: Describe Template
            # 7.2.2. Cloud > Space Display
            # check display correctly
            case.result = upload_cloud_dz_page.designer_upload_template.check_UsedSpaceInfo()

        with uuid('0037e58a-3507-47ce-9d38-dda65893e441') as case:
            # 7.2. Step1: Describe Template
            # 7.2.3. Info > Details
            # link to related account webpage correctly
            case.result = upload_cloud_dz_page.designer_upload_template.check_DetailsLink()
            time.sleep(DELAY_TIME * 3)

        with uuid('21afa8da-5838-40ed-87f3-77c2ff6083d0') as case:
            # 7.2. Step1: Describe Template
            # 7.2.3. Info > Title
            # check template info display as settings
            case.result = check_result_4

        with uuid('9960e8d6-b59d-45c7-a18d-a2558211668b') as case:
            # 7.2. Step1: Describe Template
            # 7.2.3. Info > Empty info (SPACE)
            # next button should disable
            upload_cloud_dz_page.designer_upload_template.edit_InputTags(' ')
            upload_cloud_dz_page.designer_upload_template.edit_InputCollection(' ')
            upload_cloud_dz_page.designer_upload_template.edit_InputDescription(' ')

            check_next_btn_status = upload_cloud_dz_page.exist(L.upload_cloud_dz.upload_btn_next).AXEnabled
            case.result = True if not check_next_btn_status else False

        with uuid('793eb424-48b2-4af4-870b-2b4922ae7eca') as case:
            # 7.2. Step1: Describe Template
            # 7.2.3. Info > Style
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_ApplyStyle(style=12)  # style: Pets
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_7_2_3-1.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_7_2_3-1.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('b1d4373d-73d4-48fe-989e-e67538f28652') as case:
            # 7.2. Step1: Describe Template
            # 7.2.3. Info > Tags
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_InputTags('bubble')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_7_2_3-2.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_7_2_3-2.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('3b7b76b4-c018-48da-8404-9e89b28477db') as case:
            # 7.2. Step1: Describe Template
            # 7.2.3. Info > Collection
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_InputCollection('cartoon')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_7_2_3-3.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_7_2_3-3.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('d08df2ac-c83f-42a5-960f-1a6cff70895c') as case:
            # 7.2. Step1: Describe Template
            # 7.2.3. Info > Description
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_InputDescription('for upload test')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_7_2_3-4.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_7_2_3-4.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('c09f3c5d-4770-476f-88fe-69ec1afa3371') as case:
            # 7.4. Step2: Upload Progress
            # 7.4.3. Upload Progress > Cancel
            # cancel progress & exit upload
            upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            upload_cloud_dz_page.designer_upload_template.edit_TickConfirm()
            upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            time.sleep(DELAY_TIME)

            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_ClickCancel()
            check_result_2 = upload_cloud_dz_page.is_not_exist(L.upload_cloud_dz.upload_template_dialog)
            case.result = check_result_1 and check_result_2

        with uuid('4a65a45f-b05c-4323-8e8d-dc52d5dceea9') as case:
            # 7.4. Step2: Upload Progress
            # 7.4.3. Upload Progress > Success
            # upload correctly
            mask_designer_page.Edit_MaskDesigner_ClickShare()
            mask_designer_page.save_as.input_name('cloud_test')
            mask_designer_page.save_as.click_ok()
            login_dz_confirm_dialog = mask_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)
            upload_cloud_dz_page.designer_upload_template.edit_Upload_To(upload_option=1)  # upload to CL Cloud
            upload_cloud_dz_page.designer_upload_template.edit_ApplyStyle(style=12)  # style: Pets
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_InputTags('bubble')
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_InputCollection('cartoon')
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_InputDescription('for upload test')
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            # upload_cloud_dz_page.designer_upload_template.edit_TickConfirm()
            # upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            time.sleep(DELAY_TIME)
            check_result_1 = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.upload_view_CL, timeout=60)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_7_4_3-1.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_7_4_3-1.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)
            check_result_3 = upload_cloud_dz_page.designer_upload_template.edit_ClickFinish()

            case.result = check_result_1 and check_result_2 and check_result_3
            mask_designer_page.Edit_MaskDesigner_CloseWindow()

            # kill uploaded template
        time.sleep(DELAY_TIME)
        main_page.enter_room(4)  # enter pip room
        pip_room_page.exist_click(L.pip_room.btn_import_media)
        pip_room_page.exist_click(L.pip_room.btn_download_from_DZ_cloud)
        download_from_cl_dz_page.find(L.download_from_cl_dz.template, timeout=20)
        download_from_cl_dz_page.select_template('cloud_test')
        time.sleep(DELAY_TIME)
        download_from_cl_dz_page.tap_delete_button()
        main_page.press_enter_key()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        with uuid('f522d8e5-6b06-4f97-8f32-4b085017d72c') as case:
            # 8.2. Step1: Describe Template
            # 8.2.5. Close > [X] button
            # close dialog correctly
            main_page.top_menu_bar_plugins_video_collage_designer()
            video_collage_designer_page.click_share()
            video_collage_designer_page.share_to.set_name('cloud_test')
            video_collage_designer_page.share_to.press_ok()
            login_dz_confirm_dialog = video_collage_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)
            upload_template_dialog = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.upload_description)
            if upload_template_dialog:
                check_result = upload_cloud_dz_page.designer_upload_template.tap_CloseWindow()
            case.result = check_result

        with uuid('32c25fb0-e1bb-427f-88ed-3477a36938eb') as case:
            # 8. Video Collage Designer
            # 8.1. Save As Template
            # 8.1.1. Enter a Name
            # Add in Custom & check saved template display as settings
            video_collage_designer_page.click_share()
            check_result_1 = video_collage_designer_page.share_to.set_name('cloud_test')
            default_slider_value = mask_designer_page.exist(L.mask_designer.save_as_dlg.slider).AXValue
            check_result_2 = False if not default_slider_value == 1.0 else True
            mask_designer_page.save_as.set_slider(value=0)
            current_slider_value = mask_designer_page.exist(L.mask_designer.save_as_dlg.slider).AXValue
            check_result_3 = False if not current_slider_value == 0 else True
            video_collage_designer_page.share_to.press_ok()
            login_dz_confirm_dialog = mask_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)

            current_title = upload_cloud_dz_page.designer_upload_template.get_TitleField()
            check_result_4 = False if not current_title == ' cloud_test' else True

            case.result = check_result_1 and check_result_4

        with uuid('26a1080f-0f6f-4f23-8942-ac1b289848ee') as case:
            # 8.1. Save As Template
            # 8.1.2. Use the Slider > Max (Default)
            # Add in Custom & check saved template display as settings
            case.result = check_result_2

        with uuid('28f3a7c9-cc37-41bc-8f7c-bae626fc6776') as case:
            # 8.1. Save As Template
            # 8.1.2. Use the Slider > Min
            # Add in Custom & check saved template display as settings
            case.result = check_result_3

        with uuid('b57f6f66-d3bb-473f-b266-41a5106e6628') as case:
            # 8.2. Step1: Describe Template
            # 8.2.1. Upload > CyberLink Cloud & DirectorZone
            # Upload template correctly & check upload display as settings
            current_upload_to_setting = upload_cloud_dz_page.exist(L.upload_cloud_dz.upload_to).AXTitle
            case.result = False if not current_upload_to_setting == 'CyberLink Cloud and Dir...' else True

            upload_cloud_dz_page.designer_upload_template.edit_Upload_To(upload_option=1)  # upload to CL Cloud

        with uuid('77f0fb98-dc6a-4346-a219-14e3f4713140') as case:
            # 8.2. Step1: Describe Template
            # 8.2.2. Cloud > Space Display
            # check display correctly
            case.result = upload_cloud_dz_page.designer_upload_template.check_UsedSpaceInfo()

        with uuid('451ab8a5-3d91-446c-8de3-14a225d5c5c3') as case:
            # 8.2. Step1: Describe Template
            # 8.2.3. Info > Details
            # link to related account webpage correctly
            case.result = upload_cloud_dz_page.designer_upload_template.check_DetailsLink()
            time.sleep(DELAY_TIME * 3)

        with uuid('4bb5f30d-e8b6-4510-9854-f56276619504') as case:
            # 8.2. Step1: Describe Template
            # 8.2.3. Info > Title
            # check template info display as settings
            case.result = check_result_4

        with uuid('5c4c7237-7238-4f57-b4c8-35f33cdb58cb') as case:
            # 8.2. Step1: Describe Template
            # 8.2.3. Info > Empty info (SPACE)
            # next button should disable
            upload_cloud_dz_page.designer_upload_template.edit_InputTags(' ')
            upload_cloud_dz_page.designer_upload_template.edit_InputCollection(' ')
            upload_cloud_dz_page.designer_upload_template.edit_InputDescription(' ')

            check_next_btn_status = upload_cloud_dz_page.exist(L.upload_cloud_dz.upload_btn_next).AXEnabled
            case.result = True if not check_next_btn_status else False

        with uuid('ab22e663-1299-4fbd-b2c6-1e9964f20f01') as case:
            # 8.2. Step1: Describe Template
            # 8.2.3. Info > Style
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_ApplyStyle(style=12)  # style: Pets
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_8_2_3-1.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_8_2_3-1.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('eeed6d94-1bdc-4bd0-b5e5-9e50074aa8fa') as case:
            # 8.2. Step1: Describe Template
            # 8.2.3. Info > Tags
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_InputTags('bubble')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_8_2_3-2.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_8_2_3-2.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('aef811df-00bf-4ef4-9d19-9818b3c8206f') as case:
            # 8.2. Step1: Describe Template
            # 8.2.3. Info > Collection
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_InputCollection('cartoon')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_8_2_3-3.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_8_2_3-3.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('13326d4a-7f4b-4cb9-aee8-414d1e96a7c2') as case:
            # 8.2. Step1: Describe Template
            # 8.2.3. Info > Description
            # check template info display as settings
            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_InputDescription('for upload test')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_8_2_3-4.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_8_2_3-4.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview, similarity=0.85)

            case.result = check_result_1 and check_result_2

        with uuid('5a548cc0-ced4-4820-a153-a31e48ed6d22') as case:
            # 8.4. Step2: Upload Progress
            # 8.4.3. Upload Progress > Cancel
            # cancel progress & exit upload
            upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            upload_cloud_dz_page.designer_upload_template.edit_TickConfirm()
            upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            time.sleep(DELAY_TIME)

            check_result_1 = upload_cloud_dz_page.designer_upload_template.edit_ClickCancel()
            check_result_2 = upload_cloud_dz_page.is_not_exist(L.upload_cloud_dz.upload_template_dialog)
            case.result = check_result_1 and check_result_2

        with uuid('23da3814-d71f-42d7-b4b8-ba46f259f0a0') as case:
            # 8.4. Step2: Upload Progress
            # 8.4.3. Upload Progress > Success
            # upload correctly
            video_collage_designer_page.click_share()
            video_collage_designer_page.share_to.set_name('cloud_test')
            video_collage_designer_page.share_to.press_ok()
            login_dz_confirm_dialog = video_collage_designer_page.is_exist(
                {'AXIdentifier': 'IDC_LOGIN_DZ_WITH_CLOUD_DIALOG_WINDOW'})
            if login_dz_confirm_dialog:
                upload_cloud_dz_page.set_AutoSignIn_To_DZ()
                time.sleep(DELAY_TIME * 5)
            upload_cloud_dz_page.designer_upload_template.edit_Upload_To(upload_option=1)  # upload to CL Cloud
            upload_cloud_dz_page.designer_upload_template.edit_ApplyStyle(style=12)  # style: Pets
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_InputTags('bubble')
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_InputCollection('cartoon')
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_InputDescription('for upload test')
            time.sleep(DELAY_TIME)
            upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            # upload_cloud_dz_page.designer_upload_template.edit_TickConfirm()
            # upload_cloud_dz_page.designer_upload_template.edit_ClickNext()
            time.sleep(DELAY_TIME)
            check_result_1 = upload_cloud_dz_page.is_exist(L.upload_cloud_dz.upload_view_CL, timeout=60)

            image_full_path = Auto_Ground_Truth_Folder + 'UL_cloud_dz_8_4_3-1.png'
            ground_truth = Ground_Truth_Folder + 'UL_cloud_dz_8_4_3-1.png'
            current_preview = upload_cloud_dz_page.snapshot(
                locator=L.upload_cloud_dz.upload_template_dialog, file_name=image_full_path)
            check_result_2 = upload_cloud_dz_page.compare(ground_truth, current_preview)
            check_result_3 = upload_cloud_dz_page.designer_upload_template.edit_ClickFinish()

            case.result = check_result_1 and check_result_2 and check_result_3

            video_collage_designer_page.layout.select_category(index=1)  # select 'Custom' category
            video_collage_designer_page.layout.remove_layout(index=1)
            video_collage_designer_page.layout.remove_layout(index=1)
            video_collage_designer_page.layout.remove_layout(index=1)
            video_collage_designer_page.exist_click(L.video_collage_designer.layout.library.btn_close)

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_1(self):
        with uuid('39d1b5cf-79e3-4329-8a4f-30eebf4b3492') as case:
            # 10. Produce: Upload a copy to CyberLink Cloud
            # 10.1. File Extension > 2D > H.264 AVC
            # upload a copy to CyberLink Cloud correctly
            # Import image > Select template "Y main.m2ts" to track1
            time.sleep(DELAY_TIME * 3)
            video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
            media_room_page.collection_view_right_click_import_media_files(video_path)
            time.sleep(DELAY_TIME * 2)
            main_page.insert_media('Y man.mp4')

            main_page.click_produce()
            in_produce_page = produce_page.check_enter_produce_page()
            if in_produce_page:
                produce_page.local.select_file_format('avc')
                produce_page.local.set_check_upload_copy_to_cyberlink_cloud()
                produce_page.select_output_folder(Test_Material_Folder + 'cloud_test/Produce')
                produce_page.exist_click(L.produce.btn_start_produce)
                produce_page.local.click_option_convert_cyberlink_cloud_copy_to_mp4_dialog(option=1)
                produce_finish = produce_page.is_exist(L.produce.btn_back_to_edit_after_upload_cl, timeout=30)
                if produce_finish:
                    check_result_1 = produce_page.is_exist(L.produce.txt_produce_and_upload_complete)
                    check_result_2 = produce_page.is_exist(L.produce.btn_view_on_cloud_hyperlink)
                else:
                    logger('produce & upload to cloud fail')
            else:
                logger('did not enter produce page')

            case.result = check_result_1 and check_result_2
            # back to edit mode and delete produced file
            produce_page.exist_click(L.produce.btn_back_to_edit_after_upload_cl)
            time.sleep(2)
            media_room_page.hover_library_media('Produce.mp4')
            main_page.right_click()
            main_page.select_right_click_menu('Move to Trash Can')

        with uuid('db0b0c89-6f55-4252-bd06-64aa2c36628c') as case:
            # 10.1. File Extension > 2D > H.265 HEVC
            # upload a copy to CyberLink Cloud correctly
            main_page.click_produce()
            in_produce_page = produce_page.check_enter_produce_page()
            if in_produce_page:
                produce_page.local.select_file_format('hevc')
                produce_page.local.set_check_upload_copy_to_cyberlink_cloud()
                produce_page.select_output_folder(Test_Material_Folder + 'cloud_test/Produce')
                produce_page.exist_click(L.produce.btn_start_produce)
                produce_page.local.click_option_convert_cyberlink_cloud_copy_to_mp4_dialog(option=1)
                produce_finish = produce_page.is_exist(L.produce.btn_back_to_edit_after_upload_cl, timeout=30)
                if produce_finish:
                    check_result_1 = produce_page.is_exist(L.produce.txt_produce_and_upload_complete)
                    check_result_2 = produce_page.is_exist(L.produce.btn_view_on_cloud_hyperlink)
                else:
                    logger('produce & upload to cloud fail')
            else:
                logger('did not enter produce page')

            case.result = check_result_1 and check_result_2
            # back to edit mode and delete produced file
            produce_page.exist_click(L.produce.btn_back_to_edit_after_upload_cl)
            time.sleep(2)
            media_room_page.hover_library_media('Produce.mp4')
            main_page.right_click()
            main_page.select_right_click_menu('Move to Trash Can')

        with uuid('679fcaf0-798b-41af-a590-7ba461c7a705') as case:
            # 10.1. File Extension > 2D > XAVC S
            # upload a copy to CyberLink Cloud correctly
            main_page.click_produce()
            in_produce_page = produce_page.check_enter_produce_page()
            if in_produce_page:
                produce_page.local.select_file_format('xavc_s')
                produce_page.local.set_check_upload_copy_to_cyberlink_cloud()
                produce_page.select_output_folder(Test_Material_Folder + 'cloud_test/Produce')
                produce_page.exist_click(L.produce.btn_start_produce)
                produce_page.local.click_option_convert_cyberlink_cloud_copy_to_mp4_dialog(option=1)
                produce_finish = produce_page.is_exist(L.produce.btn_back_to_edit_after_upload_cl, timeout=30)
                if produce_finish:
                    check_result_1 = produce_page.is_exist(L.produce.txt_produce_and_upload_complete)
                    check_result_2 = produce_page.is_exist(L.produce.btn_view_on_cloud_hyperlink)
                else:
                    logger('produce & upload to cloud fail')
            else:
                logger('did not enter produce page')

            case.result = check_result_1 and check_result_2
            # back to edit mode and delete produced file
            produce_page.exist_click(L.produce.btn_back_to_edit_after_upload_cl)
            time.sleep(2)
            media_room_page.hover_library_media('Produce.mp4')
            main_page.right_click()
            main_page.select_right_click_menu('Move to Trash Can')

        with uuid('44eccce3-dac6-4535-ab73-dc55a93fffbe') as case:
            # 10.2. Convert to MP4 video > Yes
            # convert video correctly
            case.result = check_result_1 and check_result_2

        with uuid('ef508495-f3d9-463d-a00c-062d501b7855') as case:
            # 10.2. Convert to MP4 video > No
            # do not convert video
            main_page.click_produce()
            in_produce_page = produce_page.check_enter_produce_page()
            if in_produce_page:
                produce_page.local.select_file_format('xavc_s')
                produce_page.local.set_check_upload_copy_to_cyberlink_cloud()
                produce_page.select_output_folder(Test_Material_Folder + 'cloud_test/Produce')
                produce_page.click(L.produce.btn_start_produce)
                produce_page.local.click_option_convert_cyberlink_cloud_copy_to_mp4_dialog(option=0)
                produce_finish = produce_page.is_exist(L.produce.btn_back_to_edit_after_upload_cl, timeout=30)
                if produce_finish:
                    check_result_1 = produce_page.is_exist(L.produce.txt_produce_and_upload_complete)
                    check_result_2 = produce_page.is_exist(L.produce.btn_view_on_cloud_hyperlink)
                else:
                    logger('produce & upload to cloud fail')
            else:
                logger('did not enter produce page')

            case.result = check_result_1 and check_result_2

            # back to edit mode and delete produced file
            produce_page.exist_click(L.produce.btn_back_to_edit_after_upload_cl)
            time.sleep(2)
            media_room_page.hover_library_media('Produce.mp4')
            main_page.right_click()
            main_page.select_right_click_menu('Move to Trash Can')

        with uuid('9485e89d-ad4f-4528-a3af-4d78df9f862b') as case:
            # 10.3. Producing Movie > Cancel Rendering
            main_page.select_library_icon_view_media('Y man.mp4')
            tips_area_page.click_TipsArea_btn_insert(1)
            time.sleep(DELAY_TIME)
            # cancel rending
            main_page.click_produce()
            in_produce_page = produce_page.check_enter_produce_page()
            if in_produce_page:
                produce_page.local.select_file_format('xavc_s')
                produce_page.local.select_profile_name(9)
                time.sleep(DELAY_TIME)
                produce_page.local.set_check_upload_copy_to_cyberlink_cloud()
                produce_page.select_output_folder(Test_Material_Folder + 'cloud_test/Produce')
                produce_page.click(L.produce.btn_start_produce)
                produce_page.local.click_option_convert_cyberlink_cloud_copy_to_mp4_dialog(option=1)
                for number_of_checks in range(10):
                    btn_cancel_rendering = produce_page.exist(L.produce.btn_cancel_rendering, timeout=10).AXEnabled
                    if not btn_cancel_rendering:
                        time.sleep(DELAY_TIME)
                        continue
                    check_result_1 = produce_page.click_cancel_rendering()
                    produce_page.click_confirm_cancel_rendering_dialog_yes()
                    break
                check_result_2 = produce_page.is_not_exist(L.produce.btn_pause_produce, timeout=10)
            else:
                logger('did not enter produce page')
            case.result = check_result_1 and check_result_2

        with uuid('c25ae962-73af-4cee-b898-aa41356bde84') as case:
            # 10.4. Uploading to CyberLink Cloud > Cancel Upload
            # cancel upload
            produce_page.local.select_file_format('xavc_s')
            produce_page.local.set_check_upload_copy_to_cyberlink_cloud()
            produce_page.exist_click(L.produce.btn_start_produce)
            produce_page.local.click_option_convert_cyberlink_cloud_copy_to_mp4_dialog(option=1)
            check_result_1 = False
            for number_of_checks in range(200):
                btn_cancel_rendering = produce_page.exist(L.produce.btn_cancel_rendering).AXEnabled
                if btn_cancel_rendering:
                    time.sleep(DELAY_TIME)
                    continue
                check_result_1 = produce_page.click_cancel_upload_video()
                logger(check_result_1)
                break
            check_result_2 = produce_page.is_not_exist(L.produce.btn_cancel_upload, timeout=30)

            case.result = check_result_1 and check_result_2

            # back to edit mode and delete produced file
            produce_page.exist_click(L.produce.btn_back_to_edit_after_upload_cl)
            time.sleep(3)
            media_room_page.handle_high_definition_dialog()
            time.sleep(1)
            media_room_page.hover_library_media('Produce.mp4')
            main_page.right_click()
            main_page.select_right_click_menu('Move to Trash Can')

            # remove uploaded content
            time.sleep(DELAY_TIME)
            media_room_page.import_media_from_cyberlink_cloud()
            time.sleep(DELAY_TIME*6)
            download_from_cl_dz_page.set_search_text('powerdirector')
            time.sleep(DELAY_TIME)
            import_media_from_cloud_page.tap_select_deselect_all_btn()
            time.sleep(DELAY_TIME)
            delete_btn_enabled = import_media_from_cloud_page.exist(
                L.import_downloaded_media_from_cl.delete_btn).AXEnabled
            if delete_btn_enabled:
                download_from_cl_dz_page.exist_click(L.import_downloaded_media_from_cl.delete_btn)
                download_from_cl_dz_page.download_project.handle_warning_msg(option='ok')
                delete_btn_status = import_media_from_cloud_page.exist(
                    L.import_downloaded_media_from_cl.delete_btn, timeout=10).AXEnabled
                if not delete_btn_status:
                    download_from_cl_dz_page.tap_close_button()
            else:
                download_from_cl_dz_page.tap_close_button()

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    6bc22249-112e-489f-8a36-f333e1c8a36a
                    a1692509-61b7-43be-a98d-ddf47c7920fc
                    45df9120-7bcd-4c81-901d-2743950397f0
                    5e2879c7-ec43-42da-b730-a530339ecee3
                    1b98d6b6-f5ca-4c35-bdc0-2a08eb265d9d
                    22651035-206b-4ae8-bdd9-3dc19d57e9e3
                    22ff1ca1-ebe4-4285-a7c3-6baee0645564
                    08bec424-6f33-4326-bbc8-098a8cb68d89
                    dea37658-68e1-45b1-9aaf-903b77b2cd3e
                    c4529aeb-32b1-42a9-bc02-76723dc52649
                    38a6caf9-13b8-4916-a448-5fe8f53f4ee8
                    1349b5a0-cb0c-4b3e-83bc-c4c5acb6b126
                    a8207bba-83ae-4ad9-9221-5e564095e566
                    23fc548b-9a94-4683-a55c-7f6b74ae4355
                    3cd2385d-037c-4d12-ab6d-04db6e45ab1d
                    38de28a1-d941-4241-a08a-268b1cb33356
                    21f65e35-f2f1-4936-8bc5-abe5a53706bf
                    ab14e350-6892-44e8-912a-ccdbd44318dd
                    a08fe177-9718-4f09-8c9c-d1db4782e6db
                    e6df569f-e206-4463-81b2-2dc731f97988
                    77914dc8-9a67-48d7-b376-8c3b631d607b
                    2135a6ee-e588-4de6-b569-370803019b0d
                    566df432-b23d-422f-be64-96d3a5840b3c
                    1072596c-f830-45cb-b200-48b9b203dca8
                    0bb6fcfb-a11d-46b3-af74-b70ea133d636
                    94bfa32d-b45a-44fe-8d5c-a14b0e636f1a
                    43d3c3e4-5c70-4c1a-a5c3-b1cbf982a731
                    4e9688a0-49b2-4e65-b0f9-356e24fea6ce
                    5bb5a977-3204-4783-bd2a-bdb7c5e30006
                    e2dad135-73c1-4788-836d-541a13f2ee97
                    c26afaf2-1ac6-4305-835a-2e1ac98f3bb7
                    663154ad-0fd2-4e32-ac00-4a8d54ce2fd6
                    af9bf8ff-fe27-468d-92f7-173f0b4b5ba0
                    6da7e369-498e-4bde-a450-81a4f2841d2b
                    6465ceb4-2db8-4f36-a61d-a4b8b47bcc14
                    456eb016-203e-48ad-9967-53e2ffb332bb
                    110aa0b7-5a17-4020-9ff4-6952b4a6e543
                    d37d29dd-adb5-4d31-80bd-a5944d6049cb
                    9613623c-a80a-43b1-a2e6-f5501e3245ca
                    ed67ff11-a8e6-4128-9374-7fd6f58263ea
                    7f4182aa-8c3a-448a-98f3-e82633f5cff3
                    bcd4004b-5da7-40ad-9d68-35dcc182ff6d
                    c0438662-e125-4f96-9208-86c80736e9c6
                    69c20104-0126-49a7-9dc6-a6da84c74f1a
                    5c290c01-51ff-44c4-ac41-1c98d22ce17f
                    b7442423-0b3a-4a66-b93b-8583fcdbd855
                    ed73abb6-3c1f-44c7-b8f5-669d227c44f0
                    4296c90d-0138-4176-af78-46c07a765f02
                    b35c3531-7264-4ecf-87b0-88d46451ae23
                    2b72c1d3-4782-4624-a4a3-64887c8c8385
                    74426591-edc3-46f5-b017-42e1c445ced4
                    7313b2ae-5d7b-4cdd-a684-1b3e24e9d0c4
                    55a493f7-b7ef-4cc9-9288-bafe05b984fc
                    e880d260-30d4-4871-9a7c-df686549232d
                    052d9076-8c40-4129-a714-43e0de2bb262
                    49c80b88-2e55-4b84-bb23-aac373224e3d
                    46174331-eab4-492e-b825-e6edfd0707ab
                    460a43ff-381c-4fce-b036-4618ec9588bb
                    8c0f884b-6065-4a04-9586-319259d5de67
                    9d95b1c0-2f1d-4473-87f1-53a1c1b85814
                    c82bfddb-4e3c-4d41-a709-c797bffe0db6
                    4092f7ea-7667-4b0f-90d0-135f47811ff7
                    e3a0cdfa-391d-4971-9455-291704f5b082
                    a47bf4dc-c588-4017-a407-da571e77051b
                    b65af3c6-e7c0-4dda-8031-a67b03fb16d2
                    be56ec21-f7ec-4204-95c6-21eace10ea41
                    2cdbebe9-a5c4-4fe9-a260-0baf46a9cbfc
                    b66d59b8-f9ef-44ba-ba7a-28cfaa27c688
                    ecfee417-cfed-41cc-986f-d8c5b30dbda6
                    327df233-1501-4c42-bf7f-dbfcb721ecf4
                    b5d80e86-6543-4c02-b879-e67934956efc
                    f2b9c3df-16e6-4f67-b184-3ef6664d6187
                    e2e904fe-c392-4936-8e41-c1d403c74b88
                    62e346b8-4831-455f-a935-3924ed9e335d
                    7c44b4cd-d416-40da-b075-f7ac67d8f0f4
                    527b6192-a363-4085-a4fc-638b16ddb2e1
                    23a436eb-e082-497a-af5e-2f44f61a14ef
                    59881f4d-8d92-4668-811a-1fbca250914d
                    9cfa0771-c574-46df-a321-62b163cfafcd
                    f13c2e37-c851-489b-b6fd-450a4acc852f
                    9b63943a-a039-47c4-a780-cb457ec287a7
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'

