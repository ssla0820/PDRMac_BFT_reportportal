import sys, os
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
base_page = PageFactory().get_page_object('base_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page', mac)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mac)
playback_window_page = PageFactory().get_page_object('playback_window_page', mac)
precut_page = PageFactory().get_page_object('precut_page', mac)
tips_area_page = PageFactory().get_page_object('tips_area_page', mac)
library_preview_page = PageFactory().get_page_object('library_preview_page', mac)
title_designer_page = PageFactory().get_page_object('title_designer_page', mac)
pan_zoom_page = PageFactory().get_page_object('pan_zoom_page', mac)
blending_mode_page = PageFactory().get_page_object('blending_mode_page', mac)
fix_enhance_page = PageFactory().get_page_object('fix_enhance_page', mac)
effect_room_page = PageFactory().get_page_object('effect_room_page', mac)
crop_zoom_pan_page = PageFactory().get_page_object('crop_zoom_pan_page', mac)
video_speed_page = PageFactory().get_page_object('video_speed_page', mac)
pip_designer_page = PageFactory().get_page_object('pip_designer_page', mac)
video_collage_designer_page = PageFactory().get_page_object('video_collage_designer_page', mac)
transition_room_page = PageFactory().get_page_object('transition_room_page', mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Effect Setting from i button menu.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
#Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/GroundTruth/Pre_Cut/'
#Auto_Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/ATGroundTruth/Pre_Cut/'
#Test_Material_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/'
Ground_Truth_Folder = app.ground_truth_root + '/effect_setting_from_i_button_menu/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/effect_setting_from_i_button_menu/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Effect_Setting_from_i_Button_Menu():
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
            google_sheet_execution_log_init('effect_setting_from_i_button_menu')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"effect_setting_from_i_button_menu result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
    def test_1_1_17(self):
        with uuid("0edc5683-4788-4ea1-bcbb-b6e76551e4d6") as case:
            #Show Audio Denoise in i menu after apply
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(1)
            main_page.enter_room(2)
            main_page.select_library_icon_view_media('Arrow 2')
            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Overlap')
            timeline_operation_page.select_timeline_media(0, 1)
            tips_area_page.more_features.link_unlink_video_audio()
            main_page.timeline_select_track(2)
            timeline_operation_page.select_timeline_media(1, 1)
            tips_area_page.click_fix_enhance()
            fix_enhance_page.fix.enable_audio_denoise()
            main_page.timeline_select_track(1)
            main_page.right_click()
            main_page.select_right_click_menu('Adjust Audio Track Height', 'Large')
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                    {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 1},
                                    {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}],
                                   {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton',
                                    'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_17_3.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_17_3.png',
                                            playback_window_snap)

        with uuid("7993bcec-4e56-400e-9668-2dc77ddc2fc3") as case:
            #Able to open Audio Denoise page from i menu correctly
            main_page.select_right_click_menu('Audio Denoise')
            case.result = fix_enhance_page.is_in_fix_enhance()

        with uuid("e55bab89-a4ed-4071-9555-4f8c2340a4dd") as case:
            # Able to change setting after open audio denoise from I menu button
            fix_enhance_page.fix.audio_denoise.set_noise_type(1)
            case.result = True if fix_enhance_page.fix.audio_denoise.get_noise_type() == 'Wind noise' else False


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_19(self):
        with uuid("33660494-d25c-489e-9279-8c58e5c96116") as case:
            #Copy & Paste then change setting after open corresponding page from I menu button
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            pan_zoom_page.apply_motion_style(4)
            timeline_operation_page.select_timeline_media(0,0)
            main_page.tap_Copy_hotkey()
            main_page.set_timeline_timecode('00_00_05_00')
            main_page.tap_Paste_hotkey()
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_19_1.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_1_19_1.png',
                                               playback_window_snap)
            main_page.select_right_click_menu('Pan & Zoom')
            case.result = pan_zoom_page.apply_motion_style(3) and case1_result

        with uuid("52f5913f-db9f-44de-815e-4f1204f63a8e") as case:
            #Cut & Paste then change setting after open corresponding page from I menu button
            main_page.click_undo()
            main_page.click_undo()
            main_page.tap_Cut_hotkey()
            main_page.tap_Paste_hotkey()
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_19_2.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_1_19_2.png',
                                               playback_window_snap)
            main_page.select_right_click_menu('Pan & Zoom')
            case.result = pan_zoom_page.apply_motion_style(2) and case1_result

        with uuid("e8490ae3-fb98-4e8f-961c-915a7672343e") as case:
            #Split then change setting after open corresponding page from I menu button
            main_page.set_timeline_timecode('00_00_02_00')
            tips_area_page.click_TipsArea_btn_split()
            timeline_operation_page.click_view_entire_video_btn()
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_19_3.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_1_19_3.png',
                                               playback_window_snap)
            main_page.select_right_click_menu('Pan & Zoom')
            case.result = pan_zoom_page.apply_motion_style(1) and case1_result

        with uuid("452d70c8-3e54-49d2-8c5d-94ad6d815e48") as case:
            #Render Preview then change setting after open corresponding page from I menu button
            timeline_operation_page.edit_timeline_render_preview()
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_19_4.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_1_19_4.png',
                                               playback_window_snap)
            main_page.select_right_click_menu('Pan & Zoom')
            case.result = pan_zoom_page.apply_motion_style(6) and case1_result

        with uuid("6021bc2f-b50f-41bc-8ef2-fcb85a0160a2") as case:
            #Undo/Redo then change setting after open corresponding page from I menu button
            main_page.click_undo()
            main_page.click_undo()
            main_page.click_redo()
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_19_5.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_1_19_5.png',
                                               playback_window_snap)
            main_page.select_right_click_menu('Pan & Zoom')
            case.result = pan_zoom_page.apply_motion_style(7) and case1_result

        with uuid("2f6b5f96-662b-4073-b10b-a95dcd104082") as case:
            #Save project and then open then change setting after open corresponding page from I menu button
            main_page.save_project('Untitled', app.testing_material + '/effect_setting_from_i_button_menu/')
            main_page.top_menu_bar_file_open_project(save_changes=False)
            main_page.handle_open_project_dialog(app.testing_material + 'effect_setting_from_i_button_menu/Untitled.pds/')
            main_page.handle_merge_media_to_current_library_dialog()
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_19_6.png')
            logger(playback_window_snap)
            case1_result = main_page.compare(Ground_Truth_Folder + '1_1_19_6.png',
                                               playback_window_snap)
            main_page.select_right_click_menu('Pan & Zoom')
            case.result = pan_zoom_page.apply_motion_style(8) and case1_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_18(self):
        with uuid("c2c5cee8-9171-4d5d-893b-ec5f029928c4") as case:
            #Pan & Zoom is disabled in i menu after link image and audio
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.select_library_icon_view_media('Speaking Out.mp3')
            main_page.tips_area_insert_media_to_selected_track()
            timeline_operation_page.select_timeline_media(0, 0)
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            pan_zoom_page.apply_motion_style(4)
            main_page.timeline_select_track(0)
            main_page.tap_SelectAll_hotkey()
            timeline_operation_page.hover_timeline_media(1, 0)
            main_page.right_click()
            main_page.select_right_click_menu('Group/Ungroup Objects')
            time.sleep(2)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            case.result = True if not main_page.select_right_click_menu('Pan & Zoom') else False

        with uuid("99afa98f-7707-4928-b96f-d61a0176b8fa") as case:
            #Blending Mode is disabled in i menu after link image and audio
            main_page.click_undo()
            main_page.click_undo()
            tips_area_page.tools.select_Blending_Mode()
            time.sleep(2)
            blending_mode_page.set_blending_mode('Darken')
            time.sleep(2)
            blending_mode_page.click_ok()
            time.sleep(2)
            main_page.timeline_select_track(0)
            main_page.tap_SelectAll_hotkey()
            timeline_operation_page.hover_timeline_media(1, 0)
            main_page.right_click()
            time.sleep(2)
            main_page.select_right_click_menu('Group/Ungroup Objects')
            time.sleep(2)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                    {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                                    {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}],
                                   {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton',
                                    'AXRoleDescription': 'button'}])
            case.result = True if not main_page.select_right_click_menu('Blending Mode') else False

        with uuid("9a670cca-ae91-4487-8afd-4bfc0c91cb55") as case:
            #White Balance is disabled in i menu after link image and audio
            main_page.click_undo()
            main_page.click_undo()
            tips_area_page.click_fix_enhance()
            fix_enhance_page.fix.switch_to_white_balance()
            fix_enhance_page.fix.white_balance.color_temperature.set_value(100)
            main_page.timeline_select_track(0)
            main_page.tap_SelectAll_hotkey()
            timeline_operation_page.hover_timeline_media(1, 0)
            main_page.right_click()
            time.sleep(2)
            main_page.select_right_click_menu('Group/Ungroup Objects')
            time.sleep(2)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                    {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                                    {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}],
                                   {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton',
                                    'AXRoleDescription': 'button'}])
            case.result = True if not main_page.select_right_click_menu('White Balance') else False

        with uuid("1825c02f-8027-4e4b-9e34-f66e5098aa01") as case:
            #Lens Correction is disabled in i menu after link image and audio
            main_page.click_undo()
            main_page.click_undo()
            tips_area_page.click_fix_enhance()
            fix_enhance_page.fix.switch_to_lens_correction()
            fix_enhance_page.fix.lens_correction.select_marker_type('HTC')
            main_page.timeline_select_track(0)
            main_page.tap_SelectAll_hotkey()
            timeline_operation_page.hover_timeline_media(1, 0)
            main_page.right_click()
            time.sleep(2)
            main_page.select_right_click_menu('Group/Ungroup Objects')
            time.sleep(2)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                    {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                                    {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}],
                                   {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton',
                                    'AXRoleDescription': 'button'}])
            case.result = True if not main_page.select_right_click_menu('Lens Correction') else False

        with uuid("f8e3820f-7a9f-4d88-b1a1-56ed2d9a448b") as case:
            #Color Adjustment is disabled in i menu after link image and audio
            main_page.click_undo()
            main_page.click_undo()
            tips_area_page.click_fix_enhance()
            fix_enhance_page.enhance.switch_to_color_adjustment()
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(200)
            main_page.timeline_select_track(0)
            main_page.tap_SelectAll_hotkey()
            timeline_operation_page.hover_timeline_media(1, 0)
            main_page.right_click()
            time.sleep(2)
            main_page.select_right_click_menu('Group/Ungroup Objects')
            time.sleep(2)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                    {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                                    {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}],
                                   {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton',
                                    'AXRoleDescription': 'button'}])
            case.result = True if not main_page.select_right_click_menu('Color Adjustment') else False

        with uuid("326b9358-2f95-4523-a6a7-a4855115446e") as case:
            #Built-in Effect is disabled in i menu after link image and audio
            main_page.click_undo()
            main_page.click_undo()
            fix_enhance_page.click_close()
            main_page.enter_room(3)
            effect_room_page.apply_effect_to_video('Beating', 0, 0)
            main_page.timeline_select_track(0)
            main_page.tap_SelectAll_hotkey()
            timeline_operation_page.hover_timeline_media(1, 0)
            main_page.right_click()
            time.sleep(2)
            main_page.select_right_click_menu('Group/Ungroup Objects')
            time.sleep(2)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                    {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                                    {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}],
                                   {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton',
                                    'AXRoleDescription': 'button'}])
            case.result = True if not main_page.select_right_click_menu('Beating') else False

        with uuid("cb598864-16e1-4ec8-ac03-b0edd206cd0e") as case:
            #LUT is disabled in i menu after link image and audio
            main_page.click_undo()
            main_page.click_undo()
            effect_room_page.import_CLUTs(app.testing_material + '/effect_setting_from_i_button_menu/3dl_1.3dl/')
            effect_room_page.apply_effect_to_video('3dl_1', 0, 0)
            main_page.timeline_select_track(0)
            main_page.tap_SelectAll_hotkey()
            timeline_operation_page.hover_timeline_media(1, 0)
            main_page.right_click()
            time.sleep(2)
            main_page.select_right_click_menu('Group/Ungroup Objects')
            time.sleep(2)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                    {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                                    {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}],
                                   {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton',
                                    'AXRoleDescription': 'button'}])
            case.result = True if not main_page.select_right_click_menu('Color LUT (3dl_1)') else False

        with uuid("6e8f9605-9576-4993-8337-8b03efb1b97e") as case:
            # Audio in Reverse is disabled in i menu after link image and audio
            main_page.click_undo()
            main_page.click_undo()
            timeline_operation_page.select_timeline_media(1, 0)
            main_page.tap_TipsArea_Tools_menu('Audio in Reverse')
            time.sleep(2)
            main_page.timeline_select_track(0)
            main_page.tap_SelectAll_hotkey()
            timeline_operation_page.hover_timeline_media(1, 0)
            main_page.right_click()
            main_page.select_right_click_menu('Group/Ungroup Objects')
            main_page.timeline_select_track(1)
            main_page.right_click()
            time.sleep(2)
            main_page.select_right_click_menu('Adjust Audio Track Height', 'Large')
            time.sleep(2)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                    {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 1},
                                    {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}],
                                   {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton',
                                    'AXRoleDescription': 'button'}])
            case.result = True if not main_page.select_right_click_menu('Audio in Reverse') else False

        with uuid("9a76a868-bb31-4a11-85c5-c14ba61d3e22") as case:
            # Audio Denoise is disabled in i menu after link image and audio
            main_page.click_undo()
            main_page.click_undo()
            main_page.timeline_select_track(1)
            main_page.right_click()
            time.sleep(2)
            main_page.select_right_click_menu('Adjust Audio Track Height', 'Medium')
            time.sleep(2)
            timeline_operation_page.select_timeline_media(1, 0)
            tips_area_page.click_fix_enhance()
            fix_enhance_page.fix.enable_audio_denoise()
            time.sleep(2)
            main_page.timeline_select_track(0)
            main_page.tap_SelectAll_hotkey()
            timeline_operation_page.hover_timeline_media(1, 0)
            main_page.right_click()
            time.sleep(2)
            main_page.select_right_click_menu('Group/Ungroup Objects')
            main_page.timeline_select_track(1)
            main_page.right_click()
            time.sleep(2)
            main_page.select_right_click_menu('Adjust Audio Track Height', 'Large')
            time.sleep(2)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                    {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 1},
                                    {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}],
                                   {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton',
                                    'AXRoleDescription': 'button'}])
            case.result = True if not main_page.select_right_click_menu('Audio Denoise') else False


