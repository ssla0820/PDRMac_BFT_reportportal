import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time, inspect, datetime, pytest, re, configparser
os.chdir(os.path.dirname(__file__))
from types import SimpleNamespace

from ATFramework import MyReport, logger
from ATFramework.drivers.driver_factory import DriverFactory
from pages.page_factory import PageFactory
from configs.app_config import *
# import pages.media_room_page
from pages.locator import locator as L

#for update_report_info
from globals import *



# read PDR cap >>
app = SimpleNamespace(**PDR_cap)
# read PDR cap <<

# create driver & page >>
mac = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mac)
#base_page = PageFactory().get_page_object('base_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page',mac)
library_preview_page = PageFactory().get_page_object('library_preview_page',mac)
mask_designer_page = PageFactory().get_page_object('mask_designer_page', mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Library Preview Window.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<



# For Ground Truth / Test Material folder
#Ground_Truth_Folder = '/Users/cl/Desktop/MacPDR_SVN_Run/SFT/GroundTruth/Library_Preview_Window/'
#Auto_Ground_Truth_Folder = '/Users/cl/Desktop/MacPDR_SVN_Run/SFT/ATGroundTruth/Library_Preview_Window/'
#Test_Material_Folder = '/Users/cl/Desktop/MacPDR_SVN_Run/Material/'

Ground_Truth_Folder = app.ground_truth_root + '/Library_Preview_Window/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Library_Preview_Window/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Library_Preview():

    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
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
            google_sheet_execution_log_init('Library_Preview_Window')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"media room result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'),
                               report.get_ovinfo('duration'))

        report.show()





    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_1(self):
        # open library preview window
        with uuid("85891bb8-7512-4015-b172-3c13c5efee7a") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            current_result = library_preview_page.library_preview_window_exist()
            case.result = current_result

        # close library preview window
        with uuid("66ef1b40-2b60-4bbd-adc4-27f8d1407072") as case:
            with uuid("a0af6b8e-3f10-4fdf-8f05-d5d4b59bf6dd") as case:
                time.sleep(DELAY_TIME * 4)
                main_page.top_menu_bar_view_show_library_preview_window(0)
                time.sleep(DELAY_TIME * 4)
                current_result = library_preview_page.library_preview_window_exist()
                logger(current_result)
                case.result = not current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_2(self):
        # check if library preview window in menu was gray in produce page
        with uuid("16eefaf6-effa-4500-a4be-f2d2fad0c041") as case:
            with uuid("0384f316-b669-437e-a8d3-60617d511c2b") as case:
                time.sleep(DELAY_TIME * 4)
                main_page.top_menu_bar_view_show_library_preview_window()
                main_page.insert_media("Food.jpg")
                main_page.click_produce()
                current_result = not library_preview_page.library_preview_window_exist()
                current_result1 = library_preview_page.view_menu_show_library_preview_window()
                case.result = current_result and current_result1
        main_page.clear_cache()

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_3(self):
        # undock
        with uuid("4c518b18-946c-4c5c-9dbd-d6fd941e0a99") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            current_result = library_preview_page.library_preview_click_undock()
            case.result = current_result

        # close by menu bar when undock
        with uuid("fe4d44c2-52a1-4e53-bed8-4a35dc27e2ad") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window(0)
            current_result = not library_preview_page.library_preview_window_exist()
            case.result = current_result
            main_page.top_menu_bar_view_show_library_preview_window()

        # relaunch PDR when undock library preview
        with uuid("7239f3f7-74e8-434c-8907-721286354483") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.close_app()
            main_page.start_app()
            time.sleep(DELAY_TIME * 8)
            library_result = library_preview_page.snapshot(locator=L.library_preview.upper_view_region,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.3.2_Relaunch.png')
            compare_result = library_preview_page.compare(Ground_Truth_Folder + 'G3.3.2_Relaunch.png',
                                                     library_result)
            case.result = compare_result
            library_preview_page.library_preview_click_dock()
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window(0)

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_4(self):
        # dock play
        with uuid("a1e231f5-f192-408c-a416-d3a09e1b595d") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            current_result = library_preview_page.library_preview_window_preview_operation(0)
            case.result = current_result

        # dock pause by hotkey
        with uuid("3193ccce-9ac6-47f1-8c83-97763b570be8") as case:
            time.sleep(DELAY_TIME * 4)
            library_preview_page.press_space_key()
            time.sleep(DELAY_TIME * 4)
            if library_preview_page.exist(L.library_preview.dock_window.dock_window_play_btn):
                current_result = True
            else:
                current_result = False
            case.result = current_result

        # dock stop
        with uuid("859019bb-6851-4932-8636-dd1d7275c124") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = library_preview_page.library_preview_window_preview_operation(1)
            case.result = current_result

        # dock Next Frame
        with uuid("88106b16-04d2-40f1-8fc3-9d2a2610858e") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = library_preview_page.library_preview_window_preview_operation(3)
            case.result = current_result

        # dock Previous Frame
        with uuid("713f60f3-064a-4f8a-8b09-cc81339420f3") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = library_preview_page.library_preview_window_preview_operation(2)
            case.result = current_result

        # dock Next Frame by hotkey
        with uuid("da47c8b4-7fb7-4318-8b33-536e2004037a") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            library_preview_page.tap_NextFrame_hotkey()
            case.result = True

        # dock Previous Frame by hotkey
        with uuid("2ecf8d75-39d6-4161-acd1-ebebf89dfbf9") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            library_preview_page.tap_PreviousFrame_hotkey()
            case.result = True

        # dock Fast forward
        with uuid("d94dc5a7-491d-4dd5-9a5c-059c4a0547f2") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = library_preview_page.library_preview_window_preview_operation(4)
            case.result = current_result

        # dock Fast forward by hotkey
        with uuid("33c47001-96d6-4525-97bd-0b16c3e1bb46") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            library_preview_page.tap_FastForward_hotkey()
            case.result = True

        # dock Stop by hotkey
        with uuid("ca69ba7c-dff5-45ed-9d52-f9183f2fa4bc") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            library_preview_page.tap_Stop_hotkey()
            case.result = True
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window(0)

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_5(self):
        # dock snapshot
        with uuid("d4070b33-bfcd-4d4f-bd3d-bd51dd13ab20") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            library_preview_page.library_preview_window_click_take_snapshot_in_docked_window()
            time.sleep(DELAY_TIME * 4)
            library_preview_page.save_as_snapshot_filename('G3.5.0_DockSnapshot.jpg', Auto_Ground_Truth_Folder)
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.5.0_DockSnapshot.jpg',
                                                     Auto_Ground_Truth_Folder + 'G3.5.0_DockSnapshot.jpg')
            case.result = compare_result

            # dock snapshot hotkey
        with uuid("984a2d42-266f-4e4e-9ae3-f3c81a4613fa") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            library_preview_page.tap_Snapshot_hotkey()
            time.sleep(DELAY_TIME * 4)
            library_preview_page.save_as_snapshot_filename('G3.5.1_DockSnapshotHotkey.jpg', Auto_Ground_Truth_Folder)
            time.sleep(DELAY_TIME*4)
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.5.1_DockSnapshotHotkey.jpg',
                                                     Auto_Ground_Truth_Folder + 'G3.5.1_DockSnapshotHotkey.jpg')
            case.result = compare_result




    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_6(self):
        # dock volume
        with uuid("4914a709-17d3-4744-b563-3d6e55a54580") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            library_preview_page.library_preview_window_adjust_volume_in_docked_window()
            library_preview_page.library_preview_window_drag_volume_slider(0.5)
            library_result = media_room_page.snapshot(locator=L.library_preview.library_preview_window_volume_slider,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.6.0_DockVolume.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.6.0_DockVolume.png',
                                                     library_result)
            case.result = compare_result
            library_preview_page.library_preview_window_drag_volume_slider(1)


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_7(self):
        # dock mark in
        with uuid("a4f533e3-cba5-4216-95a2-55fb41a55ea6") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            library_preview_page.set_library_preview_window_timecode('00_00_01_00')
            library_preview_page.edit_library_preview_window_click_mark_in()
            library_result = media_room_page.snapshot(locator=L.library_preview.library_preview_window_slider,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.7.0_DockMarkIn.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.7.0_DockMarkIn.png',
                                                     library_result)
            case.result = compare_result

        # dock mark out
        with uuid("733dfcc9-e768-4ebf-b4ca-4d47a74f66bc") as case:
            library_preview_page.set_library_preview_window_timecode('00_00_05_00')
            library_preview_page.edit_library_preview_window_click_mark_out()
            library_result = media_room_page.snapshot(locator=L.library_preview.library_preview_window_slider,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.7.1_DockMarkOut.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.7.1_DockMarkOut.png',
                                                     library_result)
            case.result = compare_result

        # dock insert on selected track
        with uuid("a0a0b9a8-ec7a-4004-9778-c8eb32f9e785") as case:
            library_preview_page.edit_library_preview_window_click_insert_on_selected_track()
            library_result = media_room_page.snapshot(locator=library_preview_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.7.2_DockInsertOnSelectedTrack.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.7.2_DockInsertOnSelectedTrack.png',
                                                     library_result)
            case.result = compare_result

        # dock overwrite on selected track
        with uuid("8e57dcaf-6464-4c1d-9bd8-6ff6e416bd12") as case:
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            library_preview_page.edit_library_preview_window_click_overwrite_on_selected_track()
            library_result = media_room_page.snapshot(locator=library_preview_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.7.3_DockOverWriteOnSelectedTrack.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.7.3_DockOverWriteOnSelectedTrack.png',
                                                     library_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_8(self):
        # dock color board insert to timeline
        with uuid("0de2d24b-351f-4293-8450-a279a3ed2971") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            main_page.select_library_icon_view_media('0,120,255')
            library_preview_page.edit_library_preview_window_click_insert_on_selected_track()
            library_result = media_room_page.snapshot(locator=library_preview_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.8.0_DockColorBoardInsertOnSelectedTrack.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.8.0_DockColorBoardInsertOnSelectedTrack.png',
                                                     library_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_9(self):
        # dock BGM play not downloaded
        with uuid("0de2d24b-351f-4293-8450-a279a3ed2971") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_background_music()
            media_room_page.search_library('1983')
            current_result = library_preview_page.library_preview_window_preview_operation(0)
            time.sleep(DELAY_TIME * 4)
            case.result = current_result

        # dock BGM played status stop
        with uuid("08171e22-3819-41ca-bb02-2e5d37b2e5b5") as case:
            library_result = media_room_page.snapshot(locator=L.library_preview.dock_window.dock_window_stop_btn,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.9.1_DockBGMPlayedStop.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.9.1_DockBGMPlayedStop.png', library_result)
            case.result = compare_result

        # dock BGM played status previous frame
        with uuid("87bca957-e168-4b2f-947e-4d9949d68af7") as case:
            library_result = media_room_page.snapshot(locator=L.library_preview.dock_window.dock_window_previous_frame_btn,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.9.2_DockBGMPlayedPreviousFrame.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.9.2_DockBGMPlayedPreviousFrame.png', library_result)
            case.result = compare_result

        # dock BGM played status next frame
        with uuid("fe43efff-149c-4ff3-ac72-c890c75be32c") as case:
            library_result = media_room_page.snapshot(locator=L.library_preview.dock_window.dock_window_next_frame_btn,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.9.3_DockBGMPlayedNextFrame.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.9.3_DockBGMPlayedNextFrame.png', library_result)
            case.result = compare_result


        # dock BGM mark in downloaded
        with uuid("1e4b0917-96f9-4251-8eda-5a325d91bb74") as case:
            media_room_page.background_music_clip_context_menu_download('1983')
            library_preview_page.set_library_preview_window_timecode('00_00_01_00')
            library_preview_page.edit_library_preview_window_click_mark_in()
            library_result = media_room_page.snapshot(locator=L.library_preview.library_preview_window_slider,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.9.4_DockBGMMarkIn.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.9.4_DockBGMMarkIn.png',
                                                     library_result)
            case.result = compare_result

        # dock BGM add clip marker
        with uuid("8e1ded55-f6ce-4d44-bbc0-5cf2dc6750f7") as case:
            with uuid("91ef9f33-cb3c-4c9a-85da-12b24761fc21") as case:
                library_preview_page.set_library_preview_window_timecode('00_00_02_00')
                current_result1 = library_preview_page.edit_library_preview_window_add_clip_marker()
                current_result2 = library_preview_page.edit_library_preview_window_clip_marker_input_text('123abc')
                case.result = current_result1 and current_result2

        # dock BGM insert on selected track
        with uuid("6bbec4d8-5b71-437d-bace-ba9b5d3b3d16") as case:
            library_preview_page.edit_library_preview_window_click_insert_on_selected_track()
            library_result = media_room_page.snapshot(locator=library_preview_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.9.5_DockBGMInsertOnSelectedTrack.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.9.5_DockBGMInsertOnSelectedTrack.png',
                                                     library_result)
            case.result = compare_result
            media_room_page.background_music_clip_context_menu_delete_from_disk('1983')

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_10(self):
        # dock Sound clip play not downloaded
        with uuid("98852537-8fa5-44c1-be97-6f60db452926") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_sound_clips()
            time.sleep(DELAY_TIME * 5)
            media_room_page.search_library('Airplane')
            current_result = library_preview_page.library_preview_window_preview_operation(0)
            time.sleep(DELAY_TIME * 4)
            case.result = current_result

        # dock Sound clip played status stop
        with uuid("8ef7dde3-82d8-4bbf-8e81-452817fe5c11") as case:
            library_result = media_room_page.snapshot(locator=L.library_preview.dock_window.dock_window_stop_btn,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.10.1_DockSoundClipPlayedStop.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.10.1_DockSoundClipPlayedStop.png', library_result)
            case.result = compare_result

        # dock Sound clip played status previous frame
        with uuid("e85c7724-1de7-4f1a-8738-2145020bba8b") as case:
            library_result = media_room_page.snapshot(locator=L.library_preview.dock_window.dock_window_previous_frame_btn,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.10.2_DockSoundClipPlayedPreviousFrame.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.10.2_DockSoundClipPlayedPreviousFrame.png', library_result)
            case.result = compare_result

        # dock Sound clip played status next frame
        with uuid("08742f12-7bad-4458-9872-b01583fd631e") as case:
            library_result = media_room_page.snapshot(locator=L.library_preview.dock_window.dock_window_next_frame_btn,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.10.3_DockSoundClipPlayedNextFrame.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.10.3_DockSoundClipPlayedNextFrame.png', library_result)
            case.result = compare_result

        # dock Sound clip mark in downloaded
        with uuid("9077d6c1-1506-49a9-acd4-6222a3cb2eec") as case:
            media_room_page.sound_clips_clip_context_menu_download('Airplane')
            library_preview_page.set_library_preview_window_timecode('00_00_01_00')
            library_preview_page.edit_library_preview_window_click_mark_in()
            library_result = media_room_page.snapshot(locator=L.library_preview.library_preview_window_slider,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.10.4_DockSoundClipMarkIn.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.10.4_DockSoundClipMarkIn.png',
                                                     library_result)
            case.result = compare_result

        # dock Sound clip add clip marker
        with uuid("0112b746-b249-4278-b78b-e879205afef8") as case:
            library_preview_page.set_library_preview_window_timecode('00_00_02_00')
            current_result1 = library_preview_page.edit_library_preview_window_add_clip_marker()
            current_result2 = library_preview_page.edit_library_preview_window_clip_marker_input_text('123abc')
            case.result = current_result1 and current_result2

        # dock Sound clip insert on selected track
        with uuid("992b400f-a8f3-45c3-be86-367396a2c032") as case:
            library_preview_page.edit_library_preview_window_click_insert_on_selected_track()
            library_result = media_room_page.snapshot(locator=library_preview_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.10.5_DockSoundClipInsertOnSelectedTrack.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.10.5_DockSoundClipInsertOnSelectedTrack.png',
                                                     library_result)
            case.result = compare_result
            media_room_page.sound_clips_clip_context_menu_delete_from_disk('Airplane')

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_11(self):
        # dock PiP insert to timeline
        with uuid("fd725192-ecf2-46aa-9b49-b1a1e1005067") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            main_page.select_library_icon_view_media('Dialog_03')
            library_preview_page.edit_library_preview_window_click_insert_on_selected_track()
            library_result = media_room_page.snapshot(locator=library_preview_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.11.0_DockPiPInsertOnSelectedTrack.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.11.0_DockPiPInsertOnSelectedTrack.png',
                                                    library_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_12(self):
        # dock Particle insert to timeline
        with uuid("b2ee8520-a605-4dbe-ac94-aa8c487ca3cc") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(5)
            main_page.select_library_icon_view_media('Effect-A')
            library_preview_page.edit_library_preview_window_click_insert_on_selected_track()
            library_result = media_room_page.snapshot(locator=library_preview_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.12.0_DockParticleInsertOnSelectedTrack.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.12.0_DockParticleInsertOnSelectedTrack.png',
                                                    library_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_13(self):
        # dock title insert to timeline
        with uuid("a90013f2-42ec-4972-81ec-0d918f327c8f") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            main_page.select_library_icon_view_media('Default')
            library_preview_page.edit_library_preview_window_click_insert_on_selected_track()
            library_result = media_room_page.snapshot(locator=library_preview_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.13.0_DockTitleInsertOnSelectedTrack.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.13.0_DockTitleInsertOnSelectedTrack.png',
                                                    library_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_14(self):
        # dock transition gray out
        with uuid("d76b7cea-8932-44eb-8ef6-acc0ea0254dc") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(2)
            main_page.select_library_icon_view_media('Blur')
            library_result = media_room_page.snapshot(locator=L.library_preview.library_preview_window_click_insert_on_selected_track,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.14.0_DocktransitionInsertOnSelectedTrack.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.14.0_DocktransitionInsertOnSelectedTrack.png',
                                                    library_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_15(self):
        # undock
        with uuid("4c518b18-946c-4c5c-9dbd-d6fd941e0a99") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            library_preview_page.library_preview_click_undock()
            current_result = library_preview_page.get_library_preview_window_status()
            if current_result == 'Undock':
                case.result = True
            else:
                case.result = False

        # undock title
        with uuid("5f5f2480-484b-4bb0-844a-43ff8c34b524") as case:
            with uuid("754328e4-0ce0-4fcd-a0c6-9b15b79a61f9") as case:
                library_result = media_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                          file_name=Auto_Ground_Truth_Folder + 'G3.15.1_UndockTitle.png')
                compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.15.1_UndockTitle.png',
                                                        library_result)
                case.result = compare_result

        # undock maximize restore
        with uuid("9975af9f-c8eb-4f24-8c00-4cac573d9b53") as case:
            library_preview_page.library_preview_click_maximize()
            library_result1 = media_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.15.2_UndockMaximize.png')
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G3.15.2_UndockMaximize.png',
                                                     library_result1)
            library_preview_page.library_preview_click_restoredown()
            library_result2 = media_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                       file_name=Auto_Ground_Truth_Folder + 'G3.15.2_UndockRestore.png')
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'G3.15.2_UndockRestore.png',
                                                      library_result2)
            case.result = compare_result1 and compare_result2

        # undock minimize
        with uuid("ec144587-b759-47d7-9949-e96d27e92321") as case:
            with uuid("1a27e0a4-207a-41b1-94f1-ff82c68f2586") as case:
                library_preview_page.library_preview_click_minimize()
                library_result = media_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                          file_name=Auto_Ground_Truth_Folder + 'G3.15.3_UndockMinimize.png')
                compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.15.3_UndockMinimize.png',
                                                         library_result)
                case.result = compare_result

        # undock show preview window
        with uuid("88444196-ebec-4df9-a4df-027486a40a7f") as case:
            library_preview_page.library_preview_show_library_preview()
            library_result = media_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.15.4_UndockShowPreviewWindow.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.15.4_UndockShowPreviewWindow.png',
                                                     library_result)
            case.result = compare_result

        # dock
        with uuid("ee368e2d-2041-4a3f-8a75-9fb453e4720e") as case:
            library_preview_page.library_preview_window_click_dock()
            library_result = media_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.15.5_Dock.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.15.5_Dock.png',
                                                     library_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_16(self):
        # in Subtitle Room
        with uuid("9305c452-24aa-44cf-ba47-15223f41850e") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media("Food.jpg")
            main_page.enter_room(8)
            current_result = library_preview_page.view_menu_show_library_preview_window()
            case.result = current_result

        # in Audio Mixing Room
        with uuid("1db29ad9-3286-4bde-a66c-a40ba1445be2") as case:
            main_page.enter_room(6)
            current_result = library_preview_page.view_menu_show_library_preview_window()
            case.result = current_result

        # in Voice-Over Recording Room
        with uuid("6c0e2797-4b26-49a5-aff1-2eb104ef8566") as case:
            main_page.enter_room(7)
            current_result = library_preview_page.view_menu_show_library_preview_window()
            case.result = current_result

        # in SVRT Room
        with uuid("69f6e96e-a253-43e9-9f2a-b50f9412b36e") as case:
            library_preview_page.SVRTInfo_hotkey()
            current_result = library_preview_page.view_menu_show_library_preview_window()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_17(self):
        # in Fix / Enhance page
        with uuid("5cd7ad08-9281-421f-aa28-925a78ec1f6d") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media("Food.jpg")
            main_page.tips_area_click_fix_enhance()
            current_result = library_preview_page.view_menu_show_library_preview_window()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_18(self):
        # in Pan & Zoom
        with uuid("d50aca44-9dc5-4c41-827d-4a3a9e48199f") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu(4)
            time.sleep(DELAY_TIME * 2)
            current_result = library_preview_page.view_menu_show_library_preview_window()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_19(self):
        # in Keyframe room
        with uuid("ab8ffa0e-46fc-47d3-b22d-fac60596ac7e") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media("Food.jpg")
            main_page.tips_area_click_key_frame()
            time.sleep(DELAY_TIME)
            current_result = library_preview_page.view_menu_show_library_preview_window()
            case.result = current_result
            time.sleep(DELAY_TIME)

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_20(self):
        # play in 2 preview
        with uuid("180c0376-17c3-412c-830f-f6b9f996cedc") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media("Food.jpg")
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            library_preview_page.library_preview_window_preview_operation(0)
            time.sleep(DELAY_TIME)
            library_preview_page.library_preview_window_preview_operation(1)
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.20.0_2Play.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.20.0_2Play.png',
                                                     library_result)
            case.result = compare_result


        # Enter designer
        with uuid("d9c0fe17-a26b-46de-a449-7c070347ea81") as case:
            main_page.select_timeline_media('Food.jpg')
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.20.1_EnterDesigner.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.20.1_EnterDesigner.png',
                                                     library_result)
            case.result = compare_result
            #library_preview_page.library_preview_click_close_preview()

        # leave designer
        with uuid("0cfc651b-73b2-495d-8035-f77cc7f125a0") as case:
            mask_designer_page.Edit_MaskDesigner_CloseWindow()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.20.2_LeaveDesigner.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.20.2_LeaveDesigner.png',
                                                     library_result)
            case.result = compare_result
            library_preview_page.library_preview_click_close_preview()


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_21(self):
        # right click enable library preview
        with uuid("5584973a-45e9-4393-a8a2-f8538bb0d15d") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            media_room_page.library_clip_context_menu_show_in_library_preview()
            library_result = media_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.21.0_RightClickEnableLibraryPreview.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.21.0_RightClickEnableLibraryPreview.png',
                                                     library_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_22(self):
        # Relaunch PDR with dock library preview
        with uuid("5c413a8f-ea5b-47c8-b0bd-22747550b7ef") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.22.0_ReLaunchWithDockLibraryPreview.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.22.0_ReLaunchWithDockLibraryPreview.png',
                                                     library_result)
            case.result = compare_result
            library_preview_page.library_preview_click_undock()

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_23(self):
        # Relaunch PDR with Undock library preview
        with uuid("7239f3f7-74e8-434c-8907-721286354483") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 4)
            library_preview_page.library_preview_click_undock()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.23.0_ReLaunchWithUnDockLibraryPreview.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.23.0_ReLaunchWithUnDockLibraryPreview.png',
                                                     library_result)
            case.result = compare_result
            library_preview_page.library_preview_window_click_dock()
            library_preview_page.library_preview_click_close_preview()

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_3_24(self):
        # Relaunch PDR without library preview
        with uuid("449c92f2-deb8-4d96-bc6d-50f47ee9dd16") as case:
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                      file_name=Auto_Ground_Truth_Folder + 'G3.24.0_ReLaunchWithoutLibraryPreview.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G3.24.0_ReLaunchWithoutLibraryPreview.png',
                                                     library_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    c8bcc593-49a4-4318-b55c-08ff2b7ecf10
                    bfb88b7e-cac1-4739-9ef6-3e32564835a9
                    2b1ca583-2473-4c63-abdd-1e95edc427d4
                    abcbdb24-61e5-400a-a5c7-1738ca65f6be
                    d4849d3e-e53c-4c39-a433-469f9ac7173b
                    fd28b925-497f-48f4-a70c-8ff33d5ac401
                    b93404d1-4c97-4012-bd27-3df58e21a220
                    9a493a0e-eb33-44d5-ad7f-3c88f64f588c
                    829317b2-4353-4049-b11a-5d525b283721
                    7934fbaa-2299-41d1-ad23-89543f217854
                    d7a8b588-a098-4867-85c0-248c1b392ffb
                    ed2fcf56-3d35-4012-8566-7a1a9a8b3c73
                ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"




















