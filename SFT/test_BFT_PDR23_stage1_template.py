import sys, os
import tempfile
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time, inspect, datetime, pytest, re, configparser
os.chdir(os.path.dirname(__file__))
from types import SimpleNamespace
from reportportal_client import step
from _pytest.runner import TestReport

from ATFramework import MyReport, logger
from ATFramework.drivers.driver_factory import DriverFactory
from pages.page_factory import PageFactory
from configs.app_config import *
from pages.locator import locator as L
from globals import *

import random
from functools import wraps

# read PDR cap >>
app = SimpleNamespace(**PDR_cap)
# read PDR cap <<

# create driver & page >>
mac = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page', mac)
precut_page = PageFactory().get_page_object('precut_page', mac)
intro_video_page = PageFactory().get_page_object('intro_video_room_page', mac)
download_from_ss_page = PageFactory().get_page_object('download_from_shutterstock_page', mac)
getty_image_page = PageFactory().get_page_object('gettyimage_page', mac)
title_designer_page = PageFactory().get_page_object('title_designer_page', mac)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mac)
tips_area_page = PageFactory().get_page_object('tips_area_page', mac)
playback_window_page = PageFactory().get_page_object('playback_window_page', mac)
produce_page = PageFactory().get_page_object('produce_page', mac)
import_media_from_cloud_page = PageFactory().get_page_object('import_downloaded_media_from_cl_page', mac)
title_room_page = PageFactory().get_page_object('title_room_page', mac)
download_from_cl_dz_page = PageFactory().get_page_object('download_from_cl_dz_page', mac)
pip_designer_page = PageFactory().get_page_object('pip_designer_page', mac)
pip_room_page = PageFactory().get_page_object('pip_room_page', mac)
shape_designer_page = PageFactory().get_page_object('shape_designer_page', mac)
particle_room_page = PageFactory().get_page_object('particle_room_page', mac)
particle_designer_page = PageFactory().get_page_object('particle_designer_page', mac)
mask_designer_page = PageFactory().get_page_object('mask_designer_page', mac)
video_collage_designer_page = PageFactory().get_page_object('video_collage_designer_page', mac)
trim_page = PageFactory().get_page_object('trim_page', mac)
project_new_page = PageFactory().get_page_object('project_new_page', mac)
library_preview_page = PageFactory().get_page_object('library_preview_page', mac)
project_room_page = PageFactory().get_page_object('project_room_page', mac)
effect_room_page = PageFactory().get_page_object('effect_room_page', mac)
effect_settings_page = PageFactory().get_page_object('effect_settings_page', mac)
audio_mixing_room_page = PageFactory().get_page_object('audio_mixing_room_page', mac)
preferences_page = PageFactory().get_page_object('preferences_page', mac)
voice_over_recording_page = PageFactory().get_page_object('voice_over_recording_page', mac)
subtitle_room_page = PageFactory().get_page_object('subtitle_room_page', mac)
blending_mode_page = PageFactory().get_page_object('blending_mode_page',mac)
crop_image_page = PageFactory().get_page_object('crop_image_page',mac)
pan_zoom_page = PageFactory().get_page_object('pan_zoom_page', mac)
crop_zoom_pan_page = PageFactory().get_page_object('crop_zoom_pan_page',mac)
video_speed_page = PageFactory().get_page_object('video_speed_page', mac)
audio_editing_page = PageFactory().get_page_object('audio_editing_page', mac)
fix_enhance_page = PageFactory().get_page_object('fix_enhance_page', mac)
motion_tracker_page = PageFactory().get_page_object('motion_tracker_page', mac)
keyframe_room_page = PageFactory().get_page_object('keyframe_room_page', mac)
transition_room_page = PageFactory().get_page_object('transition_room_page', mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="PDR22 Mac BFT_20231106.html")
uuid = report.uuid
report.report_type = "ReportPortal"
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/BFT_21_Stage1/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/BFT_21_Stage1/'
Test_Material_Folder = app.testing_material
Export_Folder  = app.export_path

DELAY_TIME = 1
EXPLORE_FILE = '' # for [Produce] Related test case

