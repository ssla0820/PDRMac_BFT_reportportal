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
    def test_1_1_1(self):
        with uuid("53df22e1-fa1f-411e-b8a6-17da6d4ff4d1") as case:
            #Show Pan & Zoom in i menu after apply Pan & Zoom
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            pan_zoom_page.apply_motion_style(4)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_1_1.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_1_1.png',
                                               playback_window_snap)

        with uuid("0edd76e0-954c-4795-a2ac-6256b4ce667c") as case:
            #Able to open Pan & Zoom from i menu correctly
            main_page.select_right_click_menu('Pan & Zoom')
            case.result = pan_zoom_page.is_enter_pan_zoom()

        with uuid("ed9e27fd-a9e5-430d-a6d4-68cf325334b9") as case:
            #Able to change setting after open Pan & Zoom from I menu button
            case.result = pan_zoom_page.apply_motion_style(3)

        with uuid("2e5ae8ee-ca41-436a-a4a6-df7dd3a7877a") as case:
            #Show Blending Mode in i menu after apply
            main_page.click_undo()
            main_page.click_undo()
            main_page.click_undo()
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.timeline_select_track(2)
            main_page.select_library_icon_view_media('Landscape 01.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            tips_area_page.tools.select_Blending_Mode()
            blending_mode_page.set_blending_mode('Darken')
            blending_mode_page.click_ok()
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 2}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_1_2.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_1_2.png',
                                               playback_window_snap)

        with uuid("7e30836f-73de-49e5-aa42-cac8f796c7b7") as case:
            #Able to open Blending Mode from i menu correctly
            main_page.select_right_click_menu('Blending Mode')
            case.result = blending_mode_page.is_in_blending_mode()

        with uuid("721b3405-110d-4978-bde7-b5fb401e5de1") as case:
            #Able to change setting after open Blending mode from I menu button
            case.result = blending_mode_page.set_blending_mode('Lighten')
            main_page.press_esc_key()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):

        with uuid("237a6f8b-3a7a-4606-9568-745eed23151c") as case:
            #Show White Balance in i menu after apply
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            tips_area_page.click_fix_enhance()
            fix_enhance_page.fix.switch_to_white_balance()
            fix_enhance_page.fix.white_balance.color_temperature.set_value(100)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_1_3.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_1_3.png',
                                               playback_window_snap)

        with uuid("ba586b6f-8de4-4502-b89e-8b17643de9e4") as case:
            #Able to open White Balance from i menu correctly
            main_page.select_right_click_menu('White Balance')
            case.result = fix_enhance_page.is_in_fix_enhance()

        with uuid("dc79cb90-b3fa-4b05-aaf8-68b6293b298d") as case:
            #Able to change setting after open White balance from I menu button
            fix_enhance_page.fix.white_balance.color_temperature.set_value(1)
            case.result = True if fix_enhance_page.fix.white_balance.color_temperature.get_value() == '1' else False

        with uuid("f5239d18-1267-4e5e-a09f-3589af049ca2") as case:
            #Show Lens Correction in i menu after apply
            fix_enhance_page.fix.switch_to_lens_correction()
            fix_enhance_page.fix.lens_correction.select_marker_type('HTC')
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_1_4.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_1_4.png',
                                               playback_window_snap)

        with uuid("57f78c18-e4aa-44dd-b9fe-3486cb0db31a") as case:
            #Able to open Lens Correction page from i menu correctly
            main_page.select_right_click_menu('Lens Correction')
            case.result = fix_enhance_page.is_in_fix_enhance()

        with uuid("361465be-d8ba-40f0-a5e7-91263c6e31a7") as case:
            #Able to change setting after open Lens correction from I menu button
            fix_enhance_page.fix.lens_correction.select_marker_type('JVC')
            case.result = True if fix_enhance_page.fix.lens_correction.get_marker_type() == 'JVC' else False

        with uuid("0a000efc-2577-4291-9a66-a00bbfebf4c4") as case:
            #Show Color Adjustment in i menu after apply
            fix_enhance_page.enhance.switch_to_color_adjustment()
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(200)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_1_5.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_1_5.png',
                                               playback_window_snap)

        with uuid("bc90d626-0b98-4941-9083-5fbcd4048098") as case:
            #Able to open Color Adjustment page from i menu correctly
            main_page.select_right_click_menu('Color Adjustment')
            case.result = fix_enhance_page.is_in_fix_enhance()

        with uuid("97cc5e18-f42d-4a4d-a2fc-3e5183fe31f9") as case:
            #Able to change setting after openColor Adjustment from I menu button
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(25)
            case.result = True if fix_enhance_page.enhance.color_adjustment.exposure.get_value() == '25' else False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid("449d5115-6655-4712-9829-028c26ae60d8") as case:
            #Show applied effect name in i menu after apply
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.enter_room(3)
            effect_room_page.apply_effect_to_video('Beating',0,0)

            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_3_1.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_3_1.png',
                                               playback_window_snap)

        with uuid("849fcdea-1e57-47cd-8ba2-dba9c1e62f26") as case:
            #Able to open effect setting from i menu correctly
            main_page.select_right_click_menu('Beating')
            current_image = effect_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_3_2.png')
            # logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1_1_3_2.png', current_image)
            case.result = compare_result

        with uuid("8035adbc-a8c2-4d98-bdb8-1ff1d0c42274") as case:
            #Able to change setting after open effect settings from I menu button
            effect_room_page.remove_from_effectsettings()
            case.result = effect_room_page.check_effect_room()

        with uuid("3b0efb1f-ed75-4096-8071-ca42e2d13f8b") as case:
            #Show applied effect name in i menu after apply(LUT)
            effect_room_page.import_CLUTs(app.testing_material + '/effect_setting_from_i_button_menu/3dl_1.3dl/')
            effect_room_page.apply_effect_to_video('3dl_1',0,0)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_3_3.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_3_3.png',
                                               playback_window_snap)

        with uuid("f39a498e-530a-4554-9765-52faeffa7c8b") as case:
            #Able to open effect setting from i menu correctly(LUT)
            main_page.select_right_click_menu('Color LUT (3dl_1)')
            current_image = effect_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_3_4.png')
            # logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1_1_3_4.png', current_image)
            case.result = compare_result

        with uuid("1e50e916-fbac-4b61-aae2-b7b690fa0331") as case:
            #Able to change setting after open effect settings from I menu button(LUT)
            effect_room_page.remove_from_effectsettings()
            case.result = effect_room_page.check_effect_room()

        with uuid("f4fa17b2-c5c5-4947-abbb-1d441c6d2fd4") as case:
            #Show applied effect name in i menu after apply(LUT)
            media_room_page.library_menu_small_icons()
            effect_room_page.apply_effect_to_video('3dl_1',0,0)
            time.sleep(DELAY_TIME * 2)
            main_page.select_LibraryRoom_category('Style Effect')
            time.sleep(DELAY_TIME*2)
            effect_room_page.apply_effect_to_video('Black and White',0,0)
            effect_room_page.apply_effect_to_video('Blackout', 0, 0)
            effect_room_page.apply_effect_to_video('Bloom', 0, 0)
            effect_room_page.apply_effect_to_video('Blur Bar', 0, 0)
            effect_room_page.apply_effect_to_video('Broken Glass', 0, 0)
            effect_room_page.apply_effect_to_video('Bump Map', 0, 0)
            effect_room_page.apply_effect_to_video('Band Noise', 0, 0)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_3_5.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_3_5.png',
                                               playback_window_snap)

        with uuid("bf511d82-53ec-48f4-8e62-256e656eb1f1") as case:
            #Able to open effect setting from i menu correctly(LUT)
            main_page.select_right_click_menu('Band Noise')
            time.sleep(DELAY_TIME)
            current_image = effect_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_3_6.png')
            # logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1_1_3_6.png', current_image)
            case.result = compare_result

        with uuid("1dbe9df2-3b03-4521-9fc8-e900208636e7") as case:
            #Able to change setting after open effect settings from I menu button(LUT)
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            case.result = effect_room_page.check_effect_room()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid("a3098860-dd69-420a-a68a-367c33bbf9d0") as case:
            #Show Pan & Zoom in i menu after apply Pan & Zoom
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            tips_area_page.tools.select_CropZoomPan()
            crop_zoom_pan_page.click_position_x_arrow("up")
            crop_zoom_pan_page.click_ok()
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_4_1.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_4_1.png',
                                               playback_window_snap)

        with uuid("dd38a1ea-7f1a-462f-9c17-c600517ff16f") as case:
            #Able to open Pan & Zoom from i menu correctly
            main_page.select_right_click_menu('Crop/Zoom/Pan')
            case.result = crop_zoom_pan_page.is_enter_crop_zoom_pan()

        with uuid("d7a2d22f-f422-4b38-ba4f-df20e420ecee") as case:
            #Able to change setting after open Pan & Zoom from I menu button
            case.result = crop_zoom_pan_page.click_position_y_arrow("up")
            crop_zoom_pan_page.click_ok()

        with uuid("b8dc7e83-9a63-455d-871e-a370979f9e4e") as case:
            #Show Video Speed in i menu after apply
            main_page.click_undo()
            main_page.click_undo()
            main_page.tap_TipsArea_Tools_menu('Video Speed')
            video_speed_page.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_ArrowButton('Up')
            video_speed_page.Edit_VideoSpeedDesigner_ClickOK()
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_4_2.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_4_2.png',
                                               playback_window_snap)

        with uuid("20b84657-24c6-4c2a-ae62-a15ce8d5f95b") as case:
            #Able to open Video Speed from i menu correctly
            main_page.select_right_click_menu('Video Speed')
            case.result = main_page.exist(L.video_speed.main)

        with uuid("903bfacf-4061-4e55-9364-59c934ef99c9") as case:
            #Able to change setting after open video speed from I menu button
            case.result = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_ArrowButton('Up')
            video_speed_page.Edit_VideoSpeedDesigner_ClickOK()

        with uuid("88fc067d-4b4d-4561-bb01-507b48c5552d") as case:
            #Show Video in Reverse in i menu after apply
            main_page.click_undo()
            main_page.click_undo()
            main_page.tap_TipsArea_Tools_menu('Video in Reverse')
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_4_3.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_4_3.png',
                                               playback_window_snap)

        with uuid("3cc930dc-b250-4f57-af8a-0081d2b2eb90") as case:
            #Disable Video in Reverse directly if click from I menu button
            main_page.select_right_click_menu('Video in Reverse')
            case.result = True if not main_page.exist([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}]) else False

        with uuid("54a99d10-f7a5-4236-90dd-7e85830c7ed7") as case:
            #Show Blending Mode in i menu after apply
            main_page.timeline_select_track(2)
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            tips_area_page.tools.select_Blending_Mode()
            blending_mode_page.set_blending_mode('Darken')
            blending_mode_page.click_ok()
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 2}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_4_5.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_4_5.png',
                                               playback_window_snap)

        with uuid("04a2ba84-7cb9-4098-8d8e-4b0700a42f4d") as case:
            #Able to open Blending Mode from i menu correctly
            main_page.select_right_click_menu('Blending Mode')
            case.result = blending_mode_page.is_in_blending_mode()

        with uuid("9f9c404e-b9d9-4f73-9a5d-c769db111ce2") as case:
            #Able to change setting after open Blending mode from I menu button
            case.result = blending_mode_page.set_blending_mode('Lighten')
            main_page.press_esc_key()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):

        with uuid("56cdbfa7-b21d-496c-bc25-0dc0f29cb5d3") as case:
            #Show White Balance in i menu after apply(Video)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            tips_area_page.click_fix_enhance()
            fix_enhance_page.fix.switch_to_white_balance()
            fix_enhance_page.fix.white_balance.color_temperature.set_value(100)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_5_1.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_5_1.png',
                                               playback_window_snap)

        with uuid("e01d6c24-065a-495e-89b5-74e74bee93c5") as case:
            #Able to open White Balance from i menu correctly
            main_page.select_right_click_menu('White Balance')
            case.result = fix_enhance_page.is_in_fix_enhance()

        with uuid("2482ac61-f67e-4505-ac1f-68940149f3af") as case:
            #Able to change setting after open White balance from I menu button
            fix_enhance_page.fix.white_balance.color_temperature.set_value(1)
            case.result = True if fix_enhance_page.fix.white_balance.color_temperature.get_value() == '1' else False

        with uuid("9d50c2a3-1a45-49e1-b5d4-5bc9b1ebf15d") as case:
            #Show Lens Correction in i menu after apply
            fix_enhance_page.fix.switch_to_lens_correction()
            fix_enhance_page.fix.lens_correction.select_marker_type('HTC')
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_5_2.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_5_2.png',
                                               playback_window_snap)

        with uuid("2302a580-6c18-4b0d-b1c2-92216892eea8") as case:
            #Able to open Lens Correction page from i menu correctly
            main_page.select_right_click_menu('Lens Correction')
            case.result = fix_enhance_page.is_in_fix_enhance()

        with uuid("d513dfc1-1e47-48aa-986e-4763bd318bde") as case:
            #Able to change setting after open Lens correction from I menu button
            fix_enhance_page.fix.lens_correction.select_marker_type('JVC')
            case.result = True if fix_enhance_page.fix.lens_correction.get_marker_type() == 'JVC' else False

        with uuid("8003cb91-0cc9-45d8-bdc2-c74c355a898a") as case:
            #Show Color Adjustment in i menu after apply
            fix_enhance_page.enhance.switch_to_color_adjustment()
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(200)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_5_3.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_5_3.png',
                                               playback_window_snap)

        with uuid("cd1ebf04-6aae-435e-b600-360059a898be") as case:
            #Able to open Color Adjustment page from i menu correctly
            main_page.select_right_click_menu('Color Adjustment')
            case.result = fix_enhance_page.is_in_fix_enhance()

        with uuid("b49a00b9-bc6d-4200-bc88-e108260c579d") as case:
            #Able to change setting after openColor Adjustment from I menu button
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(25)
            case.result = True if fix_enhance_page.enhance.color_adjustment.exposure.get_value() == '25' else False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid("44505fc8-9d34-4f5e-92c4-d75f69b5f267") as case:
            #Show applied effect name in i menu after apply
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.enter_room(3)
            effect_room_page.apply_effect_to_video('Beating',0,0)

            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_6_1.png')
            logger(playback_window_snap)
            result = main_page.compare(Ground_Truth_Folder + '1_1_6_1.png', playback_window_snap)
            case.result = result

        with uuid("588ea505-526b-46fb-9f85-0d0440f11561") as case:
            #Able to open effect setting from i menu correctly
            main_page.select_right_click_menu('Beating')
            current_image = effect_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_6_2.png')
            # logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1_1_6_2.png', current_image)
            case.result = compare_result

        with uuid("1683db8f-2d3e-4c42-89b4-8cd64a608efb") as case:
            #Able to change setting after open effect settings from I menu button
            effect_room_page.remove_from_effectsettings()
            case.result = effect_room_page.check_effect_room()

        with uuid("e9a4a67b-8268-445e-bcc7-1214747034e3") as case:
            #Show applied effect name in i menu after apply(LUT)
            effect_room_page.import_CLUTs(app.testing_material + '/effect_setting_from_i_button_menu/3dl_1.3dl/')
            main_page.select_specific_tag('Color LUT')
            effect_room_page.apply_effect_to_video('3dl_1',0,0)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_6_3.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_6_3.png',
                                               playback_window_snap)

        with uuid("c1c9746b-2241-4c38-9176-ddf12cd504ef") as case:
            #Able to open effect setting from i menu correctly(LUT)
            main_page.select_right_click_menu('Color LUT (3dl_1)')
            current_image = effect_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_6_4.png')
            # logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1_1_6_4.png', current_image)
            case.result = compare_result

        with uuid("5a202e67-b43b-441a-a46c-e9751251a288") as case:
            #Able to change setting after open effect settings from I menu button(LUT)
            effect_room_page.remove_from_effectsettings()
            case.result = effect_room_page.check_effect_room()

        with uuid("66b95849-7400-4235-8a0e-004dfb9758a3") as case:
            #Show applied effect name in i menu after apply(LUT)
            media_room_page.library_menu_small_icons()
            effect_room_page.apply_effect_to_video('3dl_1',0,0)
            time.sleep(DELAY_TIME * 2)
            main_page.select_LibraryRoom_category('Style Effect')
            time.sleep(DELAY_TIME*2)
            effect_room_page.apply_effect_to_video('Black and White',0,0)
            effect_room_page.apply_effect_to_video('Blackout', 0, 0)
            effect_room_page.apply_effect_to_video('Bloom', 0, 0)
            effect_room_page.apply_effect_to_video('Blur Bar', 0, 0)
            effect_room_page.apply_effect_to_video('Broken Glass', 0, 0)
            effect_room_page.apply_effect_to_video('Bump Map', 0, 0)
            effect_room_page.apply_effect_to_video('Band Noise', 0, 0)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_6_5.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_6_5.png',
                                               playback_window_snap)

        with uuid("a2e0cbad-f511-40ac-98df-0614cd1d292b") as case:
            #Able to open effect setting from i menu correctly(LUT)
            main_page.select_right_click_menu('Band Noise')
            current_image = effect_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_6_6.png')
            # logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1_1_6_6.png', current_image)
            case.result = compare_result

        with uuid("b402b66d-4f1e-46bd-80f4-acd234312a53") as case:
            #Able to change setting after open effect settings from I menu button(LUT)
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            case.result = effect_room_page.check_effect_room()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):

        with uuid("9e5fb192-7e40-465b-a5ef-9958e695c5cb") as case:
            #Show Audio in Reverse in i menu after apply
            main_page.select_library_icon_view_media('Speaking Out.mp3')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.tap_TipsArea_Tools_menu('Audio in Reverse')
            main_page.timeline_select_track(1)
            main_page.right_click()
            main_page.select_right_click_menu('Adjust Audio Track Height', 'Large')
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 1}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_7_2.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_7_2.png',
                                               playback_window_snap)

        with uuid("8f4318b2-9aef-4b8c-8a73-9f12f4399ea8") as case:
            #Disable Video in Reverse directly if click from I menu button
            main_page.select_right_click_menu('Audio in Reverse')
            case.result = True if not main_page.exist([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 1}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}]) else False

        with uuid("24a66157-2fc6-47a1-a88c-227d47cc9efa") as case:
            #Show Audio Denoise in i menu after apply
            main_page.click_undo()
            main_page.click_undo()
            tips_area_page.click_fix_enhance()
            fix_enhance_page.fix.enable_audio_denoise()
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                    {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 1},
                                    {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}],
                                   {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton',
                                    'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_7_3.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_7_3.png',
                                            playback_window_snap)

        with uuid("439a0084-1164-412c-941b-51c2d105d9c6") as case:
            #Able to open Audio Denoise page from i menu correctly
            main_page.select_right_click_menu('Audio Denoise')
            case.result = fix_enhance_page.is_in_fix_enhance()

        with uuid("fa19bbaa-a702-4169-9da2-710ccff9d336") as case:
            # Able to change setting after open audio denoise from I menu button
            fix_enhance_page.fix.audio_denoise.set_noise_type(1)
            case.result = True if fix_enhance_page.fix.audio_denoise.get_noise_type() == 'Wind noise' else False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        with uuid("7b92304d-3273-473f-9d9c-f57966330a6e") as case:
            # Show Blending Mode in i menu after apply (color board)
            media_room_page.enter_color_boards()
            main_page.timeline_select_track(1)
            main_page.click_library_details_view()
            media_room_page.sound_clips_select_media('2, 52, 111')
            #main_page.select_library_icon_view_media('4,48,239')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.timeline_select_track(2)
            media_room_page.sound_clips_select_media('81, 0, 103')
            #main_page.select_library_icon_view_media('19,228,4')
            main_page.click_library_icon_view()
            main_page.tips_area_insert_media_to_selected_track()
            main_page.tap_TipsArea_Tools_menu('PiP Designer')
            pip_designer_page.switch_mode('Advanced')
            pip_designer_page.express_mode.unfold_properties_object_setting_tab()
            pip_designer_page.drag_properties_scroll_bar(10)
            pip_designer_page.set_blending_mode_multiply()
            pip_designer_page.click_ok()
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                    {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 2},
                                    {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}],
                                   {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton',
                                    'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_8_1.png')
            logger(playback_window_snap)
            result = main_page.compare(Ground_Truth_Folder + '1_1_8_1.png', playback_window_snap)
            case.result = result

        with uuid("fe16067d-b5ae-4c0b-9a14-59df885b531a") as case:
            #Disable function in I menu
            case.result = True if not main_page.select_right_click_menu('Blending Mode') else False

        with uuid("7a3c3222-6f70-4d13-b74f-4b43d87d824f") as case:
            #Show applied effect name in i menu after apply
            main_page.click_undo()
            main_page.click_undo()
            timeline_operation_page.select_timeline_media(0,0)
            main_page.enter_room(3)
            effect_room_page.apply_effect_to_video('Beating',0,0)

            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_8_2.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_8_2.png',
                                               playback_window_snap)

        with uuid("b9316a08-dd04-4c02-a30c-9d0c2f07eb7e") as case:
            #Able to open effect setting from i menu correctly
            main_page.select_right_click_menu('Beating')
            current_image = effect_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_8_3.png')
            # logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1_1_8_3.png', current_image)
            case.result = compare_result

        with uuid("fbbf9a64-cad9-420a-95f0-ab4561b8d519") as case:
            #Able to change setting after open effect settings from I menu button
            effect_room_page.remove_from_effectsettings()
            case.result = effect_room_page.check_effect_room()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        with uuid("2586b03b-eba6-47b3-88ef-86d3e0466d9e") as case:
            #Show applied effect name in i menu after apply(title)
            main_page.enter_room(1)
            main_page.select_library_icon_view_media('Default')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.enter_room(3)
            effect_room_page.apply_effect_to_video('Beating',0,0)

            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_9_2.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_9_2.png',
                                               playback_window_snap)

        with uuid("80428bbe-3e91-4c75-9b62-b9bbe47cf177") as case:
            #Able to open effect setting from i menu correctly
            main_page.select_right_click_menu('Beating')
            current_image = effect_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_9_3.png')
            # logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1_1_9_3.png', current_image)
            case.result = compare_result

        with uuid("02cee294-5bcd-4a06-aedf-88e1a5992783") as case:
            #Able to change setting after open effect settings from I menu button
            effect_room_page.remove_from_effectsettings()
            case.result = effect_room_page.check_effect_room()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_12(self):
        with uuid("1793c004-d3b2-449a-9dbf-e3a0ffad1971") as case:
            #Show applied effect name in i menu after apply(PiP)
            main_page.enter_room(4)
            main_page.select_LibraryRoom_category('Shape')
            main_page.select_library_icon_view_media('Shape 001')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.enter_room(3)
            effect_room_page.apply_effect_to_video('Beating',0,0)
            time.sleep(3)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_12_1.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_12_1.png',
                                               playback_window_snap)

        with uuid("54469e67-54a9-4d9a-b97f-11e66a38007f") as case:
            #Able to open effect setting from i menu correctly
            main_page.select_right_click_menu('Beating')
            time.sleep(3)
            current_image = effect_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_12_2.png')
            # logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1_1_12_2.png', current_image)
            case.result = compare_result

        with uuid("1cf048d6-3f9a-4a28-b632-6a252c6d672b") as case:
            #Able to change setting after open effect settings from I menu button
            effect_room_page.remove_from_effectsettings()
            case.result = effect_room_page.check_effect_room()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_13(self):
        with uuid("78ecd11f-6af6-4e54-a50a-14af6f0f9f4b") as case:
            #Show applied effect name in i menu after apply(Video_Collage)
            main_page.top_menu_bar_plugins_video_collage_designer()
            video_collage_designer_page.media.select_media('Skateboard 01.mp4')
            video_collage_designer_page.media.click_auto_fill()
            video_collage_designer_page.click_ok()
            main_page.enter_room(3)
            effect_room_page.apply_effect_to_video('Beating',0,0)

            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 0}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_13_1.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_13_1.png',
                                               playback_window_snap)

        with uuid("e829f201-9df4-45cd-838a-3e0d7c42f92d") as case:
            #Able to open effect setting from i menu correctly
            main_page.select_right_click_menu('Beating')
            current_image = effect_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_13_2.png')
            # logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1_1_13_2.png', current_image)
            case.result = compare_result

        with uuid("77469ebd-017c-4dee-a01d-cd153c7b40a8") as case:
            #Able to change setting after open effect settings from I menu button
            effect_room_page.remove_from_effectsettings()
            case.result = effect_room_page.check_effect_room()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_14(self):
        with uuid("523dda80-b494-4cb5-a55c-47218078d889") as case:
            #Show Pan & Zoom in i menu after apply Pan & Zoom(Transition)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(1)
            main_page.enter_room(2)
            main_page.select_library_icon_view_media('Arrow 2')
            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Cross')
            timeline_operation_page.select_timeline_media(0,1)
            tips_area_page.tools.select_CropZoomPan()
            crop_zoom_pan_page.click_position_x_arrow("up")
            crop_zoom_pan_page.click_ok()
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_14_1.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_14_1.png',
                                               playback_window_snap)

        with uuid("a04c5854-e1fb-4d55-b07f-83f156951dd6") as case:
            #Able to open Pan & Zoom from i menu correctly
            main_page.select_right_click_menu('Crop/Zoom/Pan')
            case.result = crop_zoom_pan_page.is_enter_crop_zoom_pan()

        with uuid("899c5e8a-ed25-405b-8792-d27e8431c6d1") as case:
            #Able to change setting after open Pan & Zoom from I menu button
            case.result = crop_zoom_pan_page.click_position_y_arrow("up")
            crop_zoom_pan_page.click_ok()

        with uuid("11b225cc-b392-4730-b00b-9168740a5091") as case:
            #Show Video Speed in i menu after apply
            main_page.click_undo()
            main_page.click_undo()
            main_page.tap_TipsArea_Tools_menu('Video Speed')
            video_speed_page.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_ArrowButton('Up')
            video_speed_page.Edit_VideoSpeedDesigner_ClickOK()
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_14_2.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_14_2.png',
                                               playback_window_snap)

        with uuid("ee0298aa-b97a-4734-b07c-d77ec4689b22") as case:
            #Able to open Video Speed from i menu correctly
            main_page.select_right_click_menu('Video Speed')
            case.result = main_page.exist(L.video_speed.main)

        with uuid("1f8f4c98-609b-4216-8448-092c64c924d9") as case:
            #Able to change setting after open video speed from I menu button
            case.result = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_ArrowButton('Up')
            video_speed_page.Edit_VideoSpeedDesigner_ClickOK()

        with uuid("f62306ae-7cb7-426b-a853-225d0cce60ea") as case:
            #Show Video in Reverse in i menu after apply
            main_page.click_undo()
            main_page.click_undo()
            main_page.tap_TipsArea_Tools_menu('Video in Reverse')
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_14_3.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_14_3.png',
                                               playback_window_snap)

        with uuid("596c65ce-85ff-4159-b88d-c88d4301487e") as case:
            #Disable Video in Reverse directly if click from I menu button
            main_page.select_right_click_menu('Video in Reverse')
            case.result = True if not main_page.exist([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}]) else False

        with uuid("092baa11-14bd-429d-be23-7941c452fa4b") as case:
            #Show Blending Mode in i menu after apply
            timeline_operation_page.select_timeline_media(0, 1)
            tips_area_page.tools.select_Blending_Mode()
            blending_mode_page.set_blending_mode('Darken')
            blending_mode_page.click_ok()
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_14_5.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_14_5.png',
                                               playback_window_snap)

        with uuid("2b5821ac-6e72-4c07-9fae-a772cc8d1b38") as case:
            #Able to open Blending Mode from i menu correctly
            main_page.select_right_click_menu('Blending Mode')
            case.result = blending_mode_page.is_in_blending_mode()

        with uuid("475ec6f6-5d3a-4f26-8702-33ab6c9160aa") as case:
            #Able to change setting after open Blending mode from I menu button
            case.result = blending_mode_page.set_blending_mode('Lighten')
            main_page.press_esc_key()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_15(self):

        with uuid("97133a9f-2437-4222-8ff7-46d4e1347c45") as case:
            #Show White Balance in i menu after apply(Transition)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(1)
            main_page.enter_room(2)
            main_page.select_library_icon_view_media('Arrow 2')
            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Cross')
            timeline_operation_page.select_timeline_media(0, 1)
            tips_area_page.click_fix_enhance()
            fix_enhance_page.fix.switch_to_white_balance()
            fix_enhance_page.fix.white_balance.color_temperature.set_value(100)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_15_1.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_15_1.png',
                                               playback_window_snap)

        with uuid("89c0dfa6-2c31-49c0-8286-c9ccd40ac96e") as case:
            #Able to open White Balance from i menu correctly
            main_page.select_right_click_menu('White Balance')
            case.result = fix_enhance_page.is_in_fix_enhance()

        with uuid("32ee2673-95db-4ff3-8327-a562357d0e05") as case:
            #Able to change setting after open White balance from I menu button
            fix_enhance_page.fix.white_balance.color_temperature.set_value(1)
            case.result = True if fix_enhance_page.fix.white_balance.color_temperature.get_value() == '1' else False

        with uuid("86b1445e-22cb-4469-88ac-2756dfaaee8a") as case:
            #Show Lens Correction in i menu after apply
            fix_enhance_page.fix.switch_to_lens_correction()
            fix_enhance_page.fix.lens_correction.select_marker_type('HTC')
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_15_2.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_15_2.png',
                                               playback_window_snap)

        with uuid("3fe06f59-9a20-4d7f-9dcf-81d4a95f73da") as case:
            #Able to open Lens Correction page from i menu correctly
            main_page.select_right_click_menu('Lens Correction')
            case.result = fix_enhance_page.is_in_fix_enhance()

        with uuid("8d030818-c4a4-4ffc-b961-10996291a593") as case:
            #Able to change setting after open Lens correction from I menu button
            fix_enhance_page.fix.lens_correction.select_marker_type('JVC')
            case.result = True if fix_enhance_page.fix.lens_correction.get_marker_type() == 'JVC' else False

        with uuid("7f6470a1-5ba7-4071-b8f5-ccbad363751e") as case:
            #Show Color Adjustment in i menu after apply
            fix_enhance_page.enhance.switch_to_color_adjustment()
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(200)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_15_3.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_15_3.png',
                                               playback_window_snap)

        with uuid("207d623c-dcc8-42d8-908a-9ae917bc3e9a") as case:
            #Able to open Color Adjustment page from i menu correctly
            main_page.select_right_click_menu('Color Adjustment')
            case.result = fix_enhance_page.is_in_fix_enhance()

        with uuid("48f0ed99-0716-40e4-b08b-3f41484b9d4a") as case:
            #Able to change setting after openColor Adjustment from I menu button
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(25)
            case.result = True if fix_enhance_page.enhance.color_adjustment.exposure.get_value() == '25' else False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_16(self):
        with uuid("4d46b154-88e4-42fe-9ea1-ca9eb36a5449") as case:
            #Show applied effect name in i menu after apply(Transition)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.tips_area_insert_media_to_selected_track(1)
            main_page.enter_room(2)
            main_page.select_library_icon_view_media('Arrow 2')
            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Cross')
            timeline_operation_page.select_timeline_media(0, 1)
            main_page.enter_room(3)
            effect_room_page.apply_effect_to_video('Beating',0,1)

            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_16_1.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_16_1.png',
                                               playback_window_snap)

        with uuid("4af8af03-823b-4d6d-a48e-d5b39598e54c") as case:
            #Able to open effect setting from i menu correctly
            main_page.select_right_click_menu('Beating')
            current_image = effect_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_16_2.png')
            # logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1_1_16_2.png', current_image)
            case.result = compare_result

        with uuid("5e398ebf-1ede-42d6-a0f7-22ba9eaf9676") as case:
            #Able to change setting after open effect settings from I menu button
            effect_room_page.remove_from_effectsettings()
            case.result = effect_room_page.check_effect_room()

        with uuid("da90b981-5cd8-4f6e-b2a5-680782b7c0aa") as case:
            #Show applied effect name in i menu after apply(LUT)
            effect_room_page.import_CLUTs(app.testing_material + '/effect_setting_from_i_button_menu/3dl_1.3dl/')
            main_page.select_specific_tag('Color LUT')
            effect_room_page.apply_effect_to_video('3dl_1',0,1)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            time.sleep(DELAY_TIME)
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_16_3.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_16_3.png',
                                               playback_window_snap)

        with uuid("4570b651-d178-4f10-bdd2-4a85646f2c88") as case:
            #Able to open effect setting from i menu correctly(LUT)
            main_page.select_right_click_menu('Color LUT (3dl_1)')
            current_image = effect_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_16_4.png')
            # logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1_1_16_4.png', current_image)
            case.result = compare_result

        with uuid("b7a72431-dbfd-4ea0-b7cf-1b19e549a31b") as case:
            #Able to change setting after open effect settings from I menu button(LUT)
            effect_room_page.remove_from_effectsettings()
            case.result = effect_room_page.check_effect_room()

        with uuid("46fb39a4-548e-469d-82f2-b73363db7f5d") as case:
            #Show applied effect name in i menu after apply(LUT)
            media_room_page.library_menu_small_icons()
            effect_room_page.apply_effect_to_video('3dl_1',0,1)
            time.sleep(DELAY_TIME * 2)
            main_page.select_LibraryRoom_category('Style Effect')
            time.sleep(DELAY_TIME*2)
            effect_room_page.apply_effect_to_video('Black and White',0,1)
            effect_room_page.apply_effect_to_video('Blackout', 0, 1)
            effect_room_page.apply_effect_to_video('Bloom', 0, 1)
            effect_room_page.apply_effect_to_video('Blur Bar', 0, 1)
            effect_room_page.apply_effect_to_video('Broken Glass', 0, 1)
            effect_room_page.apply_effect_to_video('Bump Map', 0, 1)
            effect_room_page.apply_effect_to_video('Band Noise', 0, 1)
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_16_5.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_16_5.png',
                                               playback_window_snap)

        with uuid("4025438e-2c71-4e3c-8443-84bb13925452") as case:
            #Able to open effect setting from i menu correctly(LUT)
            main_page.select_right_click_menu('Band Noise')
            current_image = effect_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_16_6.png')
            # logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1_1_16_6.png', current_image)
            case.result = compare_result

        with uuid("f00eec3b-811e-4b15-a0aa-63d95f332b59") as case:
            #Able to change setting after open effect settings from I menu button(LUT)
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            effect_room_page.remove_from_effectsettings()
            case.result = effect_room_page.check_effect_room()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_17(self):
        with uuid("5f3b3974-0403-41c4-88c6-ea47b4333eb8") as case:
            #Show Audio in Reverse in i menu after apply
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
            main_page.tap_TipsArea_Tools_menu('Audio in Reverse')
            main_page.timeline_select_track(1)
            main_page.right_click()
            main_page.select_right_click_menu('Adjust Audio Track Height', 'Large')
            main_page.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 1}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            playback_window_snap = main_page.snapshot(locator=L.timeline_operation.workspace,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_17_2.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_17_2.png',
                                               playback_window_snap)

        with uuid("18627ea6-7fb3-43d3-a3c6-fbb2e2990307") as case:
            #Disable Video in Reverse directly if click from I menu button
            main_page.select_right_click_menu('Audio in Reverse')
            case.result = True if not main_page.exist([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 1}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}]) else False

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
            logger(app.testing_material + 'effect_setting_from_i_button_menu/3dl_1.3dl/')
            effect_room_page.import_CLUTs(app.testing_material + 'effect_setting_from_i_button_menu/3dl_1.3dl/')
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

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_19(self):
        with uuid("33660494-d25c-489e-9279-8c58e5c96116") as case:
            #Copy & Paste then change setting after open corresponding page from I menu button
            time.sleep(DELAY_TIME*1)
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
    def test_1_1_20(self):
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
    def test_skip_case(self):
        with uuid('''
630a6861-27cc-468d-abe6-1e8a85e47709
905ab428-1eb1-4a52-893d-f98ed018c02e
036cde27-993a-479f-8936-c94c474e04f8
dd613244-9453-42b1-a0e0-e01a649d6da7
296deb5c-19b0-4c7a-b48e-a3f925447ee9
ef7ffffc-6938-4a9f-879a-e126eac292ff
0d6ea4b2-de8f-4ea2-b7a5-8fcffd1fb737
24acee5c-96c4-4967-aa6c-67d8abfb02df
e83b0eb4-7d36-482b-a7ac-8cf0358abba4
7b5b8204-3210-4f97-8777-548cf4eb740e
aa9ceb09-307a-4b0a-a82f-fdc8de0495eb
14f15201-5dde-4503-b0b0-40912232c930
1bb8af53-5d7a-4be7-aa5d-f68e17fabd68
cf282a11-0436-45fa-bc05-a60d86fadc42
592560d8-f997-42eb-847d-fd31c6493f44
c4a0f591-0426-4ced-927b-faa637832aaf
e90274ef-5be3-4e3e-b11b-1ec84c87002f
fbd7da32-0e9a-4c58-8d51-55dcc9afd3a5
256b9014-565c-4305-9ed6-7e5927f7b077
6d00022c-d1af-4a51-8103-10f5d99866f6
db985244-7be8-4dfb-af67-f38be65075af
adc2a555-845c-416d-bf91-34cce5da269d
439d6f37-2ed3-40fa-b9f4-c9d9a9ad418f
318fc829-eaba-4866-9891-2eb180a6943f
                        ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"