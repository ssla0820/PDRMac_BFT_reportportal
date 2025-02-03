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


# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Nested Project.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Nested_Project/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Nested_Project/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Nested_Project():
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
            google_sheet_execution_log_init('Nested_Project')

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

    @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        # default is nested project in preferences
        with uuid("89d3fd4b-ddd2-4b11-97c6-18683c502e7b") as case:
            # Insert project to timeline
            with uuid("a0c1ecbe-4e72-4891-b474-232fe3d9b336") as case:
                time.sleep(2)
                main_page.top_menu_bar_file_open_project()
                project_path = Test_Material_Folder + 'nested_project/NestedProject_pds.pds'
                main_page.handle_open_project_dialog(project_path)
                main_page.handle_merge_media_to_current_library_dialog(option='no')
                time.sleep(1)
                main_page.tap_NewWorkspace_hotkey()
                main_page.press_esc_key()
                time.sleep(1)
                project_room_page.enter_project_room()
                main_page.select_library_icon_view_media('NestedProject_pds')
                tips_area_page.click_TipsArea_btn_insert_project()
                time.sleep(2)
                current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                                     file_name=Auto_Ground_Truth_Folder + 'Project_Workspace.png')
                compare_result = timeline_page.compare(Ground_Truth_Folder + 'Project_Workspace.png', current_image)
                case.result = compare_result
            case.result = compare_result

        # check the nested project tab
        with uuid("04578c26-3ac8-478a-9d69-1ab5da48ee26") as case:
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.nest_project.nest_project_track,
                                                   file_name=Auto_Ground_Truth_Folder + 'Project_tab.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Project_tab.png', current_image)
            case.result = compare_result

        # check the nested project tab
        with uuid("6eb4b2b8-7ea9-4306-a35d-ec274fa85912") as case:
            time.sleep(1)
            media_room_page.tap_MediaRoom_hotkey()
            media_room_page.library_menu_empty_the_library()
            time.sleep(2)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.nest_project.nest_project_track,
                                                   file_name=Auto_Ground_Truth_Folder + 'Project_tab_Insert.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Project_tab_Insert.png', current_image)
            case.result = compare_result

        # auto import project content in library
        with uuid("ffc19bd8-f5dd-46dc-9e19-bda7c760bbf3") as case:
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.base.Area.library_icon_view,
                                                   file_name=Auto_Ground_Truth_Folder + 'AutoImport_InsertProject.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'AutoImport_InsertProject.png', current_image)
            case.result = compare_result

        # Change to expanded project in preferences
        with uuid("ddd3c265-57d1-4d4a-be65-d7c3815ef7c3") as case:
            time.sleep(1)
            main_page.click_set_user_preferences()
            preferences_page.switch_to_editing()
            preferences_page.editing.set_default_insert_project_behavior_status('expanded')
            preferences_page.click_ok()
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            time.sleep(1)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/NestedProject_pds.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                                   file_name=Auto_Ground_Truth_Folder + 'Workspace_InsertExpandProject.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_InsertExpandProject.png', current_image)
            case.result = compare_result

        # Re-launch PDR, it still keep expanded setting
        with uuid("2b082a86-9dc2-4970-aa7d-545e936ea1a1") as case:
            time.sleep(1)
            main_page.close_and_restart_app()
            time.sleep(2)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/NestedProject_pds.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                                   file_name=Auto_Ground_Truth_Folder + 'Workspace_ExpandProject2.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_ExpandProject2.png',
                                                   current_image)
            case.result = compare_result

    @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        # Drag project to timeline, nested project display correctly in workspace
        with uuid("04c12c53-53e8-4e2a-b629-be00a0f31c57") as case:
            time.sleep(2)
            main_page.top_menu_bar_file_open_project()
            project_path = Test_Material_Folder + 'nested_project/NestedProject_pds.pds'
            main_page.handle_open_project_dialog(project_path)
            main_page.handle_merge_media_to_current_library_dialog(option='no')
            time.sleep(1)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            time.sleep(1)
            main_page.timeline_select_track(2)
            main_page.insert_media('Landscape 02.jpg')
            project_room_page.enter_project_room()
            main_page.drag_media_to_timeline_playhead_position('NestedProject_pds', 1)
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                                   file_name=Auto_Ground_Truth_Folder + 'Workspace_DragProject.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_DragProject.png', current_image)
            case.result = compare_result

        # project tab display correctly
        with uuid("6b7310ff-3586-4ed4-876a-59e9a4ec6a6f") as case:
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.nest_project.nest_project_track,
                                                   file_name=Auto_Ground_Truth_Folder + 'Project_tab_Drag.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Project_tab_Drag.png', current_image)
            case.result = compare_result

        # preview is correct if clip put above nested project
        with uuid("d18aa6e4-ce81-4ae9-9135-f2ffbb4fdc68") as case:
            time.sleep(1)
            timeline_page.select_timeline_media('2', '0')
            playback_window_page.adjust_timeline_preview_on_canvas_resize_to_small()
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Preview_UnderProject.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Preview_UnderProject.png', current_image)
            case.result = compare_result

        # preview is correct if clip put below nested project
        with uuid("aa75ab8d-6776-4246-9b8b-6264b32855cf") as case:
            time.sleep(1)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            time.sleep(1)
            media_room_page.tap_MediaRoom_hotkey()
            main_page.insert_media('Landscape 02.jpg')
            project_room_page.enter_project_room()
            main_page.drag_media_to_timeline_playhead_position('NestedProject_pds', 2)
            playback_window_page.adjust_timeline_preview_on_canvas_resize_to_small()
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Preview_BelowProject.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Preview_BelowProject.png', current_image)
            case.result = compare_result

        # preview is correct if title put above nested project
        with uuid("287c9c8e-57ec-4b29-91be-8113b50a4cbf") as case:
            time.sleep(1)
            main_page.exist_click(L.main.top_menu_bar.btn_file)
            main_page.top_menu_bar_select_click_menu(L.main.top_menu_bar.option_open_project)
            time.sleep(1)
            main_page.handle_no_save_project_dialog()
            project_path = Test_Material_Folder + 'nested_project/NestedProject_title.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            time.sleep(1)
            main_page.insert_media('Landscape 02.jpg')
            project_room_page.enter_project_room()
            main_page.drag_media_to_timeline_playhead_position('NestedProject_title', 2)
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Preview_TitleProject.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Preview_TitleProject.png', current_image)
            case.result = compare_result

    @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        # Open project and insert nested project to timeline, snapshot the main tab
        with uuid("3d3d97fe-6cc9-461e-9a7c-150ee5542280") as case:
            # also snapshot the inserted project tab
            with uuid("c2e06c08-420c-41ed-b423-27d04eee59b2") as case:
                # insert project is long file name
                with uuid("9d103b60-6f62-4dd2-8aaa-7acd418100a7") as case:
                    time.sleep(1)
                    main_page.top_menu_bar_file_open_project()
                    project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
                    main_page.handle_open_project_dialog(project_path)
                    main_page.handle_merge_media_to_current_library_dialog(option='no')
                    time.sleep(1)
                    main_page.set_timeline_timecode('00_00_00_00')
                    project_room_page.enter_project_room()
                    main_page.timeline_select_track(2)
                    main_page.select_library_icon_view_media('Nested_0123456789012')
                    tips_area_page.click_TipsArea_btn_insert_project()
                    time.sleep(2)
                    current_image = timeline_page.snapshot(locator=L.nest_project.nest_project_track,
                                                   file_name=Auto_Ground_Truth_Folder + 'Project_name.png')
                    compare_result = timeline_page.compare(Ground_Truth_Folder + 'Project_name.png', current_image)
                    case.result = compare_result
                case.result = compare_result
            case.result = compare_result

        # save as project and main tab will update project name
        with uuid("b4133c0d-bead-4f50-b996-35cd34ad96c5") as case:
            # save as long file name
            with uuid("09512d2f-a0b0-405d-8a19-9074809957e7") as case:
                time.sleep(1)
                project_new_page.tap_SaveProjectAs_hotkey()
                project_new_page.save_file.handle_save_file('012345678901234567', Test_Material_Folder + 'nested_project/')
                time.sleep(2)
                current_image = timeline_page.snapshot(locator=L.nest_project.nest_project_track,
                                                   file_name=Auto_Ground_Truth_Folder + 'Project_new_name.png')
                compare_result = timeline_page.compare(Ground_Truth_Folder + 'Project_new_name.png', current_image)
                case.result = compare_result
            case.result = compare_result

        # show tooltip if main project has long project name
        with uuid("d0d4e50e-6ca0-4aa6-bea5-28fa03fdd6bc") as case:
            time.sleep(1)
            nest_project_page.hover_main_tab()
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.nest_project.nest_project_track,
                                                   file_name=Auto_Ground_Truth_Folder + 'ProjectName_main.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'ProjectName_main.png', current_image)
            case.result = compare_result

        # show tooltip if inserted project has long project name
        with uuid("cd489452-5e3d-4b16-a014-41b014874e03") as case:
            time.sleep(1)
            nest_project_page.hover_sub_project_tab(1)
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.nest_project.nest_project_track,
                                                   file_name=Auto_Ground_Truth_Folder + 'ProjectName_Sub.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'ProjectName_Sub.png', current_image)
            case.result = compare_result

        # close inserted project
        with uuid("381c2f2e-d97e-4b58-893c-f31fcae3d602") as case:
            time.sleep(1)
            nest_project_page.close_sub_project_tab(1)
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                                   file_name=Auto_Ground_Truth_Folder + 'Workspace_CloseSub.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_CloseSub.png', current_image)
            case.result = compare_result

        # undo and insert project many times then scroll right
        with uuid("2218aa81-6cf6-4e85-b354-d4949b39c71d") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            time.sleep(1)
            main_page.select_library_icon_view_media('Nested_0123456789012')
            tips_area_page.click_TipsArea_btn_insert_project()
            main_page.select_library_icon_view_media('Nested_0123456789012')
            tips_area_page.click_TipsArea_btn_insert_project()
            main_page.select_library_icon_view_media('Nested_0123456789012')
            tips_area_page.click_TipsArea_btn_insert_project()
            main_page.select_library_icon_view_media('Nested_0123456789012')
            tips_area_page.click_TipsArea_btn_insert_project()
            main_page.select_library_icon_view_media('Nested_0123456789012')
            tips_area_page.click_TipsArea_btn_insert_project()
            main_page.select_library_icon_view_media('Nested_0123456789012')
            tips_area_page.click_TipsArea_btn_insert_project()
            main_page.select_library_icon_view_media('Nested_0123456789012')
            tips_area_page.click_TipsArea_btn_insert_project()
            main_page.select_library_icon_view_media('Nested_0123456789012')
            tips_area_page.click_TipsArea_btn_insert_project()
            main_page.select_library_icon_view_media('Nested_0123456789012')
            tips_area_page.click_TipsArea_btn_insert_project()
            main_page.select_library_icon_view_media('Nested_0123456789012')
            tips_area_page.click_TipsArea_btn_insert_project()
            main_page.select_library_icon_view_media('Nested_0123456789012')
            tips_area_page.click_TipsArea_btn_insert_project()
            main_page.select_library_icon_view_media('Nested_0123456789012')
            tips_area_page.click_TipsArea_btn_insert_project()
            main_page.select_library_icon_view_media('Nested_0123456789012')
            tips_area_page.click_TipsArea_btn_insert_project()
            time.sleep(1)
            nest_project_page.click_btn_next_scroll()
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.nest_project.nest_project_track,
                                                   file_name=Auto_Ground_Truth_Folder + 'Project_ScrollR.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Project_ScrollR.png', current_image)
            case.result = compare_result

        # undo and insert project many times then scroll left
        with uuid("218a38c6-7a05-492e-a467-a5297cc8e4e8") as case:
            time.sleep(1)
            nest_project_page.click_btn_prev_scroll()
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.nest_project.nest_project_track,
                                                   file_name=Auto_Ground_Truth_Folder + 'Project_ScrollL.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Project_ScrollL.png', current_image)
            case.result = compare_result

    @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        # try the ripple editing menu function - 2nd option - insert
        with uuid("d3264551-b131-46cd-a1c1-b394c4f23606") as case:
            time.sleep(1)
            main_page.top_menu_bar_file_open_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            main_page.handle_merge_media_to_current_library_dialog(option='no')
            time.sleep(1)
            main_page.tap_NewWorkspace_hotkey()
            main_page.press_esc_key()
            time.sleep(1)
            project_room_page.enter_project_room()
            main_page.select_library_icon_view_media('Nested_0123456789012')
            tips_area_page.click_TipsArea_btn_insert_project()
            time.sleep(1)
            timeline_page.tap_Copy_hotkey()
            timeline_page.tap_Paste_hotkey()
            timeline_page.keyboard.down()
            timeline_page.keyboard.down()
            timeline_page.keyboard.enter()
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.nest_project.nest_project_track,
                                                   file_name=Auto_Ground_Truth_Folder + 'Project_RippleEditing.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Project_RippleEditing.png', current_image)
            case.result = compare_result

        # copy first and then paste and cut the nested project
        with uuid("f264cae0-032d-46d8-bb06-d1b0cc6d9f2c") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            time.sleep(1)
            main_page.set_timeline_timecode('00_00_20_00')
            time.sleep(1)
            main_page.tap_Paste_hotkey()
            time.sleep(1)
            main_page.tap_Cut_hotkey()
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.nest_project.nest_project_track,
                                                   file_name=Auto_Ground_Truth_Folder + 'Project_CopyPasteCut.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Project_CopyPasteCut.png', current_image)
            case.result = compare_result

        # trim the nested project
        with uuid("2016fb2f-614d-4808-aaf7-83b0677f04f0") as case:
            time.sleep(1)
            timeline_page.timeline_click_zoomin_btn()
            timeline_page.timeline_click_zoomin_btn()
            timeline_page.select_timeline_media('0', '0')
            timeline_page.drag_timeline_clip('Last', 0.5, 0, 0)
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=L.library_preview.display_panel,
                                                         file_name=Auto_Ground_Truth_Folder + 'NestedProject_Trim.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'NestedProject_Trim.png', current_image)
            case.result = compare_result

        # split the nested project
        with uuid("55e55226-8da5-4014-9fc8-c2543c8c511d") as case:
            time.sleep(1)
            main_page.tap_Undo_hotkey()
            main_page.set_timeline_timecode('00_00_05_00')
            tips_area_page.click_TipsArea_btn_split()
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                                       file_name=Auto_Ground_Truth_Folder + 'Workspace_SplitProject_5s.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_SplitProject_5s.png',
                                                       current_image)
            case.result = compare_result

    # check menu status in More features button
    def test_1_1_5(self):
        # workspace is empty after cut the nested project
        with uuid("c793fd66-dd56-49c6-aaf0-31a40fb7a0ee") as case:
            time.sleep(3)
            main_page.top_menu_bar_file_insert_project()
            project_path = Test_Material_Folder + 'nested_project/Nested_0123456789012.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(1)
            timeline_page.timeline_click_zoomin_btn()
            time.sleep(1)
            tips_area_page.more_features.cut()
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                           file_name=Auto_Ground_Truth_Folder + 'Workspace_Empty_Cut.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_Empty_Cut.png',
                                           current_image)
            case.result = compare_result

        # workspace has two clip after copy and then paste nested project
        with uuid("1f800180-74a4-406b-ae6a-44139c84b35a") as case:
            with uuid("897b8262-c8c1-43ba-ab25-b3ec7b93ac3d") as case:
                time.sleep(1)
                main_page.tap_Undo_hotkey()
                time.sleep(1)
                tips_area_page.more_features.copy()
                main_page.set_timeline_timecode('00_00_20_00')
                time.sleep(2)
                tips_area_page.more_features.paste()
                time.sleep(2)
                main_page.move_mouse_to_0_0()
                current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                           file_name=Auto_Ground_Truth_Folder + 'Workspace_CopyPasteProject.png')
                compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_CopyPasteProject.png',
                                           current_image)
                case.result = compare_result
            case.result = compare_result

        # Select copy keyframe attributes from more features menu
        with uuid("51a67fc6-9245-4c1a-b4de-1cd1ea650ef7") as case:
            time.sleep(1)
            check_result = tips_area_page.more_features.copy_keyframe_attributes()
            case.result = check_result

        # Select paste keyframe attributes from more features menu
        with uuid("112b1aad-45c8-41ed-bd49-0f3a1ddc5471") as case:
            time.sleep(1)
            timeline_page.select_timeline_media('0', '0')
            check_result = tips_area_page.more_features.paste_keyframe_attributes()
            case.result = check_result

        # workspace has only 1 project after remove one from more features menu
        with uuid("37657134-e50f-4db0-b56f-2f94857c53d7") as case:
            time.sleep(1)
            timeline_page.select_timeline_media('0', '1')
            tips_area_page.more_features.remove()
            time.sleep(2)
            current_image = timeline_page.snapshot(locator=L.timeline_operation.workspace,
                                           file_name=Auto_Ground_Truth_Folder + 'Workspace_AfterRemoveOne.png')
            compare_result = timeline_page.compare(Ground_Truth_Folder + 'Workspace_AfterRemoveOne.png',
                                           current_image)
            case.result = compare_result


    @exception_screenshot
    def test_1_1_21(self):
        with uuid("""38d804c1-94b7-4aad-8dad-cdc9c3b69274
        ded1b2bc-0e4c-4ac2-ba7a-00c00317784d""") as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"

'''
        
'''
