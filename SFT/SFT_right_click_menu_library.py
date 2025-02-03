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
pip_designer_page = PageFactory().get_page_object('pip_designer_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Right Click Menu (Library).html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Right_Click_Menu_Library/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Right_Click_Menu_Library/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Right_Click_Menu_Library():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME*4)
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
            google_sheet_execution_log_init('Right_Click_Menu_Library')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"right click menu-library result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        with uuid('1b4e2707-c8b4-4474-943f-97f397395b98') as case:
            # 1. Media Room
            # 1.1. Right click on image
            # 1.1.1. insert to selected track > add right clicked clip to selected track
            media_room_page.hover_library_media('Food.jpg')
            media_room_page.library_clip_context_menu_insert_on_selected_track()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_1_1_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_1_1_1.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            media_room_page.tap_Remove_hotkey()

        with uuid('f264617c-02f9-4dac-af25-51ea5b180f17') as case:
            # 1.1. Right click on image
            # 1.1.2. remove from library > remove clicked clip from library
            media_room_page.hover_library_media('Food.jpg')
            media_room_page.library_clip_context_menu_remove_from_library()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_1_2_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_1_2_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('3dc15e08-2b30-4f1c-b92a-637e98cfbef2') as case:
            # 1.1. Right click on image
            # 1.1.4. Add to > add to custom tag
            media_room_page.add_new_tag('custom_tag')
            media_room_page.hover_library_media('Landscape 01.jpg')
            media_room_page.library_clip_context_menu_add_to('custom_tag')
            media_room_page.select_specific_category('custom_tag')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_1_4_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_1_4_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('37c25004-6c57-49a8-b5bf-561b802ba69e') as case:
            # 1.1. Right click on image
            # 1.1.5. Change Alias > change clip name in library
            media_room_page.hover_library_media('Landscape 01.jpg')
            media_room_page.library_clip_context_menu_change_alias('change_alias')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_1_5_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_1_5_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('3766407d-383a-4be2-b29e-e715e332ff85') as case:
            # 1.1. Right click on image
            # 1.1.6. Reset Alias > reset clip name
            media_room_page.hover_library_media('change_alias')
            check_result = media_room_page.library_clip_context_menu_reset_alias('Landscape 01.jpg')
            case.result = check_result

        with uuid('fbeda66e-33ab-478c-920a-f9e38cc483be') as case:
            # 1.1. Right click on image
            # 1.1.7. Rotate Right > rotate selected image
            media_room_page.hover_library_media('Landscape 01.jpg')
            media_room_page.library_clip_context_menu_rotate_right()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_1_7_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_1_7_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('5cdd018d-2a76-42fb-ad35-fc12c8ba8e46') as case:
            # 1.1. Right click on image
            # 1.1.8. Rotate Left > rotate selected image
            media_room_page.hover_library_media('Landscape 01.jpg')
            media_room_page.library_clip_context_menu_rotate_left()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_1_8_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_1_8_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('eef3a46d-ed6a-40aa-8da9-a95b1e381942') as case:
            # 1.1. Right click on image
            # 1.1.10. Pre-cut > should disable
            media_room_page.hover_library_media('Landscape 01.jpg')
            main_page.right_click()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_1_10_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_1_10_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.press_esc_key()

        with uuid('cbe2b1ad-bfc7-4e46-a077-f6f48e6a3610') as case:
            # 1.1. Right click on image
            # 1.1.17. Open File Location > open windows file browser to clip location
            media_room_page.hover_library_media('Landscape 01.jpg')
            check_result = media_room_page.library_clip_context_menu_open_file_location()
            case.result = check_result

        with uuid('89f1be4b-c7b4-437f-8bb2-6fd07e71f46f') as case:
            # 1.1. Right click on image
            # 1.1.18. Dock/Undock Library Window > operation
            # dock or undock library windows
            media_room_page.hover_library_media('Landscape 01.jpg')
            check_result = media_room_page.library_clip_context_menu_dock_undock_library_window()
            case.result = check_result

        with uuid('ad6c77da-c159-464f-b176-78ad3fa83eb4') as case:
            # 1.1. Right click on image
            # 1.1.18. Dock/Undock Library Window > minimize
            # able to minimize window
            check_result = media_room_page.undock_library_window_click_minimize()
            case.result = check_result

        with uuid('28ad488c-8838-4890-b617-b342dac5aea9') as case:
            # 1.1. Right click on image
            # 1.1.18. Dock/Undock Library Window > minimize
            # show "Media Library" button in upper-right
            check_result = media_room_page.is_exist(L.media_room.top_tool_bar.btn_show_minimized_library_window)
            case.result = check_result

        with uuid('45398a5c-4390-4af2-87b3-ffecc4b2be5d') as case:
            # 1.1. Right click on image
            # 1.1.18. Dock/Undock Library Window > minimize
            # able to open library window if click "Media Library"
            check_result = media_room_page.click_show_minimized_library_window()
            case.result = check_result

        with uuid('8f062297-92a7-46b5-bf57-3e934afaa428') as case:
            # 1.1. Right click on image
            # 1.1.19. Reset All Undocked Windows > dock all undocked windows
            media_room_page.hover_library_media('Landscape 01.jpg')
            check_result = media_room_page.library_clip_context_menu_reset_all_undocked_window()
            case.result = check_result

        with uuid('2b300992-1c17-4260-b06d-92fcb6582675') as case:
            # 1.1. Right click on image
            # 1.1.20. Show in Library Preview window > enable library preview and show this clip
            media_room_page.hover_library_media('Landscape 01.jpg')
            check_result = media_room_page.library_clip_context_menu_show_in_library_preview()
            case.result = check_result

            library_preview_page.library_preview_click_close_preview()

        with uuid('a75f9e7b-4fc7-4f08-95ca-c765a703e0ff') as case:
            # 1.1. Right click on image
            # 1.1.21. View Properties > open properties dialog
            media_room_page.hover_library_media('Landscape 01.jpg')
            check_result = media_room_page.library_clip_context_menu_view_properties()
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid('1b726ddd-5855-45af-a254-6269ffa77619') as case:
            # 1. Media Room
            # 1.2. Right click on video
            # 1.2.1. insert to selected track > add right clicked clip to selected track
            media_room_page.hover_library_media('Skateboard 01.mp4')
            media_room_page.library_clip_context_menu_insert_on_selected_track()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_2_1_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_2_1_1.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            media_room_page.tap_Remove_hotkey()

        with uuid('f2528cf2-de5e-4ee9-a11c-be2b49607ae7') as case:
            # Close Speech to Text Bubble
            time.sleep(DELAY_TIME)
            main_page.timeline_select_track(1)

            # 1.2. Right click on video
            # 1.2.2. remove from library > remove clicked clip from library
            media_room_page.hover_library_media('Skateboard 01.mp4')
            media_room_page.library_clip_context_menu_remove_from_library()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_2_2_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_2_2_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('7e2ce08f-6416-402a-869e-8d1f6a2b7333') as case:
            # 1.2. Right click on video
            # 1.2.4. Add to > add to custom tag
            media_room_page.add_new_tag('custom_tag')
            media_room_page.hover_library_media('Skateboard 02.mp4')
            media_room_page.library_clip_context_menu_add_to('custom_tag')
            media_room_page.select_specific_category('custom_tag')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_2_4_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_2_4_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('b6813283-2073-4e69-b4fe-b72ad1ac68bc') as case:
            # 1.2. Right click on video
            # 1.2.5. Change Alias > change clip name in library
            media_room_page.hover_library_media('Skateboard 02.mp4')
            media_room_page.library_clip_context_menu_change_alias('change_alias')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_2_5_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_2_5_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('a361ba1f-90fe-4132-8de1-e303c7d4d42d') as case:
            # 1.2. Right click on video
            # 1.2.6. Reset Alias > reset clip name
            media_room_page.hover_library_media('change_alias')
            check_result = media_room_page.library_clip_context_menu_reset_alias('Skateboard 02.mp4')
            case.result = check_result

        with uuid('af9dbd6c-2d89-42da-adf7-b50f21ea4da5') as case:
            # 1.2. Right click on video
            # 1.2.9. Pre-cut > open Precut with selected clip
            media_room_page.hover_library_media('Skateboard 02.mp4')
            check_result = media_room_page.library_clip_context_menu_precut()
            case.result = check_result

            main_page.press_esc_key()

        with uuid('0d17b8b5-e180-4894-a2fc-e53d3b135399') as case:
            # 1.2. Right click on video
            # 1.2.16. Open File Location > open windows file browser to clip location
            media_room_page.hover_library_media('Skateboard 02.mp4')
            check_result = media_room_page.library_clip_context_menu_open_file_location()
            case.result = check_result

        with uuid('e6471f9e-c797-4905-aaa0-48bf2f61d4a0') as case:
            # 1.2. Right click on video
            # 1.2.19. Show in Library Preview window > enable library preview and show this clip
            media_room_page.hover_library_media('Skateboard 02.mp4')
            check_result = media_room_page.library_clip_context_menu_show_in_library_preview()
            case.result = check_result

            library_preview_page.library_preview_click_close_preview()

        with uuid('93a823fc-ccf4-4ab6-9bad-ab1ebce47d90') as case:
            # 1.2. Right click on video
            # 1.2.20. View Properties > open properties dialog
            media_room_page.hover_library_media('Skateboard 02.mp4')
            check_result = media_room_page.library_clip_context_menu_view_properties()
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid('83463b84-116f-473b-b8f1-95c27997c38f') as case:
            # 1. Media Room
            # 1.3. Right click on audio
            # 1.3.1. insert to selected track > add right clicked clip to selected track
            media_room_page.hover_library_media('Speaking Out.mp3')
            media_room_page.library_clip_context_menu_insert_on_selected_track()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_3_1_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_3_1_1.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            media_room_page.tap_Remove_hotkey()

        with uuid('15729eb4-e163-476f-b7c1-15b69894581d') as case:
            # 1.3. Right click on audio
            # 1.3.2. remove from library > remove clicked clip from library
            media_room_page.hover_library_media('Speaking Out.mp3')
            media_room_page.library_clip_context_menu_remove_from_library()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_3_2_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_3_2_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('5f1e6699-06eb-4a07-9b0c-b94442b810be') as case:
            # 1.3. Right click on audio
            # 1.3.4. Add to > add to custom tag
            media_room_page.add_new_tag('custom_tag')
            media_room_page.hover_library_media('Mahoroba.mp3')
            media_room_page.library_clip_context_menu_add_to('custom_tag')
            media_room_page.select_specific_category('custom_tag')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_3_4_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_3_4_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('69211645-eb56-4cba-af9e-2c1916908ba2') as case:
            # 1.3. Right click on audio
            # 1.3.5. Change Alias > change clip name in library
            media_room_page.hover_library_media('Mahoroba.mp3')
            media_room_page.library_clip_context_menu_change_alias('change_alias')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_3_5_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_3_5_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('eafd1b5a-2eff-43a5-b710-edd877db1ecb') as case:
            # 1.3. Right click on audio
            # 1.3.6. Reset Alias > reset clip name
            media_room_page.hover_library_media('change_alias')
            check_result = media_room_page.library_clip_context_menu_reset_alias('Mahoroba.mp3')
            case.result = check_result

        with uuid('737243dc-1d02-4a2d-99f3-0f91000f1b51') as case:
            # 1.3. Right click on audio
            # 1.3.8. Pre-cut > should disable
            media_room_page.hover_library_media('Mahoroba.mp3')
            main_page.right_click()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_3_8_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_3_8_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.press_esc_key()

        with uuid('fe57df52-c032-43e6-b127-9d56704a987b') as case:
            # 1.3. Right click on audio
            # 1.3.16. Open File Location > open windows file browser to clip location
            media_room_page.hover_library_media('Mahoroba.mp3')
            check_result = media_room_page.library_clip_context_menu_open_file_location()
            case.result = check_result

        with uuid('6ad8c8cb-7321-44d3-b52f-50a4c71b661d') as case:
            # 1.3. Right click on audio
            # 1.3.19. Show in Library Preview window > enable library preview and show this clip
            media_room_page.hover_library_media('Mahoroba.mp3')
            check_result = media_room_page.library_clip_context_menu_show_in_library_preview()
            case.result = check_result

            library_preview_page.library_preview_click_close_preview()

        with uuid('59300b13-173b-4338-94b8-2949991dadcf') as case:
            # 1.3. Right click on audio
            # 1.3.20. View Properties > open properties dialog
            media_room_page.hover_library_media('Mahoroba.mp3')
            check_result = media_room_page.library_clip_context_menu_view_properties()
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid('aff94055-d232-4f49-8a31-9952c61ddbc7') as case:
            # 1. Media Room
            # 1.4. Right click on empty space
            # 1.4.1. import Media files...
            # open import media dialog
            main_page.insert_media('Food.jpg')
            check_result = media_room_page.collection_view_right_click_import_media_files(Test_Material_Folder)
            case.result = check_result

            main_page.press_esc_key()

        with uuid('f3871239-8b4f-4e11-9b3d-9df6e1c4df9a') as case:
            # 1.4. Right click on empty space
            # 1.4.2. Import a Media Folder...
            # open import media folder dialog
            check_result = media_room_page.collection_view_right_click_import_a_media_folder(
                Test_Material_Folder + 'Right_Click')
            case.result = check_result

        with uuid('bcc15fd4-fd5d-46d9-bf14-8df2e5697f91') as case:
            # 1.4. Right click on empty space
            # 1.4.3. Download From > Cloud
            # open Flickr dialog
            check_result = media_room_page.collection_view_right_click_download_from_cyberlink_cloud()
            time.sleep(DELAY_TIME)
            case.result = check_result

            main_page.press_esc_key()

        with uuid('c752ad7b-41cb-4778-a771-5803b76fea75') as case:
            # 1.4. Right click on empty space
            # 1.4.4. Select All
            # select all contents in library
            media_room_page.collection_view_right_click_select_all()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_4_4_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_4_4_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('9745fec4-baab-4360-b1d2-0bb0ad24f0c6') as case:
            # 1.4. Right click on empty space
            # 1.4.9. Sort by > Duration
            media_room_page.collection_view_right_click_sort_by_duration()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_4_9_2.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_4_9_2.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('48d71e4d-2ca3-42c8-a485-dc215a6733fb') as case:
            # 1.4. Right click on empty space
            # 1.4.9. Sort by > File Size
            media_room_page.collection_view_right_click_sort_by_file_size()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_4_9_3.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_4_9_3.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('229cccc5-26ba-4f6c-afd4-281533418a11') as case:
            # 1.4. Right click on empty space
            # 1.4.9. Sort by > Created Date
            media_room_page.collection_view_right_click_sort_by_created_date()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_4_9_4.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_4_9_4.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('1eed9312-97ff-4b87-8243-dc73cf88d83e') as case:
            # 1.4. Right click on empty space
            # 1.4.9. Sort by > Modified Date
            media_room_page.collection_view_right_click_sort_by_modified_date()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_4_9_5.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_4_9_5.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('a8d2a98b-848a-42f2-919b-21e2942f5a60') as case:
            # 1.4. Right click on empty space
            # 1.4.9. Sort by > Type
            media_room_page.collection_view_right_click_sort_by_type()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_4_9_6.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_4_9_6.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('1e7c620e-d1d0-4d45-91a2-b59b9e8e6341') as case:
            # 1.4. Right click on empty space
            # 1.4.9. Sort by > Name
            media_room_page.collection_view_right_click_sort_by_name()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_4_9_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_4_9_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('ca3f1c54-0092-447d-94fe-f4579bd40a6b') as case:
            # 1.4. Right click on empty space
            # 1.4.10. Dock/Undock Library Window
            # dock or undock library windows
            check_result = media_room_page.collection_view_right_click_dock_undock_library_window()
            case.result = check_result

        with uuid('e5a916e2-252b-4363-b765-714376ec474b') as case:
            # 1.4. Right click on empty space
            # 1.4.11. Reset All Undocked Windows
            # dock all undocked windows
            check_result = media_room_page.collection_view_right_click_reset_all_undocked_windows()
            case.result = check_result

        with uuid('3566eb18-9676-4388-b023-3b9f2a87617b') as case:
            # 1.4. Right click on empty space
            # 1.4.8. Remove All Unused Content from Library
            # remove unused contents
            # main_page.insert_media('Food.jpg')
            media_room_page.collection_view_right_click_remove_all_unused_content_from_library()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_4_8_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_4_8_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('4a2adf04-6c0c-4f0d-b4cd-1d1624a52eb4') as case:
            # 1.4. Right click on empty space
            # 1.4.7. Empty the Library
            # remove all contents in library
            media_room_page.collection_view_right_click_empty_library()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_4_7_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_4_7_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid('9e4c434f-212b-4f0f-ac81-a1e4bcebab2e') as case:
            # 1. Media Room
            # 1.6. Right click on Color board
            # 1.6.1. insert on selected track
            # color board insert to track directly
            time.sleep(DELAY_TIME * 3)
            media_room_page.enter_color_boards()
            #media_room_page.color_board_context_menu_insert_on_selected_track('0,0,0')
            main_page.click_library_details_view()
            media_room_page.sound_clips_select_media('0, 0, 0')
            main_page.tips_area_insert_media_to_selected_track()
            #main_page.click_library_icon_view()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_6_1_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_6_1_1.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('e2d70f9e-6977-42df-9f72-b6ec02f93374') as case:
            # 1.6. Right click on Color board
            # 1.6.2. Remove from media library
            # remove from library directly
            #media_room_page.hover_library_media('0,0,0')
            media_room_page.sound_clips_select_media('0, 0, 0')
            media_room_page.color_board_context_menu_remove_from_media_library()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_6_2_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_6_2_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('9443f8b9-d745-4d24-82b8-b433259eb751') as case:
            # 1.6. Right click on Color board
            # 1.6.3. Change Alias > in library
            # alias change correctly
            media_room_page.sound_clips_select_media('81, 0, 103')
            media_room_page.color_board_context_menu_change_alias('change_alias')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_6_3_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_6_3_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('1d8b91b8-f8fe-4cea-93f7-2088442756fc') as case:
            # 1.6. Right click on Color board
            # 1.6.4. Reset Alias
            # reset alias to default correctly
            media_room_page.sound_clips_select_media('change_alias')
            check_result = media_room_page.color_board_context_menu_reset_alias('0,120,255')
            case.result = check_result

        with uuid('250763bc-af04-4fcb-9036-d86e0abd1b69') as case:
            # 1. Media Room
            # 1.7. Right click on Background Music
            # 1.7.1. Download
            # able to download selected audio file
            media_room_page.enter_downloaded()
            time.sleep(DELAY_TIME*15)
            check_category = main_page.select_library_icon_view_media('1983')
            if check_category:
                #media_room_page.background_music_clip_context_menu_delete_from_disk('1983')
                media_room_page.right_click()
                media_room_page.select_right_click_menu('Remove from Disk')
                media_room_page.exist_click(L.media_room.confirm_dialog.btn_yes)
            else:
                media_room_page.enter_media_content()

            media_room_page.enter_background_music()
            media_room_page.background_music_clip_context_menu_download('1983')
            check_result_1 = media_room_page.sound_clips_check_download_mark('1983')

            media_room_page.select_specific_category('Downloaded')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_7_1_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_7_1_1.png'
            current_preview = main_page.snapshot(
                locator=media_room_page.area.library_detail_view, file_name=image_full_path)

            check_result_2 = main_page.compare(ground_truth, current_preview)
            case.result = check_result_1 and check_result_2

        with uuid('06d30d42-ef82-47ee-9b86-765c60db37c4') as case:
            # 1.7. Right click on Background Music
            # 1.7.2. Delete
            # able to delete the downloaded audio
            check_result = media_room_page.background_music_clip_context_menu_delete_from_disk('1983')
            time.sleep(DELAY_TIME * 2)
            case.result = check_result

        with uuid('6a6cdcaf-cd8d-4a41-8617-6075bc3559a9') as case:
            # 1. Media Room
            # 1.8. Right click on Sound Clips
            # 1.8.1. Download
            # able to download selected audio file
            media_room_page.enter_sound_clips()
            time.sleep(DELAY_TIME)
            media_room_page.sound_clips_clip_context_menu_download('Airplane')
            media_room_page.select_specific_category('Downloaded')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_1_8_1_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_1_8_1_1.png'
            current_preview = main_page.snapshot(
                locator=media_room_page.area.library_detail_view, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('8cac5ddc-e32e-49d0-aa87-662b9bf5c1f5') as case:
            # 1.8. Right click on Sound Clips
            # 1.8.2. Delete
            # able to delete the downloaded audio
            check_result = media_room_page.sound_clips_clip_context_menu_delete_from_disk('Airplane')
            time.sleep(DELAY_TIME * 2)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid('960a5663-07f6-4dca-9624-8d90f5dc3651') as case:
            # 2. Effect Room
            # 2.1. Right click on Effect
            # 2.1.1. Add to Timeline
            # add select effect to effect track
            time.sleep(DELAY_TIME * 3)
            main_page.enter_room(3)
            time.sleep(DELAY_TIME)
            # effect_room_page.hover_library_media('Aberration')
            effect_room_page.right_click_addto_timeline('Aberration')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_2_1_1_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_2_1_1_1.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('a0125696-2cb7-4c77-998f-19b57563d29d') as case:
            # 2.1. Right click on Effect
            # 2.1.2. Add to > My Favorites
            # add effect to favorites tag
            effect_room_page.hover_library_media('Aberration')
            effect_room_page.right_click_addto('My Favorites')
            media_room_page.select_specific_tag('My Favorites')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_2_1_2_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_2_1_2_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('fe9eb337-b0f3-46b9-911b-d5d8a3fb2623') as case:
            # 2.1. Right click on Effect
            # 2.1.3. Remove from Favorites
            # remove effect from favorites
            effect_room_page.hover_library_media('Aberration')
            effect_room_page.remove_from_favorites()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_2_1_3_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_2_1_3_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            effect_room_page.select_specific_tag('All Content')

        with uuid('977cb258-6d6f-477c-b4f9-82971c57c2f5') as case:
            # 2.1. Right click on Effect
            # 2.1.2. Add to > Custom tags
            # add effect to custom tag
            effect_room_page.add_effectroom_new_tag('custom_tag')
            effect_room_page.hover_library_media('Aberration')
            effect_room_page.right_click_addto('custom_tag')
            effect_room_page.select_specific_tag('custom_tag')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_2_1_2_2.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_2_1_2_2.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        with uuid('c1a428df-3b35-4773-98b4-b96a567791f9') as case:
            # 3. PiP Object Room
            # 3.1. Right click on PiP Object
            # 3.1.1. Add to Timeline
            # add right clicked clip to selected track
            time.sleep(DELAY_TIME * 3)
            main_page.enter_room(4)
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_3_1_1_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_3_1_1_1.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('9bb4a832-058e-4c66-9930-1433fa91e5c1') as case:
            # 3.1. Right click on PiP Object
            # 3.1.2. Change Alias
            # change clip name in library
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.save_as_name('')
            pip_designer_page.input_template_name_and_click_ok('lake')
            pip_designer_page.click_cancel()
            # pip_room_page.select_specific_tag('Custom')
            pip_room_page.hover_library_media('lake')
            pip_room_page.select_RightClickMenu_ChangeAlias('001_lake')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_3_1_2_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_3_1_2_1.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('a4616f4b-834a-430c-b7d2-97e2d8a64ce2') as case:
            # 3.1. Right click on PiP Object
            # 3.1.3. Modify Template... > Modify PiP Attribute
            # open PiP designer
            pip_room_page.select_specific_tag('General')
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_ModifyTemplate('PiP')

            check_result = pip_room_page.check_in_PiP_designer()
            case.result = check_result

            # leave pip designer
            pip_room_page.press_esc_key()

        with uuid('98c8fa69-0f54-406c-bdaf-f60ae4e3cd7e') as case:
            # 3.1. Right click on PiP Object
            # 3.1.3. Modify Template... > Modify Mask Attribute
            # open Mask designer
            pip_room_page.hover_library_media('Dialog_03')
            check_result = pip_room_page.select_RightClickMenu_ModifyTemplate('Mask')
            case.result = check_result

            # leave pip designer
            pip_room_page.press_esc_key()

        # with uuid('df2d193b-f3c2-4d00-bdf6-0bc22758e997') as case:
        #     # 3.1. Right click on PiP Object
        #     # 3.1.4. Share and Upload to the Internet...
        #     # open upload dialog
        #     # pip_room_page.hover_library_media('001_lake')
        #     # pip_room_page.select_RightClickMenu_ShareUploadToInternet()
        #     case.result = None

        with uuid('bec32a15-6d04-485c-8e3e-84d7991a892a') as case:
            # 3.1. Right click on PiP Object
            # 3.1.6. Delete (only for custom/downloaded)
            # remove selected template
            pip_room_page.click_ImportPiPObject(Test_Material_Folder + '2144330281-1615752299605.dzp')
            time.sleep(DELAY_TIME * 3)
            pip_room_page.click_OK_onEffectExtractor()

            pip_room_page.select_specific_tag('Downloaded')
            pip_room_page.hover_library_media('Frame5317')
            check_result = pip_room_page.select_RightClickMenu_Delete()
            case.result = check_result

        with uuid('5292eaf1-4b60-4f93-9a2f-14a960a2168d') as case:
            # 3.1. Right click on PiP Object
            # 3.1.7. Add to > Custom tags
            # add template to custom tag
            pip_room_page.select_specific_tag('All Content')
            pip_room_page.add_new_tag('New Tag')
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_Addto('New Tag')

            pip_room_page.select_specific_tag('New Tag')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_3_1_7_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_3_1_7_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        with uuid('bc4e7cc8-0063-46a3-9d62-b79d3be5f1ca') as case:
            # 4. Particle Room
            # 4.1. Right click on Particle Object
            # 4.1.1. Add to Timeline
            # add right clicked clip to selected track
            time.sleep(DELAY_TIME * 3)
            main_page.enter_room(5)
            pip_room_page.select_specific_tag('General')
            media_room_page.select_media_content('Maple')
            particle_room_page.select_RightClickMenu_AddToTimeline()

            # set timecode to 00_00_05_00 and then snapshot the preview screen
            main_page.set_timeline_timecode('00_00_05_00')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_4_1_1_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_4_1_1_1.png'
            current_preview = main_page.snapshot(
                locator=media_room_page.area.preview.main, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('24ab6b8e-8b7c-4496-82bb-7ec9cdd56c82') as case:
            # 4.1. Right click on Particle Object
            # 4.1.7. Addto
            # add template to custom tag
            particle_room_page.click_import_particle_objects(Test_Material_Folder + 'particle_effect.dzp')
            particle_room_page.click_OK_onEffectExtractor()

            particle_room_page.add_particleroom_new_tag('New Tag')

            particle_room_page.select_specific_tag('Downloaded')
            particle_room_page.hover_library_media('pa.')
            particle_room_page.select_RightClickMenu_Addto('New Tag')
            particle_room_page.select_specific_tag('New Tag')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_4_1_7_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_4_1_7_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('858b0886-bf33-4a41-9b59-fa3f5c8e09ba') as case:
            # 4.1. Right click on Particle Object
            # 4.1.6. Delete (only for Custom/Downloaded)
            # remove selected template
            particle_room_page.select_specific_tag('Downloaded')
            particle_room_page.hover_library_media('pa.')
            check_result_1 = particle_room_page.select_RightClickMenu_Delete()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_4_1_6_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_4_1_6_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result_2 = main_page.compare(ground_truth, current_preview)
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        with uuid('bd34254f-7aa3-4a01-80e1-e73724bda37b') as case:
            # 5. Title Room
            # 5.1. Right click on Title Object
            # 5.1.1. Add to Timeline
            # add right clicked clip to selected track
            time.sleep(DELAY_TIME * 3)
            main_page.enter_room(1)
            media_room_page.select_media_content('Default')
            title_room_page.select_RightClickMenu_AddToTimeline()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_5_1_1_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_5_1_1_1.png'
            current_preview = main_page.snapshot(
                locator=title_room_page.area.timeline, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        # with uuid('c2511956-e237-4252-985f-4d3867ec2a9a') as case:
        #     # 5.1. Right click on Title Object
        #     # 5.1.2. Change Alias > In library
        #     # alias change correctly
        #     title_room_page.select_specific_tag('All Content')
        #     # title_room_page.hover_library_media('Default') # waiting for create custom pip object function ready
        #     # title_room_page.select_RightClickMenu_ChangeAlias('01_change_alias')
        #
        #     image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_5_1_2_1.png'
        #     ground_truth = Ground_Truth_Folder + 'right_click_menu_library_5_1_2_1.png'
        #     current_preview = pip_room_page.snapshot(
        #         locator=L.media_room.library_listview.main_frame, file_name=image_full_path)
        #
        #     check_result = pip_room_page.compare(ground_truth, current_preview)
        #     case.result = None

        with uuid('5adbbdcb-2506-4c15-8e64-0c1a24b18406') as case:
            # 5.1. Right click on Title Object
            # 5.1.3. Modify Template...
            # open Title Designer
            media_room_page.hover_library_media('Default')
            check_result = title_room_page.select_RightClickMenu_ModifyTemplate()
            case.result = check_result
            time.sleep(DELAY_TIME)
            main_page.press_esc_key()

        # with uuid('0a0c8188-c06c-44fa-90f6-0884c254df0e') as case:
        #     # 5.1. Right click on Title Object
        #     # 5.1.4. Share and Upload to Internet
        #     # open upload dialog
        #     # title_room_page.hover_library_media('custom_title')
        #     # title_room_page.select_RightClickMenu_ShareUploadToInternet()
        #     # waiting for create custom title object page function ready
        #     case.result = None

        with uuid('2bf902f9-ab4a-4ccb-82d7-077242c920d2') as case:
            # 5.1. Right click on Title Object
            # 5.1.7. Addto > Custom tags
            # add template to custom tag
            title_room_page.click_ImportTitleTemplates(Test_Material_Folder + 'title.dzt')
            title_room_page.click_OK_onEffectExtractor()

            title_room_page.add_titleroom_new_tag('New Tag')

            title_room_page.select_specific_tag('Downloaded')
            title_room_page.hover_library_media('My SIMPLE TITLE 017')
            title_room_page.select_RightClickMenu_Addto('New Tag')
            title_room_page.select_specific_tag('New Tag')

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_5_1_7_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_5_1_7_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('7d0a3f5b-c5b8-4be6-b74d-ebf64b0b4ac3') as case:
            # 5.1. Right click on Title Object
            # 5.1.6. Delete (only for Custom/Downloaded)
            # remove selected template
            title_room_page.select_specific_tag('Downloaded')
            title_room_page.hover_library_media('My SIMPLE TITLE 017')
            check_result_1 = title_room_page.select_RightClickMenu_Delete()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_5_1_6_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_5_1_6_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result_2 = main_page.compare(ground_truth, current_preview)
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_10(self):
        with uuid('d48b0c0b-6bf2-499e-83de-f8fb92580931') as case:
            # 6. Transition Room
            # 6.1. Right click on Transition
            # 6.1.5. Add to > My Favorites
            # add template to favorites tag
            time.sleep(DELAY_TIME * 3)
            main_page.enter_room(2)
            transition_room_page.hover_library_media('Aberration')
            transition_room_page.select_RightClickMenu_Addto('My Favorites')

            transition_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Aberration')
            case.result = check_result

        with uuid('23cc54c6-6064-4b06-b704-53b7442fd99e') as case:
            # 6.1. Right click on Transition
            # 6.1.5. Add to > Custom tags
            # add template to custom tag
            transition_room_page.add_transitionroom_new_tag('New Tag')
            media_room_page.hover_library_media('Aberration')
            transition_room_page.select_RightClickMenu_Addto('New Tag')

            transition_room_page.select_LibraryRoom_category('New Tag')
            check_result = main_page.select_library_icon_view_media('Aberration')
            case.result = check_result

        with uuid('c49007c3-8a85-461a-8f82-711bb81941e4') as case:
            # 6.1. Right click on Transition
            # 6.1.6. Remove from Favorites
            # remove effect from favorites
            transition_room_page.select_LibraryRoom_category('My Favorites')
            main_page.select_library_icon_view_media('Aberration')
            transition_room_page.select_RightClickMenu_RemoveFromFavorites()

            image_full_path = Auto_Ground_Truth_Folder + 'right_click_menu_library_6_1_6_1.png'
            ground_truth = Ground_Truth_Folder + 'right_click_menu_library_6_1_6_1.png'
            current_preview = main_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('ce767a4a-8300-4d6d-ae66-57fd1820f9d8') as case:
            # v20.0.3223 remove the item on (Right Click Menu) : skip this case
            # 1.1. Right click on image
            # 1.1.9. Find in Timeline > select to same clip on timeline
            case.result = None
            case.fail_log = '*SKIP - item remove 20.0.3223'

        with uuid('fd9f646c-21c8-4ebd-a200-a870e4344432') as case:
            # v20.0.3223 remove the item on (Right Click Menu) : skip this case
            # 1.2. Right click on video
            # 1.2.7. Find in Timeline > select to same clip on timeline
            case.result = None
            case.fail_log = '*SKIP - item remove 20.0.3223'

        with uuid('c7612586-8e79-4f67-a003-146482fa1e59') as case:
            # v20.0.3223 remove the item on (Right Click Menu) : skip this case
            # 1.3. Right click on audio
            # 1.3.7. Find in Timeline > select to same clip on timeline
            case.result = None
            case.fail_log = '*SKIP - item remove 20.0.3223'

        with uuid('''
                    3fab010b-d825-43a6-9d50-f2e0262bbdeb
                    d792bd69-02ee-4517-a9c1-2d77802dca99
                    0543c0fe-555e-4220-a3a0-3d8055cf30b9
                    805109eb-f1bf-4abb-99dc-10c9e0acc921
                    91b54b2f-2f99-4381-92c5-a24519c3d11d
                    67aed150-7bb5-408d-9204-e0f477c0370e
                    8d1262dc-b134-420a-a6f0-1ae13aba7056
                    62664000-5536-4020-80e3-1fb331a3d3bb
                    674405bc-aea3-4ff8-9eed-92dd0956efc3
                    96ed676c-2d91-4260-8b0c-c5d8f024e108
                    3b828853-3ba2-4830-86b3-2749cda4006c
                    f9957712-e452-43f3-878d-16d1ab54346f
                    9597fcaa-d8e2-4ced-bc47-1195869ce22f
                    e5dc3e8d-54e9-4b47-ae96-99b48e0337f6
                    c1766bda-c5b7-4221-98ed-c2791ecd1272
                    09fe6d22-dc55-4414-bf1b-6b741316098e
                    a90a54f3-e9e0-45bd-a236-c92fb4dbc9de
                    db2c1c57-40b0-4b24-b07d-18dbb10894fb
                    9359bedf-3746-4b27-8e72-a29fd57f7435
                    0f5d77f5-86d7-45d7-a3a9-96b89e8da1f7
                    485eca8b-9a07-4922-bdef-002b04dcc16e
                    e79f6acf-3634-4028-8cc0-574ee7ff0a53
                    e8f04d61-9295-4de8-91e2-6bbc22bfa74d
                    86d672df-0b2a-4872-9c95-eeab0244cbff
                    32e9d7c9-d36a-455b-bcac-1ed8d5bd9cef
                    f2de0869-3f42-430e-8e31-a989f98731c3
                    30a5b907-42b6-4785-b20c-115f6f9cde4c
                    57ba6e3c-67b2-4de4-b2be-d137fbdc464c
                    11f4b036-15cd-49a2-afbe-2a75d2fa7271
                    42378a74-cd11-4f75-b37f-eda5641a6e52
                    e35d2f35-b571-4087-99b3-061e7dbcf9e7
                    ec7fdb4a-9cd2-4311-b635-78add450f6d8
                    bd112122-e149-477e-9fe5-75ec1c6c6334
                    7451ee60-a409-4ce1-b974-e44dd7143577
                    a18616f1-471d-4ff0-9fac-95057a99ca09
                    6952d074-3ed3-4548-84ce-1bfc8b8bc5ae
                    565ffa74-214d-44c7-81fd-94fac3344f40
                    3afcb073-478e-4b3c-a6a6-90253b4e0ea1
                    88570752-8dce-48ef-b608-0bb330eafda5
                    5af78ee0-2c67-4bc6-91f1-3564d116b335
                    e87be995-b23e-4bd2-b6ef-e101e94efe13
                    61753de8-9122-45d3-a539-5f110c4c6bed
                    e2249372-2698-4ebc-9de5-4e3b6ce715d1
                    04412f8b-cd41-4d9c-aef9-ebd8f1067451
                    61c8f98a-395b-444c-9219-f5a28a8fd38c
                    e49adcb1-6fd0-43be-9adb-45fefa3af972
                    b97661f6-512b-4739-bfa0-b9ea45f47025
                    bf2313ad-af8d-4a49-a91b-2a9726d5c061
                    56b31c91-695d-4256-8478-95badb664a71
                    5ff18751-005b-44f0-9bb1-9ba5fe4a974d
                    df2d193b-f3c2-4d00-bdf6-0bc22758e997
                    b41aa97d-7d71-4bb3-9962-5b5f97518651
                    e210a4fe-c17d-4307-9bcb-5da7a0499b73
                    7811be6a-b842-4df1-ab3d-9442f72f5db1
                    8b611155-b76d-44f2-8c64-6a8a355f0131
                    8a4000a6-93f4-47f5-94e7-42d3c0d6e1e9
                    6c21a74f-3d2e-49dd-8a78-bd289a562de3
                    e5ab525c-bfa4-42cc-befa-7be9edbe126e
                    bca2f105-789e-45a0-b614-d7beb6e052ef
                    d0220b13-10c1-4e41-9d3a-0a7d1e3b0e38
                    d8460e0c-a2c4-4f3d-8ddd-615f553ed31c
                    d79aa5bf-da96-4a5e-ba62-8174795e8cf8
                    609e0f46-0a1a-49d8-b3e2-c1249b5513a2
                    99c1407a-2bdd-41e6-89e7-573b2d57331c
                    9194293f-2b74-4a34-aab3-05af95274f90
                    92c46d80-1877-4ee9-9c93-fd26ada12ead
                    d78a3be9-d852-416d-92ea-4528fa7e2f95
                    b21e512e-6bf3-48a3-8c70-1829578763fd
                    ab57a383-da83-4f81-b5a3-269fe3a846ea
                    b2dc4c08-f40c-4425-8b6a-826b438322cc
                    7ccf624a-2e14-4588-b792-51a3dafd4331
                    28da7e4d-3cde-4e59-b36c-927c2cfb5256
                    dc751970-7488-47dc-acdf-706f6fcebf5c
                    863053d2-985b-46b3-906f-5a236d758c65
                    7c37fa33-4edf-43c5-a408-f8a52c0e9b4e
                    a0098aa5-595f-4f70-885c-e26080032e85
                    813b3932-f448-40de-b1ad-78a3352055b8
                    c207c416-1467-4d84-8a2b-0b3ef77fea29
                    470a43e6-4fdb-460e-a7ff-548b10a25b89
                    96b6c3ec-04b1-40cc-9c3a-ff55c5e6917f
                    8636f063-abbe-467d-a625-3c5acb5c8b09
                    c2511956-e237-4252-985f-4d3867ec2a9a
                    0a0c8188-c06c-44fa-90f6-0884c254df0e
                    a355e9d3-8302-41d4-916e-c1976e534cd9
                    f42a2350-5d24-4392-b202-ebe2126d8277
                    9cb2b079-0046-4d87-98a3-ec19f4312016
                    d873c9c8-90a6-4006-a22c-ca48781e1049
                    3476ac02-2211-4834-8426-51329988bb84
                    8760b7e6-376d-4a5d-b930-97b724f2ca2d
                    bca07f5f-bb7d-406f-b622-4beeddd3c98e
                    820cd87c-9503-4335-8aa9-dff09b10c98b
                    d2921996-77ab-43c3-96ae-976a02961a80
                    8616a50e-e038-4ea5-8e8f-c1ae66e8f772
                    4f7ff86f-fb33-496c-bec6-bd36e1039f88
                    8e1d0155-8ff2-476d-b092-1a89709844dc
                    c9f5340e-09bd-49c5-aebb-96c387f47dee
                    f450c1ef-42e3-4f0b-a6cc-f8295fec0dd4
                    7079e4fb-41ca-4eb3-b7bd-01c9725b2c4b
                    5d4d8a66-afb5-45ed-b36e-fe85e33bf076
                    203d93e5-331e-497e-94d0-f3203c7f9161
                    f436c8d5-3e06-4f46-884d-c3455e68900a
                    876cbe26-b4aa-4d56-b35c-f53e82108236
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'