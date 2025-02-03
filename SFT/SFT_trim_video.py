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
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)
precut_page = PageFactory().get_page_object('precut_page', mwc)
trim_page = PageFactory().get_page_object('trim_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Trim Video.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Trim_Video/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Trim_Video/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1


class Test_Trim_Video():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
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
            google_sheet_execution_log_init('Trim_Video')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"trim video result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        with uuid('68c07231-1cfc-4eea-bcc3-af849eca745f') as case:
            # 1. General
            # 1.1. Entry Point
            # 1.1.1. Timeline > Video > Tip area
            # Show Trim icon in tip area for video content on timeline
            main_page.insert_media('Skateboard 02.mp4')
            check_result = trim_page.is_exist(L.tips_area.button.btn_trim, timeout=5)
            case.result = check_result

        with uuid('f9689684-c084-43ef-aa1f-9f0a7de6923e') as case:
            # 1.1. Entry Point
            # 1.1.1. Timeline > Video > Tip area
            # Open Trim window after clicking Trim icon
            tips_area_page.click_TipsArea_btn_Trim(type='video')
            check_result = trim_page.check_in_Trim()
            case.result = check_result

        with uuid('c62a5f5f-d113-4e49-89be-d45014f4a554') as case:
            # 1.2. Caption bar
            # 1.2.1. File name
            # Show clip name on the caption bar
            caption_bar_title = trim_page.get_trim_title()
            check_result = False if not caption_bar_title == 'Skateboard 02.mp4' else True
            case.result = check_result

        with uuid('7b5a10ef-644d-46b0-b508-aae7f9671e10') as case:
            # 1.2. Caption bar
            # 1.2.2. Maximize / Restore button
            # Maximize/restore window size
            img_before = precut_page.screenshot()
            precut_page.click_window_max_restore_btn()
            current_result = precut_page.wait_for_image_changes(img_before)
            case.result = current_result
            if current_result is True:
                precut_page.click_window_max_restore_btn()

        with uuid('f46a09a3-d7c7-43a0-8357-e8265341e77b') as case:
            # 1.2. Caption bar
            # 1.2.3. Close button
            # Close trim dialog without changes
            precut_page.close_precut_window()
            check_result = trim_page.check_in_Trim()
            case.result = True if not check_result else False

        with uuid('67b05c56-1085-4935-9d26-89af0121a007') as case:
            # 1.1. Entry Point
            # 1.1.1. Timeline > Video > Right click menu
            # Show Trim function in right-click menu if select timeline's video
            timeline_operation_page.hover_timeline_media(track_index=0, clip_index=0)
            timeline_operation_page.right_click()
            timeline_operation_page.select_right_click_menu('Edit Video')

            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_1_1_1-1.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_1_1_1-1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result = timeline_operation_page.compare(ground_truth, current_preview, similarity=0.9)
            case.result = check_result

            main_page.press_esc_key()

        with uuid('5b23e9b7-f201-487f-9ae9-de3515bb0971') as case:
            # 1.1. Entry Point
            # 1.1.1. Timeline > Video > Right click menu
            # Open TrIm window after selecting Trim function
            timeline_operation_page.hover_timeline_media(track_index=0, clip_index=0)
            timeline_operation_page.right_click()
            timeline_operation_page.select_right_click_menu('Edit Video', 'Trim...')
            check_result = trim_page.check_in_Trim()
            case.result = check_result

            precut_page.close_precut_window()

        with uuid('80e240c4-daf0-49da-94ba-83ea9eb34937') as case:
            # 1.1. Entry Point
            # 1.1.1. Timeline > Video > Hotkey: [Option] + [Command] + [T]
            # Open the Trim window if current focus is video
            trim_page.tap_Trim_hotkey()
            check_result = trim_page.check_in_Trim()
            case.result = check_result

            precut_page.close_precut_window()

        with uuid('8b6ed4e2-5cc7-4125-8bd0-a3c81e52931a') as case:
            # 1.1. Entry Point
            # 1.1.1. Timeline > Photo
            # Trim function should disable for photo content
            timeline_operation_page.tap_Remove_hotkey()
            main_page.insert_media('Food.jpg')
            check_result = trim_page.is_not_exist(L.tips_area.button.btn_trim, timeout=5)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        main_page.insert_media('Skateboard 02.mp4')
        tips_area_page.click_TipsArea_btn_Trim(type='video')
        trim_page.exist(L.trim.main_window, timeout=5)
        with uuid('f1231699-7899-4d34-92b0-281529f2a1c3') as case:
            # 2. Main Function
            # 2.1. Category
            # 2.1.1. Module switch
            # Switch between Single and Multi Trim correctly
            check_result_1 = precut_page.edit_precut_switch_trim_mode(mode='Multi')
            time.sleep(DELAY_TIME * 3)
            check_result_2 = precut_page.edit_precut_switch_trim_mode(mode='Single')
            case.result = check_result_1 and check_result_2

        with uuid('56cec6f1-aba5-4be8-8f09-1c6beb0e23c9') as case:
            # 2.1. Category
            # 2.1.2. Editing Interrupt (Multi -> Single)
            # Show warning to remind user if interrupt multi trim process
            precut_page.edit_precut_switch_trim_mode(mode='Multi')
            time.sleep(DELAY_TIME * 3)

            precut_page.tap_multi_trim_mark_in()
            precut_page.set_precut_timecode('00;00;02;00')
            # precut_page.drag_multi_trim_slider(hour=0, min=0, sec=2, mini_sec=0)
            precut_page.tap_multi_trim_mark_out()

            precut_page.set_precut_timecode('00;00;04;00')
            precut_page.tap_multi_trim_mark_in()
            precut_page.set_precut_timecode('00;00;06;00')
            precut_page.tap_multi_trim_mark_out()
            precut_page.edit_precut_switch_trim_mode(mode='Single')

            check_result = precut_page.handle_changes_not_applied_want_continue()
            case.result = check_result

            precut_page.close_precut_window()
            precut_page.handle_save_change_before_leaving(option=1)  # No save

        with uuid('b1959a21-2dc3-4e83-bdeb-ba0dd81f34b3') as case:
            # 2.2. Single Trim
            # 2.2.1. [Mark in] icon
            # Drag mark in icon to set beginning point directly
            tips_area_page.click_TipsArea_btn_Trim(type='video')
            trim_page.exist(L.trim.main_window, timeout=5)

            case.result = None  # AT limitation, cannot control yellow mark in/out icon
            case.fail_log = '*SKIP by AT limitation'

        with uuid('a42767a5-2486-42a5-a096-ff50ba1f768c') as case:
            # 2.2. Single Trim
            # 2.2.2. [Mark out] icon
            # Drag mark out icon to set ending point directly
            case.result = None  # AT limitation, cannot control yellow mark in/out icon
            case.fail_log = '*SKIP by AT limitation'

        with uuid('0c1e7352-b76a-4536-83c2-b1c2aeab618e') as case:
            # 2.2. Single Trim
            # 2.2.3. Mark in > Button
            # Move indicator to the beginning point then click mark in button or hotkey "I",
            # the mark in icon would set on current position
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 2, 0)
            precut_page.tap_single_trim_mark_in()

            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_2_3-1.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_2_3-1.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('61f0ac60-d9ed-47b6-be10-791643a48ac1') as case:
            # 2.2. Single Trim
            # 2.2.3. Mark in > Button
            # Clip duration would be update correctly
            current_duration = precut_page.get_precut_single_trim_duration()
            case.result = False if not current_duration == '00;00;08;00' else True

        with uuid('5196b566-d292-46fd-8b19-4fe062db7383') as case:
            # 2.2. Single Trim
            # 2.2.3. Mark in > Button
            # In position timecode & instant preview would be updated correctly
            in_position_timecode = precut_page.get_single_trim_precut_in_position()
            check_result_1 = False if not in_position_timecode == '00;00;02;00' else True
            check_result_2 = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_2_3-2.png', area='in position thumbnail')
            case.result = check_result_1 and check_result_2

        with uuid('d3699042-8bdf-419b-9b2d-b04e54fd07de') as case:
            # 2.2. Single Trim
            # 2.2.4. Mark out > Button
            # Move indicator to the ending point then click mark out button or hotkey "O",
            # the mark out icon would set on current position
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 8, 0)
            precut_page.tap_single_trim_mark_out()

            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_2_4-1.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_2_4-1.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('f6d92e90-7661-4ac2-8c0f-6c65ec22381c') as case:
            # 2.2. Single Trim
            # 2.2.4. Mark out > Button
            # Clip duration would be update correctly
            current_duration = precut_page.get_precut_single_trim_duration()
            case.result = False if not current_duration == '00;00;06;00' else True

        with uuid('9623f130-15ad-43c7-a2f1-450e825df423') as case:
            # 2.2. Single Trim
            # 2.2.4. Mark out > Button
            # Out position timecode & instant preview would be updated correctly
            out_position_timecode = precut_page.get_single_trim_precut_out_position()
            check_result_1 = False if not out_position_timecode == '00;00;08;00' else True
            check_result_2 = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_2_4-2.png', area='out position thumbnail')
            case.result = check_result_1 and check_result_2

        with uuid('2eccc699-4861-4033-867a-4512dc47eb88') as case:
            # 2.2. Single Trim
            # 2.2.3. Mark in > Hotkey
            # Hotkey can work correctly
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 1, 0)
            precut_page.tap_MarkIn_onLibraryPreview_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_2_3-3.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_2_3-3.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('2dc3fc6f-025b-4d7a-a282-568495a78be4') as case:
            # 2.2. Single Trim
            # 2.2.4. Mark out > Hotkey
            # Hotkey can work correctly
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 9, 0)
            precut_page.tap_MarkOut_onLibraryPreview_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_2_3-4.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_2_3-4.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('cf59a60e-85bf-4cac-b774-00db7786da01') as case:
            # 2.2. Single Trim
            # 2.2.5. [Unlock/Lock] icon	> Unlock status
            # Trim duration is not fixed
            precut_page.click_precut_single_trim_lock_duration()

            check_result_1 = not precut_page.exist(L.precut.single_trim_precut_duration).AXEnabled
            check_result_2 = not precut_page.exist(L.precut.single_trim_precut_in_position).AXEnabled
            check_result_3 = not precut_page.exist(L.precut.single_trim_precut_out_position).AXEnabled

            old_duration = precut_page.get_precut_single_trim_duration()
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 1, 15)
            precut_page.tap_single_trim_mark_in()
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result_4 = False if not old_duration == current_duration else True

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('07efbcc3-61a0-4f7c-ae47-ec289d7f2707') as case:
            # 2.2. Single Trim
            # 2.2.5. [Unlock/Lock] icon	> Lock status
            # Trim duration is fixed
            case.result = check_result_4

        with uuid('33fc8d61-5d62-40e3-83de-8970c8e1cf2e') as case:
            # 2.2. Single Trim
            # 2.2.5. [Unlock/Lock] icon	> Lock status
            # Fixed segment can be moved position on slide bar
            case.result = check_result_4

        with uuid('c5398bd3-e433-44e8-bd26-f12df8b65e02') as case:
            # 2.2. Single Trim
            # 2.2.5. [Unlock/Lock] icon	> Unlock status
            # Mark in and Mark out button are not disabled
            precut_page.click_precut_single_trim_lock_duration()
            precut_page.set_precut_timecode('00;00;03;00')
            check_result_1 = precut_page.exist(L.precut.single_trim_mark_out).AXEnabled
            precut_page.set_precut_timecode('00;00;07;00')
            check_result_2 = precut_page.exist(L.precut.single_trim_mark_in).AXEnabled
            case.result = check_result_1 and check_result_2

        with uuid('42cd75be-ca1a-4b36-a428-aa43f8d983a0') as case:
            # 2.2. Single Trim
            # 2.2.5. [Unlock/Lock] icon	> Lock status
            # Mark in and Mark out are disabled
            precut_page.click_precut_single_trim_lock_duration()
            precut_page.set_precut_timecode('00;00;03;00')
            check_result_1 = not precut_page.exist(L.precut.single_trim_mark_out).AXEnabled
            precut_page.set_precut_timecode('00;00;07;00')
            check_result_2 = not precut_page.exist(L.precut.single_trim_mark_in).AXEnabled
            case.result = check_result_1 and check_result_2

        with uuid('d1809aef-4adb-4a11-9ee8-7cf60f1d0493') as case:
            # 2.2. Single Trim
            # 2.2.5. [Unlock/Lock] icon	> Lock status
            # [Duration] can't modify
            check_result = not precut_page.exist(L.precut.single_trim_precut_duration).AXEnabled
            case.result = check_result

            precut_page.close_precut_window()
            precut_page.handle_save_change_before_leaving(option=1)

        with uuid('00b0ca09-ab31-4424-acaf-614f6c0c47fe') as case:
            # 2.2. Single Trim
            # 2.2.6. [Duration] input box > Default value
            # Display original clip duration for 1st entry
            tips_area_page.click_TipsArea_btn_Trim(type='video')
            trim_page.exist(L.trim.main_window, timeout=5)
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result = False if not current_duration == '00;00;10;00' else True
            case.result = check_result

        with uuid('4dbb1a3a-e676-4c21-aeca-620417675f00') as case:
            # 2.2. Single Trim
            # 2.2.5. [Unlock/Lock] icon	> Lock status
            # Min fixed duration is 1 frame
            precut_page.tap_single_trim_mark_in()
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 0, 1)
            precut_page.tap_single_trim_mark_out()
            precut_page.click_precut_single_trim_lock_duration()
            time.sleep(DELAY_TIME)
            check_result = precut_page.get_precut_single_trim_duration()
            case.result = False if not check_result == '00;00;00;01' else True

            precut_page.click_precut_single_trim_lock_duration()  # unlock

        with uuid('83ace45b-d048-40bb-9320-ce978e82bfc9') as case:
            # 2.2. Single Trim
            # 2.2.6. [Duration] input box > Keyboard
            # Input new clip duration by keyboard
            precut_page.set_precut_single_trim_duration('00_08_00')
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result = False if not current_duration == '00;00;08;00' else True
            case.result = check_result

        with uuid('1c85bfc5-253e-4c94-bd90-d63d9d64816e') as case:
            # 2.2. Single Trim
            # 2.2.6. [Duration] input box > Keyboard
            # Out position would also be updated accordingly
            check_result = precut_page.get_single_trim_precut_out_position()
            case.result = False if not check_result == '00;00;08;00' else True

        with uuid('e1010c64-83cb-4b3a-9a07-bc0488b7855c') as case:
            # 2.2. Single Trim
            # 2.2.6. [Duration] input box > Keyboard
            # Mark out icon would be updated accordingly
            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_2_6-1.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_2_6-1.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('25c9c057-2823-4647-b137-a7f2fddd41a4') as case:
            # 2.2. Single Trim
            # 2.2.6. [Duration] input box > Less button
            # Decrease 1 frame for each click
            check_result_1 = precut_page.click_precut_single_trim_duration_arrow_button(option=1)  # 0: up, 1: down
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result_2 = False if not current_duration == '00;00;07;29' else True
            case.result = check_result_1 and check_result_2

        with uuid('ae2b4b87-157d-43b2-8a52-7157c0912f2e') as case:
            # 2.2. Single Trim
            # 2.2.6. [Duration] input box > Less button
            # Out position would also decrease 1 frame and update the preview thumbnail correctly
            current_out_position = precut_page.get_single_trim_precut_out_position()
            check_result_1 = False if not current_out_position == '00;00;07;29' else True
            check_result_2 = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_2_6-2.png', 'out position thumbnail')

            case.result = check_result_1 and check_result_2

        with uuid('428ac064-810a-409c-a0b4-604a5ee4e408') as case:
            # 2.2. Single Trim
            # 2.2.6. [Duration] input box > Less button
            # Mark out icon would be updated accordingly
            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_2_6-3.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_2_6-3.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('c4b22428-69b1-41df-82d2-6a57db10fcc9') as case:
            # 2.2. Single Trim
            # 2.2.6. [Duration] input box > More button
            # Increase 1 frame for each click
            check_result_1 = precut_page.click_precut_single_trim_duration_arrow_button(option=0)  # 0: up, 1: down
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result_2 = False if not current_duration == '00;00;08;00' else True
            case.result = check_result_1 and check_result_2

        with uuid('b2669afe-c398-4ebb-b27b-27a2bc6374f8') as case:
            # 2.2. Single Trim
            # 2.2.6. [Duration] input box > More button
            # Out position would also increase 1 frame and update the preview thumbnail correctly
            current_out_position = precut_page.get_single_trim_precut_out_position()
            check_result_1 = False if not current_out_position == '00;00;08;00' else True
            check_result_2 = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_2_6-4.png', 'out position thumbnail')

            case.result = check_result_1 and check_result_2

        with uuid('407ae7e4-add1-4440-8b8c-824a0026224b') as case:
            # 2.2. Single Trim
            # 2.2.6. [Duration] input box > More button
            # Mark out icon would be updated accordingly
            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_2_6-5.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_2_6-5.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('125fbf4f-ad7c-4116-b4e0-2c088be7f885') as case:
            # 2.2. Single Trim
            # 2.2.6. [Duration] input box > Min value
            # Min: 1 frame
            precut_page.set_precut_single_trim_duration('00_00_00')
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result = False if not current_duration == '00;00;00;01' else True
            case.result = check_result

        with uuid('2fe478e8-050d-436b-96d0-d955eaa7343e') as case:
            # 2.2. Single Trim
            # 2.2.6. [Duration] input box > Max value
            # Max: untrimmed clip duration
            precut_page.set_precut_single_trim_duration('00_15_00')
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result = False if not current_duration == '00;00;10;00' else True
            case.result = check_result

        with uuid('00544f37-1089-4653-975e-e66f55fffc75') as case:
            # 2.2. Single Trim
            # 2.2.6. [Duration] input box > Default value
            # Display trimmed clip duration for re-entry
            precut_page.set_precut_single_trim_duration('00_08_00')
            precut_page.click_ok()
            tips_area_page.click_TipsArea_btn_Trim(type='video')
            trim_page.exist(L.trim.main_window, timeout=5)
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result = False if not current_duration == '00;00;08;00' else True
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        main_page.insert_media('Skateboard 02.mp4')
        tips_area_page.click_TipsArea_btn_Trim(type='video')
        trim_page.exist(L.trim.main_window, timeout=5)
        with uuid('ab789b5a-1c13-4aa4-927f-bd3a8899aa41') as case:
            # 2.2. Single Trim
            # 2.2.7. [In position] input box > Default value
            # Set 00:00:00:00 as default
            current_in_position = precut_page.get_single_trim_precut_in_position()
            check_result = False if not current_in_position == '00;00;00;00' else True
            case.result = check_result

        with uuid('63c6308d-0201-458e-bb8a-f4de9e69b060') as case:
            # 2.2. Single Trim
            # 2.2.7. [In position] input box > Keyboard
            # Input new in position timecode by keyboard
            precut_page.set_single_trim_precut_in_position('00_02_00')
            current_in_position = precut_page.get_single_trim_precut_in_position()
            check_result = False if not current_in_position == '00;00;02;00' else True
            case.result = check_result

        with uuid('9f5c5d8d-6f66-48fa-b636-d1e6b300a316') as case:
            # 2.2. Single Trim
            # 2.2.7. [In position] input box > Keyboard
            # Clip duration would also be updated accordingly
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result = False if not current_duration == '00;00;08;00' else True
            case.result = check_result

        with uuid('cd351275-e0b6-4fe7-be1a-c769d1877b1a') as case:
            # 2.2. Single Trim
            # 2.2.7. [In position] input box > Keyboard
            # Mark in icon would be updated accordingly
            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_2_7-1.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_2_7-1.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('be7b8959-e0d7-4535-b528-81c6e9cd59f0') as case:
            # 2.2. Single Trim
            # 2.2.7. [In position] input box > Less button
            # In position would decrease 1 frame for each click and update the preview thumbnail accordingly
            check_result_1 = precut_page.click_precut_single_trim_in_position_arrow_button(option=1)  # 0: up, 1: down
            current_in_position = precut_page.get_single_trim_precut_in_position()
            check_result_2 = False if not current_in_position == '00;00;01;29' else True
            check_result_3 = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_2_7-2.png', 'in position thumbnail')

            case.result = check_result_1 and check_result_2 and check_result_3

        with uuid('dda4b7eb-37c5-416c-af8a-4ded255b5747') as case:
            # 2.2. Single Trim
            # 2.2.7. [In position] input box > Less button
            # Clip duration would also be updated accordingly
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result = False if not current_duration == '00;00;08;01' else True
            case.result = check_result

        with uuid('7b0ecb4b-0467-490c-a723-d5d3232dbdc5') as case:
            # 2.2. Single Trim
            # 2.2.7. [In position] input box > Less button
            # Mark in icon would be updated accordingly
            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_2_7-3.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_2_7-3.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('e2ce60c2-8427-44f6-87f5-5705bf513f86') as case:
            # 2.2. Single Trim
            # 2.2.7. [In position] input box > More button
            # In position would increase 1 frame for each click and update the preview thumbnail accordingly
            check_result_1 = precut_page.click_precut_single_trim_in_position_arrow_button(option=0)  # 0: up, 1: down
            current_in_position = precut_page.get_single_trim_precut_in_position()
            check_result_2 = False if not current_in_position == '00;00;02;00' else True
            check_result_3 = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_2_7-4.png', 'in position thumbnail')

            case.result = check_result_1 and check_result_2 and check_result_3

        with uuid('4cb3be9c-e5c1-4360-a33c-4ff509d7779b') as case:
            # 2.2. Single Trim
            # 2.2.7. [In position] input box > More button
            # Clip duration would also be updated accordingly
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result = False if not current_duration == '00;00;08;00' else True
            case.result = check_result

        with uuid('37004189-0605-42df-99cb-c58b18c6a377') as case:
            # 2.2. Single Trim
            # 2.2.7. [In position] input box > More button
            # Mark in icon would be updated accordingly
            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_2_7-5.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_2_7-5.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('ff7f5ac6-9a5d-48e3-8f66-c6aff456e74a') as case:
            # 2.2. Single Trim
            # 2.2.7. [In position] input box > Min value
            # Is 00:00:00:00
            precut_page.set_single_trim_precut_in_position('00_00_00')
            current_in_position = precut_page.get_single_trim_precut_in_position()
            check_result = False if not current_in_position == '00;00;00;00' else True
            case.result = check_result

        with uuid('07cee5b4-1019-400a-b5e2-e9db1eb7bc2d') as case:
            # 2.2. Single Trim
            # 2.2.7. [In position] input box > Max value
            # Max: Total Duration - 1 frame
            precut_page.set_single_trim_precut_in_position('00_15_30')
            current_in_position = precut_page.get_single_trim_precut_in_position()
            check_result = False if not current_in_position == '00;00;09;29' else True
            case.result = check_result

        with uuid('381b9bf9-09c3-4659-a00d-7a3632964838') as case:
            # 2.2. Single Trim
            # 2.2.7. [In position] input box > Default value
            # Display trimmed clip duration for re-entry
            precut_page.set_single_trim_precut_in_position('00_02_00')
            precut_page.click_ok()
            tips_area_page.click_TipsArea_btn_Trim(type='video')
            trim_page.exist(L.trim.main_window, timeout=5)
            current_in_position = precut_page.get_single_trim_precut_in_position()
            check_result = False if not current_in_position == '00;00;02;00' else True
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        main_page.insert_media('Skateboard 02.mp4')
        tips_area_page.click_TipsArea_btn_Trim(type='video')
        trim_page.exist(L.trim.main_window, timeout=5)
        with uuid('efd0ad7c-7b32-432b-a11a-9e5ca03de1fa') as case:
            # 2.2. Single Trim
            # 2.2.8. [Out position] input box > Default value
            # Display original clip duration for 1st entry
            current_out_position = precut_page.get_single_trim_precut_out_position()
            check_result = False if not current_out_position == '00;00;10;00' else True
            case.result = check_result

        with uuid('829b0ffc-bf43-42f1-b28d-17ede8b1c464') as case:
            # 2.2. Single Trim
            # 2.2.8. [Out position] input box > Keyboard
            # Input new out position timecode by keyboard
            precut_page.set_single_trim_precut_out_position('00_08_00')
            current_out_position = precut_page.get_single_trim_precut_out_position()
            check_result = False if not current_out_position == '00;00;08;00' else True
            case.result = check_result

        with uuid('64c33ba7-69f2-4045-a67f-c62fd0fbc04b') as case:
            # 2.2. Single Trim
            # 2.2.8. [Out position] input box > Keyboard
            # Clip duration would also be updated accordingly
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result = False if not current_duration == '00;00;08;00' else True
            case.result = check_result

        with uuid('ef35ee16-c7b6-4651-a168-15703ce61ac9') as case:
            # 2.2. Single Trim
            # 2.2.8. [Out position] input box > Keyboard
            # Mark out icon would be updated accordingly
            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_2_8-1.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_2_8-1.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('ad82ee21-1850-4522-80d3-b305100dabce') as case:
            # 2.2. Single Trim
            # 2.2.8. [Out position] input box > Less button
            # out position would decrease 1 frame for each click and update the preview thumbnail accordingly
            check_result_1 = precut_page.click_precut_single_trim_out_position_arrow_button(option=1)  # 0: up, 1: down
            current_out_position = precut_page.get_single_trim_precut_out_position()
            check_result_2 = False if not current_out_position == '00;00;07;29' else True
            check_result_3 = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_2_8-2.png', 'out position thumbnail')

            case.result = check_result_1 and check_result_2 and check_result_3

        with uuid('c1e569ce-3a33-4ed5-b118-8d98bd3254d0') as case:
            # 2.2. Single Trim
            # 2.2.8. [Out position] input box > Less button
            # Clip duration would also be updated accordingly
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result = False if not current_duration == '00;00;07;29' else True
            case.result = check_result

        with uuid('256acd73-6167-47a3-a57a-68c71856b3b5') as case:
            # 2.2. Single Trim
            # 2.2.8. [Out position] input box > Less button
            # Mark out icon would be updated accordingly
            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_2_8-3.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_2_8-3.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('ca7016ab-094b-4388-9eac-8e0f850f3403') as case:
            # 2.2. Single Trim
            # 2.2.8. [Out position] input box > More button
            # out position would increase 1 frame for each click and update the preview thumbnail accordingly
            check_result_1 = precut_page.click_precut_single_trim_out_position_arrow_button(option=0)  # 0: up, 1: down
            current_out_position = precut_page.get_single_trim_precut_out_position()
            check_result_2 = False if not current_out_position == '00;00;08;00' else True
            check_result_3 = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_2_8-4.png', 'out position thumbnail')

            case.result = check_result_1 and check_result_2 and check_result_3

        with uuid('be842eda-d984-44e5-9130-5aa4bd6e4463') as case:
            # 2.2. Single Trim
            # 2.2.8. [Out position] input box > More button
            # Clip duration would also be updated accordingly
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result = False if not current_duration == '00;00;08;00' else True
            case.result = check_result

        with uuid('be2bbefd-1534-476a-a84d-510ca33aeb68') as case:
            # 2.2. Single Trim
            # 2.2.8. [Out position] input box > More button
            # Mark out icon would be updated accordingly
            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_2_8-5.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_2_8-5.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('7c29a8b8-5440-46a4-a8bf-b45c1caa9eb7') as case:
            # 2.2. Single Trim
            # 2.2.8. [Out position] input box > Min value
            # Min: 1 frame
            precut_page.set_single_trim_precut_out_position('00_00_00')
            current_out_position = precut_page.get_single_trim_precut_out_position()
            check_result = False if not current_out_position == '00;00;00;01' else True
            case.result = check_result

        with uuid('276416b4-1f40-464c-b3aa-6686f67438ec') as case:
            # 2.2. Single Trim
            # 2.2.8. [Out position] input box > Max value
            # Max: Total Duration
            precut_page.set_single_trim_precut_out_position('00_15_30')
            current_out_position = precut_page.get_single_trim_precut_out_position()
            check_result = False if not current_out_position == '00;00;10;00' else True
            case.result = check_result

        with uuid('d57e6032-44cc-4eea-942c-85fb1e8a8d83') as case:
            # 2.2. Single Trim
            # 2.2.8. [Out position] input box > Keyboard
            # Larger than [In position]
            precut_page.set_single_trim_precut_in_position('00_05_00')
            precut_page.set_single_trim_precut_out_position('00_04_00')
            current_out_position = precut_page.get_single_trim_precut_out_position()
            check_result = False if not current_out_position == '00;00;05;01' else True
            case.result = check_result

        with uuid('b085bab0-609a-4421-8764-2f74dadb3002') as case:
            # 2.2. Single Trim
            # 2.2.8. [Out position] input box > Default value
            # Display trimmed clip duration for re-entry
            precut_page.set_single_trim_precut_out_position('00_08_00')
            precut_page.click_ok()
            tips_area_page.click_TipsArea_btn_Trim(type='video')
            trim_page.exist(L.trim.main_window, timeout=5)
            current_out_position = precut_page.get_single_trim_precut_out_position()
            check_result = False if not current_out_position == '00;00;08;00' else True
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        main_page.insert_media('Skateboard 02.mp4')
        tips_area_page.click_TipsArea_btn_Trim(type='video')
        trim_page.exist(L.trim.main_window, timeout=5)
        precut_page.edit_precut_switch_trim_mode(mode='Multi')
        with uuid('4d39921b-e4c3-47ea-8312-52dafe7e0119') as case:
            # 2.3. Multi Trim
            # 2.3.2. [Mark in] icon
            # Drag mark in icon to set beginning point directly
            case.result = None  # AT limitation, cannot control yellow mark in/out icon

        with uuid('83d12ccd-0c11-49ea-aa7b-c899505bf969') as case:
            # 2.3. Multi Trim
            # 2.3.4. Mark in > Button
            # Move indicator to the beginning point then click mark in button or hotkey "I",
            # the mark in icon would set on current position
            precut_page.drag_multi_trim_slider(0, 0, 2, 0)
            precut_page.tap_multi_trim_mark_in()

            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_3_4-1.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_3_4-1.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('5aeec0f3-4285-4b5d-929f-0d15f3e83799') as case:
            # 2.3. Multi Trim
            # 2.3.2. [Mark in] icon
            # Magnification box will follow slider position to move
            time.sleep(DELAY_TIME * 3)
            check_result = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_3_2-2.png', area='thumbnail slider')
            case.result = check_result

        with uuid('71fe0120-d178-46a5-9e24-568b35b37c38') as case:
            # 2.3. Multi Trim
            # 2.3.7. Invert trim result > One segment
            # Show correct result in slide bar and Selected Segments
            check_result = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_3_7-1.png', area='selected segments')
            case.result = check_result

        with uuid('af639c4b-e19a-4ce0-8009-741bc275ea53') as case:
            # 2.3. Multi Trim
            # 2.3.3. [Mark out] icon
            # Drag mark out icon to set ending point directly
            case.result = None  # AT limitation, cannot control yellow mark in/out icon

        with uuid('03961ac6-9d0f-417e-99ea-8db413b7f650') as case:
            # 2.3. Multi Trim
            # 2.3.5. Mark out > Button
            # Move indicator to the ending point then click mark out button or hotkey "]",
            # the mark out icon would set on current position
            precut_page.drag_multi_trim_slider(0, 0, 4, 0)
            precut_page.tap_multi_trim_mark_out()

            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_3_5-1.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_3_5-1.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('ab3ea1a9-ec9a-46ee-a086-526bccea4147') as case:
            # 2.3. Multi Trim
            # 2.3.3. [Mark out] icon
            # Magnification box will follow slider position to move
            check_result = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_3_3-2.png', area='thumbnail slider')
            case.result = check_result

        with uuid('de759c05-566b-4edc-8037-041e34a25681') as case:
            # 2.3. Multi Trim
            # 2.3.4. Mark in > Hotkey
            # hotkey work correctly
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 6, 0)
            precut_page.tap_MarkIn_onLibraryPreview_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_3_4-3.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_3_4-3.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('744b64f0-203f-40eb-9206-cea964974351') as case:
            # 2.3. Multi Trim
            # 2.3.4. Mark in > Multi Mark in
            # Mark in at another position for multi trim correctly
            case.result = check_result

        with uuid('2d78f6a9-06be-41ca-a2da-b1c8833ec223') as case:
            # 2.3. Multi Trim
            # 2.3.5. Mark out > Hotkey
            # hotkey work correctly
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 8, 0)
            precut_page.tap_MarkOut_onLibraryPreview_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_3_5-4.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_3_5-4.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('e894bb36-b905-4838-89ca-992c339a3162') as case:
            # 2.3. Multi Trim
            # 2.3.5. Mark out > Multi Mark out
            # Mark out at another position for multi trim correctly
            case.result = check_result

        with uuid('bb02b31c-4359-4047-8f85-f75b0a4f607b') as case:
            # 2.3. Multi Trim
            # 2.3.7. Invert trim result > Multi Trim
            # Show correct result in slide bar and Selected Segments
            check_result_1 = precut_page.tap_multi_trim_invert_trim()

            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_3_7-2.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_3_7-2.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result_2 = trim_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('fca06ae4-d19f-4a8a-994a-346dfc2b88e0') as case:
            # 2.3. Multi Trim
            # 2.3.9. [Selected Segments] panel > Invert > invert Trim
            # Show correct segment in this panel
            time.sleep(DELAY_TIME * 2)
            check_result = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_3_9-1.png', area='selected segments')
            case.result = check_result

        with uuid('ee9e0646-423f-4f4d-8d0f-6a21ab74737a') as case:
            # 2.3. Multi Trim
            # 2.3.9. [Selected Segments] panel > Invert > Uninvert Trim
            # Show correct segment in this panel
            precut_page.tap_multi_trim_invert_trim()

            check_result = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_3_9-2.png', area='selected segments')
            case.result = check_result

        with uuid('ca8519a0-5370-4767-82ed-64c0a45be01c') as case:
            # 2.3. Multi Trim
            # 2.3.9. [Selected Segments] panel > Context menu > Invert Selection
            # Display Inverted segments
            precut_page.click_multi_trim_segment(segment_index=1)
            precut_page.right_click_multi_trim_segment_invert_selection()
            check_result = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_3_9-6.png', area='selected segments')
            case.result = check_result

        with uuid('2768e980-a791-4b24-9252-464e5716595f') as case:
            # 2.3. Multi Trim
            # 2.3.9. [Selected Segments] panel > Delete > Unselect
            # Delete button should disable
            precut_page.click_multi_trim_segment_unselect_segment()
            btn_status = precut_page.exist(L.precut.multi_trim_remove).AXEnabled
            check_result = True if not btn_status else False
            case.result = check_result

        with uuid('0a442a39-df88-4a78-88d7-3d86eab8f887') as case:
            # 2.3. Multi Trim
            # 2.3.9. [Selected Segments] panel > Delete > Select
            # Delete selected segment correctly
            precut_page.click_multi_trim_segment(segment_index=0)
            check_result_1 = precut_page.tap_multi_trim_remove()
            check_result_2 = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_3_9-4.png', area='selected segments')
            case.result = check_result_1 and check_result_2

        with uuid('3838c88b-04f4-44b7-8178-1053c0f03a5a') as case:
            # 2.3. Multi Trim
            # 2.3.9. [Selected Segments] panel > Context menu > Remove Selected
            # Remove selected clip
            precut_page.click_multi_trim_segment(segment_index=1)
            precut_page.right_click_multi_trim_segment_remove_selected()
            check_result = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_3_9-5.png', area='selected segments')
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        main_page.insert_media('Skateboard 02.mp4')
        tips_area_page.click_TipsArea_btn_Trim(type='video')
        trim_page.exist(L.trim.main_window, timeout=5)
        with uuid('fa03bb6b-fea8-407f-b00c-3b1d47ee10d7') as case:
            # 2.4. Playback panel
            # 2.4.1. Play > Original mode
            # Playback whole video from the beginning to the end smoothly
            check_result_1 = precut_page.precut_preview_operation('Play')
            check_result_2 = precut_page.is_exist(L.precut.precut_pause, timeout=3)
            check_result_3 = precut_page.is_exist(L.precut.precut_play, timeout=15)

            case.result = check_result_1 and check_result_2 and check_result_3

        with uuid('4aa62deb-bebd-45c9-b097-ee561781155a') as case:
            # 2.4. Playback panel
            # 2.4.1. Play > Seek
            # Seek slider during preview
            precut_page.precut_preview_operation('Play')
            while precut_page.exist(L.precut.precut_window_current_time).AXValue[7] < '9':
                if precut_page.exist(L.precut.precut_window_current_time).AXValue[7] < '5':
                    continue
                check_result = precut_page.edit_precut_single_trim_drag_slider(0, 0, 2, 0)
                break
            case.result = check_result

            precut_page.is_exist(L.precut.precut_play, timeout=15)

        with uuid('ab3bc295-cb37-44e7-9c1e-75b07dd43994') as case:
            # 2.4. Playback panel
            # 2.4.2. Pause
            # Pause preview at current position
            precut_page.precut_preview_operation('Play')
            while precut_page.exist(L.precut.precut_window_current_time).AXValue[7] < '9':
                if precut_page.exist(L.precut.precut_window_current_time).AXValue[7] < '5':
                    continue
                check_result_1 = precut_page.precut_preview_operation('Pause')
                check_result_2 = precut_page.is_exist(L.precut.precut_play, timeout=5)
                break
            case.result = check_result_1 and check_result_2

        with uuid('ac8204f4-11df-4fa4-b740-e98669268082') as case:
            # 2.4. Playback panel
            # 2.4.3. Stop > Original mode
            # Stop preview
            precut_page.precut_preview_operation('Play')
            while precut_page.exist(L.precut.precut_window_current_time).AXValue[7] < '9':
                if precut_page.exist(L.precut.precut_window_current_time).AXValue[7] < '7':
                    continue
                check_result_1 = precut_page.precut_preview_operation('Stop')
                check_result_2 = precut_page.is_exist(L.precut.precut_play, timeout=5)
                break
            case.result = check_result_1 and check_result_2

        with uuid('2620b12e-3314-4e6d-b98c-0df2b97ee0a1') as case:
            # 2.4. Playback panel
            # 2.4.3. Stop > Original mode
            # Indicator would be moved to the beginning of clip
            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_4_3-1.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_4_3-1.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('3b826e2d-bcbe-46c1-bc68-451945509dec') as case:
            # 2.4. Playback panel
            # 2.4.1. Play > output mode
            # Playback trimmed video from mark in to mark out
            precut_page.edit_precut_switch_trim_mode(mode='Multi')
            precut_page.drag_multi_trim_slider(0, 0, 1, 0)
            precut_page.tap_multi_trim_mark_in()
            precut_page.drag_multi_trim_slider(0, 0, 9, 0)
            precut_page.tap_multi_trim_mark_out()
            precut_page.switch_multi_trim_preview_mode(str_mode='Output')
            precut_page.precut_preview_operation('Play')
            check_result_1 = precut_page.is_exist(L.precut.precut_pause, timeout=2)
            start_time = time.time()
            check_result_2 = precut_page.is_exist(L.precut.precut_play, timeout=10)
            end_time = time.time()

            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_4_1-2.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_4_1-2.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result_3 = trim_page.compare(ground_truth, current_preview)

            duration_time = end_time - start_time
            logger(duration_time)
            check_result_4 = False if not duration_time < 9.5 else True

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('6d757c10-4148-4110-9fa0-27650a4f7354') as case:
            # 2.4. Playback panel
            # 2.4.3. Stop > output mode
            # Stop preview
            precut_page.precut_preview_operation('Play')
            while precut_page.exist(L.precut.precut_window_current_time).AXValue[7] < '9':
                if precut_page.exist(L.precut.precut_window_current_time).AXValue[7] < '5':
                    continue
                check_result_1 = precut_page.precut_preview_operation('Stop')
                check_result_2 = precut_page.is_exist(L.precut.precut_play, timeout=5)
                break
            case.result = check_result_1 and check_result_2

        with uuid('0d2a294e-5dcd-41fd-8a98-bb6d5cea6513') as case:
            # 2.4. Playback panel
            # 2.4.3. Stop > output mode
            # Indicator would be moved to the mark in position
            image_full_path = Auto_Ground_Truth_Folder + 'trim_video_2_4_3-2.png'
            ground_truth = Ground_Truth_Folder + 'trim_video_2_4_3-2.png'
            current_preview = trim_page.snapshot(locator=L.precut.multi_trim_slider, file_name=image_full_path)
            check_result = trim_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('2f007de2-4d18-4f58-869a-62ca5a675c97') as case:
            # 2.4. Playback panel
            # 2.4.4. Previous frame
            # Move indicator to the previous frame
            precut_page.set_precut_timecode('00_00_05_00')
            for number_of_clicks in range(10):
                precut_page.precut_preview_operation('Previous_Frame')
                time.sleep(DELAY_TIME * 0.2)
            current_timecode =  precut_page.get_precut_preview_timecode()
            check_result_1 = False if not current_timecode == '00;00;04;20' else True

            check_result_2 = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_4_4-1.png', area='designer window')
            case.result = check_result_1 and check_result_2

        with uuid('384bb88f-442d-48af-92ad-a218c8829059') as case:
            # 2.4. Playback panel
            # 2.4.4. Previous frame
            # Preview update accordingly
            case.result = check_result_2

        with uuid('f8d90d03-909a-43c9-9e0d-7ffeffbf7a25') as case:
            # 2.4. Playback panel
            # 2.4.5. Next frame
            # Move indicator to the next frame
            precut_page.set_precut_timecode('00_00_05_00')
            for number_of_clicks in range(10):
                precut_page.precut_preview_operation('Next_Frame')
                time.sleep(DELAY_TIME * 2)
            current_timecode = precut_page.get_precut_preview_timecode()
            check_result_1 = False if not current_timecode == '00;00;05;10' else True

            check_result_2 = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_4_5-1.png', area='designer window')
            case.result = check_result_1 and check_result_2

        with uuid('efe97650-f8fe-4437-839f-4b81f675adc9') as case:
            # 2.4. Playback panel
            # 2.4.5. Next frame
            # Preview update accordingly
            case.result = check_result_2

        with uuid('6a4f3ecd-7cf8-47ed-a437-ccdf92de0093') as case:
            # 2.4. Playback panel
            # 2.4.7. Current time
            # Base on slider position to show current time correctly
            precut_page.drag_multi_trim_slider(0, 0, 4, 10)
            current_timecode = precut_page.get_precut_preview_timecode()
            check_result = False if not current_timecode == '00;00;04;10' else True
            case.result = check_result

        with uuid('5d87181e-0154-48e7-902a-f935dba97e9b') as case:
            # 2.4. Playback panel
            # 2.4.7. Current time
            # Seek frame by inputing timecode directly then preview would be updated accordingly
            precut_page.set_precut_timecode('00_00_07_20')
            check_result = precut_page.check_precut_preview(
                Ground_Truth_Folder + 'trim_video_2_4_7-1.png', area='designer window')
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        main_page.insert_media('Skateboard 02.mp4')
        tips_area_page.click_TipsArea_btn_Trim(type='video')
        trim_page.exist(L.trim.main_window, timeout=5)
        with uuid('bc9349b8-6436-42fe-a619-e1da47b5fb57') as case:
            # 2.5. Final Confirmation
            # 2.5.2. Cancel > Single Trim
            # Close trim window and trim result is not applied
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 1, 0)
            precut_page.tap_single_trim_mark_in()
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 9, 0)
            precut_page.tap_single_trim_mark_out()
            check_result_1 = precut_page.click_cancel()
            precut_page.handle_save_change_before_leaving(option=1)  # 0: cancel, 1: No, 2: Yes

            tips_area_page.click_TipsArea_btn_Trim(type='video')
            trim_page.exist(L.trim.main_window, timeout=5)
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result_2 = False if not current_duration == '00;00;10;00' else True
            case.result = check_result_1 and check_result_2

        with uuid('d6aad6d2-9069-443e-a330-443163df741e') as case:
            # 2.5. Final Confirmation
            # 2.5.1. OK > Single Trim
            # Close trim window and trim result is correct in timeline preview
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 1, 0)
            precut_page.tap_single_trim_mark_in()
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 3, 0)
            precut_page.tap_single_trim_mark_out()
            check_result_1 = precut_page.click_ok()

            tips_area_page.click_TipsArea_btn_Trim(type='video')
            trim_page.exist(L.trim.main_window, timeout=5)
            current_duration = precut_page.get_precut_single_trim_duration()
            check_result_2 = False if not current_duration == '00;00;02;00' else True
            case.result = check_result_1 and check_result_2

        with uuid('8a10a404-35c0-4f21-963f-cf9118525a3f') as case:
            # 2.5. Final Confirmation
            # 2.5.2. Cancel > Multi Trim
            # Close trim window and trim result is not applied
            precut_page.edit_precut_switch_trim_mode('Multi')
            precut_page.drag_multi_trim_slider(0, 0, 5, 0)
            precut_page.tap_multi_trim_mark_in()
            precut_page.drag_multi_trim_slider(0, 0, 7, 0)
            precut_page.tap_multi_trim_mark_out()
            check_result_1 = precut_page.click_cancel()
            precut_page.handle_save_change_before_leaving(option=1)  # 0: cancel, 1: No, 2: Yes

            clips_amount = timeline_operation_page.get_clips_amount(track_index=0, sleep_time=10)
            check_result_2 = False if not clips_amount == 1 else True
            case.result = check_result_1 and check_result_2

            main_page.enter_room(0)

        with uuid('42aef28f-78d6-40fd-a0a3-73c278fb8195') as case:
            # 2.5. Final Confirmation
            # 2.5.1. OK > Multi Trim
            # Close trim window and trim result is correct in timeline preview
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            tips_area_page.click_TipsArea_btn_Trim(type='video')
            trim_page.exist(L.trim.main_window, timeout=5)
            precut_page.edit_precut_switch_trim_mode('Multi')
            precut_page.drag_multi_trim_slider(0, 0, 5, 0)
            precut_page.tap_multi_trim_mark_in()
            precut_page.drag_multi_trim_slider(0, 0, 7, 0)
            precut_page.tap_multi_trim_mark_out()
            check_result_1 = precut_page.click_ok()
            clips_amount = timeline_operation_page.get_clips_amount(track_index=0, sleep_time=10)
            check_result_2 = False if not clips_amount == 2 else True
            case.result = check_result_1 and check_result_2

        with uuid('0f8cbf35-d0b8-4cf4-aa8e-d7332d302594') as case:
            # 2.5. Final Confirmation
            # 2.5.3. Back to Library
            # In the precut folder after complete
            case.result = None  # trim video does not save in precut folder

        with uuid('cccfcce8-b8eb-492c-94e2-a60457f4510b') as case:
            # 2.5. Final Confirmation
            # 2.5.3. Back to Library > Up One Level
            # Leave precut folder if Up One Level
            case.result = None  # trim video does not save in precut folder

        with uuid('969da594-3381-40ae-86e9-58a73195c74d') as case:
            # 2.5. Final Confirmation
            # 2.5.3. Back to Library > Precut folder
            # Show folder icon on source thumbnail
            case.result = None  # trim video does not save in precut folder

        with uuid('bb485c0c-125e-4afe-b862-6a0f897b39db') as case:
            # 2.5. Final Confirmation
            # 2.5.3. Back to Library > Precut folder
            # Able to enter the precut folder again
            case.result = None  # trim video does not save in precut folder


    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    c15bb34b-4036-4289-81f6-d5594bf8f940
                    b1959a21-2dc3-4e83-bdeb-ba0dd81f34b3
                    a42767a5-2486-42a5-a096-ff50ba1f768c
                    1c45c09a-5c54-457b-9cdb-9aa1abceb45a
                    efa629ee-8d3f-49ca-8c54-1d3edc48f1e8
                    b48b921f-1b6e-41e2-a47f-531a5ab81de4
                    0d42cb14-c862-4091-aec0-2d5c5bf8d358
                    3fb390b2-a232-4b8f-9d11-5b61c569935f
                    080a592c-fdad-4ad9-aa5a-5995008cf532
                    ef2ba665-151d-4638-8ec7-ded34aa1420f
                    d7f47f86-701a-46b9-8592-1c3467498b55
                    4d39921b-e4c3-47ea-8312-52dafe7e0119
                    af639c4b-e19a-4ce0-8009-741bc275ea53
                    2df8243f-f81a-4efb-b422-4e8cc0df8e8e
                    a4b32837-5dd8-4338-8e8b-638de03d9354
                    073e84b4-4c49-4d6d-acf0-5fe501900810
                    f5f99cf8-830e-4915-95e8-1447dbd9e802
                    9b39974d-81ca-446b-8cc6-65a95a5822b5
                    727240b8-1dbb-4151-91d8-1ba60cd44a9d
                    f1c9ceec-67f1-427d-b7b4-03015dd9b935
                    8e797fd2-f63f-42d9-ad33-b218061a5d48
                    e618fa8f-a7b6-4f47-9776-9a9d9c961a30
                    0f8cbf35-d0b8-4cf4-aa8e-d7332d302594
                    cccfcce8-b8eb-492c-94e2-a60457f4510b
                    969da594-3381-40ae-86e9-58a73195c74d
                    bb485c0c-125e-4afe-b862-6a0f897b39db
                    e586355c-d964-4e29-8c84-008b9d94889b
                    3cef17b5-9d30-4a77-a670-51291de1aa78
                    79b765be-8225-4c7a-b2b8-848a2fa93503
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'



