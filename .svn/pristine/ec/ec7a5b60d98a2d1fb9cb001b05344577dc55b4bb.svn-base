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
mask_designer_page = PageFactory().get_page_object('mask_designer_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page', mwc)
effect_room_page = PageFactory().get_page_object('effect_room_page', mwc)
transition_room_page = PageFactory().get_page_object('transition_room_page', mwc)
title_designer_page = PageFactory().get_page_object('title_designer_page', mwc)
timeline_page = PageFactory().get_page_object('timeline_operation_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)
preferences_page = PageFactory().get_page_object('preferences_page', mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page', mwc)
fix_enhance_page = PageFactory().get_page_object('fix_enhance_page', mwc)
pip_designer_page = PageFactory().get_page_object('pip_designer_page', mwc)
crop_zoom_pan_page = PageFactory().get_page_object('crop_zoom_pan_page', mwc)
pan_zoom_page = PageFactory().get_page_object('pan_zoom_page', mwc)
video_speed_page = PageFactory().get_page_object('video_speed_page', mwc)
blending_mode_page = PageFactory().get_page_object('blending_mode_page', mwc)

# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Render Preview.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Render_Preview/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Render_Preview/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Render_Preview():
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
            google_sheet_execution_log_init('Render_Preview')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"Motion Graphics Title result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        # case 1~6
        # render preview for sample video
        with uuid("6a3f9bba-4f39-4c26-97d2-959130774a6f") as case:
            # render default 30p
            with uuid("7afa44fc-48c0-491b-b1e4-9caac0e18435") as case:
                time.sleep(3)
                main_page.insert_media('Skateboard 01.mp4')
                timeline_page.edit_timeline_render_preview()
                main_page.set_timeline_timecode('00_00_05_00')
                time.sleep(5)
                current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                         file_name=Auto_Ground_Truth_Folder + 'Render_video.png')
                compare_result = title_room_page.compare(Ground_Truth_Folder + 'Render_video.png', current_image)
                case.result = compare_result
            case.result = compare_result

        with uuid("2f7d5fd1-a93a-4bad-bd20-ef7dbe6a45bc") as case:
            # render 24p
            time.sleep(2)
            main_page.set_timeline_timecode('00_00_00_00')
            main_page.click_set_user_preferences()
            time.sleep(1)
            preferences_page.general.timeline_frame_rate_set_24_fps()
            preferences_page.click_ok()
            timeline_page.edit_timeline_render_preview()
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0, file_name=Auto_Ground_Truth_Folder + 'Render_24p.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_24p.png', current_image)
            case.result = compare_result

        with uuid("51dc5976-93c9-471e-938f-56b8d29f5eec") as case:
            # render 25p
            time.sleep(2)
            main_page.click_set_user_preferences()
            time.sleep(1)
            preferences_page.general.timeline_frame_rate_set_25_fps()
            preferences_page.click_ok()
            timeline_page.edit_timeline_render_preview()
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0, file_name=Auto_Ground_Truth_Folder + 'Render_25p.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_25p.png', current_image)
            case.result = compare_result

        with uuid("aa9cca85-ff4a-4e6d-9925-7501a13fb0fe") as case:
            # render 50p
            time.sleep(2)
            main_page.click_set_user_preferences()
            time.sleep(1)
            preferences_page.general.timeline_frame_rate_set_50_fps()
            preferences_page.click_ok()
            timeline_page.edit_timeline_render_preview()
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_50p.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_50p.png', current_image)
            case.result = compare_result

        with uuid("1569e777-9837-4217-a26c-fabe8abaaabb") as case:
            # render 60p
            time.sleep(2)
            main_page.click_set_user_preferences()
            time.sleep(1)
            preferences_page.general.timeline_frame_rate_set_60_fps()
            preferences_page.click_ok()
            timeline_page.edit_timeline_render_preview()
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_60p.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_60p.png', current_image)
            case.result = compare_result

    @exception_screenshot
    def test_1_1_2(self):
        # case 7 ~ 12
        with uuid("8f51f5c6-e8a4-4d45-a0f5-d8fd272a6ec8") as case:
            # render sample image
            time.sleep(3)
            main_page.insert_media('Landscape 01.jpg')
            timeline_page.edit_timeline_render_preview()
            main_page.set_timeline_timecode('00_00_02_00')
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_image.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_image.png', current_image)
            case.result = compare_result

        with uuid("30f0d982-9da7-4d6a-a68a-ea3cdc05c923") as case:
            # render pip
            time.sleep(1)
            timeline_page.press_del_key()
            main_page.tap_PiPRoom_hotkey()
            pip_room_page.select_specific_tag('Romance')
            tips_area_page.click_TipsArea_btn_insert(-1)
            timeline_page.edit_timeline_render_preview()
            main_page.set_timeline_timecode('00_00_02_00')
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Render_pip.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Render_pip.png', current_image)
            case.result = compare_result

        with uuid("74f953b6-a290-4a7e-a00b-1272a1de7c2b") as case:
            # render particle
            time.sleep(1)
            timeline_page.press_del_key()
            main_page.tap_ParticleRoom_hotkey()
            main_page.select_library_icon_view_media('Effect-A')
            tips_area_page.click_TipsArea_btn_insert(-1)
            timeline_page.edit_timeline_render_preview()
            main_page.set_timeline_timecode('00_00_02_00')
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Render_particle.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Render_particle.png', current_image)
            case.result = compare_result

        with uuid("f72acc9e-f5b9-46ef-9e29-722e146724be") as case:
            # render title
            time.sleep(1)
            timeline_page.press_del_key()
            main_page.tap_TitleRoom_hotkey()
            title_room_page.select_specific_tag('General')
            main_page.select_library_icon_view_media('Clover_03')
            tips_area_page.click_TipsArea_btn_insert(-1)
            main_page.set_timeline_timecode('00_00_05_00')
            timeline_page.edit_timeline_render_preview()
            time.sleep(15)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Render_title.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Render_title.png', current_image)
            case.result = compare_result

        with uuid("6f15014e-01b8-4edf-a8ea-33e0cb47633e") as case:
            # render effect
            time.sleep(1)
            timeline_page.press_del_key()
            main_page.tap_EffectRoom_hotkey()
            effect_room_page.right_click_addto_timeline('Back Light')
            timeline_page.edit_timeline_render_preview()
            timeline_page.drag_timeline_vertical_scroll_bar(1)
            time.sleep(8)
            current_image = timeline_page.snapshot_timeline_render_clip(6, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_effect.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_effect.png', current_image)
            case.result = compare_result

        with uuid("6ab47063-303f-409a-b150-0051636ddd1e") as case:
            time.sleep(1)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            main_page.tap_MediaRoom_hotkey()
            media_room_page.media_filter_display_image_only()
            media_room_page.library_menu_select_all()
            tips_area_page.click_TipsArea_btn_insert(-1)
            main_page.tap_TransitionRoom_hotkey()
            transition_room_page.select_specific_tag('Distortion')
            main_page.drag_transition_to_timeline_clip('Laser', 'Landscape 01')
            transition_room_page.select_specific_tag('Glitch')
            transition_room_page.drag_TransitionRoom_Scroll_Bar(1)
            time.sleep(2)
            main_page.drag_transition_to_timeline_clip('Noise', 'Landscape 02')
            transition_room_page.select_specific_tag('Geometric')
            main_page.drag_transition_to_timeline_clip('Fade 1', 'Sport 01')
            transition_room_page.select_specific_tag('All Content')
            time.sleep(2)
            transition_room_page.search_Transition_room_library('Binary 2')
            main_page.drag_transition_to_timeline_clip('Binary 2', 'Sport 02')
            timeline_page.select_timeline_media(track_index=0, clip_index=0)
            timeline_page.edit_timeline_render_preview()
            time.sleep(15)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_1st_tansi.png')
            compare_result_1 = timeline_page.compare(Ground_Truth_Folder + 'Render_1st_tansi.png', current_image)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 1,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_2nd_tansi.png')
            compare_result_2 = timeline_page.compare(Ground_Truth_Folder + 'Render_2nd_tansi.png', current_image)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 2,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_3rd_tansi.png')
            compare_result_3 = timeline_page.compare(Ground_Truth_Folder + 'Render_3rd_tansi.png', current_image)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 3,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_4th_tansi.png')
            compare_result_4 = timeline_page.compare(Ground_Truth_Folder + 'Render_4th_tansi.png', current_image)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 4,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_5th_tansi.png')
            compare_result_5 = timeline_page.compare(Ground_Truth_Folder + 'Render_5th_tansi.png', current_image)

            case.result = compare_result_1 and compare_result_2 and compare_result_3 and compare_result_4 and compare_result_5

    @exception_screenshot
    def test_1_1_3(self):
        # no shadow, case 13 ~ 20
        with uuid("dded4e45-3f54-4207-9a8d-f89ab9a33c92") as case:
            # duplicate clip should also mark as render
            with uuid("74ed26b1-934c-49a9-aa0e-c18e0d6c0aa6") as case:
                time.sleep(3)
                main_page.insert_media('Skateboard 01.mp4')
                timeline_page.edit_timeline_render_preview()
                time.sleep(3)
                main_page.select_library_icon_view_media('Skateboard 01.mp4')
                tips_area_page.click_TipsArea_btn_insert(1)
                time.sleep(1)
                current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                            file_name=Auto_Ground_Truth_Folder + 'Video_duplicate.png')
                compare_result = timeline_page.compare(Ground_Truth_Folder + 'Video_duplicate.png', current_image)
                case.result = compare_result
            case.result = compare_result

        with uuid("3c1ca219-af7e-4d61-b3bf-5bd3060cdbbd") as case:
        # Default HD preview quality
            with uuid("297fcce8-0086-4088-88d1-93ffbcc27ddb") as case:
            # enable shadow 1280x720
                time.sleep(2)
                main_page.tap_NewWorkspace_hotkey()
                main_page.press_esc_key()
                time.sleep(1)
                main_page.click_set_user_preferences()
                preferences_page.general.enable_shadow_file_set_check(1)
                preferences_page.click_ok()
                time.sleep(30)
                main_page.insert_media('Skateboard 02.mp4')
                timeline_page.edit_timeline_render_preview()
                time.sleep(2)
                current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                    file_name=Auto_Ground_Truth_Folder + 'Video_720p.png')
                compare_result = timeline_page.compare(Ground_Truth_Folder + 'Video_720p.png', current_image)
                case.result = compare_result
            case.result = compare_result

        with uuid("ea5a3c73-6b96-4eb9-ac38-af35e24bacc8") as case:
        # set shadow to 720x480
            time.sleep(2)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            time.sleep(1)
            main_page.click_set_user_preferences()
            preferences_page.general.shadow_file_apply_resolution(1)
            preferences_page.click_ok()
            time.sleep(30)
            main_page.insert_media('Skateboard 02.mp4')
            timeline_page.edit_timeline_render_preview()
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                    file_name=Auto_Ground_Truth_Folder + 'Video_480p.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Video_480p.png', current_image)
            case.result = compare_result

        with uuid("8dbf6e2a-e041-4c02-984d-48cc18c8bbe8") as case:
        # set shadow to 1920x1080
            time.sleep(2)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            time.sleep(1)
            main_page.click_set_user_preferences()
            preferences_page.general.shadow_file_apply_resolution(3)
            preferences_page.click_ok()
            time.sleep(30)
            main_page.insert_media('Skateboard 03.mp4')
            timeline_page.edit_timeline_render_preview()
            time.sleep(3)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                    file_name=Auto_Ground_Truth_Folder + 'Video_1080p.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Video_1080p.png', current_image)
            case.result = compare_result

        with uuid("9305bfc4-fd97-4e9e-8fb5-095545ec3f3b") as case:
        # set low preview quality
            time.sleep(2)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            time.sleep(1)
            main_page.click_set_user_preferences()
            preferences_page.general.enable_shadow_file_set_check(0)
            preferences_page.click_ok()
            main_page.insert_media('Skateboard 02.mp4')
            playback_window_page.Edit_TimelinePreview_SetPreviewQuality('Low')
            timeline_page.edit_timeline_render_preview()
            main_page.set_timeline_timecode('00_00_05_00')
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                    file_name=Auto_Ground_Truth_Folder + 'Render_Low.png')
            compare_result_1 = timeline_page.compare(Ground_Truth_Folder + 'Render_Low.png', current_image)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                 file_name=Auto_Ground_Truth_Folder + 'Preview_Low.png')
            compare_result_2 = title_room_page.compare(Ground_Truth_Folder + 'Preview_Low.png', current_image)
            case.result = compare_result_1 and compare_result_2

        with uuid("75e4ba82-b8c9-42a8-a271-d10c796d2f72") as case:
        # set Normal preview quality
            time.sleep(2)
            main_page.set_timeline_timecode('00_00_00_00')
            playback_window_page.Edit_TimelinePreview_SetPreviewQuality('Normal')
            timeline_page.edit_timeline_render_preview()
            main_page.set_timeline_timecode('00_00_05_00')
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                    file_name=Auto_Ground_Truth_Folder + 'Render_Normal.png')
            compare_result_1 = timeline_page.compare(Ground_Truth_Folder + 'Render_Normal.png', current_image)
            case.result = compare_result_1 and compare_result_2

    @exception_screenshot
    def test_1_1_4(self):
        # Render for High preview quality. case 21~30
        with uuid("e3df050e-76c0-4fb0-af70-c4d1c0480192") as case:
            time.sleep(3)
            main_page.insert_media('Skateboard 01.mp4')
            playback_window_page.Edit_TimelinePreview_SetPreviewQuality('High')
            timeline_page.edit_timeline_render_preview()
            time.sleep(3)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_High.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_High.png', current_image)
            case.result = compare_result

        # change to ultra HD, render not keep
        with uuid("44c5b252-e035-47a9-ba9e-5d167d798b8a") as case:
            time.sleep(3)
            playback_window_page.Edit_TimelinePreview_SetPreviewQuality('Ultra HD')
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_NOT_Keep.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_NOT_Keep.png', current_image)
            case.result = compare_result

        # render Ultra HD
        with uuid("eb79e156-a107-4e1f-85f6-4f6185f4126f") as case:
            time.sleep(3)
            timeline_page.edit_timeline_render_preview()
            time.sleep(5)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_UltraHD.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_UltraHD.png', current_image)
            case.result = compare_result

        # change to FullHD, render will keep
        with uuid("e61a9e9b-7cbc-43f3-aa1d-02b1ad830d4f") as case:
            time.sleep(3)
            playback_window_page.Edit_TimelinePreview_SetPreviewQuality('Full HD')
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_Keep.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_Keep.png', current_image)
            case.result = compare_result

        # new workspace and render for FullHD preview quality
        with uuid("20015275-a84a-493e-9b5c-aff2e867194d") as case:
            time.sleep(3)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            main_page.insert_media('Skateboard 02.mp4')
            timeline_page.edit_timeline_render_preview()
            time.sleep(3)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_FullHD.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_FullHD.png', current_image)
            case.result = compare_result

        # move clip position, the render will keep
        with uuid("41807242-be26-4581-809c-9b5529f051c3") as case:
            time.sleep(3)
            timeline_page.drag_single_media_move_to(0, 0, 20)
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_Reposition.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_Reposition.png', current_image)
            case.result = compare_result

        # Render then trim(from video end)
        with uuid("13677a1a-1451-49a1-b612-8c716a935cd5") as case:
            time.sleep(3)
            main_page.click_undo()
            timeline_page.drag_timeline_clip('Last', 0.5, 0, 0)
            main_page.set_timeline_timecode('00_00_00_00')
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_trim.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_trim.png', current_image)
            case.result = compare_result

        # Render then split
        with uuid("36546742-b45b-4dfc-8b35-6d7d593de2f9") as case:
            time.sleep(3)
            main_page.click_undo()
            main_page.set_timeline_timecode('00_00_05_00')
            tips_area_page.click_TipsArea_btn_split()
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_Split1.png')
            compare_result_1 = timeline_page.compare(Ground_Truth_Folder + 'Render_Split1.png', current_image)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 1,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_Split2.png')
            compare_result_2 = timeline_page.compare(Ground_Truth_Folder + 'Render_Split2.png', current_image)
            case.result = compare_result_1 and compare_result_2

        # trim then render
        with uuid("d836fb76-a9b1-4842-afa3-4e26450146b8") as case:
            time.sleep(3)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            main_page.insert_media('Skateboard 03.mp4')
            timeline_page.drag_timeline_clip('Last', 0.5, 0, 0)
            main_page.set_timeline_timecode('00_00_00_00')
            timeline_page.edit_timeline_render_preview()
            time.sleep(3)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Trim_Render.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Trim_Render.png', current_image)
            case.result = compare_result

        # Split then render
        with uuid("c2545a34-1ac2-4843-adb7-b11ea7dd3710") as case:
            time.sleep(3)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            main_page.insert_media('Skateboard 03.mp4')
            main_page.set_timeline_timecode('00_00_05_00')
            tips_area_page.click_TipsArea_btn_split()
            main_page.set_timeline_timecode('00_00_00_00')
            timeline_page.edit_timeline_render_preview()
            time.sleep(3)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Split_Render1.png')
            compare_result_1 = timeline_page.compare(Ground_Truth_Folder + 'Split_Render1.png', current_image)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 1,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Split_Render2.png')
            compare_result_2 = timeline_page.compare(Ground_Truth_Folder + 'Split_Render2.png', current_image)
            case.result = compare_result_1 and compare_result_2

    @exception_screenshot
    def test_1_1_5(self):
        # render preview then apply WB, render not keep
        with uuid("f8d6ef2e-df1c-4662-add7-f4403a2a716c") as case:
            time.sleep(3)
            main_page.insert_media('Skateboard 01.mp4')
            timeline_page.edit_timeline_render_preview()
            time.sleep(5)
            tips_area_page.click_fix_enhance()
            fix_enhance_page.fix.enable_white_balance(True)
            fix_enhance_page.fix.white_balance.tint.set_value(80)
            time.sleep(1)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_NotKeep_WB.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_NotKeep_WB.png', current_image)
            case.result = compare_result

        # apply fix and then render preview
        with uuid("2995fc85-f4bf-401b-9065-b0e327354eea") as case:
            time.sleep(2)
            timeline_page.edit_timeline_render_preview()
            time.sleep(5)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_WB.png')
            compare_result_1 = timeline_page.compare(Ground_Truth_Folder + 'Render_WB.png', current_image)
            main_page.set_timeline_timecode('00_00_05_00')
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Preview_WB_Render.png')
            compare_result_2 = title_room_page.compare(Ground_Truth_Folder + 'Preview_WB_Render.png', current_image)
            case.result = compare_result_1 and compare_result_2

        # render preview and then apply lens correction
        with uuid("ba180a26-f514-4f51-ab94-ac4381e594eb") as case:
            time.sleep(2)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            main_page.insert_media('Skateboard 02.mp4')
            timeline_page.edit_timeline_render_preview()
            time.sleep(5)
            tips_area_page.click_fix_enhance()
            fix_enhance_page.fix.enable_lens_correction(True)
            fix_enhance_page.fix.lens_correction.fisheye_distortion.set_value(-80)
            time.sleep(1)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_NotKeep_Lens.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_NotKeep_Lens.png', current_image)
            case.result = compare_result

        # apply lens correction then render preview
        with uuid("452c8fe2-2736-4246-bf88-84b2f23cf596") as case:
            time.sleep(2)
            timeline_page.edit_timeline_render_preview()
            time.sleep(5)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_Lens.png')
            compare_result_1 = timeline_page.compare(Ground_Truth_Folder + 'Render_Lens.png', current_image)
            main_page.set_timeline_timecode('00_00_05_00')
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Preview_Lens_Render.png')
            compare_result_2 = title_room_page.compare(Ground_Truth_Folder + 'Preview_Lens_Render.png', current_image)
            case.result = compare_result_1 and compare_result_2

        # render preview then apply color adjustment, render not keep
        with uuid("cdf113cb-a526-4dba-a678-9e6708403c58") as case:
            time.sleep(2)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            main_page.insert_media('Skateboard 03.mp4')
            timeline_page.edit_timeline_render_preview()
            time.sleep(5)
            tips_area_page.click_fix_enhance()
            fix_enhance_page.enhance.enable_color_adjustment(True)
            fix_enhance_page.enhance.color_adjustment.hue.set_value(160)
            time.sleep(1)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_NotKeep_ColorA.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_NotKeep_ColorA.png', current_image)
            case.result = compare_result

        # render preview then apply color adjustment, then undo, it should be no effect
        with uuid("0cf77e40-9c0c-4a37-a8b1-c688ffbda9df") as case:
            time.sleep(2)
            main_page.click_undo()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Preview_UndoFix.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Preview_UndoFix.png', current_image)
            case.result = compare_result

        # Redo color adjustment then render preview
        with uuid("a457b5c0-ff77-446a-994a-775ba6f3902d") as case:
            time.sleep(2)
            main_page.click_redo()
            time.sleep(1)
            timeline_page.edit_timeline_render_preview()
            time.sleep(5)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_ColorA.png')
            compare_result_1 = timeline_page.compare(Ground_Truth_Folder + 'Render_ColorA.png', current_image)
            main_page.set_timeline_timecode('00_00_05_00')
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Preview_ColorA_Render.png')
            compare_result_2 = title_room_page.compare(Ground_Truth_Folder + 'Preview_ColorA_Render.png', current_image)
            case.result = compare_result_1 and compare_result_2

    @exception_screenshot
    def test_1_1_6(self):
        # Render pip and modify in designer
        with uuid("da0f1459-0371-4b31-9f07-c874187c0f08") as case:
            time.sleep(2)
            main_page.tap_PiPRoom_hotkey()
            main_page.select_LibraryRoom_category('General')
            main_page.select_library_icon_view_media('Dialog_07')
            tips_area_page.click_TipsArea_btn_insert(-1)
            timeline_page.edit_timeline_render_preview()
            time.sleep(3)
            tips_area_page.tools.select_PiP_Designer()
            pip_designer_page.click_maximize_btn()
            pip_designer_page.switch_mode('Advanced')
            pip_designer_page.express_mode.unfold_properties_object_setting_tab(1)
            pip_designer_page.input_scale_width_value('0.6')
            pip_designer_page.input_rotation_degree_value('45')
            time.sleep(1)
            image_result = pip_designer_page.snapshot(locator=L.pip_designer.preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'PIP_Modify.png')
            compare_result = pip_designer_page.compare(Ground_Truth_Folder + 'PIP_Modify.png', image_result)
            case.result = compare_result

        # after modify in designer, the render not keep
        with uuid("4bb65eff-eaa6-47cb-9034-01513c42a08f") as case:
            time.sleep(1)
            pip_designer_page.click_ok()
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_NotKeep_PiPModify.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_NotKeep_PiPModify.png', current_image)
            case.result = compare_result

        # render title and modify in designer
        with uuid("1329a93d-9ed2-46f8-8ff6-1bb608ecc9d9") as case:
            time.sleep(1)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            main_page.enter_room(1)
            title_room_page.select_specific_tag('General')
            media_room_page.select_media_content('Radar')
            tips_area_page.click_TipsArea_btn_insert(-1)
            timeline_page.edit_timeline_render_preview()
            time.sleep(3)
            tips_area_page.click_TipsArea_btn_Designer('title')
            title_designer_page.click_maximize_btn()
            title_designer_page.switch_mode(2)
            title_designer_page.unfold_object_character_presets_tab(1)
            title_designer_page.apply_character_presets(7)
            title_designer_page.unfold_object_character_presets_tab(0)
            title_designer_page.unfold_object_object_setting_tab(1)
            title_designer_page.input_object_setting_scale_width_value('2')
            title_designer_page.set_timecode('00_00_05_00')
            time.sleep(2)
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_video_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'Title_Modify.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'Title_Modify.png', image_result)
            case.result = compare_result

        # after modify in designer, the render not keep
        with uuid("c8c83948-6a51-4f90-add8-cbde5b08c347") as case:
            time.sleep(1)
            title_designer_page.click_ok()
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_NotKeep_TitleModify.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_NotKeep_TitleModify.png', current_image)
            case.result = compare_result

        # render the mask template
        with uuid("f34e00b4-9840-41d1-8d37-eb40d7c5bf7f") as case:
            time.sleep(1)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            main_page.enter_room(0)
            main_page.insert_media('Food.jpg')
            tips_area_page.tools.select_Mask_Designer()
            mask_designer_page.MaskDesigner_Apply_template(2)
            mask_designer_page.Edit_MaskDesigner_ClickOK()
            time.sleep(1)
            timeline_page.edit_timeline_render_preview()
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_Mask.png')
            compare_result_1 = timeline_page.compare(Ground_Truth_Folder + 'Render_Mask.png', current_image)
            main_page.set_timeline_timecode('00_00_05_00')
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Preview_Mask_Render.png')
            compare_result_2 = title_room_page.compare(Ground_Truth_Folder + 'Preview_Mask_Render.png', current_image)
            case.result = compare_result_1 and compare_result_2

        # Able to Modify the mask in designer
        with uuid("f31d6907-a2cf-48f6-86b4-9630105b3679") as case:
            time.sleep(1)
            tips_area_page.tools.select_Mask_Designer()
            mask_designer_page.MaskDesigner_Apply_template(8)
            time.sleep(2)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window,
                                                     file_name=Auto_Ground_Truth_Folder + 'Preview_Mask_Modify.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'Preview_Mask_Modify.png', current_image)
            case.result = compare_result

        # After modify mask, the render not keep
        with uuid("06aeb65c-da10-495f-aa6f-93f2ef5de5d2") as case:
            time.sleep(1)
            mask_designer_page.Edit_MaskDesigner_ClickOK()
            time.sleep(1)
            main_page.set_timeline_timecode('00_00_00_00')
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_Mask_NotKeep.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_Mask_NotKeep.png', current_image)
            case.result = compare_result
    """
    @exception_screenshot
    def test_1_1_7(self):
        # Crop/zoom/pan and then render preview
        with uuid("2b863d13-9335-48c3-8eb5-b98f8311bf32") as case:
            time.sleep(1)
            main_page.insert_media('Skateboard 03.mp4')
            tips_area_page.tools.select_CropZoomPan()

            crop_zoom_pan_page.set_AspectRatio_4_3()
            crop_zoom_pan_page.click_ok()
            time.sleep(1)
            timeline_page.edit_timeline_render_preview()
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_CropZoomPan.png')
            compare_result_1 = timeline_page.compare(Ground_Truth_Folder + 'Render_CropZoomPan.png', current_image)
            main_page.set_timeline_timecode('00_00_05_00')
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Preview_CropZoomPan.png')
            compare_result_2 = title_room_page.compare(Ground_Truth_Folder + 'Preview_CropZoomPan.png', current_image)
            case.result = compare_result_1 and compare_result_2

        # Re-enter Crop/zoom/pan and then modify
        with uuid("3007aaae-1b26-4378-a353-f8de802b0cd0") as case:
            time.sleep(1)
            tips_area_page.tools.select_CropZoomPan()
            crop_zoom_pan_page.set_AspectRatio_9_16()
            current_image = mask_designer_page.snapshot(locator=L.crop_zoom_pan.preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'Preview_Modify_CropZoomPan.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'Preview_Modify_CropZoomPan.png', current_image)
            case.result = compare_result

        # render not keep after modify
        with uuid("2b90813d-1709-49c8-8740-cc5fd2db8f05") as case:
            time.sleep(1)
            crop_zoom_pan_page.click_ok()
            main_page.set_timeline_timecode('00_00_00_00')
            time.sleep(1)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_CZP_NotKeep.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_CZP_NotKeep.png', current_image)
            case.result = compare_result
    """
    @exception_screenshot
    def test_1_1_8(self):
        # Pan & Zoom and then render preview
        with uuid("af9cca2a-b76b-49b0-a361-90a3e207ef3c") as case:
            time.sleep(1)
            main_page.insert_media('Sport 01.jpg')
            tips_area_page.tools.select_Pan_Zoom()
            pan_zoom_page.apply_motion_style(2)
            timeline_page.edit_timeline_render_preview()
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_PanZoom.png')
            compare_result_1 = timeline_page.compare(Ground_Truth_Folder + 'Render_PanZoom.png', current_image)
            main_page.set_timeline_timecode('00_00_02_15')
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Preview_PanZoom.png')
            compare_result_2 = title_room_page.compare(Ground_Truth_Folder + 'Preview_PanZoom.png', current_image, similarity=0.9)
            case.result = compare_result_1 and compare_result_2

        # Change Pan & Zoom style and preview is normal
        with uuid("ac9bd7ed0-9911-4334-84d0-6867c1f0a1f1") as case:
            time.sleep(1)
            main_page.set_timeline_timecode('00_00_00_00')
            tips_area_page.tools.select_Pan_Zoom()
            pan_zoom_page.apply_motion_style(3)
            main_page.set_timeline_timecode('00_00_04_00')
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Preview_PanZoom_Change.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Preview_PanZoom_Change.png', current_image)
            case.result = compare_result

        # Change Pan & Zoom style and render not keep
        with uuid("9e82dba8-85cc-4982-8fd3-8fdda82fc8d9") as case:
            time.sleep(1)
            main_page.set_timeline_timecode('00_00_00_00')
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_PanZoom_NotKeep.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_PanZoom_NotKeep.png', current_image)
            case.result = compare_result


        # Apply video speed to 0.5x and then render preview
        with uuid("0d8d7a02-e1fc-480c-a4e4-cc0a6a6d0c93") as case:
            time.sleep(1)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            time.sleep(1)
            main_page.insert_media('Skateboard 02.mp4')
            time.sleep(1)
            timeline_page.drag_to_change_speed(0, 0, 'Last', 'Right', 1)
            time.sleep(1)
            main_page.set_timeline_timecode('00_00_00_00')
            timeline_page.edit_timeline_render_preview()
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_VideoSpeed.png')
            compare_result_1 = timeline_page.compare(Ground_Truth_Folder + 'Render_VideoSpeed.png', current_image)
            main_page.set_timeline_timecode('00_00_15_00')
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Preview_VideoSpeed.png')
            compare_result_2 = title_room_page.compare(Ground_Truth_Folder + 'Preview_VideoSpeed.png', current_image)
            case.result = compare_result_1 and compare_result_2

        # Able to change video speed
        with uuid("b8e09593-f350-4312-9179-839ca558479c") as case:
            time.sleep(1)
            timeline_page.drag_to_change_speed(0, 0, 'Last', 'Left', 0.25)
            time.sleep(1)
            current_duration = playback_window_page.get_timecode_slidebar()
            logger(current_duration)
            if current_duration == '00;00;15;07':
                case.result = True
            else:
                case.result = False

        # After change video speed and render not keep
        with uuid("15d603a9-6a1f-4e3d-a84d-d1970cee3019") as case:
            time.sleep(1)
            main_page.set_timeline_timecode('00_00_00_00')
            time.sleep(2)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_VSpeed_NotKeep.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_VSpeed_NotKeep.png', current_image)
            case.result = compare_result

    @exception_screenshot
    def test_1_1_9(self):
        # Clip render preview and then set blending mode
        with uuid("f5464a0a-60da-4f5f-9a1d-7b795f9bb0b7") as case:
            time.sleep(3)
            media_room_page.enter_color_boards()
            main_page.click_library_details_view()
            media_room_page.sound_clips_select_media('2, 52, 111')
            #main_page.select_library_icon_view_media('0,175,255')
            tips_area_page.click_TipsArea_btn_insert()
            main_page.tap_PiPRoom_hotkey()
            main_page.select_LibraryRoom_category('General')
            main_page.drag_media_to_timeline_playhead_position('Dialog_07', 2)
            timeline_page.edit_timeline_render_preview()
            time.sleep(3)
            timeline_page.hover_timeline_media(2, 0)
            timeline_page.right_click()
            timeline_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Difference')
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Preview_ApplyBlending.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Preview_ApplyBlending.png', current_image)
            case.result = compare_result

        # Clip render preview wont keep
        with uuid("15aaf868-24cb-414b-9849-fd0efdf87f89") as case:
            time.sleep(1)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_BlendingNotKeep.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_BlendingNotKeep.png', current_image)
            case.result = compare_result

        # Clip render preview again
        with uuid("0b1084ba-a1dc-420d-91ca-3b197341a74d") as case:
            time.sleep(1)
            timeline_page.edit_timeline_render_preview()
            time.sleep(3)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_BlendingMode.png')
            compare_result_1 = timeline_page.compare(Ground_Truth_Folder + 'Render_BlendingMode.png', current_image)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Preview_Blending.png')
            compare_result_2 = title_room_page.compare(Ground_Truth_Folder + 'Preview_Blending.png', current_image)
            case.result = compare_result_1 and compare_result_2

            # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_21(self):
        with uuid("""44c5b252-e035-47a9-ba9e-5d167d798b8a
e61a9e9b-7cbc-43f3-aa1d-02b1ad830d4f
60477890-746b-457a-b9f2-c779f56f0909
f4fbc2ec-9e62-44af-9623-8e998ef16a40
276ea962-b811-4e19-954f-2e43132d0987
2b90813d-1709-49c8-8740-cc5fd2db8f05
c9bd7ed0-9911-4334-84d0-6867c1f0a1f1
3007aaae-1b26-4378-a353-f8de802b0cd0""") as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"