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
nest_project_page = PageFactory().get_page_object('nest_project_page', mwc)
project_room_page = PageFactory().get_page_object('project_room_page', mwc)
project_new_page = PageFactory().get_page_object('project_new_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
produce_page = PageFactory().get_page_object('produce_page', mwc)
keyframe_room_page = PageFactory().get_page_object('keyframe_room_page', mwc)
precut_page = PageFactory().get_page_object('precut_page', mwc)
crop_image_page = PageFactory().get_page_object('crop_image_page', mwc)
video_collage_designer_page = PageFactory().get_page_object('video_collage_designer_page', mwc)

# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Nested Project_p2.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Nested_Project/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Nested_Project/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Nested_Project_p2():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(3)
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
            google_sheet_execution_log_init('Nested_Project_p2')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"Nested Project result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
    def test_1_1_6(self):
        # unlink the inserted project
        with uuid("3c4351b5-21a5-4b8e-8812-a786446f6482") as case:
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            timeline_page.timeline_click_zoomin_btn()
            timeline_page.timeline_click_zoomin_btn()
            time.sleep(1)
            tips_area_page.more_features.link_unlink_video_audio()
            main_page.timeline_select_track(3)
            timeline_page.select_timeline_media('1', '0')
            tips_area_page.more_features.remove()
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                                   file_name=Auto_Ground_Truth_Folder + 'Workspace_unlink_remove.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_unlink_remove.png',
                                                   current_image)
            case.result = compare_result

        # undo, select all
        with uuid("c073af26-0787-48af-9147-7e84ab64a099") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            tips_area_page.more_features.select_all()
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                           file_name=Auto_Ground_Truth_Folder + 'Workspace_SelectAll.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_SelectAll.png',
                                           current_image)
            case.result = compare_result

        # group clips, move to other track
        with uuid("155508b1-4c42-40bf-b5b1-59c149b695d5") as case:
            time.sleep(1)
            tips_area_page.more_features.group_ungroup_obj()
            main_page.timeline_select_track(3)
            timeline_page.select_timeline_media('1', '0')
            timeline_page.drag_single_media_to_other_track(0, 0, 100, 1)
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                                   file_name=Auto_Ground_Truth_Folder + 'Workspace_GroupMove.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_GroupMove.png',
                                                   current_image)
            case.result = compare_result

        # undo, split, remove
        with uuid("659ae1e8-91be-4afb-bf10-cd8f72a38d0e") as case:
            time.sleep(1)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            main_page.set_timeline_timecode('00_00_10_00')
            tips_area_page.more_features.split()
            tips_area_page.more_features.remove()
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                                   file_name=Auto_Ground_Truth_Folder + 'Workspace_SplitRemove.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_SplitRemove.png',
                                                   current_image)
            case.result = compare_result

        # undo, edit alias
        with uuid("864721af-75f0-4e8d-a35f-ae5cf76bc76f") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            main_page.tap_Undo_hotkey()
            tips_area_page.more_features.click_change_alias()
            case.result = tips_area_page.more_features.set_alias('345678900123')

        # reset alias
        with uuid("6023b056-df9d-4c0e-a9bb-c9196c6f43f2") as case:
            time.sleep(1)
            tips_area_page.more_features.click_reset_alias()
            check_result = tips_area_page.more_features.get_alias()
            if check_result == "":
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        # view properties is disable for nested project
        with uuid("edb5f2e0-2681-4682-b4f9-32ce78bd5751") as case:
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            tips_area_page.more_features.click_btn()
            time.sleep(1)
            check_result = tips_area_page.more_features.get_menu_status('View Properties')
            if check_result == None:
                case.result = False
            else:
                case.result = not check_result

        # Reset all undocked window is disable if all window is docked
        with uuid("07c8bda6-5c50-4b49-865a-558ebb5adfcd") as case:
            time.sleep(1)
            tips_area_page.more_features.click_btn()
            time.sleep(1)
            check_result = tips_area_page.more_features.get_menu_status('Reset All Undocked Windows')
            if check_result == None:
                case.result = False
            else:
                case.result = not check_result

        # undock timeline window
        with uuid("49c53175-5e79-4daa-aa1f-788453154fd1") as case:
            time.sleep(1)
            case.result = tips_area_page.more_features.dock_undock_timeline_window(True)

        # reset all undocked window from more features button
        with uuid("ac6704fc-3ea9-4045-b2f9-10ea76d49668") as case:
            with uuid("e2b473b6-e27f-4378-973e-5e045a174921") as case:
                time.sleep(1)
                case.result = tips_area_page.more_features.reset_all_undock_windows()
            case.result = True

        # split nested project
        with uuid("e690ece2-70a5-4bc6-9951-a12dfe4387c7") as case:
            time.sleep(1)
            timeline_page.timeline_click_zoomin_btn()
            timeline_page.timeline_click_zoomin_btn()
            main_page.set_timeline_timecode('00_00_10_00')
            time.sleep(1)
            tips_area_page.click_TipsArea_btn_split()
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                                   file_name=Auto_Ground_Truth_Folder + 'Workspace_SplitProject.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_SplitProject.png',
                                                   current_image)
            case.result = compare_result

        # open keyframe room
        with uuid("1eb19560-337f-430d-ae26-479a0384cf2a") as case:
            time.sleep(1)
            case.result = tips_area_page.tips_area_click_key_frame()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        # copy and then paste the range selection
        with uuid("0a69f05a-e464-44fe-b872-67a9210fcd07") as case:
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            timeline_page.timeline_click_zoomin_btn()
            timeline_page.timeline_click_zoomin_btn()
            main_page.set_timeline_timecode('00_00_10_00')
            time.sleep(1)
            # 1 sec = 30 frame, (5 sec, 15 sec) = 150, 450
            timeline_operation_page.set_range_markin_markout(150, 450)
            time.sleep(1)
            tips_area_page.click_TipsArea_btn_Copy()
            tips_area_page.click_TipsArea_btn_Paste()
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                                   file_name=Auto_Ground_Truth_Folder + 'Workspace_PasteNestedProject.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_PasteNestedProject.png',
                                                   current_image)
            case.result = compare_result

        # cut the range selection
        with uuid("d777cc8e-e772-4aa1-886a-6d87f318669f") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            time.sleep(1)
            tips_area_page.click_TipsArea_btn_Cut()
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                           file_name=Auto_Ground_Truth_Folder + 'Workspace_CutProject.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_CutProject.png',
                                           current_image)
            case.result = compare_result

        # remove the range selection
        with uuid("9ec47e19-5c71-4b3c-b05e-acc46c89acef") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            time.sleep(1)
            tips_area_page.click_TipsArea_btn_Remove()
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                           file_name=Auto_Ground_Truth_Folder + 'Workspace_RemoveProject.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_RemoveProject.png',
                                           current_image)
            case.result = compare_result

        # render the range selection
        with uuid("2f41f6e8-f98c-4da4-8808-03b9c399ca81") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            time.sleep(1)
            playback_window_page.Edit_Timeline_PreviewOperation('Stop')
            time.sleep(1)
            timeline_page.edit_timeline_render_preview()
            time.sleep(6)
            current_image = timeline_page.snapshot_timeline_render_clip(0, 0,
                                                                        file_name=Auto_Ground_Truth_Folder + 'Render_NestedProject.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Render_NestedProject.png', current_image)
            case.result = compare_result

        # lock the range selection and able to seek out of range
        with uuid("5c796a08-d014-4a1e-8a6e-d1bf2b6809c3") as case:
            time.sleep(1)
            timeline_operation_page.set_range_markin_markout(150, 450)
            time.sleep(1)
            tips_area_page.click_TipsArea_btn_Lock_Range()
            time.sleep(1)
            case.result = main_page.set_timeline_timecode('00_00_18_00')

        # able to switch to produce page for selected range
        with uuid("6591dc0c-d97f-4f60-af88-e6e8df2bbd03") as case:
            time.sleep(1)
            case.result = tips_area_page.click_TipsArea_btn_Produce_Range()
            logger('335')
            time.sleep(5)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        # move frame from timeline preview
        with uuid("aec5345b-6dab-4695-b008-147372d9fd3b") as case:
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            playback_window_page.adjust_timeline_preview_on_canvas_drag_move_to_left()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'MoveFromPreview.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'MoveFromPreview.png', current_image)
            case.result = compare_result

        # undo and then resize frame from timeline preview
        with uuid("221aff61-2ef5-4761-bf2d-b45f1314bf48") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            time.sleep(1)
            playback_window_page.adjust_timeline_preview_on_canvas_resize_to_small()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'ResizeFromPreview.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'ResizeFromPreview.png', current_image, similarity=0.7)
            case.result = compare_result

        # undo and then rotate frame from timeline preview
        with uuid("214e341b-c29a-4fc5-9376-472be68a6a58") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            time.sleep(1)
            playback_window_page.adjust_timeline_preview_on_canvas_drag_rotate_clockwise()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                             file_name=Auto_Ground_Truth_Folder + 'RotateFromPreview.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'RotateFromPreview.png', current_image)
            case.result = compare_result

        # undo and then set freeform from timeline preview
        with uuid("269880e1-0537-49de-8aec-fe047400b07f") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            time.sleep(1)
            playback_window_page.adjust_timeline_preview_on_canvas_freeform()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'SetFreeformFromPreview.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'SetFreeformFromPreview.png', current_image)
            case.result = compare_result

        # undo and switch into keyframe, check the project thumb
        with uuid("9cbd73a2-8d5a-4884-a50b-a2fc3242df37") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            time.sleep(1)
            tips_area_page.click_keyframe()
            time.sleep(1)
            current_image = keyframe_room_page.snapshot(locator=L.keyframe_room.image_thumbnail,
                                             file_name=Auto_Ground_Truth_Folder + 'KeyframeRoom_ProjectThumb.png')
            compare_result = keyframe_room_page.compare(Ground_Truth_Folder + 'KeyframeRoom_ProjectThumb.png', current_image)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_10(self):
        # insert project and set position keyframe for nested project
        # Add and then remove keyframe
        with uuid("bf1b17c9-9cf7-4872-aa37-e41fd0226c07") as case:
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            main_page.set_timeline_timecode('00_00_07_00')
            tips_area_page.click_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.unfold_tab(1)
            time.sleep(1)
            case.result_1 = keyframe_room_page.clip_attributes.position.add_remove_keyframe()
            time.sleep(1)
            case.result_2 = keyframe_room_page.clip_attributes.position.add_remove_keyframe()
            case.result = case.result_1 and case.result_2

        # Add and then reset position keyframe
        with uuid("79010f1a-ead4-4033-b43e-d54d303079c0") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.position.add_remove_keyframe()
            time.sleep(1)
            case.result = keyframe_room_page.clip_attributes.position.reset_keyframe()

        # switch position keyframe by next keyframe and previous keyframe button
        with uuid("bdcce006-5948-4edb-8c75-ced84eae3f65") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.position.add_remove_keyframe()
            time.sleep(1)
            main_page.set_timeline_timecode('00_00_12_00')
            time.sleep(1)
            keyframe_room_page.clip_attributes.position.add_remove_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.position.previous_keyframe()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Switch_Prev_frame.png')
            compare_result_1 = title_room_page.compare(Ground_Truth_Folder + 'Switch_Prev_frame.png',
                                                       current_image)
            keyframe_room_page.clip_attributes.position.next_keyframe()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Switch_Next_frame.png')
            compare_result_2 = title_room_page.compare(Ground_Truth_Folder + 'Switch_Next_frame.png',
                                                       current_image)
            case.result = compare_result_1 and compare_result_2

        # set position x value
        with uuid("5b0e16e9-7e5b-4b0e-a0a3-86601006365c") as case:
            time.sleep(1)
            case.result_1 = keyframe_room_page.clip_attributes.position.previous_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.position.x.set_value(0.6)
            time.sleep(1)
            check_value = keyframe_room_page.clip_attributes.position.x.get_value()
            logger(check_value)
            if check_value == '0.600':
                case.result = True
            else:
                case.result = False

        # set position y value
        with uuid("a20d96c9-cfc9-4a17-9af0-bae243d7ffb3") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.position.y.set_value(0.7)
            time.sleep(1)
            check_value = keyframe_room_page.clip_attributes.position.y.get_value()
            logger(check_value)
            if check_value == '0.700':
                case.result = True
            else:
                case.result = False

        # set ease out and value
        with uuid("3575cd3e-17cb-453f-aa30-6a51ddf37f62") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.position.ease_out.set_checkbox(True)
            keyframe_room_page.clip_attributes.position.ease_out.set_value(0.6)
            check_value = keyframe_room_page.clip_attributes.position.ease_out.get_value()
            logger(check_value)
            if check_value == '0.60':
                case.result = True
            else:
                case.result = False

        # to next position keyframe and set ease in & value, then reset keyframe finally
        with uuid("8f163b75-a140-4a3a-b99e-8738d0908c98") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.position.next_keyframe()
            keyframe_room_page.clip_attributes.position.ease_in.set_checkbox(True)
            keyframe_room_page.clip_attributes.position.ease_in.set_value(0.7)
            time.sleep(1)
            check_value = keyframe_room_page.clip_attributes.position.ease_in.get_value()
            logger(check_value)
            if check_value == '0.70':
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_11(self):
        # insert project and set scale keyframe for nested project
        # Add and then remove keyframe
        with uuid("bb782470-34fe-44b0-b410-e03c5a65516c") as case:
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            main_page.set_timeline_timecode('00_00_07_00')
            tips_area_page.click_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.unfold_tab(1)
            time.sleep(1)
            case.result_1 = keyframe_room_page.clip_attributes.scale.add_remove_keyframe()
            time.sleep(1)
            case.result_2 = keyframe_room_page.clip_attributes.scale.add_remove_keyframe()
            case.result = case.result_1 and case.result_2

        # Add and then reset scale keyframe
        with uuid("cfa74700-1907-49b6-a8b5-5966b9a2a2f5") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.scale.add_remove_keyframe()
            time.sleep(1)
            case.result = keyframe_room_page.clip_attributes.scale.reset_keyframe()

        # switch scale keyframe by next keyframe and previous keyframe button
        with uuid("316f95d4-1ba3-40ec-859b-bbe3095c144a") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.scale.add_remove_keyframe()
            time.sleep(1)
            main_page.set_timeline_timecode('00_00_12_00')
            time.sleep(1)
            keyframe_room_page.clip_attributes.scale.add_remove_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.scale.previous_keyframe()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Switch_Prev_ScaleKey.png')
            compare_result_1 = title_room_page.compare(Ground_Truth_Folder + 'Switch_Prev_ScaleKey.png',
                                                       current_image)
            keyframe_room_page.clip_attributes.scale.next_keyframe()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Switch_Next_ScaleKey.png')
            compare_result_2 = title_room_page.compare(Ground_Truth_Folder + 'Switch_Next_ScaleKey.png',
                                                       current_image, similarity=0.8)
            case.result = compare_result_1 and compare_result_2

        # set scale width value when maintain aspect ratio
        with uuid("79e8c1de-98e0-4ed9-b3f0-69c315dbedc4") as case:
            time.sleep(1)
            case.result_1 = keyframe_room_page.clip_attributes.scale.previous_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.scale.width.set_value(0.300)
            time.sleep(1)
            check_value = keyframe_room_page.clip_attributes.scale.width.get_value()
            logger(check_value)
            if check_value == '0.300':
                case.result = True
            else:
                case.result = False

        # check scale height value if same as scale width
        with uuid("3ece3976-7100-456c-82c8-7688818e8c84") as case:
            time.sleep(1)
            check_value = keyframe_room_page.clip_attributes.scale.height.get_value()
            logger(check_value)
            if check_value == '0.300':
                case.result = True
            else:
                case.result = False

        # uncheck maintain aspect ratio and then set scale height
        with uuid("212f4fb9-cae6-4aaa-bbc0-7840e4e99504") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.scale.set_maintain_aspect_ratio(0)
            keyframe_room_page.clip_attributes.scale.height.set_value(0.800)
            time.sleep(1)
            check_value = keyframe_room_page.clip_attributes.scale.height.get_value()
            logger(check_value)
            if check_value == '0.800':
                case.result = True
            else:
                case.result = False

        # set ease out for scale keyframe
        with uuid("c4fa307e-d084-420e-bfa7-51157008c6a9") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.scale.ease_out.set_checkbox(True)
            keyframe_room_page.clip_attributes.scale.ease_out.set_value(0.75)
            check_value = keyframe_room_page.clip_attributes.scale.ease_out.get_value()
            logger(check_value)
            if check_value == '0.75':
                case.result = True
            else:
                case.result = False

        # set ease in for scale keyframe
        with uuid("d3b7ff48-f340-4972-b400-5d3c5bca4851") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.scale.next_keyframe()
            keyframe_room_page.clip_attributes.scale.ease_in.set_checkbox(True)
            keyframe_room_page.clip_attributes.scale.ease_in.set_value(0.65)
            check_value = keyframe_room_page.clip_attributes.scale.ease_in.get_value()
            logger(check_value)
            if check_value == '0.65':
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_12(self):
        # insert project and set opacity keyframe for nested project
        # Add and then remove keyframe
        with uuid("8da61fcd-3430-456a-968e-c01da238ac73") as case:
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            main_page.set_timeline_timecode('00_00_07_00')
            tips_area_page.click_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.opacity.show()
            time.sleep(1)
            case.result_1 = keyframe_room_page.clip_attributes.opacity.add_remove_keyframe()
            time.sleep(1)
            case.result_2 = keyframe_room_page.clip_attributes.opacity.add_remove_keyframe()
            case.result = case.result_1 and case.result_2

        # Add opacity keyframe and then reset
        with uuid("21713d41-3dba-4729-8234-e4bfced0c208") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.opacity.add_remove_keyframe()
            time.sleep(1)
            case.result = keyframe_room_page.clip_attributes.opacity.reset_keyframe()

        # Add two opacity keyframes and then switch keyframe
        with uuid("9c82ab7f-5ae2-47d3-ae5b-588a2c1ea6f9") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.opacity.add_remove_keyframe()
            main_page.set_timeline_timecode('00_00_12_00')
            time.sleep(1)
            keyframe_room_page.clip_attributes.opacity.add_remove_keyframe()
            keyframe_room_page.clip_attributes.opacity.previous_keyframe()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Switch_Prev_OpacityKey.png')
            compare_result_1 = title_room_page.compare(Ground_Truth_Folder + 'Switch_Prev_OpacityKey.png',
                                                       current_image)
            keyframe_room_page.clip_attributes.opacity.next_keyframe()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Switch_Next_OpacityKey.png')
            compare_result_2 = title_room_page.compare(Ground_Truth_Folder + 'Switch_Next_OpacityKey.png',
                                                       current_image)
            case.result = compare_result_1 and compare_result_2

        # Set opacity value
        with uuid("0ad96a1f-f72a-4751-9ae8-6177fabbe29d") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.opacity.set_value(50)
            time.sleep(1)
            check_value = keyframe_room_page.clip_attributes.opacity.get_value()
            logger(check_value)
            if check_value == '50':
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_13(self):
        # insert project and set rotation keyframe for nested project
        # Add and then remove keyframe
        with uuid("8c96c8c4-ae60-4a0a-8ab9-fd7e8e582ce4") as case:
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            main_page.set_timeline_timecode('00_00_07_00')
            tips_area_page.click_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.rotation.show()
            time.sleep(1)
            case.result_1 = keyframe_room_page.clip_attributes.rotation.add_remove_keyframe()
            time.sleep(1)
            case.result_2 = keyframe_room_page.clip_attributes.rotation.add_remove_keyframe()
            case.result = case.result_1 and case.result_2

        # Add rotation keyframe and then reset
        with uuid("94c3f8ea-3dc2-4324-a4b3-0b43981dd6d8") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.rotation.add_remove_keyframe()
            time.sleep(1)
            case.result = keyframe_room_page.clip_attributes.rotation.reset_keyframe()

        # Add two rotation keyframes and then switch keyframe
        with uuid("2accb331-2eb2-4c31-80f6-008c23bb29f8") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.rotation.add_remove_keyframe()
            main_page.set_timeline_timecode('00_00_12_00')
            time.sleep(1)
            keyframe_room_page.clip_attributes.rotation.add_remove_keyframe()
            keyframe_room_page.clip_attributes.rotation.previous_keyframe()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                         file_name=Auto_Ground_Truth_Folder + 'Switch_Prev_RotateKey.png')
            compare_result_1 = title_room_page.compare(Ground_Truth_Folder + 'Switch_Prev_RotateKey.png',
                                                           current_image)
            keyframe_room_page.clip_attributes.rotation.next_keyframe()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                         file_name=Auto_Ground_Truth_Folder + 'Switch_Next_RotateKey.png')
            compare_result_2 = title_room_page.compare(Ground_Truth_Folder + 'Switch_Next_RotateKey.png',
                                                           current_image)
            case.result = compare_result_1 and compare_result_2

        # Set rotation value
        with uuid("23b6ba78-42e9-4e58-9544-f39dbcc6339c") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.rotation.set_value(45)
            time.sleep(1)
            check_value = keyframe_room_page.clip_attributes.rotation.get_value()
            logger(check_value)
            if check_value == '45.00':
                case.result = True
            else:
                case.result = False

        # set ease out for rotation keyframe
        with uuid("b3dc9a05-ec12-4655-b836-18a3739fd437") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.rotation.previous_keyframe()
            keyframe_room_page.clip_attributes.rotation.ease_out.set_checkbox(True)
            keyframe_room_page.clip_attributes.rotation.ease_out.set_value(0.80)
            check_value = keyframe_room_page.clip_attributes.rotation.ease_out.get_value()
            logger(check_value)
            if check_value == '0.80':
                case.result = True
            else:
                case.result = False

        # set ease in for rotation keyframe
        with uuid("1a649fa1-9185-45d2-a545-acd08a4c3cf7") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.rotation.next_keyframe()
            keyframe_room_page.clip_attributes.rotation.ease_in.set_checkbox(True)
            keyframe_room_page.clip_attributes.rotation.ease_in.set_value(0.60)
            check_value = keyframe_room_page.clip_attributes.rotation.ease_in.get_value()
            logger(check_value)
            if check_value == '0.60':
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_14(self):
        # insert project and set freeform keyframe for nested project
        # Add and then remove keyframe
        with uuid("f9367d73-dede-4a50-8b54-e658bc8698ec") as case:
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            main_page.set_timeline_timecode('00_00_07_00')
            tips_area_page.click_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.freeform.show()
            time.sleep(1)
            case.result_1 = keyframe_room_page.clip_attributes.freeform.add_remove_keyframe()
            time.sleep(1)
            case.result_2 = keyframe_room_page.clip_attributes.freeform.add_remove_keyframe()
            case.result = case.result_1 and case.result_2

        # Add freeform keyframe and then reset
        with uuid("e3d8e673-b715-41a7-a923-e6618deb4ff8") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.freeform.add_remove_keyframe()
            time.sleep(1)
            case.result = keyframe_room_page.clip_attributes.freeform.reset_keyframe()

        # add two freeform keyframe and then switch
        with uuid("db7d815c-9303-4df8-a0e2-749ae784330a") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.freeform.add_remove_keyframe()
            main_page.set_timeline_timecode('00_00_12_00')
            time.sleep(1)
            keyframe_room_page.clip_attributes.freeform.add_remove_keyframe()
            keyframe_room_page.clip_attributes.freeform.previous_keyframe()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                         file_name=Auto_Ground_Truth_Folder + 'Switch_Prev_FreeFormKey.png')
            compare_result_1 = title_room_page.compare(Ground_Truth_Folder + 'Switch_Prev_FreeFormKey.png',
                                                           current_image)
            keyframe_room_page.clip_attributes.freeform.next_keyframe()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                         file_name=Auto_Ground_Truth_Folder + 'Switch_Next_FreeFormKey.png')
            compare_result_2 = title_room_page.compare(Ground_Truth_Folder + 'Switch_Next_FreeFormKey.png',
                                                           current_image)
            case.result = compare_result_1 and compare_result_2

        # set top-left position x/y value
        with uuid("6c539c6f-cfa9-4910-a4d6-aecccac2a9c3") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.freeform.top_left_x.set_value(0.300)
            check_value_1 = keyframe_room_page.clip_attributes.freeform.top_left_x.get_value()
            logger(check_value_1)
            if check_value_1 == '0.300':
                case.result_1 = True
            else:
                case.result_1 = False

            keyframe_room_page.clip_attributes.freeform.top_left_y.set_value(0.500)
            check_value_2 = keyframe_room_page.clip_attributes.freeform.top_left_y.get_value()
            logger(check_value_2)
            if check_value_2 == '0.500':
                case.result_2 = True
            else:
                case.result_2 = False

            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                             file_name=Auto_Ground_Truth_Folder + 'FreeForm_Top_Left.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'FreeForm_Top_Left.png',
                                               current_image, similarity=0.8)

            case.result = case.result_1 and case.result_2 and compare_result

        # Remove keyframe and add keyframe, set top-right position x/y value
        with uuid("9b7aad59-769a-43eb-a0e0-eed7e71a6fdf") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.freeform.add_remove_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.freeform.add_remove_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.freeform.top_right_x.set_value(0.400)
            check_value_1 = keyframe_room_page.clip_attributes.freeform.top_right_x.get_value()
            logger(check_value_1)
            if check_value_1 == '0.400':
                case.result_1 = True
            else:
                case.result_1 = False

            keyframe_room_page.clip_attributes.freeform.top_right_y.set_value(0.300)
            check_value_2 = keyframe_room_page.clip_attributes.freeform.top_right_y.get_value()
            logger(check_value_2)
            if check_value_2 == '0.300':
                case.result_2 = True
            else:
                case.result_2 = False

            case.result = case.result_1 and case.result_2

        # Remove keyframe and add keyframe, set bottom-left position x/y value
        with uuid("c445c265-d0ac-41f2-8c3b-6f36be6b09e6") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.freeform.add_remove_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.freeform.add_remove_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.freeform.bottom_left_x.set_value(0.600)
            check_value_1 = keyframe_room_page.clip_attributes.freeform.bottom_left_x.get_value()
            logger(check_value_1)
            if check_value_1 == '0.600':
                case.result_1 = True
            else:
                case.result_1 = False

            keyframe_room_page.clip_attributes.freeform.bottom_left_y.set_value(0.800)
            check_value_2 = keyframe_room_page.clip_attributes.freeform.bottom_left_y.get_value()
            logger(check_value_2)
            if check_value_2 == '0.800':
                case.result_2 = True
            else:
                case.result_2 = False

            case.result = case.result_1 and case.result_2

        # Remove keyframe and add keyframe, set bottom-right position x/y value and then snapshot
        with uuid("162c48ae-17d2-47a7-8733-dae7d719839e") as case:
            time.sleep(1)
            keyframe_room_page.clip_attributes.freeform.add_remove_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.freeform.add_remove_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.freeform.bottom_right_x.set_value(0.600)
            check_value_1 = keyframe_room_page.clip_attributes.freeform.bottom_right_x.get_value()
            logger(check_value_1)
            if check_value_1 == '0.600':
                case.result_1 = True
            else:
                case.result_1 = False

            keyframe_room_page.clip_attributes.freeform.bottom_right_y.set_value(0.700)
            check_value_2 = keyframe_room_page.clip_attributes.freeform.bottom_right_y.get_value()
            logger(check_value_2)
            if check_value_2 == '0.700':
                case.result_2 = True
            else:
                case.result_2 = False

            main_page.set_timeline_timecode('00_00_10_00')
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'FreeForm_Bottom_Right.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'FreeForm_Bottom_Right.png',
                                                     current_image, similarity=0.8)

            case.result = case.result_1 and case.result_2 and compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_15(self):
        # insert project and set keyframe for nested project, and copy keyframe from right-click menu
        with uuid("3a316f6c-4af2-43a9-b994-f6d821038285") as case:
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            main_page.tap_Copy_hotkey()
            time.sleep(1)
            main_page.tap_Paste_hotkey()
            time.sleep(1)
            timeline_page.select_right_click_menu('Insert')
            time.sleep(1)
            tips_area_page.click_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.rotation.show()
            keyframe_room_page.clip_attributes.rotation.add_remove_keyframe()
            time.sleep(1)
            keyframe_room_page.clip_attributes.rotation.set_value(90)
            keyframe_room_page.drag_scroll_bar(0)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Keyframe_Copy.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Keyframe_Copy.png',
                                                     current_image)
            case.result_1 = keyframe_room_page.clip_attributes.right_click_menu('Copy')
            case.result = compare_result and case.result_1


        # Select 2nd nested project and paste keyframe from right-click menu
        with uuid("ddfa9d53-80b1-486f-a427-8c7cee0803f0") as case:
            time.sleep(1)
            timeline_page.select_timeline_media(0, 1)
            time.sleep(1)
            keyframe_room_page.clip_attributes.right_click_menu('Paste')
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Keyframe_Paste.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Keyframe_Paste.png',
                                                     current_image)
            case.result = compare_result
            case.fail_log = "VDE223923-0053"

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_16(self):
        # insert project and edit project's video by trim
        with uuid("3de68cac-fc2d-4fc5-a552-a81ae4f32660") as case:
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            nest_project_page.click_sub_project_tab()
            timeline_page.select_timeline_media(0, 0)
            tips_area_page.click_TipsArea_btn_Trim('video')
            precut_page.set_precut_single_trim_duration('00_05_00')
            case.result = precut_page.click_ok()

        # Edit project's video by pip designer
        with uuid("92867cf0-e6cd-4bf1-8306-9d018028e3f7") as case:
            time.sleep(1)
            tips_area_page.tools.select_PiP_Designer()
            time.sleep(1)
            pip_designer_page.express_mode.unfold_properties_object_setting_tab()
            pip_designer_page.express_mode.drag_object_setting_opacity_slider(20)
            pip_designer_page.click_ok()
            time.sleep(3)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'ModifyByPiPDesigner.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'ModifyByPiPDesigner.png',
                                                     current_image, similarity=0.8)
            case.result = compare_result

        # Edit project's video by mask designer
        with uuid("53100e37-09f6-4808-86da-7136ceca6e43") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            time.sleep(1)
            tips_area_page.tools.select_Mask_Designer()
            time.sleep(1)
            mask_designer_page.MaskDesigner_Apply_template(2)
            mask_designer_page.Edit_MaskDesigner_ClickOK()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                             file_name=Auto_Ground_Truth_Folder + 'ModifyByMaskDesigner.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'ModifyByMaskDesigner.png',
                                             current_image)
            case.result = compare_result

        # Edit project's video by crop/zoom/pan
        with uuid("82956240-d226-49e5-abaa-93411815b71b") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            time.sleep(1)
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(1)
            crop_zoom_pan_page.set_AspectRatio_4_3()
            crop_zoom_pan_page.click_ok()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'ModifyByCropZoomPan.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'ModifyByCropZoomPan.png',
                                                     current_image)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_17(self):
        # insert project and edit project's image crop
        with uuid("8080047b-a326-438e-8fa8-0d32ddbfbea5") as case:
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            nest_project_page.click_sub_project_tab()
            timeline_page.select_timeline_media(0, 1)
            time.sleep(1)
            tips_area_page.click_TipsArea_btn_Crop_Image()
            crop_image_page.aspect_ratio.set_1_1()
            crop_image_page.click_ok()
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Project_CropImage.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Project_CropImage.png',
                                                     current_image, similarity=0.8)
            case.result = compare_result

        # undo and edit project's image duration
        with uuid("a0b31080-1f4a-4a22-89a7-19fef05bb3f5") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            time.sleep(1)
            tips_area_page.click_TipsArea_btn_Duration()
            case.result = tips_area_page.apply_duration_settings('00_00_03_00')

        # undo and edit project's image with pan & zoom function
        with uuid("536a6dbb-23b3-4cd6-891d-6ef9122bfe74") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            time.sleep(1)
            tips_area_page.tools.select_Pan_Zoom()
            check_value = pan_zoom_page.apply_motion_style(13)
            logger(check_value)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                             file_name=Auto_Ground_Truth_Folder + 'Project_PanZoom.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Project_PanZoom.png',
                                             current_image, similarity=0.8)
            case.result = compare_result

        # undo, insert color board and edit project's image with blending mode at track 2
        with uuid("98a2228e-e89e-41bd-b467-9a2baff5f9f3") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            time.sleep(1)
            pan_zoom_page.click_close()
            main_page.tap_MediaRoom_hotkey()
            media_room_page.enter_color_boards()
            main_page.click_library_details_view()
            media_room_page.sound_clips_select_media('17, 208, 68')
            main_page.click_library_icon_view()
            tips_area_page.tips_area_insert_media_to_selected_track(1)
            media_room_page.enter_media_content()
            main_page.timeline_select_track(2)
            media_room_page.select_media_content('Landscape 01.jpg')
            tips_area_page.tips_area_insert_media_to_selected_track(-1)
            tips_area_page.tools.select_Blending_Mode()
            blending_mode_page.set_blending_mode('Multiply')
            blending_mode_page.click_ok()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Project_BlendingMode.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Project_BlendingMode.png',
                                                     current_image)
            case.result = compare_result

        # undo, adjust video's speed in nested project
        with uuid("ddfb5860-c831-4a6d-a9cd-6fad0a675bdb") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            main_page.tap_Undo_hotkey()
            main_page.tap_Undo_hotkey()
            main_page.tap_Undo_hotkey()
            timeline_page.select_timeline_media(0, 2)
            tips_area_page.more_features.remove()
            timeline_page.select_timeline_media(0, 1)
            tips_area_page.more_features.remove()
            timeline_page.drag_to_change_speed(0, 0, 'Last', 'Right', 1)
            time.sleep(1)
            nest_project_page.click_nest_project_main_tab()
            main_page.set_timeline_timecode('00_00_15_00')
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                             file_name=Auto_Ground_Truth_Folder + 'Project_VideoSpeed.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Project_VideoSpeed.png',
                                             current_image, similarity=0.9)
            case.result = compare_result

        # undo, adjust video with inverse in nested project
        with uuid("057403c6-cb0f-4290-aae9-9ac54f2e5846") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            main_page.tap_Undo_hotkey()
            main_page.tap_Undo_hotkey()
            main_page.tap_Undo_hotkey()
            timeline_page.select_timeline_media(0, 0)
            tips_area_page.tools.select_Video_in_Reverse()
            nest_project_page.click_nest_project_main_tab()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Project_VideoReverse.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Project_VideoReverse.png',
                                                     current_image)
            case.result = compare_result

        # undo, apply white balance on selected video in nested project
        with uuid("821f4a5f-c737-434e-8ac9-4a1a081138b1") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            main_page.tap_Undo_hotkey()
            tips_area_page.click_fix_enhance()
            fix_enhance_page.fix.enable_white_balance(True)
            fix_enhance_page.fix.white_balance.color_temperature.set_value(75)
            nest_project_page.click_nest_project_main_tab()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Project_WB.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Project_WB.png',
                                                     current_image)
            case.result = compare_result

        # undo, apply video stabilizer on selected video in nested project
        with uuid("1c7cf9d1-8428-4028-b056-06e890ecf80a") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            main_page.tap_Undo_hotkey()
            fix_enhance_page.fix.enable_white_balance(False)
            fix_enhance_page.fix.enable_video_stabilizer(True)
            fix_enhance_page.fix.video_stabilizer.correction_level.set_value(90)
            nest_project_page.click_nest_project_main_tab()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Project_Stabilizer.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Project_Stabilizer.png',
                                                     current_image)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_18(self):
        # insert pdk project and snapshot project tab
        with uuid("4a2797e6-dea4-4933-828d-932a742cf714") as case:
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pdk'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(3)
            main_page.press_enter_key()
            time.sleep(3)
            main_page.press_esc_key()
            time.sleep(3)
            current_image = timeline_page.snapshot(locator=L.nest_project.nest_project_track,
                                           file_name=Auto_Ground_Truth_Folder + 'PDKProject.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'PDKProject.png', current_image)
            case.result = compare_result

        # New workpsace, insert pds project
        with uuid("859916a2-95f3-4c42-bd5e-99561afc88fa") as case:
            time.sleep(1)
            main_page.tap_NewWorkspace_hotkey()
            time.sleep(2)
            main_page.press_esc_key()
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            current_image = timeline_page.snapshot(locator=L.nest_project.nest_project_track,
                                           file_name=Auto_Ground_Truth_Folder + 'PDSProject.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'PDSProject.png', current_image)
            case.result = compare_result

        # To fix enhance > Lens correction > snapshot in main tab
        with uuid("db7542ac-bcc5-4be9-9623-4b12b563fb77") as case:
            time.sleep(1)
            nest_project_page.click_sub_project_tab()
            timeline_page.select_timeline_media(0, 0)
            tips_area_page.click_fix_enhance()
            fix_enhance_page.fix.enable_lens_correction(True)
            fix_enhance_page.fix.lens_correction.fisheye_distortion.set_value(-100)
            nest_project_page.click_nest_project_main_tab()
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Project_Lens.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Project_Lens.png',
                                                     current_image)
            case.result = compare_result

        # Undo > snapshot in main tab
        with uuid("a2906611-75f6-44f5-89c5-70930371035c") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            main_page.tap_Undo_hotkey()
            main_page.tap_Undo_hotkey()
            nest_project_page.click_nest_project_main_tab()
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                             file_name=Auto_Ground_Truth_Folder + 'Undo_Lens.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Undo_Lens.png',
                                             current_image)
            case.result = compare_result

        # To sub project tab > apply color adjustment > enable split preview
        with uuid("ff366c78-4c62-4404-84af-157d1567a507") as case:
            time.sleep(1)
            nest_project_page.click_sub_project_tab()
            timeline_page.select_timeline_media(0, 0)
            tips_area_page.click_fix_enhance()
            fix_enhance_page.enhance.enable_color_adjustment(True)
            fix_enhance_page.enhance.color_adjustment.hue.set_value(35)
            fix_enhance_page.set_check_compare_in_split_preview(True)
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'SplitPreview_Color.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'SplitPreview_Color.png',
                                                     current_image)
            case.result = compare_result

        # To main project tab > snapshot
        with uuid("e2eb5cdc-1333-4751-8f9a-30336e79faa2") as case:
            time.sleep(1)
            nest_project_page.click_nest_project_main_tab()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'MainProject_Color.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'MainProject_Color.png',
                                                     current_image)
            case.result = compare_result

        # To sub project tab > set playhead to the end and insert video collage clip
        with uuid("3722a538-ba76-4a6e-98f7-a9527214fbc4") as case:
            time.sleep(1)
            nest_project_page.click_sub_project_tab()
            timeline_page.select_timeline_media(0, 2)
            main_page.set_timeline_timecode('00_00_05_00')
            main_page.top_menu_bar_plugins_video_collage_designer()
            time.sleep(2)
            video_collage_designer_page.media.click_auto_fill()
            time.sleep(1)
            video_collage_designer_page.click_ok()
            time.sleep(2)
            main_page.set_timeline_timecode('00_00_03_00')
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'SubProject_CollageClip.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'SubProject_CollageClip.png',
                                                     current_image)
            case.result = compare_result

    @exception_screenshot
    def test_1_1_21(self):
        with uuid("""ddfa9d53-80b1-486f-a427-8c7cee0803f0""") as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"

'''
        
'''
