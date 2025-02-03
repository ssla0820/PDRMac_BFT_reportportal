import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
mac = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mac)
base_page = PageFactory().get_page_object('base_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page', mac)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mac)
playback_window_page = PageFactory().get_page_object('playback_window_page', mac)
precut_page = PageFactory().get_page_object('precut_page', mac)
tips_area_page = PageFactory().get_page_object('tips_area_page', mac)
library_preview_page = PageFactory().get_page_object('library_preview_page', mac)

# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Ripple editing.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
#Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/GroundTruth/Pre_Cut/'
#Auto_Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/ATGroundTruth/Pre_Cut/'
#Test_Material_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/'
Ground_Truth_Folder = app.ground_truth_root + '/Ripple_editing/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Ripple_editing/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Ripple_editing():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME*4)
        yield mac
        main_page.close_app()

    @classmethod
    def setup_class(cls):
        main_page.clear_cache()
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('Ripple_editing')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"Ripple editing result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        with uuid("944bf615-b5cb-42b6-b287-01f9b9732c74") as case:
            # [F7] Video & Video Object overwrite beginning

            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            timeline_operation_page.drag_single_media_move_to(0,0,35)
            time.sleep(5)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            time.sleep(3)
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track(option=0)
            time.sleep(3)
            main_page.select_timeline_media('Skateboard 01.mp4')
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos != '00;00;10;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_1_1.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_1_1_1.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("aa5b8d2d-0245-4dcd-a0ce-31939ba14f31") as case:
            # [F9] Video & Video Object insert beginning

            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Skateboard 01.mp4')
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;10;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_1_2.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_1_1_2.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("53e3fdea-d178-4c13-8de0-5e3503dd7f31") as case:
            # [F11] Video & Video Object insert beginning and move all

            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Skateboard 02.mp4')

        with uuid("9c47c151-815d-4564-aabc-119c8de6901d") as case:
            # [F13] Video & Video All timeline clips move to later correctly
            main_page.select_timeline_media('Skateboard 01.mp4')
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;10;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_1_3.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_1_1_3.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("051506e5-f36c-4e5b-96cc-b4a9ea652c29") as case:
            # [F14] Video & Video Crossfade transition appears at the beginning overlap region

            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=3)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            case.result = timeline_operation_page.exist_transition_effect(track_index=0,clip_index=1)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid("d51dc590-387c-4715-bd06-eb4d9057bfe1") as case:
            # [F16] Video & Video Object overwrite middle
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_00_05_00")
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Skateboard 01.mp4')
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;05;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_2_1.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_1_2_1.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("1cbc3c16-af74-46d5-903c-96d21bc8c376") as case:
            # [F18] Video & Video Object insert middle

            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Skateboard 01.mp4', index=1)
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;05;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_2_2.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_1_2_2.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("ca186d81-cf7a-4d70-af1f-583597fa6859") as case:
            # [F20] Video & Video Object insert middle

            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Skateboard 02.mp4')

        with uuid("a5a2fde7-e1ca-49dd-a574-a701881b3c37") as case:
            # [F22] Video & Video Object insert middle and all timeline clips move to later correctly
            main_page.select_timeline_media('Skateboard 01.mp4', index=1)
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;05;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_2_3.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_1_2_3.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid("4633e632-f9bf-405f-b047-0f4cd83dd284") as case:
            # [F24] Video & Video Object overwrite ending
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_00_09_00")
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Skateboard 01.mp4')
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;09;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_3_1.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_1_3_1.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("bde732fb-b89c-4e96-b083-c8e0d250220f") as case:
            # [F26] Video & Video Object insert ending

            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Skateboard 01.mp4',index=1)
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;01;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_3_2.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_1_3_2.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("ade3f9ca-391f-4171-a413-02a3b4495f73") as case:
            # [F28] Video & Video Object insert ending

            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Skateboard 02.mp4')

        with uuid("0cc44bbf-7016-4402-a675-6778ece9862b") as case:
            # [F30] Video & Video Object insert ending and all timeline clips move to later correctly
            main_page.select_timeline_media('Skateboard 01.mp4', index=1)
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;01;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_3_3.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_1_3_3.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("8abb16fb-d896-460f-97ee-ac012ccac9c2") as case:
            # [F31] Video & Video Crossfade transition appears at the ending overlap region

            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=3)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            case.result = timeline_operation_page.exist_transition_effect(track_index=0,clip_index=1)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid("28ddd471-00b6-457c-b421-69e792f533e4") as case:
            # [F33] Video & Video Object overwrite 2 clips middle area
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_00_10_00")
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            main_page.set_timeline_timecode("00_00_05_00")
            time.sleep(3)
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Skateboard 01.mp4')
            playback_window_page.context.click_edit_trim()
            check_in_pos1 = precut_page.get_precut_single_trim_duration()
            if check_in_pos1 == '00;00;05;00':
                check_in_pos1 = True
            else:
                check_in_pos1 = False
            main_page.press_esc_key()
            main_page.select_timeline_media('Skateboard 02.mp4')
            playback_window_page.context.click_edit_trim()
            check_in_pos2 = precut_page.get_precut_single_trim_duration()
            if check_in_pos2 == '00;00;05;00':
                check_in_pos2 = True
            else:
                check_in_pos2 = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_4_1.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_1_4_1.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos1 and check_in_pos2 and compare_result

        with uuid("b37cea5f-c8a2-4b76-a2b1-d556598bd757") as case:
            # [F35] Video & Video Object invert 2 clips middle area

            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            time.sleep(3)
            main_page.select_timeline_media('Skateboard 01.mp4', index=1)
            playback_window_page.context.click_edit_trim()
            check_in_pos1 = precut_page.get_precut_single_trim_duration()
            if check_in_pos1 == '00;00;05;00':
                check_in_pos1 = True
            else:
                check_in_pos1 = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_4_2.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_1_4_2.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos1 and compare_result

        with uuid("5429899d-c71d-4818-8a34-edb2455a5d5e") as case:
            # [F37] Video & Video Object invert 2 clips middle area

            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Skateboard 03.mp4')

        with uuid("8710ecd0-a29c-4660-b0b0-b23849126fc8") as case:
            # [F39] Video & Video Object invert and move all 2 clips middle area
            main_page.select_timeline_media('Skateboard 01.mp4',index=1)
            playback_window_page.context.click_edit_trim()
            check_in_pos1 = precut_page.get_precut_single_trim_duration()
            if check_in_pos1 == '00;00;05;00':
                check_in_pos1 = True
            else:
                check_in_pos1 = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_4_3.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_1_4_3.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos1 and compare_result

    """ #function cancel
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_15(self):
        with uuid("4cf2afb8-04f5-4a46-a65b-1c171a1ebb7d") as case:
            # [F40] Video & Video Object invert 2 clips middle area
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_00_10_00")
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            main_page.set_timeline_timecode("00_00_05_00")
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=3)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            check_transition1 = timeline_operation_page.exist_transition_effect(track_index=0,clip_index=0)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            check_transition2 = timeline_operation_page.exist_transition_effect(track_index=0,clip_index=2)
            case.result = check_transition1 and check_transition2"
        """

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_2_1(self):
        with uuid("bbd1c9ea-009f-42b8-942d-7d9b36b35d09") as case:
            # [F43] Photo & Video Object overwrite beginning

            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            timeline_operation_page.drag_single_media_move_to(0,0,35)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Food.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue != '00;00;05;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("b3486ca9-6b42-47b9-876e-82e02eebf639") as case:
            # [F45] Photo & Video Object insert beginning
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Food.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;05;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("d9a960c1-aa19-41e4-a478-54bc1e040369") as case:
            # [F47] Photo & Video Object insert beginning and move all
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Skateboard 02.mp4')

        with uuid("6872433b-470f-4f70-bccc-4811a14efc37") as case:
            # [F49] Photo & Video All timeline clips move to later correctly
            main_page.select_timeline_media('Food.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;05;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("d8924c0d-1dc0-4eb1-9937-83e3a22e0530") as case:
            # [F50] Photo & Video Crossfade transition appears at the beginning overlap region
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=3)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            case.result = timeline_operation_page.exist_transition_effect(track_index=0,clip_index=1)


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_2_2(self):
        with uuid("47c9e400-9d29-4451-9cda-6533d6cfc7ab") as case:
            # [F52] Photo & Video Object overwrite middle
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_00_02_00")
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Food.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;02;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("0e0e0525-0045-4de5-9c0e-3cadde7351d5") as case:
            # [F55] Photo & Video Object insert middle
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Food.jpg', index=1)
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;03;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("251c231a-3516-4551-80ed-09db97d89342") as case:
            # [F57] Photo & Video Object insert middle
            main_page.press_esc_key()
            time.sleep(3)
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Skateboard 02.mp4')

        with uuid("9e027c5e-1534-452c-9bfb-10cf7e3c959c") as case:
            # [F59] Photo & Video Object insert middle and all timeline clips move to later correctly
            main_page.select_timeline_media('Food.jpg', index=1)
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;03;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_2_3(self):
        with uuid("ed5773f5-440c-43c3-b2c7-66e620109944") as case:
            # [F61] Photo & Video Object overwrite ending
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_00_04_00")
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Food.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;04;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("db09485e-08cc-44f1-b9a1-816467e9772f") as case:
            # [F63] Photo & Video Object insert ending
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Food.jpg', index=1)
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;01;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("45827959-a9e9-4625-b445-521aca160928") as case:
            # [F65] Photo & Video Object insert ending
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Skateboard 02.mp4')

        with uuid("522417f1-7cc3-4aa7-b8af-ff87de41cca9") as case:
            # [F67] Photo & Video Object insert ending and all timeline clips move to later correctly
            main_page.select_timeline_media('Food.jpg', index=1)
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;01;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("999dd54b-92bc-4a88-ab3c-a426dee3da1a") as case:
            # [F68] Photo & Video Crossfade transition appears at the ending overlap region
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=3)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            case.result = timeline_operation_page.exist_transition_effect(track_index=0, clip_index=1)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_2_4(self):
        with uuid("caaef813-5b1c-4c4d-b95e-2d9f2ac6bff4") as case:
            # [F70] Photo & Video Object overwrite 2 clips middle area
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_00_05_00")
            main_page.select_library_icon_view_media('Landscape 01.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            timeline_operation_page.drag_single_media_move_to(0, 1, 24)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            main_page.set_timeline_timecode("00_00_02_00")
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Food.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            check = main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue
            main_page.press_esc_key()
            if check == '00;00;02;00':
                check_in_pos1 = True
            else:
                check_in_pos1 = False

            main_page.select_timeline_media('Landscape 01.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue != '00;00;05;00':
                check_in_pos2 = True
            else:
                check_in_pos2 = False
            case.result = check_in_pos1 and check_in_pos2

        with uuid("72125754-c0ac-4891-a4b8-14c0aad9a855") as case:
            # [F72] Photo & Video Object invert 2 clips middle area
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Food.jpg',index=1)
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;03;00':
                check_in_pos1 = True
            else:
                check_in_pos1 = False
            main_page.press_esc_key()
            main_page.select_timeline_media('Landscape 01.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;05;00':
                check_in_pos2 = True
            else:
                check_in_pos2 = False
            case.result = check_in_pos1 and check_in_pos2

        with uuid("6b655bc0-1d94-484f-9897-401a092c9ede") as case:
            # [F74] Photo & Video Object invert 2 clips middle area
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.set_timeline_timecode("00_00_02_00")
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Skateboard 03.mp4')

        with uuid("ce6e1c86-2e0b-46f1-9e49-650f6bfc3708") as case:
            # [F76] Photo & Video Object invert and move all 2 clips middle area
            main_page.select_timeline_media('Food.jpg', index=1)
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;03;00':
                check_in_pos1 = True
            else:
                check_in_pos1 = False
            main_page.press_esc_key()
            main_page.select_timeline_media('Landscape 01.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;05;00':
                check_in_pos2 = True
            else:
                check_in_pos2 = False
            case.result = check_in_pos1 and check_in_pos2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_3_1(self):
        with uuid("bcbd4517-64d1-425c-8b44-6d152dc35113") as case:
            # [F80] Audio & Video Object overwrite beginning

            main_page.select_library_icon_view_media('Mahoroba.mp3')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Mahoroba.mp3')
            playback_window_page.context.click_edit_trim()
            main_page.press_enter_key()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;02;09;11':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("6fa10a15-ef00-4353-94f4-079845140ba5") as case:
            # [F82] Audio & Video Object insert beginning and move all
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Mahoroba.mp3')
            playback_window_page.context.click_edit_trim()
            main_page.press_enter_key()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;02;19;11':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("f655eda8-146f-447c-922a-4b0525ee449e") as case:
            # [F84] Audio & Video Object insert beginning and move all
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Mahoroba.mp3')

        with uuid("7856ca6c-5f29-4a33-a800-25f7e0e1a6e6") as case:
            # [F86] Audio & Video All timeline clips move to later correctly
            main_page.select_timeline_media('Mahoroba.mp3')
            playback_window_page.context.click_edit_trim()
            main_page.press_enter_key()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;02;19;11':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_3_2(self):
        with uuid("7527fc8c-8707-4a42-ab08-de65b00b6afd") as case:
            # [F88] Audio & Video Object overwrite middle
            main_page.select_library_icon_view_media('Mahoroba.mp3')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_01_00_00", False)
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Mahoroba.mp3')
            playback_window_page.context.click_edit_trim()
            main_page.press_enter_key()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;01;00;02':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("b2b98d8d-8160-4ed2-bd40-74b9c88a33ec") as case:
            # [F90] Audio & Video Object insert middle
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Mahoroba.mp3', index=1)
            playback_window_page.context.click_edit_trim()
            main_page.press_enter_key()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;01;19;09':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("a2519de5-a574-4292-8afb-432501cba595") as case:
            # [F92] Audio & Video Object insert middle
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Skateboard 02.mp4')

        with uuid("7af896dd-cf66-40f7-b5d5-390693a8dab8") as case:
            # [F94] Audio & Video Object insert middle and all timeline clips move to later correctly
            main_page.select_timeline_media('Mahoroba.mp3', index=1)
            playback_window_page.context.click_edit_trim()
            main_page.press_enter_key()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;01;19;09':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_3_3(self):
        with uuid("2ec6eb03-ec66-4f3e-8ce2-ed7a851658b1") as case:
            # [F96] Audio & Video Object overwrite ending
            main_page.select_library_icon_view_media('Mahoroba.mp3')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_02_10_00", False)
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Mahoroba.mp3')
            playback_window_page.context.click_edit_trim()
            main_page.press_enter_key()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;02;10;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("f24476fc-e1af-41b1-bc25-5e7c90470eb7") as case:
            # [F98] Audio & Video Object insert ending
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Mahoroba.mp3', index=1)
            playback_window_page.context.click_edit_trim()
            main_page.press_enter_key()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;09;11':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("1f68b187-4cff-4b95-aad9-17ff08a3f194") as case:
            # [F100] Audio & Video Object insert ending & move all
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Skateboard 02.mp4')

        with uuid("75d43c38-2fa5-431e-8419-86fb72764a6e") as case:
            # [F102] Audio & Video Object insert ending and all timeline clips move to later correctly
            main_page.select_timeline_media('Mahoroba.mp3', index=1)
            playback_window_page.context.click_edit_trim()
            main_page.press_enter_key()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;09;11':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_3_4(self):
        with uuid("4f76c558-3a56-4097-97c2-dcebe8ce16ea") as case:
            # [F104] Audio & Video Object overwrite 2 clips middle area
            main_page.select_library_icon_view_media('Mahoroba.mp3')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_02_19_11", False)
            main_page.select_library_icon_view_media('Mahoroba.mp3')
            time.sleep(3)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            main_page.select_timeline_media('Mahoroba.mp3')

            main_page.set_timeline_timecode("00_02_10_00", False)
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Mahoroba.mp3')
            playback_window_page.context.click_edit_trim()
            main_page.press_enter_key()
            check_in_pos1 = precut_page.get_precut_single_trim_duration()
            if check_in_pos1 == '00;02;10;00':
                check_in_pos1 = True
            else:
                check_in_pos1 = False
            main_page.press_esc_key()
            case.result = check_in_pos1

        with uuid("9909a6bb-29cd-4524-a70a-7b6a424ca85a") as case:
            # [F106] Audio & Video Object invert 2 clips middle area
            time.sleep(3)
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Mahoroba.mp3', index=1)
            playback_window_page.context.click_edit_trim()
            main_page.press_enter_key()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;09;11':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("e931bc40-dcdd-4a94-85ac-7eec78b50bca") as case:
            # [F108] Audio & Video Object invert 2 clips middle area & move all
            time.sleep(3)
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Skateboard 02.mp4')

        with uuid("81300bb4-3adb-47ee-a4bf-234169ed4864") as case:
            # [F110] Audio & Video Object invert and move all 2 clips middle area
            time.sleep(3)
            main_page.select_timeline_media('Mahoroba.mp3', index=1)
            playback_window_page.context.click_edit_trim()
            main_page.press_enter_key()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;09;11':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_4_1(self):
        with uuid("04f0a83e-0e74-4679-bbab-36762302ad03") as case:
            # [F113] Photo & Photo Object overwrite beginning
            main_page.select_library_icon_view_media('Sport 01.jpg')
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track()
            timeline_operation_page.drag_single_media_move_to(0, 0, 17)
            time.sleep(5)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            time.sleep(3)
            main_page.select_library_icon_view_media('Sport 02.jpg')
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Sport 01.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue != '00;00;05;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("6b47c897-4385-45bb-a426-c60be0ff3fb6") as case:
            # [F115] Photo & Photo Object insert beginning
            time.sleep(3)
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            time.sleep(3)
            main_page.select_timeline_media('Sport 01.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;05;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("be8a9e77-1fb2-426d-aabe-7e41aa4380a5") as case:
            # [F117] Photo & Photo Object insert beginning and move all
            time.sleep(3)
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Sport 02.jpg')

        with uuid("63ffce0f-a5bd-4323-96a5-96c43cac2431") as case:
            # [F119] Photo & Photo All timeline clips move to later correctly
            time.sleep(3)
            main_page.select_timeline_media('Sport 01.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;05;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("e89ad45a-c8cd-4f7c-afdf-ccb914d62c86") as case:
            # [F120] Photo & Photo crossfade beginning
            main_page.press_esc_key()
            main_page.click_undo()
            time.sleep(3)
            main_page.select_library_icon_view_media('Sport 02.jpg')
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track(option=3)
            time.sleep(3)
            case.result = timeline_operation_page.exist_transition_effect(track_index=0, clip_index=1)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_4_2(self):
        with uuid("9e038802-0e0b-430b-8b3f-71b4adbf02c8") as case:
            # [F122] Photo & Photo Object overwrite middle

            main_page.select_library_icon_view_media('Sport 01.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_00_02_00")
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Sport 01.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;02;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("baf37250-dbf6-4d06-b3d7-c5c600c3f596") as case:
            # [F124] Photo & Photo Object insert middle
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Sport 01.jpg',index=1)
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;03;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("dfe1808c-b886-4e5c-b7e6-04e195dbf594") as case:
            # [F126] Photo & Photo Object insert middle and move all
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track(option=2)
            time.sleep(3)
            case.result = main_page.select_timeline_media('Sport 02.jpg')

        with uuid("0f52a630-84f2-4000-81bb-4f2d3d9890f1") as case:
            # [F128] Photo & Photo All timeline clips move to later correctly
            main_page.select_timeline_media('Sport 01.jpg', index=1)
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;03;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        """with uuid("e89ad45a-c8cd-4f7c-afdf-ccb914d62c86") as case:
            # [F129] Photo & Photo crossfade middle
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=3)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            case.result = timeline_operation_page.exist_transition_effect(track_index=0, clip_index=1)"""

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_4_3(self):
        with uuid("a1d358e7-a435-431c-9ec5-3551688a8532") as case:
            # [F130] Photo & Photo Object overwrite ending
            main_page.select_library_icon_view_media('Sport 01.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_00_04_00", False)
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Sport 01.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;04;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("7f9628e3-f0b7-4555-ae43-171934ea5884") as case:
            # [F132] Photo & Photo Object insert ending
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Sport 01.jpg', index=1)
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;01;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("ab6a91f3-23ae-42f9-9760-b1430b1f24e1") as case:
            # [F134] Photo & Photo Object insert ending and move all
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track(option=2)
            time.sleep(3)
            case.result = main_page.select_timeline_media('Sport 02.jpg')

        with uuid("cf37910c-a3fc-4803-a9c8-c30ef0b905c6") as case:
            # [F136] Photo & Photo All timeline clips move to later correctly
            main_page.select_timeline_media('Sport 01.jpg', index=1)
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;01;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("495d293a-d3c2-4bb2-a2c8-14e0b41d84d1") as case:
            # [F137] Photo & Photo crossfade ending
            main_page.press_esc_key()
            main_page.click_undo()
            time.sleep(3)
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=3)
            time.sleep(3)
            case.result = timeline_operation_page.exist_transition_effect(track_index=0, clip_index=1)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_4_4(self):
        with uuid("b351b0f6-b50a-42d3-a896-596b1b15f4aa") as case:
            # [F139] Photo & Photo Object overwrite 2 clips middle area

            main_page.select_library_icon_view_media('Sport 01.jpg')
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_00_05_00", False)
            time.sleep(3)
            main_page.select_library_icon_view_media('Sport 02.jpg')
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track()
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            time.sleep(3)
            main_page.set_timeline_timecode("00_00_04_00", False)
            time.sleep(3)
            main_page.select_library_icon_view_media('Sport 02.jpg')
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Sport 01.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;04;00':
                check_in_pos1 = True
            else:
                check_in_pos1 = False
            main_page.press_esc_key()
            main_page.select_timeline_media('Sport 02.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;01;00':
                check_in_pos2 = True
            else:
                check_in_pos2 = False
            case.result = check_in_pos1 and check_in_pos2

        with uuid("2b713d1f-3998-4a67-8233-3598cea68c87") as case:
            # [F141] Photo & Photo Object insert 2 clips middle area
            time.sleep(3)
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Sport 01.jpg', index=1)
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;01;00':
                check_in_pos1 = True
            else:
                check_in_pos1 = False
            main_page.press_esc_key()
            main_page.select_timeline_media('Sport 02.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;05;00':
                check_in_pos2 = True
            else:
                check_in_pos2 = False
            case.result = check_in_pos1 and check_in_pos2

        with uuid("a15d86d4-af53-49b2-8585-fc749ddf449c") as case:
            # [F143] Photo & Photo Object insert 2 clips middle area and move all
            time.sleep(3)
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            time.sleep(3)
            case.result = main_page.select_timeline_media('Sport 02.jpg')

        with uuid("7b58b350-7fa1-4185-aa79-1c38d2a236b4") as case:
            # [F145] Photo & Photo All timeline clips move to later correctly
            time.sleep(3)
            main_page.select_timeline_media('Sport 01.jpg', index=1)
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;01;00':
                check_in_pos1 = True
            else:
                check_in_pos1 = False
            main_page.press_esc_key()
            main_page.select_timeline_media('Sport 02.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;05;00':
                check_in_pos2 = True
            else:
                check_in_pos2 = False
            case.result = check_in_pos1 and check_in_pos2

    """
            with uuid("ed3b47b2-9741-4a4d-b2d8-121255ee7da8") as case:
                # [F146] Photo & Photo crossfade 2 clips middle area
                main_page.press_esc_key()
                main_page.click_undo()
                main_page.select_library_icon_view_media('Sport 02.jpg')
                main_page.tips_area_insert_media_to_selected_track(option=3)
                case.result = timeline_operation_page.exist_transition_effect(track_index=0, clip_index=1)
    """

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_5_1(self):
        with uuid("e3e2815d-c939-4996-a24a-39626a5df1aa") as case:
            # [F149] Video & Photo Object overwrite beginning

            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            timeline_operation_page.drag_single_media_move_to(0, 0, 17)
            time.sleep(5)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            time.sleep(3)
            main_page.select_library_icon_view_media('Sport 02.jpg')
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Skateboard 01.mp4')
            if playback_window_page.context.click_edit_trim() == False:
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_1_1.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_5_1_1.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("0470e524-6bea-4710-bc85-ff151db93230") as case:
            # [F151] Video & Photo Object insert beginning
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Skateboard 01.mp4')
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;10;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_1_2.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_5_1_2.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("36bb1804-b96a-4e95-ab13-5853089903cc") as case:
            # [F153] Video & Photo Object insert beginning and move all
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Sport 02.jpg')

        with uuid("a140e9de-a91a-407f-8d82-9dd84a66bbf2") as case:
            # [F155] Video & Photo All timeline clips move to later correctly
            main_page.select_timeline_media('Skateboard 01.mp4')
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;10;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_1_3.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_5_1_3.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("574fad4f-d747-4d28-8747-ad0276753897") as case:
            # [F156] Video & Photo crossfade beginning
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track(option=3)
            case.result = timeline_operation_page.exist_transition_effect(track_index=0, clip_index=1)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_5_2(self):
        with uuid("d30d8c50-a120-4993-8d78-ef4cc4da6558") as case:
            # [F158] Video & Photo Object overwrite middle

            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_00_03_00")
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Skateboard 01.mp4', index=1)
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;02;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_2_1.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_5_2_1.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("3c2610bd-6764-4681-8629-4b084c5d94b8") as case:
            # [F160] Video & Photo Object insert middle
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Skateboard 01.mp4', index=1)
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;07;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_2_2.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_5_2_2.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("366d2e9a-6ede-4a28-84bf-f1e12e3f8bd2") as case:
            # [F162] Video & Photo Object insert middle and move all
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Sport 02.jpg')

        with uuid("f7bfe9a1-db5c-41ce-8541-7c04010435a7") as case:
            # [F164] Video & Photo All timeline clips move to later correctly
            main_page.select_timeline_media('Skateboard 01.mp4',index=1)
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;07;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_2_3.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_5_2_3.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_5_3(self):
        with uuid("86caa65f-a8b9-49aa-8104-2368b53fa383") as case:
            # [F166] Video & Photo Object overwrite ending

            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_00_09_00")
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Sport 02.jpg')
            if playback_window_page.context.click_edit_trim() == False:
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_3_1.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_5_3_1.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("1e830de9-c771-4e99-adb6-62438244ecee") as case:
            # [F168] Video & Photo Object insert ending
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track(option=1)
            time.sleep(3)
            main_page.select_timeline_media('Skateboard 01.mp4', index=1)
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;01;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_3_2.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_5_3_2.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("61e61441-c1a2-4925-b6dd-f20faeb7b0ba") as case:
            # [F170] Video & Photo Object insert ending and move all
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Sport 02.jpg')

        with uuid("e77fd7c3-df8a-4774-b8a8-35cef0ba9530") as case:
            # [F172] Video & Photo All timeline clips move to later correctly
            main_page.select_timeline_media('Skateboard 01.mp4',index=1)
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;01;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_3_3.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_5_3_3.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("d93b39dd-e16a-4101-868c-ee76c0445a82") as case:
            # [F173] Video & Photo crossfade ending
            main_page.click_undo()
            time.sleep(3)
            main_page.select_library_icon_view_media('Sport 02.jpg')
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track(option=3)
            time.sleep(3)
            case.result = timeline_operation_page.exist_transition_effect(track_index=0, clip_index=1)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_5_4(self):
        with uuid("006bba2f-7af9-457e-be46-375c566cc09d") as case:
            # [F175] Video & Photo Object overwrite 2 clips' middle area
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.set_timeline_timecode("00_00_10_00")
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            main_page.set_timeline_timecode("00_00_09_00")
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            main_page.select_timeline_media('Skateboard 02.mp4')
            if playback_window_page.context.click_edit_trim() == False:
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_4_1.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_5_4_1.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("727a9262-6619-44e0-b9ee-458d812e3dc5") as case:
            # [F177] Video & Photo Object insert 2 clips' middle area
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Skateboard 01.mp4', index=1)
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;01;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_4_2.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_5_4_2.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("68423288-00c0-44cf-babf-2bf333140341") as case:
            # [F179] Video & Photo Object insert ending and move all
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            case.result = main_page.select_timeline_media('Sport 02.jpg')

        with uuid("a1e592e7-2b33-4aa6-89c0-d3de35c228fb") as case:
            # [F181] Video & Photo All timeline clips move to later correctly
            main_page.select_timeline_media('Skateboard 01.mp4',index=1)
            playback_window_page.context.click_edit_trim()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            if check_in_pos == '00;00;01;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_4_3.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_5_4_3.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        """with uuid("1c6ef461-9d54-4d23-af11-8da5cbf533f5") as case:
            # [F182] Video & Photo crossfade 2 clips' middle area
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=3)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            case.result = timeline_operation_page.exist_transition_effect(track_index=0, clip_index=1)"""

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_6_1(self):
        with uuid("38459957-2387-4509-967c-8cfd7024f6b1") as case:
            # [F185] Multiselect Library clips and drag to timeline overwrite
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            media_room_page.library_menu_select_all()
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track(option=0)
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_6_1_1.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_6_1_1.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = compare_result

        with uuid("7e1544e8-0fd4-498b-959a-ca2a940fdcbe") as case:
            # [F186] Multiselect Library clips and drag to timeline insert
            main_page.click_undo()
            media_room_page.library_menu_select_all()
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Skateboard 01.mp4', index=1)
            main_page.press_space_key()
            main_page.press_space_key()
            if playback_window_page.get_timecode_slidebar() != '00;00;00;00':
                case.result = True
            else:
                case.result = False

        with uuid("95247599-337c-49aa-a192-55f7ad68766a") as case:
            # [F187] Multiselect Library clips and drag to timeline insert and move all
            main_page.click_undo()
            media_room_page.library_menu_select_all()
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track(option=2)
            main_page.select_timeline_media('Skateboard 01.mp4', index=1)
            main_page.press_space_key()
            main_page.press_space_key()
            if playback_window_page.get_timecode_slidebar() != '00;00;00;00':
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_6_2(self):
        with uuid("5dd1f2bf-e508-4288-86af-c110af7c0032") as case:
            # [F188] Drag timeline clip's edge to trim only
            main_page.select_library_icon_view_media('Sport 01.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            time.sleep(3)
            timeline_operation_page.trim_enlarge_drag_clip_edge(0,10)
            main_page.select_timeline_media('Sport 01.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue != '00;00;05;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("8a5658e3-038e-4da7-a3a2-536aade15e48") as case:
            # [F189] Drag timeline clip's edge to trim and move clips
            main_page.press_esc_key()
            main_page.click_undo()
            main_page.set_timeline_timecode("00_00_05_00")
            main_page.select_library_icon_view_media('Sport 02.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            timeline_operation_page.trim_enlarge_drag_clip_edge(0, 10, index=1)
            main_page.select_timeline_media('Sport 01.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue != '00;00;05;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            main_page.select_timeline_media('Sport 02.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;05;00':
                check_in_pos1 = True
            else:
                check_in_pos1 = False
            case.result = check_in_pos and check_in_pos1

        with uuid("75487ffc-24c7-4a75-9896-d3f6ea2cf950") as case:
            # [F190] Drag timeline clip's edge to trim and move all
            main_page.press_esc_key()
            main_page.click_undo()
            timeline_operation_page.trim_enlarge_drag_clip_edge(0, 10, index=2)
            main_page.select_timeline_media('Sport 01.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue != '00;00;05;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            main_page.select_timeline_media('Sport 02.jpg')
            tips_area_page.click_TipsArea_btn_Duration()
            if main_page.exist(locator=L.main.duration_setting_dialog.txt_duration).AXValue == '00;00;05;00':
                check_in_pos1 = True
            else:
                check_in_pos1 = False
            case.result = check_in_pos and check_in_pos1

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_6_3(self):
        with uuid("5ea5706d-788c-4499-8580-54d480c546ed") as case:
            # [F191] Cut and Leave Gap
            main_page.select_library_icon_view_media('Sport 02.jpg')
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track()
            time.sleep(3)
            main_page.select_library_icon_view_media('Sport 01.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Sport 01.jpg')
            main_page.tap_cut_and_leave_gap_hotkey()
            time.sleep(3)
            main_page.select_timeline_media('Sport 02.jpg')
            main_page.press_space_key()
            main_page.press_space_key()
            if playback_window_page.get_timecode_slidebar() != "00;00;00;00":
                case.result = True
            else:
                case.result = False

        with uuid("d4c832c6-fec5-44e5-b343-3573cc5d4875") as case:
            # [F192] Cut and Fill Gap
            main_page.click_undo()
            main_page.select_timeline_media('Sport 01.jpg')
            main_page.tap_cut_and_fill_gap_hotkey()
            main_page.select_timeline_media('Sport 02.jpg')
            main_page.press_space_key()
            main_page.press_space_key()
            if playback_window_page.get_timecode_slidebar() != "00;00;05;00":
                case.result = True
            else:
                case.result = False

        with uuid("5aa8727a-4dcb-41ad-9fc2-d427abb53fe8") as case:
            # [F193] Cut and Fill Gap and move all clips
            main_page.click_undo()
            main_page.select_timeline_media('Sport 01.jpg')
            main_page.tap_cut_fill_gap_and_move_all_clips_hotkey()
            main_page.select_timeline_media('Sport 02.jpg')
            main_page.press_space_key()
            main_page.press_space_key()
            if playback_window_page.get_timecode_slidebar() != "00;00;05;00":
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_6_4(self):
        with uuid("bc7ac75b-5d42-473b-8ed3-3270d10eee54") as case:
            # [F194] Paste & overwrite
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.tap_Copy_hotkey()
            timeline_operation_page.drag_single_media_move_to(0, 0, 25)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            main_page.set_timeline_timecode("00_00_03_00")
            main_page.tap_Paste_hotkey()
            main_page.select_right_click_menu('Overwrite                          	  ⌃+Drop')
            main_page.select_timeline_media('Skateboard 01.mp4', index=1)
            playback_window_page.context.click_edit_trim()
            time.sleep(2)
            check_in_pos = precut_page.get_precut_single_trim_duration()
            time.sleep(2)
            if check_in_pos != '00;00;10;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_6_4_1.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_6_4_1.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("679690e5-70a6-4a07-82a0-488b3bc5472d") as case:
            # [F195] Paste and Trim to Fit
            main_page.tap_Undo_hotkey()
            main_page.select_timeline_media('Skateboard 01.mp4')
            time.sleep(2)
            main_page.tap_Copy_hotkey()
            time.sleep(2)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            main_page.set_timeline_timecode("00_00_03_00")
            main_page.tap_Paste_hotkey()
            main_page.select_right_click_menu('Trim to Fit')
            main_page.select_timeline_media('Skateboard 01.mp4', index=0)
            playback_window_page.context.click_edit_trim()
            time.sleep(2)
            check_in_pos = precut_page.get_precut_single_trim_duration()
            time.sleep(2)
            if check_in_pos != '00;00;10;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_6_4_2.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_6_4_2.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("7643cbd5-f227-4d00-adee-73389a304a58") as case:
            # [F196] Paste and Speed up to Fit
            main_page.tap_Undo_hotkey()
            main_page.select_timeline_media('Skateboard 01.mp4')
            main_page.tap_Copy_hotkey()
            time.sleep(2)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            main_page.set_timeline_timecode("00_00_03_00")
            main_page.tap_Paste_hotkey()
            main_page.select_right_click_menu('Speed up to Fit')
            main_page.select_timeline_media('Skateboard 01.mp4', index=0)
            playback_window_page.context.click_edit_trim()
            time.sleep(2)
            main_page.press_enter_key()
            check_in_pos = precut_page.get_precut_single_trim_duration()
            time.sleep(2)
            if check_in_pos == '00;00;10;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_6_4_4.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_6_4_4.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("0117afea-6449-40d2-add9-48213c1b7717") as case:
            # [F197] Paste and Insert
            main_page.tap_Undo_hotkey()
            main_page.select_timeline_media('Skateboard 01.mp4')
            main_page.tap_Copy_hotkey()
            time.sleep(2)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            main_page.set_timeline_timecode("00_00_03_00")
            main_page.tap_Paste_hotkey()
            main_page.select_right_click_menu('Insert')
            main_page.select_timeline_media('Skateboard 01.mp4', index=0)
            playback_window_page.context.click_edit_trim()
            time.sleep(2)
            check_in_pos = precut_page.get_precut_single_trim_duration()
            time.sleep(2)
            if check_in_pos == '00;00;10;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_6_4_4.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_6_4_4.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("20564918-65ff-4d43-bcff-cfa72e30433a") as case:
            # [F198] Paste, Insert, Move All Clips
            main_page.tap_Undo_hotkey()
            main_page.select_timeline_media('Skateboard 01.mp4')
            main_page.tap_Copy_hotkey()
            time.sleep(2)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            main_page.set_timeline_timecode("00_00_03_00")
            main_page.tap_Paste_hotkey()
            main_page.select_right_click_menu('Insert and Move All Clips	  ⇧+Drop')
            main_page.select_timeline_media('Skateboard 01.mp4', index=0)
            playback_window_page.context.click_edit_trim()
            time.sleep(2)
            check_in_pos = precut_page.get_precut_single_trim_duration()
            time.sleep(2)
            if check_in_pos == '00;00;10;00':
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_6_4_5.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_6_4_5.png',
                                               playback_window_snap)
            logger(compare_result)
            case.result = check_in_pos and compare_result

        with uuid("2b783c11-282d-47a6-888e-586db3d70ade") as case:
            # [F199] Paste and Crossfade
            main_page.tap_Undo_hotkey()
            main_page.select_timeline_media('Skateboard 01.mp4')
            main_page.tap_Copy_hotkey()
            time.sleep(2)
            playback_window_page.Edit_Timeline_PreviewOperation("Play")
            playback_window_page.Edit_Timeline_PreviewOperation("Stop")
            main_page.set_timeline_timecode("00_00_03_00")
            main_page.tap_Paste_hotkey()
            main_page.select_right_click_menu('Crossfade                         	  ⌥+Drop')
            case.result = timeline_operation_page.exist_transition_effect(track_index=0, clip_index=1)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_6_5(self):
        with uuid("02a3be6b-011a-423c-b81e-283fdb8bca1f") as case:
            # [F200] Remove and Leave Gap
            main_page.select_library_icon_view_media('Sport 02.jpg')
            time.sleep(3)
            main_page.tips_area_insert_media_to_selected_track()
            time.sleep(3)
            main_page.select_library_icon_view_media('Sport 01.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Sport 01.jpg')
            main_page.tap_remove_and_leave_gap_hotkey()
            time.sleep(3)
            main_page.select_timeline_media('Sport 02.jpg')
            main_page.press_space_key()
            main_page.press_space_key()
            if playback_window_page.get_timecode_slidebar() != "00;00;00;00":
                case.result = True
            else:
                case.result = False

        with uuid("70fb157e-393d-4aae-a435-7c54ee156e3f") as case:
            # [F201] Remove and Fill Gap
            main_page.click_undo()
            main_page.select_timeline_media('Sport 01.jpg')
            main_page.tap_remove_and_fill_gap_hotkey()
            main_page.select_timeline_media('Sport 02.jpg')
            main_page.press_space_key()
            main_page.press_space_key()
            if playback_window_page.get_timecode_slidebar() != "00;00;05;00":
                case.result = True
            else:
                case.result = False

        with uuid("0fb9c451-a4cb-44e9-ab51-599402bb25e6") as case:
            # [F202] Remove and Fill Gap and move all clips
            main_page.click_undo()
            main_page.select_timeline_media('Sport 01.jpg')
            main_page.tap_remove_fill_gap_and_move_all_clips_hotkey()
            main_page.select_timeline_media('Sport 02.jpg')
            main_page.press_space_key()
            main_page.press_space_key()
            if playback_window_page.get_timecode_slidebar() != "00;00;05;00":
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_6_6(self):
        with uuid("5a6c92b0-0870-43c6-8d5b-bfb94124e2e4") as case:
            # [F203] Clips at same track and move on same track
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            timeline_operation_page.drag_multi_media_move_to(0,0,0,1,35)
            main_page.select_timeline_media('Skateboard 01.mp4')
            main_page.press_space_key()
            main_page.press_space_key()
            if playback_window_page.get_timecode_slidebar() != "00;00;00;00":
                case.result = True
            else:
                case.result = False

        with uuid("f7f7cef5-cd53-42e6-abad-4c523e4bdf99") as case:
            # [F204] Clips at same track and move cross to different track
            main_page.tap_Undo_hotkey()
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            if timeline_operation_page.drag_multi_media_move_to_other_track(0,0,0,1,35,1) == True:
                check = True
            else:
                check = False
            main_page.select_timeline_media('Skateboard 01.mp4')
            main_page.press_space_key()
            main_page.press_space_key()
            if playback_window_page.get_timecode_slidebar() != "00;00;00;00":
                check2 = True
            else:
                check2 = False
            case.result = check and check2

        with uuid("af5705a5-249e-49d1-971d-b8ba14c48f1e") as case:
            # [F205] Clips at different track and move on same track
            main_page.tap_Undo_hotkey()
            main_page.tap_Undo_hotkey()
            main_page.timeline_select_track(2)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            if timeline_operation_page.drag_multi_media_move_to(0, 0, 2, 0, 35) == True:
                check = True
            else:
                check = False
            main_page.select_timeline_media('Skateboard 01.mp4')
            main_page.press_space_key()
            main_page.press_space_key()
            if playback_window_page.get_timecode_slidebar() != "00;00;00;00":
                check2 = True
            else:
                check2 = False
            case.result = check and check2

        with uuid("4ad4552e-8515-4104-862a-ec270cf84e36") as case:
            # [F206] Clips at different track and move cross to differnt track
            main_page.tap_Undo_hotkey()
            main_page.tap_Undo_hotkey()
            main_page.timeline_select_track(2)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            if timeline_operation_page.drag_multi_media_move_to_other_track(0, 0, 2, 0, 35, 1) == True:
                check = True
            else:
                check = False
            main_page.select_timeline_media('Skateboard 01.mp4')
            main_page.press_space_key()
            main_page.press_space_key()
            if playback_window_page.get_timecode_slidebar() != "00;00;00;00":
                check2 = True
            else:
                check2 = False
            case.result = check and check2

