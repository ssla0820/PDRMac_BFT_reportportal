import sys, os
import tempfile
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
playback_window_page = PageFactory().get_page_object('playback_window_page', mac)
effect_room_page = PageFactory().get_page_object('effect_room_page', mac)
effect_settings_page = PageFactory().get_page_object('effect_settings_page', mac)
tips_area_page = PageFactory().get_page_object('tips_area_page', mac)
timeline_page = PageFactory().get_page_object('timeline_operation_page', mac)
download_from_ss_page = PageFactory().get_page_object('download_from_shutterstock_page', mac)
fix_enhance_page = PageFactory().get_page_object('fix_enhance_page', mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Scan Effect Setting.html")
cpu_memory_usage = report.get_driver(0)
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
#Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/GroundTruth/Pre_Cut/'
#Auto_Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/ATGroundTruth/Pre_Cut/'
#Test_Material_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/'
Ground_Truth_Folder = app.ground_truth_root + '/Intro_Video_Room/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Intro_Video_Room/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Effect_Settings_Quality():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME*3)
        yield mac
        main_page.close_app()
        main_page.clear_cache()
        time.sleep(DELAY_TIME * 2)

    @classmethod
    def setup_class(cls):
        main_page.clear_cache()
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('Scan_Effect_Settings_Quality')

    @classmethod
    def teardown_class(cls):
        logger('Test Case are completed.')

        logger('teardown_class - export report')
        report.export()
        logger(
            f"Scan Effect Settings Quality result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()

    def enter_style_effect(self):
        # Enter Effect Room
        main_page.enter_room(3)
        time.sleep(DELAY_TIME*4)

        # Close Body Effect bb
        main_page.timeline_select_track(1)

        effect_room_page.select_LibraryRoom_category('Style Effect')
        time.sleep(DELAY_TIME * 2)

    def enter_body_effect(self):
        # Enter Effect Room
        main_page.enter_room(3)
        time.sleep(DELAY_TIME*4)

        # Close Body Effect bb
        main_page.timeline_select_track(1)

        effect_room_page.select_LibraryRoom_category('Body Effect')
        time.sleep(DELAY_TIME)

    def click_modify_then_click_reset(self):
        # Click [Modify] to enter (Effect Settings)
        main_page.click(L.tips_area.button.btn_effect_modify)
        time.sleep(DELAY_TIME * 2)

        # Click [Reset]
        effect_settings_page.click_reset_btn()
        time.sleep(DELAY_TIME * 2)

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

    def check_download_body_effect(self, wait_time=900):
        return self.body_effect_download_complete(wait_time)

    def check_body_effect_apply_not_ok(self):
        return main_page.is_not_exist(L.tips_area.button.btn_effect_modify)

    def apply_effect_to_timeline_clip(self, effect_string):
        main_page.select_library_icon_view_media(effect_string)
        time.sleep(DELAY_TIME * 15)
        main_page.right_click()
        main_page.select_right_click_menu('Apply Selected Effect to All Clips on Selected Track')

    # 3 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1(self):
        # [M395] Add "Aberration" to Effect track
        with uuid("34902466-3097-4265-97b6-9758304ca53d") as case:
            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Select Aberration to effect track
            effect_room_page.apply_effect_to_effecttrack('Aberration')

            # Verify Step:
            if main_page.exist(L.tips_area.button.btn_effect_modify, timeout=7):
                case.result = True
            else:
                case.result = False

        # [M6] Add "Sport 01.jpg" to track 2 > Check Frequency update
        with uuid("b219fa19-c4aa-4ca4-82f4-be52bf20e828") as case:
            # Enter Media room
            main_page.enter_room(0)

            # Snapshot Default "Sport 01.jpg" Ground truth
            main_page.select_library_icon_view_media('Sport 01.jpg')
            time.sleep(DELAY_TIME)

            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to track2
            main_page.timeline_select_track(2)
            main_page.select_library_icon_view_media('Sport 01.jpg')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()

            # Click Aberration of effect track (first click to handle / close Blue bubble)
            main_page.timeline_select_track(2)
            time.sleep(DELAY_TIME)
            timeline_page.get_effect_clip_name(6,0)
            main_page.select_timeline_media('Aberration')
            time.sleep(DELAY_TIME)

            # Click [Modify] to adjust parameter
            main_page.click(L.tips_area.button.btn_effect_modify)
            time.sleep(DELAY_TIME*2)

            # Adjust Frequency
            effect_settings_page.aberration.adjust_frequency_slider()

            # close effect setting
            main_page.click(L.tips_area.button.btn_effect_close)

            # Set timecode = 4 sec.
            main_page.set_timeline_timecode('00_00_04_00')
            time.sleep(DELAY_TIME * 4)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            case.result = not main_page.compare(default_preview, applied_preview, similarity=0.999)

        # [M7] Check Strength adjust
        with uuid("dcd91784-ec8e-43b6-8dfb-af84457d2479") as case:
            # Click [Modify] then close [Reset]
            self.click_modify_then_click_reset()

            # Adjust Strength
            effect_settings_page.aberration.adjust_strength_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview_2 = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            case.result = not main_page.compare(default_preview, applied_preview_2, similarity=0.999)

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_2(self):
        # [M8] Add "Back Light" > Check Strength preview
        with uuid("29e7efdf-f4a1-4aa9-8f6c-b0bd22691cca") as case:
            # Snapshot Default : "Skateboard 01.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)

            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()
            time.sleep(DELAY_TIME * 3)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Back Light')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.back_light.adjust_strength_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.97)
            case.result = adjust_result and preview_update

        # [M10] Add "Back Light" > Check Degree preview
        with uuid("ce9be7de-4cf1-41c3-b816-6582a22121ce") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.back_light.adjust_degree_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.97)
            case.result = adjust_result and preview_update

        # [M11] Add "Back Light" > Check Degree preview
        with uuid("8acf0052-8e34-42e2-8e96-4afc218dd5fd") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.back_light.adjust_light_color('1232C6')
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.999)
            case.result = adjust_result and preview_update

        # [M43] Add "Color Crayon" > Check BG Texture preview
        with uuid("bd6853ca-0c38-4b2d-8e5b-1d1f676d01a2") as case:
            # Click remove button of (Chinese Painting) effect
            effect_settings_page.click_remove_btn()

            # Search library content: Color Crayon
            media_room_page.search_library('Color Crayon')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Color Crayon')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.color_crayon.set_BG_texture()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.985)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M44] Add "Color Painting" > Check Edge Thickness preview
        with uuid("3b6349db-c00c-4380-932b-6971a05bb55a") as case:
            # Click remove button of (Chinese Painting) effect
            effect_settings_page.click_remove_btn()

            # Search library content: Color Painting
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Color Painting')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Color Painting')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.color_painting.adjust_edge_thickness_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M45] "Color Painting" > Check Color Lightness preview
        with uuid("8c1b1e16-5258-4fa2-b76e-472fb3682132") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.color_painting.adjust_color_lightness_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview)
            case.result = adjust_result and preview_update

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_3(self):
        # [M12] Add "Band Noise" > Check Frequency preview
        with uuid("09d2405e-d5fe-4f2f-a4e7-4b5e1fa16add") as case:
            # Snapshot Default : "Skateboard 02.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:03:22
            main_page.set_timeline_timecode('00_00_03_22')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Band Noise')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.band_noise.adjust_frequency_slider()

            # Set timecode 00:00:03:22
            main_page.set_timeline_timecode('00_00_03_22')
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.992)
            case.result = adjust_result and preview_update

        # [M13] Add "Band Noise" > Check Strength preview
        with uuid("b1f4c4ff-0694-430d-952e-b07d7e53d5cb") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.band_noise.adjust_strength_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.999)
            case.result = adjust_result and preview_update

        # [M46] Add "Continuous Shooting" > Check Segment preview
        with uuid("93a4aec2-2268-40b0-82e0-79f2ce42dd2c") as case:
            # Click remove button of (Chinese Painting) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library('Continuous')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Continuous Shooting')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.continuous_shooting.adjust_segment_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.7)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M47] Add "Delay" > Check Regularity preview
        with uuid("151757db-e985-41bb-8f54-4881d9a64df3") as case:
            # Click remove button of (Chinese Painting) effect
            effect_settings_page.click_remove_btn()

            # Select Style Effect category
            effect_room_page.select_LibraryRoom_category('Style Effect')
            time.sleep(DELAY_TIME)

            # Search library content
            media_room_page.search_library('Delay')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Delay')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.delay.adjust_regularity_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M48] Add "Disturbance" > Check Frequency preview
        with uuid("da6813b4-3a48-465b-8b39-2d3706c6f8f6") as case:
            # Click remove button of (Chinese Painting) effect
            effect_settings_page.click_remove_btn()

            # Select Style Effect category
            effect_room_page.select_LibraryRoom_category('Style Effect')
            time.sleep(DELAY_TIME)

            # Search library content
            media_room_page.search_library('Disturbance')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Disturbance')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.disturbance.adjust_frequency_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M49] "Disturbance" > Check Strength preview
        with uuid("59c0243a-e88a-4856-a349-b6f4f1cd77c0") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.disturbance.adjust_strength_slider()
            logger(adjust_result)

            applied_preview_2 = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(applied_preview_2, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_4(self):
        # [M14] Add "Beating" > Check Frequency preview
        with uuid("e4473744-d736-4e9c-8f5b-08a8a19fba01") as case:
            # Snapshot Default : "Skateboard 03.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:01:24
            main_page.set_timeline_timecode('00_00_01_24')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Beating')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.beating.adjust_frequency_slider()
            logger(adjust_result)

            # Click play then pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.press_space_key()

            # Set timecode 00:00:01:24
            main_page.set_timeline_timecode('00_00_01_24')
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M15] Add "Beating" > Check Strength preview
        with uuid("3dff891b-ea07-4665-826f-742d8946cbfa") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.beating.adjust_strength_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.999)
            case.result = adjust_result and preview_update

        # [M50] Add "Disturbance 2" > Check Frequency preview
        with uuid("1940dbc5-6a25-4c2a-822b-100e2e7eb7c3") as case:
            # Click remove button of (Chinese Painting) effect
            effect_settings_page.click_remove_btn()

            # Select Style Effect category
            effect_room_page.select_LibraryRoom_category('Style Effect')
            time.sleep(DELAY_TIME)

            # Search library content
            media_room_page.search_library('Disturbance')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Disturbance 2')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.disturbance_2.adjust_frequency_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M51] "Disturbance 2" > Check Shift preview
        with uuid("f920a9fd-b232-4eb8-b355-bc25f7d26795") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.disturbance_2.adjust_shift_slider()
            logger(adjust_result)

            applied_preview_shift = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(applied_preview_shift, applied_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M52] "Disturbance 2" > Check Strength preview
        with uuid("b42093be-0f36-4808-832c-633702883074") as case:
            # Click [Undo]
            main_page.click_undo()

            # Adjust parameter
            adjust_result = effect_settings_page.disturbance_2.adjust_strength_slider()
            logger(adjust_result)

            applied_preview_strength = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(applied_preview_strength, applied_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M53] "Disturbance 2" > Check Range preview
        with uuid("1f3d7f80-8ba2-4f0f-8d37-2464dd0c749d") as case:
            # Click [Undo]
            main_page.click_undo()

            # Adjust parameter
            adjust_result = effect_settings_page.disturbance_2.adjust_range_slider()
            logger(adjust_result)

            applied_preview_range = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(applied_preview_range, applied_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 1 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_5(self):
        # [M21] Add "Blackout" > Check Frequency preview
        with uuid("b75c3483-f774-4560-94f5-acfba0e4a591") as case:
            # Insert Y man.mp4
            video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:04:25
            main_page.set_timeline_timecode('00_00_04_25')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Blackout')

            # Select timeline clip
            main_page.select_timeline_media('Y man')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.blackout.adjust_frequency_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_6(self):
        # [M22] Add "Bloom" > Check (Sample Number) preview
        with uuid("d1544323-a401-4219-9eaf-f6d3b667f086") as case:
            # Insert Y man.mp4
            video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:06:23
            main_page.set_timeline_timecode('00_00_06_23')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Bloom')

            # Select timeline clip
            main_page.select_timeline_media('Y man')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.bloom.adjust_sample_number_slider()
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M23] "Bloom" > Check (Light Number) preview
        with uuid("58ea6bd2-ee39-4f3b-af45-7d66a64cdcb6") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.bloom.adjust_light_number_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.999)
            case.result = adjust_result and preview_update

        # [M24] "Bloom" > Check (Sample Weight) preview
        with uuid("a42c3980-5941-47f4-a257-cc1919d82d2e") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.bloom.adjust_sample_weight_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.999)
            case.result = adjust_result and preview_update

        # [M25] "Bloom" > Check Angle preview
        with uuid("ed7c265d-f669-4228-ab79-f08a4fc9679f") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.bloom.adjust_angle_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.999)
            case.result = adjust_result and preview_update

        # [M26] "Bloom" > Check Sample Space preview
        with uuid("c24e30e2-8d1e-441b-b001-c489c78cf2ce") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.bloom.adjust_sample_space_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.999)
            case.result = adjust_result and preview_update

        # [M74] Add "Fine Noise" > Check Noise preview
        with uuid("71c40ee7-d5a8-4444-be36-2d753a42a7d4") as case:
            # Click remove button of (Bloom) effect
            effect_settings_page.click_remove_btn()

            # Select Style Effect category
            effect_room_page.select_LibraryRoom_category('Style Effect')
            time.sleep(DELAY_TIME)

            # Search library content
            media_room_page.search_library('Fine Noise')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Fine Noise')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.fine_noise.adjust_noise_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_7(self):
        # Select Default : "Skateboard 03.mp4" to insert track1
        main_page.select_library_icon_view_media('Skateboard 03.mp4')
        time.sleep(DELAY_TIME)

        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:01:17
        main_page.set_timeline_timecode('00_00_01_17')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # Click [Stop] for CTI back to 00:00:00:00
        playback_window_page.Edit_Timeline_PreviewOperation('stop')

        # [M27] Add "Blur Bar" to Effect track > Check Frequency preview
        with uuid("c3d2bc59-d11d-49cf-8a1c-0b0c629a871d") as case:
            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Select Aberration to effect track
            effect_room_page.apply_effect_to_effecttrack('Blur Bar')

            # Click [Modify] to adjust parameter
            main_page.click(L.tips_area.button.btn_effect_modify)
            time.sleep(DELAY_TIME*2)

            # Adjust Frequency
            effect_settings_page.blur_bar.adjust_frequency_slider()
            time.sleep(DELAY_TIME * 2)

            # Click [Close] effect setting
            main_page.click(L.tips_area.button.btn_effect_close)

            # Click [Play] 2 sec. then pause
            playback_window_page.Edit_Timeline_PreviewOperation('play')
            time.sleep(DELAY_TIME * 2)
            main_page.press_space_key()

            # Set timecode 00:00:01:17
            main_page.set_timeline_timecode('00_00_01_17')
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            case.result = not main_page.compare(default_preview, applied_preview, similarity=0.999)

        # [M28] Click "Blur Bar" of Effect track > Check Range preview
        with uuid("be5812b0-9e84-4e0f-8579-c14054d3cb58") as case:
            # Click Blur Bar of effect track
            timeline_page.get_effect_clip_name(6,0)

            # Click [Modify] to adjust parameter
            main_page.click(L.tips_area.button.btn_effect_modify)
            time.sleep(DELAY_TIME*2)

            # Adjust Range
            effect_settings_page.blur_bar.adjust_range_slider()
            time.sleep(DELAY_TIME * 2)

            applied_preview_2 = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            case.result = not main_page.compare(applied_preview_2, applied_preview, similarity=0.999)

        # [M29] Click "Blur Bar" of Effect track > Check Shift preview
        with uuid("b81ada17-d51a-40ad-8dc2-2ad125287857") as case:
            # Set Range to default value (100)
            main_page.exist(L.effect_settings.slider_2).AXValue = 100

            # Adjust Shift
            check_slider_result = effect_settings_page.blur_bar.adjust_shift_slider()
            time.sleep(DELAY_TIME * 2)

            applied_preview_3 = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(applied_preview_3, applied_preview, similarity=0.999)
            case.result = check_slider_result and preview_update

        # [M30] Broken Glass > Check Degree preview
        with uuid("79352669-be27-4511-8f39-8c25bd635d37") as case:
            # Click Blur Bar of effect track > Right click > Click [Remove]
            timeline_page.get_effect_clip_name(6, 0)

            main_page.right_click()
            main_page.select_right_click_menu('Remove')

            # Scroll up for timeline vertical
            timeline_page.drag_timeline_vertical_scroll_bar(0)

            # Select Broken Glass to insert timeline video
            main_page.drag_media_to_timeline_playhead_position('Broken Glass')

            # Click [Modify] to adjust parameter
            main_page.click(L.tips_area.button.btn_effect_modify)
            time.sleep(DELAY_TIME*2)

            # Adjust Degree
            check_slider_result = effect_settings_page.broken_glass.adjust_degree_slider()
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            check_preview = not main_page.compare(default_preview, applied_preview)
            case.result = check_slider_result and check_preview

        # [M62] Add "Dreamy" > Check Degree preview
        with uuid("82b9495b-17c0-4fdc-a710-cacd9b91b929") as case:
            # Click remove button of (Broken Glass) effect
            effect_settings_page.click_remove_btn()

            # Select Style Effect category
            effect_room_page.select_LibraryRoom_category('Style Effect')
            time.sleep(DELAY_TIME)

            # Search library content
            media_room_page.search_library('Dreamy')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Dreamy')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.dreamy.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M63] "Dreamy" > Check Mask type preview
        with uuid("08c9b59e-b3bd-434b-9709-3559f35967ef") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.dreamy.set_mask_type()
            logger(adjust_result)

            applied_preview_circle = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(applied_preview_circle, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M64] "Dreamy" > Check Gradient depth preview
        with uuid("f1602e9e-5598-4132-b3fc-4c21989304d6") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.dreamy.adjust_gradient_depth_slider()
            logger(adjust_result)

            applied_preview_gradient = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(applied_preview_circle, applied_preview_gradient, similarity=0.993)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M66] "Dreamy" > Check invert preview
        with uuid("a47dfb1e-3041-4827-9f8c-03ddd7f7f9e2") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)
            reset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            # Adjust parameter
            adjust_result = effect_settings_page.dreamy.enable_invert_masked_area()
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(reset_preview, applied_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_8(self):
        # [M31] Add "Bump Map" > Check Degree preview
        with uuid("a36fd551-99a5-44d0-9712-da25fbf70c39") as case:
            # Insert girl.mp4
            video_path = Test_Material_Folder + 'Produce_Local/girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:01:25
            main_page.set_timeline_timecode('00_00_01_25')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Bump Map')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.bump_map.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M32] Add "Chinese Painting" > Check Blur preview
        with uuid("ef749a8a-248e-4144-bf11-b488d983a7f4") as case:
            # Click remove button of (Bump map) effect
            effect_settings_page.click_remove_btn()

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Chinese Painting')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.chinese_paint.adjust_blur_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M33] Add "Chinese Painting 2" > Check Brush size preview
        with uuid("4e67788c-9bbc-46de-9fe8-2040a24c2cd0") as case:
            # Click remove button of (Chinese Painting) effect
            effect_settings_page.click_remove_btn()

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Chinese Painting 2')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.chinese_paint_2.adjust_brush_size_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M34] "Chinese Painting 2" > Check Gray Degree preview
        with uuid("3bf98fe2-5a5c-439b-b0b8-428a3366a5c2") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.chinese_paint_2.adjust_gray_degree_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.98)
            case.result = adjust_result and preview_update

        # [M54] Add "Double FishEye" > Check Degree preview
        with uuid("cc6f1e37-bd60-485e-b131-a194dbf1c4ba") as case:
            # Click remove button of (Chinese Painting 2) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library('Double FishEye')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Double FishEye')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.double_fisheye.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update


        # [M57] "Double FishEye" > Check Invert preview
        with uuid("e319ff97-adc3-4951-b365-a5ca0637f27e") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            reset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            # Adjust parameter
            adjust_result = effect_settings_page.double_fisheye.enable_inverse()
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(reset_preview, applied_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M56] "Double FishEye" > Check Size preview
        with uuid("07df22f7-6059-4cfd-8ea2-256a66dae005") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.double_fisheye.adjust_size_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(reset_preview, applied_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M85] Add "Glass" > Check Degree preview
        with uuid("a654bb54-226f-489a-b8b3-46e930447915") as case:
            # Click remove button of (Double FishEye) effect
            effect_settings_page.click_remove_btn()

            # Select Style Effect category
            effect_room_page.select_LibraryRoom_category('Style Effect')
            time.sleep(DELAY_TIME)

            # Search library content
            media_room_page.search_library('Glass')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Glass')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.glass.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_9(self):
        # [M35] Add "Color Balance" > Check Red preview
        with uuid("ef67923d-6943-4064-b09d-29a5dccfd71c") as case:
            # Insert girl.mp4
            video_path = Test_Material_Folder + 'Produce_Local/girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:02:02
            main_page.set_timeline_timecode('00_00_02_02')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()
            time.sleep(DELAY_TIME * 2)

            # Search library content: Color Balance
            media_room_page.search_library('Color Balance')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Color Balance')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.color_balance.adjust_red_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M36] "Color Balance" > Check Blue preview
        with uuid("a2405b7f-8fd9-49bc-86dc-d286b5b4cabe") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.color_balance.adjust_blue_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.98)
            case.result = adjust_result and preview_update

        # [M37] "Color Balance" > Check Green preview
        with uuid("01720f51-3f67-4cfb-a2ac-91fdcd5560a6") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.color_balance.adjust_green_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.98)
            case.result = adjust_result and preview_update

        # [M38] "Color Balance" > Check Gradient Depth preview
        with uuid("632060b5-9f26-4a11-9355-b97fd027621a") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.color_balance.adjust_gradient_depth_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.98)
            case.result = adjust_result and preview_update

        # [M39] "Color Balance" > Check Mask type preview
        with uuid("d32463fe-bd40-4e3f-a549-592cdd9fb3c4") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.color_balance.set_mask_type()
            time.sleep(DELAY_TIME * 2)
            adjust_circle = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(adjust_circle)

            preview_update = not main_page.compare(default_preview, adjust_circle, similarity=0.98)
            case.result = adjust_result and preview_update

        # [M42] "Color Balance" > Check Invert masked area
        with uuid("3d23be7e-a1b0-4ab6-b296-1f7218f626f0") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.color_balance.enable_invert_masked_area()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(applied_preview, adjust_circle, similarity=0.98)
            case.result = adjust_result and preview_update

        # [M41] "Color Balance" > Check Grayscale area
        with uuid("06e9ea59-7873-4b43-82a6-6f394ae999ee") as case:
            # Disable invert masked area
            effect_settings_page.color_balance.enable_invert_masked_area(value=False)

            # Adjust parameter
            adjust_result = effect_settings_page.color_balance.enable_grayscale_area()
            time.sleep(DELAY_TIME * 2)
            applied_grayscale_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_grayscale_preview)

            preview_update = not main_page.compare(default_preview, applied_grayscale_preview, similarity=0.98)
            case.result = adjust_result and preview_update

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_10(self):
        # [M58] Add "Drain" > Check Degree preview
        with uuid("975acf62-dbc6-4582-9476-711ff14dc6fe") as case:
            # Insert HEVC clip
            video_path = Test_Material_Folder + 'Timeline_Right_Click_Menu/TheIncredibles_HEVC.ts'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:16:04
            main_page.set_timeline_timecode('00_00_16_04')
            time.sleep(DELAY_TIME * 4)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search library content
            media_room_page.search_library('Drain')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Drain')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.drain.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M60] "Drain" > Check Size preview
        with uuid("38181ce9-3641-42b8-88f4-b54f000df301") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.drain.adjust_size_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            case.result = adjust_result and preview_update

        # [M61] "Drain" > Check Invert preview
        with uuid("55de3370-70ec-4726-a070-ecb0dd8dd104") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.drain.enable_inverse()
            time.sleep(DELAY_TIME * 2)
            invert_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(invert_preview, applied_preview)
            case.result = adjust_result and preview_update

        # [M75] Add "Fish Eye" > Check Degree preview
        with uuid("0667e942-1d66-43ff-aa14-b24130e44c22") as case:
            # Click remove button of (Drain) effect
            effect_settings_page.click_remove_btn()

            # Select Style Effect category
            effect_room_page.select_LibraryRoom_category('Style Effect')
            time.sleep(DELAY_TIME)

            # Search library content
            media_room_page.search_library('Fish Eye')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Fish Eye')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.fish_eye.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M78] "Fish Eye" > Check Invert preview
        with uuid("4fedcde6-ad34-4d31-ba9b-1148e10ac051") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.fish_eye.enable_inverse()
            time.sleep(DELAY_TIME * 2)
            invert_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(invert_preview, applied_preview)
            case.result = adjust_result and preview_update

        # [M77] "Fish Eye" > Check Size preview
        with uuid("e0cbd692-589f-4d70-b2d9-b783d6c52a66") as case:
            # Set invert to disable
            effect_settings_page.fish_eye.enable_inverse(value=False)
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.fish_eye.adjust_size_slider()
            time.sleep(DELAY_TIME * 2)
            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, applied_preview)
            case.result = adjust_result and preview_update

        # [M86] Add "Glass Tile" > Check Degree preview
        with uuid("31195eac-2ace-4d57-a47c-3d2826648bf9") as case:
            # Click remove button of (Fish Eye) effect
            effect_settings_page.click_remove_btn()

            # Select Style Effect category
            effect_room_page.select_LibraryRoom_category('Style Effect')
            time.sleep(DELAY_TIME)

            # Search library content
            media_room_page.search_library('Glass')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Glass Tile')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.glass_tile.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_11(self):
        # [M67] Add "Emboss" > Check Gradient Depth preview
        with uuid("b8ccbe8d-3d27-4f94-b139-b62aca07925e") as case:
            # Insert HEVC clip
            video_path = Test_Material_Folder + 'Timeline_Right_Click_Menu/TheIncredibles_HEVC.ts'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:19:10
            main_page.set_timeline_timecode('00_00_19_10')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search library content
            media_room_page.search_library('Emboss')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Emboss')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.emboss.adjust_gradient_depth_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M68] "Emboss" > Check Mask type preview
        with uuid("33c6beff-1c4f-4dcc-9399-10f6587260ed") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.emboss.set_mask_type()
            time.sleep(DELAY_TIME * 2)
            mask_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(mask_preview, applied_preview)
            case.result = adjust_result and preview_update

        # [M69] "Emboss" > Check Direction preview
        with uuid("a31c0bc8-3e08-455a-97ed-b6bf3c2e85c5") as case:
            # Click Undo (Set mask type to Box)
            main_page.click_undo()

            # Adjust parameter
            adjust_result = effect_settings_page.emboss.set_direction()
            time.sleep(DELAY_TIME * 2)
            direction_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(direction_preview, applied_preview)
            case.result = adjust_result and preview_update

        # [M71] "Emboss" > Check Invert preview
        with uuid("e81f4078-6a97-48d3-ba9e-198605c8d93a") as case:
            # Click Undo (Set Direction to Upper left)
            main_page.click_undo()

            # Adjust parameter
            adjust_result = effect_settings_page.emboss.enable_invert_masked_area()
            time.sleep(DELAY_TIME * 2)
            invert_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(invert_preview, applied_preview)
            case.result = adjust_result and preview_update

        # [M97] Add "Halftone (Color)" > Check Sport preview
        with uuid("e031bfd0-9b80-4df0-93c1-f1408025da61") as case:
            # Click remove button of (Emboss) effect
            effect_settings_page.click_remove_btn()

            # Select Style Effect category
            effect_room_page.select_LibraryRoom_category('Style Effect')
            time.sleep(DELAY_TIME)

            # Search library content
            media_room_page.search_library('Halftone')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Halftone (Color)')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.halftone_color.adjust_sport_size_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M98] "Halftone (Color)" > Check Intensity preview
        with uuid("af982af5-a4c7-434d-b043-194031b585d6") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            reset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Adjust parameter
            adjust_result = effect_settings_page.halftone_color.adjust_intensity_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(reset_preview, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M103] Add "Jitter" > Check Frequency preview
        with uuid("19251140-8fdc-467e-903f-23bc14de0e20") as case:
            # Click remove button of (Halftone Color) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Jitter')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Jitter')
            time.sleep(DELAY_TIME * 2)

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.jitter.adjust_frequency_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update


    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_12(self):
        # [M89] Add "Grid" > Check Width preview
        with uuid("0838a287-e269-4003-9e1a-53d23da14fd9") as case:
            # Snapshot Default : "Skateboard 01.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:07:02
            main_page.set_timeline_timecode('00_00_07_02')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search library content
            media_room_page.search_library('Grid')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Grid')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.grid.adjust_width_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M91] Add "Grid" > Check Height preview
        with uuid("94604e7a-e2f1-4cf2-a0d9-0b4937406c1b") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            reset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Adjust parameter
            adjust_result = effect_settings_page.grid.adjust_height_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(reset_preview, applied_preview)
            case.result = adjust_result and preview_update

        # [M90] Add "Grid" > Check Line Width preview
        with uuid("0f6138ce-bfad-4052-a4dd-d311cae7b22f") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.grid.adjust_line_width_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(reset_preview, applied_preview)
            case.result = adjust_result and preview_update

        # [M92] Add "Grid" > Check BG color preview
        with uuid("9eb8f0b7-b92e-4433-ae49-c4092666f39a") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.grid.adjust_BG_color('CB3500')
            time.sleep(DELAY_TIME * 2)
            update_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(update_color_preview, applied_preview)
            case.result = adjust_result and preview_update

        # [M93] Add "Halftone" > Check Sport size preview
        with uuid("e126e7d6-406f-4480-8e30-c5cfae5fecf7") as case:
            # Click remove button of (Halftone Color) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Halftone')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Halftone')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.halftone.adjust_sport_size_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.85)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M94] "Halftone" > Check Foreground Color preview
        with uuid("4be12841-25e1-40fa-a39c-d97ee126880d") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            reset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Adjust parameter
            adjust_result = effect_settings_page.halftone.adjust_FG_color('B21D50')
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(reset_preview, applied_preview, similarity=0.999)
            case.result = adjust_result and preview_update

        # [M96] "Halftone" > Check BG Color preview
        with uuid("685d98cd-38df-41f8-ac12-95527e0b679c") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.halftone.adjust_BG_color('5F12FD')
            time.sleep(DELAY_TIME * 2)
            bg_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(bg_color_preview, applied_preview)
            case.result = adjust_result and preview_update

        # [M95] "Halftone" > Check Intensity preview
        with uuid("285825e0-f64f-4b58-8c1e-dc5c66015b71") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.halftone.adjust_intensity_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(bg_color_preview, applied_preview, similarity=0.999)
            case.result = adjust_result and preview_update

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_13(self):
        # [M80] Add "Gaussian Blur" > Check Degree preview
        with uuid("d7e80d23-bb66-4806-bf49-d677adcce650") as case:
            # Select aspect ratio to 4:3
            main_page.set_project_aspect_ratio_4_3()

            # Insert AVI clip
            video_path = Test_Material_Folder + 'Crop_Zoom_Pan/DV-AVI_720x480_4_3_24.4Mbps_LPCM.AVI'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:01:26:02
            main_page.set_timeline_timecode('00_01_26_02')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search library content
            media_room_page.search_library('Gaussian')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Gaussian Blur')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.gaussian_blur.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M81] "Gaussian Blur" > Check Mask Type preview
        with uuid("b136b564-20ca-4ee9-8138-80bf8c729181") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.gaussian_blur.set_mask_type()
            time.sleep(DELAY_TIME * 2)
            circle_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(circle_preview, applied_preview, similarity=0.992)
            case.result = adjust_result and preview_update

        # [M82] "Gaussian Blur" > Check Gradient depth preview
        with uuid("721706a1-5fd9-411f-bc2f-5fb495ed4991") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.gaussian_blur.adjust_gradient_depth_slider()
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(circle_preview, applied_preview, similarity=0.999)
            case.result = adjust_result and preview_update

        # [M84] "Gaussian Blur" > Check Invert mask preview
        with uuid("ec6f0756-1419-406a-ac4f-e8baa713d259") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.gaussian_blur.enable_invert_masked_area()
            time.sleep(DELAY_TIME * 2)
            invert_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(invert_preview, applied_preview, similarity=0.98)
            case.result = adjust_result and preview_update

        # [M87] Add "Glow" > Check Blur preview
        with uuid("8fac6fd3-1d37-4281-aece-b0aaf29e10e0") as case:
            # Click remove button of (Gaussian Blur) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Glow')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Glow')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.glow.adjust_blur_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M88] "Glow" > Check Glow level preview
        with uuid("f9a12914-4486-4cef-acea-ce9223e72650") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.glow.adjust_glow_slider()
            time.sleep(DELAY_TIME * 2)
            glow_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(glow_preview, applied_preview)
            case.result = adjust_result and preview_update

        # [M139] Add "Pen Ink" > Check Blackness preview
        with uuid("e653d71d-5cea-4065-8c69-0ee340a53147") as case:
            # Click remove button of (Glow) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Pen Ink')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Pen Ink')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.pen_ink.adjust_blackness_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 10 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_14(self):
        # [M99] Add "Horizontal Stretch" > Check Degree preview
        with uuid("27b9241b-6f1b-4c38-8129-efc5649d6a2e") as case:
            # Insert HEVC clip
            video_path = Test_Material_Folder + 'Timeline_Right_Click_Menu/TheIncredibles_HEVC.ts'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:11:00
            main_page.set_timeline_timecode('00_00_11_00')
            time.sleep(DELAY_TIME * 4)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search library content
            media_room_page.search_library('Horizontal')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Horizontal Stretch')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.horizontal_stretch.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M100] "Horizontal Stretch" > Check X Offset preview
        with uuid("a968eb42-7a54-4312-86a1-b7b10123b38f") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.horizontal_stretch.adjust_x_offset_slider()
            time.sleep(DELAY_TIME * 2)
            offset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, applied_preview)
            case.result = adjust_result and preview_update

        # [M102] "Horizontal Stretch" > Check Inverse preview
        with uuid("387cb37c-8bc5-4c1f-913d-26abd97a0d81") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.horizontal_stretch.enable_inverse()
            time.sleep(DELAY_TIME * 2)
            inverse_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, inverse_preview)
            case.result = adjust_result and preview_update

        # [M101] "Horizontal Stretch" > Check Size preview
        with uuid("e60f19a2-b618-446b-8252-62f44ce54f65") as case:
            # Disable inverse
            adjust_result = effect_settings_page.horizontal_stretch.enable_inverse(value= False)
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.horizontal_stretch.adjust_size_slider()
            time.sleep(DELAY_TIME * 2)
            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, size_preview)
            case.result = adjust_result and preview_update

        # [M104] Add "Kaleidoscope" > Check Angle preview
        with uuid("779b5370-76dd-4d54-aeaf-1e8c3a9b0326") as case:
            # Click remove button of (Horizontal Stretch) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Kaleidoscope')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Kaleidoscope')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.kaleidoscope.adjust_angle_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M105] "Kaleidoscope" > Check X offset preview
        with uuid("6aabc074-a2a4-4f75-a1fb-eee1725ac56e") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.kaleidoscope.adjust_x_offset_slider()
            logger(adjust_result)

            offset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M106] "Kaleidoscope" > Check segment preview
        with uuid("ba19846b-825c-4448-a0fa-c0b32452458f") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.kaleidoscope.adjust_segment_slider()
            logger(adjust_result)

            segment_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, segment_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M107] "Kaleidoscope" > Check Y offset preview
        with uuid("a16f4801-6fa8-4de0-9e30-4d56d5737192") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.kaleidoscope.adjust_y_offset_slider()
            logger(adjust_result)

            y_offset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, y_offset_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M114] Add "Mirror" > Check X Offset preview
        with uuid("bca303c7-eba5-4a81-a16a-24f441711289") as case:
            # Click remove button of (Kaleidoscope) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Mirror')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Mirror')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.mirror.adjust_x_offset_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M115] Add "Mirror" > Check Inverse preview
        with uuid("d51a9dc5-83a0-4601-b8f5-9851b0b513c1") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.mirror.enable_inverse()
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            inverse_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(inverse_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 9 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_15(self):
        # [M121] Add "Mosaic" > Check Width preview
        with uuid("0aea94e7-262c-4ff5-a429-c5790f807dcd") as case:
            # Insert girl.mp4
            video_path = Test_Material_Folder + 'Produce_Local/girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:04:06
            main_page.set_timeline_timecode('00_00_04_06')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search effect
            media_room_page.search_library('Mosaic')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Mosaic')

            # Select timeline clip
            main_page.select_timeline_media('girl')
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.mosaic.adjust_width_slider()
            logger(adjust_result)
    
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)
    
            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M122] "Mosaic" > Check Mask type preview
        with uuid("016355ed-f4b7-4984-bb52-44bb40b09fc7") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.mosaic.set_mask_type()
            logger(adjust_result)

            applied_circle_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(applied_circle_preview, applied_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M123] "Mosaic" > Check Height preview
        with uuid("f3ceec8c-038a-47f5-a591-ecff92251c31") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.mosaic.adjust_height_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(applied_circle_preview, applied_preview, similarity=0.96)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M126] Add "Neutral Density Filter" > Check Alpha degree preview
        with uuid("811c93b9-6f48-437f-a179-cbf11e9b46e8") as case:
            # Click remove button of (Mosaic) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Neutral')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Neutral Density Filter')

            # Select timeline clip
            main_page.select_timeline_media('girl')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.neutral_filter.adjust_alpha_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M125] "Neutral Density Filter" > Check Start position preview
        with uuid("559eb87b-8174-406f-b75d-8b1e8d487a2d") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.neutral_filter.adjust_start_slider()
            logger(adjust_result)

            start_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(start_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M127] "Neutral Density Filter" > Check End position preview
        with uuid("755e286c-d6de-4933-a13a-309abed7dc00") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.neutral_filter.adjust_end_slider()
            logger(adjust_result)

            start_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(start_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M128] "Neutral Density Filter" > Check Replace color preview
        with uuid("9746906c-8c50-4e97-ac83-8d81cab9174f") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.neutral_filter.adjust_replace_color('9400D6')
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(start_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M112] Add "Line Noise" > Check Frequency preview
        with uuid("0cb7c657-2cea-489b-be48-a6a04919d0d6") as case:
            # Click remove button of (Neutral Density Filter) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Line')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Line Noise')

            # Select timeline clip
            main_page.select_timeline_media('girl')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.line_noise.adjust_frequency_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M113] "Line Noise" > Check Strength preview
        with uuid("4602cbb7-7024-4937-8853-a5b6d2fac31c") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.line_noise.adjust_strength_slider()
            logger(adjust_result)

            strength_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(strength_preview, applied_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_16(self):
        # [M116] Add "Moon Light" > Check Degree preview
        with uuid("9b8bfadf-d26e-4529-a991-d29d10d1077a") as case:
            # Insert skateboard_girl.mp4
            video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:03:12
            main_page.set_timeline_timecode('00_00_03_12')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search effect
            media_room_page.search_library('Moon')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Moon Light')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.moon_light.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.999)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.95)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M117] "Moon Light" > Check Mask type preview
        with uuid("3cefb42d-bc78-4e9e-b225-2e733ac86940") as case:
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.moon_light.set_mask_type()
            logger(adjust_result)

            mask_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(mask_preview, applied_preview, similarity=0.999)
            preview_most_same = main_page.compare(mask_preview, applied_preview, similarity=0.95)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M118] "Moon Light" > Check Gradient Depth preview
        with uuid("aad2d9aa-e03c-4e08-a0d4-c4ddf4ab595b") as case:
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.moon_light.adjust_gradient_depth_slider()
            logger(adjust_result)

            depth_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(mask_preview, depth_preview, similarity=0.999)
            preview_most_same = main_page.compare(mask_preview, depth_preview, similarity=0.95)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M120] "Moon Light" > Check Gradient Depth preview
        with uuid("7de821d0-ff1a-43f6-82e4-8e800a5bf7dd") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.moon_light.enable_invert_masked_area()
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)
            invert_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(invert_preview, depth_preview, similarity=0.999)
            preview_most_same = main_page.compare(invert_preview, depth_preview, similarity=0.95)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M108] Add "Laser" > Check Percentage preview
        with uuid("76778967-fa5d-4928-8f22-c430b743dbe3") as case:
            # Click remove button of (Moon Light) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Laser')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Laser')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.laser.adjust_percentage_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.999)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.95)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M110] Add "Light Ray" > Check Degree preview
        with uuid("b0b0e1d1-277a-4b44-91e2-457b2cd162ca") as case:
            # Click remove button of (Moon Light) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Light Ray')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Light Ray')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.light_ray.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.999)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.95)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M140] Add "Pop Art" > Check Degree preview
        with uuid("d5a3e660-d998-4cae-8019-cd92c4c93bcc") as case:
            # Click remove button of (Moon Light) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Pop Art')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Pop Art')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.pop_art.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.98)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_17(self):
        # [M131] Add "Old Movie" > Check Artifact Quantity preview
        with uuid("1ff2e3a7-affa-4244-abae-70d9ed350863") as case:
            # Insert Y man.mp4
            video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:04:19
            main_page.set_timeline_timecode('00_00_04_19')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search effect
            media_room_page.search_library('Old Movie')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Old Movie')

            # Select timeline clip
            main_page.select_timeline_media('Y man')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.old_movie.adjust_artifact_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.999)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.95)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M132] "Old Movie" > Check Scratch Quantity preview
        with uuid("1d4a7789-a83c-46fd-9fd0-8c6eb89eab7a") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.old_movie.adjust_scratch_slider()
            logger(adjust_result)

            scratch_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(scratch_preview, applied_preview, similarity=0.999)
            preview_most_same = main_page.compare(scratch_preview, applied_preview, similarity=0.95)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M133] "Old Movie" > Check Degree preview
        with uuid("80eb9ad9-9f4f-4ab4-b4b1-d344e6fa3d04") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.old_movie.adjust_degree_slider()
            logger(adjust_result)

            degree_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(scratch_preview, degree_preview)
            preview_most_same = main_page.compare(scratch_preview, degree_preview, similarity=0.8)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M134] "Old Movie" > Check Noise preview
        with uuid("7e03d466-c7a8-45c8-8abd-aea931263d59") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.old_movie.adjust_noise_slider()
            logger(adjust_result)

            noise_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(noise_preview, degree_preview, similarity=0.999)
            preview_most_same = main_page.compare(noise_preview, degree_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M135] "Old Movie" > Check Jitter preview
        with uuid("3e24c336-bf5d-4a18-8c58-83aa0066794e") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.old_movie.adjust_jitter_slider()
            logger(adjust_result)

            jitter_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_most_same = main_page.compare(noise_preview, jitter_preview, similarity=0.8)
            logger(preview_most_same)
            case.result = adjust_result and preview_most_same

        # [M137] "Old Movie" > Check Front preview
        with uuid("379904fa-ec27-428b-8446-08b73634bf11") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.old_movie.adjust_front_color('45C456')
            logger(adjust_result)

            front_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_most_same = main_page.compare(front_preview, jitter_preview, similarity=0.7)
            logger(preview_most_same)
            case.result = adjust_result and preview_most_same

        # [M136] "Old Movie" > Check Flicker preview
        with uuid("e2b3cc79-5d62-47f6-9a46-a522abebbe03") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.old_movie.adjust_flicker_slider()
            logger(adjust_result)

            flicker_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_most_same = main_page.compare(front_preview, flicker_preview, similarity=0.6)
            logger(preview_most_same)
            case.result = adjust_result and preview_most_same

        # [M138] "Old Movie" > Check Background color preview
        with uuid("f6201f37-3171-4d74-92f3-7636d5c80eda") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.old_movie.adjust_BG_color('B20920')
            logger(adjust_result)

            background_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_most_same = main_page.compare(background_preview, flicker_preview, similarity=0.8)
            logger(preview_update)
            case.result = adjust_result and preview_most_same

    # 11 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_18(self):
        # [M149] Add "Radial Blur" > Check Degree preview
        with uuid("a6f07c84-8bcf-42a3-b64d-08b7d123dbcd") as case:
            # Snapshot Default : "Skateboard 01.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:07:02
            main_page.set_timeline_timecode('00_00_07_02')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search library content
            media_room_page.search_library('Radial Blur')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Radial Blur')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.radial_blur.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M150] Add "Ripple" > Check Wavelets preview
        with uuid("c19b1b67-b84f-46f1-924f-d4f498bf590d") as case:
            # Click remove button of (Radial Blur) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Ripple')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Ripple')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.ripple.adjust_wavelets_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M151] "Ripple" > Check Progress preview
        with uuid("6c46aa76-4be8-41ca-ac04-a3deebcf8b06") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.ripple.adjust_progress_slider()
            logger(adjust_result)

            progress_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_most_same = main_page.compare(applied_preview, progress_preview, similarity=0.89)
            logger(preview_update)
            case.result = adjust_result and preview_most_same

        # [M152] "Ripple" > Check Speed preview
        with uuid("478996a8-7782-412b-9684-896e2bf5a07c") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            reset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Adjust parameter
            adjust_result = effect_settings_page.ripple.adjust_speed_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(reset_preview, applied_preview, similarity=0.97)
            case.result = adjust_result and preview_update

        # [M79] Add "Gamma Correction" > Check Gamma Level preview
        with uuid("7808ba2d-a6e9-4312-869d-6cd262216df8") as case:
            # Click remove button of (Ripple) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Gamma Correction')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Gamma Correction')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 01')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.gamma_correction.adjust_gamma_level_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M129] Add "Noise 2" > Check Frequency preview
        with uuid("987c7fbe-ff5d-4e2d-8b8f-32eb9f444c18") as case:
            # Click remove button of (Gamma Correction) effect
            effect_settings_page.click_remove_btn()

            # Set timecode 00:00:06:25
            main_page.set_timeline_timecode('00_00_06_25')
            time.sleep(DELAY_TIME * 2)

            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Noise 2')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Noise 2')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 01')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.noise_2.adjust_frequency_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M130] "Noise 2" > Check Strength preview
        with uuid("a12681a3-cb83-4f79-a737-32a725fc4c26") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.noise_2.adjust_strength_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.998)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M141] Add "Pop Art Wall" > Check Pattern preview
        with uuid("507a9cf5-453f-49de-9f09-98e484da2617") as case:
            # Click remove button of (Ripple) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Pop Art Wall')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Pop Art Wall')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 01')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.pop_art_wall.adjust_pattern_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.9)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.74)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M142] "Pop Art Wall" > Check Degree preview
        with uuid("afb5d396-a222-4f07-9546-bbd65f78ba42") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.pop_art_wall.adjust_degree_slider()
            logger(adjust_result)

            degree_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(degree_preview, applied_preview, similarity=0.98)
            preview_most_same = main_page.compare(degree_preview, applied_preview, similarity=0.74)
            case.result = adjust_result and preview_update and preview_most_same

        # [M158] Add "Sepia" > Check Degree preview
        with uuid("f09f97b4-dd69-45bb-bf6e-3e53f14ca86d") as case:
            # Click remove button of (Pop Art Wall) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Sepia')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Sepia')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.sepia.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.92)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M159] "Sepia" > Check Color preview
        with uuid("4d10f499-c4b1-4abd-8c34-7460bfb337e8") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.sepia.adjust_front_color('642DCB')
            logger(adjust_result)

            degree_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(degree_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(degree_preview, applied_preview, similarity=0.9)
            case.result = adjust_result and preview_update and preview_most_same

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_19(self):
        # [M193] Add "Vignette (Focus)" > Check Degree preview
        with uuid("93411e5a-95b1-40ab-b05b-24a94014394d") as case:
            # Snapshot Default : "Skateboard 02.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            time.sleep(DELAY_TIME)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:04:02
            main_page.set_timeline_timecode('00_00_04_02')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search library content
            media_room_page.search_library('Vignette')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Vignette (Focus)')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 02')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.vignette.adjust_width_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M194] "Vignette (Focus)" > Check Gradient depth preview
        with uuid("8c256e3a-cc68-4e73-b317-8845463151fe") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.vignette.adjust_gradient_depth_slider()
            logger(adjust_result)

            depth_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(depth_preview, applied_preview, similarity=0.95)
            preview_most_same = main_page.compare(depth_preview, applied_preview, similarity=0.8)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M195] "Vignette (Focus)" > Check Height preview
        with uuid("77aa09c4-d1ea-461c-ac27-c29b77c98a51") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.vignette.adjust_height_slider()
            logger(adjust_result)

            height_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(depth_preview, height_preview, similarity=0.9)
            preview_most_same = main_page.compare(depth_preview, height_preview, similarity=0.7)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M196] "Vignette (Focus)" > Check Alpha preview
        with uuid("07a4ab2e-4f86-42e0-af44-e7b55392a693") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.vignette.adjust_alpha_degree_slider()
            logger(adjust_result)

            height_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(depth_preview, height_preview, similarity=0.9)
            preview_most_same = main_page.compare(depth_preview, height_preview, similarity=0.75)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M198] "Vignette (Focus)" > Check BG color preview
        with uuid("c208cb0c-68c4-48aa-9cd0-7d1228fdc0fd") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.vignette.adjust_BG_color('E49Dc6')
            logger(adjust_result)

            color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(color_preview, height_preview, similarity=0.8)
            preview_most_same = main_page.compare(color_preview, height_preview, similarity=0.68)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M154] Add "Rocking" > Check Frequency preview
        with uuid("0585f16d-72dc-4a73-8fef-845ff6f88e51") as case:
            # Click remove button of (Noise 2) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Rocking')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Rocking')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.rocking.adjust_frequency_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M155] Add "Rocking" > Check Strength preview
        with uuid("4d8d0269-d04f-41de-80cc-5d20fa90c337") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.rocking.adjust_strength_slider()
            logger(adjust_result)

            strength_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(strength_preview, applied_preview)
            preview_most_same = main_page.compare(strength_preview, applied_preview, similarity=0.8)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M143] Add "Posterize" > Check Level preview
        with uuid("bc2d072d-799c-4170-b8e7-654e977fb586") as case:
            # Click remove button of (Rocking) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Posterize')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Posterize')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.posterize.adjust_levels_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.85)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_20(self):
        # [M144] Add "Quake" > Check Quake level preview
        with uuid("09646696-5418-4dbb-9713-11ef553121bb") as case:
            # Snapshot Default : "Skateboard 01.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:05:11
            main_page.set_timeline_timecode('00_00_05_11')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search library content
            media_room_page.search_library('Quake')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Quake')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.quake.adjust_quake_level_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.85)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M145] "Quake" > Check Angle preview
        with uuid("c341c376-1393-48f0-98fd-d22720fa7ea8") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.quake.adjust_starting_angle_slider()
            logger(adjust_result)

            angle_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(angle_preview, applied_preview)
            preview_most_same = main_page.compare(angle_preview, applied_preview, similarity=0.8)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M146] "Quake" > Check Frequency preview
        with uuid("1c3db009-560d-4c45-902f-b0d6627d4950") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.quake.adjust_frequency_slider()
            logger(adjust_result)

            case.result = adjust_result

        # [M147] "Quake" > Check Stepping Angle preview
        with uuid("d40e36e3-dd3d-43e0-85be-9f18e921a4f9") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.quake.adjust_stepping_angle_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(angle_preview, applied_preview)
            preview_most_same = main_page.compare(angle_preview, applied_preview, similarity=0.8)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M148] "Quake" > Check Stepping Angle preview
        with uuid("393185d5-0633-4740-a9c5-8a05511c9f3a") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.quake.adjust_BG_color('C827D6')
            logger(adjust_result)

            color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(color_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(color_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M160] Add "Skip" > Check Frequency preview
        with uuid("53b3198a-2441-4afb-b039-64b01a58db69") as case:
            # Click remove button of (Quake) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Skip')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Skip')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.skip.adjust_frequency_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Click next frame
            for x in range(4):
                playback_window_page.Edit_Timeline_PreviewOperation('next_frame')
                time.sleep(DELAY_TIME)
            later_frame_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            preview_no_update = main_page.compare(later_frame_preview, applied_preview, similarity=0.99)
            case.result = adjust_result and preview_no_update

        # [M156] Add "Scratch Noise" > Check Frequency preview
        with uuid("2acb648e-f639-4caf-b0b2-90ee24ad0cdf") as case:
            # Click remove button of (Skip) effect
            effect_settings_page.click_remove_btn()

            # Set timecode 00:00:05:21
            main_page.set_timeline_timecode('00_00_05_21')
            time.sleep(DELAY_TIME * 2)

            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Scratch Noise')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Scratch Noise')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.scratch_noise.adjust_frequency_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.998)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.85)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M157] "Scratch Noise" > Check Strength preview
        with uuid("a96aa4e5-edac-4c97-b317-f4d91b5834ce") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.scratch_noise.adjust_strength_slider()
            logger(adjust_result)

            strength_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(strength_preview, applied_preview, similarity=0.98)
            preview_most_same = main_page.compare(strength_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_21(self):
        # [M162] Add "Spotlight" > Check Width preview
        with uuid("721cdc55-da0d-4d94-9509-0a401c0bc87d") as case:
            # Insert skateboard_girl.mp4
            video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:03:12
            main_page.set_timeline_timecode('00_00_03_12')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search effect
            media_room_page.search_library('Spotlight')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Spotlight')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.spotlight.adjust_width_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M163] "Spotlight" > Check Gradient depth preview
        with uuid("4bbccf5c-603f-4f85-8fef-55364032a1bd") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.spotlight.adjust_gradient_depth_slider()
            logger(adjust_result)

            depth_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(depth_preview, applied_preview, similarity=0.998)
            preview_most_same = main_page.compare(depth_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M164] "Spotlight" > Check Height preview
        with uuid("e5301342-185c-471e-8f4f-39cdbd3ffe2e") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.spotlight.adjust_height_slider()
            logger(adjust_result)

            height_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(depth_preview, height_preview, similarity=0.999)
            preview_most_same = main_page.compare(depth_preview, height_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M165] "Spotlight" > Check Brightness preview
        with uuid("01874480-8d93-4f75-a5c5-ec62d8ca1a5a") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.spotlight.adjust_brightness_slider()
            logger(adjust_result)

            brightness_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(brightness_preview, height_preview, similarity=0.996)
            preview_most_same = main_page.compare(brightness_preview, height_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M166] "Spotlight" > Check Mean preview
        with uuid("a939b72e-d6e8-47a4-a8c3-200826449de0") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.spotlight.adjust_mean_slider()
            logger(adjust_result)

            mean_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(brightness_preview, mean_preview, similarity=0.99)
            preview_most_same = main_page.compare(brightness_preview, mean_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M168] "Spotlight" > Check Color preview
        with uuid("ea2a072a-b051-4d38-a846-d7f5bcf38f4c") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.spotlight.adjust_BG_color('F3FF4C')
            logger(adjust_result)

            color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(color_preview, mean_preview, similarity=1)
            preview_most_same = main_page.compare(color_preview, mean_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_22(self):
        # [M171] Add "Squeeze" > Check Degree preview
        with uuid("0b6e6c76-cff4-4e88-9beb-219dc1826255") as case:
            # Insert girl.mp4
            video_path = Test_Material_Folder + 'Produce_Local/girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:07:02
            main_page.set_timeline_timecode('00_00_07_02')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search library content
            media_room_page.search_library('Squeeze')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Squeeze')
            time.sleep(DELAY_TIME)

            # Select timeline clip
            main_page.select_timeline_media('girl')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.squeeze.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.8)
            case.result = adjust_result and preview_update and preview_most_same

        # [M173] "Squeeze" > Check Size preview
        with uuid("9d3c8527-65ea-4675-8c1e-afdb9eba8f09") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.squeeze.adjust_size_slider()
            logger(adjust_result)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, applied_preview, similarity=0.9)
            preview_most_same = main_page.compare(size_preview, applied_preview, similarity=0.8)
            case.result = adjust_result and preview_update and preview_most_same

        # [M174] "Squeeze" > Check Inverse preview
        with uuid("ea1e0fba-042b-4bd0-8d1c-239ff6cc0b5e") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.squeeze.enable_inverse()
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)
            inverse_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, inverse_preview, similarity=0.99)
            preview_most_same = main_page.compare(size_preview, inverse_preview)
            case.result = adjust_result and preview_update and preview_most_same

        # [M187] Add "TV Wall" > Check Horizontal number preview
        with uuid("380e4651-2bc7-4c95-b8cf-6540b8765ddf") as case:
            # Click remove button of (Squeeze) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('TV Wall')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('TV Wall')
            time.sleep(DELAY_TIME)

            # Select timeline clip
            main_page.select_timeline_media('girl')
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.tv_wall.adjust_horizontal_slider()
            time.sleep(DELAY_TIME * 2)
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.9)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.4)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M188] "TV Wall" > Check Vertical number preview
        with uuid("60ca138d-7482-4727-9c02-c01abefee202") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.tv_wall.adjust_vertical_slider()
            time.sleep(DELAY_TIME * 2)
            logger(adjust_result)

            vertical_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(vertical_preview, applied_preview, similarity=0.9)
            preview_most_same = main_page.compare(vertical_preview, applied_preview, similarity=0.4)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M180] Add "Tiles" > Check Tile count preview
        with uuid("36fbfa6c-40aa-43e8-8d16-5381188d8941") as case:
            # Click remove button of (TV Wall) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Tiles')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Tiles')
            time.sleep(DELAY_TIME)

            # Select timeline clip
            main_page.select_timeline_media('girl')
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.tiles.adjust_count_slider()
            time.sleep(DELAY_TIME * 2)
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M181] "Tiles" > Check BG color preview
        with uuid("60436865-1d76-48ea-aa4e-5955536438bd") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.tiles.adjust_BG_color('E43D76')
            time.sleep(DELAY_TIME * 2)
            logger(adjust_result)

            color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(color_preview, applied_preview, similarity=1)
            preview_most_same = main_page.compare(color_preview, applied_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M161] Add "Solarize" > Check threshold preview
        with uuid("5924f284-35a6-4962-ae28-7a9087740ec3") as case:
            # Click remove button of (Tiles) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Solarize')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Solarize')
            time.sleep(DELAY_TIME)

            # Select timeline clip
            main_page.select_timeline_media('girl')
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.solarize.adjust_threshold_slider()
            time.sleep(DELAY_TIME * 2)
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.5)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.2)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_23(self):
        # [M199] Add "Water Reflection" > Check Vertical Mirror Center preview
        with uuid("cdf2a652-ec26-4836-8666-f29bee172ad1") as case:
            # Insert girl.mp4
            video_path = Test_Material_Folder + 'Produce_Local/girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:04:04
            main_page.set_timeline_timecode('00_00_04_04')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search library content
            media_room_page.search_library('Water Reflection')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Water Reflection')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.water_reflection.adjust_vertical_mirror_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            logger(preview_update)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.75)
            case.result = adjust_result and preview_update and preview_most_same

        # [M200] "Water Reflection" > Check Wave Interval preview
        with uuid("75432838-668d-48cc-9e32-7fc34455cdf9") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.water_reflection.adjust_wave_interval_slider()
            logger(adjust_result)

            wave_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(applied_preview, wave_preview, similarity=0.99)
            preview_most_same = main_page.compare(applied_preview, wave_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M201] "Water Reflection" > Check Wavelet preview
        with uuid("27701aa4-c1f6-49be-a9ca-09f9c6454aca") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.water_reflection.adjust_wavelet_slider()
            logger(adjust_result)

            wavelet_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(wavelet_preview, wave_preview, similarity=0.99)
            preview_most_same = main_page.compare(wavelet_preview, wave_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M202] "Water Reflection" > Check Brightness preview
        with uuid("36084d97-28c5-4922-a535-d295806d6ef8") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.water_reflection.adjust_brightness_slider()
            logger(adjust_result)

            appiled_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(wavelet_preview, appiled_preview, similarity=0.99)
            preview_most_same = main_page.compare(wavelet_preview, appiled_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M203] "Water Reflection" > Check Speed preview
        with uuid("bd6dd0d7-3071-46d0-bb7d-6fb9822db8f3") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.water_reflection.adjust_speed_slider()
            logger(adjust_result)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(speed_preview, appiled_preview, similarity=0.999)
            preview_most_same = main_page.compare(speed_preview, appiled_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M204] "Water Reflection" > Check Inverse preview
        with uuid("ada201b0-586f-40f1-8544-0425318b03f0") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.water_reflection.enable_inverse()
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            inverse_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(speed_preview, inverse_preview, similarity=0.8)
            preview_most_same = main_page.compare(speed_preview, inverse_preview, similarity=0.55)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M178] Add "Threshold" > Check Degree preview
        with uuid("80f1c137-799c-4964-a980-b4cf8970726e") as case:
            # Click remove button of (Sepia) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Threshold')
            time.sleep(DELAY_TIME * 3)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Threshold')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.threshold.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.9)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.8)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M179] "Threshold"  > Check BG color preview
        with uuid("78d37641-5830-4043-ac6e-1615033633bd") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.threshold.adjust_BG_color('D6D400')
            logger(adjust_result)

            inverse_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(speed_preview, inverse_preview)
            preview_most_same = main_page.compare(speed_preview, inverse_preview, similarity=0.7)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_24(self):
        # [M175] Add "Swing" > Check Angle preview
        with uuid("2c059c55-c07e-429b-8de9-ba4b2351a9fa") as case:
            # Insert girl.mp4
            video_path = Test_Material_Folder + 'Produce_Local/girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:03:14
            main_page.set_timeline_timecode('00_00_03_14')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search library content
            media_room_page.search_library('Swing')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Swing')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.swing.adjust_angle_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.7)
            logger(preview_update)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.3)
            case.result = adjust_result and preview_update and preview_most_same

        # [M176] "Swing"  > Check BG color preview
        with uuid("c141bd25-4585-462f-b7fb-b22425550d18") as case:
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME)

            # Adjust parameter
            adjust_result = effect_settings_page.swing.adjust_BG_color('00D2A0')
            logger(adjust_result)

            bg_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(applied_preview, bg_preview, similarity=0.7)
            preview_most_same = main_page.compare(applied_preview, bg_preview, similarity=0.4)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M177] "Swing"  > Check Type preview
        with uuid("1186753f-79ce-48b6-9b7b-9455e24a0f11") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.swing.set_type()
            logger(adjust_result)

            type_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(type_preview, bg_preview, similarity=0.85)
            preview_most_same = main_page.compare(type_preview, bg_preview, similarity=0.7)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M182] Add "Triangle Stretch"  > Check Degree preview
        with uuid("277acceb-40e9-4abd-83e9-1ec854d4027a") as case:
            # Click remove button of (Swing) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Triangle Stretch')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Triangle Stretch')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.triangle_stretch.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M184] "Triangle Stretch"  > Check Size preview
        with uuid("344722b2-25c6-4fb9-9e1c-f4b4d34f25c8") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.triangle_stretch.adjust_size_slider()
            logger(adjust_result)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(size_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M185] "Triangle Stretch"  > Check Inverse preview
        with uuid("b646a1a1-85c9-4fc4-b7d3-1528150acf9f") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.triangle_stretch.enable_inverse()
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)
            inverse_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, inverse_preview, similarity=0.95)
            preview_most_same = main_page.compare(size_preview, inverse_preview, similarity=0.85)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M209] Add "Woodcut"  > Check Brush size preview
        with uuid("ae700687-327b-40f1-8a0b-7f2b95275988") as case:
            # Click remove button of (Triangle Stretch) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Woodcut')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Woodcut')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.woodcut.adjust_brush_size_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.9)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.7)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_25(self):
        # [M189] Add "Vertical Stretch" > Check Degree preview
        with uuid("48888109-a2bd-48ca-aad4-a001a42ee9e9") as case:
            # Insert HEVC clip
            video_path = Test_Material_Folder + 'Timeline_Right_Click_Menu/TheIncredibles_HEVC.ts'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:11:00
            main_page.set_timeline_timecode('00_00_11_00')
            time.sleep(DELAY_TIME * 4)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search library content
            media_room_page.search_library('Vertical')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Vertical Stretch')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.vertical_stretch.adjust_degree_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.8)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M190] "Vertical Stretch"  > Check Y offset preview
        with uuid("c854f28c-a12f-47e3-9c51-9e9f9143ef09") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.vertical_stretch.adjust_y_offset_slider()
            logger(adjust_result)

            y_offset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(applied_preview, y_offset_preview, similarity=0.9)
            preview_most_same = main_page.compare(applied_preview, y_offset_preview, similarity=0.78)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M191] "Vertical Stretch"  > Check Size preview
        with uuid("4af5184d-e874-4111-b329-86af3225679e") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.vertical_stretch.adjust_size_slider()
            logger(adjust_result)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, y_offset_preview, similarity=0.85)
            preview_most_same = main_page.compare(size_preview, y_offset_preview, similarity=0.7)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M192] "Vertical Stretch"  > Check Inverse preview
        with uuid("d1425c42-e907-4e67-8746-87af62765bd9") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.vertical_stretch.enable_inverse()
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            inverse_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, inverse_preview, similarity=0.6)
            preview_most_same = main_page.compare(size_preview, inverse_preview, similarity=0.4)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M210] Add "Zoom In"  > Check Width preview
        with uuid("29eade00-56e8-46b2-92ea-98b515a852c5") as case:
            # Click remove button of (Vertical Stretch) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Zoom In')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Zoom In')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.zoom_in.adjust_width_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.8)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.5)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M211] "Zoom In"  > Check Height preview
        with uuid("53b1c217-8997-44cf-9ad3-45b4c9047da0") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.zoom_in.adjust_height_slider()
            logger(adjust_result)

            height_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(height_preview, applied_preview, similarity=0.8)
            preview_most_same = main_page.compare(height_preview, applied_preview, similarity=0.5)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_26(self):
        # [M205] Add "Wave" > Check Period preview
        with uuid("f7150eac-e03c-4dfd-8ab1-47602eea1a45") as case:
            # Insert Y man.mp4
            video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:03:19
            main_page.set_timeline_timecode('00_00_03_19')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search library content
            media_room_page.search_library('Wave')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Wave')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.wave.adjust_period_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M206] "Wave" > Check Amplitude preview
        with uuid("6f3be252-92aa-4ffa-b0f6-1b3b30352aa4") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.wave.adjust_amplitude_slider()
            logger(adjust_result)

            amplitude_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(amplitude_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(amplitude_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M207] Add "Wave Noise"  > Check Frequency preview
        with uuid("f19ed0fc-888b-4df0-9926-7c77d41c0d75") as case:
            # Click remove button of (Wave) effect
            effect_settings_page.click_remove_btn()

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Wave Noise')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.wave_noise.adjust_frequency_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=1)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M208] "Wave Noise" > Check Strength preview
        with uuid("fa468ca8-21bf-48de-899d-4650d90b22aa") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.wave_noise.adjust_strength_slider()
            logger(adjust_result)

            strength_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(strength_preview, applied_preview, similarity=0.9998)
            preview_most_same = main_page.compare(strength_preview, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M212] Add "Zoom Out"  > Check Width preview
        with uuid("c0cd2a26-f67b-4eab-9085-2bdf2447945f") as case:
            # Click remove button of (Wave Noise) effect
            effect_settings_page.click_remove_btn()

            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Zoom Out')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Zoom Out')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.zoom_out.adjust_width_slider()
            logger(adjust_result)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(default_preview, applied_preview, similarity=0.6)
            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.37)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M214] "Zoom Out" > Check BG preview
        with uuid("b7e1b3ae-494f-4e6e-8a53-b31278030aba") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.zoom_out.adjust_BG_color('BFE100')
            logger(adjust_result)

            color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(color_preview, applied_preview, similarity=0.5)
            preview_most_same = main_page.compare(color_preview, applied_preview, similarity=0.28)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M213] "Zoom Out" > Check Height preview
        with uuid("b6a43c12-837f-4024-ad47-f3c44ba1ac17") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.zoom_out.adjust_height_slider()
            logger(adjust_result)

            height_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(color_preview, height_preview, similarity=0.9)
            preview_most_same = main_page.compare(color_preview, height_preview, similarity=0.8)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

    # For Body Effect
    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_1(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M217] Add "Aura 1" > Download Effect
        with uuid("23fa5851-7b39-4210-b2ca-c6c1fd59530d") as case:
            # Snapshot Default : "Skateboard 02.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:03:22
            main_page.set_timeline_timecode('00_00_03_22')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Aura 1')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Aura 1')

            result = self.check_download_body_effect()
            logger(result)

            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                main_page.drag_media_to_timeline_playhead_position('Aura 1')
                time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:03:22
            main_page.set_timeline_timecode('00_00_03_22')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.99)
            case.result = not preview_update

        # [M219] "Aura 1" > Check Offset preview
        with uuid("50b89505-4315-412c-87e1-e0fa9020f48f") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0,200, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(current_preview, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M223] "Aura 1" > Check Preset preview
        with uuid("06d5889c-4534-471e-9d6d-81aafe36f128") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.set_dropdown_menu(custom_type='Preset 1', custom_locator=L.effect_settings.cbx_preset)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            preset_1_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(preset_1_preview)

            preview_update = not main_page.compare(preset_1_preview, applied_preview, similarity=0.992)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M221] "Aura 1" > Check Glow color preview
        with uuid("eb9435c4-1e9b-45d9-b8af-f28f4afc614d") as case:
            # Click [Reset]
            for x in range(2):
                effect_settings_page.click_reset_btn()
                time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('FFFF04', option=L.effect_settings.btn_glow_color)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(current_preview, applied_preview, similarity=0.9999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M218] "Aura 1" > Check Glow size preview
        with uuid("24c566ce-5a4d-444d-8540-324c0d51d67d") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 199)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(size_preview, applied_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M220] "Aura 1" > Check Polygon size preview
        with uuid("bbb87c4e-d625-43ae-a944-8de81179b84a") as case:
            # Adjust Offset parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(10, 200, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            # Adjust size parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(1, 200, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            max_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            # Adjust size parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 1, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            min_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(max_preview, min_preview, similarity=1)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M222] "Aura 1" > Check Polygon color preview
        with uuid("7998c952-28f2-45d5-b254-fb8e64c80085") as case:
            # Adjust size parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('44FFFF', option=L.effect_settings.btn_polygon_color)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(min_preview, applied_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 4 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_2(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M223] Add "Aura 2" > Download Effect
        with uuid("19cc23fc-6aa7-4bca-b138-d1bf1f88e911") as case:
            # Insert skateboard_girl.mp4
            video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:03:23
            main_page.set_timeline_timecode('00_00_03_23')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Aura 2')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Aura 2')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')
            # Set timecode 00:00:03:23
            main_page.set_timeline_timecode('00_00_03_23')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.99)
            case.result = not preview_update

        # [M224] "Aura 2" > Check Glow Size preview
        with uuid("dc8df1d1-8f3a-4b49-8c07-fb3b0a28413e") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0,185)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(current_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M225] "Aura 2" > Check Glow Color preview
        with uuid("a1a7fe6c-0ed8-491b-9314-7b2858948e1f") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('FF290B', option=L.effect_settings.btn_glow_color)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            glow_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(glow_color_preview, applied_preview, similarity=0.988)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M227] "Aura 2" > Check Preset preview
        with uuid("64f08df3-2f33-4aad-91a2-020547b14c00") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.set_dropdown_menu(custom_type='Preset 1', custom_locator=L.effect_settings.cbx_preset)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            preset_1_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(preset_1_preview)

            preview_update = not main_page.compare(preset_1_preview, glow_color_preview, similarity=0.992)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 3 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_3(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M227] Add "Comics 01" > Download Effect
        with uuid("b45d977f-0b7d-42f0-9449-ebdfc51830db") as case:
            # Insert skateboard_girl.mp4
            video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:03:29
            main_page.set_timeline_timecode('00_00_03_29')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Comics 01')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Comics 01')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')
            # Set timecode 00:00:03:29
            main_page.set_timeline_timecode('00_00_03_29')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.9)
            case.result = not preview_update

        # [M228] "Comics 01" > Check Speed preview
        with uuid("c91feea9-c2b9-474d-97c7-7db3d5d35099") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200,0)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(current_preview, applied_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M229] "Comics 01" > Check Size preview
        with uuid("a9cbb0e4-6aea-479e-829a-855bef025b5c") as case:
            # Adjust parameter
            effect_settings_page.body_effect.adjust_1st_slider(13, 145, 2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(size_preview, applied_preview, similarity=0.88)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 3 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_4(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M230] Add "Comics 02" > Download Effect
        with uuid("10d3af62-c4ef-4b86-9e71-7e881085f007") as case:
            # Snapshot Default : "Skateboard 01.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:04:05
            main_page.set_timeline_timecode('00_00_04_05')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Comics 02')
            time.sleep(DELAY_TIME * 4)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Comics 02')
            time.sleep(DELAY_TIME * 2)
            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 01')
            # Set timecode 00:00:04:05
            main_page.set_timeline_timecode('00_00_04_05')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.99)
            case.result = not preview_update

        # [M231] "Comics 02" > Check Speed preview
        with uuid("7ef39417-eea0-4b33-acf8-f3d7e8cf9aa7") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200,0)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(current_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M232] "Comics 02" > Check Size preview
        with uuid("8e603a23-fa03-4404-a6a0-f048095ca89d") as case:
            # Adjust parameter
            effect_settings_page.body_effect.adjust_1st_slider(13, 198, 2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(size_preview, applied_preview, similarity=0.88)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_5(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M234] Add "Contour 1" > Download Effect
        with uuid("71c27d24-ffc9-487e-b404-2ed246e199ad") as case:
            # Insert skateboard_girl.mp4
            video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:06:13
            main_page.set_timeline_timecode('00_00_06_13')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Contour')
            time.sleep(DELAY_TIME * 4)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Contour 1')
            time.sleep(DELAY_TIME * 4)
            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')

            # Set timecode 00:00:06:13
            main_page.set_timeline_timecode('00_00_06_13')
            time.sleep(DELAY_TIME * 4)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.99)
            case.result = not preview_update

        # [M239] "Contour 1" > Check Preset preview
        with uuid("bd8c42c1-4224-4350-b350-0b223483ab6a") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.set_dropdown_menu(custom_type='Preset 1', custom_locator=L.effect_settings.cbx_preset)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            preset_1_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(preset_1_preview, current_preview, similarity=0.992)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M235] "Contour 1" > Check Size preview
        with uuid("ddb559f4-3de4-4338-81a2-a7267ed1c646") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 0)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(preset_1_preview, applied_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M237] "Contour 1" > Check Offset preview
        with uuid("e868a5dd-c0f0-4b1d-9c7b-024cd3597b36") as case:
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 0, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, applied_preview, similarity=0.998)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M238] "Contour 1" > Check opacity preview
        with uuid("b26bf24e-1ff9-4ae2-ac1a-02b66548ba99") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 100, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            opacity_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, opacity_preview, similarity=0.9999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M236] "Contour 1" > Check Color preview
        with uuid("1d7bd8c8-0e7b-4597-8cc7-48c8495e1275") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.grid.adjust_BG_color('F1F810')
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(applied_preview, opacity_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_6(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M240] Add "Contour 2" > Download Effect
        with uuid("b69a547e-7413-4b67-886d-f1cbaac5f8f2") as case:
            # Snapshot Default : "Skateboard 02.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:03:10
            main_page.set_timeline_timecode('00_00_03_10')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Contour')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Contour 2')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 02')
            # Set timecode 00:00:03:10
            main_page.set_timeline_timecode('00_00_03_10')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.999)
            case.result = not preview_update

        # [M245] "Contour 2" > Check Preset preview
        with uuid("202228e7-58f8-4c6b-8f6c-ae9e1c7353c1") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.set_dropdown_menu(custom_type='Preset 2', custom_locator=L.effect_settings.cbx_preset)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            preset_2_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(preset_2_preview, current_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M242] "Contour 2" > Adjust color preview
        with uuid("e8bf121a-3f10-4273-ac38-4c37c9f9dd18") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('981E05')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(preset_2_preview, color_preview, similarity=0.9999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M243] "Contour 2" > Adjust Offset preview
        with uuid("2f24c7e5-dc09-4c09-ba84-032c4fa70b86") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            offset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, color_preview, similarity=0.995)
            logger(preview_update)
            case.result = adjust_result and preview_update


        # [M241] "Contour 2" > Adjust Size preview
        with uuid("f60b6700-40d5-4e47-95f0-c4a61f4cd024") as case:
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 0)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            min_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            max_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(max_preview, min_preview, similarity=0.995)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M244] "Contour 2" > Adjust opacity preview
        with uuid("850ff201-118b-4f6d-a808-52869e81daf2") as case:
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(100, 0, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            min_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = main_page.compare(default_preview, min_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_7(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M246] Add "Electric Shock 1" > Download Effect
        with uuid("603eba87-4a29-423f-a236-6ae964be69dd") as case:
            # Snapshot Default : "Skateboard 03.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:07:12
            main_page.set_timeline_timecode('00_00_07_12')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Electric Shock')
            time.sleep(DELAY_TIME * 4)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Electric Shock 1')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')
            time.sleep(DELAY_TIME * 4)

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 03')
            # Set timecode 00:00:07:12
            main_page.set_timeline_timecode('00_00_07_12')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.999)
            case.result = not preview_update

        # [M253] "Electric Shock 1" > Check Preset preview
        with uuid("d347951b-ce66-45e7-bda2-be94539b6018") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.set_dropdown_menu(custom_type='Preset 1', custom_locator=L.effect_settings.cbx_preset)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            preset_1_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(preset_1_preview, current_preview, similarity=0.9999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M247] "Electric Shock 1" > Check Size preview
        with uuid("c606fd41-e3da-43a1-8a98-68dd0560fafa") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(preset_1_preview, size_preview, similarity=0.985)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M249] "Electric Shock 1" > Check Length preview
        with uuid("dbad28a7-510d-4ee2-88cd-b538990a423c") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            offset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, size_preview, similarity=0.985)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M252] "Electric Shock 1" > Check Opacity preview
        with uuid("058c445f-555c-440e-88ce-90ea3d870d5d") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 0, option=5)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            opacity_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = main_page.compare(default_preview, opacity_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M251] "Electric Shock 1" > Adjust color preview
        with uuid("8e5e5d76-7c59-4846-9cfd-717539cfc52d") as case:
            # Click undo
            main_page.click_undo()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('D21004')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, applied_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M248] "Electric Shock 1" > Adjust Offset preview
        with uuid("2022055d-9a9e-42a5-ad40-f0da4917bf6f") as case:
            # Click undo
            main_page.click_undo()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            offset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M250] "Electric Shock 1" > Adjust Period preview
        with uuid("849d7243-4ace-4d29-b544-5f44af0537be") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 180, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            period_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, period_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_8(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M254] Add "Electric Shock 2" > Download Effect
        with uuid("f41e4fe7-23c9-4b6c-9a7c-442a817ca8ab") as case:
            # Snapshot Default : "Skateboard 03.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:03:00
            main_page.set_timeline_timecode('00_00_03_00')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Electric Shock')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Electric Shock 2')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 03')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Electric Shock 2')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 03')

            # Set timecode 00:00:03:00
            main_page.set_timeline_timecode('00_00_03_00')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.999)
            case.result = not preview_update

        # [M261] "Electric Shock 2" > Check Preset preview
        with uuid("18c353ae-0dd2-4251-91d8-a9381ca55d8e") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.set_dropdown_menu(custom_type='Preset 2', custom_locator=L.effect_settings.cbx_preset)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            preset_2_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(preset_2_preview, current_preview, similarity=0.9999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M258] "Electric Shock 2" > Adjust Period preview
        with uuid("94591615-ac84-4df6-8689-c41f9a06536f") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 42, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            period_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(preset_2_preview, period_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M255] "Electric Shock 2" > Adjust Size preview
        with uuid("a73f20de-8aaa-4a01-a83d-714714493ca0") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, period_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M256] "Electric Shock 2" > Adjust Offset preview
        with uuid("d590d768-57ca-4ecd-820a-75bd104eff07") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 185, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M257] "Electric Shock 2" > Adjust Length preview
        with uuid("a9f65f34-75c6-44fa-a007-5156c4ea116e") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 31, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            length_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(length_preview, applied_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M259] "Electric Shock 2" > Adjust Color preview
        with uuid("4a56ae9b-840d-4bcc-a037-ec6289aeaad4") as case:
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            before_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('F100FF')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(before_preview, applied_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M260] "Electric Shock 2" > Adjust Opacity preview
        with uuid("3cdfb042-5ce3-4fbb-83bd-c884b948e6a8") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(100, 7, option=5)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            opacity_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(opacity_preview, applied_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 3 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_9(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M262] Add "Energy Pulse" > Download Effect
        with uuid("92ffa5a0-f6df-4ffa-9bb1-812848da2b15") as case:
            # Snapshot Default : "Skateboard 03.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:02:25
            main_page.set_timeline_timecode('00_00_02_25')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Energy Pulse')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            #main_page.drag_media_to_timeline_playhead_position('Energy Pulse')
            self.apply_effect_to_timeline_clip('Energy Pulse')
            time.sleep(DELAY_TIME * 2)
            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 03')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Energy Pulse')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 03')

            # Set timecode 00:00:02:25
            main_page.set_timeline_timecode('00_00_02_25')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview)
            case.result = not preview_update

        # [M263] "Electric Shock 2" > Check Speed preview
        with uuid("6279d9c9-3b64-4949-927c-47cf1c2333f2") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 0)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, speed_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M264] "Electric Shock 2" > Check Hue shift preview
        with uuid("08926a74-6aa1-4735-b56d-66cb1c122390") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 164, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            hue_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(hue_preview, speed_preview, similarity=1)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_10(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M265] Add "Ghost 1" > Download Effect
        with uuid("3ca8ffd5-9c84-4e85-9b8b-87cbdfafb44d") as case:
            # Insert skateboard_girl.mp4
            video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:01:04
            main_page.set_timeline_timecode('00_00_01_04')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()
            time.sleep(DELAY_TIME * 2)

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Ghost 1')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Ghost 1')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Ghost 1')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')

            # Set timecode 00:00:01:04
            main_page.set_timeline_timecode('00_00_01_04')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.999)
            case.result = not preview_update

        # [M266] "Ghost 1" > Check Size preview
        with uuid("74a16ef0-6c1a-4c63-8684-c99c22e52b7c") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, size_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M267] "Ghost 1" > Check Distance preview
        with uuid("4e3030d5-bfc3-4121-8f33-5381f9115083") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 2, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            distance_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(distance_preview, size_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M268] "Ghost 1" > Check Opacity preview
        with uuid("859f303f-1163-4597-9b4e-ed0bfa88e204") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 9, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            opacity_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(distance_preview, opacity_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M269] "Ghost 1" > Adjust color preview
        with uuid("7c993fcd-5311-473e-bf95-ce7ffef9f473") as case:
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME)
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('FB0024')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(distance_preview, color_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M271] "Ghost 1" > Check preset preview
        with uuid("9da3abed-9655-4f51-979a-5cd590d335ec") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.set_dropdown_menu(custom_type='Preset 2', custom_locator=L.effect_settings.cbx_preset)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            preset_2_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(preset_2_preview, color_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_11(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M272] Add "Ghost 2" > Download Effect
        with uuid("5799d990-b6a1-46a6-ac9c-d24cc3abbeea") as case:
            # Snapshot Default : "Skateboard 01.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:05:24
            main_page.set_timeline_timecode('00_00_05_24')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Ghost 2')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Ghost 2')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 01')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Ghost 2')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 01')

            # Set timecode 00:00:05:24
            main_page.set_timeline_timecode('00_00_05_24')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.99)
            case.result = not preview_update

        # [M274] "Ghost 2" > Check Distance preview
        with uuid("fd47228c-c2d1-4a92-b6fb-e5382fac1bce") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 7, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            distance_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, distance_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M273] "Ghost 2" > Check Size preview
        with uuid("00dd4df2-37ca-4a74-a9bc-f1fb6e4b745e") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 168)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, distance_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M275] "Ghost 2" > Check Opacity preview
        with uuid("e4f1b395-3ac2-4a3e-aae9-29d45098b394") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            opacity_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(opacity_preview, size_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M279] "Ghost 2" > Check Preset preview
        with uuid("e76a0799-9e08-4693-9f65-370045a94ee5") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.set_dropdown_menu(custom_type='Preset 1', custom_locator=L.effect_settings.cbx_preset)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            preset_1_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(preset_1_preview, opacity_preview, similarity=0.96)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M276] "Ghost 2" > Check Glow Strength preview
        with uuid("0376b93e-23de-4250-a633-09bf86960ce1") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            # Preview is no update
            # verify step: Only check adjust result
            case.result = adjust_result

        # [M277] "Ghost 2" > Adjust color preview
        with uuid("3560c134-02bc-4764-821d-7fa64d53c696") as case:
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('BF25DB')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(preset_1_preview, color_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 4 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_12(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M280] Add "Graffiti 01" > Download Effect
        with uuid("30a7b68f-f319-4128-936a-7d8fd2b1dd4b") as case:
            # Snapshot Default : "Skateboard 01.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:05:24
            main_page.set_timeline_timecode('00_00_05_24')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Graffiti 01')
            time.sleep(DELAY_TIME * 2)

            # Select effect to insert video track
            self.apply_effect_to_timeline_clip('Graffiti 01')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 01')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Graffiti 01')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 01')

            # Set timecode 00:00:05:24
            main_page.set_timeline_timecode('00_00_05_24')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview)
            case.result = not preview_update

        # [M281] "Graffiti 01" > Check Speed preview
        with uuid("7a161495-2eb8-44d8-b679-c0f04874dcc1") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 195)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, speed_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M282] "Graffiti 01" > Check Hue preview
        with uuid("d57c7856-c11a-4f48-8839-b71cc6c8fb73") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 177, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            hue_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(hue_preview, speed_preview, similarity=0.999)
            preview_most_same = main_page.compare(hue_preview, speed_preview, similarity=0.9)
            logger(preview_update)
            logger(preview_most_same)
            case.result = adjust_result and preview_update and preview_most_same

        # [M283] "Graffiti 01" > Check Size preview
        with uuid("1a3364a2-0c90-45da-8311-51c33f65aa08") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(hue_preview, size_preview, similarity=0.97)
            preview_most_same = main_page.compare(hue_preview, size_preview, similarity=0.87)
            logger(preview_update)
            logger(preview_most_same)
            case.result = adjust_result and preview_update and preview_most_same

    # 4 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_13(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M284] Add "Graffiti 02" > Download Effect
        with uuid("1221f0c6-6a6d-4815-a987-a50e9fe92b71") as case:
            # Snapshot Default : "Skateboard 02.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:05:24
            main_page.set_timeline_timecode('00_00_05_24')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Graffiti 02')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Graffiti 02')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 02')
            # Set timecode 00:00:05:24
            main_page.set_timeline_timecode('00_00_05_24')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.99)
            preview_most_same = main_page.compare(default_preview, current_preview, similarity=0.9)

            case.result = preview_update and preview_most_same

        # [M285] "Graffiti 02" > Check Speed preview
        with uuid("2fd02007-65ba-4fb4-a454-e0f832634519") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 0)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, speed_preview, similarity=0.985)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M286] "Graffiti 02" > Check Hue preview
        with uuid("80a46f41-69eb-4073-b442-abd5a9f0f8db") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 67, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            hue_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(hue_preview, speed_preview, similarity=1)
            preview_most_same = main_page.compare(hue_preview, speed_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M287] "Graffiti 02" > Check Size preview
        with uuid("241296a9-357e-4c48-8482-030579c5657e") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            hue_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(hue_preview, speed_preview, similarity=0.99)
            preview_most_same = main_page.compare(hue_preview, speed_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_14(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M288] Add "Light Snake 1" > Download Effect
        with uuid("4c9347d2-005a-4de1-954c-0c2189a230f0") as case:
            # Snapshot Default : "Skateboard 03.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:04:09
            main_page.set_timeline_timecode('00_00_04_09')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Light Snake 1')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Light Snake 1')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 03')
            # Set timecode 00:00:04:09
            main_page.set_timeline_timecode('00_00_04_09')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.9999)
            preview_most_same = main_page.compare(default_preview, current_preview, similarity=0.9)

            case.result = preview_update and preview_most_same

        # [M291] "Light Snake 1" > Check Length preview
        with uuid("79577a9e-b234-46ef-901c-e42bc3987637") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, applied_preview, similarity=1)
            preview_most_same = main_page.compare(current_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M289] "Light Snake 1" > Check Size preview
        with uuid("61829ce2-52fa-40bd-9458-368f3c119062") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, applied_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M290] "Light Snake 1" > Check Offset preview
        with uuid("db5db511-3623-4640-8b08-f74895205c5c") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            offset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, applied_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M292] "Light Snake 1" > Check Period preview
        with uuid("fd70f78a-54d6-4931-87cb-e51f588050bd") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            period_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, period_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M294] "Light Snake 1" > Check Opacity preview
        with uuid("aad9488f-f088-43c3-9a48-2c43bf4be64c") as case:
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 100, option=5)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            opacity_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(opacity_preview, offset_preview, similarity=1)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M293] "Light Snake 1" > Adjust Color preview
        with uuid("0864a778-eb15-457a-95cf-2741e808f5dd") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('421010')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(opacity_preview, color_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M294] "Light Snake 1" > Adjust Preset preview
        with uuid("ad71c0e5-9f6f-4515-a816-19e0d9730629") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.set_dropdown_menu(custom_type='Preset 1', custom_locator=L.effect_settings.cbx_preset)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            preset_1_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(preset_1_preview, color_preview, similarity=0.99)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_15(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M296] Add "Light Snake 2" > Download Effect
        with uuid("2ee6a38b-23ac-4bcc-9036-9011cf010bed") as case:
            # Insert skateboard_girl.mp4
            video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:01:04
            main_page.set_timeline_timecode('00_00_01_04')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Light Snake 2')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Light Snake 2')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')
            # Set timecode 00:00:01:04
            main_page.set_timeline_timecode('00_00_01_04')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.999)
            case.result = not preview_update

        # [M299] "Light Snake 2" > Check Length preview
        with uuid("de087cdf-346a-4cde-a15a-f09e14962d7c") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, applied_preview, similarity=1)
            preview_most_same = main_page.compare(current_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M301] "Light Snake 2" > Adjust Color preview
        with uuid("fdde268c-e292-49b4-a255-ac07d59a551b") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('6719B5')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(applied_preview, color_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M302] "Light Snake 2" > Check Opacity preview
        with uuid("78c41f82-ce1e-4280-bd26-afa60e4b9f75") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(100, 0, option=5)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_most_same = main_page.compare(default_preview, applied_preview, similarity=0.99)
            logger(preview_most_same)
            case.result = adjust_result and preview_most_same

        # [M300] "Light Snake 2" > Check Period preview
        with uuid("7942d682-130e-4e34-b8d5-7d48864f436d") as case:
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 0, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            period_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(applied_preview, period_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M297] "Light Snake 2" > Check Size preview
        with uuid("fc7fc826-edd1-41d0-b039-676f31571525") as case:
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 17)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, period_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M298] "Light Snake 2" > Check Offset preview
        with uuid("6496e1d1-6730-42bf-9a92-dfcb26f156e9") as case:
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            offset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, offset_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M303] "Light Snake 2" > Adjust Preset preview
        with uuid("52b34f9c-6800-4e5a-9e78-10ee21c18932") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.set_dropdown_menu(custom_type='Preset 1', custom_locator=L.effect_settings.cbx_preset)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            preset_1_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(preset_1_preview, offset_preview, similarity=0.999)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_16(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M304] Add "Lightning" > Download Effect
        with uuid("6f47d72f-250c-4d58-afe8-19c06340a9be") as case:
            # Snapshot Default : "Skateboard 03.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            time.sleep(DELAY_TIME)

            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Lightning')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Lightning')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 03')

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.9999)
            preview_most_same = main_page.compare(default_preview, current_preview, similarity=0.9)

            case.result = preview_update and preview_most_same

        # [M305] "Lightning" > Check Speed preview
        with uuid("afa13c9e-a0ee-479d-8713-0e8eef35ac8c") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 117)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, applied_preview, similarity=0.995)
            preview_most_same = main_page.compare(current_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M306] "Lightning" > Check Width preview
        with uuid("2c235f98-5fc0-460e-a0c8-e5ab07fae184") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            width_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(width_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(width_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M307] "Lightning" > Check Height preview
        with uuid("fac021ee-b578-4b79-b3cf-7b1c3150112b") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(179, 43, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            height_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(width_preview, height_preview, similarity=0.99)
            preview_most_same = main_page.compare(width_preview, height_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M308] "Lightning" > Check Position preview
        with uuid("cc618507-d500-4b1d-9081-b25f5d440a85") as case:
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 47, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            pos_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(width_preview, pos_preview)
            preview_most_same = main_page.compare(width_preview, pos_preview, similarity=0.85)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M309] "Lightning" > Check Hue preview
        with uuid("3a02f0b3-1993-40bc-951f-0eaac6154232") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 46, option=5)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            hue_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(hue_preview, pos_preview, similarity=0.999)
            case.result = adjust_result and preview_update

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_17(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M310] Add "Magic Swirl 01" > Download Effect
        with uuid("0a2b2053-2f72-4181-a84b-b9245a0c7600") as case:
            # Snapshot Default : "Skateboard 01.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:04:02
            main_page.set_timeline_timecode('00_00_04_02')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()
            time.sleep(DELAY_TIME * 2)

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Magic Swirl 01')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Magic Swirl 01')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 01')

            # Set timecode 00:00:04:02
            main_page.set_timeline_timecode('00_00_04_02')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.9999)
            preview_most_same = main_page.compare(default_preview, current_preview, similarity=0.9)

            case.result = preview_update and preview_most_same

        # [M311] "Magic Swirl 01" > Check Speed preview
        with uuid("73bd4f2f-bb42-4cae-ae3b-35f755a98493") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 198)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(current_preview, applied_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M312] "Magic Swirl 01" > Check Width preview
        with uuid("3ed104d5-ce25-4fd9-89d9-2d1f60e0f979") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            width_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(width_preview, applied_preview, similarity=0.99)
            preview_most_same = main_page.compare(width_preview, applied_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M313] "Magic Swirl 01" > Check Height preview
        with uuid("c1a7f467-b774-49a8-ade2-a6b7fae8fc5e") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(190, 92, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            height_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(width_preview, height_preview, similarity=0.99)
            preview_most_same = main_page.compare(width_preview, height_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M314] "Magic Swirl 01" > Check Position preview
        with uuid("8165173e-b357-41d0-97af-cf2a3c217ef1") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 166, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            pos_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(pos_preview, height_preview, similarity=0.99)
            preview_most_same = main_page.compare(pos_preview, height_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

        # [M315] "Magic Swirl 01" > Check Hue preview
        with uuid("91a1618e-019c-4755-ad32-c6e06924c3a4") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(10, 147, option=5)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            hue_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(hue_preview, pos_preview, similarity=1)
            case.result = adjust_result and preview_update

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_18(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M316] Add "Magic Swirl 02" > Download Effect
        with uuid("6ec27ad3-12e2-4cb9-8ef9-d14e95e2241c") as case:
            # Insert skateboard_girl.mp4
            video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:06:20
            main_page.set_timeline_timecode('00_00_06_20')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Magic Swirl 02')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Magic Swirl 02')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')
            # Set timecode 00:00:06:20
            main_page.set_timeline_timecode('00_00_06_20')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.99)
            preview_most_same = main_page.compare(default_preview, current_preview)
            case.result = (not preview_update) and preview_most_same

        # [M321] "Magic Swirl 02" > Check Hue preview
        with uuid("a362954b-5ca8-46bd-acfd-00dcf84ede68") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 141, option=5)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            hue_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(hue_preview, current_preview, similarity=1)
            case.result = adjust_result and preview_update

        # [M318] "Magic Swirl 02" > Check Width preview
        with uuid("20df7951-03b3-4691-bfb5-45a04eed2513") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 146, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            width_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(hue_preview, width_preview, similarity=0.99)
            preview_most_same = main_page.compare(hue_preview, width_preview)
            case.result = adjust_result and preview_update and preview_most_same

        # [M317] "Magic Swirl 02" > Check Speed preview
        with uuid("a4bf58ec-dc61-4bf6-817c-7bb9d2f1281f") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 178)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(speed_preview, width_preview, similarity=0.99)
            preview_most_same = main_page.compare(speed_preview, width_preview, similarity=0.9)
            case.result = adjust_result and preview_update and preview_most_same

        # [M319] "Magic Swirl 02" > Check Height preview
        with uuid("5c9fa047-9b91-48a2-8926-57831e9c1ca1") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 55, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            height_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(speed_preview, height_preview, similarity=0.99)
            preview_most_same = main_page.compare(speed_preview, height_preview, similarity=0.9)
            case.result = adjust_result and preview_update and preview_most_same

        # [M320] "Magic Swirl 02" > Check Position preview
        with uuid("0df9cc57-7492-4282-ba82-3a2ee105fa91") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 176, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            height_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(speed_preview, height_preview, similarity=0.99)
            preview_most_same = main_page.compare(speed_preview, height_preview, similarity=0.9)
            case.result = adjust_result and preview_update and preview_most_same

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_19(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M322] Add "Magic Swirl 03" > Download Effect
        with uuid("c945eb0b-2bcf-42fe-8c78-17ee148e0509") as case:
            # Snapshot Default : "Skateboard 02.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:05:21
            main_page.set_timeline_timecode('00_00_05_21')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Magic Swirl 03')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Magic Swirl 03​')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 02')
            # Set timecode 00:00:05:21
            main_page.set_timeline_timecode('00_00_05_21')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.999)
            preview_most_same = main_page.compare(default_preview, current_preview)
            case.result = (not preview_update) and preview_most_same

        # [M324] "Magic Swirl 03" > Check Width preview
        with uuid("50dd95d8-a0e6-40f1-a490-55737a94a556") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(91, 199, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            width_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, width_preview, similarity=0.999)
            preview_most_same = main_page.compare(current_preview, width_preview)
            case.result = adjust_result and preview_update and preview_most_same

        # [M327] "Magic Swirl 03" > Check Hue preview
        with uuid("6a904623-8e34-4f6a-bda3-582ec38fb4bb") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 71, option=5)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            hue_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(width_preview, hue_preview, similarity=1)
            preview_most_same = main_page.compare(width_preview, hue_preview, similarity=0.97)
            case.result = adjust_result and preview_update and preview_most_same

        # [M323] "Magic Swirl 03" > Check Speed preview
        with uuid("bb1c8afb-c4c4-4143-8b17-35c6843384bc") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(2, 174)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(speed_preview, hue_preview, similarity=1)
            preview_most_same = main_page.compare(speed_preview, hue_preview)
            case.result = adjust_result and preview_update and preview_most_same

        # [M326] "Magic Swirl 03" > Check Position preview
        with uuid("685b10ca-d276-47e4-8a68-05584d784087") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 146, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            pos_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(speed_preview, pos_preview, similarity=0.99)
            preview_most_same = main_page.compare(speed_preview, pos_preview)
            case.result = adjust_result and preview_update and preview_most_same

        # [M325] "Magic Swirl 03" > Check Height preview
        with uuid("1b762534-549c-4d69-a41f-599cf51b8ab6") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(195, 80, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            h_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(h_preview, pos_preview, similarity=0.996)
            preview_most_same = main_page.compare(h_preview, pos_preview)
            case.result = adjust_result and preview_update and preview_most_same

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_20(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M328] Add "Marching Ants" > Download Effect
        with uuid("513613b4-bd49-456c-be6f-37410daa7297") as case:
            # Snapshot Default : "Skateboard 03.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:05:21
            main_page.set_timeline_timecode('00_00_05_21')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Marching Ants')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Marching Ants')
            self.apply_effect_to_timeline_clip('Marching Ants')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 03')
            # Set timecode 00:00:05:21
            main_page.set_timeline_timecode('00_00_05_21')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.999)
            preview_most_same = main_page.compare(default_preview, current_preview)
            case.result = (not preview_update) and preview_most_same

        # [M329] "Marching Ants" > Check Size preview
        with uuid("e588d4ae-7a90-48e8-b860-8c268a7bdffc") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 40)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, size_preview, similarity=0.999)
            preview_most_same = main_page.compare(current_preview, size_preview)
            case.result = adjust_result and preview_update and preview_most_same

        # [M330] "Marching Ants" > Check Offset preview
        with uuid("43a930c2-6dcf-4941-8b91-4b38fe38f073") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            offset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, size_preview, similarity=0.999)
            preview_most_same = main_page.compare(offset_preview, size_preview)
            case.result = adjust_result and preview_update and preview_most_same

        # [M331] "Marching Ants" > Check (Length and Space) preview
        with uuid("c41b152e-654e-4c23-8535-8799ce0456ea") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 0, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            space_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, space_preview, similarity=0.999)
            preview_most_same = main_page.compare(offset_preview, space_preview)
            case.result = adjust_result and preview_update and preview_most_same

        # [M332] "Marching Ants" > Change color preview
        with uuid("e44d8682-bfb7-4d11-8c64-6d2932236746") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('94F617')
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(space_preview, applied_preview, similarity=0.999)
            case.result = adjust_result and preview_update

        # [M334] "Marching Ants" > Check Preset preview
        with uuid("addbe1ac-90b9-4169-b99a-2c51337cf98f") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.set_dropdown_menu(custom_type='Preset 2', custom_locator=L.effect_settings.cbx_preset)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            preset_2_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(preset_2_preview)

            preview_update = not main_page.compare(preset_2_preview, applied_preview, similarity=0.992)
            preview_most_same = main_page.compare(preset_2_preview, applied_preview)
            case.result = adjust_result and preview_update and preview_most_same

        # [M333] "Marching Ants" > Check opacity preview
        with uuid("f26f3cfb-0ea4-4b7d-a4da-d9be845c6e05") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 100, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            opacity_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(preset_2_preview, opacity_preview, similarity=1)
            preview_most_same = main_page.compare(preset_2_preview, opacity_preview)
            case.result = adjust_result and preview_update and preview_most_same

    # 4 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_21(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M335] Add "Motion Lines 01" > Download Effect
        with uuid("8da17b98-b134-434b-817f-6834116f1157") as case:
            # Insert skateboard_girl.mp4
            video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:06:20
            main_page.set_timeline_timecode('00_00_06_20')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Motion Lines 01')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Motion Lines 01​')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')
            # Set timecode 00:00:06:20
            main_page.set_timeline_timecode('00_00_06_20')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.99)
            preview_most_same = main_page.compare(default_preview, current_preview)
            case.result = (not preview_update) and preview_most_same

        # [M336] "Motion Lines 1" > Check Speed preview
        with uuid("811e57f2-bee6-4e67-96eb-c03e54916259") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 164)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, speed_preview, similarity=0.999)
            preview_most_same = main_page.compare(current_preview, speed_preview)
            case.result = adjust_result and preview_update and preview_most_same

        # [M337] "Motion Lines 1" > Adjust color preview
        with uuid("0c1ce5df-06c5-434f-a4ce-54f1430363f6") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('FC1D27')
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(applied_preview, speed_preview, similarity=0.999)
            preview_most_same = main_page.compare(applied_preview, speed_preview)
            case.result = adjust_result and preview_update and preview_most_same

        # [M338] "Motion Lines 1" > Check Size preview
        with uuid("ba462057-94da-4845-bfe1-e7b305abd334") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 25, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, applied_preview, similarity=0.999)
            preview_most_same = main_page.compare(size_preview, applied_preview)
            case.result = adjust_result and preview_update and preview_most_same

    # 4 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_22(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M339] Add "Motion Lines 02" > Download Effect
        with uuid("83bc5d5a-1cb5-478f-9953-185e700a13d9") as case:
            # Insert skateboard_girl.mp4
            video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:04:15
            main_page.set_timeline_timecode('00_00_04_15')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Motion Lines 02')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Motion Lines 02')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')
            # Set timecode 00:00:04:15
            main_page.set_timeline_timecode('00_00_04_15')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.99)
            preview_most_same = main_page.compare(default_preview, current_preview, similarity=0.9)
            case.result = (not preview_update) and preview_most_same

        # [M340] "Motion Lines 02" > Check Speed preview
        with uuid("58dcbd84-45d2-4f76-b7c9-760bbe8637d5") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, speed_preview, similarity=0.999)
            preview_most_same = main_page.compare(current_preview, speed_preview, similarity=0.8)
            case.result = adjust_result and preview_update and preview_most_same

        # [M342] "Motion Lines 02" > Check Size preview
        with uuid("1099a973-6ba6-4a83-b147-2dbb6622b433") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 144, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, speed_preview, similarity=0.999)
            preview_most_same = main_page.compare(size_preview, speed_preview, similarity=0.8)
            case.result = adjust_result and preview_update and preview_most_same

        # [M341] "Motion Lines 02" > Adjust color preview
        with uuid("615bec94-6ef9-40e2-a113-71e51e4a0585") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('DC1589')
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(applied_preview, size_preview, similarity=0.999)
            preview_most_same = main_page.compare(applied_preview, size_preview)
            case.result = adjust_result and preview_update and preview_most_same

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_23(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M362] Add "Motion Trail - Pulse 2" > Download Effect
        with uuid("1f7eed61-3c73-4b2a-9d92-c8d46c5acfb1") as case:
            # Snapshot Default : "Skateboard 02.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:03:12
            main_page.set_timeline_timecode('00_00_03_12')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Motion Trail')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Motion Trail - Pulse 2')

            result = self.check_download_body_effect()
            logger(result)

            # Click [Play] 3 sec. then pause
            playback_window_page.Edit_Timeline_PreviewOperation('play')
            time.sleep(DELAY_TIME * 3)
            playback_window_page.Edit_Timeline_PreviewOperation('pause')
            time.sleep(DELAY_TIME * 3)

            # Set timecode 00:00:03:12
            main_page.set_timeline_timecode('00_00_03_12')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.96)
            preview_most_same = main_page.compare(default_preview, current_preview, similarity=0.9)
            case.result = (not preview_update) and preview_most_same

        # [M363] "Motion Trail - Pulse 2" > Check Distance preview
        with uuid("56e0acee-7cd7-4d86-ad45-1de1141f97cc") as case:
            # Select timeline clip
            main_page.select_timeline_media('Skateboard 02')
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 172)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            distance_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, distance_preview)
            preview_most_same = main_page.compare(current_preview, distance_preview, similarity=0.9)
            case.result = adjust_result and preview_update and preview_most_same

        # [M364] "Motion Trail - Pulse 2" > Check scale preview
        with uuid("868307cf-ecfb-4db7-8363-bff2857f7587") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            scale_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(scale_preview, distance_preview)
            preview_most_same = main_page.compare(scale_preview, distance_preview, similarity=0.9)
            case.result = adjust_result and preview_update and preview_most_same

        # [M365] "Motion Trail - Pulse 2" > Check period preview
        with uuid("db0f983a-79c4-4974-bb2c-62173ebcddd1") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 25, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            scale_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(scale_preview, distance_preview)
            preview_most_same = main_page.compare(scale_preview, distance_preview, similarity=0.9)
            case.result = adjust_result and preview_update and preview_most_same

        # [M366] "Motion Trail - Pulse 2" > Check clone count preview
        with uuid("b65f6e70-5f60-477c-8df3-51444e22417b") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(5, 1, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            count_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(scale_preview, count_preview, similarity=0.98)
            preview_most_same = main_page.compare(scale_preview, count_preview, similarity=0.9)
            case.result = adjust_result and preview_update and preview_most_same

        # [M367] "Motion Trail - Pulse 2" > Check opacity count preview
        with uuid("270725f6-0660-46e4-a8d9-e68ed54d69b4") as case:
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)
            opacity_124_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 28, option=5)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            opacity_28_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(opacity_124_preview, opacity_28_preview, similarity=0.97)
            preview_most_same = main_page.compare(opacity_124_preview, opacity_28_preview, similarity=0.9)
            case.result = adjust_result and preview_update and preview_most_same

        # [M370] "Motion Trail - Pulse 2" > Check Preset preview
        with uuid("46d17bfe-fd22-4ea6-8fca-72f4c4cb5b6f") as case:
            # Set timecode 00:00:00:28
            main_page.set_timeline_timecode('00_00_00_28')
            time.sleep(DELAY_TIME * 2)
            default_preset = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.set_dropdown_menu(custom_type='Preset 2', custom_locator=L.effect_settings.cbx_preset)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            preset_2_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(preset_2_preview)

            preview_update = not main_page.compare(preset_2_preview, default_preset, similarity=0.992)
            logger(preview_update)
            case.result = adjust_result and preview_update

    # 2 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_24(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M379] Add "Particle - Stars" > Download Effect
        with uuid("9d50293a-a6a5-4c46-b258-5fa4e42cf60d") as case:
            # Snapshot Default : "Skateboard 01.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:04:00
            main_page.set_timeline_timecode('00_00_04_00')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Particle')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Particle - Stars')

            result = self.check_download_body_effect()
            logger(result)

            # Set timecode 00:00:04:00
            main_page.set_timeline_timecode('00_00_04_00')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.99)
            preview_most_same = main_page.compare(default_preview, current_preview, similarity=0.9)
            case.result = (not preview_update) and preview_most_same

        # [M380] "Particle - Stars" > Check speed preview
        with uuid("52190631-1b8c-4ab3-8593-fafce422622c") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 0)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, speed_preview, similarity=0.97)
            preview_most_same = main_page.compare(current_preview, speed_preview, similarity=0.9)
            case.result = adjust_result and preview_update and preview_most_same

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_25(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M381] Add "Shadow" > Download Effect
        with uuid("1c7edb58-8d77-437b-9f03-01eaccff100e") as case:
            # Insert skateboard_girl.mp4
            video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:06:19
            main_page.set_timeline_timecode('00_00_06_19')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Shadow')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Shadow')

            result = self.check_download_body_effect()
            logger(result)

            # Set timecode 00:00:06:19
            main_page.set_timeline_timecode('00_00_06_19')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.998)
            preview_most_same = main_page.compare(default_preview, current_preview, similarity=0.9)
            case.result = (not preview_update) and preview_most_same

        # [M382] "Shadow" > Check opacity preview
        with uuid("e77f78ac-9ba0-4897-bb9e-ce8ebadb4dfe") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            opacity_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, opacity_preview, similarity=1)
            preview_most_same = main_page.compare(current_preview, opacity_preview)
            case.result = adjust_result and preview_update and preview_most_same

        # [M383] "Shadow" > Check color preview
        with uuid("c812034f-b301-44b8-a19e-bcbb6181182d") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('FF24FF', option=L.effect_settings.btn_clone_color)
            time.sleep(DELAY_TIME * 2)
            applied_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_preview)

            preview_update = not main_page.compare(applied_preview, opacity_preview, similarity=1)
            preview_most_same = main_page.compare(applied_preview, opacity_preview)
            case.result = adjust_result and preview_update and preview_most_same

        # [M384] "Shadow" > Check clone count preview
        with uuid("6c58418b-a104-469d-9e97-71d05c3bce0f") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 10, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            count_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(applied_preview, count_preview, similarity=0.999)
            preview_most_same = main_page.compare(applied_preview, count_preview, similarity=0.9)
            case.result = adjust_result and preview_update and preview_most_same

        # [M386] "Shadow" > Check Preset preview
        with uuid("b93b999a-3402-4db8-99c6-07e9fa5f8761") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.set_dropdown_menu(custom_type='Preset 1', custom_locator=L.effect_settings.cbx_preset)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            preset_1_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(preset_1_preview)

            preview_update = not main_page.compare(preset_1_preview, count_preview, similarity=0.99)
            preview_most_same = main_page.compare(applied_preview, count_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_most_same

    # 4 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_26(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M381] Add "Silhouette" > Download Effect
        with uuid("1a96276e-e14e-498f-9f3d-8243102f10ae") as case:
            # Insert skateboard_girl.mp4
            video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:06:07
            main_page.set_timeline_timecode('00_00_06_07')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Silhouette')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Silhouette')

            result = self.check_download_body_effect()
            logger(result)

            # Set timecode 00:00:06:07
            main_page.set_timeline_timecode('00_00_06_07')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.995)
            preview_most_same = main_page.compare(default_preview, current_preview, similarity=0.9)
            case.result = (not preview_update) and preview_most_same

        # [M388] "Silhouette" > Check opacity preview
        with uuid("bacd5352-3879-483b-9bbd-20db39c92bb4") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            opacity_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, opacity_preview, similarity=1)
            preview_most_same = main_page.compare(current_preview, opacity_preview)
            case.result = adjust_result and preview_update and preview_most_same

        # [M390] "Silhouette" > Check Clone count preview
        with uuid("0adcd4dd-bf68-431b-985f-4aac91912bd5") as case:
            # Click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 10, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            count_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, count_preview, similarity=0.99)
            preview_most_same = main_page.compare(current_preview, count_preview)
            case.result = adjust_result and preview_update and preview_most_same

        # [M392] "Silhouette" > Check Preset preview
        with uuid("76e8ee76-8207-4048-a613-37d8cd193e80") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.set_dropdown_menu(custom_type='Preset 1', custom_locator=L.effect_settings.cbx_preset)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            preset_1_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(preset_1_preview, count_preview, similarity=0.98)
            preview_most_same = main_page.compare(preset_1_preview, count_preview)
            case.result = adjust_result and preview_update and preview_most_same

    # 1 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_3_1(self):
        # [M396] Bug regression : VDE235020-0004
        with uuid("8bb74f8a-caaf-4068-bdf9-7cb4f75a5da8") as case:
            # clear AI module
            main_page.clear_AI_module()

            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            time.sleep(DELAY_TIME)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Motion Trail')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Motion Trail - Color')

            result = self.check_download_body_effect()
            logger(result)

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result_1 = effect_settings_page.body_effect.adjust_1st_slider(0, 15, option=3)
            logger(adjust_result_1)
            time.sleep(DELAY_TIME * 2)
            playback_window_page.Edit_Timeline_PreviewOperation('play')
            time.sleep(DELAY_TIME * 8)
            playback_window_page.Edit_Timeline_PreviewOperation('pause')
            adjust_result_2 = effect_settings_page.body_effect.adjust_1st_slider(6, 25, option=3)
            logger(adjust_result_2)
            adjust_result_3 = effect_settings_page.body_effect.adjust_1st_slider(0, 30, option=3)
            logger(adjust_result_3)
            case.result = adjust_result_1 and adjust_result_2 and adjust_result_3

    # 1 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_3_2(self):
        # [M397] Bug regression : VDE235008-0003
        with uuid("8c8076f5-60ed-4e12-b1af-8f135b6c61dd") as case:
            # clear AI module
            main_page.clear_AI_module()

            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Comics')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Comics 01')

            result = self.check_download_body_effect()
            logger(result)

            playback_window_page.Edit_Timeline_PreviewOperation('play')
            time.sleep(DELAY_TIME * 5)
            playback_window_page.Edit_Timeline_PreviewOperation('pause')

            # Close App then re-launch PDR
            main_page.close_and_restart_app()
            time.sleep(DELAY_TIME*4)

            # Click (Import sample video)
            if main_page.exist(L.media_room.string_use_sample_media, timeout=7):
                main_page.click(L.media_room.string_use_sample_media)
                time.sleep(DELAY_TIME*4)

            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Comics')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Comics 01')
            time.sleep(DELAY_TIME * 5)

            result = main_page.is_exist(L.tips_area.button.btn_effect_modify)
            case.result = result

    # 1 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_3_3(self):
        # [M398] Bug regression : VDE235020-0004
        with uuid("ce913f47-216f-4f4c-8081-c1df39876c85") as case:
            # clear AI module
            main_page.clear_AI_module()

            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            time.sleep(DELAY_TIME)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Motion Trail')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Motion Trail - Color')

            result = self.check_download_body_effect()
            logger(result)

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            playback_window_page.Edit_Timeline_PreviewOperation('play')
            time.sleep(DELAY_TIME * 5)
            playback_window_page.Edit_Timeline_PreviewOperation('pause')

            # Adjust parameter
            adjust_result_1 = effect_settings_page.body_effect.adjust_1st_slider(0, 15, option=3, custom_loop_time=10)
            logger(adjust_result_1)
            time.sleep(DELAY_TIME * 2)
            adjust_result_2 = effect_settings_page.body_effect.adjust_1st_slider(0, 30, option=3, custom_loop_time=30)
            logger(adjust_result_2)
            time.sleep(DELAY_TIME * 2)
            adjust_result_3 = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=2, custom_loop_time=10)
            logger(adjust_result_3)
            case.result = adjust_result_1 and adjust_result_2 and adjust_result_3

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_4_1(self):
        # [M404] Add "Magnifier" > Check Magnify Rate preview
        with uuid("857b00a5-8fda-4a02-9e2b-f4474007218a") as case:
            # Insert Y man.mp4
            video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:03:19
            main_page.set_timeline_timecode('00_00_03_19')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search Effect
            media_room_page.search_library('Magnifier')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Magnifier')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.magnifier.adjust_magnify_rate_slider()
            logger(adjust_result)

            # Click play then pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.press_space_key()

            # Set timecode 00:00:03:19
            main_page.set_timeline_timecode('00_00_03_19')
            time.sleep(DELAY_TIME * 2)

            applied_rate_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_rate_preview)

            preview_update = not main_page.compare(default_preview, applied_rate_preview, similarity=0.94)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M405] Add "Magnifier" > Check Frame Width preview
        with uuid("dbf05994-f93c-4b9c-b0b0-19ad6804c016") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.magnifier.adjust_frame_width_slider()
            time.sleep(DELAY_TIME * 2)
            applied_frame_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_frame_preview)

            preview_update = not main_page.compare(applied_rate_preview, applied_frame_preview, similarity=0.96)
            case.result = adjust_result and preview_update

        # [M408] Add "Magnifier" > Check Frame Feather preview
        with uuid("41b4e74e-8b45-4160-a17a-08c88102306b") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.magnifier.adjust_frame_feather_slider()
            time.sleep(DELAY_TIME * 2)
            applied_feather_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_feather_preview)

            preview_update = not main_page.compare(applied_feather_preview, applied_frame_preview, similarity=0.98)
            case.result = adjust_result and preview_update

        # [M409] Add "Magnifier" > adjust Magnifier type then check preview
        with uuid("9ea26311-45ca-4d4b-8746-23081bf8b482") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.magnifier.set_magnify_type('Box')
            time.sleep(DELAY_TIME * 2)
            applied_type_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_type_preview)

            preview_update = not main_page.compare(applied_feather_preview, applied_type_preview, similarity=0.98)
            case.result = adjust_result and preview_update

        # [M406] Add "Magnifier" > adjust Magnify Size then check preview
        with uuid("dc075b99-f70d-43c7-93f3-43431814703d") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.magnifier.adjust_magnify_size_slider()
            time.sleep(DELAY_TIME * 2)
            applied_size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_size_preview)

            preview_update = not main_page.compare(applied_size_preview, applied_type_preview, similarity=0.8)
            case.result = adjust_result and preview_update

        # [M407] Add "Magnifier" > Aspect ratio update preview
        with uuid("fa1a04a5-e20c-4fde-a287-65f9ba4ef72e") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.magnifier.adjust_aspect_ratio_slider()
            time.sleep(DELAY_TIME * 2)
            applied_ratio_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_ratio_preview)

            preview_update = not main_page.compare(applied_size_preview, applied_ratio_preview, similarity=0.75)
            case.result = adjust_result and preview_update

        # [M411] Add "Magnifier" > adjust Frame Color update preview
        with uuid("2a508b6a-028e-4b07-9d60-3e54ff829396") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.magnifier.adjust_frame_color('FF63E0')
            time.sleep(DELAY_TIME * 2)
            applied_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_color_preview)

            preview_update = not main_page.compare(applied_color_preview, applied_ratio_preview, similarity=0.98)
            case.result = adjust_result and preview_update

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_4_2(self):
        # [M412] Add "Pencil Sketch" > Check Degree preview
        with uuid("1c0bc78b-38a5-46ad-9f5e-30e5525c3114") as case:
            # Insert skateboard_girl.mp4
            video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:03:08
            main_page.set_timeline_timecode('00_00_03_08')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search Effect
            media_room_page.search_library('Pencil')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Pencil Sketch')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.pencil_sketch.adjust_degree_slider()
            logger(adjust_result)

            # Click play then pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.press_space_key()

            # Set timecode 00:00:03:08
            main_page.set_timeline_timecode('00_00_03_08')
            time.sleep(DELAY_TIME * 2)

            applied_degree_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_degree_preview)

            preview_update = not main_page.compare(default_preview, applied_degree_preview, similarity=0.9)
            preview_no_update = main_page.compare(default_preview, applied_degree_preview, similarity=0.7)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M413] Add "Pencil Sketch" > Check Edge intensity preview
        with uuid("5ee1eb13-2c7b-422b-9dfe-ef25bec0a4d2") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.pencil_sketch.adjust_edge_intensity_slider()
            time.sleep(DELAY_TIME * 2)
            applied_intensity_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_intensity_preview)

            preview_update = not main_page.compare(applied_degree_preview, applied_intensity_preview, similarity=1)
            case.result = adjust_result and preview_update

        # [M414] Add "Pencil Sketch" > Check Edge degree preview
        with uuid("e6e703ce-6a7b-4e42-ab68-40e4a235bb01") as case:
            # click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.pencil_sketch.adjust_edge_degree_slider()
            time.sleep(DELAY_TIME * 2)
            applied_edge_degree_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_edge_degree_preview)

            preview_update = not main_page.compare(applied_degree_preview, applied_edge_degree_preview, similarity=1)
            case.result = adjust_result and preview_update

        # [M415] Add "Pencil Sketch" > Check Gradient preview
        with uuid("e01e35fa-2861-48d4-9215-803b9a42c10b") as case:
            # click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.pencil_sketch.adjust_gradient_depth_slider()
            time.sleep(DELAY_TIME * 2)
            applied_gradient_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_gradient_preview)

            preview_update = not main_page.compare(applied_degree_preview, applied_gradient_preview, similarity=0.94)
            preview_no_update = main_page.compare(applied_degree_preview, applied_gradient_preview, similarity=0.8)
            case.result = adjust_result and preview_update and preview_no_update

        # [M416] Add "Pencil Sketch" > Check Mask type preview
        with uuid("7eb74cef-bd51-4320-b0ae-437cde84b702") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.pencil_sketch.set_mask_type()
            time.sleep(DELAY_TIME * 2)
            applied_mask_type_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_mask_type_preview)

            preview_update = not main_page.compare(applied_gradient_preview, applied_mask_type_preview, similarity=0.99)
            case.result = adjust_result and preview_update

        # [M418] Add "Pencil Sketch" > Check Grayscale preview
        with uuid("c7201c5c-fca5-4297-950e-09deec1f4b65") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.pencil_sketch.enable_grayscale()
            time.sleep(DELAY_TIME * 2)
            applied_grayscale_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_grayscale_preview)

            preview_update = not main_page.compare(applied_grayscale_preview, applied_mask_type_preview, similarity=1)
            case.result = adjust_result and preview_update

        # [M419] Add "Pencil Sketch" > Check Invert masked preview
        with uuid("68e1fa7d-458a-45bd-b8c6-47b9335f5eb4") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.pencil_sketch.enable_invert_masked_area()
            time.sleep(DELAY_TIME * 2)
            applied_invert_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_invert_preview)

            preview_update = not main_page.compare(applied_grayscale_preview, applied_invert_preview, similarity=0.9)
            preview_no_update = main_page.compare(applied_grayscale_preview, applied_invert_preview, similarity=0.75)
            case.result = adjust_result and preview_update and preview_no_update

        # [M420] Add "Pencil Sketch" > Check Random stroke preview
        with uuid("c4518e02-34e0-4890-8211-aedb20eacc26") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.pencil_sketch.enable_random_stroke()
            time.sleep(DELAY_TIME * 2)
            applied_stroke_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_stroke_preview)

            preview_update = not main_page.compare(applied_stroke_preview, applied_invert_preview, similarity=1)
            case.result = adjust_result and preview_update

    # 3 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_4_3(self):
        # [M421] Add "Edge" > Check Degree preview
        with uuid("21900324-7458-4e6f-acad-3a718e565aa2") as case:
            main_page.select_library_icon_view_media('Sport 02.jpg')
            time.sleep(DELAY_TIME)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Style Effect category
            self.enter_style_effect()

            # Search Effect
            media_room_page.search_library('Edge')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            main_page.drag_media_to_timeline_playhead_position('Edge')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()

            # Adjust parameter
            adjust_result = effect_settings_page.edge.adjust_degree_slider()
            logger(adjust_result)

            # Click play then pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)

            applied_degree_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_degree_preview)

            preview_update = not main_page.compare(default_preview, applied_degree_preview, similarity=0.5)
            preview_no_update = main_page.compare(default_preview, applied_degree_preview, similarity=0.3)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M422] Add "Edge" > Check Background Color preview
        with uuid("01c4c0cb-f2ad-4f67-ad97-fa84df1e323c") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.edge.adjust_BG_color('C8E300')
            time.sleep(DELAY_TIME * 2)
            applied_bg_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_bg_preview)

            preview_update = not main_page.compare(applied_bg_preview, applied_degree_preview, similarity=0.8)
            preview_no_update = main_page.compare(applied_bg_preview, applied_degree_preview, similarity=0.6)
            case.result = adjust_result and preview_update and preview_no_update

        # [M423] Add "Edge" > Check Front Color preview
        with uuid("da7b46d4-71e2-4856-9196-2b43273465cb") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.edge.adjust_FG_color('FF09FF')
            time.sleep(DELAY_TIME * 2)
            applied_font_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(applied_font_preview)

            preview_update = not main_page.compare(applied_bg_preview, applied_font_preview, similarity=0.8)
            preview_no_update = main_page.compare(applied_bg_preview, applied_font_preview, similarity=0.6)
            case.result = adjust_result and preview_update and preview_no_update

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_1(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M426] Add "Body Flicker" > Download Effect
        with uuid("05f1e319-b166-4805-8380-2be4df287a1e") as case:
            # Snapshot Default : "Skateboard 01.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:05:15
            main_page.set_timeline_timecode('00_00_05_15')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Body Flicker')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Body Flicker')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 01')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Body Flicker')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 01')

            # Click play then pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:05:15
            main_page.set_timeline_timecode('00_00_05_15')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.94)
            preview_no_update = main_page.compare(default_preview, current_preview, similarity=0.83)
            case.result = preview_update and preview_no_update

        # [M427] "Body Flicker" > Check Size preview
        with uuid("1ba75533-1911-47e2-b727-780064dd08c9") as case:
            # Select timeline clip
            main_page.select_timeline_media('Skateboard 01')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(22, 200)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, size_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update

        # [M428] "Body Flicker" > Check Object color preview
        with uuid("1a79c043-ee94-4fa3-818d-b188cd3863e7") as case:
            # Set timecode 00:00:06:15
            main_page.set_timeline_timecode('00_00_06_15')
            time.sleep(DELAY_TIME * 2)

            color_0_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(36, 93, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            color_93_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(color_0_preview, color_93_preview, similarity=1)
            preview_no_update = main_page.compare(color_0_preview, color_93_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M429] "Body Flicker" > Check Background color preview
        with uuid("6dab1bf7-260f-4ba8-8b58-3a751cc2f8d3") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(185, 87, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            bg_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(bg_color_preview, color_93_preview, similarity=1)
            preview_no_update = main_page.compare(bg_color_preview, color_93_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M430] "Body Flicker" > Check Speed preview
        with uuid("9ad57620-f001-41bb-a965-899d9a532511") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 123, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(bg_color_preview, speed_preview, similarity=0.98)
            preview_no_update = main_page.compare(bg_color_preview, speed_preview, similarity=0.8)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 3 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_2(self):
        # clear AI module
        main_page.clear_AI_module()

        # Insert skateboard_girl.mp4
        video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # [M431] Add "Butterfly Glow" > Download Effect
        with uuid("264413de-f1c2-4f2a-8f4a-2a42c72694f5") as case:
            # Set timecode 00:00:04:05
            main_page.set_timeline_timecode('00_00_04_05')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Butterfly Glow')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Butterfly Glow')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('skateboard_girl')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')

            # Click play then pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:04:05
            main_page.set_timeline_timecode('00_00_04_05')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.99)
            preview_no_update = main_page.compare(default_preview, current_preview, similarity=0.93)
            case.result = preview_update and preview_no_update

        # [M432] "Butterfly Glow" > Check Background Color preview
        with uuid("efb51464-3d82-4a4d-9278-4d50f88e0474") as case:
            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(189, 93)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            bg_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(bg_color_preview, current_preview, similarity=0.99)
            preview_no_update = main_page.compare(bg_color_preview, current_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M433] "Butterfly Glow" > Check Object Color preview
        with uuid("f9023014-8cd6-4501-a676-4edfe19bce89") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 72, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            object_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(bg_color_preview, object_color_preview, similarity=1)
            preview_no_update = main_page.compare(bg_color_preview, object_color_preview, similarity=0.94)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_3(self):
        # clear AI module
        main_page.clear_AI_module()

        # Insert skateboard_girl.mp4
        video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # [M434] Add "Cosmic Comets" > Download Effect
        with uuid("f4543306-7308-4057-94b9-9cbb31ada015") as case:
            # Set timecode 00:00:01:19
            main_page.set_timeline_timecode('00_00_01_19')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Cosmic Comets')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Cosmic Comets')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('skateboard_girl')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')

            # Click play then pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:01:19
            main_page.set_timeline_timecode('00_00_01_19')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.99)
            preview_no_update = main_page.compare(default_preview, current_preview, similarity=0.93)
            case.result = preview_update and preview_no_update

        # [M435] "Cosmic Comets" > Check Background Color preview
        with uuid("d83d607f-7729-4448-b498-cba40effa8ea") as case:
            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 108)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            bg_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(bg_color_preview, current_preview, similarity=0.99)
            preview_no_update = main_page.compare(bg_color_preview, current_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M436] "Cosmic Comets" > Check Glow size preview
        with uuid("3205598d-7f87-41af-b489-616e55c846ab") as case:
            # Set timecode 00:00:00:10
            main_page.set_timeline_timecode('00_00_00_10')
            time.sleep(DELAY_TIME * 2)

            size_0_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_200_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_0_preview, size_200_preview, similarity=1)
            preview_no_update = main_page.compare(size_0_preview, size_200_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M437] "Cosmic Comets" > Check Offset preview
        with uuid("4c6f8c93-8d70-453b-b148-467848b019c6") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            offset_200_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_200_preview, size_200_preview, similarity=0.995)
            preview_no_update = main_page.compare(offset_200_preview, size_200_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M438] "Cosmic Comets" > Check Edge Color preview
        with uuid("1f1b9634-d92c-493f-802a-5155518a4db4") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('10FF10')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_200_preview, color_preview, similarity=0.999999)
            preview_no_update = main_page.compare(offset_200_preview, color_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_4(self):
        # clear AI module
        main_page.clear_AI_module()

        # Insert skateboard_girl.mp4
        video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Fix / Enhance
        main_page.tips_area_click_fix_enhance()

        # Enable (White Balance)
        fix_enhance_page.fix.enable_white_balance(True)

        # Set (Color temperature) value = 90
        fix_enhance_page.fix.white_balance.color_temperature.set_value(19)
        time.sleep(DELAY_TIME * 2)

        # Close x  to leave (Fix/Enhance) page
        fix_enhance_page.click_close()
        time.sleep(DELAY_TIME * 2)

        # [M439] Add "Cloud Swirl" > Download Effect
        with uuid("ac6c744e-ca94-4915-97b4-75a52c522ca0") as case:
            # Set timecode 00:00:00:17
            main_page.set_timeline_timecode('00_00_00_17')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Cloud Swirl')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Cloud Swirl')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('skateboard_girl')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.999)
            preview_no_update = main_page.compare(default_preview, current_preview, similarity=0.93)
            case.result = preview_update and preview_no_update

        # [M440] "Cosmic Comets" > Check Width preview update
        with uuid("a5cb8a39-19b6-4f61-a89a-9c49e51a2bf9") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            width_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(width_preview, current_preview)
            preview_no_update = main_page.compare(width_preview, current_preview, similarity=0.84)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M441] "Cosmic Comets" > Check Position preview update
        with uuid("f2b7c4b0-c315-47c7-8092-2953d483665f") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 130, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            position_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(width_preview, position_preview)
            preview_no_update = main_page.compare(width_preview, position_preview, similarity=0.84)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M443] "Cosmic Comets" > Check Speed preview update
        with uuid("98fd9058-5927-45e3-983f-50bae03e935a") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(12, 89, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(width_preview, speed_preview)
            preview_no_update = main_page.compare(width_preview, speed_preview, similarity=0.84)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M442] "Cosmic Comets" > Check Height preview update
        with uuid("8259de2c-fe02-4ebc-97e5-256af6e1b880") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(2, 109, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            height_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(height_preview, speed_preview)
            preview_no_update = main_page.compare(height_preview, speed_preview, similarity=0.85)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 4 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_5(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M444] Add "Digital Discs" > Download Effect
        with uuid("95f697d1-c762-4de1-90cc-8caec21b78a3") as case:
            # Snapshot Default : "Skateboard 01.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:04:25
            main_page.set_timeline_timecode('00_00_04_25')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Digital Discs')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Digital Discs')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 03')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Digital Discs')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 03')

            # Click play then pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:04:25
            main_page.set_timeline_timecode('00_00_04_25')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.97)
            preview_no_update = main_page.compare(default_preview, current_preview, similarity=0.87)
            case.result = preview_update and preview_no_update

        # [M445] "Digital Discs" > Check Width preview update
        with uuid("009c8cb5-812f-4793-9d74-315d9fa50737") as case:
            # Select timeline clip
            main_page.select_timeline_media('Skateboard 03')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(38, 189)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            width_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(width_preview, current_preview)
            preview_no_update = main_page.compare(width_preview, current_preview, similarity=0.8)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M446] "Digital Discs" > Check Position preview update
        with uuid("c95f0d12-2e5e-466c-bed9-fc6bb6913348") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(186, 31, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            position_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(width_preview, position_preview, similarity=0.9)
            preview_no_update = main_page.compare(width_preview, position_preview, similarity=0.78)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M447] "Digital Discs" > Check Height preview update
        with uuid("d6a53743-ba91-411c-97d3-724d2738b866") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 80, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            height_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(height_preview, position_preview)
            preview_no_update = main_page.compare(height_preview, position_preview, similarity=0.83)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 3 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_6(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M448] Add "Electric energy" > Download Effect
        with uuid("14a34627-c75e-4842-a0d1-96c8ea5e0ace") as case:
            # Snapshot Default : "Skateboard 01.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:06:25
            main_page.set_timeline_timecode('00_00_06_25')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Electric Energy')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Electric Energy')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 03')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Electric Energy')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 03')

            # Click play then pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:06:25
            main_page.set_timeline_timecode('00_00_06_25')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.98)
            preview_no_update = main_page.compare(default_preview, current_preview, similarity=0.9)
            case.result = preview_update and preview_no_update

        # [M450] "Electric energy" > Check Foreground Color preview update
        with uuid("77a577bd-66b0-4127-a869-5314203cfc13") as case:
            # Select timeline clip
            main_page.select_timeline_media('Skateboard 03')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(10, 153, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            foreground_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(foreground_preview, current_preview, similarity=0.9999)
            preview_no_update = main_page.compare(foreground_preview, current_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M449] "Electric energy" > Check Background Color preview update
        with uuid("9d04f71c-df89-483b-85f8-70273d4a6a04") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(10, 115)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            background_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(foreground_preview, background_preview, similarity=0.9999)
            preview_no_update = main_page.compare(foreground_preview, background_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_7(self):
        # clear AI module
        main_page.clear_AI_module()

        # Insert Y man.mp4
        video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:05:19
        main_page.set_timeline_timecode('00_00_05_19')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # [M451] Add "Energy Dots and Stripes" > Download Effect
        with uuid("c261bfc2-8544-482b-97b8-4dd81ad27d20") as case:
            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Energy Dots and Stripes')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Energy Dots and Stripes')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Y man')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Energy Dots and Stripes')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('Y man')

            # Click play then pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.set_timeline_timecode('00_00_00_19')
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:05:19
            main_page.set_timeline_timecode('00_00_05_19')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.98)
            preview_no_update = main_page.compare(default_preview, current_preview, similarity=0.9)
            case.result = preview_update and preview_no_update

        # [M453] "Energy Dots and Stripes" > Check Foreground Color preview update
        with uuid("8c299869-850e-4c52-9b9a-f5526cb05859") as case:
            # Select timeline clip
            main_page.select_timeline_media('Y man')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 99, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            foreground_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(foreground_preview, current_preview, similarity=0.999)
            preview_no_update = main_page.compare(foreground_preview, current_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M453] "Energy Dots and Stripes" > Check Background Color preview update
        with uuid("65cba16e-ccf6-4747-bc4a-0cf70b493751") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(2, 147)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            bg_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(foreground_preview, bg_preview, similarity=1)
            preview_no_update = main_page.compare(foreground_preview, bg_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M455] "Energy Dots and Stripes" > Check Edit Color preview update
        with uuid("7e59f65f-a260-46fc-a034-b2c85781938f") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('0518DA')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            new_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(new_color_preview, bg_preview, similarity=1)
            preview_no_update = main_page.compare(new_color_preview, bg_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M454] "Energy Dots and Stripes" > Check Offset preview update
        with uuid("8aa252c6-6847-42fb-9681-bb44b93cb1fe") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(2, 200, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            offset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(new_color_preview, offset_preview, similarity=1)
            preview_no_update = main_page.compare(new_color_preview, offset_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_8(self):
        # clear AI module
        main_page.clear_AI_module()

        # Insert Y man.mp4
        video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:06:18
        main_page.set_timeline_timecode('00_00_06_18')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # [M456] Add "Energy Swirl" > Download Effect
        with uuid("02a5800a-2fbc-433f-a8ee-b4069655889e") as case:
            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Energy Swirl')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Energy Swirl')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Y man')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Energy Swirl')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('Y man')

            # Click play then pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.set_timeline_timecode('00_00_03_04')
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:06:18
            main_page.set_timeline_timecode('00_00_06_18')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.99)
            preview_no_update = main_page.compare(default_preview, current_preview, similarity=0.9)
            case.result = preview_update and preview_no_update

        # [M461] "Energy Swirl" > Check Position preview update
        with uuid("2e37e6c9-e48f-48bd-94b0-1fb33e2a10fe") as case:
            # Select timeline clip
            main_page.select_timeline_media('Y man')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(26, 142, option=5)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            position_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(position_preview, current_preview, similarity=0.99)
            preview_no_update = main_page.compare(position_preview, current_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M457] "Energy Swirl" > Check Width preview update
        with uuid("6bbc0e8c-2a97-4b43-a3c8-80d625591d57") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(199, 91)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            width_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(position_preview, width_preview, similarity=0.99)
            preview_no_update = main_page.compare(position_preview, width_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M458] "Energy Swirl" > Check Foreground Color preview update
        with uuid("564f38d3-6d5e-4c8f-b779-d2774796ac56") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(5, 141, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            fg_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(fg_preview, width_preview, similarity=1)
            preview_no_update = main_page.compare(fg_preview, width_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M460] "Energy Swirl" > Check Object Color preview update
        with uuid("6cc84edb-f214-4050-8185-e9be10e94011") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(196, 119, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            object_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(fg_preview, object_preview, similarity=0.999)
            preview_no_update = main_page.compare(fg_preview, object_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M459] "Energy Swirl" > Check Height preview update
        with uuid("17364753-dac5-4250-9dbf-457d870f564c") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 64, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            height_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(height_preview, object_preview, similarity=0.999)
            preview_no_update = main_page.compare(height_preview, object_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 4 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_9(self):
        # clear AI module
        main_page.clear_AI_module()

        # Insert Y man.mp4
        video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:03:29
        main_page.set_timeline_timecode('00_00_03_29')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # [M462] Add "Fairy Dust" > Download Effect
        with uuid("0ac40e06-25ff-4159-bb72-30e26415eb38") as case:
            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Fairy Dust')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Fairy Dust')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Y man')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Fairy Dust')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('Y man')

            # Click play then pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.set_timeline_timecode('00_00_01_04')
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:03:29
            main_page.set_timeline_timecode('00_00_03_29')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.99)
            preview_no_update = main_page.compare(default_preview, current_preview, similarity=0.9)
            case.result = preview_update and preview_no_update

        # [M464] "Fairy Dust" > Check Speed preview update
        with uuid("51e3f03b-140e-492e-a460-68c1e080dd3c") as case:
            # Select timeline clip
            main_page.select_timeline_media('Y man')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(6, 153, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(speed_preview, current_preview, similarity=0.995)
            preview_no_update = main_page.compare(speed_preview, current_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M465] "Fairy Dust" > Check Distance preview update
        with uuid("d69e0fad-e9c6-4164-a66a-1dda09577bf7") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            distance_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(speed_preview, distance_preview, similarity=1)
            preview_no_update = main_page.compare(speed_preview, distance_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M463] "Fairy Dust" > Check Background Color preview update
        with uuid("a66feb42-fafe-4f44-982b-b89465d5aff9") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 58)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            bg_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(bg_preview, distance_preview, similarity=0.999)
            preview_no_update = main_page.compare(bg_preview, distance_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 3 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_10(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M467] Add "Fiery Gas" > Download Effect
        with uuid("58da0460-95a5-4f20-be4b-53946448de4b") as case:
            # Snapshot Default : "Skateboard 02.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            time.sleep(DELAY_TIME)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:05:25
            main_page.set_timeline_timecode('00_00_05_25')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Click [Stop] for CTI back to 00:00:00:00
            playback_window_page.Edit_Timeline_PreviewOperation('stop')

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Fiery Gas')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Fiery Gas')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 02')
            # Set timecode 00:00:05:25
            main_page.set_timeline_timecode('00_00_05_25')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.995)
            case.result = not preview_update

        # [M468] "Fiery Gas" > Check Strength preview update
        with uuid("0be3830b-3ce5-4f07-947e-96a2c28334ec") as case:
            # Select timeline clip
            main_page.select_timeline_media('Skateboard 02')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(6, 200)
            logger(adjust_result)

            # close effect setting
            main_page.click(L.tips_area.button.btn_effect_close)

            # Click play then pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 4)
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.set_timeline_timecode('00_00_04_07')
            time.sleep(DELAY_TIME * 2)
            main_page.set_timeline_timecode('00_00_05_25')
            time.sleep(DELAY_TIME * 2)


            strength_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(strength_preview, current_preview, similarity=0.995)
            preview_no_update = main_page.compare(strength_preview, current_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M469] "Fiery Gas" > Check Color preview update
        with uuid("24624677-c2b9-47ea-ab15-a10c18df1483") as case:
            # Select timeline clip
            main_page.select_timeline_media('Skateboard 02')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 88, option=2)
            logger(adjust_result)

            # close effect setting
            main_page.click(L.tips_area.button.btn_effect_close)

            # Click play then pause
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 4)
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.set_timeline_timecode('00_00_03_07')
            time.sleep(DELAY_TIME * 2)
            main_page.set_timeline_timecode('00_00_05_25')
            time.sleep(DELAY_TIME * 2)


            color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(strength_preview, color_preview, similarity=0.995)
            preview_no_update = main_page.compare(strength_preview, color_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_11(self):
        # clear AI module
        main_page.clear_AI_module()

        # Snapshot Default : "Skateboard 02.mp4" Ground truth
        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        time.sleep(DELAY_TIME)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:06:05
        main_page.set_timeline_timecode('00_00_06_05')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # Click [Stop] for CTI back to 00:00:00:00
        playback_window_page.Edit_Timeline_PreviewOperation('stop')

        # [M470] Add "Geometric Light Shadow" > Download Effect
        with uuid("9c86da18-d076-4cd8-b576-61cbfeed93da") as case:
            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Geometric Light Shadow')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Geometric Light Shadow')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 02')
            # Set timecode 00:00:06:05
            main_page.set_timeline_timecode('00_00_06_05')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(current_preview, default_preview, similarity=0.995)
            preview_no_update = main_page.compare(current_preview, default_preview)
            logger(preview_update)
            case.result = preview_update and preview_no_update

        # [M471] "Geometric Light Shadow" > Check Background Color  preview update
        with uuid("a05aca82-649d-4581-9912-b09fb6dea21e") as case:
            # Select timeline clip
            main_page.select_timeline_media('Skateboard 02')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 73)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            bg_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(bg_preview, current_preview, similarity=1)
            preview_no_update = main_page.compare(bg_preview, current_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M472] "Geometric Light Shadow" > Check Clone Count preview update
        with uuid("d28593d7-04c4-4b35-8505-071c793ba805") as case:
            # Set timecode 00:00:03:02
            main_page.set_timeline_timecode('00_00_03_02')
            time.sleep(DELAY_TIME * 2)

            count_2_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(1, 4, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            count_4_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(count_2_preview, count_4_preview, similarity=0.993)
            preview_no_update = main_page.compare(count_2_preview, count_4_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M473] "Geometric Light Shadow" > Check Distance preview update
        with uuid("41bfb75f-5106-4363-936d-afc59ed617b6") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 0, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            distance_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(distance_preview, count_4_preview)
            preview_no_update = main_page.compare(distance_preview, count_4_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M474] "Geometric Light Shadow" > Check Direction preview update
        with uuid("a1e30265-1c93-40f3-acd8-6da7a6901f4f") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            direction_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(distance_preview, direction_preview)
            preview_no_update = main_page.compare(distance_preview, direction_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_12(self):
        # clear AI module
        main_page.clear_AI_module()

        # Snapshot Default : "Skateboard 02.mp4" Ground truth
        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        time.sleep(DELAY_TIME)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:01:09
        main_page.set_timeline_timecode('00_00_01_09')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # Click [Stop] for CTI back to 00:00:00:00
        playback_window_page.Edit_Timeline_PreviewOperation('stop')

        # [M476] Add "Glam Light Body Shadow" > Download Effect
        with uuid("e93dbffa-6a65-4c99-9ae5-591b213332ff") as case:
            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Glam Light Body Shadow')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Glam Light Body Shadow')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 02')
            # Set timecode 00:00:01:09
            main_page.set_timeline_timecode('00_00_01_09')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(current_preview, default_preview, similarity=0.96)
            preview_no_update = main_page.compare(current_preview, default_preview, similarity=0.9)
            logger(preview_update)
            case.result = preview_update and preview_no_update

        # [M477] "Glam Light Body Shadow" > Check Background size preview update
        with uuid("3c0ad682-7ffc-4934-a9e1-d88fc4c7a06c") as case:
            # Select timeline clip
            main_page.select_timeline_media('Skateboard 02')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, current_preview, similarity=0.999)
            preview_no_update = main_page.compare(size_preview, current_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M479] "Glam Light Body Shadow" > Check Background color preview update
        with uuid("6e2f83cd-2230-450f-bc6c-25c0fb4ece47") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(167, 64, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, color_preview, similarity=0.999)
            preview_no_update = main_page.compare(size_preview, color_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M478] "Glam Light Body Shadow" > Check Size preview update
        with uuid("c025cecb-ec73-4bf0-ac11-9355b7f93daa") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            leg_size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(leg_size_preview, color_preview, similarity=0.99)
            preview_no_update = main_page.compare(leg_size_preview, color_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M480] "Glam Light Body Shadow" > Check Clone Count  preview update
        with uuid("606a6567-ac9f-4f56-bfef-dcfb8af05cec") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 4, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            count_4_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(leg_size_preview, count_4_preview, similarity=0.99)
            preview_no_update = main_page.compare(leg_size_preview, count_4_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M482] "Glam Light Body Shadow" > Check Distance preview update
        with uuid("201da897-774c-40a9-9f65-d3598d0c4255") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=6)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            distance_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(distance_preview, count_4_preview, similarity=0.99)
            preview_no_update = main_page.compare(distance_preview, count_4_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M483] "Glam Light Body Shadow" > Check Speed preview update
        with uuid("ac6845c0-9fa1-4707-bd50-5739bdaa1c37") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(194, 75, option=7)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(distance_preview, speed_preview, similarity=0.999)
            preview_no_update = main_page.compare(distance_preview, speed_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M481] "Glam Light Body Shadow" > Check Opacity preview update
        with uuid("c0f530fa-7c45-4638-87f9-3be38616a00a") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 14, option=5)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            opacity_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(opacity_preview, speed_preview, similarity=0.96)
            preview_no_update = main_page.compare(opacity_preview, speed_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    #  uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_13(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M484] Add "Heart Lights" > Download Effect
        with uuid("6836b6a7-c911-47d7-bc95-e33bd9702108") as case:
            # Insert Y man.mp4
            video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Set timecode 00:00:01:23
            main_page.set_timeline_timecode('00_00_01_23')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Heart Lights')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Heart Lights')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Y man')
            # Set timecode 00:00:01:23
            main_page.set_timeline_timecode('00_00_01_23')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(current_preview, default_preview, similarity=0.99)
            preview_no_update = main_page.compare(current_preview, default_preview)
            logger(preview_update)
            case.result = preview_update and preview_no_update

        # [M485] "Heart Lights" > Check Background color preview update
        with uuid("1764fa40-1a9d-4e6c-a48b-6cbffb94003a") as case:
            # Select timeline clip
            main_page.select_timeline_media('Y man')

            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(28, 128)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            bg_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(bg_preview, current_preview, similarity=0.999)
            preview_no_update = main_page.compare(bg_preview, current_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M486] "Heart Lights" > Check Edge color preview update
        with uuid("07809ee4-78b7-4d49-bb76-21fbd31fb2b4") as case:
            # Set timecode 00:00:07:09
            main_page.set_timeline_timecode('00_00_07_09')
            time.sleep(DELAY_TIME * 2)

            org_edge_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('35FB11')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            green_edge_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(org_edge_color_preview, green_edge_color_preview, similarity=1)
            preview_no_update = main_page.compare(org_edge_color_preview, green_edge_color_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 4 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_14(self):
        # clear AI module
        main_page.clear_AI_module()

        # Insert skateboard_girl.mp4
        video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # [M487] Add "Heart Star Glow" > Download Effect
        with uuid("7abbe120-ad72-480b-8a19-9492afe4dde7") as case:
            # Set timecode 00:00:00:17
            main_page.set_timeline_timecode('00_00_00_17')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Heart Star Glow')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Heart Star Glow')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('skateboard_girl')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.999)
            preview_no_update = main_page.compare(default_preview, current_preview, similarity=0.93)
            case.result = preview_update and preview_no_update

        # [M490] "Heart Star Glow" > Check Color preview update
        with uuid("b1657574-1c88-4fc5-90f7-984034d9b22d") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('07E580')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            green_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, green_color_preview, similarity=1)
            preview_no_update = main_page.compare(current_preview, green_color_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M488] "Heart Star Glow" > Check Foreground color preview update
        with uuid("6326ecbf-1dc4-4705-aeef-95bef36c97fe") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(12, 155)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            fc_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(green_color_preview, fc_preview, similarity=1)
            preview_no_update = main_page.compare(green_color_preview, fc_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M489] "Heart Star Glow" > Check Opacity preview update
        with uuid("4b2db947-61c3-4076-99ce-20560a0feff8") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(100, 9, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            opacity_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(opacity_preview, fc_preview, similarity=1)
            preview_no_update = main_page.compare(opacity_preview, fc_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_15(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M491] Add "Hero Glow" > Download Effect
        with uuid("43a90b49-3295-4f12-8abd-1d8088590c3b") as case:
            # Snapshot Default : "Skateboard 03.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:07:12
            main_page.set_timeline_timecode('00_00_07_12')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Hero Glow')
            time.sleep(DELAY_TIME * 4)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Hero Glow')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')
            time.sleep(DELAY_TIME * 4)

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 03')
            # Set timecode 00:00:07:12
            main_page.set_timeline_timecode('00_00_07_12')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.99)
            preview_no_update = main_page.compare(default_preview, current_preview, similarity=0.97)

            case.result = preview_update and preview_no_update

        # [M495] "Hero Glow" > Check Light Color preview update
        with uuid("3302370d-261c-433d-b78c-e63d3d1a7eb9") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('C408F4')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            light_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, light_color_preview, similarity=0.9999)
            preview_no_update = main_page.compare(current_preview, light_color_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M492] "Hero Glow" > Check Light Strength preview update
        with uuid("cd4fcbb3-047c-4922-bd34-bbd1fd39280e") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 0)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            strength_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            preview_no_update = main_page.compare(default_preview, strength_preview, similarity=0.99)
            logger(preview_no_update)
            case.result = adjust_result and preview_no_update

        # [M493] "Hero Glow" > Check X offset preview update
        with uuid("3bf6af44-94df-453b-a947-d51bf1610120") as case:
            # click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(194, 67, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            x_offset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            preview_update = not main_page.compare(x_offset_preview, light_color_preview, similarity=0.9999)
            preview_no_update = main_page.compare(x_offset_preview, light_color_preview, similarity=0.97)
            logger(preview_no_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M494] "Hero Glow" > Check Y offset preview update
        with uuid("72134b47-542c-442b-9232-a0348a1db62e") as case:
            # click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(14, 200, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            y_offset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            preview_update = not main_page.compare(x_offset_preview, y_offset_preview, similarity=0.9995)
            preview_no_update = main_page.compare(x_offset_preview, y_offset_preview, similarity=0.97)
            logger(preview_no_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_16(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M496] Add "Light Bubbles" > Download Effect
        with uuid("7efcee64-1426-4f13-89ce-920ee82fbd09") as case:
            # Insert skateboard_girl.mp4
            video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:04:11
            main_page.set_timeline_timecode('00_00_04_11')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()
            time.sleep(DELAY_TIME * 2)

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Light Bubbles')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Light Bubbles')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Light Bubbles')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')

            # Set timecode 00:00:04:11
            main_page.set_timeline_timecode('00_00_04_11')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = main_page.compare(default_preview, current_preview, similarity=0.999)
            case.result = not preview_update

        # [M497] "Light Bubbles" > Check Width preview update
        with uuid("8a33d571-89df-4130-835f-beea8e1d009c") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(31, 184)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            width_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, width_preview)
            preview_no_update = main_page.compare(current_preview, width_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M502] "Light Bubbles" > Check Edge Color preview update
        with uuid("3985c768-f7bb-486c-91d2-e53ffe6c5c3f") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('3BFF63')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            edge_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(width_preview, edge_color_preview, similarity=1)
            preview_no_update = main_page.compare(width_preview, edge_color_preview, similarity=0.98)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M498] "Light Bubbles" > Check Background Color preview update
        with uuid("a8964f79-b88c-4031-bf72-b033deb58545") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(13, 144, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            bg_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(edge_color_preview, bg_preview, similarity=1)
            preview_no_update = main_page.compare(edge_color_preview, bg_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M500] "Light Bubbles" > Check Object Color preview update
        with uuid("ddcbfcd2-ac99-490d-be12-0adc3aca7149") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(15, 101, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            object_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(object_preview, bg_preview, similarity=0.99999)
            preview_no_update = main_page.compare(object_preview, bg_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M501] "Light Bubbles" > Check Position preview update
        with uuid("7202aed6-13aa-41ea-821e-9cf9e0fc0afd") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(15, 172, option=5)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            pos_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(object_preview, pos_preview)
            preview_no_update = main_page.compare(object_preview, pos_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M499] "Light Bubbles" > Check Height preview update
        with uuid("1fa5ceb4-bc98-44d1-922a-55d6c942fb91") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(195, 65, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            height_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(height_preview, pos_preview, similarity=0.993)
            preview_no_update = main_page.compare(height_preview, pos_preview, similarity=0.96)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M503] "Light Bubbles" > Check Opacity preview update
        with uuid("c5492d7e-37d8-42ab-92a0-7be4ba392727") as case:
            # click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(100, 0, option=6)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            opacity_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(pos_preview, opacity_preview, similarity=0.99999)
            preview_no_update = main_page.compare(pos_preview, opacity_preview, similarity=0.96)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    #  uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_17(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M504] Add "Lights, Camera, Action" > Download Effect
        with uuid("c1cc9434-80f9-4a42-b51a-42826453dae9") as case:
            # Snapshot Default : "Skateboard 01.mp4" Ground truth
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)

            # Set timecode 00:00:04:12
            main_page.set_timeline_timecode('00_00_04_12')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Lights, Camera, Action')
            time.sleep(DELAY_TIME * 4)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Lights, Camera, Action')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')
            time.sleep(DELAY_TIME * 4)

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 01')
            # Set timecode 00:00:04:12
            main_page.set_timeline_timecode('00_00_04_12')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview)
            preview_no_update = main_page.compare(default_preview, current_preview, similarity=0.9)
            logger(preview_update)
            case.result = result and preview_update and preview_no_update

        # [M505] "Lights, Camera, Action" > Check Size preview update
        with uuid("5bca56ce-5c8a-4643-bbaa-e77d2470c239") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(10, 195)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, size_preview)
            preview_no_update = main_page.compare(current_preview, size_preview, similarity=0.9)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M506] "Lights, Camera, Action" > Check Speed preview update
        with uuid("ce7cf952-1dfd-497a-975a-13fe0a1ee410") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(10, 156, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(speed_preview, size_preview)
            preview_no_update = main_page.compare(speed_preview, size_preview, similarity=0.89)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M507] "Lights, Camera, Action" > Check Background Color preview update
        with uuid("127f3ce6-6a57-4203-86b2-0ceefcefbd2c") as case:
            # click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(22, 106, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            bg_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(speed_preview, bg_preview)
            preview_no_update = main_page.compare(speed_preview, bg_preview, similarity=0.87)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_18(self):
        # clear AI module
        main_page.clear_AI_module()

        # [M508] Add "Light Waves" > Download Effect
        with uuid("fe315507-c398-4cf4-81af-ea60aa4ac1e8") as case:
            # Insert skateboard_girl.mp4
            video_path = Test_Material_Folder + 'BFT_21_Stage1/skateboard_girl.mp4'
            media_room_page.import_media_file(video_path)
            media_room_page.handle_high_definition_dialog()
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:03:23
            main_page.set_timeline_timecode('00_00_03_23')
            time.sleep(DELAY_TIME * 2)
            default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(default_preview)

            # Insert to timeline track
            main_page.tips_area_insert_media_to_selected_track()

            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Light Waves')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Light Waves')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('skateboard_girl')
            # Set timecode 00:00:03:23
            main_page.set_timeline_timecode('00_00_03_23')
            time.sleep(DELAY_TIME * 2)

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.99)
            preview_no_update = main_page.compare(default_preview, current_preview, similarity=0.94)
            case.result = preview_update and preview_no_update

        # [M509] "Light Waves" > Check Size preview update
        with uuid("b337c290-ae05-4f14-aa95-44653f33376f") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, size_preview, similarity=0.99)
            preview_no_update = main_page.compare(current_preview, size_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M510] "Light Waves" > Check Edge Size preview update
        with uuid("812de65c-0aab-48b6-b746-b298f3f37a0d") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(0, 200, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            edge_size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(edge_size_preview, size_preview, similarity=0.99)
            preview_no_update = main_page.compare(edge_size_preview, size_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M511] "Light Waves" > Check Background Color preview update
        with uuid("064dec74-c667-4da6-b6e2-9d748e233ee0") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(12, 157, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            bg_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(edge_size_preview, bg_preview, similarity=0.9995)
            preview_no_update = main_page.compare(edge_size_preview, bg_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M512] "Light Waves" > Check Offset preview update
        with uuid("4424e0f0-2a65-48c1-b5c2-64a5e606930d") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(1, 200, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            offset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, bg_preview, similarity=0.9995)
            preview_no_update = main_page.compare(offset_preview, bg_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M514] "Light Waves" > Check Color preview update
        with uuid("fca3de4b-1e38-4d3b-9f85-ba723dd8e618") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('FFFB35')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, color_preview, similarity=0.999999)
            preview_no_update = main_page.compare(offset_preview, color_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M515] "Light Waves" > Check Opacity preview update
        with uuid("c662daa2-fc1a-4f5a-a55c-8b6a3f147b97") as case:
            # click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 0, option=6)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            opacity_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(opacity_preview, offset_preview, similarity=0.995)
            preview_no_update = main_page.compare(opacity_preview, offset_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M513] "Light Waves" > Check Speed preview update
        with uuid("318ad0ca-ddec-40c3-a581-b1f9109b5ed8") as case:
            # click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(20, 154, option=5)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(speed_preview, offset_preview, similarity=0.97)
            preview_no_update = main_page.compare(speed_preview, offset_preview, similarity=0.93)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_19(self):
        # clear AI module
        main_page.clear_AI_module()

        # Insert Skateboard 01.mp4 to timeline
        main_page.select_library_icon_view_media('Skateboard 01.mp4')
        time.sleep(DELAY_TIME)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:03:11
        main_page.set_timeline_timecode('00_00_03_11')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # [M516] Add "Star Shower" > Download Effect
        with uuid("9b4ec68d-f495-479d-8a4e-0b5750a0e05a") as case:
            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Star Shower')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Star Shower')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 01')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Star Shower')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('Skateboard 01')


            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.986)
            preview_no_update = main_page.compare(default_preview, current_preview)
            case.result = preview_update and preview_no_update

        # [M522] "Star Shower" > Check Edge Color preview update
        with uuid("cd322000-98ea-4ba9-b403-dad4d4174019") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('FF0B00')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            edge_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, edge_color_preview, similarity=0.9993)
            preview_no_update = main_page.compare(current_preview, edge_color_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M517] "Star Shower" > Check Size preview update
        with uuid("307ae99f-5470-428f-a5c4-a2aca19144a0") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(2, 200)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            size_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, edge_color_preview, similarity=0.99)
            preview_no_update = main_page.compare(size_preview, edge_color_preview, similarity=0.93)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M518] "Star Shower" > Check Opacity preview update
        with uuid("51b53d43-013e-4e23-a0f8-fa347726199c") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(195, 0, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            opacity_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, opacity_preview, similarity=0.9999)
            preview_no_update = main_page.compare(size_preview, opacity_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M519] "Star Shower" > Check Background Color preview update
        with uuid("ee638f85-d4b1-48c5-8fc4-66a6864a9bd7") as case:
            # click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(29, 145, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            bg_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(size_preview, bg_preview, similarity=0.9999)
            preview_no_update = main_page.compare(size_preview, bg_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M520] "Star Shower" > Check Glow Size preview update
        with uuid("4749b56d-bac1-46ff-9e7b-831e54d69d98") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(198, 0, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            glow_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(glow_preview, bg_preview, similarity=0.9994)
            preview_no_update = main_page.compare(glow_preview, bg_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update


        # [M521] "Star Shower" > Check Speed preview update
        with uuid("29b23d6d-2c85-4f10-a276-757f8af751aa") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(8, 179, option=5)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            speed_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(glow_preview, speed_preview, similarity=0.999)
            preview_no_update = main_page.compare(glow_preview, speed_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 3 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_20(self):
        # clear AI module
        main_page.clear_AI_module()

        # Insert Y man.mp4
        video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:07:00
        main_page.set_timeline_timecode('00_00_07_00')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # [M523] Add "Splashy Paint" > Download Effect
        with uuid("ee662174-979d-4dfb-96d4-ed39b195de4b") as case:
            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Splashy Paint')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Splashy Paint')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Y man')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Splashy Paint')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('Y man')

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.99)
            preview_no_update = main_page.compare(default_preview, current_preview)
            case.result = preview_update and preview_no_update

        # [M524] "Splashy Paint" > Check Scale Ratio preview update
        with uuid("40f92578-82ca-40cc-82ad-4b1e788c122d") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(38, 146)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            scale_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, scale_preview, similarity=0.99)
            preview_no_update = main_page.compare(current_preview, scale_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M525] "Splashy Paint" > Check Object Color preview update
        with uuid("278b230c-72b4-4c89-998c-0c49d1636f30") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(180, 86, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            object_color_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(object_color_preview, scale_preview, similarity=0.997)
            preview_no_update = main_page.compare(object_color_preview, scale_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 4 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_21(self):
        # clear AI module
        main_page.clear_AI_module()

        # Insert Y man.mp4
        video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:03:22
        main_page.set_timeline_timecode('00_00_03_22')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # [M526] Add "Super Star Power" > Download Effect
        with uuid("099b1755-8a4b-408f-a60d-9f205bcd241c") as case:
            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Super Star Power')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Super Star Power')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Y man')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Super Star Power')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('Y man')

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview)
            preview_no_update = main_page.compare(default_preview, current_preview, similarity=0.89)
            case.result = preview_update and preview_no_update

        # [M527] "Super Star Power" > Check Background Color preview update
        with uuid("0b6243dc-a460-4005-abca-6284f89fe465") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(15, 161)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            bg_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, bg_preview, similarity=0.99)
            preview_no_update = main_page.compare(current_preview, bg_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M528] "Super Star Power" > Check Edge Color preview update
        with uuid("5176c884-f8ed-4070-874d-2135077cf4f5") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_BG_color('1B56DA')
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            edge_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(edge_preview, bg_preview, similarity=0.99999)
            preview_no_update = main_page.compare(edge_preview, bg_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M529] "Super Star Power" > Check Offset preview update
        with uuid("5011e7d2-7594-44d8-8536-7f5efe627490") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(1, 200, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            offset_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(offset_preview, edge_preview, similarity=0.997)
            preview_no_update = main_page.compare(offset_preview, edge_preview)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_5_22(self):
        # clear AI module
        main_page.clear_AI_module()

        # Insert Y man.mp4
        video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:06:26
        main_page.set_timeline_timecode('00_00_06_26')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # [M530] Add "Wind Slash" > Download Effect
        with uuid("720b4630-1f74-475e-b4e4-297be90ab804") as case:
            # Enter Effect Room > Body Effect category
            self.enter_body_effect()

            # Search Effect
            media_room_page.search_library('Wind Slash')
            time.sleep(DELAY_TIME * 2)

            # Select  effect to insert video track
            self.apply_effect_to_timeline_clip('Wind Slash')

            result = self.check_download_body_effect()
            logger(f'check download result : {result}')

            # Select timeline clip
            main_page.select_timeline_media('Y man')
            check_not_ok = self.check_body_effect_apply_not_ok()
            # Select  effect to insert video track again
            if check_not_ok:
                self.apply_effect_to_timeline_clip('Wind Slash')
                time.sleep(DELAY_TIME * 2)

            # Select timeline clip
            main_page.select_timeline_media('Y man')

            current_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
            logger(current_preview)

            preview_update = not main_page.compare(default_preview, current_preview, similarity=0.993)
            preview_no_update = main_page.compare(default_preview, current_preview, similarity=0.98)
            case.result = preview_update and preview_no_update

        # [M531] "Wind Slash" > Check Width preview update
        with uuid("e8ad6231-74e5-4477-a139-d41ae59844e9") as case:
            # Click [Effect] button
            tips_area_page.click_TipsArea_btn_effect()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(15, 161)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            width_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(current_preview, width_preview, similarity=0.97)
            preview_no_update = main_page.compare(current_preview, width_preview, similarity=0.93)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M532] "Wind Slash" > Check Position preview update
        with uuid("b59fd1ad-65e5-42f1-b96e-6be359899ede") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(200, 24, option=2)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            position_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(position_preview, width_preview)
            preview_no_update = main_page.compare(position_preview, width_preview, similarity=0.88)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M534] "Wind Slash" > Check Foreground Color preview update
        with uuid("c95a1a5f-05b3-463e-b03f-66c0799e6973") as case:
            # click undo
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(10, 125, option=4)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            fc_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(width_preview, fc_preview, similarity=0.99999)
            preview_no_update = main_page.compare(width_preview, fc_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M535] "Wind Slash" > Check Object Color  preview update
        with uuid("5f0dce34-2f14-408e-a4f4-db128d23d499") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(42, 99, option=5)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            object_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(object_preview, fc_preview, similarity=0.99999)
            preview_no_update = main_page.compare(object_preview, fc_preview, similarity=0.97)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update

        # [M533] "Wind Slash" > Check Height  preview update
        with uuid("3348ac4e-e99d-47dc-a9cf-1ff86c5c0304") as case:
            # Adjust parameter
            adjust_result = effect_settings_page.body_effect.adjust_1st_slider(192, 26, option=3)
            logger(adjust_result)
            time.sleep(DELAY_TIME * 2)

            height_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)

            preview_update = not main_page.compare(object_preview, height_preview, similarity=0.97)
            preview_no_update = main_page.compare(object_preview, height_preview, similarity=0.92)
            logger(preview_update)
            case.result = adjust_result and preview_update and preview_no_update
