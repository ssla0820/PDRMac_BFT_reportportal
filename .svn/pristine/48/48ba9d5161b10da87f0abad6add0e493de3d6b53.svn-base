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
mwc = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mwc)
base_page = PageFactory().get_page_object('base_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
fix_enhance_page = PageFactory().get_page_object('fix_enhance_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
keyframe_room_page = PageFactory().get_page_object('keyframe_room_page', mwc)
effect_room_page = PageFactory().get_page_object('effect_room_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
transition_room_page = PageFactory().get_page_object('transition_room_page', mwc)
pip_designer_page = PageFactory().get_page_object('pip_designer_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
precut_page = PageFactory().get_page_object('precut_page', mwc)
mask_designer_page = PageFactory().get_page_object('mask_designer_page', mwc)
video_speed_page = PageFactory().get_page_object('video_speed_page', mwc)
blending_mode_page = PageFactory().get_page_object('blending_mode_page',mwc)
video_collage_designer_page = PageFactory().get_page_object('video_collage_designer_page', mwc)
library_preview_page = PageFactory().get_page_object('library_preview_page',mwc)
crop_zoom_pan_page = PageFactory().get_page_object('crop_zoom_pan_page',mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page',mwc)



# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Video & Audio in Reverse.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder - Setup for Overall Project
Ground_Truth_Folder = app.ground_truth_root + '/Video_Audio_In_Reverse/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Video_Audio_In_Reverse/'
Test_Material_Folder = app.testing_material

# For Ground Truth / Test Material folder - Setup for Duncan personal testing
# Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/GroundTruth/Title_Room/'
# Auto_Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/ATGroundTruth/Title_Room/'
# Test_Material_Folder = '/Users/cl/Desktop/Duncan/Material/'

DELAY_TIME = 1

class Test_Video_Audio_In_Reverse():
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
            google_sheet_execution_log_init('Video_Audio_In_Reverse')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"test case template result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'),
                               report.get_ovinfo('duration'))
        report.show()

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        with uuid("9ef44749-2a30-45ef-bdf3-f36702ede088") as case:
            # 1.1.1 Entry Point - Select Video in Timeline - Tip Area > Tools - Video in Reverse
            # Context menu is unchecked as default
            time.sleep(5)
            # Import one video into timeline
            main_page.insert_media('Skateboard 01.mp4')
            # Verify if option is un-ticked as default
            current_result = tips_area_page.tools.get_select_Video_in_Reverse_status()
            logger(f"{current_result= }")
            case.result = not current_result

        with uuid("46897573-0662-44e8-8be5-aec612115fb3") as case:
            # 1.1.2 Entry Point - Select Video in Timeline - Tip Area > Tools - Audio in Reverse
            # Context menu is unchecked as default
            main_page.click_undo()
            # Import one audio into timeline
            main_page.insert_media('Speaking Out.mp3')
            # Verify if option is un-ticked as default
            current_result = tips_area_page.tools.get_select_Audio_in_Reverse_status()
            logger(f"{current_result= }")
            case.result = not current_result

        with uuid("81ce65b0-5fc8-4e1b-bff5-a6321cbb224b") as case:
            # 2.1.5 Audio in Reverse - Tick it - Apply
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            current_image_audio = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1_Original_Audio.png')
            tips_area_page.tools.select_Audio_in_Reverse()
            # Verify if option is ticked
            current_result = tips_area_page.tools.get_select_Audio_in_Reverse_status()
            logger(f"{current_result= }")
            # snapshot timeline area to verify if adjustment is applied
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1-5_Apply_Audio.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-1-5_Apply_Audio.png', current_image)
            logger(f"{compare_result= }")
            case.result = current_result and compare_result

        with uuid("fe6ebcc8-e426-48a5-bcdd-3396285620a4") as case:
            # 2.1.6 Audio in Reverse - Tick it - Undo
            # Restore to previous clip
            main_page.click_undo()
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1-6_Undo.png')
            compare_result = media_room_page.compare(current_image_audio, current_image, similarity=0.9)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("66ad64d9-db21-48ca-b8e2-224c5adf7df3") as case:
            # 2.1.7 Audio in Reverse - Tick it - Redo
            # Reverse function works correctly
            main_page.click_redo()
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1-7_Redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-1-6_Undo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("184a3b20-a966-4835-a5ac-a119382c38a9") as case:
            # 2.1.8 Audio in Reverse - UnTick it - NOT Apply
            # Reverse function works correctly
            tips_area_page.tools.select_Audio_in_Reverse()
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1-8_NotApply.png')
            compare_result = media_room_page.compare(current_image_audio, current_image, similarity=0.9)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("41cbddef-c0c8-489a-89d5-9da69214a2e9") as case:
            # 2.1.1 Video in Reverse - Tick it - Apply
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            main_page.press_del_key()
            time.sleep(1)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(1)
            current_image_video = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1_Original_Video.png')
            tips_area_page.tools.select_Video_in_Reverse()
            # Verify if option is ticked
            current_result = tips_area_page.tools.get_select_Video_in_Reverse_status()
            logger(f"{current_result= }")
            # snapshot timeline area to verify if adjustment is applied
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1-1_Apply_Video.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-1-1_Apply_Video.png', current_image)
            logger(f"{compare_result= }")
            case.result = current_result and compare_result

        with uuid("e4875114-7ba4-4b17-a685-d201b1993628") as case:
            # 2.1.2 Video in Reverse - Tick it - Undo
            # Restore to previous clip
            main_page.click_undo()
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1-2_Undo.png')
            compare_result = media_room_page.compare(current_image_video, current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("73282eaf-24ef-467f-94ea-a880af940af0") as case:
            # 2.1.3 Video in Reverse - Tick it - Redo
            # Reverse function works correctly
            main_page.click_redo()
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1-3_Redo.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-1-3_Redo.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("5f1dd5b8-bd0d-47c8-8fb8-2c0ae5ad48a6") as case:
            # 2.1.4 Video in Reverse - UnTick it - NOT Apply
            # Reverse function works correctly
            time.sleep(1)
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(1)
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1-4_NotApply.png')
            compare_result = media_room_page.compare(current_image_video, current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("b02cdfad-31fe-45e6-a6c1-0397206c3af9") as case:
            # 3.1.1 Original & Edit Media - Video
            # Original
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            main_page.press_del_key()
            main_page.insert_media('Skateboard 02.mp4')
            main_page.move_mouse_to_0_0()
            current_image_audio = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '3-1-1_Original_Video.png')
            # apply effect twice
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(1)
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(1)
            main_page.move_mouse_to_0_0()
            # snapshot timeline area to verify if result is original
            compare_result = media_room_page.compare(current_image_audio, current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_2_1(self):
        with uuid("74edde4b-4a66-49e7-8133-8b0aa8272187") as case:
            # 3.2.1 Original & Edit Media - Audio
            # Original
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            time.sleep(5)
            main_page.insert_media('Speaking Out.mp3')
            main_page.move_mouse_to_0_0()
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '3-2-1_Original_Audio.png')
            # apply effect twice
            tips_area_page.tools.select_Audio_in_Reverse()
            tips_area_page.tools.select_Audio_in_Reverse()
            main_page.move_mouse_to_0_0()
            # snapshot timeline area to verify if result is original
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-2-1_Original_Audio.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_3_1_2(self):
        with uuid("21805f18-009d-42ad-9190-d16255192910") as case:
            # 3.1.2 Original & Edit Media - Video
            # w/ Preview Updated - w/ Position
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            time.sleep(5)
            # Import one video into timeline
            main_page.insert_media('Skateboard 03.mp4')
            # Adjust in playback window
            playback_window_page.adjust_timeline_preview_on_canvas_arrow_key_move_up(times=2)
            playback_window_page.adjust_timeline_preview_on_canvas_arrow_key_move_left(times=2)
            # apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-2_Position.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-2_Position.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("aa34e444-234c-463a-9a41-9cf0f1be41b6") as case:
            # 3.1.3 Original & Edit Media - Video
            # w/ Preview Updated - w/ Scale
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Reset to default
            main_page.click_undo()
            main_page.click_undo()
            main_page.click_undo()
            main_page.click_undo()
            main_page.click_undo()
            # Adjust in playback window
            playback_window_page.adjust_timeline_preview_on_canvas_resize_to_small()
            # apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-3_Scale.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-3_Scale.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("9439f11b-0442-4d5c-b646-0398b13a7737") as case:
            # 3.1.4 Original & Edit Media - Video
            # w/ Preview Updated - w/ Transform
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Reset to default
            main_page.click_undo()
            main_page.click_undo()
            # Adjust in playback window
            playback_window_page.adjust_timeline_preview_on_canvas_freeform()
            # apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-4_Transform.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-4_Transform.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("d2c56a40-0c3b-421f-8151-59d8391a07d1") as case:
            # 3.1.5 Original & Edit Media - Video
            # w/ Preview Updated - w/ Rotation
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Reset to default
            main_page.click_undo()
            main_page.click_undo()
            # Adjust in playback window
            playback_window_page.adjust_timeline_preview_on_canvas_drag_rotate_clockwise()
            # apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-5_Rotation.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-5_Rotation.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_3_1_6(self):
        with uuid("8ea66ab2-7e1f-4001-847a-9c7c8e63be8c") as case:
            # 3.1.6 Original & Edit Media - Video
            # w/ PiP Designer Applied - w/ Object Settings (All)
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            time.sleep(5)
            main_page.insert_media('Skateboard 02.mp4')
            # Import one Pip into timeline
            main_page.enter_room(4)
            time.sleep(2)
            # enter pip designer
            main_page.select_LibraryRoom_category('General')
            media_room_page.select_media_content('Dialog_06')
            pip_room_page.click_ModifyAttribute_btn('PiP')
            timeline_operation_page.double_click()
            check_in_PiP_result = pip_room_page.check_in_PiP_designer()
            logger(f"{check_in_PiP_result= }")
            # Edit in pip designer
            pip_designer_page.switch_mode('Express')
            pip_designer_page.express_mode.unfold_properties_object_setting_tab(1)
            pip_designer_page.input_position_opacity_value('80')
            pip_designer_page.express_mode.unfold_properties_object_setting_tab(0)
            pip_designer_page.click_ok()
            # Save template then back to pip room
            pip_designer_page.input_template_name_and_click_ok('01_Object_Settings')
            tips_area_page.click_TipsArea_btn_insert(option=3)
            main_page.select_timeline_media('Skateboard 02.mp4')
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            main_page.set_timeline_timecode("00_00_02_00")
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-6_PiP_Object.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-6_PiP_Object.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("630a641a-a4b9-4f35-ac19-362dfc875da2") as case:
            # 3.1.7 Original & Edit Media - Video
            # w/ PiP Designer Applied - w/ Chroma Key
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Reset back to non-pip status
            main_page.click_undo()
            main_page.click_undo()
            pip_room_page.hover_library_media('01_Object_Settings')
            main_page.double_click()
            check_in_PiP_result = pip_room_page.check_in_PiP_designer()
            logger(f"{check_in_PiP_result= }")
            # Edit in pip designer
            pip_designer_page.express_mode.unfold_properties_chroma_key_tab(1)
            pip_designer_page.express_mode.set_check_chromakey(1)
            pip_designer_page.exist_click(L.pip_designer.chromakey.btn_dropper)
            pip_designer_page.exist_click(L.pip_designer.preview)
            pip_designer_page.express_mode.unfold_properties_chroma_key_tab(0)
            pip_designer_page.click_ok()
            # Import edited pip into timeline
            tips_area_page.click_TipsArea_btn_insert(option=3)
            main_page.select_timeline_media('Skateboard 02.mp4')
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            main_page.set_timeline_timecode("00_00_02_00")
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-7_PiP_Chroma.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-7_PiP_Chroma.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("218e8b3c-e79e-4d50-8d19-21e8d19a16e1") as case:
            # 3.1.8 Original & Edit Media - Video
            # w/ PiP Designer Applied - w/ border
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Reset back to non-pip status
            main_page.click_undo()
            main_page.click_undo()
            pip_room_page.hover_library_media('01_Object_Settings')
            main_page.double_click()
            check_in_PiP_result = pip_room_page.check_in_PiP_designer()
            logger(f"{check_in_PiP_result= }")
            # Edit in pip designer
            pip_designer_page.express_mode.unfold_properties_border_tab(1)
            pip_designer_page.express_mode.set_border_checkbox(1)
            pip_designer_page.express_mode.drag_border_size_slider('9')
            pip_designer_page.express_mode.unfold_properties_border_tab(0)
            pip_designer_page.click_ok()
            # Import edited pip into timeline
            tips_area_page.click_TipsArea_btn_insert(option=3)
            main_page.select_timeline_media('Skateboard 02.mp4')
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            main_page.set_timeline_timecode("00_00_02_00")
            time.sleep(DELAY_TIME*2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-8_PiP_Border.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-8_PiP_Border.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("ab49e72b-3226-48d7-9912-678a121372b1") as case:
            # 3.1.9 Original & Edit Media - Video
            # w/ PiP Designer Applied - w/ shadow
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Reset back to non-pip status
            main_page.click_undo()
            main_page.click_undo()
            pip_room_page.hover_library_media('01_Object_Settings')
            main_page.double_click()
            check_in_PiP_result = pip_room_page.check_in_PiP_designer()
            logger(f"{check_in_PiP_result= }")
            # Edit in pip designer
            pip_designer_page.express_mode.unfold_properties_shadow_tab(1)
            pip_designer_page.express_mode.set_shadow_checkbox(1)
            pip_designer_page.express_mode.input_shadow_distance_value('100')
            pip_designer_page.express_mode.unfold_properties_shadow_tab(0)
            pip_designer_page.click_ok()
            # Import edited pip into timeline
            tips_area_page.click_TipsArea_btn_insert(option=3)
            main_page.select_timeline_media('Skateboard 02.mp4')
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            main_page.set_timeline_timecode("00_00_02_00")
            time.sleep(DELAY_TIME*2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-9_PiP_Shadow.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-9_PiP_Shadow.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("cc79e6ca-e75d-467e-9ed0-2f478c176c4e") as case:
            # 3.1.10 Original & Edit Media - Video
            # w/ PiP Designer Applied - w/ Flip
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Reset back to non-pip status
            main_page.click_undo()
            main_page.click_undo()
            pip_room_page.hover_library_media('01_Object_Settings')
            main_page.double_click()
            check_in_PiP_result = pip_room_page.check_in_PiP_designer()
            logger(f"{check_in_PiP_result= }")
            # Edit in pip designer
            pip_designer_page.apply_flip(1)
            pip_designer_page.click_ok()
            # Import edited pip into timeline
            tips_area_page.click_TipsArea_btn_insert(option=3)
            main_page.select_timeline_media('Skateboard 02.mp4')
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            main_page.set_timeline_timecode("00_00_02_00")
            time.sleep(DELAY_TIME*2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-10_PiP_Flip.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-10_PiP_Flip.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("54e0b15a-0d7a-4e92-9d98-7b069750df94") as case:
            # 3.1.11 Original & Edit Media - Video
            # w/ PiP Designer Applied - w/ Fades
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Reset back to non-pip status
            main_page.click_undo()
            main_page.click_undo()
            pip_room_page.hover_library_media('01_Object_Settings')
            main_page.double_click()
            check_in_PiP_result = pip_room_page.check_in_PiP_designer()
            logger(f"{check_in_PiP_result= }")
            # Edit in pip designer
            pip_designer_page.express_mode.unfold_properties_fades_tab(0, 1)
            pip_designer_page.express_mode.set_enable_fade_in_checkbox(1)
            pip_designer_page.click_ok()
            # Import edited pip into timeline
            tips_area_page.click_TipsArea_btn_insert(option=3)
            main_page.select_timeline_media('Skateboard 02.mp4')
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            main_page.set_timeline_timecode("00_00_01_00")
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-11_PiP_Fades.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-11_PiP_Fades.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_3_1_12(self):
        with uuid("da9d683f-9e19-4523-a327-e4d1f68681bb") as case:
            # 3.1.12 Original & Edit Media - Video
            # w/ Mask Designer Applied - w/ Default Mask
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            time.sleep(5)
            main_page.insert_media('Skateboard 03.mp4')
            # enter mask designer
            tips_area_page.tools.select_Mask_Designer()
            # Verify if enter mask designer
            is_in_mask_designer = mask_designer_page.exist(L.mask_designer.mask_property.category)
            logger(f"{is_in_mask_designer= }")
            # Apply default mask
            mask_designer_page.MaskDesigner_Apply_template(5)
            mask_designer_page.Edit_MaskDesigner_ClickOK()
            main_page.select_timeline_media('Skateboard 03.mp4')
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-12_Mask_Default.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-12_Mask_Default.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("3c4008f2-8336-431b-a686-60a4524b9850") as case:
            # 3.1.13 Original & Edit Media - Video
            # w/ Mask Designer Applied - w/ Customized Mask
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Reset back to non-mask status
            main_page.click_undo()
            main_page.click_undo()
            # enter mask designer
            tips_area_page.tools.select_Mask_Designer()
            # Apply customize mask
            mask_designer_page.Edit_MaskDesigner_CreateImageMask(Test_Material_Folder + 'Video_Audio_In_Reverse/Sample.png')
            mask_designer_page.MaskDesigner_Select_Mask_Alpha_Channel(option=1)
            mask_designer_page.Edit_MaskDesigner_ClickOK()
            time.sleep(1)
            main_page.select_timeline_media('Skateboard 03.mp4')
            time.sleep(1)
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-13_Mask_Default.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-13_Mask_Default.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("170b7e44-b47f-43ef-af06-45a4d4acc998") as case:
            # 3.1.14 Original & Edit Media - Video
            # w/ Mask Designer Applied - w/ Invert Mask
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # enter mask designer
            tips_area_page.tools.select_Mask_Designer()
            # Apply invert mask
            mask_designer_page.Edit_MaskDesigner_Invert_mask_SetCheck(check=True)
            mask_designer_page.Edit_MaskDesigner_ClickOK()
            main_page.select_timeline_media('Skateboard 03.mp4')
            time.sleep(1)
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-14_Invert_Mask.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-14_Invert_Mask.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("9e8ba353-4839-4341-bb4d-4a689ee288f8") as case:
            # 3.1.19 Original & Edit Media - Video
            # w/ Video Speed Applied - w/ Entire Clip
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            tips_area_page.tools.select_VideoSpeed()
            video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_DragSlider(0.9)
            video_speed_page.Edit_VideoSpeedDesigner_ClickOK()
            time.sleep(1)
            main_page.select_timeline_media('Skateboard 03.mp4')
            time.sleep(1)
            main_page.set_timeline_timecode("00_00_01_00")
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-19_VideoSpeed_Entire.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-19_VideoSpeed_Entire.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("1497aab9-8dd9-4f23-bcbf-1807b5bb510b") as case:
            # 3.1.20 Original & Edit Media - Video
            # w/ Video Speed Applied - w/ Selected Range
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            main_page.click_undo()
            tips_area_page.tools.select_VideoSpeed()
            video_speed_page.Edit_VideoSpeedDesigner_SelectTab('Selected Range')
            video_speed_page.VideoSpeedDesigner_SelectRange_Click_Upper_CreateTimeShift_btn()
            video_speed_page.Edit_VideoSpeedDesigner_SelectRange_Duration_SetValue('00_00_02_16')
            video_speed_page.Edit_VideoSpeedDesigner_ClickOK()
            time.sleep(1)
            main_page.select_timeline_media('Skateboard 03.mp4')
            time.sleep(1)
            main_page.set_timeline_timecode("00_00_01_00")
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-20_VideoSpeed_SelectedRange.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-20_VideoSpeed_SelectedRange.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("55c13340-21c2-4c44-8188-2a290571f050") as case:
            # 3.1.21 Original & Edit Media - Video
            # w/ Blending Mode Applied
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            main_page.click_undo()
            main_page.click_undo()
            main_page.click_undo()
            # Select video clip to enter blending mode
            main_page.select_timeline_media('Skateboard 03.mp4')
            tips_area_page.tools.select_Blending_Mode()
            blending_mode_page.set_blending_mode('Overlay')
            blending_mode_page.click_ok()
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-21_Blending.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-21_Blending.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_3_1_26(self):
        with uuid("30eecad7-3edd-40a4-b654-fe08701c6ea5") as case:
            # 3.1.26 Original & Edit Media - Video
            # w/ Context Menu Applied - w/ Overwrite
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            time.sleep(5)
            # enlarge timeline
            timeline_operation_page.timeline_click_zoomin_btn()
            # Import one photo into timeline and move position
            main_page.insert_media('Skateboard 01.mp4')
            main_page.select_timeline_media('Skateboard 01.mp4')
            # Move clip to right side
            timeline_operation_page.drag_single_media_move_to(0, 0, 100)
            main_page.select_timeline_media('Skateboard 01.mp4')
            media_room_page.select_media_content('Skateboard 02.mp4')
            tips_area_page.click_TipsArea_btn_insert(option=0)  # 0-Overwrite
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode("00_00_03_15")
            time.sleep(DELAY_TIME*2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-26_Overwrite.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-26_Overwrite.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("2f4ac252-060d-4d6c-8905-f16e0c93247c") as case:
            # 3.1.27 Original & Edit Media - Video
            # w/ Context Menu Applied - w/ Trim to Fit
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            main_page.select_timeline_media('Skateboard 01.mp4')
            tips_area_page.more_features.copy()
            tips_area_page.more_features.paste(option='Trim')
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(DELAY_TIME * 2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel,  file_name=Auto_Ground_Truth_Folder + '3-1-27_Trim.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-27_Trim.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("dc871d4a-cefe-43ef-b3ae-d0fde7c5baae") as case:
            # 3.1.28 Original & Edit Media - Video
            # w/ Context Menu Applied - w/ Speed up to Fit
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            main_page.select_timeline_media('Skateboard 01.mp4')
            tips_area_page.more_features.paste(option='Speed')
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(DELAY_TIME * 2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-28_Speed.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-28_Speed.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("6c56dc7b-d626-4051-bff0-d1c75708881b") as case:
            # 3.1.29 Original & Edit Media - Video
            # w/ Context Menu Applied - w/ Insert
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            main_page.select_timeline_media('Skateboard 01.mp4')
            tips_area_page.more_features.paste(option='Insert')
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(DELAY_TIME * 2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel,  file_name=Auto_Ground_Truth_Folder + '3-1-29_Insert.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-29_Insert.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("dbfdb5e8-bb7b-4346-b58f-ce8ecd959b4c") as case:
            # 3.1.30 Original & Edit Media - Video
            # w/ Context Menu Applied - w/ Insert and Move All Clips
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            main_page.select_timeline_media('Skateboard 01.mp4')
            media_room_page.select_media_content('Skateboard 02.mp4')
            tips_area_page.click_TipsArea_btn_insert(option=2)  # 2-insert_and_move_all_clips
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode("00_00_05_06")
            time.sleep(DELAY_TIME*2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-30_MoveAll.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-30_MoveAll.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("eaedb4a9-8ecb-439e-8cc3-28c9533a7367") as case:
            # 3.1.31 Original & Edit Media - Video
            # w/ Context Menu Applied - w/ Crossfade
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            media_room_page.select_media_content('Skateboard 02.mp4')
            tips_area_page.click_TipsArea_btn_insert(option=3)  # 3-CrossFade
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode("00_00_02_29")
            time.sleep(DELAY_TIME*2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-31_Crossfade.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-31_Crossfade.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("bbafbe16-42a0-442c-9f7b-cc7192f31d30") as case:
            # 3.1.32 Original & Edit Media - Video
            # w/ Context Menu Applied - w/ Replace
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            media_room_page.select_media_content('Skateboard 02.mp4')
            tips_area_page.click_TipsArea_btn_insert(option=4)  # 4-Replace
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            # Snapshot library preview result to verify
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode("00_00_09_28")
            time.sleep(DELAY_TIME*2)
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-32_Replace.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-32_Replace.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_1_33(self):
        with uuid("9c407082-22ac-4f95-9df3-6be86e856a07") as case:
            # 3.1.33 Original & Edit Media - Video
            # w/ Effect Applied - w/ Style Effect
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            time.sleep(5)
            main_page.insert_media('Skateboard 01.mp4')
            # enlarge timeline
            timeline_operation_page.timeline_click_zoomin_btn()
            # Enter effect room
            main_page.enter_room(3)
            time.sleep(2)
            # Apply one style effect
            effect_room_page.search_and_input_text('pop')
            main_page.drag_media_to_timeline_playhead_position('Pop Art Wall')
            # Apply in reverse
            main_page.set_timeline_timecode("00_00_02_00")
            tips_area_page.tools.select_Video_in_Reverse()
            playback_window_page.Edit_Timeline_PreviewOperation('Previous_Frame')
            playback_window_page.Edit_Timeline_PreviewOperation('Next_Frame')
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-33_StyleEffect.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-33_StyleEffect.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("fc83ba15-d2f9-4311-a207-7058b8e7a398") as case:
            # 3.1.34 Original & Edit Media - Video
            # w/ Effect Applied - w/ Color LUT
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            time.sleep(2)
            effect_room_page.import_CLUTs(app.testing_material + '/Video_Audio_In_Reverse/m3d.m3d')
            main_page.drag_media_to_timeline_playhead_position('m3d')
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            main_page.set_timeline_timecode("00_00_03_00")
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-34_CLUT.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-34_CLUT.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0b1fedc5-cacd-4a99-bc9d-5c6a34121a25") as case:
            # 3.1.35 Original & Edit Media - Video
            # w/ Effect Applied - w/ Blending Effect
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            effect_room_page.select_specific_tag('Blending Effect')
            main_page.drag_media_to_timeline_playhead_position('Analog Film')
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            main_page.set_timeline_timecode("00_00_04_00")
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-35_Blending.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-35_Blending.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("1d043aac-80bf-4133-9df3-d49fe914df6f") as case:
            # 3.1.36 Original & Edit Media - Video
            # w/ Split Applied
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            main_page.select_timeline_media('Skateboard 01.mp4')
            main_page.set_timeline_timecode("00_00_04_00")
            main_page.tap_Split_hotkey()
            time.sleep(1)
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-36_Split.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-36_Split.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("b4422729-acb1-4cf5-84f6-8c9d710ba7c5") as case:
            # 3.1.37 Original & Edit Media - Video
            # w/ Trim Applied - w/ Single Trim
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            main_page.select_timeline_media('Skateboard 01.mp4')
            main_page.tap_Trim_hotkey()
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 1, 0)
            time.sleep(1)
            precut_page.tap_single_trim_mark_in()
            time.sleep(1)
            precut_page.click_ok()
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-37_Single.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-37_Single.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0e5d7fbf-226e-4bc1-be73-d57437783604") as case:
            # 3.1.38 Original & Edit Media - Video
            # w/ Trim Applied w/ Multiple Trim
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            main_page.select_timeline_media('Skateboard 01.mp4')
            main_page.tap_Trim_hotkey()
            precut_page.edit_precut_switch_trim_mode('Multi')
            # Drag slider
            precut_page.drag_multi_trim_slider(0, 0, 1, 0)
            precut_page.tap_multi_trim_mark_in()
            precut_page.drag_multi_trim_slider(0, 0, 3, 0)
            precut_page.tap_multi_trim_mark_out()
            precut_page.tap_multi_trim_mark_in()
            time.sleep(1)
            precut_page.click_ok()
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-38_Multi.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-38_Multi.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("a456a42f-d43a-43be-a66a-c464b76d6664") as case:
            # 3.1.39 Original & Edit Media - Video
            # w/ Length Adjusted via drag
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            time.sleep(1)
            main_page.click_undo()
            time.sleep(1)
            main_page.select_timeline_media('Skateboard 01.mp4')
            timeline_operation_page.drag_timeline_clip(mode = 'Last', ratio = 0.5, track_index1 = 0, clip_index1 = 0, track_index2 = None, clip_index2 = None)
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-39_Drag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-39_Drag.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_1_40(self):
        with uuid("e77de85e-387f-4624-afda-cecc2b209ee4") as case:
            # 3.1.40 Original & Edit Media - Video
            # w/ Fix & Enhance Applied - w/ White Balance
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            time.sleep(5)
            main_page.insert_media('Skateboard 01.mp4')
            # enlarge timeline
            timeline_operation_page.timeline_click_zoomin_btn()
            # Enter Fix enhance page
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            fix_enhance_page.fix.enable_white_balance()
            fix_enhance_page.fix.white_balance.color_temperature.set_value(30)
            fix_enhance_page.fix.white_balance.tint.set_value(90)
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-40_Fix_WB.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-40_Fix_WB.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("d58f50ca-15ba-4272-b070-9b09789d8d1e") as case:
            # 3.1.41 Original & Edit Media - Video
            # w/ Fix & Enhance Applied - w/ Lens Correction
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Click Reset button
            fix_enhance_page.click_reset()
            # Tick lens correction option - GoPro HERO7 Black (Wide)
            fix_enhance_page.fix.enable_lens_correction()
            fix_enhance_page.fix.lens_correction.select_marker_type('GoPro')
            fix_enhance_page.fix.lens_correction.select_model_type(18)
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-41_Fix_Lens.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-41_Fix_Lens.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("8b889f34-24ad-48db-a416-e0fe0a3e8204") as case:
            # 3.1.42 Original & Edit Media - Video
            # w/ Fix & Enhance Applied - w/ Audio Denoise
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Click Reset button
            fix_enhance_page.click_reset()
            # Tick audio denoise option
            fix_enhance_page.fix.enable_audio_denoise()
            # Check if switch to "Stationary noise" noise type
            # 1=Stationary noise, 2=Wind noise, 3=Clicking noise
            fix_enhance_page.fix.audio_denoise.set_noise_type(0)
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse(skip=1)
            time.sleep(2)
            # Snapshot timeline preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '3-1-42_Fix_Audio.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-42_Fix_Audio.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("6e1d0bed-9757-4196-ab24-2e851390d690") as case:
            # 3.1.43 Original & Edit Media - Video
            # w/ Fix & Enhance Applied - w/ Color Adjustment
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Click Reset button
            fix_enhance_page.click_reset()
            # Tick color adjustment option
            fix_enhance_page.enhance.switch_to_color_adjustment()
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(10)
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.base.Area.preview.only_mtk_view, file_name=Auto_Ground_Truth_Folder + '3-1-43_Fix_Color.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-43_Fix_Color.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_1_44(self):
        with uuid("e46a9e85-c239-449d-a8b9-7df4bcfaf059") as case:
            # 3.1.44 Original & Edit Media - Video
            # w/ Keyframe Applied - w/ Auto Denoise
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            time.sleep(5)
            main_page.insert_media('Skateboard 01.mp4')
            # enlarge timeline
            timeline_operation_page.timeline_click_zoomin_btn()
            timeline_operation_page.timeline_click_zoomin_btn()
            # Enter keyframe room
            tips_area_page.click_keyframe()
            # Change timecode
            library_preview_page.set_library_preview_window_timecode('00_00_04_00')
            # Change setting for Audio Denoise
            keyframe_room_page.fix_enhance.unfold_tab(value=1)
            unfold_fix_enhance = keyframe_room_page.fix_enhance.show()
            logger(f"{unfold_fix_enhance= }")
            keyframe_room_page.drag_scroll_bar(0.22)
            keyframe_room_page.fix_enhance.audio_denoise.unfold_tab(value=1)
            keyframe_room_page.fix_enhance.audio_denoise.show()
            keyframe_room_page.fix_enhance.audio_denoise.noise.set_type(2)
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot timeline preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '3-1-44_Keyframe_Denoise.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-44_Keyframe_Denoise.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("b15e2a4b-65c5-4869-9cc8-c4708c6361c9") as case:
            # 3.1.45 Original & Edit Media - Video
            # w/ Keyframe Applied - w/ Color Adjustment
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            # set exposure of the current keyframe by slider
            keyframe_room_page.fix_enhance.color_adjustment.exposure.show()
            keyframe_room_page.fix_enhance.color_adjustment.exposure.set_slider(30)
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot timeline preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.base.Area.preview.only_mtk_view, file_name=Auto_Ground_Truth_Folder + '3-1-45_Keyframe_Color.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-45_Keyframe_Color.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("3845e993-2ab5-4f9a-a1dd-111ea0be3854") as case:
            # 3.1.46 Original & Edit Media - Video
            # w/ Keyframe Applied - w/ White Balance
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            # set WB of the current keyframe by slider
            keyframe_room_page.fix_enhance.white_balance.show()
            keyframe_room_page.fix_enhance.white_balance.color_temperature.show()
            keyframe_room_page.fix_enhance.white_balance.select_color_temperature()
            keyframe_room_page.fix_enhance.white_balance.color_temperature.set_slider(70)
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot timeline preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-46_Keyframe_WB.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-46_Keyframe_WB.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("61e15ea7-fa84-4feb-9a3a-0e3895e77349") as case:
            # 3.1.47 Original & Edit Media - Video
            # w/ Keyframe Applied - w/ Clip Attributes (All)
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            # set set x position of the current keyframe
            keyframe_room_page.clip_attributes.unfold_tab(value=1)
            keyframe_room_page.clip_attributes.position.x.set_value(value='0.2')  # keyframe 00;00;00;00
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot timeline preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-1-47_Keyframe_Attributes.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-47_Keyframe_Attributes.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("71b4ac3c-c054-434e-a7e1-4538cdabb4e7") as case:
            # 3.1.48 Original & Edit Media - Video
            # w/ Keyframe Applied - w/ Volume
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            # set volume of the current keyframe
            keyframe_room_page.volume.show()
            keyframe_room_page.volume.set_slider(value=80)
            # Apply in reverse
            tips_area_page.tools.select_Video_in_Reverse()
            time.sleep(2)
            # Snapshot timeline preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '3-1-48_Keyframe_Volume.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-1-48_Keyframe_Volume.png',  current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_2_7(self):
        with uuid("7769222c-dd69-4bc5-bc96-fd7bfaec4126") as case:
            # 3.2.7 Original & Edit Media - Audio
            # w/ Context Menu Applied - w/ Overwrite
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            time.sleep(5)
            # Import one audio into timeline and move position
            main_page.insert_media('Mahoroba.mp3')
            main_page.select_timeline_media('Mahoroba.mp3')
            timeline_operation_page.drag_single_audio_move_to(1, 0, 200)
            # Move clip to right side
            media_room_page.select_media_content('Speaking Out.mp3')
            tips_area_page.click_TipsArea_btn_insert(option=0)  # 0-Overwrite
            # Apply in reverse
            tips_area_page.tools.select_Audio_in_Reverse()
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-2-7_Overwrite.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-2-7_Overwrite.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("4a81599e-26cf-4658-aa15-5c95f3582b8d") as case:
            # 3.2.8 Original & Edit Media - Audio
            # w/ Context Menu Applied - w/ Trim to Fit
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            main_page.select_timeline_media('Mahoroba.mp3')
            tips_area_page.more_features.copy()
            tips_area_page.more_features.paste(option='Trim')
            # Apply in reverse
            tips_area_page.tools.select_Audio_in_Reverse()
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-2-8_Trim.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-2-8_Trim.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("ef9336f4-9fab-4b19-b10b-685c4f439df5") as case:
            # 3.2.9 Original & Edit Media - Audio
            # w/ Context Menu Applied - w/ Speed up to Fit
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            main_page.select_timeline_media('Mahoroba.mp3')
            tips_area_page.more_features.paste(option='Speed')
            # Apply in reverse
            tips_area_page.tools.select_Audio_in_Reverse()
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-2-9_Speed.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-2-9_Speed.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("9012898c-ad2b-47c2-95f7-18d31127b0ef") as case:
            # 3.2.10 Original & Edit Media - Audio
            # w/ Context Menu Applied - w/ Insert
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            main_page.select_timeline_media('Mahoroba.mp3')
            tips_area_page.more_features.paste(option='Insert')
            # Apply in reverse
            tips_area_page.tools.select_Audio_in_Reverse()
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-2-10_Insert.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-2-10_Insert.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("35c3b8b4-15c9-420a-8e28-c6ee312ea095") as case:
            # 3.2.11 Original & Edit Media - Audio
            # w/ Context Menu Applied - w/ Insert and Move All Clips
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            media_room_page.select_media_content('Speaking Out.mp3')
            tips_area_page.click_TipsArea_btn_insert(option=2)  # 2-insert_and_move_all_clips
            # Apply in reverse
            tips_area_page.tools.select_Audio_in_Reverse()
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-2-11_MoveAll.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-2-11_MoveAll.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("a8a5029b-94ef-4188-9d5a-4355bee191d4") as case:
            # 3.2.12 Original & Edit Media - Video
            # w/ Context Menu Applied - w/ Crossfade
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            media_room_page.select_media_content('Speaking Out.mp3')
            tips_area_page.click_TipsArea_btn_insert(option=3)  # 3-CrossFade
            # Apply in reverse
            tips_area_page.tools.select_Audio_in_Reverse()
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-2-12_Crossfade.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-2-12_Crossfade.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("51d563f0-ff39-4c3a-9863-6a329d397e9b") as case:
            # 3.2.13 Original & Edit Media - Video
            # w/ Context Menu Applied - w/ Replace
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            media_room_page.select_media_content('Speaking Out.mp3')
            tips_area_page.click_TipsArea_btn_insert(option=4)  # 4-Replace
            # Apply in reverse
            tips_area_page.tools.select_Audio_in_Reverse()
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-2-13_Replace.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-2-13_Replace.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("31609e5f-6874-48bc-a4a2-3eae67bbbabd") as case:
            # 3.2.14 Original & Edit Media - Audio
            # w/ Split Applied
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            main_page.select_timeline_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 1.5)
            main_page.set_timeline_timecode("00_00_04_00")
            time.sleep(DELAY_TIME)
            main_page.tap_Split_hotkey()
            time.sleep(1)
            # Apply in reverse
            tips_area_page.tools.select_Audio_in_Reverse()
            time.sleep(DELAY_TIME)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-2-14_Split.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-2-14_Split.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("fa77eb82-1729-4f9b-82fa-2ee8d7a7b005") as case:
            # 3.2.16 Original & Edit Media - Audio
            # w/ Length Adjusted via drag
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            time.sleep(DELAY_TIME)
            main_page.click_undo()
            time.sleep(DELAY_TIME)
            main_page.select_timeline_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME)
            timeline_operation_page.drag_timeline_clip(mode='Last', ratio=0.8, track_index1=1, clip_index1=0, track_index2=None, clip_index2=None)

            # Apply in reverse
            tips_area_page.tools.select_Audio_in_Reverse()
            time.sleep(DELAY_TIME*2)
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-2-16_Drag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-2-16_Drag.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("aac520f0-73f3-4a9a-869f-a20f33865f84") as case:
            # 3.2.17 Original & Edit Media - Audio
            # w/ Fix & Enhance Applied - w/ Audio Denoise
            # Undo twice to reset adjustment and reverse
            main_page.click_undo()
            main_page.click_undo()
            main_page.select_timeline_media('Mahoroba.mp3')
            # Enter Fix enhance page
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            fix_enhance_page.fix.enable_audio_denoise()
            fix_enhance_page.fix.audio_denoise.set_noise_type(1)
            fix_enhance_page.fix.audio_denoise.degree.adjust_slider(55)
            # Apply in reverse
            tips_area_page.tools.select_Audio_in_Reverse()
            # Snapshot library preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '3-2-17_Fix_Enhance.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-2-17_Fix_Enhance.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("a4f9757e-acd6-46b8-917b-8d8ef77126ce") as case:
            # 3.2.18 Original & Edit Media - Audio
            # w/ Fix & Enhance Applied - w/ Audio Denoise
            # Click Reset button
            fix_enhance_page.click_reset()
            # Enter keyframe room
            tips_area_page.click_keyframe()
            # Change setting for Audio Denoise
            keyframe_room_page.fix_enhance.unfold_tab(value=1)
            unfold_fix_enhance = keyframe_room_page.fix_enhance.show()
            logger(f"{unfold_fix_enhance= }")
            keyframe_room_page.fix_enhance.audio_denoise.unfold_tab(value=1)
            keyframe_room_page.fix_enhance.audio_denoise.show()
            keyframe_room_page.fix_enhance.audio_denoise.noise.set_type(2)
            # Apply in reverse
            tips_area_page.tools.select_Audio_in_Reverse()
            # Snapshot timeline preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '3-2-18_Keyframe_Denoise.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-2-18_Keyframe_Denoise.png',  current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("cdd77a4c-e7d9-4e83-84e3-3a591e1f11ce") as case:
            # 3.2.19 Original & Edit Media - Audio
            # w/ Keyframe Applied - w/ Volume
            # [i] button and Info tip displays correctly, context menu is checked & reverse waveform and playback works correctly
            # Click Reset button
            fix_enhance_page.click_reset()
            # set volume of the current keyframe
            keyframe_room_page.volume.show()
            keyframe_room_page.volume.set_slider(value=90)
            # Apply in reverse
            tips_area_page.tools.select_Audio_in_Reverse()
            # Snapshot timeline preview result to verify
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '3-2-19_Keyframe_Volume.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '3-2-19_Keyframe_Volume.png',  current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    ################
    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    # 2.1.22 (Audio Editor)
                    b585e12e-3ee9-47e2-9b4f-9c5c88db812c
                    297e5a89-ed10-44d2-9fc8-4206e067735f
                    7764e069-c9c0-4e9c-9375-5358690550cc
                    bf44bc7a-042b-4a80-a361-75142df8ba3c
                    # 3.1.49 ~ 3.1.61
                    67726a05-0977-41cb-9809-3c8743efc142
                    dc15fe42-9830-40fa-873f-4ef47064ce6e
                    fb667cab-b32a-4bde-901b-2960250125c5
                    0a868839-a669-4706-94bf-e4a9c8ba8da7
                    04541223-4f3c-4388-afcc-9a914e7aeaf6
                    0e0df5ff-fb34-425c-acd8-bb5c5b127ed5
                    1fdfd920-6f7c-42f8-a958-3afe02703c70
                    52e69439-2024-499e-9af8-7ed7f20796d4
                    8db7b53d-2cfa-4535-9dc5-9d621930b74f
                    d2d6b5d1-0796-4c6a-9eb4-9d78923b8a85
                    9c652f3e-8164-4360-96a7-7f052e3f694b
                    1d5a368b-5e54-4b9d-bdf7-ddf287a55b9f
                    # 3.2.2 ~ 3.2.5
                    7cfc687f-40e7-437e-bb76-d195d80daac6
                    f2052142-4afb-4a47-a1ae-ea3deba1a6ad
                    6ea447df-df00-45a4-a7f5-039eaa601b6e
                    aa70a00c-dd10-4d0b-b573-ee26a9d3865c
                    3f00ac6c-a7bb-470f-8ac2-24a5870fd876                    
                    # 3.2.15
                    e50b9cfa-4556-41f5-8e60-8acd8c67dd21                   
                    # 3.2.20 ~ 3.2.31
                    47f0d21b-2134-4e91-9a9d-0e789ffa3f50
                    3721cd84-1167-40c0-822f-ef43977eef2b
                    2195c425-707c-48b1-909e-c85058ac25b8
                    d4cfc654-05e6-4f33-8fa3-adcf588d51dc
                    acc70219-4f14-4b62-8722-5a57e1ecde48
                    abcfc2be-30e1-4b51-a817-80df9fb5bcbc
                    f383396d-2ede-48c1-9a79-878c865da294
                    3c81803c-6f60-4229-85a8-55a0371f0ec1
                    88e9f016-6d80-42b7-a81d-447766b1257a
                    66cfae1c-5a32-45f9-9bd4-f9e6e6b85f80
                    fdf1fa83-2546-494c-bdb5-4800cae45b81
                    27b594b4-35e7-4d3b-93a0-c026658b8afe
                    # 4.1
                    81727919-3074-483a-9d81-27aa0c07db94
                    fa7c693b-6957-4df1-8248-c648393f48da
                    98299ca5-2905-4711-81d1-a9622de4ead7
                    # 5.1 ~ 5.3
                    5e601fac-a2dd-4d3a-93f1-252d32919494
                    95dfd121-8687-4f56-a35d-abe0cb24efbb
                    315df7b4-8218-4592-9cd2-bb9d9cccb441
                    b6149e6f-a35f-4481-b814-40487c116568
                    01a70f2f-78e2-4d2f-a5c2-fcab02fbc0f5
                    dafac63b-c5ca-4c85-9471-936017ddc1d9
                    85cc41ca-04b8-4fd1-a45c-463048a3d776
                    aa1422ed-10ad-4650-b56f-a3431f3bb818
                    a582d503-e18c-47f4-ac60-a64f610dd06d
                    ce8e5fc0-3e77-451f-b4f4-58c83ae3e86d
                    3c5ef235-17b6-4733-a249-3a42c88a07d0
                    ae703cc1-683e-47e3-bcdd-a73137f24ebb
                    247a8834-1972-4e7a-9eb7-4dd5786b66f3
                    1687c006-7ee7-4684-8341-1c98dfa466f4
                    afe2d5dc-e401-4267-b1d3-3a5d44cab64d
                    28eef22c-b57f-4a92-b669-9d5344d68578
                    0ebe6c30-8ba2-4bb4-b4fa-da655632d77f
                    357baaac-6eeb-43e5-9dcd-f343ee622758
                    037132a2-4472-4671-ac8e-d1634f51ef6e
                    362710c9-f854-4745-83cd-700ad1bb9533
                    0e0109bb-145c-4bc4-bd63-a53624e6a2d8
                    e4ed5d3d-ab7d-4e95-8db8-6bb84eb945d4
                    80b7f9e4-a51f-4208-bd7a-4512a87ceb81
                    6ba67000-9b42-43ed-a477-ff4008e7ca74
                    6c664874-ef94-4ae0-8a79-a63321891f56
                    8fa28852-4332-47a8-a39e-77c8792c8d4f
                    
                ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"