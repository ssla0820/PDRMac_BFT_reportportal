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
pip_designer_page = PageFactory().get_page_object('pip_designer_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="PiP Designer.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/PiP_Designer/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/PiP_Designer/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_PiP_Designer():
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
            google_sheet_execution_log_init('PiP_Designer')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"pip designer result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        with uuid('5c47f7c5-63e3-4944-bfeb-2c1ec82334fa') as case:
            # 1. General
            # 1.1. Entry Point
            # 1.1.1. PiP Room > New template
            # create a new pip object from an image then switch into designer page
            main_page.enter_room(4)
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')

            check_result = pip_room_page.check_in_PiP_designer()
            case.result = check_result

            pip_room_page.press_esc_key()

        with uuid('5d17f092-17f5-4fab-9836-3f437ad7d708') as case:
            # 1. General
            # 1.1. Entry Point
            # 1.1.1. PiP Room > Modify template > Modify button
            # switch into designer page and show selected template correctly
            pip_room_page.click_ModifyAttribute_btn('PiP')
            check_result = pip_room_page.check_in_PiP_designer()
            case.result = check_result

            pip_room_page.press_esc_key()

        with uuid('f6c0c8de-cc1c-4667-b979-696bd46556ab') as case:
            # 1. General
            # 1.1. Entry Point
            # 1.1.1. PiP Room > Modify template > Right-Click menu
            # switch into designer page and show selected template correctly
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_ModifyTemplate('PiP')
            check_result = pip_room_page.check_in_PiP_designer()
            case.result = check_result

            pip_room_page.press_esc_key()

        with uuid('b1e1f3a6-ce81-4e38-beb7-79e5b7a2526a') as case:
            # 1. General
            # 1.1. Entry Point
            # 1.1.1. PiP Room > Modify template > Double click template
            # switch into designer page and show selected template correctly
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.double_click()
            check_result = pip_room_page.check_in_PiP_designer()
            case.result = check_result

            pip_room_page.press_esc_key()

        with uuid('12f29ec9-422c-4a44-b0f6-b4db7825a29d') as case:
            # 1. General
            # 1.1. Entry Point
            # 1.1.2. Tips area > Tools > PiP Designer
            # switch into designer page and media file correctly
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            tips_area_page.tools.select_PiP_Designer()
            check_result = pip_room_page.check_in_PiP_designer()
            case.result = check_result

            pip_room_page.press_esc_key()
            main_page.click_undo()

        with uuid('d1a772c8-f673-4c51-ac53-c32f902861bd') as case:
            # 1. General
            # 1.1. Entry Point
            # 1.1.3. Timeline > Photo > JPG
            # double click on photo then ap should switch into pip designer
            main_page.enter_room(0)
            main_page.insert_media('Food.jpg')
            timeline_operation_page.hover_timeline_media(track_index=0, clip_index=0)
            timeline_operation_page.double_click()
            check_result = pip_room_page.check_in_PiP_designer()
            case.result = check_result

            pip_room_page.press_esc_key()
            main_page.click_undo()

        with uuid('c2fa12c3-d46e-4e87-9860-43c87beee6b4') as case:
            # 1. General
            # 1.1. Entry Point
            # 1.1.3. Timeline > Video > MP4
            # double click on video then ap should switch into pip designer
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.hover_timeline_media(track_index=0, clip_index=0)
            timeline_operation_page.double_click()
            check_result = pip_room_page.check_in_PiP_designer()
            case.result = check_result

        with uuid('2e5e0a2d-c9f6-4be5-9572-3f67a7cc9d07') as case:
            # 1. General
            # 1.3. Window control
            # 1.3.1. ? Button (TBD) > Help > Click item
            # open file correctly
            check_result = pip_designer_page.tap_menu_bar_help()
            time.sleep(DELAY_TIME)
            case.result = check_result

            title_room_page.close_chrome_page()
            time.sleep(DELAY_TIME)
            pip_designer_page.activate()

        with uuid('134143f0-00a7-4058-afb6-bdf0aeb09ffa') as case:
            # 1. General
            # 1.3. Window control
            # 1.3.2. Restore down / Maximize
            # restore down / maximize window correctly
            pip_designer_page.click_maximize_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_1_3_2_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_1_3_2_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview)

            pip_designer_page.click_restore_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_1_3_2_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_1_3_2_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('98085e2b-0087-4600-bd1a-1f91276ca314') as case:
            # 1. General
            # 1.3. Window control
            # 1.3.3. Close
            # exit module
            pip_designer_page.click_close_btn()

            check_result = pip_designer_page.exist(L.pip_designer.designer_window)
            if not check_result:
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid('33ce865e-cb68-4c27-9155-70f83ef8f0b1') as case:
            # 3. Express Mode
            # 3.1. Properties
            # 3.1.1. Object Settings > Opacity > Default value (100%)
            # adjustment works correctly with default value
            main_page.enter_room(4)
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.switch_mode('Express')
            pip_designer_page.express_mode.unfold_properties_object_setting_tab()

            check_result = pip_designer_page.express_mode.get_object_setting_opacity_value()
            if not check_result == '100%':
                case.result = False
            else:
                case.result = True

        with uuid('7638da91-d60b-41c7-835a-dec6b9a56bde') as case:
            # 3.1. Properties
            # 3.1.1. Object Settings > Opacity > Minimum value (0%)
            # adjustment works correctly with minimum value
            pip_designer_page.input_position_opacity_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('a6b689c7-09f8-46f0-9b72-4437e4c0be4c') as case:
            # 3.1. Properties
            # 3.1.1. Object Settings > Opacity > Maximum value (100%)
            # adjustment works correctly with maximum value
            pip_designer_page.input_position_opacity_value('100')

            display_value = pip_designer_page.express_mode.get_object_setting_opacity_value()
            if not display_value == '100%':
                check_result_1 = False
            else:
                check_result_1 = True

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('7a291cbb-2112-4af8-b108-e9f80221d14c') as case:
            # 3.1. Properties
            # 3.1.1. Object Settings > Opacity > Adjust by Slider
            # opacity keyframe and previous/next works on timeline correctly
            pip_designer_page.express_mode.drag_object_setting_opacity_slider(50)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

            pip_designer_page.express_mode.drag_object_setting_opacity_slider(100)

        with uuid('35bb7809-382a-4d41-acb2-acd83d712f5c') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > Enable / Disable
            # enable / disable related settings correctly
            pip_designer_page.express_mode.unfold_properties_chroma_key_tab()
            pip_designer_page.express_mode.set_check_chromakey(1)
            pip_designer_page.exist_click(L.pip_designer.chromakey.btn_dropper)
            pip_designer_page.exist_click(L.pip_designer.preview)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview)

            pip_designer_page.express_mode.set_check_chromakey(0)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_5.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('1ba4730c-30cd-4b12-a5cf-474fc02aa738') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > Dropper
            # color display correctly after selecting color on viewer
            pip_designer_page.express_mode.set_check_chromakey(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_6.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('4c6db2b8-af74-4ecd-b89c-26890dedef78') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > Trash can (Remove) > Only one chroma key
            # it is disabled
            btn_status = pip_designer_page.express_mode.get_chromakey_remove_status()
            if not btn_status:
                case.result = True
            else:
                case.result = False

        with uuid('a82bc239-868a-4b47-bc22-97890feeae56') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > Color Range > Default value (10)
            # adjustment works correctly with default value
            check_result = pip_designer_page.exist(L.pip_designer.chromakey.color_range_value).AXValue
            if not check_result == '10':
                case.result = False
            else:
                case.result = True

        with uuid('0d5d3ab1-a864-418c-be1d-16aed4dba785') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > Color Range > Minimum value (0)
            # adjustment works correctly with minimum value
            pip_designer_page.input_color_range_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_7.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('08ab6019-3e88-401b-9154-b3396940283c') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > Color Range > Maximum value (60)
            # adjustment works correctly with maximum value
            pip_designer_page.input_color_range_value('60')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_8.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('74e605e8-7a3d-4580-a04b-a2e56d83acfe') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > Color Range > Adjust by Input
            # Rotation keyframe and previous/next works on timeline correctly
            case.result = check_result

        with uuid('94870d27-ed8d-4dfd-b8e6-17a09a587bf8') as case:
            # 2. Caption Bar
            # 2.2. Edit
            # 2.2.1. Undo > Click item
            # show previous editing status
            pip_designer_page.tap_undo_btn()
            display_value = pip_designer_page.exist(L.pip_designer.chromakey.color_range_value).AXValue
            if not display_value == '0':
                case.result = False
            else:
                case.result = True

        with uuid('d3110465-5b6d-42b6-804a-7e5a4c191813') as case:
            # 2.2. Edit
            # 2.2.2. Redo > Click item
            # show next editing status
            pip_designer_page.tap_redo_btn()
            display_value = pip_designer_page.exist(L.pip_designer.chromakey.color_range_value).AXValue
            if not display_value == '60':
                case.result = False
            else:
                case.result = True

        with uuid('c7b5d56e-e725-43b9-91d2-40101ebcd1ec') as case:
            # 2.2. Edit
            # 2.2.1. Undo > Hotkey
            # show previous editing status
            pip_designer_page.tap_Undo_hotkey()
            display_value = pip_designer_page.exist(L.pip_designer.chromakey.color_range_value).AXValue
            if not display_value == '0':
                case.result = False
            else:
                case.result = True

        with uuid('c6831526-acfe-4f37-8beb-dccd35ccf185') as case:
            # 2.2. Edit
            # 2.2.2. Redo > Hotkey
            # show next editing status
            pip_designer_page.tap_Redo_hotkey()
            display_value = pip_designer_page.exist(L.pip_designer.chromakey.color_range_value).AXValue
            if not display_value == '60':
                case.result = False
            else:
                case.result = True

        with uuid('f7f41489-256e-404e-b70a-2a96f25c77a7') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > Color Range > Adjust by Slider
            # Rotation keyframe and previous/next works on timeline correctly
            pip_designer_page.drag_color_range_slider('40')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_9.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_9.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('6a21536a-6a28-4c8d-81c2-151d8b230b06') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > Color Range > Adjust by ^/v button
            # Rotation keyframe and previous/next works on timeline correctly
            for number_of_clicks in range(20):
                pip_designer_page.click_color_range_arrow_btn(1)
            for number_of_clicks in range(10):
                pip_designer_page.click_color_range_arrow_btn(0)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_10.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_10.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('cc070dc0-9608-4e81-b763-4ba84f8a4bcf') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > DeNoise > Default value (20)
            # adjustment works correctly with default value
            check_result = pip_designer_page.exist(L.pip_designer.chromakey.denoise_value).AXValue

            if not check_result == '20':
                case.result = False
            else:
                case.result = True

        with uuid('e4aa6cb6-98f1-4dff-a374-6009d523bc25') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > DeNoise > Minimum value (0)
            # adjustment works correctly with minimum value
            pip_designer_page.input_denoise_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_11.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_11.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('cc3ee7d1-e4f3-409f-9d78-918ba8144e94') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > DeNoise > Maximum value (100)
            # adjustment works correctly with maximum value
            pip_designer_page.input_denoise_value('100')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_12.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_12.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('aec47cc8-3708-440b-9cf9-b56427a41f9d') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > DeNoise > Adjust by Input
            # Object show effect directly after adjusting
            case.result = check_result

        with uuid('687f60a6-d65a-4c05-9db9-c3cad72a206f') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > DeNoise > Adjust by Slider
            # Object show effect directly after adjusting
            pip_designer_page.drag_denoise_slider('60')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_13.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_13.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('d6a79533-6547-45cf-acae-8ea3d0d8c181') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > DeNoise > Adjust by ^/v button
            # Object show effect directly after adjusting
            for number_of_clicks in range(20):
                pip_designer_page.click_denoise_arrow_btn(1)
            for number_of_clicks in range(10):
                pip_designer_page.click_denoise_arrow_btn(0)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_14.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_14.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('45163421-e879-4e62-87bf-180104d6237d') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > Add a new key
            # add a new key setting directly
            pip_designer_page.express_mode.click_chromakey_add_new_key_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_15.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_15.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('d3a1dad4-15f1-4fe5-a8b0-931b6e2f9438') as case:
            # 3.1. Properties
            # 3.1.2. Chroma Key > Trash can (Remove) > Multiple chroma key
            # it can enable and remove chroma key directly
            btn_status = pip_designer_page.express_mode.get_chromakey_remove_status()

            pip_designer_page.express_mode.click_chromakey_remove_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_1_16.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_1_16.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = btn_status and check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid('654aa4f8-382b-4559-af46-027f92315e9c') as case:
            # 3.1. Properties
            # 3.1.3. Border > Enable / Disable
            # enable / disable related settings correctly
            main_page.enter_room(4)
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.switch_mode('Express')
            pip_designer_page.express_mode.unfold_properties_border_tab()
            pip_designer_page.express_mode.set_border_checkbox(1)

            btn_status = pip_designer_page.exist(L.pip_designer.border.size_slider).AXEnabled

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            check_result_1 = btn_status and check_result

            pip_designer_page.express_mode.set_border_checkbox(0)

            btn_status = not pip_designer_page.exist(L.pip_designer.border.size_slider).AXEnabled

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            check_result_2 = btn_status and check_result

            case.result = check_result_1 and check_result_2

            pip_designer_page.express_mode.set_border_checkbox(1)

        with uuid('11758802-33af-4709-ab60-61523b851b4f') as case:
            # 3.1. Properties
            # 3.1.3. Border > Size > Default value (3)
            # adjustment works correctly with default value
            check_result = pip_designer_page.express_mode.get_border_size_value()

            if not check_result == '3':
                case.result = False
            else:
                case.result = True

        with uuid('6418566d-6129-48f9-938c-6be49ace69ba') as case:
            # 3.1. Properties
            # 3.1.3. Border > Size > Minimum value (0)
            # adjustment works correctly with minimum value
            pip_designer_page.express_mode.input_border_size_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('bab76f4b-c296-4593-84c8-3c8ae7dada3e') as case:
            # 3.1. Properties
            # 3.1.3. Border > Size > Maximum value (10)
            # adjustment works correctly with maximum value
            pip_designer_page.express_mode.input_border_size_value('10')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('ccdac930-2de9-444d-91db-3b7f94fdaf9c') as case:
            # 3.1. Properties
            # 3.1.3. Border > Size > Adjust by Input
            # show effect directly after adjusting
            case.result = check_result

        with uuid('b788725d-3bba-4e84-bc32-d64a9067f041') as case:
            # 3.1. Properties
            # 3.1.3. Border > Size > Adjust by Slider
            # show effect directly after adjusting
            pip_designer_page.express_mode.drag_border_size_slider('5')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_5.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('b6013297-f249-40ff-8728-0dad0235c571') as case:
            # 3.1. Properties
            # 3.1.3. Border > Size > Adjust by ^/v button
            # show effect directly after adjusting
            for number_of_clicks in range(3):
                pip_designer_page.express_mode.click_border_size_arrow_btn(0)
            for number_of_clicks in range(3):
                pip_designer_page.express_mode.click_border_size_arrow_btn(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_6.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('583f6a84-65d2-49df-b20a-ef846b87f2d9') as case:
            # 3.1. Properties
            # 3.1.3. Border > Blur > Default value (0)
            # adjustment works correctly with default value
            check_result = pip_designer_page.express_mode.get_border_blur_value()

            if not check_result == '0':
                case.result = False
            else:
                case.result = True

        with uuid('2c78b81d-83cc-4c5a-8e5a-fae901861441') as case:
            # 3.1. Properties
            # 3.1.3. Border > Blur > Maximum value (20)
            # adjustment works correctly with maximum value
            pip_designer_page.express_mode.input_border_blur_value('20')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_7.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('b3fc4c66-ddf6-4097-a632-14a4bc18c46f') as case:
            # 3.1. Properties
            # 3.1.3. Border > Blur > Minimum value (0)
            # adjustment works correctly with minimum value
            pip_designer_page.express_mode.input_border_blur_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_8.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('b307b62d-b7c4-4e4b-acbc-6dfcfca3bba6') as case:
            # 3.1. Properties
            # 3.1.3. Border > Blur > Adjust by Input
            # show effect directly after adjusting
            case.result = check_result

        with uuid('cd22dbf6-d1a8-458e-bc7f-73a95bcc7717') as case:
            # 3.1. Properties
            # 3.1.3. Border > Blur > Adjust by Slider
            # show effect directly after adjusting
            pip_designer_page.express_mode.drag_border_blur_slider('10')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_9.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_9.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('7c2dfdf5-596f-44c6-b70f-1578ec8b80ff') as case:
            # 3.1. Properties
            # 3.1.3. Border > Blur > Adjust by ^/v button
            # show effect directly after adjusting
            for number_of_clicks in range(5):
                pip_designer_page.express_mode.click_border_blur_arrow_btn(0)
            for number_of_clicks in range(5):
                pip_designer_page.express_mode.click_border_blur_arrow_btn(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_10.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_10.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('83933435-cc1a-4ba4-b0be-ab1237868c40') as case:
            # 3.1. Properties
            # 3.1.3. Border > Opacity > Default value (100%)
            # adjustment works correctly with default value
            check_result = pip_designer_page.express_mode.get_border_opacity_value()

            if not check_result == '100%':
                case.result = False
            else:
                case.result = True

        with uuid('0990c9f8-e29a-432d-a910-9c82deb08a16') as case:
            # 3.1. Properties
            # 3.1.3. Border > Opacity > Minimum value (0)
            # adjustment works correctly with minimum value
            pip_designer_page.input_border_opacity_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_11.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_11.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('3cbb9827-0a51-4989-8a09-5e7e960fe148') as case:
            # 3.1. Properties
            # 3.1.3. Border > Opacity > Maximum value (100%)
            # adjustment works correctly with maximum value
            pip_designer_page.input_border_opacity_value('100')

            display_value = pip_designer_page.express_mode.get_border_opacity_value()
            if not display_value == '100%':
                check_result_1 = False
            else:
                check_result_1 = True

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_12.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_12.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('bf82e1e6-4225-44fd-834a-62d01630cf1e') as case:
            # 3.1. Properties
            # 3.1.3. Border > Opacity > Adjust by Input
            # show effect directly after adjusting
            case.result = check_result

        with uuid('f5858c64-8a13-49bf-9ef0-31a0ab3fc5b3') as case:
            # 3.1. Properties
            # 3.1.3. Border > Opacity > Adjust by Slider
            # show effect directly after adjusting
            pip_designer_page.express_mode.drag_border_opacity_slider('90')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_13.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_13.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('78195876-a681-445c-be9d-0a33a23915c0') as case:
            # 3.1. Properties
            # 3.1.3. Border > Opacity > Adjust by ^/v button
            # show effect directly after adjusting
            for number_of_clicks in range(5):
                pip_designer_page.express_mode.click_border_opacity_arrow_btn(1)
            for number_of_clicks in range(15):
                pip_designer_page.express_mode.click_border_opacity_arrow_btn(0)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_14.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_14.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('2598575e-7a5e-486f-8467-14b9987cb3db') as case:
            # 3.1. Properties
            # 3.1.3. Fill Type > Default (1 color)
            # show different color form after selecting
            pip_designer_page.express_mode.set_border_uniform_color('FF0000')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_15.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_15.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('bf3e2aa9-a599-4230-8642-97e84638517f') as case:
            # 3.1. Properties
            # 3.1.3. Fill Type > 2 Color Gradient
            # show different color form after selecting
            pip_designer_page.apply_border_2_color('0', '255', '0', '0', '0', '255')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_16.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_16.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('20eb41f2-a813-4165-acf2-1fc13b7f947d') as case:
            # 3.1. Properties
            # 3.1.3. Fill Type > 4 Color Gradient
            # show different color form after selecting
            pip_designer_page.apply_border_4_color(
                '0', '255', '0', '0', '0', '255', '255', '0', '0', '255', '255', '255')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_3_17.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_3_17.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('534bf701-e281-4c62-850f-b10d304fe2fb') as case:
            # 3.1. Properties
            # 3.1.3. Uniform Color > Basic colors
            # show color effect on viewer directly after selecting
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid('6a25aad7-18db-4637-a41b-756d91706de7') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Enable / Disable
            # enable / disable related settings correctly
            main_page.enter_room(4)
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.switch_mode('Express')
            pip_designer_page.express_mode.unfold_properties_border_tab(1)
            pip_designer_page.express_mode.set_border_checkbox(1)
            pip_designer_page.express_mode.drag_border_size_slider('8')
            pip_designer_page.express_mode.unfold_properties_shadow_tab(1)
            time.sleep(DELAY_TIME)
            pip_designer_page.express_mode.set_shadow_checkbox(1)

            btn_status = pip_designer_page.exist(L.pip_designer.shadow.distance_slider).AXEnabled

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_4_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_4_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            check_result_1 = btn_status and check_result

            pip_designer_page.express_mode.set_shadow_checkbox(0)

            btn_status = not pip_designer_page.exist(L.pip_designer.shadow.distance_slider).AXEnabled

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_4_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_4_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            check_result_2 = btn_status and check_result

            case.result = check_result_1 and check_result_2

            pip_designer_page.apply_shadow(1)

        with uuid('9e1b45d1-ebee-48cb-8465-5e0fdace9e46') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Distance > Default value (3)
            # adjustment works correctly with default value
            check_result = pip_designer_page.express_mode.get_shadow_distance_value()

            if not check_result == '3.0':
                case.result = False
            else:
                case.result = True

        with uuid('4e17ec66-a6ac-4df7-86fe-4b3789f281c5') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Distance > Minimum value (0)
            # adjustment works correctly with minimum value
            pip_designer_page.express_mode.input_shadow_distance_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_4_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_4_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('28c38e3d-1841-474b-a997-0253c6feb627') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Distance > Maximum value (100)
            # adjustment works correctly with maximum value
            pip_designer_page.express_mode.input_shadow_distance_value('100')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_4_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_4_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('ffb87e60-ce78-4d77-b50c-66e6ae87d8e0') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Distance > Adjust by Input
            # show effect directly after adjusting
            case.result = check_result

        with uuid('6b172f2a-657a-4b7a-8f1f-3d0c3d1fb5e5') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Distance > Adjust by Slider
            # show effect directly after adjusting
            pip_designer_page.express_mode.drag_shadow_distance_slider('10')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_4_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_4_5.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('c378f060-d461-4f10-9c13-b4cf83532282') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Distance > Adjust by ^/v button
            # show effect directly after adjusting
            for number_of_clicks in range(20):
                pip_designer_page.express_mode.click_shadow_distance_arrow_btn(0)
            for number_of_clicks in range(10):
                pip_designer_page.express_mode.click_shadow_distance_arrow_btn(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_4_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_4_6.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('856718bb-f486-4385-8c44-3c368b719923') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Blur > Default value (0)
            # adjustment works correctly with default value
            check_result = pip_designer_page.express_mode.get_shadow_blur_value()

            if not check_result == '0':
                case.result = False
            else:
                case.result = True

        with uuid('587dba90-7995-4517-8456-c328ea53c641') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Blur > Maximum value (20)
            # adjustment works correctly with maximum value
            pip_designer_page.express_mode.input_shadow_blur_value('20')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_4_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_4_7.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('a3f18b5d-8e98-413e-9497-2a2b7700265b') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Blur > Minimum value (0)
            # adjustment works correctly with minimum value
            pip_designer_page.express_mode.input_shadow_blur_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_4_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_4_8.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('5b4a40f3-e740-46de-809b-0d69180e11ea') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Blur > Adjust by Input
            # show effect directly after adjusting
            case.result = check_result

        with uuid('9f87e740-2804-4564-a454-8ec0711496c8') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Blur > Adjust by Slider
            # show effect directly after adjusting
            pip_designer_page.express_mode.drag_shadow_blur_slider('10')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_4_9.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_4_9.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('07d7efac-f547-454d-a8e3-c8456bda69d8') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Blur > Adjust by ^/v button
            # show effect directly after adjusting
            for number_of_clicks in range(5):
                pip_designer_page.express_mode.click_shadow_blur_arrow_btn(0)
            for number_of_clicks in range(5):
                pip_designer_page.express_mode.click_shadow_blur_arrow_btn(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_4_10.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_4_10.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('ecc5e255-a144-4161-8407-c1b494583515') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Opacity > Default value (100%)
            # adjustment works correctly with default value
            check_result = pip_designer_page.express_mode.get_shadow_opacity_value()

            if not check_result == '100%':
                case.result = False
            else:
                case.result = True

        with uuid('1f57a35d-ca46-4c8b-884e-dd212820d6ea') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Opacity > Minimum value (0)
            # adjustment works correctly with minimum value
            pip_designer_page.input_shadow_opacity_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_4_11.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_4_11.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('79b85a32-5fe1-4a41-8bb4-a73a3f87069b') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Opacity > Adjust by Input
            # show effect directly after adjusting
            case.result = check_result

        with uuid('61168835-44e9-409e-a35f-8aba73f42029') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Opacity > Maximum value (100%)
            # adjustment works correctly with maximum value
            pip_designer_page.input_shadow_opacity_value('100')

            display_value = pip_designer_page.express_mode.get_shadow_opacity_value()
            if not display_value == '100%':
                check_result_1 = False
            else:
                check_result_1 = True

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_4_12.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_4_12.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('41dc1a04-60e3-4263-ae93-c456af09c13d') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Opacity > Adjust by Slider
            # show effect directly after adjusting
            pip_designer_page.express_mode.drag_shadow_opacity_slider('90')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_4_13.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_4_13.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('57674817-a50b-494c-9836-5bfafcca6113') as case:
            # 3.1. Properties
            # 3.1.4. Shadow > Opacity > Adjust by ^/v button
            # show effect directly after adjusting
            for number_of_clicks in range(5):
                pip_designer_page.express_mode.click_shadow_opacity_arrow_btn(1)
            for number_of_clicks in range(15):
                pip_designer_page.express_mode.click_shadow_opacity_arrow_btn(0)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_4_14.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_4_14.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('d56a7b26-1e34-4e3c-9205-e6acd554003b') as case:
            # 3.1. Properties
            # 3.1.4. Select color > Basic colors
            # show selected color directly after adjusting
            pip_designer_page.express_mode.set_shadow_select_color('ff0000')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_4_15.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_4_15.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('cf4b22cc-125b-4bc9-bc26-0250e9f9d6d5') as case:
            # 3.1. Properties
            # 3.1.5. Fades > Enable / Disable
            # enable / disable related settings correctly
            pip_designer_page.express_mode.unfold_properties_fades_tab(0, 1)
            time.sleep(DELAY_TIME)
            check_result_1 = pip_designer_page.express_mode.set_fades_checkbox(1)
            check_result_2 = pip_designer_page.express_mode.set_fades_checkbox(0)

            case.result = check_result_1 and check_result_2

            pip_designer_page.express_mode.set_fades_checkbox(1)

        with uuid('dff99275-ab6b-4fa4-9bf6-b4cc211d019f') as case:
            # 3.1. Properties
            # 3.1.5. Fades > Enable fade-in
            # object show fade-in while previewing
            pip_designer_page.express_mode.set_enable_fade_in_checkbox(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_5_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_5_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('123b8e4f-28a0-43bb-b303-f3b1031939b4') as case:
            # 3.1. Properties
            # 3.1.5. Fades > Enable fade-out
            # object show fade-out while previewing
            pip_designer_page.express_mode.set_enable_fade_out_checkbox(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_3_1_5_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_3_1_5_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid('15373155-ba15-4bc3-a7ad-2ec10a51ff11') as case:
            # 4. Advanced Mode
            # 4.1. Properties
            # 4.1.1. Object Settings > Position > X position
            # show correct object position correctly
            main_page.enter_room(4)
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.switch_mode('Advanced')
            pip_designer_page.exist_click(L.pip_designer.object_setting.object_setting)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('a57a5054-4820-4083-8295-a466ec8b7d89') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position > Y position
            # show correct object position correctly
            case.result = check_result

        with uuid('d81d1d28-f07a-4216-abf4-6f55ca6b8219') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position > Default value
            # default (0.500)
            check_result_1 = pip_designer_page.exist(L.pip_designer.object_setting.x_position_value).AXValue
            check_result_2 = pip_designer_page.exist(L.pip_designer.object_setting.y_position_value).AXValue

            check_result = check_result_1 == '0.500' and check_result_2 == '0.500'
            if not check_result:
                case.result = False
            else:
                case.result = True

        with uuid('0bc536fc-dab4-40ea-a094-8d954badb2cd') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position > Max. value
            # maximum (2.0)
            pip_designer_page.input_x_position_value('2.000')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview)

            pip_designer_page.input_x_position_value('0.500')
            pip_designer_page.input_y_position_value('2.000')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

            pip_designer_page.input_y_position_value('0.500')

        with uuid('665f21af-1e3e-418f-b5b4-3b8bdd7b2f47') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position > Min. value
            # minimum (-2)
            pip_designer_page.input_x_position_value('-2.000')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview)

            pip_designer_page.input_x_position_value('0.500')
            pip_designer_page.input_y_position_value('-2.000')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_5.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2
            pip_designer_page.input_y_position_value('0.500')

        with uuid('9c568d4c-96f4-4057-9399-cae466525cf5') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position > Adjust by input
            # adjust correctly
            case.result = check_result_1 and check_result_2

        with uuid('20d0a13d-4cc4-4f99-8989-eaa4fbd55a50') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position > Adjust by ^/v
            # adjust correctly
            for number_of_clicks in range(80):
                pip_designer_page.click_x_position_arrow_btn(0)
            for number_of_clicks in range(30):
                pip_designer_page.click_x_position_arrow_btn(1)
            for number_of_clicks in range(80):
                pip_designer_page.click_y_position_arrow_btn(0)
            for number_of_clicks in range(30):
                pip_designer_page.click_y_position_arrow_btn(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_6.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('80acfc35-b9d2-4eaa-8c71-c3b92298e68b') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position > Add/Remove keyframe
            # add keyframe
            pip_designer_page.set_timecode('00_00_02_00')
            pip_designer_page.add_remove_position_current_keyframe()
            pip_designer_page.set_timecode('00_00_04_00')
            pip_designer_page.add_remove_position_current_keyframe()
            pip_designer_page.set_timecode('00_00_06_00')
            pip_designer_page.add_remove_position_current_keyframe()
            pip_designer_page.set_timecode('00_00_08_00')
            pip_designer_page.add_remove_position_current_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_7.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('4b4f29b4-8de1-41e6-a61a-00fb18a3d849') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position > Add/Remove keyframe
            # remove current selected keyframe
            pip_designer_page.add_remove_position_current_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_8.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('6a2b44d6-1a4f-4de7-86d2-7e10bad97a45') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position > Previous keyframe
            # switch to previous keyframe
            pip_designer_page.tap_position_previous_keyframe()
            pip_designer_page.tap_position_previous_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_9.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_9.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('322f002c-4b15-4b3e-a1ae-90e537ea1f7f') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position>Ease in & Ease out > Default value
            # default is 0.4
            pip_designer_page.click_position_ease_in_checkbox(1)
            check_result_1 = pip_designer_page.exist(L.pip_designer.object_setting.ease_in_value).AXValue
            pip_designer_page.click_position_ease_out_checkbox(1)
            check_result_2 = pip_designer_page.exist(L.pip_designer.object_setting.ease_out_value).AXValue

            check_result = check_result_1 == '0.40' and check_result_2 == '0.40'
            if not check_result:
                case.result = False
            else:
                case.result = True

        with uuid('4429badf-8751-42d4-8d3c-fcd118481f02') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position>Ease in & Ease out > Max value
            # max is 1.0
            pip_designer_page.input_position_ease_in_value('1.0')
            pip_designer_page.input_position_ease_out_value('1.0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_10.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_10.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

            pip_designer_page.input_position_ease_in_value('0.40')
            pip_designer_page.input_position_ease_out_value('0.40')

        with uuid('6c903b13-04fa-42f2-b0ac-a5144374a3c9') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position>Ease in & Ease out > Adjust by input
            # adjust correctly
            case.result = check_result

        with uuid('42b1c7c8-77e7-4f86-b646-aa144eb20278') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position>Ease in & Ease out > Min value
            # min is 0.01
            pip_designer_page.input_position_ease_in_value('0.01')
            pip_designer_page.input_position_ease_out_value('0.01')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_11.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_11.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('9b509f24-d547-4b03-ac37-8469e61cb455') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position>Ease in & Ease out > Adjust by Slider
            # adjust correctly
            pip_designer_page.drag_position_ease_in_slider('0.5')
            pip_designer_page.drag_position_ease_out_slider('0.5')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_12.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_12.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('77e210d8-8fb3-43c1-8de8-7653f84461ca') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position>Ease in & Ease out > Adjust by ^/v
            # adjust correctly
            for number_of_clicks in range(30):
                pip_designer_page.click_position_ease_in_arrow_btn(0)
            for number_of_clicks in range(10):
                pip_designer_page.click_position_ease_in_arrow_btn(1)
            for number_of_clicks in range(30):
                pip_designer_page.click_position_ease_out_arrow_btn(0)
            for number_of_clicks in range(10):
                pip_designer_page.click_position_ease_out_arrow_btn(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_13.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_13.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('79ce6cd0-3167-4e04-a674-df140b84058c') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position > Next keyframe
            # switch to next keyframe
            pip_designer_page.tap_position_next_keyframe()
            pip_designer_page.tap_position_next_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_14.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_14.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('f64c2041-57b8-406b-96c8-742c5f312a55') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Position > Reset keyframe
            # reset all keyframes
            pip_designer_page.reset_position_keyframe()
            pip_designer_page.click_yes_on_reset_all_keyframe_dialog()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_15.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_15.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid('09467587-40d1-409b-b69a-8da7d9d6d528') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale > Default value
            # default 1.0
            main_page.enter_room(4)
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.switch_mode('Advanced')
            pip_designer_page.exist_click(L.pip_designer.object_setting.object_setting)

            check_result = pip_designer_page.exist(L.pip_designer.object_setting.scale.height_value).AXValue
            if not check_result == '1.000':
                case.result = False
            else:
                case.result = True

        with uuid('786e4072-3015-4c46-9016-d71df427d52f') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale > Max value
            # maximum 6.000
            pip_designer_page.drag_scale_height_slider(value=100)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_15.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_15.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview)

            current_value = pip_designer_page.exist(L.pip_designer.object_setting.scale.height_value).AXValue
            check_result_2 = False if not current_value == '6.000' else True

            case.result = check_result_1 and check_result_2

            pip_designer_page.input_scale_height_value('1.000')

        with uuid('bb393569-5d95-41b5-90ce-1e843f710a35') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale > Min value
            # minimum 0.001
            pip_designer_page.drag_scale_height_slider(value=0)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_16.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_16.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview)

            current_value = pip_designer_page.exist(L.pip_designer.object_setting.scale.height_value).AXValue
            check_result_2 = False if not current_value == '0.001' else True

            case.result = check_result_1 and check_result_2

        with uuid('c727562a-b184-4262-8519-1fbf5dfe5029') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale > Adjust by input
            # adjust correctly
            check_result_1 = pip_designer_page.input_scale_height_value('1')
            current_value = pip_designer_page.exist(L.pip_designer.object_setting.scale.height_value).AXValue
            check_result_2 = False if not current_value == '1.000' else True

            case.result = check_result_1 and check_result_2

        with uuid('e3a4ebbb-95ad-4886-a51b-6c0f1c837366') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale > Adjust by Slider
            # adjust correctly
            pip_designer_page.drag_scale_height_slider(0.3)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_17.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_17.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

            pip_designer_page.input_scale_height_value('1.000')

        with uuid('1bd71693-c3f7-4e76-8395-d322f133a39e') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale > Adjust by ^/v
            # adjust correctly
            for number_of_clicks in range(20):
                pip_designer_page.click_scale_width_arrow_btn(0)
            for number_of_clicks in range(10):
                pip_designer_page.click_scale_width_arrow_btn(1)
            for number_of_clicks in range(20):
                pip_designer_page.click_scale_height_arrow_btn(0)
            for number_of_clicks in range(10):
                pip_designer_page.click_scale_height_arrow_btn(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_18.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_18.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('7d788275-e98d-44e2-832b-9883652d6ae0') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale > Maintain aspect ratio
            # keep aspect ratio if select checkbox
            width_value = pip_designer_page.exist(L.pip_designer.object_setting.scale.width_value).AXValue
            height_value = pip_designer_page.exist(L.pip_designer.object_setting.scale.height_value).AXValue

            if not width_value == height_value:
                case.result = True
            else:
                case.result = False

        with uuid('09eb6df2-d75d-4e44-84cf-fe42a2e42356') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale > Add/Remove keyframe
            # add keyframe
            pip_designer_page.set_timecode('00_00_02_00')
            pip_designer_page.add_remove_scale_current_keyframe()
            pip_designer_page.set_timecode('00_00_04_00')
            pip_designer_page.add_remove_scale_current_keyframe()
            pip_designer_page.set_timecode('00_00_06_00')
            pip_designer_page.add_remove_scale_current_keyframe()
            pip_designer_page.set_timecode('00_00_08_00')
            pip_designer_page.add_remove_scale_current_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_19.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_19.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('b46e20cf-cc05-4dd1-a0be-8e91c38729a3') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale > Add/Remove keyframe
            # remove current selected keyframe
            pip_designer_page.add_remove_scale_current_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_20.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_20.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('caa78c53-db4e-4373-a476-c3f5e231434b') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale > Previous keyframe
            # switch to previous keyframe
            pip_designer_page.tap_scale_previous_keyframe()
            pip_designer_page.tap_scale_previous_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_21.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_21.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('cc3d7899-2a29-4278-9d3a-3d40d7682466') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale>Ease in & Ease out > Default value
            # default is 0.4
            pip_designer_page.click_scale_ease_in_checkbox(1)
            check_result_1 = pip_designer_page.exist(L.pip_designer.object_setting.scale.ease_in_value).AXValue
            pip_designer_page.click_scale_ease_out_checkbox(1)
            check_result_2 = pip_designer_page.exist(L.pip_designer.object_setting.scale.ease_out_value).AXValue

            check_result = check_result_1 == '0.40' and check_result_2 == '0.40'
            if not check_result:
                case.result = False
            else:
                case.result = True

        with uuid('25bcf300-d722-4057-b708-98368a3bc4cb') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale>Ease in & Ease out > Max value
            # max is 1.0
            pip_designer_page.input_scale_ease_in_value('1.00')
            pip_designer_page.input_scale_ease_out_value('1.00')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_22.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_22.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

            pip_designer_page.input_scale_ease_in_value('0.40')
            pip_designer_page.input_scale_ease_out_value('0.40')

        with uuid('c9546e91-9e08-4011-aefc-242b44c5bca8') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale>Ease in & Ease out > Min value
            # min is 0.01
            pip_designer_page.input_scale_ease_in_value('0.01')
            pip_designer_page.input_scale_ease_out_value('0.01')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_23.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_23.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('40e29eea-4dca-4899-956a-d848e1daadea') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale>Ease in & Ease out > Adjust by input
            # adjust correctly
            case.result = check_result

        with uuid('a8e69f4d-ff85-47cd-b4f2-60909467ff96') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale>Ease in & Ease out > Adjust by Slider
            # adjust correctly
            pip_designer_page.drag_scale_ease_in_slider('0.5')
            pip_designer_page.drag_scale_ease_out_slider('0.5')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_24.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_24.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('95b28d85-4e7f-4b2e-abf5-2fa579386202') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale>Ease in & Ease out > Adjust by ^/v
            # adjust correctly
            for number_of_clicks in range(20):
                pip_designer_page.click_scale_ease_in_arrow_btn(0)
            for number_of_clicks in range(10):
                pip_designer_page.click_scale_ease_in_arrow_btn(1)
            for number_of_clicks in range(20):
                pip_designer_page.click_scale_ease_out_arrow_btn(0)
            for number_of_clicks in range(10):
                pip_designer_page.click_scale_ease_out_arrow_btn(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_25.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_25.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('7c5d47e7-26dd-420b-b75c-f0f1aba61a2e') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale > Width adjustment
            # scale keyframe adn previous/next works on timeline correctly
            pip_designer_page.tap_scale_previous_keyframe()
            pip_designer_page.input_scale_width_value('0.500')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_26.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_26.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('578010ce-d1d0-4511-997d-e132322cdbef') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale > Height adjustment
            # scale keyframe adn previous/next works on timeline correctly
            pip_designer_page.tap_scale_next_keyframe()
            pip_designer_page.input_scale_width_value('1.000')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_27.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_27.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('f96333e1-a2c9-42b6-9079-76ed5ec3e2a0') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale > Next keyframe
            # switch to next keyframe
            pip_designer_page.tap_scale_next_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_28.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_28.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('b7f77c09-80c8-437d-93d2-a8e2ba92ce2d') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Scale > Reset keyframe
            # reset all keyframe
            pip_designer_page.reset_scale_keyframe()
            pip_designer_page.click_yes_on_reset_all_keyframe_dialog()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_29.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_29.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        with uuid('8179bb19-35e9-4819-a4fe-9ac83b14c5be') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Opacity > Default value
            # 100%
            main_page.enter_room(4)
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.switch_mode('Advanced')
            pip_designer_page.exist_click(L.pip_designer.object_setting.object_setting)
            pip_designer_page.drag_properties_scroll_bar(1.0)

            check_result = pip_designer_page.exist(L.pip_designer.object_setting.opacity.opacity_value).AXValue
            if not check_result == '100%':
                case.result = False
            else:
                case.result = True

        with uuid('2c961a91-bae6-48c1-a104-d2ce00df3d48') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Opacity > Minimum value
            # 0%
            pip_designer_page.input_position_opacity_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_30.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_30.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('dcf69f72-c4ab-47a6-adf5-d8f237e79291') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Opacity > Adjust by Input
            # adjust correctly
            case.result = check_result

        with uuid('78d7d2a0-07f5-46a7-a297-9786b4d71cf4') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Opacity > Maximum value
            # 100%
            pip_designer_page.input_position_opacity_value('100')

            display_value = pip_designer_page.exist(L.pip_designer.object_setting.opacity.opacity_value).AXValue
            if not display_value == '100%':
                check_result_1 = False
            else:
                check_result_1 = True

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_31.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_31.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('7956ff38-5a66-4695-8578-d3e8ce76383a') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Opacity > Adjust by Slider
            # adjust correctly
            pip_designer_page.drag_position_opacity_slider(50)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_32.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_32.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('d155cc65-f61e-4fd0-8848-bd716fde5811') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Opacity > Adjust by ^/v button
            # adjust correctly
            for number_of_clicks in range(20):
                pip_designer_page.click_position_opacity_arrow_btn(0)
            for number_of_clicks in range(10):
                pip_designer_page.click_position_opacity_arrow_btn(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_33.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_33.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('395f060f-bb1d-49ee-8906-3aa68eb04b4d') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Opacity > Add/Remove keyframe
            # add keyframe
            pip_designer_page.set_timecode('00_00_02_00')
            pip_designer_page.add_remove_position_opacity_current_keyframe()
            pip_designer_page.set_timecode('00_00_04_00')
            pip_designer_page.add_remove_position_opacity_current_keyframe()
            pip_designer_page.set_timecode('00_00_06_00')
            pip_designer_page.add_remove_position_opacity_current_keyframe()
            pip_designer_page.set_timecode('00_00_08_00')
            pip_designer_page.add_remove_position_opacity_current_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_34.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_34.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('2dd34b6d-0634-452a-b55e-be319712899c') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Opacity > Add/Remove keyframe
            # remove current selected keyframe
            pip_designer_page.add_remove_position_opacity_current_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_35.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_35.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('5e676858-d869-4b2d-9435-93521f6a6cee') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Opacity > Previous keyframe
            # switch to previous keyframe
            pip_designer_page.tap_position_opacity_previous_keyframe()
            pip_designer_page.tap_position_opacity_previous_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_36.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_36.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('ff9e6393-f3d6-48e2-a46f-d8d8296a2537') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Opacity > Next keyframe
            # switch to next keyframe
            pip_designer_page.tap_position_opacity_next_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_37.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_37.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('7698d585-9da8-463d-b6de-ddac21a181f7') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Opacity > Reset keyframe
            # reset all keyframes
            pip_designer_page.reset_position_opacity_keyframe()
            pip_designer_page.click_yes_on_reset_all_keyframe_dialog()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_38.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_38.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        with uuid('3ed3498b-fbe2-4938-b1c2-898a9076431e') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Default value
            # 0
            main_page.enter_room(4)
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.switch_mode('Advanced')
            pip_designer_page.exist_click(L.pip_designer.object_setting.object_setting)
            pip_designer_page.drag_properties_scroll_bar(1.0)
            pip_designer_page.drag_keyframe_scroll_bar(1.0)

            check_result = pip_designer_page.exist(L.pip_designer.object_setting.rotation.degree_value).AXValue
            if not check_result == '0.00':
                case.result = False
            else:
                case.result = True

        with uuid('0da8edbd-52a3-4c85-9a87-3c4c944406d1') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Minimum value
            # -9999
            pip_designer_page.input_rotation_degree_value('-9999')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_39.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_39.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('90559a7d-56fe-4d43-867f-a8ac10a1db61') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Maximum value
            # 9999
            pip_designer_page.input_rotation_degree_value('9999')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_40.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_40.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

            pip_designer_page.input_rotation_degree_value('0')

        with uuid('f8c936b3-19a6-4fa6-8ede-dd064afd5380') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Adjust by Input
            # adjust correctly
            case.result = check_result

        with uuid('6346df8e-9e17-4fce-8ac6-ba575521936d') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Adjust by ^/v button
            # adjust correctly
            for number_of_clicks in range(50):
                pip_designer_page.click_rotation_degree_arrow_btn(0)
            for number_of_clicks in range(10):
                pip_designer_page.click_rotation_degree_arrow_btn(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_41.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_41.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('d3bca986-f789-461a-be42-4ec3f0d99095') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Add/Remove keyframe
            # add keyframe
            pip_designer_page.set_timecode('00_00_02_00')
            pip_designer_page.add_remove_rotation_current_keyframe()
            pip_designer_page.set_timecode('00_00_04_00')
            pip_designer_page.add_remove_rotation_current_keyframe()
            pip_designer_page.set_timecode('00_00_06_00')
            pip_designer_page.add_remove_rotation_current_keyframe()
            pip_designer_page.set_timecode('00_00_08_00')
            pip_designer_page.add_remove_rotation_current_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_42.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_42.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('ea557e49-5af1-4aed-9baf-195c4ceb8c38') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Add/Remove keyframe
            # remove current selected keyframe
            pip_designer_page.add_remove_rotation_current_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_43.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_43.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('2b983879-f50c-4e4f-9d5a-d809e6437138') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Previous keyframe
            # switch to previous keyframe
            pip_designer_page.tap_rotation_previous_keyframe()
            pip_designer_page.tap_rotation_previous_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_44.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_44.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('fcd019e3-560e-4556-b251-d25ed72c12a1') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Ease in & Ease out > Default value
            # default is 0.40
            pip_designer_page.click_rotation_ease_in_checkbox(1)
            check_result_1 = pip_designer_page.exist(L.pip_designer.object_setting.rotation.ease_in_value).AXValue
            pip_designer_page.click_rotation_ease_out_checkbox(1)
            check_result_2 = pip_designer_page.exist(L.pip_designer.object_setting.rotation.ease_out_value).AXValue

            check_result = check_result_1 == '0.40' and check_result_2 == '0.40'
            if not check_result:
                case.result = False
            else:
                case.result = True

        with uuid('71436c72-35da-4c2c-968a-3a1ffe77c2ba') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Ease in & Ease out > Max value
            # max is 1.00
            pip_designer_page.input_rotation_ease_in_value('1.00')
            pip_designer_page.input_rotation_ease_out_value('1.00')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_45.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_45.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

            pip_designer_page.input_rotation_ease_in_value('0.40')
            pip_designer_page.input_rotation_ease_out_value('0.40')

        with uuid('e8727218-be19-4a14-8e75-eaeacbbb2cbe') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Ease in & Ease out > Min value
            # min is 0.01
            pip_designer_page.input_rotation_ease_in_value('0.01')
            pip_designer_page.input_rotation_ease_out_value('0.01')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_46.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_46.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('59069ad8-b71f-47fe-bcd0-22c2d21bb19a') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Ease in & Ease out > Adjust by Input
            # adjust correctly
            case.result = check_result

        with uuid('3f8516e9-b01a-4469-86e6-33428761001d') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Ease in & Ease out > Adjust by Slider
            # adjust correctly
            pip_designer_page.drag_rotation_ease_in_slider('0.5')
            pip_designer_page.drag_rotation_ease_out_slider('0.5')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_47.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_47.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('8e4404f2-7fa5-4c12-b1df-c98060083391') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Ease in & Ease out > Adjust by ^/v
            # adjust correctly
            for number_of_clicks in range(20):
                pip_designer_page.click_rotation_ease_in_arrow_btn(0)
            for number_of_clicks in range(10):
                pip_designer_page.click_rotation_ease_in_arrow_btn(1)
            for number_of_clicks in range(20):
                pip_designer_page.click_rotation_ease_out_arrow_btn(0)
            for number_of_clicks in range(10):
                pip_designer_page.click_rotation_ease_out_arrow_btn(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_48.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_48.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('696eae8f-19a1-450d-8648-ec6b8aea29c2') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Next keyframe
            # switch to next keyframe
            pip_designer_page.tap_rotation_next_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_49.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_49.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('af8bae87-ffac-4c37-a56c-18676394351c') as case:
            # 4.1. Properties
            # 4.1.1. Object Settings > Rotation > Reset keyframe
            # reset all keyframes
            pip_designer_page.reset_rotation_keyframe()
            pip_designer_page.click_yes_on_reset_all_keyframe_dialog()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_1_50.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_1_50.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        with uuid('42a143e7-2332-4aed-9df1-0d1df0f4d5f2') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > Enable / Disable
            # enable/disable related settings correctly
            main_page.enter_room(4)
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.switch_mode('Advanced')
            pip_designer_page.apply_chromakey(1)
            pip_designer_page.exist_click(L.pip_designer.chromakey.btn_dropper)
            pip_designer_page.exist_click(L.pip_designer.preview)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_2_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_2_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview)

            pip_designer_page.apply_chromakey(0)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_2_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_2_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('bd7f8af5-f189-4ee3-b761-b73469ebf09c') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > Dropper
            # color display correctly after selecting color on viewer
            pip_designer_page.apply_chromakey(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_2_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_2_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('1bb6f65b-03a8-418d-af72-ef21050fcc90') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > Trash can (Remove) > Only one chroma key
            # it is disabled
            check_result = pip_designer_page.exist(L.pip_designer.chromakey.btn_remove).AXEnabled
            if not check_result:
                case.result = True
            else:
                case.result = False

        with uuid('6814b160-5bba-458f-95e2-e8131834e9c4') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > Color Range > Default value (10)
            # adjustment works correctly with default value
            check_result = pip_designer_page.exist(L.pip_designer.chromakey.color_range_value).AXValue
            if not check_result == '10':
                case.result = False
            else:
                case.result = True

        with uuid('10eb28c5-0248-4781-b68f-a9ca355bbe89') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > Color Range > Minimum value (0)
            # adjustment works correctly with minimum value
            pip_designer_page.input_color_range_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_2_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_2_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('8a503d9b-38f9-43d1-980e-4d3a1ff8db55') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > Color Range > Maximum value (60)
            # adjustment works correctly with maximum value
            pip_designer_page.input_color_range_value('60')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_2_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_2_5.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('93a9670e-33eb-4c33-b5a5-404f309e5b94') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > Color Range > Adjust by Input
            # object show effect directly after adjusting
            case.result = check_result

        with uuid('82e102e9-68de-4a53-be6f-a70f78085e1a') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > Color Range > Adjust by Slider
            # object show effect directly after adjusting
            pip_designer_page.drag_color_range_slider('40')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_2_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_2_6.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('35c7aadc-dad0-4494-9230-e7d02a6b32c6') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > Color Range > Adjust by ^/v button
            # object show effect directly after adjusting
            for number_of_clicks in range(20):
                pip_designer_page.click_color_range_arrow_btn(1)
            for number_of_clicks in range(10):
                pip_designer_page.click_color_range_arrow_btn(0)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_2_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_2_7.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('3db6d8cd-613a-4a69-9581-953328d09a9c') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > DeNoise > Default value (20)
            # adjustment works correctly with default value
            check_result = pip_designer_page.exist(L.pip_designer.chromakey.denoise_value).AXValue

            if not check_result == '20':
                case.result = False
            else:
                case.result = True

        with uuid('74c72d40-9302-4459-b1c9-9899458d39f4') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > DeNoise > Minimum value (0)
            # adjustment works correctly with minimum value
            pip_designer_page.input_denoise_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_2_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_2_8.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('74b9fb64-f158-4f07-96cf-5c881f287044') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > DeNoise > Maximum value (100)
            # adjustment works correctly with maximum value
            pip_designer_page.input_denoise_value('100')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_2_9.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_2_9.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('750ad124-a424-4415-b33f-0bfdbfb81cc5') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > DeNoise > Adjust by Input
            # object show effect directly after adjusting
            case.result = check_result

        with uuid('f959d094-3663-4803-a589-b5fc0c0dafad') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > DeNoise > Adjust by Slider
            # object show effect directly after adjusting
            pip_designer_page.drag_denoise_slider('60')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_2_10.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_2_10.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('f6ea3dd1-2704-4d23-9503-ab270ea31a66') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > DeNoise > Adjust by ^/v button
            # object show effect directly after adjusting
            for number_of_clicks in range(20):
                pip_designer_page.click_denoise_arrow_btn(1)
            for number_of_clicks in range(10):
                pip_designer_page.click_denoise_arrow_btn(0)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_2_11.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_2_11.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('1c6d03e6-f0a6-4529-b713-3d624f310307') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > Add a new key
            # add a new key setting directly
            pip_designer_page.add_chromakey_new_key()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_2_12.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_2_12.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('aa5e5149-3422-4e60-9e4a-463f85f10c3b') as case:
            # 4.1. Properties
            # 4.1.2. Chroma Key > Trash can (Remove) > Multiple chroma key
            # it can enable and remove chroma key directly
            btn_status = pip_designer_page.exist(L.pip_designer.chromakey.btn_remove).AXEnabled

            pip_designer_page.tap_chromakey_remove_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_2_13.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_2_13.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = btn_status and check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_1(self):
        with uuid('11b82e81-74ab-409c-aea5-c230c2f067f3') as case:
            # 4.1. Properties
            # 4.1.3. Border > Enable / Disable
            # enable/disable related settings correctly
            main_page.enter_room(4)
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.switch_mode('Advanced')
            pip_designer_page.apply_border(1)

            btn_status = pip_designer_page.exist(L.pip_designer.border.size_slider).AXEnabled

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            check_result_1 = btn_status and check_result

            pip_designer_page.apply_border(0)

            btn_status = not pip_designer_page.exist(L.pip_designer.border.size_slider).AXEnabled

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            check_result_2 = btn_status and check_result

            case.result = check_result_1 and check_result_2

            pip_designer_page.apply_border(1)

        with uuid('70c9ca71-7fc0-450e-94c9-f3ff499286f2') as case:
            # 4.1. Properties
            # 4.1.3. Border > Size > Default value (3)
            # adjustment works correctly with default value
            check_result = pip_designer_page.exist(L.pip_designer.border.size_value).AXValue

            if not check_result == '3':
                case.result = False
            else:
                case.result = True

        with uuid('0f91a3a6-2aed-4551-88b6-83f7d04652ec') as case:
            # 4.1. Properties
            # 4.1.3. Border > Size > Minimum value (0)
            # adjustment works correctly with minimum value
            pip_designer_page.input_border_size_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('7d8d98bd-5e60-462c-93ec-4e3d909f92cf') as case:
            # 4.1. Properties
            # 4.1.3. Border > Size > Maximum value (10)
            # adjustment works correctly with maximum value
            pip_designer_page.input_border_size_value('10')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('a79a0648-87e9-4315-885a-0f0be6929ff6') as case:
            # 4.1. Properties
            # 4.1.3. Border > Size > Adjust by Input
            # show effect directly after adjusting
            case.result = check_result

        with uuid('7069d4f4-bf3f-4bbd-b877-d9863ef0074e') as case:
            # 4.1. Properties
            # 4.1.3. Border > Size > Adjust by Slider
            # show effect directly after adjusting
            pip_designer_page.drag_border_size_slider('5')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_5.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('753a03a5-ab20-455e-9bf1-1eb05c8ecd73') as case:
            # 4.1. Properties
            # 4.1.3. Border > Size > Adjust by ^/v button
            # show effect directly after adjusting
            for number_of_clicks in range(3):
                pip_designer_page.click_border_size_arrow_btn(0)
            for number_of_clicks in range(3):
                pip_designer_page.click_border_size_arrow_btn(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_6.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('28637ede-0ac8-45e2-89ce-7230fde81f68') as case:
            # 4.1. Properties
            # 4.1.3. Border > Blur > Default value (0)
            # adjustment works correctly with default value
            check_result = pip_designer_page.exist(L.pip_designer.border.blur_value).AXValue

            if not check_result == '0':
                case.result = False
            else:
                case.result = True

        with uuid('e34e0744-423d-4123-9049-4a1f47dc2787') as case:
            # 4.1. Properties
            # 4.1.3. Border > Blur > Maximum value (20)
            # adjustment works correctly with maximum value
            pip_designer_page.input_border_blur_value('20')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_7.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('3a479f14-c8cb-4860-865b-583b4942e7c0') as case:
            # 4.1. Properties
            # 4.1.3. Border > Blur > Minimum value (0)
            # adjustment works correctly with minimum value
            pip_designer_page.input_border_blur_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_8.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('2165fd9a-0b8c-4741-95fd-d7d959c45016') as case:
            # 4.1. Properties
            # 4.1.3. Border > Blur > Adjust by Input
            # show effect directly after adjusting
            case.result = check_result

        with uuid('0b22fbc0-c67d-42a4-9ce2-487d0a991ba1') as case:
            # 4.1. Properties
            # 4.1.3. Border > Blur > Adjust by Slider
            # show effect directly after adjusting
            pip_designer_page.drag_border_blur_slider('10')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_9.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_9.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('9adc2d11-4ecb-4f5a-a45d-d7a4d649f9d9') as case:
            # 4.1. Properties
            # 4.1.3. Border > Blur > Adjust by ^/v button
            # show effect directly after adjusting
            for number_of_clicks in range(5):
                pip_designer_page.click_border_blur_arrow_btn(0)
            for number_of_clicks in range(5):
                pip_designer_page.click_border_blur_arrow_btn(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_10.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_10.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('1bea8d71-72cb-4f20-b2ad-43729f3c0ddf') as case:
            # 4.1. Properties
            # 4.1.3. Border > Opacity > Default value (100%)
            # adjustment works correctly with default value
            check_result = pip_designer_page.exist(L.pip_designer.border.opacity_value).AXValue

            if not check_result == '100%':
                case.result = False
            else:
                case.result = True

        with uuid('4acaf5a7-2015-4372-ade6-2976a6e0b8a0') as case:
            # 4.1. Properties
            # 4.1.3. Border > Opacity > Minimum value (0)
            # adjustment works correctly with minimum value
            pip_designer_page.input_border_opacity_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_11.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_11.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('63ba465a-0adb-4830-9904-465ff74d7237') as case:
            # 4.1. Properties
            # 4.1.3. Border > Opacity > Maximum value (100%)
            # adjustment works correctly with maximum value
            pip_designer_page.input_border_opacity_value('100')

            display_value = pip_designer_page.exist(L.pip_designer.border.opacity_value).AXValue
            if not display_value == '100%':
                check_result_1 = False
            else:
                check_result_1 = True

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_12.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_12.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('6e55b083-34a2-4e01-a4b7-5fcbd33c7e9b') as case:
            # 4.1. Properties
            # 4.1.3. Border > Opacity > Adjust by Input
            # show effect directly after adjusting
            case.result = check_result

        with uuid('62a4c52a-9439-4f79-a7c5-294a9c7efb06') as case:
            # 4.1. Properties
            # 4.1.3. Border > Opacity > Adjust by Slider
            # show effect directly after adjusting
            pip_designer_page.drag_border_opacity_slider('90')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_13.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_13.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('53d0a011-16ab-4a46-8016-54035b98a4c4') as case:
            # 4.1. Properties
            # 4.1.3. Border > Opacity > Adjust by ^/v button
            # show effect directly after adjusting
            for number_of_clicks in range(5):
                pip_designer_page.click_border_opacity_arrow_btn(1)
            for number_of_clicks in range(15):
                pip_designer_page.click_border_opacity_arrow_btn(0)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_14.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_14.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('1b864f5f-a563-415d-b0db-54da102bdfb6') as case:
            # 4.1. Properties
            # 4.1.3. Border > Fill Type > Default (1 Color)
            # show different color form after selecting
            pip_designer_page.apply_border_uniform_color('255', '0', '0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_15.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_15.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('43179ac0-2b10-4163-8fcb-ae33b3141dde') as case:
            # 4.1. Properties
            # 4.1.3. Border > Fill Type > 2 Color Gradient
            # show different color form after selecting
            pip_designer_page.apply_border_2_color('0', '255', '0', '0', '0', '255')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_16.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_16.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('08ece8f8-c0cf-46a2-8a46-c2777c1c6357') as case:
            # 4.1. Properties
            # 4.1.3. Border > Fill Type > 4 Color Gradient
            # show different color form after selecting
            pip_designer_page.apply_border_4_color(
                '0', '255', '0', '0', '0', '255', '255', '0', '0', '255', '255', '255')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_3_17.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_3_17.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('fc8f1b02-fbd9-4505-a6f7-5865ab736c95') as case:
            # 4.1. Properties
            # 4.1.3. Border > Uniform Color > Basic colors
            # show color effect on viewer directly after setting
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_2(self):
        with uuid('6e4ff8a2-1443-436e-8473-98baf85bf003') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Enable / Disable
            # enable / disable related settings correctly
            main_page.enter_room(4)
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.switch_mode('Advanced')
            pip_designer_page.apply_border(1)
            pip_designer_page.drag_border_size_slider('8')
            pip_designer_page.apply_shadow(1)

            btn_status = pip_designer_page.exist(L.pip_designer.shadow.distance_slider).AXEnabled

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            check_result_1 = btn_status and check_result

            pip_designer_page.apply_shadow(0)

            btn_status = not pip_designer_page.exist(L.pip_designer.shadow.distance_slider).AXEnabled

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)
            check_result_2 = btn_status and check_result

            case.result = check_result_1 and check_result_2

            pip_designer_page.apply_shadow(1)

        with uuid('a1f5feba-0c98-4785-8505-9fb00340b569') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Apply shadow to > Border only
            # setting apply on object in preview
            pip_designer_page.apply_shadow_to(2)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('e727a457-a8cb-463b-a4f2-6a8773220656') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Apply shadow to > Object only
            # setting apply on object in preview
            pip_designer_page.apply_shadow_to(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('00d0cf24-f014-4a3f-a227-e379e1a0379d') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Apply shadow to > Object and Border
            # setting apply on object in preview
            pip_designer_page.apply_shadow_to(0)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_5.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('b951af0b-222c-4b3a-96c8-2d266194c903') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Distance > Default value (3)
            # adjustment works correctly with default value
            check_result = pip_designer_page.exist(L.pip_designer.shadow.distance_value).AXValue

            if not check_result == '3.0':
                case.result = False
            else:
                case.result = True

        with uuid('cdc3e4a8-fe5a-446d-b52c-242bc5beec2a') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Distance > Minimum value (0)
            # adjustment works correctly with minimum value
            pip_designer_page.input_shadow_distance_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_6.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('074bd010-3b6b-4c48-90c7-587725973a32') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Distance > Maximum value (100)
            # adjustment works correctly with maximum value
            pip_designer_page.input_shadow_distance_value('100')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_7.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('fbbe8bbf-00a8-48d5-912f-a326f33fd77a') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Distance > Adjust by Input
            # show effect directly after adjusting
            case.result = check_result

        with uuid('0bd28f85-744c-4844-a33b-74eadae821e3') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Distance > Adjust by Slider
            # show effect directly after adjusting
            pip_designer_page.drag_shadow_distance_slider('10')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_8.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('61fb1eee-2514-4600-8065-d66f6a9029ba') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Distance > Adjust by ^/v button
            # show effect directly after adjusting
            for number_of_clicks in range(20):
                pip_designer_page.click_shadow_distance_arrow_btn(0)
            for number_of_clicks in range(10):
                pip_designer_page.click_shadow_distance_arrow_btn(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_9.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_9.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('5b271e0b-514d-47c4-89b3-e3659c218181') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Blur > Default value (0)
            # adjustment works correctly with default value
            check_result = pip_designer_page.exist(L.pip_designer.shadow.blur_value).AXValue

            if not check_result == '0':
                case.result = False
            else:
                case.result = True

        with uuid('847989fd-5164-45dd-ae69-515dd1b39e39') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Blur > Maximum value (20)
            # adjustment works correctly with maximum value
            pip_designer_page.input_shadow_blur_value('20')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_10.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_10.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('d1887d5f-256f-4c65-b61b-364491b044dd') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Blur > Minimum value (0)
            # adjustment works correctly with minimum value
            pip_designer_page.input_shadow_blur_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_11.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_11.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('fdd5fcf6-9fc6-4fa1-abaa-832ab8880467') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Blur > Adjust by Input
            # show effect directly after adjusting
            case.result = check_result

        with uuid('4356256b-39a9-4125-af14-eeaecb36d9ac') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Blur > Adjust by Slider
            # show effect directly after adjusting
            pip_designer_page.drag_shadow_blur_slider('10')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_12.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_12.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('c199a512-77ef-4ff7-b2f8-d7d10c217974') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Blur > Adjust by ^/v button
            # show effect directly after adjusting
            for number_of_clicks in range(5):
                pip_designer_page.click_shadow_blur_arrow_btn(0)
            for number_of_clicks in range(5):
                pip_designer_page.click_shadow_blur_arrow_btn(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_13.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_13.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('fefd3a41-7468-47af-8f4e-acd564127548') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Opacity > Default value (100%)
            # adjustment works correctly with default value
            check_result = pip_designer_page.exist(L.pip_designer.shadow.opacity_value).AXValue

            if not check_result == '100%':
                case.result = False
            else:
                case.result = True

        with uuid('d2f9d6c6-bac2-4d33-9def-c00f9887f66a') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Opacity > Minimum value (0%)
            # adjustment works correctly with minimum value
            pip_designer_page.input_shadow_opacity_value('0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_14.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_14.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('18fd7618-a3fd-41cc-b89c-cc0c9e375d14') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Opacity > Adjust by Input
            # show effect directly after adjusting
            case.result = check_result

        with uuid('0e263e58-3209-403c-89f8-c8b02486754c') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Opacity > Maximum value (100%)
            # adjustment works correctly with maximum value
            pip_designer_page.input_shadow_opacity_value('100')

            display_value = pip_designer_page.exist(L.pip_designer.shadow.opacity_value).AXValue
            if not display_value == '100%':
                check_result_1 = False
            else:
                check_result_1 = True

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_15.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_15.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('07027826-f234-4555-b49a-0d1aeebd33a4') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Opacity > Adjust by Slider
            # show effect directly after adjusting
            pip_designer_page.drag_shadow_opacity_slider('90')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_16.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_16.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('5cc54e27-86fe-4f4a-8f40-820df29efff3') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Opacity > Adjust by ^/v button
            # show effect directly after adjusting
            for number_of_clicks in range(5):
                pip_designer_page.click_shadow_opacity_arrow_btn(1)
            for number_of_clicks in range(15):
                pip_designer_page.click_shadow_opacity_arrow_btn(0)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_17.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_17.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('f74d08c1-5f62-40f2-9586-56c8d8897afe') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Select color > Basic colors
            # show selected color directly after adjusting
            pip_designer_page.select_shadow_color('255', '0', '0')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_18.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_18.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('1fdc33f3-98eb-4bc1-a12a-1ef3d810f04d') as case:
            # 4.1. Properties
            # 4.1.4. Shadow > Shadow direction
            # show correct direction directly after adjusting
            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_4_19.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_4_19.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('e4fdc017-9bd4-47d3-a735-18bb15053e7a') as case:
            # 4.1. Properties
            # 4.1.6. Flip > Enable / Disable
            # enable / disable related settings correctly
            pip_designer_page.apply_flip(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_6_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_6_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview)

            pip_designer_page.apply_flip(0)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_6_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_6_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

            pip_designer_page.apply_flip(1)

        with uuid('68d95d96-4566-493c-9194-98c3a824badf') as case:
            # 4.1. Properties
            # 4.1.6. Flip > Upside down
            # show correct flip setting
            pip_designer_page.apply_flip_type(0)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_6_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_6_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('bfbbb4ee-fe1a-41f9-bb16-53dae0a33df1') as case:
            # 4.1. Properties
            # 4.1.6. Flip > Left and right
            # show correct flip setting
            pip_designer_page.apply_flip_type(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_6_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_6_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('16680bc9-1ea4-4d2d-a515-2ef7aab7435e') as case:
            # 4.1. Properties
            # 4.1.8. Fade > Enable / Disable
            # enable / disable related settings correctly
            check_result_1 = pip_designer_page.apply_fades(1)
            check_result_2 = pip_designer_page.apply_fades(0)

            case.result = check_result_1 and check_result_2

            pip_designer_page.apply_fades(1)

        with uuid('6d9a7cf6-8411-4df0-805e-dd1314f673f0') as case:
            # 4.1. Properties
            # 4.1.8. Fade > Enable fade-in
            # object show fade-in while previewing
            pip_designer_page.apply_enable_fade_in(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_8_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_8_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('4ebec7f4-122a-454e-a97d-ba83a3b25693') as case:
            # 4.1. Properties
            # 4.1.8. Fade > Enable fade-out
            # object show fade-out while previewing
            pip_designer_page.apply_enable_fade_out(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_4_1_8_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_4_1_8_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_3(self):
        with uuid('f606dbfd-76d5-4545-8ebc-a14b78653e4c') as case:
            # 5.1. Assist Function
            # 5.1.5. Zoom out
            # control viewer to zoom out correctly
            main_page.enter_room(4)
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.switch_mode('Advanced')
            pip_designer_page.click_zoom_out_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_1_5_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_1_5_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('bac56171-251c-4cf3-9399-c1001f5a2113') as case:
            # 5.1. Assist Function
            # 5.1.6. Zoom in
            # control viewer to zoom in correctly
            pip_designer_page.click_zoom_in_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_1_6_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_1_6_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('bd4112cb-acce-42bb-a122-e83a4227fe74') as case:
            # 5.1. Assist Function
            # 5.1.7. Viewer % > 10%
            # Viewer should adjust as setting directly
            pip_designer_page.click_viewer_zoom_dropdown_menu('10%')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_1_7_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_1_7_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('3afe55b6-5b2a-421d-9b8e-8e8913a07917') as case:
            # 5.1. Assist Function
            # 5.1.7. Viewer % > 25%
            # Viewer should adjust as setting directly
            pip_designer_page.click_viewer_zoom_dropdown_menu('25%')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_1_7_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_1_7_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('a69a41e6-3ea3-4f48-bdd1-09748bce6d99') as case:
            # 5.1. Assist Function
            # 5.1.7. Viewer % > 50%
            # Viewer should adjust as setting directly
            pip_designer_page.click_viewer_zoom_dropdown_menu('50%')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_1_7_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_1_7_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('3a84a031-80a3-40d7-b3a2-1f0b22d46857') as case:
            # 5.1. Assist Function
            # 5.1.7. Viewer % > 75%
            # Viewer should adjust as setting directly
            pip_designer_page.click_viewer_zoom_dropdown_menu('75%')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_1_7_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_1_7_5.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('6137a4a6-936f-40b1-83cf-ee300219e426') as case:
            # 5.1. Assist Function
            # 5.1.7. Viewer % > 100%
            # Viewer should adjust as setting directly
            pip_designer_page.click_viewer_zoom_dropdown_menu('100%')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_1_7_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_1_7_6.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('d74d9d5a-b79c-4c85-8a27-575963b36d8e') as case:
            # 5.1. Assist Function
            # 5.1.7. Viewer % > 200%
            # Viewer should adjust as setting directly
            pip_designer_page.click_viewer_zoom_dropdown_menu('200%')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_1_7_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_1_7_7.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('a7f2b3f6-1571-42e3-9403-119e43ec9791') as case:
            # 5.1. Assist Function
            # 5.1.7. Viewer % > 300%
            # Viewer should adjust as setting directly
            pip_designer_page.click_viewer_zoom_dropdown_menu('300%')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_1_7_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_1_7_8.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('4d19362c-db24-4047-9f57-b9be40adf093') as case:
            # 5.1. Assist Function
            # 5.1.7. Viewer % > 400%
            # Viewer should adjust as setting directly
            pip_designer_page.click_viewer_zoom_dropdown_menu('400%')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_1_7_9.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_1_7_9.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('c3dab7a9-fa1f-4635-b022-c60fb02be924') as case:
            # 5.1. Assist Function
            # 5.1.7. Viewer % > Fit
            # Viewer should adjust as setting directly
            pip_designer_page.click_viewer_zoom_dropdown_menu('Fit')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_1_7_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_1_7_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('ce1a5762-d582-4f1c-b74f-8dd3bf3f32d0') as case:
            # 5.2. Object adjustment on viewer
            # 5.2.1. Size
            # drag the point at corner/border to adjust object size correctly
            # AT limitation
            case.result = None
            case.fail_log = "*AT limitation*"

        with uuid('76cd60a6-55e2-48f7-9e84-219d9ebd0e90') as case:
            # 5.2. Object adjustment on viewer
            # 5.2.2. Position
            # drag and drop the object to any position on viewer correctly
            # AT limitation
            case.result = None
            case.fail_log = "*AT limitation*"

        with uuid('7d56a6a7-d726-4620-845a-3e5ecdc79758') as case:
            # 5.2. Object adjustment on viewer
            # 5.2.3. Rotation
            # drag the green point to rotate object correctly
            # AT limitation
            case.result = None
            case.fail_log = "*AT limitation*"

        with uuid('ab27e2eb-64cd-4a53-8eff-7c103e802621') as case:
            # 5.3. Playback control
            # 5.3.1. Play / Pause
            # preview control correctly
            pip_designer_page.exist_click(L.pip_designer.object_setting.object_setting)
            pip_designer_page.set_timecode('00_00_00_00')
            pip_designer_page.add_remove_scale_current_keyframe()
            pip_designer_page.input_scale_height_value('0.432')
            pip_designer_page.set_timecode('00_00_10_00')
            pip_designer_page.add_remove_scale_current_keyframe()
            pip_designer_page.input_scale_height_value('1.000')
            pip_designer_page.click_preview_operation('Stop')
            pip_designer_page.set_timecode('00_00_00_00')
            pip_designer_page.add_remove_position_current_keyframe()
            pip_designer_page.input_x_position_value('0.270')
            pip_designer_page.input_y_position_value('0.783')
            pip_designer_page.set_timecode('00_00_10_00')
            pip_designer_page.add_remove_position_current_keyframe()
            pip_designer_page.input_x_position_value('0.500')
            pip_designer_page.input_y_position_value('0.500')

            pip_designer_page.click_preview_operation('Stop')
            pip_designer_page.click_preview_operation('Play')
            time.sleep(DELAY_TIME * 2)

            pause_button_status = pip_designer_page.exist(L.pip_designer.preview_pause).AXEnabled

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_3_1_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_3_1_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview) and pause_button_status

            time.sleep(DELAY_TIME * 2)
            pip_designer_page.click_preview_operation('Pause')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_3_1_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_3_1_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('73121849-f8cb-4842-bd9d-40dbfdd7eeb2') as case:
            # 5.3. Playback control
            # 5.3.3. Go to previous frame
            # preview control correctly
            for number_of_clicks in range(10):
                pip_designer_page.click_preview_operation('Previous_Frame')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_3_3_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_3_3_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('6c6011e0-f04a-4776-b04e-cb0e45b04668') as case:
            # 5.3. Playback control
            # 5.3.4. Go to next frame
            # preview control correctly
            for number_of_clicks in range(10):
                pip_designer_page.click_preview_operation('Next_Frame')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_3_4_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_3_4_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('13f2b5cc-e73e-4e0c-b687-3baf2c172a9e') as case:
            # 5.3. Playback control
            # 5.3.5. Fast Forward
            # preview control correctly
            pip_designer_page.click_preview_operation('Fast_Forward')
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_3_5_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_3_5_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('fbfe4a51-f6be-4f8c-b222-063ff3a4146e') as case:
            # 5.3. Playback control
            # 5.3.2. Stop
            # preview control correctly
            pip_designer_page.click_preview_operation('Stop')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_3_2_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_3_2_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('d6ad4244-acc0-463e-ab51-12dc92056ed5') as case:
            # 5.3. Playback control
            # 5.3.6. Timecode > Input
            # slider will locate at input timecode directly
            pip_designer_page.set_timecode('00_00_05_00')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_3_6_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_3_6_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('7c9c8295-f73a-4a8f-872c-8150cba26196') as case:
            # 5.3. Playback control
            # 5.3.6. Timecode > Display
            # show current timecode correctly
            check_result = pip_designer_page.get_timecode()
            if not check_result == '00;00;05;00':
                case.result = False
            else:
                case.result = True

        with uuid('b50295a0-6efc-40d9-8249-b4d683145a92') as case:
            # 5.4. Toggle TV safe zone / grid lines on/off
            # 5.4.3. Grid Lines > None
            # no grid lines on viewer
            pip_designer_page.apply_grid_lines_format('1')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_4_3_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_4_3_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('acac8825-249f-402d-a53c-9b749a9de7ed') as case:
            # 5.4. Toggle TV safe zone / grid lines on/off
            # 5.4.3. Grid Lines > 2x2
            # show correct grid lines on viewer
            pip_designer_page.apply_grid_lines_format('2')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_4_3_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_4_3_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('6b7b94c5-f405-44b5-916d-b51e29142ca2') as case:
            # 5.4. Toggle TV safe zone / grid lines on/off
            # 5.4.3. Grid Lines > 3x3
            # show correct grid lines on viewer
            pip_designer_page.apply_grid_lines_format('3')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_4_3_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_4_3_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('fa51be62-f36f-4149-999e-8815b217a747') as case:
            # 5.4. Toggle TV safe zone / grid lines on/off
            # 5.4.3. Grid Lines > 4x4
            # show correct grid lines on viewer
            pip_designer_page.apply_grid_lines_format('4')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_4_3_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_4_3_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('4a946791-94e2-47b6-bcbf-2a5c6cac33e6') as case:
            # 5.4. Toggle TV safe zone / grid lines on/off
            # 5.4.3. Grid Lines > 5x5
            # show correct grid lines on viewer
            pip_designer_page.apply_grid_lines_format('5')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_4_3_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_4_3_5.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('111b22b3-19a4-4344-9f8c-485eb652176b') as case:
            # 5.4. Toggle TV safe zone / grid lines on/off
            # 5.4.3. Grid Lines > 6x6
            # show correct grid lines on viewer
            pip_designer_page.apply_grid_lines_format('6')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_4_3_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_4_3_6.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('f560d666-954b-4b1d-9acd-e7e64b9b4392') as case:
            # 5.4. Toggle TV safe zone / grid lines on/off
            # 5.4.3. Grid Lines > 7x7
            # show correct grid lines on viewer
            pip_designer_page.apply_grid_lines_format('7')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_4_3_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_4_3_7.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('0d5a3bbf-e920-492f-83a9-d32e5cdf1c6b') as case:
            # 5.4. Toggle TV safe zone / grid lines on/off
            # 5.4.3. Grid Lines > 8x8
            # show correct grid lines on viewer
            pip_designer_page.apply_grid_lines_format('8')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_4_3_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_4_3_8.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('68b1d1c8-dfcb-4997-83e3-d10ae0132a2c') as case:
            # 5.4. Toggle TV safe zone / grid lines on/off
            # 5.4.3. Grid Lines > 9x9
            # show correct grid lines on viewer
            pip_designer_page.apply_grid_lines_format('9')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_4_3_9.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_4_3_9.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('e8f2cf5a-7b3d-4a44-9d44-e3549b4ff0bd') as case:
            # 5.4. Toggle TV safe zone / grid lines on/off
            # 5.4.3. Grid Lines > 10x10
            # show correct grid lines on viewer
            pip_designer_page.apply_grid_lines_format('10')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_4_3_10.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_4_3_10.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('8bb22c68-1018-49e3-9e0d-789762e924e1') as case:
            # 5.4. Toggle TV safe zone / grid lines on/off
            # 5.4.1. Snap to Reference Lines > UnSelect
            # object won't snap to reference lines
            pip_designer_page.apply_snap_to_reference_lines(0)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_4_1_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_4_1_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('f5f17973-853f-4426-883e-9e7532b6b234') as case:
            # 5.4. Toggle TV safe zone / grid lines on/off
            # 5.4.1. Snap to Reference Lines > Select
            # object will snap to reference lines if there are grid lines
            pip_designer_page.apply_snap_to_reference_lines(1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_4_1_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_4_1_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('94e4bcd2-111d-4398-b06b-dc728c2232f0') as case:
            # 5. Viewer
            # 5.1. Assist Function
            # 5.1.1. Undo button
            # show previous editing status
            pip_designer_page.tap_undo_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_1_1_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_1_1_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('1129a61d-1976-4853-a73a-8904a35f90d0') as case:
            # 5.1. Assist Function
            # 5.1.2. Redo button
            # show next editing status
            pip_designer_page.tap_redo_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_5_1_2_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_5_1_2_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_4(self):
        with uuid('4394edbe-8def-4ed4-a45e-e670bf4c8d93') as case:
            # 6.1. Timecode
            # 6.1.1. Mode > Movie Timecode
            # switch to movie timecode correctly
            main_page.insert_media('Food.jpg')
            main_page.select_library_icon_view_media("Landscape 01.jpg")
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Food.jpg')
            tips_area_page.tools.select_PiP_Designer()
            pip_designer_page.switch_mode('Advanced')

            pip_designer_page.switch_timecode_mode(1)

            check_result = pip_designer_page.get_timecode()
            if not check_result == '00;00;05;00':
                check_result_1 = False
            else:
                check_result_1 = True

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_1_1_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_1_1_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('f684fb55-ccb4-4eb1-8acf-243718f6c9e4') as case:
            # 6. Timeline
            # 6.1. Timecode
            # 6.1.1. Mode > Clip Timecode
            # switch to clip timecode correctly
            pip_designer_page.switch_timecode_mode(0)

            check_result = pip_designer_page.get_timecode()
            if not check_result == '00;00;00;00':
                check_result_1 = False
            else:
                check_result_1 = True

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_1_1_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_1_1_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('d16a06ff-5cf7-481f-88d9-14626b65a3a6') as case:
            # 6.1. Timecode
            # 6.1.2. Zoon in / Zoom out > Click +/- button
            # zoom in /zoom out correctly
            pip_designer_page.click_timeline_zoom_in_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_1_2_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_1_2_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview)

            pip_designer_page.click_timeline_zoom_out_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_1_2_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_1_2_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('00746a53-6e19-4122-929a-2705a21edfd1') as case:
            # 6.1. Timecode
            # 6.1.2. Zoon in / Zoom out > Drag on timeline to Left / Right
            # zoom in /zoom out correctly
            # AT limitation
            # pip_designer_page.click(L.pip_designer.timeline_scrollarea)
            # position_1 = pip_designer_page.get_mouse_pos()
            # pip_designer_page.drag_mouse((position_1[0]+15, position_1[1]), (position_1[0]+50, position_1[1]))
            case.result = None
            case.fail_log = "*AT limitation*"

        with uuid('6e03dd79-9401-4b70-871e-ffec231c7fe5') as case:
            # 6.1. Timecode
            # 6.1.3. Display / Hide timeline mode
            # function works correctly
            pip_designer_page.hide_timeline_mode()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_1_3_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_1_3_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview)

            pip_designer_page.display_timeline_mode()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_1_3_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_1_3_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('d4215bcd-ed74-431b-91f1-d50de8ce4ab9') as case:
            # 6.2. Keyframe
            # 6.2.1. Position > Button control > Add keyframe (*)
            # add keyframe on timeline via *
            pip_designer_page.set_timecode('00_00_00_00')
            pip_designer_page.add_remove_position_track_current_keyframe()
            pip_designer_page.input_x_position_value('0.000')
            pip_designer_page.input_y_position_value('0.000')
            pip_designer_page.set_timecode('00_00_01_00')
            pip_designer_page.add_remove_position_track_current_keyframe()
            pip_designer_page.input_x_position_value('0.100')
            pip_designer_page.input_y_position_value('0.100')
            pip_designer_page.set_timecode('00_00_02_00')
            pip_designer_page.add_remove_position_track_current_keyframe()
            pip_designer_page.input_x_position_value('0.200')
            pip_designer_page.input_y_position_value('0.200')
            pip_designer_page.set_timecode('00_00_03_00')
            pip_designer_page.add_remove_position_track_current_keyframe()
            pip_designer_page.input_x_position_value('0.300')
            pip_designer_page.input_y_position_value('0.300')
            pip_designer_page.set_timecode('00_00_04_00')
            pip_designer_page.add_remove_position_track_current_keyframe()
            pip_designer_page.input_x_position_value('0.400')
            pip_designer_page.input_y_position_value('0.400')
            pip_designer_page.set_timecode('00_00_05_00')
            pip_designer_page.add_remove_position_track_current_keyframe()
            pip_designer_page.input_x_position_value('0.500')
            pip_designer_page.input_y_position_value('0.500')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_1_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_1_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            pip_designer_page.click_preview_operation('Stop')
            pip_designer_page.click_preview_operation('Play')

        with uuid('28f0cff0-6545-4515-9932-b79130116a38') as case:
            # 6.2. Keyframe
            # 6.2.1. Position > Button control > </>
            # switch focus on correct keyframe via </>
            # waiting for btn_next_keyframe enable
            item = pip_designer_page.exist(L.pip_designer.simple_position_track.next_keyframe)
            # wait item [status: ready]
            for x in range(15):
                if item.AXEnabled:
                    logger('break')
                    break
                if x == 14:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)

            pip_designer_page.tap_position_track_next_keyframe()
            pip_designer_page.tap_position_track_next_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_1_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_1_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview)

            pip_designer_page.tap_position_track_previous_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_1_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_1_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('65bd4014-a6e9-4f3a-9f3e-459719c2838b') as case:
            # 6.2. Keyframe
            # 6.2.1. Position > Button control > Remove keyframe (*)
            # remove selected keyframe via *
            pip_designer_page.add_remove_position_track_current_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_1_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_1_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            pip_designer_page.add_remove_position_track_current_keyframe()

        with uuid('2d0ba1c9-75b0-4649-8805-f76823d58bd0') as case:
            # 6.2. Keyframe
            # 6.2.1. Position > Right-click menu > Ease In
            # ease in effect works correctly with tick/untick status
            pip_designer_page.right_click_timeline_keyframe_context_menu(1, 5)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_1_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_1_5.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('844d1436-c4f2-49d8-b30a-07c2a9b0121a') as case:
            # 6.2. Keyframe
            # 6.2.1. Position > Right-click menu > Ease Out
            # ease out effect works correctly with tick/untick status
            pip_designer_page.right_click_timeline_keyframe_context_menu(1, 6)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_1_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_1_6.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('2f4981ca-eacf-43d5-89b8-f4024f7ce6f2') as case:
            # 6.2. Keyframe
            # 6.2.1. Position > Right-click menu > Remove keyframe
            # remove selected keyframe
            pip_designer_page.right_click_timeline_keyframe_context_menu(1, 1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_1_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_1_7.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('6f6bd7c1-4578-46bc-aded-ff8faaa81d23') as case:
            # 6.2. Keyframe
            # 6.2.1. Position > Right-click menu > Duplicate previous keyframe
            # same setting as previous keyframe
            pip_designer_page.right_click_timeline_keyframe_context_menu(1, 3)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_1_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_1_8.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('be3332fb-20f3-4920-8c19-846dd63fe11d') as case:
            # 6.2. Keyframe
            # 6.2.1. Position > Right-click menu > Duplicate next keyframe
            # same setting as next keyframe
            pip_designer_page.right_click_timeline_keyframe_context_menu(1, 4)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_1_9.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_1_9.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('26de3b86-6b6d-48d7-84e5-3d316de2241f') as case:
            # 6.2. Keyframe
            # 6.2.1. Position > Right-click menu > Remove all keyframes
            # remove all keyframes
            pip_designer_page.right_click_timeline_keyframe_context_menu(1, 2)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_1_10.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_1_10.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            pip_designer_page.input_x_position_value('0.500')
            pip_designer_page.input_y_position_value('0.500')

        with uuid('e0dd6528-1a4b-4619-adfd-897883354a7c') as case:
            # 6.2. Keyframe
            # 6.2.2. Scale > Button control > Add keyframe (*)
            # add keyframe on timeline via *
            pip_designer_page.set_timecode('00_00_00_00')
            pip_designer_page.add_remove_scale_track_current_keyframe()
            pip_designer_page.input_scale_width_value('0.200')
            pip_designer_page.set_timecode('00_00_01_00')
            pip_designer_page.add_remove_scale_track_current_keyframe()
            pip_designer_page.input_scale_width_value('0.400')
            pip_designer_page.set_timecode('00_00_02_00')
            pip_designer_page.add_remove_scale_track_current_keyframe()
            pip_designer_page.input_scale_width_value('0.600')
            pip_designer_page.set_timecode('00_00_03_00')
            pip_designer_page.add_remove_scale_track_current_keyframe()
            pip_designer_page.input_scale_width_value('0.800')
            pip_designer_page.set_timecode('00_00_04_00')
            pip_designer_page.add_remove_scale_track_current_keyframe()
            pip_designer_page.input_scale_width_value('1.000')
            pip_designer_page.set_timecode('00_00_05_00')
            pip_designer_page.add_remove_scale_track_current_keyframe()
            pip_designer_page.input_scale_width_value('1.200')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_2_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_2_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            pip_designer_page.click_preview_operation('Stop')
            pip_designer_page.click_preview_operation('Play')

        with uuid('a2818fe2-5d66-4305-bfd6-b1c9c11b5b34') as case:
            # 6.2. Keyframe
            # 6.2.2. Scale > Button control > </>
            # switch focus on correct keyframe via </>
            # waiting for btn_next_keyframe enable
            item = pip_designer_page.exist(L.pip_designer.simple_scale_track.next_keyframe)
            # wait item [status: ready]
            for x in range(15):
                if item.AXEnabled:
                    logger('break')
                    break
                if x == 14:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)

            pip_designer_page.tap_scale_track_next_keyframe()
            pip_designer_page.tap_scale_track_next_keyframe()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_2_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_2_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview)

            pip_designer_page.tap_scale_track_previous_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_2_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_2_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('54737152-2060-4c14-8b3c-f1c09aecc8c2') as case:
            # 6.2. Keyframe
            # 6.2.2. Scale > Button control > Remove keyframe (*)
            # remove selected keyframe via *
            pip_designer_page.add_remove_scale_track_current_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_2_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_2_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            pip_designer_page.add_remove_scale_track_current_keyframe()

        with uuid('3b213715-3177-476d-b293-d51ee736b5c2') as case:
            # 6.2. Keyframe
            # 6.2.2. Scale > Right-click menu > Ease In
            # ease in effect works correctly with tick/untick status
            pip_designer_page.right_click_timeline_keyframe_context_menu(2, 5)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_2_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_2_5.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('e095f413-bc25-4d4d-80e3-673cd76fb422') as case:
            # 6.2. Keyframe
            # 6.2.2. Scale > Right-click menu > Ease Out
            # ease out effect works correctly with tick/untick status
            pip_designer_page.right_click_timeline_keyframe_context_menu(2, 6)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_2_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_2_6.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('e1da70af-7686-495a-ab39-695b2136b93a') as case:
            # 6.2. Keyframe
            # 6.2.2. Scale > Right-click menu > Remove keyframe
            # remove selected keyframe
            pip_designer_page.right_click_timeline_keyframe_context_menu(2, 1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_2_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_2_7.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('db5f9265-19aa-4b16-bdf0-586ccddd7ba1') as case:
            # 6.2. Keyframe
            # 6.2.2. Scale > Right-click menu > Duplicate previous keyframe
            # same setting as previous keyframe
            pip_designer_page.right_click_timeline_keyframe_context_menu(2, 3)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_2_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_2_8.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('3323115d-d3b3-4a84-af98-7768b0b6e358') as case:
            # 6.2. Keyframe
            # 6.2.2. Scale > Right-click menu > Duplicate next keyframe
            # same setting as next keyframe
            pip_designer_page.right_click_timeline_keyframe_context_menu(2, 4)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_2_9.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_2_9.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('0004ea8b-4f9d-4679-9485-8eb4f0761166') as case:
            # 6.2. Keyframe
            # 6.2.2. Scale > Right-click menu > Remove all keyframes
            # remove all keyframes
            pip_designer_page.right_click_timeline_keyframe_context_menu(2, 2)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_2_10.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_2_10.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            pip_designer_page.input_scale_width_value('1.000')

        with uuid('3dc8914b-6cfc-4b8f-ac83-bfcd54b568ee') as case:
            # 6.2. Keyframe
            # 6.2.3. Opacity > Button control > Add keyframe (*)
            # add keyframe on timeline via *
            pip_designer_page.drag_properties_scroll_bar(1.0)
            pip_designer_page.set_timecode('00_00_00_00')
            pip_designer_page.add_remove_opacity_track_current_keyframe()
            pip_designer_page.drag_position_opacity_slider(0)
            pip_designer_page.set_timecode('00_00_01_00')
            pip_designer_page.add_remove_opacity_track_current_keyframe()
            pip_designer_page.drag_position_opacity_slider(20)
            pip_designer_page.set_timecode('00_00_02_00')
            pip_designer_page.add_remove_opacity_track_current_keyframe()
            pip_designer_page.drag_position_opacity_slider(40)
            pip_designer_page.set_timecode('00_00_03_00')
            pip_designer_page.add_remove_opacity_track_current_keyframe()
            pip_designer_page.drag_position_opacity_slider(60)
            pip_designer_page.set_timecode('00_00_04_00')
            pip_designer_page.add_remove_opacity_track_current_keyframe()
            pip_designer_page.drag_position_opacity_slider(80)
            pip_designer_page.set_timecode('00_00_05_00')
            pip_designer_page.add_remove_opacity_track_current_keyframe()
            pip_designer_page.drag_position_opacity_slider(100)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_3_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_3_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            pip_designer_page.click_preview_operation('Stop')
            pip_designer_page.click_preview_operation('Play')

        with uuid('8a191781-e4a7-4844-9dd3-b27aafab73eb') as case:
            # 6.2. Keyframe
            # 6.2.3. Opacity > Button control > </>
            # switch focus on correct keyframe via </>
            # waiting for btn_next_keyframe enable
            item = pip_designer_page.exist(L.pip_designer.simple_opacity_track.next_keyframe)
            # wait item [status: ready]
            for x in range(15):
                if item.AXEnabled:
                    logger('break')
                    break
                if x == 14:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)

            pip_designer_page.tap_opacity_track_next_keyframe()
            pip_designer_page.tap_opacity_track_next_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_3_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_3_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview)

            pip_designer_page.tap_opacity_track_previous_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_3_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_3_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('e13d5eaf-d809-471c-9118-ff8613b52ef3') as case:
            # 6.2. Keyframe
            # 6.2.3. Opacity > Button control > Remove keyframe (*)
            # remove selected keyframe via *
            pip_designer_page.add_remove_opacity_track_current_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_3_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_3_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            pip_designer_page.add_remove_opacity_track_current_keyframe()

        with uuid('08814768-716c-4644-a3e5-8ecdf5365b3d') as case:
            # 6.2. Keyframe
            # 6.2.3. Opacity > Right-click menu > Remove keyframe
            # remove selected keyframe
            pip_designer_page.right_click_timeline_keyframe_context_menu(3, 1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_3_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_3_5.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('dbee4df6-91da-470e-9d6e-ff2618466914') as case:
            # 6.2. Keyframe
            # 6.2.3. Opacity > Right-click menu > Duplicate previous keyframe
            # same setting as previous keyframe
            pip_designer_page.right_click_timeline_keyframe_context_menu(3, 3)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_3_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_3_6.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('a25005b3-ffd5-4ab1-b815-a0744785681e') as case:
            # 6.2. Keyframe
            # 6.2.3. Opacity > Right-click menu > Duplicate next keyframe
            # same setting as next keyframe
            pip_designer_page.right_click_timeline_keyframe_context_menu(3, 4)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_3_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_3_7.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('b3f47365-e1ce-452e-b241-20069b7840a6') as case:
            # 6.2. Keyframe
            # 6.2.3. Opacity > Right-click menu > Remove all keyframes
            # remove all keyframes
            pip_designer_page.right_click_timeline_keyframe_context_menu(3, 2)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_3_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_3_8.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            pip_designer_page.drag_position_opacity_slider(100)

        with uuid('2058a0d6-12f7-43bc-9863-81709d0a099f') as case:
            # 6.2. Keyframe
            # 6.2.4. Rotation > Button control > Add keyframe (*)
            # add keyframe on timeline via *
            pip_designer_page.drag_keyframe_scroll_bar(1.0)
            pip_designer_page.set_timecode('00_00_00_00')
            pip_designer_page.add_remove_rotation_track_current_keyframe()
            pip_designer_page.input_rotation_degree_value('0.00')
            pip_designer_page.set_timecode('00_00_01_00')
            pip_designer_page.add_remove_rotation_track_current_keyframe()
            pip_designer_page.input_rotation_degree_value('60.00')
            pip_designer_page.set_timecode('00_00_02_00')
            pip_designer_page.add_remove_rotation_track_current_keyframe()
            pip_designer_page.input_rotation_degree_value('120.00')
            pip_designer_page.set_timecode('00_00_03_00')
            pip_designer_page.add_remove_rotation_track_current_keyframe()
            pip_designer_page.input_rotation_degree_value('180.00')
            pip_designer_page.set_timecode('00_00_04_00')
            pip_designer_page.add_remove_rotation_track_current_keyframe()
            pip_designer_page.input_rotation_degree_value('270.00')
            pip_designer_page.set_timecode('00_00_05_00')
            pip_designer_page.add_remove_rotation_track_current_keyframe()
            pip_designer_page.input_rotation_degree_value('360.00')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_4_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_4_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            pip_designer_page.click_preview_operation('Stop')
            pip_designer_page.click_preview_operation('Play')

        with uuid('08ba4d3d-e4d5-4e77-9336-fa9eff39d009') as case:
            # 6.2. Keyframe
            # 6.2.4. Rotation > Button control > </>
            # switch focus on correct keyframe via </>
            # waiting for btn_next_keyframe enable
            item = pip_designer_page.exist(L.pip_designer.simple_rotation_track.next_keyframe)
            # wait item [status: ready]
            for x in range(15):
                if item.AXEnabled:
                    logger('break')
                    break
                if x == 14:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)

            pip_designer_page.tap_rotation_track_next_keyframe()
            pip_designer_page.tap_rotation_track_next_keyframe()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_4_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_4_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview)

            pip_designer_page.tap_rotation_track_previous_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_4_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_4_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('6e92f269-530d-4be4-a9ad-f3f33b39548a') as case:
            # 6.2. Keyframe
            # 6.2.4. Rotation > Button control > Remove keyframe (*)
            # remove selected keyframe via *
            pip_designer_page.add_remove_rotation_track_current_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_4_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_4_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            pip_designer_page.add_remove_rotation_track_current_keyframe()

        with uuid('1e8eec68-291c-4b0f-925b-3757cc637c30') as case:
            # 6.2. Keyframe
            # 6.2.4. Rotation > Right-click menu > Ease In
            # ease in effect works correctly with tick/untick status
            pip_designer_page.right_click_timeline_keyframe_context_menu(4, 5)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_4_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_4_5.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('af0a00b1-f391-4864-a127-83e02d0834c4') as case:
            # 6.2. Keyframe
            # 6.2.4. Rotation > Right-click menu > Ease Out
            # ease out effect works correctly with tick/untick status
            pip_designer_page.right_click_timeline_keyframe_context_menu(4, 6)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_4_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_4_6.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('ab8ac9d9-f8a6-42ea-bc84-2c85ae7fa68f') as case:
            # 6.2. Keyframe
            # 6.2.4. Rotation > Right-click menu > Remove keyframe
            # remove selected keyframe
            pip_designer_page.right_click_timeline_keyframe_context_menu(4, 1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_4_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_4_7.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('2651a5a1-4b31-42d4-8e3f-56b4c5c72b0c') as case:
            # 6.2. Keyframe
            # 6.2.4. Rotation > Right-click menu > Duplicate previous keyframe
            # same setting as previous keyframe
            pip_designer_page.right_click_timeline_keyframe_context_menu(4, 3)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_4_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_4_8.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('4758eb49-6bc2-47da-b3e4-8ee00000e1d9') as case:
            # 6.2. Keyframe
            # 6.2.4. Rotation > Right-click menu > Duplicate next keyframe
            # same setting as next keyframe
            pip_designer_page.right_click_timeline_keyframe_context_menu(4, 4)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_4_9.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_4_9.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('580875a0-4b89-482c-9d3c-55abff240e7a') as case:
            # 6.2. Keyframe
            # 6.2.4. Rotation > Right-click menu > Remove all keyframes
            # remove all keyframes
            pip_designer_page.right_click_timeline_keyframe_context_menu(4, 2)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_4_10.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_4_10.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            pip_designer_page.input_rotation_degree_value('0.00')

        with uuid('8d7554ca-89c8-4a84-82e4-1c92ca315fc1') as case:
            # 6.2. Keyframe
            # 6.2.5. Freeform > Button control > Add keyframe (*)
            # add keyframe on timeline via *
            pip_designer_page.set_timecode('00_00_00_00')
            pip_designer_page.add_remove_freeform_track_current_keyframe()
            pip_designer_page.set_timecode('00_00_01_00')
            pip_designer_page.add_remove_freeform_track_current_keyframe()
            pip_designer_page.set_timecode('00_00_02_00')
            pip_designer_page.add_remove_freeform_track_current_keyframe()
            pip_designer_page.set_timecode('00_00_03_00')
            pip_designer_page.add_remove_freeform_track_current_keyframe()
            pip_designer_page.set_timecode('00_00_04_00')
            pip_designer_page.add_remove_freeform_track_current_keyframe()
            pip_designer_page.set_timecode('00_00_05_00')
            pip_designer_page.add_remove_freeform_track_current_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_5_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_5_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            pip_designer_page.click_preview_operation('Stop')
            pip_designer_page.click_preview_operation('Play')

        with uuid('12dd5687-8b95-46fd-80de-5cde1e7163ed') as case:
            # 6.2. Keyframe
            # 6.2.5. Freeform > Button control > </>
            # switch focus on correct keyframe via </>
            # waiting for btn_next_keyframe enable
            item = pip_designer_page.exist(L.pip_designer.simple_freeform_track.next_keyframe)
            # wait item [status: ready]
            for x in range(15):
                if item.AXEnabled:
                    logger('break')
                    break
                if x == 14:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)

            pip_designer_page.tap_freeform_track_next_keyframe()
            pip_designer_page.tap_freeform_track_next_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_5_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_5_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_1 = pip_designer_page.compare(ground_truth, current_preview)

            pip_designer_page.tap_freeform_track_previous_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_5_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_5_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result_2 = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('042c6e04-278e-4bd9-a63b-5ed36befe2ac') as case:
            # 6.2. Keyframe
            # 6.2.5. Freeform > Button control > Remove keyframe (*)
            # remove selected keyframe via *
            pip_designer_page.add_remove_freeform_track_current_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_5_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_5_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

            pip_designer_page.add_remove_freeform_track_current_keyframe()

        with uuid('2979e833-6698-42a5-a9ea-1b57ea1a72bb') as case:
            # 6.2. Keyframe
            # 6.2.5. Freeform > Right-click menu > Remove keyframe
            # remove selected keyframe
            pip_designer_page.right_click_timeline_keyframe_context_menu(5, 1)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_5_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_5_5.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('063dbafe-f6e1-46b4-81f5-da42121a910a') as case:
            # 6.2. Keyframe
            # 6.2.5. Freeform > Right-click menu > Duplicate previous keyframe
            # same setting as previous keyframe
            pip_designer_page.right_click_timeline_keyframe_context_menu(5, 3)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_5_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_5_6.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('386c796c-bca0-47ee-9acd-7667f6f229bd') as case:
            # 6.2. Keyframe
            # 6.2.5. Freeform > Right-click menu > Duplicate next keyframe
            # same setting as next keyframe
            pip_designer_page.right_click_timeline_keyframe_context_menu(5, 4)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_5_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_5_7.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('82cee43f-8cd7-4d1b-82f0-ffff08961474') as case:
            # 6.2. Keyframe
            # 6.2.5. Freeform > Right-click menu > Remove all keyframes
            # remove all keyframes
            pip_designer_page.right_click_timeline_keyframe_context_menu(5, 2)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_6_2_5_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_6_2_5_8.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_5(self):
        with uuid('cc5ecc11-9329-4026-b72f-322b1ce28bfd') as case:
            # 7. Result
            # 7.1. Editing confirmation
            # 7.1.1. OK > New template
            # pop up "save as template" to processed the saving precess
            main_page.enter_room(4)
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.switch_mode('Advanced')

            # Position
            pip_designer_page.set_timecode('00_00_00_00')
            pip_designer_page.add_remove_position_track_current_keyframe()
            pip_designer_page.input_x_position_value('0.000')
            pip_designer_page.input_y_position_value('0.000')
            pip_designer_page.set_timecode('00_00_05_00')
            pip_designer_page.add_remove_position_track_current_keyframe()
            pip_designer_page.input_x_position_value('0.500')
            pip_designer_page.input_y_position_value('0.500')

            pip_designer_page.click_preview_operation('Stop')

            # Scale
            pip_designer_page.set_timecode('00_00_00_00')
            pip_designer_page.add_remove_scale_track_current_keyframe()
            pip_designer_page.input_scale_width_value('0.200')
            pip_designer_page.set_timecode('00_00_05_00')
            pip_designer_page.add_remove_scale_track_current_keyframe()
            pip_designer_page.input_scale_width_value('1.200')

            pip_designer_page.click_preview_operation('Stop')

            # Opacity
            pip_designer_page.drag_properties_scroll_bar(1.0)
            pip_designer_page.set_timecode('00_00_00_00')
            pip_designer_page.add_remove_opacity_track_current_keyframe()
            pip_designer_page.drag_position_opacity_slider(0)
            pip_designer_page.set_timecode('00_00_05_00')
            pip_designer_page.add_remove_opacity_track_current_keyframe()
            pip_designer_page.drag_position_opacity_slider(100)

            pip_designer_page.click_preview_operation('Stop')

            # Rotation
            pip_designer_page.drag_keyframe_scroll_bar(1.0)
            pip_designer_page.set_timecode('00_00_00_00')
            pip_designer_page.add_remove_rotation_track_current_keyframe()
            pip_designer_page.input_rotation_degree_value('0.00')
            pip_designer_page.set_timecode('00_00_05_00')
            pip_designer_page.add_remove_rotation_track_current_keyframe()
            pip_designer_page.input_rotation_degree_value('360.00')

            pip_designer_page.click_preview_operation('Stop')
            pip_designer_page.click_preview_operation('Play')

            # waiting for btn enable
            item = pip_designer_page.exist(L.pip_designer.timecode)
            # wait item [status: ready]
            for x in range(15):
                if item.AXEnabled:
                    logger('break')
                    break
                if x == 14:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)

            pip_designer_page.click_ok()
            pip_designer_page.input_template_name_and_click_ok('01_newpip')

            check_result_1 = pip_room_page.check_is_in_Custom_category('01_newpip')

            check_result = pip_designer_page.exist(L.pip_designer.designer_window)
            if not check_result:
                check_result_2 = True
            else:
                check_result_2 = False
            case.result = check_result_1 and check_result_2

        with uuid('32f99b5f-a2d1-44c7-847f-64bc80178ca0') as case:
            # 7.1. Editing confirmation
            # 7.1.4. Cancel > No editing
            # leave module directly
            pip_room_page.click_ModifyAttribute_btn('PiP')
            pip_designer_page.switch_mode('Express')
            pip_designer_page.express_mode.unfold_properties_object_setting_tab()
            pip_designer_page.click_cancel()

            check_result_1 = pip_designer_page.exist(L.pip_designer.designer_window)
            if not check_result_1:
                check_result = True
            else:
                check_result = False
            case.result = check_result

        with uuid('18a3fc13-34f5-4c5a-a075-41d6c156caac') as case:
            # 7.1. Editing confirmation
            # 7.1.4. Cancel > Have editing > Confirmation = Yes
            # editing result is saved then return to timeline directly
            pip_room_page.click_ModifyAttribute_btn('PiP')
            pip_designer_page.switch_mode('Express')
            pip_designer_page.express_mode.unfold_properties_object_setting_tab()

            pip_designer_page.drag_position_opacity_slider(100)

            pip_designer_page.click_cancel()
            pip_designer_page.click_cancel_yes()

            pip_room_page.click_ModifyAttribute_btn('PiP')
            pip_designer_page.switch_mode('Express')
            pip_designer_page.express_mode.unfold_properties_object_setting_tab()

            check_result = pip_designer_page.express_mode.get_object_setting_opacity_value()
            if not check_result == '100%':
                case.result = False
            else:
                case.result = True

        with uuid('b8412270-6622-4885-87ca-f9e63145dd52') as case:
            # 7.1. Editing confirmation
            # 7.1.4. Cancel > Have editing > Confirmation = No
            # editing result isn't saved then return to timeline directly
            pip_designer_page.input_position_opacity_value('80')

            pip_designer_page.click_cancel()
            pip_designer_page.click_cancel_no()

            pip_room_page.click_ModifyAttribute_btn('PiP')
            pip_designer_page.switch_mode('Express')
            pip_designer_page.express_mode.unfold_properties_object_setting_tab()

            check_result = pip_designer_page.express_mode.get_object_setting_opacity_value()
            if not check_result == '100%':
                case.result = False
            else:
                case.result = True

            pip_designer_page.click_cancel()

        with uuid('b8346fd8-29b7-464d-8dd6-dccf0ada003f') as case:
            # 7.1. Editing confirmation
            # 7.1.4. Cancel > Have editing > Confirmation = Cancel
            # saving dialog close and stay in motion tracker
            pip_room_page.click_ModifyAttribute_btn('PiP')
            pip_designer_page.switch_mode('Express')
            pip_designer_page.express_mode.unfold_properties_object_setting_tab()
            pip_designer_page.input_position_opacity_value('80')

            pip_designer_page.click_cancel()
            pip_designer_page.click_cancel_cancel()

            check_result = pip_designer_page.exist(L.pip_designer.designer_window)
            if not check_result:
                case.result = False
            else:
                case.result = True

        with uuid('6f400ac2-1e3d-4fbb-80d8-684bf87ea27d') as case:
            # 7.1. Editing confirmation
            # 7.1.2. Save As... > Result > Cancel
            # pop up "save as template" and don't save
            pip_designer_page.save_as_name('01_modifyPiP')
            pip_designer_page.exist_click(L.pip_designer.save_as_cancel_btn)

            check_result = pip_designer_page.get_title()
            if not check_result == '01_modifyPiP':
                case.result = True
            else:
                case.result = False

        with uuid('1935e955-aab2-44eb-9a6e-305d9eb2f836') as case:
            # 7.1. Editing confirmation
            # 7.1.2. Save As... > Template Thumbnail > Slider
            # drag slider to set the template thumbnail correctly
            pip_designer_page.save_as_name('01_modifyPiP')
            pip_designer_page.save_as_set_slider(0.2)

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_7_1_2_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_7_1_2_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('fbc5354f-5a4e-4436-ba96-c20c0369a065') as case:
            # 7.1. Editing confirmation
            # 7.1.2. Save As... > Result > OK
            # pop up "save as template" and save template correctly
            pip_designer_page.exist_click(L.pip_designer.save_as_ok)

            check_result = pip_designer_page.get_title()
            if not check_result == '01_modifyPiP':
                case.result = False
            else:
                case.result = True

        with uuid('26397f43-da4e-4328-96c2-7222c077a109') as case:
            # 7.1. Editing confirmation
            # 7.1.3. Share > DZ & Cloud
            # upload successful and template on website is correct
            # AT limitation
            case.result = None
            case.fail_log = "*AT limitation*"

        with uuid('adfb66cf-8fd7-4a3d-9162-5ba05354764d') as case:
            # 7.1. Editing confirmation
            # 7.1.1. OK > Modified template
            # editing is saved and template is overwrite then leave module directly
            pip_designer_page.click_ok()

            check_result_1 = pip_room_page.check_is_in_Custom_category('01_modifyPiP')

            check_result = pip_designer_page.exist(L.pip_designer.designer_window)
            if not check_result:
                check_result_2 = True
            else:
                check_result_2 = False
            case.result = check_result_1 and check_result_2



        with uuid('08406117-2ce8-4c3e-a9ae-c68d519f4d7e') as case:
            # 7.2. Blending Mode
            # 7.2.1. Save Blending mode setting with template > Set Blending mode on timeline right click menu > Darken
            # pip can apply blending correctly
            main_page.enter_room(0)
            main_page.insert_media('Food.jpg')
            timeline_operation_page.timeline_select_track(2)
            main_page.enter_room(4)
            pip_room_page.hover_library_media('01_modifyPiP')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            main_page.tap_TipsArea_Tools_menu(index=0)
            pip_designer_page.switch_mode('Advanced')

            item = pip_designer_page.exist(L.pip_designer.object_setting.position)
            if not item:
                pip_designer_page.exist_click(L.pip_designer.object_setting.object_setting)
            else:
                pip_designer_page.drag_properties_scroll_bar(1.0)

            pip_designer_page.set_timecode('00_00_01_00')
            pip_designer_page.set_blending_mode_darken()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_7_2_1_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_7_2_1_1.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('0f6c505b-6f8f-4f44-8e90-a519cf860314') as case:
            # 7.2. Blending Mode
            # 7.2.1. Save Blending mode setting with template > Set Blending mode on timeline right click menu > Multiply
            # pip can apply blending correctly
            pip_designer_page.set_blending_mode_multiply()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_7_2_1_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_7_2_1_2.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('2186c419-8819-4dcd-be65-30198b3e5f96') as case:
            # 7.2. Blending Mode
            # 7.2.1. Save Blending mode setting with template > Set Blending mode on timeline right click menu > Lighten
            # pip can apply blending correctly
            pip_designer_page.set_blending_mode_lighten()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_7_2_1_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_7_2_1_3.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('c3ad0293-c99a-41b4-adf9-99a2277e2f16') as case:
            # 7.2. Blending Mode
            # 7.2.1. Save Blending mode setting with template > Set Blending mode on timeline right click menu > Screen
            # pip can apply blending correctly
            pip_designer_page.set_blending_mode_screen()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_7_2_1_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_7_2_1_4.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('13d028b2-d42e-4ac7-ab6b-de3936df9765') as case:
            # 7.2. Blending Mode
            # 7.2.1. Save Blending mode setting with template > Set Blending mode on timeline right click menu > Overlay
            # pip can apply blending correctly
            pip_designer_page.set_blending_mode_overlay()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_7_2_1_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_7_2_1_5.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('d4c67747-7c2d-4f85-a8e8-a687765a5cf1') as case:
            # 7.2. Blending Mode
            # 7.2.1. Save Blending mode setting with template > Set Blending mode on timeline right click menu > Difference
            # pip can apply blending correctly
            pip_designer_page.set_blending_mode_difference()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_7_2_1_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_7_2_1_6.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('936a34a5-fa52-4444-9774-0d1c0fc9397a') as case:
            # 7.2. Blending Mode
            # 7.2.1. Save Blending mode setting with template > Set Blending mode on timeline right click menu > Hue
            # pip can apply blending correctly
            pip_designer_page.set_blending_mode_hue()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_7_2_1_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_7_2_1_7.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('c0572cc0-5170-437a-9e28-3ea3df057438') as case:
            # 7.2. Blending Mode
            # 7.2.1. Save Blending mode setting with template > Set Blending mode on timeline right click menu > Normal
            # pip can apply blending correctly
            pip_designer_page.set_blending_mode_normal()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_designer_7_2_1_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_designer_7_2_1_8.png'
            current_preview = pip_designer_page.snapshot(
                locator=L.pip_designer.designer_window, file_name=image_full_path)
            check_result = pip_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    dc5e4f16-8226-4521-ae83-1e5ed49d308d
                    a883f2f0-c595-4fa8-b288-ba7b0893a4b6
                    dc9ea225-1432-41b5-92ac-991c40baafe9
                    f2ff5751-dd0c-42a8-a347-7f522ee6c7f2
                    dbf1f0e2-b24f-49e0-8310-dc7b2554fcce
                    878268fc-a763-42e5-b740-99cd6db72641
                    395b2563-8c85-4689-aa18-14bd4a2a9d0e
                    91780072-9706-464e-8442-4fe844a2cc67
                    33b96c79-5075-4ce6-ad4d-2cb475b4ec82
                    ce4f3342-9790-4637-8f39-5ec6f42fabdc
                    00eaaaba-95db-4641-b6b7-02b0e83f78b1
                    8fb9b948-5e33-45b0-8590-183df1ddc6bc
                    ac58b904-fa8c-4d92-ad3d-d396e00aecc7
                    806932c0-45ab-4840-bbed-12491047ecc0
                    1395dd40-84b9-4b4b-ad81-b69715724061
                    a2771c2b-5647-46c9-a2aa-4cd1b0ad9dd1
                    cbafedaa-ad25-40e4-b109-d105419fe6d9
                    f9317131-c9c2-461d-bd6f-5362d0848beb
                    f5afc837-7a99-403c-a4cf-492bc282ce21
                    ff29cb85-3c9a-4343-bc19-ee74b9da4490
                    33ddd1de-dd3a-4d91-b007-af2bb6bc92ef
                    97e67db6-4edc-4db0-a8b9-9bc0aefbb6d8
                    09741064-04b1-456c-a2ee-db8aa0fab89a
                    49b278a1-46dc-41a4-8aa3-f23c8c411217
                    5f5726a1-a7e3-4397-9a32-eee0ed9567b5
                    91e7c6ad-0ebb-45cb-8898-26f481ee7019
                    324f4f40-c308-40d5-870d-b6e6b154a6a8
                    6d6161cf-6a47-4338-ba3c-95af2eed64ab
                    1d4f1d30-023e-4fbf-9404-27a7682cdddd
                    93d94423-1da5-40b6-a4f9-c41638f40805
                    a379699a-e039-4124-ba86-e894d8ad0272
                    8080ea26-8e56-4445-9876-52600c6d7614
                    687b1ce4-dd64-4b39-ad93-7fbeb4ba578f
                    ec63aeaf-c16a-4d52-83e3-9ca8b8b03a15
                    8d6dac40-fd22-4317-9f5f-07573a1b6caf
                    191984f5-1a94-4d94-999e-b1df0cf7ca90
                    d52bbb8a-c588-469b-b3b4-7259d8790a38
                    3df32b92-79e1-43c9-a0d8-1a1abe629a01
                    3d64f981-d4fd-45a2-8617-c46a0b090889
                    f459d701-5d49-4819-a362-46129011100a
                    b517bc73-147d-4bfd-860d-61a0272b7945
                    6b1e6054-ad7b-4ca2-89da-338d5eed2f65
                    971f93bc-75bc-4217-a68b-30a764f19ad5
                    094e4d01-a0b2-49c5-be24-276f39c62594
                    3970b5e0-96a4-482c-9bbb-54f0bf8975e7
                    0b355948-df65-4765-bd4c-05e4b819f945
                    9071e6ff-28de-4aa7-b4a6-4aaf92dbc297
                    2806fc53-1d70-4668-b336-406366da3663
                    cc24bc72-c4e0-4126-8c04-bdfbaec9a644
                    437e140a-b3a8-40de-ab6e-2a92e8f2652b
                    7040b5a1-4750-4612-b9c8-d339c0c8274e
                    0e5e4f9f-8bd1-4cc5-aa70-e780cf6f969c
                    3a8c27c7-4ac5-42bc-9d7b-119b555a4fc6
                    ca4b54b1-3c2a-4d68-9b7f-0792383f0045
                    7b48a894-e331-4987-8d57-b038515d75f5
                    923363d6-cb3c-47ac-90ca-4c8c2e5b5b29
                    2610755f-10bf-4a72-b2ba-79ea5fda3d14
                    b3127ee8-2e5f-4868-9af9-7126066b4d0e
                    a815369d-c625-4095-9ebc-386cb0795876
                    84226664-1cbb-4c1a-b944-bc893ef929cb
                    181f37d2-cf5e-40d3-a82f-6cfa950514b3
                    f1e24c40-f4df-4a0c-b7f6-49e4de45612a
                    599d516a-173c-4c2b-9d4f-6db259dd62b4
                    363f0055-6020-4b10-8d50-a55289339b99
                    f991c925-26c9-41e5-9e1a-539a2a8cec99
                    261839b6-e925-4c3e-8dd0-30145029e015
                    ff70b162-d283-4859-b985-27b403334468
                    b8f1f119-672e-4887-93c1-c0f21aafa371
                    cfa52ea6-401a-4dff-96e0-93344b01fb1c
                    2f4bb3e3-a057-4979-a79d-45d3ea50418e
                    967b0bff-e2ba-4c2a-a731-834a7b488b05
                    9e260b51-86fd-44ce-8c81-8e6fb9df01a6
                    356d1060-adf8-41ea-9810-ade2dd5f0883
                    4f6ba940-3773-4a0b-8a40-44d92bf30034
                    c6bcfbec-31fb-4b7d-b9bc-2057561f2378
                    418efbf4-2d0c-438f-b85b-ea497a5603c4
                    ef7be442-b688-4aad-ab80-3b44dc758482
                    8da5f99c-58d6-41b8-bb1a-5517409df403
                    70b26d38-3a46-405e-80e6-3ab76f45459a
                    2b5ed12c-a04a-4c4a-b2fe-9eae2b98494b
                    52140202-6ad8-4cf1-b327-6d3023f2edac
                    b9da434d-c597-48c3-8794-6e159db35c83
                    b65ceb70-8b20-4094-a76c-a6940b47d50a
                    b423e68c-9637-4656-95bd-8f2823992915
                    9d152874-6543-4168-8ddc-0c34466535aa
                    cfab31b3-33b7-4a01-99b4-aca0498191aa
                    b3d4d819-4ded-4f9e-b1ed-cb99ee7d6f9e
                    abbb3173-cee5-45af-817b-aceac1f9fbaf
                    d9420967-d952-4c2d-bc3e-8e69c8b6a54c
                    61cfc2c6-877f-4fbe-a86c-63668c016ca5
                    a957f44f-c30a-4995-897d-cc414acda930
                    ac21a3e7-4ea8-455d-b695-4bdf089a2d34
                    c7b3c35e-01bc-4b08-9c65-7624cb746b9e
                    b6f35c67-752f-41fb-b997-2ceecc2520f6
                    c0f9b824-e0df-430b-bc8f-099bd88c6ae4
                    7536c52a-e280-491d-a457-fb7607366e17
                    7b44abe8-4ae7-4b29-a87a-0848f1a5e90c
                    8b61f9e8-e0ea-49b3-8fc4-fa1fd525078d
                    0266354f-9a4c-4a3a-a52d-91ef7af6c33d
                    9efb44e7-5c8d-4266-a5ed-722e8bc42a3a
                    d999afa7-0a9e-4860-885e-7fcd5d85a0ad
                    36c3f7b4-898c-46ab-aca8-8a984b249652
                    7df89f00-f6de-409a-b3c3-658b5b3161af
                    0bddbd57-2266-4652-a3f6-e411f5111702
                    fb07dce9-7fe1-4e62-a5ca-90ad68ffec0b
                    57bf5017-d3e4-4428-847a-cc92dabbbeda
                    98236623-3d68-43f0-b5c9-eb3031f6352b
                    805e3a6c-3fd8-4fdd-9c4e-da03a7219f66
                    62024066-6d8f-4808-87d0-f3128e2bd4d0
                    cc36a543-a096-4de2-a47f-d252d1583dc1
                    562f93f5-68bf-4009-9dfe-17a33ec2a418
                    d727e4e3-108d-4311-a85a-fb454c63f0d4
                    1c0f7e04-d46a-40fb-9605-2782fcccc8df
                    ca24222c-ddb3-4cbd-b529-cb43c0be11bd
                    0a541e22-dae6-41da-98e4-29ba632550d1
                    4045bb5a-b849-4b6b-9a6e-a9babc71effc
                    8e97e4fa-0317-43c1-b840-1271d2a03338
                    7fcd9f42-0e92-4dd1-bd80-7055af2a2772
                    a09eb96a-e143-4f6f-b106-ca4c001a5387
                    b9326e03-3864-47fa-b945-545541f1b0c7
                    91d20fdd-0d52-4531-88fd-df08e367d987
                    898fc69b-c5c1-4e57-9c0c-9b0a10bc8d62
                    ce1a5762-d582-4f1c-b74f-8dd3bf3f32d0
                    76cd60a6-55e2-48f7-9e84-219d9ebd0e90
                    7d56a6a7-d726-4620-845a-3e5ecdc79758
                    d049dcdf-da80-4230-a461-b809053f3a48
                    c22a2fe2-15ac-4a39-80d5-6eb5e8cdf009
                    3b49c1e6-0e68-49dd-9b20-232c8dd04df6
                    d433f5ee-d2db-47b6-98b9-76605241da45
                    8c0489e3-b5e4-4b49-b1bd-6324273cb158
                    f5ab8a19-3ace-4295-9cd0-756f56b821eb
                    c34a7115-0639-4ad7-b889-4b71d1da56db
                    99a17170-1003-4544-b094-cc1e2511775b
                    da2c2a08-a5f3-4432-ac23-a6703183afef
                    4594f3c0-f97e-454a-8233-cf20a467f5a5
                    c677d10e-a9e5-474f-bdc7-3586c00c7ed1
                    a583e67c-705d-45f1-8d33-52ab896d0ac3
                    a7acfca0-fda2-43d8-b00c-ad408982e025
                    fe5f0a51-01e8-4773-8c1c-d6c21d63bfda
                    3b42498a-107e-4c8d-94ac-1a583777ccc0
                    748078ce-547c-46bf-8374-7a051454b58f
                    0255b290-25c3-4d86-a73d-f6e0688fb310
                    658935f8-dcd7-414a-86d6-6255bb493589
                    00746a53-6e19-4122-929a-2705a21edfd1
                    e0077cc2-4923-44f5-90cb-05cabffc7b61
                    259cf435-efb1-47e6-bb46-d86f1f9f6a53
                    a868b5ae-4f21-45d1-b288-333f0a745c82
                    db5bb3a6-8882-4150-aa0c-125f19083db8
                    21114a73-7c66-4714-ae11-fbc020bb2f61
                    f2ab1844-fb36-44fc-8fb8-bc4ce915709f
                    23d504c3-32f0-4055-9958-08196a8992e2
                    a2ae4c65-528a-4623-894b-99cd9861c696
                    4cb61b28-9ba7-4556-8a2a-875c768e79da
                    6f3843ce-42e3-48b3-8b43-21ceedd8e944
                    df56b069-af42-48cb-b08c-16650529ec95
                    d40c059a-38af-4dad-b6f1-2c5d675bd45a
                    61cce6f1-f308-4313-ad17-bdc76cdc3feb
                    26397f43-da4e-4328-96c2-7222c077a109
                    b2c833d0-55b3-4c6f-8af4-e3ecca04d7f4
                    d875b581-99c9-4006-8c34-26f35c429681
                    4ba3494b-3df0-463a-804a-fb8f683025f5
                    9dd824f5-5aca-4cfb-b8e9-69d52fc179b3
                    437f04b4-3a41-4228-b37a-68af6995efdf
                    02f182f2-d99a-4444-9f4a-2a14b5f4c5dd
                  ''') as case:

            case.result = None
            case.fail_log = "*SKIP by AT*"



