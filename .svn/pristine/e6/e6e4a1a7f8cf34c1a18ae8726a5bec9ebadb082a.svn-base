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
mwc = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mwc)
base_page = PageFactory().get_page_object('base_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
fix_enhance_page = PageFactory().get_page_object('fix_enhance_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
keyframe_room_page = PageFactory().get_page_object('keyframe_room_page', mwc)
effect_room_page = PageFactory().get_page_object('effect_room_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
transition_room_page = PageFactory().get_page_object('transition_room_page', mwc)
pip_designer_page = PageFactory().get_page_object('pip_designer_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
precut_page = PageFactory().get_page_object('precut_page', mwc)
mask_designer_page = PageFactory().get_page_object('mask_designer_page', mwc)
video_speed_page = PageFactory().get_page_object('video_speed_page', mwc)
blending_mode_page = PageFactory().get_page_object('blending_mode_page',mwc)
video_collage_designer_page = PageFactory().get_page_object('video_collage_designer_page', mwc)
library_preview_page = PageFactory().get_page_object('library_preview_page',mwc)



# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Undo Redo.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder - Setup for Overall Project
Ground_Truth_Folder = app.ground_truth_root + '/Undo_Redo/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Undo_Redo/'
Test_Material_Folder = app.testing_material

# For Ground Truth / Test Material folder - Setup for Duncan personal testing
# Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/GroundTruth/Title_Room/'
# Auto_Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/ATGroundTruth/Title_Room/'
# Test_Material_Folder = '/Users/cl/Desktop/Duncan/Material/'

DELAY_TIME = 1

class Test_Undo_Redo():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
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
            google_sheet_execution_log_init('Undo_Redo')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"test case template result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'),
                               report.get_ovinfo('duration'))
        report.show()

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        with uuid("ca972d36-451e-437d-b32e-b3ef389b890a") as case:
            # 1.1.1 Add/Remove Clips To Timeline - 1.1 Add - Type - [Media: Photo]
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-1-1_Photo.png')
            main_page.insert_media('Landscape 01.jpg')
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-1_Photo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("5acd26a7-5f24-445b-ba5d-81cb0d289d7c") as case:
            # 1.1.2 Add/Remove Clips To Timeline - 1.1 Add - Type - [Media: Video]
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-1-2_Video.png')
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(1)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-2_Video.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("9bf9c9a8-9caf-4240-b499-0c776fb75b03") as case:
            # 1.1.3 Add/Remove Clips To Timeline - 1.1 Add - Type - [Media: Audio]
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-1-3_Audio.png')
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(1)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-3_Audio.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("ad287b78-3087-44fc-be60-af38080bf54c") as case:
            # 1.1.4 Add/Remove Clips To Timeline - 1.1 Add - Type - [Media: Select All]
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-1-4_All.png')
            media_room_page.library_menu_select_all()
            tips_area_page.click_TipsArea_btn_insert()
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-4_All.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid("8e62d0ba-a777-40ef-8678-a92cb29d46a9") as case:
            # 1.1.5 Add/Remove Clips To Timeline - 1.1 Add - Type - [Effect]
            time.sleep(5)
            main_page.hover_library_media('Skateboard 01.mp4')
            media_room_page.library_clip_context_menu_insert_on_selected_track()
            main_page.enter_room(3)
            time.sleep(2)
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-1-5_effect.png')
            effect_room_page.search_and_input_text('pop')
            main_page.drag_media_to_timeline_playhead_position('Pop Art Wall')
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-5_effect.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            main_page.click_redo()

        with uuid("2907df3f-9061-4bf3-a128-9dbea085ddc9") as case:
            # 1.1.6 Add/Remove Clips To Timeline - 1.1 Add - Type - [PiP]
            main_page.enter_room(4)
            time.sleep(2)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME)
            media_room_page.select_media_content('Dialog_06')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-1-6_PiP.png')
            tips_area_page.tips_area_insert_media_to_selected_track(option=2)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-6_PiP.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            main_page.click_redo()

        with uuid("996c83cd-7d2c-4dba-8b42-1f262d4f2c8f") as case:
            # 1.1.7 Add/Remove Clips To Timeline - 1.1 Add - Type - [particle]
            main_page.enter_room(5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME)
            media_room_page.select_media_content('Maple')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-1-7_particle.png')
            tips_area_page.tips_area_insert_media_to_selected_track(option=2)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-7_particle.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            main_page.click_redo()

        with uuid("5818b3ef-5f46-4f35-80b7-72a878a0ad86") as case:
            # 1.1.8 Add/Remove Clips To Timeline - 1.1 Add - Type - [Title]
            main_page.enter_room(1)
            title_room_page.select_LibraryRoom_category('Text Only')
            media_room_page.select_media_content('Default')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-1-8_title.png')
            tips_area_page.tips_area_insert_media_to_selected_track(option=2)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-8_title.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("89b78401-34e0-45eb-bb06-f9bbd47d26e8") as case:
            # 1.1.11 Add/Remove Clips To Timeline - 1.1 Add - Method - [Add / Insert ... to track] button
            media_room_page.select_media_content('Default')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-1-11_add.png')
            tips_area_page.tips_area_insert_media_to_selected_track(option=2)
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-11_add.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("89599705-5908-4dc3-b39d-dc5ba1b8ac8f") as case:
            # 1.1.9 Add/Remove Clips To Timeline - 1.1 Add - Type - [Transition]
            main_page.enter_room(2)
            time.sleep(1)
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-1-9_transition.png')
            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Prefix')
            main_page.set_timeline_timecode('00_00_01_08')
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-9_transition.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            main_page.click_undo()


    #@pytest.mark.skip
    @exception_screenshot
    def test_1_2_1(self):
        with uuid("a3ffe371-a088-42c5-9285-ce24758504b4") as case:
            # 1.2.1 Add/Remove Clips To Timeline - 1.2 Remove - Type - [Media: Photo]
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Landscape 01.jpg')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-2-1_Photo.png')
            # Press ""backspace"" (Mac shows ""delete"") key
            main_page.press_del_key()
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-1_Photo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            main_page.click_redo()

        with uuid("19935a3e-7d09-4bb6-9f3e-2f35c1e39d1d") as case:
            # 1.2.2 Add/Remove Clips To Timeline - 1.2 Remove - Type - [Media: Video]
            main_page.insert_media('Skateboard 01.mp4')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-2-2_Video.png')
            # Press ""backspace"" (Mac shows ""delete"") key
            main_page.press_del_key()
            # Expect Result: Undo operation is correct
            time.sleep(1)
            main_page.click_undo()
            time.sleep(1)
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-2_Video.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            main_page.click_redo()

        with uuid("8e5863de-2644-40a7-838c-9c7f8761a9f8") as case:
            # 1.2.3 Add/Remove Clips To Timeline - 1.2 Remove - Type - [Media: Audio]
            time.sleep(1)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(1)
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-2-3_Audio.png')
            # Press ""backspace"" (Mac shows ""delete"") key
            main_page.press_del_key()
            # Expect Result: Undo operation is correct
            time.sleep(1)
            main_page.click_undo()
            time.sleep(1)
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-3_Audio.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            main_page.click_redo()

        with uuid("9fd2418d-8d60-41db-8437-6ef8ce6fd194") as case:
            # 1.2.4 Add/Remove Clips To Timeline - 1.2 Remove - Type - [Media: Select All]
            media_room_page.library_menu_select_all()
            tips_area_page.click_TipsArea_btn_insert()
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-2-4_All.png')
            # Press ""backspace"" (Mac shows ""delete"") key
            main_page.press_del_key()
            # Expect Result: Undo operation is correct
            time.sleep(1)
            main_page.click_undo()
            time.sleep(1)
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-4_All.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            main_page.click_redo()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_2_5(self):
        with uuid("ce3df65b-b5cd-498b-8cc7-1d129796b21b") as case:
            # 1.2.5 Add/Remove Clips To Timeline - 1.2 Remove - Type - [Effect]
            time.sleep(5)
            main_page.hover_library_media('Skateboard 01.mp4')
            media_room_page.library_clip_context_menu_insert_on_selected_track()
            main_page.enter_room(3)
            time.sleep(2)
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-2-5_effect.png')
            effect_room_page.search_and_input_text('pop')
            main_page.drag_media_to_timeline_playhead_position('Pop Art Wall')
            # Press ""backspace"" (Mac shows ""delete"") key
            main_page.press_del_key()
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-5_effect.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("df96de50-4a2e-4f73-b71a-ef571acbb792") as case:
            # 1.2.6 Add/Remove Clips To Timeline - 1.2 Remove - Type - [PiP]
            main_page.enter_room(4)
            time.sleep(2)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME)
            media_room_page.select_media_content('Dialog_06')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-2-6_PiP.png')
            tips_area_page.tips_area_insert_media_to_selected_track(option=2)
            # Delete and fill gap
            main_page.tap_cut_and_fill_gap_hotkey()
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-6_PiP.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            main_page.click_redo()

        with uuid("d998efbf-2b28-4932-af3c-275273ae8451") as case:
            # 1.2.7 Add/Remove Clips To Timeline - 1.2 Remove - Type - [particle]
            main_page.enter_room(5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME)
            media_room_page.select_media_content('Maple')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-2-7_particle.png')
            tips_area_page.tips_area_insert_media_to_selected_track(option=2)
            # Delete and fill gap
            main_page.tap_cut_and_fill_gap_hotkey()
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-7_particle.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            main_page.click_redo()

        with uuid("ea07e32f-14d3-4cc4-b4f8-a41bb5f31cba") as case:
            # 1.2.8 Add/Remove Clips To Timeline - 1.2 Remove - Type - [Title]
            main_page.enter_room(1)
            title_room_page.select_LibraryRoom_category('Text Only')
            media_room_page.select_media_content('Default')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-2-8_title.png')
            tips_area_page.tips_area_insert_media_to_selected_track(option=2)
            # Delete and fill gap
            main_page.tap_cut_and_fill_gap_hotkey()
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-8_title.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("7cc11a6f-49f2-4082-8016-cfbc21809f4a") as case:
            # 1.2.11 Add/Remove Clips To Timeline - 1.2 Remove - Method - [Add / Insert ... to track] button
            media_room_page.select_media_content('Default')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-2-11_add.png')
            tips_area_page.tips_area_insert_media_to_selected_track(option=2)
            # Delete and fill gap
            main_page.tap_cut_and_fill_gap_hotkey()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-11_add.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            main_page.click_redo()

        with uuid("75a46a97-d93f-4863-ac92-4ab2f5808231") as case:
            # 1.2.9 Add/Remove Clips To Timeline - 1.2 Remove - Type - [Transition]
            main_page.enter_room(2)
            time.sleep(1)
            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Prefix')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '1-2-9_transition.png')
            # Delete and fill gap
            main_page.tap_cut_and_fill_gap_hotkey()
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-9_transition.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            main_page.click_undo()

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_1_1(self):
        with uuid("dceefce3-a594-4fbc-a815-5e291655b938") as case:
            # 2.1.1 General Timeline operation - 2.1 Move - Clip - Same Track - Undo operation is correct
            time.sleep(5)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1-1_same_track.png')
            main_page.tips_area_insert_media_to_selected_track()
            timeline_operation_page.drag_single_media_move_to(0,0,35)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-1-1_same_track.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("b22a562c-7948-4c20-b370-d52856f25060") as case:
            # 2.1.2 General Timeline operation - 2.1 Move - Clip - Same Track - Redo operation is correct
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-1-2_same_track.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("e9b1874a-0ff9-4329-877b-86938f3f09a3") as case:
            # 2.1.3 General Timeline operation - 2.1 Move - Clip - Different Tracks - Undo operation is correct
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1-3_different_track.png')
            timeline_operation_page.drag_single_media_to_other_track(0, 0, -200, 2)
            current_image2 = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1-4_different_track.png')
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-1-3_different_track.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("07affcb6-3ce2-45b9-9894-c95d5401e844") as case:
            # 2.1.4 General Timeline operation - 2.1 Move - Clip - Different Track - Redo operation is correct
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1-4_different_track.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-1-4_different_track.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_2_1(self):
        with uuid("3837284d-8043-40e7-9fd1-8c58edbccb83") as case:
            # 2.2.2.1 Trim - Single Trim Video - Undo operation is correct
            time.sleep(5)
            # Import 2 clips into timeline
            main_page.insert_media('Skateboard 02.mp4')
            main_page.select_library_icon_view_media("Skateboard 03.mp4")
            main_page.tips_area_insert_media_to_selected_track(option=1)
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-1_TrimSingle_Undo.png')
            # Trim the last video by by dragging clip edge
            timeline_operation_page.drag_timeline_clip(mode = 'Last', ratio = 0.5, track_index1 = 0, clip_index1 = 1, track_index2 = None, clip_index2 = None)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-1_TrimSingle_Undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("277eafb6-c582-4bf7-8577-8aaec9c37c55") as case:
            # 2.2.2.2 Trim - Single Trim Video - Redo operation is correct
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-2_TrimSingle_Redo.png')
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-2_TrimSingle_Redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("32883297-e40c-4894-92ad-54aae2b7ee31") as case:
            # 2.2.2.3 Trim - Multiple Trim Video - Undo operation is correct
            main_page.tap_Trim_hotkey()
            precut_page.edit_precut_switch_trim_mode('Multi')
            # Drag slider
            precut_page.drag_multi_trim_slider(0, 0, 3, 0)
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + '2-2-3_Multiple_undo.png')
            # Click mark in button
            precut_page.tap_multi_trim_mark_in()
            # Expect Result: Undo operation is correct
            main_page.tap_Undo_hotkey()
            # Snapshot indicator position
            logger(f"{current_image=}")
            compare_result = precut_page.compare(Ground_Truth_Folder + '2-2-3_Multiple_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("36227bcf-aa6b-43cc-84da-00c66ea02dc4") as case:
            # 2.2.2.4 Trim - Multiple Trim Video - Redo operation is correct
            # Expect Result: Undo operation is correct
            main_page.tap_Redo_hotkey()
            # Snapshot indicator position
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + '2-2-4_Multiple_redo.png')
            logger(f"{current_image=}")
            compare_result = precut_page.compare(Ground_Truth_Folder + '2-2-4_Multiple_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("cccd589a-dd34-466a-a5e1-b8a377e47e7f") as case:
            # 2.2.2.5 Trim - Trim Audio
            # Close Trim dialog
            precut_page.click_ok()
            logger(f"{precut_page.click_ok=}")
            # Insert audio file
            main_page.select_library_icon_view_media("Speaking Out.mp3")
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-5_Audio_Undo.png')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            # Trim the last video by by dragging clip edge
            timeline_operation_page.drag_timeline_clip('Last', 0.5, 1, 1)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-5_Audio_Undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("6eb2743e-ddd9-43f7-a7a7-3ed2bc3c26b6") as case:
            # 2.2.2.6 Trim - Trim Audio
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-5_Audio_redo.png')
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-5_Audio_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result


    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_3_1(self):
        with uuid("4d6948d4-780d-4ab6-b901-d65e7a146ef1") as case:
            # 2.2.3.1 Split - Single clip
            time.sleep(5)
            # Import 2 clips into timeline
            main_page.insert_media('Skateboard 02.mp4')
            main_page.select_library_icon_view_media("Skateboard 03.mp4")
            main_page.tips_area_insert_media_to_selected_track(option=1)
            # Change timecode
            main_page.set_timeline_timecode('00_00_05_11', is_verify=False)
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-3-1_Split_Undo.png')
            # Click split
            main_page.tap_Split_hotkey()
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-3-1_Split_Undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("8fa77fff-88df-42d6-9d0f-bae3ad10f933") as case:
            # 2.2.3.2 Split - Single clip - Redo operation is correct
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-3-2_Split_Redo.png')
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-3-2_Split_Redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("8c96d0a4-b10b-46bd-b366-4c928368a802") as case:
            # 2.2.3.3 Split - Multiple Clips (video+image)
            media_room_page.hover_library_media('Landscape 02.jpg')
            main_page.drag_media_to_timeline_clip('Skateboard 03.mp4', 0, 1, 0)
            # Change timecode
            main_page.set_timeline_timecode('00_00_03_11', is_verify=False)
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-3-3_Split_Undo.png')
            # Click split
            main_page.tap_Split_hotkey()
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-3-3_Split_Undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("2e1394d5-495a-41be-b238-162a5d4b72da3") as case:
            # 2.2.3.4 Split - Multiple Clips (video+image) - Redo operation is correct
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-3-4_Split_Redo.png')
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-3-4_Split_Redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("e83bbbb4-7d73-4b6e-b979-482237cfffd0") as case:
            # 2.2.3.5 Split - Audio
            time.sleep(5)
            media_room_page.hover_library_media('Mahoroba.mp3')
            main_page.drag_media_to_timeline_clip('Skateboard 03.mp4', 0, 1, 0)
            # Change timecode
            main_page.set_timeline_timecode('00_00_03_11', is_verify=False)
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-3-5_Split_Undo.png')
            # Click split
            main_page.tap_Split_hotkey()
            time.sleep(2)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-3-5_Split_Undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("cfff6c27-4b6c-4e9a-813e-add0d3c2e7e6") as case:
            # 2.2.3.6 Split - Audio- Redo operation is correct
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-3-6_Split_Redo.png')
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-3-6_Split_Redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_4_1(self):
        with uuid("7bab4dd1-46ef-4da6-86d6-270149be7ab7") as case:
            # 2.2.4.1 Change Duration - Image
            time.sleep(5)
            main_page.insert_media('Food.jpg')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-4-1_Duration_Undo.png')
            main_page.select_timeline_media('Food.jpg')
            # Change Duration via right click menu
            main_page.right_click()
            main_page.select_right_click_menu('Set Clip Attributes', 'Set Duration...')
            main_page.adjust_duration_settings('00_01_01_01')
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-4-1_Duration_Undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("270bc865-a522-4a15-b357-1c2b447c61fc") as case:
            # 2.2.4.2 Change Duration - Image
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-4-2_Duration_Redo.png')
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-4-2_Duration_Redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0bd53ba3-7b82-4536-9aed-9540cd2ef664") as case:
            # 2.2.4.3 Change Duration - Template - Effect - Undo operation is correct
            main_page.enter_room(3)
            time.sleep(1)
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-4-3_effect_undo.png')
            effect_room_page.search_and_input_text('pop')
            main_page.drag_media_to_timeline_playhead_position('Pop Art Wall')
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-2-4-3_effect_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            main_page.click_redo()

        with uuid("daeb42e8-5d0f-45c7-a0f8-d170aba8be07") as case:
            # 2.2.4.4 Change Duration - Template - Effect - Undo operation is correct
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-4-4_Effect_Redo.png')
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-4-4_Effect_Redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("63ed9943-35da-48c3-92d2-0c3bb21fb157") as case:
            # 2.2.4.5 Change Duration - Template - PiP - Undo operation is correct
            main_page.enter_room(4)
            time.sleep(1)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME)
            media_room_page.select_media_content('Dialog_06')
            tips_area_page.tips_area_insert_media_to_selected_track(option=2)
            main_page.select_timeline_media('Dialog_06')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-4-5_PIP_Undo.png')
            # Change Duration via right click menu
            main_page.right_click()
            main_page.select_right_click_menu('Set Clip Attributes', 'Set Duration...')
            main_page.adjust_duration_settings('00_02_02_02')
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-4-5_PIP_Undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("b31c9eae-e75d-4612-9bb7-ddf4cc539fc3") as case:
            # 2.2.4.6 Change Duration - Template - particle - Undo operation is correct
            main_page.enter_room(5)
            time.sleep(1)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME)
            media_room_page.select_media_content('Maple')
            tips_area_page.tips_area_insert_media_to_selected_track(option=2)
            # Change Duration via right click menu
            main_page.select_timeline_media('Maple')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-4-6_particle_Undo.png')
            main_page.right_click()
            main_page.select_right_click_menu('Set Duration...')
            main_page.adjust_duration_settings('00_03_03_03')
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-4-6_particle_Undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("ce66e289-6fea-47d7-b139-99769827afc8") as case:
            # 2.2.4.7 Change Duration - Template - title - Undo operation is correct
            main_page.enter_room(1)
            time.sleep(1)
            title_room_page.select_LibraryRoom_category('Text Only')
            media_room_page.select_media_content('Default')
            tips_area_page.tips_area_insert_media_to_selected_track(option=2)
            # Change Duration via right click menu
            main_page.select_timeline_media('My Title')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-2-4-7_title_Undo.png')
            main_page.right_click()
            main_page.select_right_click_menu('Set Duration...')
            main_page.adjust_duration_settings('00_04_04_04')
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-4-7_title_Undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    '''
        # Skip due to transition settings page function is not implemented
        with uuid("5f844ce7-ee55-4fdf-95cc-ee2997e7d244") as case:
            # 2.2.4.8 Change Duration - Template - transition - Undo operation is correct
            main_page.enter_room(2)
            time.sleep(1)
            main_page.drag_transition_to_timeline_clip('Aberration 2', 'My Title', clip_index=0)
            tips_area_page.click_TipsArea_btn_Modify('Transition', close_win=False)
            main_page.set_time_code()
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace,
                                                             file_name=Auto_Ground_Truth_Folder + '2-2-4-8_transition_Undo.png')
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-2-4-8_transition_Undo.png',
                                                             current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
    '''



    #@pytest.mark.skip
    @exception_screenshot
    def test_3_1_1(self):
        with uuid("a7ff6541-7865-4074-9c35-24c9d0e884ae") as case:
            # 3.1.1 - Add/Remove FX & Transition - 3.1 FX - Single FX - Undo
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Skateboard 03.mp4')
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            # Snapshot image of preview window before WB is ticked
            fix_enhance_page.fix.enable_white_balance()
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-2-4_ColorTemperature_Slider.png')
            # Adjust color temperature to 90 by slider
            fix_enhance_page.fix.white_balance.set_color_temperature_slider(90)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-1_Undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("a48045f6-df57-4a80-b9f4-8b589ae1b002") as case:
            # 3.1.2 - Add/Remove FX & Transition - 3.1 FX - Single FX - Redo
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '3-1-2_Redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-2_Redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("06646fe5-35d2-4155-98a3-6190d7a811bd") as case:
            # 3.1.3 - Add/Remove FX & Transition - 3.1 FX - Mulitple FX on same clip - Undo
            current_image = timeline_operation_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '3-1-3_Undo.png')
            # Tick video stabilizer option
            fix_enhance_page.fix.enable_video_stabilizer()
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-3_Undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("ac56b702-5588-4c4a-a4d2-fe346e408f60") as case:
            # 3.1.4 - Add/Remove FX & Transition - 3.1 FX - Mulitple FX on same clip - Redo
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            time.sleep(DELAY_TIME*2)
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '3-1-4_Redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-4_Redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_3_3_2_1(self):
        with uuid("f34064b6-2df8-4653-a841-cb6ada9c59ff") as case:
            # 3.3.2.1 - Transition - Prefix - Undo operation is correct
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            # Import 2 clips into timeline
            main_page.insert_media('Skateboard 01.mp4')
            media_room_page.hover_library_media('Skateboard 02.mp4')
            main_page.drag_media_to_timeline_clip('Skateboard 01.mp4', 0, 1, 1)
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '3-3-2_prefix_undo.png')
            main_page.enter_room(2)
            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Prefix')
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-3-2_prefix_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("928bb18c-2a83-4309-852e-be983f606c45") as case:
            # 3.3.2.2 - Transition - Prefix - Redo operation is correct
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '3-3-2_prefix_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-3-2_prefix_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to no transition status
            main_page.click_undo()

        with uuid("bf6722fd-5cfa-4644-a1c1-6e02f37f79ca") as case:
            # 3.3.2.3 - Transition - Postfix - Undo operation is correct
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '3-3-2_Postfix_undo.png')
            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Postfix')
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-3-2_Postfix_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("69d7b0bd-3e1d-4eb1-8c64-eb3191b16dea") as case:
            # 3.3.2.4 - Transition - Postfix - Redo operation is correct
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '3-3-2_Postfix_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-3-2_Postfix_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to no transition status
            main_page.click_undo()

        with uuid("50e6a3bb-f7fb-423e-95a1-4e56b88b81c3") as case:
            # 3.3.2.5 - Transition - Cross - Undo operation is correct
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '3-3-2_Cross_undo.png')
            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Cross')
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-3-2_Cross_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("2fda15fc-3615-4f39-8022-9045c03bb259") as case:
            # 3.3.2.6 - Transition - Cross - Redo operation is correct
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '3-3-2_Cross_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-3-2_Cross_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to no transition status
            main_page.click_undo()

        with uuid("0304d55f-16a4-4581-a819-13790e18c7b6") as case:
            # 3.3.2.7 - Transition - Overlap - Undo operation is correct
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '3-3-2_Overlap_undo.png')
            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Overlap')
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-3-2_Overlap_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("ac5cbb56-11f2-45d5-b645-8b97f658d54c") as case:
            # 3.3.2.6 - Transition - Overalap - Redo operation is correct
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '3-3-2_Overlap_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-3-2_Overlap_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to no transition status
            main_page.click_undo()

    #@pytest.mark.skip
    @exception_screenshot
    def test_4_1_1(self):
        with uuid("12af27c3-8ee1-4a11-be3c-59c594238022") as case:
            # 4.1.1 Context Menu - 4.1 Image + Image (Ripple editing) - Overwrite
            time.sleep(5)
            # Import 2 clips into timeline
            main_page.insert_media('Landscape 01.jpg')
            time.sleep(1)
            media_room_page.hover_library_media('Landscape 02.jpg')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-1-1_Overwrite_undo.png')
            main_page.drag_media_to_timeline_clip('Landscape 01.jpg', 0, 1, 0)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-1-1_Overwrite_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("2d77cc13-2148-4493-a2aa-a97f4d781a87") as case:
            # 4.1.2 Context Menu - 4.1 Image + Image (Ripple editing) - Overwrite
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-1-2_Overwrite_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-1-2_Overwrite_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to default
            main_page.click_undo()

        with uuid("77bfb45e-8829-408b-91ac-bddcd3786eb3") as case:
            # 4.1.3 Context Menu - 4.1 Image + Image (Ripple editing) - Overwrite
            # Import 2nd clip into timeline
            media_room_page.hover_library_media('Landscape 02.jpg')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-1-3_Overwrite_undo.png')
            main_page.drag_media_to_timeline_clip('Landscape 01.jpg', 0, 1, 4)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-1-3_Overwrite_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("e2ceec19-5f87-4127-bcc6-c5d7139c4130") as case:
            # 4.1.4 Context Menu - 4.1 Image + Image (Ripple editing) - Overwrite
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-1-4_Overwrite_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-1-4_Overwrite_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to default
            main_page.click_undo()

        with uuid("24eb443e-f336-4912-84ac-c3bf0bedee15") as case:
            # 4.1.5 Context Menu - 4.1 Image + Image (Ripple editing) - Insert
            # Import 2nd clip into timeline
            media_room_page.hover_library_media('Landscape 02.jpg')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-1-5_Insert_undo.png')
            main_page.drag_media_to_timeline_clip('Landscape 01.jpg', 0, 1, 1)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-1-5_Insert_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("a328fb44-2828-4534-86dc-7d08030859ab") as case:
            # 4.1.6 Context Menu - 4.1 Image + Image (Ripple editing) - Insert
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-1-6_Insert_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-1-6_Insert_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to default
            main_page.click_undo()

        with uuid("0e3a5d86-f0af-4169-ae39-7dff09bd5680") as case:
            # 4.1.7 Context Menu - 4.1 Image + Image (Ripple editing) - Insert and move all clips
            # Import 2nd clip into timeline
            media_room_page.hover_library_media('Landscape 02.jpg')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-1-7_InsertMove_redo.png')
            main_page.drag_media_to_timeline_clip('Landscape 01.jpg', 0, 1, 2)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-1-7_InsertMove_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("52af51c7-679b-4d70-9c6a-6227020591ee") as case:
            # 4.1.8 Context Menu - 4.1 Image + Image (Ripple editing) - Insert and move all clips
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-1-8_InsertMove_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-1-8_InsertMove_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to default
            main_page.click_undo()

        with uuid("e227e9c3-979c-47f4-a236-56b1f73542dc") as case:
            # 4.1.9 Context Menu - 4.1 Image + Image (Ripple editing) - Crossfade
            # Import 2nd clip into timeline
            media_room_page.hover_library_media('Landscape 02.jpg')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-1-9_Crossfade_undo.png')
            main_page.drag_media_to_timeline_clip('Landscape 01.jpg', 0, 1, 3)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-1-9_Crossfade_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("d9043163-7a02-4d53-9ec4-b9e49a4a8626") as case:
            # 4.1.10 Context Menu - 4.1 Image + Image (Ripple editing) - Crossfade
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-1-10_Crossfade_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-1-10_Crossfade_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_4_2_1(self):
        with uuid("3360536b-8a4a-4387-86ab-8e8dd4066e89") as case:
            # 4.2.1 Context Menu - 4.2 Audio + Audio (Ripple editing) - Overwrite
            time.sleep(5)
            # Import 2 clips into timeline
            main_page.insert_media('Mahoroba.mp3')
            media_room_page.hover_library_media('Speaking Out.mp3')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-2-1_Overwrite_undo.png')
            main_page.drag_media_to_timeline_clip('Mahoroba.mp3', 0, 1, 0)
            # Expect Result: undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-2-1_Overwrite_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("04107656-b05f-4dab-b3da-8f30766e715e") as case:
            # 4.2.2 Context Menu - 4.2 Audio + Audio (Ripple editing) - Overwrite
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-2-2_Overwrite_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-2-2_Overwrite_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to default
            main_page.click_undo()

        with uuid("84165b67-97d8-425a-8ddb-b9e71158adcd") as case:
            # 4.2.3 Context Menu - 4.2 Audio + Audio (Ripple editing) - Overwrite
            # Import 2nd clip into timeline
            media_room_page.hover_library_media('Speaking Out.mp3')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-2-3_Overwrite_undo.png')
            main_page.drag_media_to_timeline_clip('Mahoroba.mp3', 0, 1, 4)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-2-3_Overwrite_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("8790ff9a-c946-427c-b203-6ab5b37e1949") as case:
            # 4.2.4 Context Menu - 4.2 Audio + Audio (Ripple editing) - Overwrite
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-2-4_Overwrite_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-2-4_Overwrite_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to default
            main_page.click_undo()

        with uuid("c73f4333-038e-458e-8db8-1e48276ad271") as case:
            # 4.2.5 Context Menu - 4.2 Audio + Audio (Ripple editing) - Insert
            # Import 2nd clip into timeline
            media_room_page.hover_library_media('Speaking Out.mp3')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-2-5_Insert_undo.png')
            main_page.drag_media_to_timeline_clip('Mahoroba.mp3', 0, 1, 1)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-2-5_Insert_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("de6ea313-0853-45fe-a28d-ee38d2fc240c") as case:
            # 4.2.6 Context Menu - 4.2 Audio + Audio (Ripple editing) - Insert
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-2-6_Insert_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-2-6_Insert_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to default
            main_page.click_undo()

        with uuid("10996413-b954-425a-bf1b-5861bb8da314") as case:
            # 4.2.7 Context Menu - 4.2 Audio + Audio (Ripple editing) - Insert and move all clips
            # Import 2nd clip into timeline
            media_room_page.hover_library_media('Speaking Out.mp3')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-2-7_InsertMove_redo.png')
            main_page.drag_media_to_timeline_clip('Mahoroba.mp3', 0, 1, 2)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-2-7_InsertMove_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("a1fd9bb3-648b-4cff-92f0-fd7dcdbd887d") as case:
            # 4.2.8 Context Menu - 4.2 Audio + Audio (Ripple editing) - Insert and move all clips
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-2-8_InsertMove_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-2-8_InsertMove_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to default
            main_page.click_undo()

        with uuid("8b9a1209-90b9-4bf5-83ac-c3b487b93940") as case:
            # 4.2.9 Context Menu - 4.2 Audio + Audio (Ripple editing) - Crossfade
            # Import 2nd clip into timeline
            media_room_page.hover_library_media('Speaking Out.mp3')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-2-9_Crossfade_undo.png')
            main_page.drag_media_to_timeline_clip('Mahoroba.mp3', 0, 1, 3)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-2-9_Crossfade_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("bafb29c7-af1b-4e4b-b3e3-52fa5304e2bf") as case:
            # 4.2.10 Context Menu - 4.2 Audio + Audio (Ripple editing) - Crossfade
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-2-10_Crossfade_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-2-10_Crossfade_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_4_3_1(self):
        with uuid("da20e03d-cffd-4307-af05-be56809ef39d") as case:
            # 4.3.1 Context Menu - 4.3 Video + Video (Ripple editing) - Overwrite
            time.sleep(5)
            # Import 2 clips into timeline
            main_page.insert_media('Skateboard 01.mp4')
            media_room_page.hover_library_media('Skateboard 02.mp4')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-3-1_Overwrite_undo.png')
            main_page.drag_media_to_timeline_clip('Skateboard 01.mp4', 0, 1, 0)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-3-1_Overwrite_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("48d0602e-2763-446c-af55-5714b373c25c") as case:
            # 4.3.2 Context Menu - 4.3 Video + Video (Ripple editing) - Overwrite
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-3-2_Overwrite_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-3-2_Overwrite_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to default
            main_page.click_undo()

        with uuid("f56e09ac-9b5f-4926-8296-90a35010be08") as case:
            # 4.3.3 Context Menu - 4.3 Video + Video (Ripple editing) - Overwrite
            # Import 2nd clip into timeline
            media_room_page.hover_library_media('Skateboard 02.mp4')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-3-3_Overwrite_undo.png')
            main_page.drag_media_to_timeline_clip('Skateboard 01.mp4', 0, 1, 4)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-3-3_Overwrite_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("54a1a0ec-a646-4edb-b34e-4cb0efb46caf") as case:
            # 4.3.4 Context Menu - 4.3 Video + Video (Ripple editing) - Overwrite
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-3-4_Overwrite_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-3-4_Overwrite_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to default
            main_page.click_undo()

        with uuid("26876c06-99c6-4690-aea1-012038fd1e2e") as case:
            # 4.3.5 Context Menu - 4.3 Video + Video (Ripple editing) - Insert
            # Import 2nd clip into timeline
            media_room_page.hover_library_media('Skateboard 02.mp4')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-3-5_Insert_undo.png')
            main_page.drag_media_to_timeline_clip('Skateboard 01.mp4', 0, 1, 1)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-3-5_Insert_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("ded13cd6-7be7-481d-b6e4-99b22d887016") as case:
            # 4.3.6 Context Menu - 4.3 Video + Video (Ripple editing) - Insert
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-3-6_Insert_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-3-6_Insert_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to default
            main_page.click_undo()

        with uuid("e4a2a23d-89f7-4ba1-aed8-a2225d4190b7") as case:
            # 4.3.7 Context Menu - 4.3 Video + Video (Ripple editing) - Insert and move all clips
            # Import 2nd clip into timeline
            media_room_page.hover_library_media('Skateboard 02.mp4')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-3-7_InsertMove_redo.png')
            main_page.drag_media_to_timeline_clip('Skateboard 01.mp4', 0, 1, 2)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-3-7_InsertMove_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("1660a6f6-9c66-416c-973f-e423f7491a86") as case:
            # 4.3.8 Context Menu - 4.3 Video + Video (Ripple editing) - Insert and move all clips
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-3-8_InsertMove_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-3-8_InsertMove_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Reset to default
            main_page.click_undo()

        with uuid("40272cda-d5ff-4e5f-a87c-dba735cb2e0c") as case:
            # 4.3.9 Context Menu - 4.3 Video + Video (Ripple editing) - Crossfade
            # Import 2nd clip into timeline
            media_room_page.hover_library_media('Skateboard 02.mp4')
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-3-9_Crossfade_undo.png')
            main_page.drag_media_to_timeline_clip('Skateboard 01.mp4', 0, 1, 3)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if expected
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-3-9_Crossfade_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("baf986a1-50a5-41a4-9eab-5b61d09bf64c") as case:
            # 4.3.10 Context Menu - 4.3 Video + Video (Ripple editing) - Crossfade
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Snapshot timeline to verify if expected
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-3-10_Crossfade_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-3-10_Crossfade_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_4_4_4_1(self):
        with uuid("3862e22b-d48e-49dc-9f36-3b97d5beb8af") as case:
            # 4.4.4.1 Link & Group - Link video & audio - Undo operation is correct
            time.sleep(5)
            # Import one clip into timeline
            main_page.insert_media('Skateboard 01.mp4')
            # Select target clip in timeline
            main_page.select_timeline_media('Skateboard 01.mp4')
            main_page.right_click()
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-4-4-1_undo.png')
            # Click from right click menu
            main_page.select_right_click_menu('Link/Unlink Video and Audio')
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            # Snapshot timeline to verify if video & audio are unlinked
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '4-4-4-1_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0e4fa0bd-5e8f-44ca-baae-69788943168b") as case:
            # 4.4.4.2 Link & Group - Link video & audio - Redo operation is correct
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            # Deselect current status
            media_room_page.media_filter_display_video_only()
            # Drag unlinked video in timeline to check the status
            timeline_operation_page.drag_single_media_move_to(0, 0, 35)
            # Snapshot timeline to verify if video & audio are unlinked correctly
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-4-4-2_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-4-4-2_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_4_4_4_3(self):
        with uuid("ff7f9acf-d88d-48f6-beba-9e3e55986c7f") as case:
            # 4.4.4.3 Link & Group - Group (image + audio) - Undo operation is correct
            time.sleep(5)
            # Import image and audio into timeline
            main_page.insert_media('Food.jpg')
            time.sleep(1)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(1)
            # Select video and audio at the same time
            main_page.select_timeline_media('Food.jpg')
            time.sleep(1)
            main_page.tap_SelectAll_hotkey()
            time.sleep(3)
            # Click from right click menu
            main_page.right_click()
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-4-4-3_undo.png')
            main_page.select_right_click_menu('Group/Ungroup Objects')
            # Drag unlinked video in timeline to check the status
            timeline_operation_page.drag_single_media_move_to(0, 0, 35)
            # Expect Result: Undo operation is correct
            main_page.click_undo()
            main_page.click_undo()
            # Snapshot timeline to verify if image and audio are grouped correctly
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-4-4-3_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("863380bc-7957-448e-958f-e2a020ddb5ee") as case:
            # 4.4.4.4 Link & Group - Group (image + audio) - Redo operation is correct
            # Expect Result: Redo operation is correct
            main_page.click_redo()
            main_page.click_redo()
            # Snapshot timeline to verify if image and audio are grouped correctly
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '4-4-4-4_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '4-4-4-4_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_5_1_1(self):
        with uuid("8e97acb1-a6d5-417b-963d-81c8567fd48d") as case:
            # 5.1.1 Tools & Fix Enhance - 5.1 Modify by Designer - PiP Designer - Undo operation is correct
            time.sleep(5)
            # Import one clip into timeline
            main_page.insert_media('Skateboard 01.mp4')
            # Enter pip room
            main_page.enter_room(4)
            time.sleep(2)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME)
            media_room_page.select_media_content('Dialog_06')
            tips_area_page.tips_area_insert_media_to_selected_track(option=3)
            # Select specific timecode to check result easily
            main_page.set_timeline_timecode('00_00_02_02')
            # Enter pip designer
            tips_area_page.tools.select_PiP_Designer()
            # Change one setting
            pip_designer_page.express_mode.unfold_properties_object_setting_tab()
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window, file_name=Auto_Ground_Truth_Folder + '5-1-1_undo.png')
            pip_designer_page.express_mode.drag_object_setting_opacity_slider(50)
            # Expect Result: Undo operation is correct
            pip_designer_page.tap_undo_btn()
            # Snapshot timeline to verify result in pip designer
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window, file_name=Auto_Ground_Truth_Folder + '5-1-1_undo.png')
            compare_result = pip_designer_page.compare(Ground_Truth_Folder + '5-1-1_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("468fcdd0-1059-465b-8d4e-b50591441aac") as case:
            # 5.1.2 Tools & Fix Enhance - 5.1 Modify by Designer - PiP Designer - Redo operation is correct
            # Expect Result: Redo operation is correct
            pip_designer_page.tap_redo_btn()
            # Snapshot timeline to verify result in pip designer
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window, file_name=Auto_Ground_Truth_Folder + '5-1-2_redo.png')
            compare_result = pip_designer_page.compare(Ground_Truth_Folder + '5-1-2_redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("bf059c80-3736-41d9-8968-a59a29dc147d") as case:
            # 5.1.3 Tools & Fix Enhance - 5.1 Modify by Designer - Mask Designer - Undo operation is correct
            # Exit pip designer page
            main_page.press_esc_key()
            main_page.handle_no_save_project_dialog(option='no')
            tips_area_page.tools.select_Mask_Designer()
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '5-1-3_undo.png')
            mask_designer_page.MaskDesigner_Apply_template(5)
            mask_designer_page.Edit_MaskDesigner_Invert_mask_SetCheck(check=True)
            # Expect Result: Undo operation is correct
            mask_designer_page.tap_MaskDesigner_Undo_btn()
            # Snapshot timeline to verify result in mask designer
            compare_result = media_room_page.compare(Ground_Truth_Folder + '5-1-3_undo.png', current_result)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("f0f2bad5-6ca5-444d-bf6f-1ff55aa1acfec") as case:
            # 5.1.4 Tools & Fix Enhance - 5.1 Modify by Designer - Mask Designer - Undo operation is correct
            # Expect Result: Redo operation is correct
            mask_designer_page.tap_MaskDesigner_Redo_btn()
            time.sleep(DELAY_TIME)
            # Snapshot timeline to verify result in mask designer
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '5-1-4_redo.png')
            time.sleep(DELAY_TIME)
            compare_result = media_room_page.compare(Ground_Truth_Folder + '5-1-4_redo.png', current_result)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_5_1_7(self):
        with uuid("d93cad90-def3-483c-af87-5a7d8d8eea1a") as case:
            # 5.1.7 Tools & Fix Enhance - 5.1 Modify by Designer - Video Speed - Undo operation is correct
            time.sleep(5)
            # Import one clip into timeline
            main_page.insert_media('Skateboard 01.mp4')
            # Exit video speed page
            tips_area_page.tools.select_VideoSpeed()
            # Set speed multiplier value = 2
            video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_SetValue(2)
            # Save change and back to main page
            video_speed_page.Edit_VideoSpeedDesigner_ClickOK()
            time.sleep(1)
            # Click undo
            main_page.click_undo()
            # Snapshot timeline to verify result
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '5-1-7_undo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '5-1-7_undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("4eac7314-0179-4a25-ba3e-8cab8288f754") as case:
            # 5.1.8 Tools & Fix Enhance - 5.1 Modify by Designer - Video Speed - Redo operation is correct
            # Click redo
            main_page.click_redo()
            # Snapshot timeline to verify result
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '5-1-8_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '5-1-8_redo.png', current_image, similarity=0.9)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_5_1_9(self):
        with uuid("e73acc0f-b47d-46a5-8b33-d19043be08e7") as case:
            # 5.1.9 Tools & Fix Enhance - 5.1 Modify by Designer - Blending Mode - Redo operation is correct
            time.sleep(5)
            # Import one color board into timeline
            media_room_page.enter_color_boards()
            main_page.click_library_details_view()
            media_room_page.sound_clips_select_media('2, 185, 253')
            #main_page.select_library_icon_view_media('0,175,255')
            tips_area_page.click_TipsArea_btn_insert()
            main_page.click_library_icon_view()
            # Import one clip into track 2
            main_page.timeline_select_track(2)
            media_room_page.enter_media_content()
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            tips_area_page.click_TipsArea_btn_insert()
            # Select video clip to enter blending mode
            main_page.select_timeline_media('Skateboard 01.mp4')
            tips_area_page.tools.select_Blending_Mode()
            blending_mode_page.set_blending_mode('Hue')
            blending_mode_page.click_ok()
            # Click undo to reset
            main_page.click_undo()
            time.sleep(DELAY_TIME)
            # Snapshot timeline to verify result
            current_image = title_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '5-1-9_undo.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '5-1-9_undo.png', current_image, similarity=0.9)
            case.result = compare_result

        with uuid("92deacf4-6676-4740-8343-d1556476071b") as case:
            # 5.1.10 Tools & Fix Enhance - 5.1 Modify by Designer - Blending Mode - Redo operation is correct
            # Expect Result: Redo operation is correct
            # Click redo to reset
            main_page.click_redo()
            time.sleep(DELAY_TIME)
            # Snapshot timeline to verify result
            current_image = title_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '5-1-10_redo.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '5-1-10_redo.png', current_image)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_5_1_13(self):
        with uuid("4fe86a6b-1db1-4f17-8d59-a4070bf04faf") as case:
            # 5.1.13 Tools & Fix Enhance - Video Collage Designer - Undo operation is correct
            time.sleep(5)
            # Enter video collage designer page and fill 2 video clips
            main_page.top_menu_bar_plugins_video_collage_designer()
            video_collage_designer_page.layout.select_layout(2)
            video_collage_designer_page.media.select_category(1)

            video_collage_designer_page.media.click_auto_fill()
            video_collage_designer_page.click_ok()

            # Enter video collage designer page again to adjust border size
            tips_area_page.tips_area_click_video_collage()
            video_collage_designer_page.border.enable_border(1)
            video_collage_designer_page.border.set_border_value('100')
            video_collage_designer_page.click_ok()
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '5-1-13_undo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '5-1-13_undo.png', current_result)

            # Select specific timecode to verify easily
            main_page.set_timeline_timecode('00_00_03_00')
            time.sleep(DELAY_TIME * 2)
            # Snapshot library preview to verify result
            case.result = compare_result

        with uuid("0acb47b8-9f78-417f-81dc-1bf8c87f399e") as case:
            # 5.1.14 Tools & Fix Enhance - Video Collage Designer - Redo operation is correct
            # Click redo
            main_page.click_redo()
            # Select specific timecode to verify easily
            main_page.set_timeline_timecode('00_00_04_00')
            time.sleep(DELAY_TIME*2)
            # Snapshot library preview to verify result
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '5-1-14_redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '5-1-14_redo.png', current_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_5_2_1(self):
        with uuid("784405b7-15cf-4ad7-85b6-001c32b88c56") as case:
            # 5.2.1 Modify by Fix Enhance - White Balance - Undo operation is correct
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            # Import clip into timeline
            main_page.insert_media('Skateboard 03.mp4')
            # Seek to specific timecode
            main_page.set_timeline_timecode('00_00_05_11', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick WB option
            fix_enhance_page.fix.enable_white_balance()
            # Change value of tint
            fix_enhance_page.fix.white_balance.tint.set_value(90)
            # Click undo
            main_page.click_undo()
            # Snapshot library preview to verify result
            current_result = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '5-2-1_WB_Undo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '5-2-1_WB_Undo.png', current_result)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("9b9c16e5-748e-4eb7-8311-3602529a9127") as case:
            # 5.2.2 Modify by Fix Enhance - White Balance - Redo operation is correct
            # Click redo
            main_page.click_redo()
            # Snapshot library preview to verify result
            current_result = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '5-2-1_WB_Redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '5-2-1_WB_Redo.png', current_result)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("83d5a0de-edfc-4fa2-8cd5-17d808837aca") as case:
            # 5.2.3 Modify by Fix Enhance - Lens Correction - Undo operation is correct
            # Tick lens correction option - GoPro HERO7 Black (Wide)
            fix_enhance_page.fix.enable_lens_correction()
            fix_enhance_page.fix.lens_correction.select_marker_type('GoPro')
            fix_enhance_page.fix.lens_correction.select_model_type(18)
            # Click undo
            main_page.click_undo()
            # Snapshot library preview to verify result
            current_result = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '5-2-3_Lens_Undo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '5-2-3_Lens_Undo.png', current_result)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("52ea5df5-dbb4-4521-a83f-f443da48f4d3") as case:
            # 5.2.4 Modify by Fix Enhance - Lens Correction	- Redo operation is correct
            # Click redo
            main_page.click_redo()
            # Snapshot library preview to verify result
            current_result = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '5-2-4_Lens_Redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '5-2-4_Lens_Redo.png', current_result)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("7d3ad286-6289-4dba-a989-b998396f11ce") as case:
            # 5.2.4 Modify by Fix Enhance - Audio Denoise - Undo operation is correct
            # Tick audio denoise option
            fix_enhance_page.fix.enable_audio_denoise()
            # Check if switch to "Wind noise" noise type
            fix_enhance_page.fix.audio_denoise.set_noise_type(1)
            fix_enhance_page.fix.audio_denoise.degree.adjust_slider(55)
            # Click undo
            main_page.click_undo()
            # Verify result if value is back to 50
            degree_value = fix_enhance_page.fix.audio_denoise.degree.get_value()
            logger(f"{degree_value= }")
            if not degree_value == '50':
                result = False
            else:
                result = True
            case.result = result

        with uuid("9cd0f0b5-580b-4f64-bd67-b95b5cc28f23") as case:
            # 5.2.5 Modify by Fix Enhance - Audio Denoise - Redo operation is correct
            # Click redo
            main_page.click_redo()
            # Verify result if value is back to 55
            degree_value = fix_enhance_page.fix.audio_denoise.degree.get_value()
            logger(f"{degree_value= }")
            if not degree_value == '55':
                result = False
            else:
                result = True
            case.result = result

        with uuid("032c4bed-35a2-4122-b30e-7714837e91ae") as case:
            # 5.2.7 Modify by Fix Enhance - Color Adjustment - Undo operation is correct
            # Tick color adjustment option
            case.result = fix_enhance_page.enhance.switch_to_color_adjustment()
            # Change Exposure setting to 100
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(150)
            # Click undo
            main_page.click_undo()
            time.sleep(1)
            # Snapshot library preview to verify result
            current_result = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '5-2-7_Color_Undo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '5-2-7_Color_Undo.png', current_result)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("e3c71a5a-7eb4-42c9-bc7d-9a701ed9a372") as case:
            # 5.2.8 Modify by Fix Enhance - Color Adjustment - Undo operation is correct
            # Click redo
            main_page.click_redo()
            time.sleep(1)
            # Snapshot library preview to verify result
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '5-2-8_Color_Redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '5-2-8_Color_Redo.png', current_result)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_6_6_1(self):
        with uuid("89c997cc-8724-4cdd-bda0-30bbd8bd4a6d") as case:
            # 6.6.1.1 Keyframe - 6.1 Fix Enhance - Audio Denoise - Undo operation is correct
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            # Import clip into timeline
            main_page.insert_media('Skateboard 01.mp4')
            # Enter keyframe room
            tips_area_page.click_keyframe()
            # Change timecode
            library_preview_page.set_library_preview_window_timecode('00_00_04_00')
            # Change setting for Audio Denoise
            keyframe_room_page.fix_enhance.unfold_tab(value=1)

            unfold_fix_enhance = keyframe_room_page.fix_enhance.show()

            logger(f"{unfold_fix_enhance= }")
            keyframe_room_page.drag_scroll_bar(0.22)
            keyframe_room_page.fix_enhance.audio_denoise.unfold_tab(value=1)

            keyframe_room_page.fix_enhance.audio_denoise.show()
            keyframe_room_page.fix_enhance.audio_denoise.noise.set_type(2)

            # Change timecode
            library_preview_page.set_library_preview_window_timecode('00_00_04_20')
            # Change setting for Audio Denoise
            keyframe_room_page.fix_enhance.audio_denoise.noise.set_type(1)
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME*2)

            image_audio_undo = Auto_Ground_Truth_Folder + '6_6_1_1_AudioDenoise_Undo.png'
            ground_truth = Ground_Truth_Folder + '6_6_1_1_AudioDenoise_Undo.png'

            # Snapshot status to check undo result
            current_preview = main_page.snapshot(locator=L.keyframe_room.main_window,
                                                file_name=image_audio_undo)

            check_result = main_page.compare(ground_truth, current_preview)
            logger(check_result)
            case.result = check_result

        with uuid("8df40f4e-90e6-435a-a51b-79991dec65f3") as case:
            # 6.6.1.2 Keyframe - 6.1 Fix Enhance - Audio Denoise - Redo operation is correct
            # Click redo
            main_page.click_redo()
            # Snapshot library preview to verify result
            image_redo = Auto_Ground_Truth_Folder + '6_6_1_2_AudioDenoise_Redo.png'
            ground_truth = Ground_Truth_Folder + '6_6_1_2_AudioDenoise_Redo.png'

            # Snapshot status to check undo result
            current_preview = main_page.snapshot(locator=L.keyframe_room.main_window,
                                                file_name=image_redo)

            check_result = main_page.compare(ground_truth, current_preview)
            logger(check_result)
            case.result = check_result


        with uuid("9dce80a7-7f7a-4a15-8db3-9bbee3b1ce78") as case:
            # 6.6.1.3 Keyframe - 6.1 Fix Enhance - Color Adjustment - undo operation is correct
            library_preview_page.set_library_preview_window_timecode('00_00_04_50')
            # Change setting for Color Adjustment
            keyframe_room_page.fix_enhance.color_adjustment.exposure.show()
            keyframe_room_page.fix_enhance.color_adjustment.exposure.set_value('61')
            # Click undo
            main_page.click_undo()
            # Snapshot library preview to verify result
            image_undo = Auto_Ground_Truth_Folder + '6_6_1_3_ColorAdj_Undo.png'
            ground_truth = Ground_Truth_Folder + '6_6_1_3_ColorAdj_Undo.png'

            # Snapshot status to check undo result
            current_preview = main_page.snapshot(locator=L.keyframe_room.main_window,
                                                file_name=image_undo)

            check_result = main_page.compare(ground_truth, current_preview)
            logger(check_result)
            case.result = check_result

        with uuid("84f4692a-f75f-428c-860a-27679f68ce00") as case:
            # 6.6.1.4 Keyframe - 6.1 Fix Enhance - Color Adjustment - undo operation is correct
            # Click redo
            main_page.click_redo()
            # Snapshot library preview to verify result
            current_result = keyframe_room_page.snapshot(locator=L.keyframe_room.main_window, file_name=Auto_Ground_Truth_Folder + '6-6-1-4_ColorAdj_Redo.png')
            time.sleep(DELAY_TIME)

            image_redo = Auto_Ground_Truth_Folder + '6-6-1-4_ColorAdj_Redo.png'
            ground_truth = Ground_Truth_Folder + '6-6-1-4_ColorAdj_Redo.png'

            # Snapshot status to check undo result
            current_preview = main_page.snapshot(locator=L.keyframe_room.main_window,
                                                file_name=image_redo)

            check_result = main_page.compare(ground_truth, current_preview)
            logger(check_result)
            case.result = check_result

        with uuid("e71235fc-bb6f-4c82-9da8-8c8c71132861") as case:
            # 6.6.1.5 Keyframe - 6.1 Fix Enhance - WB - undo operation is correct
            library_preview_page.set_library_preview_window_timecode('00_00_05_20')
            # Change setting for White Balance
            keyframe_room_page.fix_enhance.white_balance.show()
            keyframe_room_page.fix_enhance.white_balance.color_temperature.show()
            keyframe_room_page.fix_enhance.white_balance.select_color_temperature()
            keyframe_room_page.fix_enhance.white_balance.color_temperature.set_value('54')
            # Click undo
            main_page.click_undo()
            # Snapshot library preview to verify result
            image_undo = Auto_Ground_Truth_Folder + '6_6_1_5_WB_Undo.png'
            ground_truth = Ground_Truth_Folder + '6_6_1_5_WB_Undo.png'

            # Snapshot status to check undo result
            current_preview = main_page.snapshot(locator=L.keyframe_room.main_window,
                                                 file_name=image_undo)

            check_result = main_page.compare(ground_truth, current_preview)
            logger(check_result)
            case.result = check_result

        with uuid("125aef90-25d9-4da1-864e-f3764c20ab1a") as case:
            # 6.6.6 Keyframe - 6.1 Fix Enhance - WB - undo operation is correct
            # Click redo
            main_page.click_redo()
            # Snapshot library preview to verify result
            image_redo = Auto_Ground_Truth_Folder + '6_6_1_6_WB_Redo.png'
            ground_truth = Ground_Truth_Folder + '6_6_1_6_WB_Redo.png'

            # Snapshot status to check undo result
            current_preview = main_page.snapshot(locator=L.keyframe_room.main_window,
                                                 file_name=image_redo)

            check_result = main_page.compare(ground_truth, current_preview)
            logger(check_result)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_6_6_2_1(self):
        with uuid("56d21216-f915-4f7c-9db2-565937001cfe") as case:
            # 6.6.2.1 Keyframe - 6.2 Effect - Parameters - Undo operation is correct
            time.sleep(5)
            # Import clip into timeline
            main_page.insert_media('Skateboard 02.mp4')
            # Apply effect from effect room
            main_page.enter_room(3)

            main_page.enter_room(0)
            time.sleep(DELAY_TIME*2)
            main_page.enter_room(3)

            main_page.drag_media_to_timeline_playhead_position('Back Light')
            # Enter keyframe room
            tips_area_page.click_keyframe()
            # Change timecode
            library_preview_page.set_library_preview_window_timecode('00_00_02_00')
            # Change setting for effect
            keyframe_room_page.effect.unfold_tab(value=1)
            keyframe_room_page.effect.aberration.strength.set_value('8')

            # Click undo
            main_page.click_undo()
            # Snapshot library preview to verify result
            image_undo = Auto_Ground_Truth_Folder + '6_6_2_1_Parameters_Undo.png'
            ground_truth = Ground_Truth_Folder + '6_6_2_1_Parameters_Undo.png'

            # Snapshot status to check undo result
            current_preview = main_page.snapshot(locator=L.keyframe_room.main_window,
                                                 file_name=image_undo)

            check_result = main_page.compare(ground_truth, current_preview)
            logger(check_result)
            case.result = check_result

        with uuid("b66f9767-f2fe-4394-872a-75d0542e5a29") as case:
            # 6.6.2.2 Keyframe - 6.2 Effect - Parameters - Redo operation is correct
            # Click redo
            main_page.click_redo()
            # Snapshot library preview to verify result
            image_redo = Auto_Ground_Truth_Folder + '6_6_2_2_Parameters_Redo.png'
            ground_truth = Ground_Truth_Folder + '6_6_2_2_Parameters_Redo.png'

            # Snapshot status to check undo result
            current_preview = main_page.snapshot(locator=L.keyframe_room.main_window,
                                                 file_name=image_redo)

            check_result = main_page.compare(ground_truth, current_preview)
            logger(check_result)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_6_6_2_3(self):
        with uuid("e164f76a-f48c-4b5b-9416-f844f6a0d769") as case:
            # 6.6.2.3 Keyframe - 6.2 Effect - Color - Undo operation is correct
            time.sleep(5)
            # Import clip into timeline
            main_page.insert_media('Skateboard 02.mp4')
            # Apply effect from effect room
            main_page.enter_room(3)
            # Apply color effect from effect room
            effect_room_page.search_and_input_text('aberration')
            main_page.drag_media_to_timeline_playhead_position('Aberration')
            # Enter keyframe room
            tips_area_page.click_keyframe()
            # Change timecode
            library_preview_page.set_library_preview_window_timecode('00_00_05_01')
            # Change setting for effect
            keyframe_room_page.effect.unfold_tab(value=1)
            keyframe_room_page.effect.aberration.strength.set_value(10)

            # Click undo
            main_page.click_undo()
            # Snapshot library preview to verify result
            image_undo = Auto_Ground_Truth_Folder + '6_6_2_3_Aberration_Undo.png'
            ground_truth = Ground_Truth_Folder + '6_6_2_3_Aberration_Undo.png'

            # Snapshot status to check undo result
            current_preview = main_page.snapshot(locator=L.keyframe_room.main_window,
                                                 file_name=image_undo)

            check_result = main_page.compare(ground_truth, current_preview)
            logger(check_result)

            case.result = check_result

        with uuid("3b4fcdb7-c167-42ab-b025-3de019da3116") as case:
            # 6.6.2.4 Keyframe - 6.2 Effect - Color - Redo operation is correct
            # Click redo
            main_page.click_redo()
            # Snapshot library preview to verify result
            image_redo = Auto_Ground_Truth_Folder + '6_6_2_4_Aberration_Redo.png'
            ground_truth = Ground_Truth_Folder + '6_6_2_4_Aberration_Redo.png'

            # Snapshot status to check undo result
            current_preview = main_page.snapshot(locator=L.keyframe_room.main_window,
                                                 file_name=image_redo)

            check_result = main_page.compare(ground_truth, current_preview)
            logger(check_result)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_6_6_3_1(self):
        with uuid("dc93346e-66ec-4035-a411-c258c5fe7163") as case:
            # 6.6.3.1 Clip Attributes - Position - Undo operation is correct
            time.sleep(5)
            # Import clip into timeline
            main_page.insert_media('Skateboard 03.mp4')
            # Apply effect from effect room
            main_page.enter_room(3)
            # Apply color effect from effect room
            effect_room_page.search_and_input_text('color')
            main_page.drag_media_to_timeline_playhead_position('Color Crayon')
            # Enter keyframe room
            tips_area_page.click_keyframe()
            # Change timecode
            library_preview_page.set_library_preview_window_timecode('00_00_02_10')
            # Change setting for Clip Attributes
            keyframe_room_page.clip_attributes.unfold_tab(value=1)
            current_result_2 = keyframe_room_page.snapshot(locator=L.keyframe_room.main_window, file_name=Auto_Ground_Truth_Folder + '6-6-3-1_ClipAttributes_Undo.png')
            keyframe_room_page.clip_attributes.position.x.set_value(value='0.200')
            keyframe_value = keyframe_room_page.clip_attributes.position.x.get_value(index_node=0)
            current_result_1 = False if not keyframe_value == '0.200' else True
            current_result_3 = keyframe_room_page.snapshot(locator=L.keyframe_room.main_window, file_name=Auto_Ground_Truth_Folder + '6-6-3-2_ClipAttributes_Redo.png')
            # Click undo
            main_page.click_undo()
            logger(f"{current_result_1= }")
            compare_result = keyframe_room_page.compare(Ground_Truth_Folder + '6-6-3-1_ClipAttributes_Undo.png', current_result_2)
            logger(f"{compare_result= }")
            case.result = current_result_1 and compare_result

        with uuid("63d214ba-571a-4e80-9fdc-aac74fcbce3f") as case:
            # 6.6.3.2 Clip Attributes - Position - Redo operation is correct
            # Click redo
            main_page.click_redo()
            # Snapshot library preview to verify result
            compare_result = keyframe_room_page.compare(Ground_Truth_Folder + '6-6-3-2_ClipAttributes_Redo.png', current_result_3)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("e1c30b51-92d7-4c47-802e-84dbb2b2b8ba") as case:
            # 6.6.3.3 Keyframe - Scale (Width & Height) - Undo operation is correct
            library_preview_page.set_library_preview_window_timecode('00_00_02_20')
            keyframe_room_page.clip_attributes.scale.show()
            current_result = keyframe_room_page.snapshot(locator=L.keyframe_room.main_window, file_name=Auto_Ground_Truth_Folder + '6-6-3-3_Scale_Undo.png')
            keyframe_room_page.clip_attributes.scale.width.set_slider(value=0.4)
            keyframe_scale_value = keyframe_room_page.clip_attributes.scale.width.get_value(index_node=0)
            check_result_4 = False if not keyframe_scale_value == '0.400' else True
            current_result_4 = keyframe_room_page.snapshot(locator=L.keyframe_room.main_window, file_name=Auto_Ground_Truth_Folder + '6-6-3-4_Scale_Redo.png')
            # Click undo
            main_page.click_undo()
            logger(f"{current_result_4= }")
            compare_result = keyframe_room_page.compare(Ground_Truth_Folder + '6-6-3-3_Scale_Undo.png', current_result, similarity=0.9)
            logger(f"{compare_result= }")
            case.result = check_result_4 and compare_result

        with uuid("a9882b26-f19e-4607-8661-4ba28454abd7") as case:
            # 6.6.3.4 Keyframe - Scale (Width & Height) - Redo operation is correct
            # Click redo
            main_page.click_redo()
            # Snapshot library preview to verify result
            compare_result = keyframe_room_page.compare(Ground_Truth_Folder + '6-6-3-4_Scale_Redo.png', current_result_4)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("9413039c-398c-4a82-bcdd-cb50538807bb") as case:
            # 6.6.3.5 Keyframe - Opacity - Setting value - Undo operation is correct
            library_preview_page.set_library_preview_window_timecode('00_00_02_30')
            keyframe_room_page.clip_attributes.opacity.show()
            current_result = keyframe_room_page.snapshot(locator=L.keyframe_room.main_window, file_name=Auto_Ground_Truth_Folder + '6-6-3-5_Opacity_Undo.png')
            keyframe_room_page.clip_attributes.opacity.set_slider(value=50)
            keyframe_opacity_value = keyframe_room_page.clip_attributes.opacity.get_value(index_node=0)
            check_result_5 = False if not keyframe_opacity_value == '50' else True
            current_result_5 = keyframe_room_page.snapshot(locator=L.keyframe_room.main_window, file_name=Auto_Ground_Truth_Folder + '6-6-3-6_Opacity_Redo.png')
            # Click undo
            main_page.click_undo()
            logger(f"{current_result_5= }")
            compare_result = keyframe_room_page.compare(Ground_Truth_Folder + '6-6-3-5_Opacity_Undo.png', current_result, similarity=0.9)
            logger(f"{compare_result= }")
            case.result = check_result_5 and compare_result

        with uuid("18203e5f-a501-41a9-9d1b-1c90bea02868") as case:
            # 6.6.3.6 Keyframe - Opacity - Setting value - Redo operation is correct
            # Click redo
            main_page.click_redo()
            # Snapshot library preview to verify result
            compare_result = keyframe_room_page.compare(Ground_Truth_Folder + '6-6-3-6_Opacity_Redo.png', current_result_5)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("307500b2-f8cc-4372-a8a7-2a43b4b1bfe9") as case:
            # 6.6.3.7 Keyframe - Opacity - Blending - Undo operation is correct
            library_preview_page.set_library_preview_window_timecode('00_00_02_40')
            current_result = keyframe_room_page.snapshot(locator=L.keyframe_room.main_window, file_name=Auto_Ground_Truth_Folder + '6-6-3-7_OpacityBlending_Undo.png')
            keyframe_room_page.clip_attributes.opacity.set_blending_mode(index_option=5, index_node=-1)
            keyframe_opacity_blending = keyframe_room_page.clip_attributes.opacity.get_blending_mode(index_node=5)
            check_result_6 = False if not keyframe_opacity_blending == 'Screen' else True
            current_result_6 = keyframe_room_page.snapshot(locator=L.keyframe_room.main_window, file_name=Auto_Ground_Truth_Folder + '6-6-3-8_OpacityBlending_Redo.png')
            # Click undo
            main_page.click_undo()
            logger(f"{check_result_6= }")
            compare_result = keyframe_room_page.compare(Ground_Truth_Folder + '6-6-3-5_Opacity_Undo.png', current_result)
            logger(f"{compare_result= }")
            case.result = check_result_6 and compare_result

        with uuid("df26b14c-7cb4-4921-b65f-872a36232d03") as case:
            # 6.6.3.8 Keyframe - Opacity - Blending - Redo operation is correct
            # Click redo
            main_page.click_redo()
            # Snapshot library preview to verify result
            compare_result = keyframe_room_page.compare(Ground_Truth_Folder + '6-6-3-8_OpacityBlending_Redo.png', current_result_6)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("30dfa319-d4f8-4bd7-925e-83d66b5701a6") as case:
            # 6.6.3.9 Keyframe - Rotation - Undo operation is correct
            library_preview_page.set_library_preview_window_timecode('00_00_03_10')
            keyframe_room_page.clip_attributes.rotation.show()
            current_result = keyframe_room_page.snapshot(locator=L.keyframe_room.main_window, file_name=Auto_Ground_Truth_Folder + '6-6-3-9_Rotation_Undo.png')
            keyframe_room_page.clip_attributes.rotation.set_value(value='-90')
            keyframe_rotation_value = keyframe_room_page.clip_attributes.rotation.get_value(index_node=0)
            check_result_7 = False if not keyframe_rotation_value == '-90.00' else True
            current_result_7 = keyframe_room_page.snapshot(locator=L.keyframe_room.main_window, file_name=Auto_Ground_Truth_Folder + '6-6-3-10_Rotation_Redo.png')
            # Click undo
            main_page.click_undo()
            logger(f"{check_result_7= }")
            compare_result = keyframe_room_page.compare(Ground_Truth_Folder + '6-6-3-9_Rotation_Undo.png', current_result)
            logger(f"{compare_result= }")
            case.result = check_result_7 and compare_result

        with uuid("f949932a-78df-498a-887f-ca40b99e736f") as case:
            # 6.6.3.10 Keyframe - Rotation - Redo operation is correct
            # Click redo
            main_page.click_redo()
            # Snapshot library preview to verify result
            compare_result = keyframe_room_page.compare(Ground_Truth_Folder + '6-6-3-10_Rotation_Redo.png', current_result_7)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("d6f727bf-fcea-490d-9e35-94507d46a802") as case:
            # 6.6.3.11 Keyframe - Freeform - Undo operation is correct
            library_preview_page.set_library_preview_window_timecode('00_00_03_30')
            keyframe_room_page.clip_attributes.freeform.show()
            current_result = keyframe_room_page.snapshot(locator=L.keyframe_room.main_window, file_name=Auto_Ground_Truth_Folder + '6-6-3-11_Freedom_Undo.png')
            keyframe_room_page.clip_attributes.freeform.add_remove_keyframe()  # 00;00;00;00
            keyframe_room_page.clip_attributes.freeform.top_left_x.set_value('0.1')
            keyframe_freedom_value = keyframe_room_page.clip_attributes.freeform.top_left_x.get_value(index_node=0)
            check_result_8 = False if not keyframe_freedom_value == '0.100' else True
            current_result_8 = keyframe_room_page.snapshot(locator=L.keyframe_room.main_window, file_name=Auto_Ground_Truth_Folder + '6-6-3-12_Freedom_Redo.png')
            # Click undo
            main_page.click_undo()
            logger(f"{check_result_8= }")
            compare_result = keyframe_room_page.compare(Ground_Truth_Folder + '6-6-3-11_Freedom_Undo.png', current_result)
            logger(f"{compare_result= }")
            case.result = check_result_8 and compare_result

        with uuid("3d226930-2783-41c6-b5c8-5817b449ee50") as case:
            # 6.6.3.12 Keyframe - Freeform - Redo operation is correct
            # Click redo
            main_page.click_redo()
            # Snapshot library preview to verify result
            compare_result = keyframe_room_page.compare(Ground_Truth_Folder + '6-6-3-12_Freedom_Redo.png', current_result_8)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_6_6_4_1(self):
        with uuid("141b0875-8a4d-4a4f-b38c-d0a1b0f09295") as case:
            # 6.6.4.1 Keyframe - Volume - Undo operation is correct
            time.sleep(5)
            # Import clip into timeline
            main_page.insert_media('Skateboard 01.mp4')
            # Enter keyframe room
            tips_area_page.click_keyframe()
            # Change setting for volume
            keyframe_room_page.volume.show()

            keyframe_room_page.volume.set_slider(value=80)
            current_volume_value = keyframe_room_page.volume.get_value(index_node=0)
            check_result_9 = False if not current_volume_value == '10.1' else True

            # Click undo
            main_page.click_undo()

            image_undo = Auto_Ground_Truth_Folder + '6_6_4_1_Volume_Undo.png'
            ground_truth = Ground_Truth_Folder + '6_6_4_1_Volume_Undo.png'

            # Snapshot status to check undo result
            current_preview = main_page.snapshot(locator=L.keyframe_room.main_window,
                                                 file_name=image_undo)
            check_result = main_page.compare(ground_truth, current_preview)
            #logger(check_result)
            case.result = check_result_9 and check_result

        with uuid("141b0875-8a4d-4a4f-b38c-d0a1b0f09295") as case:
            # 6.6.4.2 Keyframe - Volume - Undo operation is correct
            # Click redo
            main_page.click_redo()
            # Snapshot library preview to verify result
            image_redo = Auto_Ground_Truth_Folder + '6_6_4_2_Volume_Redo.png'
            ground_truth = Ground_Truth_Folder + '6_6_4_2_Volume_Redo.png'

            # Snapshot status to check undo result
            current_preview = main_page.snapshot(locator=L.keyframe_room.main_window,
                                                 file_name=image_redo)
            check_result = main_page.compare(ground_truth, current_preview)
            #logger(check_result)
            case.result = check_result

    ################
    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    # 1.1.10
                    2a299acb-5926-4d66-85d1-315bc1052e01
                    # 1.2.10
                    2a299acb-5926-4d66-85d1-315bc1052e01                    
                    # 2.2.4.8
                    5f844ce7-ee55-4fdf-95cc-ee2997e7d244
                    # 2.4
                    7bab4dd1-46ef-4da6-86d6-270149be7ab7
                    270bc865-a522-4a15-b357-1c2b447c61fc
                    0bd53ba3-7b82-4536-9aed-9540cd2ef664
                    daeb42e8-5d0f-45c7-a0f8-d170aba8be07
                    63ed9943-35da-48c3-92d2-0c3bb21fb157
                    b31c9eae-e75d-4612-9bb7-ddf4cc539fc3
                    ce66e289-6fea-47d7-b139-99769827afc8
                    5f844ce7-ee55-4fdf-95cc-ee2997e7d244
                    # 4.3 Speed Up to Fit	
                    8dfa80ec-333c-4b42-8446-343b3b2e6eaf
                    d60569da-4a72-4904-b204-3e908018dab0
                    # 5.1.5 Crop/Zoom/Pan
                    a5a490a2-99d0-4fbb-87ec-8f7c95e0882a
                    ed5d4905-901d-4237-aa24-9d9c25f7cbbd
                    # 5.1.11 Magic Motion Designer	
                    c43d1aea-c907-4134-adb8-32a12a58ba31
                    c2cbe047-309c-4cbb-bdb6-b9646227f83f
                ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"