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
download_from_cl_dz_page = PageFactory().get_page_object('download_from_cl_dz_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
transition_room_page = PageFactory().get_page_object('transition_room_page', mwc)
title_designer_page = PageFactory().get_page_object('title_designer_page', mwc)
crop_zoom_pan_page = PageFactory().get_page_object('crop_zoom_pan_page', mwc)
pan_zoom_page = PageFactory().get_page_object('pan_zoom_page', mwc)
timeline_page = PageFactory().get_page_object('timeline_operation_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
particle_designer_page = PageFactory().get_page_object('particle_designer_page', mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)
mask_designer_page = PageFactory().get_page_object('mask_designer_page', mwc)
gettyimage_page = PageFactory().get_page_object('gettyimage_page', mwc)
library_preview_page = PageFactory().get_page_object('library_preview_page', mwc)
shape_designer_page = PageFactory().get_page_object('shape_designer_page', mwc)
precut_page = PageFactory().get_page_object('precut_page', mwc)
project_room_page = PageFactory().get_page_object('project_room_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Shape Designer_v2.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Shape_Designer_v2/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Shape_Designer_v2/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Shape_Designer_v2():
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
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('Shape_Designer_v2')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"shape designer_v2 result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
    def test_1_7_3(self):
        #Timeline operation
        #Render Preview > Default shape > General shape
        with uuid("39e22e96-ae4a-4c41-85d0-3f3d5df731b2") as case:
            main_page.enter_room(4)
            pip_room_page.click_CreateNewShape_btn()
            time.sleep(DELAY_TIME * 3)
            shape_designer_page.click_ok()
            shape_designer_page.save_as.set_name('Default General')
            shape_designer_page.save_as.click_ok()
            timeline_operation_page.tips_area_insert_media_to_selected_track()
            # Ripple editing > Replace
            with uuid("0f1887e8-2f50-48cb-abba-d297fbd48f10") as case:
                main_page.select_library_icon_view_media('Default General')
                case.result = main_page.tips_area_insert_media_to_selected_track(4)
            case.result = timeline_operation_page.edit_timeline_render_preview()

        # Render Preview > Default shape > Linear shape
        with uuid("ab53bdc6-9042-4e56-871c-ed2f0cf9fc3c") as case:
            pip_room_page.click_CreateNewShape_btn()
            time.sleep(DELAY_TIME * 3)
            shape_designer_page.properties.unfold_shape_type()
            shape_designer_page.properties.shape_type.apply_type(3)
            shape_designer_page.click_ok()
            shape_designer_page.save_as.set_name('Default Linear')
            shape_designer_page.save_as.click_ok()
            # Ripple editing > Overwrite
            with uuid("7f122640-150e-4a0a-b518-c45c3611eadb") as case:
                case.result = main_page.tips_area_insert_media_to_selected_track(0)
            case.result = timeline_operation_page.edit_timeline_render_preview()

        #Render Preview > Custom shape > General shape
        with uuid("7728ff45-ef66-4a63-9e4b-3b106f94e6ef") as case:
            pip_room_page.click_CreateNewShape_btn()
            time.sleep(DELAY_TIME * 3)
            shape_designer_page.adjust_object_on_Canvas_move_to_left()
            shape_designer_page.click_ok()
            shape_designer_page.save_as.set_name('Custom General')
            shape_designer_page.save_as.click_ok()
            # Ripple editing > Insert
            with uuid("8dc13920-2600-446c-b61c-1413a351ef69") as case:
                case.result = main_page.tips_area_insert_media_to_selected_track(1)
            case.result = timeline_operation_page.edit_timeline_render_preview()

        # Render Preview > Custom shape > Linear shape
        with uuid("4f19b454-8379-4e2c-b1df-48402fdbd20c") as case:
            pip_room_page.click_CreateNewShape_btn()
            time.sleep(DELAY_TIME * 3)
            shape_designer_page.properties.unfold_shape_type()
            shape_designer_page.properties.shape_type.apply_type(3)
            shape_designer_page.adjust_object_on_Canvas_move_to_left()
            shape_designer_page.click_ok()
            shape_designer_page.save_as.set_name('Custom Linear')
            shape_designer_page.save_as.click_ok()
            # Ripple editing > Insert and move all clips
            with uuid("c1228b57-f107-4bac-bd5d-fb9fa33dbfdd") as case:
                case.result = main_page.tips_area_insert_media_to_selected_track(2)
            case.result = timeline_operation_page.edit_timeline_render_preview()

        # Duration
        with uuid("023b2620-9ccc-42b6-b971-266c51da169a") as case:

            case.result = main_page.set_timeline_timecode("00_00_05_00")

        # Split
        with uuid("56e6f895-df96-4692-8c83-adfc6754ecfe") as case:
            tips_area_page.click_TipsArea_btn_split()
            case.result = main_page.select_timeline_media('Custom Linear', 1)

        # Context menu > Copy
        with uuid("b32d288c-509c-44cc-a305-828de7793eb2") as case:
            main_page.select_timeline_media('Default Linear')
            main_page.right_click()
            case.result = main_page.select_right_click_menu('Copy')

        # Context menu > Cut
        with uuid("280a8644-3ef3-41cf-b90e-a0c4c76d8da5") as case:
            main_page.select_timeline_media('Default Linear')
            main_page.right_click()
            case.result = main_page.select_right_click_menu('Cut')

        # Context menu > Paste
        with uuid("46de0e73-73fa-4578-ad65-2865b3d12e34") as case:
            main_page.select_timeline_media('Custom General')
            main_page.right_click()
            case.result = main_page.select_right_click_menu('Paste', 'Paste and Insert')

        # Context menu > Remove
        with uuid("b311b401-e231-42a2-9622-4a27a7640e62") as case:
            main_page.select_timeline_media('Default Linear')
            main_page.right_click()
            case.result = main_page.select_right_click_menu('Remove')

        # Context menu > Select All
        with uuid("cfb2f446-bb87-423c-b32e-141292809770") as case:
            main_page.select_timeline_media('Custom General')
            main_page.right_click()
            case.result = main_page.select_right_click_menu('Select All')

        # Context menu > Group/Ungroup
        with uuid("4439b41a-f4f9-48c8-91db-c80f9f6e401c") as case:
            main_page.select_timeline_media('Custom General')
            main_page.right_click()
            case.result = main_page.select_right_click_menu('Group/Ungroup Objects')
            main_page.press_backspace_key()

        # Context menu > Set Duration...
        with uuid("e6405001-63ad-4973-b803-7f93c84543ee") as case:
            main_page.select_library_icon_view_media('Custom General')
            timeline_operation_page.tips_area_insert_media_to_selected_track()
            main_page.select_timeline_media('Custom General')
            main_page.right_click()
            main_page.select_right_click_menu('Set Duration...')
            case.result = main_page.exist(L.tips_area.window.duration_settings)
            main_page.press_esc_key()

        # Context menu > Split
        with uuid("faefa7c8-55b0-40fa-8ea0-8537e3f21484") as case:
            main_page.set_timeline_timecode("00_00_05_00")
            main_page.select_timeline_media('Custom General')
            main_page.right_click()
            main_page.select_right_click_menu('Split')
            case.result = main_page.select_timeline_media('Custom General', 1)

        # Context menu > Edit Clip Alias > Change Alias...
        with uuid("6bbe40f2-21b4-4529-b4a7-1103a51168ec") as case:
            main_page.right_click()
            case.result = main_page.select_right_click_menu('Edit Clip Alias', 'Change Alias...')
            main_page.press_esc_key()
            main_page.press_esc_key()

        # Context menu > Edit Clip Alias > Reset Alias...
        with uuid("3e2382cd-ad46-48a9-8b5c-1b8120cb83d8") as case:
            main_page.select_timeline_media('Custom General', 1)
            main_page.right_click()
            case.result = main_page.select_right_click_menu('Edit Clip Alias', 'Reset Alias')

        # Context menu > Edit Clip Alias > Dock/Undock Timeline Window
        with uuid("7399756f-ca3c-4481-8350-c346b0932235") as case:
            main_page.select_timeline_media('Custom General', 1)
            main_page.right_click()
            case.result = main_page.select_right_click_menu('Dock/Undock Timeline Window')


        # Context menu > Edit Clip Alias > Reset Alias...
        with uuid("7f3f7343-88e4-4f09-9ef4-ff1d0de795cd") as case:
            main_page.select_timeline_media('Custom General', 1)
            main_page.right_click()
            case.result = main_page.select_right_click_menu('Reset All Undocked Windows')

            # Context menu > Link/Unlink
        with uuid("109acbf0-9fd4-4f7f-a6cf-f8e1236d3b70") as case:
            main_page.enter_room(0)
            main_page.select_library_icon_view_media('Mahoroba.mp3')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.tap_command_and_hold()
            main_page.select_timeline_media('Custom General', 1)
            main_page.release_command_key()
            main_page.right_click()
            case.result = main_page.select_right_click_menu('Link/Unlink Video and Audio')

        # Save Project then open
        with uuid('''
        ada770ca-fe2a-4672-9128-d5d44378a06b
        f10b146d-0912-47f0-8a60-aef999791f51
        8326f794-27f4-4044-8596-29a3ce3cb8ce
        dc9614c5-da63-4c33-ac1f-145e8cf690eb
        ''') as case:
            main_page.enter_room(4)
            main_page.select_library_icon_view_media('Default General')
            main_page.tips_area_insert_media_to_selected_track(1)
            main_page.select_library_icon_view_media('Default Linear')
            main_page.tips_area_insert_media_to_selected_track(1)
            main_page.select_library_icon_view_media('Custom General')
            main_page.tips_area_insert_media_to_selected_track(1)
            main_page.select_library_icon_view_media('Custom Linear')
            main_page.tips_area_insert_media_to_selected_track(1)
            main_page.save_project('shape_designer', app.testing_material + '/shape_designer_v2/')
            main_page.top_menu_bar_file_open_project(save_changes=False)
            main_page.handle_open_project_dialog(app.testing_material + 'shape_designer_v2/shape_designer.pds/')
            main_page.handle_merge_media_to_current_library_dialog()
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_7_3_1.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_7_3_1.png',
                                               playback_window_snap)
            case.result = case1_result

        '''
        # Nested Project
        with uuid('''
        #38ac7f47-45f7-4a06-8573-4140d5d469b3
        #3fddb243-b98e-45a9-9961-048c49fbb209
        #997b737b-cc85-43b5-9d2c-2ff583eed2c4
        #17c9e32f-0517-40c6-920e-46b34e0fdd5f
        ''') as case:
            project_room_page.enter_project_room()
            main_page.select_library_icon_view_media('shape_designer')
            project_room_page.tips_area_insert_project_to_selected_track()
            main_page.select_timeline_media('shape_designer')
            main_page.double_click()
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_7_3_2.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_7_3_2.png',
                                               playback_window_snap)
            case.result = case1_result

        # Pack Project then open
        with uuid('''
        #a5b500fa-0f43-4bdb-8c17-547e220b1c05
        #813524b4-41ab-475a-9f26-deb02cfc2ad4
        #4712a17b-13db-4dd4-9232-967bb47892e2
        #6bf184dc-e35b-471f-8c25-966180a31410
        ''') as case:
            main_page.top_menu_bar_file_pack_project_materials(app.testing_material + '/shape_designer_v2/test1/')
            main_page.top_menu_bar_file_open_project(save_changes=False)
            main_page.handle_open_project_dialog(app.testing_material + 'shape_designer_v2/test1.pdk/')
            main_page.press_esc_key()
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_7_3_3.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_7_3_3.png',
                                               playback_window_snap)
            case.result = case1_result
        '''
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_5_1(self):
        # 5.1 Timecode
        # Movie Timecode
        with uuid("b45cd114-7618-4b62-b892-d5631ac35724") as case:
            main_page.enter_room(4)
            pip_room_page.click_CreateNewShape_btn()
            time.sleep(DELAY_TIME * 3)
            shape_designer_page.click_keyframe_tab()
            case.result = shape_designer_page.switch_timecode_mode(2)

        # Clip Timecode
        with uuid("3267aeaa-12b6-432d-859e-d3893b1d8719") as case:
            case.result = shape_designer_page.switch_timecode_mode(1)

        # Zoom in > Click + / - button
        with uuid("e55b9628-349c-4ced-90f8-7cadea304179") as case:
            case.result = shape_designer_page.simple_timeline.click_zoom_in(1)

        # Zoom in > Drag on timeline to Left / Right
        with uuid("16d4b755-9951-4067-b54b-10d4be2da8dc") as case:
            case.result = shape_designer_page.simple_timeline.drag_zoom_slider(0)

        # Position > Add keyframe (◆)
        with uuid("1ba288b7-17d4-4be2-a50d-a5200dd98e1e") as case:
            shape_designer_page.simple_timeline.position.add_keyframe()
            playback_window_snap = main_page.snapshot(locator=L.shape_designer.simple_track.keyframe_track_outlineview,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_1_1.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_5_1_1.png',
                                               playback_window_snap, similarity=0.85)
            case.result = case1_result

            # Position > Switch focus on correct keyframe via ◄ / ►
        with uuid("44274099-3ea0-4d67-9c90-fcbbbec68e04") as case:
            shape_designer_page.set_timecode('00_00_03_00')
            shape_designer_page.simple_timeline.position.add_keyframe()
            shape_designer_page.simple_timeline.position.click_previous_keyframe()
            playback_window_snap = main_page.snapshot(locator=L.shape_designer.simple_track.keyframe_track_outlineview,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_1_2.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_5_1_2.png',
                                               playback_window_snap, similarity=0.85)
            case.result = case1_result

        # Position > Remove keyframe (◆)
        with uuid("e971e394-40a9-4eae-8bdd-da95373910ef") as case:
            case.result = shape_designer_page.simple_timeline.position.add_keyframe()
            playback_window_snap = main_page.snapshot(locator=L.shape_designer.simple_track.keyframe_track_outlineview,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_1_3.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_5_1_3.png',
                                               playback_window_snap, similarity=0.85)
            case.result = case1_result

        # scale > Add keyframe (◆)
        with uuid("0dc8e28c-85fc-48c7-bc52-373b90a0ee7d") as case:
            shape_designer_page.simple_timeline.scale.add_keyframe()
            playback_window_snap = main_page.snapshot(locator=L.shape_designer.simple_track.keyframe_track_outlineview,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_1_4.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_5_1_4.png',
                                               playback_window_snap, similarity=0.85)
            case.result = case1_result

            # scale > Switch focus on correct keyframe via ◄ / ►
        with uuid("7535b177-4ab2-4916-a782-1d7fc22f4719") as case:
            shape_designer_page.set_timecode('00_00_03_00')
            shape_designer_page.simple_timeline.scale.add_keyframe()
            shape_designer_page.simple_timeline.scale.click_previous_keyframe()
            playback_window_snap = main_page.snapshot(locator=L.shape_designer.simple_track.keyframe_track_outlineview,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_1_5.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_5_1_5.png',
                                               playback_window_snap, similarity=0.85)
            case.result = case1_result

        # scale > Remove keyframe (◆)
        with uuid("e913ba02-13be-4298-afd8-3c991a5b7ad4") as case:
            case.result = shape_designer_page.simple_timeline.scale.add_keyframe()
            playback_window_snap = main_page.snapshot(locator=L.shape_designer.simple_track.keyframe_track_outlineview,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_1_6.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_5_1_6.png',
                                               playback_window_snap, similarity=0.85)
            case.result = case1_result

        # opacity > Add keyframe (◆)
        with uuid("9415272d-4056-43fb-8e84-41384f2c7f94") as case:
            # v21.3.4830 does not show scroll bar
            shape_designer_page.simple_timeline.drag_scroll_bar(0.5)
            shape_designer_page.simple_timeline.opacity.add_keyframe()
            playback_window_snap = main_page.snapshot(locator=L.shape_designer.simple_track.keyframe_track_outlineview,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_1_7.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_5_1_7.png',
                                               playback_window_snap, similarity=0.85)
            case.result = case1_result

            # opacity > Switch focus on correct keyframe via ◄ / ►
        with uuid("74eec57c-10a4-4694-ae97-1a85f66ed3c7") as case:
            shape_designer_page.set_timecode('00_00_03_00')
            shape_designer_page.simple_timeline.opacity.add_keyframe()
            shape_designer_page.simple_timeline.opacity.click_previous_keyframe()
            playback_window_snap = main_page.snapshot(locator=L.shape_designer.simple_track.keyframe_track_outlineview,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_1_8.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_5_1_8.png',
                                               playback_window_snap)
            case.result = case1_result

        # opacity > Remove keyframe (◆)
        with uuid("511153be-a22e-4196-89fd-b5408e5f4939") as case:
            case.result = shape_designer_page.simple_timeline.opacity.add_keyframe()
            playback_window_snap = main_page.snapshot(locator=L.shape_designer.simple_track.keyframe_track_outlineview,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_1_9.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_5_1_9.png',
                                               playback_window_snap)
            case.result = case1_result

        # rotation > Add keyframe (◆)
        with uuid("cfb9b74d-d42e-42e9-b871-4d9d8367ae59") as case:
            shape_designer_page.simple_timeline.drag_scroll_bar(1)
            shape_designer_page.simple_timeline.rotation.add_keyframe()
            playback_window_snap = main_page.snapshot(locator=L.shape_designer.simple_track.keyframe_track_outlineview,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_1_10.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_5_1_10.png',
                                               playback_window_snap)
            case.result = case1_result

            # rotation > Switch focus on correct keyframe via ◄ / ►
        with uuid("09322256-b7b1-417c-a3ae-7bc00db4b41c") as case:
            shape_designer_page.set_timecode('00_00_03_00')
            shape_designer_page.simple_timeline.rotation.add_keyframe()
            shape_designer_page.simple_timeline.rotation.click_previous_keyframe()
            playback_window_snap = main_page.snapshot(locator=L.shape_designer.simple_track.keyframe_track_outlineview,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_1_11.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_5_1_11.png',
                                               playback_window_snap)
            case.result = case1_result

        # rotation > Remove keyframe (◆)
        with uuid("18c8a594-1086-4a10-ae94-1eb191bf9ee7") as case:
            case.result = shape_designer_page.simple_timeline.rotation.add_keyframe()
            playback_window_snap = main_page.snapshot(locator=L.shape_designer.simple_track.keyframe_track_outlineview,
                                                      file_name=Auto_Ground_Truth_Folder + '1_5_1_12.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_5_1_12.png',
                                               playback_window_snap)
            case.result = case1_result







