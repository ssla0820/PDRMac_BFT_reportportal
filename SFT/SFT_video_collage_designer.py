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
video_collage_designer_page = PageFactory().get_page_object('video_collage_designer_page', mwc)
preferences_page = PageFactory().get_page_object('preferences_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Video Collage.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Video_Collage_Designer/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Video_Collage_Designer/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Video_Collage_Designer():
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
            google_sheet_execution_log_init('Video_Collage_Designer')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"video collage designer result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        with uuid('7a8b416d-092c-49bd-8b49-3df64de2d1d9') as case:
            # 1. General
            # 1.1. Entry Point
            # 1.1.1. [Plug-ins] tab -> Video Collage > 4:3 Project
            # show the function and enter designer page correctly
            main_page.set_project_aspect_ratio_4_3()
            main_page.top_menu_bar_plugins_video_collage_designer()

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_1_1_1_1.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)
            case.result = check_result

            video_collage_designer_page.press_esc_key()

        with uuid('3854b5fb-98e7-43fe-8b95-33dc2491a821') as case:
            # 1.1. Entry Point
            # 1.1.1. [Plug-ins] tab -> Video Collage > 9:16 Project
            # show the function and enter designer page correctly
            main_page.set_project_aspect_ratio_9_16()
            main_page.top_menu_bar_plugins_video_collage_designer()

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_1_1_1_2.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)
            case.result = check_result

            video_collage_designer_page.press_esc_key()

        with uuid('92bb690f-e445-4706-8a5c-f19c76490f57') as case:
            # 1.1. Entry Point
            # 1.1.1. [Plug-ins] tab -> Video Collage > 1:1 Project
            # show the function and enter designer page correctly
            main_page.set_project_aspect_ratio_1_1()
            main_page.top_menu_bar_plugins_video_collage_designer()

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_1_1_1_3.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)
            case.result = check_result

            video_collage_designer_page.press_esc_key()

        with uuid('dbeed3d5-5f63-4a5c-963f-4804d1fade78') as case:
            # 1.1. Entry Point
            # 1.1.1. [Plug-ins] tab -> Video Collage > 16:9 Project
            # show the function and enter designer page correctly
            main_page.set_project_aspect_ratio_16_9()
            main_page.top_menu_bar_plugins_video_collage_designer()

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_1_1_1_4.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)
            case.result = check_result

            video_collage_designer_page.press_esc_key()

        with uuid('b0370a0c-50a8-4884-8507-86ca1ccad27e') as case:
            # 1.2. Preference Settings
            # 1.2.2. Shadow file > Enable
            # show shadow icon and preview is fine
            main_page.click_set_user_preferences()
            preferences_page.general.enable_shadow_file_set_check(1)
            preferences_page.click_ok()
            main_page.top_menu_bar_plugins_video_collage_designer()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_1_2_2_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_1_2_2_1.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

            video_collage_designer_page.press_esc_key()

        with uuid('37142f52-8a6e-4fb9-ada9-f4d332fd8c43') as case:
            # 1.2. Preference Settings
            # 1.2.2. Shadow file > Disable (default)
            # no shadow icon and preview is fine
            main_page.click_set_user_preferences()
            preferences_page.general.enable_shadow_file_set_check(0)
            preferences_page.click_ok()
            main_page.top_menu_bar_plugins_video_collage_designer()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_1_2_2_2.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_1_2_2_2.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('83c1b314-f500-4948-9a8d-377b97f557c4') as case:
            # 2. Main UI
            # 2.1. Caption Bar
            # 2.1.1. Function Name
            # show function name correctly
            check_title = video_collage_designer_page.exist(L.video_collage_designer.main_window).AXTitle

            case.result = False if not check_title == 'Video Collage Designer' else True

        with uuid('0c5508b4-de3a-4c6d-a806-c0e8b17cad9c') as case:
            # 2.1. Caption Bar
            # 2.1.3. Window > Maximum
            # maximum the designer window directly
            video_collage_designer_page.layout.library.click_zoom()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_1_3_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_1_3_1.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.base.main_window, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('d30d22c2-58d7-4697-9f96-c4cc1c78dd78') as case:
            # 2.1. Caption Bar
            # 2.1.3. Window > Restore Down
            # restore down the window directly
            video_collage_designer_page.layout.library.click_zoom()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_1_3_2.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_1_3_2.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.base.main_window, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('e7a52f79-1c17-49fb-a002-c6a433fbed73') as case:
            # 2.1. Caption Bar
            # 2.1.4. [X] button > w/o adjustment
            # close dialog directly
            video_collage_designer_page.exist_click(L.video_collage_designer.layout.library.btn_close)

            check_result = video_collage_designer_page.exist(L.video_collage_designer.main_window)
            case.result = True if not check_result else False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid('558d505f-fee3-40f7-a714-2df032ae47de') as case:
            # 2.2. Media Library
            # 2.2.1. Import Media > Image > bmp
            # image displays in slot correctly after import into library
            media_room_page.collection_view_right_click_empty_library()
            main_page.top_menu_bar_plugins_video_collage_designer()
            video_collage_designer_page.media.select_category(2)
            video_collage_designer_page.media.import_media(Test_Material_Folder + 'video_collage/' + 'BMP.bmp')

            check_result_1 = video_collage_designer_page.media.is_exist_media('BMP.bmp')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_1_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_1_1.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('6a2f8be6-4dbd-41f3-b0cc-091ccef9e3a6') as case:
            # 2.2. Media Library
            # 2.2.1. Import Media > Image > jpg / jpeg / jpe
            # image displays in slot correctly after import into library
            video_collage_designer_page.media.import_media(Test_Material_Folder + 'video_collage/' + 'JPG.jpg')

            check_result_1 = video_collage_designer_page.media.is_exist_media('JPG.jpg')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_1_2.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_1_2.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            check_result_jpg = check_result_1 and check_result_2

            video_collage_designer_page.media.import_media(Test_Material_Folder + 'video_collage/' + 'JPE.jpe')

            check_result_1 = video_collage_designer_page.media.is_exist_media('JPE.jpe')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_1_3.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_1_3.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            check_result_jpe = check_result_1 and check_result_2
            case.result = check_result_jpg and check_result_jpe

        with uuid('4ccc5207-1f9e-4ac6-a320-be66982c2798') as case:
            # 2.2. Media Library
            # 2.2.1. Import Media > Image > png
            # image displays in slot correctly after import into library
            video_collage_designer_page.media.import_media(Test_Material_Folder + 'video_collage/' + 'PNG.png')

            check_result_1 = video_collage_designer_page.media.is_exist_media('PNG.png')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_1_4.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_1_4.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('588692a1-bd89-4db0-b1f7-150d2ab4c30d') as case:
            # 2.2. Media Library
            # 2.2.1. Import Media > Image > gif
            # image displays in slot correctly after import into library
            video_collage_designer_page.media.import_media(Test_Material_Folder + 'video_collage/' + 'GIF.gif')

            check_result_1 = video_collage_designer_page.media.is_exist_media('GIF.gif')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_1_5.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_1_5.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('c1bd4048-c302-421b-bd59-2c01b0655846') as case:
            # 2.2. Media Library
            # 2.2.1. Import Media > Image > tif / tiff
            # image displays in slot correctly after import into library
            video_collage_designer_page.media.import_media(Test_Material_Folder + 'video_collage/' + 'TIFF.tiff')

            check_result_1 = video_collage_designer_page.media.is_exist_media('TIFF.tiff')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_1_6.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_1_6.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('30d000be-4c35-45ea-bd27-1cb9a6bb7818') as case:
            # 2.2. Media Library
            # 2.2.1. Import Media > Image > Raw file
            # image displays in slot correctly after import into library
            video_collage_designer_page.media.import_media(Test_Material_Folder + 'video_collage/' + 'CR2.cr2')

            check_result_1 = video_collage_designer_page.media.is_exist_media('CR2.jpg')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_1_7.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_1_7.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            check_result_cr2 = check_result_1 and check_result_2
            time.sleep(DELAY_TIME * 3)

            video_collage_designer_page.media.import_media(Test_Material_Folder + 'video_collage/' + 'NEF.nef')

            check_result_1 = video_collage_designer_page.media.is_exist_media('NEF.jpg')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_1_8.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_1_8.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            check_result_nef = check_result_1 and check_result_2
            case.result = check_result_cr2 and check_result_nef

            time.sleep(DELAY_TIME * 3)

        with uuid('d9a91260-2da7-4b00-9abe-cd13dbd76ade') as case:
            # 2.2. Media Library
            # 2.2.1. Import Media > Vertical > Image
            # image displays in slot correctly after import into library
            case.result = check_result_nef

        with uuid('759291d2-001b-41fb-bf22-debca03d892d') as case:
            # 2.2. Media Library
            # 2.2.1. Import Media > Image > HEIC
            # image displays in slot correctly after import into library
            video_collage_designer_page.media.import_media(Test_Material_Folder + 'video_collage/' + 'HEIC.heic')

            check_result_1 = video_collage_designer_page.media.is_exist_media('HEIC.heic')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_1_9.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_1_9.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('1f9fb158-b3fc-45ea-b18f-1ab8f70eb94e') as case:
            # 2.2. Media Library
            # 2.2.2. Filter Option > Images
            # image all can show under this setting
            case.result = check_result_2

        with uuid('8a52e0bf-49bb-4317-9ded-414519453a19') as case:
            # 2.2. Media Library
            # 2.2.1. Import Media > Video > H264 mp4 / mts / m2t / m2ts
            # image displays in slot correctly after import into library
            video_collage_designer_page.media.select_category(1)
            video_collage_designer_page.media.import_media(Test_Material_Folder + 'video_collage/' + 'H264.mp4')

            check_result_1 = video_collage_designer_page.media.is_exist_media('H264.mp4')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_1_10.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_1_10.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            check_result_h264 = check_result_1 and check_result_2

            video_collage_designer_page.media.import_media(Test_Material_Folder + 'video_collage/' + 'M2TS.m2ts')

            check_result_1 = video_collage_designer_page.media.is_exist_media('M2TS.m2ts')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_1_11.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_1_11.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            check_result_m2ts = check_result_1 and check_result_2
            case.result = check_result_h264 and check_result_m2ts

        with uuid('7137d409-8ef6-44a2-81cb-0774aa4fa4c1') as case:
            # 2.2. Media Library
            # 2.2.1. Import Media > Video > H265 HEVC
            # image displays in slot correctly after import into library
            video_collage_designer_page.media.import_media(Test_Material_Folder + 'video_collage/' + 'H265.mp4')

            check_result_1 = video_collage_designer_page.media.is_exist_media('H265.mp4')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_1_12.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_1_12.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('25b83705-c781-4997-8925-0fb34cdbfe4b') as case:
            # 2.2. Media Library
            # 2.2.1. Import Media > 4K source
            # image displays in slot correctly after import into library
            video_collage_designer_page.media.import_media(Test_Material_Folder + 'video_collage/' + '4K.mp4')

            check_result_1 = video_collage_designer_page.media.is_exist_media('4K.mp4')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_1_13.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_1_13.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('dd538836-5308-49f6-b01d-6f1a149efc59') as case:
            # 2.2. Media Library
            # 2.2.1. Import Media > Vertical > Video
            # image displays in slot correctly after import into library
            video_collage_designer_page.media.import_media(Test_Material_Folder + 'video_collage/' + 'Portrait.mp4')

            check_result_1 = video_collage_designer_page.media.is_exist_media('Portrait.mp4')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_1_14.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_1_14.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('06269438-0d65-458e-838c-39047b65b968') as case:
            # 2.2. Media Library
            # 2.2.2. Filter Option > Video
            # video clips all can show under this setting
            case.result = check_result_2

        with uuid('d7d3fc19-8a6c-40e9-9559-1f9e8a09c9a7') as case:
            # 2.2. Media Library
            # 2.2.2. Filter Option > Color Board
            # show different color board under this setting
            video_collage_designer_page.media.select_category(3)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_2_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_2_1.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('798d8add-1bb3-4c5a-98bd-ff7eb2ae4817') as case:
            # 2.2. Media Library
            # 2.2.2. Filter Option > All Media
            # show all media source
            video_collage_designer_page.media.select_category(0)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_2_2.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_2_2.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('3cd64ae7-8867-4f5f-830d-d71fe483fff0') as case:
            # 2.2. Media Library
            # 2.2.3. Fill the slots from media room > Click [Auto fill...] button
            # auto fill the empty slots from media room
            video_collage_designer_page.media.click_auto_fill()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_3_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_3_1.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.main_window, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('63817854-ce7f-41cc-90af-72f5651130a0') as case:
            # 2.2. Media Library
            # 2.2.6. Library Panel adjustment
            # can adjust the width of media room
            video_collage_designer_page.adjust_splitter(+200)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_6_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_6_1.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.main_window, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('37e1f15d-7c70-4ea4-9073-de3539a292d7') as case:
            # 2.2. Media Library
            # 2.2.7. Hotkey > Multi select (Command +)
            # select files correctly
            video_collage_designer_page.media.select_multiple_media('4K.mp4', 'BMP.bmp', 'H264.mp4', 'CR2.jpg')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_7_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_7_1.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('2492120a-d7a9-4a63-ab3f-4f6e805ec3b6') as case:
            # 2.2. Media Library
            # 2.2.7. Hotkey > Select all (Command + a)
            # select files correctly
            video_collage_designer_page.tap_SelectAll_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_7_2.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_7_2.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('0a2387ea-db37-4f61-a461-3a63a2c6b45b') as case:
            # 2.2. Media Library
            # 2.2.7. Hotkey > Remove (Del key)
            # select files correctly
            video_collage_designer_page.press_del_key()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_2_7_3.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_2_7_3.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid('4c816a6f-30b1-40b6-b125-ec0730e9fad6') as case:
            # 2.3. layout
            # 2.3.1. layout Panel > Template > Free download
            # open DZ page if clicking
            # AT limitation
            case.result = None
            case.fail_log = "AT limitation"

        with uuid('263bba95-304f-4e68-84db-c39cdb93ad46') as case:
            # 2.3. layout
            # 2.3.1. layout Panel > Template > Build-in layout (30)
            # preview is correct after selecting other layouts
            main_page.top_menu_bar_plugins_video_collage_designer()
            check_result_1 = video_collage_designer_page.layout.hover_layout(30)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_1_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_1_1.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.frame, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('9b473bfc-b9e3-41fc-b84c-04acf7b48d58') as case:
            # 2.3. layout
            # 2.3.1. layout Panel > Scroll > '<'
            # Scroll layout panel directly
            for i in range(4):
                video_collage_designer_page.layout.click_scroll_left()
                time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_1_2.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_1_2.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.frame, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('995bf1dd-6d39-4cd9-be15-0f86748c2153') as case:
            # 2.3. layout
            # 2.3.1. layout Panel > Scroll > '>'
            # Scroll layout panel directly
            for i in range(4):
                video_collage_designer_page.layout.click_scroll_right()
                time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_1_3.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_1_3.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.frame, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('50a520ae-0101-4948-9bdf-2dd883c72aff') as case:
            # 2.3. layout
            # 2.3.1. layout Panel > Template > Custom layout
            # custom template is located at the left side of build-in layout
            video_collage_designer_page.border.set_interclip_value('50')
            video_collage_designer_page.click_save_as_with_name('custom_collage')

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_1_4.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_1_4.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.frame, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('300ad9cf-bb21-45ae-b43b-e9f8711f9fa8') as case:
            # 2.3. layout
            # 2.3.1. layout Panel > Choose layout > Downloaded
            # show correct category to match setting
            video_collage_designer_page.layout.select_category(2)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_1_5.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_1_5.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.frame, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('8e10a345-b6e8-457c-991d-477dfff67d9f') as case:
            # 2.3. layout
            # 2.3.1. layout Panel > Choose layout > Custom
            # show correct category to match setting
            video_collage_designer_page.layout.select_category(1)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_1_6.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_1_6.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.frame, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('6acb2784-443a-406b-9945-55d7a0716880') as case:
            # 2.3. layout
            # 2.3.1. layout Panel > Delete layout > Custom
            # layout can be deleted from right click menu
            video_collage_designer_page.layout.remove_layout(1)
            video_collage_designer_page.layout.click_remove_yes()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_1_7.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_1_7.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.frame, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('6ed4a362-09b4-4534-b0bf-80e9eca2f961') as case:
            # 2.3. layout
            # 2.3.1. layout Panel > Delete layout > Downloaded
            # layout can be deleted from right click menu
            # AT limitation, cannot download layout template from DZ
            case.result = None
            case.fail_log = "AT limitation"

        with uuid('c4948e4a-881c-46bf-afcb-53081586aa51') as case:
            # 2.3. layout
            # 2.3.1. layout Panel > Choose layout > All
            # show correct category to match setting
            video_collage_designer_page.layout.select_category(0)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_1_8.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_1_8.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.frame, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('5e85e794-14dd-4bea-8a2a-b5bbe9c5ba2a') as case:
            # 2.3. layout
            # 2.3.1. layout Panel > View collage template library
            # prompt to display collage templates dialog entirely
            video_collage_designer_page.border.set_interclip_value('50')
            video_collage_designer_page.click_save_as_with_name('custom_collage')

            check_result_1 = video_collage_designer_page.layout.open_layout_library()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_1_8.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_1_8.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.library.frame, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('92fbd30a-c133-4f67-96b4-b8b476ce4d98') as case:
            # 2.3. layout
            # 2.3.2. Collage template library > Category > Downloaded
            # show correct category to match setting
            check_result_1 = video_collage_designer_page.layout.library.select_category(2)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_2_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_2_1.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.library.frame, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('b5c0cade-3041-4951-ae8f-b78fa2c90125') as case:
            # 2.3. layout
            # 2.3.2. Collage template library > Category > Custom
            # show correct category to match setting
            check_result_1 = video_collage_designer_page.layout.library.select_category(1)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_2_2.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_2_2.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.library.frame, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('99f59d02-ca16-41ac-a72a-f1ad6fca4214') as case:
            # 2.3. layout
            # 2.3.2. Collage template library > Category > All
            # show correct category to match setting
            check_result_1 = video_collage_designer_page.layout.library.select_category(0)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_2_3.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_2_3.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.library.frame, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('90947820-5943-4045-b655-6a222c77f857') as case:
            # 2.3. layout
            # 2.3.2. Collage template library > Window Control > Maximize / Restore
            # control library window correctly
            video_collage_designer_page.layout.library.click_zoom()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_2_4.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_2_4.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.base.main_window, file_name=image_full_path)
            check_result_1 = video_collage_designer_page.compare(ground_truth, current_preview)

            video_collage_designer_page.layout.library.click_zoom()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_2_5.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_2_5.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.base.main_window, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('24cc66e4-789f-4635-ba90-4e4e378be6a2') as case:
            # 2.3. layout
            # 2.3.2. Collage template library > Window Control > Scroll bar
            # scrolling is correct to view all layouts
            check_result_1 = video_collage_designer_page.layout.library.set_scroll_bar(1.0)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_2_6.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_2_6.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.library.frame, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('1b21e336-dfac-44cf-ab40-60317e1c2884') as case:
            # 2.3. layout
            # 2.3.2. Collage template library > Change layout
            # layout should change directly
            video_collage_designer_page.layout.library.click_zoom()
            check_result_1 = video_collage_designer_page.layout.library.select_layout(20)

            video_collage_designer_page.layout.library.click_ok()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_2_7.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_2_7.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.library.frame, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('cb546a50-70de-4f86-896d-c4d900df4d38') as case:
            # 2.3. layout
            # 2.3.2. Collage template library > Free Download
            # open DZ download page correctly
            video_collage_designer_page.layout.open_layout_library()
            time.sleep(DELAY_TIME)
            video_collage_designer_page.layout.library.select_layout(0)
            time.sleep(DELAY_TIME * 3)

            check_result = title_room_page.close_chrome_page()
            time.sleep(DELAY_TIME)
            case.result = check_result
            video_collage_designer_page.activate()

        with uuid('5f51e83c-0df5-4d1d-be14-4d41ad7363bb') as case:
            # 2.3. layout
            # 2.3.2. Collage template library > Confirmation > Cancel
            # close this window w/o layout applied directly
            video_collage_designer_page.layout.library.select_layout(7)

            check_result_1 = video_collage_designer_page.layout.library.click_cancel()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_2_8.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_2_8.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.library.frame, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('2dc28061-5fa5-47ee-8db5-229624022038') as case:
            # 2.3. layout
            # 2.3.2. Collage template library > Confirmation > OK
            # layout is applied correctly
            video_collage_designer_page.layout.open_layout_library()
            time.sleep(DELAY_TIME)
            video_collage_designer_page.layout.library.select_layout(7)

            check_result_1 = video_collage_designer_page.layout.library.click_ok()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_2_9.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_2_9.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.library.frame, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('6bc9df11-fe78-46f8-9ecb-c7942d694dac') as case:
            # 2.3. layout
            # 2.3.2. Collage template library > Window Control > Close
            # close this window w/o layout applied directly
            check_result_1 = video_collage_designer_page.exist_click(L.video_collage_designer.layout.library.btn_close)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_3_2_10.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_3_2_10.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.base.main_window, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid('40514b6b-0cf4-4897-8f41-83a4cfe034ba') as case:
            # 2.4. Slot
            # 2.4.1. Duration
            # show current duration on preview screen
            main_page.top_menu_bar_plugins_video_collage_designer()
            video_collage_designer_page.layout.select_layout(2)
            video_collage_designer_page.media.select_category(1)
            video_collage_designer_page.media.click_auto_fill()
            time.sleep(DELAY_TIME)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_4_1_1.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)
            case.result = check_result

        with uuid('986721d8-b10c-448e-a0f3-a69105c6e02b') as case:
            # 2.4. Slot
            # 2.4.2. Edit Button (Hover status) > Video > Trim
            # open trim dialog and trim correctly
            video_collage_designer_page.click(L.video_collage_designer.main_window)
            video_collage_designer_page.exist_click(L.video_collage_designer.preview.btn_trim)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_4_2_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_4_2_1.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.base.main_window, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            video_collage_designer_page.press_esc_key()

        with uuid('e05c3417-6525-4f66-a3e5-f91b6c343cf6') as case:
            # 2.4. Slot
            # 2.4.2. Edit Button (Hover status) > Video > Mute/Un-mute
            # mute/un-mute clip
            video_collage_designer_page.click(L.video_collage_designer.main_window)
            video_collage_designer_page.exist_click(L.video_collage_designer.preview.btn_mute)
            check_result_1 = video_collage_designer_page.exist(L.video_collage_designer.preview.btn_mute).AXValue

            video_collage_designer_page.exist_click(L.video_collage_designer.preview.btn_mute)
            check_result_2 = video_collage_designer_page.exist(L.video_collage_designer.preview.btn_mute).AXValue

            case.result = False if not check_result_1 == 1 and check_result_2 == 0 else True

        with uuid('a69e1b5e-84fa-49bc-bea7-1e4b6176bfea') as case:
            # 2.4. Slot
            # 2.4.3. Right Click Menu > Video > Mute clip
            # mute this clip
            video_collage_designer_page.right_click()
            video_collage_designer_page.select_right_click_menu('Mute clip')

            check_result = video_collage_designer_page.exist(L.video_collage_designer.preview.btn_mute).AXValue

            case.result = False if not check_result == 1 else True

            video_collage_designer_page.click(L.video_collage_designer.main_window)
            video_collage_designer_page.right_click()
            video_collage_designer_page.select_right_click_menu('Mute clip')

        with uuid('14f226a5-0b39-4aa8-bee1-26d6505db330') as case:
            # 2.4. Slot
            # 2.4.3. Right Click Menu > Video > Mute other clips
            # mute other clips
            video_collage_designer_page.click(L.video_collage_designer.main_window)
            current_position = video_collage_designer_page.get_mouse_pos()

            video_collage_designer_page.right_click()
            video_collage_designer_page.select_right_click_menu('Mute other clips')
            time.sleep(DELAY_TIME)
            video_collage_designer_page.mouse.move(current_position[0] + 150, current_position[1])
            time.sleep(DELAY_TIME)

            check_result = video_collage_designer_page.exist(L.video_collage_designer.preview.btn_mute).AXValue
            case.result = False if not check_result == 1 else True

        with uuid('447c8736-63d3-4e6d-aac2-dd8d874dd5bf') as case:
            # 2.4. Slot
            # 2.4.3. Right Click Menu > Video > Trim...
            # open trim dialog and trim correctly
            video_collage_designer_page.click(L.video_collage_designer.main_window)
            video_collage_designer_page.right_click()
            video_collage_designer_page.select_right_click_menu('Trim...')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_4_3_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_4_3_1.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.base.main_window, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            video_collage_designer_page.press_esc_key()

        with uuid('1ed9dde0-8929-4f59-b5b1-43d72bbbb1ff') as case:
            # 2.4. Slot
            # 2.4.3. Right Click Menu > Video > Remove
            # remove this clip from slot
            video_collage_designer_page.click(L.video_collage_designer.main_window)
            video_collage_designer_page.right_click()
            video_collage_designer_page.select_right_click_menu('Remove')

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_4_3_2.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)
            case.result = check_result

        with uuid('9416db82-1d10-4491-9f9f-e97a03477d6a') as case:
            # 2.1. Caption Bar
            # 2.1.4. [X] button > w adjustment
            # show confirmed msg directly
            video_collage_designer_page.exist_click(L.video_collage_designer.layout.library.btn_close)
            time.sleep(DELAY_TIME)
            main_page.handle_no_save_project_dialog()
            time.sleep(DELAY_TIME)

            check_result = video_collage_designer_page.exist(L.video_collage_designer.main_window)
            case.result = True if not check_result else False

        with uuid('e1ee4c70-3679-4ac6-9aac-e48f15f02f0a') as case:
            # 2.4. Slot
            # 2.4.2. Edit Button (Hover status) > Image > Duration Setting
            # open duration setting dialog and set correctly
            main_page.top_menu_bar_plugins_video_collage_designer()
            video_collage_designer_page.layout.select_layout(2)
            video_collage_designer_page.media.select_category(2)
            video_collage_designer_page.media.click_auto_fill()
            time.sleep(DELAY_TIME)
            video_collage_designer_page.click(L.video_collage_designer.main_window)
            video_collage_designer_page.exist_click(L.video_collage_designer.preview.btn_set_duration)
            video_collage_designer_page.preview.set_duration('00_00_10_00')
            time.sleep(DELAY_TIME)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_4_2_2.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)
            case.result = check_result

        with uuid('f031460d-837f-4c09-b53f-a76ec9e4d8aa') as case:
            # 2.4. Slot
            # 2.4.2. Edit Button (Hover status) > Zoom in/out > Slider
            # adjust zoom setting correctly
            video_collage_designer_page.exist_click(L.video_collage_designer.preview.slider_zoom)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_4_2_3.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)
            case.result = check_result

        with uuid('6fea1667-4fc4-43b0-9756-f65f8900960e') as case:
            # 2.4. Slot
            # 2.4.2. Edit Button (Hover status) > Zoom in/out > -/+ button
            # adjust zoom setting correctly
            for i in range(3):
                video_collage_designer_page.exist_click(L.video_collage_designer.preview.btn_zoom_in)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_4_2_4.png'
            check_result_1 = video_collage_designer_page.verify_preview(ground_truth)

            for i in range(5):
                video_collage_designer_page.exist_click(L.video_collage_designer.preview.btn_zoom_out)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_4_2_5.png'
            check_result_2 = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result_1 and check_result_2

        with uuid('c89f19d6-f32f-4c92-87b1-a378a9045807') as case:
            # 2.4. Slot
            # 2.4.3. Right Click Menu > Image > Duration Setting
            # open duration setting to adjust image duration
            video_collage_designer_page.click(L.video_collage_designer.main_window)
            video_collage_designer_page.right_click()
            video_collage_designer_page.select_right_click_menu('Set duration...')
            video_collage_designer_page.preview.set_duration('00_00_05_00')
            time.sleep(DELAY_TIME)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_4_3_3.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)
            case.result = check_result

        with uuid('8188ee05-f6c5-49c8-8dac-d091172b0306') as case:
            # 2.4. Slot
            # 2.4.3. Right Click Menu > Image > Remove
            # remove this clip from slot
            video_collage_designer_page.right_click()
            video_collage_designer_page.select_right_click_menu('Remove')
            time.sleep(DELAY_TIME)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_4_3_4.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)
            case.result = check_result

        with uuid('2690980e-cc4b-47d9-8d1c-3b912adfc58e') as case:
            # 2.4. Slot
            # 2.4.4. Separate Line > Resize > Horizontal
            # adjust separate line to resize slot region
            # AT limitation
            case.result = None
            case.fail_log = "AT limitation"

        with uuid('ab5d7d71-a2e9-4a19-99d3-6c35b6fd8213') as case:
            # 2.4. Slot
            # 2.4.4. Separate Line > Resize > Vertical
            # adjust separate line to resize slot region
            # AT limitation
            case.result = None
            case.fail_log = "AT limitation"

        with uuid('a0db8b9a-c5a1-4dbe-a910-2d87b7cc7dfc') as case:
            # 2.4. Slot
            # 2.4.4. Separate Line > Resize > Slanting
            # adjust separate line to resize slot region
            # AT limitation
            case.result = None
            case.fail_log = "AT limitation"

        with uuid('568f7530-ae1d-4cf5-a2d8-9e4672add135') as case:
            # 2.4. Slot
            # 2.4.5. Drag clips > Display range
            # adjust the displayed clip region
            # AT limitation
            case.result = None
            case.fail_log = "AT limitation"

        with uuid('5f1960cf-dca5-44e6-96e3-8ce2e50ccf93') as case:
            # 2.4. Slot
            # 2.4.5. Drag clips > Remove (drag to outside)
            # remove clip from slot
            # AT limitation
            case.result = None
            case.fail_log = "AT limitation"

        with uuid('074664a2-57ef-438c-bbd1-f83f19f46e63') as case:
            # 2.4. Slot
            # 2.4.5. Drag clips > Clip Exchange
            # exchange media clip
            # AT limitation
            case.result = None
            case.fail_log = "AT limitation"

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid('8716ada6-16a1-4a75-9239-23b554dde690') as case:
            # 2.5. Settings
            # 2.5.1. Border > Checkbox > Unselect
            # No border exists
            main_page.top_menu_bar_plugins_video_collage_designer()
            video_collage_designer_page.border.enable_border(0)
            time.sleep(DELAY_TIME)

            btn_status = video_collage_designer_page.exist(L.video_collage_designer.border.slider_border).AXEnabled
            check_result_1 = True if not btn_status else False

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_1.png'
            check_result_2 = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result_1 and check_result_2

        with uuid('7f472c6c-d935-4024-b480-c0e69ce62086') as case:
            # 2.5. Settings
            # 2.5.1. Border > Checkbox > Select
            # there is border existing
            video_collage_designer_page.border.enable_border(1)
            time.sleep(DELAY_TIME)

            btn_status = video_collage_designer_page.exist(L.video_collage_designer.border.slider_border).AXEnabled
            check_result_1 = False if not btn_status else True

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_2.png'
            check_result_2 = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result_1 and check_result_2

        with uuid('074b759d-da61-4578-a665-9fba11c9832f') as case:
            # 2.5. Settings
            # 2.5.1. Border > Size > 0(default)
            # border displays correctly after setting
            default_value = video_collage_designer_page.exist(L.video_collage_designer.border.value_border).AXValue
            check_result_1 = False if not default_value == '0' else True

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_3.png'
            check_result_2 = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result_1 and check_result_2

        with uuid('41eb26fa-1e32-4f50-a30d-84a4f0f7ce0c') as case:
            # 2.5. Settings
            # 2.5.1. Border > Size > 100(max)
            # border displays correctly after setting
            video_collage_designer_page.border.set_border_value('100')
            time.sleep(DELAY_TIME)

            border_value = video_collage_designer_page.exist(L.video_collage_designer.border.value_border).AXValue
            check_result_1 = False if not border_value == '100' else True

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_4.png'
            check_result_2 = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result_1 and check_result_2

        with uuid('3ba2c38f-e65f-47fa-b6ff-a90b20271487') as case:
            # 2.5. Settings
            # 2.5.1. Border > Size > 0(min)
            # border displays correctly after setting
            video_collage_designer_page.border.set_border_value('0')
            time.sleep(DELAY_TIME)

            border_value = video_collage_designer_page.exist(L.video_collage_designer.border.value_border).AXValue
            check_result_1 = False if not border_value == '0' else True

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_5.png'
            check_result_2 = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result_1 and check_result_2

        with uuid('b269789c-3142-4fad-8b33-e11a554f89be') as case:
            # 2.5. Settings
            # 2.5.1. Border > Size > Others
            # border displays correctly after setting
            video_collage_designer_page.border.set_border_value('50')
            time.sleep(DELAY_TIME)

            border_value = video_collage_designer_page.exist(L.video_collage_designer.border.value_border).AXValue
            check_result_1 = False if not border_value == '50' else True

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_6.png'
            check_result_2 = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result_1 and check_result_2

        with uuid('835959ee-6a3b-43c6-8358-25e05729fa31') as case:
            # 2.5. Settings
            # 2.5.1. Border > Size > Adjust by keyboard input
            # change will apply on screen directly
            case.result = check_result_1 and check_result_2

        with uuid('90f5d588-5850-46a6-b1f7-ece41ec6aa41') as case:
            # 2.5. Settings
            # 2.5.1. Border > Size > Adjust by slider
            # change will apply on screen directly
            video_collage_designer_page.border.set_border_slider(30)
            time.sleep(DELAY_TIME)

            border_value = video_collage_designer_page.exist(L.video_collage_designer.border.value_border).AXValue
            check_result_1 = False if not border_value == '30' else True

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_7.png'
            check_result_2 = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result_1 and check_result_2

        with uuid('e1a67af2-ad7b-48e4-864b-eaede1e02dfc') as case:
            # 2.5. Settings
            # 2.5.1. Border > Size > Adjust by ^/v button
            # change will apply on screen directly
            for i in range(2):
                video_collage_designer_page.border.click_border_arrow('up')
            for j in range(4):
                video_collage_designer_page.border.click_border_arrow('down')

            border_value = video_collage_designer_page.exist(L.video_collage_designer.border.value_border).AXValue
            check_result_1 = False if not border_value == '28' else True

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_8.png'
            check_result_2 = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result_1 and check_result_2

        with uuid('dd401fe9-306a-4f90-9860-b30352d602eb') as case:
            # 2.5. Settings
            # 2.5.1. Border > Color > Gray(default)
            # default border is white on screen
            default_color = video_collage_designer_page.border.is_border_color('565656')
            video_collage_designer_page.border.click_close()

            case.result = default_color

        with uuid('9e10dc5b-1db3-4488-891c-54a74c16dde5') as case:
            # 2.5. Settings
            # 2.5.1. Border > Color > Customize
            # customize color setting is also applied correctly
            video_collage_designer_page.border.set_border_color('FF0000')

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_9.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

        with uuid('c918c16d-d87c-41ff-8fc7-52c0ce6db7f2') as case:
            # 2.5. Settings
            # 2.5.1. Border > Interclip size > 10(default)
            # default size is correct on preview
            interclip_value = video_collage_designer_page.exist(L.video_collage_designer.border.value_interclip).AXValue

            case.result = False if not interclip_value == '10' else True

        with uuid('cdf5e4a7-4e6f-46b7-bd65-5ff79187bc8e') as case:
            # 2.5. Settings
            # 2.5.1. Border > Interclip size > 0(min)
            # min size is correct on preview
            video_collage_designer_page.border.set_interclip_value('0')

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_10.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

        with uuid('c4295fca-f417-4e03-bd40-4b3bc26786ce') as case:
            # 2.5. Settings
            # 2.5.1. Border > Interclip size > 100(max)
            # max size is correct on preview
            video_collage_designer_page.border.set_interclip_value('100')

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_11.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

        with uuid('f0bafe40-f7f7-473d-882e-f110218b9f3b') as case:
            # 2.5. Settings
            # 2.5.1. Border > Interclip size > Other size
            # set correctly
            video_collage_designer_page.border.set_interclip_value('50')

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_12.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

        with uuid('2cbcedcc-2e6a-4add-8b15-1fb77565c30b') as case:
            # 2.5. Settings
            # 2.5.1. Border > Interclip size > Adjust by keyboard input
            # adjustment work correctly
            case.result = check_result

        with uuid('8eab7114-0569-4bfb-a697-27187afb7afe') as case:
            # 2.5. Settings
            # 2.5.1. Border > Interclip size > Adjust by slider
            # adjustment work correctly
            video_collage_designer_page.border.set_interclip_slider(30)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_13.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

        with uuid('5e3b787f-d7cc-497d-924e-e4fcb2b9ce28') as case:
            # 2.5. Settings
            # 2.5.1. Border > Interclip size > Adjust by ^/v button
            # adjustment work correctly
            for i in range(2):
                video_collage_designer_page.border.click_interclip_arrow('up')
            for j in range(4):
                video_collage_designer_page.border.click_interclip_arrow('down')

            border_value = video_collage_designer_page.exist(L.video_collage_designer.border.value_border).AXValue
            check_result_1 = False if not border_value == '28' else True

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_14.png'
            check_result_2 = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result_1 and check_result_2

        with uuid('49a3a69a-dcf2-4f24-afb1-3c9cc6421024') as case:
            # 2.5. Settings
            # 2.5.1. Border > Fill type > Interclip texture
            # image file is selected and displays correctly
            video_collage_designer_page.border.set_fill_type(1)
            video_collage_designer_page.border.select_interclip_texture(Test_Material_Folder + '97982237.jpg')

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_15.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

        with uuid('5276dd60-f5fe-4704-b4a5-126f86018697') as case:
            # 2.5. Settings
            # 2.5.1. Border > Fill type > Uniform color
            # color can be selected and displays correctly
            video_collage_designer_page.border.set_fill_type(0)
            video_collage_designer_page.border.set_uniform_color('0000FF')

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_1_16.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

        with uuid('37887af1-6f26-4a90-bce7-e080b62fc03c') as case:
            # 2.5. Settings
            # 2.5.2. Frame Animation > During Closing
            # after apply, preview should display as setting correctly
            video_collage_designer_page.border.set_frame_animation(1)
            video_collage_designer_page.set_timecode('00_00_02_00')

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_2_1.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('e2f66e1e-1e57-41a2-bc89-b24e8dded350') as case:
            # 2.5. Settings
            # 2.5.2. Frame Animation > Off
            # after apply, preview should display as setting correctly
            video_collage_designer_page.border.set_frame_animation(2)
            video_collage_designer_page.set_timecode('00_00_02_00')

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_2_2.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('2c74e90d-0155-434a-9e37-98a2c6995df1') as case:
            # 2.5. Settings
            # 2.5.2. Frame Animation > From Beginning
            # after apply, preview should display as setting correctly
            video_collage_designer_page.border.set_frame_animation(0)
            video_collage_designer_page.set_timecode('00_00_02_00')

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_2_3.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('91f68830-3b1a-4ca9-bfe8-de4a9a602c7e') as case:
            # 2.5. Settings
            # 2.5.3. Start clip playback > From Beginning > with animations(default)
            # clip plays with the animations
            video_collage_designer_page.media.import_media(Test_Material_Folder + 'run_kid.mp4')
            video_collage_designer_page.layout.select_layout(2)
            video_collage_designer_page.media.select_category(1)
            video_collage_designer_page.media.click_auto_fill()
            time.sleep(DELAY_TIME)
            video_collage_designer_page.set_timecode('00_00_01_00')
            time.sleep(DELAY_TIME)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_3_1.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('907e3a2d-9f37-4b30-830d-f8cf91fd6d15') as case:
            # 2.5. Settings
            # 2.5.3. Start clip playback > From Beginning > after animations
            # clip plays after the animations
            video_collage_designer_page.border.set_start_playback(1)
            video_collage_designer_page.set_timecode('00_00_01_00')
            time.sleep(DELAY_TIME)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_3_2.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('90a582be-ca47-4cbe-bb64-ac07499ba2ec') as case:
            # 2.5. Settings
            # 2.5.3. Start clip playback > During Closing > Pause with the animation
            # playback will pause during animation
            video_collage_designer_page.border.set_frame_animation(1)
            video_collage_designer_page.border.set_pause_playback(1)
            video_collage_designer_page.set_timecode('00_00_11_00')
            time.sleep(DELAY_TIME)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_3_3.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('8c34d045-869c-4ef4-9a15-d921796d0aa2') as case:
            # 2.5. Settings
            # 2.5.3. Start clip playback > During Closing > Pause after the animation
            # playback will pause as setting
            video_collage_designer_page.border.set_pause_playback(0)

            video_collage_designer_page.set_timecode('00_00_09_00')
            time.sleep(DELAY_TIME)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_3_4.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('724cd5ba-1541-400f-ba7e-c3b31e426248') as case:
            # 2.5. Settings
            # 2.5.3. Start clip playback > Off > Disable(default)
            # when frame animation is off, this setting is disabled
            video_collage_designer_page.border.set_frame_animation(2)
            video_collage_designer_page.set_timecode('00_00_01_00')
            time.sleep(DELAY_TIME)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_3_5.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('963bd97b-3957-4809-a637-6cf351f5ca79') as case:
            # 2.5. Settings
            # 2.5.4. Before/after clip playback > Color board
            # show selected color under non playback status
            video_collage_designer_page.border.set_scroll_bar(1.0)
            video_collage_designer_page.border.set_before_after_clip_playback(1)
            video_collage_designer_page.border.set_before_after_color_board('00FF00')
            video_collage_designer_page.border.click_close()
            video_collage_designer_page.set_timecode('00_00_09_00')
            time.sleep(DELAY_TIME)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_4_1.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('17370983-02fe-4424-806a-f317aab2b3c0') as case:
            # 2.5. Settings
            # 2.5.4. Before/after clip playback > Restart playback
            # restart playback if partial clip end
            video_collage_designer_page.border.set_before_after_clip_playback(2)
            video_collage_designer_page.set_timecode('00_00_09_00')
            time.sleep(DELAY_TIME)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_4_2.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('511cee75-7802-4a78-8163-861c6e7039bc') as case:
            # 2.5. Settings
            # 2.5.4. Before/after clip playback > Freeze the video
            # show the last frame under non playback status
            video_collage_designer_page.border.set_before_after_clip_playback(0)
            video_collage_designer_page.set_timecode('00_00_09_00')
            time.sleep(DELAY_TIME)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_4_3.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('f560c167-1896-4ce4-a3e9-ca96a3473ccd') as case:
            # 2.5. Settings
            # 2.5.5. Advanced Settings > Playback Timing > Delay ? Seconds
            # 1. number can set 1~60 sec. by input or ^/v
            # 2. preview is correct by this setting
            video_collage_designer_page.border.click_advanced_setting()
            video_collage_designer_page.border.advanced.set_playback_timing(1)
            video_collage_designer_page.border.advanced.set_delay_sec(3)
            video_collage_designer_page.border.advanced.click_ok()
            video_collage_designer_page.set_timecode('00_00_04_00')
            time.sleep(DELAY_TIME)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_5_1.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('2f6b9748-9e0f-49f9-bcd2-e9ba72dbe631') as case:
            # 2.5. Settings
            # 2.5.5. Advanced Settings > Playback Timing > One after another
            # preview is correct by clip ordering
            video_collage_designer_page.border.click_advanced_setting()
            video_collage_designer_page.border.advanced.set_playback_timing(2)
            video_collage_designer_page.border.advanced.click_ok()
            video_collage_designer_page.set_timecode('00_00_07_00')
            time.sleep(DELAY_TIME)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_5_2.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('848ee9fb-1e2f-4588-8215-3b842a1bfac3') as case:
            # 2.5. Settings
            # 2.5.5. Advanced Settings > Playback Timing > All at once
            # all slots play at beginning
            video_collage_designer_page.border.click_advanced_setting()
            video_collage_designer_page.border.advanced.set_playback_timing(0)
            video_collage_designer_page.border.advanced.click_ok()
            video_collage_designer_page.set_timecode('00_00_07_00')
            time.sleep(DELAY_TIME)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_5_3.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('3cff7b99-3243-41d5-ba14-8d031a24a4bf') as case:
            # 2.5. Settings
            # 2.5.5. Advanced Settings > Match collage duration to > All Videos (default)
            # duration should match as setting
            video_collage_designer_page.border.click_advanced_setting()
            video_collage_designer_page.border.advanced.set_match_collage_duration_to(0)
            video_collage_designer_page.border.advanced.click_ok()

            video_collage_designer_page.set_timecode('00_00_12_00')
            check_duration = video_collage_designer_page.exist(L.video_collage_designer.time_code).AXValue
            case.result = False if not check_duration == '00;00;10;00' else True

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('1d8c56ce-77cb-42fb-8cee-082a47240f28') as case:
            # 2.5. Settings
            # 2.5.5. Advanced Settings > Match collage duration to > The longest clip
            # duration should match as setting
            video_collage_designer_page.border.click_advanced_setting()
            video_collage_designer_page.border.advanced.set_match_collage_duration_to(1)
            video_collage_designer_page.border.advanced.click_ok()

            video_collage_designer_page.set_timecode('00_00_12_00')
            check_duration = video_collage_designer_page.exist(L.video_collage_designer.time_code).AXValue
            case.result = False if not check_duration == '00;00;10;00' else True

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('7e280c99-86aa-465d-bd06-bb222c0cf734') as case:
            # 2.5. Settings
            # 2.5.5. Advanced Settings > Match collage duration to > The shortest clip
            # duration should match as setting
            video_collage_designer_page.border.click_advanced_setting()
            video_collage_designer_page.border.advanced.set_match_collage_duration_to(2)
            video_collage_designer_page.border.advanced.click_ok()

            video_collage_designer_page.set_timecode('00_00_12_00')
            check_duration = video_collage_designer_page.exist(L.video_collage_designer.time_code).AXValue
            case.result = False if not check_duration == '00;00;05;00' else True

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('d49a715a-a1bf-4980-aeb2-3e4f29666964') as case:
            # 2.5. Settings
            # 2.5.5. Advanced Settings > Match collage duration to > Clip 1~N
            # duration should match as setting
            video_collage_designer_page.border.click_advanced_setting()
            video_collage_designer_page.border.advanced.set_match_collage_duration_to(3)
            video_collage_designer_page.border.advanced.click_ok()

            video_collage_designer_page.set_timecode('00_00_12_00')
            check_duration = video_collage_designer_page.exist(L.video_collage_designer.time_code).AXValue
            case.result = False if not check_duration == '00;00;05;00' else True

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('77ecbbe2-b9f6-4475-a1f3-cad99a768a73') as case:
            # 2.5. Settings
            # 2.5.5. Advanced Settings > Confirmation > Default
            # restore all settings to default directly
            video_collage_designer_page.border.click_advanced_setting()
            video_collage_designer_page.border.advanced.click_default()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_5_5_4.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_5_5_4.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.base.main_window, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('8433aa23-302d-43d6-a918-3a1b6fb89e97') as case:
            # 2.5. Settings
            # 2.5.5. Advanced Settings > Confirmation > OK
            # apply the change after dialog close
            check_result = video_collage_designer_page.border.advanced.click_ok()
            case.result = check_result

            video_collage_designer_page.move_mouse_to_0_0()

        with uuid('8046ed91-9cf7-4cc9-8689-85c73b8b1c15') as case:
            # 2.5. Settings
            # 2.5.5. Advanced Settings > Confirmation > Cancel
            # don't apply the change after dialog close
            video_collage_designer_page.border.click_advanced_setting()
            video_collage_designer_page.border.advanced.set_match_collage_duration_to(2)
            video_collage_designer_page.border.advanced.click_cancel()

            video_collage_designer_page.set_timecode('00_00_12_00')
            check_duration = video_collage_designer_page.exist(L.video_collage_designer.time_code).AXValue
            case.result = False if not check_duration == '00;00;10;00' else True

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('fc543395-b231-4b2b-b325-8e35c3d08232') as case:
            # 2.5. Settings
            # 2.5.5. Advanced Settings > Confirmation > ESC
            # don't apply the change after dialog close
            video_collage_designer_page.border.click_advanced_setting()
            video_collage_designer_page.border.advanced.set_match_collage_duration_to(2)
            time.sleep(DELAY_TIME)
            video_collage_designer_page.press_esc_key()

            video_collage_designer_page.set_timecode('00_00_12_00')
            check_duration = video_collage_designer_page.exist(L.video_collage_designer.time_code).AXValue
            case.result = False if not check_duration == '00;00;10;00' else True

            video_collage_designer_page.click_preview_operation('Stop')

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid('3fffcd09-5246-490b-99d9-547b8358f6c2') as case:
            # 2.6. Playback Control
            # 2.6.1. Play/Pause > Play
            # play or pause the clips
            main_page.top_menu_bar_plugins_video_collage_designer()
            video_collage_designer_page.layout.select_layout(2)
            video_collage_designer_page.media.select_category(1)
            video_collage_designer_page.media.click_auto_fill()
            time.sleep(DELAY_TIME)
            check_result_1 = video_collage_designer_page.click_preview_operation('Play')
            time.sleep(DELAY_TIME * 2)
            check_result_2 = video_collage_designer_page.click_preview_operation('Pause')

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_6_1_1.png'
            check_result_3 = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result_1 and check_result_3

        with uuid('420fcf8a-16f0-4a7f-871a-b2719d88308a') as case:
            # 2.6. Playback Control
            # 2.6.1. Play/Pause > Pause
            # play or pause the clips
            case.result = check_result_2 and check_result_3

        with uuid('1338b1c8-98df-4937-83d7-5f7aa42ac019') as case:
            # 2.6. Playback Control
            # 2.6.3. [Previous Frame] button
            # seek to previous frame
            for i in range(5):
                video_collage_designer_page.click_preview_operation('Previous_Frame')
                time.sleep(DELAY_TIME * 0.5)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_6_3_1.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

        with uuid('41500284-f15d-4456-9096-87da05ecaa28') as case:
            # 2.6. Playback Control
            # 2.6.4. [Next Frame] button
            # seek to next frame
            for i in range(5):
                video_collage_designer_page.click_preview_operation('Next_Frame')
                time.sleep(DELAY_TIME * 0.5)

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_6_4_1.png'
            check_result = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result

        with uuid('0469fcc5-59d1-4cf5-a92e-8ae99b037abf') as case:
            # 2.6. Playback Control
            # 2.6.5. Take a snapshot > jpg
            # snapshot is normal with frame selected
            check_result = video_collage_designer_page.click_snapshot(Test_Material_Folder + 'snapshot')

            case.result = check_result

        with uuid('4d9efcc9-5f94-4d68-8d90-0b50833527f0') as case:
            # 2.6. Playback Control
            # 2.6.2. [Stop] button
            # stop the preview
            check_result_1 = video_collage_designer_page.click_preview_operation('Stop')

            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_6_2_1.png'
            check_result_2 = video_collage_designer_page.verify_preview(ground_truth)

            case.result = check_result_1 and check_result_2

        with uuid('240a0b7a-d901-40c8-8c52-783dcf175fd0') as case:
            # 2.6. Playback Control
            # 2.6.6. Set preview quality / display option
            # open settings for selection
            check_result = video_collage_designer_page.select_quality('High')

            case.result = check_result

        with uuid('c97a57b1-dc12-4ff0-b0e3-58bf1a5ce9b3') as case:
            # 2.6. Playback Control
            # 2.6.7. Adjust volume
            # control sound setting or mute
            check_result = video_collage_designer_page.set_volume(0.8)

            case.result = check_result

        with uuid('35a4bc86-b6e3-43af-b70e-50764c3afc67') as case:
            # 2.6. Playback Control
            # 2.6.9. Seek slide bar > During preview
            # seek preview correctly
            check_result_1 = video_collage_designer_page.adjust_playback_slider(0.8)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_6_9_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_6_9_1.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.preview.slider_playback, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('4541592c-6d82-4535-b4fd-9535a11cf434') as case:
            # 2.6. Playback Control
            # 2.6.8. Timecode > Displays
            # show current timecode
            current_timecode = video_collage_designer_page.exist(L.video_collage_designer.time_code).AXValue
            case.result = False if not current_timecode == '00;00;08;00' else True

        with uuid('8918fd40-016a-4d9a-9ba5-11e3d98672da') as case:
            # 2.6. Playback Control
            # 2.6.8. Timecode > Input
            # input number then seek to correct position
            video_collage_designer_page.set_timecode('00_00_05_00')
            check_duration = video_collage_designer_page.exist(L.video_collage_designer.time_code).AXValue
            case.result = False if not check_duration == '00;00;05;00' else True

            video_collage_designer_page.click_preview_operation('Stop')

        with uuid('a36060e0-7bf9-4018-80e1-fddc6fdc770f') as case:
            # 2.7. Confirmation
            # 2.7.1. Share > DZ > Uploading process
            # Template can share to DZ correctly
            # skip upload template to Cloud/DZ
            case.result = None
            case.fail_log = "AT limitation"

        with uuid('c5b72920-2085-4b8d-9889-a4946fd09570') as case:
            # 2.7. Confirmation
            # 2.7.1. Share > Cloud > Uploading process
            # Template can share to cloud correctly
            # skip upload template to Cloud/DZ
            case.result = None
            case.fail_log = "AT limitation"

        with uuid('8ae74d61-34cc-4b71-816b-8f2bedbcc15b') as case:
            # 2.7. Confirmation
            # 2.7.2. Save As > Template name
            # correct template name displays in tooltip after save to layout panel
            video_collage_designer_page.border.set_interclip_value('50')
            video_collage_designer_page.click_save_as_with_name('custom_collage')
            video_collage_designer_page.layout.hover_layout(1)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_7_2_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_7_2_1.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.library.frame, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('8713f4c0-2d5c-4a0c-9d90-dc1c9367fa64') as case:
            # 2.7. Confirmation
            # 2.7.2. Save As > Thumbnail
            # thumbnail is correct at layout panel after save as
            case.result = check_result

        with uuid('cafa4c61-1c06-478c-a94c-ead2ad1f6c22') as case:
            # 2.7. Confirmation
            # 2.7.2. Save As > OK
            # after apply saved layout, all settings are correct
            video_collage_designer_page.border.set_interclip_value('100')
            video_collage_designer_page.exist_click(L.video_collage_designer.btn_save_as)
            check_result_1 = video_collage_designer_page.click_save_as_ok('custom_collage_1')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_7_2_2.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_7_2_2.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.library.frame, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('876bb10c-8c39-4382-8c3a-15cee60efc5c') as case:
            # 2.7. Confirmation
            # 2.7.2. Save As > Cancel
            # close dialog w/o saving
            check_result_1 = video_collage_designer_page.click_save_as_then_cancel()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_7_2_3.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_7_2_3.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.layout.library.frame, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('745b300c-71b3-46e2-bb7d-b58df702718e') as case:
            # 2.7. Confirmation
            # 2.7.3. [OK] button
            # save the setting and show effect on timeline
            check_result_1 = video_collage_designer_page.click_ok()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_2_7_3_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_2_7_3_1.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result_2 = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('45838c7a-7b6a-466a-b558-6b8372c8a797') as case:
            # 2.7. Confirmation
            # 2.7.3. [OK] button
            # preview match customize settings in designer
            case.result = check_result_2

        with uuid('0c05be09-ddbf-4c25-a0ff-4c1b0bb4cdd1') as case:
            # 2.7. Confirmation
            # 2.7.3. [OK] button
            # in library, clip is selected
            case.result = check_result_2

        with uuid('c435da64-5654-42bd-8970-797239f713c3') as case:
            # 2.7. Confirmation
            # 2.7.4. [Cancel] button > No edit
            # return to edit directly
            main_page.top_menu_bar_plugins_video_collage_designer()
            video_collage_designer_page.layout.select_layout(2)
            check_result_1 = video_collage_designer_page.click_cancel()
            time.sleep(DELAY_TIME)

            check_result = video_collage_designer_page.exist(L.video_collage_designer.main_window)
            check_result_2 = True if not check_result else False

            case.result = check_result_1 and check_result_2

        with uuid('5b41b680-4aeb-4f52-ab51-16252022e55e') as case:
            # 2.7. Confirmation
            # 2.7.4. [Cancel] button > Confirmation > Yes
            # close dialog directly
            main_page.top_menu_bar_plugins_video_collage_designer()
            video_collage_designer_page.layout.select_layout(2)
            video_collage_designer_page.media.select_category(1)
            video_collage_designer_page.media.click_auto_fill()
            check_result_1 = video_collage_designer_page.click_cancel(option=1)

            check_result = video_collage_designer_page.exist(L.video_collage_designer.main_window)
            check_result_2 = True if not check_result else False

            case.result = check_result_1 and check_result_2

        with uuid('bb4c1e08-9fc1-4ea9-b66e-325aef1e593e') as case:
            # 2.7. Confirmation
            # 2.7.4. [Cancel] button > Confirmation > No
            # leave
            main_page.top_menu_bar_plugins_video_collage_designer()
            video_collage_designer_page.layout.select_layout(2)
            video_collage_designer_page.media.select_category(1)
            video_collage_designer_page.media.click_auto_fill()
            check_result_1 = video_collage_designer_page.click_cancel(option=2)

            check_result = video_collage_designer_page.exist(L.video_collage_designer.main_window)
            check_result_2 = True if not check_result else False

            case.result = check_result_1 and check_result_2

        with uuid('4b547535-9cbe-4c34-a952-0cca076a73fc') as case:
            # 2.7. Confirmation
            # 2.7.4. [Cancel] button > Confirmation > Cancel
            # show confirmation if save change or not
            main_page.top_menu_bar_plugins_video_collage_designer()
            video_collage_designer_page.layout.select_layout(2)
            video_collage_designer_page.media.select_category(1)
            video_collage_designer_page.media.click_auto_fill()
            check_result_1 = video_collage_designer_page.click_cancel(option=3)

            check_result = video_collage_designer_page.exist(L.video_collage_designer.main_window)
            check_result_2 = False if not check_result else True

            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        with uuid('9c314a9b-97ff-4d2c-8a2a-c8e490062ab9') as case:
            # 3. Timeline Operation
            # 3.1. Status
            # 3.1.1. Virtual cut clip > Video thumbnail
            # display the correct thumbnail for video collage clip
            main_page.top_menu_bar_plugins_video_collage_designer()
            video_collage_designer_page.layout.select_layout(2)
            video_collage_designer_page.border.set_interclip_value('50')
            video_collage_designer_page.media.select_category(1)
            video_collage_designer_page.media.click_auto_fill()
            video_collage_designer_page.click_ok()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_3_1_1_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_3_1_1_1.png'
            current_preview = video_collage_designer_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result = video_collage_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('7f652d99-9ae0-4cdf-8f6e-a4de2249cb8a') as case:
            # 3.1. Status
            # 3.1.1. Virtual cut clip > Tooltip
            # show tooltip when hover on video collage clip
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_3_1_1_2.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_3_1_1_2.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result = timeline_operation_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('c3c724d5-c408-4a65-9ba1-6f817d3026d6') as case:
            # 3.1. Status
            # 3.1.2. Entry for modify clip > [Video Collage] button
            # re-open designer and all settings are match as previous
            check_result = main_page.tips_area_click_video_collage()
            case.result = check_result

            video_collage_designer_page.press_esc_key()

        with uuid('74ea3a23-c084-499a-ad66-772164bf84aa') as case:
            # 3.2. Video collage clip
            # 3.2.1. Trim
            # video frame displays correctly after trim
            timeline_operation_page.drag_timeline_clip(mode='Last', ratio=0.5, track_index1=0, clip_index1=0)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_3_2_1_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_3_2_1_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.click_undo()

        with uuid('283b59a9-4311-4b32-bb7e-2a37fd917b96') as case:
            # 3.2. Video collage clip
            # 3.2.2. Enlarge clip duration > Drag clip edge
            # cannot enlarge clip duration
            # AT limitation
            case.result = None
            case.fail_log = "AT limitation"

        with uuid('0a146fbf-dd19-41fa-b4b3-5504ec87e77b') as case:
            # 3.2. Video collage clip
            # 3.2.3. Split
            # video frame displays correctly after split
            main_page.set_timeline_timecode('00_00_05_00')
            # main_page.tips_area_click_split()
            media_room_page.tap_Split_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_3_2_3_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_3_2_3_1.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.click_undo()

        with uuid('1a866a31-d672-4677-8b31-0b236f32a74e') as case:
            # 3.2. Video collage clip
            # 3.2.4. Move position
            # video frame displays correctly after reposition
            timeline_operation_page.drag_single_media_move_to(0, 0, 200)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_3_2_4_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_3_2_4_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('3108b8c0-0c6a-4d48-805c-7b2b6faabbff') as case:
            # 3.2. Video collage clip
            # 3.2.7. Undo / Redo
            # video frame displays correctly after undo / redo
            main_page.click_undo()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_3_2_7_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_3_2_7_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result_1 = timeline_operation_page.compare(ground_truth, current_preview)

            main_page.click_redo()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_3_2_7_2.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_3_2_7_2.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result_2 = timeline_operation_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('d288ee0b-fc61-4c71-8f06-93f69e97ca0c') as case:
            # 3.2. Video collage clip
            # 3.2.6. Render Preview
            # complete precess for virtual cut clip
            timeline_operation_page.edit_timeline_render_preview()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_3_2_6_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_3_2_6_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result = timeline_operation_page.compare(ground_truth, current_preview)

            case.result = check_result
            time.sleep(DELAY_TIME * 2)

        with uuid('6b822aa2-985f-4f33-adc5-e8149c8bc713') as case:
            # 3.3. Project
            # 3.3.1. Save project then open
            # 1. save project correctly
            # 2. content is correct after open saved project
            main_page.save_project('video_collage_test', Test_Material_Folder + 'video_collage')
            time.sleep(DELAY_TIME * 2)
            main_page.close_and_restart_app()
            time.sleep(DELAY_TIME * 5)

            main_page.top_menu_bar_file_open_project()
            main_page.handle_open_project_dialog(Test_Material_Folder + 'video_collage/video_collage_test.pds')
            main_page.handle_merge_media_to_current_library_dialog()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_3_3_1_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_3_3_1_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result = timeline_operation_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('a627b32b-edd9-488c-9805-fc41d4479e28') as case:
            # 3.2. Video collage clip
            # 3.2.5. Remove
            # video collage clip remove from timeline directly
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            video_collage_designer_page.press_del_key()

            image_full_path = Auto_Ground_Truth_Folder + 'video_collage_designer_3_2_5_1.png'
            ground_truth = Ground_Truth_Folder + 'video_collage_designer_3_2_5_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result = timeline_operation_page.compare(ground_truth, current_preview)

            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    dffa2bd5-8d87-4d97-aae6-cc6a660739a7
                    c5b06ce2-abe0-4819-9899-507cfef589e9
                    8fb51bee-dda7-4513-8a08-78ee78c55d0c
                    bf87919e-3f1f-4f9a-aeb5-5f3592418c12
                    cae89a88-c523-499c-bce5-f5cf63fdee59
                    58a74539-5442-4b4a-9b51-b020de7a1b5e
                    5255b08f-a2cd-4bd1-8ee4-15ab50e0f96a
                    9bedaf4d-3faf-4d66-9f15-844578466171
                    6af4aecd-23a5-42e8-aa9c-392ccb064b15
                    42d3adff-205a-4acf-bdc9-4c5d83eb3be3
                    3b6e4103-a907-4553-98ee-c0028cc61e9c
                    e4766bd9-e3ea-4c81-8d25-ff5617c21307
                    3ce37c12-e428-4750-b801-8acd8abeaab0
                    c984601e-a5c3-4703-adc5-aba1eee04d87
                    e68052d1-c265-413d-b89d-4a55a612e905
                    4a48fcf4-8103-43e3-adce-9843300d6dbb
                    9f51977a-54c7-47f6-88df-214f44f921dd
                    986385fd-d9cc-4f42-82a6-fad4527b14f4
                    348d0647-2fa9-45de-92ab-50a7dc81043e
                    a3f068a3-0c79-45f5-aa64-6e58ec989852
                    956a14eb-89c5-4687-b2c3-716159f121af
                    534f8fd3-e2a1-4105-99bc-dadb72b8f384
                    c9e20d59-b78f-4e9c-ad1b-f70a0443e45a
                    4c816a6f-30b1-40b6-b125-ec0730e9fad6
                    6ed4a362-09b4-4534-b0bf-80e9eca2f961
                    d1796a4f-57d8-4fda-bc99-845f0385aba7
                    52489c83-d89d-4600-90be-06003cd2d0fc
                    2690980e-cc4b-47d9-8d1c-3b912adfc58e
                    ab5d7d71-a2e9-4a19-99d3-6c35b6fd8213
                    a0db8b9a-c5a1-4dbe-a910-2d87b7cc7dfc
                    568f7530-ae1d-4cf5-a2d8-9e4672add135
                    5f1960cf-dca5-44e6-96e3-8ce2e50ccf93
                    074664a2-57ef-438c-bbd1-f83f19f46e63
                    09693369-4ccf-4d0c-93d5-4a6d53cc49a0
                    64c05203-72da-48f4-a394-a6cdac72f51a
                    db951c41-238b-4105-b6e6-3e530e089a41
                    bd47bf5e-6384-4db8-89a1-cbb7493b65f9
                    7a785468-8869-42ef-8df6-8ce4b69692fb
                    a36060e0-7bf9-4018-80e1-fddc6fdc770f
                    1c614ba5-f812-485e-a78f-089c24687de6
                    c5b72920-2085-4b8d-9889-a4946fd09570
                    ea28c1a4-0f0f-486b-b0f1-35e898fa3c95
                    d4caeb25-72ae-47c8-9693-b11d38c5f39a
                    283b59a9-4311-4b32-bb7e-2a37fd917b96
                    c38af646-27f0-4048-924b-7a3ec4ddb50d
                    58439587-f2da-4f95-a7bc-99143ce0eba7
                ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"




