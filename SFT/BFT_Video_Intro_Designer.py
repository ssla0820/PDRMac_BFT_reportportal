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
gettyimage_page = PageFactory().get_page_object('gettyimage_page', mac)
preferences_page = PageFactory().get_page_object('preferences_page', mac)
video_speed_page = PageFactory().get_page_object('video_speed_page', mac)
subtitle_room_page = PageFactory().get_page_object('subtitle_room_page', mac)
pip_designer_page = PageFactory().get_page_object('pip_designer_page', mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Video Intro_S1 regression.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Video_Intro_Designer/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Video_Intro_Designer/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Video_Intro_Designer_scrope1():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """

        # Get "mac_driver" path
        temp_dir = os.path.abspath(tempfile.gettempdir() + "/mac_driver")
        logger(temp_dir)

        # delete mac_driver
        main_page.delete_folder(temp_dir)

        # launch APP
        main_page.start_app()
        time.sleep(DELAY_TIME*5)
        yield mac
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
            google_sheet_execution_log_init('Video Intro_BFT')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"Video Intro_BFT result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()

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

    def download_intro_complete(self, timeout=60):
        # pop up (Downloading Files) then check result
        time.sleep(DELAY_TIME*6)

        if not download_from_ss_page.download.has_dialog():
            logger("Download dialog is not found now")
            time.sleep(DELAY_TIME)
            return True

        download_status = False
        # Check (download intro template is ready) for loop
        for x in range(timeout):
            time.sleep(1)
            if download_from_ss_page.download.has_dialog():
                time.sleep(2)
            else:
                logger('Cannot find progress dialog')
                download_status = True
                break
        time.sleep(DELAY_TIME)
        return download_status

    #========== For cutout >> ==========#
    def download_cutout_complete(self, timeout=60):
        # pop up (PROGRESS) then check result
        time.sleep(DELAY_TIME*6)

        if not download_from_ss_page.download.has_dialog():
            logger("Download cutout dialog is not found now")
            time.sleep(DELAY_TIME)
            return True

        download_status = False
        # Check (download Cutout module is ready) for loop
        for x in range(timeout):
            time.sleep(1)
            if download_from_ss_page.download.has_dialog():
                time.sleep(2)
            else:
                logger('Cannot find progress dialog \n Download cutout is ready!')
                download_status = True
                break
        time.sleep(DELAY_TIME)
        return download_status

    @exception_screenshot
    def easy_cutout(self):
        # Bug regression (VDE235413-0028)
        # Insert Sport 01.jpg
        main_page.select_library_icon_view_media('Sport 02.jpg')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()

        # Click TipsArea > Pip Designer
        check_status = tips_area_page.tools.select_PiP_Designer()
        if not check_status:
            raise Exception

        # Switch to Advanced mode
        pip_designer_page.switch_mode('Advanced')
        time.sleep(DELAY_TIME * 2)

        # Switch (Motion) tab
        pip_designer_page.advanced.switch_to_motion()

        # Unfold path
        pip_designer_page.advanced.unfold_path_menu(set_unfold=1)

        # Apply one path
        pip_designer_page.path.select_template(4)

        # Switch (Animation) tab
        pip_designer_page.advanced.switch_to_animation()

        # Unfold (In Animation) then apply one (In Animation)
        pip_designer_page.advanced.unfold_in_animation_menu(set_unfold=1)

        # Apply one path
        pip_designer_page.in_animation.select_template(7)

        # Switch (Animation) tab
        pip_designer_page.advanced.switch_to_properties()

        # Apply cutout
        pip_designer_page.apply_chromakey()
        time.sleep(DELAY_TIME * 2)

        # Get cutout status then Enable Auto cutout
        cutout_button_object = main_page.exist(L.pip_designer.chromakey.cutout_button)
        logger(cutout_button_object.AXValue)
        if cutout_button_object.AXValue == 0:
            main_page.click(L.pip_designer.chromakey.cutout_button)
            # Check download cutout module is ready or not
            self.download_cutout_complete()

        # Click [OK]
        pip_designer_page.click_ok()
        time.sleep(DELAY_TIME * 2)

        # Select clip # 1 of track 1 to Enter Pip Designer again
        timeline_operation_page.select_timeline_media(0,0)
        time.sleep(DELAY_TIME * 2)

        # Click TipsArea > Pip Designer
        check_status = tips_area_page.tools.select_PiP_Designer()
        if not check_status:
            raise Exception
        time.sleep(DELAY_TIME * 3)

        # Check cutout preview
        preview_0sec = main_page.snapshot(L.pip_designer.preview)


        # seek time code to (00:00:03:15)
        pip_designer_page.set_timecode('00_00_03_15')
        time.sleep(DELAY_TIME * 2)
        preview_new = main_page.snapshot(L.pip_designer.preview)
        effect_result_same = not main_page.compare(preview_0sec, preview_new, similarity=0.7)
        effect_result_diff = main_page.compare(preview_0sec, preview_new, similarity=0.4)
        check_cutout_result = effect_result_same and effect_result_diff
        if not check_cutout_result:
            logger('Verify preview no update after apply cutout then seek other timecode')
            raise Exception

        # Click [OK]
        pip_designer_page.click_ok()
        time.sleep(DELAY_TIME * 2)

        return check_cutout_result

    def detect_memory_usage(self, f, value=None):
        if value and (value == 'final'):
            f.write(f'\nFinal - Memory: ')
        elif value:
            f.write(f'Step {value} - Memory: ')
        f.write(str(main_page.driver.ram))
        f.write(f'\n')
    #========== For cutout << ==========#

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        # aspect ratio is (1:1)
        main_page.set_project_aspect_ratio_1_1()

        # Insert Food to timeline
        main_page.select_library_icon_view_media("Landscape 01.jpg")
        main_page.right_click()
        main_page.select_right_click_menu("Insert on Selected Track")

        # enter Video Intro Room > sort by date
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 4)
        self.sort_by_date()
        time.sleep(DELAY_TIME * 4)

        # select category
        intro_video_page.click_intro_specific_category('Education')
        time.sleep(DELAY_TIME * 4)

        # select 1st template
        intro_video_page.select_intro_template_method_2(1)

        # [K164] Drag to timeline
        with uuid("f29170fd-3f94-406a-bf6d-0a544120faaf") as case:
            drag_result = intro_video_page.drag_intro_media_to_timeline_playhead_position(1)
            #logger(drag_result)

            # Click yes to enter Video Intro designer
            if main_page.exist({'AXIdentifier': 'IDD_CLALERT'}):
                main_page.click(L.base.confirm_dialog.btn_yes)
                self.download_intro_complete()

            case.result = drag_result

            # [K179] Caption bar > Name
            with uuid("88a362cb-bd2a-4f5a-8adc-024f69d26390") as case:
                check_title = intro_video_page.get_designer_title()
                if check_title == 'Video Intro Designer':
                    case.result = True
                else:
                    case.result = False

            # [K227] Crop > Click button
            with uuid("54d1a34d-8d20-4b9c-ab50-b7032d96b5fb") as case:
                check_btn = intro_video_page.click_crop_btn()
                case.result = check_btn

            # [K228] Crop > Resize
            with uuid("cf4638cf-40f0-4e9a-bef5-52acfc4b18d0") as case:
                img_before = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
                check_resize = intro_video_page.crop_zoom_pan.resize_to_small()
                case.result = check_resize

            # [K237] Crop > Done (Close dialog w/ save change)
            with uuid("fd17047e-cf75-4784-b1b2-95167d1b604b") as case:
                intro_video_page.click(L.intro_video_room.intro_video_designer.crop_window.btn_OK)
                time.sleep(3)
                # Verify : Preview is changed
                # similarity < 97% : test result = True
                # similarity > = 97% : test result = False
                img_after = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
                designer_preview_result = main_page.compare(img_before, img_after, similarity=0.97)
                case.result = not designer_preview_result

            # [K184] Caption bar > Click close
            with uuid("a456bc4a-d21c-4ea6-8f3e-35d292fa8408") as case:
                intro_video_page.click_upper_close_btn()
                intro_video_page.handle_warning_save_change_before_leaving('No')
                time.sleep(DELAY_TIME*2)
                if not main_page.exist(L.intro_video_room.intro_video_designer.main_window):
                    case.result = True
                else:
                    case.result = False

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        # aspect ratio is (4:3)
        main_page.set_project_aspect_ratio_4_3()

        # enter Video Intro Room > sort by date
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 4)
        self.sort_by_date()
        time.sleep(DELAY_TIME * 4)

        # select category
        #current_category = intro_video_page.get_Video_Intro_sub_category_string(8)
        #main_page.select_specific_tag(current_category)
        intro_video_page.click_intro_specific_category('Design')
        time.sleep(DELAY_TIME * 3)

        # select 1st template
        intro_video_page.select_intro_template_method_2(1)

        # [K165] Add to track
        with uuid("262a571a-8d10-4164-b81c-2e764c84cb8b") as case:
            result = tips_area_page.click_TipsArea_btn_insert_project()

            # Click yes to enter Video Intro designer
            self.download_intro_complete()
            if main_page.exist({'AXIdentifier': 'IDD_CLALERT'}):
                main_page.click(L.base.confirm_dialog.btn_yes)

            case.result = result

        # [K640] 3.2 Aspect ratio > 4:3
        with uuid("ec4f17c6-fe65-4380-a106-cc0e37bb65ca") as case:

            # [K242] 2.7 Add text - General text > Click
            # Open context menu and contain "General text" and "Motion Graphics title"
            with uuid("26149e21-cf48-461b-953f-9f108bf0d54a") as case:
                time.sleep(DELAY_TIME*6)
                img_before = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

                add_result = intro_video_page.click_add_text(1)
                time.sleep(DELAY_TIME)
                #img_after = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

                #designer_preview_result = main_page.compare(img_before, img_after, similarity=0.97)
                #case.result = not designer_preview_result
                case.result = add_result
            case.result = add_result

        # [K270] General text > Backdrop Settings > Click
        with uuid("e079b461-4209-44fc-bb6d-9d4f9058dc1d") as case:
            intro_video_page.general_title.click_backdrop_button()
            time.sleep(DELAY_TIME*2)

            # [K275] General text > Backdrop Settings > Enable/Disable backdrop
            with uuid("d2c5fd6b-c658-4015-b8e6-183376d3595d") as case:
                intro_video_page.backdrop_settings.enable_backdrop()
                time.sleep(DELAY_TIME*2)
                title_designer_page.handle_effect_want_to_continue()
                time.sleep(DELAY_TIME)

                img_after = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

                designer_preview_result = main_page.compare(img_before, img_after, similarity=0.999)
                case.result = not designer_preview_result

            case.result = not designer_preview_result

        # [K313] General text > Remove
        with uuid("8045098d-1f82-4e75-bf36-87e0af346b02") as case:
            check_result = intro_video_page.general_title.click_remove_button()
            case.result = check_result
            time.sleep(DELAY_TIME)


        # [K180] Caption Bar > Click DZ button
        with uuid("ce9b7b4e-4349-42f5-812b-41f65102f108") as case:
            time.sleep(DELAY_TIME*4)
            check_DZ = intro_video_page.click_DZ_btn()
            case.result = check_DZ

        # [K181] Caption Bar > Click Help button
        with uuid("231b21da-7c78-46b6-9e59-adbbed975ab3") as case:
            time.sleep(DELAY_TIME)
            check_help = intro_video_page.click_menu_bar_help()
            case.result = check_help
            time.sleep(DELAY_TIME)
            #main_page.tap_close_chrome_tab_hotkey()
            logger(check_help)
            main_page.activate()

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        # aspect ratio is (9:16)
        main_page.set_project_aspect_ratio_9_16()

        # enter Video Intro Room > sort by date
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 6)
        self.sort_by_date()
        time.sleep(DELAY_TIME * 4)

        # select category
        intro_video_page.click_intro_specific_category('Love')
        time.sleep(DELAY_TIME * 3)

        # select 1st template
        intro_video_page.select_intro_template_method_2(1)
        current_template_index = 1

        # [K167] Edit in Intro Video Designer
        with uuid("52bdc83d-8f83-4696-a7fc-b2aa5cf1aa46") as case:
            main_page.right_click()
            time.sleep(DELAY_TIME)
            main_page.select_right_click_menu('Edit in Video Intro Designer')

            # Check to enter Video Intro designer
            self.download_intro_complete()
            check_result = intro_video_page.check_in_intro_designer()

            case.result = check_result

        img_before = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

        # [K277] General text > Backdrop Settings > Ellipse
        with uuid("87ce3a8c-2069-4393-98d5-81f3a9e46bbf") as case:
            intro_video_page.click_add_text(1)
            time.sleep(DELAY_TIME*2)

            # handle (too many object) case
            if main_page.exist(L.intro_video_room.too_many_object_decteced_dialog.description):
                main_page.click(L.intro_video_room.too_many_object_decteced_dialog.btn_ok)

                # leave designer
                intro_video_page.click_upper_close_btn()
                time.sleep(DELAY_TIME * 2)

                # Select next template then enter designer
                current_template_index = current_template_index + 1
                intro_video_page.select_intro_template_method_2(current_template_index)
                main_page.double_click()

                intro_video_page.click_add_text(1)
                time.sleep(DELAY_TIME*2)

            intro_video_page.general_title.click_backdrop_button()
            time.sleep(DELAY_TIME * 2)
            intro_video_page.backdrop_settings.enable_backdrop()
            time.sleep(DELAY_TIME)
            title_designer_page.handle_effect_want_to_continue()
            time.sleep(DELAY_TIME)
            intro_video_page.backdrop_settings.set_type(2,1)
            check_type = intro_video_page.backdrop_settings.get_fit_backdrop_status()
            if check_type == 'Ellipse':
                check_type_result = True
            else:
                check_type_result = False

            img_after = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            designer_preview_result = main_page.compare(img_before, img_after, similarity=0.999)
            case.result = (not designer_preview_result) and check_type_result

        # [K281] General text > Backdrop Settings > Fill type > Uniform Color
        with uuid("efb7cb1f-31d7-480c-bf6b-fc1d6b6dab2d") as case:
            org_color = intro_video_page.backdrop_settings.get_uniform_color()
            if org_color != 'E816BB':
                intro_video_page.backdrop_settings.set_uniform_color('E816BB')
                var_plan = 1
            else:
                intro_video_page.backdrop_settings.set_uniform_color('C116BB')
                var_plan = 2
            time.sleep(DELAY_TIME)
            current_color = intro_video_page.backdrop_settings.get_uniform_color()
            if (var_plan == 1) & (current_color == 'E816BB'):
                case.result = True
            elif (var_plan == 2) & (current_color == 'C116BB'):
                case.result = True
            else:
                case.result = False


        # [K292] General text > Animation > Click
        with uuid("ab05f5b1-23d7-42be-8cbf-162fe82c173e") as case:
            intro_video_page.general_title.click_animation_button()
            time.sleep(DELAY_TIME)
            if main_page.exist(L.intro_video_room.intro_video_designer.general_title.animation_setting.main_window):
                case.result = True
            else:
                case.result = False

        # [K302] General text > In Animation > Click template
        with uuid("eaeaa563-fc1f-4b3d-87b8-9f6f7557fc69") as case:
            # 2023/07/21 Jamie update: v22.0.5520 remove effect combobox
            #intro_video_page.general_title.in_animation.select_specific_effect_combobox(6)
            #time.sleep(0.5)
            check_result = intro_video_page.general_title.in_animation.select_template(2)
            title_designer_page.handle_effect_want_to_continue()
            case.result = check_result

        intro_video_page.cancel_selection_button()

        # [K190] 2.3 Preview Window > Stop
        with uuid("ac11c061-2dd6-4a09-a2ec-a8b71c386663") as case:

            current_timecode = intro_video_page.get_designer_timecode()
            logger(current_timecode)

            intro_video_page.click_preview_operation('Stop')
            time.sleep(DELAY_TIME)
            stop_timecode = intro_video_page.get_designer_timecode()
            logger(stop_timecode)

            if (current_timecode != stop_timecode) & (stop_timecode == '00:00'):
                case.result = True
            else:
                logger('Verify FAIL')
                case.result = False

        # [K643] 3.2 Aspect ratio > 9:16, apply w/o error
        with uuid("a1b39efa-987b-42bd-9a74-3c2d6bb633c3") as case:
            intro_video_page.click_btn_save_as('9_16')
            time.sleep(DELAY_TIME*4)

            intro_video_page.enter_saved_category()

            intro_video_page.select_intro_template_method_2(1)

            img_initial = intro_video_page.snapshot(locator=produce_page.area.preview.main)

            # Verify : Set timecode to (00:00:02:00)
            main_page.set_timeline_timecode('00_00_01_00', is_verify=False)
            time.sleep(DELAY_TIME*7)
            img_check = intro_video_page.snapshot(locator=produce_page.area.preview.main)
            designer_preview_result = main_page.compare(img_initial, img_check, similarity=0.995)
            case.result = not designer_preview_result

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        # aspect ratio is (1:1)
        main_page.set_project_aspect_ratio_1_1()

        # enter Video Intro Room > sort by date
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 4)
        self.sort_by_date()
        time.sleep(DELAY_TIME * 4)

        # select category
        intro_video_page.click_intro_specific_category('Sport')
        time.sleep(DELAY_TIME * 3)

        # select 5th template
        intro_video_page.select_intro_template_method_2(5)

        # [K166] Right Click > Add to timeline
        with uuid("b7f6b97d-9564-415b-9d75-ead9d676730d") as case:
            main_page.right_click()
            time.sleep(DELAY_TIME)
            main_page.select_right_click_menu('Add to Timeline')
            for x in range(15):
                if main_page.exist(L.title_designer.backdrop.warning.dialog):
                    title_designer_page.handle_effect_want_to_continue()
                    break
                else:
                    time.sleep(DELAY_TIME)
            # Check to enter Video Intro designer
            self.download_intro_complete()
            check_result = intro_video_page.check_in_intro_designer()

            case.result = check_result

        img_before = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
        # [K203] Import a Media File… > Photo
        with uuid("b74de9b3-00c5-4dbf-9678-8dc4c47f5f8c") as case:
            intro_video_page.click_replace_media(1)
            time.sleep(DELAY_TIME*2)
            main_page.select_file(Test_Material_Folder + 'fix_enhance_20/colorful.jpg')
            time.sleep(DELAY_TIME*3)
            img_after_photo = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            designer_preview_result = main_page.compare(img_before, img_after_photo, similarity=0.985)

            # Preview should be updated
            case.result = not designer_preview_result

        # [K204] Import a Media File… > Video
        with uuid("e311ec3b-fa88-4113-981f-6e3023c91dac") as case:
            intro_video_page.click_replace_media(1)
            time.sleep(DELAY_TIME)
            main_page.select_file(Test_Material_Folder + 'Produce_Local/Produce_G172.m2ts')

            # [K212] Pop up Trim dialog when selected video is exceed duration
            with uuid("582b602c-7475-4e37-a10c-d84347966511") as case:
                if main_page.exist(L.trim.main_window, timeout=10):
                    case.result = True
                    time.sleep(DELAY_TIME*5)
                    main_page.press_esc_key()
                    time.sleep(DELAY_TIME*5)
                else:
                    logger('Verify FAIL')
                    case.result = False

            img_after_video = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            designer_preview_result = main_page.compare(img_before, img_after_video, similarity=0.985)
            case.result = not designer_preview_result

        # [K185] Caption Bar > Undo
        with uuid("af7698c2-4e80-49c7-89ba-efbfff998f4e") as case:

            intro_video_page.click_undo_button()
            intro_video_page.click_undo_button()
            time.sleep(DELAY_TIME*2)
            img_undo = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            designer_preview_result = main_page.compare(img_undo, img_before, similarity=0.95)
            case.result = designer_preview_result

        # [K186] Caption Bar > Redo
        with uuid("84e63310-e3d7-4efe-8904-4c79ca2633ff") as case:

            intro_video_page.click_redo_button()
            intro_video_page.click_redo_button()
            time.sleep(DELAY_TIME*3)
            img_redo = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            designer_preview_result = main_page.compare(img_redo, img_after_video, similarity=0.95)
            case.result = designer_preview_result

        # [K216] 2.5 Trim > Click button
        with uuid("76c0bf60-7cc4-476e-bfbb-9542a239a11d") as case:
            intro_video_page.click_trim_btn()
            if main_page.exist(L.trim.main_window, timeout=10):
                case.result = True
                time.sleep(DELAY_TIME)
                main_page.press_esc_key()
                time.sleep(DELAY_TIME * 5)
            else:
                logger('Verify FAIL')
                case.result = False

        # [K641] 3.2 Aspect ratio > 1:1, apply w/o error
        with uuid("b73f34db-e739-4f6a-b4cc-5468eed1faf3") as case:
            intro_video_page.click_btn_save_as('123')
            time.sleep(DELAY_TIME*4)

            # Drag (Scroll bar) to top
            main_page.exist(L.intro_video_room.category_scroll_bar).AXValue = 0
            time.sleep(DELAY_TIME * 2)

            intro_video_page.enter_saved_category()

            intro_video_page.select_intro_template_method_2(1)

            # Verify : Set timecode to (00:00:02:00)
            main_page.set_timeline_timecode('00_00_02_00', is_verify=False)
            time.sleep(DELAY_TIME*5)
            img_check = intro_video_page.snapshot(locator=produce_page.area.preview.main)

            # Set timecode to (00:00:00:00)
            main_page.set_timeline_timecode('00_00_00_00', is_verify=False)
            time.sleep(DELAY_TIME * 5)
            img_initial = intro_video_page.snapshot(locator=produce_page.area.preview.main)

            designer_preview_result = main_page.compare(img_initial, img_check, similarity=0.98)
            case.result = not designer_preview_result

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):

        # enter Video Intro Room > sort by date
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 4)
        self.sort_by_date()
        time.sleep(DELAY_TIME * 4)

        # select category
        intro_video_page.click_intro_specific_category('Pets')
        time.sleep(DELAY_TIME * 3)

        # select 2nd template
        intro_video_page.select_intro_template_method_2(2)

        # [K168] Room template > Double click
        with uuid("98c3f2c5-8561-4ce9-bb72-a005a074b9d1") as case:
            main_page.double_click()

            # Check if enter Video Intro designer
            self.download_intro_complete()

            case.result = intro_video_page.check_in_intro_designer()

        # [K183] 2.2 Caption Bar > Restore down
        with uuid("9c815212-9401-4e68-a7f8-dc07beb7c4ee") as case:
            time.sleep(DELAY_TIME*8)
            img_restore_org = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.main_window)

            intro_video_page.click_max_restore_btn()
            time.sleep(DELAY_TIME*2)
            img_max = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.main_window)

            intro_video_page.click_max_restore_btn()
            time.sleep(DELAY_TIME*2)
            img_restore_again = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.main_window)

            intro_video_page.click_max_restore_btn()
            time.sleep(DELAY_TIME*2)
            img_max_again = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.main_window)

            check_restore = main_page.compare(img_restore_org, img_restore_again, similarity=0.99)
            case.result = check_restore


            # [K182] 2.2 Caption Bar > Maximize
            with uuid("f3e8eb9c-4372-440d-a942-f463b2c817be") as case:
                intro_video_page.click_max_restore_btn()
                time.sleep(DELAY_TIME*2)
                check_result = main_page.compare(img_max, img_max_again, similarity=0.99)
                case.result = check_result

        # [K207] 2.4 Download and Replace > Download Media from Shutterstock and Getty Images... > Video / Photo
        with uuid("9d620641-8010-4173-916d-13883e21a35b") as case:
            img_org = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            intro_video_page.click_replace_media(2)
            time.sleep(DELAY_TIME*4)
            gettyimage_page.switch_to_SS()
            time.sleep(DELAY_TIME*4)
            download_from_ss_page.switch_to_video()
            time.sleep(DELAY_TIME*5)
            download_from_ss_page.search.search_text('child two four')
            time.sleep(10)
            download_from_ss_page.video.select_thumbnail_for_video_intro_designer(5)

            # check download Getty Image complete
            self.download_intro_complete()
            for x in range(6):
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
            check_SS_result = main_page.compare(img_org, img_updated, similarity=0.95)
            case.result = not check_SS_result

        # [K243] 2.7 Add text - General text > Add text via select "General text"
        with uuid("2abb2eb5-6e72-4318-8918-3158eeaabe54") as case:
            check_title = intro_video_page.click_add_text(1)
            time.sleep(DELAY_TIME)
            case.result = check_title

            intro_video_page.click_btn_save_as('123')
            time.sleep(DELAY_TIME * 4)

        # [K176] Download template > Download template w/o error
        with uuid("65d8cea2-1996-4f7b-ade7-a128fdf912e8") as case:
            # Drag (Scroll bar) to top
            main_page.exist(L.intro_video_room.category_scroll_bar).AXValue = 0
            time.sleep(DELAY_TIME * 2)

            intro_video_page.enter_downloaded_category()
            time.sleep(DELAY_TIME * 2)

            # select 1st template
            intro_video_page.select_intro_template_method_2(1)
            main_page.double_click()
            time.sleep(DELAY_TIME * 5)

            img_download = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_download = main_page.compare(img_org, img_download, similarity=0.95)
            case.result = check_download

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):

        # enter Video Intro Room > sort by date
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 4)
        self.sort_by_date()
        time.sleep(DELAY_TIME * 4)

        # select category
        intro_video_page.click_intro_specific_category('Design')
        time.sleep(DELAY_TIME * 3)

        # select 2nd template
        intro_video_page.select_intro_template_method_2(2)

        # Right Click > Add to timeline
        main_page.right_click()
        time.sleep(DELAY_TIME)
        main_page.select_right_click_menu('Add to Timeline')
        for x in range(15):
            if main_page.exist(L.title_designer.backdrop.warning.dialog):
                title_designer_page.handle_effect_want_to_continue()
                break
            else:
                time.sleep(DELAY_TIME)
        # Check to enter Video Intro designer
        self.download_intro_complete()
        intro_video_page.check_in_intro_designer()

        # [K487] 2.9 Add image > Button [Click]
        with uuid("ffd86ff4-9346-4c24-9bed-bb082557607b") as case:
            img_org = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            intro_video_page.click_add_image(1)
            time.sleep(DELAY_TIME)
            main_page.select_file(Test_Material_Folder + 'fix_enhance_20/colorful.jpg')

            # Click [OK] to close Crop window
            if main_page.exist(L.intro_video_room.intro_video_designer.crop_window.main_window, timeout=10):
                main_page.click(L.intro_video_room.intro_video_designer.crop_window.btn_OK)
            time.sleep(DELAY_TIME*3)
            img_replace = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_image_result = main_page.compare(img_org, img_replace, similarity=0.98)
            case.result = not check_image_result

        # [K522] 2.9 Add image > Edit object settings > Button [Click]
        with uuid("4816cb23-8dde-48af-bb23-81a90873450f") as case:
            result = intro_video_page.image.click_object_settings_btn()
            case.result = result

        # [K531] 2.9 Add image > Edit object settings > Border tab > Enable
        with uuid("66f7da2c-1d1b-453d-9b6f-306ac3529790") as case:
            intro_video_page.image.object_settings.unfold_border(1)
            check_initial = intro_video_page.image.object_settings.get_border_status()
            intro_video_page.image.object_settings.enable_border(1)
            time.sleep(DELAY_TIME * 2)
            set_result = intro_video_page.image.object_settings.get_border_status()
            case.result = (not check_initial) and set_result

        # [K411] 2.9 Add image > Edit object settings > Border tab > Size
        with uuid("6dc6e1d3-37c4-41f9-9a1a-3bc79cb2d0f9") as case:
            check_intial_border = intro_video_page.image.object_settings.get_border_size()
            logger(check_intial_border)
            check_intial_border = int(check_intial_border)
            if check_intial_border != 3:
                new_value = 3
                initial_result = False
            else:
                new_value = 10
                initial_result = True

            logger(new_value)

            intro_video_page.image.object_settings.set_border_size(new_value)
            time.sleep(DELAY_TIME * 2)
            set_result = intro_video_page.image.object_settings.get_border_size()
            new_value = str(new_value)
            if set_result != new_value:
                set_size_result = False
            else:
                set_size_result = True

            case.result = initial_result and set_size_result

            # Close (Object Settings window)
            main_page.press_esc_key()

        # [K424] 2.9 Add image > Animation > Button [Click]
        with uuid("86e78c90-a176-4a99-8672-408ee46f087b") as case:
            result = intro_video_page.image.click_animation_btn()
            case.result = result

        # [K433] 2.9 Add image > Animation > In Animation > Click template (Blizzard)
        with uuid("5fb14981-e23f-4591-986a-0be3d6276329") as case:
            # Unfold
            intro_video_page.image.in_animation.unfold_setting(1)
            check_image_result = intro_video_page.image.in_animation.select_template('Blizzard')
            time.sleep(DELAY_TIME)

            case.result = check_image_result

        # [K188] 2.3 Preview Window > Play
        with uuid("199072e8-9eb0-4e50-a8ce-2fd40f06b7b6") as case:

            # Click [Stop] to timecode 00:00
            intro_video_page.click_preview_operation('Stop')
            time.sleep(DELAY_TIME*2)
            stop_timecode = intro_video_page.get_designer_timecode()
            logger(stop_timecode)

            # Click [Play]
            intro_video_page.click_preview_operation('Play')
            time.sleep(DELAY_TIME * 2)

            # Verify 1 : check preview is different
            check_preview_change = main_page.Check_PreviewWindow_is_different(area=L.intro_video_room.intro_video_designer.preview_area, sec=3)
            logger(check_preview_change)

            # Verify 2: check timecode result
            play_timecode = intro_video_page.get_designer_timecode()
            logger(play_timecode)
            if (stop_timecode == '00:00') and (play_timecode != '00:00'):
                check_timecode = True
            else:
                check_timecode = False

            case.result = check_preview_change and check_timecode

        # [K189] 2.3 Preview Window > Pause
        with uuid("fcfea058-3bfa-4e8d-8a55-69a3b4915850") as case:

            # Click [Pause]
            intro_video_page.click_preview_operation('Pause')

            # Verify : check timecode result
            pause_timecode = intro_video_page.get_designer_timecode()
            logger(pause_timecode)
            if play_timecode != pause_timecode:
                pause_result = True
            else:
                pause_result = False

            # Verify 2: find the play button
            play_button_result = main_page.find(L.intro_video_room.intro_video_designer.operation.btn_play)

            case.result = pause_result and play_button_result

    #  7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        # aspect ratio is (9:16)
        main_page.set_project_aspect_ratio_9_16()

        # enter Video Intro Room > sort by date
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 4)
        self.sort_by_date()
        time.sleep(DELAY_TIME * 4)

        # select category
        intro_video_page.click_intro_specific_category('Handwritten')
        time.sleep(DELAY_TIME * 3)

        # select 2nd template
        intro_video_page.select_intro_template_method_2(1)

        main_page.right_click()
        time.sleep(DELAY_TIME)
        main_page.select_right_click_menu('Edit in Video Intro Designer')

        # Check to enter Video Intro designer
        self.download_intro_complete()
        intro_video_page.check_in_intro_designer()


        # [K396] 2.8 Add text - Motion Graphics title > Button [Click]
        with uuid("d08a73b8-569d-4f65-b7e6-9734a684fbae") as case:
            img_org = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            check_title = intro_video_page.click_add_text(2)
            time.sleep(DELAY_TIME*3)
            case.result = check_title
        # [K400] 2.8 Add text - Motion Graphics title > Title Room > Caption Bar > Close button
        with uuid("c3fd3e88-425f-4b0c-a740-6b03486db5b9") as case:
            check_close_btn = main_page.find(L.intro_video_room.intro_video_designer.motion_graphics.title_room.btn_close)
            main_page.click(L.intro_video_room.intro_video_designer.motion_graphics.title_room.btn_close)
            time.sleep(DELAY_TIME)

            #Verify : Cannot find the (Title Room) window
            if not main_page.exist(L.intro_video_room.intro_video_designer.motion_graphics.title_room.main_window):
                check_result = True
            else:
                check_result = False

            case.result = check_close_btn and check_result

        # [K326] 2.8 Add text - Motion Graphics title > Title Room > Select title
        with uuid("6cc6c1fe-3006-48ea-8378-b9020ee2b7ca") as case:
            intro_video_page.click_add_text(2)
            time.sleep(DELAY_TIME * 3)

            # Insert Blogger Titles 04
            intro_video_page.motion_graphics.select_template(2, category=4)
            time.sleep(DELAY_TIME * 5)
            img_after = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_image_result = main_page.compare(img_org, img_after, similarity=0.999)
            case.result = not check_image_result

        # [K349] 2.8 Add text - Motion Graphics title > Motion Graphics Settings - Advanced mode > Button [Click]
        with uuid("1bdc3a4a-39d9-4e80-b1a1-8b1800c240cf") as case:
            check_result = intro_video_page.motion_graphics.click_settings_button()
            case.result = check_result

        # [K374] 2.8 Add text - Motion Graphics title > Remove button
        with uuid("083c8da0-27f4-43b5-96d7-9e79f90fa30e") as case:
            intro_video_page.motion_graphics.click_remove_button()
            time.sleep(DELAY_TIME*2)
            img_remove_result = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_image_result = main_page.compare(img_org, img_remove_result, similarity=0.99)
            case.result = check_image_result

            intro_video_page.click_undo_button()
            time.sleep(DELAY_TIME*2)
            intro_video_page.motion_graphics.click_settings_button()
            time.sleep(DELAY_TIME * 2)

        # [K358] 2.8 Add text - Motion Graphics title > Motion Graphics Settings - Advanced mode > Title tab > Text
        with uuid("2d2c0612-3128-4dff-8087-0bbc22198506") as case:
            get_initial_title = intro_video_page.motion_graphics.get_title_text()
            if get_initial_title != 'Add Title Here':
                get_initial = False
            else:
                get_initial = True

            intro_video_page.motion_graphics.set_title_text('Mac 12^&@1 Test')
            time.sleep(DELAY_TIME * 2)
            get_edit_title = intro_video_page.motion_graphics.get_title_text()
            if get_edit_title != 'Mac 12^&@1 Test':
                get_edit = False
            else:
                get_edit = True

            case.result = get_initial and get_edit

        # [K377] 2.8 Add text - Motion Graphics title > Cancel selection
        with uuid("aaf3d1d0-b982-4b23-b424-638686bed26e") as case:
            intro_video_page.cancel_selection_button()

            # Verify : Cannot find the (Motion Graphics Setting) window
            if not main_page.exist(L.intro_video_room.intro_video_designer.motion_graphics.mgt_settings.main_window):
                case.result = True
            else:
                case.result = False

    #  7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        # aspect ratio is (1:1)
        main_page.set_project_aspect_ratio_1_1()

        # Insert Food to timeline
        main_page.select_library_icon_view_media("Landscape 01.jpg")
        main_page.right_click()
        main_page.select_right_click_menu("Insert on Selected Track")

        # enter Video Intro Room > sort by date
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 4)
        self.sort_by_date()
        time.sleep(DELAY_TIME * 4)

        # select category
        intro_video_page.click_intro_specific_category('Handwritten')
        time.sleep(DELAY_TIME * 3)

        # select 5th template
        intro_video_page.select_intro_template_method_2(1)

        # Drag to timeline
        intro_video_page.drag_intro_media_to_timeline_playhead_position(1)

        # Click yes to enter Video Intro designer
        if main_page.exist({'AXIdentifier': 'IDD_CLALERT'}):
            main_page.click(L.base.confirm_dialog.btn_yes)
            self.download_intro_complete()

        intro_video_page.set_designer_timecode('04_00')
        time.sleep(DELAY_TIME)

        # Add image w/ colorful.jpg
        main_page.move_mouse_to_0_0()
        intro_video_page.click_add_image(1)
        time.sleep(DELAY_TIME)
        main_page.select_file(Test_Material_Folder + 'fix_enhance_20/colorful.jpg')
        time.sleep(DELAY_TIME*2)
        # Click [OK] to close Crop window
        if main_page.exist(L.intro_video_room.intro_video_designer.crop_window.main_window, timeout=10):
            main_page.click(L.intro_video_room.intro_video_designer.crop_window.btn_OK)
        time.sleep(DELAY_TIME * 2)
        img_org = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

        # [K448] 2.9 Add image > Replace > Button [Click]
        with uuid("6314053f-e3d3-4394-9f70-e08f6a3c48ae") as case:
            intro_video_page.image.click_replace_btn()
            time.sleep(DELAY_TIME)
            main_page.select_right_click_menu('Import a Media File...')
            time.sleep(DELAY_TIME)
            main_page.select_file(Test_Material_Folder + 'fix_enhance_20/hastur.jpg')
            time.sleep(DELAY_TIME * 2)
            img_replace = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            check_replce_result = main_page.compare(img_org, img_replace, similarity=0.995)
            case.result = not check_replce_result

        # [K457] 2.9 Add image > Cancel selection
        with uuid("4960add8-ed51-4d67-bb21-2656ddbfa0a5") as case:
            if main_page.exist(L.intro_video_room.intro_video_designer.image.btn_remove):
                current_status = True
            else:
                current_status = False
            intro_video_page.cancel_selection_button()
            time.sleep(DELAY_TIME * 2)

            # Verify :
            if not main_page.exist(L.intro_video_room.intro_video_designer.image.btn_remove):
                check_result = True
            else:
                check_result = False

            case.result = current_status and check_result

        # [K238] 2.6 Crop > Cancel w/o saving
        with uuid("3ac1ab0b-81e5-49f5-8f1b-6171741ed19a") as case:
            # Click crop
            intro_video_page.click_crop_btn()
            time.sleep(DELAY_TIME*2)

            # Resize to small
            intro_video_page.crop_zoom_pan.resize_to_small()
            time.sleep(DELAY_TIME * 2)
            intro_video_page.crop_zoom_pan.click_cancel('No')
            time.sleep(3)
            img_cancel_crop = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            check_result = main_page.compare(img_replace, img_cancel_crop, similarity=0.99)
            case.result = check_result

        # [K461] 2.10 Video Overlay (PiP) > Click
        with uuid("309dd1d4-448f-498e-9e17-c17aa8980545") as case:
            # [K478] 2.10 Video Overlay (PiP) > Double Click to import Sticker
            with uuid("a32b2f16-362e-4d6f-b104-865fa2da6bcf") as case:

                # Click (Add sticker)
                intro_video_page.click_add_pip_object()
                time.sleep(DELAY_TIME)

                # Video Overlay Room
                intro_video_page.select_pip_template(3, 'Social Media')
                time.sleep(DELAY_TIME)

                # Leave edit mode
                intro_video_page.cancel_selection_button()
                time.sleep(DELAY_TIME)

                intro_video_page.set_designer_timecode('02_14')
                time.sleep(DELAY_TIME)

                img_sticker = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

                check_result = main_page.compare(img_cancel_crop, img_sticker, similarity=0.999)
                case.result = not check_result
            case.result = not check_result

        # [K515] 2.10 Video Overlay (PiP) > Animation > Click
        with uuid("8ed09f21-026f-4846-a2b3-d4e9b0fed1c0") as case:
            # Click undo then insert sticker again
            intro_video_page.click_undo_button()
            time.sleep(DELAY_TIME)

            intro_video_page.click_add_pip_object()
            time.sleep(DELAY_TIME * 2)

            # 2023/09/08 check w/ PM: Server already remove "General" category
            # Video Overlay Room
            intro_video_page.select_pip_template(4, 'Nature')
            time.sleep(DELAY_TIME)

            # Click animation button
            case.result = intro_video_page.image.click_animation_btn()

            # Press [Esc] to close animation setting
            main_page.press_esc_key()
            time.sleep(DELAY_TIME)

        # [K524] 2.10 Video Overlay (PiP) > Animation > In Animation > Click template (Wipe Soft)
        with uuid("e935be43-f26d-459f-94c2-71b44b267d15") as case:
            # Click cancel button
            intro_video_page.cancel_selection_button()

            # Set timecode :
            intro_video_page.set_designer_timecode('00_10')
            time.sleep(DELAY_TIME * 2)
            check_before = main_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            # Click preview center
            intro_video_page.click_preview_center()
            time.sleep(DELAY_TIME * 2)

            # Click animation button
            intro_video_page.image.click_animation_btn()

            # Unfold
            intro_video_page.image.in_animation.unfold_setting(1)
            intro_video_page.image.in_animation.select_template('Blur')

            # Click cancel button
            intro_video_page.cancel_selection_button()

            # Click stop button
            intro_video_page.click_preview_operation('Stop')
            time.sleep(DELAY_TIME * 2)

            # Set timecode :
            intro_video_page.set_designer_timecode('00_21')
            time.sleep(DELAY_TIME * 2)
            check_animation = main_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            case.result = not main_page.compare(check_before, check_animation, similarity=0.999)

    # 10 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        # aspect ratio is keep 16:9

        # Insert Food to timeline
        main_page.select_library_icon_view_media("Food.jpg")
        main_page.right_click()
        main_page.select_right_click_menu("Insert on Selected Track")

        # enter Video Intro Room
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 4)

        # Input search keyword
        main_page.exist_click(L.media_room.input_search)
        main_page.keyboard.send('lpmpp')
        main_page.press_enter_key()
        time.sleep(DELAY_TIME * 5)

        # select 1st template
        intro_video_page.select_intro_template_method_2(1)
        time.sleep(DELAY_TIME)

        # Drag to timeline
        intro_video_page.drag_intro_media_to_timeline_playhead_position(1)

        # Click yes to enter Video Intro designer
        if main_page.exist({'AXIdentifier': 'IDD_CLALERT'}):
            main_page.click(L.base.confirm_dialog.btn_yes)
            self.download_intro_complete()

        # [K613] 2.14 Duration > Animation > Button > Click
        with uuid("6ff398ba-4155-4fb5-a9b4-83d6fca74437") as case:
            # Set designer timecode (99:00) to get last sec
            intro_video_page.set_designer_timecode('99_00')
            time.sleep(DELAY_TIME * 4)
            current_duration = intro_video_page.get_designer_timecode_only_sec()

            intro_video_page.click_duration_btn()
            if main_page.exist(L.intro_video_room.intro_video_designer.duration.main_window):
                case.result = True
            else:
                case.result = False
            time.sleep(DELAY_TIME)

        # [K618] 2.14 Duration > Original duration
        with uuid("5da4c1cb-b760-4adf-ae9a-ffe532770af0") as case:
            result = intro_video_page.duration_setting.get_org_duration()

            current_duration = int(current_duration)
            if result != f'{current_duration} seconds':
                case.result = False
            else:
                case.result = True

        # [K619] 2.14 Duration > Set duration (Max.)
        with uuid("20732e9b-3002-425c-abc4-4afdfc8937a4") as case:
            set_value = current_duration * 1.5
            if set_value > 15:
                set_value = 15
            set_value = int(set_value)
            logger(set_value)
            intro_video_page.duration_setting.set_new_duration(set_value)
            time.sleep(DELAY_TIME)
            get_value = intro_video_page.duration_setting.get_new_duration()

            # Current INT should transfer to String
            set_value = str(set_value)

            if get_value != set_value:
                case.result = False
            else:
                case.result = True

        # [K620] 2.14 Duration > Set duration (Min.)
        with uuid("03f6833a-9c65-460e-a315-351a5b2a54b6") as case:
            # [K624] 2.14 Duration > Click [OK]
            with uuid("3fd6e80e-31ef-4c4f-8a5f-636ebad8dea6") as case:

                set_value = (current_duration * 0.5)
                set_value = math.ceil(set_value)
                set_value = int(set_value)
                logger(set_value)
                if set_value < 5:
                    set_value = 5

                set_animation_value = set_value
                intro_video_page.duration_setting.set_new_duration(set_value)
                time.sleep(DELAY_TIME)

                intro_video_page.duration_setting.click_OK()

                intro_video_page.click_duration_btn()
                time.sleep(DELAY_TIME)
                get_value = intro_video_page.duration_setting.get_new_duration()

                # Current INT should transfer to String
                set_value = str(set_value)

                if get_value != set_value:
                    case.result = False
                else:
                    case.result = True

            if get_value != set_value:
                case.result = False
            else:
                case.result = True
            intro_video_page.duration_setting.click_OK()

        # [K280] General text > Backdrop Settings > Rounded Rectangle
        with uuid("8d24ce9d-1ce7-43d1-9b6b-318dc43f54e1") as case:
            intro_video_page.click_add_text(1)
            time.sleep(DELAY_TIME * 2)

            #  ----- snapshot for verify animation ----->
            # Seek timecode
            set_animation_value = set_animation_value - 1
            logger(set_animation_value)

            add_zero_flag = 0
            # if set_animation_value < 10, should add zero for seek page function
            if set_animation_value < 10:
                add_zero_flag = 1

            # Current INT should transfer to String
            set_animation_value = str(set_animation_value)

            if add_zero_flag:
                intro_video_page.set_designer_timecode(f'0{set_animation_value}_24')
            else:
                intro_video_page.set_designer_timecode(f'{set_animation_value}_24')
            time.sleep(DELAY_TIME * 2)

            default_no_animation = main_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            #  ----- snapshot for verify animation <-----

            intro_video_page.click_preview_center()
            time.sleep(DELAY_TIME*2)
            intro_video_page.general_title.click_backdrop_button()
            time.sleep(DELAY_TIME * 2)
            intro_video_page.backdrop_settings.enable_backdrop()
            time.sleep(DELAY_TIME)
            title_designer_page.handle_effect_want_to_continue()
            time.sleep(DELAY_TIME)
            intro_video_page.backdrop_settings.set_type(2, 4)
            check_type = intro_video_page.backdrop_settings.get_fit_backdrop_status()
            if check_type == 'Rounded Rectangle':
                check_type_result = True
            else:
                check_type_result = False

            case.result = check_type_result

        # [K279] General text > Backdrop Settings > Curve-edged Rectangle
        with uuid("09128d32-1a5a-44de-bdd3-ebdc2f43b91f") as case:

            time.sleep(DELAY_TIME)
            intro_video_page.backdrop_settings.set_type(2, 3)
            check_type = intro_video_page.backdrop_settings.get_fit_backdrop_status()
            if check_type == 'Curve-edged Rectangle':
                check_type_result = True
            else:
                check_type_result = False

            case.result = check_type_result

        # [K298] General text > In Animation > Tab (Unfold / Fold)
        with uuid("f45595bb-8bd4-4bb2-8233-0eb41de45c66") as case:
            intro_video_page.general_title.click_animation_button()
            time.sleep(DELAY_TIME)

            intro_video_page.general_title.in_animation.unfold_setting(0)
            time.sleep(0.5)
            check_result = intro_video_page.general_title.in_animation.get_unfold_setting()
            if check_result == 0:
                case.result = True
            else:
                case.result = False

        # [K307] General text > Out Animation > Click template
        with uuid("eb9724ab-3913-4d60-96d2-29cc200a01ed") as case:
            # Unfold (Out Animation)
            intro_video_page.general_title.out_animation.unfold_setting(1)
            time.sleep(0.5)

            # PDR Mac v22.0.5520 remove (In animation) effect combobox for Loop SPEC.
            #intro_video_page.general_title.out_animation.select_specific_effect_combobox(5)
            time.sleep(0.5)
            # Apply Out animation > Pop-up I
            check_result = intro_video_page.general_title.in_animation.select_template(3)
            title_designer_page.handle_effect_want_to_continue()

            # Seek timecode xx:24
            if add_zero_flag:
                intro_video_page.set_designer_timecode(f'0{set_animation_value}_24')
            else:
                intro_video_page.set_designer_timecode(f'{set_animation_value}_24')
            time.sleep(DELAY_TIME * 2)

            apply_animation = main_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_preview_change = main_page.compare(apply_animation, default_no_animation, similarity=0.9)
            case.result = check_result and (not check_preview_change)

        # [K638] 3.2 Aspect ratio > Video Intro Room > 16:9
        with uuid("7cc21ed6-09af-469d-a65e-493c45113227") as case:
            intro_video_page.click_btn_save_as('16_9')
            time.sleep(DELAY_TIME * 4)

            # Enter Media room
            main_page.enter_room(0)
            time.sleep(DELAY_TIME * 1.5)

            # enter Video Intro Room
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 3)

            intro_video_page.enter_saved_category()

            intro_video_page.select_intro_template_method_2(1)
            main_page.press_space_key()
            check_preview_change = main_page.Check_PreviewWindow_is_different(sec=3)
            case.result = check_preview_change

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_10(self):

        # enter Video Intro Room > sort by date
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 4)
        self.sort_by_date()
        time.sleep(DELAY_TIME * 4)

        # select category
        intro_video_page.click_intro_specific_category('Retro')
        time.sleep(DELAY_TIME * 3)

        # select 1st template
        intro_video_page.select_intro_template_method_2(1)

        # Add to track
        tips_area_page.click_TipsArea_btn_insert_project()

        # Download template
        self.download_intro_complete()
        # Click yes to enter Video Intro designer
        main_page.click(L.base.confirm_dialog.btn_yes)
        # Check (download intro template is ready) for loop
        self.download_intro_complete()
        img_no_sticker = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

        # [K539] 2.10 Video Overlay (PiP) > Replace > Click button
        with uuid("d2037096-4283-49a8-8c1a-e09194974ceb") as case:
            # Double Click to import Sticker
            intro_video_page.click_add_pip_object()
            time.sleep(DELAY_TIME)

            # Video Overlay Room
            intro_video_page.select_pip_template(3, 'Decorations')
            time.sleep(DELAY_TIME)

            img_sticker_1 = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            intro_video_page.image.click_replace_btn()
            time.sleep(DELAY_TIME)

            # Replace sticker
            intro_video_page.select_pip_template(1, 'Decorations')
            time.sleep(DELAY_TIME*5)
            img_sticker_2 = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            check_result = main_page.compare(img_sticker_1, img_sticker_2, similarity=0.999)
            case.result = not check_result

        # [K548] 2.10 Video Overlay (PiP) > Click "x" button to cancel selection
        with uuid("05fc31df-f860-43bf-bd5f-1dd71effe848") as case:
            intro_video_page.cancel_selection_button()
            time.sleep(DELAY_TIME*2)
            if not main_page.exist(L.intro_video_room.intro_video_designer.image.btn_remove):
                check_result = True
            else:
                check_result = False

            case.result = check_result

        # [K545] 2.10 Video Overlay (PiP) > Remove > Click button
        with uuid("46f7c6c3-0920-40e5-be38-bb3393b2c03b") as case:
            intro_video_page.click_preview_center()
            time.sleep(DELAY_TIME)
            intro_video_page.image.click_remove_button()
            main_page.move_mouse_to_0_0()
            time.sleep(DELAY_TIME)
            img_remove_sticker = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            check_result = main_page.compare(img_no_sticker, img_remove_sticker)
            case.result = check_result

        # [K276] General text > Backdrop Settings > Solid background bar
        with uuid("63f08d21-48a8-4f4b-ac76-540371b15970") as case:
            intro_video_page.click_add_text(1)
            time.sleep(DELAY_TIME*2)

            intro_video_page.general_title.click_backdrop_button()
            time.sleep(DELAY_TIME * 2)
            intro_video_page.backdrop_settings.enable_backdrop()
            time.sleep(DELAY_TIME)
            title_designer_page.handle_effect_want_to_continue()
            time.sleep(DELAY_TIME)
            intro_video_page.backdrop_settings.set_type(1)
            check_type = intro_video_page.backdrop_settings.get_type()
            if check_type == 1:
                check_type_result = True
            else:
                check_type_result = False

            case.result = check_type_result
            img_solid_backdrop = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

        # [K278] General text > Backdrop Settings > Rectangle
        with uuid("3497e749-e27d-41f8-a926-52e7ac612d5f") as case:

            time.sleep(DELAY_TIME)
            intro_video_page.backdrop_settings.set_type(2, 2)
            check_type = intro_video_page.backdrop_settings.get_fit_backdrop_status()
            if check_type == 'Rectangle':
                check_type_result = True
            else:
                check_type_result = False

            img_rectangle_backdrop = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            check_preview = main_page.compare(img_solid_backdrop, img_rectangle_backdrop, similarity=0.99999)
            case.result = check_type_result and (not check_preview)

        intro_video_page.cancel_selection_button()
        # [K362] MGT > Title tab > Font face color
        with uuid("4d6ce10b-d578-440d-b351-8e8b22d259ac") as case:
            intro_video_page.click_add_text(2)
            time.sleep(DELAY_TIME * 2)

            # Insert Minimalist Titles 03
            intro_video_page.motion_graphics.select_template(3, category=3)
            time.sleep(DELAY_TIME * 3)
            img_mgt_initial = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_image_result = main_page.compare(img_rectangle_backdrop, img_mgt_initial, similarity=0.999)

            # Click (Motion Graphics Setting)
            intro_video_page.motion_graphics.click_settings_button()
            time.sleep(DELAY_TIME)

            # Set font face color
            intro_video_page.motion_graphics.set_font_color('FF3B13')

            # Get font face color
            hex_color = intro_video_page.motion_graphics.get_font_color()
            if hex_color == 'FF3B13':
                hex_color_result = True
            else:
                hex_color_result = False

            img_mgt_modify_color = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_color_result = main_page.compare(img_mgt_initial, img_mgt_modify_color, similarity=0.999)
            case.result = (not check_image_result) and (not check_color_result) and hex_color_result

            # close Video Intro designer
            intro_video_page.click_btn_close()
            time.sleep(DELAY_TIME)
            intro_video_page.handle_warning_save_change_before_leaving(option='No')

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_11(self):

        # enter Video Intro Room
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 5)
        intro_video_page.enter_my_favorites()
        time.sleep(DELAY_TIME * 3)

        # select 1st template
        intro_video_page.select_intro_template_method_2(1)

        # [K157] 1.8 Sharable Template from Room > Right Click Menu > View on Cyberlink DZ
        with uuid("343e2bb5-5f92-41d6-be1e-f35aef2b822a") as case:
            main_page.right_click()
            main_page.select_right_click_menu('View on DirectorZone')

            time.sleep(DELAY_TIME * 3)

            result = main_page.check_chrome_page()
            time.sleep(DELAY_TIME)
            main_page.tap_close_chrome_tab_hotkey()
            # Verify : Open Chrome page
            if result:
                case.result = True
            else:
                case.result = False

        # Add to track
        tips_area_page.click_TipsArea_btn_insert_project()

        # Download template
        self.download_intro_complete()
        # Click yes to enter Video Intro designer
        main_page.click(L.base.confirm_dialog.btn_yes)
        # Check (download intro template is ready) for loop
        self.download_intro_complete()
        img_initial = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
        #logger(img_initial)
        # [K270] Color LUT > Click button
        with uuid("f74920e3-d83b-42cf-a1b1-9465c4113e7f") as case:
            intro_video_page.click_LUT_btn()
            check_elem = main_page.exist(L.intro_video_room.intro_video_designer.color_filter_window.main_window)
            if check_elem:
                case.result = True
            else:
                case.result = False

        # [K271] Color LUT > Caption Bar
        with uuid("fe7d5c90-48b6-4ccc-9b7b-62215a9b989d") as case:
            if check_elem.AXTitle == 'Color Filter':
                case.result = True
            else:
                case.result = False

        # [K272] Color LUT > Caption Bar > Close (X button)
        with uuid("1b82b8de-bf12-42a5-b037-546611256bc5") as case:
            case.result = intro_video_page.color_filter.close_x()

        intro_video_page.click_LUT_btn()
        time.sleep(DELAY_TIME)
        # [K278] Color LUT > Categories
        with uuid("79576226-7861-45c6-81c6-a7c0c7a31482") as case:
            elem = L.intro_video_room.intro_video_designer.color_filter_window.combobox_category
            if main_page.exist(elem).AXTitle == 'Color LUT':
                default_status = True
            else:
                default_status = False

            intro_video_page.color_filter.select_LUT_template(3, 'Soft Pink')
            elem = L.intro_video_room.intro_video_designer.color_filter_window.combobox_category
            if main_page.exist(elem).AXTitle == 'Soft Pink':
                switch_status = True
            else:
                switch_status = False
            logger(f'{default_status} & {switch_status}')
            case.result = default_status and switch_status

        # [K279] Color LUT > Template (IAD)
        with uuid("0530a0f5-107f-4b5d-8024-5417e2abf02b") as case:
            # [K281] Color LUT > Template Apply
            with uuid("d903ed2b-4325-456b-800b-c3ea35d80edf") as case:

                img_applied = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
                check_color_result = main_page.compare(img_initial, img_applied, similarity=0.98)
                logger(check_color_result)
                case.result = not check_color_result
            case.result = not check_color_result

        # [K277] Color LUT > Strength > Input value
        with uuid("b2deb381-c997-4a79-83a6-5df08a856868") as case:
            get_initial = main_page.exist(L.intro_video_room.intro_video_designer.color_filter_window.strength.editbox_value).AXValue
            if get_initial == '100%':
                default_status = True
            else:
                default_status = False
            intro_video_page.color_filter.set_strength_value(15)
            get_initial = main_page.exist(L.intro_video_room.intro_video_designer.color_filter_window.strength.editbox_value).AXValue
            if get_initial == '15%':
                after_status = True
            else:
                after_status = False

            case.result = default_status and after_status

    # 11 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_12(self):
        time.sleep(DELAY_TIME * 3)
        # enter Video Intro Room
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 3)
        intro_video_page.enter_my_favorites()

        # select 1st template
        intro_video_page.select_intro_template_method_2(1)

        # enter designer
        main_page.double_click()
        self.download_intro_complete()
        img_initial = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

        # [K426] 2.8 MGT > Right Click Menu > Move to bottom
        with uuid("c763d68b-3233-4543-9793-1824dc1791c7") as case:
            intro_video_page.click_preview_center()
            time.sleep(DELAY_TIME*2)
            intro_video_page.right_click()
            intro_video_page.select_right_click_menu('Send to Back')
            time.sleep(DELAY_TIME*3)
            img_MGT_to_back = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_result = main_page.compare(img_initial, img_MGT_to_back, similarity=0.98)
            case.result = not check_result

        # [K466] 2.8 MGT > Layer Order > Context menu (Move to top)
        with uuid("753256dd-6f3c-453c-9f9a-737ffda11ce2") as case:
            intro_video_page.click_layer_order(1)
            time.sleep(DELAY_TIME*3)
            img_MGT_to_Font = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_result = main_page.compare(img_initial, img_MGT_to_Font, similarity=0.99)
            case.result = check_result

        intro_video_page.click_undo_button()
        intro_video_page.click_preview_center()

        # [K686] 2.9.1 Add Color Board > Layer Order > Context menu (Move to top)
        with uuid("6225169e-fc3a-44e6-8524-f206ad1b40b1") as case:
            check_button = intro_video_page.click_layer_order(1)
            img_color_board_to_top = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_result = main_page.compare(img_MGT_to_back, img_color_board_to_top, similarity=0.99)
            case.result = check_button and (not check_result)

        # [K681] Add Color Board > Change Color > Button
        with uuid("02aa8433-23ab-4850-91e3-28dbbd048172") as case:
            intro_video_page.click_change_color('0C0D35')
            img_change_color = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_result = main_page.compare(img_color_board_to_top, img_change_color, similarity=0.98)
            case.result = (not check_result)

        # [K636] Add Color Board > Edit object settings > Click Button
        with uuid("3de77d2a-978c-4f1b-9d42-ab9c583964d0") as case:
            result = intro_video_page.image.click_object_settings_btn()
            case.result = result
            time.sleep(DELAY_TIME*2)

        # [K645] Add Color Board > Edit object settings > Border tab > Enable
        with uuid("83cb2cfb-b24f-4975-b3c0-bc3012516e2e") as case:
            intro_video_page.image.object_settings.unfold_border(1)
            check_initial = intro_video_page.image.object_settings.get_border_status()
            intro_video_page.image.object_settings.enable_border(1)
            time.sleep(DELAY_TIME * 2)
            set_result = intro_video_page.image.object_settings.get_border_status()
            case.result = (not check_initial) and set_result

        # [K648] Add Color Board > Edit object settings > Click Button
        with uuid("6047648f-8e10-436a-b764-7082f1804be3") as case:
            check_intial_border = intro_video_page.image.object_settings.get_border_size()
            logger(check_intial_border)
            check_intial_border = int(check_intial_border)
            if check_intial_border != 3:
                new_value = 3
                initial_result = False
            else:
                new_value = 10
                initial_result = True

            logger(new_value)

            intro_video_page.image.object_settings.set_border_size(new_value)
            time.sleep(DELAY_TIME * 2)
            set_result = intro_video_page.image.object_settings.get_border_size()
            new_value = str(new_value)
            if set_result != new_value:
                set_size_result = False
            else:
                set_size_result = True

            case.result = initial_result and set_size_result

            # Close (Object Settings window)
            main_page.press_esc_key()

        # [K692] 2.9.1 Add Color Board > Layer Order > Context menu (Move to button)
        with uuid("a3ae16e5-a12e-44c9-aab1-a6d22e6b4633") as case:
            check_button = intro_video_page.click_layer_order(4)
            img_color_board_to_button = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_result = main_page.compare(img_initial, img_color_board_to_button, similarity=0.99)
            case.result = check_button and (not check_result)

        # [K318] 2.7 Add Text - General text > Right Click Menu > Context menu (Move to button)
        with uuid("07fd1eb6-bb18-4b62-b0de-bfc589694252") as case:
            intro_video_page.click_undo_button()
            intro_video_page.click_undo_button()
            time.sleep(DELAY_TIME)
            # Cancel selection
            intro_video_page.cancel_selection_button()

            # Add text
            intro_video_page.click_add_text(1)
            time.sleep(DELAY_TIME*2)
            img_add_title_top = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_text_result_1 = main_page.compare(img_add_title_top, img_change_color, similarity=0.99)
            logger(check_text_result_1)
            intro_video_page.hover_preview_center()
            main_page.right_click()
            intro_video_page.select_right_click_menu('Send to Back')
            time.sleep(DELAY_TIME*3)
            img_title_back = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_text_result = main_page.compare(img_add_title_top, img_title_back, similarity=0.99)
            logger(check_text_result)
            case.result = (not check_text_result_1) and (not check_text_result)

        # [K375] 2.7 Add Text - General text > Layer Order > Button (Click)
        with uuid("36518e07-6be5-49fe-b787-40c8da72c2d3") as case:
            # [K377] 2.7 Add Text - General text > Layer Order > Context Menu > Move to top
            with uuid("236886a2-b92d-4ebb-87bf-f3eefcfdee3d") as case:
                check_button = intro_video_page.click_layer_order(1)
                time.sleep(DELAY_TIME * 3)
                img_title_to_top = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
                check_result = main_page.compare(img_add_title_top, img_title_to_top, similarity=0.99)
                case.result = check_button and check_result
            case.result = check_button and check_result

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_13(self):

        # enter Video Intro Room
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 3)
        intro_video_page.enter_my_favorites()

        # select 1st template
        intro_video_page.select_intro_template_method_2(1)

        # enter designer
        main_page.double_click()
        self.download_intro_complete()
        img_initial = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

        # [K741] 2.10 Video Overlay (Pip) > Right click menu > Move to button
        with uuid("9198808f-24c7-41e7-9649-f4fa49f6f316") as case:
            # select sticker object
            ori_pos = main_page.exist(L.intro_video_room.intro_video_designer.preview_area).AXPosition
            size_w, size_h = main_page.exist(L.intro_video_room.intro_video_designer.preview_area).AXSize
            new_pos = (ori_pos[0] + size_w * (0.2), ori_pos[1] + size_h * (0.4))
            main_page.mouse.move(new_pos[0], new_pos[1])
            time.sleep(DELAY_TIME)
            main_page.mouse.click()
            time.sleep(DELAY_TIME)

            # Move to button
            main_page.right_click()
            intro_video_page.select_right_click_menu('Send to Back')
            time.sleep(DELAY_TIME * 2)
            img_sticker_back = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_to_back_result = main_page.compare(img_initial, img_sticker_back, similarity=0.99)
            case.result = not check_to_back_result

        # [K803] 2.10 Video Overlay (Pip) > Layer Order > Button (Click)
        with uuid("1750e092-b6f1-4bb2-92b2-85c0505d3d9e") as case:
            # [K805] 2.10 Video Overlay (Pip) > Layer Order > Context Menu > Move to top
            with uuid("bb7ff543-6069-435f-83c7-8084ccc38fd2") as case:
                check_button = intro_video_page.click_layer_order(1)
                time.sleep(DELAY_TIME*2)
                img_sticker_to_top = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
                check_result = main_page.compare(img_initial, img_sticker_to_top, similarity=0.99)
                case.result = check_button and check_result
            case.result = check_button and check_result

        # [K811] 2.10 Video Overlay (Pip) > Layer Order > Context Menu > Move to button
        with uuid("8dd23960-2b0b-4d0f-b352-15d6a692e39c") as case:
            check_button = intro_video_page.click_layer_order(4)
            img_sticker_to_back = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_result = main_page.compare(img_sticker_back, img_sticker_to_back, similarity=0.99)
            case.result = check_button and check_result

        # [K735] 2.10 Video Overlay (Pip) > Right click menu > Move to top
        with uuid("1de6a729-6fc9-4e7c-88e6-254b2276d0c6") as case:
            main_page.mouse.move(new_pos[0], new_pos[1])
            time.sleep(DELAY_TIME)
            main_page.mouse.click()
            time.sleep(DELAY_TIME)

            # Move to button
            main_page.right_click()
            intro_video_page.select_right_click_menu('Bring to Front')
            time.sleep(DELAY_TIME * 2)
            img_sticker_font = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
            check_to_front_result = main_page.compare(img_sticker_font, img_sticker_to_top, similarity=0.99)
            case.result = check_to_front_result

    # 3 uuid (Share template) + 1 uuid (Check My Profile DZ button)
    # If share successfully then delete it
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_1(self):
        # aspect ratio is (1:1)
        main_page.set_project_aspect_ratio_1_1()

        # Insert Food to timeline
        # main_page.select_library_icon_view_media("Food.jpg")
        main_page.select_library_icon_view_media("Landscape 01.jpg")
        main_page.right_click()
        main_page.select_right_click_menu("Insert on Selected Track")

        # enter Video Intro Room
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 4)

        # Open (My Profile)
        intro_video_page.enter_my_profile()
        time.sleep(DELAY_TIME * 10)
        img_my_profile_initial = intro_video_page.snapshot(locator=L.intro_video_room.my_profile.main_window)
        # Close (My Profile)
        main_page.press_esc_key()

        # Sort by date
        self.sort_by_date()
        time.sleep(DELAY_TIME * 4)

        # select category
        intro_video_page.click_intro_specific_category('Health')
        time.sleep(DELAY_TIME * 3)

        # select 2nd template
        intro_video_page.select_intro_template_method_2(2)

        # Drag to timeline
        intro_video_page.drag_intro_media_to_timeline_playhead_position(2)

        # Click yes to enter Video Intro designer
        if main_page.exist({'AXIdentifier': 'IDD_CLALERT'}):
            main_page.click(L.base.confirm_dialog.btn_yes)
            self.download_intro_complete()

        # Replace video from GI
        intro_video_page.click_replace_media(2)
        time.sleep(6)
        getty_image_page.handle_what_is_stock_media()
        time.sleep(DELAY_TIME*2)
        download_from_ss_page.search.search_text('ocean ocean swim girl')
        time.sleep(DELAY_TIME * 2)
        download_from_ss_page.video.select_thumbnail_for_video_intro_designer(index=9)

        # handle High definition
        time.sleep(DELAY_TIME)
        media_room_page.handle_high_definition_dialog(option='no')

        # if open trim dialog
        if main_page.exist(L.trim.main_window, timeout=10):
            time.sleep(DELAY_TIME * 5)
            main_page.press_esc_key()
            time.sleep(DELAY_TIME * 5)

        # Set designer timecode (00:00) to get last sec
        intro_video_page.set_designer_timecode('00_00')
        time.sleep(DELAY_TIME*2)
        # Check designer preview is OK
        img_initial = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
        main_page.press_space_key()
        time.sleep(DELAY_TIME*2)
        img_play = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
        check_play_result = main_page.compare(img_initial, img_play, similarity=0.995)

        if check_play_result:
            logger('Verify Preview [NG], preview does not update when play')
            raise Exception

        # [K585] 2.13 Share dialog > Click (Open Share Template page)
        with uuid("8e2994b7-399f-434d-a0b9-8807037772ed") as case:
            # Click [Share Template] button
            intro_video_page.click_btn_share_template('Swim')

            # Confirm Copyright Disclaimer
            result = intro_video_page.share_temp.click_confirm()
            case.result = result

        # [K609] 2.13 Share dialog > Success share > Done
        with uuid("42d3ff28-cfd9-47a3-8c41-1318de3381e5") as case:

            # [K601] 2.13 Share dialog > Share button
            with uuid("c71942ad-d25b-48d9-ba72-7c82ae905755") as case:
                result = intro_video_page.share_temp.click_share()
                case.result = result

                # Click [Close] to leave designer
                intro_video_page.click_btn_close()

            # Open (My Profile)
            intro_video_page.enter_my_profile()
            time.sleep(DELAY_TIME * 10)
            img_my_profile_added = intro_video_page.snapshot(locator=L.intro_video_room.my_profile.main_window)
            # Close (My Profile)
            main_page.press_esc_key()
            # Check (My Profile) is changed
            check_add_result = main_page.compare(img_my_profile_initial, img_my_profile_added, similarity=0.7)

            case.result = result and (not check_add_result)

        # If share successfully, then delete template
        if not check_add_result:
            # Open (My Profile)
            intro_video_page.enter_my_profile()
            time.sleep(DELAY_TIME * 10)

            intro_video_page.my_profile.delete_1st_template()
            time.sleep(DELAY_TIME * 5)

        # close (My Profile)
        main_page.press_esc_key()
        time.sleep(DELAY_TIME*2)

        # [K109] 1.6 My Profile > Cyberlink DZ
        with uuid("be29d6ae-af4c-4f50-b1a0-7556e3094971") as case:
            # Open (My Profile)
            intro_video_page.enter_my_profile()
            time.sleep(DELAY_TIME * 10)

            main_page.click(L.intro_video_room.my_profile.btn_dz)
            time.sleep(DELAY_TIME*3)

            result = main_page.check_chrome_page()
            time.sleep(DELAY_TIME)
            main_page.tap_close_chrome_tab_hotkey()
            # Verify : Open Chrome page
            if result:
                case.result = True
            else:
                case.result = False

    # 2 uuid (Search library with CHT/JPN)
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_2(self):
        # enter Video Intro Room
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME * 4)

        # [K53] 1.4 Search bar > Search JPN
        # PC bug code: VDE222031-0089
        with uuid("41c4ef13-09aa-45f8-80b9-44da26cc51c5") as case:

            # Input search keyword
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('スイーツ')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME*3)
            current_preview = intro_video_page.snapshot(locator=produce_page.area.preview.main,
                                                          file_name=Auto_Ground_Truth_Folder + 'Search_JPN_result.png')

            check_result = produce_page.compare(Ground_Truth_Folder + 'Empty_result.png', current_preview, similarity=0.98)
            time.sleep(DELAY_TIME * 2)
            case.result = not check_result

        # [K52] 1.4 Search bar > Search CHT
        # PC bug code: VDE222031-0089
        with uuid("8f688dce-1e72-4dfc-9d62-839b7b87c61f") as case:

            # switch to Title room
            main_page.tap_TitleRoom_hotkey()
            time.sleep(DELAY_TIME*2)

            # enter Video Intro Room
            intro_video_page.enter_intro_video_room()

            # Input search keyword
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('父親')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME*3)
            current_preview = intro_video_page.snapshot(locator=produce_page.area.preview.main,
                                                          file_name=Auto_Ground_Truth_Folder + 'Search_CHT_result.png')

            check_result = produce_page.compare(Ground_Truth_Folder + 'Empty_result.png', current_preview, similarity=0.98)
            time.sleep(DELAY_TIME * 2)
            case.result = not check_result

    # Bug code: VDE224508-0018
    # Detect the crash case if (Download media from cloud) then select all to delete
    # @pytest.mark.skip
    @exception_screenshot
    def test_3_1_1(self):
        # [K979] 4.1 Bug list [S1]
        with uuid("f57fe1c3-a24d-4a85-8d4a-e3d38cce6888") as case:
            # enter Media Room > Downloaded category
            media_room_page.enter_downloaded()
            time.sleep(DELAY_TIME * 8)
            before_downloaded_status = main_page.screenshot()
            logger(before_downloaded_status)

            # enter media content
            media_room_page.enter_media_content()
            media_room_page.collection_view_deselected_media()
            media_room_page.right_click()
            media_room_page.select_right_click_menu('Download from', 'Download Media from CyberLink Cloud...')
            import_media_from_cloud_page.is_exist(L.import_downloaded_media_from_cl.downloaded_media_window, timeout=30)
            time.sleep(DELAY_TIME*4)

            # Step 1: Video Page > Double click "1st" folder (name: PowerDirector)
            import_media_from_cloud_page.double_click_folder(folder_index=0)
            time.sleep(DELAY_TIME * 2)

            # Step 2: Search keyword 'at'
            import_media_from_cloud_page.input_text_in_seacrh_library('at')
            time.sleep(DELAY_TIME * 2)

            # Step 3: Select all
            import_media_from_cloud_page.tap_select_deselect_all_btn()
            time.sleep(DELAY_TIME)

            # Step 4: Click [Download]
            import_media_from_cloud_page.tap_download_btn()

            time_count = 0
            for x in range(60):
                if time_count == 3:
                    break
                result = media_room_page.is_show_high_definition_dialog()
                if result:
                    media_room_page.handle_high_definition_dialog()
                    time_count = time_count + 1
                else:
                    time.sleep(1)

            time.sleep(DELAY_TIME * 6)
            import_media_from_cloud_page.tap_ok_btn()
            time.sleep(DELAY_TIME * 5)

            # Step 5: Close (Download Media) window
            for x in range(3):
                main_page.press_esc_key()
                time.sleep(DELAY_TIME)

            # Step 6: Select all videos
            # AT_h264_fullhd.mp4, AT_h265.mkv, AT_h265_fullhd.mp4, AT_xavc.mp4, AT_xavc_hd.mp4
            media_room_page.select_media_content('AT_264_fullhd.mp4')
            main_page.tap_command_and_hold()
            media_room_page.select_media_content('AT_h265.mkv')
            media_room_page.select_media_content('AT_h265_fullhd.mp4')
            media_room_page.select_media_content('AT_xavc.mp4')
            media_room_page.select_media_content('AT_xavc_hd.mp4')

            # Step 7 : Top Menu Bar > Click [Edit] Menu > Click (Remove)
            main_page.top_menu_bar_edit_remove()
            time.sleep(DELAY_TIME*2)
            main_page.release_command_key()
            if main_page.find(L.main.confirm_dialog.main_window):
                main_page.click(L.main.confirm_dialog.btn_yes)

            # Step 8: Check pop up WER dialog / Close PDR
            time.sleep(DELAY_TIME * 6)
            after_remove_video = main_page.screenshot()
            logger(after_remove_video)

            # Verify Step:
            check_result = main_page.compare(before_downloaded_status, after_remove_video)
            case.result = check_result
            logger(check_result)

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_1_2(self):
        # [K980] 4.1 Bug list [S1] : Bugcode (VDE224722-0038)
        with uuid("d972e421-cd03-40fb-acea-5e8d1a176a3c") as case:
            # Enable volume meter
            check_enable = main_page.top_menu_bar_view_show_timeline_preview_volume_meter()
            if not check_enable:
                logger('Test_3_1_2: Cannot enable volume meter')
                raise Exception

            # Enable 5.1 channel
            # Open Preference setting > General > Audio channel > Set 5.1 Surround
            main_page.click_set_user_preferences()
            time.sleep(DELAY_TIME * 2)
            preferences_page.general.audio_channels_set_51_surround()
            time.sleep(DELAY_TIME)

            # Click OK to close (Preference setting)
            preferences_page.click_ok()

            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()

            main_page.select_timeline_media('Skateboard 01')
            time.sleep(DELAY_TIME)

            # Enter (Video Speed)
            tips_area_page.tools.select_VideoSpeed()
            time.sleep(DELAY_TIME)

            # Switch to (Selected Range)
            video_speed_page.Edit_VideoSpeedDesigner_SelectTab('selected range')

            # Click [Time Shift]
            check_result = video_speed_page.VideoSpeedDesigner_SelectRange_Click_Upper_CreateTimeShift_btn()
            logger(check_result)
            time.sleep(DELAY_TIME * 2)

            # Verify Step 1:
            # Check (Time Shift) button is disable
            elem_btn = main_page.exist(L.video_speed.time_shift_1)
            if elem_btn.AXEnabled == False:
                verify_step = True
            else:
                verify_step = False

            # Apply Speed multiplier = 9.1
            # Set speed to 9.1 for (Time shift)
            video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_SetValue(9.1)
            time.sleep(DELAY_TIME)
            video_speed_page.Edit_VideoSpeedDesigner_ClickOK()

            # Click [Play] then pause
            playback_window_page.Edit_Timeline_PreviewOperation('play')
            time.sleep(DELAY_TIME * 5)
            main_page.press_space_key()

            # Verify step 2:
            preview_area = main_page.is_exist(L.base.Area.preview.only_mtk_view)

            case.result = verify_step and preview_area

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_1_3(self):
        # [K981] 4.1 Bug list [S1] : Bugcode (VDE224621-0024)
        with uuid("902f6afe-60f5-49d3-9af8-72717948f856") as case:
            # Enter Title Room
            main_page.enter_room(1)
            time.sleep(DELAY_TIME*4)
            # Select Motion Graphics category
            main_page.select_LibraryRoom_category('Motion Graphics')

            # Search MGT2
            media_room_page.search_library('Motion Graphics 002')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media('Motion Graphics 002')
            time.sleep(DELAY_TIME)

            # Double click to enter title designer
            main_page.double_click()
            time.sleep(DELAY_TIME * 2)
            title_designer_page.mgt.click_warning_msg_ok()

            check_title_caption = title_designer_page.get_title()
            logger(check_title_caption)

            if check_title_caption == 'Motion Graphics 002':
                open_title_designer = True
            else:
                open_title_designer = False
                logger(open_title_designer)

            # Adjust object on preview > Rotate
            title_designer_page.adjust_title_on_canvas.drag_rotate_clockwise('120')
            time.sleep(DELAY_TIME * 2)

            # Verify Step:
            undo_btn = main_page.exist(L.title_designer.btn_undo)
            if undo_btn.AXEnabled == True:
                verify_step = True
            else:
                verify_step = False
                logger(verify_step)

            # Click [Undo]
            title_designer_page.click_undo_btn()
            time.sleep(DELAY_TIME * 2)

            # Click [Max] button
            title_designer_page.click_maximize_btn()
            time.sleep(DELAY_TIME * 2)

            # Verify Step:
            check_title_caption = title_designer_page.get_title()

            if check_title_caption == 'Motion Graphics 002':
                after_click_max = True
            else:
                after_click_max = False
                logger(after_click_max)

            case.result = open_title_designer and verify_step and after_click_max


    # @pytest.mark.skip
    @exception_screenshot
    def test_3_1_4(self):
        # [K982] 4.1 Bug list [S1] : Bugcode (VDE235114-0019)
        with uuid("1e5810ec-2b19-4123-8d81-858439a263af") as case:
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()

            main_page.select_timeline_media('Skateboard 01')
            time.sleep(DELAY_TIME)

            # Enter Subtitle Room
            main_page.enter_room(8)
            time.sleep(DELAY_TIME * 2)

            # Click [Create Subtitle manually]
            subtitle_room_page.library_menu.click_manually_create()

            # Click [+] button
            subtitle_room_page.click_add_btn()
            time.sleep(DELAY_TIME)

            # Add subtitle text on subtitle no.1
            subtitle_room_page.modify_subtitle_text(1, string1='55555')
            time.sleep(DELAY_TIME * 2)

            # Modify subtitle text on subtitle no.1
            subtitle_room_page.modify_subtitle_text_without_clear_old_text(1, string1='7', right_times=5)
            time.sleep(DELAY_TIME * 2)

            # Click [Split]
            subtitle_room_page.click_split_btn()
            time.sleep(DELAY_TIME * 2)

            case.result = main_page.is_exist(L.subtitle_room.btn_split)

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_1_5(self):
        # [K983] 4.1 Bug list [S1] : Bugcode (VDE235028-0010)
        with uuid("11c5ac63-2eee-494c-818a-e0c9b908553e") as case:
            # enter Video Intro Room
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            intro_video_page.enter_my_favorites()
            time.sleep(DELAY_TIME * 3)

            # select 1st template
            intro_video_page.select_intro_template_method_2(1)

            # enter Intro designer
            main_page.double_click()
            time.sleep(DELAY_TIME * 11)
            img_initial = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            # select Sticker object
            ori_pos = main_page.exist(L.intro_video_room.intro_video_designer.preview_area).AXPosition
            size_w, size_h = main_page.exist(L.intro_video_room.intro_video_designer.preview_area).AXSize
            new_pos = (ori_pos[0] + size_w * (0.2), ori_pos[1] + size_h * (0.4))
            main_page.mouse.move(new_pos[0], new_pos[1])
            time.sleep(DELAY_TIME)
            main_page.mouse.click()
            time.sleep(DELAY_TIME*3)

            # Click [Replace] button
            intro_video_page.image.click_replace_btn()
            time.sleep(DELAY_TIME*3)

            # Replace sticker
            intro_video_page.select_pip_template(3, 'Seasonal')
            time.sleep(DELAY_TIME*5)
            img_sticker_2 = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

            # Verify Step:
            preview_no_update = main_page.compare(img_initial, img_sticker_2, similarity=0.98)
            logger(preview_no_update)

            # Click [Undo]
            intro_video_page.click_undo_button()
            time.sleep(DELAY_TIME)

            # Move mouse to any position for delay three sec.
            main_page.mouse.move(new_pos[0] + 450, new_pos[1] + 5)
            time.sleep(DELAY_TIME)
            main_page.mouse.move(new_pos[0] + 480, new_pos[1] - 100)
            time.sleep(DELAY_TIME)
            main_page.mouse.move(new_pos[0] + 510, new_pos[1] + 2)
            time.sleep(DELAY_TIME*2)

            # Click [Undo]
            intro_video_page.click_undo_button()
            time.sleep(DELAY_TIME)

            # Click [Close] to leave intro designer
            intro_video_page.click_upper_close_btn()
            time.sleep(DELAY_TIME * 3)

            # Enter Pip Room then verify step
            check_result = main_page.enter_room(4)

            case.result = (not preview_no_update) and check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_1_6(self):
        # [K984] 4.1 Bug list [S1] : Bugcode (VDE235413-0028)
        with uuid("5c45ab41-8d6e-4972-a5be-022d72392053") as case:
            cutout_loop = 20
            for x in range(cutout_loop):
                logger('----')
                logger(x)
                cutout_result = self.easy_cutout()

                # new workspace
                main_page.tap_NewWorkspace_hotkey()
                main_page.handle_no_save_project_dialog('no')
                logger(cutout_result)
                logger('----')
            case.result = cutout_result

    def enter_pip_designer_then_click_ok(self):
        # Click TipsArea > Pip Designer
        check_status = tips_area_page.tools.select_PiP_Designer()
        if not check_status:
            raise Exception

        # Click [OK]
        pip_designer_page.click_ok()
        time.sleep(DELAY_TIME * 2)

    def apply_path_out_animation_for_second_video(self, f):

        # Insert Y man.mp4
        video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert 473327443_fhd.mov
        main_page.select_library_icon_view_media('Y man.mp4')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()

        # Set timecode
        main_page.set_timeline_timecode('00_00_09_00')
        time.sleep(DELAY_TIME * 2)

        # Click Split
        tips_area_page.click_TipsArea_btn_split()

        # View entire video
        timeline_operation_page.click_view_entire_video_btn()

        # Select clip # 2 of track 1 to remove
        timeline_operation_page.select_timeline_media(0,1)
        time.sleep(DELAY_TIME * 2)
        tips_area_page.more_features.remove(1)

        # Bug: Step 6 <-- end
        time.sleep(DELAY_TIME * 2)
        self.detect_memory_usage(f, 6)

        # Insert HEVC clip
        video_path = Test_Material_Folder + 'Timeline_Right_Click_Menu/TheIncredibles_HEVC.ts'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Select timeline track 2
        main_page.timeline_select_track(2)
        time.sleep(DELAY_TIME * 2)

        # Set timecode
        main_page.set_timeline_timecode('00_00_16_02')
        time.sleep(DELAY_TIME * 5)

        # Insert TheIncredibles_HEVC.ts
        main_page.select_library_icon_view_media('TheIncredibles_HEVC.ts')
        time.sleep(DELAY_TIME * 4)
        media_room_page.library_clip_context_menu_insert_on_selected_track()

        # Bug: Step 7 <-- end
        time.sleep(DELAY_TIME * 2)
        self.detect_memory_usage(f, 7)

        # Click TipsArea > Pip Designer
        check_status = tips_area_page.tools.select_PiP_Designer()
        if not check_status:
            raise Exception

        # =====
        # Switch to Advanced mode
        pip_designer_page.switch_mode('Advanced')
        time.sleep(DELAY_TIME * 4)

        # Switch (Motion) tab
        pip_designer_page.advanced.switch_to_motion()
        time.sleep(DELAY_TIME * 3)

        # Unfold path
        pip_designer_page.advanced.unfold_path_menu(set_unfold=1)
        time.sleep(DELAY_TIME * 2)
        # Apply one path
        pip_designer_page.path.select_template(8)
        time.sleep(DELAY_TIME * 3)

        # Switch (Animation) tab
        pip_designer_page.advanced.switch_to_animation()
        time.sleep(DELAY_TIME * 3)

        # Fold (In Animation)
        pip_designer_page.advanced.unfold_in_animation_menu(set_unfold=0)
        time.sleep(DELAY_TIME * 2)
        # Unfold (Out Animation) then apply one (Out Animation)
        pip_designer_page.advanced.unfold_out_animation_menu(set_unfold=1)
        time.sleep(DELAY_TIME * 2)
        # Apply one (Out animation)
        pip_designer_page.out_animation.select_template(10)
        time.sleep(DELAY_TIME * 2)

        # Unfold (In Animation)
        pip_designer_page.advanced.unfold_in_animation_menu(set_unfold=1)
        # Apply one (In animation)
        pip_designer_page.in_animation.select_template(11)
        time.sleep(DELAY_TIME * 2)

        # Bug: Step 8 <-- end
        time.sleep(DELAY_TIME * 2)
        self.detect_memory_usage(f, 8)

    def back_properties_apply_auto_cutout(self, f):
        # Switch (Properties) tab
        pip_designer_page.advanced.switch_to_properties()

        # =====
        # Apply cutout
        pip_designer_page.apply_chromakey()
        time.sleep(DELAY_TIME * 2)

        # Get cutout status
        cutout_button_object = main_page.exist(L.pip_designer.chromakey.cutout_button)
        #logger(cutout_button_object.AXValue)
        if cutout_button_object.AXValue == 0:
            main_page.click(L.pip_designer.chromakey.cutout_button)
            time.sleep(DELAY_TIME * 2)

        # Bug: Step 9 <-- end
        time.sleep(DELAY_TIME * 2)
        self.detect_memory_usage(f, 9)

        # check current preview
        apply_cutout_result = main_page.snapshot(L.pip_designer.preview)
        logger(apply_cutout_result)

        # Move cutout object to left
        pip_designer_page.move_to_left_on_canvas(-30)
        time.sleep(DELAY_TIME * 3)

        # Move cutout object to left
        pip_designer_page.move_to_left_on_canvas(-30)
        time.sleep(DELAY_TIME * 2)

        # check current preview
        move_left_result = main_page.snapshot(L.pip_designer.preview)
        logger(move_left_result)

        # Click [OK]
        pip_designer_page.click_ok()
        time.sleep(DELAY_TIME * 2)

        # Bug: Step 10 <-- end
        self.detect_memory_usage(f, 10)

    @exception_screenshot
    def bug_regression(self, f):
        # Bug regression (VDE235413-0028)
        # Insert Sport 01.jpg
        main_page.select_library_icon_view_media('Sport 02.jpg')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()
        # Bug: Step 2 <-- end
        time.sleep(DELAY_TIME * 2)
        self.detect_memory_usage(f, 2)

        # Click TipsArea > Pip Designer
        check_status = tips_area_page.tools.select_PiP_Designer()
        if not check_status:
            raise Exception

        # Switch to Advanced mode
        pip_designer_page.switch_mode('Advanced')
        time.sleep(DELAY_TIME * 2)

        # Switch (Motion) tab
        pip_designer_page.advanced.switch_to_motion()

        # Unfold path
        pip_designer_page.advanced.unfold_path_menu(set_unfold=1)

        # Apply one path
        pip_designer_page.path.select_template(4)

        # Switch (Animation) tab
        pip_designer_page.advanced.switch_to_animation()

        # Unfold (In Animation) then apply one (In Animation)
        pip_designer_page.advanced.unfold_in_animation_menu(set_unfold=1)

        # Apply one path
        pip_designer_page.in_animation.select_template(7)
        # Bug: Step 3 <-- end
        time.sleep(DELAY_TIME * 2)
        self.detect_memory_usage(f, 3)

        # Switch (Animation) tab
        pip_designer_page.advanced.switch_to_properties()

        # Apply cutout
        pip_designer_page.apply_chromakey()
        time.sleep(DELAY_TIME * 2)

        # Get cutout status then Enable Auto cutout
        cutout_button_object = main_page.exist(L.pip_designer.chromakey.cutout_button)
        #logger(cutout_button_object.AXValue)
        if cutout_button_object.AXValue == 0:
            main_page.click(L.pip_designer.chromakey.cutout_button)
            # Check download cutout module is ready or not
            self.download_cutout_complete()

        # Click [OK]
        pip_designer_page.click_ok()
        time.sleep(DELAY_TIME * 2)

        # Bug: Step 4 <-- end
        time.sleep(DELAY_TIME * 2)
        self.detect_memory_usage(f, 4)

        # Select clip # 1 of track 1 to Enter Pip Designer again
        timeline_operation_page.select_timeline_media(0,0)
        time.sleep(DELAY_TIME * 2)

        # Click TipsArea > Pip Designer and click [OK]
        self.enter_pip_designer_then_click_ok()

        # Set timecode
        main_page.set_timeline_timecode('00_00_05_00')
        time.sleep(DELAY_TIME * 2)

        # Insert another video ( Y man and TheIncredibles_HEVC.ts) to timeline then apply out animation & cutout
        self.apply_path_out_animation_for_second_video(f)

        self.back_properties_apply_auto_cutout(f)
        # Select clip # 1 of track 1 to Enter Pip Designer again
        timeline_operation_page.select_timeline_media(2,0)
        time.sleep(DELAY_TIME * 2)

        # Click TipsArea > Pip Designer and click [OK]
        self.enter_pip_designer_then_click_ok()
        # Bug: Step 11 <-- end
        time.sleep(DELAY_TIME * 2)
        self.detect_memory_usage(f, 11)


        # Play preview then pause
        playback_window_page.Edit_Timeline_PreviewOperation('play')
        time.sleep(DELAY_TIME * 5)
        # Bug: Step 12 <-- end
        time.sleep(DELAY_TIME * 2)
        self.detect_memory_usage(f, 12)

        playback_window_page.Edit_Timeline_PreviewOperation('pause')
        time.sleep(DELAY_TIME * 5)
        # Bug: Step 13 <-- end
        time.sleep(DELAY_TIME * 2)
        self.detect_memory_usage(f, 13)

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_1_7(self):
        # [K985] 4.1 Bug list [S1] : Bugcode (VDE235413-0028)
        # report path
        detect_memory_report = main_page.get_project_path('SFT/Report') + '/AT_RAM_usage_report.txt'
        logger(detect_memory_report)
        f = open(detect_memory_report, 'w')

        f.write('---- BFT_Video_Intro_Designer : test_3_1_7 ----\n')
        with uuid("da381584-c9d5-4094-b90b-77119e7f024d") as case:
            cutout_loop = 20
            for x in range(cutout_loop):
                logger('----')
                logger(x)
                number = x + 1
                f.write(f'\n[Loop {number}] \n')
                self.bug_regression(f)

                # new workspace
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)

                main_page.handle_no_save_project_dialog('no')
                time.sleep(DELAY_TIME * 2)
                # Bug: Step 14 <-- end
                self.detect_memory_usage(f, 14)

                media_room_page.enter_media_content()
                logger('----')

            # Only check PDR is fine or crash
            case.result = main_page.select_library_icon_view_media('Food.jpg')

        self.detect_memory_usage(f, 'final')
        f.write('---- Test end  ----\n')
        f.close()

    @pytest.mark.skip
    @exception_screenshot
    def test_3_1_8(self):
        # Only testing for RD request (VDE235625-0007) Step14: Save project, Step15: New workspace
        # [K985] 4.1 Bug list [S1] : Bugcode (VDE235413-0028)
        # report path
        detect_memory_report = main_page.get_project_path('SFT/Report') + '/AT_RAM_usage_save_project_report.txt'
        logger(detect_memory_report)
        f = open(detect_memory_report, 'w')

        f.write('---- BFT_Video_Intro_Designer : test_3_1_8 ----\n')
        with uuid("da381584-c9d5-4094-b90b-77119e7f024d") as case:
            cutout_loop = 20
            for x in range(cutout_loop):
                logger('----')
                logger(x)
                number = x + 1
                f.write(f'\n[Loop {number}] \n')
                self.bug_regression(f)

                # Step14: Save project:
                main_page.top_menu_bar_file_save_project_as()
                main_page.handle_save_file_dialog(name='test_case_3_1_8',
                                                  folder_path=Test_Material_Folder + 'Video_Intro_Designer/')
                time.sleep(DELAY_TIME * 2)
                # Bug: Step 14 <-- end
                self.detect_memory_usage(f, 14)

                # Step15: new workspace
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)

                #main_page.handle_no_save_project_dialog('no')
                #time.sleep(DELAY_TIME * 2)
                # Bug: Step 15 <-- end
                self.detect_memory_usage(f, 15)

                media_room_page.enter_media_content()
                logger('----')

            # Only check PDR is fine or crash
            case.result = main_page.select_library_icon_view_media('Food.jpg')

        self.detect_memory_usage(f, 'final')
        f.write('---- Test end  ----\n')
        f.close()