# add a decorator for main_page.close_app()
def close_app(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        finally:
            main_page.close_app()
    return wrapper


class Test_BFT_365_OS14():

    @pytest.fixture(autouse=True)
    def initial(self, request):
        """
        Common setup & teardown fixture with test result capturing.
        """
        time.sleep(DELAY_TIME * 4)  # Simulate delay for setup
        yield

    @classmethod
    def setup_class(cls):
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('BFT_365_os14')

    @classmethod
    def teardown_class(cls):
        pass

        # logger('teardown_class - export report')
        # report.export()
        # logger(
        #     f"BFT_365_os14 result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        # update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
        #                    report.get_ovinfo('skip'),
        #                    report.get_ovinfo('duration'))
        # # for test case module google sheet execution log (2021/04/12)
        # if get_enable_case_execution_log():
        #     google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
        #                        report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        # report.show()
    
    @step("[Action] Set color to HexColor code")
    def _set_color(self, HexColor):
        try:
            main_page.color_picker_switch_category_to_RGB()
            main_page.double_click(L.base.colors.input_hex_color)
            time.sleep(DELAY_TIME)
            main_page.exist(L.base.colors.input_hex_color).sendKeys(HexColor)
            time.sleep(DELAY_TIME)
            main_page.keyboard.enter()
            time.sleep(DELAY_TIME * 2)
            main_page.click(L.base.colors.btn_close)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True

    def _get_color(self):
        try:
            main_page.color_picker_switch_category_to_RGB()
            time.sleep(DELAY_TIME)
            current_hex = main_page.exist(L.base.colors.input_hex_color)
            time.sleep(DELAY_TIME)
            # main_page.exist(L.base.colors.btn_close).press()
            # time.sleep(DELAY_TIME)
            main_page.click(L.base.colors.btn_close)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return current_hex.AXValue

    def sort_by_date(self):
        try:
            if not main_page.exist_click(L.media_room.library_menu.btn_menu):
                raise Exception

            if not main_page.select_right_click_menu('Sort by', 'Date'):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step("[Action] Sort by Likes")
    def sort_by_like(self):
        try:
            if not main_page.exist_click(L.media_room.library_menu.btn_menu):
                raise Exception('Cannot find menu button')

            if not main_page.select_right_click_menu('Sort by', 'Likes'):
                raise Exception('Cannot find Sort by Likes')

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def check_open_intro_template(self):
        check_open_status = False
        # Downloading template for open Intro designer
        for x in range(15):
            check_open_status = intro_video_page.check_in_intro_designer()
            if check_open_status:
                break
            else:
                time.sleep(DELAY_TIME)

        # Loading template when open intro template
        check_loading_status = False
        for x in range(15):
            check_loading_status = main_page.is_not_exist(L.download_from_shutterstock.download.frame)
            if check_loading_status:
                logger('loading complete')
                break
            else:
                time.sleep(DELAY_TIME)
        return check_loading_status

    # Return current subtitle row number
    def get_total_subtitle_rows(self, timeout=35):
        # select first row
        subtitle_room_page.select_subtitle_row(1)

        # press [Down] repeatedly
        subtitle_count = 1
        for y in range(timeout):
            area = main_page.area.preview.main
            old_img = main_page.snapshot(area)
            main_page.input_keyboard(main_page.keyboard.key.down)
            time.sleep(0.5)
            new_img = main_page.snapshot(area)
            result = main_page.compare(old_img, new_img, 0.9999)
            #logger(result)
            if result:
                break
            else:
                subtitle_count = subtitle_count + 1
        return subtitle_count

    @step("[Action] Download [AI Module]")
    def download_AI_module_complete(self, timeout=60):
        # pop up (PROGRESS) then check result
        time.sleep(DELAY_TIME*6)

        if not download_from_ss_page.download.has_dialog():
            logger("Download AI module dialog is not found now")
            time.sleep(DELAY_TIME)
            return True

        download_status = False
        # Check (download AI module is ready) for loop
        for x in range(timeout):
            time.sleep(1)
            if download_from_ss_page.download.has_dialog():
                time.sleep(2)
            else:
                logger('Cannot find progress dialog \n Download cutout is ready!')
                download_status = True
                break
        time.sleep(DELAY_TIME * 3)
        return download_status
    
    @step("[Action] Wait for downloading AI module")
    def check_downloading_AI_module(self):
        # Check if downloading component now or not
        download_component = download_from_ss_page.download.has_dialog()

        # Download (Motion tracker) component
        if download_component:
            for x in range(500):
                check_result = download_from_ss_page.download.has_dialog()
                if check_result:
                    time.sleep(DELAY_TIME*3)
                else:
                    logger(f'now download is completed, x= {x}')
                    break

    @step("[Action] Wait until download [Body Effect] complete")
    def body_effect_download_complete(self, timeout=60):
        # pop up (Downloading Components) then check result
        time.sleep(DELAY_TIME * 13)

        if not download_from_ss_page.download.has_dialog():
            logger("Download dialog is not found now")
            return True

        download_status = False
        # Check download Body Effect for loop
        for x in range(timeout):
            time.sleep(1)
            if download_from_ss_page.download.has_dialog():
                current_value = download_from_ss_page.download.get_progress()
                if float(current_value) > 0.95:
                    logger('Arrive 95%')
                    download_status = True
                    time.sleep(6)
                    break
            else:
                logger('Cannot find progress dialog')
                break

        # Check Installing component
        for y in range(60):
            if not download_from_ss_page.download.has_dialog():
                logger('No install component now')
                break
            else:
                time.sleep(1.5)
        return download_status

    step("[Action] Click [Launch Free Version] button and enter main program by new project")
    def launch_Essential_build(self):
        # Click [Launch Free Version]
        check_free_version = main_page.launch_free_version()
        if not check_free_version:
            raise Exception ('Unable to Launch Free Version due to "Launch Free Version" button not found on Essential dialog')

        time.sleep(DELAY_TIME * 2)
        main_page.refresh_top()
        main_page.click_new_project_on_launcher()
        time.sleep(DELAY_TIME * 3)
        return check_free_version
    
    @step("[Action] Launch 365 build with clear cache and enter project")
    def launch_365_build_with_clear_cache(self):
        main_page.clear_cache_and_gdpr()
        if not main_page.launch_app(): return False
        main_page.click(L.base.gdpr_dialog.btn_accept_continue)
        main_page.refresh_top()
        main_page.click_CEIP_dialog()
        main_page.refresh_top()
        if not main_page.click_new_project_on_launcher(): return False
        main_page.exist(L.base.seasonal_bb_window.main, timeout=7)
        main_page.press_esc_key()
        if main_page.exist(L.base.seasonal_bb_window.main, timeout=3): return False
        return True

    def sign_in_365_again(self):
        # Clear Cache (Clear sign in log) to become Essential build
        main_page.clear_log_in()

        # launch APP
        main_page.clear_cache()

        # launch PDR
        logger('Launch PDR')
        main_page.launch_app()
        time.sleep(DELAY_TIME * 8)

        # launch Essential build to enter timeline mode
        self.launch_Essential_build()

        if main_page.exist(L.base.seasonal_bb_window.main):
            # Close seasonal BB dialog (What's new dialog)
            main_page.press_esc_key()
            time.sleep(DELAY_TIME * 2)

        # click [Sign in] icon to sign in 365 account
        main_page.handle_sign_in(account='sistarftcn.005@gmail.com', pw='ilovecc680520')

        # Pop up Activate limitation
        main_page.exist_click(L.main.activate_dialog.btn_activate, None, btn="left", timeout=6, no_warning=True)

        # Click [Restart]
        btn_restart = main_page.exist(
            {'AXTitle': 'Restart', 'AXIdentifier': 'IDC_CLALERT_BUTTON_0', 'AXRole': 'AXButton'}, timeout=15)
        main_page.mouse.click(*btn_restart.center)

        # Pop up Activate limitation
        time.sleep(DELAY_TIME * 3)
        main_page.exist_click(L.main.activate_dialog.btn_activate, None, btn="left", timeout=6, no_warning=True)

        # click (No, thank you) checkbox
        time.sleep(DELAY_TIME * 5)
        main_page.refresh_top()
        main_page.click_CEIP_dialog()
        logger('12130')
        main_page.refresh_top()
        main_page.click_new_project_on_launcher()
        logger('12133')
        main_page.refresh_top()

    @step('[Action] Open packed project')
    def open_packed_project(self, project_name, save_name):
        folder_path = '/Users/qadf_at/Desktop/AT/BFT_Material/'
        if not main_page.exist_file(folder_path + project_name):
            assert False, f"Project file {folder_path + project_name} doesn't exist!"

        # Open project
        main_page.top_menu_bar_file_open_project(save_changes='no')
        check_open_result = main_page.handle_open_project_dialog(folder_path + project_name)
        if not check_open_result:
            assert False, "Dealing with Open project dialog FAIL!"

        # Select extract path
        main_page.delete_folder(folder_path + save_name)
        main_page.select_file(folder_path + save_name)
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')
        return True
    
    @step('[Action] Open Recent Project')
    def open_recent_project(self, project_name, save_name):
        if not main_page.exist_file(Test_Material_Folder + project_name):
            assert False, f"Project file {project_name} doesn't exist!"

        # Open project
        main_page.top_menu_bar_file_open_recent_projects(Test_Material_Folder + project_name)

        # Select extract path
        main_page.delete_folder(Test_Material_Folder + save_name)
        main_page.select_file(Test_Material_Folder + save_name)
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')
        return True
    
    def check_download_body_effect(self, wait_time=900):
        return self.body_effect_download_complete(wait_time)

    @step('[Action] Insert media to timeline')
    def temp_for_os_14_insert_function(self, press_down_times=0):
        # replace the function: Insert to timeline
        # e.g. main_page.tips_area_insert_media_to_selected_track(1) >>> Insert: press_down_times = 1
        # e.g. main_page.tips_area_insert_media_to_selected_track(3) >>> CrossFade: press_down_times = 3
        time.sleep(DELAY_TIME * 2)
        main_page.click(L.main.tips_area.btn_insert_to_selected_track)
        time.sleep(DELAY_TIME * 2)

        # Move mouse position to right side (Hover right click menu "1st item")
        # Get current media position
        start_pos = main_page.get_mouse_pos()
        main_page.mouse.move(start_pos[0] + 10, start_pos[1])

        if press_down_times > 0:
            for x in range(press_down_times):
                main_page.keyboard.down()
                time.sleep(DELAY_TIME * 2)
        time.sleep(DELAY_TIME * 2)
        main_page.press_enter_key()

    #  Only for debug
    @pytest.mark.skip
    @exception_screenshot
    def test_bft_debug(self):
        # Clear Cache (Clear sign in log) to become Essential build
        main_page.clear_log_in()

        main_page.clear_cache_and_gdpr()
        time.sleep(DELAY_TIME*4)
        main_page.launch_app()
        time.sleep(DELAY_TIME * 5)

        # [L9] Click [Accept and Continue] button
        btn_continue = main_page.exist(L.base.gdpr_dialog.btn_accept_continue)
        if btn_continue:
            main_page.click(L.base.gdpr_dialog.btn_accept_continue)

    @step("[Initial] Check dependency test result")
    def ensure_dependency(self, dependency_test, run_dependency=True):
        """
        Ensures a dependency test is run and passed before continuing.

        Args:
            dependency_test (str): Name of the dependency test to check.
            logger (callable): Logging function.
            step (callable): Context manager for steps.
            run_dependency (bool): Whether to run the dependency test if it has not been run yet. 
                - If True: Run the dependency test if it has not been run yet./ If dependency test is failed, skip the current test.
                - If False: if the dependency test has not been run yet or it is failed, return None/ False directly

        Raises:
            pytest.skip: Skips the current test if the dependency fails or is skipped.
        """

        # Check the result of the dependency test
        result = pytest.test_results.get(dependency_test, None)

        if result is None:  # Dependency test not run
            with step(f"[Initial] Set up initialized status for the test case which is requiring [{dependency_test}] ready"):
                # close AP at first
                main_page.close_app()
                if run_dependency:
                    try:
                        # Dynamically call the dependency test
                        getattr(self, dependency_test)()
                    except AssertionError as e:
                        logger(f"{dependency_test} failed: {str(e)}")
                        pytest.skip(f"Skipping test case because [{dependency_test}] did not pass.")
                return None # Give boolen that dependency test is not run
        elif not result:  # Dependency test failed or skipped
            if run_dependency:
                logger(f"{dependency_test} result: {result}")
                pytest.skip(f"Skipping test case because [{dependency_test}] did not pass.")
            else:
                return False # Give boolen that dependency test is failed
        return True # Give boolen that dependency test is passed

