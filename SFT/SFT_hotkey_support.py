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
effect_room_page = PageFactory().get_page_object('effect_room_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
transition_room_page = PageFactory().get_page_object('transition_room_page', mwc)
library_preview_page = PageFactory().get_page_object('library_preview_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Hotkey Support.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder /Users/cl/Desktop/SFT_M1_2922
Ground_Truth_Folder = app.ground_truth_root + '/Hotkey_Support/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Hotkey_Support/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Hotkey_Support():
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

    @classmethod
    def setup_class(cls):
        main_page.clear_cache()
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('Hotkey_Support')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"hotkey support result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        with uuid("a3812b08-137e-4f93-967d-bb725bdbb841") as case:
            # 1. Hotkey Category
            # 1.1. Menu Bar
            # 1.1.2. [PowerDirector] > preferences
            main_page.tap_Preferences_hotkey()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_1_2_1.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_1_2_1.png'
            current_preview = media_room_page.snapshot(
                locator=L.preferences.main_window, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.press_esc_key()

        with uuid("21a5e289-bde2-4b6e-a4ac-0cfe29521110") as case:
            # 1.1. Menu Bar
            # 1.1.2. [PowerDirector] > hide PowerDirector
            main_page.tap_HidePDR_hotkey()
            time.sleep(DELAY_TIME)
            check_result = main_page.is_pdr_hide()
            if not check_result:
                case.result = False
            else:
                case.result = True
            # un-hide PDR
            main_page.activate()
            time.sleep(DELAY_TIME * 3)

        with uuid("39d153f8-51df-4c97-81c7-984098f8794d") as case:
            # 1.1. Menu Bar
            # 1.1.2. [PowerDirector] > quit PowerDirector
            main_page.tap_QuitPDR_hotkey()
            time.sleep(DELAY_TIME * 2)
            check_result = main_page.is_pdr_exist()
            if not check_result:
                case.result = True
            else:
                case.result = False

            main_page.refresh_top()

        with uuid("8765fa95-c944-4052-81d4-1a2d2ba10a60") as case:
            # 1.1. Menu Bar
            # 1.1.3. [File] > Create new Project
            main_page.insert_media("Food.jpg")
            main_page.tap_CreateNewProject_hotkey()

            check_result = main_page.handle_no_save_project_dialog()
            case.result = check_result

        with uuid("00663cd9-ce4b-4299-a9b5-2591083c55b3") as case:
            # 1.1. Menu Bar
            # 1.1.3. [File] > New workspace
            main_page.insert_media("Food.jpg")
            main_page.tap_NewWorkspace_hotkey()

            check_result = main_page.handle_no_save_project_dialog()
            case.result = check_result

        with uuid("e76dee12-000b-491f-b72e-037d7ec3bd83") as case:
            # 1.1. Menu Bar
            # 1.1.3. [File] > open existing project
            main_page.tap_OpenProject_hotkey()
            main_page.handle_open_project_dialog(Test_Material_Folder + 'test_pip_custom_tag_save.pds')
            main_page.handle_no_save_project_dialog()
            time.sleep(DELAY_TIME * 3)

            check_result = main_page.get_project_name()
            if not check_result == 'test_pip_custom_tag_save':
                case.result = False
            else:
                case.result = True

        with uuid("4773fa46-4b11-458b-ac43-11194c6103af") as case:
            # 1.1. Menu Bar
            # 1.1.3. [File] > save project
            main_page.insert_media('Food.jpg')
            main_page.click_undo()

            check_result = main_page.get_project_name()
            if not check_result == 'test_pip_custom_tag_save*':
                case.result = False
            else:
                main_page.tap_SaveProject_hotkey()
                time.sleep(DELAY_TIME)
                check_result = main_page.get_project_name()
                if not check_result == 'test_pip_custom_tag_save':
                    case.result = False
                else:
                    case.result = True

        with uuid("59a8f1c4-13da-4f88-a969-d45930ffe56e") as case:
            # 1.1. Menu Bar
            # 1.1.3. [File] > save project as
            main_page.tap_SaveProjectAs_hotkey()
            main_page.handle_save_file_dialog('test_save_as_project', Test_Material_Folder + 'test_save_as_project')
            time.sleep(DELAY_TIME)
            check_result = main_page.get_project_name()
            if not check_result == 'test_save_as_project':
                case.result = False
            else:
                case.result = True

        with uuid("1c7ff055-bb03-4fca-86bd-b5bf1deca478") as case:
            # 1.1. Menu Bar
            # 1.1.4. [Edit] > redo
            main_page.tap_Redo_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_1_4_2.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_1_4_2.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid("d1f22cdc-0df3-4aea-8ae4-f08a56586848") as case:
            # 1.1. Menu Bar
            # 1.1.4. [Edit] > cut
            main_page.tap_Cut_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_1_4_3.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_1_4_3.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid("59e5af97-f0e4-4600-9da1-a17cab52a932") as case:
            # 1.1. Menu Bar
            # 1.1.4. [Edit] > undo
            main_page.tap_Undo_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_1_4_1.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_1_4_1.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid("9c17e45c-d630-4643-a699-e1ca9bf653a5") as case:
            # 1.1. Menu Bar
            # 1.1.4. [Edit] > copy
            main_page.tap_Copy_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_1_4_4.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_1_4_4.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.select_timeline_media('Food.jpg')
            main_page.tap_Remove_hotkey()

        with uuid("f9097791-2589-4ed4-88c6-47b9d86f94f6") as case:
            # 1.1. Menu Bar
            # 1.1.4. [Edit] > paste
            main_page.tap_Paste_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_1_4_5.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_1_4_5.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid("843ded49-3f4a-4568-9c78-8172a8c5312a") as case:
            # 1.1. Menu Bar
            # 1.1.4. [Edit] > remove
            main_page.tap_Remove_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_1_4_6.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_1_4_6.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid("05ec2eb0-c5ff-4af6-9412-b15930841bf7") as case:
            # 1.1. Menu Bar
            # 1.1.4. [Edit] > select all in library
            main_page.tap_SelectAll_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_1_4_7.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_1_4_7.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid("b75dec74-31d7-4093-ac61-2fe2d347f00f") as case:
            # 1.1. Menu Bar
            # 1.1.5. [View] > enter full screen
            main_page.EnterFullScreen_hotkey()
            time.sleep(DELAY_TIME)

            check_result = main_page.is_full_screen()
            case.result = check_result

            main_page.EnterFullScreen_hotkey()
            time.sleep(DELAY_TIME)

        with uuid("d88de755-48ec-4e6c-be51-db54442d4494") as case:
            # 1.1. Menu Bar
            # 1.1.5. [View] > SVRT information
            main_page.SVRTInfo_hotkey()

            check_result = media_room_page.has_svrt_info_window()
            case.result = check_result
            case.fail_log = 'VDE213308-0012'
            # PDR20.0.3303 Bug

            main_page.exist_click(L.timeline_operation.workspace)
            main_page.right_click()
            main_page.select_right_click_menu('Show SVRT Track')

        with uuid("72264f43-3da0-400c-bc6d-1daa42e9bf8b") as case:
            # 1.1. Menu Bar
            # 1.1.6. [Window] > minimize
            time.sleep(DELAY_TIME)
            main_page.tap_MinimizeWindow_hotkey()
            time.sleep(DELAY_TIME)

            check_result = main_page.is_minimize()
            if not check_result:
                case.result = False
            else:
                case.result = True

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid('50b0b60a-5ca5-408b-acdb-34f35345a253') as case:
            # 1.2. Room
            # 1.2.2. Effect Room > F4
            main_page.insert_media('Skateboard 01.mp4')
            main_page.tap_EffectRoom_hotkey()

            check_result = effect_room_page.check_effect_room()
            case.result = check_result

        with uuid('cf02f9f2-a9e5-4466-827f-acbd3ad207a7') as case:
            # 1. Hotkey Category
            # 1.2. Room
            # 1.2.1. Media Room > F3
            main_page.tap_MediaRoom_hotkey()

            check_result = L.media_room.tag_main_frame
            if not media_room_page.is_exist(locator=check_result):
                case.result = False
            else:
                case.result = True

        with uuid('baadae15-734f-4d35-ac29-e7510c51297d') as case:
            # 1.2. Room
            # 1.2.3. Video overlay (PiP Object) Room > F5
            main_page.tap_PiPRoom_hotkey()

            check_result = pip_room_page.check_in_Pip_room()
            case.result = check_result

        with uuid('4cf1819d-7c44-4c29-b24b-21db45006796') as case:
            # 1.2. Room
            # 1.2.4. Particle Room > F6
            main_page.tap_ParticleRoom_hotkey()

            check_result = particle_room_page.check_in_particle_room()
            case.result = check_result

        with uuid('9e4c324b-b907-41d3-a774-d2d8660d9ac0') as case:
            # 1.2. Room
            # 1.2.5. Title Room > F7
            main_page.tap_TitleRoom_hotkey()

            check_result = title_room_page.check_in_title_room()
            case.result = check_result

        with uuid('71e01441-275f-47ac-9dd7-070a3e41ac7e') as case:
            # 1.2. Room
            # 1.2.6. Transition Room > F8
            main_page.tap_TransitionRoom_hotkey()

            check_result = L.transition_room.explore_view_region.table_all_content_tags
            if not transition_room_page.is_exist(locator=check_result):
                case.result = False
            else:
                case.result = True

        with uuid('3ca1e623-783b-443a-8b06-0e55f22e2ab8') as case:
            # 1.2. Room
            # 1.2.7. Audio Mixing Room > F9
            main_page.tap_AudioMixingRoom_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_2_7_1.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_2_7_1.png'
            current_preview = main_page.snapshot(
                locator=L.audio_mixing_room.audio_mixing_track, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            # main_page.tap_MediaRoom_hotkey()

        with uuid('d1f642d7-48c3-4245-96e4-bd3342ddf322') as case:
            # 1.2. Room
            # 1.2.8. Voice-Over Recording Room > F10
            main_page.tap_VoiceRecordRoom_hotkey()
            main_page.exist_click(L.base.button_ok)

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_2_8_1.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_2_8_1.png'
            current_preview = main_page.snapshot(
                locator=L.library_preview.upper_view_region, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('ad2b1aa8-6a36-4e78-b409-d5edea9803ed') as case:
            # 1.2. Room
            # 1.2.9. Subtitle Room > F12
            main_page.tap_SubtitleRoom_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_2_9_1.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_2_9_1.png'
            current_preview = main_page.snapshot(
                locator=L.library_preview.upper_view_region, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.exist_click(L.timeline_operation.workspace)
            main_page.right_click()
            main_page.select_right_click_menu('Show Subtitle Track')

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid('aa1403f7-bf43-4189-bcd6-1cf6891eafb1') as case:
            # 1.4. Timeline Operation
            # 1.4.1. Select All
            main_page.insert_media("Food.jpg")
            main_page.select_library_icon_view_media("Landscape 01.jpg")
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_library_icon_view_media("Skateboard 01.mp4")
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_library_icon_view_media("Skateboard 02.mp4")
            main_page.tips_area_insert_media_to_selected_track(option=1)

            media_room_page.tap_SelectAll_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_4_1_1.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_4_1_1.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('885aa4e4-d507-42c5-8dc7-3b4621528518') as case:
            # 1.4. Timeline Operation
            # 1.4.2. Split
            main_page.set_timeline_timecode('00_00_05_00')
            media_room_page.tap_Split_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_4_2_1.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_4_2_1.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('c60ce439-c1d8-4620-844b-f80b90b7d0aa') as case:
            # 1.4. Timeline Operation
            # 1.4.3. Trim
            media_room_page.tap_Trim_hotkey()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_4_3_1.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_4_3_1.png'
            current_preview = main_page.snapshot(
                locator=L.base.main_window, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.press_esc_key()

        with uuid('d1318fd9-8818-4a77-a46d-82e5b2668461') as case:
            # 1.4. Timeline Operation
            # 1.4.7. Ripple Editing > cut and leave gap
            media_room_page.tap_cut_and_leave_gap_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_4_7_1.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_4_7_1.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.tap_Undo_hotkey()

        with uuid('b49f4b10-2fe1-4dcc-8d8a-10d94ad48d28') as case:
            # 1.4. Timeline Operation
            # 1.4.7. Ripple Editing > cut and fill gap
            media_room_page.tap_cut_and_fill_gap_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_4_7_2.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_4_7_2.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.tap_Undo_hotkey()

        with uuid('07e93cf5-7923-4822-be29-c2cca950360c') as case:
            # 1.4. Timeline Operation
            # 1.4.7. Ripple Editing > cut, fill gap and move all clips
            media_room_page.tap_cut_fill_gap_and_move_all_clips_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_4_7_3.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_4_7_3.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.tap_Undo_hotkey()

        with uuid('f9a6f9c5-8b95-42b8-942e-94008c4fe2ac') as case:
            # 1.4. Timeline Operation
            # 1.4.7. Ripple Editing > Remove and leave gap
            media_room_page.tap_remove_and_leave_gap_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_4_7_4.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_4_7_4.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.tap_Undo_hotkey()

        with uuid('32f0f42d-b6f7-4a4b-b5ed-b2d2e3fcc6b5') as case:
            # 1.4. Timeline Operation
            # 1.4.7. Ripple Editing > Remove and fill gap
            media_room_page.tap_remove_and_fill_gap_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_4_7_5.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_4_7_5.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.tap_Undo_hotkey()

        with uuid('4cc09417-62cd-404b-9bf3-eb6671f96988') as case:
            # 1.4. Timeline Operation
            # 1.4.7. Ripple Editing > Remove, fill gap and move all clips
            media_room_page.tap_remove_fill_gap_and_move_all_clips_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_4_7_6.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_4_7_6.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.tap_Undo_hotkey()
            main_page.tap_Undo_hotkey()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid('f0e919d7-6068-4b40-9cee-2c0b72ee4c92') as case:
            # 1.3. Display Panel (Preview)
            # 1.3.1. Play/Pause > Space bar
            # able to play clip
            media_room_page.select_media_content('Skateboard 01.mp4')
            media_room_page.press_space_key()
            time.sleep(DELAY_TIME * 5)
            media_room_page.press_space_key()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_3_1_1.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_3_1_1.png'
            current_preview = media_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result = media_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('5740d733-d73f-4986-8418-5b6506f3d9c6') as case:
            # 1.3. Display Panel (Preview)
            # 1.3.1. Play/Pause > Space bar
            # able to pause preview
            media_room_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            media_room_page.press_space_key()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_3_1_2.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_3_1_2.png'
            current_preview = media_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result = media_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('97b4ce4f-8830-4669-8c55-81f65ed4372b') as case:
            # 1.3. Display Panel (Preview)
            # 1.3.2. Stop > cmd + /
            media_room_page.tap_Stop_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_3_2_1.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_3_2_1.png'
            current_preview = media_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result = media_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('0c0c12e3-e4e9-4be0-906e-6eddaf6ad6fa') as case:
            # 1.3. Display Panel (Preview)
            # 1.3.3. Next frame > .
            # switch to next frame
            for i in range(20):
                media_room_page.tap_NextFrame_hotkey()
                time.sleep(DELAY_TIME * 0.2)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_3_3_1.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_3_3_1.png'
            current_preview = media_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result = media_room_page.compare(ground_truth, current_preview, similarity=0.95)
            case.result = check_result

        with uuid('330aa63f-7217-452a-b641-4163212ef38c') as case:
            # 1.3. Display Panel (Preview)
            # 1.3.4. Previous frame > ,
            # switch to previous frame
            for i in range(10):
                media_room_page.tap_PreviousFrame_hotkey()
                time.sleep(DELAY_TIME * 0.2)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_3_4_1.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_3_4_1.png'
            current_preview = media_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result = media_room_page.compare(ground_truth, current_preview, similarity=0.95)
            case.result = check_result

        with uuid('e9cc34db-4d86-488f-b2d2-7729bfb1432e') as case:
            # 1.3. Display Panel (Preview)
            # 1.3.5. Fast Forward > 2X
            media_room_page.tap_FastForward_hotkey()
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_3_5_1.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_3_5_1.png'
            current_preview = media_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result = media_room_page.compare(ground_truth, current_preview, similarity=0.95)
            case.result = check_result

            time.sleep(DELAY_TIME * 3)

        with uuid('8a3d72cd-f650-42bb-8d21-6e31d48c0995') as case:
            # 1.3. Display Panel (Preview)
            # 1.3.5. Fast Forward > 4X
            for i in range(2):
                media_room_page.tap_FastForward_hotkey()
                time.sleep(DELAY_TIME * 0.2)

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_3_5_2.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_3_5_2.png'
            current_preview = media_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result = media_room_page.compare(ground_truth, current_preview, similarity=0.95)
            case.result = check_result

            time.sleep(DELAY_TIME * 2)

        with uuid('15f777e0-43bd-4c18-aa74-c76cd994da50') as case:
            media_room_page.tap_Stop_hotkey()
            time.sleep(DELAY_TIME * 0.5)
            # 1.3. Display Panel (Preview)
            # 1.3.5. Fast Forward > 8X
            for i in range(3):
                media_room_page.tap_FastForward_hotkey()
                time.sleep(DELAY_TIME * 0.3)

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_3_5_3.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_3_5_3.png'
            current_preview = media_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result = media_room_page.compare(ground_truth, current_preview, similarity=0.95)
            case.result = check_result

        with uuid('44d58b54-8828-426c-af39-f2d2220879ac') as case:
            # 1.3. Display Panel (Preview)
            # 1.3.5. Fast Forward > 16X
            media_room_page.tap_Stop_hotkey()
            time.sleep(DELAY_TIME * 0.5)
            for i in range(4):
                media_room_page.tap_FastForward_hotkey()
                time.sleep(DELAY_TIME * 0.2)

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_3_5_4.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_3_5_4.png'
            current_preview = media_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result = media_room_page.compare(ground_truth, current_preview, similarity=0.95)
            case.result = check_result

            time.sleep(DELAY_TIME * 1)

        with uuid('a99c5c84-e691-416d-b181-46833ad1f119') as case:
            # 1.3. Display Panel (Preview)
            # 1.3.6. Library preview window > Mark in
            # Set mark in position
            main_page.top_menu_bar_view_show_library_preview_window()
            library_preview_page.library_preview_window_exist()
            library_preview_page.set_library_preview_window_timecode('00_00_02_00')
            media_room_page.tap_MarkIn_onLibraryPreview_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_3_6_1.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_3_6_1.png'
            current_preview = media_room_page.snapshot(
                locator=L.main.library_preview_window.slider, file_name=image_full_path)

            check_result = media_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('887cfe54-e431-457b-a5bc-cb1b9125a80c') as case:
            # 1.3. Display Panel (Preview)
            # 1.3.6. Library preview window > mark out
            # set mark out position
            library_preview_page.set_library_preview_window_timecode('00_00_08_00')
            media_room_page.tap_MarkOut_onLibraryPreview_hotkey()

            image_full_path = Auto_Ground_Truth_Folder + 'hotkey_support_1_3_6_2.png'
            ground_truth = Ground_Truth_Folder + 'hotkey_support_1_3_6_2.png'
            current_preview = media_room_page.snapshot(
                locator=L.main.library_preview_window.slider, file_name=image_full_path)

            check_result = media_room_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    3b464aa2-a601-48fe-9038-eb3ea018f373
                    1373e3b7-d0af-42a5-abd6-2693376e7d0a
                    4c0f15ea-3b79-482b-b373-ca0fd7bea50e
                    fcf6ee5a-d6c4-44d9-9fa1-cfaaa8e9c731
                    fca91ee8-b96d-4908-99e2-02662cc316df
                    2962d5b1-1eba-40a6-a1cf-f0d51bcb32e3
                    ae755547-cef4-464c-b8c4-86b893a21481
                    e9648d42-48da-4f90-a758-6d15b92ee46d
                    3119b4d8-985f-427a-b847-2ab0549523b7
                    e75a6afe-843a-45b6-8bdc-5da4c35ce488
                    4aee2a58-be4a-4702-9e2d-624abfded640
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'