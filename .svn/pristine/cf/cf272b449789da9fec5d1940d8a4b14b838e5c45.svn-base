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
report = MyReport("MyReport", driver=mac, html_name="Scan Blending Effect.html")
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

class Test_Blending_Effect():
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
            google_sheet_execution_log_init('Scan_Blending_Effect')

    @classmethod
    def teardown_class(cls):
        logger('Test Case are completed.')

        logger('teardown_class - export report')
        report.export()
        logger(
            f"Scan Blending Effect result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()

    def enter_blending_effect(self):
        # Enter Effect Room
        main_page.enter_room(3)
        time.sleep(DELAY_TIME*4)

        # Close Body Effect bb
        main_page.timeline_select_track(1)

        effect_room_page.select_LibraryRoom_category('Blending Effect')
        time.sleep(DELAY_TIME)

    def blending_effect_download_complete(self, timeout=60):
        # pop up (Downloading Files) then check result
        time.sleep(DELAY_TIME*6)

        if not download_from_ss_page.download.has_dialog():
            logger("Download dialog is not found now")
            time.sleep(DELAY_TIME)
            return True

        download_status = False
        # Check (download Blending Effect is ready) for loop
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
    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1(self):
        # Insert Landscape 01.jpg
        main_page.select_library_icon_view_media('Landscape 01.jpg')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=main_page.area.preview.main)
        logger(default_preview)

        # [M6] Add "Lens Flare 01" to Timeline track
        with uuid("4423ab94-837e-469b-a1dc-4b2edede69b8") as case:
            # Enter Effect Room > Blending Effect category
            self.enter_blending_effect()

            # Input search Lens Flare 01
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Lens Flare 01')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 01')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 01 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M7] Add "Lens Flare 02" to Timeline track
        with uuid("481ca2a6-dc3e-4cd6-918b-3fbf60d4a836") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 02')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 02')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 02 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M8] Add "Lens Flare 03" to Timeline track
        with uuid("d4da5c48-3c32-4e66-b218-683668238645") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 03')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 03')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - LLens Flare 03 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M9] Add "Lens Flare 04" to Timeline track
        with uuid("1f07d35d-11c6-403b-b7ec-2538d46c46cc") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 04')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 04')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 04 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M10] Add "Lens Flare 05" to Timeline track
        with uuid("0f1e401b-18a4-47a0-b29b-83bb27b7cd01") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 05')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 05')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 05 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_2(self):
        # Insert AAC 6 ch clip
        video_path = Test_Material_Folder + 'Crop_Zoom_Pan/AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:01:15:26
        main_page.set_timeline_timecode('00_01_15_26')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # [M11] Add "Lens Flare 06" to Timeline track
        with uuid("15396227-426a-4d5b-8ef8-7c3c4b0f12e7") as case:
            # Enter Effect Room > Blending Effect category
            self.enter_blending_effect()

            # Input search Lens Flare 06
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Lens Flare 06')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 06')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 06 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M12] Add "Lens Flare 07" to Timeline track
        with uuid("6c553786-90a4-45a9-9d3e-33041e6b5b05") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 07')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 07')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 07 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()

        # Set timecode 00:01:19:11
        main_page.set_timeline_timecode('00_01_19_11')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # Set timecode 00:01:15:26
        main_page.set_timeline_timecode('00_01_15_26')

        # [M13] Add "Lens Flare 08" to Timeline track
        with uuid("3b0291eb-86c3-4fb0-89ef-5a338f80dbef") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 08')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 08')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 08 [NG], raise exception')
                raise Exception

            # Play preview then pause
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 5)
            playback_window_page.Edit_Timeline_PreviewOperation('Pause')
            time.sleep(DELAY_TIME * 3)
            # Set timecode 00:01:19:11
            main_page.set_timeline_timecode('00_01_19_11')
            time.sleep(DELAY_TIME * 3)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # Set timecode 00:01:19:11
        main_page.set_timeline_timecode('00_01_19_11')
        time.sleep(DELAY_TIME * 3)

        # [M14] Add "Lens Flare 09" to Timeline track
        with uuid("febadb21-f716-4489-b4b5-c55d88333dd0") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 09')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 09')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 09 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.98)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.92)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()

        # [M15] Add "Lens Flare 10" to Timeline track
        with uuid("7bdfe62c-47e4-4249-b4f0-28348faf2e1b") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 10')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 10')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 10 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.91)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.81)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_3(self):
        # Insert Skateboard 01.mp4
        main_page.select_library_icon_view_media('Skateboard 01.mp4')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()
        time.sleep(DELAY_TIME * 2)

        # Set timecode 00:00:07:02
        main_page.set_timeline_timecode('00_00_07_02')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=main_page.area.preview.main)
        logger(default_preview)

        # [M16] Add "Lens Flare 11" to Timeline track
        with uuid("9f60756c-938b-40cc-a431-c1a0fc9cab03") as case:
            # Enter Effect Room > Blending Effect category
            self.enter_blending_effect()

            # Input search Lens Flare 11
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Lens Flare 11')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 11')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - LLens Flare 11 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()

        # [M17] Add "Lens Flare 12" to Timeline track
        with uuid("b7752af1-73a0-4f0f-810e-3ab1306af677") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 12')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 12')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 12 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M18] Add "Lens Flare 13" to Timeline track
        with uuid("82742286-ffb4-428a-86d3-1b051265d711") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 13')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 13')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 13 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()

        # Set timecode 00:00:02:06
        main_page.set_timeline_timecode('00_00_02_06')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=main_page.area.preview.main)
        logger(default_preview)

        # [M19] Add "Lens Flare 14" to Timeline track
        with uuid("b7b325f5-faa5-42ba-a8cb-ba47653c478c") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 14')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 14')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 14 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M20] Add "Lens Flare 15" to Timeline track
        with uuid("a4816266-8970-4425-957b-31fa44edd301") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 15')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 15')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 15 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M21] Add "Lens Flare 16" to Timeline track
        with uuid("d20b6e08-6bc9-4d9c-9dee-45d4103cc93a") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 16')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 16')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 16 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_4(self):
        # Insert Travel 01.jpg
        main_page.select_library_icon_view_media('Travel 01.jpg')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()
        time.sleep(DELAY_TIME * 2)

        # Set timecode 00:00:03:10
        main_page.set_timeline_timecode('00_00_03_10')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=main_page.area.preview.main)
        logger(default_preview)

        # [M22] Add "Lens Flare 17" to Timeline track
        with uuid("3da50fc0-c18e-49f0-82a3-6a36b35e609a") as case:
            # Enter Effect Room > Blending Effect category
            self.enter_blending_effect()

            # Input search Lens Flare 17
            main_page.exist_click(L.media_room.input_search)
            main_page.keyboard.send('Lens Flare 17')
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 17')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 17 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M23] Add "Lens Flare 18" to Timeline track
        with uuid("5361d0ec-7e54-491b-a3b5-62fba983b30d") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 18')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 18')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 18 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M24] Add "Lens Flare 19" to Timeline track
        with uuid("fa7d9eb1-5752-48d6-b898-ad509f33c787") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 19')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 19')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 19 [NG], raise exception')
                raise Exception

            effect_19_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(effect_19_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(effect_19_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M25] Add "Lens Flare 20" to Timeline track
        with uuid("ebfd67ae-9831-4f3a-bf46-43286e41fb06") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 20')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 20')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 20 [NG], raise exception')
                raise Exception

            effect_20_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(effect_19_preview, effect_20_preview, similarity=0.995)
            effect_result_diff = main_page.compare(effect_19_preview, effect_20_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M55] Add "Light Leak 01 Blue" to Timeline track
        with uuid("256c7359-0362-47f9-86dc-d85e8c8eb22c") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Light Leak 01')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 01 Blue')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 01 Blue [NG], raise exception')
                raise Exception

            effect_blue_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_blue_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_blue_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M56] Add "Light Leak 01 Green" to Timeline track
        with uuid("e268d2c1-b4a7-4103-8462-bc6c22b3b24b") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 01 Green')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 01 Green [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M57] Add "Light Leak 01 Pink" to Timeline track
        with uuid("c4c29922-d0c2-425f-94fd-1bd5ac144172") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 01 Pink')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 01 Pink [NG], raise exception')
                raise Exception

            effect_pink_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_pink_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_pink_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M58] Add "Light Leak 01 Purple" to Timeline track
        with uuid("154014f4-0474-4801-b49a-1c42e1e2798e") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 01 Purple')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 01 Purple [NG], raise exception')
                raise Exception

            effect_purple_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_purple_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_purple_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_5(self):
        # Insert AAC 6 ch clip
        video_path = Test_Material_Folder + 'Crop_Zoom_Pan/AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:02:15:14
        main_page.set_timeline_timecode('00_02_15_14')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # Enter Effect Room > Blending Effect category
        self.enter_blending_effect()

        # [M59] Add "Light Leak 02 Blue" to Timeline track
        with uuid("ed95e629-44ad-4b2a-b0ff-b0857b3ba78e") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Light Leak 02')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 02 Blue')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 02 Blue [NG], raise exception')
                raise Exception

            effect_blue_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_blue_preview, similarity=0.98)
            effect_result_diff = main_page.compare(default_preview, effect_blue_preview, similarity=0.93)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M60] Add "Light Leak 02 Green" to Timeline track
        with uuid("c79e8eac-9d0b-4f15-97fe-cf1e92e05d1e") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 02 Green')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 02 Green [NG], raise exception')
                raise Exception

            effect_purple_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_purple_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_purple_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M61] Add "Light Leak 02 Pink" to Timeline track
        with uuid("14ee011a-ecde-4f32-bdcb-2fca35f977fe") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 02 Pink')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 02 Pink [NG], raise exception')
                raise Exception

            effect_purple_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_purple_preview, similarity=0.98)
            effect_result_diff = main_page.compare(default_preview, effect_purple_preview, similarity=0.94)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M62] Add "Light Leak 02 Yellow" to Timeline track
        with uuid("5f167bf9-bd42-4eab-b7cd-6310918be3b2") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 02 Yellow')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 02 Yellow [NG], raise exception')
                raise Exception

            effect_purple_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_purple_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_purple_preview, similarity=0.94)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()

        # Cancel search result then Search library content
        media_room_page.search_library_click_cancel()
        time.sleep(DELAY_TIME)
        media_room_page.search_library('Light Leak 03')
        time.sleep(DELAY_TIME * 3)

        # [M63] Add "Light Leak 03 Blue" to Timeline track
        with uuid("4b674b81-e2f4-4354-8447-533a62460989") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 03 Blue')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 03 Blue [NG], raise exception')
                raise Exception

            effect_purple_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_purple_preview, similarity=0.7)
            effect_result_diff = main_page.compare(default_preview, effect_purple_preview, similarity=0.6)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M64] Add "Light Leak 03 Green" to Timeline track
        with uuid("de693107-d33c-44f6-b56c-66211fca60c1") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 03 Green')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 03 Green [NG], raise exception')
                raise Exception

            effect_purple_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_purple_preview, similarity=0.85)
            effect_result_diff = main_page.compare(default_preview, effect_purple_preview, similarity=0.75)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M65] Add "Light Leak 03 Purple" to Timeline track
        with uuid("a8201726-6d05-4377-88ec-d47ba5f2ec85") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 03 Purple')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 03 Purple [NG], raise exception')
                raise Exception

            effect_purple_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_purple_preview, similarity=0.76)
            effect_result_diff = main_page.compare(default_preview, effect_purple_preview, similarity=0.68)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M66] Add "Light Leak 03 Yellow" to Timeline track
        with uuid("b7941368-4de8-46ae-ab5c-ad9d8b23c8c3") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 03 Yellow')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 03 Yellow [NG], raise exception')
                raise Exception

            effect_purple_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_purple_preview, similarity=0.85)
            effect_result_diff = main_page.compare(default_preview, effect_purple_preview, similarity=0.78)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_6(self):
        # Insert AAC 6 ch clip
        video_path = Test_Material_Folder + 'Crop_Zoom_Pan/AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:01:24:18
        main_page.set_timeline_timecode('00_01_24_18')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # [M67] Add "Light Leak 04 Blue" to Timeline track
        with uuid("64d5def4-58e3-4f07-9308-138119827899") as case:
            # Enter Effect Room > Blending Effect category
            self.enter_blending_effect()

            # Input search Light Leak 04
            media_room_page.search_library('Light Leak 04')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 04 Blue')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 04 Blue [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.89)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.8)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M68] Add "Light Leak 04 Green" to Timeline track
        with uuid("9de62a20-558b-44e2-a3ea-6fec3915ce12") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 04 Green')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 04 Green [NG], raise exception')
                raise Exception

            effect_purple_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_purple_preview, similarity=0.7)
            effect_result_diff = main_page.compare(default_preview, effect_purple_preview, similarity=0.63)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M69] Add "Light Leak 04 Orange" to Timeline track
        with uuid("6e019777-86e8-497f-9969-8f7a9678cbb6") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 04 Orange')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 04 Orange [NG], raise exception')
                raise Exception

            effect_purple_preview = main_page.snapshot(locator=main_page.area.preview.main)
            time.sleep(DELAY_TIME)
            effect_result_same = not main_page.compare(default_preview, effect_purple_preview, similarity=0.71)
            effect_result_diff = main_page.compare(default_preview, effect_purple_preview, similarity=0.58)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M70] Add "Light Leak 04 Purple" to Timeline track
        with uuid("78c8a96e-4a57-4e2f-91c2-a3f2017c9334") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 04 Purple')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 04 Purple [NG], raise exception')
                raise Exception

            effect_purple_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_purple_preview, similarity=0.86)
            effect_result_diff = main_page.compare(default_preview, effect_purple_preview, similarity=0.81)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M71] Add "Light Leak 05 Blue" to Timeline track
        with uuid("72d70975-1e6a-48f5-a39b-33702fff1782") as case:
            # Input search Light Leak 04
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Light Leak 05')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 05 Blue')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 05 Blue [NG], raise exception')
                raise Exception

            effect_purple_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_purple_preview, similarity=0.95)
            effect_result_diff = main_page.compare(default_preview, effect_purple_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M72] Add "Light Leak 05 Green" to Timeline track
        with uuid("6bd3288f-8f03-4060-a1a0-e7ac8c3f397f") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 05 Green')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 05 Green [NG], raise exception')
                raise Exception

            effect_purple_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_purple_preview, similarity=0.991)
            effect_result_diff = main_page.compare(default_preview, effect_purple_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M73] Add "Light Leak 05 Orange" to Timeline track
        with uuid("53ea6afc-4ff0-440d-a6e4-2ad177263453") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 05 Orange')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 05 Orange [NG], raise exception')
                raise Exception

            effect_purple_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_purple_preview, similarity=0.991)
            effect_result_diff = main_page.compare(default_preview, effect_purple_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M74] Add "Light Leak 05 Yellow" to Timeline track
        with uuid("c7e4153a-5f04-476c-aff4-ea0ae8072f84") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 05 Yellow')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 05 Yellow [NG], raise exception')
                raise Exception

            effect_purple_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_purple_preview, similarity=0.95)
            effect_result_diff = main_page.compare(default_preview, effect_purple_preview, similarity=0.85)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_7(self):
        # Insert beauty.jpg
        video_path = Test_Material_Folder + 'BFT_21_Stage1/beauty.jpg'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:01:12
        main_page.set_timeline_timecode('00_00_01_12')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # [M75] Add "Light Leak 06 Blue" to Timeline track
        with uuid("944e3254-9071-496b-b0a8-278841ce0061") as case:
            # Enter Effect Room > Blending Effect category
            self.enter_blending_effect()

            # Input search Light Leak 06
            media_room_page.search_library('Light Leak 06')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 06 Blue')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 06 Blue [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.993)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M76] Add "Light Leak 06 Orange" to Timeline track
        with uuid("50e9d984-9a36-4d2e-a4d0-96a89fb535be") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 06 Orange')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 06 Orange [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M77] Add "Light Leak 06 Pink" to Timeline track
        with uuid("49d6c878-569f-41ff-9c1c-327a871e36ae") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 06 Pink')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 06 Pink [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.97)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.92)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M78] Add "Light Leak 06 Yellow" to Timeline track
        with uuid("6c88d121-ea11-4963-9c47-352c830fa3ac") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 06 Yellow')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 06 Yellow [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.991)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M87] Add "Light Leak 09 Blue" to Timeline track
        with uuid("15511337-5f25-4347-8c00-b0b9b9b288a0") as case:
            # Input search Light Leak 09
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Light Leak 09')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 09 Blue')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 09 Blue [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M88] Add "Light Leak 09 Green" to Timeline track
        with uuid("9e5e29ec-e1f7-43fc-9dfd-da569b687a55") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 09 Green')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 09 Green [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M89] Add "Light Leak 09 Orange" to Timeline track
        with uuid("8076e085-ff64-4985-95ee-f28cc3f8dbb3") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 09 Orange')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 09 Orange [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M90] Add "Light Leak 09 Pink" to Timeline track
        with uuid("11e3e6de-a7c3-4483-a0ac-b4c79e6a990b") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 09 Pink')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 09 Pink [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.97)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.93)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_8(self):
        # Insert hastur.jpg
        video_path = Test_Material_Folder + 'fix_enhance_20/hastur.jpg'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:03:07
        main_page.set_timeline_timecode('00_00_03_07')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # [M79] Add "Light Leak 07 Blue" to Timeline track
        with uuid("7b0c71db-988f-482f-a489-0a349748f8ae") as case:
            # Enter Effect Room > Blending Effect category
            self.enter_blending_effect()

            # Input search Light Leak 07
            media_room_page.search_library('Light Leak 07')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 07 Blue')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 07 Blue [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.993)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M80] Add "Light Leak 07 Green" to Timeline track
        with uuid("f83a8392-9a2d-4175-9bdb-14f40fdc3e47") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 07 Green')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 07 Green [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.993)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M81] Add "Light Leak 07 Purple" to Timeline track
        with uuid("62bd1366-5a8b-48bf-951b-14f233bab74a") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 07 Purple')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 07 Purple [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.993)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M82] Add "Light Leak 07 Yellow" to Timeline track
        with uuid("77aab13c-604f-4384-be8d-aa6239ee5bf4") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 07 Yellow')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 07 Yellow [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.98)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.93)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M91] Add "Light Leak 10 Blue" to Timeline track
        with uuid("d96ddf41-2652-4751-887a-200bdacbf740") as case:
            # Input search Light Leak 10
            media_room_page.search_library_click_cancel()
            media_room_page.search_library('Light Leak 10')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 10 Blue')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 10 Blue [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.98)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.93)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M92] Add "Light Leak 10 Purple" to Timeline track
        with uuid("69cccff1-eb32-4d0b-a898-82a78175a73b") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 10 Purple')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 10 Purple [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.97)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.92)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M93] Add "Light Leak 10 Red" to Timeline track
        with uuid("6520c441-1d6d-475f-aa30-e42d637e28b4") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 10 Red')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 10 Red [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.97)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M94] Add "Light Leak 10 Yellow" to Timeline track
        with uuid("7021f05c-8c7d-43c3-bbc5-6a2d84a7c783") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 10 Yellow')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 10 Yellow [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.97)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.91)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_9(self):
        # Insert Landscape 02.jpg
        main_page.select_library_icon_view_media('Landscape 02.jpg')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()
        time.sleep(DELAY_TIME * 2)

        # Set timecode 00:00:00:06
        main_page.set_timeline_timecode('00_00_00_06')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=main_page.area.preview.main)
        logger(default_preview)

        # [M83] Add "Light Leak 08 Green" to Timeline track
        with uuid("a7cf35df-0b43-413a-b112-b7d5eabd604e") as case:
            # Enter Effect Room > Blending Effect category
            self.enter_blending_effect()

            # Input search Light Leak 07
            media_room_page.search_library('Light Leak 08')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 08 Green')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 08 Green [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.97)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M84] Add "Light Leak 08 Orange" to Timeline track
        with uuid("fa255141-1a97-4029-b251-e99081d1df37") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 08 Orange')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 08 Orange [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.985)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.94)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M85] Add "Light Leak 08 Pink" to Timeline track
        with uuid("b2780dd6-b6b6-4766-b39b-aa0f3ad08d20") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 08 Pink')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 08 Pink [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.96)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M86] Add "Light Leak 08 Purple" to Timeline track
        with uuid("2217dd08-934f-4d62-b6a1-5153f47a7552") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 08 Purple')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 08 Purple [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.95)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.88)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M95] Add "Light Leak 11 Blue" to Timeline track
        with uuid("286858e0-58eb-4f7c-b839-61d50647f13c") as case:
            # Input search Light Leak 10
            media_room_page.search_library_click_cancel()
            media_room_page.search_library('Light Leak 11')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 11 Blue')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 11 Blue [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.96)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M96] Add "Light Leak 11 Orange" to Timeline track
        with uuid("790c60f1-df0e-4aca-8dac-adcfac103c88") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 11 Orange')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 11 Orange [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.96)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M97] Add "Light Leak 11 Purple" to Timeline track
        with uuid("1d5f7fa3-7b69-4f7e-a179-5360d5f3a807") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 11 Purple')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 11 Purple [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.98)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.93)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M98] Add "Light Leak 11 Yellow" to Timeline track
        with uuid("83130ae1-f641-4172-9fe0-7ad48e16ac52") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 11 Yellow')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 11 Yellow [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.96)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_10(self):
        # Insert Travel 01.jpg
        main_page.select_library_icon_view_media('Skateboard 03.mp4')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()
        time.sleep(DELAY_TIME * 2)

        # Set timecode 00:00:01:27
        main_page.set_timeline_timecode('00_00_01_27')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=main_page.area.preview.main)
        logger(default_preview)

        # Enter Effect Room > Blending Effect category
        self.enter_blending_effect()

        # [M99] Add "Light Leak 12 Blue" to Timeline track
        with uuid("122475ed-542c-4f0b-a00f-41d8a017b97e") as case:
            # Input search Light Leak 12
            media_room_page.search_library_click_cancel()
            media_room_page.search_library('Light Leak 12')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 12 Blue')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 12 Blue [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M100] Add "Light Leak 12 Green" to Timeline track
        with uuid("977424fd-6f6f-4653-aec4-f6c330c73039") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 12 Green')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 12 Green [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.992)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M101] Add "Light Leak 12 Orange" to Timeline track
        with uuid("cfc8ae5a-2f5d-4be3-aa80-d9f781b714f4") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 12 Orange')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 12 Orange [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.992)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M102] Add "Light Leak 12 Red" to Timeline track
        with uuid("c0260b30-7698-448d-b687-df49f3983b8b") as case:
            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Light Leak 12 Red')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Light Leak 12 Red [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.992)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_11(self):
        # Insert m2ts clip
        video_path = Test_Material_Folder + 'fix_enhance_20/shopping_mall.m2ts'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:01:27
        main_page.set_timeline_timecode('00_00_01_27')
        time.sleep(DELAY_TIME * 2)

        # Enter (Fix/ Enhance)
        tips_area_page.click_fix_enhance()

        # Enhance > Tick (Color Adjustment)
        fix_enhance_page.enhance.enable_color_adjustment()

        # Set Brightness = -69
        fix_enhance_page.enhance.color_adjustment.brightness.adjust_slider(-69)
        time.sleep(DELAY_TIME * 2)

        default_preview = main_page.snapshot(locator=main_page.area.preview.main)
        logger(default_preview)

        # Close (Fix/Enhance) page
        fix_enhance_page.click_close()
        time.sleep(DELAY_TIME * 2)

        # Enter Effect Room > Blending Effect category
        self.enter_blending_effect()

        # [M26] Add "Lens Flare 21" to Timeline track
        with uuid("a0ecbe42-3f54-437f-917f-628204e9c413") as case:
            # Search library content
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 21')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 21')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 21 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M28] Add "Lens Flare 23" to Timeline track
        with uuid("9b490b96-8916-4670-91f7-428ec30d9f3e") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 23')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 23')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 23 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M29] Add "Lens Flare 24" to Timeline track
        with uuid("ebccf2a5-b5a4-45c3-8cde-2161613b440c") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 24')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 24')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 24 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M27] Add "Lens Flare 22" to Timeline track
        with uuid("9f6323d2-0a92-437f-950e-8ccaa21b1d79") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 22')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 22')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 22 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.995)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M30] Add "Lens Flare 25" to Timeline track
        with uuid("742ff2a6-901e-447c-8aa3-8dfecd578150") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 25')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 25')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 25 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.985)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.94)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M31] Add "Lens Flare 26" to Timeline track
        with uuid("9ddf7cd8-3afa-455a-b3e4-71df738e42b5") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 26')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 26')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 26 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.94)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M32] Add "Lens Flare 27" to Timeline track
        with uuid("90f1ea25-a5b4-423a-8ce2-c034327b6631") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 27')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 27')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 27 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.98)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.93)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M33] Add "Lens Flare 28" to Timeline track
        with uuid("03c26cfa-4c0b-4231-be10-5c190de3b601") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 28')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 28')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 28 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.98)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.93)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_12(self):
        # Insert Travel 01.jpg
        main_page.select_library_icon_view_media('Travel 01.jpg')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()
        time.sleep(DELAY_TIME * 2)

        # Set timecode 00:00:01:27
        main_page.set_timeline_timecode('00_00_01_27')
        time.sleep(DELAY_TIME * 2)

        # Enter (Fix/ Enhance)
        tips_area_page.click_fix_enhance()

        # Enhance > Tick (Color Adjustment)
        fix_enhance_page.enhance.enable_color_adjustment()

        # Set Hue = 26
        fix_enhance_page.enhance.color_adjustment.hue.adjust_slider(26)
        time.sleep(DELAY_TIME * 2)

        default_preview = main_page.snapshot(locator=main_page.area.preview.main)
        logger(default_preview)

        # Close (Fix/Enhance) page
        fix_enhance_page.click_close()
        time.sleep(DELAY_TIME * 2)

        # Enter Effect Room > Blending Effect category
        self.enter_blending_effect()

        # [M34] Add "Lens Flare 29" to Timeline track
        with uuid("a5200f56-b187-4baa-a734-dbf6fe5f9c66") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 29')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 29')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 29 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.94)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M35] Add "Lens Flare 30" to Timeline track
        with uuid("b7de50f0-d63c-4af3-afbc-852f0148ed5f") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 30')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 30')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 30 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.94)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M36] Add "Lens Flare 31" to Timeline track
        with uuid("1f784c40-b625-4f37-9101-3035f1828fa0") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 31')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 31')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 31 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.94)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M37] Add "Lens Flare 32" to Timeline track
        with uuid("08fa4a4d-2f37-4e6e-a7df-81bb78173c84") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 32')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 32')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 32 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.94)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M38] Add "Lens Flare 33" to Timeline track
        with uuid("fee8e17a-652b-4b55-9e6a-a202f27e9d68") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 33')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 33')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 33 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.94)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M39] Add "Lens Flare 34" to Timeline track
        with uuid("8da38ac8-c37e-44ff-aac6-078e34104f27") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 34')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 34')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 34 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_13(self):
        # Insert mp4 clip
        video_path = Test_Material_Folder + 'fix_enhance_20/mountain.mp4'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:09:13
        main_page.set_timeline_timecode('00_00_09_13')
        time.sleep(DELAY_TIME * 2)

        # Enter (Fix/ Enhance)
        tips_area_page.click_fix_enhance()

        # Enhance > Tick (Color Adjustment)
        fix_enhance_page.enhance.enable_color_adjustment()
        time.sleep(DELAY_TIME * 2)

        # Set Exposure = 73
        fix_enhance_page.enhance.color_adjustment.exposure.adjust_slider(73)

        # Set Contrast = 100
        fix_enhance_page.enhance.color_adjustment.contrast.adjust_slider(100)
        time.sleep(DELAY_TIME * 2)

        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # Close (Fix/Enhance) page
        fix_enhance_page.click_close()
        time.sleep(DELAY_TIME * 2)

        # Enter Effect Room > Blending Effect category
        self.enter_blending_effect()

        # [M40] Add "Lens Flare 35" to Timeline track
        with uuid("90ce2af0-ee0b-4411-9ef5-0a0db1ccfca5") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 35')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 35')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 35 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.94)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M41] Add "Lens Flare 36" to Timeline track
        with uuid("668386d2-f022-4e95-b8d3-acee8a68ec86") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 36')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 36')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 36 [NG], raise exception')
                raise Exception

            # Set timecode 00:00:01:15
            main_page.set_timeline_timecode('00_00_01_15')
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:09:13
            main_page.set_timeline_timecode('00_00_09_13')
            time.sleep(DELAY_TIME * 2)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.94)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M42] Add "Lens Flare 37" to Timeline track
        with uuid("a8fec6cc-9dc7-483d-96f1-57ab9d7e181c") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 37')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 37')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 37 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.96)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M43] Add "Lens Flare 38" to Timeline track
        with uuid("bdc2a476-3097-4744-b29a-a50f93a125dc") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 38')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 38')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 38 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.96)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M44] Add "Lens Flare 39" to Timeline track
        with uuid("bbf68634-f149-43be-b068-297767e48ec6") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 39')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 39')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 39 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.96)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M45] Add "Lens Flare 40" to Timeline track
        with uuid("2f80036e-ec76-4240-b565-c846a6d1a8c2") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 40')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 40')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 40 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.96)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_14(self):
        # Insert Food.jpg
        main_page.select_library_icon_view_media('Food.jpg')
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:03:00
        main_page.set_timeline_timecode('00_00_03_00')
        time.sleep(DELAY_TIME * 2)

        # Enter (Fix/ Enhance)
        tips_area_page.click_fix_enhance()

        # Enhance > Tick (Color Adjustment)
        fix_enhance_page.enhance.enable_color_adjustment()
        time.sleep(DELAY_TIME * 2)

        # Set Brightness = -44
        fix_enhance_page.enhance.color_adjustment.brightness.adjust_slider(-44)
        time.sleep(DELAY_TIME * 2)

        default_preview = main_page.snapshot(locator=main_page.area.preview.main)
        logger(default_preview)

        # Close (Fix/Enhance) page
        fix_enhance_page.click_close()
        time.sleep(DELAY_TIME * 2)

        # Enter Effect Room > Blending Effect category
        self.enter_blending_effect()

        # [M46] Add "Lens Flare 41" to Timeline track
        with uuid("39713b9b-8b3a-49b5-9ef6-6b750196e205") as case:
            # Search library content
            media_room_page.search_library('Lens Flare 41')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 41')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 41 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.95)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M47] Add "Lens Flare 42" to Timeline track
        with uuid("2661dff4-8d6c-4567-bd02-473b53dd3f88") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 42')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 42')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 42 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.96)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M48] Add "Lens Flare 43" to Timeline track
        with uuid("aa097aae-d406-4b63-8ddc-9add769f1ec9") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 43')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 43')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 43 [NG], raise exception')
                raise Exception

            # Set timecode 00:00:01:05
            main_page.set_timeline_timecode('00_00_01_05')
            time.sleep(DELAY_TIME * 2)

            # Set timecode 00:00:03:00
            main_page.set_timeline_timecode('00_00_03_00')
            time.sleep(DELAY_TIME * 2)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.96)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M49] Add "Lens Flare 44" to Timeline track
        with uuid("8eb13aaa-031b-493b-8f16-22fca566dc43") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 44')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 44')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 44 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.96)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M50] Add "Lens Flare 45" to Timeline track
        with uuid("b8c78be1-790d-4387-bcfb-179335dc0fb2") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 45')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 45')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 45 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.98)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.93)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M51] Add "Lens Flare 46" to Timeline track
        with uuid("c647a40b-8a9e-4d8c-addb-f9bbd2579c23") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 46')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 46')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 46 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.96)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click undo
        main_page.click_undo()
        # [M52] Add "Lens Flare 47" to Timeline track
        with uuid("12776a06-8780-48fd-b8c2-2bb4c083cd55") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 47')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 47')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 47 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.94)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        main_page.click_undo()
        # [M53] Add "Lens Flare 47" to Timeline track
        with uuid("ee8c8925-1c4c-42c2-b4ca-b030d65cc76e") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Lens Flare 48')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Lens Flare 48')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Lens Flare 48 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.97)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.91)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_15(self):
        # Insert Landscape 02.jpg
        main_page.select_library_icon_view_media('Landscape 02.jpg')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()
        time.sleep(DELAY_TIME * 2)

        # Set timecode 00:00:02:16
        main_page.set_timeline_timecode('00_00_02_16')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # [M107] Add "Film Effect 04" to Timeline track
        with uuid("1c7c86d6-3553-4eac-87f1-219f539f8f4e") as case:
            # Enter Effect Room > Blending Effect category
            self.enter_blending_effect()

            # Input search Film Effect 04
            media_room_page.search_library('Film Effect 04')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Film Effect 04')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Film Effect 04 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.996)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.96)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click Undo
        main_page.click_undo()
        # [M108] Add "Film Effect 05" to Timeline track
        with uuid("19a2bd3a-0b31-4d7f-9db5-5b91e96a52db") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Film Effect 05')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Film Effect 05')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Film Effect 05 [NG], raise exception')
                raise Exception

            # Set timecode 00:00:02:04
            main_page.set_timeline_timecode('00_00_02_04')
            time.sleep(DELAY_TIME * 2)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click Undo
        main_page.click_undo()
        # [M111] Add "Film Effect 08" to Timeline track
        with uuid("5c8299f6-9fde-4a06-ad13-ccaf821731cc") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Film Effect 08')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Film Effect 08')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Film Effect 08 [NG], raise exception')
                raise Exception

            # Set timecode 00:00:03:11
            main_page.set_timeline_timecode('00_00_03_11')
            time.sleep(DELAY_TIME * 2)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.94)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.85)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click Undo
        main_page.click_undo()
        # [M104] Add "Film Effect 01" to Timeline track
        with uuid("06ccbf55-d7a4-4af1-bf28-1d3c34046bd4") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Film Effect 01')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Film Effect 01')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Film Effect 01 [NG], raise exception')
                raise Exception

            # Set timecode 00:00:02:03
            main_page.set_timeline_timecode('00_00_02_03')
            time.sleep(DELAY_TIME * 2)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.95)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click Undo
        main_page.click_undo()
        # [M118] Add "Film Effect 15" to Timeline track
        with uuid("6eb721de-232e-4536-a845-c7842d895702") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Film Effect 15')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Film Effect 15')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Film Effect 15 [NG], raise exception')
                raise Exception

            # Set timecode 00:00:00:14
            main_page.set_timeline_timecode('00_00_00_14')
            time.sleep(DELAY_TIME * 2)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.95)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_16(self):
        # Insert hastur.jpg
        video_path = Test_Material_Folder + 'fix_enhance_20/hastur.jpg'
        media_room_page.import_media_file(video_path)
        media_room_page.handle_high_definition_dialog()
        time.sleep(DELAY_TIME * 2)

        # Insert to timeline track
        main_page.tips_area_insert_media_to_selected_track()

        # Set timecode 00:00:02:16
        main_page.set_timeline_timecode('00_00_02_16')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # [M105] Add "Film Effect 02" to Timeline track
        with uuid("5404db99-4a10-4a99-b846-db36b4bce491") as case:
            # Enter Effect Room > Blending Effect category
            self.enter_blending_effect()

            # Input search Film Effect 04
            media_room_page.search_library('Film Effect 02')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Film Effect 02')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Film Effect 02 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.99)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.96)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click Undo
        main_page.click_undo()
        # [M106] Add "Film Effect 03" to Timeline track
        with uuid("46b61663-c236-494f-bb5a-332fafa973e7") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Film Effect 03')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Film Effect 03')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Film Effect 03 [NG], raise exception')
                raise Exception

            # Set timecode 00:00:00:14
            main_page.set_timeline_timecode('00_00_00_14')
            time.sleep(DELAY_TIME * 2)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.95)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)
            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click Undo
        main_page.click_undo()
        # [M109] Add "Film Effect 06" to Timeline track
        with uuid("aa23cd48-7738-4a91-a09e-024c70a358cc") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Film Effect 06')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Film Effect 06')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Film Effect 06 [NG], raise exception')
                raise Exception

            # Set timecode 00:00:01:27
            main_page.set_timeline_timecode('00_00_00_19')
            time.sleep(DELAY_TIME * 2)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.999)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.97)

            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click Undo
        main_page.click_undo()
        # [M112] Add "Film Effect 09" to Timeline track
        with uuid("23b49d71-717b-4ff0-9bc5-36568afc3931") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Film Effect 09')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Film Effect 09')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Film Effect 09 [NG], raise exception')
                raise Exception

            # Set timecode 00:00:03:13
            main_page.set_timeline_timecode('00_00_03_13')
            time.sleep(DELAY_TIME * 2)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.95)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.9)

            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click Undo
        main_page.click_undo()
        # [M113] Add "Film Effect 10" to Timeline track
        with uuid("2860edcc-bab4-451e-9ddd-3bcd921f197e") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Film Effect 10')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Film Effect 10')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Film Effect 10 [NG], raise exception')
                raise Exception

            # Set timecode 00:00:00:14
            main_page.set_timeline_timecode('00_00_00_14')
            time.sleep(DELAY_TIME * 2)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.992)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.96)

            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click Undo
        main_page.click_undo()
        # [M114] Add "Film Effect 11" to Timeline track
        with uuid("41f3e086-fdc3-4742-8ca8-733838660547") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Film Effect 11')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Film Effect 11')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Film Effect 11 [NG], raise exception')
                raise Exception

            # Set timecode 00:00:03:23
            main_page.set_timeline_timecode('00_00_03_23')
            time.sleep(DELAY_TIME * 2)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.9)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.82)

            test_result = effect_result_same and effect_result_diff
            case.result = test_result

    #  uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_17(self):
        # Insert Landscape 02.jpg
        main_page.select_library_icon_view_media('Food.jpg')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()
        time.sleep(DELAY_TIME * 2)

        # Enter (Fix/ Enhance)
        tips_area_page.click_fix_enhance()

        # Enhance > Tick (Color Adjustment)
        fix_enhance_page.enhance.enable_color_adjustment()

        # Set Brightness = -100
        fix_enhance_page.enhance.color_adjustment.brightness.adjust_slider(-100)
        time.sleep(DELAY_TIME * 2)

        default_preview = main_page.snapshot(locator=main_page.area.preview.main)
        logger(default_preview)

        # Close (Fix/Enhance) page
        fix_enhance_page.click_close()
        time.sleep(DELAY_TIME * 2)

        # Set timecode 00:00:03:19
        main_page.set_timeline_timecode('00_00_03_19')
        time.sleep(DELAY_TIME * 2)
        default_preview = main_page.snapshot(locator=L.base.Area.preview.only_mtk_view)
        logger(default_preview)

        # [M110] Add "Film Effect 07" to Timeline track
        with uuid("6eeefdb2-754c-43a0-ac4e-7a93068ded84") as case:
            # Enter Effect Room > Blending Effect category
            self.enter_blending_effect()

            # Input search Film Effect 04
            media_room_page.search_library('Film Effect 07')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Film Effect 07')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Film Effect 07 [NG], raise exception')
                raise Exception

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.9999)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.96)

            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click Undo
        main_page.click_undo()
        # [M115] Add "Film Effect 12" to Timeline track
        with uuid("41b900d6-72da-4908-82d9-5a7b317fe72f") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Film Effect 12')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Film Effect 12')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Film Effect 11 [NG], raise exception')
                raise Exception

            # Set timecode 00:00:00:28
            main_page.set_timeline_timecode('00_00_00_28')
            time.sleep(DELAY_TIME * 2)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.only_mtk_view)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.9)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.78)

            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click Undo
        main_page.click_undo()
        # [M116] Add "Film Effect 13" to Timeline track
        with uuid("cd59d8ff-a222-4ad6-b518-f54b64d67f5e") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Film Effect 13')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Film Effect 13')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Film Effect 13 [NG], raise exception')
                raise Exception

            # Set timecode 00:00:01:10
            main_page.set_timeline_timecode('00_00_01_10')
            time.sleep(DELAY_TIME * 2)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.8)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.55)

            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click Undo
        main_page.click_undo()
        # [M117] Add "Film Effect 14" to Timeline track
        with uuid("d9a43fcd-7fec-4aa8-a22c-b4fa027e7c42") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Film Effect 14')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Film Effect 14')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Film Effect 14 [NG], raise exception')
                raise Exception

            # Set timecode 00:00:01:00
            main_page.set_timeline_timecode('00_00_01_00')
            time.sleep(DELAY_TIME * 2)

            # Play preview then pause
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 2)
            playback_window_page.Edit_Timeline_PreviewOperation('Pause')
            time.sleep(DELAY_TIME * 2)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.85)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.79)

            test_result = effect_result_same and effect_result_diff
            case.result = test_result

        # Click Undo
        main_page.click_undo()
        # [M120] Add "Analog Film" to Timeline track
        with uuid("9581384e-fc2e-4979-b7f4-a9bba518cdf0") as case:
            # Search library content
            media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            media_room_page.search_library('Analog Film')
            time.sleep(DELAY_TIME * 3)

            # Drag media to timeline
            main_page.drag_media_to_timeline_playhead_position('Analog Film')
            # Check download Blending effect is completed or not
            if not self.blending_effect_download_complete():
                logger('download blending effect - Analog Film [NG], raise exception')
                raise Exception

            # Set timecode 00:00:04:18
            main_page.set_timeline_timecode('00_00_04_18')
            time.sleep(DELAY_TIME * 2)

            effect_preview = main_page.snapshot(locator=main_page.area.preview.main)
            effect_result_same = not main_page.compare(default_preview, effect_preview, similarity=0.999)
            effect_result_diff = main_page.compare(default_preview, effect_preview, similarity=0.96)

            test_result = effect_result_same and effect_result_diff
            case.result = test_result