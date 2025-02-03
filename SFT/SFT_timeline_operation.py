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
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page', mwc)
effect_room_page = PageFactory().get_page_object('effect_room_page', mwc)
transition_room_page = PageFactory().get_page_object('transition_room_page', mwc)
video_speed_page = PageFactory().get_page_object('video_speed_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Timeline Operation.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Timeline_Operation/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Timeline_Operation/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Timeline_Operation():
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
            google_sheet_execution_log_init('Timeline_Operation')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"timeline operation result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        with uuid('f06ff3db-a548-4c0a-a676-ddf942ed644a') as case:
            # 2. Scale
            # 2.1. Scale Adjustment
            # 2.1.1. Slider bar > Slider > Zoom out
            # adjust scale correctly
            timeline_operation_page.drag_zoom_sliderbar(0.8)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_2_1_1_1.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_2_1_1_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('db158dbc-1967-4d1e-9478-f524e4939064') as case:
            # 2.1. Scale Adjustment
            # 2.1.1. Slider bar > Slider > Zoom in
            # adjust scale correctly
            timeline_operation_page.drag_zoom_sliderbar(0.2)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_2_1_1_2.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_2_1_1_2.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

            timeline_operation_page.drag_zoom_sliderbar(0.5)

        with uuid('38b5cf73-4e99-4289-a2e0-139bb0f28652') as case:
            # 2.1. Scale Adjustment
            # 2.1.1. Slider bar > -/+ button > Zoom out
            # adjust scale correctly
            for i in range(5):
                timeline_operation_page.click_zoomout_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_2_1_1_3.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_2_1_1_3.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('6f92d4e9-3f7b-43c5-80f4-ef16f36e436f') as case:
            # 2.1. Scale Adjustment
            # 2.1.1. Slider bar > -/+ button > Zoom in
            # adjust scale correctly
            for i in range(5):
                timeline_operation_page.timeline_click_zoomin_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_2_1_1_4.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_2_1_1_4.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        # with uuid('f414358a-c943-412e-85ea-da3caf43056e') as case:
        #     # 2.1. Scale Adjustment
        #     # 2.1.2. Drag Scale Bar > To Right
        #     # enlarge the timeline scale
        #     # AT limitation
        #     case.result = None

        # with uuid('fb2360a4-1276-4431-918a-46c1d87424b8') as case:
        #     # 2.1. Scale Adjustment
        #     # 2.1.2. Drag Scale Bar > To Left
        #     # reduce the timeline scale
        #     # AT limitation
        #     case.result = None

        with uuid('becb3a0f-1dd0-4353-bbca-5676daf4e12d') as case:
            # 2.1. Scale Adjustment
            # 2.1.3. [View entire movie] button > Before inserting any file to timeline
            # keep original scale
            timeline_operation_page.click_view_entire_video_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_2_1_3_1.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_2_1_3_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('93137009-bfee-4fcc-996f-7dc9961a8d56') as case:
            # 2.1. Scale Adjustment
            # 2.1.3. [View entire movie] button > After inserting file to timeline
            # adjust scale to fit current timeline contents
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.click_view_entire_video_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_2_1_3_2.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_2_1_3_2.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        # with uuid('04a8a4c7-f547-4611-9c25-c65e96595061') as case:
        #     # 2.1. Scale Adjustment
        #     # 2.1.4. Enlarge timeline scale for audio track > Unselect(default)
        #     # minimum timeline scale is 00:00:00:05
        #     # Preferences >Editing > PDR Mac v2529 does not support this function
        #     case.result = None

        with uuid('82c2c422-09a0-462c-9348-fdccf77a6a21') as case:
            # 2.2. Timeline Viewer Control
            # 2.2.1. Horizontal > Scroll bar
            # viewer is controlled correctly
            timeline_operation_page.set_add_tracks_video(1, 'Above track 3')
            timeline_operation_page.drag_timeline_horizontal_scroll_bar(0.3)
            time.sleep(DELAY_TIME * 2)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_2_2_1_1.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_2_2_1_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('cb2685b2-99bd-4773-9873-acb55fe81634') as case:
            # 2.2. Timeline Viewer Control
            # 2.2.2. Vertical > Scroll bar
            # viewer is controlled correctly
            timeline_operation_page.drag_timeline_vertical_scroll_bar(0.3)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_2_2_2_1.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_2_2_2_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        # with uuid('2fd448c7-0754-4e68-8aa2-0d221b1c931c') as case:
        #     # 2.3. Operation on Scale Bar
        #     # 2.3.1. Seek at scale
        #     # red line show on timeline
        #     # AT limitation
        #     case.result = None

        # with uuid('ba5334cf-ad72-4b56-ac50-0009fab3be74') as case:
        #     # 2.3. Operation on Scale Bar
        #     # 2.3.1. Seek at scale
        #     # show correct preview if seek at scale
        #     # AT limitation
        #     case.result = None

        # with uuid('686cad20-34fd-4d46-9589-e1897b8916e7') as case:
        #     # 2.3. Operation on Scale Bar
        #     # 2.3.2. Range Selection > Range > Mark in
        #     # show yellow line at mark in/out position
        #     # AT limitation
        #     case.result = None

        # with uuid('65756340-ebae-4538-946e-4ee643eef230') as case:
        #     # 2.3. Operation on Scale Bar
        #     # 2.3.2. Range Selection > Range > Mark in
        #     # show slight yellow for selected range
        #     # AT limitation
        #     case.result = None

        # with uuid('459083e6-6d03-42a5-affa-866a282627fa') as case:
        #     # 2.3. Operation on Scale Bar
        #     # 2.3.2. Range Selection > Range > Mark out
        #     # show yellow line at mark in/out position
        #     # AT limitation
        #     case.result = None

        # with uuid('daa5804f-2992-410a-b980-89da68c2a381') as case:
        #     # 2.3. Operation on Scale Bar
        #     # 2.3.2. Range Selection > Range > Mark out
        #     # show slight yellow for selected range
        #     # AT limitation
        #     case.result = None

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid('b7b4d77e-6ea4-4bf4-bb1e-4f2bddb36727') as case:
            # 3. Track
            # 3.1. Track Manager
            # 3.1.1. Enable/Disable this Track > Select (default) > Video Track
            # content displays correctly when previewing
            main_page.insert_media('Skateboard 01.mp4')
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 10)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_1_1_1.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_1_1_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.playback_window.main, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.click_undo()

        with uuid('1dd59bc9-2410-4b7c-bb8e-10e83fd3d721') as case:
            # 3.1. Track Manager
            # 3.1.1. Enable/Disable this Track > Select (default) > Audio Track
            # content displays correctly when previewing
            main_page.insert_media('Mahoroba.mp3')
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 10)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_1_1_2.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_1_1_2.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.playback_window.main, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.click_undo()

        with uuid('e35c5eda-9916-4a69-b3b9-784e9bf5f31c') as case:
            # 3.1. Track Manager
            # 3.1.1. Enable/Disable this Track > Select (default) > Effect Track
            # content displays correctly when previewing
            main_page.insert_media('Skateboard 01.mp4')
            main_page.enter_room(3)
            effect_room_page.right_click_addto_timeline('Aberration')
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 10)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_1_1_3.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_1_1_3.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.playback_window.main, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('215d77b6-7c6f-442d-880e-bde5aa7845fc') as case:
            # 3.1. Track Manager
            # 3.1.1. Enable/Disable this Track > Unselect > Video Track
            # content will not show when previewing
            timeline_operation_page.drag_timeline_vertical_scroll_bar(0.0)
            timeline_operation_page.edit_specific_track_set_enable(0, 0)

            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 10)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_1_1_4.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_1_1_4.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.playback_window.main, file_name=image_full_path)

            check_result_1 = timeline_operation_page.compare(ground_truth, current_preview)

            current_status = timeline_operation_page.get_specific_video_track_enable_status(0)
            if not current_status == 'Disable':
                check_result_2 = False
            else:
                check_result_2 = True

            case.result = check_result_1 and check_result_2

        with uuid('dd646d6f-98ac-4ed0-9308-b4431a540f5d') as case:
            # 3.1. Track Manager
            # 3.1.1. Enable/Disable this Track > Unselect > Audio Track
            # content will not show when previewing
            timeline_operation_page.edit_specific_track_set_enable(1, 0)

            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 10)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_1_1_5.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_1_1_5.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.playback_window.main, file_name=image_full_path)

            check_result_1 = timeline_operation_page.compare(ground_truth, current_preview)

            current_status = timeline_operation_page.get_specific_audio_track_enable_status(1)
            if not current_status == 'Disable':
                check_result_2 = False
            else:
                check_result_2 = True

            case.result = check_result_1 and check_result_2

        with uuid('b138ff0e-b76f-40d7-9348-3b4d741c43cf') as case:
            # 3.1. Track Manager
            # 3.1.1. Enable/Disable this Track > Unselect > Effect Track
            # content will not show when previewing
            timeline_operation_page.drag_timeline_vertical_scroll_bar(1.0)
            timeline_operation_page.edit_specific_track_set_enable(6, 0)

            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 10)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_1_1_6.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_1_1_6.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.playback_window.main, file_name=image_full_path)

            check_result_1 = timeline_operation_page.compare(ground_truth, current_preview)

            current_status = timeline_operation_page.get_specific_effect_track_enable_status(6)
            if not current_status == 'Disable':
                check_result_2 = False
            else:
                check_result_2 = True

            case.result = check_result_1 and check_result_2

        with uuid('3213d7fd-d174-4781-8aea-33541c45c37c') as case:
            # 3.1. Track Manager
            # 3.1.2. Lock/Unlock this Track > Unlock (default) > Video Track
            # track can be selected
            timeline_operation_page.drag_timeline_vertical_scroll_bar(0.0)

            current_status = timeline_operation_page.get_specific_video_track_lock_status(0)
            if not current_status == 'Unlock':
                case.result = False
            else:
                case.result = True

        with uuid('5474e7b3-5f73-48d6-b405-e6bc79b23c61') as case:
            # 3.1. Track Manager
            # 3.1.2. Lock/Unlock this Track > Unlock (default) > Audio Track
            # track can be selected
            current_status = timeline_operation_page.get_specific_audio_track_lock_status(1)
            if not current_status == 'Unlock':
                case.result = False
            else:
                case.result = True

        with uuid('c3406f86-b5aa-4c88-beb3-c1d882297ba9') as case:
            # 3.1. Track Manager
            # 3.1.2. Lock/Unlock this Track > Unlock (default) > Effect Track
            # track can be selected
            timeline_operation_page.drag_timeline_vertical_scroll_bar(1.0)
            current_status = timeline_operation_page.get_specific_effect_track_lock_status(6)
            if not current_status == 'Unlock':
                case.result = False
            else:
                case.result = True

        with uuid('172d0848-7500-48e8-9621-7573db6c2590') as case:
            # 3.1. Track Manager
            # 3.1.2. Lock/Unlock this Track > Lock > Video Track
            # track cannot be selected for any editing
            timeline_operation_page.drag_timeline_vertical_scroll_bar(0.0)
            timeline_operation_page.edit_specific_video_track_set_lock_unlock(0)

            current_status = timeline_operation_page.get_specific_video_track_lock_status(0)
            if not current_status == 'Lock':
                case.result = False
            else:
                case.result = True

            timeline_operation_page.edit_specific_video_track_set_lock_unlock(0)

        with uuid('3742059e-5ad4-4129-a7a3-fafe32c9cb13') as case:
            # 3.1. Track Manager
            # 3.1.2. Lock/Unlock this Track > Lock > Audio Track
            # track cannot be selected for any editing
            timeline_operation_page.edit_specific_audio_track_set_lock_unlock(1)

            current_status = timeline_operation_page.get_specific_audio_track_lock_status(1)
            if not current_status == 'Lock':
                case.result = False
            else:
                case.result = True

            timeline_operation_page.edit_specific_audio_track_set_lock_unlock(1)

        with uuid('31fdf5b2-7e74-4fbd-9cbb-e9b4c6c33433') as case:
            # 3.1. Track Manager
            # 3.1.2. Lock/Unlock this Track > Lock > Effect Track
            # track cannot be selected for any editing
            timeline_operation_page.drag_timeline_vertical_scroll_bar(1.0)
            timeline_operation_page.edit_specific_effect_track_set_lock_unlock(6)

            current_status = timeline_operation_page.get_specific_effect_track_lock_status(6)
            if not current_status == 'Lock':
                case.result = False
            else:
                case.result = True

            timeline_operation_page.edit_specific_effect_track_set_lock_unlock(6)

        with uuid('c3024711-b70e-4e9f-a5a7-3e1e551fe1cb') as case:
            # 3.1. Track Manager
            # 3.1.3. Track name > Input Character
            # input displays correctly
            timeline_operation_page.drag_timeline_vertical_scroll_bar(0.0)
            timeline_operation_page.drag_to_show_track_name()
            timeline_operation_page.edit_video_trackname(0, 'Track_0')
            time.sleep(DELAY_TIME)

            check_result = timeline_operation_page.get_video_trackname(0)
            if not check_result == 'Track_0':
                case.result = False
            else:
                case.result = True

            timeline_operation_page.drag_to_hide_track_name()

        with uuid('40677eb8-b6b5-46e5-9e56-a9210c51aae5') as case:
            # 3.1. Track Manager
            # 3.1.4. Add additional track > Add track > Video Track
            # can add additional track correctly
            timeline_operation_page.set_add_tracks_video(1, 'Above track 1')

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_1_4_1.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_1_4_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('c4bac7d4-4b4a-49ff-9b83-a555499aab1e') as case:
            # 3.1. Track Manager
            # 3.1.4. Add additional track > Add track > Audio Track
            # can add additional track correctly
            timeline_operation_page.set_add_tracks_audio(1, 'Above track 1')

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_1_4_2.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_1_4_2.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('de2658cd-896b-4433-8fd2-07d33929e2b6') as case:
            # 3.1. Track Manager
            # 3.1.4. Add additional track > Add track > Effect Track
            # can add additional track correctly
            timeline_operation_page.set_add_tracks_effect(1, 'Above track 2')

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_1_4_3.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_1_4_3.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('ba1a5f94-422e-4257-8ca5-8df0b8940b0d') as case:
            # 3.1. Track Manager
            # 3.1.4. Add additional track > Limitation > Video Track
            # limitation is total 100 video tracks
            timeline_operation_page.set_add_tracks_video(100, 'Above track 1')
            timeline_operation_page.drag_timeline_vertical_scroll_bar(1.0)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_1_4_4.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_1_4_4.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

            timeline_operation_page.drag_timeline_vertical_scroll_bar(0.0)

        with uuid('731a4eb1-7b46-48b6-948b-8835a84839ed') as case:
            # 3.1. Track Manager
            # 3.1.4. Add additional track > Limitation > Audio Track
            # limitation is total 100 audio tracks
            timeline_operation_page.set_add_tracks_audio(100, 'Above track 1')
            timeline_operation_page.drag_timeline_vertical_scroll_bar(1.0)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_1_4_5.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_1_4_5.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

            timeline_operation_page.drag_timeline_vertical_scroll_bar(0.0)

        with uuid('a70c496c-dd62-43ba-86e0-0d5a3e15c1aa') as case:
            # 3.1. Track Manager
            # 3.1.4. Add additional track > Limitation > Effect Track
            # limitation is total 5 effect tracks
            timeline_operation_page.right_click_remove_empty_tracks()
            timeline_operation_page.set_add_tracks_effect(5, 'Above track 2')
            timeline_operation_page.drag_timeline_vertical_scroll_bar(0.0)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_1_4_6.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_1_4_6.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

            timeline_operation_page.right_click_remove_empty_tracks()

        # with uuid('1945e7db-9536-4a1a-8626-86250f9422b5') as case:
        #     # 3.1. Track Manager
        #     # 3.1.5. Reorder > By Track Dragging
        #     # can drag track to change track ordering
        #     # No page function support
        #     case.result = None

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid('136f915d-b172-4c50-9ba6-6742e9703d26') as case:
            # 3.2. Clip Marker Track
            # 3.2.1. Show / Unshow Clip Marker > Unshow (default)
            # unshow clip marker track
            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_2_1_1.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_2_1_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('837fdc65-f8b5-47ca-88c1-34e53c29e2fd') as case:
            # 3.2. Clip Marker Track
            # 3.2.1. Show / Unshow Clip Marker > Show > Tick
            # Show clip marker track
            timeline_operation_page.mouse_move_to_video_track1()
            timeline_operation_page.right_click_show_clip_marker_track()

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_2_1_2.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_2_1_2.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('2b1b649d-24ff-4c0c-8734-4986e0461d50') as case:
            # 3.2. Clip Marker Track
            # 3.2.2. Context Menu / Add Clip Marker > Disable
            # No clip selected
            timeline_operation_page.right_click_menu_clip_marker_track_unselected_clip()

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_2_2_1.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_2_2_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        # with uuid('0789e1b4-d1da-4b2b-935b-ec17435d8433') as case:
        #     # 3.2. Clip Marker Track
        #     # 3.2.2. Context Menu / Add Clip Marker
        #     # select marker(s). (Right click on marker)
        #     # AT limitation, cannot right click "Clip Marker"
        #     case.result = None

        with uuid('5c92b576-105a-461b-a591-fcc14353de43') as case:
            # 3.2. Clip Marker Track
            # 3.2.2. Context Menu / Add Clip Marker > Enable
            # add marker dialog pops up. (adjust marker time/edit note)
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.right_click_menu_add_clip_marker(0, 0)
            timeline_operation_page.set_clipmarker_time('00_00_05_00')

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_2_2_2.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_2_2_2.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        # with uuid('07e4c03e-0045-42d4-817e-ecc74db78ece') as case:
        #     # 3.2. Clip Marker Track
        #     # 3.2.2. Context Menu / Remove Selected Clip Marker > Enable
        #     # remove selected clip marker (yellow markers)
        #     # AT limitation, cannot right click "Clip Marker"
        #     case.result = None

        # with uuid('67106ca6-9735-49ee-b460-4f41ad4a5d38') as case:
        #     # 3.2. Clip Marker Track
        #     # 3.2.2. Context Menu / Remove Selected Clip Marker > Disable
        #     # no clip selected
        #     # AT limitation, cannot right click "Clip Marker"
        #     case.result = None

        # with uuid('d10ed3dd-fefe-47a9-83ff-8c12c743086b') as case:
        #     # 3.2. Clip Marker Track
        #     # 3.2.2. Context Menu / Remove Selected Clip Marker > Disable
        #     # no marker on clip(s)
        #     # AT limitation, cannot right click "Clip Marker"
        #     case.result = None

        with uuid('fffaaaf1-1b67-4b22-bede-3037b5bd3f3d') as case:
            # 3.2. Clip Marker Track
            # 3.2.2. Context Menu / Remove All Clip Markers > Enable
            # able to remove all clip markers
            timeline_operation_page.click_right_click_menu_remove_all_clips_marker()

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_2_2_3.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_2_2_3.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('87adf02b-dd12-41b4-bea6-54c49c281346') as case:
            # 3.2. Clip Marker Track
            # 3.2.2. Context Menu / Remove All Clip Markers > Disable
            # no marker on clip(s)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_2_2_4.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_2_2_4.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        # with uuid('e6236a1d-d69a-4625-8f9c-6300d12c0a04') as case:
        #     # 3.2. Clip Marker Track
        #     # 3.2.2. Context Menu / Edit Clip Marker > Enable
        #     # edit marker dialog pops up. (adjust marker time/edit note)
        #     # AT limitation, cannot right click "Clip Marker"
        #     case.result = None

        # with uuid('cd66c554-4550-48c9-bd41-6811246715e3') as case:
        #     # 3.2. Clip Marker Track
        #     # 3.2.2. Context Menu / Edit Clip Marker > Disable
        #     # no marker selected
        #     # AT limitation, cannot right click "Clip Marker"
        #     case.result = None

        with uuid('3b9a0aee-6278-42c4-a173-49f0f911d3fa') as case:
            # 3.2. Clip Marker Track
            # 3.2.2. Context Menu / Dock/Undock Timeline Window > Enable
            # dock/undock timeline window
            timeline_operation_page.right_click_menu_clip_marker_track_dock_undock_timeline_window()

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_2_2_5.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_2_2_5.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('7caaf576-43c2-4dd6-950e-1c3a419befc5') as case:
            # 3.2. Clip Marker Track
            # 3.2.2. Context Menu / Reset All Undocked Windows > Enable
            # reset all undocked windows to docked
            timeline_operation_page.right_click_menu_clip_marker_track_reset_all_undocked_window()

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_2_2_6.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_2_2_6.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

            timeline_operation_page.right_click_show_clip_marker_track()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid('b92dbe68-2613-4a1f-974b-88399b05308f') as case:
            # 3.3. Content and Adjustment
            # 3.3.1. Content info > Audio Track > Alias
            # show alias correctly
            main_page.insert_media('Mahoroba.mp3')

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_1_5.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_1_5.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.click_undo()

        with uuid('32386741-c4e3-4faa-9d72-a00804316b46') as case:
            # 3.3. Content and Adjustment
            # 3.3.1. Content info > Video Track > Alias
            # show alias correctly
            main_page.insert_media('Skateboard 01.mp4')

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_1_1.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_1_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('b18093a5-0835-489b-9fa5-fdc2880eb288') as case:
            # 3.3. Content and Adjustment
            # 3.3.1. Content info > Video Track > Thumbnail
            # show clip thumbnail correctly
            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_1_2.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_1_2.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('9201d36d-37e1-4163-a375-6a3500564e19') as case:
            # 3.3. Content and Adjustment
            # 3.3.1. Content info > Effect Track > Alias
            # show alias correctly
            main_page.enter_room(3)
            effect_room_page.right_click_addto_timeline('Aberration')

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_1_6.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_1_6.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.click_undo()

            object_status = timeline_operation_page.exist(L.timeline_operation.timeline_vertical_scroll_bar)
            if not object_status:
                logger('timeline vertical scroll bar disable')
            else:
                timeline_operation_page.drag_timeline_vertical_scroll_bar(0.0)

        with uuid('aa99a901-db12-4704-b423-510024be0b43') as case:
            # 3.3. Content and Adjustment
            # 3.3.1. Content info > Video Track > Effect i mark
            # show all fixes/adjustment when hover on i icon
            effect_room_page.apply_effect_to_video('Aberration', 0, 0)
            timeline_operation_page.hover_i_mark(0, 0)

            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_1_3.png'
            current_preview = timeline_operation_page.snapshot_i_mark_tooltip(0, 0)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('e157fa9e-9cc5-4e91-b30d-e8d6572094c1') as case:
            # 3.3. Content and Adjustment
            # 3.3.1. Content info > Video Track > Transition icon
            # show correct transition icon
            main_page.enter_room(0)
            main_page.select_library_icon_view_media("Skateboard 02.mp4")
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.enter_room(2)
            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Cross')
            timeline_operation_page.click_view_entire_video_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_1_4.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_1_4.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid('178d1907-f770-4a56-ab98-65aa4d6877ad') as case:
            # 3.3. Content and Adjustment
            # 3.3.2. Reposition > Single file > to same track
            # clip can move to different position correctly
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.drag_single_media_move_to(0, 0, 200)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_2_1.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_2_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('c625e71e-251a-4143-b222-a8f38b5d8fd9') as case:
            # 3.3. Content and Adjustment
            # 3.3.2. Reposition > Single file > to different track
            # clip can move to different position correctly
            timeline_operation_page.drag_single_media_to_other_track(0, 0, -200, 2)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_2_2.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_2_2.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('67d8588f-87ab-4159-be6c-276478a67ddf') as case:
            # 3.3. Content and Adjustment
            # 3.3.2. Reposition > Multi select files > to same track
            # clip can move to different position correctly
            main_page.select_library_icon_view_media("Skateboard 02.mp4")
            main_page.tips_area_insert_media_to_selected_track(option=1)
            timeline_operation_page.drag_multi_media_move_to(2, 0, 2, 1, 200)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_2_3.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_2_3.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('9ccd1d6f-7076-42c8-8f42-c205d1e195ba') as case:
            # 3.3. Content and Adjustment
            # 3.3.2. Reposition > Multi select files > to different track
            # clip can move to different position correctly
            timeline_operation_page.deselect_clip(2, 1, 100)
            timeline_operation_page.drag_multi_media_move_to_other_track(2, 0, 2, 1, -200, -2)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_2_4.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_2_4.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('a6d095a5-8cdd-4d9b-9a78-f0b2e13109db') as case:
            # 3.3. Content and Adjustment
            # 3.3.3. Trim (Drag the content left/right border) > Single file
            # clip can trim duration correctly
            timeline_operation_page.drag_timeline_clip('Last', 0.5, 0, 1)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_3_1.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_3_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.click_undo()

        # with uuid('dc5b7024-f590-477a-8b4e-9528d2c980bc') as case:
        #     # 3.3. Content and Adjustment
        #     # 3.3.3. Trim (Drag the content left/right border) > Virtual cut video
        #     # clip can trim duration correctly
        #     # AT page function not ready (Video Collage Designer)
        #     case.result = None

        with uuid('7f74d938-ab8c-4409-962f-1c2d7be2ba4e') as case:
            # 3.3. Content and Adjustment
            # 3.3.3. Trim (Drag the content left/right border) > Multi select files
            # clip can trim duration correctly
            timeline_operation_page.deselect_clip(track_index=0, last_clip_index=1, movement=100)
            timeline_operation_page.drag_single_media_to_other_track(
                track_index=0, clip_index=0, distance=0, track_num=2)
            timeline_operation_page.select_multiple_timeline_media(
                media1_track_index=2, media1_clip_index=0, media2_track_index=0, media2_clip_index=0)
            timeline_operation_page.drag_timeline_clip(
                mode='Last', ratio=0.5, track_index1=0, clip_index1=0, track_index2=None, clip_index2=None)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_3_2.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_3_2.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('8d112ec7-7a81-4300-b598-9ee645f19f94') as case:
            # 3.3. Content and Adjustment
            # 3.3.4. Speed Adjustment (Hold Ctrl Key and drag the content left/right border) > Video speed
            # speed can adjust correctly
            main_page.close_and_restart_app()
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.drag_to_change_speed(
                track_index=0, clip_index=0, mode='Last', direction='Right', ratio=1)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_4_1.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_4_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('de0728d0-3d7b-4459-be09-0ca3e74739e2') as case:
            # 3.3. Content and Adjustment
            # 3.3.4. Speed Adjustment (Hold Ctrl Key and drag the content left/right border) > Video speed
            # setting will sync speed designer
            main_page.tap_TipsArea_Tools_menu('Video Speed')
            set_check_result = L.video_speed.main
            time.sleep(DELAY_TIME * 2)
            if not video_speed_page.exist(locator=set_check_result):
                case.result = False
            else:
                image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_4_2.png'
                ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_4_2.png'
                current_preview = timeline_operation_page.snapshot(
                    locator=set_check_result, file_name=image_full_path)

                check_result = timeline_operation_page.compare(ground_truth, current_preview)
                case.result = check_result

            main_page.press_esc_key()
            time.sleep(DELAY_TIME)
            main_page.click_undo()
            main_page.click_undo()
            main_page.click_undo()

        with uuid('937c7719-e3ef-49e6-97be-5cafe74262c4') as case:
            # 3.3. Content and Adjustment
            # 3.3.4. Speed Adjustment (Hold Ctrl Key and drag the content left/right border) > Audio speed
            # speed can adjust correctly
            main_page.insert_media('Mahoroba.mp3')
            timeline_operation_page.drag_to_change_speed(
                track_index=1, clip_index=0, mode='Last', direction='Left', ratio=0.5)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_4_3.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_4_3.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('991dc151-f29a-4d85-b352-ffd1ebd14467') as case:
            # 3.3. Content and Adjustment
            # 3.3.4. Speed Adjustment (Hold Ctrl Key and drag the content left/right border) > Audio speed
            # setting will sync speed designer
            main_page.tap_TipsArea_Tools_menu('Audio Speed')
            time.sleep(DELAY_TIME * 2)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_4_4.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_4_4.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.base.main_window, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.press_esc_key()

        with uuid('7322642e-3fd1-4c83-a903-94cca58c636b') as case:
            # 3.3. Content and Adjustment
            # 3.3.7. Skip "Snap" by pressing Alt Key > Move Clip
            # no snap with other timeline object
            main_page.close_and_restart_app()
            main_page.insert_media('Skateboard 01.mp4')
            main_page.select_library_icon_view_media("Skateboard 02.mp4")
            main_page.tips_area_insert_media_to_selected_track(option=1)
            timeline_operation_page.drag_single_media_move_to(0, 1, 100)

            check_result = timeline_operation_page.drag_no_snap(0)
            case.result = check_result

            main_page.click_undo()
            main_page.click_undo()

        with uuid('9f6227d8-4f23-4919-b2e0-e257dd5746a4') as case:
            # 3.3. Content and Adjustment
            # 3.3.7. Skip "Snap" by pressing Alt Key > Trim by dragging clip edge
            # no snap with other timeline object
            timeline_operation_page.trim_no_snap(0, 1)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_3_3_7_1.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_3_3_7_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.click_undo()

        with uuid('1ec0ecd8-0f50-4283-9b96-1b0ed4934bf1') as case:
            # 4. Advanced Testing
            # 4.1. Playback
            # 4.1.1. Previous / Next frame > Click button when playing
            # pause and seed to previous/next frame
            playback_window_page.Edit_Timeline_PreviewOperation('Stop')
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 3)
            for i in range(5):
                playback_window_page.Edit_Timeline_PreviewOperation('Next_Frame')
                time.sleep(DELAY_TIME * 0.5)
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 3)
            for i in range(5):
                playback_window_page.Edit_Timeline_PreviewOperation('Previous_Frame')
                time.sleep(DELAY_TIME * 0.5)

            image_full_path = Auto_Ground_Truth_Folder + 'timeline_operation_4_1_1_1.png'
            ground_truth = Ground_Truth_Folder + 'timeline_operation_4_1_1_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.playback_window.main, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    292c8c63-6043-4f8a-9573-83b16ea06be6
                    2444bfee-7f6d-45fe-b571-40d10e293438
                    d3842e6d-66dc-41e7-a644-ec74d482271a
                    83a7b17f-c07f-496c-bc4e-030c2a53e546
                    ae5957b2-e117-4dfc-9a52-6e5889ae76ef
                    f414358a-c943-412e-85ea-da3caf43056e
                    fb2360a4-1276-4431-918a-46c1d87424b8
                    04a8a4c7-f547-4611-9c25-c65e96595061
                    902f44ed-00be-4000-b6f0-e5208e2d19e8
                    af424f04-f50a-4c78-9335-2404a63503ee
                    0ecb63ca-dcf4-441d-94bb-8034ca44336f
                    8d708def-30a2-43fc-a5da-9ce59b673148
                    dddce75b-98d4-4433-93b0-aa38948cc120
                    2ebe8d7a-73e8-4fcf-b7f8-0f096dfb656f
                    62866169-c89a-46c1-ae80-e8d416571918
                    4fb96f45-0259-412a-99be-3bf3a3bc016f
                    2fd448c7-0754-4e68-8aa2-0d221b1c931c
                    ba5334cf-ad72-4b56-ac50-0009fab3be74
                    686cad20-34fd-4d46-9589-e1897b8916e7
                    65756340-ebae-4538-946e-4ee643eef230
                    459083e6-6d03-42a5-affa-866a282627fa
                    daa5804f-2992-410a-b980-89da68c2a381
                    9cbe07b1-9835-4066-9116-ea5a46ea66e1
                    4896998a-3dfe-48b9-b84a-88c9e425fed0
                    9050898e-c436-45a0-84cf-60f85cce3cce
                    5eb932bd-ac7f-4368-9c25-a1eb19f7ba65
                    35dec4cb-cd78-421c-bdb3-5ed664d3e89d
                    c2784023-3f72-4621-b136-386d6f9425cd
                    1945e7db-9536-4a1a-8626-86250f9422b5
                    578b944d-5574-46e2-9e1d-89b7fae39e59
                    0789e1b4-d1da-4b2b-935b-ec17435d8433
                    07e4c03e-0045-42d4-817e-ecc74db78ece
                    67106ca6-9735-49ee-b460-4f41ad4a5d38
                    d10ed3dd-fefe-47a9-83ff-8c12c743086b
                    e6236a1d-d69a-4625-8f9c-6300d12c0a04
                    cd66c554-4550-48c9-bd41-6811246715e3
                    8031bea4-5c35-4a13-8bbc-cb87e96e5c3d
                    f3b1f353-cad6-4f93-8ce6-7feb760973e0
                    90e633dd-72ea-4365-b794-6c9ee4ba0151
                    426775d9-4476-4bc2-80db-9941b0056394
                    20ee22d4-22dd-4074-8bfc-f4fcd2ae9621
                    4cd52b97-7d77-411b-9ef6-f55cd4850ed9
                    dc5b7024-f590-477a-8b4e-9528d2c980bc
                    a7ace6f4-6152-404f-baea-d9420106a5a2
                    9413e968-4fd6-47da-b87b-991974561054
                    dccdb6cd-3ca4-405b-92a4-6ca2f5b73546
                    d10c7cc5-ad41-424b-a3ea-ae862e07e705
                    d15403d8-a449-411c-b47a-ef86f66dc1b5
                    3957ca13-fa15-4944-b687-235070c06bca
                    003363eb-4ab3-41ad-900c-f4b07baadabe
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'
