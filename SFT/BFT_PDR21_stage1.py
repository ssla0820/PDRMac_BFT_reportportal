import sys, os
import tempfile
import math
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

import random

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
# create driver & page <<

# For Report >>
#report = MyReport("MyReport", driver=mac, html_name="PDR21 Mac BFT_20220926.html")
report = MyReport("MyReport", driver=mac, html_name="PDR22 Mac BFT_20231106.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/BFT_21_Stage1/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/BFT_21_Stage1/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_BFT_21_stage1():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """

        time.sleep(DELAY_TIME*4)
        yield mac
        main_page.close_app()

    @classmethod
    def setup_class(cls):
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('BFT_PDR21_stage1')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"BFT_PDR21_stage1 result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()

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
            main_page.exist(L.base.colors.btn_close).press()
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

    def sort_by_like(self):
        try:
            if not main_page.exist_click(L.media_room.library_menu.btn_menu):
                raise Exception

            if not main_page.select_right_click_menu('Sort by', 'Likes'):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
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

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        # Clear Cache (Clear sign in log) to become Essential build
        main_page.clear_log_in()

        # Before AT execution, only test_1_1_1 need to clear_cache()
        # Clear Cache + GDPR
        main_page.clear_cache_and_gdpr()
        time.sleep(DELAY_TIME * 3)

        # launch PDR
        logger('Launch PDR')
        main_page.launch_app()
        time.sleep(DELAY_TIME * 5)

        # [L7] Pop up GDPR dialog
        with uuid("fec6b64b-8ab2-4422-b056-b8a711e5725f") as case:
            qdpr_window = main_page.exist(L.base.gdpr_dialog.main)
            case.result = qdpr_window

        # [L9] Click [Accept and Continue] button
        with uuid("98c0a3ab-d4de-46ef-bb16-39884f6a1caf") as case:
            btn_continue = main_page.exist(L.base.gdpr_dialog.btn_accept_continue)
            case.result = btn_continue
            if btn_continue:
                main_page.click(L.base.gdpr_dialog.btn_accept_continue)

        # [L11] Click [Upgrade Now] button
        with uuid("c9b335af-3053-4807-accb-2671a5de7c46") as case:
            # Click [Upgrade Now]
            time.sleep(DELAY_TIME*10)
            upgrade_link = main_page.exist({'AXTitle': 'GET PREMIUM', 'AXRole': 'AXLink'})
            upgrade_btn = main_page.exist({'AXTitle': 'Upgrade Now', 'AXRole': 'AXButton'})
            check_upgrade = 0

            if upgrade_link:
                main_page.mouse.click(*upgrade_link.center)
                check_upgrade = 1
            elif upgrade_btn:
                main_page.mouse.click(*upgrade_btn.center)
                check_upgrade = 1
            else:
                logger('cannot find upgrade button')

            logger(check_upgrade)
            time.sleep(DELAY_TIME*10)
            #main_page.activate()
            case.result = check_upgrade
            time.sleep(DELAY_TIME * 2)


        # [L12] Launch PDR Essential build
        with uuid("ebc38a68-9415-48ab-9914-16aa63afadb5") as case:
            # Click [Launch Free Version]
            free_version_link = main_page.exist({'AXTitle': 'LAUNCH FREE VERSION', 'AXRole': 'AXLink'})
            free_version_btn = main_page.exist({'AXTitle': 'Launch Free Version', 'AXRole': 'AXButton'})
            check_free_version = 0
            if free_version_link:
                main_page.mouse.click(*free_version_link.center)
                check_free_version = 1
            elif free_version_btn:
                main_page.mouse.click(*free_version_btn.center)
                check_free_version = 1
            else:
                logger('cannot find it')

            time.sleep(DELAY_TIME * 2)
            main_page.refresh_top()
            logger('handle launcher')
            main_page.click_new_project_on_launcher()

            # Verify Step
            check_import_icon = main_page.exist(L.media_room.btn_media_filter_display_audio_only, timeout=10)
            case.result = check_import_icon and check_free_version
            time.sleep(DELAY_TIME * 3)

        # Handle Seasonal BB (Click ESC to close BB)
        if main_page.exist(L.base.seasonal_bb_window.main, timeout=7):
            # Close seasonal BB dialog
            main_page.press_esc_key()
            time.sleep(DELAY_TIME * 2)

        # [L14] Able to sign in account
        with uuid("89b5f8e9-dc8f-42d7-9fda-2771939dfb81") as case:
            # [L15] Able to sign in account
            with uuid("45d2632c-6975-4bed-bd4a-5c13667d1cc0") as case:
                # Click User icon
                main_page.click(L.main.btn_user_sign_in_icon)
                time.sleep(DELAY_TIME * 10)


                # Input E-mail field
                e_mail_field = main_page.exist({'AXRoleDescription': 'text field', 'AXRole': 'AXTextField'})
                main_page.mouse.click(*e_mail_field.center)
                email_string = 'pdrmacat001@gmail.com'
                main_page.keyboard.send(email_string)
                time.sleep(DELAY_TIME)

                # Input PW field
                password_field = main_page.exist({'AXRoleDescription': 'secure text field', 'AXRole': 'AXTextField'})
                main_page.mouse.click(*password_field.center)
                password_string = 'qadf1234'
                main_page.keyboard.send(password_string)

                # Click [Sign in]
                btn_sign_in = main_page.exist({'AXTitle': 'Sign in', 'AXRole': 'AXLink'})
                main_page.mouse.click(*btn_sign_in.center)

                # Pop up Activate limitation
                logger('150')
                main_page.exist_click(L.main.activate_dialog.btn_activate, None, btn="left", timeout=6, no_warning=True)

                # Click [Restart]
                btn_restart = main_page.exist(
                    {'AXTitle': 'Restart', 'AXIdentifier': 'IDC_CLALERT_BUTTON_0', 'AXRole': 'AXButton'}, timeout=15)
                main_page.mouse.click(*btn_restart.center)

                # Pop up Activate limitation
                time.sleep(DELAY_TIME*3)
                main_page.exist_click(L.main.activate_dialog.btn_activate, None, btn="left", timeout=6, no_warning=True)

                # click (No, thank you) checkbox
                time.sleep(DELAY_TIME * 5)
                main_page.refresh_top()
                main_page.click_CEIP_dialog()
                logger('319')
                main_page.refresh_top()
                main_page.click_new_project_on_launcher()
                logger('322')
                main_page.refresh_top()

                # Check restart ok
                verify_step = False
                for x in range(20):
                    if main_page.is_exist(L.media_room.btn_import_media, None, 2):
                        logger('Launch PDR ready')
                        verify_step = True
                        break
                    else:
                        time.sleep(DELAY_TIME)
                case.result = verify_step
            case.result = verify_step

    #  18 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # [L111] 3.1 Video Intro Designer > Modify template > From Favorites
        with uuid("e5d5704c-a66b-410f-8ec0-8e93053ee302") as case:
            # enter Video Intro Room > My Favorites category
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 6)
            intro_video_page.enter_my_favorites()

            # select 1st template
            intro_video_page.select_intro_template_method_2(1)

            # Double click to enter designer
            main_page.double_click()

            time.sleep(DELAY_TIME * 2)

            if not main_page.exist(L.intro_video_room.intro_video_designer.main_window, timeout=15):
                case.result = False
            else:
                case.result = True

        # [L112] 3.1 Video Intro Designer > Preview template
        with uuid("2efc9aa9-0f89-4f28-a1cf-1a1181d52f8e") as case:
            img_before = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            time.sleep(DELAY_TIME)
            intro_video_page.click_preview_operation('Play')
            time.sleep(DELAY_TIME * 2)
            intro_video_page.click_preview_operation('Pause')

            # Verify step 1: Check preview
            img_after = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            designer_preview_result = main_page.compare(img_before, img_after, similarity=1)
            time.sleep(DELAY_TIME)

            # Verify step 2: Check timecode
            intro_video_page.click_preview_operation('Stop')
            time.sleep(DELAY_TIME)

            stop_timecode = intro_video_page.get_designer_timecode()
            logger(stop_timecode)

            if (stop_timecode == '00:00'):
                timocode_check = True
            else:
                logger('Verify FAIL')
                timocode_check = False

            case.result = (not designer_preview_result) and timocode_check

        # [L113] 3.1 Video Intro Designer > Edit > Change template duration
        with uuid("dad38202-8be2-45d8-a38a-aca3df0831d6") as case:
            intro_video_page.click_duration_btn()
            time.sleep(DELAY_TIME)

            # Get default duration
            result = intro_video_page.duration_setting.get_org_duration()
            if result != '7 seconds':
                default_duration = False
            else:
                default_duration = True

            # Change duration
            intro_video_page.duration_setting.set_new_duration(9)

            get_value = intro_video_page.duration_setting.get_new_duration()

            # Current INT should transfer to String
            if get_value != '9':
                set_result = False
            else:
                set_result = True

            case.result = default_duration and set_result
            intro_video_page.duration_setting.click_OK()

        # [L116] 3.1 Video Intro Designer > Edit > Replace master video correctly from Color Board
        with uuid("71de433f-e2cd-465d-b13d-4504f2263308") as case:
            # Click [Replace Background Media] > Use a Color Board
            intro_video_page.click_replace_media(3)
            time.sleep(DELAY_TIME)
            self._set_color('7B17FF')
            time.sleep(DELAY_TIME)

            img_7B17FF = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            time.sleep(DELAY_TIME)
            # Verify Step
            intro_video_page.click_replace_media(3)
            check_current_RBG = self._get_color()
            if check_current_RBG == '7B17FF':
                case.result = True
            else:
                case.result = False

        # [L122] 3.1 Video Intro Designer > Edit > Add Color Board (Able to modify setting for color board)
        with uuid("59f54e15-0b43-4b7e-8e2b-3f00ddfb41b7") as case:
            intro_video_page.click_replace_media(3)
            time.sleep(DELAY_TIME)
            self._set_color('95C029')
            time.sleep(DELAY_TIME)

            img_95C029 = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            time.sleep(DELAY_TIME)

            designer_preview_result = main_page.compare(img_7B17FF, img_95C029, similarity=0.98)
            case.result = not designer_preview_result

        # [L114] 3.1 Video Intro Designer > Edit > Replace master video from local content
        with uuid("6e03aff5-5870-41fc-add3-a2358348a59a") as case:
            intro_video_page.click_replace_media(1)
            main_page.select_file(Test_Material_Folder + 'Produce_Local/Produce_G367.mkv')

            # [L118] 3.1 Video Intro Designer > Edit > Trim Video
            with uuid("0a7af36b-f05b-481b-8867-a5ee0a2870be") as case:
                if main_page.exist(L.trim.main_window, timeout=10):
                    case.result = True
                    time.sleep(DELAY_TIME)
                    main_page.click(L.trim.btn_OK)
                    time.sleep(DELAY_TIME * 5)
                else:
                    logger('Verify FAIL')
                    case.result = False

                # Remove yellow MGT and Color board
                for x in range(2):
                    intro_video_page.click_preview_center()
                    intro_video_page.motion_graphics.click_remove_button()
                    time.sleep(2)

                # move Sticker (Pip_10_00000) to down
                time.sleep(DELAY_TIME)
                intro_video_page.move_preview_object_to_down()

                # Leave edit mode
                intro_video_page.cancel_selection_button()
                time.sleep(DELAY_TIME)

            current_image = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area,
                                                      file_name=Auto_Ground_Truth_Folder + 'I114.png')
            check_result = main_page.compare(Ground_Truth_Folder + 'I114.png', current_image)
            case.result = check_result

        # [L124] 3.1 Video Intro Designer > Edit > Add sticker
        with uuid("f4df2783-70c0-4745-9d5c-fadc90167b44") as case:
            with uuid("8c048835-df6d-4d2a-af28-4fdba6c2a2ad") as case:
                # [L124] Click (Add sticker)
                intro_video_page.click_add_pip_object()
                time.sleep(DELAY_TIME)

                # Video Overlay Room
                intro_video_page.select_pip_template(5, 'Travel')
                time.sleep(DELAY_TIME*5)

                # move Sticker to left upper
                time.sleep(DELAY_TIME)
                intro_video_page.move_preview_object_to_left_upper(x_threshold=0.5)

                # Leave edit mode
                intro_video_page.cancel_selection_button()
                time.sleep(DELAY_TIME)

                # [L123] 3.1 Video Intro Designer > Edit > Apply LUT
                intro_video_page.click_LUT_btn()
                time.sleep(DELAY_TIME * 2)

                elem = L.intro_video_room.intro_video_designer.color_filter_window.combobox_category
                if main_page.exist(elem).AXTitle == 'Color LUT':
                    default_status = True
                else:
                    default_status = False

                intro_video_page.color_filter.select_LUT_template(4, 'Urban Minimalist')

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area,
                                                          file_name=Auto_Ground_Truth_Folder + 'I123.png')
                check_result = main_page.compare(Ground_Truth_Folder + 'I123.png', current_image)
                case.result = check_result

            case.result = check_result and default_status

            # Close (Color Filter) window
            intro_video_page.color_filter.close_x()

        # [L119] 3.1 Video Intro Designer > Edit > Add general title
        with uuid("b0027c68-672d-416d-a969-aa875ddaae46") as case:
            intro_video_page.click_add_text(1)
            time.sleep(DELAY_TIME * 2)

            # Enable backdrop
            intro_video_page.general_title.click_backdrop_button()
            time.sleep(DELAY_TIME * 2)
            intro_video_page.backdrop_settings.enable_backdrop()
            time.sleep(DELAY_TIME)

            intro_video_page.backdrop_settings.set_type(2, 4)
            check_type = intro_video_page.backdrop_settings.get_fit_backdrop_status()
            if check_type == 'Rounded Rectangle':
                case.result = True
            else:
                case.result = False

            # Leave edit mode
            intro_video_page.cancel_selection_button()
            time.sleep(DELAY_TIME)

        # [L115] 3.1 Video Intro Designer > Edit > Download and replace master video correctly form SS
        with uuid("73912396-9399-463e-8fde-9e4e5c68b91e") as case:
            # Replace media from Shutterstock(Video)
            # 2023/05/04 modify: Replace media from iStock(Video)
            intro_video_page.click_replace_media(2)
            time.sleep(DELAY_TIME * 6)
            getty_image_page.handle_what_is_stock_media()
            #getty_image_page.switch_to_SS()
            time.sleep(DELAY_TIME * 6)
            download_from_ss_page.search.search_text('child happy pink circle boy')
            time.sleep(10)
            download_from_ss_page.video.select_thumbnail_for_video_intro_designer(1)

            for x in range(40):
                if main_page.exist(L.media_room.confirm_dialog.btn_no):
                    media_room_page.handle_high_definition_dialog(option='no')
                    time.sleep(DELAY_TIME*3)
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Verify : If pop up Trim window, Press ESC to leave Trim window
            if main_page.exist(L.trim.main_window, timeout=6):
                main_page.press_esc_key()
                time.sleep(DELAY_TIME * 2)

            img_updated = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_SS_result = main_page.compare(current_image, img_updated, similarity=0.95)
            case.result = not check_SS_result

        # [L120] 3.1 Video Intro Designer > Edit > Add MGT
        with uuid("4c6d937b-e72a-4ed9-852c-2c1134cb7812") as case:
            intro_video_page.click_add_text(2)
            time.sleep(DELAY_TIME * 3)

            # Insert Speech bubble 01
            intro_video_page.motion_graphics.select_template(1, category=5)
            time.sleep(DELAY_TIME * 5)

            # [L125] 3.1 Video Intro Designer > Edit > Change layer order
            with uuid("963f4ce6-e3b2-46c7-9bdd-3aa36c1fd0bd") as case:
                intro_video_page.click_layer_order(4)
                time.sleep(DELAY_TIME)
                intro_video_page.cancel_selection_button()
                time.sleep(DELAY_TIME)
                current_image = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area,
                                                          file_name=Auto_Ground_Truth_Folder + 'I125.png')
                check_result = main_page.compare(Ground_Truth_Folder + 'I125.png', current_image)
                case.result = check_result

            case.result = check_result

        # [L117] 3.1 Video Intro Designer > Edit > Crop
        with uuid("9d046ecb-a8ac-4339-9355-3f25d5b77d84") as case:
            # Click crop
            intro_video_page.click_crop_btn()
            time.sleep(DELAY_TIME * 2)

            # Resize to small
            intro_video_page.crop_zoom_pan.resize_to_small()
            time.sleep(DELAY_TIME * 2)
            intro_video_page.crop_zoom_pan.leave_crop('Yes')
            time.sleep(3)
            img_cancel_crop = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            check_result = main_page.compare(current_image, img_cancel_crop, similarity=0.99)
            case.result = not check_result

        # [L121] 3.1 Video Intro Designer > Edit > Add image
        with uuid("59ddae48-a065-48f3-a593-06cbf725c81f") as case:
            intro_video_page.click_add_image(1)
            time.sleep(DELAY_TIME)
            main_page.select_file(Test_Material_Folder + 'fix_enhance_20/colorful.jpg')

            # move image to right > up
            time.sleep(DELAY_TIME)
            intro_video_page.move_preview_object_to_right_upper()

            # Add animation
            intro_video_page.image.click_animation_btn()

            # Unfold
            intro_video_page.image.in_animation.unfold_setting(1)
            check_image_result = intro_video_page.image.in_animation.select_template('Blizzard')
            time.sleep(DELAY_TIME)

            # Verify Step
            after_add_photo = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            # Set Video Intro timecode: 01:15
            intro_video_page.set_designer_timecode('01_15')
            time.sleep(DELAY_TIME)

            check_animation = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_result = main_page.compare(after_add_photo, check_animation)
            case.result = not check_result

        # [L126] 3.1 Video Intro Designer > Edit > Add BGM
        # 2023/05/05 update: Skip this case << Download from Meta / Shutterstock (Music) >>

        # [L129] 3.1 Video Intro Designer > Save Template
        with uuid("3049da80-c0d6-40f7-86db-e317ef278b7b") as case:
            intro_video_page.click_btn_save_as('stage_1')

            # Enter (Save Templates)
            intro_video_page.enter_saved_category()
            intro_video_page.select_intro_template_method_2(1)
            main_page.double_click()
            time.sleep(DELAY_TIME*6)

            # Verify Step 1: Check preview
            current_image = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area,
                                                    file_name=Auto_Ground_Truth_Folder + 'I129.png')
            check_result = main_page.compare(Ground_Truth_Folder + 'I129.png', current_image)

            # Set Video Intro timecode: 01:15
            intro_video_page.set_designer_timecode('00_01')
            time.sleep(DELAY_TIME)

            main_page.press_space_key()
            time.sleep(DELAY_TIME * 4)
            main_page.press_space_key()

            case.result = check_result

        # [L128] 3.1 Video Intro Designer > Share after modify
        with uuid("94ed80fa-11d3-4b2f-a414-dbcd960110e8") as case:
            # Modify step: Drag (photo) to lower position
            intro_video_page.hover_preview_center()
            main_page.right_click()
            intro_video_page.move_preview_object_to_right_upper(y_threshold=0.6)

            # Edit General title to Swimming ring
            intro_video_page.hover_preview_center(y_threshold=0.5)
            main_page.double_click()
            main_page.input_text('Swimming ring')

            # Leave (Edit mode)
            intro_video_page.cancel_selection_button()

            # Share template step:
            # Click [Share Template] button
            intro_video_page.click_btn_share_template('pink swimming ring')

            # Confirm Copyright Disclaimer
            intro_video_page.share_temp.click_confirm()

            # Input 'Have a nice day' then click share
            share_result = intro_video_page.share_temp.click_share()
            case.result = share_result

        # [L130] 3.1 Video Intro Designer > Add to timeline
        with uuid("6ba6a1b7-3d61-43fd-97b8-17b5865d7d5a") as case:
            intro_video_page.click_btn_add_to_timeline()
            time.sleep(DELAY_TIME * 3)
            # Verify Step1 : Check (OH MINE) MGT is in Video track 2
            timeline_operation_page.select_timeline_media(track_index=2, clip_index=0)
            main_page.double_click()
            check_warning = title_designer_page.mgt.handle_warning_msg(tick_option=0)
            if check_warning:
                title_designer_page.mgt.click_warning_msg_ok()
                check_warning_result = True
            else:
                check_warning_result = False

            # Verify Step 2: Check preview
            title_designer_page.set_timecode('00_00_08_00')
            current_image = intro_video_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                      file_name=Auto_Ground_Truth_Folder + 'I130.png')
            check_result = main_page.compare(Ground_Truth_Folder + 'I130.png', current_image)

            # press ESC to leave title designer
            main_page.press_esc_key()

            case.result = check_warning_result and check_result

            # Save project:
            main_page.top_menu_bar_file_save_project_as()
            main_page.handle_save_file_dialog(name='test_case_1_1_2',
                                              folder_path=Test_Material_Folder + 'BFT_21_Stage1/')

            # Remove (share Video Intro template)
            # If share successfully, then delete template
            if share_result:
                # Open (My Profile)
                intro_video_page.enter_my_profile()
                time.sleep(DELAY_TIME * 8)

                intro_video_page.my_profile.delete_1st_template()
                time.sleep(DELAY_TIME * 5)

            # close (My Profile)
            main_page.press_esc_key()
            time.sleep(DELAY_TIME * 2)

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3_a(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open Preference > Editing > Set default Title duration to 10 (For v21.6.5303 PM request)
        main_page.click_set_user_preferences()
        time.sleep(DELAY_TIME * 2)
        preferences_page.switch_to_editing()
        time.sleep(DELAY_TIME)
        preferences_page.editing.durations_title_set_value('10.0')
        time.sleep(DELAY_TIME * 3)
        preferences_page.click_ok()
        time.sleep(DELAY_TIME)

        # Open project: test_case_1_1_2
        #main_page.top_menu_bar_file_open_project(save_changes='no')
        #main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_2.pds')
        #main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

        # [L132] 3.2 Title Designer > Open Title designer
        with uuid("7a0b1dbb-0c33-4634-8289-ad6a0acd92e1") as case:
            # enter Title room
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 3)

            # Select default title (21.6.5219 : search then select default title)
            media_room_page.search_library('Default')
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('Default')
            main_page.double_click()

            # Verify Step
            check_selected_object = title_designer_page.get_title_text_content()
            if check_selected_object == 'My Title':
                selected_title_content = True
            else:
                selected_title_content = False

            check_caption_bar_content = title_designer_page.get_full_title()
            if check_caption_bar_content == 'Title Designer | Default':
                check_caption_bar = True
            else:
                check_caption_bar = False

            case.result = selected_title_content and check_caption_bar


        # if Font Face is fold, click arrow to unfold
        title_designer_page.unfold_object_font_face_tab(0)
        time.sleep(DELAY_TIME * 2)

        # [L133] 3.2 Title Designer > Modify > Input text case
        with uuid("12487b29-26d5-469a-8b57-64cb21a89679") as case:
            # Express mode
            title_designer_page.switch_mode(1)

            canvas_elem = main_page.exist(L.title_designer.area.frame_video_preview)
            main_page.mouse.click(*canvas_elem.center)
            main_page.double_click()
            title_designer_page.edit_object_title('ÆÂÇÐÉÑ ØÜ Ýåþðìü')
            time.sleep(DELAY_TIME*4)

            # Verify step
            check_selected_object = title_designer_page.get_title_text_content()
            if check_selected_object == 'ÆÂÇÐÉÑ ØÜ Ýåþðìü':
                case.result = True
            else:
                case.result = False

            # Set text string to Two line
            title_text_elem = main_page.exist(L.title_designer.area.edittext_text_content)
            main_page.mouse.click(*title_text_elem.center)
            main_page.press_enter_key()
            main_page.input_text('AWR')

        # [L137] 3.2 Title Designer > Set in [Object] > Font /Paragraph
        with uuid("7b458139-00b3-4178-a4f6-8515fc581f6a") as case:
            main_page.mouse.click(*canvas_elem.center)
            main_page.double_click()
            # Set font
            title_designer_page.set_font_type('IM FELL DW Pica SC Regular')

            # Set size
            title_designer_page.set_font_size('36')

            # Set line spacing amount
            title_designer_page.set_line_spacing_amount('-8')

            # Set text spacing amount
            title_designer_page.set_text_spacing_amount('5')

            # Set font face color
            title_designer_page.set_font_face_color('120', '83', '236')

            # Set kerning
            title_designer_page.set_kerning_check()

            # Set align
            title_designer_page.set_align(2)

            express_mode_preview = main_page.snapshot(locator=L.title_designer.area.window_title_designer)
            # [L135] 3.2 Title Designer > Switch to Advanced mode
            with uuid("9337d05d-e71b-452b-88ed-accf281de8f5") as case:
                # Advanced mode
                title_designer_page.switch_mode(2)

                advance_mode_preview = main_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'L135.png')
                compare_result = main_page.compare(Ground_Truth_Folder + 'L135.png',
                                                        advance_mode_preview)

                # express mode
                title_designer_page.switch_mode(1)
                change_mode = main_page.snapshot(locator=L.title_designer.area.window_title_designer)
                compare_express = main_page.compare(change_mode, express_mode_preview)
                case.result = compare_result and compare_express

            case.result = compare_result

        # [L136] 3.2 Title Designer > Set in [Object] > Character Presets
        with uuid("917276cd-2119-4f6e-a94b-10d03795a2cf") as case:
            time.sleep(DELAY_TIME*2)
            # Apply preset 18
            title_designer_page.apply_character_presets(17)
            time.sleep(DELAY_TIME*2)
            preset_18 = main_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'L136.png')
            compare_preset_18 = main_page.compare(Ground_Truth_Folder + 'L136.png',
                                                        preset_18)

            # Apply preset 10
            title_designer_page.apply_character_presets(9)
            time.sleep(DELAY_TIME * 2)

            # Check preview change
            preset_x = main_page.snapshot(locator=L.title_designer.area.window_title_designer)
            compare_preset_x = main_page.compare(preset_x, preset_18, similarity=0.7)

            # Check preview is NOT the same
            different_preset_x = not main_page.compare(preset_x, preset_18, similarity=0.985)
            case.result = compare_preset_18 and compare_preset_x and different_preset_x

            if main_page.exist(L.title_designer.character_presets.btn_character_presets).AXValue == 1:
                main_page.exist_click(L.title_designer.character_presets.btn_character_presets)
                time.sleep(DELAY_TIME*1.5)

        # [L141] 3.2 Title Designer > Set in [Object] > Backdrop
        with uuid("09c9be51-6a81-4087-9df3-fdd9af36cf60") as case:
            title_designer_page.backdrop.set_unfold_tab()
            time.sleep(DELAY_TIME)
            title_designer_page.backdrop.set_checkbox(bApply=1)

            # Verify 1: Check apply type (Fit with title)
            get_backdrop_type= title_designer_page.backdrop.get_type()
            if get_backdrop_type == 2:
                default_backdrop_type = True
            else:
                default_backdrop_type = False

            # Switch backdrop type (Solid background bar)
            title_designer_page.backdrop.set_type(1)

            # Verify 2: Check width disable
            check_width_disable_result = title_designer_page.backdrop.check_width_disable()

            # Adjust Height value
            title_designer_page.backdrop.height.value.adjust_slider(1.73)
            time.sleep(DELAY_TIME)

            # Un-tick maintain aspect ratio
            title_designer_page.backdrop.set_maintain_aspect_ratio(0)

            title_designer_page.backdrop.height.value.click_arrow(0, 8)
            get_height_value = title_designer_page.backdrop.height.value.get_value()
            if get_height_value == '1.81':
                check_height_value = True
            else:
                logger(get_height_value)
                check_height_value = False
            logger(check_height_value)

            # Check Width value
            get_width_value = title_designer_page.backdrop.width.value.get_value()
            if get_width_value == '1.73':
                check_width_value = True
            else:
                check_width_value = False
            logger(check_width_value)

            # Set uniform color
            title_designer_page.backdrop.apply_uniform_color('#3f24b2')

            # scroll down (scroll bar)
            title_designer_page.drag_object_vertical_slider(1)
            time.sleep(DELAY_TIME)

            # Set opacity
            title_designer_page.backdrop.opacity.value.set_value(88)
            title_designer_page.backdrop.opacity.value.adjust_slider(95)

            # Check opacity value
            get_opacity = title_designer_page.backdrop.opacity.value.get_value()
            if get_opacity == '95':
                check_opacity_value = True
            else:
                check_opacity_value = False
            logger(check_opacity_value)

            # Adjust offset Y to -0.809
            title_designer_page.backdrop.offset_y.value.set_value('-0.809')
            # Check offset Y value
            get_offset_y = title_designer_page.backdrop.offset_y.value.get_value()
            if get_offset_y == '-0.809':
                check_offset_value = True
            else:
                check_offset_value = False
            logger(check_offset_value)

            # scroll down (scroll bar)
            title_designer_page.drag_object_vertical_slider(0.67)
            time.sleep(DELAY_TIME)

            # Switch backdrop type (Fit with title) > Ellipse
            title_designer_page.backdrop.set_type(2,1)
            time.sleep(DELAY_TIME)
            type_ellipse = main_page.snapshot(locator=L.title_designer.area.window_title_designer)

            # Switch backdrop type (Solid background bar)
            title_designer_page.backdrop.set_type(1)
            time.sleep(DELAY_TIME)
            type_sloid = main_page.snapshot(locator=L.title_designer.area.window_title_designer)

            different_type_result = not main_page.compare(type_ellipse, type_sloid, similarity=0.99999)
            case.result = default_backdrop_type and check_width_disable_result and check_height_value and check_width_value and check_opacity_value and check_offset_value and different_type_result

            # fold tab
            title_designer_page.backdrop.set_unfold_tab(unfold=0)
            time.sleep(DELAY_TIME)

            # Set font face color
            title_designer_page.set_check_font_face(bCheck=1)
            title_designer_page.set_font_face_color('128', '215', '144')

            # Set font
            title_designer_page.set_font_type('Barbaro')

            # Disable Border
            title_designer_page.apply_border(bApply=0)

            # Disable Shadow + fold tab
            title_designer_page.set_check_shadow(bCheck=0)
            title_designer_page.unfold_object_shadow_tab(unfold=0)

        # [L134] 3.2 Title Designer > Insert new title
        with uuid("3675bbb6-5abb-4a0c-80a4-f17f0b55b590") as case:
            title_designer_page.insert_title(' suiod fw5')

            # Set size
            title_designer_page.set_font_size('88')

            # Title font: Mystery Quest
            title_designer_page.set_font_type('Mystery Quest')

            # Set font face color
            title_designer_page.set_font_face_color('255', '27', '169')

            # Set line spacing amount
            title_designer_page.set_line_spacing_amount('0')

            # Set text spacing amount
            title_designer_page.set_text_spacing_amount('0')

            # Set kerning
            title_designer_page.set_kerning_check(0)

            time.sleep(DELAY_TIME*2)
            second_title_preview = main_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                      file_name=Auto_Ground_Truth_Folder + 'L134.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L134.png',
                                               second_title_preview)
            case.result = compare_result

        # [L140] 3.2 Title Designer > Set in [Object] > Shadow
        with uuid("cbe24c99-189b-4ce8-8255-16fd4f25e5a5") as case:
            # unfold tab
            title_designer_page.unfold_object_shadow_tab()
            time.sleep(DELAY_TIME)

            # Set Shadow
            title_designer_page.apply_shadow(bApply=1)
            time.sleep(DELAY_TIME)

            # scroll down (scroll bar)
            title_designer_page.drag_object_vertical_slider(1)
            time.sleep(DELAY_TIME)

            # Set distance = 32.5
            title_designer_page.drag_shadow_distance_slider('32')
            for x in range(5):
                title_designer_page.click_shadow_distance_arrow_btn(0)
                time.sleep(DELAY_TIME*0.5)

            # Set blur = 15
            title_designer_page.input_shadow_blur_value('16')
            title_designer_page.click_shadow_blur_arrow_btn(1)

            # Set opacity = 87
            title_designer_page.drag_shadow_opacity_slider('19')
            title_designer_page.input_shadow_opacity_value('87')

            # Set fill shadow = 0
            title_designer_page.set_check_shadow_fill_shadow(bCheck=0)
            title_designer_page.set_shadow_fill_shadow_color('105','250', '5')
            time.sleep(DELAY_TIME)
            no_fill_shadow_preview = main_page.snapshot(locator=L.title_designer.area.window_title_designer)

            # Set fill shadow = 1
            title_designer_page.set_check_shadow_fill_shadow(bCheck=1)
            title_designer_page.set_shadow_fill_shadow_color('33', '134', '215')
            # Set distance = 76.8
            title_designer_page.input_shadow_distance_value('76.8')
            time.sleep(DELAY_TIME)
            fill_shadow_preview = main_page.snapshot(locator=L.title_designer.area.window_title_designer)

            # Check preview change
            compare_fill_preview = main_page.compare(no_fill_shadow_preview, fill_shadow_preview, similarity=0.94)

            # Check preview is NOT the same
            different_fill = not main_page.compare(no_fill_shadow_preview, fill_shadow_preview, similarity=0.99)

            # Set shadow direction = 125
            title_designer_page.input_shadow_direction_value('130')
            title_designer_page.click_shadow_direction_arrow_btn(0)
            for times in range(6):
                title_designer_page.click_shadow_direction_arrow_btn(1)
            main_page.move_mouse_to_0_0()
            time.sleep(DELAY_TIME)
            check_preview = main_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                      file_name=Auto_Ground_Truth_Folder + 'L140.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L140.png',
                                               check_preview)
            case.result = compare_fill_preview and different_fill and compare_result
            # fold tab
            title_designer_page.unfold_object_shadow_tab(unfold=0)

        # Save Template
        title_designer_page.save_as_name('test_1_1_3_a', click_ok=1)

        # Close title designer
        title_designer_page.click_ok()
        time.sleep(DELAY_TIME * 2)

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3_b(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # If test_case_1_1_2 doesn't exist, return skip
        if not main_page.exist_file(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_2.pds'):
            logger('CAN NOT find test_case_1_1_2.pds')
            return

        # Open project: test_case_1_1_2
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_2.pds')
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

        # enter Title Room
        main_page.enter_room(1)
        time.sleep(DELAY_TIME * 3)

        # Custom template
        main_page.select_LibraryRoom_category('Custom')

        # Select 1st Custom teplate "test_1_1_3_a"
        main_page.select_library_icon_view_media('test_1_1_3_a')
        main_page.double_click()
        time.sleep(DELAY_TIME * 6)

        # [L149] 3.2 Title Designer > Manually adjust on canvas
        with uuid("f54750cd-3f0e-463f-8b05-8b84ba456351") as case:
            # Resize
            title_designer_page.adjust_title_on_canvas.resize_to_small(x=5, y=3)
            time.sleep(DELAY_TIME * 2)
            # Rotate
            title_designer_page.adjust_title_on_canvas.drag_rotate_clockwise('45')

            # Switch to Advance mode
            title_designer_page.switch_mode(2)
            time.sleep(DELAY_TIME)

            # Unfold Object
            title_designer_page.unfold_object_object_setting_tab()
            time.sleep(DELAY_TIME * 2)
            title_designer_page.drag_object_vertical_slider(0.757)
            time.sleep(DELAY_TIME * 0.5)

            # Verify step
            check_scale_width_value = title_designer_page.get_object_setting_scale_width_value()
            if float(check_scale_width_value) < 1:
                check_resize_width = True
            else:
                check_resize_width = False

            check_scale_height_value = title_designer_page.get_object_setting_scale_height_value()
            if float(check_scale_height_value) < 1:
                check_resize_height = True
            else:
                check_resize_height = False

            check_rotate_value = title_designer_page.get_object_setting_rotation_value()
            if float(check_rotate_value) > 50:
                check_rotate = True
            else:
                check_rotate = False

            case.result = check_resize_width and check_resize_height and check_rotate

        # [L142] 3.2 Title Designer > Object Settings
        with uuid("adfdbb15-9d4a-4338-be3a-39d0922f896a") as case:
            # Add position 1st keyframe
            title_designer_page.click_object_setting_position_add_keyframe_control()

            title_designer_page.set_timecode('00_00_09_00')
            time.sleep(DELAY_TIME)
            # Add position 2nd keyframe
            title_designer_page.input_object_setting_x_position_value('0.24')
            title_designer_page.input_object_setting_y_position_value('0.935')
            # Add previous keyframe
            title_designer_page.click_object_setting_position_previous_keyframe()

            # Add scale 1st keyframe
            title_designer_page.click_object_setting_scale_add_keyframe_control()

            title_designer_page.set_timecode('00_00_08_00')
            time.sleep(DELAY_TIME)
            # Add position 2nd keyframe
            title_designer_page.input_object_setting_scale_height_value('1.64')

            # scroll down (scroll bar)
            title_designer_page.drag_object_vertical_slider(1)
            time.sleep(DELAY_TIME)

            # Add opacity keyframe
            title_designer_page.click_object_setting_opacity_add_keyframe_control()
            # Add 2nd keyframe
            title_designer_page.set_timecode('00_00_03_00')
            time.sleep(DELAY_TIME)
            title_designer_page.drag_object_setting_opacity_slider('59')
            title_designer_page.drag_object_vertical_slider(1)
            time.sleep(DELAY_TIME)

            # Add rotate keyframe
            title_designer_page.input_object_setting_rotation_value('60')
            title_designer_page.click_object_setting_rotation_add_keyframe_control()
            # Add 2nd keyframe
            title_designer_page.set_timecode('00_00_09_00')
            time.sleep(DELAY_TIME*2)
            title_designer_page.input_object_setting_rotation_value('260')
            time.sleep(DELAY_TIME*2)

            # scroll simple track (scroll bar)
            title_designer_page.drag_simple_track_vertical_slider(0.97)

            # Verify preview
            title_designer_page.set_timecode('00_00_08_00')
            time.sleep(DELAY_TIME)
            check_preview = main_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                               file_name=Auto_Ground_Truth_Folder + 'L142.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L142.png', check_preview, similarity=0.9)
            case.result = compare_result

        # [L143] 3.2 Title Designer > Object Settings > Ease in / Ease out work
        with uuid("94d981a1-511c-44b0-996f-ec255d2ce28a") as case:
            # scroll down (scroll bar)
            title_designer_page.drag_object_vertical_slider(0.65)
            time.sleep(DELAY_TIME)

            # Set Ease in on Scale keyframe
            title_designer_page.set_check_object_setting_scale_ease_in()
            title_designer_page.drag_object_setting_scale_ease_in_slider(0.71)
            check_ease_in_value = title_designer_page.get_object_setting_scale_ease_in_value()
            if float(check_ease_in_value) == 0.71:
                adjust_ease_in_result = True
            else:
                logger(check_ease_in_value)
                adjust_ease_in_result = False

            # click previous keyframe
            title_designer_page.click_object_setting_scale_previous_keyframe()

            # Set Ease out on Scale keyframe
            title_designer_page.set_check_object_setting_scale_ease_out()
            title_designer_page.drag_object_setting_scale_ease_out_slider(0.83)
            check_ease_out_value = title_designer_page.get_object_setting_scale_ease_out_value()
            if float(check_ease_out_value) == 0.83:
                adjust_ease_out_result_scale = True
            else:
                adjust_ease_out_result_scale = False

            logger(adjust_ease_out_result_scale)

            # Reset Scale keyframe
            title_designer_page.click_object_setting_scale_reset_keyframe_control()
            time.sleep(DELAY_TIME*2)
            # Click [Yes] when pop up waring (This operation will reset all keyframe ...)
            main_page.exist_click(L.title_designer.backdrop.warning.btn_yes)

            # scroll upper (scroll bar)
            title_designer_page.drag_object_vertical_slider(0.52)
            time.sleep(DELAY_TIME)

            # Reset Position keyframe
            title_designer_page.click_object_setting_position_reset_keyframe_control()
            time.sleep(DELAY_TIME*2)
            # Click [Yes] when pop up waring (This operation will reset all keyframe ...)
            main_page.exist_click(L.title_designer.backdrop.warning.btn_yes)

            # click next keyframe
            title_designer_page.click_object_setting_rotation_next_keyframe()

            # scroll down (scroll bar)
            title_designer_page.drag_object_vertical_slider(1)
            time.sleep(DELAY_TIME)

            # Set Ease out on Rotation keyframe
            title_designer_page.set_check_object_setting_rotation_ease_out()
            title_designer_page.input_object_setting_rotation_ease_out_value('0.75')
            time.sleep(DELAY_TIME)
            check_ease_out_value = title_designer_page.get_object_setting_rotation_ease_out_value()
            if float(check_ease_out_value) == 0.75:
                adjust_ease_out_result_rotation = True
            else:
                logger(check_ease_out_value)
                adjust_ease_out_result_rotation = False

            case.result = adjust_ease_in_result and adjust_ease_out_result_scale and adjust_ease_out_result_rotation

        # [L148] 3.2 Title Designer > Object Settings > Simple timeline Add / Remove / Switch keyframe
        with uuid("ad107e46-3c92-4dcd-b68c-0d7122e36b04") as case:
            # Check 2nd Title on simple track
            # Current timecode = 00:00:03:00
            title_designer_page.drag_simple_track_vertical_slider(1)

            # Click simple track : Opacity next keyframe
            title_designer_page.click_simple_track_opacity_next_keyframe(track_no=8)
            time.sleep(DELAY_TIME*2)

            # Verify next keyframe button
            current_time_code = title_designer_page.get_timecode()
            if current_time_code == '00:00:08:00':
                check_next_keyframe_btn = True
            else:
                check_next_keyframe_btn = False
            logger(current_time_code)
            logger(check_next_keyframe_btn)

            # Click simple track : Rotation previous keyframe
            title_designer_page.click_simple_track_opacity_previous_keyframe(track_no=9)
            time.sleep(DELAY_TIME*2)

            # Verify previous keyframe button
            current_time_code = title_designer_page.get_timecode()
            if current_time_code == '00:00:03:00':
                check_pre_keyframe_btn = True
            else:
                check_pre_keyframe_btn = False

            logger(check_pre_keyframe_btn)

            # Click simple track : Opacity keyframe [Reset] on the 3s keyframe
            title_designer_page.click_simple_track_opacity_keyframe_control(track_no=8)
            time.sleep(DELAY_TIME*2)

            # Jump to 8s keyframe > Then click [Previous] keyframe to check previous keyframe
            current_time_code = title_designer_page.set_timecode('00_00_08_00')
            title_designer_page.click_simple_track_opacity_previous_keyframe(track_no=8)
            time.sleep(DELAY_TIME * 2)

            # Verify  keyframe Reset button
            current_time_code = title_designer_page.get_timecode()
            if current_time_code == '00:00:08:00':
                check_reset_btn = True
            else:
                logger(current_time_code)
                check_reset_btn = False
            logger(check_reset_btn)

            # Click simple track : Opacity keyframe [Add] for Rotation keyframe
            title_designer_page.click_simple_track_opacity_keyframe_control(track_no=9)
            time.sleep(DELAY_TIME*2)
            # Jump to 9s keyframe > Then click [Previous] keyframe to check previous keyframe
            title_designer_page.set_timecode('00_00_09_00')
            title_designer_page.click_simple_track_opacity_previous_keyframe(track_no=9)
            time.sleep(DELAY_TIME * 2)

            # Verify  keyframe Add button
            current_time_code = title_designer_page.get_timecode()
            if current_time_code == '00:00:08:00':
                check_add_btn = True
            else:
                logger(current_time_code)
                check_add_btn = False
            logger(check_add_btn)

            case.result = check_next_keyframe_btn and check_pre_keyframe_btn and check_reset_btn and check_add_btn

        # [L144] 3.2 Title Designer > Set in [Object] > Special Effect
        with uuid("9019594e-a256-461d-9c2f-0657541e569a") as case:
            # scroll upper (scroll bar)
            title_designer_page.drag_object_vertical_slider(0.64)
            time.sleep(DELAY_TIME)

            # fold tab
            title_designer_page.unfold_object_object_setting_tab(0)
            time.sleep(DELAY_TIME)

            # unfold tab
            title_designer_page.special_effects.set_unfold_tab(1)

            # Apply LED sign
            current_title_preview = main_page.snapshot(locator=L.title_designer.area.obj_title)
            title_designer_page.special_effects.apply_effect(4)

            # Warning: Do you want to continue?
            title_designer_page.handle_special_effect_want_to_continue(option=1)
            time.sleep(DELAY_TIME*5)
            led_title_preview = main_page.snapshot(locator=L.title_designer.area.obj_title)
            is_applied_special_effect_led = not main_page.compare(current_title_preview, led_title_preview, similarity=0.95)
            logger(is_applied_special_effect_led)

            # scroll down (scroll bar)
            title_designer_page.drag_object_vertical_slider(1)
            time.sleep(DELAY_TIME)

            # Check size value
            get_current_value = title_designer_page.special_effects.size.value.get_value()
            if get_current_value == '53':
                check_default_size = True
            else:
                check_default_size = False

            # Apply LED > Look 4
            title_designer_page.special_effects.set_look_menu(4)
            time.sleep(DELAY_TIME * 2)
            # Check current size
            get_current_value = title_designer_page.special_effects.size.value.get_value()
            if get_current_value == '49':
                check_change_size = True
            else:
                check_change_size = False

            # ----------
            # Apply Electric Wave
            title_designer_page.special_effects.apply_effect(6)
            time.sleep(DELAY_TIME * 2)

            # scroll down (scroll bar)
            title_designer_page.drag_object_vertical_slider(1)
            time.sleep(DELAY_TIME)

            # Set size to 108
            title_designer_page.special_effects.size.value.set_value(108)
            # Set Length to 167
            title_designer_page.special_effects.length.value.adjust_slider(167)
            time.sleep(DELAY_TIME * 2)

            electric_title_preview = main_page.snapshot(locator=L.title_designer.area.obj_title)
            is_applied_special_effect = not main_page.compare(electric_title_preview, led_title_preview, similarity=0.95)
            logger(is_applied_special_effect)

            case.result = check_default_size and check_change_size and is_applied_special_effect_led and is_applied_special_effect

        # scroll down (scroll bar)
        title_designer_page.drag_object_vertical_slider(1)
        time.sleep(DELAY_TIME)

        # fold special effect
        title_designer_page.special_effects.set_unfold_tab(0)
        time.sleep(DELAY_TIME)

        # Save Template
        title_designer_page.save_as_name('test_1_1_3_b', click_ok=1)

        # Close title designer
        title_designer_page.click_ok()
        time.sleep(DELAY_TIME * 2)

    # 10 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3_c(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # If test_case_1_1_2 doesn't exist, return skip
        if not main_page.exist_file(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_2.pds'):
            logger('CAN NOT find test_case_1_1_2.pds')
            return

        # Open project: test_case_1_1_2
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_2.pds')
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

        # enter Title Room
        main_page.enter_room(1)
        time.sleep(DELAY_TIME * 3)

        # Custom template
        main_page.select_LibraryRoom_category('Custom')

        # Select 1st Custom teplate "test_1_1_3_b"
        main_page.select_library_icon_view_media('test_1_1_3_b')
        main_page.double_click()
        time.sleep(DELAY_TIME * 6)

        # Current status: Open Title Designer (Advanced) and only unfold "Font / Paragraph"

        # [L145] 3.2 Title Designer > Set Animation > Starting Effect
        with uuid("bb27103b-0bd1-4f73-9eb5-948375335ba1") as case:
            # Set timecode to snapshot before apply animation
            title_designer_page.set_timecode('00_00_02_18')
            time.sleep(DELAY_TIME * 2)
            no_in_animation_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview)

            # Switch to Animation tab > Unfold
            title_designer_page.click_animation_tab()
            title_designer_page.unfold_animation_in_animation_tab()
            title_designer_page.set_timecode('00_00_00_00')

            # Apply In animation: Popup > Magnets II
            title_designer_page.select_animation_in_animation_effect(4, 4)

            # Warning: Do you want to continue?
            title_designer_page.handle_special_effect_want_to_continue(option=1)
            time.sleep(DELAY_TIME*2)

            # Preview play > Pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME*2)
            main_page.press_space_key()

            # Set timecode :
            title_designer_page.set_timecode('00_00_02_18')
            time.sleep(DELAY_TIME * 2)

            # Verify preview 1
            animation_4_title_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview)
            is_applied_in_Magnets_ii = not main_page.compare(animation_4_title_preview, no_in_animation_preview, similarity=0.96)
            logger(is_applied_in_Magnets_ii)

            # Click [Stop]
            title_designer_page.click_preview_operation('Stop')
            time.sleep(DELAY_TIME)

            # Apply In animation: Video rotation > Rotate Counterclockwise
            title_designer_page.select_animation_in_animation_effect(8, 3)
            # Preview play > Pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME*1.6)

            # Click [Stop]
            title_designer_page.click_preview_operation('Stop')
            time.sleep(DELAY_TIME)

            # Verify preview 2
            animation_3_title_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview)
            is_applied_in_Counterclockwise = not main_page.compare(animation_3_title_preview, animation_4_title_preview, similarity=0.98)
            logger(is_applied_in_Counterclockwise)
            case.result = is_applied_in_Magnets_ii and is_applied_in_Counterclockwise

        # ---------------------------------
        # Move 2nd title to left
        # Switch to Object tab > Unfold
        title_designer_page.click_object_tab()

        # Unfold tab
        title_designer_page.unfold_object_object_setting_tab(1)
        time.sleep(DELAY_TIME)

        # Set x position = 0
        title_designer_page.input_object_setting_x_position_value('0')

        # Set roation = 90
        title_designer_page.input_object_setting_rotation_value('90')

        # fold tab
        title_designer_page.unfold_object_object_setting_tab(0)
        time.sleep(DELAY_TIME)
        # ---------------------------------
        # Switch highlight to 1st title
        canvas_elem = main_page.exist(L.title_designer.area.frame_video_preview)
        main_page.mouse.click(*canvas_elem.center)

        # Switch to Animation tab > Unfold
        title_designer_page.click_animation_tab()

        # Warning: Do you want to continue?
        title_designer_page.handle_special_effect_want_to_continue(option=1)
        time.sleep(DELAY_TIME * 2)

        # [L146] 3.2 Title Designer > Set Animation > Ending Effect
        with uuid("df9f83b6-b009-4cbe-9180-2168fd1ad35c") as case:
            # Fold (In animation)
            title_designer_page.unfold_animation_in_animation_tab(0)

            # UnFold (Out animation)
            title_designer_page.unfold_animation_out_animation_tab()

            # Set timecode to snapshot before apply out animation
            title_designer_page.set_timecode('00_00_09_08')
            time.sleep(DELAY_TIME * 2)
            no_out_animation_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview)
            title_designer_page.set_timecode('00_00_00_00')

            # Apply Out animation: Pop up III
            title_designer_page.select_animation_out_animation_effect(6, 5)

            # Warning: Do you want to continue?
            title_designer_page.handle_special_effect_want_to_continue(option=1)
            time.sleep(DELAY_TIME*2)

            # Preview play > Pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME*2)
            main_page.press_space_key()

            # Set timecode :
            title_designer_page.set_timecode('00_00_09_08')
            time.sleep(DELAY_TIME * 2)

            # Verify preview 1
            animation_5_title_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview)
            is_applied_out_slide = not main_page.compare(animation_5_title_preview, no_out_animation_preview, similarity=0.82)
            logger(is_applied_out_slide)

            # Click [Stop]
            title_designer_page.click_preview_operation('Stop')
            time.sleep(DELAY_TIME)

            # Apply Out animation: Vanish
            title_designer_page.select_animation_out_animation_effect(9, 2)

            # Preview play > Pause
            title_designer_page.click_preview_operation('Play')
            time.sleep(DELAY_TIME * 2)
            title_designer_page.click_preview_operation('Pause')

            # Set timecode :
            title_designer_page.set_timecode('00_00_09_08')
            time.sleep(DELAY_TIME * 2)

            # Verify preview 1
            animation_4_title_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview)
            is_applied_out_wipe = not main_page.compare(animation_4_title_preview, animation_5_title_preview,
                                                        similarity=0.98)
            logger(is_applied_out_wipe)

            case.result = is_applied_out_slide and is_applied_out_wipe

        # ---------------------------------
        # Click [Stop]
        title_designer_page.click_preview_operation('Stop')
        time.sleep(DELAY_TIME)

        # [L147] 3.2 Title Designer > Set Motion
        with uuid("c37a6bbf-5989-49ce-bb91-47aac338ddb0") as case:
            # Switch to Motion tab > Unfold
            title_designer_page.click_motion_tab()

            # UnFold Path
            title_designer_page.path.set_unfold()
            time.sleep(DELAY_TIME)

            # scroll down (scroll bar)
            title_designer_page.drag_object_vertical_slider(1)
            time.sleep(DELAY_TIME)

            # Apply path
            title_designer_page.path.select_path(25)
            time.sleep(DELAY_TIME)

            # Verify preview 1
            path_25_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview)

            # scroll down (scroll bar)
            title_designer_page.drag_object_vertical_slider(1)
            time.sleep(DELAY_TIME)

            # Apply path
            title_designer_page.path.select_path(10)
            time.sleep(DELAY_TIME)

            # Verify preview 2
            path_10_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview)
            is_different_path = not main_page.compare(path_25_preview, path_10_preview, similarity=0.9)
            logger(is_different_path)

            # Preview play > Pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 4)
            main_page.press_space_key()

            # Set timecode :
            title_designer_page.set_timecode('00_00_02_29')
            time.sleep(DELAY_TIME * 2)

            # Verify preview 3
            check_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview,
                                               file_name=Auto_Ground_Truth_Folder + 'L147.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L147.png', check_preview, similarity=0.9)
            case.result = compare_result and is_different_path

        # [L150] 3.2 Title Designer > Insert object > Particle
        with uuid("01518edc-0a14-4a92-95c5-baaed5ae0c51") as case:
            # Click [Stop]
            title_designer_page.click_preview_operation('Stop')
            time.sleep(DELAY_TIME)

            # Switch to Object tab > Unfold
            title_designer_page.click_object_tab()

            # Click [Insert particle]
            title_designer_page.click_insert_particle_btn()
            # Select Recreation > 6th template
            title_designer_page.insert_particle(menu_index=6, particle_index=5)

            # Set timecode :
            title_designer_page.set_timecode('00_00_05_28')
            time.sleep(DELAY_TIME * 2)

            # Verify preview 1
            recreation_6_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview)

            title_designer_page.click_undo_btn()
            time.sleep(DELAY_TIME)

            # Click [Insert particle]
            title_designer_page.click_insert_particle_btn()
            # Select Holiday > 1st template (naming: Bamboo)
            title_designer_page.insert_particle(menu_index=4, particle_index=0)

            # Verify preview 2
            hodiday_4_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview)
            is_different_particle = not main_page.compare(recreation_6_preview, hodiday_4_preview, similarity=0.9)
            logger(is_different_particle)

            # Check insert template title
            elem = main_page.exist(L.title_designer.area.edittext_text_content)
            if elem.AXValue == 'Bamboo':
                check_title = True
            else:
                check_title = False
                logger(elem.AXValue)
            case.result = is_different_particle and check_title

        # [L151] 3.2 Title Designer > Insert object > Image
        with uuid("941b1888-0447-45df-b9fd-51f984b219b2") as case:
            # Click [Insert image]
            title_designer_page.insert_image(Test_Material_Folder + 'BFT_21_Stage1/beauty.jpg')

            # Check insert template title
            elem = main_page.exist(L.title_designer.area.edittext_text_content)
            if elem.AXValue == 'beauty.jpg':
                check_image_title = True
            else:
                check_image_title = False

            time.sleep(DELAY_TIME * 2)

            # Resize / move the Image object
            title_designer_page.adjust_title_on_canvas.drag_move_to_left(x=120)
            title_designer_page.adjust_title_on_canvas.resize_to_large(x=80, y=80)
            title_designer_page.adjust_title_on_canvas.drag_rotate_clockwise(45)

            # Set timecode :
            title_designer_page.set_timecode('00_00_02_06')
            time.sleep(DELAY_TIME * 2)

            current_image = main_page.snapshot(locator=L.title_designer.area.frame_video_preview, file_name=Auto_Ground_Truth_Folder + 'L151.png')
            check_image = main_page.compare(Ground_Truth_Folder + 'L151.png', current_image, similarity=0.9)
            case.result = check_image_title and check_image

        # [L152] 3.2 Title Designer > Insert object > Background Image
        with uuid("ea00aff9-e85e-447f-981a-ecd745ad0838") as case:
            # Click [Insert BG]
            title_designer_page.insert_background(Test_Material_Folder + 'BFT_21_Stage1/outside.jpg')

            title_designer_page.insert_background_adjust_setting(0)
            time.sleep(DELAY_TIME*2)
            # Check preview update:
            current_image = main_page.snapshot(locator=L.title_designer.area.frame_video_preview)
            check_BG = not main_page.compare(Ground_Truth_Folder + 'L151.png', current_image, similarity=0.9)

            # Click (Delete BG) button
            title_designer_page.click_delete_background_btn()
            time.sleep(DELAY_TIME)

            current_image = main_page.snapshot(locator=L.title_designer.area.frame_video_preview)
            check_no_BG = main_page.compare(Ground_Truth_Folder + 'L151.png', current_image)
            case.result = check_BG and check_no_BG

            # Undo
            title_designer_page.click_undo_btn()

        # [L153] 3.2 Title Designer > Preview > in designer & full screen
        with uuid("609fda02-864a-4c71-900b-6bf39f7b54ac") as case:
            # Click [full screen]
            title_designer_page.click_maximize_btn()

            # Preview play > Pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME*7)

            # Click [Stop]
            title_designer_page.click_preview_operation('Stop')
            time.sleep(DELAY_TIME*2)

            full_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview, file_name=Auto_Ground_Truth_Folder + 'L153_full.png')
            check_result_full = main_page.compare(Ground_Truth_Folder + 'L153_full.png', full_preview, similarity=0.9)

            # Click [restore button]
            title_designer_page.click_maximize_btn()
            time.sleep(DELAY_TIME*2)

            restore_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview, file_name=Auto_Ground_Truth_Folder + 'L153.png')
            check_result_restore = main_page.compare(Ground_Truth_Folder + 'L153.png', restore_preview, similarity=0.9)
            case.result = check_result_full and check_result_restore

        # [L154] 3.2 Title Designer > Share template DZ and Cloud
        with uuid("441355f4-e673-45fc-b3e4-1b8189a15db8") as case:
            # Click [Share] > Upload to "Cyberlink Cloud and DZ"
            # Verify DZ link
            check_upload = title_designer_page.share_to_dz(name='title_particle_text', upload_option=0, style='Romance', tags='123', collection='test', description='Great', verify_dz_link=1)
            check_dz_result = check_upload
            logger(check_dz_result)

            # Click [Cancel] to close title designer
            title_designer_page.click_cancel()

            # Click download content form CL/DZ
            title_room_page.click_DownloadContent_from_DZCL()
            time.sleep(DELAY_TIME * 2)

            # Already enter "Download Title Templates" > Open My Cyberlink Cloud
            # Select template name "title_particle_text"
            check_CL_content = download_from_cl_dz_page.select_template('title_particle_text')
            logger(check_CL_content)
            time.sleep(DELAY_TIME)
            download_from_cl_dz_page.tap_delete_button()
            time.sleep(DELAY_TIME*3)

            # Close "Download Title Templates" window
            # download_from_cl_dz_page.tap_close_button()
            main_page.press_esc_key()
            time.sleep(DELAY_TIME)

            case.result = check_dz_result and check_CL_content

        # [L155] 3.2 Title Designer > Save template
        with uuid("5ce4dc5e-1d12-4e48-83f2-ffcc25408da0") as case:
            # Click "title_particle_text" template to title designer
            main_page.select_library_icon_view_media('title_particle_text')
            main_page.right_click()
            main_page.select_right_click_menu('Modify Template')

            # Enter title designer > Modify font face
            # Set font face color
            title_designer_page.set_font_face_color('85', '6', '208')

            time.sleep(DELAY_TIME)

            # Save template
            main_page.click(L.title_designer.btn_save_as)
            title_designer_page.click_custom_name_ok('BFT_title_Save')

            current_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview)

            # Click [Cancel]
            title_designer_page.click_cancel()

            # Verify Step
            main_page.select_library_icon_view_media('BFT_title_Save')
            main_page.right_click()
            main_page.select_right_click_menu('Modify Template')

            # Set timecode :
            title_designer_page.set_timecode('00_00_05_00')
            time.sleep(DELAY_TIME * 2)

            saved_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview)
            check_save_result = main_page.compare(current_preview, saved_preview, similarity=0.99)
            case.result = check_save_result

        # [L156] 3.2 Title Designer > Add saved title template to timeline
        with uuid("fb5b54c4-d0a8-4a3d-ac92-09e88ccf330b") as case:
            # Click [Cancel] to close title designer
            title_designer_page.click_cancel()

            # select timeline track 1
            main_page.timeline_select_track(1)

            # Set timecode :
            main_page.set_timeline_timecode('00_00_10_00')
            time.sleep(DELAY_TIME * 2)

            # Drag BFT_title_Save to timeline track1
            main_page.drag_media_to_timeline_playhead_position('BFT_title_Save')

            # Play timeline preview
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 6)
            main_page.press_space_key()

            # Set timecode :
            main_page.set_timeline_timecode('00_00_16_23')
            time.sleep(DELAY_TIME * 2)

            timeline_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view, file_name=Auto_Ground_Truth_Folder + 'L156.png')
            check_current_title = main_page.compare(Ground_Truth_Folder + 'L156.png', timeline_preview, similarity=0.9)
            case.result = check_current_title

        # Save project:
        main_page.top_menu_bar_file_save_project_as()
        main_page.handle_save_file_dialog(name='test_case_1_1_3',
                                          folder_path=Test_Material_Folder + 'BFT_21_Stage1/')
        time.sleep(DELAY_TIME * 2)

    # 13 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open project: test_case_1_1_3
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_3.pds')
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

        # [L158] 3.3 Title Designer (motion graphics title) > Open Title designer
        with uuid("f36c7d26-cec9-47aa-a29c-9aff9bb61e6c") as case:
            # enter Title room
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 3)
            main_page.select_LibraryRoom_category('Motion Graphics')
            time.sleep(DELAY_TIME)
            main_page.select_library_icon_view_media('Motion Graphics 002')

            # Enter title designer
            main_page.double_click()
            time.sleep(DELAY_TIME * 2)
            title_designer_page.mgt.click_warning_msg_ok()

            check_title_caption = title_designer_page.get_title()
            logger(check_title_caption)

            if check_title_caption == 'Motion Graphics 002':
                case.result = True
            else:
                case.result = False

        # [L159] 3.3 Title Designer (motion graphics title) > Title > Select title track
        with uuid("1819ea47-ec11-402e-ab01-bf894b84a615") as case:
            # Unfold Title
            title_designer_page.mgt.unfold_title_tab()

            # Get current selected track
            selected_track_elem = main_page.exist(L.title_designer.title.cbx_select_title).AXTitle
            if selected_track_elem == 'PowerDirector':
                default_status = True
            else:
                default_status = False

            # Switch to other track
            title_designer_page.mgt.select_title_track('By CyberLink')

            # Check current selected track
            selected_track_elem = main_page.exist(L.title_designer.title.cbx_select_title).AXTitle
            if selected_track_elem == 'By CyberLink':
                selected_status = True
            else:
                selected_status = False

            case.result = default_status and selected_status

        # [L160] 3.3 Title Designer (motion graphics title) > Title > Edit text
        with uuid("b7e68c42-15cc-4296-92c2-8ed8ff57bbe1") as case:
            title_designer_page.mgt.input_title_text('がぎぐげご さしすせ')

            # Check current selected track
            selected_track_elem = main_page.exist(L.title_designer.title.cbx_select_title).AXTitle
            if selected_track_elem == 'がぎぐげご さしすせ':
                edit_result = True
            else:
                edit_result = False

            # Modify font type
            title_designer_page.mgt.apply_font_type('Trebuchet MS Regular')

            # Apply Bold
            title_designer_page.mgt.click_bold_btn()

            # Apply font color
            title_designer_page.mgt.apply_font_face_color('2200E9')

            # Switch to other track -----------------------------------
            title_designer_page.mgt.select_title_track('PowerDirector')

            title_designer_page.mgt.input_title_text('許功蓋＠＃&*_-<>?')

            # Modify font type
            title_designer_page.mgt.apply_font_type('Hoefler Text Regular')

            # Apply font color
            title_designer_page.mgt.apply_font_face_color('EA10D7')

            # Check current selected track
            selected_track_elem = main_page.exist(L.title_designer.title.cbx_select_title).AXTitle
            if selected_track_elem == '許功蓋＠＃&*_-<>?':
                modify_result = True
            else:
                modify_result = False

            case.result = edit_result and modify_result

            # Click [Zoom in] > 87%
            for x in range(3):
                title_designer_page.click_zoom_in()

        # [L161] 3.3 Title Designer (motion graphics title) > Able to change group color
        with uuid("d8e3d3ad-3758-42e4-922b-6f74d499130a") as case:
            # Unfold Graphics Color
            title_designer_page.mgt.unfold_graphics_color_tab()

            # Change color 1
            title_designer_page.mgt.apply_graphics_color(group_no=1, HexColor='A81B22')

            # Change color 2
            title_designer_page.mgt.apply_graphics_color(group_no=2, HexColor='C8D996')

            # Change color 3
            title_designer_page.mgt.apply_graphics_color(group_no=3, HexColor='18FA4F')

            time.sleep(DELAY_TIME*1.5)
            mgt_preview = main_page.snapshot(locator=L.title_designer.main_window, file_name=Auto_Ground_Truth_Folder + 'L161.png')
            check_current_title = main_page.compare(Ground_Truth_Folder + 'L161.png', mgt_preview)
            case.result = check_current_title

        # [L162] 3.3 Title Designer (motion graphics title) > Object Settings > Position
        with uuid("14b89fd0-4bcb-4247-abaf-011187aa74e2") as case:
            # Unfold Object Setting
            title_designer_page.mgt.unfold_object_setting_tab()
            default_x_value = title_designer_page.mgt.get_position_x_value()

            if default_x_value == '0.500':
                default_x_status = True
            else:
                default_x_status = False

            default_y_value = title_designer_page.mgt.get_position_y_value()

            if default_y_value == '0.500':
                default_y_status = True
            else:
                default_y_status = False

            # Set x = 0.603, y = 0.531
            title_designer_page.mgt.set_position_x_value('0.60')
            title_designer_page.mgt.set_position_y_value('0.53')
            title_designer_page.mgt.click_position_x_arrow_btn(0, 3)
            title_designer_page.mgt.click_position_y_arrow_btn(0, 1)

            time.sleep(DELAY_TIME)
            check_x_value = title_designer_page.mgt.get_position_x_value()

            if check_x_value == '0.603':
                modify_x = True
            else:
                modify_x = False

            check_y_value = title_designer_page.mgt.get_position_y_value()

            if check_y_value == '0.531':
                modify_y = True
            else:
                modify_y = False

            case.result = default_x_status and default_y_status and modify_x and modify_y
        # Scroll down
        title_designer_page.drag_object_vertical_slider(1)

        # [L163] 3.3 Title Designer (motion graphics title) > Object Settings > Scale
        with uuid("b30d1cc7-6482-472d-8a2f-382ed7bf011b") as case:
            default_w_value = title_designer_page.mgt.get_scale_width_value()

            if default_w_value == '1.25':
                default_w_status = True
            else:
                default_w_status = False

            default_h_value = title_designer_page.mgt.get_scale_height_value()

            if default_h_value == '1.25':
                default_h_status = True
            else:
                default_h_status = False

            # Set w = 2.01, h = 3.26
            title_designer_page.mgt.set_scale_width_value('2.1')
            title_designer_page.mgt.click_maintain_aspect_ratio(0)

            title_designer_page.mgt.set_scale_height_value('3.3')
            title_designer_page.mgt.click_scale_width_arrow_btn(1, 9)
            title_designer_page.mgt.click_scale_height_arrow_btn(1, 4)

            time.sleep(DELAY_TIME)

            # Verify Step
            check_w_value = title_designer_page.mgt.get_scale_width_value()

            if check_w_value == '2.01':
                modify_w = True
            else:
                modify_w = False

            check_h_value = title_designer_page.mgt.get_scale_height_value()

            if check_h_value == '3.26':
                modify_h = True
            else:
                modify_h = False

            case.result = default_w_status and default_h_status and modify_w and modify_h

        # [L164] 3.3 Title Designer (motion graphics title) > Object Settings > Rotation
        with uuid("a4cd66bc-3eb9-4e64-b37c-92ed9118657e") as case:
            default_rotation_value = title_designer_page.mgt.get_rotation_value()
            if default_rotation_value == '0.00':
                default_rotation = True
            else:
                default_rotation = False

            title_designer_page.mgt.set_rotation_value('146')
            time.sleep(DELAY_TIME)

            check_rotation_value = title_designer_page.mgt.get_rotation_value()
            if check_rotation_value == '146.00':
                check_rotation = True
            else:
                check_rotation = False

            rotate_preview = main_page.snapshot(locator=L.title_designer.main_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'L164.png')
            check_current_title = main_page.compare(Ground_Truth_Folder + 'L164.png', rotate_preview)

            # Click [Zoom out] twice : 67%
            for x in range(2):
                title_designer_page.click_zoom_out()

            case.result = default_rotation and check_rotation and check_current_title

        # [L165] 3.3 Title Designer (motion graphics title) > Adjust object on preview > Resize

        with uuid("1ca3cc38-c3b0-4e76-a6dd-d29e2d813324") as case:
            # Click [Undo] button > Rotation = 0
            title_designer_page.click_undo_btn()
            time.sleep(DELAY_TIME)

            mgt_default_preview = main_page.snapshot(locator=L.title_designer.area.obj_title)
            #logger(mgt_default_preview)

            # Resize
            title_designer_page.adjust_title_on_canvas.resize_to_small(x=25, y=30)
            mgt_resize_preview = main_page.snapshot(locator=L.title_designer.area.obj_title)
            #logger(mgt_resize_preview)

            check_resize_result = main_page.compare(mgt_default_preview, mgt_resize_preview)

            case.result = not check_resize_result

        # [L167] 3.3 Title Designer (motion graphics title) > Adjust object on preview > Move
        with uuid("8a0620c0-7a8a-48c6-945d-640efcf63cbf") as case:
            # Scroll up
            title_designer_page.drag_object_vertical_slider(0)

            # Switch to other track
            title_designer_page.mgt.select_title_track('がぎぐげご さしすせ')

            time.sleep(DELAY_TIME*2)
            # Move right
            title_designer_page.adjust_title_on_canvas.drag_move_MGT_to_right(drag_x=55)

            mgt_move_preview = main_page.snapshot(locator=L.title_designer.area.obj_title)
            check_move_result = main_page.compare(mgt_resize_preview, mgt_move_preview)

            case.result = not check_move_result

        # [L166] 3.3 Title Designer (motion graphics title) > Adjust object on preview > Rotate

        with uuid("ffe8e1ca-1579-4072-a267-44c543fc7f43") as case:
            # Max window (VDE224621-0024)
            # title_designer_page.click_maximize_btn()
            time.sleep(DELAY_TIME)
            before_rotate_preview = main_page.snapshot(locator=L.title_designer.main_window)
            if before_rotate_preview is None:
                case.result = False
                case.fail_log = 'VDE224621-0024'
            else:
                # Rotate
                title_designer_page.adjust_title_on_canvas.drag_rotate_clockwise('120')
                time.sleep(DELAY_TIME)
                after_rotate_preview = main_page.snapshot(locator=L.title_designer.main_window)

                check_rotate_result = main_page.compare(before_rotate_preview, after_rotate_preview)
                case.result = not check_rotate_result

        # [L168] 3.3 Title Designer (motion graphics title) > Preview in designer
        with uuid("eaaca4e6-220a-4e9f-bf56-15612cc92425") as case:
            # Play then stop
            title_designer_page.mgt.click_preview_operation('Play')
            check_preview_update = main_page.Check_PreviewWindow_is_different(L.title_designer.area.frame_preview, sec=2)
            logger(check_preview_update)

            time.sleep(DELAY_TIME*4)
            #main_page.press_space_key()
            title_designer_page.mgt.click_preview_operation('Stop')
            time.sleep(DELAY_TIME)

            # Set timecode :
            title_designer_page.set_timecode('00_00_08_16')
            time.sleep(DELAY_TIME * 2)

            current_timecode_preview = main_page.snapshot(locator=L.title_designer.area.frame_preview, file_name=Auto_Ground_Truth_Folder + 'L168.png')

            check_preview = main_page.compare(Ground_Truth_Folder + 'L168.png', current_timecode_preview)
            case.result = check_preview

        # [L169] 3.3 Title Designer (motion graphics title) > Save / Save as template
        with uuid("c95ee09b-deb2-48b5-a606-e08332a79148") as case:
            # Save template
            main_page.click(L.title_designer.btn_save_as)
            title_designer_page.click_custom_name_ok('BFT_MGT_Save')

            current_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview)

            # Click [OK]
            title_designer_page.click_ok()

            # Verify Step
            main_page.select_library_icon_view_media('BFT_MGT_Save')
            main_page.double_click()
            time.sleep(DELAY_TIME * 2)
            title_designer_page.mgt.click_warning_msg_ok()

            # Set timecode :
            title_designer_page.set_timecode('00_00_08_16')
            time.sleep(DELAY_TIME*2)

            # Set zoom menu to 67%
            title_designer_page.mgt.click_zoom_in()
            time.sleep(DELAY_TIME)

            saved_preview = main_page.snapshot(locator=L.title_designer.area.frame_preview,  file_name=Auto_Ground_Truth_Folder + 'L169.png')
            check_save_result = main_page.compare(Ground_Truth_Folder + 'L168.png', saved_preview, similarity=0.98)
            case.result = check_save_result
        # Click [OK]
        title_designer_page.click_ok()

        # [L170] 3.3 Title Designer (motion graphics title) > Add saved
        with uuid("6f207683-e25a-43e9-96d0-dde73bc9db9b") as case:
            # select timeline track 2
            main_page.timeline_select_track(2)

            # Set timecode :
            main_page.set_timeline_timecode('00_00_09_00')
            time.sleep(DELAY_TIME * 2)

            # Drag BFT_title_Save to timeline track 2
            main_page.drag_media_to_timeline_playhead_position('BFT_MGT_Save', track_no=2)

            # Play timeline preview
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 5.5)
            playback_window_page.Edit_Timeline_PreviewOperation('STOP')

            # Set timecode :
            main_page.set_timeline_timecode('00_00_17_19')
            time.sleep(DELAY_TIME * 2)

            timeline_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view, file_name=Auto_Ground_Truth_Folder + 'L170.png')
            check_current_title = main_page.compare(Ground_Truth_Folder + 'L170.png', timeline_preview, similarity=0.85)
            case.result = check_current_title

        # Save project:
        main_page.top_menu_bar_file_save_project_as()
        main_page.handle_save_file_dialog(name='test_case_1_1_4',
                                          folder_path=Test_Material_Folder + 'BFT_21_Stage1/')

    #  22 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME * 4)

        # Open project: test_case_1_1_4
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_4.pds')
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

        # select timeline track 3
        main_page.timeline_select_track(3)

        # Set timecode :
        main_page.set_timeline_timecode('00_00_09_00')
        time.sleep(DELAY_TIME * 2)

        # [L172] 3.3 Pip Designer (Dialog_09) > Open PiP designer
        with uuid("4ddeabc0-9f40-4621-bd9a-118beeef450e") as case:
            # enter PiP room
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 3)
            # Select template (21.6.5219 : search then select Mood Sticker 09)
            media_room_page.search_library('Mood Sticker')
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Mood Stickers 09')
            # Download IAD template
            time.sleep(DELAY_TIME * 4)
            main_page.right_click()
            main_page.select_right_click_menu('Add to Timeline')
            time.sleep(DELAY_TIME * 2)

            # Set template duration to 10 sec.
            #tips_area_page.click_TipsArea_btn_Duration()
            #tips_area_page.apply_duration_settings('00_00_10_00')

            main_page.tips_area_click_set_length_of_selected_clip('00_00_10_00')

            # On timeline track 2 : Select Dialog_09 > double click to enter pip designer
            timeline_operation_page.select_timeline_media(track_index=4, clip_index=1)
            main_page.double_click()
            check_title = pip_designer_page.get_title()
            if check_title == 'Mood Stickers 09':
                case.result = True
            else:
                case.result = False

        # [L173] 3.3 Pip Designer > Switch to [Advance] mode or [Express] Mode
        with uuid("ef3ed38d-1e2a-483d-a25e-f59b89c4fa5f") as case:
            get_mode = pip_designer_page.express_mode.get_current_mode()
            if get_mode == 'Express Mode':
                default_express_mode = True
            else:
                default_express_mode = False
            logger(default_express_mode)

            pip_designer_page.switch_mode('Advanced')
            time.sleep(DELAY_TIME*2)
            animation_elem = main_page.exist(L.pip_designer.tab_animation)
            if animation_elem == None:
                switch_advanced_mode = False
            else:
                switch_advanced_mode = True

            pip_designer_page.switch_mode('Express')
            time.sleep(DELAY_TIME*2)
            get_mode = pip_designer_page.express_mode.get_current_mode()
            logger(get_mode)
            if get_mode == 'Express Mode':
                switch_express_mode = True
            else:
                logger(get_mode)
                switch_express_mode = False

            case.result = default_express_mode and switch_advanced_mode and switch_express_mode
            logger(default_express_mode)
            logger(switch_advanced_mode)
            logger(switch_express_mode)

        # [L174] 3.3 Pip Designer > Set in [Properties] > Object Setting - Opacity
        with uuid("6d387c5c-3982-4b6e-ab94-a79ee7b4cbd0") as case:
            # Unfold Object Settings
            pip_designer_page.express_mode.unfold_properties_object_setting_tab()
            get_opacity_default = pip_designer_page.express_mode.get_object_setting_opacity_value()
            logger(get_opacity_default)

            if get_opacity_default == '100%':
                default_value = True
            else:
                default_value = False

            # Click arrow button to 76%
            pip_designer_page.express_mode.click_object_setting_opacity_arrow_btn(1,25)
            time.sleep(DELAY_TIME)
            pip_designer_page.express_mode.click_object_setting_opacity_arrow_btn(0, 1)

            check_opacity = pip_designer_page.express_mode.get_object_setting_opacity_value()
            if check_opacity == '76%':
                apply_opacity = True
            else:
                apply_opacity = False

            case.result = default_value and apply_opacity
            logger(default_value)
            logger(apply_opacity)

        # [L179] 3.3 Pip Designer > Object Setting > Able to add position/scale/opacity/Rotation keyframe with correct value
        with uuid("91625334-9a98-4452-8055-5a199526738f") as case:
            pip_designer_page.switch_mode('Advanced')

            # Add position keyframe: 0s Position: (0.5, 0.5)
            pip_designer_page.add_remove_position_current_keyframe()

            # Set (04:12), Position: (0.803, 0.68)
            pip_designer_page.set_timecode('00_00_04_12')
            pip_designer_page.input_x_position_value('0.803')
            time.sleep(DELAY_TIME)
            pip_designer_page.input_y_position_value('0.68')

            # Click previous keyframe
            pip_designer_page.tap_position_previous_keyframe()
            get_timecode = pip_designer_page.get_timecode()
            if get_timecode == '00:00:00:00':
                set_1st_keyframe = True
            else:
                set_1st_keyframe = False
            logger(set_1st_keyframe)

            # Click next keyframe
            pip_designer_page.tap_position_next_keyframe()
            get_x_value = pip_designer_page.get_x_position_value()
            logger(get_x_value)
            if get_x_value == '0.803':
                set_2nd_x_keyframe = True
            else:
                set_2nd_x_keyframe = False

            get_y_value = pip_designer_page.get_y_position_value()
            logger(get_y_value)
            if get_y_value == '0.680':
                set_2nd_y_keyframe = True
            else:
                set_2nd_y_keyframe = False

            # -----------
            # Set Scale : 1st keyframe
            pip_designer_page.drag_scale_width_slider('1.733')
            pip_designer_page.add_remove_scale_current_keyframe()

            pip_designer_page.click_scale_maintain_aspect_ratio(bCheck=0)
            # Set (07:15)
            pip_designer_page.set_timecode('00_00_07_15')

            # Set Scale : 2nd keyframe
            pip_designer_page.input_scale_height_value('2.857')

            # Set Position : 3rd keyframe
            pip_designer_page.input_x_position_value('0.350')
            time.sleep(DELAY_TIME)
            pip_designer_page.input_y_position_value('0.761')

            # Click previous keyframe
            pip_designer_page.tap_position_previous_keyframe()
            time.sleep(DELAY_TIME)
            # Remove 2nd Position keyframe (only exist 1st, last keyframe)
            pip_designer_page.add_remove_position_current_keyframe()

            # drag scroll bar
            pip_designer_page.drag_properties_scroll_bar(0.72)
            # Set Rotation : 1st keyframe on (04:12)  0 degree
            pip_designer_page.add_remove_rotation_current_keyframe()

            # drag simple timeline to larger (Can see Rotation keyframe track)
            pip_designer_page.drag_simple_timeline_track_to_lager()

            # Click max button
            pip_designer_page.click_maximize_btn()
            time.sleep(DELAY_TIME)
            # drag properties scroll bar
            pip_designer_page.drag_properties_scroll_bar(0)

            # Verify step:
            # Check position on timecode 04:12
            current_x_value = pip_designer_page.get_x_position_value()
            logger(current_x_value)
            if current_x_value == '0.412':
                check_pos_x = True
            else:
                check_pos_x = False

            current_y_value = pip_designer_page.get_y_position_value()
            logger(current_y_value)
            if current_y_value == '0.653':
                check_pos_y = True
            else:
                check_pos_y = False

            case.result = set_1st_keyframe and set_2nd_x_keyframe and set_2nd_y_keyframe and check_pos_x and check_pos_y
            logger(set_1st_keyframe)
            logger(set_2nd_x_keyframe)
            logger(set_2nd_y_keyframe)
            logger(check_pos_x)
            logger(check_pos_y)

        # [L183] 3.3 Pip Designer > Adjust keyframe > Add
        with uuid("9e576f88-8a62-47ff-bc6a-58f75116b112") as case:
            # Set Opacity : 1st keyframe (00:20)
            pip_designer_page.set_timecode('00_00_00_20')
            pip_designer_page.add_remove_opacity_track_current_keyframe()

            # Set Opacity : 2nd keyframe (01:20)
            pip_designer_page.set_timecode('00_00_01_20')
            pip_designer_page.add_remove_opacity_track_current_keyframe()

            # Set Opacity : 3rd keyframe (03:10)
            pip_designer_page.set_timecode('00_00_03_10')
            pip_designer_page.add_remove_opacity_track_current_keyframe()

            # Set Rotation : 2nd keyframe (03:10) 270 degree
            pip_designer_page.add_remove_rotation_track_current_keyframe()
            pip_designer_page.input_rotation_degree_value(270)

            # Set Opacity to 99% on 3rd keyframe
            pip_designer_page.express_mode.drag_object_setting_opacity_slider('99')

            # Set Opacity to 25% on 2nd keyframe
            pip_designer_page.tap_opacity_track_previous_keyframe()
            pip_designer_page.express_mode.drag_object_setting_opacity_slider('25')

            # Verify step:
            check_timecode = pip_designer_page.get_timecode()
            if check_timecode == '00:00:01:20':
                add_opacity_keyframe_ok = True
            else:
                add_opacity_keyframe_ok = False

            # Check 1st rotation keyframe & degree
            pip_designer_page.tap_rotation_next_keyframe()
            check_timecode = pip_designer_page.get_timecode()
            if check_timecode == '00:00:03:10':
                add_rotation_keyframe_ok = True
            else:
                add_rotation_keyframe_ok = False

            # Check degree
            current_degree = pip_designer_page.exist(L.pip_designer.object_setting.rotation.degree_value)
            if current_degree.AXValue == '270':
                current_degree_value = True
            else:
                current_degree_value = False
                logger(current_degree.AXValue)

            case.result = add_opacity_keyframe_ok and add_rotation_keyframe_ok and current_degree_value
            logger(add_opacity_keyframe_ok)
            logger(add_rotation_keyframe_ok)
            logger(current_degree_value)

        # [L185] 3.3 Pip Designer > Adjust keyframe > Switch keyframe
        with uuid("fb1acb9f-1c3a-4f23-b1c6-389d9d42d3d5") as case:
            # Click Scale next keyframe
            for x in range(2):
                pip_designer_page.tap_scale_track_next_keyframe()
                time.sleep(DELAY_TIME)

            # Click Position previous keyframe
            pip_designer_page.tap_position_track_previous_keyframe()

            # Verify Step:
            check_timecode = pip_designer_page.get_timecode()
            if check_timecode == '00:00:00:00':
                switch_keyframe_ok = True
            else:
                switch_keyframe_ok = False

            check_preview = main_page.snapshot(locator=L.pip_designer.designer_window,
                                               file_name=Auto_Ground_Truth_Folder + 'L185.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L185.png', check_preview)
            case.result = switch_keyframe_ok and compare_result
            logger(switch_keyframe_ok)
            logger(compare_result)

        # Reset all Position keyframe
        pip_designer_page.reset_position_keyframe()
        time.sleep(DELAY_TIME*2)
        main_page.click(L.main.confirm_dialog.btn_yes)
        # Reset all Scale keyframe
        pip_designer_page.reset_scale_keyframe()
        time.sleep(DELAY_TIME*2)
        main_page.click(L.main.confirm_dialog.btn_yes)

        # Reset all Opacity keyframe
        pip_designer_page.reset_position_opacity_keyframe()
        time.sleep(DELAY_TIME*2)
        main_page.click(L.main.confirm_dialog.btn_yes)

        # Reset all Rotation keyframe
        pip_designer_page.reset_rotation_keyframe()
        time.sleep(DELAY_TIME*2)
        main_page.click(L.main.confirm_dialog.btn_yes)

        # Set Scale  width / height to 0.378
        pip_designer_page.click_scale_maintain_aspect_ratio(bCheck=1)
        pip_designer_page.drag_scale_width_slider('0.378')

        # Set Position : 0s (0.919, 0.164)
        pip_designer_page.input_x_position_value('0.919')
        time.sleep(DELAY_TIME)
        pip_designer_page.input_y_position_value('0.164')

        # [L180] 3.3 Pip Designer > Object Settings > Able to set Ease in/out setting
        with uuid("1a408d6c-fdf1-4e46-9856-e3caaa0bcc65") as case:
            # Add position 1st keyframe
            pip_designer_page.add_remove_position_track_current_keyframe()

            # Set Position 2nd keyframe at timecode (05:04)
            pip_designer_page.set_timecode('00_00_05_04')
            pip_designer_page.input_x_position_value('0.106')

            # Set Position 3rd keyframe at timecode (10:00)
            pip_designer_page.set_timecode('00_00_10_00')
            pip_designer_page.input_x_position_value('0.894')
            time.sleep(DELAY_TIME)
            pip_designer_page.input_y_position_value('0.836')

            # Enable Ease in and Ease out on 2nd keyframe
            pip_designer_page.click_specific_keyframe(1)
            pip_designer_page.click_position_ease_in_checkbox(1)
            pip_designer_page.input_position_ease_in_value('0.88')

            pip_designer_page.click_position_ease_out_checkbox(1)
            pip_designer_page.input_position_ease_out_value('0.97')

            # Verify Step
            pip_designer_page.click_specific_keyframe(1)
            check_menu_ease_in_status = pip_designer_page.simple_timeline.right_click_menu.get_ease_in_status()
            logger(check_menu_ease_in_status)
            pip_designer_page.click_specific_keyframe(1)
            check_menu_ease_out_status = pip_designer_page.simple_timeline.right_click_menu.get_ease_out_status()
            logger(check_menu_ease_out_status)

            # Check position (x) in timecode (04:11)
            pip_designer_page.set_timecode('00_00_04_11')
            check_x_position = pip_designer_page.get_x_position_value()
            logger(check_x_position)
            if check_x_position == '0.132':
                check_x_status = True
            else:
                check_x_status = False

            # Check position (y) in timecode (06:01)
            pip_designer_page.set_timecode('00_00_06_01')
            check_y_position = pip_designer_page.get_y_position_value()
            logger(check_y_position)
            if check_y_position == '0.197':
                check_y_status = True
            else:
                check_y_status = False

            case.result = check_menu_ease_in_status and check_menu_ease_out_status and check_x_status and check_y_status

        # [L184] 3.3 Pip Designer > Adjust keyframe > Remove
        with uuid("8249bb39-3372-4174-9cf8-813a881f9816") as case:
            # Remove Position keyframe: 1st , 2nd
            for x in range(2):
                # Click previous keyframe
                pip_designer_page.tap_position_track_previous_keyframe()
                # Remove keyframe
                pip_designer_page.add_remove_position_current_keyframe()

            # Remove Position keyframe: 3rd
            pip_designer_page.tap_position_next_keyframe()
            pip_designer_page.add_remove_position_current_keyframe()

            # Verify Step:
            # Click previous keyframe
            pip_designer_page.tap_position_track_previous_keyframe()

            check_timecode = pip_designer_page.get_timecode()
            logger(check_timecode)
            if check_timecode == '00:00:10:00':
                remove_keyframe_ok = True
            else:
                remove_keyframe_ok = False

            case.result = remove_keyframe_ok

        # [L188] 3.3 Pip Designer > Set [Motion] > Select Path
        with uuid("39370a35-82b8-44e5-a531-5560b5062ef0") as case:
            # Set opacity = 100
            pip_designer_page.express_mode.drag_object_setting_opacity_slider('100')

            # Switch to motion > Unfold path menu
            pip_designer_page.advanced.switch_to_motion()
            time.sleep(DELAY_TIME)
            pip_designer_page.advanced.unfold_path_menu()

            # Select path template
            pip_designer_page.path.select_template(index=3)

            # You have not saved the changes ... Do you want to save the changes now? Click [No]
            main_page.exist_click(L.title_designer.backdrop.warning.btn_no)

            # Verify Step
            pip_designer_page.set_timecode('00_00_04_00')
            time.sleep(DELAY_TIME)
            check_preview = main_page.snapshot(locator=L.pip_designer.designer_window,
                                               file_name=Auto_Ground_Truth_Folder + 'L188.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L188.png', check_preview, similarity=0.85)

            case.result = compare_result

        # fold path menu
        pip_designer_page.advanced.unfold_path_menu(0)

        # Switch to properties
        pip_designer_page.advanced.switch_to_properties()

        # [L186] 3.3 Pip Designer > Manual adjust on canvas
        with uuid("8a6515af-cdf1-4c1b-ac78-ac44dca720ca") as case:
            # Set rotation to 0
            pip_designer_page.input_rotation_degree_value(0)

            # Resize on Canvas : To larger
            pip_designer_page.resize_on_canvas(drag_x=75, drag_y=60)
            time.sleep(DELAY_TIME * 2)

            # Verify Step: check scale size
            width_text_field = main_page.exist(L.pip_designer.object_setting.scale.width_value)
            logger(width_text_field.AXValue)
            if float(width_text_field.AXValue) > 0.378:
                check_resize = True
            else:
                check_resize = False
            logger(check_resize)

            # Move object to left on Canvas
            pip_designer_page.move_to_left_on_canvas(drag_x=40)

            # Verify Step: check position x value
            current_x_value = pip_designer_page.get_x_position_value()
            logger(current_x_value)
            #if (current_x_value == '0.292') or (current_x_value == '0.285') or (current_x_value == '0.284'):
            if float(current_x_value) > 0.25:
                check_move = True
            else:
                check_move = False

            case.result = check_resize and check_move

        # [L181] 3.3 Pip Designer > Set in [Properties] > Flip
        with uuid("a249d010-4d02-499a-9309-c57675e8b5a9") as case:
            check_horizontal = pip_designer_page.apply_flip_horizontally()
            check_vertical = pip_designer_page.apply_flip_vertically()

            logger(check_horizontal)
            logger(check_vertical)

            pip_designer_page.set_timecode('00_00_02_10')
            time.sleep(DELAY_TIME)
            timeline_preview = main_page.snapshot(locator=L.pip_designer.preview,
                                                  file_name=Auto_Ground_Truth_Folder + 'L181.png')
            check_current_result = main_page.compare(Ground_Truth_Folder + 'L181.png', timeline_preview,
                                                     similarity=0.9)
            logger(check_current_result)
            case.result = check_current_result

        # [L182] 3.3 Pip Designer > Only show the selected track in preview
        with uuid("888b424f-1eab-496e-9288-6fda16cf3b57") as case:
            # Fold Object Settings
            pip_designer_page.express_mode.unfold_properties_object_setting_tab(unfold=0)
            time.sleep(DELAY_TIME)

            # Switch to motion
            pip_designer_page.advanced.switch_to_motion()
            time.sleep(DELAY_TIME)

            # Tick [Only show selected track]
            main_page.click(L.pip_designer.show_the_selected_track)
            time.sleep(DELAY_TIME)

            # Verify Step
            check_checkbox = pip_designer_page.get_selected_track_checkbox_status()
            logger(check_checkbox)

            pip_designer_page.set_timecode('00_00_05_25')
            time.sleep(DELAY_TIME)
            check_preview = main_page.snapshot(locator=L.pip_designer.preview,
                                               file_name=Auto_Ground_Truth_Folder + 'L182.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L182.png', check_preview)

            case.result = compare_result and check_checkbox

        # [L189] 3.3 Pip Designer > Set [Motion Blur]
        with uuid("6ab4ebf9-4369-4944-bc0e-93eded165757") as case:
            # Unfold Motion Blur
            pip_designer_page.advanced.unfold_motion_blur_menu()

            # Set checkbox of Motion Blur
            pip_designer_page.motion_blur.set_checkbox(tick=1)

            # Un-Tick [Only show selected track]
            main_page.click(L.pip_designer.show_the_selected_track)
            time.sleep(DELAY_TIME)

            # Set Blur length = 1.88
            pip_designer_page.motion_blur.length.set_value(1.88)
            # Set Blur density = 28
            pip_designer_page.motion_blur.density.adjust_slider(28)
            time.sleep(DELAY_TIME)

            # Verify Step
            get_length = pip_designer_page.motion_blur.length.get_value()
            logger(get_length)
            if get_length == '1.88':
                check_length = True
            else:
                check_length = False

            get_density = pip_designer_page.motion_blur.density.get_value()
            logger(get_density)
            if get_density == '28':
                check_density = True
            else:
                check_density = False

            # Switch to properties
            pip_designer_page.advanced.switch_to_properties()

            pip_designer_page.set_timecode('00_00_02_10')
            time.sleep(DELAY_TIME)
            check_preview = main_page.snapshot(locator=L.pip_designer.preview,
                                               file_name=Auto_Ground_Truth_Folder + 'L189.png')

            # Compare preview is changed when apply motion blur
            compare_result = main_page.compare(Ground_Truth_Folder + 'L181.png', check_preview, similarity=0.9999)
            logger(compare_result)

            case.result = (not compare_result) and check_length and check_density

        # [L176] 3.3 Pip Designer > Set in [Properties] > Border
        with uuid("fb425a56-1501-4a70-a285-f9398d894f8a") as case:
            # Apply border
            pip_designer_page.apply_border()

            # Check Default size
            current_value = pip_designer_page.express_mode.get_border_size_value()
            if current_value == '3':
                default_size = True
            else:
                default_size = False
            logger(default_size)

            # Set Border size = 7
            pip_designer_page.express_mode.click_border_size_arrow_btn(0,4)

            time.sleep(DELAY_TIME)
            current_value = pip_designer_page.express_mode.get_border_size_value()
            if current_value == '7':
                apply_border_size = True
            else:
                apply_border_size = False
            logger(apply_border_size)

            # Set Blur = 3
            pip_designer_page.express_mode.input_border_blur_value('3')

            time.sleep(DELAY_TIME)
            current_value = pip_designer_page.express_mode.get_border_blur_value()
            if current_value == '3':
                apply_blur = True
            else:
                apply_blur = False
            logger(apply_blur)

            # Set opacity = 96%
            pip_designer_page.express_mode.drag_border_opacity_slider('96')

            time.sleep(DELAY_TIME)
            current_value = pip_designer_page.express_mode.get_border_opacity_value()
            if current_value == '96%':
                apply_opacity = True
            else:
                apply_opacity = False
            logger(apply_opacity)

            # Set color
            pip_designer_page.express_mode.set_border_uniform_color('0F2E12')

            case.result = default_size and apply_border_size and apply_blur and apply_opacity
            # Fold border menu
            pip_designer_page.express_mode.unfold_properties_border_tab(0)

        # [L177] 3.3 Pip Designer > Set in [Properties] > Shadow
        with uuid("bad37a4f-6327-42ed-8214-4e245fdaa0a2") as case:
            # Unfold shadow menu
            pip_designer_page.express_mode.unfold_properties_shadow_tab(1)

            # Enable Shadow
            pip_designer_page.apply_shadow()
            time.sleep(DELAY_TIME)

            # Set distance = 37.1
            pip_designer_page.express_mode.input_shadow_distance_value('37.1')

            # Set color
            pip_designer_page.express_mode.set_shadow_select_color('B7AFE3')

            check_preview = main_page.snapshot(locator=L.pip_designer.preview,
                                               file_name=Auto_Ground_Truth_Folder + 'L177.png')

            # Compare preview is changed when apply Shadow
            compare_result = main_page.compare(Auto_Ground_Truth_Folder + 'L189.png', check_preview, similarity=0.9999)
            logger(compare_result)

            case.result = (not compare_result)

            # Fold shadow menu
            pip_designer_page.express_mode.unfold_properties_shadow_tab(0)

        # [L178] 3.3 Pip Designer > Set in [Properties] > Fade
        with uuid("50370c50-3035-42d5-bab2-34a04165c2e2") as case:
            # Unfold fades menu
            pip_designer_page.express_mode.unfold_properties_fades_tab(type=1, unfold=1)

            # Set timecode (00:00:00:24)
            pip_designer_page.set_timecode('00_00_00_24')
            time.sleep(DELAY_TIME)
            no_fade_in_preview = main_page.snapshot(locator=L.pip_designer.preview)

            # Set timecode (00:00:08:23)
            pip_designer_page.set_timecode('00_00_08_23')
            time.sleep(DELAY_TIME)
            no_fade_out_preview = main_page.snapshot(locator=L.pip_designer.preview)

            # Apply faddes
            pip_designer_page.apply_fades()

            # Apply fade-in and fade-out
            pip_designer_page.apply_enable_fade_in()
            pip_designer_page.apply_enable_fade_out()

            # Set timecode (00:00:00:24)
            pip_designer_page.set_timecode('00_00_00_24')
            time.sleep(DELAY_TIME)
            has_fade_in_preview = main_page.snapshot(locator=L.pip_designer.preview)

            # Set timecode (00:00:08:23)
            pip_designer_page.set_timecode('00_00_08_23')
            time.sleep(DELAY_TIME)
            has_fade_out_preview = main_page.snapshot(locator=L.pip_designer.preview)

            # Compare preview is changed when apply fade in
            compare_fade_in_result = main_page.compare(no_fade_in_preview, has_fade_in_preview, similarity=0.99)
            compare_fade_out_result = main_page.compare(no_fade_out_preview, has_fade_out_preview, similarity=0.99)

            logger(compare_fade_in_result)
            logger(compare_fade_out_result)

            case.result = (not compare_fade_in_result) and (not compare_fade_out_result)

            # Fold fades menu
            pip_designer_page.express_mode.unfold_properties_fades_tab(type=1, unfold=0)

        # [L175] 3.3 Pip Designer > Set in [Properties] > Chroma Key
        with uuid("3b57839e-be4f-45b4-9cf6-e11bf494a44b") as case:
            # Unfold chroma key menu
            # pip_designer_page.express_mode.unfold_properties_chroma_key_tab(unfold=1)

            # Set timecode (00:00:04:00)
            pip_designer_page.set_timecode('00_00_04_00')

            # Apply Chroma key
            pip_designer_page.apply_chromakey()
            time.sleep(DELAY_TIME)

            # Click dropper button
            main_page.click(L.pip_designer.chromakey.btn_dropper)

            # Select one color
            pip_object = main_page.exist(L.pip_designer.preview)
            org_pos = pip_object.AXPosition
            size_w, size_h = pip_object.AXSize

            des_pos = (org_pos[0] + size_w * 0.5, org_pos[1] + size_h * 0.35)
            main_page.mouse.click(*des_pos)

            check_preview = main_page.snapshot(locator=L.pip_designer.preview,
                                               file_name=Auto_Ground_Truth_Folder + 'L175.png')

            # Compare preview after apply chromakey
            compare_result = main_page.compare(Ground_Truth_Folder + 'L175.png', check_preview, similarity=0.8)
            logger(compare_result)

            case.result = compare_result

            time.sleep(DELAY_TIME)
            # Fold fades menu
            pip_designer_page.express_mode.unfold_properties_chroma_key_tab(unfold=0)
            time.sleep(DELAY_TIME*2)

        # [L187] 3.3 Pip Designer > Set Animation
        with uuid("34f35e0f-aff7-46bc-8624-81866440a7f8") as case:
            pip_designer_page.advanced.switch_to_animation()

            pip_designer_page.advanced.unfold_in_animation_menu(1)
            # Apply (Brush Transition 02) animation
            #pip_designer_page.in_animation.select_effect('Glitch')
            pip_designer_page.in_animation.select_template(10)

            # Set timecode (00:00:01:09)
            pip_designer_page.set_timecode('00_00_01_09')
            time.sleep(DELAY_TIME * 3)
            check_preview = main_page.snapshot(locator=L.pip_designer.preview,
                                               file_name=Auto_Ground_Truth_Folder + 'L187.png')

            # Compare preview after apply chromakey
            compare_result = main_page.compare(Ground_Truth_Folder + 'L187.png', check_preview, similarity=0.9)
            logger(compare_result)

            case.result = compare_result

            time.sleep(DELAY_TIME)
            pip_designer_page.advanced.unfold_in_animation_menu(0)

        # [L190] 3.3 Pip Designer > Preview in Designer
        with uuid("55666272-8ab9-4b7f-a6b1-dfbf0c6322ad") as case:
            # Switch
            pip_designer_page.switch_mode('Express')

            main_page.press_space_key()
            time.sleep(DELAY_TIME * 6)
            pip_designer_page.click_preview_operation('Stop')

            # Set timecode (00:00:08:05)
            pip_designer_page.set_timecode('00_00_08_05')
            time.sleep(DELAY_TIME * 3)
            check_preview = main_page.snapshot(locator=L.pip_designer.designer_window,
                                               file_name=Auto_Ground_Truth_Folder + 'L190.png')

            # Compare preview
            compare_result = main_page.compare(Ground_Truth_Folder + 'L190.png', check_preview, similarity=0.9)
            logger(compare_result)

            # Click max button / Leave full mode
            pip_designer_page.click_maximize_btn()

            case.result = compare_result

        # [L191] 3.4 Pip Designer > [Share] template online
        with uuid("fbce1533-d0d5-4ca9-9aed-2f0e4ade18c4") as case:
            # Click [Share] > Upload to "Cyberlink Cloud and DZ"
            # Verify DZ link

            check_upload = pip_designer_page.share_to_cloud(name='dialog09_chroma', tags='123', collection='test', description='Apply chroma key', verify_dz_link=1)
            logger(check_upload)

            # Click [Save as] > Save custom name to close PiP designer
            main_page.click(L.pip_designer.save_as_button)
            time.sleep(DELAY_TIME)
            pip_designer_page.input_template_name_and_click_ok('BFT_Pip_Custom')
            time.sleep(DELAY_TIME)
            pip_designer_page.click_ok()

            # Click download content form CL/DZ
            pip_room_page.click_DownloadContent_from_DZCL()

            # Already enter "Download PiP Objects" > Open My Cyberlink Cloud
            # Select template name "dialog09_chroma"
            check_CL_content = download_from_cl_dz_page.select_template('dialog09_chroma')
            time.sleep(DELAY_TIME)
            download_from_cl_dz_page.tap_delete_button()
            time.sleep(DELAY_TIME*3)

            # Close "Download PiP Objects" window
            # download_from_cl_dz_page.tap_close_button()
            main_page.press_esc_key()
            time.sleep(DELAY_TIME * 5)

            case.result = check_upload and check_CL_content

        # [L192] 3.4 Pip Designer > Save template
        with uuid("4b3b937e-ce77-4946-8c43-cb1eaaf4a264") as case:
            time.sleep(DELAY_TIME * 2)
            # Select custom template: BFT_PiP_Custom
            main_page.select_library_icon_view_media('BFT_Pip_Custom')
            time.sleep(DELAY_TIME * 5)
            # Check preview update
            check_result = main_page.Check_PreviewWindow_is_different(area=L.base.Area.preview.main, sec=3)
            case.result = check_result

        # [L193] 3.4 Pip Designer > Add saved pip template to timeline
        with uuid("b63cc42d-7ae7-49e8-9584-36d0afb9af10") as case:
            # select timeline track 3
            main_page.timeline_select_track(3)

            # Set timecode :
            main_page.set_timeline_timecode('00_00_19_00')
            time.sleep(DELAY_TIME * 2)

            # Drag BFT_Pip_Custom to timeline track 3
            main_page.drag_media_to_timeline_playhead_position('BFT_Pip_Custom', track_no=3)

            # Set timecode :
            main_page.set_timeline_timecode('00_00_02_06')
            time.sleep(DELAY_TIME * 2)

            timeline_preview = main_page.snapshot(locator=main_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'L193.png')
            check_current_dialog09 = main_page.compare(Ground_Truth_Folder + 'L193.png', timeline_preview, similarity=0.9)
            case.result = check_current_dialog09

        # Save project:
        main_page.top_menu_bar_file_save_project_as()
        main_page.handle_save_file_dialog(name='test_case_1_1_5',
                                          folder_path=Test_Material_Folder + 'BFT_21_Stage1/')

    # 17 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open project: test_case_1_1_5
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_5.pds')
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

        # [L195] 3.5 Shape Designer (Shape 10) > Open Shape designer
        with uuid("d31e8163-f315-43f3-bf3b-1ef15d347554") as case:
            # enter PiP room
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 3)

            # Input search Shape 010
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Shape 010')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)
            main_page.select_library_icon_view_media('Shape 010')
            main_page.double_click()

            check_title = shape_designer_page.get_title()
            if check_title == 'Shape 010':
                case.result = True
            else:
                case.result = False

        # [L196] 3.5 Shape Designer (Shape 10) > Input text
        with uuid("649e782e-02f5-4d11-98f8-43c305c69daa") as case:
            shape_designer_page.click_center_on_Canvas()
            shape_designer_page.edit_title_on_Canvas('Happy Hour')
            time.sleep(DELAY_TIME)

            time.sleep(DELAY_TIME * 3)
            check_preview = main_page.snapshot(locator=L.shape_designer.canvas_object_shape,
                                               file_name=Auto_Ground_Truth_Folder + 'L196.png')

            # Compare preview after select Shape 10 & input text : Happy Hour
            compare_result = main_page.compare(Ground_Truth_Folder + 'L196.png', check_preview)
            logger(compare_result)
            case.result = compare_result
            shape_designer_page.unselect_title_on_Canvas()
            check_preview_25 = main_page.snapshot(locator=L.shape_designer.canvas_split_view)

        # [L198] 3.5 Shape Designer (Shape 10) > Properties tab > Shape Type (Linear shape)
        with uuid("281801de-64bc-4c6c-8c47-ab1dd7f8e0fa") as case:
            # Unfold Shape Type
            shape_designer_page.properties.unfold_shape_type(set_unfold=1)

            # Drag scroll bar of (shape type) to 0
            shape_designer_page.properties.shape_type.drag_scroll_bar('0')

            # Apply shape 8
            shape_designer_page.properties.shape_type.apply_type(8)
            time.sleep(DELAY_TIME)

            # Verify Step
            check_preview_08 = main_page.snapshot(locator=L.shape_designer.canvas_split_view)
            compare_result_w_08 = main_page.compare(check_preview_25, check_preview_08)
            logger(compare_result_w_08)

            # Apply shape 4
            shape_designer_page.properties.shape_type.apply_type(4)
            time.sleep(DELAY_TIME)

            # Verify Step
            # If preview (Linear 08 -> Linear 04) is not changed, it's known bug (VDE224706-0064)
            check_preview_04 = main_page.snapshot(locator=L.shape_designer.canvas_split_view)
            compare_result_w_04 = main_page.compare(check_preview_08, check_preview_04, similarity=0.9999)
            logger(compare_result_w_04)

            case.result = (not compare_result_w_08) and (not compare_result_w_04)
            case.fail_log = 'VDE224706-0064'

        # [L197] 3.5 Shape Designer (Shape 10) > Properties tab > Shape Type (General shape)
        with uuid("1c24089b-4989-459e-b2aa-105da9c3cf1e") as case:
            shape_designer_page.click_cancel(option=1)
            time.sleep(DELAY_TIME)

            main_page.select_library_icon_view_media('Shape 010')
            main_page.double_click()

            shape_designer_page.click_center_on_Canvas()
            shape_designer_page.edit_title_on_Canvas('Happy Hour')
            time.sleep(DELAY_TIME)

            # Drag scroll bar of (shape type) to 0.314
            shape_designer_page.properties.shape_type.drag_scroll_bar('0')
            time.sleep(DELAY_TIME)
            shape_designer_page.properties.shape_type.apply_type(10)
            shape_designer_page.properties.shape_type.drag_scroll_bar('0.14')
            time.sleep(DELAY_TIME * 2)
            shape_designer_page.properties.shape_type.apply_type(10)

            # Apply shape 14
            shape_designer_page.properties.shape_type.apply_type(14)
            shape_designer_page.properties.shape_type.drag_scroll_bar('0.34')
            time.sleep(DELAY_TIME * 2)
            # Apply shape 14
            shape_designer_page.properties.shape_type.apply_type(14)
            time.sleep(DELAY_TIME)

            check_preview_14 = main_page.snapshot(locator=L.shape_designer.canvas_object_shape)

            # Compare preview after select Shape 14 vs Shape 25
            compare_result_14 = main_page.compare(Ground_Truth_Folder + 'L196.png', check_preview_14)
            logger(compare_result_14)

            # Apply shape 19
            shape_designer_page.properties.shape_type.apply_type(19)
            time.sleep(DELAY_TIME)

            check_preview_19 = main_page.snapshot(locator=L.shape_designer.canvas_object_shape)

            # Compare preview after select Shape 19 vs Shape 14
            compare_result_19 = main_page.compare(check_preview_19, check_preview_14)
            logger(compare_result_19)

            case.result = (not compare_result_14) and (not compare_result_19)
            # Fold Shape Type
            shape_designer_page.properties.unfold_shape_type(set_unfold=0)

        # [L199] 3.5 Shape Designer (Shape 10) > Properties tab > Preset
        with uuid("53bde9e0-8ccd-4155-995c-50815b552ddd") as case:
            # Unfold Preset Type
            shape_designer_page.properties.unfold_shape_preset(set_unfold=1)

            check_preset_2 = main_page.snapshot(locator=L.shape_designer.canvas_object_shape)

            # Apply preset 4
            shape_designer_page.properties.shape_preset.apply_preset(4)

            check_preset_4 = main_page.snapshot(locator=L.shape_designer.canvas_object_shape,
                                                file_name=Auto_Ground_Truth_Folder + 'L199.png')

            # Compare preview after apply preset 4
            should_different = main_page.compare(check_preset_2, check_preset_4)
            logger(should_different)

            compare_result = main_page.compare(Ground_Truth_Folder + 'L199.png', check_preset_4)
            logger(compare_result)
            case.result = (not should_different) and compare_result

            # Fold Preset Type
            shape_designer_page.properties.unfold_shape_preset(set_unfold=0)

        # [L200] 3.5 Shape Designer (Shape 10) > Properties tab > Fill
        with uuid("0925be85-d8bc-4a20-bd47-80b7c2f3ba35") as case:
            # Unfold Fill Type
            shape_designer_page.properties.unfold_shape_fill(set_unfold=1)

            # Set Gradient begin : 362A45
            shape_designer_page.properties.shape_fill.set_gradient_begin('E31E35')

            # Set Gradient end : 91F3C1
            shape_designer_page.properties.shape_fill.set_gradient_end('91F3C1')

            # Set blur : 5
            shape_designer_page.properties.shape_fill.blur.set_value(5)
            # Set opacity : 94%
            shape_designer_page.properties.shape_fill.opacity.click_arrow(1, 6)

            # Verify Step:
            # Get blur value
            check_blur = shape_designer_page.properties.shape_fill.blur.get_value()
            if check_blur == '5':
                apply_blur = True
            else:
                apply_blur = False
            logger(apply_blur)

            # Get opacity value
            check_blur = shape_designer_page.properties.shape_fill.opacity.get_value()
            if check_blur == '94%':
                apply_opacity = True
            else:
                apply_opacity = False
            logger(apply_opacity)

            # Check shape preview
            check_fill = main_page.snapshot(locator=L.shape_designer.canvas_object_shape)

            compare_different = main_page.compare(Auto_Ground_Truth_Folder + 'L199.png', check_fill, similarity=0.98)
            logger(compare_different)
            case.result = apply_blur and apply_opacity and (not compare_different)

            # Fold Fill Type
            shape_designer_page.properties.unfold_shape_fill(set_unfold=0)

        # [L201] 3.5 Shape Designer (Shape 10) > Properties tab > Outline
        with uuid("81e6ab89-f81c-4ec3-926f-6611abe5cef2") as case:
            # Unfold Outline
            shape_designer_page.properties.unfold_shape_outline(set_unfold=1)

            # maximize
            shape_designer_page.click_restore_btn()
            time.sleep(DELAY_TIME*1.5)

            # Set checkbox
            shape_designer_page.properties.shape_outline.apply_checkbox()

            # Set size
            shape_designer_page.properties.shape_outline.size.set_value(2)

            # Set 3rd type
            shape_designer_page.properties.shape_outline.set_line_type(3)

            # Set blur
            shape_designer_page.properties.shape_outline.blur.set_slider(1)

            # Set color
            shape_designer_page.properties.shape_outline.set_uniform_color('F3C4DE')

            # Click center
            shape_designer_page.click_center_on_Canvas()
            time.sleep(DELAY_TIME)

            check_preview = main_page.snapshot(locator=L.shape_designer.canvas_object_shape,
                                               file_name=Auto_Ground_Truth_Folder + 'L201.png')

            # Compare preview
            compare_result = main_page.compare(Ground_Truth_Folder + 'L201.png', check_preview, similarity=0.9)
            case.result = compare_result

            # Fold Outline
            shape_designer_page.properties.unfold_shape_outline(set_unfold=0)

        # [L202] 3.5 Shape Designer (Shape 10) > Properties tab > Shadow
        with uuid("f9c22e54-7e9d-4341-ac36-496bf86861d1") as case:
            # Unfold Shadow
            shape_designer_page.properties.unfold_shadow(set_unfold=1)

            # Set checkbox
            shape_designer_page.properties.shadow.apply_checkbox(1)
            checkbox_value = shape_designer_page.properties.shadow.get_checkbox_status()
            logger(checkbox_value)

            # Set apply shadow to (Outline Only)
            shape_designer_page.properties.shadow.set_apply_shadow_to(2)
            check_shadow_to_result = shape_designer_page.properties.shadow.get_apply_shadow_to()
            if check_shadow_to_result == 'Outline Only':
                shadow_to_result = True
            else:
                shadow_to_result = False
            logger(shadow_to_result)

            # Set distance
            shape_designer_page.properties.shadow.distance.set_value(35.6)

            # Set opacity
            shape_designer_page.properties.shadow.opacity.set_slider(88)

            # Set Blur
            shape_designer_page.properties.shadow.blur.set_value(1)

            # Set Fill shadow
            shape_designer_page.properties.shadow.fill_shadow.apply_checkbox(1)

            # Set direction
            shape_designer_page.properties.shadow.direction.set_value(17)

            check_preview = main_page.snapshot(locator=L.shape_designer.canvas_object_shape)

            # Compare preview
            compare_result = main_page.compare(Ground_Truth_Folder + 'L201.png', check_preview, similarity=0.99)
            logger(compare_result)
            case.result = (not compare_result) and checkbox_value and shadow_to_result

            # Fold Shadow
            shape_designer_page.properties.unfold_shadow(set_unfold=0)

        # [L203] 3.5 Shape Designer (Shape 10) > Properties tab > Title
        with uuid("a148b797-eb2a-4bc8-89e3-ff4f648c6b05") as case:
            # Unfold Title
            shape_designer_page.properties.unfold_title(set_unfold=1)

            # Set font type: pigmo
            shape_designer_page.properties.title.set_font_type('pigmo')

            # Set size = 21
            shape_designer_page.properties.title.set_font_size(21)

            # Set font color
            shape_designer_page.properties.title.set_font_color('B5FFFF')

            # Compare preview
            check_preview = main_page.snapshot(locator=L.shape_designer.canvas_object_shape,
                                               file_name=Auto_Ground_Truth_Folder + 'L203.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L203.png', check_preview, similarity=0.9)
            logger(compare_result)
            case.result = compare_result

            # Fold Title
            shape_designer_page.properties.unfold_title(set_unfold=0)

        # [L208] 3.5 Shape Designer (Shape 10) > Manual adjust on canvas
        with uuid("47acdd2c-75cb-48c9-bce2-64a188a62cb4") as case:
            shape_designer_page.adjust_object_on_Canvas_resize_to_large()
            time.sleep(DELAY_TIME)

            # Verify : Preview is changed
            check_resize = main_page.snapshot(locator=L.shape_designer.canvas_object_shape)
            compare_resize_result = main_page.compare(Ground_Truth_Folder + 'L203.png', check_resize)
            logger(compare_resize_result)

            shape_designer_page.click_undo()
            time.sleep(DELAY_TIME)

            shape_designer_page.adjust_object_on_Canvas_move_to_left()

            # Switch Keyframe menu
            shape_designer_page.click_keyframe_tab()
            time.sleep(DELAY_TIME)

            # Verify position x value
            current_x = shape_designer_page.keyframe.object_settings.position.x.get_value()
            logger(current_x)
            if current_x == '0.359':
                move_left = True
            else:
                move_left = False
            logger(move_left)

            case.result = (not compare_resize_result) and move_left

        # [L205] 3.5 Shape Designer (Shape 10) > Keyframe tab > Adjust keyframe
        with uuid("c70a3ee9-2263-4772-a7d7-d4f859315ec0") as case:
            # Set position = (0.199, 0.297)
            shape_designer_page.keyframe.object_settings.position.x.set_value(0.199)
            shape_designer_page.keyframe.object_settings.position.y.set_value(0.297)

            # Set position 1st keyframe on 0s
            shape_designer_page.keyframe.object_settings.position.keyframe.click_add_remove()

            # Set timecode
            shape_designer_page.set_timecode('00_00_03_10')

            # Set position = (0.783, 0.440) w/ 2nd keyframe
            shape_designer_page.keyframe.object_settings.position.x.set_value(0.783)
            shape_designer_page.keyframe.object_settings.position.y.set_value(0.440)

            # Set timecode
            shape_designer_page.set_timecode('00_00_05_25')

            # Set position = (0.276, 0.621) w/ 3rd keyframe
            shape_designer_page.keyframe.object_settings.position.x.set_value(0.276)
            shape_designer_page.keyframe.object_settings.position.y.set_value(0.621)

            # Set scale 1st keyframe
            shape_designer_page.keyframe.object_settings.scale.keyframe.click_add_remove()

            # Set timecode
            shape_designer_page.set_timecode('00_00_08_10')

            # Set position = (0.676, 0.304) w/ 4th keyframe
            shape_designer_page.keyframe.object_settings.position.x.set_value(0.676)
            shape_designer_page.keyframe.object_settings.position.y.set_value(0.304)

            # Set scale W = 0.672, H = 0.748 w/ 2nd keyframe
            shape_designer_page.keyframe.object_settings.scale.w.set_value(0.672)
            shape_designer_page.keyframe.object_settings.scale.h.set_value(0.748)

            # Set Rotation 1st keyframe on 8s 10 frame
            shape_designer_page.keyframe.object_settings.rotation.keyframe.click_add_remove()

            # Drag simple timeline scroll bar to 1
            #shape_designer_page.simple_timeline.drag_scroll_bar(1)

            # Click previous keyframe
            shape_designer_page.keyframe.object_settings.position.keyframe.click_previous()

            # Set Rotation 2nd keyframe on (05:25)
            shape_designer_page.keyframe.object_settings.rotation.keyframe.click_add_remove()

            # Set Rotation degree = 250
            shape_designer_page.keyframe.object_settings.rotation.value.set_value(250)

            # Set timecode
            shape_designer_page.set_timecode('00_00_06_29')
            time.sleep(DELAY_TIME*1.5)

            # Compare preview
            check_preview = main_page.snapshot(locator=L.shape_designer.designer_window,
                                               file_name=Auto_Ground_Truth_Folder + 'L205.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L205.png', check_preview, similarity=0.88)
            case.result = compare_result

        # [L206] 3.5 Shape Designer (Shape 10) > Keyframe tab > Adjust ease in / out
        with uuid("4eda0d6a-b0ea-4100-a22a-317fffdfb976") as case:
            # Click next keyframe
            shape_designer_page.keyframe.object_settings.position.keyframe.click_next()

            # Position > Set Ease in
            shape_designer_page.keyframe.object_settings.position.ease_in.set_checkbox()
            # Set Ease in value = 0.61
            shape_designer_page.keyframe.object_settings.position.ease_in.set_value('0.61')

            # Click previous keyframe
            shape_designer_page.keyframe.object_settings.position.keyframe.click_previous()

            # Position > Set Ease out
            shape_designer_page.keyframe.object_settings.position.ease_out.set_checkbox()
            # Set Ease out value = 0.61
            shape_designer_page.keyframe.object_settings.position.ease_out.set_value('0.77')

            # Set timecode
            shape_designer_page.set_timecode('00_00_06_29')
            time.sleep(DELAY_TIME*1.5)

            # Compare preview
            check_preview = main_page.snapshot(locator=L.shape_designer.designer_window,
                                               file_name=Auto_Ground_Truth_Folder + 'L206_ease_in_out.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L205.png', check_preview, similarity=0.98)
            case.result = not compare_result

        # [L207] 3.5 Shape Designer (Shape 10) > Add keyframe in simple timeline
        with uuid("1df5b03f-b8c4-4da6-87be-582d3c308826") as case:
            # Click next keyframe
            shape_designer_page.simple_timeline.position.click_next_keyframe()

            # Remove 4th position keyframe
            shape_designer_page.simple_timeline.position.add_keyframe()

            # Click previous keyframe
            shape_designer_page.simple_timeline.scale.click_previous_keyframe()

            # Set timecode
            shape_designer_page.set_timecode('00_00_05_13')
            # Add scale keyframe
            shape_designer_page.simple_timeline.scale.add_keyframe()
            # Set scale W = 0.982
            shape_designer_page.keyframe.object_settings.scale.w.set_value(0.982)

            # Set timecode
            shape_designer_page.set_timecode('00_00_06_29')
            time.sleep(DELAY_TIME * 1.5)

            # Compare preview
            check_preview = main_page.snapshot(locator=L.shape_designer.designer_window,
                                               file_name=Auto_Ground_Truth_Folder + 'L207.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L207.png', check_preview, similarity=0.88)
            case.result = compare_result

        # [L209] 3.5 Shape Designer (Shape 10) > Preview in designer
        with uuid("57fc39a2-bd36-432d-a9f1-e9e148f9816d") as case:
            # Restore window
            shape_designer_page.click_restore_btn()
            time.sleep(DELAY_TIME)

            # Switch to properties
            shape_designer_page.click_properties_tab()
            time.sleep(DELAY_TIME)

            # Click Stop
            shape_designer_page.click_preview_operation('Stop')
            time.sleep(DELAY_TIME * 0.5)

            # Click Play
            shape_designer_page.click_preview_operation('Play')
            time.sleep(DELAY_TIME * 4)

            # Click Pause
            shape_designer_page.click_preview_operation('Pause')

            # Set timecode
            shape_designer_page.set_timecode('00_00_04_29')
            time.sleep(DELAY_TIME * 1.5)

            # Compare preview
            check_preview = main_page.snapshot(locator=L.shape_designer.designer_window,
                                               file_name=Auto_Ground_Truth_Folder + 'L209.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L209.png', check_preview)
            case.result = compare_result

        # [L210] 3.5 Shape Designer (Shape 10) > Save as template
        with uuid("7a48ed0f-e18b-40e0-8749-82321bac9821") as case:
            shape_designer_page.click_save_as()
            time.sleep(DELAY_TIME * 0.5)
            shape_designer_page.save_as.set_name('Custom_shape_10')
            time.sleep(DELAY_TIME*0.5)
            shape_designer_page.save_as.click_ok()
            time.sleep(DELAY_TIME * 1.5)

            # Verify Step 1: check caption bar
            current_title = shape_designer_page.get_title()
            logger(current_title)
            if current_title == 'Custom_shape_10':
                save_result = True
            else:
                save_result = False
            logger(save_result)

            # Click [OK]
            shape_designer_page.click_ok()

            # select timeline track 1
            main_page.timeline_select_track(1)

            # Set CTI timeline to (00:00:19:00)
            main_page.set_timeline_timecode('00_00_19_00')

            # Verify Step2:
            custom_select_result = main_page.select_library_icon_view_media('Custom_shape_10')
            logger(custom_select_result)
            case.result = save_result and custom_select_result

        # [L211] 3.5 Shape Designer (Shape 10) > Add saved template to timeline
        with uuid("ae82fd12-b91f-40e1-ade5-5cca22803e7e") as case:
            main_page.select_library_icon_view_media('Custom_shape_10')
            main_page.right_click()
            time.sleep(DELAY_TIME)
            main_page.select_right_click_menu('Add to Timeline')

            # Verify Step1 : Check (Custom_shape_10) is in Video track 1
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=2)
            main_page.double_click()
            time.sleep(DELAY_TIME*1.5)

            current_title = shape_designer_page.get_title()
            logger(current_title)
            if current_title == 'Custom_shape_10':
                check_caption_title = True
            else:
                check_caption_title = False

            # Verify Step2: Play then Pause
            # Click Play
            shape_designer_page.click_preview_operation('Play')
            time.sleep(DELAY_TIME * 2)

            # Click Pause
            shape_designer_page.click_preview_operation('Pause')

            # Set timecode
            shape_designer_page.set_timecode('00_00_02_01')
            time.sleep(DELAY_TIME * 1.5)

            # Compare preview
            check_preview = main_page.snapshot(locator=L.shape_designer.designer_window,
                                               file_name=Auto_Ground_Truth_Folder + 'L211.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L211.png', check_preview, similarity=0.9)
            case.result = compare_result and check_caption_title

        # [L204] 3.5 Shape Designer (Shape 10) > Only show the selected track
        with uuid("12c35c84-9c7b-4ba1-bcdb-7510d1dc1555") as case:
            # Click Stop
            shape_designer_page.click_preview_operation('Stop')
            time.sleep(DELAY_TIME)

            # Check checkbox default status
            elem_checkbox = main_page.exist(L.shape_designer.show_the_selected_track)
            default_value = elem_checkbox.AXValue
            if default_value == 0:
                default_status = True
            else:
                default_status = False
            logger(default_status)

            # Set only show the selected track
            main_page.click(L.shape_designer.show_the_selected_track)

            # Set timecode
            shape_designer_page.set_timecode('00_00_02_01')
            time.sleep(DELAY_TIME * 1.5)

            # Compare preview
            check_preview_204 = main_page.snapshot(locator=L.shape_designer.designer_window)
            compare_result = main_page.compare(Ground_Truth_Folder + 'L211.png', check_preview_204)
            logger(compare_result)
            case.result = (not compare_result) and default_status
        shape_designer_page.click_cancel()

        # Save project:
        main_page.top_menu_bar_file_save_project_as()
        main_page.handle_save_file_dialog(name='test_case_1_1_6',
                                          folder_path=Test_Material_Folder + 'BFT_21_Stage1/')

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open project: test_case_1_1_6
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_6.pds')
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

        # [L213] 3.6 Particle Designer (Should support opacity) > Open Particle designer
        with uuid("51d8dc04-c9dc-4f8e-b7e2-bfb9e802e19b") as case:
            # enter Particle room
            main_page.enter_room(5)
            time.sleep(DELAY_TIME * 3)
            particle_room_page.search_Particle_room_library('Snowflakes')

            main_page.select_library_icon_view_media('Snowflakes')
            time.sleep(DELAY_TIME*7)

            # Drag BFT_title_Save to timeline track 2
            main_page.drag_media_to_timeline_playhead_position('Snowflakes', track_no=2)

            # Click tips area [Designer] button
            main_page.tips_area_click_designer(2)
            time.sleep(DELAY_TIME * 1.5)

            check_title = particle_designer_page.get_particle_designer_title()
            logger(check_title)

            if check_title == 'Snowflakes':
                case.result = True
            else:
                case.result = False

        # [L214] 3.6 Particle Designer (Should support opacity) > modify parameter
        with uuid("56edc685-fdb3-4aa5-9fbb-36060e6a5223") as case:
            # Get default Emit / Max / Life / Size / Speed / Opacity  value
            default_emit_value = particle_designer_page.express_mode.get_Emit_value()
            default_max_value = particle_designer_page.express_mode.get_Max_value()
            default_life_value = particle_designer_page.express_mode.get_Life_value()
            default_size_value = particle_designer_page.express_mode.get_Size_value()
            default_speed_value = particle_designer_page.express_mode.get_Speed_value()
            default_opacity_value = particle_designer_page.express_mode.get_Opacity_value()

            logger(default_emit_value)
            logger(default_max_value)
            logger(default_life_value)
            logger(default_size_value)
            logger(default_speed_value)
            logger(default_opacity_value)

            # Verify step: check all parameters "default" value
            # If average value = 100000, then True
            avg_default = (default_emit_value + default_max_value + default_life_value + default_size_value + default_speed_value + default_opacity_value) / 6
            logger(avg_default)

            if int(avg_default) == 100000:
                check_default = True
            else:
                check_default = False
            logger(check_default)

            # Set paramter
            # Emit = 10407, Max = 170621, Life = 200000, Size = 178940, Speed = 121610, Opacity = 194574
            particle_designer_page.express_mode.drag_Emit_slider(10407)
            time.sleep(DELAY_TIME)
            particle_designer_page.express_mode.drag_Max_slider(170621)
            time.sleep(DELAY_TIME)
            particle_designer_page.express_mode.drag_Life_slider(200000)
            time.sleep(DELAY_TIME)
            particle_designer_page.express_mode.drag_Size_slider(171940)
            time.sleep(DELAY_TIME)
            particle_designer_page.express_mode.click_Size_plus_btn(7)
            time.sleep(DELAY_TIME)
            particle_designer_page.express_mode.drag_Speed_slider(126610)
            time.sleep(DELAY_TIME)
            particle_designer_page.express_mode.click_Speed_minus_btn(5)
            time.sleep(DELAY_TIME)
            particle_designer_page.express_mode.drag_Opacity_slider(194574)

            # drag scroll bar to 1
            #particle_designer_page.drag_properties_scroll_bar(1)

            # Set timecode = 00:00:04:09
            particle_designer_page.set_timecode('00_00_04_09')
            time.sleep(DELAY_TIME*1.5)

            # Verify Step;
            check_preview = main_page.snapshot(locator=L.particle_designer.designer_window,
                                               file_name=Auto_Ground_Truth_Folder + 'L214.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L214.png', check_preview)

            case.result = check_default and compare_result

        # [L215] 3.6 Particle Designer (Should support opacity) > preview in designer
        with uuid("3bc57b03-6b38-45a7-b7d4-83db0bb56922") as case:
            # Seek next frame to 00:00:04:18
            for x in range(9):
                particle_designer_page.click_preview_operation('Next_Frame')
                time.sleep(DELAY_TIME*0.5)

            # Verify Step;
            check_preview = main_page.snapshot(locator=L.particle_designer.designer_window)
            compare_result = main_page.compare(Ground_Truth_Folder + 'L214.png', check_preview)
            logger(compare_result)
            case.result = not compare_result

        # [L216] 3.6 Particle Designer (Should support opacity) > [Share] template online
        with uuid("6030bf73-af59-4bef-ba28-051b275491ec") as case:
            check_upload = particle_designer_page.share_to_cloud(name='snowflakes_design', tags='123', collection='test', description='white color', verify_dz_link=1)
            logger(check_upload)

            time.sleep(DELAY_TIME*3)

            # Verify step: check title
            check_title = particle_designer_page.get_particle_designer_title()
            logger(check_title)

            if check_title == 'snowflakes_design':
                upload_save_back = True
            else:
                upload_save_back = False
            logger(upload_save_back)

            # ---------------------------------
            # Click [Save as] > Save custom name then close Particle designer
            particle_designer_page.save_as_name('BFT_snowflakes_custom')
            time.sleep(DELAY_TIME)
            particle_designer_page.save_as_ok()
            particle_designer_page.click_OK()


            # Click download content form CL/DZ
            particle_room_page.click_DownloadContent_from_DZCloud()
            time.sleep(DELAY_TIME*6)

            # Already enter "Download Particle Objects" > Open My Cyberlink Cloud
            # Select template name "dialog09_chroma"
            check_CL_content = download_from_cl_dz_page.select_template('snowflakes_design')
            time.sleep(DELAY_TIME)
            download_from_cl_dz_page.tap_delete_button()
            time.sleep(DELAY_TIME*3)

            # Close "Download Particle Objects" window
            # download_from_cl_dz_page.tap_close_button()
            main_page.press_esc_key()

            case.result = check_upload and upload_save_back and check_CL_content

        # [L217] 3.6 Particle Designer (Should support opacity) > Save / Save as template
        with uuid("23140e39-6b80-4d37-b572-266f1481fca1") as case:
            main_page.select_library_icon_view_media('BFT_snowflakes_custom')
            check_different = main_page.Check_PreviewWindow_is_different(sec=4)
            logger(check_different)
            case.result = check_different

        # [L218] 3.6 Particle Designer (Should support opacity) > Add saved title template to timeline
        with uuid("5945daf9-f385-471b-aa11-4b9445c4736f") as case:
            # select timeline track 1
            main_page.timeline_select_track(1)

            # Set CTI timeline to (00:00:29:00)
            main_page.set_timeline_timecode('00_00_29_00')
            time.sleep(DELAY_TIME*1.5)

            # Add to timeline
            main_page.select_library_icon_view_media('BFT_snowflakes_custom')
            time.sleep(DELAY_TIME*2)
            main_page.tips_area_insert_media_to_selected_track()

            time.sleep(DELAY_TIME * 2)
            main_page.set_timeline_timecode('00_00_03_02')
            time.sleep(DELAY_TIME*1.5)

            timeline_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view, file_name=Auto_Ground_Truth_Folder + 'L217.png')
            check_timeline_particle = main_page.compare(Ground_Truth_Folder + 'L217.png', timeline_preview, similarity=0.8)
            case.result = check_timeline_particle

        # Save project:
        main_page.top_menu_bar_file_save_project_as()
        main_page.handle_save_file_dialog(name='test_case_1_1_7',
                                          folder_path=Test_Material_Folder + 'BFT_21_Stage1/')

    # 19 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open project: test_case_1_1_7
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_7.pds')
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

        # select timeline track 3
        main_page.timeline_select_track(3)

        # Set timecode :
        main_page.set_timeline_timecode('00_00_24_00')
        time.sleep(DELAY_TIME * 2)

        # Drag Spor t02.jpg to timeline track3
        main_page.drag_media_to_timeline_playhead_position('Sport 02.jpg', track_no=3)
        time.sleep(DELAY_TIME * 2)

        # [L220] 3.7 Mask Designer (Sport 02.jpg) > Open Mask Designer
        with uuid("152b2168-2061-4e23-bdf0-1301392bcdee") as case:
            # Click Tools > select (Mask designer)
            main_page.click(L.main.tips_area.btn_tools)
            time.sleep(DELAY_TIME * 2)
            main_page.select_right_click_menu('Mask Designer')
            time.sleep(DELAY_TIME * 2)

            # Verify Step:
            check_mask_window = main_page.exist(L.mask_designer.mask_designer_window)
            if not check_mask_window:
                logger('Cannot enter mask designer window')
                case.result = False
            elif check_mask_window.AXTitle == 'Mask Designer  |  Sport 02':
                case.result = True
            else:
                case.result = False

        # [L221] 3.7 Mask Designer (Sport 02.jpg) > Apply default mask
        with uuid("e4a71739-d5e3-4598-8f18-af2a81a6e91c") as case:
            mask_default_preview = main_page.snapshot(locator=L.mask_designer.preview_window)
            #check_timeline_particle = main_page.compare(Ground_Truth_Folder + 'L217.png', timeline_preview, similarity=0.93)
            time.sleep(DELAY_TIME * 2)

            # random
            # Apply mask random (2 ~ 8)
            x = random.randrange(1,7)
            logger(f'select preset {x}+1 - random select')
            mask_designer_page.MaskDesigner_Apply_template(x)
            time.sleep(DELAY_TIME * 2)
            mask_x_preview = main_page.snapshot(locator=L.mask_designer.preview_window)

            mask_designer_page.MaskDesigner_Apply_template(index=8)
            time.sleep(DELAY_TIME * 2)
            mask_star_preview = main_page.snapshot(locator=L.mask_designer.preview_window)

            check_first_mask = main_page.compare(mask_default_preview, mask_x_preview, similarity=0.98)
            logger(check_first_mask)
            check_second_mask = main_page.compare(mask_x_preview, mask_star_preview, similarity=0.98)
            logger(check_second_mask)

            case.result = (not check_first_mask) and (not check_second_mask)

        # [L233] 3.7 Mask Designer (Sport 02.jpg) > Manual adjust on canvas > Move > Operation works fine.
        with uuid("1f9a1e2a-df56-4083-bb11-bfe9de94793d") as case:
            # Move mask object to lower right
            mask_designer_page.move_object_on_canvas(offset_x=30, offset_y=40)

            # Verify Step:
            lower_right_preview = main_page.snapshot(locator=L.mask_designer.preview_window)
            check_no_updated = main_page.compare(mask_star_preview, lower_right_preview)
            case.result = (not check_no_updated)

            # click undo
            mask_designer_page.tap_MaskDesigner_Undo_btn()
            time.sleep(DELAY_TIME)

        # [L222] 3.7 Mask Designer (Sport 02.jpg) > custom mask from image
        with uuid("f244a59e-d7c8-4da3-b94e-65caa7672ca3") as case:
            mask_designer_page.Edit_MaskDesigner_CreateImageMask(Test_Material_Folder + 'BFT_21_Stage1/beauty.jpg')
            time.sleep(DELAY_TIME * 4)

            # Verify Step1:
            # Play preview then check (preview is changed)
            mask_designer_page.Edit_MaskDesigner_PreviewOperation('play')
            preview_is_updated = main_page.Check_PreviewWindow_is_different(area=L.mask_designer.preview_window, sec=2)
            logger(preview_is_updated)
            mask_designer_page.Edit_MaskDesigner_PreviewOperation('stop')
            time.sleep(DELAY_TIME*2)

            # Verify Step2:
            zero_sec_preview = main_page.snapshot(locator=L.mask_designer.mask_designer_window, file_name=Auto_Ground_Truth_Folder + 'L222.png')
            check_star_mask = main_page.compare(Ground_Truth_Folder + 'L222.png', zero_sec_preview, similarity=0.93)

            # Verify Step3:
            # Remove custom mask
            check_remove_custom = mask_designer_page.Edit_MaskDesigner_RemoveCustomMask(index=1)

            case.result = check_star_mask and preview_is_updated and check_remove_custom

        # [L226] 3.7 Mask Designer (Sport 02.jpg) > Invert mask
        with uuid("2010b0ee-ff55-4ac8-9556-d618b6cb89d0") as case:
            # Set (Only show the selected track)
            mask_designer_page.Edit_MaskDesigner_Only_Show_Selected_track_SetCheck()

            # Tick invert mask
            mask_designer_page.Edit_MaskDesigner_Invert_mask_SetCheck()
            time.sleep(DELAY_TIME)

            # Verify Step:
            current_preview = main_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'L226.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L226.png', current_preview)
            case.result = check_preview

        # [L223] 3.7 Mask Designer (Sport 02.jpg) > Create title mask
        with uuid("efbff806-82b5-4247-a182-3edc78866548") as case:
            # Un-tick invert mask
            mask_designer_page.Edit_MaskDesigner_Invert_mask_SetCheck(check=False)
            time.sleep(DELAY_TIME)

            # Title mask
            mask_designer_page.click_create_text_mask_btn()
            time.sleep(DELAY_TIME * 1.5)

            # Check is in (Mask composer)
            current_status = mask_designer_page.is_enter_mask_composer()
            if not current_status:
                logger('Cannot enter Mask composer after call click_create_text_mask_btn()')
                raise Exception
            else:
                main_page.click(L.title_designer.area.edittext_text_content)
                main_page.mouse.click(times=3)
                main_page.keyboard.send('Etxkhq')
                main_page.press_enter_key()
                main_page.keyboard.send('WTrdi')
                time.sleep(DELAY_TIME)
                main_page.click(L.title_designer.btn_ok)

            time.sleep(DELAY_TIME*1.5)

            # Hide simple timeline
            main_page.click(L.mask_designer.btn_hide_timeline_mode)
            time.sleep(DELAY_TIME)

            # Verify Step:
            current_preview = main_page.snapshot(locator=L.mask_designer.mask_designer_window, file_name=Auto_Ground_Truth_Folder + 'L223.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L223.png', current_preview)
            case.result = check_preview

        # [L232] 3.7 Mask Designer (Sport 02.jpg) > Rotate
        with uuid("5a933fab-12ff-464c-8551-b16ef67de363") as case:
            # Rotate object degree = 35
            mask_designer_page.rotate_object_on_canvas()

            # [L230] 3.7 Mask Designer (Sport 02.jpg) > Set [Motion]
            with uuid("b36192a8-c280-447a-89a5-f0dad4142943") as case:
                # Un-tick (Only show the selected track)
                mask_designer_page.Edit_MaskDesigner_Only_Show_Selected_track_SetCheck(check_it=False)

                # Switch to Motion tab
                mask_designer_page.switch_to_motion()
                time.sleep(DELAY_TIME * 0.5)

                # Open path tab
                mask_designer_page.motion.open_path_tag()

                # random
                # Apply mask random (5 ~ 20)
                x = random.randrange(5, 20)
                logger(f'select preset {x} - random select')
                mask_designer_page.motion.select_path_template(x)
                time.sleep(DELAY_TIME * 2)
                motion_x_preview = main_page.snapshot(locator=L.mask_designer.preview_window)

                mask_designer_page.motion.select_path_template(4)
                time.sleep(DELAY_TIME * 2)
                motion_fourth_preview = main_page.snapshot(locator=L.mask_designer.preview_window)

                check_path_no_updated = main_page.compare(motion_fourth_preview, motion_x_preview, similarity=0.98)
                case.result = (not check_path_no_updated)

            # Set designer timecode (00:00:00:25)
            mask_designer_page.set_MaskDesigner_timecode('00_00_00_25')
            time.sleep(DELAY_TIME*2)

            # Verify Step:
            current_preview = main_page.snapshot(locator=L.mask_designer.mask_designer_window, file_name=Auto_Ground_Truth_Folder + 'L232.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L232.png', current_preview)
            case.result = check_preview

        # [L234] 3.7 Mask Designer (Sport 02.jpg) > Adjust keyframe in simple timeline
        with uuid("ee9c8e69-b7c6-4288-956e-8074c75500d7") as case:
            # Show simple timeline
            main_page.click(L.mask_designer.btn_display_timeline_mode)
            time.sleep(DELAY_TIME)

            # Add 1st rotation keyframe on (00:00:00:25)
            mask_designer_page.simple_timeline.rotation.add_keyframe()
            time.sleep(DELAY_TIME)

            # Fold Path tab
            mask_designer_page.motion.open_path_tag(open=0)
            time.sleep(DELAY_TIME * 0.5)

            # Switch to Mask tab
            mask_designer_page.switch_to_mask()
            time.sleep(DELAY_TIME * 0.5)

            # Drag Properties scroll bar to down (1)
            mask_designer_page.drag_Mask_Settings_Scroll_Bar(1)

            # Set designer timecode (00:00:02:20)
            mask_designer_page.set_MaskDesigner_timecode('00_00_02_20')
            time.sleep(DELAY_TIME*2)

            # Set Rotation degree = 75 (2nd keyframe)
            mask_designer_page.object_settings.set_rotation('75')

            # Rotation : Click previous keyframe
            mask_designer_page.simple_timeline.rotation.click_previous_keyframe()

            # Verify Step:
            current_timecode = mask_designer_page.get_timecode()
            if current_timecode == '00:00:00:25':
                rotation_keyframe_settings = True
            else:
                rotation_keyframe_settings = False

            # Position : Click previous keyframe
            mask_designer_page.simple_timeline.position.click_previous_keyframe()
            time.sleep(DELAY_TIME * 0.5)

            # Position : Click next keyframe
            mask_designer_page.simple_timeline.position.click_next_keyframe()
            time.sleep(DELAY_TIME * 0.5)

            # Verify Step:
            current_preview = main_page.snapshot(locator=L.mask_designer.mask_designer_window, file_name=Auto_Ground_Truth_Folder + 'L234.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L234.png', current_preview)
            case.result = check_preview and rotation_keyframe_settings

            # Drag Properties scroll bar to top (0)
            mask_designer_page.drag_Mask_Settings_Scroll_Bar(0)

            # Remove custom mask (Title mask)
            mask_designer_page.Edit_MaskDesigner_RemoveCustomMask(index=1)

        # [L227] 3.7 Mask Designer (Sport 02.jpg) > feather radius
        with uuid("84117991-9ca4-43e0-a942-1dcb13a1bd6a") as case:
            # Fold Path tab
            mask_designer_page.Edit_MaskDesigner_Feather_radius_InputValue('5')
            time.sleep(DELAY_TIME)

            # Verify Step
            check_value = main_page.exist(L.mask_designer.mask_property.feather_slider).AXValue
            if check_value == 5:
                case.result = True
            else:
                case.result = False

        # [L229] 3.7 Mask Designer (Sport 02.jpg) > Set in [Object Settings] > Adjust ease in / ease out
        with uuid("36403805-ed5c-4f70-91e5-1d2fa25e3049") as case:
            # Set designer timecode (00:00:00:29)
            mask_designer_page.set_MaskDesigner_timecode('00_00_00_29')
            time.sleep(DELAY_TIME*2)
            no_ease_out_preview = main_page.snapshot(locator=L.mask_designer.preview_window)

            # Set designer timecode (00:00:02:10)
            mask_designer_page.set_MaskDesigner_timecode('00_00_02_10')
            time.sleep(DELAY_TIME*2)
            no_ease_in_preview = main_page.snapshot(locator=L.mask_designer.preview_window)

            # Drag scroll bar to down
            mask_designer_page.drag_Mask_Settings_Scroll_Bar(1)

            # [Object setting] left panel: Click Rotation next keyframe to timecode (00:00:02:20)
            mask_designer_page.object_settings.rotation.click_next_keyframe()

            # Set ease in & ease in value = 0.94
            mask_designer_page.object_settings.rotation.ease_in.set_checkbox(value=True)
            time.sleep(DELAY_TIME)
            mask_designer_page.object_settings.rotation.ease_in.set_value('0.94')

            # [Object setting] left panel: Click Rotation previous keyframe to timecode (00:00:00:25)
            mask_designer_page.object_settings.rotation.click_previous_keyframe()

            # Set ease out & ease out value = 0.89
            mask_designer_page.object_settings.rotation.ease_out.set_checkbox(value=True)
            time.sleep(DELAY_TIME)
            mask_designer_page.object_settings.rotation.ease_out.set_value('0.89')

            # Verify step:

            # Set designer timecode (00:00:00:29)
            mask_designer_page.set_MaskDesigner_timecode('00_00_00_29')
            time.sleep(DELAY_TIME*2)
            apply_ease_out_preview = main_page.snapshot(locator=L.mask_designer.preview_window)

            # Set designer timecode (00:00:02:10)
            mask_designer_page.set_MaskDesigner_timecode('00_00_02_10')
            time.sleep(DELAY_TIME*2)
            apply_ease_in_preview = main_page.snapshot(locator=L.mask_designer.preview_window)

            # Similarity should less than 0.98, check_ease_out should be False
            check_ease_out = main_page.compare(no_ease_out_preview, apply_ease_out_preview, similarity=0.98)
            logger(check_ease_out)
            # Similarity should less than 0.98, check_ease_out should be False
            check_ease_in = main_page.compare(no_ease_in_preview, apply_ease_in_preview, similarity=0.98)
            logger(check_ease_in)

            case.result = (not check_ease_out) and (not check_ease_in)

        # [L228] 3.7 Mask Designer (Sport 02.jpg) > Set in [Object Settings] > Adjust keyframe
        with uuid("1912a860-16dd-4c0f-9d4f-a91a54b5117c") as case:
            # Set designer timecode (00:00:01:20)
            mask_designer_page.set_MaskDesigner_timecode('00_00_01_20')
            get_rotation_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_Rotation_Value()
            logger(get_rotation_value)

            # Rotation: Reset all rotation keyframe
            check_reset_btn = mask_designer_page.object_settings.rotation.click_reset_keyframe()
            logger(check_reset_btn)

            # Rotation: Get next keyframe status (False)
            check_rotation_next_keyframe = mask_designer_page.object_settings.rotation.click_next_keyframe()
            logger(check_rotation_next_keyframe)

            mask_designer_page.set_MaskDesigner_timecode('00_00_02_20')
            time.sleep(DELAY_TIME*1.5)
            verify_rotation_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_Rotation_Value()
            logger(verify_rotation_value)
            if get_rotation_value == verify_rotation_value:
                current_rotation_value = True
            else:
                current_rotation_value = False

            # Drag scroll bar to upper
            mask_designer_page.drag_Mask_Settings_Scroll_Bar(0.655)
            time.sleep(DELAY_TIME)

            # Position: Click next keyframe to timecode (00:00:05:00)
            mask_designer_page.object_settings.position.click_next_keyframe()
            time.sleep(DELAY_TIME)

            # Position: Get next keyframe status (False)
            check_pos_next_keyframe = mask_designer_page.object_settings.position.click_next_keyframe()
            logger(check_pos_next_keyframe)

            case.result = check_reset_btn and current_rotation_value and (not check_rotation_next_keyframe) and (not check_pos_next_keyframe)

        # [L235] 3.7 Mask Designer (Sport 02.jpg) > Check preview
        with uuid("566f1b44-0467-4ba1-ba9c-32c908bd5d9d") as case:
            # Click [Stop] to let timecode move to 0s
            mask_designer_page.Edit_MaskDesigner_PreviewOperation('Stop')
            time.sleep(DELAY_TIME)

            # Click [Play] button to check preview different
            mask_designer_page.Edit_MaskDesigner_PreviewOperation('Play')
            check_preview_update = main_page.Check_PreviewWindow_is_different(L.mask_designer.preview_window, sec=3)
            # Click [Stop]
            mask_designer_page.Edit_MaskDesigner_PreviewOperation('Stop')

            # check preview
            mask_designer_page.set_MaskDesigner_timecode('00_00_03_03')
            time.sleep(DELAY_TIME*2)

            # Verify Step:
            current_preview = main_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'L235.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L235.png', current_preview)
            case.result = check_preview and check_preview_update

        # [L224] 3.7 Mask Designer (Sport 02.jpg) > Create Brush Mask
        with uuid("60a044e9-e3b9-43c1-9cf4-58e937d2f0be") as case:
            # Drag scroll bar to top
            mask_designer_page.drag_Mask_Settings_Scroll_Bar(0)
            time.sleep(DELAY_TIME)

            # Click [Paint Mask]
            mask_designer_page.click_create_brush_mask_btn()
            check_enter = mask_designer_page.is_enter_brush_mask_designer()
            logger(check_enter)
            if check_enter:
                before_brush_preview = main_page.snapshot(locator=L.mask_designer.mask_property.brush_mask_designer.window)

            # Set tool width = 73
            mask_designer_page.brush_mask.width.set_value('73')
            time.sleep(DELAY_TIME)

            # Draw canvas w/ brush tool
            mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_left()
            mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_right()
            mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_middle()
            time.sleep(DELAY_TIME)

            apply_brush_preview = main_page.snapshot(locator=L.mask_designer.mask_property.brush_mask_designer.window)

            # Verify step (after used round tool)
            check_update = main_page.compare(before_brush_preview, apply_brush_preview)
            logger(check_update)

            # Click reset button
            mask_designer_page.brush_mask.click_reset()
            time.sleep(DELAY_TIME*1.5)
            main_page.click(L.main.confirm_dialog.btn_ok)

            # Change tool to (Add to selection)
            mask_designer_page.brush_mask.tools.set_smart_brush()

            # Set tool width = 22
            mask_designer_page.brush_mask.width.set_value('22')
            time.sleep(DELAY_TIME)

            # Draw canvas w/ brush tool
            mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_left()
            mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_middle()
            time.sleep(DELAY_TIME)

            apply_smart_preview = main_page.snapshot(locator=L.mask_designer.mask_property.brush_mask_designer.window)

            # Verify step (after used smart tool)
            check_smart = main_page.compare(apply_smart_preview, apply_brush_preview)
            logger(check_smart)

            # Click OK button
            mask_designer_page.brush_mask.click_ok_btn()
            time.sleep(DELAY_TIME*3)
            check_remove_custom = mask_designer_page.Edit_MaskDesigner_RemoveCustomMask(index=1)

            case.result = check_enter and (not check_update) and (not check_smart) and check_remove_custom

        # [L225] 3.7 Mask Designer (Sport 02.jpg) > Create Selection Mask
        with uuid("bdcee9e2-2f36-4b79-9444-fb6ad8484ebb") as case:
            # Click [Selection mask]
            mask_designer_page.click_create_selection_mask_btn()
            time.sleep(DELAY_TIME)

            # Draw mask
            mask_designer_page.draw_triangle_on_canvas(angle=5)
            time.sleep(DELAY_TIME)

            # Verify Step:
            current_preview = main_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'L225.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L225.png', current_preview, similarity=0.8)
            case.result = check_preview

        # [L231] 3.7 Mask Designer (Sport 02.jpg) > Manual adjust on canvas > Resize
        with uuid("e8a7cdf0-52b7-4353-9cf0-5a9d85c88406") as case:
            # Apply template
            mask_designer_page.MaskDesigner_Apply_template(14)

            # Set timecode
            mask_designer_page.set_MaskDesigner_timecode('00_00_01_26')
            time.sleep(DELAY_TIME)

            inital_apply_preview = main_page.snapshot(locator=L.mask_designer.preview_window)

            # resize
            mask_designer_page.adjust_object_on_canvas_resize(x=35, y=30)
            time.sleep(DELAY_TIME)
            after_resize_preview = main_page.snapshot(locator=L.mask_designer.preview_window)
            check_preview = main_page.compare(inital_apply_preview, after_resize_preview, similarity=0.965)
            logger(check_preview)

            case.result = not check_preview

        # [L236] 3.7 Mask Designer (Sport 02.jpg) > [Share] template online
        with uuid("346b278c-7aa6-4d43-a4b3-c0da5abc1b53") as case:
            # Apply template
            check_upload = mask_designer_page.share_to_cloud(name='mask_custom', tags='123', collection='test', description='move mask', verify_dz_link=1)
            logger(check_upload)
            time.sleep(DELAY_TIME*3)

            # Verify step: check title
            check_title = main_page.exist(L.mask_designer.mask_designer_window)
            logger(check_title.AXTitle)
            if check_title.AXTitle == 'Mask Designer  |  mask_custom':
                upload_save_back = True
            else:
                upload_save_back = False
            logger(upload_save_back)

            # ---------------------------------
            # Click [Save as] > Save custom name then close Mask designer
            mask_designer_page.Edit_MaskDesigner_ClickSaveAs()
            time.sleep(DELAY_TIME)
            mask_designer_page.save_as.input_name('BFT_mask_template')
            time.sleep(DELAY_TIME)
            mask_designer_page.save_as.click_ok()
            mask_designer_page.Edit_MaskDesigner_ClickOK()
            time.sleep(DELAY_TIME*2)
            # Enter Pip Room
            main_page.enter_room(4)

            # Click download content form CL/DZ
            pip_room_page.click_DownloadContent_from_DZCL()

            # Already enter "Download PiP Objects" > Open My Cyberlink Cloud
            # Select template name "dialog09_chroma"
            check_CL_content = download_from_cl_dz_page.select_template('mask_custom')
            time.sleep(DELAY_TIME)
            download_from_cl_dz_page.tap_delete_button()
            time.sleep(DELAY_TIME*3)

            # Close "Download PiP Objects" window
            # download_from_cl_dz_page.tap_close_button()
            main_page.press_esc_key()

            case.result = check_upload and upload_save_back and check_CL_content

        # [L237] 3.7 Mask Designer (Sport 02.jpg) > [OK] / [Save As] template
        with uuid("c07c3fd9-1aca-4e3e-931e-bf159193b7a3") as case:
            # Pip Room > Enter custom category
            main_page.select_LibraryRoom_category('Custom')
            time.sleep(DELAY_TIME*2)

            # Verify step: custom preview normally
            main_page.select_library_icon_view_media('BFT_mask_template')
            check_preview_update = main_page.Check_PreviewWindow_is_different(sec=2)
            logger(check_preview_update)
            case.result = check_preview_update

        # [L238] 3.7 Mask Designer (Sport 02.jpg) > Add mask template to timeline
        with uuid("7b75d53d-25d6-4cd5-be71-dc622abf75bc") as case:
            # Select timeline track 3
            main_page.timeline_select_track(3)

            # Set timeline timecode = (00:00:26:07)
            main_page.set_timeline_timecode('00_00_26_07')
            time.sleep(DELAY_TIME * 2)

            # Verify Step:
            current_preview = main_page.snapshot(locator=main_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'L238.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L238.png', current_preview)
            case.result = check_preview

        # Save project:
        main_page.top_menu_bar_file_save_project_as()
        main_page.handle_save_file_dialog(name='test_case_1_1_8',
                                          folder_path=Test_Material_Folder + 'BFT_21_Stage1/')
        time.sleep(DELAY_TIME * 3)

    #'''
    # 36 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # [L240] 3.8 Video Collage Designer > Open [Video Collage Designer]
        with uuid("ceac8405-fa0b-4210-a0d7-156b65fcdbde") as case:
            main_page.top_menu_bar_plugins_video_collage_designer()
            time.sleep(DELAY_TIME*2)

            main_window = main_page.exist(L.video_collage_designer.main_window)
            if main_window:
                case.result = True
            else:
                case.result = False

        # [L242] 3.8 Video Collage Designer > Choose layout (Default)
        with uuid("b2eeb6d2-27c9-40f3-91eb-21188f760789") as case:
            # Select layout 7
            video_collage_designer_page.layout.select_layout(7)

            # [L243] 3.8 Video Collage Designer > Import (Image and Video)
            with uuid("92df3704-1c50-4a1b-8b26-06bb72b48fb0") as case:
                # Import video to library
                video_collage_designer_page.media.import_media(Test_Material_Folder + 'fix_enhance_20/mountain.mp4')
                time.sleep(DELAY_TIME * 1.5)

                # Image mountain.mp4 to section 2
                video_collage_designer_page.media.click_auto_fill()

                # Import Image to library
                video_collage_designer_page.media.import_media(Test_Material_Folder + 'Video_Audio_In_Reverse/Sample.png')
                time.sleep(DELAY_TIME * 1.5)

                # Image Sample.png to section 1
                video_collage_designer_page.media.select_media('Sample.png')
                video_collage_designer_page.media.click_auto_fill()

                time.sleep(DELAY_TIME * 1.5)

                # Verify Step:
                current_preview = main_page.snapshot(locator=L.video_collage_designer.main_window, file_name=Auto_Ground_Truth_Folder + 'L242.png')
                check_preview = main_page.compare(Ground_Truth_Folder + 'L242.png', current_preview, similarity=0.9)
                case.result = check_preview
            case.result = check_preview


        # [L244] 3.8 Video Collage Designer > Filter options (Video only & color board)
        with uuid("967c9ed2-79d9-4360-b314-5b7a18582f21") as case:
            # Select layout 11 (index=10)
            video_collage_designer_page.layout.select_layout(10)

            all_media_library = main_page.snapshot(locator=L.video_collage_designer.media_library)
            logger(all_media_library)
            time.sleep(DELAY_TIME)

            # switch to color boards
            video_collage_designer_page.media.select_category(3)
            time.sleep(DELAY_TIME*2)
            color_board_media_library = main_page.snapshot(locator=L.video_collage_designer.media_library)
            logger(color_board_media_library)

            # Insert Blue color board
            main_page.double_click()
            time.sleep(DELAY_TIME* 1.5)
            video_collage_designer_page.media.click_auto_fill()
            time.sleep(DELAY_TIME * 1.5)

            # switch to video only
            video_collage_designer_page.media.select_category(1)

            # Skateboard 01.mp4 to section 1
            video_collage_designer_page.media.select_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)
            video_collage_designer_page.media.click_auto_fill()
            time.sleep(DELAY_TIME*2)

            # Verify Step:
            current_preview = main_page.snapshot(locator=L.video_collage_designer.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'L244.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L244.png', current_preview, similarity=0.9)

            check_update = main_page.compare(all_media_library, color_board_media_library, similarity=0.9)
            case.result = (not check_update) and check_preview

            # [L245] 3.8 Video Collage Designer > [Auto Fill] button
            with uuid("c38ba371-183f-4214-b115-02ba7d4cd789") as case:
                case.result = check_preview


        # [L253] 3.8 Video Collage Designer > Adjust Border > Size
        with uuid("5f8eeb3f-8323-4025-8701-eba85e26d586") as case:
            initial_border_value = video_collage_designer_page.border.get_border_value()
            logger(initial_border_value)
            video_collage_designer_page.border.set_border_slider(16)
            time.sleep(DELAY_TIME)
            apply_border_value = video_collage_designer_page.border.get_border_value()
            logger(apply_border_value)

            if initial_border_value == '0':
                initial_status = True
            else:
                initial_status = False

            if apply_border_value == '16':
                apply_status = True
            else:
                apply_status = False
            case.result = initial_status and apply_status

        # [L254] 3.8 Video Collage Designer > Adjust Border > Change Color
        with uuid("e8a29b39-2cbd-4533-9a6c-89c2362c6882") as case:
            # Set color to C4DE5A
            video_collage_designer_page.border.set_border_color('C4DE5A')
            time.sleep(DELAY_TIME)
            check_color = video_collage_designer_page.border.is_border_color('C4DE5A')
            logger(check_color)
            case.result = check_color

        # [L255] 3.8 Video Collage Designer > Adjust Border > Interclip size
        with uuid("5999111f-6785-45be-b1cd-d3ba9b243884") as case:
            initial_interclip_value = video_collage_designer_page.border.get_interclip_value()
            # Check initial value
            if initial_interclip_value == '10':
                initial_status = True
            else:
                initial_status = False

            # Set interclip size = 20
            video_collage_designer_page.border.set_interclip_slider(20)

            current_interclip_value = video_collage_designer_page.border.get_interclip_value()
            if current_interclip_value == '20':
                apply_slider = True
            else:
                apply_slider = False

            case.result = initial_status and apply_slider

        # [L258] 3.8 Video Collage Designer > Frame animation
        with uuid("b5701127-215f-44e9-a122-efdc14274086") as case:
            # Default is From Beginning
            video_collage_designer_page.set_timecode('00_00_00_12')
            time.sleep(DELAY_TIME)
            from_beginning_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)
            logger(from_beginning_preview)
            video_collage_designer_page.click_preview_operation('STOP')

            # Set frame animation to During closing
            video_collage_designer_page.border.set_frame_animation(index=1)

            video_collage_designer_page.set_timecode('00_00_00_12')
            time.sleep(DELAY_TIME)
            during_closing_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)
            logger(during_closing_preview)
            video_collage_designer_page.click_preview_operation('STOP')
            check_preview_no_update = main_page.compare(from_beginning_preview, during_closing_preview, similarity=0.98)
            logger(check_preview_no_update)

            video_collage_designer_page.set_timecode('00_00_09_17')
            time.sleep(DELAY_TIME)

            # Verify Step:
            current_preview = main_page.snapshot(locator=L.video_collage_designer.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'L258.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L258.png', current_preview)

            case.result = check_preview and (not check_preview_no_update)

        # [L256] 3.8 Video Collage Designer > Adjust [Border] > Fill type - Uniform color
        with uuid("95e51f49-8829-4b21-9886-08a95163ac0b") as case:
            video_collage_designer_page.click_preview_operation('STOP')
            time.sleep(DELAY_TIME)
            video_collage_designer_page.border.set_uniform_color('06471E')
            time.sleep(DELAY_TIME)

            current_interclip_value = video_collage_designer_page.border.get_uniform_color()
            if current_interclip_value == '06471E':
                case.result = True
            else:
                case.result = False

        # [L257] 3.8 Video Collage Designer > Adjust [Border] > Fill type - interclip texture
        with uuid("2113a2c8-b374-4e67-be7c-80b062d71439") as case:
            current_uniform_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)

            # Set fill type to interclip texture
            video_collage_designer_page.border.set_fill_type(1)
            time.sleep(DELAY_TIME)
            video_collage_designer_page.border.select_interclip_texture(Test_Material_Folder + 'Video_Audio_In_Reverse/Sample.png')

            # Set interclip size to 100
            video_collage_designer_page.border.set_interclip_value(100)

            # Verify Step:
            interclip_texture_preview = main_page.snapshot(locator=L.video_collage_designer.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'L257.png')
            check_interclip_texture = main_page.compare(Ground_Truth_Folder + 'L257.png', interclip_texture_preview)
            preview_no_changed = main_page.compare(interclip_texture_preview, current_uniform_preview)

            case.result = check_interclip_texture and (not preview_no_changed)

        # [L260] 3.8 Video Collage Designer > Start clip playback > After frame animation
        with uuid("c240b30c-d5d9-4dbb-972f-6d687ee8fd9a") as case:
            # Set interclip size to 16
            video_collage_designer_page.border.set_interclip_value(16)

            # Set frame animation to From Beginning
            video_collage_designer_page.border.set_frame_animation(index=0)
            time.sleep(DELAY_TIME*0.5)

            # Set (After frame animation)
            video_collage_designer_page.border.set_start_playback(1)

            video_collage_designer_page.set_timecode('00_00_01_29')
            time.sleep(DELAY_TIME)

            # Verify Step:
            current_preview = main_page.snapshot(locator=L.video_collage_designer.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'L260.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L260.png', current_preview)

            case.result = check_preview

        # [L248] 3.8 Video Collage Designer > Edit in Tile (above 4 tiles) > Set duration
        with uuid("57bbc6d9-bfd0-491b-a4a1-f6b5b7ab30a6") as case:
            video_collage_designer_page.click_preview_operation('STOP')
            elem_menu = main_page.exist(L.video_collage_designer.border.menu_frame_animation)
            ori_pos = elem_menu.AXPosition
            size_w, size_h = elem_menu.AXSize
            new_pos = (ori_pos[0] - size_w, ori_pos[1])
            main_page.mouse.move(new_pos[0], new_pos[1])
            main_page.right_click()
            time.sleep(DELAY_TIME)
            main_page.select_right_click_menu('Set duration...')

            # set duration = 9s
            main_page.set_time_code(el_locator=L.main.duration_setting_dialog.txt_duration,duration='00_00_09_00')

            # Get new duration
            main_page.mouse.move(new_pos[0], new_pos[1])
            main_page.right_click()
            time.sleep(DELAY_TIME)
            main_page.select_right_click_menu('Set duration...')
            time.sleep(DELAY_TIME*1.6)
            new_duration = main_page.exist(L.main.duration_setting_dialog.txt_duration)
            if new_duration.AXValue == '00:00:09:00':
                case.result = True
                # close duration dialog
                main_page.keyboard.enter()
            else:
                case.result = False
                logger(new_duration.AXValue)

        # [L252] 3.8 Video Collage Designer > Edit in Tile (above 4 tiles) > Remove clip from slot
        with uuid("e272149d-73ff-419f-be46-df32f13e7aec") as case:
            elelm_menu = main_page.exist(L.video_collage_designer.border.menu_frame_animation)
            ori_pos = elelm_menu.AXPosition
            size_w, size_h = elelm_menu.AXSize
            target_slot_pos = (ori_pos[0] - size_w, ori_pos[1])
            main_page.mouse.move(target_slot_pos[0], target_slot_pos[1])
            main_page.right_click()
            time.sleep(DELAY_TIME)
            case.result = main_page.select_right_click_menu('Remove')
            time.sleep(DELAY_TIME)


        # [L246] 3.8 Video Collage Designer > Edit in Tile (above 4 tiles) > Exchange slot media
        with uuid("bbe3cfc9-06c2-45f8-9eab-a3c5a9bdd651") as case:
            elelm_menu = main_page.exist(L.video_collage_designer.border.menu_frame_animation)
            ori_pos = elelm_menu.AXPosition
            size_w, size_h = elelm_menu.AXSize
            target_slot_pos = (ori_pos[0] - size_w, ori_pos[1])
            upper_slot_pos = (ori_pos[0] - size_w, ori_pos[1] - size_h * 5)
            main_page.drag_mouse(upper_slot_pos, target_slot_pos)
            time.sleep(DELAY_TIME*2)

            # Verify Step:
            current_preview = main_page.snapshot(locator=L.video_collage_designer.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'L246.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L246.png', current_preview)

            case.result = check_preview
        time.sleep(DELAY_TIME*2)

        # [L250] 3.8 Video Collage Designer > Edit in Tile (above 4 tiles) > Mute/ un-mute
        with uuid("63aa5fba-c432-4b8f-85c5-e125f457d1e2") as case:
            # Mouse Hover Slot 3
            elelm_menu = main_page.exist(L.video_collage_designer.border.menu_frame_animation)
            ori_pos = elelm_menu.AXPosition
            size_w, size_h = elelm_menu.AXSize
            target_slot_pos = (ori_pos[0] - size_w, ori_pos[1])
            main_page.mouse.move(target_slot_pos[0], target_slot_pos[1])

            un_mute_icon = main_page.exist(locator=L.video_collage_designer.preview.btn_mute)

            # Verify Step:
            un_mute_icon_image = main_page.snapshot(locator=L.video_collage_designer.preview.btn_mute,
                                                 file_name=Auto_Ground_Truth_Folder + 'L250.png')
            check_un_mute_icon_ = main_page.compare(Ground_Truth_Folder + 'L250.png', un_mute_icon_image)

            if un_mute_icon:
                main_page.click(L.video_collage_designer.preview.btn_mute)
                time.sleep(DELAY_TIME)

            mute_icon_image = main_page.snapshot(locator=L.video_collage_designer.preview.btn_mute)
            logger(mute_icon_image)
            check_no_update = main_page.compare(mute_icon_image, un_mute_icon_image)
            case.result = check_un_mute_icon_ and (not check_no_update)

        # [L259] 3.8 Video Collage Designer > Start clip playback > With frame animation
        with uuid("2c3ae0f3-5981-4f0a-ad2d-c5cf5f49ee80") as case:
            # Add Skateboard 03.mp4 to Slot 4
            video_collage_designer_page.media.select_media('Skateboard 03.mp4')
            time.sleep(DELAY_TIME)
            video_collage_designer_page.media.click_auto_fill()
            time.sleep(DELAY_TIME*2)

            # Set (With frame animation)
            video_collage_designer_page.border.set_start_playback(0)

            video_collage_designer_page.set_timecode('00_00_01_29')
            time.sleep(DELAY_TIME)

            # Verify Step:
            current_preview = main_page.snapshot(locator=L.video_collage_designer.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'L259.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L259.png', current_preview)

            case.result = check_preview

        # [L247] 3.8 Video Collage Designer > Edit in Tile (above 4 tiles) > Zoom Slider
        with uuid("78bc1294-a79a-44e3-8857-783c1442ff48") as case:
            video_collage_designer_page.click_preview_operation('STOP')
            time.sleep(DELAY_TIME)
            no_zoom_in_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)

            elelm_menu = main_page.exist(L.video_collage_designer.border.menu_frame_animation)
            ori_pos = elelm_menu.AXPosition
            size_w, size_h = elelm_menu.AXSize
            target_slot_pos = (ori_pos[0] - size_w*3, ori_pos[1])
            main_page.mouse.move(target_slot_pos[0], target_slot_pos[1])

            zoom_in_btn = main_page.exist(L.video_collage_designer.preview.btn_zoom_in)
            zoom_out_btn = main_page.exist(L.video_collage_designer.preview.btn_zoom_out)
            zoom_slider = main_page.exist(L.video_collage_designer.preview.slider_zoom)
            if not zoom_in_btn:
                case.result = False
            elif not zoom_out_btn:
                case.result = False
            elif not zoom_slider:
                case.result = False
            else:
                for x in range(5):
                    main_page.click(L.video_collage_designer.preview.btn_zoom_in)
                    time.sleep(DELAY_TIME*0.5)

                time.sleep(DELAY_TIME)
                apply_zoom_in_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)
                check_zoom_in_no_update = main_page.compare(no_zoom_in_preview, apply_zoom_in_preview, similarity=0.98)
                logger(check_zoom_in_no_update)

                # Set zoom slider to (Zoom out)
                zoom_slider.AXValue = 0

                time.sleep(DELAY_TIME)
                apply_zoom_out_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)
                check_zoom_out = main_page.compare(no_zoom_in_preview, apply_zoom_out_preview, similarity=0.98)
                logger(check_zoom_out)
                case.result = not check_zoom_in_no_update and check_zoom_out

        # [L249] 3.8 Video Collage Designer > Edit in Tile (above 4 tiles) > Trim Video
        with uuid("6531953b-b585-4c45-b250-8afa2a929835") as case:
            main_page.click(L.video_collage_designer.preview.btn_trim)
            time.sleep(DELAY_TIME * 0.5)

            # Check open Trim window
            is_enter_trim = trim_page.check_in_Trim()
            logger(is_enter_trim)

            # Set (In Position) to 00;00;05;09
            precut_page.set_single_trim_precut_in_position('00_05_09')
            time.sleep(DELAY_TIME)

            # Verify step: Get duration
            current_duration = precut_page.get_precut_single_trim_duration()
            logger(current_duration)

            if current_duration == '00:00:05:27':
                apply_trim = True
            else:
                apply_trim = False
            logger(apply_trim)

            # click [OK] to close trim window
            precut_page.click_ok()

            case.result = is_enter_trim and apply_trim

        # [L262] 3.8 Video Collage Designer > Before/after clip playback > Display color board
        with uuid("13847aea-4ede-4802-9b3f-0c308044aa69") as case:
            # Scroll down to show (Before/after clip playback) settings
            video_collage_designer_page.border.set_scroll_bar(1)

            # Set Display color board
            video_collage_designer_page.border.set_before_after_clip_playback(1)

            # Set color
            video_collage_designer_page.border.set_before_after_color_board('BE3400')

            # Verify step:
            video_collage_designer_page.set_timecode('00_00_09_29')
            time.sleep(DELAY_TIME)

            current_preview = main_page.snapshot(locator=L.video_collage_designer.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'L262.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L262.png', current_preview)

            case.result = check_preview

        # [L266] 3.8 Video Collage Designer > Advanced Settings > Playback timing > One after another
        with uuid("f50cc40e-42c3-455e-8607-9b1802e32821") as case:
            video_collage_designer_page.click_preview_operation('STOP')
            time.sleep(DELAY_TIME)

            video_collage_designer_page.set_timecode('00_00_04_29')
            time.sleep(DELAY_TIME)

            before_apply_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)
            video_collage_designer_page.click_preview_operation('STOP')
            time.sleep(DELAY_TIME)

            # Click [Advanced Settings] button
            video_collage_designer_page.border.click_advanced_setting()

            # Set (One after another)
            video_collage_designer_page.border.advanced.set_playback_timing(2)

            # Click [Advanced ok]
            video_collage_designer_page.border.advanced.click_ok()

            # Verify step:
            video_collage_designer_page.set_timecode('00_00_04_29')
            time.sleep(DELAY_TIME)

            after_apply_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)

            check_preview_no_update = main_page.compare(after_apply_preview, before_apply_preview, similarity=0.98)

            case.result = not check_preview_no_update

        # [L263] 3.8 Video Collage Designer > Before/after clip playback > Restart playback
        with uuid("41e1f553-adaa-41ff-912a-91780fbe30ea") as case:
            #video_collage_designer_page.set_timecode('00_00_23_03')
            video_collage_designer_page.set_timecode('00_00_18_00')
            time.sleep(DELAY_TIME)

            # Verify Step:
            before_set_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)

            video_collage_designer_page.click_preview_operation('STOP')
            time.sleep(DELAY_TIME)

            # Set Restart playback
            video_collage_designer_page.border.set_before_after_clip_playback(2)

            # Verify step:
            video_collage_designer_page.set_timecode('00_00_18_00')
            time.sleep(DELAY_TIME)

            after_set_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)

            # Check before/after is different preview
            check_preview_the_same = main_page.compare(after_set_preview, before_set_preview, similarity=0.98)
            logger(check_preview_the_same)
            case.result = not check_preview_the_same

        # [L261] 3.8 Video Collage Designer > Before/after clip playback > Freeze
        with uuid("3f20acc7-53cd-4fb9-abe5-a6f74ac92f01") as case:
            video_collage_designer_page.click_preview_operation('STOP')
            time.sleep(DELAY_TIME)

            # Set Freeze
            video_collage_designer_page.border.set_before_after_clip_playback(0)

            # Verify step:
            video_collage_designer_page.set_timecode('00_00_18_00')
            time.sleep(DELAY_TIME)

            after_freeze_preview = main_page.snapshot(locator=L.video_collage_designer.main_window,
                                             file_name=Auto_Ground_Truth_Folder + 'L261.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L261.png', after_freeze_preview)
            case.result = check_preview

        # [L264] 3.8 Video Collage Designer > Advanced Settings > Playback timing > All at once
        with uuid("c8738608-13c3-42b0-a7d4-1dcfad025805") as case:
            video_collage_designer_page.click_preview_operation('STOP')
            time.sleep(DELAY_TIME)

            video_collage_designer_page.set_timecode('00_00_07_00')
            time.sleep(DELAY_TIME)
            before_apply_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)

            video_collage_designer_page.click_preview_operation('STOP')
            time.sleep(DELAY_TIME)

            # Click [Advanced Settings] button
            video_collage_designer_page.border.click_advanced_setting()

            # Set (All at once)
            video_collage_designer_page.border.advanced.set_playback_timing(0)

            # Click [Advanced ok]
            video_collage_designer_page.border.advanced.click_ok()

            video_collage_designer_page.set_timecode('00_00_07_00')
            time.sleep(DELAY_TIME)

            # Verify Step:
            all_at_once_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)
            check_preview_no_update = main_page.compare(before_apply_preview, all_at_once_preview, similarity=0.99)
            logger(check_preview)
            case.result = not check_preview_no_update

        # [L265] 3.8 Video Collage Designer > Advanced Settings > Playback timing > Delay three seconds
        with uuid("8c66467f-082c-4788-9878-7e4cf92aa5c5") as case:
            video_collage_designer_page.click_preview_operation('STOP')
            time.sleep(DELAY_TIME)

            # Click [Advanced Settings] button
            video_collage_designer_page.border.click_advanced_setting()

            # Set (Delay three seconds)
            video_collage_designer_page.border.advanced.set_playback_timing(1)
            video_collage_designer_page.border.advanced.set_delay_sec(3)

            # Click [Advanced ok]
            video_collage_designer_page.border.advanced.click_ok()

            # Verify step:
            video_collage_designer_page.set_timecode('00_00_07_00')
            time.sleep(DELAY_TIME)

            after_delay_3_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)
            check_no_update = main_page.compare(all_at_once_preview, after_delay_3_preview, similarity=0.99)
            case.result = not check_no_update

        # [L269] 3.8 Video Collage Designer > Advanced Settings > Match collage duration to > Shortest Clip
        with uuid("c425f63d-e7f7-4a78-a05b-a488a0b84ca8") as case:
            video_collage_designer_page.click_preview_operation('STOP')
            time.sleep(DELAY_TIME)

            # Click [Advanced Settings] button
            video_collage_designer_page.border.click_advanced_setting()

            # Set shortest
            video_collage_designer_page.border.advanced.set_match_collage_duration_to(2)

            # Click [Advanced ok]
            video_collage_designer_page.border.advanced.click_ok()
            time.sleep(DELAY_TIME*2)

            # Verify step:
            video_collage_designer_page.set_timecode('00_00_10_30')
            time.sleep(DELAY_TIME)

            timecode = main_page.exist(L.video_collage_designer.time_code).AXValue
            logger(timecode)

            if timecode == '00:00:05:27':
                case.result = True
            else:
                case.result = False

        # [L270] 3.8 Video Collage Designer > Advanced Settings > Match collage duration to > Clip N
        with uuid("df6edb35-12ab-45c4-9f3b-4f0cf1044bde") as case:
            video_collage_designer_page.click_preview_operation('STOP')
            time.sleep(DELAY_TIME)

            # Click [Advanced Settings] button
            video_collage_designer_page.border.click_advanced_setting()

            # Set match to clip3
            video_collage_designer_page.border.advanced.set_match_collage_duration_to(5)

            # Click [Advanced ok]
            video_collage_designer_page.border.advanced.click_ok()
            time.sleep(DELAY_TIME*2)

            # Verify step:
            video_collage_designer_page.set_timecode('00_00_18_10')
            time.sleep(DELAY_TIME)

            timecode = main_page.exist(L.video_collage_designer.time_code).AXValue
            logger(timecode)

            if timecode == '00:00:13:00':
                case.result = True
            else:
                case.result = False

        # [L268] 3.8 Video Collage Designer > Advanced Settings > Match collage duration to > Longest
        with uuid("b0f2b7b4-15cc-4b14-85e4-a932883c3de9") as case:
            video_collage_designer_page.click_preview_operation('STOP')
            time.sleep(DELAY_TIME)

            # Click [Advanced Settings] button
            video_collage_designer_page.border.click_advanced_setting()

            # Set Longest clip
            video_collage_designer_page.border.advanced.set_match_collage_duration_to(1)

            # Set (Delay one seconds)
            video_collage_designer_page.border.advanced.set_delay_sec(1)

            # Click [Advanced ok]
            video_collage_designer_page.border.advanced.click_ok()
            time.sleep(DELAY_TIME*2)

            # Verify step:
            video_collage_designer_page.set_timecode('00_00_18_29')
            time.sleep(DELAY_TIME)

            timecode = main_page.exist(L.video_collage_designer.time_code).AXValue
            logger(timecode)

            if timecode == '00:00:11:00':
                case.result = True
            else:
                case.result = False

        # [L267] 3.8 Video Collage Designer > Advanced Settings > Match collage duration to > All Videos
        with uuid("dd2c1071-c8ba-4f9a-a76f-7c0ba43c966b") as case:
            video_collage_designer_page.click_preview_operation('STOP')
            time.sleep(DELAY_TIME)

            # Click [Advanced Settings] button
            video_collage_designer_page.border.click_advanced_setting()

            # Set (All Videos)
            video_collage_designer_page.border.advanced.set_match_collage_duration_to(0)

            # Click [Advanced ok]
            video_collage_designer_page.border.advanced.click_ok()
            time.sleep(DELAY_TIME*2)

            # Verify step:
            video_collage_designer_page.set_timecode('00_00_18_29')
            time.sleep(DELAY_TIME)

            timecode = main_page.exist(L.video_collage_designer.time_code).AXValue
            logger(timecode)

            if timecode == '00:00:13:00':
                check_timecode = True
            else:
                check_timecode = False

            current_preview = main_page.snapshot(locator=L.video_collage_designer.main_window,
                                             file_name=Auto_Ground_Truth_Folder + 'L267.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L267.png', current_preview)
            case.result = check_preview and check_timecode

        # [L271] 3.8 Video Collage Designer > [Preview] in designer
        with uuid("b47f849f-5fae-4bab-8b57-595bb7f6e2aa") as case:
            video_collage_designer_page.click_preview_operation('STOP')
            time.sleep(DELAY_TIME)

            # Verify step:
            video_collage_designer_page.set_timecode('00_00_08_05')
            time.sleep(DELAY_TIME)

            current_preview = main_page.snapshot(locator=L.video_collage_designer.main_window,
                                             file_name=Auto_Ground_Truth_Folder + 'L271.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L271.png', current_preview)
            case.result = check_preview

        # [L272] 3.8 Video Collage Designer > Advanced Settings > [Save as] Video Collage layout
        with uuid("7a264c7c-3140-489d-960b-38f2bf42a0c6") as case:
            video_collage_designer_page.click_save_as_with_name('video_collage_custom_test')
            time.sleep(DELAY_TIME*2)

            # Check layout to show the custom layout
            check_layout_frame = main_page.snapshot(locator=L.video_collage_designer.layout.frame,
                                             file_name=Auto_Ground_Truth_Folder + 'L272.png')
            check_custom_frame_result = main_page.compare(Ground_Truth_Folder + 'L272.png', check_layout_frame)


            # Current custom layout w/ custom template
            current_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)
            time.sleep(DELAY_TIME)

            # Set layout to 13th (index=13)
            video_collage_designer_page.layout.select_layout(13)
            time.sleep(DELAY_TIME*2)
            apply_13_layout_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)
            time.sleep(DELAY_TIME*2)

            # Set layout to 1st (index=1)
            video_collage_designer_page.layout.select_layout(1)
            time.sleep(DELAY_TIME * 2)
            apply_1_layout_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)

            check_no_update = main_page.compare(current_preview, apply_13_layout_preview)
            check_the_same_preview = main_page.compare(current_preview, apply_1_layout_preview, similarity=0.99)

            case.result = check_custom_frame_result and (not check_no_update) and check_the_same_preview

        # [L273] 3.8 Video Collage Designer > [Share] template online
        with uuid("c956d061-593c-439f-84c8-a9222942b172") as case:
            check_upload_result = video_collage_designer_page.share_to_dz('test_video_collage')
            logger(check_upload_result)
            time.sleep(DELAY_TIME*2)
            case.result = check_upload_result

        current_L273_preview = main_page.snapshot(locator=L.video_collage_designer.main_window)
        logger(current_L273_preview)

        # [L274] 3.8 Video Collage Designer > Click [OK] to timeline
        with uuid("d8525e33-043e-49ec-8931-81c006580b72") as case:
            video_collage_designer_page.click_ok()
            time.sleep(DELAY_TIME*2)

            # Verify 0s
            current_0_sec_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                    file_name=Auto_Ground_Truth_Folder + 'L274_0sec.png')
            check_0_result = main_page.compare(Ground_Truth_Folder + 'L274_0sec.png', current_0_sec_preview, similarity=0.9)
            logger(check_0_result)

            # Verify 00:00:09:00
            main_page.set_timeline_timecode('00_00_09_00')
            time.sleep(DELAY_TIME*2)
            current_9_sec_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                    file_name=Auto_Ground_Truth_Folder + 'L274_9sec.png')
            check_9_result = main_page.compare(Ground_Truth_Folder + 'L274_9sec.png', current_9_sec_preview, similarity=0.9)
            logger(check_9_result)

            case.result = check_0_result and check_9_result

        # [L275] 3.8 Video Collage Designer > Back to Designer from tips area [Video Collage] button
        with uuid("39a7ac17-ade8-4e8f-b87f-b0ff4cb815bd") as case:
            # Click tips area [Video Collage] button to enter Video Collage designer
            tips_area_page.click_TipsArea_btn_VideoCollage()
            time.sleep(DELAY_TIME*2)

            # Verify step:
            collage_designer_elem = main_page.exist(L.video_collage_designer.main_window)
            if not collage_designer_elem:
                case.result = False
            else:
                case.result = True

                # remove 2 custom template
                # 1st: save as template, 2nd: upload online
                for x in range(2):
                    # Set layout to 1st (index=1) to remove custom layout
                    video_collage_designer_page.layout.select_layout(1)

                    # right click menu > delete
                    main_page.right_click()
                    time.sleep(DELAY_TIME * 0.5)
                    main_page.select_right_click_menu('Delete (only for Custom/Downloaded)')

                    # click yes if pop up warning message
                    video_collage_designer_page.layout.click_remove_yes()

        # Click ok to leave designer / back to timeline
        video_collage_designer_page.click_ok()

        # [L276] 3.8 Video Collage Designer > Save Project & Pack material
        with uuid("06e25859-e0ac-49f6-b667-bd4dae1342c8") as case:
            # Enter intro room > Saved Templates category
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 4)

            intro_video_page.enter_saved_category()

            # Insert custom template from (Intro Room)
            intro_video_page.select_intro_template_method_2(1)
            main_page.right_click()
            main_page.select_right_click_menu('Add to Timeline')

            # handle warning message "Do you want to edit the template in the Video Intro Designer?"
            main_page.click(L.base.confirm_dialog.btn_no)
            time.sleep(DELAY_TIME*5)

            # Enter Title Room > Custom category
            main_page.enter_room(1)
            time.sleep(DELAY_TIME*3)
            main_page.select_LibraryRoom_category('Custom')

            # Select track 1
            main_page.timeline_select_track(1)

            # Set timecode
            main_page.set_timeline_timecode('00_00_22_00')

            # Insert Custom title to track 1
            main_page.drag_media_to_timeline_playhead_position('BFT_title_Save', track_no=1)

            # Insert Custom title to track 2
            main_page.drag_media_to_timeline_playhead_position('BFT_MGT_Save', track_no=2)

            # Enter Title Room > Custom category
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 3)
            main_page.select_LibraryRoom_category('Custom')

            # Insert Custom title to track 3
            main_page.drag_media_to_timeline_playhead_position('BFT_mask_template', track_no=3)

            # Select track 1
            main_page.timeline_select_track(1)

            # Set timecode
            main_page.set_timeline_timecode('00_00_09_00')

            # Insert Custom title to track 3
            main_page.drag_media_to_timeline_playhead_position('BFT_Pip_Custom', track_no=3)

            # Insert Custom title to track 2
            main_page.drag_media_to_timeline_playhead_position('Custom_shape_10', track_no=2)

            # Enter Particle Room > Custom category
            main_page.enter_room(5)
            time.sleep(DELAY_TIME * 2)
            main_page.select_LibraryRoom_category('Custom')

            # Select track 3
            main_page.timeline_select_track(3)

            # Set timecode
            main_page.set_timeline_timecode('00_00_14_00')

            main_page.select_library_icon_view_media('BFT_snowflakes_custom')

            # Insert button > Trim to fit
            main_page.tips_area_insert_media_to_selected_track(5)

            # Select track 3
            main_page.timeline_select_track(2)

            # Set timecode
            main_page.set_timeline_timecode('00_00_17_23')
            time.sleep(DELAY_TIME*3)

            # Verify Step:
            current_17_sec_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                    file_name=Auto_Ground_Truth_Folder + 'L276_17sec.png')
            check_17_result = main_page.compare(Ground_Truth_Folder + 'L276_17sec.png', current_17_sec_preview, similarity=0.9)
            logger(check_17_result)

            # Pack project
            pack_result = main_page.top_menu_bar_file_pack_project_materials(project_path=Test_Material_Folder + 'BFT_21_Stage1/second_project/')

            # wait pack project processing ready
            time.sleep(DELAY_TIME * 15)

            case.result = check_17_result and pack_result

        # [L277] 3.8 Video Collage Designer > Re-launch PDR
        with uuid("ab28eca5-7ac6-451d-953a-ced27c3579e3") as case:
            main_page.close_and_restart_app()

            # Verify step
            case.result = main_page.select_library_icon_view_media('Mahoroba.mp3')

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_10(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # [L389] 5. Produce > Open Recent project
        with uuid("4cc570a7-5122-4edc-880b-1bc832bd6a40") as case:
            # Open recent project
            main_page.top_menu_bar_file_open_recent_projects(Test_Material_Folder + 'BFT_21_Stage1/second_project.pdk')
            time.sleep(DELAY_TIME*3)
            # Select extract path
            main_page.delete_folder(Test_Material_Folder + 'BFT_21_Stage1/extract_flder_2')
            time.sleep(DELAY_TIME)
            main_page.select_file(Test_Material_Folder + 'BFT_21_Stage1/extract_flder_2')
            time.sleep(DELAY_TIME*5)
            main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')
            time.sleep(DELAY_TIME*3)

            project_new_page.open_project.file_missing.click_browse()
            time.sleep(DELAY_TIME)
            main_page.select_file(Test_Material_Folder + 'Video_Audio_In_Reverse/Sample.png')
            time.sleep(DELAY_TIME * 5)


            # Verify Step:

            # Set timeline timecode = (00:00:11:23)
            main_page.set_timeline_timecode('00_00_11_23')
            time.sleep(DELAY_TIME * 4)
            # Check preview with timeline timecode = (00:00:11:23)
            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view, file_name=Auto_Ground_Truth_Folder + 'L389.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L389.png', current_preview, similarity=0.9)
            logger(check_preview)
            case.result = check_preview

        # [L390] 5. Produce > H.264 AVC > Format : M2TS
        with uuid("96a3cc91-a4f0-40ea-a95c-92238604beca") as case:
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            produce_page.local.select_file_extension('m2ts')
            time.sleep(DELAY_TIME)

            current_file_extension = main_page.exist(L.produce.local.cbx_file_extension).AXTitle
            if current_file_extension == 'M2TS':
                case.result = True
            else:
                case.result = False

        # [L391] 5. Produce > H.264 > Format : 1280x720/24p
        with uuid("88eaa322-c562-42ae-aa49-9546031d7ab7") as case:
            produce_page.local.select_profile_name(3)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 1280 x 720/24p (16 Mbps)':
                case.result = False
                case.fail_log = check_profile
            else:
                case.result = True

            # Get produced file name
            explore_file = produce_page.get_produced_filename()
            logger(explore_file)

        # [L392] 5. Produce > H.264 > Select encode type (HW)
        with uuid("f59de452-91d4-44c6-967e-f20638dbfe2f") as case:
            produce_page.local.set_fast_video_rendering_hardware_encode()
            time.sleep(DELAY_TIME)
            current_HW_status = produce_page.local.set_fast_video_rendering_hardware_encode()
            case.result = current_HW_status

        # [L393] 5. Produce > H.264 > Upload a copy to Cloud
        with uuid("d3b1d266-84a5-4c43-9c48-5d73b14f6fd1") as case:
            produce_page.local.set_check_upload_copy_to_cyberlink_cloud(is_check=1)
            time.sleep(DELAY_TIME)
            current_upload_checkbox = produce_page.local.check_visible_upload_copy_to_cyberlink_cloud()
            logger(current_upload_checkbox)
            case.result = current_upload_checkbox

        # [L394] 5. Produce > H.264 > Start [Produce] w/ handle (Convert to MP4 = No)
        with uuid("7849c8fe-7f00-4830-a9a3-bf15ffc129da") as case:
            # Set timecode to last frame
            produce_page.local.set_preview_timecode('00_00_50_00')
            time.sleep(DELAY_TIME*1.5)
            current_last_frame = produce_page.get_preview_timecode()
            logger(current_last_frame)
            if current_last_frame == '00_00_39_00':
                check_last_frame = True
            else:
                check_last_frame = False
            logger(check_last_frame)

            # Start : produce
            produce_page.click(L.produce.btn_start_produce)
            time.sleep(DELAY_TIME*1.5)

            # handle dialog: Convert to MP4 = No
            produce_page.local.click_option_convert_cyberlink_cloud_copy_to_mp4_dialog(option=0)
            for x in range(60):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # wait for video upload to cloud
            for x in range(40):
                back_btn = main_page.exist(L.produce.btn_back_to_edit_after_upload_cl)
                if back_btn:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click(L.produce.btn_back_to_edit_after_upload_cl)
            time.sleep(DELAY_TIME * 5)

            # Verify step:
            check_explore_file = main_page.select_library_icon_view_media(explore_file)

            # Verify step2: Remove the upload video
            # Click Import media > (Download media from Cyberlink cloud)
            media_room_page.import_media_from_cyberlink_cloud()

            time.sleep(DELAY_TIME * 3)

            # Double click to enter PowerDirector folder
            import_media_from_cloud_page.select_content_in_folder_level(folder_index=0, click_times=2)

            # Search explore_file
            import_media_from_cloud_page.input_text_in_seacrh_library(explore_file)

            # Tick 'Select all'
            import_media_from_cloud_page.tap_select_deselect_all_btn()

            # Check remove button
            remove_btn = main_page.exist(L.import_downloaded_media_from_cl.delete_btn).AXEnabled

            # Remove
            import_media_from_cloud_page.tap_remove_btn()

            case.result = check_explore_file and remove_btn

            # Close (Download Media) window
            time.sleep(DELAY_TIME)
            main_page.click(L.import_downloaded_media_from_cl.close_btn)

        # [L395] 5. Produce > Playback produced clip
        with uuid("5143f3c6-d5a5-4414-90ff-f4bdb3722454") as case:
            main_page.select_library_icon_view_media(explore_file)
            # Verify 1: Check produce clip "preview" is updated
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            check_result = main_page.Check_PreviewWindow_is_different(area=L.base.Area.preview.main, sec=5)
            playback_window_page.Edit_Timeline_PreviewOperation('Stop')
            time.sleep(DELAY_TIME*2)

            # Change timecode to check preview
            main_page.set_timeline_timecode('00_00_11_23')
            time.sleep(DELAY_TIME * 2)
            # Check preview with timeline timecode = (00:00:11:23)
            current_preview = main_page.snapshot(locator=main_page.area.preview.main)
            check_2_preview = main_page.compare(Ground_Truth_Folder + 'L389.png', current_preview, similarity=0.93)
            case.result = check_result and check_2_preview

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_11(self):
        # [L47] 2.1 Media Room > My Project > Open project
        with uuid("30dd64f8-7edd-4a15-a3a0-61f667a3b5fc") as case:
            # launch APP
            main_page.start_app()
            time.sleep(DELAY_TIME * 4)

            # Enter My Project
            project_room_page.enter_project_room()
            time.sleep(DELAY_TIME*2)

            before_open_project = main_page.snapshot(locator=main_page.area.library_icon_view)

            # Open project
            main_page.top_menu_bar_file_open_project(save_changes='no')
            main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/can_del.pds')
            main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

            # Enter My Project
            project_room_page.enter_project_room()
            time.sleep(DELAY_TIME*2)

            after_open_project = main_page.snapshot(locator=main_page.area.library_icon_view)

            thumbnail_no_update = main_page.compare(before_open_project, after_open_project, similarity=0.999)
            thumbnail_little_update = main_page.compare(before_open_project, after_open_project, similarity=0.85)
            case.result = (not thumbnail_no_update) and thumbnail_little_update

            main_page.close_and_restart_app()
            time.sleep(DELAY_TIME*4)

        # [L51] 2.1 Media Room > My Project > Nested project editing
        with uuid("811ecd35-7548-48d3-8f55-9d25ad29d0f9") as case:
            # Enter My Project
            project_room_page.enter_project_room()
            time.sleep(DELAY_TIME*2)

            main_page.select_library_icon_view_media('can_del')
            project_room_page.tips_area_insert_project_to_selected_track()

            # select timeline track 2
            main_page.timeline_select_track(2)

            # select timeline track 1
            main_page.timeline_select_track(1)

            # Click [View Entire Video]
            timeline_operation_page.click_view_entire_video_btn()
            time.sleep(DELAY_TIME*2)
            before_edit_timeline = main_page.snapshot(locator=L.timeline_operation.workspace)

            # Enter Media room
            media_room_page.enter_media_content()

            # Insert Landscape 01.jpg to timeline
            main_page.select_library_icon_view_media('Landscape 01.jpg')
            main_page.tips_area_insert_media_to_selected_track(1)

            # Click [View Entire Video] (Timeline should update)
            timeline_operation_page.click_view_entire_video_btn()
            time.sleep(DELAY_TIME*2)
            after_edit_timeline = main_page.snapshot(locator=L.timeline_operation.workspace)

            check_nested_editing_no_update = main_page.compare(before_edit_timeline, after_edit_timeline, similarity=0.98)
            case.result = not check_nested_editing_no_update

        # [L53] 2.1 Media Room > Insert clip to timeline & preview (4:3)
        with uuid("167d01d3-97d1-4ca7-95df-36bdaff67a08") as case:
            main_page.set_project_aspect_ratio_4_3()

            # Set timecode :
            main_page.set_timeline_timecode('00_00_08_00')
            time.sleep(DELAY_TIME * 2)

            aspect_ratio43_preview = main_page.snapshot(locator=main_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'L53.png')
            time.sleep(DELAY_TIME * 2)
            check_result = main_page.compare(Ground_Truth_Folder + 'L53.png', aspect_ratio43_preview)
            case.result = check_result

        # [L52] 2.1 Media Room > Insert clip to timeline & preview > Able to insert clip to selected track
        with uuid("d52b3eed-f381-4384-8166-cfa75b44b373") as case:
            playback_window_page.Edit_Timeline_PreviewOperation('stop')

            # select timeline track 2
            main_page.timeline_select_track(2)

            # Insert Mahoroba.mp3 to timeline
            main_page.select_library_icon_view_media('Mahoroba.mp3')
            insert_result = main_page.tips_area_insert_media_to_selected_track()

            insert_audio = main_page.snapshot(locator=L.timeline_operation.workspace)
            audio_no_update = main_page.compare(after_edit_timeline, insert_audio, similarity=0.98)
            case.result = insert_result and (not audio_no_update)

        # [L49] 2.1 Media Room > My Project > Context menu > Add to tag fine
        with uuid("662a20c0-623c-4131-9a3f-fc76be83780e") as case:
            # Enter My Project
            project_room_page.enter_project_room()
            time.sleep(DELAY_TIME * 2)

            media_room_page.add_new_tag('auto_Testing_project_tag')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media('can_del')
            main_page.right_click()
            check_add_tag = main_page.select_right_click_menu('Add to custom tag', 'auto_Testing_project_tag')

            # DEL the custom tag
            check_delete_tag = media_room_page.right_click_delete_tag('auto_Testing_project_tag', count=1)

            case.result = check_add_tag and check_delete_tag

        # [L56] 2.1 Media Room > Insert clip to timeline & preview > Enable volume meter (form View menu)
        with uuid("520dee77-bb49-428a-8477-dcaf33324820") as case:
            # Enable volume meter
            check_enable = main_page.top_menu_bar_view_show_timeline_preview_volume_meter()

            # select timeline track 2
            main_page.timeline_select_track(2)

            # play music then stop
            playback_window_page.Edit_Timeline_PreviewOperation('play')
            time.sleep(DELAY_TIME*7)
            playback_window_page.Edit_Timeline_PreviewOperation('stop')

            # Disable volume meter
            check_disable = main_page.top_menu_bar_view_show_timeline_preview_volume_meter()
            case.result = check_enable and check_disable

        # [L54] 2.1 Media Room > Insert clip to timeline & preview > Project aspect ratio 9:16
        with uuid("9c2cb23c-3a2d-48f1-8a0a-178e7f0ffbba") as case:
            # enter media content
            media_room_page.enter_media_content()
            time.sleep(DELAY_TIME * 2)

            # New Workspace
            main_page.tap_NewWorkspace_hotkey()
            time.sleep(2)

            # handle (Do you want to save the changes now?)
            main_page.handle_no_save_project_dialog()
            time.sleep(2)

            # Project aspect ratio 9:16
            main_page.set_project_aspect_ratio_9_16()

            # Import Image to library
            media_room_page.import_media_file(Test_Material_Folder + 'Video_Audio_In_Reverse/Sample.png')
            time.sleep(DELAY_TIME * 2)

            # Select Sample.png photo
            main_page.select_library_icon_view_media('Sample.png')

            # Insert to timeline
            main_page.tips_area_insert_media_to_selected_track()
            time.sleep(DELAY_TIME * 2)

            aspect_ratio916_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                         file_name=Auto_Ground_Truth_Folder + 'L54.png')
            time.sleep(DELAY_TIME * 2)
            check_result = main_page.compare(Ground_Truth_Folder + 'L54.png', aspect_ratio916_preview, similarity=0.93)
            case.result = check_result

        # [L55] 2.1 Media Room > Insert clip to timeline & preview > Project aspect ratio 1:1
        with uuid("7a173798-3d3b-45e1-955d-1907aaf3c7dd") as case:
            # New Workspace
            main_page.tap_NewWorkspace_hotkey()
            time.sleep(2)

            # handle (Do you want to save the changes now?)
            main_page.handle_no_save_project_dialog()
            time.sleep(1)

            # Project aspect ratio 1:1
            main_page.set_project_aspect_ratio_1_1()

            # Import Image to library
            media_room_page.import_media_file(Test_Material_Folder + 'Subtitle_Room/JPN.mp4')
            time.sleep(DELAY_TIME * 1.5)

            # Select Sample.png photo
            main_page.select_library_icon_view_media('JPN.mp4')

            # Insert to timeline
            main_page.click(L.main.tips_area.btn_insert_to_selected_track)

            # Handle aspect ratio conflict
            main_page.handle_aspect_ratio_conflict()

            # Set timecode :
            main_page.set_timeline_timecode('00_00_28_03')
            time.sleep(DELAY_TIME * 2)

            aspect_ratio43_preview = main_page.snapshot(locator=main_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'L55.png')
            time.sleep(DELAY_TIME * 2)
            check_result = main_page.compare(Ground_Truth_Folder + 'L55.png', aspect_ratio43_preview)
            case.result = check_result

    # 23 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_12(self):
        main_page.clear_cache()
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*4)
        main_page.set_project_aspect_ratio_16_9()
        time.sleep(DELAY_TIME)

        # Open can_del project
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/can_del.pds')
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

        # Close PDR then re-launch
        main_page.close_and_restart_app()
        time.sleep(DELAY_TIME * 4)

        food_preview = main_page.snapshot(locator=L.base.Area.preview.main)
        # [L27] 2.1 Media Room > Import  > Download fom Stock Content
        with uuid("012b2e9c-9f94-4c7d-a5b2-b771fd5a5912") as case:
            # Open Shutterstock
            media_room_page.import_media_from_shutterstock()
            time.sleep(DELAY_TIME*4)
            getty_image_page.handle_what_is_stock_media()

            # Switch to video tab
            download_from_ss_page.switch_to_video()
            # SS > Search keyword
            time.sleep(DELAY_TIME * 5)
            download_from_ss_page.search.search_text('bubble pink circle')
            time.sleep(7)

            # Tick 3rd thumbnail then click [Download]
            download_from_ss_page.video.select_thumbnail_for_video_intro_designer(3)

            for x in range(70):
                media_room_page.handle_high_definition_dialog()
                if main_page.exist(L.download_from_shutterstock.download.btn_complete_ok):
                    time.sleep(DELAY_TIME * 2)
                    # Click [OK] when pop up download complete
                    download_from_ss_page.download.click_complete_ok()
                    time.sleep(DELAY_TIME * 10)
                    break
                else:
                    time.sleep(DELAY_TIME*2)

            # Leave download page
            getty_image_page.switch_to_GI()

            # download second GI video
            time.sleep(DELAY_TIME * 5)
            download_from_ss_page.search.search_text('pink hand color 23 flower')
            time.sleep(20)

            # Tick 1st thumbnail then click [Download]
            download_from_ss_page.video.select_thumbnail_for_video_intro_designer(1)

            for x in range(100):
                media_room_page.handle_high_definition_dialog()
                if main_page.exist(L.download_from_shutterstock.download.btn_complete_ok):
                    time.sleep(DELAY_TIME * 2)
                    # Click [OK] when pop up download complete
                    download_from_ss_page.download.click_complete_ok()
                    time.sleep(DELAY_TIME * 10)
                    break
                else:
                    time.sleep(DELAY_TIME*2)
            # ----- download complete ------

            # Press [Esc] to close iStock window
            main_page.press_esc_key()

            # Verify Step:
            download_complete_preview = main_page.snapshot(locator=L.base.Area.preview.main)

            check_no_different = main_page.compare(food_preview, download_complete_preview)
            case.result = not check_no_different

        # [L25] 2.1 Media Room > Media Content > Import > Local (File can import correctly by import button)
        with uuid("885259d0-006d-4260-b4ff-90b3f3d7cf7f") as case:
            # Switch to (Media Content) category
            media_room_page.enter_media_content()
            time.sleep(DELAY_TIME)

            # Insert Y man.mp4
            video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Verify Step:
            y_main_preview = main_page.snapshot(locator=L.base.Area.preview.main)

            check_no_different = main_page.compare(y_main_preview, download_complete_preview)
            case.result = not check_no_different

        # [L18] 2.1 Media Room > Enable Library preview window
        with uuid("9bb42cbf-e645-4b01-a9e2-48b2ba9d48d4") as case:
            # Enable Library preview window
            enable_two_preview = main_page.top_menu_bar_view_show_library_preview_window()

            case.result = enable_two_preview

            upper_preview_0_sec = main_page.snapshot(locator=L.library_preview.upper_view_region)

        # [L19] 2.1 Media Room > Library preview window > Playback Controls
        with uuid("8e8d3530-c835-4d09-82d5-7ff0ab10bcf0") as case:
            # Click Play button
            library_preview_page.library_preview_window_preview_operation(0)

            time.sleep(DELAY_TIME)
            # Click Pause button
            library_preview_page.library_preview_window_preview_operation(0)

            time.sleep(DELAY_TIME)
            pause_preview = main_page.snapshot(locator=L.library_preview.upper_view_region)

            # Click Stop button
            library_preview_page.library_preview_window_preview_operation(1)
            stop_preview = main_page.snapshot(locator=L.library_preview.upper_view_region)

            # Verify step
            no_playback = main_page.compare(upper_preview_0_sec, pause_preview, similarity=0.98)
            logger(no_playback)

            check_stop_result = main_page.compare(stop_preview, upper_preview_0_sec)

            case.result = (not no_playback) and check_stop_result

        # [L22] 2.1 Media Room > Library preview window > Undock
        with uuid("d8f210ce-d0dc-4de2-b2bf-3a16f104ca13") as case:
            library_preview_page.library_preview_click_undock()
            undock_library_preview = main_page.snapshot(locator=L.library_preview.upper_view_region)
            logger(undock_library_preview)

            # Verify step
            check_undock_no_change = main_page.compare(undock_library_preview, stop_preview)
            case.result = not check_undock_no_change

        # [L21] 2.1 Media Room > Library preview window > Able to add marker
        with uuid("97c72edd-d447-4142-8e00-80f5a86bb389") as case:
            # Set library timecode
            library_preview_page.set_library_preview_timecode('00_00_07_11')
            time.sleep(DELAY_TIME)

            # Add marker
            library_preview_page.edit_library_preview_window_add_clip_marker()
            time.sleep(DELAY_TIME)
            add_marker_preview = main_page.snapshot(locator=L.library_preview.upper_view_region)

            # Input marker text
            check_marker_result = library_preview_page.edit_library_preview_window_clip_marker_input_text('Test BFT and add marker')
            logger(check_marker_result)

            # Verify Step:
            check_marker_preview = main_page.compare(undock_library_preview, add_marker_preview, similarity=0.98)
            case.result = (not check_marker_preview) and check_marker_result

        # [L20] 2.1 Media Room > Library preview window > Able to Mark in / out then insert timeline
        with uuid("f8b3ffb5-4799-4a41-a42a-a5b8f9fe8800") as case:
            # Set library timecode
            library_preview_page.set_library_preview_timecode('00_00_03_00')
            time.sleep(DELAY_TIME)

            # Click Mark in
            library_preview_page.edit_library_preview_window_click_mark_in()

            # Set library timecode
            library_preview_page.set_library_preview_timecode('00_00_10_07')
            time.sleep(DELAY_TIME)

            # Click Mark out
            library_preview_page.edit_library_preview_window_click_mark_out()

            # Insert to timeline
            library_preview_page.edit_library_preview_window_click_insert_on_selected_track()

            # Verify Step:
            insert_marker_in_out_preview = main_page.snapshot(locator=L.library_preview.upper_view_region)
            logger(insert_marker_in_out_preview)
            check_in_out_no_update = main_page.compare(insert_marker_in_out_preview, add_marker_preview)

            # Click Trim
            tips_area_page.click_TipsArea_btn_Trim(type='video')
            precut_page.edit_precut_switch_trim_mode('Single')
            get_video_duration = precut_page.get_precut_single_trim_duration()
            if get_video_duration == '00:00:07:07':
                check_mark_in_out_result = True
            else:
                check_mark_in_out_result = False
                logger(get_video_duration)
            logger(check_mark_in_out_result)

            # Close Trim window
            precut_page.click_ok()

            case.result = (not check_in_out_no_update) and check_mark_in_out_result

        # [L23] 2.1 Media Room > Library preview window > Minimize window
        with uuid("4cc511f4-4fb7-4de7-8ef0-7982c3305ef9") as case:
            case.result = library_preview_page.library_preview_click_minimize()

        # [L24] 2.1 Media Room > Library preview window > Disable library preview window
        with uuid("5a30f3ff-290d-4179-9e15-06a92a2e3a4d") as case:
            # Click (Show the minimized window)
            library_preview_page.library_preview_show_library_preview()
            time.sleep(DELAY_TIME)

            # Click [Dock] button
            library_preview_page.library_preview_click_dock()
            time.sleep(DELAY_TIME * 3)

            # Click [x] to close (Library preview window)
            case.result = library_preview_page.library_preview_click_close_preview()

        # [L31] 2.1 Media Room > Search > Keyword
        with uuid("5c4130d7-69f4-4fbd-8463-114132f01b92") as case:
            media_room_page.search_library('02')
            time.sleep(DELAY_TIME)

            check_search_result = main_page.select_library_icon_view_media('Travel 02.jpg')
            time.sleep(DELAY_TIME * 1.5)

            # Verify Step:
            travel_02_preview = main_page.snapshot(locator=L.base.Area.preview.main)
            preview_no_update = main_page.compare(travel_02_preview, y_main_preview)
            case.result = check_search_result and (not preview_no_update)

        # [L32] 2.1 Media Room > Search > Cancel search
        with uuid("87f7672e-ca55-4a88-a1fb-3eec037b21d7") as case:
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME*2)

            cancel_search_preview = main_page.snapshot(locator=L.base.Area.preview.main)

            # Verify step:
            check_result = main_page.compare(food_preview, cancel_search_preview)
            case.result = check_result

        # [L33] 2.1 Media Room > Explorer view
        with uuid("44845949-83ed-4c11-97cb-b9d9bcf61d78") as case:
            media_room_page.click_display_hide_explore_view()
            time.sleep(DELAY_TIME*2)

            media_content_category_elem = main_page.exist(L.media_room.tag_media_content)
            if not media_content_category_elem:
                case.result = True
                media_room_page.click_display_hide_explore_view()
            else:
                case.result = False

        # [L34] 2.1 Media Room > Add new tag
        with uuid("db26dc5e-dbbc-4439-b29c-87b426dd4c16") as case:
            case.result = media_room_page.add_new_tag('auto_Testing')

        # [L35] 2.1 Media Room > Modify tag name
        with uuid("01dff930-9d5a-4c98-ad0a-4e2b306b1572") as case:
            case.result = media_room_page.right_click_rename_tag('auto_Testing', 'QADF_testing')

        # [L36] 2.1 Media Room > Tag clip to custom tag
        with uuid("11d4f4e0-284c-4255-b620-baab55eb233b") as case:
            media_room_page.enter_media_content()
            time.sleep(DELAY_TIME*2)
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            case.result = media_room_page.library_clip_context_menu_add_to('QADF_testing')

            # DEL the custom tag
            media_room_page.right_click_delete_tag('QADF_testing', count=1)

        # [L37] 2.1 Media Room > Color Board > Uniform color
        with uuid("c1e06126-1100-45f2-85b5-a2c9ffe9e89b") as case:
            # select timeline track 1
            main_page.timeline_select_track(1)

            # Set timecode :
            main_page.set_timeline_timecode('00_00_10_07')
            time.sleep(DELAY_TIME * 2)

            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME*2)
            media_room_page.library_menu_new_color_board(hex_color='F2E0B7')
            time.sleep(DELAY_TIME*1.5)
            uniform_color_board_preview = main_page.snapshot(locator=main_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'L37.png')
            check_custom_color = main_page.compare(Ground_Truth_Folder + 'L37.png', uniform_color_board_preview)
            case.result = check_custom_color

        # [L39] 2.1 Media Room > Color Board > Insert to timeline and change color
        with uuid("5e96c098-f404-4992-bae7-3b946d2927b5") as case:
            # Insert to timeline
            main_page.tips_area_insert_media_to_selected_track()
            time.sleep(DELAY_TIME)
            current_timeline_preview = main_page.snapshot(locator=main_page.area.preview.main)
            check_custom_color = main_page.compare(Ground_Truth_Folder + 'L37.png', current_timeline_preview)

            # Change color
            tips_area_page.click_TipsArea_btn_ChangeColor('882ECC')

            new_color_preview = main_page.snapshot(locator=main_page.area.preview.main)
            no_change_color = main_page.compare(current_timeline_preview, new_color_preview, similarity=0.98)

            case.result = check_custom_color and (not no_change_color)

        # [L38] 2.1 Media Room > Color Board > Gradient color
        with uuid("894866e2-b166-4edd-baff-ea6e9b856207") as case:
            media_room_page.library_menu_new_gradient_color(hex_color='7028E1')
            title_designer_page.click_custom_name_ok('custom_purple')
            gradient_color_board_preview = main_page.snapshot(locator=main_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'L38.png')
            check_custom_color = main_page.compare(Ground_Truth_Folder + 'L38.png', gradient_color_board_preview)
            case.result = check_custom_color

        # [L40] 2.1 Media Room > Color Board > Insert to timeline and change color
        with uuid("db6ad390-d4fd-4758-ab3a-f0ba4fbf89bc") as case:
            # Insert to timeline
            main_page.tips_area_insert_media_to_selected_track(1)
            time.sleep(DELAY_TIME)
            current_timeline_preview = main_page.snapshot(locator=main_page.area.preview.main)
            check_custom_color = main_page.compare(Ground_Truth_Folder + 'L38.png', current_timeline_preview)

            # Change color
            # Click [Change Color]
            main_page.exist_click(L.tips_area.button.btn_change_color)

            # Handle Gradient color
            media_room_page.handle_color_gradient('2DB727')
            time.sleep(DELAY_TIME*2)

            new_color_preview = main_page.snapshot(locator=main_page.area.preview.main)
            no_change_color = main_page.compare(current_timeline_preview, new_color_preview, similarity=0.9999)
            case.result = check_custom_color and (not no_change_color)

        # [L45] 2.1 Media Room > Downloaded > Downloaded file display correctly
        with uuid("78cdbc6d-29f5-49f6-ade7-0ace8a99fa93") as case:
            media_room_page.enter_downloaded()
            time.sleep(DELAY_TIME * 2)

            # Check SS (Video)
            main_page.select_library_icon_view_media('472764339_fhd')
            main_page.press_space_key()

            # Verify step : Preview is updated
            check_video_preview = main_page.Check_PreviewWindow_is_different(main_page.area.preview.main, sec=5)
            main_page.press_space_key()

            case.result = check_video_preview

        # [L46] 2.1 Media Room > My Project > Open / Save project > Show project thumb after save project
        with uuid("9bec537a-3428-418f-bedb-c1dc1d023bcd") as case:
            # Enter My Project
            project_room_page.enter_project_room()
            check_project_result = main_page.select_library_icon_view_media('can_del')
            case.result = check_project_result

        # [L48] 2.1 Media Room > My Project > Context menu > Open file location correctly
        with uuid("c7470b6b-7f32-4a85-a838-4c29056f3f62") as case:
            main_page.select_library_icon_view_media('can_del')
            time.sleep(DELAY_TIME*0.5)
            case.result = media_room_page.library_clip_context_menu_open_file_location()

        # [L50] 2.1 Media Room > My Project > Context Menu > Delete project
        with uuid("992029d0-3f9e-4b72-b97a-ee36040ad761") as case:
            main_page.select_library_icon_view_media('can_del')
            main_page.right_click()
            case.result = main_page.select_right_click_menu('Remove')

        main_page.select_timeline_media('Y man')
        time.sleep(DELAY_TIME)
        main_page.right_click()
        main_page.select_right_click_menu('Clip Marker', 'Remove All Clip Markers')
        time.sleep(DELAY_TIME)

        # Save project:
        main_page.top_menu_bar_file_save_project_as()
        main_page.handle_save_file_dialog(name='test_case_1_1_12',
                                          folder_path=Test_Material_Folder + 'BFT_21_Stage1/')

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_13(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open project: test_case_1_1_12
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_12.pds')
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

        # [L58] 2.2 Intro Video Room > Template display
        with uuid("5656c3b0-9b2b-499a-bc27-f134bba2dc51") as case:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            intro_video_page.click_intro_specific_category('Beauty')
            time.sleep(DELAY_TIME * 5)
            first_library_preview = main_page.snapshot(locator=main_page.area.preview.main)
            intro_video_page.select_intro_template_method_2(2)
            time.sleep(DELAY_TIME * 1.5)
            second_library_preview = main_page.snapshot(locator=main_page.area.preview.main)
            first_no_change = main_page.compare(first_library_preview, second_library_preview, similarity=0.98)

            # Enter Health
            intro_video_page.click_intro_specific_category('Health')
            time.sleep(DELAY_TIME * 3)
            intro_video_page.select_intro_template_method_2(10)
            time.sleep(DELAY_TIME * 1.5)
            third_library_preview = main_page.snapshot(locator=main_page.area.preview.main)
            second_no_change = main_page.compare(second_library_preview, third_library_preview, similarity=0.98)

            case.result = (not first_no_change) and (not second_no_change)

        # [L59] 2.2 Intro Video Room > Category display
        with uuid("1e6335f3-c46a-4b2a-869a-c9768c44212b") as case:
            # Enter Beauty
            intro_video_page.click_intro_specific_category('Beauty')
            time.sleep(DELAY_TIME * 3)

            # Check Beauty category : 01 ~ 16 template thumbnail
            beauty_template_icon_preview = main_page.snapshot(locator=L.media_room.library_frame)

            # Enter Handwritten
            intro_video_page.click_intro_specific_category('Handwritten')
            time.sleep(DELAY_TIME * 3)
            intro_video_page.select_intro_template_method_2(6)
            time.sleep(DELAY_TIME * 1.5)
            # Check Handwritten category : 01 ~ 16 template thumbnail
            handwritten_template_icon_preview = main_page.snapshot(locator=L.media_room.library_frame)
            template_thumbnail_check = main_page.compare(beauty_template_icon_preview, handwritten_template_icon_preview, similarity=0.98)
            case.result = (not template_thumbnail_check)

            intro_video_page.click_intro_specific_category('Beauty')

        # [L60] 2.2 Intro Video Room > My profile
        with uuid("9f19ce26-268c-4255-9467-033156ceb53f") as case:
            # Open (My Profile)
            intro_video_page.enter_my_profile()
            time.sleep(DELAY_TIME * 10)

            # Verify Step:
            profile_preview = main_page.snapshot(locator=L.intro_video_room.my_profile.main_window, file_name=Auto_Ground_Truth_Folder + 'L60.png')
            check_result = main_page.compare(Ground_Truth_Folder + 'L60.png', profile_preview, similarity=0.8)
            case.result = check_result

            # Close My profile
            main_page.press_esc_key()

        # [L61] 2.2 Intro Video Room > Open Intro Video Designer
        with uuid("eae9c5b2-b7b1-4cc9-99b0-8953963a869a") as case:
            # Input search keyword
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('universer')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Sort by Like
            self.sort_by_like()

            # Select 1st template after search
            intro_video_page.select_intro_template_method_2(1)

            # Click TipsArea button
            tips_area_page.click_TipsArea_btn_insert_project()
            time.sleep(DELAY_TIME * 7)

            # Click Yes if pop up warning (Do you want to edit the template in Video Intro designer?)
            main_page.click(L.main.confirm_dialog.btn_yes)

            # Check open intro template result
            self.check_open_intro_template()

            img_before = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area, file_name=Auto_Ground_Truth_Folder + 'L61_initial.png')

            # Click [Replace BG Media) > Video
            intro_video_page.click_replace_media(1)
            time.sleep(DELAY_TIME)
            main_page.select_file(Test_Material_Folder + 'Produce_Local/4978895.mov')

            # Pop up trim dialog
            if main_page.exist(L.trim.main_window, timeout=10):
                check_trim_result = True
                time.sleep(DELAY_TIME * 5)
                main_page.press_esc_key()
                time.sleep(DELAY_TIME * 5)
            else:
                logger('Verify FAIL')
                check_trim_result = False

            # Verify Step
            current_preview = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area,
                                                   file_name=Auto_Ground_Truth_Folder + 'L61_replace_Video.png')

            check_result = main_page.compare(Ground_Truth_Folder + 'L61_replace_Video.png', current_preview)
            case.result = check_result and check_trim_result

        # Click [Save template]
        intro_video_page.click_btn_save_as(custom_name='Test_save_intro')

        # switch to Title room
        main_page.enter_room(1)
        time.sleep(DELAY_TIME*2)

        # enter Video Intro Room
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 2)

        # [L62] 2.2 Intro Video Room > Add template to timeline > Right click menu
        with uuid("8996d86e-4c16-450e-9863-9e96aebf3400") as case:
            intro_video_page.enter_saved_category()
            time.sleep(DELAY_TIME * 2)
            intro_video_page.select_intro_template_method_2(1)
            main_page.right_click()
            time.sleep(DELAY_TIME)
            main_page.select_right_click_menu('Add to Timeline')

            # handle warning message "Do you want to edit the template in the Video Intro Designer?"
            main_page.click(L.base.confirm_dialog.btn_no)
            time.sleep(DELAY_TIME*5)

            # Verify step:
            # Play timeline preview
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            case.result = main_page.Check_PreviewWindow_is_different(main_page.area.preview.main, sec=4)
            playback_window_page.Edit_Timeline_PreviewOperation('STOP')

        main_page.click_undo()

        # [L63] 2.2 Intro Video Room > Add template to timeline > Tips Area button
        with uuid("0fb947c2-c718-4b81-8bed-7e0a78a84c33") as case:
            # Select 1st template after save template
            intro_video_page.select_intro_template_method_2(1)

            # Click TipsArea button
            tips_area_page.click_TipsArea_btn_insert_project()
            time.sleep(DELAY_TIME*7)

            # handle warning message "Do you want to edit the template in the Video Intro Designer?"
            main_page.click(L.base.confirm_dialog.btn_no)
            time.sleep(DELAY_TIME*5)

            # Set timecode
            main_page.set_timeline_timecode('00_00_07_00')
            time.sleep(DELAY_TIME * 2)

            current_timeline = main_page.snapshot(locator=main_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'L63.png')
            check_result = main_page.compare(Ground_Truth_Folder + 'L63.png', current_timeline)
            case.result = check_result

            # Set timecode
            main_page.set_timeline_timecode('00_00_00_00')
            time.sleep(DELAY_TIME * 2)

            # Save project:
            main_page.top_menu_bar_file_save_project_as()
            main_page.handle_save_file_dialog(name='test_case_1_1_13',
                                              folder_path=Test_Material_Folder + 'BFT_21_Stage1/')

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_14(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open Preference > Editing > Set default Title duration to 10 (For v21.6.5303 PM request)
        main_page.click_set_user_preferences()
        time.sleep(DELAY_TIME * 2)
        preferences_page.switch_to_editing()
        time.sleep(DELAY_TIME)
        preferences_page.editing.durations_title_set_value('10.0')
        time.sleep(DELAY_TIME * 3)
        preferences_page.click_ok()
        time.sleep(DELAY_TIME)

        # Open project: test_case_1_1_13
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_13.pds')
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

        # Set timecode
        main_page.set_timeline_timecode('00_00_27_07')
        time.sleep(DELAY_TIME * 2)

        # [L73] 2.3 Title Room > Designer Entry > Modify Title template
        with uuid("2e04cf5c-c013-4165-97b5-30463bf82f88") as case:
            # switch to Title room
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 2)

            # Input search Windshield
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Windshield')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Insert to timeline
            main_page.select_library_icon_view_media('Windshield')
            main_page.tips_area_insert_media_to_selected_track()

            # Click [Designer]
            main_page.tips_area_click_designer()

            # Switch to express mode / basic mode : Mode=1
            title_designer_page.switch_mode()
            time.sleep(DELAY_TIME * 2)

            # Edit selected object on canvas
            canvas_elem = main_page.exist(L.title_designer.area.frame_video_preview)
            main_page.mouse.click(*canvas_elem.center)
            main_page.double_click()
            title_designer_page.edit_object_title('恭ぱ囧＠')
            time.sleep(DELAY_TIME*4)

            # Verify step
            check_selected_object = title_designer_page.get_title_text_content()
            if check_selected_object == '恭ぱ囧＠':
                first_row_result = True
            else:
                first_row_result = False

            # Set text string to Two line
            title_text_elem = main_page.exist(L.title_designer.area.edittext_text_content)
            main_page.mouse.click(*title_text_elem.center)
            main_page.press_enter_key()
            main_page.input_text('ｶﾞヂョたりポｶﾞ')

            # Verify preview 1
            windshield_designer_preview = main_page.snapshot(locator=L.title_designer.area.frame_video_preview, file_name=Auto_Ground_Truth_Folder + 'L73.png')
            check_edit_result = main_page.compare(Ground_Truth_Folder + 'L73.png', windshield_designer_preview)
            logger(check_edit_result)

            # Click [OK] to leave title designer
            title_designer_page.click_ok()

            # Click [Play]
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            check_animation_result = main_page.Check_PreviewWindow_is_different(main_page.area.preview.main, sec=2.5)
            playback_window_page.Edit_Timeline_PreviewOperation('STOP')

            case.result = first_row_result and check_edit_result and check_animation_result

        # Set timecode
        main_page.set_timeline_timecode('00_00_37_07')
        time.sleep(DELAY_TIME * 2)

        # [L65] 2.3 Title Room > Add Built-In templates to timeline & Preview >  Motion Graphic 007, Clover_04, Windshield
        with uuid("e99fa28d-f1cd-4d28-8a93-acb64c81441b") as case:
            # 2023/04/24: Cannot find Clover_04 on v21.6.5221
            # Enter Credit category
            #main_page.select_LibraryRoom_category('Credits/Scroll')

            # Insert Clover_04 to timeline
            #main_page.select_library_icon_view_media('Clover_04')
            #main_page.tips_area_insert_media_to_selected_track()

            # Click track3
            main_page.timeline_select_track(3)

            # Enter MGT category
            main_page.select_LibraryRoom_category('Motion Graphics')

            # Insert Clover_04 to timeline
            main_page.select_library_icon_view_media('Motion Graphics 007')
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode (Clip mode)
            main_page.set_timeline_timecode('00_00_06_16')
            time.sleep(DELAY_TIME * 2)

            build_in_title_preview = main_page.snapshot(locator=main_page.area.preview.main,
                                                             file_name=Auto_Ground_Truth_Folder + 'L65.png')
            case.result = main_page.compare(Ground_Truth_Folder + 'L65.png', build_in_title_preview)

        playback_window_page.Edit_Timeline_PreviewOperation('STOP')

        # [L69] 2.3 Title Room > Add Built-In templates to timeline & Preview >  Maple
        with uuid("b8589cce-cb99-4c02-8edd-bb81daf86604") as case:
            # switch to Particle room
            main_page.enter_room(5)
            time.sleep(DELAY_TIME * 2)

            # Input search Maple
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Maple')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Click track 2
            main_page.timeline_select_track(2)

            # Insert to timeline
            main_page.select_library_icon_view_media('Maple')
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode (Clip mode)
            main_page.set_timeline_timecode('00_00_02_28')
            time.sleep(DELAY_TIME * 2)

            build_in_particle_preview = main_page.snapshot(locator=main_page.area.preview.main,
                                                             file_name=Auto_Ground_Truth_Folder + 'L69.png')
            case.result = main_page.compare(Ground_Truth_Folder + 'L69.png', build_in_particle_preview)

        # [L76] 2.3 Particle Room > Designer Entry > Modify Particle template
        with uuid("54220852-77ba-4003-87cb-b106f9afcb51") as case:
            for x in range(3):
                # Click [Designer]
                main_page.tips_area_click_designer(check_designer=2)

                # Set Size
                particle_designer_page.express_mode.drag_Size_slider(186283)

                # Click ok
                particle_designer_page.click_OK()

            time.sleep(DELAY_TIME*3)
            edit_particle_preview = main_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'L76.png')
            case.result = main_page.compare(Ground_Truth_Folder + 'L76.png', edit_particle_preview)

        # [L67] 2.3 Add build-in template to timeline > Effect : back light, Analog film
        with uuid("97b588be-0e89-402e-9bda-259f71152dd7") as case:
            # Click trac 1
            main_page.timeline_select_track(1)
            playback_window_page.Edit_Timeline_PreviewOperation('STOP')

            # switch to Effect room
            main_page.enter_room(3)
            time.sleep(DELAY_TIME * 2)

            # Input search Analog
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Analog')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Analog Film')

            main_page.set_timeline_timecode('00_00_04_10')
            time.sleep(DELAY_TIME * 2)
            analog_preview = main_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'L67_analog.png')
            build_in_effect_1_result = main_page.compare(Ground_Truth_Folder + 'L67_analog.png', analog_preview)
            logger(build_in_effect_1_result)

            # Enter All Content category
            main_page.select_LibraryRoom_category('All Content')

            # Click Undo
            main_page.click_undo()

            # Input search Back
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Back')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Back Light')

            main_page.set_timeline_timecode('00_00_04_10')
            time.sleep(DELAY_TIME * 2)
            back_preview = main_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'L67_back.png')
            build_in_effect_2_result = main_page.compare(Ground_Truth_Folder + 'L67_back.png', back_preview)
            logger(build_in_effect_2_result)

            case.result = build_in_effect_1_result and build_in_effect_2_result

        main_page.set_timeline_timecode('00_00_00_00')
        time.sleep(DELAY_TIME * 2)

        # Save project:
        main_page.top_menu_bar_file_save_project_as()
        main_page.handle_save_file_dialog(name='test_case_1_1_14',
                                          folder_path=Test_Material_Folder + 'BFT_21_Stage1/')

    # 4 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_15(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open project: test_case_1_1_13
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_14.pds')
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

        # [L41] 2.1 Media Room > Background Music / Sound Clips > Sample preview
        with uuid("e071a716-a769-4153-9d27-98d183a98f31") as case:
            # Enter Background Music
            media_room_page.enter_background_music()

            # BGM search "Hey Baby"
            media_room_page.search_library('Hey Baby')
            time.sleep(DELAY_TIME * 2)

            # check default is (not download)
            check_default = media_room_page.background_music_check_download_mark('Hey Baby (Your Lullaby Song)')
            logger(check_default)

            # select clip
            media_room_page.sound_clips_select_media('Hey Baby (Your Lullaby Song)')
            time.sleep(DELAY_TIME*2)

            # Verify Step by check timecode
            # Click [Play]
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME*4)
            main_page.press_space_key()

            current_timecode = playback_window_page.get_timecode_slidebar()
            logger(current_timecode)
            if current_timecode != '00:00:00:00':
                case.result = True
            else:
                case.result = False

        # [L42] 2.1 Media Room > Background Music / Sound Clips > Download
        with uuid("bf802ba9-50a6-4def-90a3-026036090f5a") as case:
            media_room_page.sound_clips_select_media('Hey Baby (Your Lullaby Song)')
            time.sleep(DELAY_TIME * 2)
            main_page.right_click()
            time.sleep(DELAY_TIME)
            main_page.select_right_click_menu('Download')
            time.sleep(DELAY_TIME * 8)
            check_download_icon = media_room_page.background_music_check_download_mark('Hey Baby (Your Lullaby Song)')
            case.result = check_download_icon

        # [L43] 2.1 Media Room > Background Music / Sound Clips > Timeline preview
        with uuid("a29435e4-7b6a-4942-abfd-1a57ec862f6a") as case:
            download_bgm_preview = main_page.snapshot(locator=main_page.area.preview.main)

            # Insert to timeline
            main_page.tips_area_insert_media_to_selected_track()
            time.sleep(DELAY_TIME*3)
            after_insert_preview = main_page.snapshot(locator=main_page.area.preview.main)
            check_result = not main_page.compare(download_bgm_preview, after_insert_preview)
            case.result = check_result

        # [L44] 2.1 Media Room > Background Music / Sound Clips > Delete from Disk
        with uuid("8312130f-2873-4609-8cb7-4b4ed2dd3cc9") as case:
            # Click Undo (no insert BGM)
            main_page.click_undo()

            # Delete BGM from disk
            media_room_page.sound_clips_select_media('Hey Baby (Your Lullaby Song)')
            time.sleep(DELAY_TIME * 2)
            main_page.right_click()
            time.sleep(DELAY_TIME)
            main_page.select_right_click_menu('Delete from Disk')
            main_page.exist_click(L.media_room.confirm_dialog.btn_yes)
            time.sleep(DELAY_TIME * 3)
            # Download mark should become default status
            bgm_del_result = not main_page.is_exist(L.media_room.scroll_area.table_view_text_field_download_ok)
            logger(bgm_del_result)

            # Enter Sound Clips
            media_room_page.enter_sound_clips()
            time.sleep(DELAY_TIME*8)

            # Sound clip search "2400Hz"
            media_room_page.search_SFX_library('2400Hz')
            time.sleep(DELAY_TIME * 2)

            media_room_page.sound_clips_select_media('2400Hz Noise')
            time.sleep(DELAY_TIME * 2)
            main_page.right_click()
            time.sleep(DELAY_TIME)
            main_page.select_right_click_menu('Download')
            time.sleep(DELAY_TIME * 5)
            sound_download_icon = media_room_page.background_music_check_download_mark('2400Hz Noise')

            # Delete Sound clip
            media_room_page.sound_clips_select_media('2400Hz Noise')
            time.sleep(DELAY_TIME * 2)
            main_page.right_click()
            time.sleep(DELAY_TIME)
            main_page.select_right_click_menu('Delete from Disk')
            main_page.exist_click(L.media_room.confirm_dialog.btn_yes)
            time.sleep(DELAY_TIME * 3)
            sound_del_result = not main_page.is_exist(L.media_room.scroll_area.table_view_text_field_download_ok)
            logger(sound_del_result)

            case.result = bgm_del_result and sound_download_icon and sound_del_result

    # 4 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_16(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open project: test_case_1_1_13
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_14.pds')
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

        # Set timecode
        main_page.set_timeline_timecode('00_00_47_07')
        time.sleep(DELAY_TIME * 2)

        # [L68] 2.3 Pip Room > Shape 017, Dialog_07, Wedding_2
        with uuid("c805bedd-ee5f-4a40-9476-be67a8c75ccb") as case:
            # 2023/04/24 update: Dialog_07 can NOT find on v21.6.5221

            # Enter Pip Room
            main_page.enter_room(4)

            # Input search Shape 017
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Shape 017')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Insert to timeline (Track 1)
            main_page.tips_area_insert_media_to_selected_track()

            # Clear search
            media_room_page.search_library_click_cancel()

            # select timeline track 2
            main_page.timeline_select_track(2)

            # Input search Wedding 2
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Wedding')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Insert to timeline (Track 2)
            main_page.tips_area_insert_media_to_selected_track()

            # Clear search
            media_room_page.search_library_click_cancel()

            # select timeline track 2
            main_page.timeline_select_track(2)

            # Set timecode
            main_page.set_timeline_timecode('00_00_50_07')
            time.sleep(DELAY_TIME * 2)

            # Input search Dialog_07
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Mood')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Insert to timeline (Track 2)
            main_page.select_library_icon_view_media('Mood Stickers 07')
            time.sleep(DELAY_TIME * 6)
            main_page.right_click()
            main_page.select_right_click_menu('Add to Timeline')

            # select timeline track 1
            main_page.timeline_select_track(1)

            # Click [Previous Frame]
            for x in range(3):
                playback_window_page.Edit_Timeline_PreviewOperation('previous_frame')
                time.sleep(DELAY_TIME * 0.5)

            time.sleep(DELAY_TIME * 2)
            shape_wedding_preview = main_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'L68_shape_wedding.png')
            shape_wedding_result = main_page.compare(Ground_Truth_Folder + 'L68_shape_wedding.png', shape_wedding_preview)

            # Click [Next Frame]
            for x in range(5):
                playback_window_page.Edit_Timeline_PreviewOperation('next_frame')
                time.sleep(DELAY_TIME * 0.5)

            time.sleep(DELAY_TIME * 2)
            shape_dialog_preview = main_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'L68_shape_dialog.png')
            shape_dialog_result = main_page.compare(Ground_Truth_Folder + 'L68_shape_dialog.png', shape_dialog_preview)

            case.result = shape_wedding_result and shape_dialog_result

        # [L75] 2.3 Pip Room > Designer entry > Shape template can modify (Shape 017)
        with uuid("b9ad4619-839d-438a-8293-eaeaf66f5479") as case:
            # Select timeline media
            main_page.select_timeline_media('Shape 017')

            # select tips area : Tools > Shape Designer
            main_page.tap_TipsArea_Tools_menu(0)

            # Check is enter shape designer
            enter_shape_designer = shape_designer_page.check_in_shape_designer()
            if not enter_shape_designer:
                case.result = False
                logger('Cannot enter shape designer')

            # Unfold Shape preset
            shape_designer_page.properties.unfold_shape_preset(1)
            time.sleep(DELAY_TIME*2)

            # Apply Shape preset
            shape_designer_page.properties.shape_preset.apply_preset(3)
            time.sleep(DELAY_TIME * 2)

            # Fold Shape preset
            shape_designer_page.properties.unfold_shape_preset(0)
            time.sleep(DELAY_TIME * 2)

            # Unfold Shape Fill
            shape_designer_page.properties.unfold_shape_fill(1)
            time.sleep(DELAY_TIME * 2)

            # Apply Shape Fill > Uniform Color
            shape_designer_page.properties.shape_fill.set_uniform_color('7E1208')

            # Fold Shape Fill
            shape_designer_page.properties.unfold_shape_fill(0)
            time.sleep(DELAY_TIME * 2)

            # Click [OK] to leave shape designer
            shape_designer_page.click_ok()
            time.sleep(DELAY_TIME * 2)

            # select timeline track 2
            main_page.timeline_select_track(2)

            # Click [Previous Frame]
            for x in range(4):
                playback_window_page.Edit_Timeline_PreviewOperation('previous_frame')
                time.sleep(DELAY_TIME * 0.5)

            time.sleep(DELAY_TIME * 2)
            shape_edit_preview = main_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'L75.png')
            check_result = main_page.compare(Ground_Truth_Folder + 'L75.png', shape_edit_preview, similarity=0.9)

            case.result = check_result

        # [L74] 2.3 Pip Room > Designer entry > Pip template can modify (Wedding 2)
        with uuid("8b400e01-576b-4297-a1e2-af05377bf860") as case:
            # Select timeline media
            main_page.select_timeline_media('Wedding 2')

            # select tips area : Tools > enter Pip Designer
            main_page.tap_TipsArea_Tools_menu(0)
            time.sleep(DELAY_TIME * 2)

            # Switch to Express mode
            pip_designer_page.switch_mode('Express')

            # Set Border checkbox = 1 (auto unfold Border menu)
            pip_designer_page.apply_border()
            time.sleep(DELAY_TIME * 2)

            # Set Border size = 4
            pip_designer_page.drag_border_size_slider(4)
            time.sleep(DELAY_TIME)

            # Set Border > color to 47C62D
            pip_designer_page.apply_border_uniform_color('71', '198', '45')

            # Fold Border menu
            main_page.click(L.pip_designer.border.border)
            time.sleep(DELAY_TIME * 2)

            # Set Shadow checkbox = 1 (auto unfold Shadow menu)
            pip_designer_page.apply_shadow()
            time.sleep(DELAY_TIME * 2)

            # Set Shadow distance
            pip_designer_page.drag_shadow_distance_slider(83)
            time.sleep(DELAY_TIME)

            # Set Shadow color
            pip_designer_page.select_shadow_color('194', '245', '124')

            # Fold Border menu
            main_page.click(L.pip_designer.shadow.shadow)
            time.sleep(DELAY_TIME * 2)

            # Click [OK] to leave pip designer
            pip_designer_page.click_ok()
            time.sleep(DELAY_TIME * 2)

            weddig_edit_preview = main_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'L74.png')
            check_result = main_page.compare(Ground_Truth_Folder + 'L74.png', weddig_edit_preview)

            case.result = check_result

        # [L66] 2.3 Transition Room > Binary 1
        with uuid("8d6fe590-d4af-4ac4-8e7d-e7e4295d4a17") as case:
            # Enter Transition Room
            main_page.enter_room(2)

            # Input search Binary 1  ---------
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Binary 1')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Insert (Binary 1) to (Wedding 2) and (Dialog_07)
            main_page.drag_transition_to_timeline_clip('Binary 1', 'Mood Stickers 07')

            main_page.set_timeline_timecode('00_00_00_28')
            time.sleep(DELAY_TIME * 2)

            binary_1_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                        file_name=Auto_Ground_Truth_Folder + 'L66_binary.png')
            check_result_01 = main_page.compare(Ground_Truth_Folder + 'L66_binary.png', binary_1_preview, similarity=0.9)

            # Click undo
            main_page.click_undo()

            # Cancel search
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME * 2)

            # Input search Blur  ---------
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Blur')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Insert (Blur) to (Wedding 2) and (Dialog_07)
            main_page.drag_transition_to_timeline_clip('Blur', 'Mood Stickers 07')

            main_page.set_timeline_timecode('00_00_00_17')
            time.sleep(DELAY_TIME * 2)

            blur_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                        file_name=Auto_Ground_Truth_Folder + 'L66_blur.png')
            check_result_02 = main_page.compare(Ground_Truth_Folder + 'L66_blur.png', blur_preview)

            # Click undo
            main_page.click_undo()

            # Cancel search
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME * 2)

            # Input search Brush Transition 01  ---------
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('brush strokes 01')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Insert (Brush Transition 01) to (Wedding 2) and (Dialog_07)
            main_page.drag_transition_to_timeline_clip('Brush Strokes 01', 'Mood Stickers 07')

            main_page.set_timeline_timecode('00_00_00_28')
            time.sleep(DELAY_TIME * 2)

            binary_1_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                  file_name=Auto_Ground_Truth_Folder + 'L66_brush_01.png')
            check_result_03 = main_page.compare(Ground_Truth_Folder + 'L66_brush_01.png', binary_1_preview)

            # Click undo
            main_page.click_undo()

            # Cancel search
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME * 2)

            # Input search Cross 2 ---------
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Cross 2')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Insert (Cross 2) to (Wedding 2) and (Dialog_07)
            main_page.drag_transition_to_timeline_clip('Cross 2', 'Mood Stickers 07')

            main_page.set_timeline_timecode('00_00_00_13')
            time.sleep(DELAY_TIME * 2)

            cross_2_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                  file_name=Auto_Ground_Truth_Folder + 'L66_cross.png')
            check_result_04 = main_page.compare(Ground_Truth_Folder + 'L66_cross.png', cross_2_preview)

            # Click undo
            main_page.click_undo()

            # Cancel search
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME * 2)

            # Input search Magnify ---------
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('magnify')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Insert (Magnify) to (Wedding 2) and (Dialog_07)
            main_page.drag_transition_to_timeline_clip('Magnify', 'Mood Stickers 07')

            main_page.set_timeline_timecode('00_00_01_00')
            time.sleep(DELAY_TIME * 2)

            magnify_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                  file_name=Auto_Ground_Truth_Folder + 'L66_magnify.png')
            check_result_05 = main_page.compare(Ground_Truth_Folder + 'L66_magnify.png', magnify_preview)

            # Cancel search
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME * 2)

            # Click undo
            main_page.click_undo()

            # Input search Disturbance ---------
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Disturbance')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Insert (Magnify) to (Wedding 2) and (Dialog_07)
            main_page.drag_transition_to_timeline_clip('Disturbance', 'Mood Stickers 07')

            main_page.set_timeline_timecode('00_00_00_27')
            time.sleep(DELAY_TIME * 5)

            disturbance_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                  file_name=Auto_Ground_Truth_Folder + 'L66_disturbance.png')
            check_result_06 = main_page.compare(Ground_Truth_Folder + 'L66_disturbance.png', disturbance_preview, similarity=0.7)

            case.result = check_result_01 and check_result_02 and check_result_03 and check_result_04 and check_result_05 and check_result_06

        # Save project:
        main_page.top_menu_bar_file_save_project_as()
        main_page.handle_save_file_dialog(name='test_case_1_1_16',
                                          folder_path=Test_Material_Folder + 'BFT_21_Stage1/')

    # 9 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_17(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open project: test_case_1_1_16
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_16.pds')
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

        main_page.set_timeline_timecode('00_00_57_07')
        time.sleep(DELAY_TIME * 2)

        # [L71] 2.3 Transition / Effect / Particle Room > IAD: Transition, Effect, Particle
        with uuid("0941636d-0f13-4fbf-baa8-e2725af12a32") as case:
            # Enter Particle Room
            main_page.enter_room(5)
            time.sleep(DELAY_TIME * 2)
            # Enter All Content category
            main_page.select_LibraryRoom_category('All Content')

            # Input search Instant Memories ---------
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Comic Style 06')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Download IAD: Instant Memories
            main_page.select_library_icon_view_media('Comic Style 06')
            time.sleep(DELAY_TIME * 5)

            # Insert (Instant Memories) to track 1
            main_page.drag_media_to_timeline_playhead_position('Comic Style 06', track_no=1)

            # Enter Transition Room ---------
            main_page.enter_room(2)
            time.sleep(DELAY_TIME * 2)

            # Input search Snow 03 ---------
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Snow 03')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Download IAD: Instant Memories
            main_page.select_library_icon_view_media('Snow 03')
            time.sleep(DELAY_TIME * 5)

            # Insert Transition (Snow 03) to (Dialog_07) and (Instant Memories)
            main_page.drag_transition_to_timeline_clip('Snow 03', 'Comic Style 06')

            main_page.set_timeline_timecode('00_00_00_27')
            time.sleep(DELAY_TIME * 2)

            transition_IAD_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                  file_name=Auto_Ground_Truth_Folder + 'L71_transition_IAD.png')
            check_result_01 = main_page.compare(Ground_Truth_Folder + 'L71_transition_IAD.png', transition_IAD_preview, similarity=0.9)


            # select timeline track 1
            main_page.timeline_select_track(1)

            main_page.set_timeline_timecode('00_00_00_00')
            time.sleep(DELAY_TIME * 2)

            # Select timeline media
            main_page.select_timeline_media('4978895')
            time.sleep(DELAY_TIME * 3)

            # If exist Effect button
            effect_button = main_page.exist(L.tips_area.button.btn_effect_modify)
            if effect_button:
                tips_area_page.click_TipsArea_btn_effect()
                time.sleep(DELAY_TIME * 2)
                effect_room_page.remove_from_effectsettings()
                time.sleep(DELAY_TIME)

            # Enter Effect Room ---------
            main_page.enter_room(3)
            time.sleep(DELAY_TIME * 2)

            # Input search lens flare 40 ---------
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('lens flare 40')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Download IAD: Lens Flare 40
            main_page.select_library_icon_view_media('Lens Flare 40')
            time.sleep(DELAY_TIME * 5)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 40')
            time.sleep(DELAY_TIME * 3)

            effect_IAD_preview = main_page.snapshot(locator=main_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'L71_flare_40.png')
            check_result_02 = main_page.compare(Ground_Truth_Folder + 'L71_flare_40.png', effect_IAD_preview, similarity=0.9)

            case.result = check_result_01 and check_result_02

        # [L72] 2.3 Effect Room > Import LUT Effect
        with uuid("5e5419f2-bdb1-4664-933c-753b9c640682") as case:
            effect_room_page.import_CLUTs(Test_Material_Folder + 'BFT_21_Stage1/3dl_1.3dl')
            time.sleep(DELAY_TIME*2)

            # Apply LUT (3dl_1.3dl) to timeline
            main_page.drag_media_to_timeline_playhead_position('3dl_1')
            time.sleep(DELAY_TIME * 2)

            lut_3dl_preview = main_page.snapshot(locator=main_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'L72_3dl.png')
            case.result = main_page.compare(Ground_Truth_Folder + 'L72_3dl.png', lut_3dl_preview)

            # Select 3dl_1 > Right click menu > Delete
            main_page.select_library_icon_view_media('3dl_1')
            time.sleep(DELAY_TIME)
            main_page.right_click()
            time.sleep(DELAY_TIME)
            main_page.select_right_click_menu('Delete')
            time.sleep(DELAY_TIME * 2)

            # handle warning message (The CLUT  will be delete ... Do you want to continue?)
            main_page.click(L.base.confirm_dialog.btn_yes)
            time.sleep(DELAY_TIME*5)

        # [L78] 2.4 Audio Mixing Room > Audio Track
        with uuid("dc590d38-160a-45f3-9b96-43d43a6986e7") as case:
            # Verify step: Check can add audio track with option "Above track 4"
            check_result = timeline_operation_page.set_add_tracks_audio(number=1, position='Above track 4')

            if check_result:
                main_page.click_undo()

            case.result = check_result
        # enter media room > select audio "Speaking Out.mp3" insert to timeline track 3
        # Enter media room
        main_page.click(L.main.room_entry.btn_media_room)
        time.sleep(DELAY_TIME * 2)
        main_page.timeline_select_track(3)
        time.sleep(DELAY_TIME * 2)
        main_page.drag_media_to_timeline_playhead_position('Skateboard 02.mp4', track_no=3)

        # [L79] 2.4 Audio Mixing Room > Video volume slider
        with uuid("5dc76d24-9097-4bfb-84bf-33b2e2df86f9") as case:
            # Enter Audio Mixing Room
            main_page.enter_room(6)
            time.sleep(DELAY_TIME *3)

            audio_3_volume_elem = audio_mixing_room_page.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': 2}, {'AXRole': 'AXValueIndicator', 'AXRoleDescription': 'value indicator'}])
            # If cannot find volume elem
            if not audio_3_volume_elem:
                raise Exception

            # Default volume value
            default_volume = audio_3_volume_elem.AXValue

            # Default volume meter preview
            audio_3_library_track = main_page.exist({'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': 2})
            audio_default_preview = main_page.snapshot(locator=audio_3_library_track)
            logger(audio_default_preview)

            # Mouse drag volume object ( Volume preview will update)
            ori_pos = audio_3_volume_elem.AXPosition
            size_w, size_h = audio_3_volume_elem.AXSize
            initial_pos = (ori_pos[0] + size_w * 0.5, ori_pos[1])
            target_pos = (ori_pos[0] + size_w * 0.5, ori_pos[1] - 150)
            main_page.drag_mouse(initial_pos, target_pos)
            time.sleep(DELAY_TIME*2)

            # Verify step:
            audio_3_volume_elem = audio_mixing_room_page.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': 2}, {'AXRole': 'AXValueIndicator', 'AXRoleDescription': 'value indicator'}])
            current_volume = audio_3_volume_elem.AXValue
            if current_volume > default_volume:
                case.result = True
                logger(current_volume)
            else:
                case.result = False
                logger(current_volume)

        # [L80] 2.4 Audio Mixing Room > Volume meter (meter should change during preview)
        with uuid("ca19991d-00ba-40a9-b678-06b0b0958b76") as case:
            audio_current_preview = main_page.snapshot(locator=audio_3_library_track)
            logger(audio_current_preview)

            check_volume_result = not main_page.compare(audio_default_preview, audio_current_preview)
            case.result = check_volume_result

        # [L83] 2.4 Audio Mixing Room > Volume meter > Stereo
        with uuid("af992c16-22d9-4e4e-a784-202d9c43865a") as case:
            audio_3_library_track = main_page.exist({'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': 2})
            stereo_preview = main_page.snapshot(locator=audio_3_library_track, file_name=Auto_Ground_Truth_Folder + 'L83.png')
            case.result = main_page.compare(Ground_Truth_Folder + 'L83.png', stereo_preview, similarity=0.9)

        # [L81] 2.4 Audio Mixing Room > Audio gain slider
        with uuid("c5e2a175-7f66-449a-b69f-1e3732b79e07") as case:
            default_gain = audio_mixing_room_page.get_audio_gain(3)
            time.sleep(DELAY_TIME)
            logger(default_gain)
            if default_gain == 50:
                check_default_result = True
            else:
                check_default_result = False

            audio_mixing_room_page.set_audio_gain(audio_no=3, value=80)
            time.sleep(DELAY_TIME)
            current_gain = audio_mixing_room_page.get_audio_gain(3)
            time.sleep(DELAY_TIME)
            if current_gain == 80:
                apply_result = True
            else:
                apply_result = False

            case.result = check_default_result and apply_result

        # [L82] 2.4 Audio Mixing Room > Fade in / Fade out
        with uuid("c7dd410d-3535-49c3-886b-adeec61f0859") as case:
            main_page.set_timeline_timecode('00_00_03_23')
            time.sleep(DELAY_TIME * 2)

            # Apply fade in / out on Audio track 3
            audio_3_library_track = main_page.exist({'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': 2})
            before_fade_in_out = main_page.snapshot(locator=audio_3_library_track, file_name=Auto_Ground_Truth_Folder + 'L82_before.png')
            time.sleep(DELAY_TIME* 2)
            check_fade_in = audio_mixing_room_page.click_fade_in(3)
            after_fade_in = main_page.snapshot(locator=audio_3_library_track,
                                                    file_name=Auto_Ground_Truth_Folder + 'L82_fade_in.png')

            check_fade_out = audio_mixing_room_page.click_fade_out(3)
            time.sleep(DELAY_TIME*2)
            after_fade_in_out = main_page.snapshot(locator=audio_3_library_track,
                                                    file_name=Auto_Ground_Truth_Folder + 'L82_after.png')

            check_fade_in_preview = not main_page.compare(before_fade_in_out, after_fade_in)
            check_preview = main_page.compare(before_fade_in_out, after_fade_in_out)
            case.result = check_fade_in and check_fade_out and check_fade_in_preview and check_preview

        # [L85] 2.4 Audio Mixing Room > Add / Remove/ Switch keyframe
        with uuid("ef413972-48da-4380-8c0f-e9530174271a") as case:
            # Click next keyframe
            audio_mixing_room_page.click_next_keyframe(3)
            time.sleep(DELAY_TIME)

            # Get current timecode
            current_timecode = playback_window_page.get_timecode_slidebar()
            if current_timecode == '00:00:10:00':
                check_next_keyframe = True
            else:
                check_next_keyframe = False
            logger(check_next_keyframe)

            # Click previous keyframe
            audio_mixing_room_page.click_previous_keyframe(3)
            time.sleep(DELAY_TIME)

            # Get current timecode
            current_timecode = playback_window_page.get_timecode_slidebar()
            if current_timecode == '00:00:05:23':
                check_previous_keyframe = True
            else:
                check_previous_keyframe = False
            logger(check_previous_keyframe)

            # Click (remove keyframe)
            audio_mixing_room_page.click_keyframe_control(3)
            time.sleep(DELAY_TIME)

            audio_mixing_room_page.click_next_keyframe(3)
            time.sleep(DELAY_TIME)
            audio_mixing_room_page.click_previous_keyframe(3)
            time.sleep(DELAY_TIME)

            # Get current timecode
            current_timecode = playback_window_page.get_timecode_slidebar()
            if current_timecode == '00:00:03:23':
                check_remove_keyframe = True
            else:
                check_remove_keyframe = False
            logger(check_remove_keyframe)


            case.result = check_previous_keyframe and check_next_keyframe and check_remove_keyframe

        # Remove timeline track3 clip: skateboard 02.mp4
        main_page.select_timeline_media('Skateboard 02')
        tips_area_page.more_features.remove(index=1)

        # Click [Stop] button
        playback_window_page.Edit_Timeline_PreviewOperation('STOP')
        time.sleep(DELAY_TIME)

        # Save project:
        main_page.top_menu_bar_file_save_project_as()
        main_page.handle_save_file_dialog(name='test_case_1_1_17',
                                          folder_path=Test_Material_Folder + 'BFT_21_Stage1/')

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_18(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Clear old capture file: Capture.m4a
        main_page.clear_capture_file()

        # [L84] 2.4 Audio Mixing Room > Volume meter > 5.1 Surround
        with uuid("0777102c-fc09-474d-b4bf-07a85ca9cfb2") as case:

            # Import video w/ 5.1 channel audio
            video_path = Test_Material_Folder + 'Crop_Zoom_Pan/AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov'
            media_room_page.import_media_file(video_path)
            time.sleep(DELAY_TIME * 2)
            media_room_page.handle_high_definition_dialog()

            # media room current preview
            l84_preview = main_page.snapshot(L.base.Area.library_icon_view)

            # Open Preference setting > General > Audio channel > Set 5.1 Surround
            main_page.click_set_user_preferences()
            time.sleep(DELAY_TIME * 2)
            preferences_page.general.audio_channels_set_51_surround()
            time.sleep(DELAY_TIME)

            # Click OK to close (Preference setting)
            preferences_page.click_ok()

            # Insert 6ch video to timeline to timeline (Track 1)
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Audio Mixing Room
            main_page.enter_room(6)
            time.sleep(DELAY_TIME *3)

            main_page.set_timeline_timecode('00_01_11_04')
            time.sleep(DELAY_TIME * 3)

            audio_1_library_track = main_page.exist({'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': 0})
            audio_track_1_library_preview = main_page.snapshot(locator=audio_1_library_track, file_name=Auto_Ground_Truth_Folder + 'L84_6ch_track.png')
            case.result = main_page.compare(Ground_Truth_Folder + 'L84_6ch_track.png', audio_track_1_library_preview)

        # [L86] 2.4 Audio Mixing Room > Normalize
        with uuid("7d77dd1e-37c5-4e05-a8aa-c350f3d945b3") as case:
            # Check normalize default status
            default_button_status = main_page.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': 0}, {'AXIdentifier': 'IDC_AUDIOMIXER_BUTTONNORMALIZE'}]).AXEnabled

            if default_button_status == False:
                check_default = True
            else:
                check_default = False
            time.sleep(DELAY_TIME)

            # Click Split button
            main_page.tips_area_click_split()
            time.sleep(DELAY_TIME)

            # Select timeline clip
            # Enter media room
            main_page.enter_room(0)
            time.sleep(DELAY_TIME*2)

            # Insert media : Skateboard 01.mp4 to timeline
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track(0)

            # Enter Audio Mixing Room
            main_page.enter_room(6)
            time.sleep(DELAY_TIME *3)

            # Click normalize
            check_click_button = audio_mixing_room_page.click_normalize(1)
            logger(check_click_button)
            logger(check_default)
            time.sleep(DELAY_TIME * 3)
            case.result = check_click_button and check_default

            # Open Preference setting > General > Audio channel > Set Stereo
            main_page.click_set_user_preferences()
            time.sleep(DELAY_TIME * 2)
            preferences_page.general.audio_channels_set_stereo()
            time.sleep(DELAY_TIME)

            # Click OK to close (Preference setting)
            preferences_page.click_ok()

        # Enter Voice-Over Recording room
        main_page.enter_room(7)

        # default timeline preview
        default_timeline = main_page.snapshot(locator=L.base.Area.timeline)

        # [L94] 2.5 Voice Over Recording Room > Recording
        with uuid("caaa3432-59bc-464d-a1c6-011da6381159") as case:
            # Open Preference
            voice_over_recording_page.click_preferences_btn()

            logger('tick TIme limit')
            # Tick time limit
            voice_over_recording_page.set_check_recording_preferences_timelimit()
            time.sleep(DELAY_TIME)

            # Set sec = 3
            voice_over_recording_page.set_timelimit_sec(3)
            time.sleep(DELAY_TIME)
            voice_over_recording_page.click_recording_preferences_ok()

            # Click recording
            voice_over_recording_page.click_record_btn(recording_time=5, skip_press_stop=1)

            # Verify step:
            current_timeline_preview = main_page.snapshot(locator=L.base.Area.timeline)
            check_update = not main_page.compare(default_timeline, current_timeline_preview)

            case.result = check_update

            # Open Preference
            voice_over_recording_page.click_preferences_btn()

            # Un-Tick time limit
            voice_over_recording_page.set_check_recording_preferences_timelimit(bCheck=0)
            time.sleep(DELAY_TIME)
            voice_over_recording_page.click_recording_preferences_ok()

        # [L88] 2.5 Voice Over Recording Room > Recording preference > Time limit
        with uuid("78e31461-7279-4e66-b18a-4d2ea49b5574") as case:

            # Verify step: check timelime timecode
            current_timecode = playback_window_page.get_timecode_slidebar()
            if current_timecode == '00:01:14:04':
                case.result = True
            else:
                case.result = False
                logger(current_timecode)

        # [L95] 2.5 Voice-Over recording Room > Stop record
        with uuid("cb943066-9ecc-4410-807e-912fa44ad580") as case:

            # Back to media room
            main_page.enter_room(0)

            # media room current preview
            l95_preview = main_page.snapshot(L.base.Area.library_icon_view)
            check_no_new_record = main_page.compare(l84_preview, l95_preview)

            case.result = not check_no_new_record

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_19(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Clear old capture file: Capture.m4a
        main_page.clear_capture_file()

        # Insert skateboard 01.mp4 to timeline
        main_page.select_library_icon_view_media('Skateboard 01.mp4')
        main_page.tips_area_insert_media_to_selected_track()
        time.sleep(DELAY_TIME)

        # default timeline preview
        default_timeline = main_page.snapshot(locator=L.base.Area.timeline)

        # [L90] 2.5 Voice-Over recording Room > Recording Preference > auto fade-in
        with uuid("10336dd8-bc56-4b3d-ae09-140d52f607c2") as case:
            # Enter Voice-Over Recording room
            main_page.enter_room(7)

            # Open Preference
            voice_over_recording_page.click_preferences_btn()

            # check default status
            default_fade_in = main_page.exist(L.voice_over_recording.chx_auto_fade_in).AXValue
            if default_fade_in == 0:
                check_default = True
            else:
                check_default = False

            time.sleep(DELAY_TIME*2)
            # Apply fade-in
            voice_over_recording_page.set_check_recording_preferences_auto_fade_in()
            time.sleep(DELAY_TIME)
            voice_over_recording_page.click_recording_preferences_ok()

            # Open Preference
            voice_over_recording_page.click_preferences_btn()

            # Verify step:
            after_fade_in = main_page.exist(L.voice_over_recording.chx_auto_fade_in).AXValue
            if after_fade_in == 1:
                apply_result = True
            else:
                apply_result = False
            logger(check_default)
            logger(apply_result)
            case.result = check_default and apply_result

            # Untick fade-in
            voice_over_recording_page.set_check_recording_preferences_auto_fade_in(bCheck=0)
            time.sleep(DELAY_TIME)

            # Close preference
            voice_over_recording_page.click_recording_preferences_ok()

        # [L91] 2.5 Voice-Over recording Room > Recording Preference > auto fade-out
        with uuid("977b1f1d-fda3-4b41-b2dd-e4a6f5de1551") as case:
            # Open Preference
            voice_over_recording_page.click_preferences_btn()

            # check default status
            default_fade_out = main_page.exist(L.voice_over_recording.chx_auto_fade_out).AXValue
            if default_fade_out == 0:
                check_default = True
            else:
                check_default = False

            time.sleep(DELAY_TIME*2)
            # Apply fade-in
            voice_over_recording_page.set_check_recording_preferences_auto_fade_out()
            time.sleep(DELAY_TIME)
            voice_over_recording_page.click_recording_preferences_ok()

            # Open Preference
            voice_over_recording_page.click_preferences_btn()

            # Verify step:
            after_fade_out = main_page.exist(L.voice_over_recording.chx_auto_fade_out).AXValue
            if after_fade_out == 1:
                apply_result = True
            else:
                apply_result = False
            logger(check_default)
            logger(apply_result)
            case.result = check_default and apply_result

            # Untick fade-in
            voice_over_recording_page.set_check_recording_preferences_auto_fade_out(bCheck=0)
            time.sleep(DELAY_TIME)

            # # Close preference
            voice_over_recording_page.click_recording_preferences_ok()

        # [L92] 2.5 Voice-Over recording Room > Mute all tracks when recording
        with uuid("ac9db627-975e-447b-ade6-307cffcce17c") as case:
            if not main_page.exist(L.voice_over_recording.chx_mute_all_tracks_when_recording):
                logger('Didnot find the chx_mute_all_tracks_when_recording')
                raise Exception

            # check default status
            default_chx_value = main_page.exist(L.voice_over_recording.chx_mute_all_tracks_when_recording).AXValue
            if default_chx_value == 0:
                check_default = True
            else:
                check_default = False

            # Set (Mute all tracks when recording)
            voice_over_recording_page.set_check_mute_all_track()
            time.sleep(DELAY_TIME)

            # Verify step:
            current_chx_value = main_page.exist(L.voice_over_recording.chx_mute_all_tracks_when_recording).AXValue
            if current_chx_value == 1:
                apply_result = True
            else:
                apply_result = False

            case.result = check_default and apply_result


            # Restore default
            # Un-tick (Mute all tracks when recording)
            voice_over_recording_page.set_check_mute_all_track(bCheck=0)

        # [L89] 2.5 Voice-Over recording Room > Auto 3 sec delay before recording
        with uuid("fc515ef1-aa48-4c66-9dea-811ca2fb70b8") as case:
            current_audio_value = main_page.exist(L.voice_over_recording.slider_audio_mixer)
            logger(current_audio_value)

            # Open Preference
            voice_over_recording_page.click_preferences_btn()

            # check default status
            default_chx_3s = main_page.exist(L.voice_over_recording.chx_delay_3s).AXValue
            if default_chx_3s == 0:
                check_default = True
            else:
                check_default = False
            time.sleep(DELAY_TIME*2)

            # Set delay 3sec
            voice_over_recording_page.set_check_recording_preferences_delay_3s()

            # Close preference
            voice_over_recording_page.click_recording_preferences_ok()

            # Click record btn
            main_page.click(L.voice_over_recording.btn_record)
            time.sleep(DELAY_TIME)

            # Stop record btn
            main_page.click(L.voice_over_recording.btn_record)

            # Verify step:
            # current timeline preview
            current_timeline = main_page.snapshot(locator=L.base.Area.timeline)
            check_preview = main_page.compare(default_timeline, current_timeline)
            case.result = check_default and check_preview

            # ---- Restore default ----
            # Open Preference
            voice_over_recording_page.click_preferences_btn()

            # Un-tick delay 3sec
            voice_over_recording_page.set_check_recording_preferences_delay_3s(bCheck=0)
            time.sleep(DELAY_TIME)

            # Close preference
            voice_over_recording_page.click_recording_preferences_ok()

        # [L98] 2.6 Subtitle Room > Speech to text (Auto Transcribe subtitle)
        with uuid("831589ab-052e-4e13-a8e6-f7d22cca3c5f") as case:
            # Back to media room
            main_page.enter_room(0)

            # Import video
            video_path = Test_Material_Folder + 'Subtitle_Room/JPN.mp4'
            media_room_page.import_media_file(video_path)
            time.sleep(DELAY_TIME * 2)

            # select timeline track1
            main_page.timeline_select_track(1)
            time.sleep(DELAY_TIME)

            # Set timeline timecode
            main_page.set_timeline_timecode('00_00_10_00')
            time.sleep(DELAY_TIME)

            # Drag media to timeline track1
            main_page.drag_media_to_timeline_playhead_position('JPN.mp4')

            # Enter subtitle room
            main_page.enter_room(8)
            time.sleep(DELAY_TIME*2)

            # Click (Auto Transcribe Subtitle)
            subtitle_room_page.library_menu.click_auto_transcribe()
            time.sleep(DELAY_TIME * 2)

            subtitle_room_page.auto_function.select_LANG('JPN')
            check_setting_lang = subtitle_room_page.auto_function.get_LANG_status()
            if check_setting_lang == "Japanese":
                lang_setting = True
            else:
                lang_setting = False
                logger(check_setting_lang)

            subtitle_room_page.auto_function.click_create()

            for x in range(200):
                if main_page.exist(L.subtitle_room.handle_progress_dialog.btn_cancel):
                    time.sleep(DELAY_TIME)
                else:
                    break

            # get total subtitle rows
            current_rows = self.get_total_subtitle_rows()
            logger(current_rows)
            if current_rows > 6:
                auto_status = True
            else:
                auto_status = False

            case.result = lang_setting and auto_status

    # 11 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_20(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # [L97] 2.6 Subtitle Room > Subtitle room should be gray out when not clips on timeline
        with uuid("a561424a-b292-474c-adef-3d5e8b4377b9") as case:
            check_button_status = main_page.exist(L.main.room_entry.btn_subtitle_room).AXEnabled
            if check_button_status == False:
                case.result = True
            else:
                case.result = False

        # Open project: test_case_1_1_17
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_17.pds')
        main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')

        # Open Preference > Editing > Set default Subtitle duration to 10 (For v21.6 PM request VDE235316-0061)
        main_page.click_set_user_preferences()
        time.sleep(DELAY_TIME * 2)
        preferences_page.switch_to_editing()
        time.sleep(DELAY_TIME)
        preferences_page.editing.durations_subtitle_set_value('10.0')
        time.sleep(DELAY_TIME * 3)
        preferences_page.click_ok()
        time.sleep(DELAY_TIME)

        # set timecode 03:23
        main_page.set_timeline_timecode('00_00_03_23')
        time.sleep(DELAY_TIME * 2)

        # [L99] 2.6 Subtitle Room > Create Subtitle manually
        with uuid("43f96c3a-118c-4c3e-955c-1c8f8fcc2bb8") as case:
            # Enter subtitle room
            main_page.enter_room(8)
            time.sleep(DELAY_TIME*2)

            # Click [Create Subtitle manually]
            click_result = subtitle_room_page.library_menu.click_manually_create()

            # Click [+]
            subtitle_room_page.click_add_btn()
            time.sleep(DELAY_TIME)

            # Add subtitle text on subtitle no.1
            subtitle_room_page.modify_subtitle_text(1, string1='Welcome 1001 Shopping Mall.', string2=' Big sale')
            time.sleep(DELAY_TIME*2)

            current_image = intro_video_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'I99.png')
            check_result = main_page.compare(Ground_Truth_Folder + 'I99.png', current_image)
            case.result = check_result

        # [L100] 2.6 Subtitle Room > Input text
        with uuid("7f4c7718-d0a0-427c-abaf-809b8555a48a") as case:
            # Back to media room
            main_page.enter_room(0)
            time.sleep(DELAY_TIME*2)

            # select track 1
            main_page.timeline_select_track(1)

            # Set timeline timecode
            main_page.set_timeline_timecode('00_00_13_23')
            time.sleep(DELAY_TIME)

            # Enter subtitle room
            main_page.enter_room(8)
            time.sleep(DELAY_TIME*2)

            # Click [+]
            subtitle_room_page.click_add_btn()
            time.sleep(DELAY_TIME)

            # Add subtitle text on subtitle no.2
            subtitle_room_page.modify_subtitle_text(2, string1='Only one day')
            time.sleep(DELAY_TIME * 2)

            current_image = intro_video_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'I100.png')
            check_result = main_page.compare(Ground_Truth_Folder + 'I100.png', current_image)
            case.result = check_result

        # [L103] 2.6 Subtitle Room > Adjust subtitle position
        with uuid("3c4d814a-b38f-426e-a04b-3bdb406cef94") as case:
            # Select subtitle 1
            subtitle_room_page.select_subtitle_row(1)
            time.sleep(DELAY_TIME*2)

            # Click [Adjust position]
            subtitle_room_page.click_adjust_pos_btn()
            time.sleep(DELAY_TIME * 2)

            # Set x = 0.58
            subtitle_room_page.position.set_x_value(0.58)
            subtitle_room_page.position.set_y_value(0.29)
            subtitle_room_page.position.close_window()

            subtitle_room_page.click_adjust_pos_btn()
            time.sleep(DELAY_TIME)
            current_x = subtitle_room_page.position.get_x_value()
            current_y = subtitle_room_page.position.get_y_value()
            if current_x == '0.58' and current_y == '0.29':
                check_setting = True
            else:
                check_setting = False
            logger(check_setting)
            subtitle_room_page.position.close_window()
            time.sleep(DELAY_TIME)

            # Verify Step: Check preview is changed
            modify_pos = intro_video_page.snapshot(locator=main_page.area.preview.main)
            check_modified_pos_preview = main_page.compare(Ground_Truth_Folder + 'I99.png', modify_pos, similarity=0.999)
            case.result = check_setting and (not check_modified_pos_preview)

            # Restore value
            subtitle_room_page.click_adjust_pos_btn()
            time.sleep(DELAY_TIME)
            subtitle_room_page.position.click_reset_btn()
            time.sleep(DELAY_TIME*2)
            subtitle_room_page.position.close_window()

        # [L101] 2.6 Subtitle Room > Merge / Split subtitle
        with uuid("f8692306-bb74-44dc-abf4-f5374b0fca0c") as case:
            subtitle_room_page.select_subtitle_row(2)
            time.sleep(DELAY_TIME*2)

            # get total subtitle rows
            before_rows = self.get_total_subtitle_rows()
            logger(before_rows)

            # Set timeline timecode
            main_page.set_timeline_timecode('00_00_10_08')
            time.sleep(DELAY_TIME)

            # click [Split] button
            subtitle_room_page.click_split_btn()
            time.sleep(DELAY_TIME)

            # get total subtitle rows
            current_rows = self.get_total_subtitle_rows()
            logger(current_rows)
            extra_add = int(current_rows) - int(before_rows)
            if extra_add == 1:
                split_result = True
            else:
                split_result = False
                logger(extra_add)

            # Check merge -----
            subtitle_room_page.multiple_select_subtitle_row(1,2)
            subtitle_room_page.click_merge_btn()
            time.sleep(DELAY_TIME*0.5)

            subtitle_room_page.select_subtitle_row(2)
            time.sleep(DELAY_TIME*2)

            # get total subtitle rows
            merge_rows = self.get_total_subtitle_rows()
            logger(merge_rows)

            if merge_rows == 2:
                merge_result = True
            else:
                merge_result = False
                logger(merge_rows)

            case.result = split_result and merge_result

        # [L104] 2.6 Subtitle Room > Change subtitle text format
        with uuid("8fa81655-5d49-4bcf-9d54-8eef4865e33e") as case:
            main_page.click_undo()

            # click change subtitle text format
            subtitle_room_page.click_change_subtitle_format()

            # font = Mom Outline, size = 22
            subtitle_room_page.character.apply_font_type('Mom Outline')
            subtitle_room_page.character.apply_size('22')
            subtitle_room_page.character.set_text_color('797AFF')

            subtitle_room_page.character.click_ok()

            # select subtitle row 2 (Verify)
            subtitle_room_page.select_subtitle_row(2)
            time.sleep(DELAY_TIME*2)
            current_image = intro_video_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'I104.png')
            case.result = main_page.compare(Ground_Truth_Folder + 'I104.png', current_image)

        # [L106] 2.6 Subtitle Room > Preview movie
        with uuid("ab3bcb63-36a3-44bb-8622-c12d44e0068d") as case:
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 3)
            playback_window_page.Edit_Timeline_PreviewOperation('STOP')
            time.sleep(DELAY_TIME * 2)

            # Switch to media room > Back to subtitle room
            main_page.enter_room(0)
            time.sleep(DELAY_TIME * 2)
            main_page.timeline_select_track(1)

            # Set timeline timecode
            main_page.set_timeline_timecode('00_00_11_04')
            time.sleep(DELAY_TIME)

            # Enter subtitle room
            main_page.enter_room(8)
            time.sleep(DELAY_TIME*2)

            current_image = intro_video_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'I106.png')
            case.result = main_page.compare(Ground_Truth_Folder + 'I106.png', current_image)

        # [L105] 2.6 Subtitle Room > EXport & Import subtitle
        with uuid("381ba551-3de8-4d4f-b5f0-2c00938a7f29") as case:
            srt_export_folder = Test_Material_Folder + 'BFT_21_Stage1/Export/additional_font/'
            if main_page.exist_file(srt_export_folder + 'test_1_20_extra_font.srt'):
                main_page.delete_folder(srt_export_folder)
            time.sleep(DELAY_TIME)
            subtitle_room_page.more.click_export_str(0)
            main_page.handle_save_file_dialog('test_1_20_extra_font.srt', srt_export_folder)
            time.sleep(DELAY_TIME)
            if main_page.exist_file(srt_export_folder + 'test_1_20_extra_font.srt'):
                explore_result = True
            else:
                explore_result = False

            logger(explore_result)

            # [L102] 2.6 Subtitle Room > Remove Subtitle
            with uuid("3c0551ff-9dc6-40cb-b37e-72c21f6fe3ab") as case:
                # select subtitle row 1 > Remove it
                subtitle_room_page.select_subtitle_row(1)
                time.sleep(DELAY_TIME * 2)

                # Click [DEL] button
                subtitle_room_page.click_del_btn()
                time.sleep(DELAY_TIME * 2)

                # Verify step: Check subtitle row 1 (Start Time)
                get_end_time = subtitle_room_page.get_start_time(1)
                if get_end_time == '00:00:08:23':
                    case.result = True
                else:
                    logger(get_end_time)
                    case.result = False

            # Restore subtitle setting
            subtitle_room_page.select_subtitle_row(2)

            # Click title font setting
            subtitle_room_page.click_change_subtitle_format()
            time.sleep(DELAY_TIME * 2)

            # Click Apply all
            subtitle_room_page.character.apply_to_all()
            logger('Restore default setting, Apply to all')
            time.sleep(DELAY_TIME * 2)

            # Remove all subtitle
            subtitle_room_page.more.click_clear_all_subtitles()
            time.sleep(DELAY_TIME * 2)

            # Import subtitle
            subtitle_room_page.more.click_import_subtitle_file()
            main_page.handle_open_project_dialog(srt_export_folder + 'test_1_20_extra_font.srt')
            time.sleep(DELAY_TIME)

            main_page.enter_room(0)
            time.sleep(DELAY_TIME*2)

            main_page.timeline_select_track(1)
            time.sleep(DELAY_TIME*0.5)

            # Set timeline timecode
            main_page.set_timeline_timecode('00_00_11_04')
            time.sleep(DELAY_TIME* 2)

            check_import_image = intro_video_page.snapshot(locator=main_page.area.preview.main)
            import_result = main_page.compare(Ground_Truth_Folder + 'I106.png', check_import_image)

            case.result = explore_result and import_result

        # [L107] 2.6 Subtitle Room > Save Project & Pack project material
        with uuid("4c2bfca6-2351-4925-ba94-9af00253b738") as case:
            # Pack project
            pack_result = main_page.top_menu_bar_file_pack_project_materials(project_path=Test_Material_Folder + 'BFT_21_Stage1/first_project/')

            case.result = pack_result
            # wait pack project processing ready
            time.sleep(DELAY_TIME*15)

        # [L108] 2.6 Subtitle Room > Re-launch PDR
        with uuid("e8516fc6-791e-433e-b83c-768fff49c3be") as case:
            main_page.close_and_restart_app()

            # Verify step
            case.result = main_page.select_library_icon_view_media('Landscape 02.jpg')

    # 9 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_21(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*4)
        main_page.timeline_select_track(1)

        # [L380] 5. Produce > XAVCS > Open Saved project
        with uuid("8d2e8c7e-3108-4cfa-bcf8-bb37446caa2a") as case:
            # Open project: first_project
            main_page.top_menu_bar_file_open_project(save_changes='no')
            check_open_result = main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/first_project.pdk')
            time.sleep(DELAY_TIME*3)
            if not check_open_result:
                logger('handle_open_project_dialog [NG]')
                case.result = False
            else:

                # Select extract path
                main_page.delete_folder(Test_Material_Folder + 'BFT_21_Stage1/extract_flder_1')
                time.sleep(DELAY_TIME)
                main_page.select_file(Test_Material_Folder + 'BFT_21_Stage1/extract_flder_1')
                time.sleep(DELAY_TIME*5)
                main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')
                time.sleep(DELAY_TIME*3)

                # Verify Step:
                # Set timeline timecode = (00:00:11:04)
                main_page.set_timeline_timecode('00_00_11_04')
                time.sleep(DELAY_TIME * 4)
                # Check preview with timeline timecode = (00_00_11_04)
                current_preview = main_page.snapshot(locator=main_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'L380.png')
                check_preview = main_page.compare(Ground_Truth_Folder + 'L380.png', current_preview)
                logger(check_preview)
                case.result = check_preview

        # [L381] 5. Produce > XAVCS > Select [Format] > XAVCS
        with uuid("6c6e909c-0333-4047-8f90-926208a8dd2b") as case:
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            produce_page.local.select_file_format('xavc_s')
            time.sleep(DELAY_TIME)

            # Get produced file name
            explore_file = produce_page.get_produced_filename()
            logger(explore_file)
            time.sleep(DELAY_TIME)

            if explore_file == 'first_project.mp4':
                check_mp4 = True
            else:
                check_mp4 = False

            if main_page.exist(L.produce.local.cbx_profile_type):
                select_xavc = True
            else:
                select_xavc = False

            case.result = check_mp4 and select_xavc

        # [L382] 5. Produce > XAVCS > Select [Format] > 1280x720/30p (17Mbps)
        with uuid("a89579e5-7a01-4abb-948e-ff28e225df65") as case:
            produce_page.local.select_profile_name(2)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'XAVC S 1280 x 720/30p (17 Mbps)':
                case.result = False
                case.fail_log = check_profile
            else:
                case.result = True

        # [L383] 5. Produce > XAVCS > Select encode type > SW
        with uuid("65a87f83-cfe7-4064-8dfa-b15ea92952d6") as case:
            # Untick Fast video rendering technology
            produce_page.local.set_fast_video_rendering(is_checked=0)
            time.sleep(DELAY_TIME)

            check_hw = main_page.exist(L.produce.local.rdb_fast_video_rendering_hardware_encode).AXValue

            if check_hw == 0:
                case.result = True
            else:
                case.result = False

        # [L385] 5. Produce > XAVCS > Set [Surround Sound] > TT Surround
        with uuid("c459820f-964b-481b-b4c7-7cbfbea9eb3b") as case:
            produce_page.local.set_surround_sound()
            time.sleep(DELAY_TIME)

            produce_page.local.set_surround_sound_true_theater_option_theater()
            time.sleep(DELAY_TIME)

            check_surround = main_page.exist(L.produce.local.rdb_surround_sound_true_theater).AXValue

            if check_surround == 1:
                case.result = True
            else:
                case.result = False

        # [L386] 5. Produce > XAVCS > Set output folder and file name
        with uuid("0092cf6f-fc69-455b-b4f1-558b992e2ee5") as case:
            default_produce_file_path = main_page.exist(L.produce.edittext_output_folder).AXValue
            time.sleep(DELAY_TIME)
            if main_page.exist_file(Test_Material_Folder + 'BFT_21_Stage1/produce/L386_xavc.mp4'):
                main_page.delete_folder(Test_Material_Folder + 'BFT_21_Stage1/produce')

            produce_page.select_output_folder(Test_Material_Folder + 'BFT_21_Stage1/produce/L386_xavc.mp4')
            time.sleep(DELAY_TIME*2)

            # Get produced file name
            explore_file = produce_page.get_produced_filename()
            logger(explore_file)
            time.sleep(DELAY_TIME)

            if explore_file == 'L386_xavc.mp4':
                case.result = True
            else:
                case.result = False

        # [L384] 5. Produce > XAVCS > Upload a copy to Cloud
        with uuid("ca0790d0-ef40-4058-b787-2e3ceaf5cbf3") as case:
            produce_page.local.set_check_upload_copy_to_cyberlink_cloud(is_check=1)
            time.sleep(DELAY_TIME * 2)
            current_upload_checkbox = produce_page.local.check_visible_upload_copy_to_cyberlink_cloud()
            logger(current_upload_checkbox)
            case.result = current_upload_checkbox

            time.sleep(DELAY_TIME*2)

        # [L387] 5. Produce > XAVCS > Start Produce
        with uuid("15d3cb75-1abf-4e44-bfbe-9602f92cf5fb") as case:
            # Start : produce
            produce_page.click(L.produce.btn_start_produce)
            time.sleep(DELAY_TIME*1.5)

            # handle dialog: Convert to MP4 = No
            produce_page.local.click_option_convert_cyberlink_cloud_copy_to_mp4_dialog(option=1)
            for x in range(600):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # wait for video upload to cloud
            for x in range(60):
                back_btn = main_page.exist(L.produce.btn_back_to_edit_after_upload_cl)
                if back_btn:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click(L.produce.btn_back_to_edit_after_upload_cl)
            time.sleep(DELAY_TIME * 5)

            # Verify step:
            check_explore_file = main_page.select_library_icon_view_media(explore_file)
            logger(check_explore_file)

            # Verify step2: Remove the upload video
            # Click Import media > (Download media from Cyberlink cloud)
            media_room_page.import_media_from_cyberlink_cloud()

            time.sleep(DELAY_TIME * 3)

            # Double click to enter PowerDirector folder
            import_media_from_cloud_page.select_content_in_folder_level(folder_index=0, click_times=2)

            # Search explore_file
            import_media_from_cloud_page.input_text_in_seacrh_library('L386_xavc')
            time.sleep(DELAY_TIME)

            # Tick 'Select all'
            import_media_from_cloud_page.tap_select_deselect_all_btn()

            # Check remove button
            remove_btn = main_page.exist(L.import_downloaded_media_from_cl.delete_btn).AXEnabled

            # Remove
            import_media_from_cloud_page.tap_remove_btn()

            case.result = check_explore_file and remove_btn

            # Close (Download Media) window
            time.sleep(DELAY_TIME)
            main_page.click(L.import_downloaded_media_from_cl.close_btn)

        # [L388] 5. Produce > XAVCS > Playback produced clip
        with uuid("b8960b0f-b0f8-4451-b163-12501bca2c9c") as case:
            main_page.select_library_icon_view_media(explore_file)
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 10)
            playback_window_page.Edit_Timeline_PreviewOperation('STOP')
            time.sleep(DELAY_TIME * 2)

            # Verify Step:
            # Set timeline timecode = (00:00:55:11)
            main_page.set_timeline_timecode('00_00_55_11')
            time.sleep(DELAY_TIME * 3)
            # Check preview with timeline timecode = (00_00_55_11)
            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view, file_name=Auto_Ground_Truth_Folder + 'L388.png')
            check_preview = main_page.compare(Ground_Truth_Folder + 'L388.png', current_preview, similarity=0.9)
            logger(check_preview)
            case.result = check_preview

    # 9 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_22(self):
        # launch APP
        main_page.clear_cache()
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Import Image to library
        media_room_page.import_media_file(Test_Material_Folder + 'Produce_Local/Produce_G182.mp4')
        time.sleep(DELAY_TIME * 1.5)

        # [L280] 4.1 Basic > Trim > Entry (from Precut)
        with uuid("f700865e-864a-4a3f-8823-8ba456586b94") as case:
            main_page.select_library_icon_view_media('Produce_G182.mp4')
            time.sleep(DELAY_TIME)
            media_room_page.library_clip_context_menu_precut()
            if not precut_page.exist(L.precut.single_trim):
                check_precut = False
            else:
                check_precut = True

            leave_result = precut_page.close_precut_window()
            time.sleep(DELAY_TIME)
            case.result = check_precut and leave_result

        # [L282] 4.1 Basic > Trim type > Single Trim
        with uuid("4a4476a8-9b44-4a22-b607-638c18431bd2") as case:
            main_page.select_library_icon_view_media('Produce_G182.mp4')
            time.sleep(DELAY_TIME)
            media_room_page.library_clip_context_menu_precut()
            time.sleep(DELAY_TIME)

            # Set timecode > Click Mark in
            precut_page.set_precut_timecode('00_00_00_21')
            time.sleep(DELAY_TIME)
            precut_page.tap_single_trim_mark_in()
            time.sleep(DELAY_TIME)

            # Set timecode > Click Mark out
            precut_page.set_precut_timecode('00_00_06_05')
            time.sleep(DELAY_TIME)
            precut_page.tap_single_trim_mark_out()
            time.sleep(DELAY_TIME)

            # Verify Step
            # Check Duration
            current_duration = precut_page.get_precut_single_trim_duration()

            if current_duration == '00:00:05:14':
                single_trim = True
            else:
                single_trim = False
            logger(single_trim)

            precut_page.click_ok()

            # Set timeline timecode
            main_page.set_timeline_timecode('00_00_16_12')

            # Verify Step: Check timeline timecode
            current_timecode = playback_window_page.get_timecode_slidebar()
            if current_timecode == '00:00:06:05':
                back_media_result = True
            else:
                back_media_result = False
            case.result = single_trim and back_media_result

        # [L281] 4.1 Basic > Entry > Tips area > Trim
        with uuid("bfe1147f-d5fc-46e4-a105-243696f4b7a6") as case:
            # Insert to timeline
            main_page.select_library_icon_view_media('Precut 0001')

            main_page.tips_area_insert_media_to_selected_track()
            time.sleep(DELAY_TIME)

            # Click Trim button on tips area > Open Trim
            tips_area_page.click_TipsArea_btn_Trim('video')
            time.sleep(DELAY_TIME)

            # Verify Step
            # Check Duration
            current_duration = precut_page.get_precut_single_trim_duration()

            if current_duration == '00:00:05:14':
                case.result = True
            else:
                case.result = False

        # [L283] 4.1 Basic > Tips type > Multi Trim
        with uuid("a7560fe1-5c8f-450c-9455-ddcfabf65d76") as case:
            # Switch to Multi trim
            precut_page.edit_precut_switch_trim_mode('Multi')

            # Remove (Single Trim) result
            precut_page.tap_multi_trim_remove()

            # First trim
            # Set timecode > Click (Multi) Mark in
            precut_page.set_precut_timecode('00_00_01_14')
            time.sleep(DELAY_TIME)
            precut_page.tap_multi_trim_mark_in()

            precut_page.set_precut_timecode('00_00_04_09')
            time.sleep(DELAY_TIME)
            precut_page.tap_multi_trim_mark_out()

            # Second trim
            # Set timecode > Click (Multi) Mark in
            precut_page.set_precut_timecode('00_00_06_18')
            time.sleep(DELAY_TIME)
            precut_page.tap_multi_trim_mark_in()

            precut_page.set_precut_timecode('00_00_08_25')
            time.sleep(DELAY_TIME)
            precut_page.tap_multi_trim_mark_out()

            # Verify Step:
            time.sleep(DELAY_TIME * 2)
            current_image = precut_page.snapshot(locator=L.precut.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'L283.png')

            check_result = precut_page.compare(Ground_Truth_Folder + 'L283.png', current_image)
            # logger(check_thumbnail)
            case.result = check_result

        # [L284] 4.1 Basic > Trim > Preview trimmed clip in timeline
        with uuid("1e8b6a66-bbb6-4408-9618-5e8cb2c9ded5") as case:
            # Close (Trim window)
            precut_page.click_ok()
            time.sleep(DELAY_TIME * 2)

            main_page.timeline_select_track(1)
            time.sleep(DELAY_TIME)
            # Check preview update
            current_preview = main_page.snapshot(locator=L.base.Area.preview.main,
                                              file_name=Auto_Ground_Truth_Folder + 'L284.png')
            check_result = precut_page.compare(Ground_Truth_Folder + 'L284.png', current_preview)

            # Click Stop
            playback_window_page.Edit_Timeline_PreviewOperation('STOP')
            time.sleep(DELAY_TIME)
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            play_preview = main_page.Check_PreviewWindow_is_different(area=L.base.Area.preview.main, sec=2)
            playback_window_page.Edit_Timeline_PreviewOperation('Stop')

            case.result = check_result and play_preview

        # Click [Up one level]
        media_room_page.media_content_click_up_one_level()

        # [L288] 4.1 Basic > Sync by audio
        with uuid("d460d39c-c631-4eb4-8e8f-4700ae1edabc") as case:
            main_page.timeline_select_track(1)

            # Set timeline timecode to drag CTI to end
            main_page.set_timeline_timecode('00_00_05_02')
            time.sleep(DELAY_TIME)

            # Insert video to timeline
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            time.sleep(DELAY_TIME)

            # Set timeline timecode
            main_page.set_timeline_timecode('00_00_05_00')

            # Click Split hotkey > to separate clip
            main_page.tap_Split_hotkey()
            time.sleep(DELAY_TIME)

            # Multi-select
            timeline_operation_page.select_multiple_timeline_media(media1_track_index=0, media1_clip_index=2, media2_track_index=0, media2_clip_index=3)
            time.sleep(DELAY_TIME)

            # Click Sync by Audio
            tips_area_page.click_sync_by_audio()

            # Select track 3 clip > Apply blending mode
            timeline_operation_page.select_timeline_media(track_index=4, clip_index=0)
            tips_area_page.tools.select_Blending_Mode()
            time.sleep(DELAY_TIME * 2)
            blending_mode_page.set_blending_mode('Difference')

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME)

            # Set timeline timecode
            main_page.set_timeline_timecode('00_00_03_16')
            time.sleep(DELAY_TIME * 3)

            # select track 1
            main_page.timeline_select_track(1)

            # Insert Landscape 01.jpg to track1
            main_page.select_library_icon_view_media('Landscape 01.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            time.sleep(DELAY_TIME)

            # Check preview update
            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                              file_name=Auto_Ground_Truth_Folder + 'L288.png')
            check_result = precut_page.compare(Ground_Truth_Folder + 'L288.png', current_preview, similarity=0.85)

            case.result = check_result

        # Modify case for v22.0.5622 RD already fix the bug of (Sync by audio) ---->
        ## Jamie 2023/08/24 modify ##
        for x in range(6):
            main_page.click_undo()
            time.sleep(DELAY_TIME*0.5)

        # select track 3
        main_page.timeline_select_track(3)

        # Insert video to timeline
        main_page.select_library_icon_view_media('Skateboard 01.mp4')
        main_page.tips_area_insert_media_to_selected_track()
        time.sleep(DELAY_TIME)

        # Set timeline timecode
        main_page.set_timeline_timecode('00_00_05_00')

        # Click Split hotkey > to separate clip
        main_page.tap_Split_hotkey()
        time.sleep(DELAY_TIME)

        # Select track 3 1st clip
        main_page.select_timeline_media('Skateboard 01')

        # Right click men > Cut > Cut and Fill gap
        main_page.right_click()
        time.sleep(DELAY_TIME)
        main_page.select_right_click_menu('Cut', 'Cut and Fill Gap')

        # select track 2
        main_page.timeline_select_track(2)

        # Set timeline timecode
        main_page.set_timeline_timecode('00_00_06_00')

        # select track 2
        main_page.timeline_select_track(2)

        # Right click men > Paste
        main_page.right_click()
        time.sleep(DELAY_TIME)
        main_page.select_right_click_menu('Paste')
        time.sleep(DELAY_TIME)

        # Select track 3, 1st clip
        timeline_operation_page.select_timeline_media(track_index=4, clip_index=0)

        tips_area_page.tools.select_Blending_Mode()
        time.sleep(DELAY_TIME * 2)
        blending_mode_page.set_blending_mode('Difference')

        # click [OK] to apply and exit Blending mode dialogue
        blending_mode_page.click_ok()
        time.sleep(DELAY_TIME)

        # Set timeline timecode
        main_page.set_timeline_timecode('00_00_03_16')
        time.sleep(DELAY_TIME * 3)
        # Modify case for v22.0.5622 RD already fix the bug of (Sync by audio) <----

        # [L285] 4.1 Basic > Crop > Open [Crop Image] window
        with uuid("40626f6d-c346-4962-98bc-f72027dbfbee") as case:
            # select track 1
            main_page.timeline_select_track(1)

            # Insert Landscape 01.jpg to track1
            main_page.select_library_icon_view_media('Landscape 01.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            time.sleep(DELAY_TIME)

            # Click [Crop the selected image]
            tips_area_page.click_TipsArea_btn_Crop_Image()

            #crop_image_page
            crop_window = main_page.exist(L.crop_image.crop_window)
            if crop_window:
                case.result = True
            else:
                case.result = False

        # [L286] 4.1 Basic > Crop > Set crop area
        with uuid("cdfdf12d-cbe7-46bd-80d1-044f5afa6ec7") as case:
            # [L287] 4.1 Basic > Crop > Preview image in timeline
            with uuid("3bf42f48-6698-4d77-b7ee-4935bff07938") as case:
                crop_image_page.aspect_ratio.set_4_3()
                time.sleep(DELAY_TIME)
                crop_image_page.click_ok()

                # Set timeline timecode
                main_page.set_timeline_timecode('00_00_04_00')
                time.sleep(DELAY_TIME* 2)

                four_sec_preview = main_page.snapshot(locator=L.base.Area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'L286.png')

                check_result = precut_page.compare(Ground_Truth_Folder + 'L286.png', four_sec_preview, similarity=0.9)
                case.result = check_result
            case.result = check_result

            # Set timeline timecode
            main_page.timeline_select_track(2)
            main_page.set_timeline_timecode('00_00_13_18')
            time.sleep(DELAY_TIME * 3)

            # Save project:
            main_page.top_menu_bar_file_save_project_as()
            main_page.handle_save_file_dialog(name='test_case_1_1_22',
                                              folder_path=Test_Material_Folder + 'BFT_21_Stage1/')

    # 11 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_23(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open project: test_case_1_1_22
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_22.pds')
        main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')

        # Insert Food.jpg
        main_page.select_library_icon_view_media('Food.jpg')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()

        # [L290] 4.2 > Tools > Pan & Zoom (image) > [Pan & Zoom] page > UI switch to Pan & Zoom
        with uuid("a7c4224f-cdd0-4eae-af6c-6d8c138e1469") as case:
            # Select track 1 : Photo clip Landscape 01 (0)
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=2)
            time.sleep(DELAY_TIME)

            # Click Tools > [Pan & Zoom page] then close
            tips_area_page.tools.select_Pan_Zoom()
            time.sleep(DELAY_TIME * 2)
            case.result = pan_zoom_page.is_enter_pan_zoom()
            pan_zoom_page.click_close()

        # [L291] 4.2 > Tools > Pan & Zoom (image) > [Pan & Zoom] page > Select style
        with uuid("f7470554-59f0-46e2-bf7d-e25c83ac7a54") as case:
            main_page.set_timeline_timecode('00_00_03_05')
            time.sleep(DELAY_TIME *2)

            # Enter Pan & Zoom
            tips_area_page.tools.select_Pan_Zoom()
            time.sleep(DELAY_TIME * 2)

            # Select style: 3rd style
            pan_zoom_page.apply_motion_style(3)

            main_page.set_timeline_timecode('00_00_04_20')
            time.sleep(DELAY_TIME * 2)

            # Verify Step
            # Check preview update
            current_preview = main_page.snapshot(locator=L.base.Area.preview.main,
                                              file_name=Auto_Ground_Truth_Folder + 'L291.png')
            time.sleep(DELAY_TIME * 2)
            check_result = precut_page.compare(Ground_Truth_Folder + 'L291.png', current_preview, similarity=0.9)

            case.result = check_result

        pan_zoom_page.click_close()
        time.sleep(DELAY_TIME * 2)

        # [L292] 4.2 > Tools > Pan & Zoom (image) > [Pan & Zoom] page > Apply to all
        with uuid("01b7c7c1-017d-4915-a6a0-f0b224a967d3") as case:
            # Apply (Right down to Left up)
            # Select track 1 : Photo clip Food.jpg
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=3)
            time.sleep(DELAY_TIME)

            tips_area_page.tools.select_Pan_Zoom()
            pan_zoom_page.apply_motion_style(11)
            time.sleep(DELAY_TIME * 2)

            # Apply to all
            pan_zoom_page.click_apply_to_all()
            time.sleep(DELAY_TIME * 2)
            pan_zoom_page.click_close()

            # Verify Step:
            # Select track 1 : Photo clip Landscape 01 (0)
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=2)
            time.sleep(DELAY_TIME)

            tips_area_page.tools.select_Pan_Zoom()
            main_page.set_timeline_timecode('00_00_04_20')
            time.sleep(DELAY_TIME * 2)
            apply_all_preview = main_page.snapshot(locator=L.base.Area.preview.main)
            case.result = not main_page.compare(Ground_Truth_Folder + 'L291.png', apply_all_preview, similarity=0.9)

        # [L293] 4.2 > Tools > Pan & Zoom (image) > Magic Motion Designer > Adjust position / scale / Rotate
        with uuid("e0c915bc-66a2-4b11-bda4-206127c3dcc6") as case:
            pan_zoom_page.click_motion_designer()
            time.sleep(DELAY_TIME * 2)
            default_aspect_ratio = pan_zoom_page.magic_motion_designer.get_current_aspect_ratio()
            logger(default_aspect_ratio)

            if default_aspect_ratio == '4:3':
                default_aspect_ratio_value = True
            else:
                default_aspect_ratio_value = False

            # Apply aspect ratio to 16:9
            pan_zoom_page.magic_motion_designer.set_aspect_ratio_16_9('ok')
            time.sleep(DELAY_TIME * 2)

            # Set rotate = 90
            pan_zoom_page.magic_motion_designer.drag_preview_object_rotate_clockwise()
            time.sleep(DELAY_TIME * 2)

            # Verify Step:
            current_degree_value = pan_zoom_page.magic_motion_designer.rotation.get_value()

            if current_degree_value == '90':
                rotate_result = True
            else:
                rotate_result = False
                logger(current_degree_value)

            case.result = default_aspect_ratio and rotate_result

        # [L295] 4.2 > Tools > Pan & Zoom (image) > Magic Motion Designer > Adjust position / scale / Rotate
        with uuid("ca4cf4fe-ee2f-4312-8416-59574bcebd88") as case:
            # Set (Magic Motion Designer) timecode
            pan_zoom_page.magic_motion_designer.set_timecode('00_00_02_08')
            time.sleep(DELAY_TIME * 2)

            # Verify Step
            # Check preview update
            current_preview = main_page.snapshot(locator=L.pan_zoom.magic_motion_designer.preview_area,
                                                 file_name=Auto_Ground_Truth_Folder + 'L295.png')

            check_result = precut_page.compare(Ground_Truth_Folder + 'L295.png', current_preview)
            case.result = check_result

        # [L296] 4.2 > Tools > Pan & Zoom (image) > Magic Motion Designer > Apply (check timeline preview)
        with uuid("fcb0b21f-bc5f-45cb-b23d-5f8bdce523ad") as case:
            # Set rotation to 120 degree
            pan_zoom_page.magic_motion_designer.rotation.set_value(120)
            time.sleep(DELAY_TIME)
            pan_zoom_page.magic_motion_designer.click_ok()
            time.sleep(DELAY_TIME * 2)

            # Verify Step
            # Check preview update
            current_preview = main_page.snapshot(locator=L.base.Area.preview.main,
                                              file_name=Auto_Ground_Truth_Folder + 'L296.png')
            check_result = precut_page.compare(Ground_Truth_Folder + 'L296.png', current_preview)

            case.result = check_result

        # [L294] 4.2 > Tools > Pan & Zoom (image) > Magic Motion Designer > Reset
        with uuid("ca1defd1-293c-4f10-b65b-cc9d6dfe1ff4") as case:
            pan_zoom_page.click_motion_designer()
            time.sleep(DELAY_TIME * 2)

            # Click reset
            pan_zoom_page.magic_motion_designer.click_reset()
            time.sleep(DELAY_TIME * 2)

            # Verify Step
            # Check preview update
            current_preview = main_page.snapshot(locator=L.pan_zoom.magic_motion_designer.preview_area,
                                                 file_name=Auto_Ground_Truth_Folder + 'L294.png')

            check_result = precut_page.compare(Ground_Truth_Folder + 'L294.png', current_preview)
            case.result = check_result

        # Click undo then click OK to close (Magic Motion Designer)
        pan_zoom_page.magic_motion_designer.click_undo()
        time.sleep(DELAY_TIME)
        pan_zoom_page.magic_motion_designer.click_ok()
        time.sleep(DELAY_TIME)

        # Close [Pan & Zoom] page
        pan_zoom_page.click_close()

        # [L297] 4.2 > Tools > Crop / Zoom / Pan > Adjust position / scale / rotation
        with uuid("1425e2a8-b34c-44ef-8e5e-70c36b51eed8") as case:
            # Select track 1 : 1st Precut001
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            time.sleep(DELAY_TIME)

            # Enter (Crop / Zoom / Pan)
            tips_area_page.tools.select_CropZoomPan()
            check_result = crop_zoom_pan_page.is_enter_crop_zoom_pan()
            if not check_result:
                logger('Not enter crop/zoom/pan now.')
                raise Exception

            # Set aspect ratio = 1:1
            crop_zoom_pan_page.set_AspectRatio_1_1()

            # Set position x =0.627
            crop_zoom_pan_page.set_position_x('0.627')

            # Scale w = 0.44
            crop_zoom_pan_page.set_scale_width('0.45')
            time.sleep(DELAY_TIME * 2)

            # Verify Step
            # Check setting update
            current_preview = main_page.snapshot(locator=L.crop_zoom_pan.window,
                                                 file_name=Auto_Ground_Truth_Folder + 'L297.png')

            check_result = precut_page.compare(Ground_Truth_Folder + 'L297.png', current_preview)
            case.result = check_result

        # [L299] 4.2 > Tools > Crop / Zoom / Pan > Preview
        with uuid("6dcb0c75-2424-4716-9a68-059d53834b8f") as case:
            # Set timecode (00;00;01;24)
            crop_zoom_pan_page.set_timecode('00_00_01_24')
            time.sleep(DELAY_TIME*2)

            # Verify Step
            # Check preview update
            current_preview = main_page.snapshot(locator=L.crop_zoom_pan.preview,
                                                 file_name=Auto_Ground_Truth_Folder + 'L299.png')

            check_result = precut_page.compare(Ground_Truth_Folder + 'L299.png', current_preview)
            case.result = check_result

        # [L300] 4.2 > Tools > Crop / Zoom / Pan > Apply (Check timeline preview after apply)
        with uuid("6ef237b8-e614-4a71-a1da-8f764d159680") as case:
            crop_zoom_pan_page.click_ok()
            time.sleep(DELAY_TIME * 2)

            main_page.set_timeline_timecode('00_00_01_15')
            time.sleep(DELAY_TIME * 2)

            # Verify Step
            # Check preview update
            current_preview = main_page.snapshot(locator=L.base.Area.preview.main,
                                              file_name=Auto_Ground_Truth_Folder + 'L300.png')
            check_result = precut_page.compare(Ground_Truth_Folder + 'L300.png', current_preview)

            case.result = check_result

        # [L298] 4.2 > Tools > Crop / Zoom / Pan > Reset
        with uuid("d4ea74c3-f6d6-4e49-be46-c0b9d452c447") as case:
            # Enter (Crop / Zoom / Pan)
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME)

            # click [Reset] button
            crop_zoom_pan_page.click_reset()
            time.sleep(DELAY_TIME * 2)

            # Verify Step
            check_aspect_ratio = crop_zoom_pan_page.get_current_AspectRatio()
            logger(check_aspect_ratio)
            if check_aspect_ratio == '16:9':
                check_aspect_ratio_result = True
            else:
                check_aspect_ratio_result = False

            current_scale_width = crop_zoom_pan_page.get_scale_width()
            logger(current_scale_width)
            if current_scale_width == '1.000':
                check_scale_width_result = True
            else:
                check_scale_width_result = False

            case.result = check_aspect_ratio_result and check_scale_width_result
            crop_zoom_pan_page.click_ok()
            time.sleep(DELAY_TIME * 2)

            # Save project:
            main_page.top_menu_bar_file_save_project_as()
            main_page.handle_save_file_dialog(name='test_case_1_1_23',
                                              folder_path=Test_Material_Folder + 'BFT_21_Stage1/')

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_24(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open project: test_case_1_1_23
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_23.pds')
        main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')

        # click timeline track2
        main_page.timeline_select_track(2)

        # Set timeline timecode
        main_page.set_timeline_timecode('00_00_11_00')
        time.sleep(DELAY_TIME * 2)

        # Import video to library
        media_room_page.import_media_file(Test_Material_Folder + 'Produce_Local/4978895.mov')
        time.sleep(DELAY_TIME * 1.5)
        media_room_page.handle_high_definition_dialog()

        # Insert to timeline
        main_page.tips_area_insert_media_to_selected_track()

        # [L304] 4.2 Tools > Video Speed > Entire Clip > Adjust from new video duration
        with uuid("5beaaacf-885e-4d34-8e20-402e9404f46b") as case:
            # Enter (Video Speed)
            tips_area_page.tools.select_VideoSpeed()
            time.sleep(DELAY_TIME)

            # Get (default) duration
            current_new_duration = video_speed_page.Edit_VideoSpeed_EntireClip_NewVideoDuration_GetValue()
            logger(current_new_duration)

            if current_new_duration == '00:00:17:26':
                default_new_duration = True
            else:
                default_new_duration = False

            # Set new duration = '00;00;10;26'
            video_speed_page.Edit_VideoSpeed_EntireClip_NewVideoDuration_SetValue('00_00_10_26')
            time.sleep(DELAY_TIME * 2)

            # Get (current) duration
            check_new_duration = video_speed_page.Edit_VideoSpeed_EntireClip_NewVideoDuration_GetValue()
            logger(check_new_duration)

            if check_new_duration == '00:00:10:26':
                apply_new_duration = True
            else:
                apply_new_duration = False

            case.result = default_new_duration and apply_new_duration

        # [L305] 4.2 Tools > Video Speed > Entire Clip > Adjust Speed multiplier
        with uuid("875648d7-cadc-497d-869a-1f8c5a2f2409") as case:
            # Check current multiplier
            check_multiplier = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_GetValue()
            logger(check_multiplier)

            if check_multiplier == '1.644':
                current_multiplier = True
            else:
                current_multiplier = False

            # Set multiplier = 0.85
            video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_DragSlider(42.45)
            time.sleep(DELAY_TIME)
            video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_ArrowButton('Up')
            time.sleep(DELAY_TIME * 2)

            # Check current multiplier
            check_multiplier = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_GetValue()
            logger(check_multiplier)

            if check_multiplier == '0.850':
                set_multiplier = True
            else:
                set_multiplier = False

            case.result = current_multiplier and set_multiplier

        # [L306] 4.2 Tools > Video Speed > Selected Range > Create a time shift
        with uuid("48ded325-7c78-4c8a-be87-0959e9b0c833") as case:
            # Switch to (Selected Range)
            video_speed_page.Edit_VideoSpeedDesigner_SelectTab('selected range')

            # Pop up warning message: (... Do you want to continue?)
            # Click [OK] button
            main_page.exist_click(L.main.confirm_dialog.btn_ok, timeout=10)

            # Click [Time Shift]
            check_result = video_speed_page.VideoSpeedDesigner_SelectRange_Click_Upper_CreateTimeShift_btn()
            logger(check_result)
            time.sleep(DELAY_TIME * 2)

            # Verify Step:
            # Check button is disable
            elem_btn = main_page.exist(L.video_speed.time_shift_1)
            if elem_btn.AXEnabled == False:
                verify_step = True
            else:
                verify_step = False
            logger(verify_step)

            case.result = check_result and verify_step

        # [L307] 4.2 Tools > Video Speed > Selected Range > Adjust speed (1.5x)
        with uuid("2de16d6c-ea92-4c32-9557-4f972f23f720") as case:
            # Get (default) multiplier
            current_multiplier = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_GetValue()
            logger(current_multiplier)

            if current_multiplier == '1.000':
                default_multiplier = True
            else:
                default_multiplier = False

            # Set speed to 1.5 for 1st (Time shift)
            video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_SetValue(1.500)

            # Verify step:

            # Get (current) multiplier
            current_multiplier = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_GetValue()
            logger(current_multiplier)

            if current_multiplier == '1.500':
                apply_multiplier = True
            else:
                apply_multiplier = False

            # Get (current) duration
            current_duration = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_VideoLength_GetValue()
            logger(current_duration)

            if current_duration == '00:00:01:15':
                check_duration = True
            else:
                check_duration = False

            case.result = default_multiplier and apply_multiplier and check_duration

        # [L308] 4.2 Tools > Video Speed > Reset
        with uuid("c79b1222-f933-4738-8062-39bf61d9e93c") as case:
            # Click [Reset]
            video_speed_page.Edit_VideoSpeedDesigner_ClickReset()
            time.sleep(DELAY_TIME * 1.5)

            # Get (current) duration
            current_duration = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_VideoLength_GetValue()
            logger(current_duration)

            if current_duration == '00:00:00:00':
                case.result = True
            else:
                case.result = False

        # [L309] 4.2 Tools > Video Speed > Preview
        with uuid("53aadaee-c816-446f-af87-a878ba5c8d0c") as case:
            # Under [Selected Range] > Seek to timecode (12 sec)
            video_speed_page.set_VideoSpeedDesigner_timecode('00_00_12_00')

            # Click [Time Shift]
            check_result = video_speed_page.VideoSpeedDesigner_SelectRange_Click_Upper_CreateTimeShift_btn()
            logger(check_result)
            time.sleep(DELAY_TIME * 2)

            # Set multiplier = 10
            video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_SetValue(10)
            time.sleep(DELAY_TIME)

            # Set timecode to 13:16
            video_speed_page.set_VideoSpeedDesigner_timecode('00_00_13_16')
            time.sleep(DELAY_TIME * 2)

            # Verify Step:
            current_preview = main_page.snapshot(locator=L.video_speed.main,
                                              file_name=Auto_Ground_Truth_Folder + 'L309.png')
            check_result = precut_page.compare(Ground_Truth_Folder + 'L309.png', current_preview)

            case.result = check_result

        # Click [OK] to save change
        video_speed_page.Edit_VideoSpeedDesigner_ClickOK()

        # Save project:
        main_page.top_menu_bar_file_save_project_as()
        main_page.handle_save_file_dialog(name='test_case_1_1_24',
                                          folder_path=Test_Material_Folder + 'BFT_21_Stage1/')

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_25(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open project: test_case_1_1_24
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_24.pds')
        main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')

        # Select timeline track2
        main_page.timeline_select_track(2)

        # Move timecode to 0s
        main_page.set_timeline_timecode('00_00_00_00')
        time.sleep(DELAY_TIME * 2)

        # Insert Food.jpg to track2
        main_page.select_library_icon_view_media('Food.jpg')
        main_page.tips_area_insert_media_to_selected_track()
        time.sleep(DELAY_TIME * 2)

        # Initial_preview

        no_blending_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

        # [L319] 4.2 Tools > Blending Mode > Image
        with uuid("76b12400-6632-4a70-88b6-e1787e0f2e10") as case:
            # First time: Click [Tools] > Blending Mode
            tips_area_page.tools.select_Blending_Mode()
            time.sleep(DELAY_TIME * 2)
            blending_mode_page.set_blending_mode('Overlay')
            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME)
            overlay_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Second time: Click [Tools] > Blending Mode -----------
            tips_area_page.tools.select_Blending_Mode()
            time.sleep(DELAY_TIME * 2)
            blending_mode_page.set_blending_mode('Screen')
            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME*2)
            screen_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Preview should be updated (Not the same)
            verify_overlay_result = main_page.compare(no_blending_preview, overlay_preview)
            verify_screen_result = main_page.compare(overlay_preview, screen_preview, similarity=0.98)

            case.result = (not verify_overlay_result) and (not verify_screen_result)

        # [L318] 4.2 Tools > Blending Mode > Video
        with uuid("5bc6914b-b112-40e7-ad78-69df9425fb16") as case:
            # Select track3, first clip
            timeline_operation_page.select_timeline_media(track_index=4, clip_index=0)

            # Set timecode
            main_page.set_timeline_timecode('00_00_03_00')
            time.sleep(DELAY_TIME * 2)
            difference_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # First : Enter Blending Mode
            tips_area_page.tools.select_Blending_Mode()
            time.sleep(DELAY_TIME * 2)
            blending_mode_page.set_blending_mode('Normal')
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME)
            normal_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Second : Enter Blending Mode -----
            tips_area_page.tools.select_Blending_Mode()
            time.sleep(DELAY_TIME * 2)
            blending_mode_page.set_blending_mode('Multiply')
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME)
            multiply_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Preview should be updated (Not the same)
            verify_normal_result = main_page.compare(difference_preview, normal_preview)
            verify_multiply_result = main_page.compare(normal_preview, multiply_preview)

            case.result = (not verify_normal_result) and (not verify_multiply_result)

        # [L310] 4.2 Tools > Video / Audio in Reverse > Tick
        with uuid("bf0eaa18-6d18-4853-aab6-71b55d267007") as case:
            # Apply (Video / Audio in Reverse)
            tips_area_page.tools.select_Video_in_Reverse(skip=1)
            time.sleep(DELAY_TIME * 2)
            reverse_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                 file_name=Auto_Ground_Truth_Folder + 'L310.png')
            check_result = precut_page.compare(Ground_Truth_Folder + 'L310.png', reverse_preview)

            case.result = check_result

        # [L311] 4.2 Tools > Video / Audio in Reverse > UnTick
        with uuid("2aa40a98-c103-4394-8c49-0ab946b8a96b") as case:
            # Apply (Video / Audio in Reverse)
            tips_area_page.tools.select_Video_in_Reverse(skip=1)
            time.sleep(DELAY_TIME * 2)
            no_reverse_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            check_result = precut_page.compare(no_reverse_preview, multiply_preview)

            case.result = check_result

        # [L322] 4.2 Tools > Audio Editor > Set Channel
        with uuid("3d06fc81-911c-4ac8-85a7-79111d7f7cb5") as case:
            # Click [Audio Editor]
            tips_area_page.tools.select_Audio_Editor()
            time.sleep(DELAY_TIME * 5)
            default_two_channel_preview = main_page.snapshot(locator=L.audio_editing.editor_window.preview_only_two_channel)
            logger(default_two_channel_preview)

            # Click [Edit Single Channel]
            audio_editing_page.audio_editor.switch_single_channel('yes')
            time.sleep(DELAY_TIME * 3)
            switch_single_channel_preview = main_page.snapshot(locator=L.audio_editing.editor_window.preview_only_two_channel)
            logger(switch_single_channel_preview)

            # Can switch to single
            check_no_update = main_page.compare(default_two_channel_preview, switch_single_channel_preview)
            logger(check_no_update)
            case.result = not check_no_update

        # [L321] 4.2 Tools > Audio Editor > Apply each adjustment function
        with uuid("902dbff1-18ec-4175-b29e-a41c53183ccc") as case:
            # Open (Special Effect) Phone > Apply
            check_result = audio_editing_page.audio_editor.open_special_effect_phone()
            logger(check_result)

            # Click [Apply] on Effect:Phone
            check_result = audio_editing_page.audio_editor.apply_phone_effect()
            logger(check_result)

            apply_phone_effect_preview = main_page.snapshot(locator=L.audio_editing.editor_window.preview_only_two_channel)

            # Verify step: waveform no update
            check_no_update = main_page.compare(apply_phone_effect_preview, switch_single_channel_preview, similarity=0.99)
            logger(check_no_update)
            case.result = not check_no_update

        # [L323] 4.2 Tools > Audio Editor > Check Preview
        with uuid("cafca61b-b8cf-4517-8996-17744a054d46") as case:
            default_timecode = audio_editing_page.audio_editor.get_current_timecode()
            logger(default_timecode)

            # Click [Space] to preview
            main_page.press_space_key()

            # Delay 1s
            time.sleep(DELAY_TIME * 2)

            # Click [Space] to Pause preview
            main_page.press_space_key()

            current_timecode = audio_editing_page.audio_editor.get_current_timecode()
            logger(current_timecode)

            # Verify Step:
            if default_timecode != current_timecode:
                case.result = True
            else:
                case.result = False

        # [L325] 4.2 Tools > Audio Editor > Apply (Result is correct in timeline after apply)
        with uuid("d3e2bba3-2613-439c-bdab-f2a5ff15071d") as case:
            # Click [OK] then apply (Audio Editor) then back to timeline
            check_ok_button = audio_editing_page.audio_editor.click_ok()

            apply_phone_effect_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            check_preview_update = main_page.compare(no_reverse_preview, apply_phone_effect_preview)
            case.result = check_preview_update and check_ok_button

        # Click timeline track 1
        main_page.timeline_select_track(1)

        # Click Stop
        playback_window_page.Edit_Timeline_PreviewOperation('Stop')

        # Save project:
        main_page.top_menu_bar_file_save_project_as()
        main_page.handle_save_file_dialog(name='test_case_1_1_25',
                                          folder_path=Test_Material_Folder + 'BFT_21_Stage1/')
        time.sleep(DELAY_TIME*3)

    # 3 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_26(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Insert sample audio (Mahoroba.mp3) to timeline
        main_page.select_library_icon_view_media('Mahoroba.mp3')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()

        # [L301] 4.2 Tools > Audio Smart Fit for Duration > Remix audio
        with uuid("fa162ec0-f523-404a-bc6b-f51cd7250a4f") as case:
            # Click Tools > (Smart Fit for Duration)
            click_button_result = tips_area_page.tools.select_smart_fit_duration()
            logger(click_button_result)

            # Switch to Original
            audio_editing_page.smart_fit.click_org_option()
            check_custom_value = audio_editing_page.smart_fit.get_custom_option_value()

            if check_custom_value == 0:
                untick_value = True
            else:
                untick_value = False
                logger(untick_value)

            # Snapshot for verify step
            original_waveform_preview = main_page.snapshot(locator=L.audio_editing.smart_fit.waveform_area)
            time.sleep(DELAY_TIME * 2)

            # Click radio button of [Custom Duration]
            audio_editing_page.smart_fit.click_custom_option()

            # Set custom new duration
            audio_editing_page.smart_fit.set_custom_new_duration('00_01_03_00')
            time.sleep(DELAY_TIME * 2)
            custom_waveform_preview = main_page.snapshot(locator=L.audio_editing.smart_fit.waveform_area)
            time.sleep(DELAY_TIME * 2)

            check_no_update = main_page.compare(original_waveform_preview, custom_waveform_preview)
            logger(check_no_update)

            case.result = (not check_no_update) and untick_value

        # [L302] 4.2 Tools > Audio Smart Fit for Duration > Preview
        with uuid("7d60615e-c270-4b9c-b30c-d3cc5f8fde31") as case:
            # Get current timecode
            default_timecode = audio_editing_page.smart_fit.get_current_timecode()
            logger(default_timecode)

            if default_timecode == '00:00:00:00':
                default_status = True
            else:
                default_status = False
                logger(default_timecode)

            # Click space to play preview
            main_page.press_space_key()

            time.sleep(DELAY_TIME *5)
            # Click space to pause preview
            main_page.press_space_key()

            # Get current timecode
            after_play_timecode = audio_editing_page.smart_fit.get_current_timecode()
            logger(after_play_timecode)

            if after_play_timecode != default_timecode:
                check_play = True
            else:
                check_play = False
                logger(check_play)

            case.result = check_play and default_status

        # [L303] 4.2 Tools > Audio Smart Fit for Duration > Apply result to timeline clip correctly
        with uuid("c655ce1a-0489-429b-a860-f06b764a254e") as case:
            result = audio_editing_page.smart_fit.click_ok()
            logger(result)

            # Verify Step:
            # Set timecode
            main_page.set_timeline_timecode('00_99_99_00')
            time.sleep(DELAY_TIME * 5)

            current_timecode = playback_window_page.get_timecode_slidebar()
            if current_timecode == '00:01:03:00':
                check_apply = True
            else:
                check_apply = False
                logger(current_timecode)

            case.result = result and check_apply

        # Remove the generate (Remix file)
        main_page.clear_remix_file('Mahoroba_remix.wav')

    # 9 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_27(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open project: test_case_1_1_25
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_25.pds')
        main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')

        # [L327] 4.3 Fix / Enhance > Enter [Fix / Enhance] page with each clip
        with uuid("d0a1e193-d13f-4e18-9ac8-e04924cfd021") as case:
            # Select track1, first clip
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)

            # Enter (Fix / Enhance]
            main_page.tips_area_click_fix_enhance()

            # Verify step:
            case.result = fix_enhance_page.is_in_fix_enhance()

        # [L329] 4.3 Fix / Enhance > Fix > Apply [Lighting Adjustment]
        with uuid("8f26c266-40d9-4a72-9403-a9c90974cad1") as case:
            # Enable (Lighting Adjustment)
            fix_enhance_page.fix.enable_lighting_adjustment()

            # Enable (Extreme backlight)
            fix_enhance_page.fix.lighting_adjustment.enable_extreme_backlight(True)

            # Set value = 75
            fix_enhance_page.fix.lighting_adjustment.extreme_backlight.set_value(75)

            # Verify Step:
            check_checkbox = fix_enhance_page.fix.lighting_adjustment.get_extreme_backlight()

            current_value = fix_enhance_page.fix.lighting_adjustment.extreme_backlight.get_value()

            if current_value == '75':
                apply_value = True
            else:
                apply_value = False
                logger(current_value)

            case.result = check_checkbox and apply_value

        # [L330] 4.3 Fix / Enhance > Fix > Apply [White Balance]
        with uuid("307558b2-3c13-4520-9004-003730df8f4c") as case:
            # Enable (White Balance)
            fix_enhance_page.fix.enable_white_balance(True)

            # Set (Color temperature) value = 90
            fix_enhance_page.fix.white_balance.color_temperature.set_value(90)
            time.sleep(DELAY_TIME)

            # Verify Step:
            # Check preview update
            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                 file_name=Auto_Ground_Truth_Folder + 'L330.png')
            check_result = precut_page.compare(Ground_Truth_Folder + 'L330.png', current_preview)

            case.result = check_result

        # [L342] 4.3 Fix / Enhance > Compare in split preview
        with uuid("67ccfb1a-5549-4d28-8fed-20757654c48d") as case:
            # Enable (Compare in split preview)
            fix_enhance_page.set_check_compare_in_split_preview(1)
            time.sleep(DELAY_TIME * 2)

            # Verify Step:
            # Check preview update
            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                 file_name=Auto_Ground_Truth_Folder + 'L342.png')
            check_compare_mode = precut_page.compare(Ground_Truth_Folder + 'L342.png', current_preview)

            # Disable (Compare in split preview)
            fix_enhance_page.set_check_compare_in_split_preview(0)
            time.sleep(DELAY_TIME * 2)
            no_compare_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            check_no_compare_mode = precut_page.compare(Ground_Truth_Folder + 'L330.png', no_compare_preview)

            case.result = check_compare_mode and check_no_compare_mode

        # [L336] 4.3 Fix / Enhance > Enhance > Apply [Color Adjustment]
        with uuid("3eaa9f75-2ff7-4f74-9d67-49badebcaa8b") as case:
            # Select track2, 3rd clip:4978895
            timeline_operation_page.select_timeline_media(track_index=2, clip_index=2)

            # Enable (Color Adjustment)
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Apply Exposure = 182, Hue = 36
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(182)
            fix_enhance_page.enhance.color_adjustment.hue.set_value(36)
            time.sleep(DELAY_TIME*2)

            # Verify Step:
            check_exposure = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            if check_exposure == '182':
                apply_exposure = True
            else:
                apply_exposure = False

            check_hue = fix_enhance_page.enhance.color_adjustment.hue.get_value()
            if check_hue == '36':
                apply_hue = True
            else:
                apply_hue = False

            case.result = apply_exposure and apply_hue

        # [L339] 4.3 Fix / Enhance > Enhance > Apply [Split Toning]
        with uuid("3dedd39f-8afd-4a17-89cc-dfa0e6da72ec") as case:
            # Enable (Split Toning)
            fix_enhance_page.enhance.enable_split_toning()

            # Apply Balance = 53
            fix_enhance_page.enhance.split_toning.balance.set_value(53)

            # Apply Shadow : Hue = 291, Saturation = 89
            fix_enhance_page.enhance.split_toning.shadow.hue.set_value(291)
            fix_enhance_page.enhance.split_toning.shadow.saturation.set_value(89)
            time.sleep(DELAY_TIME*2)

            # Verify Step:
            # Check preview update
            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                 file_name=Auto_Ground_Truth_Folder + 'L339.png')
            check_result = precut_page.compare(Ground_Truth_Folder + 'L339.png', current_preview)

            case.result = check_result

        # [L328] 4.3 Fix / Enhance > Enter [Fix / Enhance] w/ Image clip
        with uuid("c91a00e7-fe55-412a-892b-15d281d69304") as case:
            # Close x  to leave (Fix/Enhance) page
            fix_enhance_page.click_close()

            # Select timeline track3
            main_page.timeline_select_track(3)

            # Insert Sport 01 to track3
            main_page.select_library_icon_view_media('Sport 01.jpg')
            time.sleep(DELAY_TIME * 2)
            media_room_page.library_clip_context_menu_insert_on_selected_track()

            # Enter (Fix / Enhance]
            main_page.tips_area_click_fix_enhance()

            # Verify step:
            case.result = fix_enhance_page.is_in_fix_enhance()

        # [L332] 4.3 Fix / Enhance > Fix > Apply Lens Correction
        with uuid("79967191-3497-482f-8767-6ab238b50b79") as case:
            fix_enhance_page.fix.switch_to_lens_correction()

            # Select marker type : Garmin
            fix_enhance_page.fix.lens_correction.select_marker_type('Garmin')
            time.sleep(DELAY_TIME)

            # Set fish eye distortion
            fix_enhance_page.fix.lens_correction.fisheye_distortion.set_value(75)

            # Verify step:
            get_marker_type = fix_enhance_page.fix.lens_correction.get_marker_type()
            logger(get_marker_type)

            if get_marker_type == 'Garmin':
                check_type = True
            else:
                check_type = False

            get_current_value = fix_enhance_page.fix.lens_correction.fisheye_distortion.get_value()
            if get_current_value == '75':
                apply_value = True
            else:
                apply_value = False

            case.result = check_type and apply_value

        # [L340] 4.3 Fix / Enhance > Enhance > Apply HDR Effect
        with uuid("4bd05dc1-8871-4893-a6e2-ac9933173ca3") as case:
            fix_enhance_page.enhance.switch_to_hdr_effect()

            # Set Glow : Strength = 89 / Radius = 31 / Balance = -17
            fix_enhance_page.enhance.hdr_effect.glow.strength.set_value(89)

            fix_enhance_page.enhance.hdr_effect.glow.radius.adjust_slider(31)
            fix_enhance_page.enhance.hdr_effect.glow.balance.set_value(-17)
            time.sleep(DELAY_TIME * 3)

            # Verify Step:
            # Check preview update
            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                 file_name=Auto_Ground_Truth_Folder + 'L340.png')
            check_result = precut_page.compare(Ground_Truth_Folder + 'L340.png', current_preview)

            case.result = check_result

        # Save project:
        main_page.top_menu_bar_file_save_project_as()
        main_page.handle_save_file_dialog(name='test_case_1_1_27',
                                          folder_path=Test_Material_Folder + 'BFT_21_Stage1/')
        time.sleep(DELAY_TIME*3)

    # 2 uuid (Color Match locator wait for RD hardcode)
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_28(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Insert (Sport 02.jpg) & (Travel 01.jpg) to track1
        main_page.select_library_icon_view_media('Sport 02.jpg')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()

        main_page.select_library_icon_view_media('Travel 01.jpg')
        time.sleep(DELAY_TIME * 2)
        tips_area_page.click_TipsArea_btn_insert(2)

        # [L346] 4.3 Fix / Enhance > Apply to All
        # 2023/08/01: Due to v22.0.5528 Fix / Enhance remove the button of [Apply to All]
        # Select timeline clip: (Travel 01.jpg) then enter (Fix / Enhance]
        main_page.tips_area_click_fix_enhance()

        # Enable HDR
        fix_enhance_page.enhance.enable_hdr_effect()

        # Select timeline clip: (Sport 02.jpg) > Set HDR (Edge.Strength = 65)
        timeline_operation_page.select_timeline_media(track_index=0, clip_index=1)
        time.sleep(DELAY_TIME)

        fix_enhance_page.enhance.hdr_effect.edge.strength.set_value(65)
        time.sleep(DELAY_TIME)

        # [L338] 4.3 Fix / Enhance > Enhance > Color Match
        with uuid("63d5644b-8272-4693-a015-75f8da7f239d") as case:
            # Select timeline clip: Travel 01.jpg  then enter Color Match
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.switch_to_color_match()

            # Click [Color Match]
            fix_enhance_page.enhance.color_match.click_color_match_button()

            # Verify Step:
            default_status = fix_enhance_page.enhance.color_match.get_match_color_status()
            if default_status == False:
                check_status = True
            else:
                check_status = False
                logger(check_status)

            # Select reference clip: (Sport 02.jpg)
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=1)
            time.sleep(DELAY_TIME)

            # Click [Match Color]
            fix_enhance_page.enhance.color_match.click_match_color()

            # Check setting update
            current_setting = main_page.snapshot(locator=L.fix_enhance.enhance.color_match.setting_scroll_view,
                                                 file_name=Auto_Ground_Truth_Folder + 'L338.png')
            check_setting_update = precut_page.compare(Ground_Truth_Folder + 'L338.png', current_setting)

            case.result = check_status and check_setting_update

        # [L343] 4.3 Fix / Enhance > Preview is correct
        with uuid("00fdc131-d451-496f-8629-31b76be21d67") as case:

            # Click [x] to apply change
            check_apply = fix_enhance_page.enhance.color_match.click_close('Yes')
            logger(check_apply)

            # Check preview update
            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                 file_name=Auto_Ground_Truth_Folder + 'L343.png')
            check_preview_update = precut_page.compare(Ground_Truth_Folder + 'L343.png', current_preview)
            case.result = check_preview_update

    # 8 uuid
    # Handle motion tracker
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_29(self):
        # clear AI module
        main_page.clear_AI_module()

        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Insert sample video
        main_page.select_library_icon_view_media('Skateboard 03.mp4')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()

        # Click TipsArea [Tools] button
        main_page.click(L.tips_area.button.btn_Tools)

        # Select (Video Speed)
        main_page.select_right_click_menu('Motion Tracker')

        # Check download AI module
        self.check_downloading_AI_module()

        # If find the tracker 2, removing the tracker 2
        motion_tracker_page.remove_tracker2()

        # [L312] 4.2 Tools > Motion Tracker > Object Tracking
        with uuid("c7d17581-dfea-4f5f-9765-82eb268dd5c7") as case:
            check_open_status = motion_tracker_page.is_in_motion_tracker()

            check_track = motion_tracker_page.click_object_track()

            case.result = check_open_status and check_track

        # [L313] 4.2 Tools > Motion Tracker > Add Text Object
        with uuid("b89b4237-429d-4d95-a76d-a1a769785e4d") as case:
            motion_tracker_page.add_title_button()
            motion_tracker_page.edit_title('ぱざだたタ../*')
            motion_tracker_page.change_title_color('CE2E47')
            time.sleep(DELAY_TIME)

            # Check preview
            current_preview = main_page.snapshot(locator=L.motion_tracker.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'L313.png')
            check_preview_update = precut_page.compare(Ground_Truth_Folder + 'L313.png', current_preview)
            case.result = check_preview_update

        # [L314] 4.2 Tools > Motion Tracker > Add Pip Object
        with uuid("8a5522c5-6f2f-4e71-9d0b-d7d7f575bc48") as case:
            motion_tracker_page.add_pip_button()
            motion_tracker_page.import_from_hard_drive(Test_Material_Folder + 'Video_Audio_In_Reverse/Sample.png')

            # Check preview
            current_preview = main_page.snapshot(locator=L.motion_tracker.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'L314.png')
            check_preview_update = precut_page.compare(Ground_Truth_Folder + 'L314.png', current_preview)
            case.result = check_preview_update

        # [L316] 4.2 Tools > Motion Tracker > Preview
        with uuid("682f463a-bed9-4eec-a15b-9ad4b7752814") as case:
            motion_tracker_page.set_timecode('00_00_06_14')
            time.sleep(DELAY_TIME*2)

            # Check preview
            current_preview = main_page.snapshot(locator=L.motion_tracker.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'L316.png')
            check_preview_update = precut_page.compare(Ground_Truth_Folder + 'L316.png', current_preview, similarity=0.97)
            case.result = check_preview_update


        # [L315] 4.2 Tools > Motion Tracker > Add Effect
        with uuid("41dce21f-2418-43eb-a16c-0d4be7b0d8de") as case:
            # Add a tracker (Tracker 2)
            motion_tracker_page.add_a_tracker()
            time.sleep(DELAY_TIME)

            # Click [Track] of Tracker 2 > Add Effect button
            check_track = motion_tracker_page.click_object_track()
            motion_tracker_page.add_effect_button()

            motion_tracker_page.set_timecode('00_00_08_01')
            time.sleep(DELAY_TIME*2)

            # Check preview
            current_preview = main_page.snapshot(locator=L.motion_tracker.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'L315.png')
            check_preview_update = precut_page.compare(Ground_Truth_Folder + 'L315.png', current_preview, similarity=0.97)
            case.result = check_preview_update

        # [L317] 4.2 Tools > Motion Tracker > Apply and return to timeline
        with uuid("24111d09-bf67-427b-91d4-2f529e1e5d19") as case:
            check_result = motion_tracker_page.click_ok()
            time.sleep(DELAY_TIME * 2)
            # Set timecode
            main_page.set_timeline_timecode('00_00_03_00')
            time.sleep(DELAY_TIME * 2)

            # Check preview update
            current_3s_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view,
                                                 file_name=Auto_Ground_Truth_Folder + 'L317.png')
            check_preview_update = precut_page.compare(Ground_Truth_Folder + 'L317.png', current_3s_preview)
            case.result = check_preview_update and check_result

        # [L348] 4.4 Keyframe > Fix Enhance > Lighting Adjustment (Degree)
        with uuid("959992a2-b8fc-4f65-afda-3f5a0dedc886") as case:
            # Select track 2 first clip (Sample.png)
            timeline_operation_page.select_timeline_media(track_index=2, clip_index=0)
            time.sleep(DELAY_TIME)

            # Click [Keyframe] on tips area
            tips_area_page.click_keyframe()

            # Unfold (Fix / Enhance)
            keyframe_room_page.fix_enhance.unfold_tab()

            # Get Lighting Adjustment (degree)
            current_degree = keyframe_room_page.fix_enhance.lighting_adjustment.degree.get_value()
            logger(current_degree)

            if current_degree == '50':
                default_value = True
            else:
                default_value = False

            # Set 1st keyframe of (00;00;03;00)
            keyframe_room_page.fix_enhance.lighting_adjustment.degree.set_value(70)

            # Set timecode
            main_page.set_timeline_timecode('00_00_07_10')
            time.sleep(DELAY_TIME * 2)

            # Set 2nd keyframe of (00;00;07;00)
            keyframe_room_page.fix_enhance.lighting_adjustment.degree.set_value(30)

            # Verify Step:
            # Get Lighting Adjustment (degree) on (00;00;07;00)
            current_degree = keyframe_room_page.fix_enhance.lighting_adjustment.degree.get_value()
            logger(current_degree)

            if current_degree == '30':
                second_apply = True
            else:
                second_apply = False

            # Click previous keyframe button
            keyframe_room_page.fix_enhance.lighting_adjustment.degree.previous_keyframe()
            time.sleep(DELAY_TIME)

            # Get Lighting Adjustment (degree) on (00;00;07;00)
            current_degree = keyframe_room_page.fix_enhance.lighting_adjustment.degree.get_value()
            logger(current_degree)

            if current_degree == '70':
                first_apply = True
            else:
                first_apply = False

            case.result = default_value and second_apply and first_apply

        # [L353] 4.4 Keyframe > Fix Enhance > White Balance
        with uuid("11f4e9ff-f7f1-4776-9424-9709cdeb7cb1") as case:
            # Set 1st keyframe of (00;00;03;00)
            keyframe_room_page.fix_enhance.white_balance.color_temperature.set_value(97)
            keyframe_room_page.fix_enhance.white_balance.tint.set_value(95)
            time.sleep(DELAY_TIME * 2)

            # Get White Balance (Color temperature)
            current_temperature = keyframe_room_page.fix_enhance.white_balance.color_temperature.get_value()
            logger(current_temperature)

            if current_temperature == '97':
                set_temp = True
            else:
                set_temp = False

            # Get White Balance (Tint)
            current_tint = keyframe_room_page.fix_enhance.white_balance.tint.get_value()
            logger(current_tint)

            if current_tint == '95':
                set_tint = True
            else:
                set_tint = False

            case.result = set_temp and set_tint

    # 9 uuid
    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_30(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # enter Title room
        main_page.enter_room(1)
        time.sleep(DELAY_TIME * 3)

        # Search library content
        media_room_page.search_library('Default')
        time.sleep(DELAY_TIME * 2)

        main_page.select_library_icon_view_media('Default')
        main_page.double_click()
        time.sleep(DELAY_TIME * 3)

        # [L138] 3.2 Title Designer (general template) > Set in [Object] > Font Face with Gradient Color
        with uuid("2112849e-965c-4704-a202-08ebf2b35550") as case:

            initial_title_preview = main_page.snapshot(locator=L.title_designer.area.view_title)

            # Font Face > (Fill Type) set Gradient Color
            title_designer_page.apply_font_face_fill_type_to_gradient()

            # Gradient style set Corner
            title_designer_page.apply_font_face_gradient_style(3)
            time.sleep(DELAY_TIME)
            title_designer_page.drag_object_vertical_slider(0.64)

            # Set 4 gradient color
            title_designer_page.apply_font_face_4_color(left_top_hex='FFCE24', right_top_hex='34FFFF',
                                                        left_bottom_hex='6E0913', right_bottom_hex='AD1BBD')

            # Verify Step:
            title_gradient_group = main_page.snapshot(locator=L.title_designer.font_face.four_color_gradient_group,
                                                    file_name=Auto_Ground_Truth_Folder + 'L138.png')
            check_gradient_group_update = precut_page.compare(Ground_Truth_Folder + 'L138.png', title_gradient_group)

            title_apply_gradient = main_page.snapshot(locator=L.title_designer.area.view_title)
            check_title_no_update = main_page.compare(initial_title_preview, title_apply_gradient)
            case.result = check_gradient_group_update and (not check_title_no_update)

            # Click [Canel] without save update
            title_designer_page.click_cancel(1)

        # [L335] 4.3 Fix/ Enhance > Fix > Wind Removal
        with uuid("6a3438b6-dbec-4838-9228-d6c1b6775bdc") as case:
            # enter media room
            main_page.enter_room(0)
            time.sleep(DELAY_TIME * 3)

            # Insert audio (Speaking Out.mp3) to timeline
            main_page.select_library_icon_view_media('Speaking Out.mp3')
            time.sleep(DELAY_TIME * 2)
            media_room_page.library_clip_context_menu_insert_on_selected_track()

            # Set timecode
            main_page.set_timeline_timecode('00_00_14_00')
            time.sleep(DELAY_TIME * 2)

            # Click [Split] (trim Speaking Out.mp3 to 14 sec)
            main_page.tips_area_click_split()

            # Select timeline track 1 : Second clip then remove it
            timeline_operation_page.select_timeline_media(track_index=1, clip_index=1)
            time.sleep(DELAY_TIME)
            main_page.press_backspace_key()

            timeline_operation_page.select_timeline_media(track_index=1, clip_index=0)
            time.sleep(DELAY_TIME)

            # Enter (Fix/Enhance) > Wind Removal
            main_page.tips_area_click_fix_enhance()
            fix_enhance_page.fix.switch_to_wind_removal()
            time.sleep(DELAY_TIME)

            # Click [Wind Removal]
            fix_enhance_page.fix.click_wind_removal()

            # Check download AI module
            self.check_downloading_AI_module()
            logger('9492')

            # Click [Apply]
            check_result = fix_enhance_page.fix.click_wind_removal_apply()

            # Verify step:
            if main_page.exist(L.fix_enhance.fix.wind_removal.main_window):
                verify_result = False
            else:
                verify_result = True
            case.result = check_result and verify_result


        # [L334] 4.3 Fix/ Enhance > Fix > Apply [Audio Denoise]
        with uuid("d49033f8-19c7-4ec1-b89e-a71d2f4f7171") as case:
            # Enter (Fix/Enhance) > Audio Denoise
            main_page.tips_area_click_fix_enhance()
            fix_enhance_page.fix.switch_to_audio_denoise()
            time.sleep(DELAY_TIME)

            # Get (Noise type)
            get_type = fix_enhance_page.fix.audio_denoise.get_noise_type()
            if get_type == 'Stationary noise':
                get_type_result = True
            else:
                get_type_result = False

            # Set Degree to 77
            fix_enhance_page.fix.audio_denoise.degree.adjust_slider(77)

            # Play timeline preview
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 5)
            playback_window_page.Edit_Timeline_PreviewOperation('STOP')

            # Set Degree to 75
            fix_enhance_page.fix.audio_denoise.degree.click_minus(2)
            time.sleep(DELAY_TIME * 2)

            # Get (Noise type)
            get_type = fix_enhance_page.fix.audio_denoise.degree.get_value()
            if get_type == '75':
                set_degree_result = True
            else:
                set_degree_result = False

            case.result = get_type_result and set_degree_result

        # [L405] 5.1 Produce 2D > Audio File > Select [Format] > AIFF
        with uuid("8e24c00f-eae2-4daa-beff-d638a97d974b") as case:
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            # File Format: Audio file
            produce_page.local.select_file_format('audio')

            # Select file extension: AIFF
            produce_page.local.select_file_extension('aiff')

            # Get produced file name
            explore_aiff_file = produce_page.get_produced_filename()
            logger(explore_aiff_file)

            # Start : produce
            produce_page.click(L.produce.btn_start_produce)
            time.sleep(DELAY_TIME * 5)

            # Back to Edit
            produce_page.click_back_to_edit(4)

            # Verify step:
            check_explore_file = main_page.select_library_icon_view_media(explore_aiff_file)
            logger(check_explore_file)

            # Remove the produced file
            if check_explore_file:
                main_page.select_library_icon_view_media(explore_aiff_file)
                media_room_page.library_clip_context_menu_move_to_trash_can()

            case.result = check_explore_file

        # [L403] 5.1 Produce 2D > Audio File > Select [Format] > M4A
        with uuid("6133a8dd-e9d3-487a-9558-793d06463611") as case:
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            # File Format: Audio file
            produce_page.local.select_file_format('audio')

            # Select file extension: M4A
            produce_page.local.select_file_extension('m4a')

            # Get produced file name
            explore_m4a_file = produce_page.get_produced_filename()
            logger(explore_m4a_file)

            # Start : produce
            produce_page.click(L.produce.btn_start_produce)
            time.sleep(DELAY_TIME * 5)

            # Back to Edit
            produce_page.click_back_to_edit(4)

            # Verify step:
            check_explore_file = main_page.select_library_icon_view_media(explore_m4a_file)
            logger(check_explore_file)

            # Remove the produced file
            if check_explore_file:
                main_page.select_library_icon_view_media(explore_m4a_file)
                media_room_page.library_clip_context_menu_move_to_trash_can()

            # Produce file name should be updated
            if explore_m4a_file != explore_aiff_file:
                set_file_extenstion = True
            else:
                set_file_extenstion = False

            case.result = check_explore_file and set_file_extenstion

        # [L404] 5.1 Produce 2D > Audio File > Select [Format] > WAV
        with uuid("ebb092ce-34bc-4958-9c53-c76c464b2277") as case:

            main_page.click_produce()
            produce_page.check_enter_produce_page()

            # File Format: Audio file
            produce_page.local.select_file_format('audio')

            # Select file extension: WAV
            produce_page.local.select_file_extension('wav')

            # Get produced file name
            explore_wav_file = produce_page.get_produced_filename()
            logger(explore_wav_file)

            # [L406] 5.1 Produce 2D > Audio File > Upload a copy to cloud
            with uuid("9590c2e7-831c-4cae-b19c-80fa62bb4411") as case:

                produce_page.local.set_check_upload_copy_to_cyberlink_cloud(is_check=1)
                time.sleep(DELAY_TIME * 2)
                current_upload_checkbox = produce_page.local.check_visible_upload_copy_to_cyberlink_cloud()
                logger(current_upload_checkbox)
                case.result = current_upload_checkbox

                time.sleep(DELAY_TIME * 2)

            # Start : produce
            produce_page.click(L.produce.btn_start_produce)
            time.sleep(DELAY_TIME * 5)

            # wait for video upload to cloud
            for x in range(60):
                back_btn = main_page.exist(L.produce.btn_back_to_edit_after_upload_cl)
                if back_btn:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click(L.produce.btn_back_to_edit_after_upload_cl)
            time.sleep(DELAY_TIME * 5)

            # Verify step:
            check_explore_file = main_page.select_library_icon_view_media(explore_wav_file)
            logger(check_explore_file)

            # Insert the produce audio to timeline
            tips_area_page.click_TipsArea_btn_insert(1)

            # Verify Step:
            # Enter Audio Mixing Room
            main_page.enter_room(6)
            time.sleep(DELAY_TIME * 3)

            # Play timeline preview
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            check_waveform_update = main_page.Check_PreviewWindow_is_different(area=L.audio_mixing_room.audio_mixing_track, sec=2)

            time.sleep(DELAY_TIME)
            playback_window_page.Edit_Timeline_PreviewOperation('STOP')

            # Remove the produced file
            # Back to media room
            main_page.enter_room(0)
            time.sleep(DELAY_TIME *3)
            if check_explore_file:
                main_page.select_library_icon_view_media(explore_wav_file)
                media_room_page.library_clip_context_menu_move_to_trash_can()

            case.result = check_waveform_update and check_explore_file
            logger(case.result)
            time.sleep(DELAY_TIME * 3)
            # Verify step2: Remove the upload audio
            # Click Import media > (Download media from Cyberlink cloud)
            media_room_page.import_media_from_cyberlink_cloud()
            time.sleep(DELAY_TIME * 3)

            # Switch to music page
            import_media_from_cloud_page.switch_to_music_page()
            time.sleep(DELAY_TIME * 2)

            # Double click to enter PowerDirector folder
            import_media_from_cloud_page.select_content_in_folder_level(folder_index=0, click_times=2)

            # Search explore_file
            import_media_from_cloud_page.input_text_in_seacrh_library('Produce')
            time.sleep(DELAY_TIME)

            # Tick 'Select all'
            import_media_from_cloud_page.tap_select_deselect_all_btn()

            # Check remove button
            if main_page.exist(L.import_downloaded_media_from_cl.delete_btn).AXEnabled:
                # Remove audio
                import_media_from_cloud_page.tap_remove_btn()
                time.sleep(DELAY_TIME)

            # Close (Download window)
            for x in range(3):
                main_page.press_esc_key()
                time.sleep(DELAY_TIME*0.5)

        # [L361] 4.4 Keyframe > Volume
        with uuid("8f39828c-1845-45a5-bb5f-aaac50c1397e") as case:
            timeline_operation_page.select_timeline_media(track_index=1, clip_index=0)

            # Click [Keyframe] on tips area
            tips_area_page.click_keyframe()

            # Unfold Volume
            keyframe_room_page.volume.unfold_tab()

            default_value = keyframe_room_page.volume.get_value()
            if default_value == '0.0':
                check_default = True
            else:
                check_default = False
                logger(check_default)

            keyframe_room_page.volume.set_value(9.1)
            time.sleep(DELAY_TIME)
            current_value = keyframe_room_page.volume.get_value()
            if current_value == '9.1':
                applied_default = True
            else:
                applied_default = False
                logger(applied_default)

            case.result = check_default and applied_default

        # [L350] 4.4 Keyframe > Fix/ Enhance > Fix > Adjust [Audio Denoise]
        with uuid("ebc3f1ce-4552-4e7d-9e9e-54fe152f66dd") as case:
            # Unfold (Fix / Enhance)
            keyframe_room_page.fix_enhance.unfold_tab()

            # Audio Denoise > Get current (Degree)
            current_value = keyframe_room_page.fix_enhance.audio_denoise.degree.get_value()

            if current_value == '75':
                check_value = True
            else:
                check_value = False
                logger(current_value)

            # Adjust Degree = 84
            keyframe_room_page.fix_enhance.audio_denoise.degree.click_stepper_up(9)
            time.sleep(DELAY_TIME)

            # Audio Denoise > Get current (Degree)
            current_value = keyframe_room_page.fix_enhance.audio_denoise.degree.get_value()

            if current_value == '84':
                edit_value = True
            else:
                edit_value = False
                logger(current_value)

            case.result = check_value and edit_value

    # 12 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_31(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open project: test_case_1_1_27
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_27.pds')
        main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')
        time.sleep(DELAY_TIME * 5)
        # Disable track 1 and track 3 (Only Enable track2)
        timeline_operation_page.edit_specific_video_track_set_enable(track_index=2, option=1)

        # [L345] 4.3 Fix/Enhance > Keyframe
        with uuid("ad0364e2-5628-480a-9e2f-46c9c9b8abb8") as case:
            # Select track2 3rd clip
            timeline_operation_page.select_timeline_media(track_index=2, clip_index=2)

            # Click [Keyframe] on tips area button
            case.result = tips_area_page.click_keyframe()

        # [L354] 4.4 Keyframe > Fix / Enhance > Adjust [Split Toning]
        with uuid("b855bdd0-ea10-44a5-bd08-77b13747d9f5") as case:
            # Unfold Fix/ Enhance
            keyframe_room_page.fix_enhance.unfold_tab()
            keyframe_room_page.drag_scroll_bar(0.77)
            time.sleep(DELAY_TIME)

            # Add keyframe of (Shadow Hue) on 00:00:00:00
            keyframe_room_page.fix_enhance.split_toning.shadow_hue.add_remove_keyframe()

            # Set timecode
            main_page.set_timeline_timecode('00_00_02_00')
            time.sleep(DELAY_TIME * 2)

            # Add second keyframe of (Shadow Hue) on 00:00:02:00 with set value = 0
            keyframe_room_page.fix_enhance.split_toning.shadow_hue.set_slider(0)
            time.sleep(DELAY_TIME)

            # Click previous keyframe then click next keyframe
            keyframe_room_page.fix_enhance.split_toning.shadow_hue.previous_keyframe()

            time.sleep(DELAY_TIME)
            keyframe_room_page.fix_enhance.split_toning.shadow_hue.next_keyframe()

            # Get timeline timecode
            current_timecode = playback_window_page.get_timecode_slidebar()
            if current_timecode == '00:00:02:00':
                check_apply = True
            else:
                check_apply = False

            # Verify value
            current_value = keyframe_room_page.fix_enhance.split_toning.shadow_hue.get_value()
            if current_value == '0':
                applied_value = True
            else:
                applied_value = False

            case.result = check_apply and applied_value

        # [L344] 4.3 Fix / Enhance > Reset
        with uuid("702cd916-959f-4504-9384-3ff7442915aa") as case:
            # Click previous keyframe (Switch to 0s)
            keyframe_room_page.fix_enhance.split_toning.shadow_hue.previous_keyframe()

            # Enter Fix / Enhance page
            tips_area_page.click_fix_enhance()
            time.sleep(DELAY_TIME)

            # Switch to (Split toning)
            fix_enhance_page.enhance.switch_to_split_toning()
            time.sleep(DELAY_TIME)

            # Click [Reset] button
            fix_enhance_page.click_reset()

            # check warning message: Thus operation resets all the keyframes in this effect.
            # Do you want to continue? Option: (Yes/ No)
            check_warning = main_page.is_exist(L.base.confirm_dialog.main_window)
            if not check_warning:
                case.result = False
            else:
                # click yes
                main_page.click(L.base.confirm_dialog.btn_yes)

            time.sleep(DELAY_TIME * 2)

            # Verify Step:
            current_balance = fix_enhance_page.enhance.split_toning.balance.get_value()
            current_hue = fix_enhance_page.enhance.split_toning.shadow.hue.get_value()
            current_saturation = fix_enhance_page.enhance.split_toning.shadow.saturation.get_value()

            if (current_balance == '0') and (current_hue == '0') and (current_saturation == '0'):
                case.result = True
            else:
                case.result = False
                logger(f'current_balance = {current_balance}, current_hue = {current_hue}, current_saturation = {current_saturation}')

        # [L351] 4.4 Keyframe > Fix / Enhance > Adjust [Color Adjustment]
        with uuid("3077f9c9-7194-4edc-b3e8-707495e22520") as case:
            # Click [Undo] : Split Toning (Balance) = 53, (Shadow.Hue) = 291, (Shadow.Saturation) = 89
            main_page.click_undo()
            time.sleep(DELAY_TIME)

            # Switch to (Color Adjustment) on fix/enhance page
            fix_enhance_page.enhance.switch_to_color_adjustment()
            time.sleep(DELAY_TIME)
            # Enter Keyframe page
            tips_area_page.click_keyframe()

            # Scroll down to Color Adjustment
            keyframe_room_page.drag_scroll_bar(0.34)

            # Add 1st keyframe on (Color Adjustment).Exposure and (Color Adjustment).Hue on (00;00;00;00)
            keyframe_room_page.fix_enhance.color_adjustment.exposure.add_remove_keyframe()
            keyframe_room_page.fix_enhance.color_adjustment.hue.add_remove_keyframe()

            # Set timecode
            main_page.set_timeline_timecode('00_00_03_00')
            time.sleep(DELAY_TIME * 2)

            # Add 2nd keyframe on (Color Adjustment).Exposure and (Color Adjustment).Hue on (00;00;03;00)
            keyframe_room_page.fix_enhance.color_adjustment.exposure.set_value(53)
            keyframe_room_page.fix_enhance.color_adjustment.hue.set_slider(182)
            time.sleep(DELAY_TIME * 2)

            # Set timecode
            main_page.set_timeline_timecode('00_00_01_22')
            time.sleep(DELAY_TIME * 2)

            # Verify Step:
            get_exposure = keyframe_room_page.fix_enhance.color_adjustment.exposure.get_value()
            get_hue = keyframe_room_page.fix_enhance.color_adjustment.hue.get_value()

            if get_exposure == '107':
                set_exposure = True
            else:
                set_exposure = False
                logger(get_exposure)

            if get_hue == '120':
                set_hue = True
            else:
                set_hue = False
                logger(set_hue)

            case.result = set_exposure and set_hue

        # [L356] 4.4 Keyframe > Clip Attribute > Position
        with uuid("e3a6c143-9a07-4385-a593-63b511cd213e") as case:
            # Fold (Fix/ Enhance) for Keyframe page
            keyframe_room_page.drag_scroll_bar(0)
            time.sleep(DELAY_TIME)
            keyframe_room_page.fix_enhance.unfold_tab(0)

            # Unfold (Clip Attribute) for Keyframe page
            keyframe_room_page.clip_attributes.unfold_tab()

            # Set position x = 0.4  / position y = 0.5 on (00;00:01;22)
            keyframe_room_page.clip_attributes.position.x.set_value(0.4)
            time.sleep(DELAY_TIME)

            # Set timeline
            main_page.set_timeline_timecode('00_00_03_12')

            # Set position x = 0.4  / position y = 0.71 on (00;00:03;12)
            keyframe_room_page.clip_attributes.position.y.set_value(0.71)
            time.sleep(DELAY_TIME)

            # Verify Step
            # Set timeline
            main_page.set_timeline_timecode('00_00_02_10')

            current_x = keyframe_room_page.clip_attributes.position.x.get_value()
            current_y = keyframe_room_page.clip_attributes.position.y.get_value()

            if current_x == '0.400':
                check_x = True
            else:
                check_x = False
                logger(current_x)

            if current_y == '0.576':
                check_y = True
            else:
                check_y = False
                logger(current_y)

            case.result = check_x and check_y

        # [L360] 4.4 Keyframe > Clip Attribute > Freeform
        with uuid("85a485fe-c64b-430a-8cd2-64bc82e15822") as case:
            keyframe_room_page.drag_scroll_bar(1)

            # Set Freeform top-right position y = 0.06 on (00;00;02;11)
            keyframe_room_page.clip_attributes.freeform.top_right_y.set_value(0.06)
            time.sleep(DELAY_TIME)

            # Set timeline
            main_page.set_timeline_timecode('00_00_00_00')
            # Set Freeform top-right position y = 0.9 on (00;00;00;00)
            keyframe_room_page.clip_attributes.freeform.top_right_y.set_value(0.9)
            time.sleep(DELAY_TIME)

            # Verify Step:
            current_1st_y_value = keyframe_room_page.clip_attributes.freeform.top_right_y.get_value()
            if current_1st_y_value == '0.900':
                check_1st_result = True
            else:
                check_1st_result = False
                logger(current_1st_y_value)

            # click next keyframe of freeform
            keyframe_room_page.clip_attributes.freeform.next_keyframe()
            time.sleep(DELAY_TIME*2)

            current_2nd_y_value = keyframe_room_page.clip_attributes.freeform.top_right_y.get_value()
            if current_2nd_y_value == '0.060':
                check_2nd_result = True
            else:
                check_2nd_result = False
                logger(current_2nd_y_value)

            case.result = check_1st_result and check_2nd_result

        # [L359] 4.4 Keyframe > Clip Attribute > Rotate
        with uuid("87b99fc8-b634-4c8b-b04f-d153cc439a0c") as case:
            keyframe_room_page.drag_scroll_bar(0.77)

            # Add rotate keyframe : Degree = 0 on (00:00:02:10)
            keyframe_room_page.clip_attributes.rotation.add_remove_keyframe()

            # Set timeline
            main_page.set_timeline_timecode('00_00_01_00')
            time.sleep(DELAY_TIME)

            # Add rotate keyframe : Degree = 130 on (00:00:01:00)
            keyframe_room_page.clip_attributes.rotation.set_value(130)

            #  Verify step:
            sec_0_value = keyframe_room_page.clip_attributes.rotation.get_value()
            if sec_0_value == '130.00':
                check_0_degree = True
            else:
                check_0_degree = False

            # Click next keyframe
            keyframe_room_page.clip_attributes.rotation.next_keyframe()
            time.sleep(DELAY_TIME)

            sec_2_value = keyframe_room_page.clip_attributes.rotation.get_value()
            if sec_2_value == '0.00':
                check_2_degree = True
            else:
                check_2_degree = False

            case.result = check_0_degree and check_2_degree

        # [L358] 4.4 Keyframe > Clip Attribute > Opacity
        with uuid("91d9dcd4-5b93-473a-9816-00952ae14584") as case:
            # Add Opacity keyframe : value = 100 on (00:00:02:10)
            keyframe_room_page.clip_attributes.opacity.add_remove_keyframe()

            # Click previous keyframe
            keyframe_room_page.clip_attributes.rotation.previous_keyframe()
            time.sleep(DELAY_TIME)

            # Add Opacity keyframe : value = 81 on (00:00:01:00)
            keyframe_room_page.clip_attributes.opacity.set_value(81)


            # Verify step:
            # Click next keyframe > previous keyframe
            keyframe_room_page.clip_attributes.opacity.next_keyframe()
            time.sleep(DELAY_TIME)
            keyframe_room_page.clip_attributes.opacity.previous_keyframe()
            time.sleep(DELAY_TIME)

            opacity_value = keyframe_room_page.clip_attributes.opacity.get_value()
            if opacity_value == '81':
                case.result = True
            else:
                case.result = False
                logger(opacity_value)

        # [L357] 4.4 Keyframe > Clip Attribute > Scale
        with uuid("9e959cab-a100-4b54-8369-db894e1acce6") as case:
            keyframe_room_page.drag_scroll_bar(0.28)
            # Add Scale keyframe on (00:00:01:00):
            # Width value = 1.000, Height value = 1.000
            keyframe_room_page.clip_attributes.scale.add_remove_keyframe()

            # Set timeline
            main_page.set_timeline_timecode('00_00_01_21')
            time.sleep(DELAY_TIME)

            # Add Scale keyframe on (00:00:01:21):
            # Width value = 0.91, Height value = 1.22
            keyframe_room_page.clip_attributes.scale.set_maintain_aspect_ratio(set_status=0)
            keyframe_room_page.clip_attributes.scale.width.set_slider(0.91)
            keyframe_room_page.clip_attributes.scale.height.set_slider(1.22)

            # Verify Step:
            # Set timeline
            main_page.set_timeline_timecode('00_00_01_13')
            time.sleep(DELAY_TIME)

            current_width_value = keyframe_room_page.clip_attributes.scale.width.get_value()
            if current_width_value == '0.944':
                check_width = True
            else:
                check_width = False

            current_height_value = keyframe_room_page.clip_attributes.scale.height.get_value()
            if current_height_value == '1.136':
                check_height = True
            else:
                check_height = False

            case.result = check_width and check_height

        # [L362] 4.4 Keyframe > Preview adjustment
        with uuid("b9762b30-d4c8-49ee-a3bc-28f77529f56f") as case:
            # Enable Video Track 1 visible
            timeline_operation_page.click_timeline_track_visible_button(0)

            # Verify Step:
            # Click [Play] button to check preview different
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            check_preview_update = main_page.Check_PreviewWindow_is_different(L.base.Area.preview.only_mtk_view, sec=3)
            # Click [Stop]
            playback_window_page.Edit_Timeline_PreviewOperation('Stop')

            # check preview
            mask_designer_page.set_MaskDesigner_timecode('00_00_01_25')
            time.sleep(DELAY_TIME * 2)
            check_preview = main_page.snapshot(L.base.Area.preview.only_mtk_view,file_name=Auto_Ground_Truth_Folder + 'L362.png')
            check_result = precut_page.compare(Ground_Truth_Folder + 'L362.png', check_preview)

            case.result = check_preview_update and check_result
            logger(check_preview_update)
            logger(check_result)

        # [L355] 4.4 Keyframe > Fix Enhance > Adjust [HDR Effect]
        with uuid("34fb1dc3-57c1-4071-a3e8-97d9eafdea04") as case:
            # Enable Video Track 3 visible
            timeline_operation_page.click_timeline_track_visible_button(4)
            # Select track 3 (Sport 01.jpg) clip
            timeline_operation_page.select_timeline_media(track_index=4, clip_index=1)

            # Fold (Clip Attribute) for Keyframe page
            keyframe_room_page.clip_attributes.unfold_tab(0)

            # Unfold (Fix / Enhance) page
            keyframe_room_page.fix_enhance.unfold_tab()
            time.sleep(DELAY_TIME)
            # Scroll down to shwo (HDR Effect)
            keyframe_room_page.drag_scroll_bar(1)

            # Add keyframe of (Glow strength) on (00;00;01;25)
            keyframe_room_page.fix_enhance.hdr_effect.glow_strength.add_remove_keyframe()

            # Set value = 92 for (Glow strength) on (00;00;01;25)
            keyframe_room_page.fix_enhance.hdr_effect.glow_strength.click_stepper_up(5)
            time.sleep(DELAY_TIME)
            keyframe_room_page.fix_enhance.hdr_effect.glow_strength.click_stepper_down(2)
            time.sleep(DELAY_TIME)

            # Verify Step:
            check_glow_strength_value = keyframe_room_page.fix_enhance.hdr_effect.glow_strength.get_value()
            if check_glow_strength_value == '92':
                case.result = True
            else:
                case.result = False

        # [L363] 4.4 Keyframe > Save as Project
        with uuid("77a67c4a-2f74-47bf-b5bc-31defc5d3280") as case:
            # Save project:
            main_page.top_menu_bar_file_save_project_as()
            check_save_result = main_page.handle_save_file_dialog(name='test_case_1_1_31',
                                              folder_path=Test_Material_Folder + 'BFT_21_Stage1/')
            time.sleep(DELAY_TIME*2)

            if not main_page.exist(L.base.main_caption):
                logger('Cannot find locator main_caption')
                check_save_name = False
            elif main_page.exist(L.base.main_caption).AXValue == 'test_case_1_1_31':
                check_save_name = True
            else:
                logger(main_page.exist(L.base.main_caption).AXValue)
                check_save_name = False

            case.result = check_save_result and check_save_name

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_32(self):
        # clear AI module
        main_page.clear_AI_module()

        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open project: test_case_1_1_31
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_31.pds')
        main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')
        time.sleep(DELAY_TIME * 5)

        # [L333] 4.3 Fix / Enhance > Fix > Apply [Video Denoise]
        with uuid("7f017914-00c7-489f-a410-e6c6f4e9e080") as case:
            # Select track 3 (Skateboard 01.mp3) clip
            timeline_operation_page.select_timeline_media(track_index=4, clip_index=0)

            # Click Fix/Enhance button
            tips_area_page.click_fix_enhance()

            # Switch to Video Denoise
            fix_enhance_page.fix.enable_video_denoise()

            # Check default value
            default_value = fix_enhance_page.fix.video_denoise.degree.get_value()
            if default_value == '50':
                check_default = True
            else:
                check_default = False
                logger(default_value)

            # Set value = 54
            fix_enhance_page.fix.video_denoise.degree.click_up(4)
            time.sleep(DELAY_TIME)

            current_value = fix_enhance_page.fix.video_denoise.degree.get_value()
            if current_value == '54':
                adjust_result = True
            else:
                adjust_result = False
                logger(current_value)

            case.result = check_default and adjust_result

        # [L349] 4.4 Keyframe > Fix / Enhance > Adjust [Video Denoise]
        with uuid("ce527c43-3c62-49c2-8e13-dd07ded26eba") as case:
            # Click [Keyframe] on below button of (Fix/Enhance page)
            fix_enhance_page.click_keyframe()

            # Can show Video Denoise of (Keyframe Settings)
            get_value = keyframe_room_page.fix_enhance.video_denoise.degree.get_value()
            logger(get_value)
            if get_value == '54':
                unfold_result = True
            else:
                unfold_result = False

            # Set timeline
            main_page.set_timeline_timecode('00_00_02_00')
            time.sleep(DELAY_TIME)

            # Add 2nd keyframe = 68  at (00;00;02;00)
            keyframe_room_page.fix_enhance.video_denoise.degree.set_slider(68)

            # Verify Step:
            # Click "Reset" keyframe button
            # Only exist 1 keyframe at (00;00;00;00)
            keyframe_room_page.fix_enhance.video_denoise.degree.reset_keyframe()

            # Click previous keyframe > then (click next keyframe) will stay at (00;00;00;00)
            keyframe_room_page.fix_enhance.video_denoise.degree.previous_keyframe()
            keyframe_room_page.fix_enhance.video_denoise.degree.next_keyframe()
            time.sleep(DELAY_TIME)

            check_timecode = playback_window_page.get_timecode_slidebar()
            if check_timecode == '00:00:00:00':
                reset_result = True
            else:
                reset_result = False
                logger(check_timecode)

            get_value = keyframe_room_page.fix_enhance.video_denoise.degree.get_value()
            logger(get_value)
            if get_value == '68':
                check_value = True
            else:
                check_value = False

            case.result = unfold_result and reset_result and check_value

        # [L337] 4.3 Fix / Enhance > Enhance > Apply [Color Enhancement]
        with uuid("60eee427-45e9-4193-9e35-66c4400c7fb8") as case:
            # Click [Fix /Enhance] button on tips area
            tips_area_page.click_fix_enhance()

            # Enable Color Enhancement
            fix_enhance_page.enhance.enable_color_enhancement()

            # Set slider = 20
            fix_enhance_page.enhance.color_enhancement.degree.adjust_slider(20)
            time.sleep(DELAY_TIME)
            check_preview_20 = main_page.snapshot(L.base.Area.preview.only_mtk_view)

            # Set slider = 99
            fix_enhance_page.enhance.color_enhancement.degree.set_value(99)
            time.sleep(DELAY_TIME)
            check_preview_99 = main_page.snapshot(L.base.Area.preview.only_mtk_view)

            # Verify Step:
            no_update = main_page.compare(check_preview_20, check_preview_99, similarity=1)
            get_value = fix_enhance_page.enhance.color_enhancement.degree.get_value()
            if get_value == '99':
                set_value= True
            else:
                set_value = False
            case.result = (not no_update) and set_value

        # [L352] 4.4 Keyframe > Fix / Enhance > Adjust [Color Enhancement]
        with uuid("e786aad5-ba6a-4ad7-87b0-e8fe9cbadaca") as case:
            # Click [Keyframe] on below button of (Fix/Enhance page)
            fix_enhance_page.click_keyframe()

            # Can show Color Enhancement of (Keyframe Settings)
            get_value = keyframe_room_page.fix_enhance.color_enhancement.degree.get_value()
            if get_value == '99':
                unfold_result = True
            else:
                unfold_result = False
                logger(get_value)

            # Adjust editbox
            # (Click arrow up : 3 times) then (Click arrow down : 5 times)
            keyframe_room_page.fix_enhance.color_enhancement.degree.click_stepper_up(3)
            keyframe_room_page.fix_enhance.color_enhancement.degree.click_stepper_down(5)
            time.sleep(DELAY_TIME)
            get_value = keyframe_room_page.fix_enhance.color_enhancement.degree.get_value()
            if get_value == '95':
                click_arrow = True
            else:
                click_arrow = False
                logger(get_value)
            case.result = unfold_result and click_arrow

        # [L341] 4.3 Fix / Enhance > Enhance > Speech Enhancement
        with uuid("346d93d8-ee16-4c75-b6cc-1828a6a632b5") as case:
            # Enable audio track3
            timeline_operation_page.click_timeline_track_visible_button(5)

            # Enter (Fix / Enhance) page
            tips_area_page.click_fix_enhance()

            # Switch to (Speech Enhancement)
            fix_enhance_page.enhance.switch_to_speech_enhancement()
            time.sleep(DELAY_TIME)

            # Click [Speech Enhancement] button
            fix_enhance_page.enhance.click_speech_enhancement()

            # Check download AI module
            self.check_downloading_AI_module()

            # Set compensation = 68%
            fix_enhance_page.enhance.speech_enhancement.compensation.set_value(68)
            time.sleep(DELAY_TIME)

            # Verify Step:
            get_value = fix_enhance_page.enhance.speech_enhancement.compensation.get_value()
            if get_value == '68%':
                set_result = True
            else:
                set_result = False

            # Click [Apply]
            fix_enhance_page.enhance.speech_enhancement.click_apply()
            time.sleep(DELAY_TIME * 2)

            # Verify Step:
            if main_page.exist(L.fix_enhance.enhance.speech_enhancement.main_window):
                apply_result = False
            else:
                apply_result = True

            case.result = set_result and apply_result

        # [L331] 4.3 Fix / Enhance > Fix > Video Stabilizer
        with uuid("3577e439-7c24-4690-8386-8c4b3f34edc1") as case:
            # Select track 3 (1st video clip): Skateboard 01.mp4
            timeline_operation_page.select_timeline_media(track_index=4, clip_index=0)

            # Enable (Video Stabilizer)
            fix_enhance_page.fix.enable_video_stabilizer()

            # Check default value = 50
            default_value = fix_enhance_page.fix.video_stabilizer.correction_level.get_value()
            if default_value == '50':
                check_default = True
            else:
                check_default = False

            # Click [+] (4 times)
            fix_enhance_page.fix.video_stabilizer.correction_level.click_plus(4)
            time.sleep(DELAY_TIME)

            # Check current value
            current_value = fix_enhance_page.fix.video_stabilizer.correction_level.get_value()
            if current_value == '54':
                apply_result = True
            else:
                apply_result = False

            case.result = check_default and apply_result

        # Save project:
        main_page.top_menu_bar_file_save_project_as()
        main_page.handle_save_file_dialog(name='test_case_1_1_32', folder_path=Test_Material_Folder + 'BFT_21_Stage1/')
        time.sleep(DELAY_TIME * 5)

        # Pack project:
        main_page.top_menu_bar_file_pack_project_materials(project_path=Test_Material_Folder + 'BFT_21_Stage1/third_project/')
        # wait pack project processing ready
        time.sleep(DELAY_TIME * 15)

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_33(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # Open project: test_case_1_1_31
        main_page.top_menu_bar_file_open_project(save_changes='no')
        main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/test_case_1_1_32.pds')
        main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')

        # Default :(00;00;05;02) current preview
        default_preview = main_page.snapshot(L.base.Area.preview.only_mtk_view)
        time.sleep(DELAY_TIME)

        # Click [View entire video]
        timeline_operation_page.click_view_entire_video_btn()

        # [L367] 4.5 Timeline operation > Range selection > Remove
        with uuid("e5c5187a-9740-43ad-9fb5-3c3594a4e72a") as case:
            timeline_operation_page.set_range_markin_markout(30, 240)
            # Click [Remove]
            tips_area_page.click_TipsArea_btn_Remove()
            time.sleep(DELAY_TIME)

            # Verify Step:
            check_timecode = playback_window_page.get_timecode_slidebar()
            if check_timecode == '00:00:01:00':
                remove_result = True
            else:
                remove_result = False
                logger(check_timecode)

            # Set timecode (00;00;05;02) to check preview is updated
            main_page.set_timeline_timecode('00_00_05_02')
            time.sleep(DELAY_TIME * 2)

            current_remove_preview = main_page.snapshot(L.base.Area.preview.only_mtk_view)
            preview_no_update = main_page.compare(default_preview, current_remove_preview, similarity=0.85)

            case.result = (not preview_no_update) and remove_result

        # [L366] 4.5 Timeline operation > Range selection > Cut
        with uuid("0113318f-180d-4b34-80c0-faf6f765a86f") as case:
            timeline_operation_page.set_range_markin_markout(240, 330)
            # Click [Cut]
            tips_area_page.click_TipsArea_btn_Cut()
            time.sleep(DELAY_TIME)

            # Verify step:
            # Select track3 2nd clip (Sport 01.jpg) to check clip duration
            timeline_operation_page.select_timeline_media(track_index=4, clip_index=1)

            # Click duration
            tips_area_page.click_TipsArea_btn_Duration()

            check_timecode = main_page.exist(L.tips_area.window.duration_timecode).AXValue
            if check_timecode == '00:00:04:00':
                cut_result = True
            else:
                cut_result = False
                logger(check_timecode)
            case.result = cut_result

            time.sleep(DELAY_TIME)
            # Press [Enter] to close (Duration Setting) window
            main_page.press_enter_key()

        # [L373] 4.5 Timeline operation > Ripple Editing > Trim to Fit (video only)
        with uuid("d3561515-1f17-4fd9-8a74-4f8fab04e604") as case:
            # Click timeline track 1
            main_page.timeline_select_track(1)

            # Set timecode (00;00;01;00)
            main_page.set_timeline_timecode('00_00_01_00')
            time.sleep(DELAY_TIME * 2)

            # Select video to insert (Trim to fit)
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            logger('select media Skateboard 03.mp4 done')
            logger('run Trim to fit page function')
            trim_to_fit_result_1 = tips_area_page.click_TipsArea_btn_insert(5)
            logger(trim_to_fit_result_1)

            time.sleep(DELAY_TIME * 2)

            # click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 1.5)

            # Bug regression : VDE235705-0020
            logger('10725')
            main_page.drag_media_to_timeline_playhead_position_offset('Skateboard 03.mp4', track_no=1)
            time.sleep(DELAY_TIME * 2)
            logger('10728')
            # Pop up Floating Menu then click 'Trim to Fit'
            menu_item1_pos = main_page.search_text_position('Trim', mouse_move=0, order=1)
            time.sleep(DELAY_TIME * 2)
            if menu_item1_pos is not False:
                main_page.mouse.click(*menu_item1_pos)
                trim_to_fit_result_2 = True
            else:
                logger('Fail to get the position of menu : Trim to Fit, Bug regression VDE235705-0020 [NG]')
                trim_to_fit_result_2 = False
            case.result = trim_to_fit_result_1 and trim_to_fit_result_2

        # [L374] 4.5 Timeline operation > Ripple Editing > Speed up to Fit (video only)
        with uuid("f851fa10-4f1b-4d47-9498-1913b1312273") as case:
            # Click Undo
            main_page.click_undo()
            time.sleep(DELAY_TIME)

            # Select video to insert (Trim to fit)
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            tips_area_page.click_TipsArea_btn_insert(6)

            # Tools > Click [Video Speed]
            tips_area_page.tools.select_VideoSpeed()
            time.sleep(DELAY_TIME*2)

            # Verify Step:
            get_speed_multiplier = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_GetValue()
            if get_speed_multiplier == '16.667':
                case.result = True
            else:
                case.result = False
                logger(get_speed_multiplier)

            # Click [OK] to close (Video Speed Designer)
            time.sleep(DELAY_TIME)
            video_speed_page.Edit_VideoSpeedDesigner_ClickOK()

        # [L372] 4.5 Timeline operation > Ripple Editing > Overwrite
        with uuid("09c94b67-75a8-40fd-8603-9aa44d88b02c") as case:
            # Select track1 2nd clip (Skateboard 03.mp4) to check clip duration
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=1)

            main_page.select_library_icon_view_media('Landscape 02.jpg')

            # Click Insert > Overwrite
            tips_area_page.click_TipsArea_btn_insert(0)
            time.sleep(DELAY_TIME)

            # Verify Step:
            # Click duration
            tips_area_page.click_TipsArea_btn_Duration()

            check_timecode = main_page.exist(L.tips_area.window.duration_timecode).AXValue
            if check_timecode == '00:00:05:00':
                case.result = True
            else:
                case.result = False
                logger(check_timecode)

            time.sleep(DELAY_TIME)
            # Press [Enter] to close (Duration Setting) window
            main_page.press_enter_key()

        # [L368] 4.5 Timeline operation > Range Selection > Render Preview
        with uuid("919cce85-cd3e-4147-9c40-ffe9dbf6a978") as case:
            # Select range : 1 min. ~ 3 sec 02 frame
            timeline_operation_page.set_range_markin_markout(30, 92)
            time.sleep(DELAY_TIME)

            # Click [Render Preview]
            click_button = timeline_operation_page.edit_timeline_render_preview()
            progress_complete = False
            for x in range(160):
                show_progress_bar = main_page.exist(L.timeline_operation.render_preview_progress_bar)
                if show_progress_bar:
                    time.sleep(DELAY_TIME)
                else:
                    progress_complete = True
                    break

            case.result = click_button and progress_complete

        # [L371] 4.5 Timeline operation > Range Selection > Lock Range
        with uuid("d9d0062d-bcf4-46f9-8c22-1d48642a5588") as case:
            timeline_operation_page.set_range_markin_markout(100, 150)
            tips_area_page.click_TipsArea_btn_Lock_Range()

            # Set timecode
            main_page.set_timeline_timecode('00_00_07_06')
            time.sleep(DELAY_TIME * 2)

            lock_range_button = main_page.exist(L.tips_area.button.btn_Lock_Range)
            if lock_range_button:
                case.result = True
                # Click [Lock Range] again to release (Lock range) setting
                tips_area_page.click_TipsArea_btn_Lock_Range()
            else:
                case.result = False

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_34(self):
        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*3)

        # [L396] 5. Produce > H.265 > Open pack project
        with uuid("8281b84c-4b96-4801-8d13-6160084f73c8") as case:
            # Open project: first_project
            main_page.top_menu_bar_file_open_project(save_changes='no')
            check_open_result = main_page.handle_open_project_dialog(Test_Material_Folder + 'BFT_21_Stage1/third_project.pdk')
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')

            time.sleep(DELAY_TIME * 3)
            if not check_open_result:
                logger('handle_open_project_dialog [NG]')
                case.result = False
            else:

                # Select extract path
                main_page.delete_folder(Test_Material_Folder + 'BFT_21_Stage1/extract_flder_3')
                time.sleep(DELAY_TIME)
                main_page.select_file(Test_Material_Folder + 'BFT_21_Stage1/extract_flder_3')
                time.sleep(DELAY_TIME * 5)
                main_page.handle_merge_media_to_current_library_dialog(do_not_show_again='no')
                # Wait for open project
                time.sleep(DELAY_TIME * 12)

                # Verify Step:
                if not main_page.exist(L.base.main_caption):
                    logger('Cannot find locator main_caption')
                    case.result = False
                elif main_page.exist(L.base.main_caption).AXValue == 'third_project':
                    case.result = True
                else:
                    logger(main_page.exist(L.base.main_caption).AXValue)
                    case.result = False

        # [L370] 4.5 Timeline operation > Range selection > Produce Range
        with uuid("806ada7f-9a80-4ce0-8d42-25117181f691") as case:
            # Click [View entire video]
            timeline_operation_page.click_view_entire_video_btn()

            timeline_operation_page.set_range_markin_markout(0, 45)
            time.sleep(DELAY_TIME * 2)

            # Click [Produce Range]
            tips_area_page.click_TipsArea_btn_Produce_Range()

            # Verify Step:
            produce_page.local.set_preview_timecode('00_00_10_30')
            time.sleep(DELAY_TIME)

            get_timecode = produce_page.get_preview_timecode()
            if get_timecode == '00:00:01:15':
                case.result = True
            else:
                case.result = False
                logger(get_timecode)

        # [L397] 5 Produce > H.265 > Select Format > MOV
        with uuid("5dbadbaa-3de2-4d89-9836-8faba7f51266") as case:
            # Click HEVC
            produce_page.local.select_file_format('hevc')
            time.sleep(DELAY_TIME)
            produce_page.local.select_file_extension('mov')
            time.sleep(DELAY_TIME)

            # Get produced file name
            explore_mov_file = produce_page.get_produced_filename()

            if explore_mov_file == 'third_project.mov':
                case.result = True
            else:
                case.result = False
                logger(explore_mov_file)

        # [L398] 5 Produce > H.265 > Select Format > 1280x720/24p
        with uuid("dc651ed7-a7df-475a-ad4f-3eeedcd5b153") as case:
            # Select profile name
            produce_page.local.select_profile_name(3)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 1280 x 720/24p (7 Mbps)':
                case.result = False
                case.fail_log = check_profile
            else:
                case.result = True

        # [L399] 5 Produce > H.265 > Enable HW
        with uuid("fcfe5a6c-52cf-4518-8f8d-d1c323f36482") as case:
            produce_page.local.set_fast_video_rendering_hardware_encode()
            time.sleep(DELAY_TIME)
            current_HW_status = produce_page.local.set_fast_video_rendering_hardware_encode()
            case.result = current_HW_status

        # [L400] 5 Produce > H.265 > Set [Surround Sound] > AAC 5.1
        with uuid("6002d3b3-0264-4e1e-89a1-ecec9563c14c") as case:
            produce_page.local.set_surround_sound()
            time.sleep(DELAY_TIME)

            produce_page.local.set_surround_sound_aac51()
            time.sleep(DELAY_TIME * 2)

            check_surround = main_page.exist(L.produce.local.rdb_surround_sound_ac51).AXValue

            if check_surround == 1:
                case.result = True
            else:
                case.result = False

        # Preview operation: Click [Stop] to stay 0s
        produce_page.click_preview_operation('stop')
        time.sleep(DELAY_TIME * 2)

        # [L401] 5 Produce > H.265 > [Start] > Produce
        with uuid("4e526fa8-9881-4304-ab8e-d90fd0825309") as case:
            # Start : produce
            produce_page.click(L.produce.btn_start_produce)
            time.sleep(DELAY_TIME * 4)

            # Wait for produce complete
            for x in range(150):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 5)

            # New Workspace
            main_page.tap_NewWorkspace_hotkey()
            time.sleep(2)

            # handle (Do you want to save the changes now?)
            main_page.handle_no_save_project_dialog()
            time.sleep(2)

            # Verify step:
            check_produce_file = main_page.select_library_icon_view_media(explore_mov_file)

            if check_produce_file:
                # Click Insert to timeline
                main_page.tips_area_insert_media_to_selected_track()

                # Select timeline produced clip to enter pip designer
                timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
                main_page.double_click()
                time.sleep(2)

                # click [Express mode]
                pip_designer_page.switch_mode('Express')

                check_preview = main_page.snapshot(locator=L.pip_designer.preview,
                                                   file_name=Auto_Ground_Truth_Folder + 'L401.png')
                compare_result = main_page.compare(Ground_Truth_Folder + 'L401.png', check_preview)
                case.result = check_produce_file and compare_result

                # Leave pip designer and Remove the produce the clip
                pip_designer_page.click_ok()
                time.sleep(DELAY_TIME * 2)

                main_page.select_library_icon_view_media(explore_mov_file)
                media_room_page.library_clip_context_menu_move_to_trash_can()
            else:
                logger('Can NOT find the produced .mov file')
                case.result = False


