import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time, inspect, datetime, pytest, re, configparser
os.chdir(os.path.dirname(__file__))
from types import SimpleNamespace

from ATFramework.pages.base_page import BasePage
from ATFramework import MyReport, logger
from ATFramework.drivers.driver_factory import DriverFactory
from pages.page_factory import PageFactory
from configs.app_config import *
# import pages.media_room_page
from pages.locator import locator as L
# Modify locator to hardcode_0408
#from pages.locator.hardcode_0408 import locator as L

#for update_report_info
from globals import *


# read PDR cap >>
app = SimpleNamespace(**PDR_cap)
# read PDR cap <<

# create driver & page >>
mwc = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
effect_room_page = PageFactory().get_page_object('effect_room_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
transition_room_page = PageFactory().get_page_object('transition_room_page', mwc)
video_speed_page = PageFactory().get_page_object('video_speed_page', mwc)
#blending_mode_page = PageFactory().get_page_object('blending_mode_page',mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page',mwc)
produce_page = PageFactory().get_page_object('produce_page',mwc)
video_collage_designer_page = PageFactory().get_page_object('video_collage_designer_page',mwc)
trim_page = PageFactory().get_page_object('trim_page',mwc)
fix_enhance_page = PageFactory().get_page_object('fix_enhance_page',mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Right Cilck Menu (Timeline).html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Timeline_Right_Click_Menu/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Timeline_Right_Click_Menu/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Timeline_Right_Click_Menu():
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
            google_sheet_execution_log_init('Test_Timeline_Right_Click_Menu')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"timeline right click menu result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        with uuid('18f67ba9-d0c9-4118-aac9-8df8a31b2038') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.2 : Show SVRT track
            # Import a clip and insert to track1
            time.sleep(8)
            import_media = media_room_page.import_media_file(Test_Material_Folder + 'Timeline_Right_Click_Menu/TheIncredibles_HEVC.ts')
            logger(import_media)

            # close high definition dialogue
            time.sleep(DELAY_TIME * 2)
            media_room_page.high_definition_video_confirm_dialog_click_no()

            # insert import clip to timeline
            main_page.insert_media('TheIncredibles_HEVC.ts')

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Show SVRT track via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Show SVRT Track')
            logger(context_menu)
            time.sleep(DELAY_TIME * 15)

            # snapshot for timeline
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.2.2_Show_SVRT_Track.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.2_Show_SVRT_Track.png',
                                                     timeline_snap)
            logger(compare_result)

            # snapshot for intelligent SVRT page
            #intelligent_svrt = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                              #file_name=Auto_Ground_Truth_Folder + 'G1.2.2_SVRT_Page.png')
            #logger(f"{intelligent_svrt=}")
            #compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G1.2.2_SVRT_Page.png', intelligent_svrt)
            #logger(compare_result1)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Hide SVRT track via context menu
            main_page.right_click()
            timeline_snap1 = main_page.select_right_click_menu('Show SVRT Track')
            logger(timeline_snap1)
            time.sleep(DELAY_TIME * 2)

            # snapshot for timeline staus (after hide SVRT track)
            timeline_snap1 = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.2.2_Hide_SVRT_Track.png')
            logger(timeline_snap1)
            compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.2_Hide_SVRT_Track.png',
                                                    timeline_snap1)
            logger(compare_result2)

            # snapshot for intelligent SVRT page (need SVRT page's locator)
            #intelligent_svrt1 = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        #file_name=Auto_Ground_Truth_Folder + 'G1.2.2_SVRT_Page_after_hiding_SVRT_Track.png')
            #logger(f"{intelligent_svrt1=}")
            #compare_result3 = media_room_page.compare(Ground_Truth_Folder + 'G1.2.2_SVRT_Page_after_hiding_SVRT_Track.png', intelligent_svrt1)
            #logger(compare_result3)
            #time.sleep(DELAY_TIME)

            # back to media room
            back_to_media_room = main_page.enter_room(0)
            logger(back_to_media_room)

            case.result = compare_result and compare_result2 #and compare_result1 and compare_result3


        with uuid('8646ad17-77ca-4022-b59f-30b74f4d1128') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.4 : Show subtitle track
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Show Subtitle track via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Show Subtitle Track')
            logger(context_menu)
            time.sleep(DELAY_TIME * 5)

            # snapshot for timeline
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.4_Show_Subtitle_Track.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.4_Show_Subtitle_Track.png',
                                                    timeline_snap)
            logger(compare_result)

            # snapshot for intelligent SVRT page
            #subtitle_page = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        #file_name=Auto_Ground_Truth_Folder + 'G1.2.4_Subtitle_Page.png')
            #logger(f"{subtitle_page=}")
            #compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G1.2.4_Subtitle_Page.png', subtitle_page)
            #logger(compare_result1)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Hide Subtitle track via context menu
            main_page.right_click()
            timeline_snap1 = main_page.select_right_click_menu('Show Subtitle Track')
            logger(timeline_snap1)
            time.sleep(DELAY_TIME * 2)

            # snapshot for timeline status (after hide Subtitle track)
            timeline_snap1 = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                     file_name=Auto_Ground_Truth_Folder + 'G1.2.4_Hide_Subtitle_Track.png')
            logger(timeline_snap1)
            compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.4_Hide_Subtitle_Track.png',
                                                     timeline_snap1)
            logger(compare_result2)

            # back to media room
            back_to_media_room = main_page.enter_room(0)
            logger(back_to_media_room)

            case.result = compare_result and compare_result2


        with uuid('a33f717a-89e9-4874-9c71-eec79a35da18') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.5 : Show clip marker track
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Show Subtitle track via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Show Clip Marker Track')
            logger(context_menu)
            time.sleep(DELAY_TIME * 5)

            # snapshot for timeline
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.5_Show_Clip_Marker_Track.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.5_Show_Clip_Marker_Track.png',
                                                    timeline_snap)
            logger(compare_result)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Hide Subtitle track via context menu
            main_page.right_click()
            timeline_snap1 = main_page.select_right_click_menu('Show Clip Marker Track')
            logger(timeline_snap1)
            time.sleep(DELAY_TIME * 2)

            # snapshot for timeline status (after hide Subtitle track)
            timeline_snap1 = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                     file_name=Auto_Ground_Truth_Folder + 'G1.2.5_Hide_Clip_Marker_Track.png')
            logger(timeline_snap1)
            compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.5_Hide_Clip_Marker_Track.png',
                                                     timeline_snap1)
            logger(compare_result2)

            time.sleep(DELAY_TIME)

            # back to media room
            #back_to_media_room = main_page.enter_room(0)
            #logger(back_to_media_room)

            case.result = compare_result and compare_result2


        with uuid('be710e08-07c6-4f85-9ee2-7ea4a140c014') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.6 : Add tracks (Open Track Manager)
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Show Subtitle track via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Add Tracks...')
            #context_menu = timeline_operation_page.right_click_add_tracks()
            logger(context_menu)
            time.sleep(DELAY_TIME * 3)

            # snapshot for track manager
            track_manager = tips_area_page.snapshot(locator=L.timeline_operation.track_manager_dialog,
                                                     file_name=Auto_Ground_Truth_Folder + 'G1.2.6_Track_Manager.png')
            logger(track_manager)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.6_Track_Manager.png',
                                                     track_manager)
            logger(compare_result1)

            # Add new video & audio track
            timeline_operation_page.edit_track_manager_add_track(2, 2, 0)

            # snapshot for timeline status (after adding 2 tracks)
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                     file_name=Auto_Ground_Truth_Folder + 'G1.2.6_Add_New_Tracks.png')
            logger(timeline_snap)
            compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.6_Add_New_Tracks.png',
                                                     timeline_snap, similarity=0.9)
            logger(compare_result2)

            case.result = compare_result1 and compare_result2


        with uuid('1420ac22-9e12-4486-b39b-77d29145b601') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.8 : Remove selected tracks (by context menu)
            # Select track1
            timeline_operation_page.drag_timeline_vertical_scroll_bar(0.38)
            time.sleep(DELAY_TIME*2)
            select_track = main_page.timeline_select_track(4)
            logger(select_track)

            # remove selected track by context menu
            main_page.right_click()
            time.sleep(DELAY_TIME)
            context_menu = main_page.select_right_click_menu('Remove Track')
            logger(context_menu)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.8_Remove_Selected_Track.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.8_Remove_Selected_Track.png',
                                                     timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 10/6
        with uuid('984a1fce-d7e6-437f-949b-4c2b574965c6') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.7 : Remove empty tracks (by context menu)
            # Select track1
            timeline_operation_page.drag_timeline_vertical_scroll_bar(0)
            time.sleep(DELAY_TIME * 2)
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # remove selected track by context menu
            main_page.right_click()
            time.sleep(DELAY_TIME)
            context_menu = main_page.select_right_click_menu('Remove Empty Tracks')
            logger(context_menu)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.7_Remove_Empty_Track.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.7_Remove_Empty_Track.png',
                                                     timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 10/6
        with uuid('8f8b9953-1f00-48e7-b6f7-f4594f9a0e42') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.9 : Enable selected track only (by context menu)

            # seek to 00:00:05:00
            set_timecode = main_page.set_timeline_timecode('00_00_05_00')
            logger(set_timecode)

            # snapshot for playback window
            preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'G1.2.9_Enable_All_Tracks_PreviewWindow.png')
            logger(preview_status)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.9_Enable_All_Tracks_PreviewWindow.png',
                preview_status)
            logger(compare_result)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # remove selected track by context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Enable Selected Track Only')
            logger(context_menu)

            # snapshot for playback window
            time.sleep(2)
            preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'G1.2.9_Enable_Selected_Track_Only_PreviewWindow.png')
            logger(preview_status)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.9_Enable_Selected_Track_Only_PreviewWindow.png',
                preview_status)
            logger(compare_result1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.9_Enable_Selected_Track_Only.png')
            logger(timeline_snap)
            compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.9_Enable_Selected_Track_Only.png',
                                                     timeline_snap)
            logger(compare_result2)

            case.result = compare_result and compare_result1 and compare_result2

        #10/6
        with uuid('343e4dc0-e55e-4595-9786-c3bb8764bdbd') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.10 : Enable all tracks (by context menu)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # remove selected track by context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Enable All Tracks')
            logger(context_menu)
            time.sleep(DELAY_TIME*2)

            # snapshot for playback window
            preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'G1.2.10_Enable_All_Tracks_PreviewWindow.png')
            logger(preview_status)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.10_Enable_All_Tracks_PreviewWindow.png',
                preview_status)
            logger(compare_result1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.10_Enable_All_Tracks.png')
            logger(timeline_snap)
            compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.10_Enable_All_Tracks.png',
                                                     timeline_snap)
            logger(compare_result2)

            case.result = compare_result1 and compare_result2


        #10/6
        with uuid('9b29b9ac-1d7d-4a11-a58f-7e68cda7c5e8') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.11 : Lock/Unlock all tracks (by context menu)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Lock all tracks by context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Lock/Unlock All Tracks')
            logger(context_menu)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.11_Lock_All_Tracks.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.11_Lock_All_Tracks.png',
                                                     timeline_snap)
            logger(compare_result1)

            # left click on track header of track#1
            timeline_operation_page.exist_click(L.timeline_operation.timeline_video_track1)

            # Unlock all tracks by context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Lock/Unlock All Tracks')
            logger(context_menu)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.11_Unlock_All_Tracks.png')
            logger(timeline_snap)
            compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.11_Unlock_All_Tracks.png',
                                                     timeline_snap)
            logger(compare_result2)

            case.result = compare_result1 and compare_result2

        #10/6
        with uuid('545cfd94-581f-4da6-98e8-02ecf1cd55fd') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.12 : Set all video track height to large (by context menu)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Lock all tracks by context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Adjust Video Track Height', 'Large')
            logger(context_menu)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.12.3_Video_Track_Height_Large.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.12.3_Video_Track_Height_Large.png',
                                                     timeline_snap)
            logger(compare_result1)

            # save as new project
            custom_path = Test_Material_Folder+'/Timeline_Right_Click_Menu/track_height.pds'
            if main_page.exist_file(custom_path):
                main_page.delete_folder(custom_path)
                time.sleep(0.5)

            save_project = main_page.save_project('track_height', Test_Material_Folder+'/Timeline_Right_Click_Menu/')
            logger(save_project)

            # new project (by hotkey)
            #new_project = main_page.tap_CreateNewProject_hotkey()
            #logger(new_project)

            # open saved project
            #Setcheck_result = main_page.top_menu_bar_file_open_recent_projects(Test_Material_Folder + 'track_height')
            #case.result = Setcheck_result
            #main_page.handle_merge_media_to_current_library_dialog('No', 'No')

            # Check test result
            case.result = compare_result1 #and compare_result2


        #10/6
        with uuid('9f777db8-782a-4e4f-92b9-76b56b9af8fe') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.12.1 : Set all video track height to small (by context menu)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Lock all tracks by context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Adjust Video Track Height', 'Small')
            logger(context_menu)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.12.1_Video_Track_Height_Small.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.12.1_Video_Track_Height_Small.png',
                                                     timeline_snap)
            logger(compare_result1)

            case.result = compare_result1


        # 10/6
        with uuid('20f3f0d2-b78b-4f8a-b3cd-780c1208b479') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.12.2 : Set all video track height to medium (by context menu)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Lock all tracks by context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Adjust Video Track Height', 'Medium')
            logger(context_menu)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.12.2_Video_Track_Height_Medium.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.12.2_Video_Track_Height_Medium.png',
                                                     timeline_snap)
            logger(compare_result1)

            case.result = compare_result1


        # 10/8
        with uuid('eda5775d-0a74-4956-82dd-b335f87076a3') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.13.3 : Set all audio track height to large (by context menu)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Lock all tracks by context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Adjust Audio Track Height', 'Large')
            logger(context_menu)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.13.3_Audio_Track_Height_Large.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.13.3_Audio_Track_Height_Large.png',
                                                     timeline_snap)
            logger(compare_result1)

            # save as new project
            #save_project = main_page.save_project('audio_track_height', Test_Material_Folder)
            #logger(save_project)

            # new project (by hotkey)
            # new_project = main_page.tap_CreateNewProject_hotkey()
            # logger(new_project)

            # open saved project
            # Setcheck_result = main_page.top_menu_bar_file_open_recent_projects(Test_Material_Folder + 'track_height')
            # case.result = Setcheck_result
            # main_page.handle_merge_media_to_current_library_dialog('No', 'No')

            # Check test result
            case.result = compare_result1

        # 10/8
        with uuid('c5e84bf7-5da5-4075-82bb-5ef897f37bda') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.13.1 : Set all audio track height to small (by context menu)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Lock all tracks by context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Adjust Audio Track Height', 'Small')
            logger(context_menu)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.2.13.1_Audio_Track_Height_Small.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.13.1_Audio_Track_Height_Small.png',
                                                         timeline_snap)
            logger(compare_result1)

            case.result = compare_result1

        # 10/8
        with uuid('968430d6-a778-4c4c-bab2-015f51b83205') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.13.2 : Set all audio track height to medium (by context menu)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Lock all tracks by context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Adjust Audio Track Height', 'Medium')
            logger(context_menu)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.2.13.2_Audio_Track_Height_Medium.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.13.2_Audio_Track_Height_Medium.png',
                                                         timeline_snap)
            logger(compare_result1)

            case.result = compare_result1

        # 10/8
        with uuid('a7dfb3bf-59c8-4860-8f90-ea320bbc2b56') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.17.1 : dock / undock timeline window (by context menu)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Undock timeline by context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Dock/Undock Timeline Window')
            logger(context_menu)

            # snapshot for timeline status

            # Dock timeline by context menu
            main_page.timeline_select_track(1)
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Dock/Undock Timeline Window')
            logger(context_menu)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.17.1_Dock_Timeline.png')
            logger(timeline_snap)
            compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.17.1_Dock_Timeline.png', timeline_snap)
            logger(compare_result2)

            case.result = compare_result1 and compare_result2


        # 10/8
        with uuid('bde189cd-febb-4b17-a321-d1fed94e686d') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.18 : Reset all undocked windows (by context menu)
            # select library clip
            media_room_page.hover_library_media('Food.jpg')

            # Undock library by context menu
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Dock/Undock Library Window')
            logger(context_menu1)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Undock timeline by context menu
            main_page.right_click()
            context_menu2 = main_page.select_right_click_menu('Dock/Undock Timeline Window')
            logger(context_menu2)

            # Undock timeline by context menu
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Reset All Undocked Windows')
            logger(context_menu)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.18_Docked_Timeline.png')
            logger(timeline_snap)
            compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.18_Docked_Timeline.png', timeline_snap)
            logger(compare_result2)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.18_Docked_Library.png')
            logger(timeline_snap)
            compare_result3 = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.18_Docked_Library.png', timeline_snap)
            logger(compare_result3)

            case.result = compare_result1 and compare_result2 and compare_result3


        # 10/14
        with uuid('47142e5d-4f7d-4ca3-aafc-c7c26b40e5c0') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.14 : Trigger "Copy Track Content to…" (by context menu)

            # Select track3
            select_track = main_page.timeline_select_track(3)
            logger(select_track)

            # right click on selected track and then copy content to another track
            copy_track = timeline_operation_page.right_click_menu_CopyTrackContent_to(3,'Above track 2', 'OK')
            logger(copy_track)
            time.sleep(DELAY_TIME*5)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.14_Copy_Track_Content.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.14_Copy_Track_Content.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result


        # 10/14
        with uuid('8bb8350c-dd66-407e-aedf-d073db810ef3') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.15 : Trigger "Move Track Content to…" (by context menu)

            # Select track3
            #select_track = main_page.timeline_select_track(3)
            #logger(select_track)

            # right click on selected track and then copy content to another track
            timeline_operation_page.right_click_menu_MoveTrackContent_to(2,'Above track 1', 'OK')

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.15_Move_Track_Content.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.2.15_Move_Track_Content.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result



    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        #10/8
        with uuid('3209ac28-418b-40cd-b374-2be2b68b4473') as case:
            # session 1.3 : Right click on PiP object (Image/Video/Audio/Slideshow/Virtual Cut/Color board)
            # case1.3.1 : Cut -> Cut and leave gap
            # Import a clip and insert to track1
            time.sleep(8)
            import_media = media_room_page.import_media_file(Test_Material_Folder + 'Timeline_Right_Click_Menu/TheIncredibles_HEVC.ts')
            logger(import_media)

            # close high definition dialogue
            time.sleep(DELAY_TIME * 2)
            if main_page.is_exist(L.media_room.confirm_dialog.main) == True:
                media_room_page.high_definition_video_confirm_dialog_click_no()

            # insert import clip to timeline
            main_page.insert_media('TheIncredibles_HEVC.ts')

            # seek to 00:01:10:23
            set_timecode = main_page.set_timeline_timecode('00_01_10_23')
            logger(set_timecode)

            # select one of library media and insert to track1
            #media_room_page.hover_library_media('Sport 01.jpg')
            main_page.select_library_icon_view_media('Sport 01.jpg')
            main_page.insert_media('Sport 01.jpg')

            # select one of library media and insert to track1
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # seek to 00:01:10:23
            set_timecode = main_page.set_timeline_timecode('00_01_20_23')
            logger(set_timecode)

            # select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select one of library media and insert to track1
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.insert_media('Skateboard 01.mp4')

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Cut "Food.jpg" and leave gap
            main_page.select_timeline_media('Food.jpg')
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Cut', 'Cut and Leave Gap')
            logger(context_menu1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.1_Cut&LeaveGap.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.1_Cut&LeaveGap.png', timeline_snap)
            logger(compare_result1)

            case.result = compare_result1


        #10/8
        with uuid('f2367b35-07a8-4575-9556-f44a090c5e3e') as case:
            # session 1.3 : Right click on PiP object (Image/Video/Audio/Slideshow/Virtual Cut/Color board)
            # case1.3.2 : Cut -> Cut and fill gap
            # undo change
            main_page.tap_Undo_hotkey()

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Cut "Food.jpg" and leave gap
            main_page.select_timeline_media('Food.jpg')
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Cut', 'Cut and Fill Gap')
            logger(context_menu1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.2_Cut&FillGap.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.2_Cut&FillGap.png', timeline_snap)
            logger(compare_result1)

            case.result = compare_result1


        #10/8
        with uuid('6c44126f-59b7-428d-9ce5-9f65db516598') as case:
            # session 1.3 : Right click on PiP object (Image/Video/Audio/Slideshow/Virtual Cut/Color board)
            # case1.3.3 : Cut -> Cut, Fill Gap and Move All Clips
            # undo change
            main_page.tap_Undo_hotkey()

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Cut "Food.jpg" and leave gap
            main_page.select_timeline_media('Food.jpg')
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Cut', 'Cut, Fill Gap, and Move All Clips')
            logger(context_menu1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.2_Cut&FillGap.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.2_Cut&FillGap.png', timeline_snap)
            logger(compare_result1)

            case.result = compare_result1


        #10/14
        with uuid('47f4e0aa-98a6-4b82-adc3-10c50d5d80a0') as case:
            # session 1.3 : Right click on PiP object (Image/Video/Audio/Slideshow/Virtual Cut/Color board)
            # case1.3.4.4 : Paste and Insert

            # Select and copy timeline object
            main_page.select_timeline_media('Sport 01.jpg')
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Paste', 'Paste and Insert')
            logger(context_menu1)
            time.sleep(DELAY_TIME*2)

            check_result = main_page.select_timeline_media('Food.jpg')
            logger(check_result)
            main_page.move_mouse_to_0_0()

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.4.4_Paste_and_Insert.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.4.4_Paste_and_Insert.png', timeline_snap)
            logger(compare_result)

            case.result = check_result and compare_result


        #10/14
        with uuid('8bab5b8d-80c5-409f-873e-69c366c6f0ce') as case:
            # session 1.3 : Right click on PiP object (Image/Video/Audio/Slideshow/Virtual Cut/Color board)
            # case1.3.2 : Copy PiP object

            # Select and copy timeline object
            main_page.select_timeline_media('TheIncredibles_HEVC.ts')
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Copy')
            logger(context_menu1)
            time.sleep(DELAY_TIME * 2)

            with uuid('3b600164-0adb-4a9a-8770-31b52c1a1be8') as case:
                # case1.3.4.1 : Paste and Overwrite
                # select another timeline clip
                main_page.select_timeline_media('Food.jpg')
                main_page.right_click()
                time.sleep(DELAY_TIME*1.5)
                main_page.select_right_click_menu('Paste')
                time.sleep(DELAY_TIME)
                main_page.click({"AXRole": "AXMenuItem", "AXIdentifier": 'IDM_INSERT_CHOICE_OVERWRITE'})


                # snapshot for timeline status
                timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.3.4.1_Paste_and_Overwrite.png')
                logger(timeline_snap)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.4.1_Paste_and_Overwrite.png',
                                                        timeline_snap)
                logger(compare_result)

                case.result = compare_result

            case.result = compare_result


    # @pytest.mark.skip
    #@exception_screenshot
    #def test_1_1_2_1(self):

        # 10/15
        with uuid('52c9529f-7370-4c89-8e87-8e3c74ea7cdd') as case:
            # session 1.3 : Right click on PiP object (Image/Video/Audio/Slideshow/Virtual Cut/Color board)
            # case1.3.4.2 : Paste -> Paste and Trim to Fit
            # undo change
            main_page.tap_Undo_hotkey()

            # Cut "Food.jpg" and leave gap
            main_page.select_timeline_media('Food.jpg')
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Cut', 'Cut and Leave Gap')
            logger(context_menu1)

            # copy timeline video
            main_page.select_timeline_media('TheIncredibles_HEVC.ts')
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Copy')
            logger(context_menu1)

            # seek to 00:01:10:23
            set_timecode = main_page.set_timeline_timecode('00_01_10_23')
            logger(set_timecode)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(0)

            # paste and trim to fit
            main_page.right_click()
            #time.sleep(DELAY_TIME*2)
            context_menu2 = main_page.select_right_click_menu('Paste', 'Paste and Trim to Fit')
            logger(context_menu2)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.4.2_Paste_and_Trim_to_Fit.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.4.2_Paste_and_Trim_to_Fit.png',
                                                    timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 10/15-1
        with uuid('e698e99f-fb44-44d3-b2fb-60b275cdd7ea') as case:
            # session 1.3 : Right click on PiP object (Image/Video/Audio/Slideshow/Virtual Cut/Color board)
            # case1.3.4.3 : Paste -> Paste and Speed up to Fit
            # seek to 00:01:10:23
            main_page.tap_Undo_hotkey()
            time.sleep(DELAY_TIME)

            set_timecode = main_page.set_timeline_timecode('00_01_10_23')
            logger(set_timecode)

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(0)

            # paste and trim to fit
            main_page.right_click()
            time.sleep(DELAY_TIME * 2)
            main_page.select_right_click_menu('Paste', 'Paste and Speed up to Fit')
            time.sleep(DELAY_TIME)
            #main_page.click({"AXRole": "AXMenuItem", "AXIdentifier": 'IDM_INSERT_CHOICE_SPEED_UP_TO_FIT'})

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.4.3_Paste_and_Speed_up_to_Fit.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.4.3_Paste_and_Speed_up_to_Fit.png',
                                                    timeline_snap)
            logger(compare_result)

            case.result = compare_result


        # 10/15-2
        with uuid('8874494d-c96e-48e6-9cb8-803aa4308eac') as case:
            # session 1.3 : Right click on PiP object (Image/Video/Audio/Slideshow/Virtual Cut/Color board)
            # case1.3.4.5 : Paste -> Paste, Insert, and Move All Clips
            # undo change
            time.sleep(DELAY_TIME*2)
            main_page.tap_Undo_hotkey()

            # seek to 00:01:10:23
            time.sleep(DELAY_TIME * 2)
            set_timecode = main_page.set_timeline_timecode('00_01_10_23')
            logger(set_timecode)

            # select track1
            time.sleep(DELAY_TIME * 2)
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(0)

            # paste and trim to fit
            main_page.right_click()
            time.sleep(DELAY_TIME * 2)
            main_page.select_right_click_menu('Paste')
            time.sleep(DELAY_TIME)
            main_page.click({"AXRole": "AXMenuItem", "AXIdentifier": 'IDM_INSERT_CHOICE_INSERT_AND_MOVE_ALL_CLIPS'})

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.4.5_Paste_Insert_and_MoveAllClips.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.4.5_Paste_Insert_and_MoveAllClips.png',
                                                    timeline_snap)
            logger(compare_result)

            case.result = compare_result


        # 10/20
        with uuid('42fb084d-f85a-402c-b6cf-5ba9f50a8291') as case:
            # session 1.3 : Right click on PiP object (Image/Video/Audio/Slideshow/Virtual Cut/Color board)
            # case1.3.4.6 : Paste -> Crossfade
            # undo change
            main_page.tap_Undo_hotkey()

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # copy timeline video
            main_page.select_timeline_media('TheIncredibles_HEVC.ts')
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Copy')
            logger(context_menu1)

            # seek to 00:01:00:23
            set_timecode = main_page.set_timeline_timecode('00_01_00_23')
            logger(set_timecode)

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            #main_page.select_timeline_media('TheIncredibles_HEVC.ts')
            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(0)

            # Paste copied video with crossfade
            main_page.right_click()
            main_page.select_right_click_menu('Paste')
            time.sleep(DELAY_TIME)
            main_page.click({"AXRole": "AXMenuItem", "AXIdentifier": 'IDM_INSERT_CHOICE_CROSSFADE'})
            time.sleep(DELAY_TIME*2)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.4.6_Paste_Crossfade.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.4.6_Paste_Crossfade.png',
                                                    timeline_snap)
            logger(compare_result)

            case.result = compare_result




    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        # 10/15
        with uuid('7770bf79-e5a3-46fe-90e0-93872ec504fa') as case:
            # case1.3.6 : Remove selected item
            # Import a clip and insert to track1
            time.sleep(8)
            import_media = media_room_page.import_media_file(Test_Material_Folder + 'Timeline_Right_Click_Menu/TheIncredibles_HEVC.ts')
            logger(import_media)

            # close high definition dialogue
            time.sleep(DELAY_TIME * 2)
            if main_page.is_exist(L.media_room.confirm_dialog.main) == True:
                media_room_page.high_definition_video_confirm_dialog_click_no()
            #media_room_page.high_definition_video_confirm_dialog_click_no()

            # insert import clip to timeline
            main_page.insert_media('TheIncredibles_HEVC.ts')

            # seek to 00:01:10:23
            set_timecode = main_page.set_timeline_timecode('00_01_10_23')
            logger(set_timecode)

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select one of library media and insert to track1
            # media_room_page.hover_library_media('Sport 01.jpg')
            main_page.select_library_icon_view_media('Sport 01.jpg')
            main_page.insert_media('Sport 01.jpg')

            # select one of library media and insert to track1
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # seek to 00:01:10:23
            set_timecode = main_page.set_timeline_timecode('00_01_20_23')
            logger(set_timecode)

            # select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select one of library media and insert to track2
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.insert_media('Skateboard 01.mp4')

            # select track2 & timeline video
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            main_page.select_timeline_media('Skateboard 01.mp4')

            # remove inserted video of track2
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Remove')
            logger(context_menu1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.6_Remove_selected_clip_from_timeline.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.6_Remove_selected_clip_from_timeline.png',
                                                    timeline_snap)
            logger(compare_result)

            case.result = compare_result


        # 10/15
        with uuid('fb34c530-3258-4733-9f8c-126bb944e9d0') as case:
            # case1.3.8 : Link/Unlink Video and Audio
            # Select video in track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            main_page.select_timeline_media('TheIncredibles_HEVC.ts')

            # unlink video and audio
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Link/Unlink Video and Audio')
            logger(context_menu1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.8_Unlink_Video_Audio.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.3.8_Unlink_Video_Audio.png',
                timeline_snap)
            logger(compare_result)

            # select video in track1 and link video & audio back
            main_page.select_timeline_media('TheIncredibles_HEVC.ts')

            # link video and audio
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Link/Unlink Video and Audio')
            logger(context_menu1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.8_Link_Video_Audio.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.3.8_Link_Video_Audio.png',
                timeline_snap)
            logger(compare_result1)

            case.result = compare_result and compare_result1


        # 10/15
        with uuid('ee695401-7c41-460c-9d7e-ba4ae9da63ff') as case:
            # case1.3.10 : Split object
            # Split object
            # seek to 00:00:20:00
            set_timecode = main_page.set_timeline_timecode('00_00_20_00')
            logger(set_timecode)

            # Select video in track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            main_page.select_timeline_media('TheIncredibles_HEVC.ts')

            # unlink video and audio
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Split')
            logger(context_menu1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.10_Split_Video.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.3.10_Split_Video.png',
                timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 10/15
        with uuid('69ef7d8c-c690-4bfb-a7bc-ae4c16b43fbc') as case:
            # case1.3.14 : Mute selected clip
            # undo change
            main_page.tap_Undo_hotkey()

            # Select video in track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            main_page.select_timeline_media('TheIncredibles_HEVC.ts')

            # Mute audio
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Mute Clip')
            logger(context_menu1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.14_Mute_Audio.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.3.14_Mute_Audio.png',
                timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 10/20
        with uuid('61182a1f-8c3c-45cd-ba45-af0b74b6bfa4') as case:
            # case1.3.17 : Normalize selected Audio
            # Insert an audio clip to track2

            # Select video in track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # Insert an audio to track2
            main_page.select_library_icon_view_media('Mahoroba.mp3')
            main_page.insert_media('Mahoroba.mp3')

            # Select video and audio clips on timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            timeline_operation_page.select_multiple_timeline_media(0,0,3,0) #select_multiple_timeline_media(self, media1_track_index, media1_clip_index, media2_track_index, media2_clip_index)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.17_Before_Normalize_Audio.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.3.17_Before_Normalize_Audio.png',
                timeline_snap)
            logger(compare_result)

            # Normalize audio
            main_page.select_timeline_media('Mahoroba.mp3')
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Normalize Audio') # may need one page function to detect progress bar
            logger(context_menu1)
            time.sleep(DELAY_TIME*5)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.17_After_Normalize_Audio.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.3.17_After_Normalize_Audio.png',
                timeline_snap)
            logger(compare_result1)

            case.result = compare_result and compare_result1

        # 10/20
        with uuid('3e62cf59-3e22-4bc4-9b64-8bd95428da60') as case:
            # case1.3.7 : Select all timeline clips
            # Select video in track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            main_page.select_timeline_media('TheIncredibles_HEVC.ts')

            # Select All timeline clips
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Select All')
            logger(context_menu1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.7_Select_All.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.3.7_Select_All.png',
                timeline_snap)
            logger(compare_result1)

            case.result = compare_result

        # 10/20
        with uuid('f1c8ba1a-ede1-4285-8843-78671fdc3312') as case:
            # case1.3.9 : Group or ungroup selected objects
            # Select video in track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            main_page.select_timeline_media('TheIncredibles_HEVC.ts')

            # Select All timeline clips
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Select All')
            logger(context_menu1)

            # Select video in track1
            #select_track = main_page.timeline_select_track(1)
            #logger(select_track)
            #main_page.select_timeline_media('TheIncredibles_HEVC.ts')

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(0)

            # Group all timeline clips
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Group/Ungroup Objects')
            logger(context_menu1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.9_Group_Objects.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.3.9_Group_Objects.png',
                timeline_snap)
            logger(compare_result1)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(0)

            # Ungroup all timeline clips
            main_page.right_click()
            context_menu1 = main_page.select_right_click_menu('Group/Ungroup Objects')
            logger(context_menu1)

            case.result = compare_result

        # 10/21
        with uuid('8c556932-0592-43dc-af66-651001b83bd2') as case:
            # case1.3.20.1 : Enter "Trim" page by context menu

            # select track1 & specific video
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            main_page.select_timeline_media('TheIncredibles_HEVC.ts')

            # Enter "Trim" page
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit Video', 'Trim...')
            logger(context_menu)
            time.sleep(DELAY_TIME*2)

            # check if enter "Trim" page correctly
            result = trim_page.check_in_Trim()
            logger(result)

            # exit Trim page by ESC key
            trim_page.press_esc_key()

            case.result = result

        # 10/21
        with uuid('02fea718-2b04-4f55-a2ee-1fa06be329e6') as case:
            # case1.3.20.7 : Enter "Fix/Enhance" page by context menu
            # select track1 & specific video
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            main_page.select_timeline_media('TheIncredibles_HEVC.ts')

            # Enter "Fix / Enhance" page
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit Video', 'Fix / Enhance')
            logger(context_menu)
            time.sleep(DELAY_TIME * 1)

            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")

            # Compare image of preview window
            current_result = media_room_page.snapshot(locator=L.fix_enhance.fix.frame_video_stabilizer,
                                                      file_name=Auto_Ground_Truth_Folder + '1.3.20.7_fix_enhance_video_stabilizer.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1.3.20.7_fix_enhance_video_stabilizer.png',
                                                     current_result)
            logger(f"{compare_result= }")
            case.result = compare_result and is_in_fix_enhance

        # 10/21
        with uuid('7d178322-1b96-4d46-bc8f-2a951c6d0581') as case:
            # case1.3.20.9 : Enable fade in and fade out by context menu
            # select track1 & specific video
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            main_page.select_timeline_media('TheIncredibles_HEVC.ts')

            # Enable fade in and fade out
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit Video', 'Enable Fade-in and Fade-out')
            logger(context_menu)
            time.sleep(DELAY_TIME * 1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.20.9_Enable_FadeIn_FadeOut.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.3.20.9_Enable_FadeIn_FadeOut.png',
                timeline_snap)
            logger(compare_result1)

            with uuid('6c728427-f834-42d7-87f3-fac3f995d4a8') as case:
                # case1.3.20.10 : Restore to original opacity level by context menu
                # select track1 & specific video
                select_track = main_page.timeline_select_track(1)
                logger(select_track)
                main_page.select_timeline_media('TheIncredibles_HEVC.ts')

                # Enable fade in and fade out
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Edit Video', 'Restore to Original Opacity Level')
                logger(context_menu)
                time.sleep(DELAY_TIME * 1)

                # snapshot for timeline status
                timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.3.20.10_Restore_to_Original_Opacity_Level.png')
                logger(timeline_snap)
                compare_result2 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.3.20.10_Restore_to_Original_Opacity_Level.png',
                    timeline_snap)
                logger(compare_result2)

                case.result = compare_result2

            case.result = compare_result1

        # 10/22
        with uuid('397399cf-c119-4e4c-8d9b-d0bc79a9de87') as case:
            # case1.3.21.1 : Edit image -> Crop image
            # select track1 & specific image
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            main_page.select_timeline_media('Food.jpg')

            # Enable Crop Image
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit Image', 'Crop Image')
            logger(context_menu)
            time.sleep(DELAY_TIME * 2)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.tips_area.window.crop_image ,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.21.1_Crop_Image.png') #need to replace with new locator
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.21.1_Crop_Image.png', timeline_snap)
            logger(compare_result)

            # exit Crop Image page by ESC key
            trim_page.press_esc_key()

            case.result = compare_result

        # 10/22
        with uuid('a9655d4e-6ab1-494f-8a8a-6adc8c06acc6') as case:
            # case1.3.21.4 : Edit image -> Pan & Zoom
            # select track1 & specific image
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            main_page.select_timeline_media('Food.jpg')

            # Enter Pan & Zoom
            main_page.right_click()
            time.sleep(DELAY_TIME)
            context_menu = main_page.select_right_click_menu('Edit Image', 'Pan & Zoom')
            logger(context_menu)
            time.sleep(DELAY_TIME * 2)

            # snapshot
            timeline_snap = tips_area_page.snapshot(locator=L.pan_zoom.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.21.4_Pan_Zoom.png')  # need to replace with new locator
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.3.21.4_Pan_Zoom.png',
                timeline_snap, similarity=0.8)
            logger(compare_result)

            # close Pan & Zoom page by switching to timeline video
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            main_page.select_timeline_media('TheIncredibles_HEVC.ts')

            case.result = compare_result #and compare_result1

        # 10/22
        with uuid('268ec41d-0892-4803-99a6-0c2e72c6b50a') as case:
            # case1.3.21.5 : Edit image -> Fix / Enhance
            # select track1 & specific image
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            main_page.select_timeline_media('Food.jpg')

            # Enable fade in and fade out
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit Image', 'Fix / Enhance')
            logger(context_menu)
            time.sleep(DELAY_TIME * 1)

            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")

            # Compare image of preview window
            current_result = media_room_page.snapshot(locator=L.fix_enhance.fix.frame_white_balance,
                                                      file_name=Auto_Ground_Truth_Folder + '1.3.21.5_fix_enhance_WB.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1.3.21.5_fix_enhance_WB.png',
                                                     current_result)
            logger(f"{compare_result= }")
            case.result = compare_result and is_in_fix_enhance

        # 10/22
        with uuid('8a626d38-fb05-49ed-8246-06efb9056f17') as case:
            # case1.3.21.7 : Enable fade in and fade out by context menu
            # select track1 & specific image
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            main_page.select_timeline_media('Food.jpg')

            # Enable fade in and fade out
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit Image', 'Enable Fade-in and Fade-out')
            logger(context_menu)
            time.sleep(DELAY_TIME * 1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.21.7_Image_Enable_FadeIn_FadeOut.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.3.21.7_Image_Enable_FadeIn_FadeOut.png',
                timeline_snap)
            logger(compare_result1)

            with uuid('aeb8e6f6-f8f6-4d0c-82de-d837f4b88870') as case:
                # case1.3.21.8 : Restore to original opacity level by context menu
                # select track1 & specific image
                select_track = main_page.timeline_select_track(1)
                logger(select_track)
                main_page.select_timeline_media('Food.jpg')

                # Enable fade in and fade out
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Edit Image', 'Restore to Original Opacity Level')
                logger(context_menu)
                time.sleep(DELAY_TIME * 1)

                # snapshot for timeline status
                timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.3.21.8_Image_Restore_to_Original_Opacity_Level.png')
                logger(timeline_snap)
                compare_result2 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.3.21.8_Image_Restore_to_Original_Opacity_Level.png',
                    timeline_snap)
                logger(compare_result2)

                case.result = compare_result2

            case.result = compare_result1

        # 10/22
        with uuid('0c25302a-67fa-43ca-a872-d1b1451a628e') as case:
            # case1.3.23.3 : Edit Clip Keyframe > Clip Attributes
            # select track1 & specific video
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            main_page.select_timeline_media('TheIncredibles_HEVC.ts')

            # Trigger Edit Clip Keyframe > Clip Attributes
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit Clip Keyframe', 'Clip Attributes')
            logger(context_menu)
            time.sleep(DELAY_TIME * 1)

            # snapshot
            timeline_snap = tips_area_page.snapshot(locator=L.keyframe_room.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.23.3_Keyframe_Room_Clip_Attributes.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.3.23.3_Keyframe_Room_Clip_Attributes.png',
                timeline_snap)
            logger(compare_result)

            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        # 10/28
        with uuid('767d240d-0538-4310-bfda-b116e2572467') as case:
            # case1.3.23.2 : Edit Clip Keyframe > Effects
            # Insert a video / image to track1
            # select track1
            time.sleep(8)
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select one of library media and insert to track1
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.insert_media('Skateboard 01.mp4')

            # select one of library media and insert to track1
            main_page.select_library_icon_view_media('Food.jpg')
            #main_page.insert_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)

            # switch to effect room
            main_page.enter_room(3)
            time.sleep(5)
            effect_room_page.search_and_input_text('pop')
            main_page.select_library_icon_view_media('Pop Art Wall')
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Apply Selected Effect to All Clips on Selected Track')
            logger(context_menu)

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select timeline object
            main_page.select_timeline_media('Skateboard 01.mp4')

            # Trigger Edit Clip Keyframe > Effects
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit Clip Keyframe', 'Effects')
            logger(context_menu)
            time.sleep(DELAY_TIME * 2)

            # snapshot
            timeline_snap = tips_area_page.snapshot(locator=L.keyframe_room.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.23.2_Keyframe_Room_Effects.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.23.2_Keyframe_Room_Effects.png',timeline_snap)
            logger(compare_result)
            case.result = compare_result

        # 10/28
        with uuid('3e333c08-344e-4721-aba0-460e5cbfa7a6') as case:
            # case1.3.23.4 : Edit Clip Keyframe > Volume
            # select track1
            time.sleep(8)
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select timeline video
            main_page.select_timeline_media('Skateboard 01.mp4')

            # Trigger Edit Clip Keyframe > Effects
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit Clip Keyframe', 'Volume')
            logger(context_menu)
            time.sleep(DELAY_TIME * 2)

            # snapshot
            timeline_snap = tips_area_page.snapshot(locator=L.keyframe_room.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.23.4_Keyframe_Room_Volume.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.23.4_Keyframe_Room_Volume.png',timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 10/28
        with uuid('dac328c6-3d4b-4e44-ab92-f06a378feebb') as case:
            # case1.3.24.1 : Set Clip Attributes > Video > Set Aspect Ratio…
            # select track1
            time.sleep(8)
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select timeline video
            main_page.select_timeline_media('Skateboard 01.mp4')

            # Trigger Edit Clip Attributes > Set Aspect Ratio
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Aspect Ratio...')
            logger(context_menu)
            time.sleep(DELAY_TIME * 5)

            # snapshot
            timeline_snap = tips_area_page.snapshot(locator=L.tips_area.button.more_features.clip_aspect_ratio.detect_aspect_ratio,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.24.1_Set_Aspect_Ratio.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.24.1_Set_Aspect_Ratio.png',timeline_snap)
            logger(compare_result)

            # Apply the settings of aspect ratio dialogue
            # tips_area_page.more_features.edit_clip_aspect_ratio_settings() --> exception

            # exit by ESC key
            main_page.press_esc_key()

            case.result = compare_result



        # 10/28
        with uuid('55e6ff42-d1e8-42eb-af9f-f40242fda7e6') as case:
            # case1.3.24.2 : Set Clip Attributes > Video > Set blending mode…
            # select track2
            time.sleep(3)
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # Enter Media Library
            main_page.enter_room(0)
            time.sleep(5)

            # select and insert a clip to track2
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.insert_media('Skateboard 02.mp4')

            # select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # seek to 00:01:00:23
            set_timecode = main_page.set_timeline_timecode('00_00_00_00')
            logger(set_timecode)

            # select and insert a clip to track2
            main_page.select_library_icon_view_media('Sport 01.jpg')
            main_page.insert_media('Sport 01.jpg')

            # select timeline video
            main_page.select_timeline_media('Skateboard 02.mp4')

            # Check applied blending mode via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Darken')
            logger(context_menu)

            # snapshot for context menu
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.3.24.2_SetBlendingMode_Darken.png')
            time.sleep(DELAY_TIME*2)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.24.2_SetBlendingMode_Darken.png',preview_wnd, similarity=0.9)
            logger(compare_result)

            case.result = compare_result
            logger(case.result)


        # 10/28
        with uuid('6121bd6a-b1bc-4c31-acd4-41057e4490d6') as case:
            # case1.3.24.3 : Set Clip Attributes > Image > Set Duration
            # select track2
            time.sleep(3)
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select timeline image
            main_page.select_timeline_media('Sport 01.jpg')

            # Set Duration via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Duration...')
            logger(context_menu)
            time.sleep(2)

            # snapshot for context menu
            preview_wnd = tips_area_page.snapshot(locator=L.tips_area.window.duration_settings,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.3.24.3_Set_Duration.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.24.3_Set_Duration.png',preview_wnd)
            logger(compare_result)

            # exit by ESC key
            main_page.press_esc_key()

            case.result = compare_result
            logger(case.result)

        # 10/28
        with uuid('c131a941-b3e4-418d-a10d-b29f8b03a7f0') as case:
            # case1.3.24.4 : Set Clip Attributes > Image > Set Image Stretch Mode
            # select track2
            time.sleep(3)
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select timeline image
            main_page.select_timeline_media('Sport 01.jpg')

            # Set Duration via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Image Stretch Mode...')
            logger(context_menu)
            time.sleep(2)

            # snapshot for context menu
            preview_wnd = tips_area_page.snapshot(locator=L.tips_area.button.more_features.image_stretch_mode.main_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.3.24.4_Set_Image_Stretch_Mode.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.24.4_Set_Image_Stretch_Mode.png',preview_wnd)
            logger(compare_result)

            # exit by ESC key
            main_page.press_esc_key()

            case.result = compare_result
            logger(case.result)

        # 10/28
        with uuid('a792016b-c848-45a1-8ed3-c0398e1ac23b') as case:
            # case1.3.24.5 : Set Clip Attributes > Image > Set Blending Mode
            # select track2
            time.sleep(3)
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select timeline image
            main_page.select_timeline_media('Sport 01.jpg')

            # Check applied blending mode via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Difference')
            logger(context_menu)

            # snapshot for context menu
            time.sleep(DELAY_TIME)
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.3.24.5_Image_SetBlendingMode_Difference.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.24.5_Image_SetBlendingMode_Difference.png',preview_wnd, similarity=0.9)
            logger(compare_result)

            case.result = compare_result
            logger(case.result)


        # 10/28
        with uuid('49c39fe5-22aa-4448-b584-66d7c84ecef1') as case:
            # case1.3.25.1 : Edit Clip Alias > Set Alias (Open Input Alias Dialogue)
            # select track2
            time.sleep(3)
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select timeline image
            main_page.select_timeline_media('Sport 01.jpg')

            # Set Duration via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit Clip Alias', 'Change Alias...')
            logger(context_menu)
            time.sleep(2)

            # input text
            main_page.input_text('test')

            # snapshot ([Warning] : type object 'set_alias' has no attribute 'AXSize')
            #preview_wnd = tips_area_page.snapshot(locator=L.tips_area.button.more_features.set_alias, file_name=Auto_Ground_Truth_Folder + 'G1.3.25.1_Change_Alias.png')
            #logger(preview_wnd)
            #compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.25.1_Change_Alias.png', preview_wnd)
            #logger(compare_result)

            # close 'set Alias...' dialogue
            tips_area_page.more_features.set_alias('test')

            # get alias
            alias = tips_area_page.more_features.get_alias()
            logger(alias)

            if alias == 'test':
                case.result = True
            else:
                case.result = False


        # 10/28
        with uuid('353a81b2-e947-4e89-979c-f815e3423a6a') as case:
            # case1.3.25.2 : Edit Clip Alias > Reset Alias
            # select track2
            time.sleep(3)
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select timeline image
            main_page.select_timeline_media('test')

            # Reset alias via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit Clip Alias', 'Reset Alias')
            logger(context_menu)

            # get alias
            alias = tips_area_page.more_features.get_alias()
            logger(alias)

            if alias == 'Sport 01':
                case.result = True
            else:
                case.result = False


        # 10/28
        with uuid('b1f796b7-d2c2-4b56-8ef5-346b4904e48d') as case:
            # case1.3.26 : View Properties
            # select track2
            time.sleep(3)
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select timeline image
            main_page.select_timeline_media('Sport 01.jpg')

            # View properties via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('View Properties')
            logger(context_menu)
            time.sleep(2)

            # snapshot for properties dialogue
            preview_wnd = tips_area_page.snapshot(locator=L.tips_area.button.more_features.properties.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.3.26_View_Properties.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.26_View_Properties.png',preview_wnd, similarity= 0.8)
            logger(compare_result)

            # exit by ESC key
            main_page.press_esc_key()

            case.result = compare_result
            logger(case.result)



    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        # 10/29
        with uuid('c67c2909-d334-430a-9cb2-d7e65a01ab9a') as case:
            # session : Right click on Particle/Title objects
            # case1.4.1.1 : Cut > Cut and Leave Gap
            # Insert a video / image to track1
            # select track1
            time.sleep(8)
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select one of library media and insert to track1
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.insert_media('Skateboard 01.mp4')

            # select one of library media and insert to track1
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)

            # select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # click "Stop" button to set timecode to 00:00:00:00
            playback_window_page.Edit_Timeline_PreviewOperation('Stop')

            # switch to particle room
            main_page.enter_room(5)
            time.sleep(5)

            # add particle to track2
            particle_room_page.hover_library_media('Effect-A')
            particle_room_page.select_RightClickMenu_AddToTimeline()

            # switch to title room
            main_page.enter_room(1)
            time.sleep(5)

            # insert title to track2
            particle_room_page.hover_library_media('Default')
            main_page.tips_area_insert_media_to_selected_track(option=2)

            # select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # snapshot for timeline status
            timeline_snap1 = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.4.1.1_Title_Before_Cut_and_Leave_Gap.png')
            logger(timeline_snap1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.1.1_Title_Before_Cut_and_Leave_Gap.png',
                timeline_snap1)
            logger(compare_result1)

            # select timeline clip
            main_page.select_timeline_media('My Title')

            # Cut via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Cut', 'Cut and Leave Gap')
            logger(context_menu)
            time.sleep(2)

            # snapshot for timeline status
            timeline_snap2 = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.4.1.1_Title_After_Cut_and_Leave_Gap.png')
            logger(timeline_snap2)
            compare_result2 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.1.1_Title_After_Cut_and_Leave_Gap.png',
                timeline_snap2)
            logger(compare_result2)

            case.result = compare_result1 and compare_result2

        # 10/29
        with uuid('9095ee68-5c6d-4e22-a25d-fcd6af74f41d') as case:
            # session : Right click on Particle/Title objects
            # case1.4.1.2 : Cut > Cut and Fill Gap
            # undo change
            main_page.click_undo()

            # select timeline clip
            main_page.select_timeline_media('My Title')

            # Cut via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Cut', 'Cut and Fill Gap')
            logger(context_menu)
            time.sleep(2)

            # snapshot for timeline status
            timeline_snap2 = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                     file_name=Auto_Ground_Truth_Folder + 'G1.4.1.2_Title_Cut_and_Fill_Gap.png')
            logger(timeline_snap2)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.1.2_Title_Cut_and_Fill_Gap.png', timeline_snap2)
            logger(compare_result)

            case.result = compare_result

        # 10/29
        with uuid('46ba505b-a60a-4610-863a-126779c46f7e') as case:
            # session : Right click on Particle/Title objects
            # case1.4.1.3 : Cut > Cut, Fill Gap, and Move All Clips
            # undo change
            main_page.click_undo()

            # select timeline clip
            main_page.select_timeline_media('My Title')

            # Cut via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Cut', 'Cut, Fill Gap, and Move All Clips')
            logger(context_menu)
            time.sleep(2)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                     file_name=Auto_Ground_Truth_Folder + 'G1.4.1.3_Title_Cut_Fill_Gap_Move_All_Clips.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.1.3_Title_Cut_Fill_Gap_Move_All_Clips.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 10/29
        with uuid('6ee061ff-73e7-4613-9dba-e4011d233ee9') as case:
            # session : Right click on Particle/Title objects
            # case1.4.2 : Copy
            # undo change
            main_page.click_undo()

            # select timeline clip
            main_page.select_timeline_media('My Title')

            # Copy clip via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Copy')
            logger(context_menu)
            time.sleep(2)

            with uuid('6744791c-2484-472a-8b92-df7b41a1b479') as case:
                # session : Right click on Particle/Title objects
                # case1.4.3.1 : paste and overwrite
                # seek to 00:00:10:00
                set_timecode = main_page.set_timeline_timecode('00_00_10_00')
                logger(set_timecode)

                # select track2
                select_track = main_page.timeline_select_track(2)
                logger(select_track)

                # move mouse to CTI position
                timeline_operation_page.move_mouse_to_CTI_position(2)

                # paste and overwrite
                main_page.right_click()
                main_page.select_right_click_menu('Paste')
                time.sleep(DELAY_TIME)
                main_page.click({"AXRole": "AXMenuItem", "AXIdentifier": 'IDM_INSERT_CHOICE_OVERWRITE'})
                time.sleep(DELAY_TIME * 2)

                # snapshot for timeline status
                timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.4.3.1_Title_Paste_and_Overwrite.png')
                logger(timeline_snap)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.4.3.1_Title_Paste_and_Overwrite.png', timeline_snap, similarity=0.9)
                logger(compare_result)

                case.result = compare_result

            case.result = compare_result

        # 10/29
        with uuid('daad0e7f-b266-40fb-a78e-1460a38f3b33') as case:
            # session : Right click on Particle/Title objects
            # case1.4.3.4 : Paste and Insert
            # undo change
            main_page.click_undo()

            # select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(2)

            # paste and overwrite
            main_page.right_click()
            context_menu2 = main_page.select_right_click_menu('Paste', 'Paste and Insert')
            logger(context_menu2)
            time.sleep(1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.4.3.4_Title_Paste_and_Insert.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.3.4_Title_Paste_and_Insert.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 10/29
        with uuid('e239a398-937a-44bb-8f33-6135d16ae8d4') as case:
            # session : Right click on Particle/Title objects
            # case1.4.3.5 : Paste, Insert, and Move All Clips
            # undo change
            main_page.click_undo()

            # select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(2)

            # paste, insert, and move all clips
            main_page.right_click()
            main_page.select_right_click_menu('Paste')
            time.sleep(DELAY_TIME)
            main_page.click({"AXRole": "AXMenuItem", "AXIdentifier": 'IDM_INSERT_CHOICE_INSERT_AND_MOVE_ALL_CLIPS'})
            time.sleep(1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.4.3.5_Title_Paste_Insert_Move_All_Clips.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.3.5_Title_Paste_Insert_Move_All_Clips.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 10/29
        with uuid('4e67520e-589d-48d0-8db2-5b348fc91f37') as case:
            # session : Right click on Particle/Title objects
            # case1.4.3.6 : Paste > Crossfade
            # undo change
            main_page.click_undo()

            # seek to 00:00:16:00
            set_timecode = main_page.set_timeline_timecode('00_00_06_00')
            logger(set_timecode)

            # select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(2)

            # paste with crossfade
            main_page.right_click()
            main_page.select_right_click_menu('Paste')
            time.sleep(DELAY_TIME)
            main_page.click({"AXRole": "AXMenuItem", "AXIdentifier": 'IDM_INSERT_CHOICE_CROSSFADE'})
            time.sleep(DELAY_TIME*2)

            # seek to 00:00:02:28
            set_timecode = main_page.set_timeline_timecode('00_00_02_28')
            logger(set_timecode)

            # snapshot for context menu
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.4.3.6_Title_Paste_Crossfade.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.4.3.6_Title_Paste_Crossfade.png',
                                                    preview_wnd)
            logger(compare_result)

            case.result = compare_result
            logger(case.result)

        # 10/29
        with uuid('239b6c2c-3989-4b4b-8112-3abb45c0dbca') as case:
            # session : Right click on Particle/Title objects
            # case1.4.4 : Remove selected object
            # undo change
            main_page.click_undo()

            # select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select timeline clip
            #main_page.select_timeline_media('My Title')
            timeline_operation_page.select_timeline_media(2,0)
            time.sleep(1)
            # Remove selected object via context menu
            main_page.right_click()

            context_menu = main_page.select_right_click_menu('Remove', 'Remove and Leave Gap')
            logger(context_menu)
            time.sleep(1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.4.4_Title_RemoveObject.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.4_Title_RemoveObject.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 10/31
        with uuid('2c5b6615-687d-49ba-9f29-6de8b9e8ce5d') as case:
            # session : Right click on Particle/Title objects
            # case1.4.5 : Select all object
            # undo change
            main_page.click_undo()

            # select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select timeline clip
            main_page.select_timeline_media('My Title')

            # Remove selected object via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Select All')
            logger(context_menu)
            time.sleep(1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.4.5_Title_SelectAllObject.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.5_Title_SelectAllObject.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result


    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        # 11/1
        with uuid('f6845931-d7d8-4844-944c-4da94bc7264b') as case:
            # session : Right click on Particle/Title objects
            # case1.4.6 : Split Particle / Title objects
            # Insert a video / image to track1
            # select track1
            time.sleep(8)

            # select one of library media and insert to track1
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.insert_media('Skateboard 01.mp4')

            # select one of library media and insert to track1
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)

            # select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # click "Stop" button to set timecode to 00:00:00:00
            playback_window_page.Edit_Timeline_PreviewOperation('Stop')

            # switch to title room
            main_page.enter_room(1)
            time.sleep(4)

            # insert title to track2
            particle_room_page.hover_library_media('Default')
            main_page.tips_area_insert_media_to_selected_track()

            # switch to particle room
            main_page.enter_room(5)
            time.sleep(3)
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)

            # add particle to track2
            particle_room_page.hover_library_media('Effect-A')
            main_page.drag_media_to_timeline_clip('My Title', pos_type=2)

            # select timeline clip
            main_page.select_timeline_media('My Title')

            # seek to 00:00:04:00
            set_timecode = main_page.set_timeline_timecode('00_00_04_00')
            logger(set_timecode)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(2)

            # Split title via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Split')
            logger(context_menu)
            time.sleep(1)

            # select timeline clip
            main_page.select_timeline_media('Effect-A')

            # copy "Particle object"
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Copy')
            logger(context_menu)

            # seek to 00:00:04:00
            set_timecode = main_page.set_timeline_timecode('00_00_06_00')
            logger(set_timecode)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(2)

            # Split particle via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Split')
            logger(context_menu)
            time.sleep(1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.4.6_Title_Particle_Split.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.6_Title_Particle_Split.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 11/1
        with uuid('238b5f38-a493-4b47-a8e9-e0b6bb2e67cf') as case:
            # session : Right click on Particle/Title objects
            # case1.4.8 : Edit Title

            # select timeline clip
            main_page.select_timeline_media('My Title')

            # Edit title via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit in Title Designer...')
            logger(context_menu)
            time.sleep(7)

            # snapshot for title designer
            title_designer_snap = tips_area_page.snapshot(locator=L.title_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.4.8_Enter_Title_Designer.png')
            logger(title_designer_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.8_Enter_Title_Designer.png', title_designer_snap)
            logger(compare_result)

            # exit by ESC key
            main_page.press_esc_key()

            case.result = compare_result

        # 11/3
        with uuid('80e4cbd7-170f-4331-9223-8a2dc6186aa2') as case:
            # session : Right click on Particle/Title objects
            # case1.4.9 : Edit Particle

            # select timeline clip
            main_page.select_timeline_media('Effect-A')

            # Edit title via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit in Particle Designer...')
            logger(context_menu)
            time.sleep(5)

            # snapshot for title designer
            particle_designer_snap = tips_area_page.snapshot(locator=L.particle_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G1.4.9_Enter_Particle_Designer.png')
            logger(particle_designer_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.9_Enter_Particle_Designer.png', particle_designer_snap)
            logger(compare_result)

            # exit by ESC key
            main_page.press_esc_key()

            case.result = compare_result


        # 11/3
        with uuid('05ea9885-8c55-4a6e-b0c9-069561632b7c') as case:
            # session : Right click on Particle/Title objects
            # case1.4.12 : Set Duration

            # select timeline clip
            main_page.select_timeline_media('Effect-A')

            # Edit particle via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Set Duration...')
            logger(context_menu)
            time.sleep(2)

            # snapshot for "Set Duration"
            duration_setting_snap = tips_area_page.snapshot(locator=L.tips_area.window.duration_settings,
                                                             file_name=Auto_Ground_Truth_Folder + 'G1.4.12_Particle_Duration_Settings.png')
            logger(duration_setting_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.12_Particle_Duration_Settings.png', duration_setting_snap)
            logger(compare_result)

            # exit by ESC key
            main_page.press_esc_key()

            # select timeline clip
            main_page.select_timeline_media('My Title')

            # Edit title via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Set Duration...')
            logger(context_menu)
            time.sleep(2)

            # snapshot for "Set Duration"
            duration_setting_snap = tips_area_page.snapshot(locator=L.tips_area.window.duration_settings,
                                                            file_name=Auto_Ground_Truth_Folder + 'G1.4.12_Title_Duration_Settings.png')
            logger(duration_setting_snap)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.12_Title_Duration_Settings.png', duration_setting_snap)
            logger(compare_result1)

            # exit by ESC key
            main_page.press_esc_key()

            case.result = compare_result and compare_result1


        # 11/3
        with uuid('896829b4-71a4-47e5-88c4-55eef07489b1') as case:
            # session : Right click on Particle/Title objects
            # case1.4.11 : Group/Ungroup objects

            # select title and particle
            timeline_operation_page.select_multiple_timeline_media(2, 0, 2, 3)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(2)

            # Group objects via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Group/Ungroup Objects')
            logger(context_menu)
            time.sleep(2)

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select timeline clip
            main_page.select_timeline_media('Food.jpg')

            # select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select timeline clip
            main_page.select_timeline_media('My Title')

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(0)

            # snapshot for timeline status
            time.sleep(DELAY_TIME*8)
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.4.11_Title_Particle_group_objects.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.11_Title_Particle_group_objects.png', timeline_snap)
            logger(compare_result)

            # Ungroup objects via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Group/Ungroup Objects')
            logger(context_menu)
            time.sleep(2)

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select timeline clip
            main_page.select_timeline_media('Food.jpg')

            # select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select timeline clip
            main_page.select_timeline_media('My Title')

            # snapshot for timeline status
            time.sleep(DELAY_TIME * 8)
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.4.11_Title_Particle_Ungroup_objects.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.11_Title_Particle_Ungroup_objects.png', timeline_snap)
            logger(compare_result1)

            case.result = compare_result and compare_result1


        # 11/3
        with uuid('2601bce9-fa16-444a-946e-f70f73b81583') as case:
            # session : Right click on Particle/Title objects
            # case1.4.3.3 : Paste > Paste and Trim to Fit
            # select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select title on timeline
            main_page.select_timeline_media('My Title', index=1)

            # Edit title via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Remove', 'Remove and Leave Gap')
            logger(context_menu)
            time.sleep(2)

            # Paste and Trim "particle object" to Fit Gap
            timeline_operation_page.move_mouse_to_CTI_position(2)
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Paste', 'Paste and Trim to Fit')
            logger(context_menu)
            time.sleep(2)

            # seek to 00:00:04:00
            set_timecode = main_page.set_timeline_timecode('00_00_04_00')
            logger(set_timecode)
            time.sleep(DELAY_TIME*2)

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.4.3.3_Particle_Paste_TrimToFit_Preview.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.4.3.3_Particle_Paste_TrimToFit_Preview.png',
                                                    preview_wnd)
            logger(compare_result)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.4.3.3_Particle_Paste_TrimToFit_Timeline.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.4.3.3_Particle_Paste_TrimToFit_Timeline.png', timeline_snap)
            logger(compare_result1)

            case.result = compare_result and compare_result1


    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        # 11/4
        with uuid('837dd50e-df4f-4ee8-8356-d6f0ea0a8449') as case:
            # session : 1.3 Right click on PiP object (Image/Video/Audio/Slideshow/Virtual Cut/Color board)
            # case1.3.20.13.1 : Select video > Edit Video > Edit in Video Collage Designer…
            # Create video collage object by designer
            time.sleep(DELAY_TIME*5)
            main_page.top_menu_bar_plugins_video_collage_designer()
            video_collage_designer_page.media.select_category(0)
            video_collage_designer_page.media.click_auto_fill()
            time.sleep(DELAY_TIME)
            check_result_1 = video_collage_designer_page.click_ok()
            logger(check_result_1)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(0)

            # Set "Alias" to "Video Collage"
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit Clip Alias', 'Change Alias...')
            logger(context_menu)
            time.sleep(2)
            tips_area_page.more_features.set_alias('collage')

            # insert a video from library to timeline
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=1)

            # select video on timeline
            main_page.select_timeline_media('Skateboard 01.mp4')

            # Check "Edit in video collage designer"
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit Video', 'Edit in Video Collage Designer...')
            logger(context_menu)
            time.sleep(2)

            if context_menu == False : # if "Edit in video collage designer" is disabled for video clip, then result is correct
                case.result = True
            else:
                case.result = False

        # 11/4
        with uuid('620dd15d-4c30-405a-8de8-fd7ea12ed3e8') as case:
            # session : 1.3 Right click on PiP object (Image/Video/Audio/Slideshow/Virtual Cut/Color board)
            # case1.3.20.13.2 : Select video collage object > Edit Video > Edit in Video Collage Designer…
            # Create video collage object by designer

            # select video Collage on timeline
            main_page.select_timeline_media('collage')

            # Check "Edit in video collage designer"
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit Video', 'Edit in Video Collage Designer...')
            logger(context_menu)
            time.sleep(2)

            #check_title = video_collage_designer_page.is_not_exist(L.video_collage_designer.main_window).AXTitle
            check_title = video_collage_designer_page.is_exist(L.video_collage_designer.main_window)
            logger (check_title)

            # exit video collage designer by ESC key
            main_page.press_esc_key()

            if check_title == True:
                result1 = True
                logger(result1)
            else:
                result1 = False
                logger(result1)

            case.result = context_menu and result1
            case.fail_log = "*blocked by VDE213501-0101"


    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        # 11/4
        with uuid('5a35a26c-0664-4ccd-8486-792848c0e122') as case:
            # session : 1.2 Right click on Timeline Empty Space / Track header
            # case1.2.1.1 : Paste > Paste and Overwrite…
            # insert video / image to timeline
            # select one of library media and insert to track1
            time.sleep(DELAY_TIME*5)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.insert_media('Skateboard 01.mp4')

            # select one of library media and insert to track1
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            time.sleep(DELAY_TIME*2)

            # select video on timeline
            main_page.select_timeline_media('Skateboard 01.mp4')

            # copy video
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Copy')
            logger(context_menu)
            #time.sleep(2)

            # select track1
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # insert a clip to track2
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.insert_media('Skateboard 02.mp4')

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select image on timeline
            main_page.select_timeline_media('Food.jpg')

            # remove image
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Remove', 'Remove and Leave Gap')
            logger(context_menu)

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # seek timeline
            timeline_operation_page.seek_timeline(60)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(0)

            # select video on timeline
            #self.mouse.move(int(clip_pos[0] - 15), int(clip_pos[0]))

            # Paste > Paste and Overwrite
            main_page.right_click()
            main_page.select_right_click_menu('Paste')
            time.sleep(DELAY_TIME)
            main_page.click({"AXRole": "AXMenuItem", "AXIdentifier": 'IDM_INSERT_CHOICE_OVERWRITE'})
            time.sleep(1)

            #self.keyboard.down()
            #self.keyboard.down()
            #self.keyboard.enter()

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.1.1_Video_Paste_and_Overwrite.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.1.1_Video_Paste_and_Overwrite.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 11/4
        with uuid('23041593-1efe-4a8b-883c-b72c094bfba7') as case:
            # session : 1.2 Right click on Timeline Empty Space / Track header
            # case1.2.1.2 : Paste > Paste and Trim to Fit
            # undo previous step
            main_page.click_undo()

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # seek timeline
            timeline_operation_page.seek_timeline(60)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(0)

            # paste and trim to fit
            main_page.right_click()
            context_menu2 = main_page.select_right_click_menu('Paste', 'Paste and Trim to Fit')
            logger(context_menu2)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.1.2_Video_Paste_and_TrimToFit.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.1.2_Video_Paste_and_TrimToFit.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 11/4
        with uuid('56d3aa60-16f3-4593-b1c7-7b31bda1e4b1') as case:
            # session : 1.2 Right click on Timeline Empty Space / Track header
            # case1.2.1.3 : Paste > Paste and Speed up to Fit
            # undo previous step
            main_page.click_undo()

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # seek timeline
            timeline_operation_page.seek_timeline(60)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(0)

            # paste and speed up to fit
            main_page.right_click()
            context_menu2 = main_page.select_right_click_menu('Paste', 'Paste and Speed up to Fit')
            logger(context_menu2)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.1.3_Video_Paste_and_SpeedUpToFit.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.1.3_Video_Paste_and_SpeedUpToFit.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 11/4
        with uuid('5d6d24ce-a3aa-4b26-aae0-2584dc9ee83c') as case:
            # session : 1.2 Right click on Timeline Empty Space / Track header
            # case1.2.1.4 : Paste > Paste and Insert
            # undo previous step
            main_page.click_undo()

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # seek timeline
            timeline_operation_page.seek_timeline(60)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(0)

            # paste and speed up to fit
            main_page.right_click()
            context_menu2 = main_page.select_right_click_menu('Paste', 'Paste and Insert')
            logger(context_menu2)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.1.4_Video_Paste_and_Insert.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.1.4_Video_Paste_and_Insert.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 11/4
        with uuid('e928cc6c-8103-4c92-b319-4d51c7c93e94') as case:
            # session : 1.2 Right click on Timeline Empty Space / Track header
            # case1.2.1.5 : Paste > Paste, Insert, and Move All Clips
            # undo previous step
            main_page.click_undo()

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # seek timeline
            timeline_operation_page.seek_timeline(60)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(0)

            # paste and speed up to fit
            main_page.right_click()
            main_page.select_right_click_menu('Paste')
            time.sleep(DELAY_TIME)
            main_page.click({"AXRole": "AXMenuItem", "AXIdentifier": 'IDM_INSERT_CHOICE_INSERT_AND_MOVE_ALL_CLIPS'})
            time.sleep(1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.1.5_Video_Paste_Insert_Move All Clips.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.1.5_Video_Paste_Insert_Move All Clips.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 11/4
        with uuid('2a45081e-756c-40a6-a91d-a9a5625284e0') as case:
            # session : 1.2 Right click on Timeline Empty Space / Track header
            # case1.2.1.6 : Paste > Crossfade
            # undo previous step
            main_page.click_undo()

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # seek timeline
            timeline_operation_page.seek_timeline(60)

            # move mouse to CTI position
            timeline_operation_page.move_mouse_to_CTI_position(0)

            # paste with cross fade
            main_page.right_click()
            main_page.select_right_click_menu('Paste')
            time.sleep(DELAY_TIME)
            main_page.click({"AXRole": "AXMenuItem", "AXIdentifier": 'IDM_INSERT_CHOICE_CROSSFADE'})
            time.sleep(DELAY_TIME * 2)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.2.1.6_Video_Paste_Crossfade.png')
            time.sleep(DELAY_TIME * 2)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.1.6_Video_Paste_Crossfade.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        # 11/4
        with uuid('801348f7-7156-439a-a880-75c568e94b2e') as case:
            # session : 1.3 Right click on PiP object (Image/Video/Audio/Slideshow/Virtual Cut/Color board)
            # case1.3.17 : Remove All Clip Markers for Selected Clips
            # open project with clip markers
            time.sleep(DELAY_TIME * 5)
            main_page.top_menu_bar_file_open_project()
            main_page.handle_open_project_dialog(Test_Material_Folder + 'Timeline_Right_Click_Menu/clip_marks/clip_marks.pds')
            time.sleep(DELAY_TIME*5)

            main_page.handle_merge_media_to_current_library_dialog('no', 'yes')

            # close high definition dialogue
            #time.sleep(DELAY_TIME * 2)
            #media_room_page.high_definition_video_confirm_dialog_click_no()
            #time.sleep(DELAY_TIME * 2)
            #media_room_page.high_definition_video_confirm_dialog_click_no()

            # select track1
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('Speaking Out')

            # paste with cross fade
            main_page.right_click()
            context_menu2 = main_page.select_right_click_menu('Remove All Clip Markers For Selected Clip')
            logger(context_menu2)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.17_Remove_Clip_Markers.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.3.17_Remove_Clip_Markers.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result


        # 11/4
        with uuid('34523c69-bd3d-4c29-9a67-34814cae9d99') as case:
            # session : 1.3 Right click on PiP object (Image/Video/Audio/Slideshow/Virtual Cut/Color board)
            # case1.3.15 : Restore to Original Volume Level

            # select track1
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('Speaking Out')

            # paste with cross fade
            main_page.right_click()
            context_menu2 = main_page.select_right_click_menu('Restore to Original Volume Level')
            logger(context_menu2)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.15_Restore to Original Volume Level.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.3.15_Restore to Original Volume Level.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result


        # 11/4
        with uuid('e2c76d54-a788-40b5-b002-806dafc4e3ff') as case:
            # session : 1.3 Right click on PiP object (Image/Video/Audio/Slideshow/Virtual Cut/Color board)
            # case1.3.3 : Copy Keyframe Attributes

            # select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('Skateboard 02')

            # Copy keyframe attributes
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Copy Keyframe Attributes')
            logger(context_menu)

            with uuid('c012859f-6d34-4ace-a42b-709fe233e289') as case:
            # session : 1.3 Right click on PiP object (Image/Video/Audio/Slideshow/Virtual Cut/Color board)
            # case1.3.5 : Paste Keyframe Attributes

                # select video on timeline
                main_page.select_timeline_media('TheIncredibles_HEVC')

                # paste keyframe attributes
                main_page.right_click()
                context_menu2 = main_page.select_right_click_menu('Paste Keyframe Attributes')
                logger(context_menu2)
                time.sleep(DELAY_TIME)

                # Press [OK] to close dialogue
                main_page.keyboard.enter() # 11/7 PDR20.0.3310 crashes after pressing [OK]

                # snapshot for timeline status
                timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.5_Paste_Keyframe_Attributes.png')
                logger(timeline_snap)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G1.3.5_Paste_Keyframe_Attributes.png', timeline_snap)
                logger(compare_result)

                case.result = compare_result
                case.fail_log = "*Bug Code: VDE213310-0012*"

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.3_Copy_Keyframe_Attributes.png')
            logger(timeline_snap)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.3.3_Copy_Keyframe_Attributes.png', timeline_snap)
            logger(compare_result1)

            case.result = compare_result and compare_result1
            case.fail_log = "*Bug Code: VDE213310-0012*"

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9_1(self):
        # 11/5
        with uuid('13f1395d-f2f3-4587-bf76-16812ae5deb1') as case:
            # session 1.2 : Right click on Timeline Empty Space / Track header
            # case1.2.17.2.1 : minimize undock timeline window
            # select one of library media and insert to track1
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.insert_media('Skateboard 01.mp4')

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # Undock timeline by context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Dock/Undock Timeline Window')
            logger(context_menu)

            # minimize timeline window
            timeline_operation_page.undock_timeline.click_min_btn()

            # check timeline status
            timeline = timeline_operation_page.is_not_exist(L.timeline_operation.workspace)
            logger(timeline)

            #if timeline == True:

            # 11/9
            with uuid('3ce7b9a9-8b11-4fab-8a89-2ecfd5ba4fd4') as case:
                # case1.2.17.2.2 : After minimize, Show "Timeline" button in Upper-Right
                #if self.is_exist(L.main.btn_show_minimized_window) == True:
                check = timeline_operation_page.undock_timeline.check_timeline_window_minimize_status()
                logger(check)

                case.result = check

            # 11/9
            with uuid('1bbf8433-620d-4cb0-9ad9-47ac4d214647') as case:
                # case.1.2.17.2.3 : Open timeline window correctly if click "Timeline" button
                check_result = timeline_operation_page.undock_timeline.click_show_timeline_window()

                case.result = check_result

            # Dock timeline by context menu
            main_page.timeline_select_track(1)
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Dock/Undock Timeline Window')
            logger(context_menu)

            case.result = timeline

            #case.result = compare_result1 and compare_result2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_10(self):
        # 11/11
        with uuid('aebdc53a-3aa0-462d-a68c-22088f63143c') as case:
            # session 1.1 : Right click on Timeline Scale
            # case1.1.1 : Add Timeline Marker
            # select one of library media and insert to track1
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.insert_media('Skateboard 01.mp4')

            # seek to specific time code
            set_timecode = main_page.set_timeline_timecode('00_00_03_05')
            logger(set_timecode)

            # Select track1
            #select_track = main_page.timeline_select_track(1)
            #logger(select_track)

            # move mouse to timeline indicator and input string into "Note"
            add_marker = timeline_operation_page.right_click_timecode_menu('Add Timeline Marker')
            logger(add_marker)
            time.sleep(DELAY_TIME*2)
            check1 = timeline_operation_page.is_exist(L.timeline_operation.clipmarker_textfield)
            logger(check1)
            timeline_operation_page.set_clipmarker_note('skateboard!')

            # seek to specific time code
            time.sleep(DELAY_TIME)
            set_timecode = main_page.set_timeline_timecode('00_00_08_00')
            logger(set_timecode)

            # move mouse to timeline indicator and input string into "Note"
            add_marker = timeline_operation_page.right_click_timecode_menu('Add Timeline Marker')
            logger(add_marker)
            time.sleep(DELAY_TIME * 2)
            check2 = timeline_operation_page.is_exist(L.timeline_operation.clipmarker_textfield)
            logger(check2)
            timeline_operation_page.set_clipmarker_note('123@')

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.1.1_Add_Timeline_Marker.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.1_Add_Timeline_Marker.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result and check1 and check2


        # 11/18
        with uuid('9ebfd9df-c576-4a92-b776-37c499aa8ec3') as case:
            # session 1.1 : Right click on Timeline Scale
            # case1.1.4.1 : Edit Timeline Marker
            # Open Edit Timeline Marker dialogue
            edit_marker = timeline_operation_page.right_click_timecode_menu('Edit Timeline Marker')
            logger(edit_marker)

            timeline_marker_wnd = timeline_operation_page.is_exist(L.timeline_operation.edit_timeline_marker.modify_window)
            logger(timeline_marker_wnd)

            case.result = timeline_marker_wnd

            # click ok
            timeline_operation_page.timeline_marker.click_ok()
        # 11/18
        with uuid('c7eb984c-b4a1-4b4f-af85-42e7941d24b7') as case:
            # session 1.1 : Right click on Timeline Scale
            # case1.1.4.2 : Edit Timeline Marker > Modified result can be applied
            # Open Edit Timeline Marker dialogue
            edit_marker = timeline_operation_page.right_click_timecode_menu('Edit All Timeline Markers')
            logger(edit_marker)

            # edit note
            timeline_operation_page.timeline_marker.edit_note(no=1, strnote='hello...@#$')

            # click ok
            timeline_operation_page.timeline_marker.click_ok()

            # re-enter timeline marker
            edit_marker = timeline_operation_page.right_click_timecode_menu('Edit All Timeline Markers')
            logger(edit_marker)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.edit_timeline_marker.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.1.4.2_Edited_Timeline_Marker.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.4.2_Edited_Timeline_Marker.png', timeline_snap)
            logger(compare_result)

            # click ok
            timeline_operation_page.timeline_marker.click_ok()

            case.result = compare_result



        # 11/11
        with uuid('4458588a-4b5c-41b4-964d-75ecb628adb0') as case:
            # session 1.1 : Right click on Timeline Scale
            # case1.1.6 : Zoom in timeline scale
            # move mouse to timeline indicator
            timeline1 = timeline_operation_page.right_click_timecode_menu('Zoom In')
            logger(timeline1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.1.6_Zoom_In_timeline_scale.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.6_Zoom_In_timeline_scale.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 11/11
        with uuid('c7838bf3-854f-4c10-99da-3f8bfb1d405d') as case:
            # session 1.1 : Right click on Timeline Scale
            # case1.1.7 : Zoom out timeline scale
            # move mouse to timeline indicator
            timeline1 = timeline_operation_page.right_click_timecode_menu('Zoom Out')
            logger(timeline1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.1.7_Zoom_Out_timeline_scale.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.1.7_Zoom_Out_timeline_scale.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 11/11
        with uuid('5d242085-098f-452f-9b4b-8b1429911cc1') as case:
            # session 1.1 : Right click on Timeline Scale
            # case1.1.5 : View entire video
            # move mouse to timeline indicator
            timeline1 = timeline_operation_page.right_click_timecode_menu('View Entire Video')
            logger(timeline1)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.1.5_View_Entire_Video.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.1.5_View_Entire_Video.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 11/11
        with uuid('7de36706-6a95-428a-bc0a-1854859d4cc7') as case:
            # session 1.1 : Right click on Timeline Scale
            # case1.1.2 : Remove Selected Marker
            # seek to specific time code
            set_timecode = main_page.set_timeline_timecode('00_00_03_05')
            logger(set_timecode)

            # move mouse to timeline indicator
            timeline1 = timeline_operation_page.right_click_timecode_menu('Remove Selected Marker')
            logger(timeline1)

            # seek to specific time code
            set_timecode = main_page.set_timeline_timecode('00_00_05_15')
            logger(set_timecode)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.1.2_Remove_Selected_Marker.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.2_Remove_Selected_Marker.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result

        # 11/11
        with uuid('de52df19-fdfd-4075-ac40-66094c897737') as case:
            # session 1.1 : Right click on Timeline Scale
            # case1.1.3 : Remove All Markers
            # undo
            main_page.click_undo()

            # seek to specific time code
            set_timecode = main_page.set_timeline_timecode('00_00_03_05')
            logger(set_timecode)

            # move mouse to timeline indicator
            timeline1 = timeline_operation_page.right_click_timecode_menu('Remove All Timeline Markers')
            logger(timeline1)

            # seek to specific time code
            set_timecode = main_page.set_timeline_timecode('00_00_05_15')
            logger(set_timecode)

            # snapshot for timeline status
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.1.3_Remove_All_Markers.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.3_Remove_All_Markers.png', timeline_snap)
            logger(compare_result)

            case.result = compare_result












    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_11(self):
        with uuid("""7b89abd7-d92c-4d71-b38d-00039d987775
cc204a22-b28b-4d73-83ad-f84ba173b24e
55105865-01be-4139-8f0b-b97596b23f24
6b745640-23c1-42b1-8afe-1a7d517488ec
2e347952-5dc1-4a77-a556-93014c78d640
75f51d38-ce1a-43d0-bd05-a318020cd478
a329b4b8-4451-417b-8c2f-7f925f99d568
f4eef73f-490a-4722-9124-5338a4b4e412""") as case:
                case.result = None
                case.fail_log = "*SKIP by AT or feature was removed*"