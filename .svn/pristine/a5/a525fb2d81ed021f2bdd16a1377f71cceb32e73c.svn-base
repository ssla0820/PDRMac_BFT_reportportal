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

import getpass
home_name = getpass.getuser()

# read PDR cap >>
app = SimpleNamespace(**PDR_cap)
# read PDR cap <<

# create driver & page >>
mac = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page', mac)
title_room_page = PageFactory().get_page_object('title_room_page', mac)
preferences_page = PageFactory().get_page_object('preferences_page', mac)
tips_area_page = PageFactory().get_page_object('tips_area_page', mac)
timeline_page = PageFactory().get_page_object('timeline_operation_page', mac)
playback_window_page = PageFactory().get_page_object('playback_window_page', mac)
library_preview_page = PageFactory().get_page_object('library_preview_page', mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Preferences_part2.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Preferences_part2/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Preferences_part2/'
Test_Material_Folder = app.testing_material

# Test for SVN update

#Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/GroundTruth/Preferences_part2/'
#Auto_Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/ATGroundTruth/Preferences_part2/'
#Test_Material_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/'
#Ground_Truth_Folder = '/Users/cl/Desktop/MacPDR_SVN_Run/SFT/GroundTruth/Preferences_part2/'
#Auto_Ground_Truth_Folder = '/Users/cl/Desktop/MacPDR_SVN_Run/SFT/ATGroundTruth/Preferences_part2/'
#Test_Material_Folder = '/Users/cl/Desktop/MacPDR_SVN_Run/Material/'

DELAY_TIME = 1

class Test_Preference_part2():
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
            google_sheet_execution_log_init('Preferences_part2')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"Preferences Part2 result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
    def enter_editing_page(self):
        main_page.click_set_user_preferences()
        time.sleep(DELAY_TIME)
        preferences_page.switch_to_editing()
        time.sleep(DELAY_TIME)

    # @pytest.mark.skip
    @exception_screenshot
    def enter_file_page(self):
        main_page.click_set_user_preferences()
        time.sleep(DELAY_TIME)
        preferences_page.switch_to_file()
        time.sleep(DELAY_TIME)

    # @pytest.mark.skip
    @exception_screenshot
    def enter_display_page(self):
        main_page.click_set_user_preferences()
        time.sleep(DELAY_TIME)
        preferences_page.switch_to_display()
        time.sleep(DELAY_TIME)

    # @pytest.mark.skip
    @exception_screenshot
    def enter_project_page(self):
        main_page.click_set_user_preferences()
        time.sleep(DELAY_TIME)
        preferences_page.switch_to_project()
        time.sleep(DELAY_TIME)

    # @pytest.mark.skip
    @exception_screenshot
    def enter_DZ_page(self):
        main_page.click_set_user_preferences()
        time.sleep(DELAY_TIME)
        preferences_page.switch_to_director_zone()
        time.sleep(DELAY_TIME)

    # @pytest.mark.skip
    @exception_screenshot
    def enter_CL_page(self):
        main_page.click_set_user_preferences()
        time.sleep(DELAY_TIME)
        preferences_page.switch_to_cyberlink_cloud()
        time.sleep(DELAY_TIME)

    # @pytest.mark.skip
    @exception_screenshot
    def import_4k_video_to_media(self):
        time.sleep(DELAY_TIME)
        four_k_path = Test_Material_Folder+'Preferences_Part2/4K HEVC 59.940 Broadcast Capture Sample.mkv'
        media_room_page.import_media_file(four_k_path)


    # @pytest.mark.skip
    @exception_screenshot
    def inter_one_video_to_timeline(self):
        time.sleep(DELAY_TIME)
        # Insert Skateboard 01.mp4
        main_page.select_library_icon_view_media('Skateboard 01.mp4')
        media_room_page.library_clip_context_menu_insert_on_selected_track()

    # @pytest.mark.skip
    @exception_screenshot
    def inter_one_image_to_timeline(self):
        time.sleep(DELAY_TIME)
        # Insert Skateboard 01.mp4
        main_page.select_library_icon_view_media('Landscape 02.jpg')
        media_room_page.library_clip_context_menu_insert_on_selected_track()

    # @pytest.mark.skip
    @exception_screenshot
    def inter_two_clip_to_timeline(self):
        self.inter_one_video_to_timeline()

        time.sleep(DELAY_TIME)
        # Insert Skateboard 03.mp4
        main_page.select_library_icon_view_media('Skateboard 03.mp4')
        main_page.tips_area_insert_media_to_selected_track(2)
        time.sleep(DELAY_TIME)


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        with uuid("5eaae77f-46b0-47f4-a27e-3a8053f423f6") as case:
            # [I87] Set default transition behavior > Cross
            self.enter_editing_page()
            preferences_page.editing.set_default_transition_behavior_apply_cross()
            check_result = preferences_page.editing.get_default_transition_behavior()
            if check_result != 'Cross':
                logger('Page function cannot apply successfully')
                case.result = False
                return

            # Close Preferences setting
            preferences_page.click_ok()

            # Insert sample clips
            self.inter_two_clip_to_timeline()

            # enter transition room > drag transition to timeline
            main_page.enter_room(2)
            timeline_page.drag_media_to_timeline_overlay_clip('Blackout', clip_index=1, index=-1)

            # check timeline result
            tips_area_page.click_TipsArea_btn_Modify(type='Transition', close_win=False)

            current_image = preferences_page.snapshot(locator=L.media_room.library_frame, file_name=Auto_Ground_Truth_Folder + 'I87.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'I87.png', current_image, similarity=0.99)
            case.result = compare_result

        with uuid("f6862ccc-bdd9-47d7-9c3a-8bb764eb7885") as case:
            # Undo ( Remove Blackout transition)
            time.sleep(DELAY_TIME)
            preferences_page.tap_Undo_hotkey()

            # [I86] Set default transition behavior > Overlap
            self.enter_editing_page()
            preferences_page.editing.set_default_transition_behavior_apply_overlap()
            check_result = preferences_page.editing.get_default_transition_behavior()
            if check_result != 'Overlap':
                logger('Page function cannot apply successfully')
                case.result = False
                return

            # Close Preferences setting
            preferences_page.click_ok()

            timeline_page.drag_media_to_timeline_overlay_clip('Blackout', clip_index=1, index=-1)

            # check timeline result
            tips_area_page.click_TipsArea_btn_Modify(type='Transition', close_win=False)

            current_image = preferences_page.snapshot(locator=L.media_room.library_frame, file_name=Auto_Ground_Truth_Folder + 'I86.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'I86.png', current_image, similarity=0.99)
            case.result = compare_result

        with uuid("9bd7bf6e-49f6-4468-b297-a7c1ad1ab19f") as case:
            # Undo ( Only insert Skateboard 01.mp4 video to timeline)
            time.sleep(DELAY_TIME)
            for x in range(2):
                preferences_page.tap_Undo_hotkey()

            # [I94] Return to clip/movie beginning after preview > Uncheck
            self.enter_editing_page()
            preferences_page.editing.return_to_beginnings_of_video_after_preview_set_check(is_check=0)
            # Close Preferences setting
            preferences_page.click_ok()

            # check timeline preview after play
            preferences_page.press_space_key()
            time.sleep(DELAY_TIME*11)

            current_image = preferences_page.snapshot(locator=preferences_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'I94.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'I94.png', current_image)
            case.result = compare_result

        with uuid("afa76b47-eaf1-49b6-9de6-da87ead6b58a") as case:
            # Click "Stop" button
            preferences_page.tap_Stop_hotkey()
            time.sleep(DELAY_TIME)

            # [I93] Return to clip/movie beginning after preview > Check (default)
            self.enter_editing_page()
            preferences_page.editing.return_to_beginnings_of_video_after_preview_set_check(is_check=1)
            # Close Preferences setting
            preferences_page.click_ok()

            # check timeline preview after play
            preferences_page.press_space_key()
            time.sleep(DELAY_TIME*11)

            current_image = preferences_page.snapshot(locator=preferences_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'I93.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'I93.png', current_image)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid("af5e2241-6271-4cc6-b2be-b71b2e886217") as case:
            with uuid("59592611-08a1-4def-9c30-d6ef5924dd76") as case:
                def get_timeline_track_seq():
                    track1_x, track1_y = preferences_page.exist(L.timeline_operation.timeline_video_track1).AXPosition
                    track3_x, track3_y = preferences_page.exist(L.timeline_operation.timeline_video_track3).AXPosition
                    return track1_y, track3_y

                # [I101] Track 1 at top
                track1_y, track3_y = get_timeline_track_seq()
                #logger(track1_y)
                #logger(track3_y)
                if track3_y < track1_y:
                    logger('Default setting is invalid.')
                    default_status = False
                else:
                    default_status = True

                # [I102] Reverse timeline track order (track 1 at bottom) > Track 1 at bottom
                self.enter_editing_page()
                preferences_page.editing.reverse_timeline_track_order_set_check(1)
                # Close Preferences setting
                preferences_page.click_ok()

                track1_y, track3_y = get_timeline_track_seq()
                if track3_y < track1_y:
                    tick_status = True
                else:
                    tick_status = False

                self.enter_editing_page()
                preferences_page.editing.reverse_timeline_track_order_set_check(0)
                # Close Preferences setting
                preferences_page.click_ok()

                track1_y, track3_y = get_timeline_track_seq()
                if track3_y < track1_y:
                    untick_status = False
                else:
                    untick_status = True

                case.result = untick_status and default_status
            case.result = tick_status

        with uuid("be46313f-7625-4d2d-8313-e011aa27646d") as case:
            # [I106] Image file duration > Value > 5 sec. (default)
            self.enter_editing_page()
            initial_value = preferences_page.editing.durations_image_files_get_value()
            # Close Preferences setting
            preferences_page.click_ok()

            if initial_value != '5.0':
                initial_result = False
            else:
                initial_result = True

            # check insert image to timeline > default duration
            main_page.select_library_icon_view_media('Food.jpg')
            media_room_page.library_clip_context_menu_insert_on_selected_track()

            time.sleep(DELAY_TIME)
            playback_window_page.set_timecode_slidebar('00_00_05_00')
            result = playback_window_page.Edit_Timeline_PreviewOperation('Next_Frame')
            #logger(result)
            time.sleep(DELAY_TIME)
            timeline_value = playback_window_page.get_timecode_slidebar()
            logger(timeline_value)

            if timeline_value != '00;00;05;00':
                timeline_result = False
            else:
                timeline_result = True
            case.result = initial_result and timeline_result

        with uuid("95488bb0-1395-4305-97f3-a9522dc6a625") as case:
            preferences_page.tap_Undo_hotkey()

            # [I107] Image file duration > Value > 0.2 sec. (min)
            with uuid("269be5db-ec75-4637-bb06-c79578137794") as case:
                # [I110] Adjustment > Input
                self.enter_editing_page()
                preferences_page.editing.durations_image_files_set_value('0.0')
                # Close Preferences setting
                preferences_page.click_ok()

                self.enter_editing_page()
                current = preferences_page.editing.durations_image_files_get_value()
                if current == '0.2':
                    case.result = True
                else:
                    case.result = False
            if current == '0.2':
                case.result = True
            else:
                case.result = False

        with uuid("6ecbb79c-3015-445a-a071-3dc73f0a1dd1") as case:
            # [I109] Click Arrow up/Down button
            preferences_page.editing.durations_image_files_set_value('5.7')
            time.sleep(DELAY_TIME)
            preferences_page.editing.durations_image_files_set_arrow_button(times=3)
            current = preferences_page.editing.durations_image_files_get_value()
            if current == '6.0':
                check_input_box_value = True
            else:
                check_input_box_value = False

            # Close Preferences setting
            preferences_page.editing.return_to_beginnings_of_video_after_preview_set_check(is_check=0)
            preferences_page.click_ok()

            # check insert image to timeline > default duration
            main_page.select_library_icon_view_media('Sport 01.jpg')
            media_room_page.library_clip_context_menu_insert_on_selected_track()

            # check timeline preview after play
            preferences_page.press_space_key()
            time.sleep(DELAY_TIME*7)

            timecode_value = playback_window_page.get_timecode_slidebar()
            #logger(timecode_value)

            if timecode_value == '00;00;06;00':
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid("129e7945-f51a-4680-9d0a-18b011fd5f6b") as case:
            # [I111] Title duration > Value > 10 sec. (default)
            self.enter_editing_page()
            initial_value = preferences_page.editing.durations_title_get_value()
            # Close Preferences setting
            preferences_page.click_ok()

            if initial_value != '10.0':
                initial_result = False
            else:
                initial_result = True

            # check insert title to timeline > default duration
            main_page.enter_room(1)
            time.sleep(DELAY_TIME)
            main_page.select_library_icon_view_media('Clover_04')
            title_room_page.select_RightClickMenu_AddToTimeline()

            time.sleep(DELAY_TIME)
            playback_window_page.set_timecode_slidebar('00_00_10_00')
            result = playback_window_page.Edit_Timeline_PreviewOperation('Next_Frame')
            #logger(result)
            time.sleep(DELAY_TIME)
            timeline_value = playback_window_page.get_timecode_slidebar()
            logger(timeline_value)

            if timeline_value != '00;00;10;00':
                timeline_result = False
            else:
                timeline_result = True
            case.result = initial_result and timeline_result

        with uuid("855f2ab9-9963-4d9c-bf82-6e40e48f171c") as case:
            preferences_page.tap_Undo_hotkey()

            # [I112] Title duration > Value > 0.2 sec. (min)
            with uuid("32ecc86e-e499-4a90-a291-7da805b76aa2") as case:
                # [I115] Adjustment > Input
                self.enter_editing_page()
                preferences_page.editing.durations_title_set_value('0.1')
                # Close Preferences setting
                preferences_page.click_ok()

                self.enter_editing_page()
                current = preferences_page.editing.durations_title_get_value()
                if current == '0.2':
                    case.result = True
                else:
                    case.result = False
            if current == '0.2':
                case.result = True
            else:
                case.result = False

        with uuid("5eb5e563-5cfe-4eff-8526-89c966832686") as case:
            # [I114] Click Arrow up/Down button
            preferences_page.editing.durations_title_set_value('7.4')
            time.sleep(DELAY_TIME)
            preferences_page.editing.durations_title_set_arrow_button(direction='down', times=4)
            current = preferences_page.editing.durations_image_files_get_value()
            if current == '7.0':
                check_input_box_value = True
            else:
                check_input_box_value = False

            # Close Preferences setting
            preferences_page.editing.return_to_beginnings_of_video_after_preview_set_check(is_check=0)
            preferences_page.click_ok()

            # check insert title to timeline > check duration
            main_page.select_library_icon_view_media('Clover_03')
            title_room_page.select_RightClickMenu_AddToTimeline()

            # check timeline preview after play
            preferences_page.press_space_key()
            time.sleep(DELAY_TIME*9)

            timecode_value = playback_window_page.get_timecode_slidebar()
            #logger(timecode_value)

            if timecode_value == '00;00;07;00':
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid("9782ad91-4bb8-4cd6-a8f4-d92999360894") as case:
            # [I116] Transition duration > Value > 2sec. (default)
            self.enter_editing_page()
            initial_value = preferences_page.editing.durations_transitions_get_value()
            # Close Preferences setting
            preferences_page.click_ok()

            if initial_value != '2.0':
                initial_result = False
            else:
                initial_result = True

            # check insert transition to timeline > default duration
            self.inter_one_video_to_timeline()
            main_page.enter_room(2)
            time.sleep(DELAY_TIME)
            timeline_page.drag_media_to_timeline_overlay_clip('Arrow 2', clip_index=0, index=-1)

            # check Timeline Preview at (00;00;01;00)
            playback_window_page.set_timecode_slidebar('00_00_01_00')
            time.sleep(DELAY_TIME)
            current_image = preferences_page.snapshot(locator=preferences_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'I116.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'I116.png', current_image)
            logger(current_image)
            playback_window_page.set_timecode_slidebar('00_00_02_00')
            playback_window_page.Edit_Timeline_PreviewOperation('Next_Frame')
            time.sleep(DELAY_TIME)
            timeline_value = playback_window_page.get_timecode_slidebar()
            logger(timeline_value)

            if timeline_value != '00;00;02;00':
                timecode_result = False
            else:
                timecode_result = True

            logger(initial_result)
            logger(compare_result)
            logger(timecode_result)
            case.result = initial_result and compare_result and timecode_result

        with uuid("afd8868e-5a79-4ef1-a8d9-15ce7c3146ac") as case:
            preferences_page.tap_Undo_hotkey()

            # [I117] Transition duration > Value > 0.2 sec. (min)
            with uuid("bb39781c-110b-4249-9850-b76b72993506") as case:
                # [I120] Adjustment > Input
                self.enter_editing_page()
                preferences_page.editing.durations_transitions_set_value('0.1')
                # Close Preferences setting
                preferences_page.click_ok()

                self.enter_editing_page()
                current = preferences_page.editing.durations_transitions_get_value()
                if current == '0.2':
                    case.result = True
                else:
                    case.result = False

            preferences_page.editing.durations_transitions_set_value('1.0')
            preferences_page.click_ok()

            self.enter_editing_page()
            current = preferences_page.editing.durations_transitions_get_value()
            # Close Preferences setting
            preferences_page.click_ok()

            if current == '1.0':
                case.result = True
            else:
                case.result = False

        with uuid("98f8a2a2-95c9-472e-8d1b-3c80050e5144") as case:
            # [I119] Click Arrow up/Down button
            self.enter_editing_page()
            preferences_page.editing.durations_transitions_set_arrow_button(times=15)
            # Close Preferences setting
            preferences_page.click_ok()
            timeline_page.drag_media_to_timeline_overlay_clip('Binary 2', clip_index=0, index=-1)

            # check Timeline Preview at (00;00;01;00)
            playback_window_page.set_timecode_slidebar('00_00_01_00')
            time.sleep(DELAY_TIME)
            current_image = preferences_page.snapshot(locator=preferences_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'I119.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'I119.png', current_image)

            playback_window_page.set_timecode_slidebar('00_00_02_15')
            playback_window_page.Edit_Timeline_PreviewOperation('Next_Frame')
            time.sleep(DELAY_TIME)
            timeline_value = playback_window_page.get_timecode_slidebar()
            #logger(timeline_value)

            if timeline_value != '00;00;02;15':
                timecode_result = False
            else:
                timecode_result = True

            case.result = compare_result and timecode_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid("77066ac8-212a-46a4-a688-aaca5bdee7af") as case:

            self.inter_one_video_to_timeline()

            # [I121] Effect duration > Value > 10sec. (default)
            self.enter_editing_page()

            initial_value = preferences_page.editing.durations_effect_get_value()
            # Close Preferences setting
            preferences_page.click_ok()

            if initial_value != '10.0':
                initial_result = False
            else:
                initial_result = True

            main_page.enter_room(3)
            time.sleep(DELAY_TIME)
            main_page.select_library_icon_view_media('Chinese Painting')
            tips_area_page.click_TipsArea_btn_add_to_effect_track()

            # check Timeline Preview at (00;00;01;00)
            playback_window_page.set_timecode_slidebar('00_00_10_00')
            time.sleep(DELAY_TIME)
            current_image = preferences_page.snapshot(locator=preferences_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'I121.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'I121.png', current_image)

            #logger(initial_result)
            #logger(compare_result)
            case.result = initial_result and compare_result

        with uuid("7958557b-674c-4d30-ac48-45d5ebf453bb") as case:
            preferences_page.tap_Undo_hotkey()

            # [I122] Effect duration > Value > 0.2 sec. (min)
            with uuid("4d2ec587-c524-4e82-b6e5-6c3a3bec48d2") as case:
                # [I125] Adjustment > Input
                self.enter_editing_page()
                preferences_page.editing.durations_effect_set_value('0.1')
                # Close Preferences setting
                preferences_page.click_ok()

                self.enter_editing_page()
                current = preferences_page.editing.durations_effect_get_value()
                if current == '0.2':
                    case.result = True
                else:
                    case.result = False

            preferences_page.editing.durations_effect_set_value('4.0')
            preferences_page.click_ok()

            self.enter_editing_page()
            current = preferences_page.editing.durations_effect_get_value()
            # Close Preferences setting
            preferences_page.click_ok()

            if current == '4.0':
                case.result = True
            else:
                case.result = False

        with uuid("cf89a819-c8a6-4123-8814-6871eaa93bcf") as case:
            # [I124] Click Arrow up/Down button

            self.enter_editing_page()
            preferences_page.editing.durations_effect_set_arrow_button(times=10)
            preferences_page.click_ok()

            time.sleep(DELAY_TIME)
            timeline_page.set_add_tracks_effect(number=1, position='Above track 2')

            main_page.select_library_icon_view_media('Black and White')
            tips_area_page.click_TipsArea_btn_add_to_effect_track()

            playback_window_page.set_timecode_slidebar('00_00_07_00')
            time.sleep(DELAY_TIME)
            current_image = preferences_page.snapshot(locator=preferences_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'I124.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'I124.png', current_image)

            timeline_value = playback_window_page.get_timecode_slidebar()
            logger(timeline_value)

            if timeline_value == '00;00;05;00':
                check_timecode = True
            else:
                check_timecode = False

            case.result = compare_result and check_timecode

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid("ed0343d7-69cc-4c3a-a4a7-8b0352d3e001") as case:
            #[E135] Default path
            self.enter_file_page()
            check_default = preferences_page.file.default_locations_import_folder_get_path()
            #logger(check_default)
            if check_default == f'/Users/{home_name}/Desktop':
                case.result = True
            else:
                case.result = False
            logger(home_name)

        with uuid("b8ef4d60-fd42-4ad2-a4c9-6320eb26a78c") as case:
            #[E136] Open [Browse for Folder] window and user can select target folder
            # if exception, need Jim to check
            preferences_page.file.default_locations_import_folder_click_browse()
            set_SFT_path = preferences_page.get_project_path('SFT')
            logger(set_SFT_path)
            preferences_page.file.default_locations_import_folder_set_path(set_SFT_path)
            preferences_page.click_ok()

            self.enter_file_page()
            check_default = preferences_page.file.default_locations_import_folder_get_path()
            if check_default == set_SFT_path:
                case.result = True
            else:
                case.result = False
            preferences_page.click_ok()

        with uuid("3ebe87e2-a96b-4614-8a99-b9516adf2456") as case:
            #[E137] Opened location should match as setting when operate import folder
            preferences_page.exist_click(L.media_room.btn_import_media)
            preferences_page.exist_click(L.media_room.import_media.option_import_media_file)
            time.sleep(DELAY_TIME*2)
            check_OCR = preferences_page.search_text_position('GroundTruth', mouse_move=0, order=1)
            print(f'{check_OCR=}')
            preferences_page.press_esc_key()
            if check_OCR is not False:
                case.result = True
            else:
                case.result = False

        with uuid("4e49bb66-db25-49f2-b1ff-afbab506e142") as case:
            #[E138] Opened location should match as setting when operate import file
            media_room_page.import_media_file(Ground_Truth_Folder + 'I93.png')
            time.sleep(DELAY_TIME)

            self.enter_file_page()
            check_default = preferences_page.file.default_locations_import_folder_get_path()
            #logger(check_default)
            #logger(Ground_Truth_Folder)
            time.sleep(DELAY_TIME)
            if Ground_Truth_Folder == check_default+'/':
                case.result = True
            else:
                case.result = False
            preferences_page.click_ok()
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        with uuid("b070e0ec-a413-4de1-a4a0-a8c16b3ece4a") as case:
            #[E1141] Default path
            self.enter_file_page()
            check_default = preferences_page.file.default_locations_export_folder_get_path()
            logger(check_default)
            if check_default == f'/Users/{home_name}/Movies/PowerDirector':
                case.result = True
            else:
                case.result = False

        with uuid("7bf811a8-fc42-4e16-a61f-ded99b41a439") as case:
            #[E1142] Open [Browse for Folder] window and user can select target folder
            preferences_page.file.default_locations_export_folder_click_browse()
            set_SFT_path = preferences_page.get_project_path('SFT')
            #logger(set_SFT_path)
            preferences_page.file.default_locations_export_folder_set_path(set_SFT_path)
            preferences_page.click_ok()

            self.enter_file_page()
            check_default = preferences_page.file.default_locations_export_folder_get_path()
            if check_default == set_SFT_path:
                case.result = True
            else:
                case.result = False
            preferences_page.click_ok()

        with uuid("47846cd1-578e-45c3-a3cb-2abe5ed2b1e6") as case:
            #[E1143] Export folder should match setting at next launch PDR after change.
            main_page.close_and_restart_app()
            time.sleep(DELAY_TIME*4)
            self.enter_file_page()
            check_current = preferences_page.file.default_locations_export_folder_get_path()
            logger(set_SFT_path)
            if check_current == set_SFT_path:
                case.result = True
            else:
                case.result = False

        with uuid("704179bd-f376-4e7c-9d7d-18d9edcf9546") as case:
            #[E1144] File can export to new folder correctly.
            preferences_page.file.default_locations_export_folder_click_browse()
            custom_path = f'/Users/{home_name}/Desktop/Preferences_SFT_test'
            check_result = preferences_page.file.default_locations_export_folder_set_path(custom_path, is_exist=0)
            preferences_page.click_ok()

            self.enter_file_page()
            check_current = preferences_page.file.default_locations_export_folder_get_path()
            if check_current == custom_path:
                check_new_folder = True
            else:
                check_new_folder = False

            case.result = check_result and check_new_folder
            preferences_page.click_ok()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        with uuid("369f1d62-fe66-4ea1-9c72-7b4cf6b71dcc") as case:
            #[I158] file extension should match as setting > > ext = jpg
            self.enter_file_page()
            default_ext = preferences_page.file.filename_snapshot_get_file_format()

            if default_ext == '.jpg':
                case.result = True
            else:
                case.result = False

        with uuid("116ccf53-871d-4e18-861a-c212c8c80487") as case:
            # [I153] File name should match as setting after capture video.
            check_snapshot_folder = preferences_page.file.default_locations_export_folder_get_path()

            default_filename = preferences_page.file.filename_snapshot_get_file_name()
            # logger(default_value)

            if default_filename == 'SnapShot':
                default_naming = True
            else:
                default_naming = False

            preferences_page.click_ok()

            # [Before test Snapshot]
            # check default snapshot path doesn't exist the same file
            # if exist the same file, delete it
            custom_path = f'{check_snapshot_folder}/SnapShot.jpg'
            if preferences_page.exist_file(path=custom_path):
                preferences_page.delete_folder(path=custom_path)

            # take a snapshot
            self.inter_one_video_to_timeline()
            playback_window_page.Edit_TimelinePreview_ClickTakeSnapshot()
            time.sleep(DELAY_TIME*2)
            preferences_page.press_enter_key()
            time.sleep(DELAY_TIME*2)
            # check snapshot file after click (TakeSnapshot)
            snapshot_result = preferences_page.exist_file(path=custom_path)

            case.result = default_naming and snapshot_result

            # [After test snapshot]
            if (preferences_page.exist_file(path=custom_path)) and (case.result is True):
                preferences_page.delete_folder(path=custom_path)

        with uuid("374ef4d6-70e9-4553-a95e-7b8d4b606efe") as case:
            # [I159] file extension should match as setting > ext = gif
            self.enter_file_page()
            preferences_page.file.filename_snapshot_set_file_format(file_ext='gif')
            preferences_page.click_ok()

            # [Before test Snapshot]
            # check default snapshot path doesn't exist the same file
            # if exist the same file, delete it
            custom_path = f'{check_snapshot_folder}/SnapShot.gif'
            if preferences_page.exist_file(path=custom_path):
                preferences_page.delete_folder(path=custom_path)

            # take a snapshot
            playback_window_page.Edit_TimelinePreview_ClickTakeSnapshot()
            time.sleep(DELAY_TIME*2)
            preferences_page.press_enter_key()
            time.sleep(DELAY_TIME*2)
            # check snapshot file after click (TakeSnapshot)
            snapshot_result = preferences_page.exist_file(path=custom_path)

            case.result = default_naming and snapshot_result

            # [After test snapshot]
            if (preferences_page.exist_file(path=custom_path)) and (case.result is True):
                preferences_page.delete_folder(path=custom_path)

        with uuid("c803ede0-9dc6-4d94-bbab-f9fbf4839176") as case:
            # [I160] file extension should match as setting > ext = png

            preferences_page.tap_Undo_hotkey()
            time.sleep(DELAY_TIME)
            media_room_page.enter_color_boards()
            media_room_page.color_board_context_menu_insert_on_selected_track('56,0,71')
            time.sleep(DELAY_TIME)

            self.enter_file_page()
            preferences_page.file.filename_snapshot_set_file_format(file_ext='png')
            preferences_page.click_ok()

            # [Before test Snapshot]
            # check default snapshot path doesn't exist the same file
            # if exist the same file, delete it
            custom_path = f'{check_snapshot_folder}/SnapShot.png'
            if preferences_page.exist_file(path=custom_path):
                preferences_page.delete_folder(path=custom_path)

            # take a snapshot
            playback_window_page.Edit_TimelinePreview_ClickTakeSnapshot()
            time.sleep(DELAY_TIME*2)
            preferences_page.press_enter_key()
            time.sleep(DELAY_TIME*2)
            # check snapshot file after click (TakeSnapshot)
            snapshot_result = preferences_page.exist_file(path=custom_path)

            # back to Media Content category
            media_room_page.enter_media_content()

            case.result = default_naming and snapshot_result

            # [After test snapshot]
            if (preferences_page.exist_file(path=custom_path)) and (case.result is True):
                preferences_page.delete_folder(path=custom_path)

        with uuid("0d87631e-b532-40eb-bb30-f7043ca42857") as case:
            # [I157] file extension should match as setting> ext = bmp
            with uuid("44217f69-3fea-42c9-ae5a-4774254d044e") as case:
                # [I154] File name should match as setting after capture video.

                preferences_page.tap_Undo_hotkey()
                time.sleep(DELAY_TIME)
                media_room_page.enter_color_boards()
                media_room_page.color_board_context_menu_insert_on_selected_track('0,175,255')
                time.sleep(DELAY_TIME)

                self.enter_file_page()
                preferences_page.file.filename_snapshot_set_file_name('SFT_AT')
                time.sleep(DELAY_TIME)
                preferences_page.file.filename_snapshot_set_file_format(file_ext='bmp')
                preferences_page.click_ok()

                # [Before test Snapshot]
                # check default snapshot path doesn't exist the same file
                # if exist the same file, delete it
                custom_path = f'{check_snapshot_folder}/SFT_AT.bmp'
                if preferences_page.exist_file(path=custom_path):
                    preferences_page.delete_folder(path=custom_path)

                # take a snapshot
                playback_window_page.Edit_TimelinePreview_ClickTakeSnapshot()
                time.sleep(DELAY_TIME*2)
                preferences_page.press_enter_key()
                time.sleep(DELAY_TIME*2)
                # check snapshot file after click (TakeSnapshot)
                snapshot_result = preferences_page.exist_file(path=custom_path)

                # back to Media Content category
                media_room_page.enter_media_content()

                case.result = default_naming and snapshot_result

                # [After test snapshot]
                if (preferences_page.exist_file(path=custom_path)) and (case.result is True):
                    preferences_page.delete_folder(path=custom_path)

        with uuid("79e3f358-1d1f-495f-bd45-0ec5875f313e") as case:
            # [I164] snapshot image will be a file and can show in library
            self.enter_file_page()
            check_default = preferences_page.file.filename_snapshot_get_file_destination()
            logger(check_default)
            if check_default == 'File':
                check_destination_result = True
            else:
                check_destination_result = False
            preferences_page.click_ok()

            current_image = preferences_page.snapshot(locator=preferences_page.area.library_icon_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'I164.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'I164.png', current_image, similarity=0.99)
            case.result = check_destination_result and compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        with uuid("b7441ceb-2c8e-4b92-b22a-15c9c5f9b6c8") as case:
            #[I168] Preview Quality > Ultra HD
            self.inter_one_video_to_timeline()
            self.enter_display_page()
            preferences_page.display.timeline_preview_quality_set_value('ultra_hd')
            preferences_page.click_ok()

            check_result = playback_window_page.Edit_TimelinePreview_GetPreviewQuality()
            if check_result == 'Ultra HD Preview Resolution':
                case.result = True
            else:
                case.result = False

        with uuid("de0e8f53-9b07-4d0f-821c-3f019fb05d2a") as case:
            #[I170] Preview Quality > Full HD
            self.enter_display_page()
            preferences_page.display.timeline_preview_quality_set_value('full_hd')
            preferences_page.click_ok()

            check_result = playback_window_page.Edit_TimelinePreview_GetPreviewQuality()
            if check_result == 'Full HD Preview Resolution':
                case.result = True
            else:
                case.result = False

        with uuid("bf23d225-b030-418a-9a63-f5b1e60191e2") as case:
            #[I174] Preview Quality > High
            self.enter_display_page()
            preferences_page.display.timeline_preview_quality_set_value('high')
            preferences_page.click_ok()

            check_result = playback_window_page.Edit_TimelinePreview_GetPreviewQuality()
            if check_result == 'High Preview Resolution':
                case.result = True
            else:
                case.result = False

        with uuid("a85984c2-6556-4ae4-9f90-569af8c9d881") as case:
            #[I176] Preview Quality > Normal
            self.enter_display_page()
            preferences_page.display.timeline_preview_quality_set_value('normal')
            preferences_page.click_ok()

            check_result = playback_window_page.Edit_TimelinePreview_GetPreviewQuality()
            if check_result == 'Normal Preview Resolution':
                case.result = True
            else:
                case.result = False

        with uuid("a4993b75-fa2a-43ee-956d-e4a9843effcb") as case:
            #[I178] Preview Quality > Low
            self.enter_display_page()
            preferences_page.display.timeline_preview_quality_set_value('low')
            preferences_page.click_ok()

            check_result = playback_window_page.Edit_TimelinePreview_GetPreviewQuality()
            if check_result == 'Low Preview Resolution':
                case.result = True
            else:
                case.result = False

        with uuid("38fdd8b8-8152-40c7-9c3c-20b92405d756") as case:
            #[I172] Preview Quality > HD
            self.enter_display_page()
            preferences_page.display.timeline_preview_quality_set_value('hd')
            preferences_page.click_ok()

            check_result = playback_window_page.Edit_TimelinePreview_GetPreviewQuality()
            if check_result == 'HD Preview Resolution':
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_10(self):
        with uuid("978a3b8f-9be1-44a9-846b-51c04b3f7fc3") as case:
            #[I186] Setting shoud keep after settings an re-launch AP
            self.enter_display_page()
            preferences_page.display.grid_lines_set_value(9)
            preferences_page.click_ok()

            main_page.close_and_restart_app()
            time.sleep(DELAY_TIME*4)
            self.enter_display_page()
            check_result = preferences_page.display.grid_lines_get_value()
            logger(check_result)
            if check_result == "9 x 9":
                case.result = True
            else:
                case.result = False
            preferences_page.click_ok()

        with uuid("498f4cfb-b019-46ac-94c1-ff87122682b4") as case:
            #[I187] Grid Line No. show on screen correctly after setting
            self.inter_one_image_to_timeline()

            current_image = preferences_page.snapshot(locator=preferences_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'I172.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'I172.png', current_image, similarity=0.99)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_11(self):
        with uuid("46779f48-1660-4cbb-a7a8-a4c7ce3d6467") as case:
            # [I197] Load the last project automatically when open PDR
            self.enter_project_page()
            preferences_page.project.auto_load_the_last_project_set_check(is_check=True)
            preferences_page.click_ok()

            # open project
            main_page.top_menu_bar_file_open_project()
            #/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/Preferences_Part2/Preferences_part2_a.pds
            project_path = Test_Material_Folder+'Preferences_Part2/Preferences_part2_a.pds'
            main_page.handle_open_project_dialog(project_path)
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')

            main_page.close_and_restart_app()
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')
            time.sleep(DELAY_TIME*4)

            current_image = preferences_page.snapshot(locator=preferences_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'I197.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'I197.png', current_image, similarity=0.99)

            logger(compare_result)
            current_project_name = preferences_page.exist(L.main.top_project_name).AXValue
            if current_project_name == 'Preferences_part2_a':
                check_opened_result = True
            else:
                check_opened_result = False

            case.result = compare_result and check_opened_result

        with uuid("11c5c2d5-9f91-4919-9e2c-133e6302cfe5") as case:
            # [I196]
            self.enter_project_page()
            preferences_page.project.auto_load_the_last_project_set_check(is_check=False)
            preferences_page.click_ok()

            main_page.close_and_restart_app()
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')
            time.sleep(DELAY_TIME*4)

            current_project_name = preferences_page.exist(L.main.top_project_name).AXValue

            if current_project_name == 'New Untitled Project':
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_12(self):
        with uuid("2f14f5f8-4207-4cec-a684-55a95eeaf0a8") as case:
            # [I191] Number of recently used projects > 10 (default)
            self.enter_project_page()
            check_value = preferences_page.project.numbers_of_recently_used_project_get_value()
            time.sleep(DELAY_TIME)
            if check_value == '10':
                check_default_result = True
            else:
                check_default_result = False


            preferences_page.project.numbers_of_recently_used_project_set_value(value=2)
            time.sleep(DELAY_TIME)
            preferences_page.click_ok()

            # open project
            main_page.top_menu_bar_file_open_project()
            #/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/Preferences_Part2/Preferences_part2_a.pds
            project_a = Test_Material_Folder+'Preferences_Part2/Preferences_part2_a.pds'
            main_page.handle_open_project_dialog(project_a)
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')

            # open project
            main_page.top_menu_bar_file_open_project()
            #/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/Preferences_Part2/Preferences_part2_b.pds
            project_b = Test_Material_Folder+'Preferences_Part2/Preferences_part2_b.pds'
            main_page.handle_open_project_dialog(project_b)
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')

            # open project
            main_page.top_menu_bar_file_open_project()
            #/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/Preferences_Part2/Preferences_part2_c.pds
            project_c = Test_Material_Folder+'Preferences_Part2/Preferences_part2_c.pds'
            main_page.handle_open_project_dialog(project_c)
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')

            main_page.top_menu_bar_file_open_recent_projects(full_path=None)

            current_image = preferences_page.snapshot(locator=L.library_preview.upper_view_region,
                                                      file_name=Auto_Ground_Truth_Folder + 'I191.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'I191.png', current_image, similarity=0.99)
            case.result = check_default_result and compare_result

        with uuid("55c06227-2bec-48c9-b1bb-05740fa90d6d") as case:
            # [I192] Number of recently used projects > 0(min)
            preferences_page.right_click()
            self.enter_project_page()

            preferences_page.project.numbers_of_recently_used_project_set_value(value=0)
            time.sleep(DELAY_TIME)
            preferences_page.click_ok()

            # Check (File menu) > (Open Recent Projects) > full_path = project_c  > Cannot open project_c [Verify OK]
            check_result = main_page.top_menu_bar_file_open_recent_projects(full_path=project_c)
            if check_result is False:
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_13(self):
        with uuid("e3245a68-ca2a-44f6-bd3d-e1f9f65582b8") as case:
            # [I198] Automatically load sample clips when PowerDirector opens > Check (default)

            current_image = preferences_page.snapshot(locator=preferences_page.area.library_icon_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'I198.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'I198.png', current_image)

            self.enter_project_page()
            check_value = preferences_page.project.auto_load_sample_clips_checkbox_get_status()
            time.sleep(DELAY_TIME)
            if check_value == 1:
                check_default_result = True
            else:
                check_default_result = False
            logger(check_value)
            logger(check_default_result)
            case.result = compare_result and check_default_result

        with uuid("efc825bf-b715-4ff4-9fd5-127654e6daba") as case:
            # [I199] Automatically load sample clips when PowerDirector opens > Uncheck
            time.sleep(DELAY_TIME)
            preferences_page.project.auto_load_sample_clips_set_check(is_check=0)
            preferences_page.click_ok()

            main_page.close_and_restart_app()
            time.sleep(DELAY_TIME)
            current_image = preferences_page.snapshot(locator=preferences_page.area.library_icon_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'I199.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'I199.png', current_image, similarity=0.99)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_14(self):
        with uuid("ff1c399a-15cb-4ab1-80fb-3e21c129f1d2") as case:
            # [I242] Reset "Don't show again" dialogs

            # Step1: Set (Don't show again)
            # open project
            main_page.top_menu_bar_file_open_project()
            #/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/Preferences_Part2/Preferences_part2_b.pds
            project_b = Test_Material_Folder+'Preferences_Part2/Preferences_part2_b.pds'
            main_page.handle_open_project_dialog(project_b)
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='yes')

            main_page.top_menu_bar_file_open_project()
            project_c = Test_Material_Folder+'Preferences_Part2/Preferences_part2_c.pds'
            main_page.handle_open_project_dialog(project_c)

            time.sleep(DELAY_TIME)
            current_image = preferences_page.snapshot(locator=preferences_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'I242.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'I242.png', current_image, similarity=0.99)

            # Sep2: Reset "Don't show again"
            main_page.click_set_user_preferences()
            time.sleep(DELAY_TIME)
            preferences_page.switch_to_confirmation()
            time.sleep(DELAY_TIME)
            preferences_page.confirmation.click_reset()
            preferences_page.click_ok()

            # Verify
            main_page.top_menu_bar_file_open_project()
            project_a = Test_Material_Folder+'Preferences_Part2/Preferences_part2_a.pds'
            main_page.handle_open_project_dialog(project_a)
            if preferences_page.exist(L.main.merge_media_to_library_dialog.chx_do_not_show_again, DELAY_TIME * 5):
                case.result = True
                main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='yes')
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_15(self):
        with uuid("e72e7718-be52-43b9-99b7-57b23ed8a329") as case:
            # [I248] Hyperlink is disabled under sign out status
            with uuid("3db52fac-0e83-430a-8cdb-3e51f1677ce5") as case:
                # [I245] Remember DZ account and not auto sign-in after re-launch PDR
                self.enter_DZ_page()
                check_default = preferences_page.director_zone.auto_sign_in_checkbox_get_status()
                if check_default == 0:
                    check_default_status = True
                else:
                    check_default_status = False
                #pdrmacat001@gmail.com / qadf1234
                preferences_page.director_zone.input_email('pdrmacat001@gmail.com')
                time.sleep(DELAY_TIME)
                preferences_page.director_zone.input_password('qadf1234')
                time.sleep(DELAY_TIME)
                preferences_page.director_zone.click_sign_in()
                preferences_page.click_ok()

                main_page.close_and_restart_app()
                time.sleep(DELAY_TIME)

                self.enter_DZ_page()
                check_current = preferences_page.director_zone.auto_sign_in_checkbox_get_status()
                if check_current == 0:
                    check_current_stats = True
                else:
                    check_current_stats = False

                logger(check_current)
                check_sign_in_link = preferences_page.director_zone.click_upload_link()
                logger(check_sign_in_link)
                case.result = check_default_status and check_current_stats and (not check_sign_in_link)
                preferences_page.click_ok()
            case.result = not check_sign_in_link

        with uuid("11daf992-6a96-45ae-a76d-26711e642e72") as case:
            # [I244] Remember DZ account after re-launch PDR
            self.enter_DZ_page()
            check_email = preferences_page.director_zone.get_email()
            check_pw = preferences_page.director_zone.get_password()
            logger(check_email)
            logger(check_pw)
            email_result = None
            pw_result = None
            if check_email == 'pdrmacat001@gmail.com':
                email_result = True

            if preferences_page.is_os_version_greater_than_or_equal_to("10.16"):
                # Check for Mac OS 11.x Big Sur
                if check_pw == '':
                    pw_result = True
            else:
                # Check for Mac OS 10.15 Catalina
                if check_pw == '⦁⦁⦁⦁⦁⦁⦁⦁':
                    pw_result = True

            auto_sign_in_click_result = False
            if email_result and pw_result:
                auto_sign_in_click_result = preferences_page.director_zone.auto_sign_in_set_check(is_check=1)
                preferences_page.director_zone.click_sign_in()
            preferences_page.click_ok()

            main_page.close_and_restart_app()
            time.sleep(DELAY_TIME)

            self.enter_DZ_page()
            check_sign_in_link = preferences_page.director_zone.click_upload_link()
            #logger(check_sign_in_link)
            case.result = auto_sign_in_click_result and check_sign_in_link
            
            time.sleep(DELAY_TIME)
            preferences_page.click_ok()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_16(self):
        with uuid("4b53df61-f74b-46d2-b0a6-be9a43f65081") as case:
            # [I260] Open [Browse for Folder] window and user can select target folder
            self.enter_CL_page()
            check_default = preferences_page.cyberlink_cloud.download_folder_get_path()
            logger(check_default)
            #/Users/qadf_at/Movies/CyberLink/CyberLink Drive/PowerDirector
            if check_default == f'/Users/{home_name}/Movies/CyberLink/CyberLink Drive/PowerDirector':
                default_path = True
            else:
                case.default_path = False
            custom_path = Test_Material_Folder+'Preferences_Part2'
            preferences_page.cyberlink_cloud.download_folder_select_folder_by_browse(full_path=custom_path)
            time.sleep(DELAY_TIME)
            preferences_page.click_ok()

            self.enter_CL_page()
            check_current = preferences_page.cyberlink_cloud.download_folder_get_path()
            if check_current == custom_path:
                current_path = True
            else:
                current_path = False

            case.result = default_path and current_path
            preferences_page.click_ok()
            logger(check_current)

        with uuid("438dda85-c57a-4a80-bd9c-635c10fc34fc") as case:
            # [I261] User can input custom path as target folder
            self.enter_CL_page()
            custom_path = f'/Users/{home_name}/Movies/CyberLink/CyberLink Drive'
            current_path = preferences_page.cyberlink_cloud.download_folder_get_path()
            preferences_page.cyberlink_cloud.download_folder_set_path(custom_path)
            time.sleep(DELAY_TIME)
            preferences_page.click_ok()

            self.enter_CL_page()
            after_change_path = preferences_page.cyberlink_cloud.download_folder_get_path()
            if after_change_path == custom_path:
                after_check = True
            else:
                after_check = False

            update_status = False
            if current_path != after_change_path:
                update_status = True

            case.result = after_check and update_status
            preferences_page.click_ok()

        with uuid("e762ce11-a42f-4683-adaa-c08e5a868ebc") as case:
            # [I271] Open the correct web page for Cloud account management.
            self.enter_CL_page()
            check_result = preferences_page.cyberlink_cloud.click_account_info_link()
            time.sleep(DELAY_TIME)
            preferences_page.click_ok()

            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_17(self):
        with uuid("f2887e79-72ac-41fe-b8f3-adc0df98658b") as case:
            # [I49] Render a preview of the timeline in Ultra HD preview quality > Uncheck (default)
            main_page.click_set_user_preferences()
            time.sleep(DELAY_TIME)
            check_default = preferences_page.general.render_preview_in_uhd_preview_quality_is_enabled()
            logger(check_default)
            preferences_page.click_ok()

            case.result = (not check_default)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_20(self):
        with uuid("880e67c8-d224-41ba-97bf-54dd25dbaecb") as case:
            # [I88] Transition type is disabled
            # ToDo
            # test case in v19.3.2529 has a  bug
            # Only handle FAIL situation

            self.enter_editing_page()
            preferences_page.editing.transition_between_photos_set_type()

            # Close Preferences setting
            preferences_page.click_ok()
            self.enter_editing_page()
            check_result = preferences_page.editing.transition_between_photos_get_checkbox_status()


            if check_result:
                case.result = False
                case.fail_log = 'VDE212619-0153'
            else:
                case.result = True

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_21(self):
        with uuid("""f02a8331-3e88-4dfc-bf9e-6ae5d4697b9d
9f892ec1-3211-4242-9c13-0da0a2cc6e46
9471acc3-bbdc-4b92-b6bc-3d3e803c4ea8
eaefd747-6b03-4a61-b225-92e4ee71bad0
dc1d8040-33ee-4db9-a5e7-957554143b90
9979aba5-6f05-4e5d-a237-3222b4c1f152
e38b6a12-b61e-44d6-a330-294220954787
a3a381a6-0a9e-47d1-85a4-2a95b46ddb9d""") as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"