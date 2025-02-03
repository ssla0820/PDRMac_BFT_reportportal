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
keyframe_room_page = PageFactory().get_page_object('keyframe_room_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
effect_room_page = PageFactory().get_page_object('effect_room_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)
fix_enhance_page = PageFactory().get_page_object('fix_enhance_page', mwc)
library_preview_page = PageFactory().get_page_object('library_preview_page', mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Keyframe Room.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Keyframe_Room/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Keyframe_Room/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Keyframe_Room():
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
            google_sheet_execution_log_init('Keyframe_Room')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"keyframe room result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number,
                                                     report.get_ovinfo('na'),
                                                     report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()

    @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        with uuid('06eb6716-ec2f-43c4-a33d-6c9430f43d28') as case:
            # 1. General
            # 1.1 Entry Point
            # 1.1.1. Tips Area > Keyframe
            # enter keyframe room
            main_page.insert_media('Skateboard 01.mp4')
            main_page.enter_room(3)
            effect_room_page.hover_library_media('Back Light')
            effect_room_page.right_click()
            effect_room_page.select_right_click_menu('Apply Selected Effect to All Clips on Selected Track')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)

            main_page.tips_area_click_key_frame()
            check_result = keyframe_room_page.is_enter_keyframe_settings()
            case.result = check_result

            keyframe_room_page.click_close()

        with uuid('e79f51ca-c64d-4da3-984a-32820a2bde6a') as case:
            # 1.1 Entry Point
            # 1.1.2. Effect Settings > Keyframe
            # enter keyframe room with effect setting opened
            tips_area_page.click_TipsArea_btn_Modify('Effect', close_win=False)
            effect_room_page.click_keyframe_btn()
            check_result = keyframe_room_page.is_enter_keyframe_settings()
            case.result = check_result

            keyframe_room_page.click_close()

        with uuid('e83820fa-2395-4435-851f-02481ba13738') as case:
            # 1.1 Entry Point
            # 1.1.3. Fix Enhance > Keyframe
            # enter keyframe room with fix/enhance tag opened
            main_page.tips_area_click_fix_enhance()
            fix_enhance_page.click_keyframe()
            check_result = keyframe_room_page.is_enter_keyframe_settings()
            case.result = check_result

            keyframe_room_page.click_close()

        with uuid('8e9c89f8-54c3-41de-86b9-d61309cef753') as case:
            # 1.1 Entry Point
            # 1.1.4. Right click on timeline clip -> Edit Clip Keyframe > Fix/Enhance
            # enter keyframe room with fix/enhance tag opened
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            timeline_operation_page.right_click()
            timeline_operation_page.select_right_click_menu('Edit Clip Keyframe', 'Fix/Enhance')
            check_result = keyframe_room_page.is_enter_keyframe_settings()
            case.result = check_result

            keyframe_room_page.click_close()

        with uuid('12e57657-e767-4e73-863a-4a8c4206f7ae') as case:
            # 1.1 Entry Point
            # 1.1.4. Right click on timeline clip -> Edit Clip Keyframe > Effects
            # enter keyframe room with effect tag opened
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            timeline_operation_page.right_click()
            timeline_operation_page.select_right_click_menu('Edit Clip Keyframe', 'Effects')
            check_result = keyframe_room_page.is_enter_keyframe_settings()
            case.result = check_result

            keyframe_room_page.click_close()

        with uuid('e8f2c058-d1dc-4816-afbd-1ceb615862aa') as case:
            # 1.1 Entry Point
            # 1.1.4. Right click on timeline clip -> Edit Clip Keyframe > Clip Attributes
            # enter keyframe room with clip attributes tag opened
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            timeline_operation_page.right_click()
            timeline_operation_page.select_right_click_menu('Edit Clip Keyframe', 'Clip Attributes')
            check_result = keyframe_room_page.is_enter_keyframe_settings()
            case.result = check_result

            keyframe_room_page.click_close()

        with uuid('9092825d-8519-4179-ac7e-eb475b8c15d2') as case:
            # 1.1 Entry Point
            # 1.1.4. Right click on timeline clip -> Edit Clip Keyframe > Volume
            # enter keyframe room with volume tag opened
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            timeline_operation_page.right_click()
            timeline_operation_page.select_right_click_menu('Edit Clip Keyframe', 'Volume')
            check_result = keyframe_room_page.is_enter_keyframe_settings()
            case.result = check_result

            keyframe_room_page.click_close()

        with uuid('b41d2df7-36e5-485c-8cf9-b14f40ac2f0b') as case:
            # 1.2. Keyframe Room
            # 1.2.1. Thumbnail
            # show the clip thumbnail
            main_page.tips_area_click_key_frame()

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_1_2_1_1.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_1_2_1_1.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.keyframe_room.image_thumbnail, file_name=image_full_path)
            check_result = keyframe_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('2b09873f-ee20-4bf2-b88e-eaf6785902f7') as case:
            # 1.2. Keyframe Room
            # 1.2.2. Duration
            # show the clip duration
            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_1_2_2_1.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_1_2_2_1.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.keyframe_room.main_window, file_name=image_full_path)
            check_result = keyframe_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('3b0d1d5f-7f9f-42b5-9f04-cd51c69aa01d') as case:
            # 1.2. Keyframe Room
            # 1.2.3. Right click menu > Copy
            # copy the keyframe settings of the selected item(s)
            keyframe_room_page.fix_enhance.unfold_tab(value=1)
            keyframe_room_page.fix_enhance.show()
            keyframe_room_page.fix_enhance.color_adjustment.unfold_tab(value=1)
            keyframe_room_page.fix_enhance.color_adjustment.show()
            library_preview_page.set_library_preview_window_timecode('00_00_02_00')
            keyframe_room_page.fix_enhance.color_adjustment.exposure.add_remove_keyframe()
            keyframe_room_page.fix_enhance.color_adjustment.exposure.show()
            keyframe_room_page.fix_enhance.color_adjustment.exposure.set_value(value=50)
            library_preview_page.set_library_preview_window_timecode('00_00_04_00')
            keyframe_room_page.fix_enhance.color_adjustment.exposure.add_remove_keyframe()
            keyframe_room_page.fix_enhance.color_adjustment.exposure.set_value(value=25)
            library_preview_page.set_library_preview_window_timecode('00_00_06_00')
            keyframe_room_page.fix_enhance.color_adjustment.exposure.add_remove_keyframe()
            keyframe_room_page.fix_enhance.color_adjustment.exposure.set_value(value=50)
            library_preview_page.set_library_preview_window_timecode('00_00_08_00')
            keyframe_room_page.fix_enhance.color_adjustment.exposure.add_remove_keyframe()
            keyframe_room_page.fix_enhance.color_adjustment.exposure.set_value(value=25)
            library_preview_page.set_library_preview_window_timecode('00_00_10_00')
            keyframe_room_page.fix_enhance.color_adjustment.exposure.add_remove_keyframe()
            keyframe_room_page.fix_enhance.color_adjustment.exposure.set_value(value=50)
            keyframe_room_page.fix_enhance.unfold_tab(value=0)

            keyframe_room_page.fix_enhance.right_click_menu('Copy')

            keyframe_room_page.right_click(L.keyframe_room.btn_category_fix_enhance)
            check_result = keyframe_room_page.exist({'AXTitle': 'Paste'},
                                                    L.keyframe_room.btn_category_fix_enhance).AXEnabled

            case.result = False if not check_result else True

            keyframe_room_page.click_close()

        with uuid('3c78e2c0-72ac-4944-97e8-fda7894800a3') as case:
            # 1.2. Keyframe Room
            # 1.2.5. Keyframe control > Add current keyframe
            # add current keyframe from this parameter
            case.result = check_result

        with uuid('19a5d3a8-7554-4c6a-a980-bd6aeab0c826') as case:
            # 1.2. Keyframe Room
            # 1.2.7. [x] button
            # close keyframe room
            keyframe_room_page.click_close()

            check_result = keyframe_room_page.is_enter_keyframe_settings()
            case.result = True if not check_result else False

        with uuid('36f44261-14ed-44f9-b82e-6c517b9c1bbc') as case:
            # 1.2. Keyframe Room
            # 1.2.3. Right click menu > Paste
            # paste the keyframe settings to the selected clip
            '''
            main_page.enter_room(0)
            main_page.insert_media('Skateboard 02.mp4')
            # main_page.select_library_icon_view_media('Skateboard 02.mp4')
            # main_page.tips_area_insert_media_to_selected_track(option=1)
            # time.sleep(DELAY_TIME)
            '''
            main_page.tips_area_click_key_frame()
            '''
            # keyframe_room_page.fix_enhance.right_click_menu('Paste')
            '''
            keyframe_room_page.fix_enhance.unfold_tab(value=1)
            keyframe_room_page.fix_enhance.show()
            keyframe_room_page.fix_enhance.color_adjustment.unfold_tab(value=1)
            keyframe_room_page.fix_enhance.color_adjustment.show()
            '''

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_1_2_3_1.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_1_2_3_1.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.keyframe_room.frame_keyframe_panel, file_name=image_full_path)
            check_result = keyframe_room_page.compare(ground_truth, current_preview)
            '''
            case.result = False  # v3303, paste attribute GP, VDE213310-0012

        with uuid('a23fedfa-cb5d-4e61-9fda-611280836a83') as case:
            # 1.2. Keyframe Room
            # 1.2.5. Keyframe control > Select next keyframe
            # select the next keyframe from this parameter
            for number_of_clicks in range(5):
                keyframe_room_page.fix_enhance.color_adjustment.exposure.next_keyframe()

            current_timecode = main_page.exist(L.main.duration_setting_dialog.txt_duration).AXValue
            check_result_1 = False if not current_timecode == '00;00;10;00' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_1_2_5_1.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_1_2_5_1.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.keyframe_room.frame_setting_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('5361395b-b976-4fa0-bb0c-d87d0595cb78') as case:
            # 1.2. Keyframe Room
            # 1.2.5. Keyframe control > Select previous keyframe
            # select the previous keyframe from this parameter
            keyframe_room_page.fix_enhance.color_adjustment.exposure.previous_keyframe()

            current_timecode = main_page.exist(L.main.duration_setting_dialog.txt_duration).AXValue
            check_result_1 = False if not current_timecode == '00;00;08;00' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_1_2_5_2.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_1_2_5_2.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.keyframe_room.frame_setting_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('94190845-2cee-4804-ac5c-68e3d0bb7df9') as case:
            # 1.2. Keyframe Room
            # 1.2.5. Keyframe control > Remove current keyframe
            # remove the current keyframe from this parameter
            keyframe_room_page.fix_enhance.color_adjustment.exposure.add_remove_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_1_2_5_3.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_1_2_5_3.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.keyframe_room.frame_keyframe_panel, file_name=image_full_path)
            check_result = keyframe_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('b1ca6e0c-b7cd-4593-965c-c56032a84971') as case:
            # 1.2. Keyframe Room
            # 1.2.5. Keyframe control > Reset keyframe from this parameter
            # reset all keyframes from this parameter
            keyframe_room_page.fix_enhance.color_adjustment.exposure.reset_keyframe()

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_1_2_5_4.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_1_2_5_4.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.keyframe_room.frame_keyframe_panel, file_name=image_full_path)
            check_result = keyframe_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('51b03edf-cf05-450b-8d9e-3b9c5814e1cb') as case:
            # 1.2. Keyframe Room
            # 1.2.3. Right click menu > Select All
            # select all tags
            keyframe_room_page.fix_enhance.unfold_tab(value=0)
            keyframe_room_page.fix_enhance.right_click_menu('Select All')

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_1_2_3_2.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_1_2_3_2.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.keyframe_room.frame_setting_panel, file_name=image_full_path)
            check_result = keyframe_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('1fd3933e-c4a5-41fb-961e-b8e339c8ad7e') as case:
            # 1.2. Keyframe Room
            # 1.2.6. Sync with Fix / Enhance page
            # fix / enhance page and keyframe room should sync
            main_page.tips_area_click_fix_enhance()
            fix_enhance_page.enhance.switch_to_color_adjustment()
            current_value = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            case.result = False if not current_value == '50' else True

    @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid('3e0d2cb1-123e-429b-98c9-5fc077e2757d') as case:
            # 2.3. Audio Denoise
            # 2.3.1. Noise type > Wind noise
            # denoise the Wind noise
            main_page.insert_media('Skateboard 01.mp4')
            main_page.enter_room(3)
            effect_room_page.hover_library_media('Back Light')
            effect_room_page.right_click()
            effect_room_page.select_right_click_menu('Apply Selected Effect to All Clips on Selected Track')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)

            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.unfold_tab(value=1)
            keyframe_room_page.fix_enhance.show()
            keyframe_room_page.fix_enhance.audio_denoise.unfold_tab(value=1)
            library_preview_page.set_library_preview_window_timecode('00_00_00_00')
            keyframe_room_page.fix_enhance.audio_denoise.show()
            keyframe_room_page.fix_enhance.audio_denoise.noise.set_type(2)

            check_result = keyframe_room_page.fix_enhance.audio_denoise.noise.get_type(index_node=0)
            case.result = False if not check_result == 'Wind noise' else True

        with uuid('63db220f-2bc3-4998-8922-35098ff66f90') as case:
            # 2.3. Audio Denoise
            # 2.3.2. Degree > Slider
            # set audio denoise degree by slider
            keyframe_room_page.fix_enhance.audio_denoise.degree.show()
            keyframe_room_page.fix_enhance.audio_denoise.degree.set_slider(40)

            check_result = keyframe_room_page.fix_enhance.audio_denoise.degree.get_value(index_node=0)
            case.result = False if not check_result == '40' else True

        with uuid('fd1625c0-c0a6-4633-bdd3-def02056019c') as case:
            # 2.5. Color Adjustment
            # 2.5.1. Exposure > Slider
            # set exposure of the current keyframe by slider
            keyframe_room_page.fix_enhance.color_adjustment.exposure.show()
            keyframe_room_page.fix_enhance.color_adjustment.exposure.set_slider(41)

            check_result = keyframe_room_page.fix_enhance.color_adjustment.exposure.get_value(index_node=0)
            case.result = False if not check_result == '41' else True

        with uuid('027118f9-1a4c-4f5b-91db-68bfc98fbdd9') as case:
            # 2.5. Color Adjustment
            # 2.5.2. Brightness > Slider
            # set Brightness of the current keyframe by slider
            keyframe_room_page.fix_enhance.color_adjustment.brightness.show()
            keyframe_room_page.fix_enhance.color_adjustment.brightness.set_slider(42)

            check_result = keyframe_room_page.fix_enhance.color_adjustment.brightness.get_value(index_node=0)
            case.result = False if not check_result == '42' else True

        with uuid('41296260-473b-49a8-a2cd-d1d806a80661') as case:
            # 2.5. Color Adjustment
            # 2.5.3. Contrast > Slider
            # set Contrast of the current keyframe by slider
            keyframe_room_page.fix_enhance.color_adjustment.contrast.show()
            keyframe_room_page.fix_enhance.color_adjustment.contrast.set_slider(43)

            check_result = keyframe_room_page.fix_enhance.color_adjustment.contrast.get_value(index_node=0)
            case.result = False if not check_result == '43' else True

        with uuid('98347a3c-79d0-4753-8524-3a5ecf1cb22a') as case:
            # 2.5. Color Adjustment
            # 2.5.4. Hue > Slider
            # set Hue of the current keyframe by slider
            keyframe_room_page.fix_enhance.color_adjustment.hue.show()
            keyframe_room_page.fix_enhance.color_adjustment.hue.set_slider(44)

            check_result = keyframe_room_page.fix_enhance.color_adjustment.hue.get_value(index_node=0)
            case.result = False if not check_result == '44' else True

        with uuid('573160a7-2125-4598-947f-25c1eeb88e97') as case:
            # 2.5. Color Adjustment
            # 2.5.5. Saturation > Slider
            # set Saturation of the current keyframe by slider
            keyframe_room_page.fix_enhance.color_adjustment.saturation.show()
            keyframe_room_page.fix_enhance.color_adjustment.saturation.set_slider(45)

            check_result = keyframe_room_page.fix_enhance.color_adjustment.saturation.get_value(index_node=0)
            case.result = False if not check_result == '45' else True

        with uuid('b355ed22-6cc1-4e56-aef3-8d2855c3d389') as case:
            # 2.5. Color Adjustment
            # 2.5.6. Vibrancy > Slider
            # set Vibrancy of the current keyframe by slider
            keyframe_room_page.fix_enhance.color_adjustment.vibrancy.show()
            keyframe_room_page.fix_enhance.color_adjustment.vibrancy.set_slider(46)

            check_result = keyframe_room_page.fix_enhance.color_adjustment.vibrancy.get_value(index_node=0)
            case.result = False if not check_result == '46' else True

        with uuid('f847f877-98c7-4a3b-bba4-6daa4443ae56') as case:
            # 2.5. Color Adjustment
            # 2.5.7. Highlight healing > Slider
            # set Highlight healing of the current keyframe by slider
            keyframe_room_page.fix_enhance.color_adjustment.highlight.show()
            keyframe_room_page.fix_enhance.color_adjustment.highlight.set_slider(47)

            check_result = keyframe_room_page.fix_enhance.color_adjustment.highlight.get_value(index_node=0)
            case.result = False if not check_result == '47' else True

        with uuid('7e0283e3-32e1-4b21-8ca1-dad45a37be01') as case:
            # 2.5. Color Adjustment
            # 2.5.8. Shadow > Slider
            # set Shadow of the current keyframe by slider
            keyframe_room_page.fix_enhance.color_adjustment.shadow.show()
            keyframe_room_page.fix_enhance.color_adjustment.shadow.set_slider(48)

            check_result = keyframe_room_page.fix_enhance.color_adjustment.shadow.get_value(index_node=0)
            case.result = False if not check_result == '48' else True

        with uuid('c2fe54dd-2fe0-44aa-9513-e3a72e74c1cb') as case:
            # 2.5. Color Adjustment
            # 2.5.9. Sharpness > Slider
            # set Sharpness of the current keyframe by slider
            keyframe_room_page.fix_enhance.color_adjustment.sharpness.show()
            keyframe_room_page.fix_enhance.color_adjustment.sharpness.set_slider(49)

            check_result = keyframe_room_page.fix_enhance.color_adjustment.sharpness.get_value(index_node=0)
            case.result = False if not check_result == '49' else True

        with uuid('d6e01e51-e471-4ef8-85b8-e36626531b7d') as case:
            # 2.6. White Balance
            # 2.6.2. Color temperature/Tint > Color temperature > Slider
            # set color temperature of the current keyframe by slider
            keyframe_room_page.fix_enhance.white_balance.show()
            keyframe_room_page.fix_enhance.white_balance.color_temperature.show()
            keyframe_room_page.fix_enhance.white_balance.select_color_temperature()
            keyframe_room_page.fix_enhance.white_balance.color_temperature.set_slider(70)

            check_result = keyframe_room_page.fix_enhance.white_balance.color_temperature.get_value(index_node=0)
            case.result = False if not check_result == '70' else True

        with uuid('00e56644-0330-40ca-aaf2-fc2c23f5056d') as case:
            # 2.6. White Balance
            # 2.6.2. Color temperature/Tint > Tint > Slider
            # set tint of the current keyframe by slider
            keyframe_room_page.fix_enhance.white_balance.tint.show()
            keyframe_room_page.fix_enhance.white_balance.tint.set_slider(40)

            check_result = keyframe_room_page.fix_enhance.white_balance.tint.get_value(index_node=0)
            case.result = False if not check_result == '40' else True

        with uuid('a7909d47-53d9-4715-a453-ae53e2a9f251') as case:
            # 2. Fix/Enhance
            # 2.3. Audio Denoise
            # 2.3.1. Noise type > Stationary noise
            # denoise the stationary noise
            library_preview_page.set_library_preview_window_timecode('00_00_02_00')
            keyframe_room_page.fix_enhance.audio_denoise.show()
            keyframe_room_page.fix_enhance.audio_denoise.noise.set_type(1)

            check_result = keyframe_room_page.fix_enhance.audio_denoise.noise.get_type(index_node=1)
            case.result = False if not check_result == 'Stationary noise' else True

        with uuid('3d4c0635-b4cc-4a55-9409-fc917abf951a') as case:
            # 2.3. Audio Denoise
            # 2.3.2. Degree > Input value
            # set audio denoise degree of the current keyframe by input value
            keyframe_room_page.fix_enhance.audio_denoise.degree.show()
            keyframe_room_page.fix_enhance.audio_denoise.degree.set_value('60')

            check_result = keyframe_room_page.fix_enhance.audio_denoise.degree.get_value(index_node=1)
            case.result = False if not check_result == '60' else True

        with uuid('3a478732-04bc-4334-b24f-0da2668497ec') as case:
            # 2.5. Color Adjustment
            # 2.5.1. Exposure > Input value
            # set exposure of the current keyframe by input value
            keyframe_room_page.fix_enhance.color_adjustment.exposure.show()
            keyframe_room_page.fix_enhance.color_adjustment.exposure.set_value('59')

            check_result = keyframe_room_page.fix_enhance.color_adjustment.exposure.get_value(index_node=1)
            case.result = False if not check_result == '59' else True

        with uuid('47ef3c51-e817-4b94-9be8-11e5b20bbbd2') as case:
            # 2.5. Color Adjustment
            # 2.5.2. Brightness > Input value
            # set Brightness of the current keyframe by input value
            keyframe_room_page.fix_enhance.color_adjustment.brightness.show()
            keyframe_room_page.fix_enhance.color_adjustment.brightness.set_value('58')

            check_result = keyframe_room_page.fix_enhance.color_adjustment.brightness.get_value(index_node=1)
            case.result = False if not check_result == '58' else True

        with uuid('56657df4-f8f1-41b4-9906-1ec692bd791c') as case:
            # 2.5. Color Adjustment
            # 2.5.3. Contrast > Input value
            # set Contrast of the current keyframe by input value
            keyframe_room_page.fix_enhance.color_adjustment.contrast.show()
            keyframe_room_page.fix_enhance.color_adjustment.contrast.set_value('57')

            check_result = keyframe_room_page.fix_enhance.color_adjustment.contrast.get_value(index_node=1)
            case.result = False if not check_result == '57' else True

        with uuid('a4958515-b7b0-4f8f-915a-d960c9fcbb5f') as case:
            # 2.5. Color Adjustment
            # 2.5.4. Hue > Input value
            # set Hue of the current keyframe by input value
            keyframe_room_page.fix_enhance.color_adjustment.hue.show()
            keyframe_room_page.fix_enhance.color_adjustment.hue.set_value('56')

            check_result = keyframe_room_page.fix_enhance.color_adjustment.hue.get_value(index_node=1)
            case.result = False if not check_result == '56' else True

        with uuid('3c8db8e1-c684-4d2c-98c8-587b07918641') as case:
            # 2.5. Color Adjustment
            # 2.5.5. Saturation > Input value
            # set Saturation of the current keyframe by input value
            keyframe_room_page.fix_enhance.color_adjustment.saturation.show()
            keyframe_room_page.fix_enhance.color_adjustment.saturation.set_value('55')

            check_result = keyframe_room_page.fix_enhance.color_adjustment.saturation.get_value(index_node=1)
            case.result = False if not check_result == '55' else True

        with uuid('6d20a8ec-1be9-418e-a6b9-3b2fefe0cb7e') as case:
            # 2.5. Color Adjustment
            # 2.5.6. Vibrancy > Input value
            # set Vibrancy of the current keyframe by input value
            keyframe_room_page.fix_enhance.color_adjustment.vibrancy.show()
            keyframe_room_page.fix_enhance.color_adjustment.vibrancy.set_value('54')

            check_result = keyframe_room_page.fix_enhance.color_adjustment.vibrancy.get_value(index_node=1)
            case.result = False if not check_result == '54' else True

        with uuid('8e37d362-2fd3-427a-b7f1-7af36d896832') as case:
            # 2.5. Color Adjustment
            # 2.5.7. Highlight healing > Input value
            # set Highlight healing of the current keyframe by input value
            keyframe_room_page.fix_enhance.color_adjustment.highlight.show()
            keyframe_room_page.fix_enhance.color_adjustment.highlight.set_value('53')

            check_result = keyframe_room_page.fix_enhance.color_adjustment.highlight.get_value(index_node=1)
            case.result = False if not check_result == '53' else True

        with uuid('e2ff7d38-76a9-4b88-b755-21c8de1df819') as case:
            # 2.5. Color Adjustment
            # 2.5.8. Shadow > Input value
            # set Shadow of the current keyframe by input value
            keyframe_room_page.fix_enhance.color_adjustment.shadow.show()
            keyframe_room_page.fix_enhance.color_adjustment.shadow.set_value('52')

            check_result = keyframe_room_page.fix_enhance.color_adjustment.shadow.get_value(index_node=1)
            case.result = False if not check_result == '52' else True

        with uuid('dae48baa-2650-452e-bd30-4fe8d897585f') as case:
            # 2.5. Color Adjustment
            # 2.5.9. Sharpness > Input value
            # set Sharpness of the current keyframe by input value
            keyframe_room_page.fix_enhance.color_adjustment.sharpness.show()
            keyframe_room_page.fix_enhance.color_adjustment.sharpness.set_value('51')

            check_result = keyframe_room_page.fix_enhance.color_adjustment.sharpness.get_value(index_node=1)
            case.result = False if not check_result == '51' else True

        with uuid('c683e9f9-d278-46d5-a8fa-ff2eee226f61') as case:
            # 2.6. White Balance
            # 2.6.2. Color temperature/Tint > Color temperature > Input value
            # set color temperature of the current keyframe by input value
            keyframe_room_page.fix_enhance.white_balance.show()
            keyframe_room_page.fix_enhance.white_balance.color_temperature.show()
            keyframe_room_page.fix_enhance.white_balance.select_color_temperature()
            keyframe_room_page.fix_enhance.white_balance.color_temperature.set_value('40')

            check_result = keyframe_room_page.fix_enhance.white_balance.color_temperature.get_value(index_node=1)
            case.result = False if not check_result == '40' else True

        with uuid('1ea5f980-1204-41b3-a8d2-c6d204dbe449') as case:
            # 2.6. White Balance
            # 2.6.2. Color temperature/Tint > Tint > Input value
            # set tint of the current keyframe by input value
            keyframe_room_page.fix_enhance.white_balance.tint.show()
            keyframe_room_page.fix_enhance.white_balance.tint.set_value('60')

            check_result = keyframe_room_page.fix_enhance.white_balance.tint.get_value(index_node=1)
            case.result = False if not check_result == '60' else True

        with uuid('6d75bd83-5ffc-45de-a4c4-047cfb9aecd6') as case:
            # 2.3. Audio Denoise
            # 2.3.2. Degree > Up/Down arrow
            # set audio denoise degree by Up/Down arrow
            library_preview_page.set_library_preview_window_timecode('00_00_04_00')
            keyframe_room_page.fix_enhance.audio_denoise.degree.show()
            for number_of_clicks in range(3):
                keyframe_room_page.fix_enhance.audio_denoise.degree.click_stepper_down()
            for number_of_clicks in range(2):
                keyframe_room_page.fix_enhance.audio_denoise.degree.click_stepper_up()

            check_result = keyframe_room_page.fix_enhance.audio_denoise.degree.get_value(index_node=2)
            case.result = False if not check_result == '59' else True

        with uuid('e6445bcd-12f2-402d-bec9-1e4514277b40') as case:
            # 2.5. Color Adjustment
            # 2.5.1. Exposure > Up/Down arrow
            # set exposure of the current keyframe by up/down arrow
            keyframe_room_page.fix_enhance.color_adjustment.exposure.show()
            for number_of_clicks in range(3):
                keyframe_room_page.fix_enhance.color_adjustment.exposure.click_stepper_down()
            for number_of_clicks in range(2):
                keyframe_room_page.fix_enhance.color_adjustment.exposure.click_stepper_up()

            check_result = keyframe_room_page.fix_enhance.color_adjustment.exposure.get_value(index_node=2)
            case.result = False if not check_result == '58' else True

        with uuid('9ad4f58f-ac5e-4e3c-95be-73ebb8e7efd7') as case:
            # 2.5. Color Adjustment
            # 2.5.2. Brightness > Up/Down arrow
            # set Brightness of the current keyframe by up/down arrow
            keyframe_room_page.fix_enhance.color_adjustment.brightness.show()
            for number_of_clicks in range(3):
                keyframe_room_page.fix_enhance.color_adjustment.brightness.click_stepper_down()
            for number_of_clicks in range(2):
                keyframe_room_page.fix_enhance.color_adjustment.brightness.click_stepper_up()

            check_result = keyframe_room_page.fix_enhance.color_adjustment.brightness.get_value(index_node=2)
            case.result = False if not check_result == '57' else True

        with uuid('d8bc1e3e-ee35-4b26-aeee-267c8a5d5dc9') as case:
            # 2.5. Color Adjustment
            # 2.5.3. Contrast > Up/Down arrow
            # set Contrast of the current keyframe by up/down arrow
            keyframe_room_page.fix_enhance.color_adjustment.contrast.show()
            for number_of_clicks in range(3):
                keyframe_room_page.fix_enhance.color_adjustment.contrast.click_stepper_down()
            for number_of_clicks in range(2):
                keyframe_room_page.fix_enhance.color_adjustment.contrast.click_stepper_up()

            check_result = keyframe_room_page.fix_enhance.color_adjustment.contrast.get_value(index_node=2)
            case.result = False if not check_result == '56' else True

        with uuid('5f63a9ec-8010-4d0d-9651-fe88fb2e4e54') as case:
            # 2.5. Color Adjustment
            # 2.5.4. Hue > Up/Down arrow
            # set Hue of the current keyframe by up/down arrow
            keyframe_room_page.fix_enhance.color_adjustment.hue.show()
            for number_of_clicks in range(3):
                keyframe_room_page.fix_enhance.color_adjustment.hue.click_stepper_down()
            for number_of_clicks in range(2):
                keyframe_room_page.fix_enhance.color_adjustment.hue.click_stepper_up()

            check_result = keyframe_room_page.fix_enhance.color_adjustment.hue.get_value(index_node=2)
            case.result = False if not check_result == '55' else True

        with uuid('27cd5722-d4d0-41a4-910e-cb8dc1be1cb5') as case:
            # 2.5. Color Adjustment
            # 2.5.5. Saturation > Up/Down arrow
            # set Saturation of the current keyframe by up/down arrow
            keyframe_room_page.fix_enhance.color_adjustment.saturation.show()
            for number_of_clicks in range(3):
                keyframe_room_page.fix_enhance.color_adjustment.saturation.click_stepper_down()
            for number_of_clicks in range(2):
                keyframe_room_page.fix_enhance.color_adjustment.saturation.click_stepper_up()

            check_result = keyframe_room_page.fix_enhance.color_adjustment.saturation.get_value(index_node=2)
            case.result = False if not check_result == '54' else True

        with uuid('2b418210-7513-4968-b33e-52b07a2e3e0b') as case:
            # 2.5. Color Adjustment
            # 2.5.6. Vibrancy > Up/Down arrow
            # set Vibrancy of the current keyframe by up/down arrow
            keyframe_room_page.fix_enhance.color_adjustment.vibrancy.show()
            for number_of_clicks in range(3):
                keyframe_room_page.fix_enhance.color_adjustment.vibrancy.click_stepper_down()
            for number_of_clicks in range(2):
                keyframe_room_page.fix_enhance.color_adjustment.vibrancy.click_stepper_up()

            check_result = keyframe_room_page.fix_enhance.color_adjustment.vibrancy.get_value(index_node=2)
            case.result = False if not check_result == '53' else True

        with uuid('874af9d0-2c1d-4d37-af8f-81aff96b41e6') as case:
            # 2.5. Color Adjustment
            # 2.5.7. Highlight healing > Up/Down arrow
            # set Highlight healing of the current keyframe by up/down arrow
            keyframe_room_page.fix_enhance.color_adjustment.highlight.show()
            for number_of_clicks in range(3):
                keyframe_room_page.fix_enhance.color_adjustment.highlight.click_stepper_down()
            for number_of_clicks in range(2):
                keyframe_room_page.fix_enhance.color_adjustment.highlight.click_stepper_up()

            check_result = keyframe_room_page.fix_enhance.color_adjustment.highlight.get_value(index_node=2)
            case.result = False if not check_result == '52' else True

        with uuid('130800f4-55d0-4fff-bb3c-80c10822d375') as case:
            # 2.5. Color Adjustment
            # 2.5.8. Shadow > Up/Down arrow
            # set Shadow of the current keyframe by up/down arrow
            keyframe_room_page.fix_enhance.color_adjustment.shadow.show()
            for number_of_clicks in range(3):
                keyframe_room_page.fix_enhance.color_adjustment.shadow.click_stepper_down()
            for number_of_clicks in range(2):
                keyframe_room_page.fix_enhance.color_adjustment.shadow.click_stepper_up()

            check_result = keyframe_room_page.fix_enhance.color_adjustment.shadow.get_value(index_node=2)
            case.result = False if not check_result == '51' else True

        with uuid('6a10852f-24d9-4161-95ca-c655dad39215') as case:
            # 2.5. Color Adjustment
            # 2.5.9. Sharpness > Up/Down arrow
            # set Sharpness of the current keyframe by up/down arrow
            keyframe_room_page.fix_enhance.color_adjustment.sharpness.show()
            for number_of_clicks in range(3):
                keyframe_room_page.fix_enhance.color_adjustment.sharpness.click_stepper_down()
            for number_of_clicks in range(2):
                keyframe_room_page.fix_enhance.color_adjustment.sharpness.click_stepper_up()

            check_result = keyframe_room_page.fix_enhance.color_adjustment.sharpness.get_value(index_node=2)
            case.result = False if not check_result == '50' else True

        with uuid('32b7dc2f-b89b-4b6e-8dc4-02f9fd0e062a') as case:
            # 2.6. White Balance
            # 2.6.2. Color temperature/Tint > Color temperature > Up/Down arrow
            # set color temperature of the current keyframe by up/down arrow
            keyframe_room_page.fix_enhance.white_balance.show()
            keyframe_room_page.fix_enhance.white_balance.color_temperature.show()
            keyframe_room_page.fix_enhance.white_balance.select_color_temperature()
            for number_of_clicks in range(3):
                keyframe_room_page.fix_enhance.white_balance.color_temperature.click_stepper_down()
            for number_of_clicks in range(2):
                keyframe_room_page.fix_enhance.white_balance.color_temperature.click_stepper_up()

            check_result_color_temperature = keyframe_room_page.fix_enhance.white_balance.\
                color_temperature.get_value(index_node=2)
            case.result = False if not check_result_color_temperature == '39' else True

        with uuid('59c66af3-b461-4231-82d9-9e9a92e5bfae') as case:
            # 2.6. White Balance
            # 2.6.2. Color temperature/Tint > Tint > Up/Down arrow
            # set tint of the current keyframe by up/down arrow
            keyframe_room_page.fix_enhance.white_balance.tint.show()
            for number_of_clicks in range(3):
                keyframe_room_page.fix_enhance.white_balance.tint.click_stepper_down()
            for number_of_clicks in range(2):
                keyframe_room_page.fix_enhance.white_balance.tint.click_stepper_up()

            check_result_tint = keyframe_room_page.fix_enhance.white_balance.tint.get_value(index_node=2)
            case.result = False if not check_result_tint == '59' else True

        with uuid('4af7c655-3d40-4c74-af51-b85f6a1c68be') as case:
            # 2.6. White Balance
            # 2.6.1. Checkbox > Color temperature/Tint
            # use color temperature / Tint on this keyframe
            case.result = check_result_color_temperature and check_result_tint

        with uuid('ac605df7-e07a-4b54-9b95-16575d4b5627') as case:
            # 2.6. White Balance
            # 2.6.1. Checkbox > White calibration
            # use white calibration on this keyframe
            keyframe_room_page.fix_enhance.white_balance.white_calibration.show()
            keyframe_room_page.fix_enhance.white_balance.select_white_calibration()
            check_result_white_calibration = keyframe_room_page.fix_enhance.white_balance.\
                white_calibration.click_i_button()
            case.result = check_result_white_calibration

        with uuid('16c65a42-c821-42de-ba5e-cc2380e8437d') as case:
            # 2.6. White Balance
            # 2.6.3. White calibration > Calibrate > (i) button
            # show what is white calibration ? dialog
            case.result = check_result_white_calibration

    @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid('d423091e-5203-43ea-ae53-4856b9332b31') as case:
            # 3. Effect
            # 3.1. Effect parameters
            # 3.1.1. Check effect parameters
            # sync with the parameters in effect modify page
            main_page.insert_media('Skateboard 01.mp4')
            main_page.enter_room(3)
            effect_room_page.hover_library_media('Aberration')
            effect_room_page.right_click()
            effect_room_page.select_right_click_menu('Apply Selected Effect to All Clips on Selected Track')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.effect.unfold_tab(value=1)
            keyframe_room_page.effect.show()
            keyframe_room_page.effect.aberration.show()

            check_value_1 = keyframe_room_page.effect.aberration.frequency.get_value()
            check_value_2 = keyframe_room_page.effect.aberration.strength.get_value()
            case.result = False if not (check_value_1 == '89' and check_value_2 == '67') else True

        with uuid('f602d627-0df3-45f2-a779-66ebb8d294b7') as case:
            # 3.1. Effect parameters
            # 3.1.2. Adjust effect parameters
            # set effect parameter of the current frame
            keyframe_room_page.effect.aberration.frequency.set_value('200')
            check_value_1 = keyframe_room_page.effect.aberration.frequency.get_value(index_node=0)
            check_result_1 = False if not check_value_1 == '200' else True
            keyframe_room_page.effect.aberration.strength.set_value('200')
            check_value_2 = keyframe_room_page.effect.aberration.strength.get_value(index_node=0)
            check_result_2 = False if not check_value_2 == '200' else True

            case.result = check_result_1 and check_result_2

        with uuid('f82c7fbf-7f0e-49e8-bf13-a122751f85d5') as case:
            # 4. Clip Attributes
            # 4.1. Position
            # 4.1.1. X position
            # set x position of the current keyframe
            keyframe_room_page.clip_attributes.unfold_tab(value=1)
            keyframe_room_page.clip_attributes.position.x.set_value(value='0.2')  # keyframe 00;00;00;00
            keyframe_value = keyframe_room_page.clip_attributes.position.x.get_value(index_node=0)
            check_result_1 = False if not keyframe_value == '0.200' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_1_1_1.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_1_1_1.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('80c12922-7323-4b0d-8b8e-f8a5ed57a638') as case:
            # 4.1. Position
            # 4.1.2. Y position
            # set y position of the current keyframe
            keyframe_room_page.clip_attributes.position.y.set_value(value='0.2')  # keyframe 00;00;00;00
            keyframe_value = keyframe_room_page.clip_attributes.position.y.get_value(index_node=0)
            check_result_1 = False if not keyframe_value == '0.200' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_1_2_1.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_1_2_1.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

            library_preview_page.set_library_preview_window_timecode('00_00_05_00')
            keyframe_room_page.clip_attributes.position.add_remove_keyframe()
            keyframe_room_page.clip_attributes.position.x.set_value('0.5')
            keyframe_room_page.clip_attributes.position.y.set_value('0.5')

            library_preview_page.set_library_preview_window_timecode('00_00_10_00')
            keyframe_room_page.clip_attributes.position.add_remove_keyframe()
            keyframe_room_page.clip_attributes.position.x.set_value('1')
            keyframe_room_page.clip_attributes.position.y.set_value('1')

            keyframe_room_page.clip_attributes.position.previous_keyframe()

        with uuid('6c49f0d6-880d-4e32-a135-b38e43fcf602') as case:
            # 4.1. Position
            # 4.1.3. ? Button
            # link to web page correctly
            case.result = keyframe_room_page.clip_attributes.position.click_tutorial_btn

        with uuid('846e11b1-025a-4041-a666-fc33bacbd8fe') as case:
            # 4.1. Position
            # 4.1.4. Ease in > Slider
            # set Ease in of the current keyframe by slider
            keyframe_room_page.clip_attributes.position.ease_in.set_checkbox(set_status=1)
            keyframe_room_page.clip_attributes.position.ease_in.set_slider(value=1)
            current_ease_in_value = keyframe_room_page.clip_attributes.position.ease_in.get_value()
            case.result = False if not current_ease_in_value == '1.00' else True

        with uuid('28c3c1cc-8533-4952-bf41-e2160dd63be5') as case:
            # 4.1. Position
            # 4.1.5. Ease out > Slider
            # set Ease out of the current keyframe by slider
            keyframe_room_page.clip_attributes.position.ease_out.set_checkbox(set_status=1)
            keyframe_room_page.clip_attributes.position.ease_out.set_slider(value=1)
            current_ease_out_value = keyframe_room_page.clip_attributes.position.ease_out.get_value()
            case.result = False if not current_ease_out_value == '1.00' else True

        with uuid('6e4326c4-7c45-4498-86ae-a799af5c166f') as case:
            # 4.1. Position
            # 4.1.4. Ease in > Input value
            # set Ease in of the current keyframe by input value
            keyframe_room_page.clip_attributes.position.ease_in.set_value(value='0.50')
            current_ease_in_value = keyframe_room_page.clip_attributes.position.ease_in.get_value(index_node=1)
            check_result_1 = False if not current_ease_in_value == '0.50' else True

            library_preview_page.set_library_preview_window_timecode('00_00_03_00')
            current_x_value = keyframe_room_page.clip_attributes.position.x.get_value()
            current_y_value = keyframe_room_page.clip_attributes.position.y.get_value()
            check_result_2 = False if not (current_x_value == '0.447' and current_y_value == '0.447') else True

            case.result = check_result_1 and check_result_2

            keyframe_room_page.clip_attributes.position.next_keyframe()

        with uuid('a7b7c238-a7e0-4761-a7bb-c60d022f6f70') as case:
            # 4.1. Position
            # 4.1.5. Ease out > Input value
            # set Ease out of the current keyframe by input value
            keyframe_room_page.clip_attributes.position.ease_out.set_value(value='0.50')
            current_ease_out_value = keyframe_room_page.clip_attributes.position.ease_out.get_value(index_node=1)
            check_result_1 = False if not current_ease_out_value == '0.50' else True

            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            current_x_value = keyframe_room_page.clip_attributes.position.x.get_value()
            current_y_value = keyframe_room_page.clip_attributes.position.y.get_value()
            check_result_2 = False if not (current_x_value == '0.589' and current_y_value == '0.589') else True

            case.result = check_result_1 and check_result_2

            keyframe_room_page.clip_attributes.position.previous_keyframe()

        with uuid('db5b4dc5-d425-44a8-a4af-650d2e7c3f98') as case:
            # 4.1. Position
            # 4.1.4. Ease in > Up/Down arrow
            # set Ease in of the current keyframe by up/down arrow
            keyframe_room_page.clip_attributes.position.ease_in.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.position.ease_in.click_stepper_down(times=3)
            current_value_ease_in = keyframe_room_page.clip_attributes.position.ease_in.get_value()
            case.result = False if not current_value_ease_in == '0.49' else True

        with uuid('4f678b47-5f0c-4c56-8c31-fc5ab3b48ee7') as case:
            # 4.1. Position
            # 4.1.5. Ease out > Up/Down arrow
            # set Ease out of the current keyframe by up/down arrow
            keyframe_room_page.clip_attributes.position.ease_out.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.position.ease_out.click_stepper_down(times=3)
            current_value_ease_out = keyframe_room_page.clip_attributes.position.ease_out.get_value()
            case.result = False if not current_value_ease_out == '0.49' else True

    @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid('a75813d4-8c4a-41a2-8757-2dd333a17ce6') as case:
            # 4.2. Scale
            # 4.2.2. Width > Slider
            # set width of the current keyframe by slider
            main_page.insert_media('Skateboard 01.mp4')
            main_page.enter_room(3)
            effect_room_page.hover_library_media('Aberration')
            effect_room_page.right_click()
            effect_room_page.select_right_click_menu('Apply Selected Effect to All Clips on Selected Track')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()

            keyframe_room_page.clip_attributes.unfold_tab(value=1)
            keyframe_room_page.clip_attributes.scale.width.set_slider(value=0.5)  # keyframe 00;00;00;00
            keyframe_value = keyframe_room_page.clip_attributes.scale.width.get_value(index_node=0)
            check_result_1 = False if not keyframe_value == '0.500' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_2_2_1.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_2_2_1.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('82601df8-60c2-4504-b70d-821f6f1c206b') as case:
            # 4.2. Scale
            # 4.2.1. Height > Slider
            # set height of the current keyframe by slider
            keyframe_room_page.clip_attributes.scale.height.set_slider(value=0.4)  # keyframe 00;00;00;00
            keyframe_value = keyframe_room_page.clip_attributes.scale.height.get_value(index_node=0)
            check_result_1 = False if not keyframe_value == '0.400' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_2_1_1.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_2_1_1.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('ac5a1a50-4f45-4b57-904c-fbfeea2c6ced') as case:
            # 4.2. Scale
            # 4.2.2. Width > Input value
            # set width of the current keyframe by input value
            library_preview_page.set_library_preview_window_timecode('00_00_05_00')
            keyframe_room_page.clip_attributes.scale.add_remove_keyframe()

            keyframe_room_page.clip_attributes.scale.width.set_value(value='3')
            keyframe_value = keyframe_room_page.clip_attributes.scale.width.get_value(index_node=1)
            check_result_1 = False if not keyframe_value == '3.000' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_2_2_2.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_2_2_2.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('c74c7d08-8bbf-4e52-a1a9-6d688d10bb31') as case:
            # 4.2. Scale
            # 4.2.1. Height > Input value
            # set height of the current keyframe by input value
            keyframe_room_page.clip_attributes.scale.height.set_value(value='3.2')
            keyframe_value = keyframe_room_page.clip_attributes.scale.height.get_value(index_node=1)
            check_result_1 = False if not keyframe_value == '3.200' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_2_1_2.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_2_1_2.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('dfb439ae-6648-4a86-8bdf-b6faee7f1a5f') as case:
            # 4.2. Scale
            # 4.2.2. Width > Up/Down arrow
            # set width of the current keyframe by up/down arrow
            library_preview_page.set_library_preview_window_timecode('00_00_10_00')
            keyframe_room_page.clip_attributes.scale.add_remove_keyframe()
            keyframe_room_page.clip_attributes.scale.width.set_value(value='5')

            keyframe_room_page.clip_attributes.scale.width.click_stepper_down(times=3)
            keyframe_room_page.clip_attributes.scale.width.click_stepper_up(times=2)
            current_width_value = keyframe_room_page.clip_attributes.scale.width.get_value()
            check_result_1 = False if not current_width_value == '4.999' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_2_2_3.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_2_2_3.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('75f092b7-0369-4ef7-ad76-7b62d6cfed08') as case:
            # 4.2. Scale
            # 4.2.1. Height > Up/Down arrow
            # set height of the current keyframe by up/down arrow
            keyframe_room_page.clip_attributes.scale.height.set_value(value='6')

            keyframe_room_page.clip_attributes.scale.height.click_stepper_down(times=3)
            keyframe_room_page.clip_attributes.scale.height.click_stepper_up(times=2)
            current_height_value = keyframe_room_page.clip_attributes.scale.height.get_value()
            check_result_1 = False if not current_height_value == '5.999' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_2_1_3.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_2_1_3.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('490bddf3-04e3-48c6-b48f-468a58b4adde') as case:
            # 4.2. Scale
            # 4.2.3. Maintain aspect ratio
            # enable maintain aspect ratio of the current keyframe
            keyframe_room_page.clip_attributes.scale.set_maintain_aspect_ratio(set_status=0)  # un-tick
            keyframe_room_page.clip_attributes.scale.height.set_value(value='2.5')

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_2_3_1.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_2_3_1.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            case.result = keyframe_room_page.compare(ground_truth, current_preview)

            main_page.click_undo()
            keyframe_room_page.clip_attributes.scale.previous_keyframe()

        with uuid('61ecb43a-a817-442a-afce-7234004b1790') as case:
            # 4.2. Scale
            # 4.2.4. Ease in > Slider
            # set Ease in of the current keyframe by slider
            keyframe_room_page.clip_attributes.scale.show()
            keyframe_room_page.clip_attributes.scale.ease_in.set_checkbox(set_status=1)
            keyframe_room_page.clip_attributes.scale.ease_in.set_slider(value=1)
            current_ease_in_value = keyframe_room_page.clip_attributes.scale.ease_in.get_value()
            case.result = False if not current_ease_in_value == '1.00' else True

        with uuid('2ed72a7f-4f15-4490-b2fd-3cb5dc02a6f6') as case:
            # 4.2. Scale
            # 4.2.5. Ease out > Slider
            # set Ease out of the current keyframe by slider
            keyframe_room_page.clip_attributes.scale.ease_out.set_checkbox(set_status=1)
            keyframe_room_page.clip_attributes.scale.ease_out.set_slider(value=1)
            current_ease_out_value = keyframe_room_page.clip_attributes.scale.ease_out.get_value()
            case.result = False if not current_ease_out_value == '1.00' else True

        with uuid('04f533ce-2cf6-48a8-b24e-6e7b0c60f8f5') as case:
            # 4.2. Scale
            # 4.2.4. Ease in > Input value
            # set Ease in of the current keyframe by input value
            keyframe_room_page.clip_attributes.scale.ease_in.set_value(value='0.50')
            current_ease_in_value = keyframe_room_page.clip_attributes.scale.ease_in.get_value(index_node=1)
            check_result_1 = False if not current_ease_in_value == '0.50' else True

            library_preview_page.set_library_preview_window_timecode('00_00_03_00')
            current_width_value = keyframe_room_page.clip_attributes.scale.width.get_value()
            current_height_value = keyframe_room_page.clip_attributes.scale.height.get_value()
            check_result_2 = False if not (current_width_value == '2.701' and current_height_value == '2.701') else True

            case.result = check_result_1 and check_result_2

            keyframe_room_page.clip_attributes.scale.next_keyframe()

        with uuid('84240e65-21c0-4765-bf4c-f1922a190469') as case:
            # 4.2. Scale
            # 4.2.5. Ease out > Input value
            # set Ease out of the current keyframe by input value
            keyframe_room_page.clip_attributes.scale.ease_out.set_value(value='0.50')
            current_ease_out_value = keyframe_room_page.clip_attributes.scale.ease_out.get_value(index_node=1)
            check_result_1 = False if not current_ease_out_value == '0.50' else True

            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            current_width_value = keyframe_room_page.clip_attributes.scale.width.get_value()
            current_height_value = keyframe_room_page.clip_attributes.scale.height.get_value()
            check_result_2 = False if not (current_width_value == '3.698' and current_height_value == '3.698') else True

            case.result = check_result_1 and check_result_2

            keyframe_room_page.clip_attributes.scale.previous_keyframe()

        with uuid('b2d25532-08cc-4189-99cf-dadffd736845') as case:
            # 4.2. Scale
            # 4.2.4. Ease in > Up/Down arrow
            # set Ease in of the current keyframe by up/down arrow
            keyframe_room_page.clip_attributes.scale.ease_in.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.scale.ease_in.click_stepper_down(times=3)
            current_value_ease_in = keyframe_room_page.clip_attributes.scale.ease_in.get_value()
            case.result = False if not current_value_ease_in == '0.49' else True

        with uuid('10a97918-b17a-4306-8c90-ba598bf1c0c6') as case:
            # 4.2. Scale
            # 4.2.5. Ease out > Up/Down arrow
            # set Ease out of the current keyframe by up/down arrow
            keyframe_room_page.clip_attributes.scale.ease_out.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.scale.ease_out.click_stepper_down(times=3)
            current_value_ease_out = keyframe_room_page.clip_attributes.scale.ease_out.get_value()
            case.result = False if not current_value_ease_out == '0.49' else True

    @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid('8fb0e26b-b74f-44da-b8b0-789f48f6925a') as case:
            # 4.3. Opacity
            # 4.3.1. Opacity > Slider
            # set opacity of the current keyframe by slider
            main_page.insert_media('Skateboard 01.mp4')
            main_page.timeline_select_track(track_no=2)
            main_page.insert_media('Skateboard 02.mp4')
            timeline_operation_page.select_timeline_media(track_index=2, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.clip_attributes.opacity.show()
            keyframe_room_page.clip_attributes.opacity.set_slider(value=50)

            current_opacity_value = keyframe_room_page.clip_attributes.opacity.get_value(index_node=0)
            check_result_1 = False if not current_opacity_value == '50' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_3_1_1.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_3_1_1.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)
            case.result = check_result_1 and check_result_2

        with uuid('3b25195f-85a2-4c69-bcdc-492094c6faaf') as case:
            # 4.3. Opacity
            # 4.3.1. Opacity > Input value
            # set opacity of the current keyframe by input value
            keyframe_room_page.clip_attributes.opacity.set_value(value='80')

            current_opacity_value = keyframe_room_page.clip_attributes.opacity.get_value(index_node=0)
            check_result_1 = False if not current_opacity_value == '80' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_3_1_2.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_3_1_2.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)
            case.result = check_result_1 and check_result_2

        with uuid('65248aa3-195d-44f0-b0f5-a0151ccbcf61') as case:
            # 4.3. Opacity
            # 4.3.1. Opacity > Up/Down arrow
            # set opacity of the current keyframe by up/down arrow
            keyframe_room_page.clip_attributes.opacity.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.opacity.click_stepper_down(times=3)

            current_opacity_value = keyframe_room_page.clip_attributes.opacity.get_value(index_node=0)
            case.result = False if not current_opacity_value == '79' else True

    @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid('4e65b542-cfa7-410c-a7a0-872bb56e1734') as case:
            # 4.4. Rotation
            # 4.4.1. Degree > Input value
            # set rotation degree of the current keyframe by input value
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.clip_attributes.rotation.show()
            keyframe_room_page.clip_attributes.rotation.add_remove_keyframe()  # 00;00;00;00

            library_preview_page.set_library_preview_window_timecode('00_00_05_00')  # 00;00;05;00
            keyframe_room_page.clip_attributes.rotation.set_value(value='-90')

            current_rotation_value = keyframe_room_page.clip_attributes.rotation.get_value(index_node=1)
            check_result_1 = False if not current_rotation_value == '-90.00' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_4_1_1.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_4_1_1.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)
            case.result = check_result_1 and check_result_2

        with uuid('2115a715-fcbb-4c04-9a25-2ae4de7d59f4') as case:
            # 4.4. Rotation
            # 4.4.1. Degree > Up/Down arrow
            # set rotation degree of the current keyframe by Up/Down arrow
            library_preview_page.set_library_preview_window_timecode('00_00_10_00')  # 00;00;10;00
            keyframe_room_page.clip_attributes.rotation.set_value(value='180.01')
            keyframe_room_page.clip_attributes.rotation.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.rotation.click_stepper_down(times=3)

            current_rotation_value = keyframe_room_page.clip_attributes.rotation.get_value(index_node=2)
            case.result = False if not current_rotation_value == '180.00' else True

            keyframe_room_page.clip_attributes.rotation.previous_keyframe()

        with uuid('442a26a0-c712-4526-b526-0119e89b3566') as case:
            # 4.4. Rotation
            # 4.4.2. Ease in > Slider
            # set Ease in of the current keyframe by slider
            keyframe_room_page.clip_attributes.rotation.ease_in.set_checkbox(set_status=1)
            keyframe_room_page.clip_attributes.rotation.ease_in.set_slider(value=1)
            current_ease_in_value = keyframe_room_page.clip_attributes.rotation.ease_in.get_value()
            case.result = False if not current_ease_in_value == '1.00' else True

        with uuid('27b5677d-93ae-41c0-a03b-54fd79dd8497') as case:
            # 4.4. Rotation
            # 4.4.3. Ease out > Slider
            # set Ease out of the current keyframe by slider
            keyframe_room_page.clip_attributes.rotation.ease_out.set_checkbox(set_status=1)
            keyframe_room_page.clip_attributes.rotation.ease_out.set_slider(value=1)
            current_ease_out_value = keyframe_room_page.clip_attributes.rotation.ease_out.get_value()
            case.result = False if not current_ease_out_value == '1.00' else True

        with uuid('4f6168dd-9ecb-4ff5-9801-16d2f2e97f55') as case:
            # 4.4. Rotation
            # 4.4.2. Ease in > Input value
            # set Ease in of the current keyframe by input value
            keyframe_room_page.clip_attributes.rotation.ease_in.set_value(value='0.50')
            current_ease_in_value = keyframe_room_page.clip_attributes.rotation.ease_in.get_value(index_node=1)
            check_result_1 = False if not current_ease_in_value == '0.50' else True

            library_preview_page.set_library_preview_window_timecode('00_00_03_00')
            current_rotation_value = keyframe_room_page.clip_attributes.rotation.get_value()
            check_result_2 = False if not current_rotation_value == '-73.97' else True

            case.result = check_result_1 and check_result_2

            keyframe_room_page.clip_attributes.rotation.next_keyframe()

        with uuid('ea4111ed-e675-4e42-8e77-8a9f2ec4a46e') as case:
            # 4.4. Rotation
            # 4.4.3. Ease out > Input value
            # set Ease out of the current keyframe by input value
            keyframe_room_page.clip_attributes.rotation.ease_out.set_value(value='0.50')
            current_ease_out_value = keyframe_room_page.clip_attributes.rotation.ease_out.get_value(index_node=1)
            check_result_1 = False if not current_ease_out_value == '0.50' else True

            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            current_rotation_value = keyframe_room_page.clip_attributes.rotation.get_value()
            check_result_2 = False if not current_rotation_value == '-41.92' else True

            case.result = check_result_1 and check_result_2

            keyframe_room_page.clip_attributes.rotation.previous_keyframe()

        with uuid('a8b61c86-a9c2-4ec9-8948-92b61d812aa1') as case:
            # 4.4. Rotation
            # 4.4.2. Ease in > Up/Down arrow
            # set Ease in of the current keyframe by up/down arrow
            keyframe_room_page.clip_attributes.rotation.ease_in.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.rotation.ease_in.click_stepper_down(times=3)
            current_value_ease_in = keyframe_room_page.clip_attributes.rotation.ease_in.get_value()
            case.result = False if not current_value_ease_in == '0.49' else True

        with uuid('0441f3b7-ee53-452f-8d8e-f7840e2d9ca1') as case:
            # 4.4. Rotation
            # 4.4.3. Ease out > Up/Down arrow
            # set Ease out of the current keyframe by up/down arrow
            keyframe_room_page.clip_attributes.rotation.ease_out.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.rotation.ease_out.click_stepper_down(times=3)
            current_value_ease_out = keyframe_room_page.clip_attributes.rotation.ease_out.get_value()
            case.result = False if not current_value_ease_out == '0.49' else True

    @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        with uuid('2de1cdf8-2284-489d-8344-95ab984652bf') as case:
            # 4.5. Freeform
            # 4.5.1. Freeform top-left position > X position > Input value
            # set freeform top-lift x position of the current keyframe by input value
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.clip_attributes.freeform.show()
            keyframe_room_page.clip_attributes.freeform.add_remove_keyframe()  # 00;00;00;00
            keyframe_room_page.clip_attributes.freeform.top_left_x.set_value('0.1')

            current_top_left_x_value = keyframe_room_page.clip_attributes.freeform.top_left_x.get_value(index_node=0)
            check_result_1 = False if not current_top_left_x_value == '0.100' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_1_1.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_1_1.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('bedbe2d7-b446-434e-9455-b280e8da0830') as case:
            # 4.5. Freeform
            # 4.5.1. Freeform top-left position > Y position > Input value
            # set freeform top-lift y position of the current keyframe by input value
            keyframe_room_page.clip_attributes.freeform.top_right_y.set_value('0.5')
            keyframe_room_page.clip_attributes.freeform.top_left_y.set_value('0.9')

            current_top_left_y_value = keyframe_room_page.clip_attributes.freeform.top_left_y.get_value(index_node=0)
            check_result_1 = False if not current_top_left_y_value == '0.900' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_1_2.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_1_2.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('c339fc98-2610-4586-bcd0-b6851a537b0f') as case:
            # 4.5. Freeform
            # 4.5.2. Freeform top-right position > X position > Input value
            # set freeform top-right x position of the current keyframe by input value
            keyframe_room_page.clip_attributes.freeform.top_right_x.set_value('0.9')

            current_top_right_x_value = keyframe_room_page.clip_attributes.freeform.top_right_x.get_value(index_node=0)
            check_result_1 = False if not current_top_right_x_value == '0.900' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_2_1.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_2_1.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('1ef59920-af51-4132-b4cf-3423d639ee2b') as case:
            # 4.5. Freeform
            # 4.5.2. Freeform top-right position > Y position > Input value
            # set freeform top-right y position of the current keyframe by input value
            keyframe_room_page.clip_attributes.freeform.top_right_y.set_value('0.9')

            current_top_right_y_value = keyframe_room_page.clip_attributes.freeform.top_right_y.get_value(index_node=0)
            check_result_1 = False if not current_top_right_y_value == '0.900' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_2_2.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_2_2.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('27b91dfd-2dec-473d-b1ef-3bdf9892c78b') as case:
            # 4.5. Freeform
            # 4.5.3. Freeform bottom-left position > X position > Input value
            # set freeform bottom-left x position of the current keyframe by input value
            keyframe_room_page.clip_attributes.freeform.bottom_left_x.set_value('0.05')

            current_bottom_left_x_value = keyframe_room_page.clip_attributes.\
                freeform.bottom_left_x.get_value(index_node=0)
            check_result_1 = False if not current_bottom_left_x_value == '0.050' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_3_1.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_3_1.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('45814c1d-3aa4-4188-8fd7-a80e4105583e') as case:
            # 4.5. Freeform
            # 4.5.3. Freeform bottom-left position > Y position > Input value
            # set freeform bottom-left y position of the current keyframe by input value
            keyframe_room_page.clip_attributes.freeform.bottom_left_y.set_value('0.95')

            current_bottom_left_y_value = keyframe_room_page.clip_attributes.\
                freeform.bottom_left_y.get_value(index_node=0)
            check_result_1 = False if not current_bottom_left_y_value == '0.950' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_3_2.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_3_2.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('44501b2b-349c-4eb4-99a7-e6842af420d5') as case:
            # 4.5. Freeform
            # 4.5.4. Freeform bottom-right position > X position > Input value
            # set freeform bottom-right x position of the current keyframe by input value
            keyframe_room_page.clip_attributes.freeform.bottom_right_x.set_value('0.95')

            current_bottom_right_x_value = keyframe_room_page.clip_attributes.\
                freeform.bottom_right_x.get_value(index_node=0)
            check_result_1 = False if not current_bottom_right_x_value == '0.950' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_4_1.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_4_1.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('b367ff2c-20e7-4b7a-a5d1-d6a73c2634f6') as case:
            # 4.5. Freeform
            # 4.5.4. Freeform bottom-right position > Y position > Input value
            # set freeform bottom-right y position of the current keyframe by input value
            keyframe_room_page.clip_attributes.freeform.bottom_right_y.set_value('0.95')

            current_bottom_right_y_value = keyframe_room_page.clip_attributes.\
                freeform.bottom_right_y.get_value(index_node=0)
            check_result_1 = False if not current_bottom_right_y_value == '0.950' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_4_2.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_4_2.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('ef9df224-b3bc-430f-a5f0-df07c54c70c3') as case:
            # 4.5. Freeform
            # 4.5.1. Freeform top-left position > X position > Up/Down arrow
            # set freeform top-lift x position of the current keyframe by up/down arrow
            library_preview_page.set_library_preview_window_timecode('00_00_10_00')
            keyframe_room_page.clip_attributes.freeform.add_remove_keyframe()  # 00;00;10;00
            keyframe_room_page.clip_attributes.freeform.top_left_x.set_value('0.051')
            keyframe_room_page.clip_attributes.freeform.top_left_x.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.freeform.top_left_x.click_stepper_down(times=3)

            current_top_left_x_value = keyframe_room_page.clip_attributes.\
                freeform.top_left_x.get_value(index_node=1)
            check_result_1 = False if not current_top_left_x_value == '0.050' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_1_3.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_1_3.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('7c78a602-314c-48e3-8556-6bd931924a6b') as case:
            # 4.5. Freeform
            # 4.5.1. Freeform top-left position > Y position > Up/Down arrow
            # set freeform top-lift y position of the current keyframe by up/down arrow
            keyframe_room_page.clip_attributes.freeform.top_left_y.set_value('0.051')
            keyframe_room_page.clip_attributes.freeform.top_left_y.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.freeform.top_left_y.click_stepper_down(times=3)

            current_top_left_y_value = keyframe_room_page.clip_attributes.freeform.top_left_y.get_value(index_node=1)
            check_result_1 = False if not current_top_left_y_value == '0.050' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_1_4.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_1_4.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('0bb7aeda-13fa-4177-be71-f2a878a2b7e3') as case:
            # 4.5. Freeform
            # 4.5.2. Freeform top-right position > X position > Up/Down arrow
            # set freeform top-right x position of the current keyframe by up/down arrow
            keyframe_room_page.clip_attributes.freeform.top_right_x.set_value('0.951')
            keyframe_room_page.clip_attributes.freeform.top_right_x.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.freeform.top_right_x.click_stepper_down(times=3)

            current_top_right_x_value = keyframe_room_page.clip_attributes.freeform.top_right_x.get_value(index_node=1)
            check_result_1 = False if not current_top_right_x_value == '0.950' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_2_3.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_2_3.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('a83f69c4-8585-4cdd-a426-2ff7ae9ac269') as case:
            # 4.5. Freeform
            # 4.5.2. Freeform top-right position > Y position > Up/Down arrow
            # set freeform top-right y position of the current keyframe by up/down arrow
            keyframe_room_page.clip_attributes.freeform.top_right_y.set_value('0.051')
            keyframe_room_page.clip_attributes.freeform.top_right_y.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.freeform.top_right_y.click_stepper_down(times=3)

            current_top_right_y_value = keyframe_room_page.clip_attributes.freeform.top_right_y.get_value(index_node=1)
            check_result_1 = False if not current_top_right_y_value == '0.050' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_2_4.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_2_4.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('22f7eb22-73d3-4383-ae2b-2171f94d5dfd') as case:
            # 4.5. Freeform
            # 4.5.3. Freeform bottom-left position > X position > Up/Down arrow
            # set freeform bottom-left x position of the current keyframe by up/down arrow
            keyframe_room_page.clip_attributes.freeform.bottom_left_x.set_value('0.051')
            keyframe_room_page.clip_attributes.freeform.bottom_left_x.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.freeform.bottom_left_x.click_stepper_down(times=3)

            current_bottom_left_x_value = keyframe_room_page.clip_attributes.\
                freeform.bottom_left_x.get_value(index_node=1)
            check_result_1 = False if not current_bottom_left_x_value == '0.050' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_3_3.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_3_3.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('50d5aa8d-ca44-4fd9-8eae-bed7379117fd') as case:
            # 4.5. Freeform
            # 4.5.3. Freeform bottom-left position > Y position > Up/Down arrow
            # set freeform bottom-left y position of the current keyframe by up/down arrow
            keyframe_room_page.clip_attributes.freeform.bottom_left_y.set_value('0.951')
            keyframe_room_page.clip_attributes.freeform.bottom_left_y.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.freeform.bottom_left_y.click_stepper_down(times=3)

            current_bottom_left_y_value = keyframe_room_page.clip_attributes.\
                freeform.bottom_left_y.get_value(index_node=1)
            check_result_1 = False if not current_bottom_left_y_value == '0.950' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_3_4.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_3_4.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('1d206419-ff2c-4646-83e2-0c791a510e7c') as case:
            # 4.5. Freeform
            # 4.5.4. Freeform bottom-right position > X position > Up/Down arrow
            # set freeform bottom-right x position of the current keyframe by up/down arrow
            keyframe_room_page.clip_attributes.freeform.bottom_right_x.set_value('0.951')
            keyframe_room_page.clip_attributes.freeform.bottom_right_x.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.freeform.bottom_right_x.click_stepper_down(times=3)

            current_bottom_right_x_value = keyframe_room_page.clip_attributes.\
                freeform.bottom_right_x.get_value(index_node=1)
            check_result_1 = False if not current_bottom_right_x_value == '0.950' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_4_3.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_4_3.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('3d15d6b7-922c-4183-9aa7-0becc0323c33') as case:
            # 4.5. Freeform
            # 4.5.4. Freeform bottom-right position > Y position > Up/Down arrow
            # set freeform bottom-right y position of the current keyframe by up/down arrow
            keyframe_room_page.clip_attributes.freeform.bottom_right_y.set_value('0.951')
            keyframe_room_page.clip_attributes.freeform.bottom_right_y.click_stepper_up(times=2)
            keyframe_room_page.clip_attributes.freeform.bottom_right_y.click_stepper_down(times=3)

            current_bottom_right_y_value = keyframe_room_page.clip_attributes.\
                freeform.bottom_right_y.get_value(index_node=1)
            check_result_1 = False if not current_bottom_right_y_value == '0.950' else True

            image_full_path = Auto_Ground_Truth_Folder + 'keyframe_room_4_5_4_4.png'
            ground_truth = Ground_Truth_Folder + 'keyframe_room_4_5_4_4.png'
            current_preview = keyframe_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result_2 = keyframe_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

            keyframe_room_page.clip_attributes.freeform.previous_keyframe()

        with uuid('f2c77075-3730-4e88-a82d-6293e88f0190') as case:
            # 5. Volume
            # 5.1. Volume
            # 5.1.1. dB > Slider
            # set db of the current keyframe by slider
            keyframe_room_page.volume.show()
            keyframe_room_page.volume.set_slider(value=100)

            current_volume_value = keyframe_room_page.volume.get_value(index_node=0)
            case.result = False if not current_volume_value == '12.0' else True

        with uuid('554e9eb1-dde0-4dcb-9bbe-a8ebc902e4fe') as case:
            # 5.1. Volume
            # 5.1.1. dB > Input value
            # set db of the current keyframe by input value
            keyframe_room_page.volume.next_keyframe()
            keyframe_room_page.volume.set_value(value=2)

            current_volume_value = keyframe_room_page.volume.get_value(index_node=1)
            case.result = False if not current_volume_value == '2.0' else True

        with uuid('935547e8-76f7-4683-a63b-e6173b1acb03') as case:
            # 5.1. Volume
            # 5.1.1. dB > Up/Down arrow
            # set db of the current keyframe by up/down arrow
            keyframe_room_page.volume.click_stepper_up(times=2)
            keyframe_room_page.volume.click_stepper_down(times=3)

            current_volume_value = keyframe_room_page.volume.get_value(index_node=1)
            case.result = False if not current_volume_value == '1.9' else True



    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        # color enhancement add/remove keyframe
        with uuid('4cce5e3e-6688-4d61-a4b5-bdc2c66c6774') as case:
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.split_toning.show()
            keyframe_room_page.fix_enhance.color_enhancement.degree.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.8.0_Fix_Enhance_Color_Enhancement_Add_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.8.0_Fix_Enhance_Color_Enhancement_Add_Keyframe.png',
                                                        preview_result)
            case.result = image_result

        # color enhancement previous keyframe
        with uuid('dca24cc6-e08b-4fad-a882-c26ee4325351') as case:
            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            keyframe_room_page.fix_enhance.color_enhancement.degree.add_remove_keyframe()
            keyframe_room_page.fix_enhance.color_enhancement.degree.previous_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.8.1_Fix_Enhance_Color_Enhancement_Previous_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.8.1_Fix_Enhance_Color_Enhancement_Previous_Keyframe.png',
                                                      preview_result)
            case.result = image_result

        # color enhancement next keyframe
        with uuid('159a28ce-e282-450f-acfb-e37ec0aec3d2') as case:
            keyframe_room_page.fix_enhance.color_enhancement.degree.next_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.8.2_Fix_Enhance_Color_Enhancement_Next_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.8.2_Fix_Enhance_Color_Enhancement_Next_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement set value slider
        with uuid('85a62a7d-6d46-484b-afba-63004aa64ea1') as case:
            keyframe_room_page.fix_enhance.color_enhancement.degree.set_slider(70)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.8.3_Fix_Enhance_Color_Enhancement_Set_Slider.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.8.3_Fix_Enhance_Color_Enhancement_Set_Slider.png',
                preview_result)
            case.result = image_result

        # color enhancement set value input
        with uuid('fbab9e72-ff72-4ec8-ac4b-ca2993d20920') as case:
            keyframe_room_page.fix_enhance.color_enhancement.degree.set_value(90)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.8.4_Fix_Enhance_Color_Enhancement_Set_Value.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.8.4_Fix_Enhance_Color_Enhancement_Set_Value.png',
                preview_result)
            case.result = image_result

        # color enhancement set value arrow
        with uuid('ee91ab54-d55c-4d75-9f5c-b8b45dac5e13') as case:
            keyframe_room_page.fix_enhance.color_enhancement.degree.click_stepper_up(times=3)
            keyframe_room_page.fix_enhance.color_enhancement.degree.click_stepper_down(times=1)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.8.5_Fix_Enhance_Color_Enhancement_Set_Arrow.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.8.5_Fix_Enhance_Color_Enhancement_Set_Arrow.png',
                preview_result)
            case.result = image_result

        # color enhancement reset
        with uuid('4f5f9438-0b0f-4269-892f-b659bf95244b') as case:
            keyframe_room_page.fix_enhance.color_enhancement.degree.reset_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.8.6_Fix_Enhance_Color_Enhancement_Reset.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.8.6_Fix_Enhance_Color_Enhancement_Reset.png',
                preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        # split toning highlights hue add/remove keyframe
        with uuid('df85ac8c-34a5-4b51-8abc-4d9eae09d171') as case:
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.split_toning.highlights_hue.show()
            keyframe_room_page.fix_enhance.split_toning.highlights_hue.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.9.0_Fix_Enhance_Split_toning_HighlightsHue_Add_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.9.0_Fix_Enhance_Split_toning_HighlightsHue_Add_Keyframe.png',
                        preview_result)
            case.result = image_result

        # color enhancement previous keyframe
        with uuid('65cfa2fd-3e05-45cf-9948-b118d09a8118') as case:
            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            keyframe_room_page.fix_enhance.split_toning.highlights_hue.add_remove_keyframe()
            keyframe_room_page.fix_enhance.split_toning.highlights_hue.previous_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.9.1_Fix_Enhance_Split_toning_HighlightsHue_Previous_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.9.1_Fix_Enhance_Split_toning_HighlightsHue_Previous_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement next keyframe
        with uuid('b26686ab-47ca-4ca9-94a5-95559fb3cc9d') as case:
            keyframe_room_page.fix_enhance.split_toning.highlights_hue.next_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.9.2_Fix_Enhance_Split_toning_HighlightsHue_Next_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.9.2_Fix_Enhance_Split_toning_HighlightsHue_Next_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement set value slider
        with uuid('7ea3368f-7f6a-4ba8-90fe-04daf9e93e4c') as case:
            keyframe_room_page.fix_enhance.split_toning.highlights_hue.set_slider(70)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.9.3_Fix_Enhance_Split_toning_HighlightsHue_Set_Slider.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.9.3_Fix_Enhance_Split_toning_HighlightsHue_Set_Slider.png',
                preview_result)
            case.result = image_result

        # color enhancement set value input
        with uuid('7d4db012-231a-445b-81de-7b33b4509943') as case:
            keyframe_room_page.fix_enhance.split_toning.highlights_hue.set_value(90)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.9.4_Fix_Enhance_Split_toning_HighlightsHue_Set_Value.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.9.4_Fix_Enhance_Split_toning_HighlightsHue_Set_Value.png',
                preview_result)
            case.result = image_result

        # color enhancement set value arrow
        with uuid('589b455b-0ada-41f5-a91c-2c14e7aeb983') as case:
            keyframe_room_page.fix_enhance.split_toning.highlights_hue.click_stepper_up(times=3)
            keyframe_room_page.fix_enhance.split_toning.highlights_hue.click_stepper_down(times=1)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.9.5_Fix_Enhance_Split_toning_HighlightsHue_Set_Arrow.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.9.5_Fix_Enhance_Split_toning_HighlightsHue_Set_Arrow.png',
                preview_result)
            case.result = image_result

        # color enhancement reset
        with uuid('a114f252-f789-43dc-af1c-f282f9160626') as case:
            keyframe_room_page.fix_enhance.split_toning.highlights_hue.reset_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.9.6_Fix_Enhance_Split_toning_HighlightsHue_Reset.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.9.6_Fix_Enhance_Split_toning_HighlightsHue_Reset.png',
                preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_10(self):
        # split toning highlights saturation add/remove keyframe
        with uuid('67d61988-dc44-4034-91e5-3df84d951ec4') as case:
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.split_toning.highlights_saturation.show()
            keyframe_room_page.fix_enhance.split_toning.highlights_saturation.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.10.0_Fix_Enhance_Split_toning_HighlightsSaturation_Add_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.10.0_Fix_Enhance_Split_toning_HighlightsSaturation_Add_Keyframe.png',
                        preview_result)
            case.result = image_result

        # color enhancement previous keyframe
        with uuid('994898c2-098c-43e3-9183-7b72a3c4fdcb') as case:
            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            keyframe_room_page.fix_enhance.split_toning.highlights_saturation.add_remove_keyframe()
            keyframe_room_page.fix_enhance.split_toning.highlights_saturation.previous_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.10.1_Fix_Enhance_Split_toning_HighlightsSaturation_Previous_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.10.1_Fix_Enhance_Split_toning_HighlightsSaturation_Previous_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement next keyframe
        with uuid('e19ce06d-6515-408a-ae53-f2d0eab1e25c') as case:
            keyframe_room_page.fix_enhance.split_toning.highlights_saturation.next_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.10.2_Fix_Enhance_Split_toning_HighlightsSaturation_Next_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.10.2_Fix_Enhance_Split_toning_HighlightsSaturation_Next_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement set value slider
        with uuid('4c24d1fc-d4f1-41aa-b222-d13e350d8b26') as case:
            keyframe_room_page.fix_enhance.split_toning.highlights_saturation.set_slider(70)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.10.3_Fix_Enhance_Split_toning_HighlightsSaturation_Set_Slider.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.10.3_Fix_Enhance_Split_toning_HighlightsSaturation_Set_Slider.png',
                preview_result)
            case.result = image_result

        # color enhancement set value input
        with uuid('c8e57fb9-527c-4847-a5e8-763a51af6632') as case:
            keyframe_room_page.fix_enhance.split_toning.highlights_saturation.set_value(90)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.10.4_Fix_Enhance_Split_toning_HighlightsSaturation_Set_Value.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.10.4_Fix_Enhance_Split_toning_HighlightsSaturation_Set_Value.png',
                preview_result)
            case.result = image_result

        # color enhancement set value arrow
        with uuid('e0ec3f01-f25b-4cb0-803b-a7025b51a9df') as case:
            keyframe_room_page.fix_enhance.split_toning.highlights_saturation.click_stepper_up(times=3)
            keyframe_room_page.fix_enhance.split_toning.highlights_saturation.click_stepper_down(times=1)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.10.5_Fix_Enhance_Split_toning_HighlightsSaturation_Set_Arrow.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.10.5_Fix_Enhance_Split_toning_HighlightsSaturation_Set_Arrow.png',
                preview_result)
            case.result = image_result

        # color enhancement reset
        with uuid('cb8a2039-e471-4058-90e0-afb6c36565f9') as case:
            keyframe_room_page.fix_enhance.split_toning.highlights_saturation.reset_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.10.6_Fix_Enhance_Split_toning_HighlightsSaturation_Reset.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.10.6_Fix_Enhance_Split_toning_HighlightsSaturation_Reset.png',
                preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_11(self):
        # split toning balance add/remove keyframe
        with uuid('4534b8a7-a203-497a-8fb0-7b5ab135fde9') as case:
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.split_toning.balance.show()
            keyframe_room_page.fix_enhance.split_toning.balance.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.11.0_Fix_Enhance_Split_toning_Balance_Add_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.11.0_Fix_Enhance_Split_toning_Balance_Add_Keyframe.png',
                        preview_result)
            case.result = image_result

        # color enhancement previous keyframe
        with uuid('fe2152f4-359a-411a-bf12-6a7f6b747a31') as case:
            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            keyframe_room_page.fix_enhance.split_toning.balance.add_remove_keyframe()
            keyframe_room_page.fix_enhance.split_toning.balance.previous_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.11.1_Fix_Enhance_Split_toning_Balance_Previous_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.11.1_Fix_Enhance_Split_toning_Balance_Previous_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement next keyframe
        with uuid('6b83cb34-d6f4-4881-a0f4-599bac30c455') as case:
            keyframe_room_page.fix_enhance.split_toning.balance.next_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.11.2_Fix_Enhance_Split_toning_Balance_Next_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.11.2_Fix_Enhance_Split_toning_Balance_Next_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement set value slider
        with uuid('6efb0aa0-ef69-45f2-a3f6-6e60135b830e') as case:
            keyframe_room_page.fix_enhance.split_toning.balance.set_slider(70)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.11.3_Fix_Enhance_Split_toning_Balance_Set_Slider.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.11.3_Fix_Enhance_Split_toning_Balance_Set_Slider.png',
                preview_result)
            case.result = image_result

        # color enhancement set value input
        with uuid('178a66c7-fc95-4092-8d9a-867b4ee1967b') as case:
            keyframe_room_page.fix_enhance.split_toning.balance.set_value(90)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.11.4_Fix_Enhance_Split_toning_Balance_Set_Value.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.11.4_Fix_Enhance_Split_toning_Balance_Set_Value.png',
                preview_result)
            case.result = image_result

        # color enhancement set value arrow
        with uuid('8e5ed449-d688-4360-ad45-9d70b6ac8000') as case:
            keyframe_room_page.fix_enhance.split_toning.balance.click_stepper_up(times=3)
            keyframe_room_page.fix_enhance.split_toning.balance.click_stepper_down(times=1)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.11.5_Fix_Enhance_Split_toning_Balance_Set_Arrow.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.11.5_Fix_Enhance_Split_toning_Balance_Set_Arrow.png',
                preview_result)
            case.result = image_result

        # color enhancement reset
        with uuid('e38b9d6a-a71c-4aec-9f8d-af1558146260') as case:
            keyframe_room_page.fix_enhance.split_toning.balance.reset_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.11.6_Fix_Enhance_Split_toning_Balance_Reset.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.11.6_Fix_Enhance_Split_toning_Balance_Reset.png',
                preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_12(self):
        # split toning shadow hue add/remove keyframe
        with uuid('477f93be-31fc-4fa9-9698-2f9348cffded') as case:
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.split_toning.shadow_hue.show()
            keyframe_room_page.fix_enhance.split_toning.shadow_hue.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.12.0_Fix_Enhance_Split_toning_ShadowHue_Add_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.12.0_Fix_Enhance_Split_toning_ShadowHue_Add_Keyframe.png',
                        preview_result)
            case.result = image_result

        # color enhancement previous keyframe
        with uuid('90fd2e01-75dc-4aa0-9708-9de9f886e340') as case:
            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            keyframe_room_page.fix_enhance.split_toning.shadow_hue.add_remove_keyframe()
            keyframe_room_page.fix_enhance.split_toning.shadow_hue.previous_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.12.1_Fix_Enhance_Split_toning_ShadowHue_Previous_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.12.1_Fix_Enhance_Split_toning_ShadowHue_Previous_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement next keyframe
        with uuid('f3de9d89-4579-4955-807c-0d7d19b28d76') as case:
            keyframe_room_page.fix_enhance.split_toning.shadow_hue.next_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.12.2_Fix_Enhance_Split_toning_ShadowHue_Next_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.12.2_Fix_Enhance_Split_toning_ShadowHue_Next_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement set value slider
        with uuid('b0b354ca-9097-4c91-a489-1135837511f3') as case:
            keyframe_room_page.fix_enhance.split_toning.shadow_hue.set_slider(70)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.12.3_Fix_Enhance_Split_toning_ShadowHue_Set_Slider.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.12.3_Fix_Enhance_Split_toning_ShadowHue_Set_Slider.png',
                preview_result)
            case.result = image_result

        # color enhancement set value input
        with uuid('9f6a3de7-e93a-4588-a85a-53b96e505356') as case:
            keyframe_room_page.fix_enhance.split_toning.shadow_hue.set_value(90)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.12.4_Fix_Enhance_Split_toning_ShadowHue_Set_Value.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.12.4_Fix_Enhance_Split_toning_ShadowHue_Set_Value.png',
                preview_result)
            case.result = image_result

        # color enhancement set value arrow
        with uuid('c4123ca4-b0fe-4b0b-b45a-3e860cae8958') as case:
            keyframe_room_page.fix_enhance.split_toning.shadow_hue.click_stepper_up(times=3)
            keyframe_room_page.fix_enhance.split_toning.shadow_hue.click_stepper_down(times=1)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.12.5_Fix_Enhance_Split_toning_ShadowHue_Set_Arrow.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.12.5_Fix_Enhance_Split_toning_ShadowHue_Set_Arrow.png',
                preview_result)
            case.result = image_result

        # color enhancement reset
        with uuid('bfb12847-ca32-4981-9a7a-338bbe1c91e7') as case:
            keyframe_room_page.fix_enhance.split_toning.shadow_hue.reset_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.12.6_Fix_Enhance_Split_toning_ShadowHue_Reset.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.12.6_Fix_Enhance_Split_toning_ShadowHue_Reset.png',
                preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_13(self):
        # split toning shadow saturation add/remove keyframe
        with uuid('20ca46f9-4497-42b7-83d2-db2fda0cd407') as case:
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.split_toning.shadow_saturation.show()
            keyframe_room_page.fix_enhance.split_toning.shadow_saturation.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.13.0_Fix_Enhance_Split_toning_ShadowSaturation_Add_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.13.0_Fix_Enhance_Split_toning_ShadowSaturation_Add_Keyframe.png',
                        preview_result)
            case.result = image_result

        # color enhancement previous keyframe
        with uuid('dd11f518-0456-48a6-98d5-99e766a0c0e2') as case:
            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            keyframe_room_page.fix_enhance.split_toning.shadow_saturation.add_remove_keyframe()
            keyframe_room_page.fix_enhance.split_toning.shadow_saturation.previous_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.13.1_Fix_Enhance_Split_toning_ShadowSaturation_Previous_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.13.1_Fix_Enhance_Split_toning_ShadowSaturation_Previous_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement next keyframe
        with uuid('efb03994-b1d3-43b0-9f47-99d778f19283') as case:
            keyframe_room_page.fix_enhance.split_toning.shadow_saturation.next_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.13.2_Fix_Enhance_Split_toning_ShadowSaturation_Next_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.13.2_Fix_Enhance_Split_toning_ShadowSaturation_Next_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement set value slider
        with uuid('45c891e0-a12e-4071-aebf-d77cd5019bcc') as case:
            keyframe_room_page.fix_enhance.split_toning.shadow_saturation.set_slider(70)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.13.3_Fix_Enhance_Split_toning_ShadowSaturation_Set_Slider.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.13.3_Fix_Enhance_Split_toning_ShadowSaturation_Set_Slider.png',
                preview_result)
            case.result = image_result

        # color enhancement set value input
        with uuid('c1f83f11-c29a-4a0e-9b77-69b0b8a29f6e') as case:
            keyframe_room_page.fix_enhance.split_toning.shadow_saturation.set_value(90)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.13.4_Fix_Enhance_Split_toning_ShadowSaturation_Set_Value.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.13.4_Fix_Enhance_Split_toning_ShadowSaturation_Set_Value.png',
                preview_result)
            case.result = image_result

        # color enhancement set value arrow
        with uuid('cffcf612-7a97-44ef-a327-29397bee3bbd') as case:
            keyframe_room_page.fix_enhance.split_toning.shadow_saturation.click_stepper_up(times=3)
            keyframe_room_page.fix_enhance.split_toning.shadow_saturation.click_stepper_down(times=1)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.13.5_Fix_Enhance_Split_toning_ShadowSaturation_Set_Arrow.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.13.5_Fix_Enhance_Split_toning_ShadowSaturation_Set_Arrow.png',
                preview_result)
            case.result = image_result

        # color enhancement reset
        with uuid('eae9ef75-1187-4a27-8428-8dff7f5a727a') as case:
            keyframe_room_page.fix_enhance.split_toning.shadow_saturation.reset_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.13.6_Fix_Enhance_Split_toning_ShadowSaturation_Reset.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.13.6_Fix_Enhance_Split_toning_ShadowSaturation_Reset.png',
                preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_14(self):
        # lighting adjustment add/remove keyframe
        with uuid('6560b1f9-6f58-4953-bd90-b03dab3fc95d') as case:
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.lighting_adjustment.extreme_backlight.show()
            keyframe_room_page.fix_enhance.lighting_adjustment.extreme_backlight.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.14.0_Fix_Enhance_Lighting_Adjustment_ExtremeBacklight_Add_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.14.0_Fix_Enhance_Lighting_Adjustment_ExtremeBacklight_Add_Keyframe.png',
                        preview_result)
            case.result = image_result

        # color enhancement previous keyframe
        with uuid('a1f1bee5-1ffc-4a18-9e93-e0037ed123c7') as case:
            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            keyframe_room_page.fix_enhance.lighting_adjustment.extreme_backlight.add_remove_keyframe()
            keyframe_room_page.fix_enhance.lighting_adjustment.extreme_backlight.previous_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.14.1_Fix_Enhance_Lighting_Adjustment_ExtremeBacklight_Previous_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.14.1_Fix_Enhance_Lighting_Adjustment_ExtremeBacklight_Previous_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement next keyframe
        with uuid('6e7f0044-17f4-4ac9-8386-9c66e35b01de') as case:
            keyframe_room_page.fix_enhance.lighting_adjustment.extreme_backlight.next_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.14.2_Fix_Enhance_Lighting_Adjustment_ExtremeBacklight_Next_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.14.2_Fix_Enhance_Lighting_Adjustment_ExtremeBacklight_Next_Keyframe.png',
                preview_result)
            case.result = image_result

        # remove keyframe
        with uuid('2c03bc6f-2c16-46de-bfc4-1fc75c2f95a0') as case:
            keyframe_room_page.fix_enhance.lighting_adjustment.extreme_backlight.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.14.3_Fix_Enhance_Lighting_Adjustment_ExtremeBacklight_Remove_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.14.3_Fix_Enhance_Lighting_Adjustment_ExtremeBacklight_Remove_Keyframe.png',
                preview_result)
            case.result = image_result

        # check box
        with uuid('a2677b22-4aac-4ccb-b991-1ad06699e052') as case:
            keyframe_room_page.fix_enhance.lighting_adjustment.extreme_backlight.add_remove_keyframe()
            keyframe_room_page.fix_enhance.lighting_adjustment.extreme_backlight.set_checkbox()
            time.sleep(DELAY_TIME * 5)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.14.4_Fix_Enhance_Lighting_Adjustment_ExtremeBacklight_Set_Check.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.14.4_Fix_Enhance_Lighting_Adjustment_ExtremeBacklight_Set_Check.png',
                preview_result)
            case.result = image_result

        # color enhancement reset
        with uuid('7d9fa566-47f7-4374-9dce-bd10023b8549') as case:
            keyframe_room_page.fix_enhance.lighting_adjustment.extreme_backlight.reset_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.14.5_Fix_Enhance_Lighting_Adjustment_ExtremeBacklight_Reset.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.14.5_Fix_Enhance_Lighting_Adjustment_ExtremeBacklight_Reset.png',
                preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_15(self):
        # lighting adjustment degree add/remove keyframe
        with uuid('d9c65045-c587-4da8-b94a-0e66e4c38ee6') as case:
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.lighting_adjustment.degree.show()
            keyframe_room_page.fix_enhance.lighting_adjustment.degree.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.15.0_Fix_Enhance_Lighting_Adjustment_Degree_Add_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.15.0_Fix_Enhance_Lighting_Adjustment_Degree_Add_Keyframe.png',
                        preview_result)
            case.result = image_result

        # color enhancement previous keyframe
        with uuid('e6153079-46c4-4cea-9ab2-a73ffb1fdee5') as case:
            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            keyframe_room_page.fix_enhance.lighting_adjustment.degree.add_remove_keyframe()
            keyframe_room_page.fix_enhance.lighting_adjustment.degree.previous_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.15.1_Fix_Enhance_Lighting_Adjustment_Degree_Previous_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.15.1_Fix_Enhance_Lighting_Adjustment_Degree_Previous_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement next keyframe
        with uuid('54c2ec4c-1f4f-425a-b0d4-5b21d8c198e3') as case:
            keyframe_room_page.fix_enhance.lighting_adjustment.degree.next_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.15.2_Fix_Enhance_Lighting_Adjustment_Degree_Next_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.15.2_Fix_Enhance_Lighting_Adjustment_Degree_Next_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement set value slider
        with uuid('97721d7f-6aa4-4632-a6fb-8f1f599b8d21') as case:
            keyframe_room_page.fix_enhance.lighting_adjustment.degree.set_slider(70)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.15.3_Fix_Enhance_Lighting_Adjustment_Degree_Set_Slider.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.15.3_Fix_Enhance_Lighting_Adjustment_Degree_Set_Slider.png',
                preview_result)
            case.result = image_result

        # color enhancement set value input
        with uuid('c8094c31-abe5-4666-bf67-79f43a799cd2') as case:
            keyframe_room_page.fix_enhance.lighting_adjustment.degree.set_value(90)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.15.4_Fix_Enhance_Lighting_Adjustment_Degree_Set_Value.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.15.4_Fix_Enhance_Lighting_Adjustment_Degree_Set_Value.png',
                preview_result)
            case.result = image_result

        # color enhancement set value arrow
        with uuid('d86d1d5d-891f-4c89-9093-3a3c06f2f001') as case:
            keyframe_room_page.fix_enhance.lighting_adjustment.degree.click_stepper_up(times=3)
            keyframe_room_page.fix_enhance.lighting_adjustment.degree.click_stepper_down(times=1)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.15.5_Fix_Enhance_Lighting_Adjustment_Degree_Set_Arrow.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.15.5_Fix_Enhance_Lighting_Adjustment_Degree_Set_Arrow.png',
                preview_result)
            case.result = image_result

        # color enhancement reset
        with uuid('dac81885-53bc-4501-9efe-63c876a335b5') as case:
            keyframe_room_page.fix_enhance.lighting_adjustment.degree.reset_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.15.6_Fix_Enhance_Lighting_Adjustment_Degree_Reset.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.15.6_Fix_Enhance_Lighting_Adjustment_Degree_Reset.png',
                preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_16(self):
        # video denoise degree add/remove keyframe
        with uuid('3184c18f-8bf6-4e1e-8af1-8fe7b2b4bd1c') as case:
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.video_denoise.degree.show()
            keyframe_room_page.drag_scroll_bar(0.18)
            keyframe_room_page.fix_enhance.video_denoise.degree.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.16.0_Fix_Enhance_Video_Denoise_Degree_Add_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.16.0_Fix_Enhance_Video_Denoise_Degree_Add_Keyframe.png',
                        preview_result)
            case.result = image_result

        # color enhancement previous keyframe
        with uuid('3f09c7a9-5370-4883-8258-aad59323e2e6') as case:
            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            keyframe_room_page.fix_enhance.video_denoise.degree.add_remove_keyframe()
            keyframe_room_page.fix_enhance.video_denoise.degree.previous_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.16.1_Fix_Enhance_Video_Denoise_Degree_Previous_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.16.1_Fix_Enhance_Video_Denoise_Degree_Previous_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement next keyframe
        with uuid('d0fc3fc6-6eb0-428c-8370-15c0410f959c') as case:
            keyframe_room_page.fix_enhance.video_denoise.degree.next_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.16.2_Fix_Enhance_Video_Denoise_Degree_Next_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.16.2_Fix_Enhance_Video_Denoise_Degree_Next_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement set value slider
        with uuid('bdfd6c40-fe57-4c11-a6db-a43e1e66cf75') as case:
            keyframe_room_page.fix_enhance.video_denoise.degree.set_slider(70)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.16.3_Fix_Enhance_Video_Denoise_Degree_Set_Slider.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.16.3_Fix_Enhance_Video_Denoise_Degree_Set_Slider.png',
                preview_result)
            case.result = image_result

        # color enhancement set value input
        with uuid('087b6dec-75d7-4f66-b78b-287d605eac97') as case:
            keyframe_room_page.fix_enhance.video_denoise.degree.set_value(90)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.16.4_Fix_Enhance_Video_Denoise_Degree_Set_Value.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.16.4_Fix_Enhance_Video_Denoise_Degree_Set_Value.png',
                preview_result)
            case.result = image_result

        # color enhancement set value arrow
        with uuid('575cf05c-4b04-411c-b2f7-70cdd7b1999b') as case:
            keyframe_room_page.fix_enhance.video_denoise.degree.click_stepper_up(times=3)
            keyframe_room_page.fix_enhance.video_denoise.degree.click_stepper_down(times=1)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.16.5_Fix_Enhance_Video_Denoise_Degree_Set_Arrow.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.16.5_Fix_Enhance_Video_Denoise_Degree_Set_Arrow.png',
                preview_result)
            case.result = image_result

        # color enhancement reset
        with uuid('a3c57f13-11cf-4cd8-a509-cbd29ed4a9d9') as case:
            keyframe_room_page.fix_enhance.video_denoise.degree.reset_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.16.6_Fix_Enhance_Video_Denoise_Degree_Reset.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.16.6_Fix_Enhance_Video_Denoise_Degree_Reset.png',
                preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_17(self):
        # HDR glow strength add/remove keyframe
        with uuid('c8727fec-fd2c-44cd-bda1-73d7c983d87c') as case:
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.hdr_effect.glow_strength.show()
            keyframe_room_page.fix_enhance.hdr_effect.glow_strength.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.17.0_Fix_Enhance_HDR_Effect_GlowStrength_Add_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.17.0_Fix_Enhance_HDR_Effect_GlowStrength_Add_Keyframe.png',
                        preview_result)
            case.result = image_result

        # color enhancement previous keyframe
        with uuid('6d8feb73-70ee-4fc9-9e60-e1a7b41c3f84') as case:
            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            keyframe_room_page.fix_enhance.hdr_effect.glow_strength.add_remove_keyframe()
            keyframe_room_page.fix_enhance.hdr_effect.glow_strength.previous_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.17.1_Fix_Enhance_HDR_Effect_GlowStrength_Previous_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.17.1_Fix_Enhance_HDR_Effect_GlowStrength_Previous_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement next keyframe
        with uuid('b4d7625a-1d48-4dd3-b8c1-56794ac72bd3') as case:
            keyframe_room_page.fix_enhance.hdr_effect.glow_strength.next_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.17.2_Fix_Enhance_HDR_Effect_GlowStrength_Next_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.17.2_Fix_Enhance_HDR_Effect_GlowStrength_Next_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement set value slider
        with uuid('fdf18227-2789-4230-b8ca-73df11c56b1b') as case:
            keyframe_room_page.fix_enhance.hdr_effect.glow_strength.set_slider(70)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.17.3_Fix_Enhance_HDR_Effect_GlowStrength_Set_Slider.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.17.3_Fix_Enhance_HDR_Effect_GlowStrength_Set_Slider.png',
                preview_result)
            case.result = image_result

        # color enhancement set value input
        with uuid('4deb6ca6-1432-4986-8530-2391fa362891') as case:
            keyframe_room_page.fix_enhance.hdr_effect.glow_strength.set_value(90)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.17.4_Fix_Enhance_HDR_Effect_GlowStrength_Set_Value.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.17.4_Fix_Enhance_HDR_Effect_GlowStrength_Set_Value.png',
                preview_result)
            case.result = image_result

        # color enhancement set value arrow
        with uuid('aa373dbb-a9c3-45e1-918a-73c94f52d181') as case:
            keyframe_room_page.fix_enhance.hdr_effect.glow_strength.click_stepper_up(times=3)
            keyframe_room_page.fix_enhance.hdr_effect.glow_strength.click_stepper_down(times=1)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.17.5_Fix_Enhance_HDR_Effect_GlowStrength_Set_Arrow.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.17.5_Fix_Enhance_HDR_Effect_GlowStrength_Set_Arrow.png',
                preview_result)
            case.result = image_result

        # color enhancement reset
        with uuid('070b1534-dfab-4108-9335-4fee0adc10ac') as case:
            keyframe_room_page.fix_enhance.hdr_effect.glow_strength.reset_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.17.6_Fix_Enhance_HDR_Effect_GlowStrength_Reset.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.17.6_Fix_Enhance_HDR_Effect_GlowStrength_Reset.png',
                preview_result)
            case.result = image_result

        # glow strength set to 0 glow radius disabled
        with uuid('48aa8f87-d8d4-42cf-81d1-660252ec534e') as case:
            with uuid('5c561c09-3d2d-42d9-a2f7-a4f10b463b63') as case:
                keyframe_room_page.fix_enhance.hdr_effect.glow_strength.set_value(0)
                time.sleep(DELAY_TIME)
                keyframe_room_page.fix_enhance.hdr_effect.glow_radius.show()
                preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                             file_name=Auto_Ground_Truth_Folder + 'G1.17.7_Fix_Enhance_HDR_Effect_GlowRadius_Disabled.png')
                image_result = keyframe_room_page.compare(
                    Ground_Truth_Folder + 'G1.17.7_Fix_Enhance_HDR_Effect_GlowRadius_Disabled.png',
                    preview_result)
                case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_18(self):
        # HDR glow radius add/remove keyframe
        with uuid('19ff85fc-4694-420a-bcdf-a83bc16a2188') as case:
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.hdr_effect.glow_radius.show()
            keyframe_room_page.fix_enhance.hdr_effect.glow_radius.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.18.0_Fix_Enhance_HDR_Effect_GlowRadius_Add_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.18.0_Fix_Enhance_HDR_Effect_GlowRadius_Add_Keyframe.png',
                        preview_result)
            case.result = image_result

        # color enhancement previous keyframe
        with uuid('1f0b761b-1d8a-4d9c-900a-3aef29106cf8') as case:
            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            keyframe_room_page.fix_enhance.hdr_effect.glow_radius.add_remove_keyframe()
            keyframe_room_page.fix_enhance.hdr_effect.glow_radius.previous_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.18.1_Fix_Enhance_HDR_Effect_GlowRadius_Previous_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.18.1_Fix_Enhance_HDR_Effect_GlowRadius_Previous_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement next keyframe
        with uuid('46e3c542-fb1d-40b3-8ee2-1b3fed23f707') as case:
            keyframe_room_page.fix_enhance.hdr_effect.glow_radius.next_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.18.2_Fix_Enhance_HDR_Effect_GlowRadius_Next_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.18.2_Fix_Enhance_HDR_Effect_GlowRadius_Next_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement set value slider
        with uuid('6bd467da-74de-4e7a-8e06-863b174eb0a5') as case:
            keyframe_room_page.fix_enhance.hdr_effect.glow_radius.set_slider(20)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.18.3_Fix_Enhance_HDR_Effect_GlowRadius_Set_Slider.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.18.3_Fix_Enhance_HDR_Effect_GlowRadius_Set_Slider.png',
                preview_result)
            case.result = image_result

        # color enhancement set value input
        with uuid('1ed71e52-6c5d-4d6c-988f-35fd47f9c9c6') as case:
            keyframe_room_page.fix_enhance.hdr_effect.glow_radius.set_value(40)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.18.4_Fix_Enhance_HDR_Effect_GlowRadius_Set_Value.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.18.4_Fix_Enhance_HDR_Effect_GlowRadius_Set_Value.png',
                preview_result)
            case.result = image_result

        # color enhancement set value arrow
        with uuid('7d818b91-df62-4d27-808c-261cac149806') as case:
            keyframe_room_page.fix_enhance.hdr_effect.glow_radius.click_stepper_up(times=3)
            keyframe_room_page.fix_enhance.hdr_effect.glow_radius.click_stepper_down(times=1)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.18.5_Fix_Enhance_HDR_Effect_GlowRadius_Set_Arrow.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.18.5_Fix_Enhance_HDR_Effect_GlowRadius_Set_Arrow.png',
                preview_result)
            case.result = image_result

        # color enhancement reset
        with uuid('3f56a037-c155-4fcc-b109-148ab61fa737') as case:
            keyframe_room_page.fix_enhance.hdr_effect.glow_radius.reset_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.18.6_Fix_Enhance_HDR_Effect_GlowRadius_Reset.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.18.6_Fix_Enhance_HDR_Effect_GlowRadius_Reset.png',
                preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_19(self):
        # HDR glow balance add/remove keyframe
        with uuid('5783a87d-ff6b-4854-b970-ba3416bd0e13') as case:
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.hdr_effect.glow_balance.show()
            keyframe_room_page.fix_enhance.hdr_effect.glow_balance.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.19.0_Fix_Enhance_HDR_Effect_GlowBalance_Add_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.19.0_Fix_Enhance_HDR_Effect_GlowBalance_Add_Keyframe.png',
                        preview_result)
            case.result = image_result

        # color enhancement previous keyframe
        with uuid('68b41937-59e1-4832-a36e-65ccd6665861') as case:
            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            keyframe_room_page.fix_enhance.hdr_effect.glow_balance.add_remove_keyframe()
            keyframe_room_page.fix_enhance.hdr_effect.glow_balance.previous_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.19.1_Fix_Enhance_HDR_Effect_GlowBalance_Previous_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.19.1_Fix_Enhance_HDR_Effect_GlowBalance_Previous_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement next keyframe
        with uuid('9ad619c5-6a60-4ab6-92bf-a7b0c2a674bf') as case:
            keyframe_room_page.fix_enhance.hdr_effect.glow_balance.next_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.19.2_Fix_Enhance_HDR_Effect_GlowBalance_Next_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.19.2_Fix_Enhance_HDR_Effect_GlowBalance_Next_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement set value slider
        with uuid('2bed0ea7-246b-4adc-a900-f84fda83065a') as case:
            keyframe_room_page.fix_enhance.hdr_effect.glow_balance.set_slider(40)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.19.3_Fix_Enhance_HDR_Effect_GlowBalance_Set_Slider.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.19.3_Fix_Enhance_HDR_Effect_GlowBalance_Set_Slider.png',
                preview_result)
            case.result = image_result

        # color enhancement set value input
        with uuid('3bb44b91-07cc-49ac-adbd-7adb4e6e05d0') as case:
            keyframe_room_page.fix_enhance.hdr_effect.glow_balance.set_value(-40)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.19.4_Fix_Enhance_HDR_Effect_GlowBalance_Set_Value.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.19.4_Fix_Enhance_HDR_Effect_GlowBalance_Set_Value.png',
                preview_result)
            case.result = image_result

        # color enhancement set value arrow
        with uuid('8bfe1a30-5f76-4a9b-9e1e-585cfbed6d26') as case:
            keyframe_room_page.fix_enhance.hdr_effect.glow_balance.click_stepper_up(times=3)
            keyframe_room_page.fix_enhance.hdr_effect.glow_balance.click_stepper_down(times=1)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.19.5_Fix_Enhance_HDR_Effect_GlowBalance_Set_Arrow.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.19.5_Fix_Enhance_HDR_Effect_GlowBalance_Set_Arrow.png',
                preview_result)
            case.result = image_result

        # color enhancement reset
        with uuid('a3431384-69df-4408-b760-14c7b05d2db0') as case:
            keyframe_room_page.fix_enhance.hdr_effect.glow_balance.reset_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.19.6_Fix_Enhance_HDR_Effect_GlowBalance_Reset.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.19.6_Fix_Enhance_HDR_Effect_GlowBalance_Reset.png',
                preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_20(self):
        # HDR edge strength add/remove keyframe
        with uuid('d486a711-aea4-4400-b17f-c00cab7b9905') as case:
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.hdr_effect.edge_strength.show()
            keyframe_room_page.fix_enhance.hdr_effect.edge_strength.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.20.0_Fix_Enhance_HDR_Effect_EdgeStrength_Add_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.20.0_Fix_Enhance_HDR_Effect_EdgeStrength_Add_Keyframe.png',
                        preview_result)
            case.result = image_result

        # color enhancement previous keyframe
        with uuid('20fc6092-e05c-4de3-be05-beecc0958fde') as case:
            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            keyframe_room_page.fix_enhance.hdr_effect.edge_strength.add_remove_keyframe()
            keyframe_room_page.fix_enhance.hdr_effect.edge_strength.previous_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.20.1_Fix_Enhance_HDR_Effect_EdgeStrength_Previous_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.20.1_Fix_Enhance_HDR_Effect_EdgeStrength_Previous_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement next keyframe
        with uuid('8b2faa7f-455c-4d1b-a362-bf4e173c7cf4') as case:
            keyframe_room_page.fix_enhance.hdr_effect.edge_strength.next_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.20.2_Fix_Enhance_HDR_Effect_EdgeStrength_Next_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.20.2_Fix_Enhance_HDR_Effect_EdgeStrength_Next_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement set value slider
        with uuid('4ac8d857-3692-4b60-8521-eb1a714a45c9') as case:
            keyframe_room_page.fix_enhance.hdr_effect.edge_strength.set_slider(-10)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.20.3_Fix_Enhance_HDR_Effect_EdgeStrength_Set_Slider.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.20.3_Fix_Enhance_HDR_Effect_EdgeStrength_Set_Slider.png',
                preview_result)
            case.result = image_result

        # color enhancement set value input
        with uuid('44d845f6-1b87-402e-b0bd-70062a72083b') as case:
            keyframe_room_page.fix_enhance.hdr_effect.edge_strength.set_value(30)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.20.4_Fix_Enhance_HDR_Effect_EdgeStrength_Set_Value.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.20.4_Fix_Enhance_HDR_Effect_EdgeStrength_Set_Value.png',
                preview_result)
            case.result = image_result

        # color enhancement set value arrow
        with uuid('0e034b69-aa49-4846-b742-0ef6b22aba3b') as case:
            keyframe_room_page.fix_enhance.hdr_effect.edge_strength.click_stepper_up(times=3)
            keyframe_room_page.fix_enhance.hdr_effect.edge_strength.click_stepper_down(times=1)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.20.5_Fix_Enhance_HDR_Effect_EdgeStrength_Set_Arrow.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.20.5_Fix_Enhance_HDR_Effect_EdgeStrength_Set_Arrow.png',
                preview_result)
            case.result = image_result

        # color enhancement reset
        with uuid('eedab962-9c38-4ea1-9a16-91ca13fc69cb') as case:
            keyframe_room_page.fix_enhance.hdr_effect.edge_strength.reset_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.20.6_Fix_Enhance_HDR_Effect_EdgeStrength_Reset.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.20.6_Fix_Enhance_HDR_Effect_EdgeStrength_Reset.png',
                preview_result)
            case.result = image_result

        # edge strength set to 0
        with uuid('006afb9d-d0df-4738-bd16-4477afdf4638') as case:
            with uuid('24c111ee-ffa4-4575-97ea-3b9cca4b73f8') as case:
                keyframe_room_page.fix_enhance.hdr_effect.edge_balance.show()
                keyframe_room_page.fix_enhance.hdr_effect.edge_strength.set_value(0)
                time.sleep(DELAY_TIME)
                preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                             file_name=Auto_Ground_Truth_Folder + 'G1.20.7_Fix_Enhance_HDR_Effect_EdgeStrength_Set_To_0.png')
                image_result = keyframe_room_page.compare(
                    Ground_Truth_Folder + 'G1.20.7_Fix_Enhance_HDR_Effect_EdgeStrength_Set_To_0.png',
                    preview_result)
                case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_21(self):
        # HDR edge radius add/remove keyframe
        with uuid('77b7ec77-cef6-48b0-8cbe-95b702746f0f') as case:
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.hdr_effect.edge_radius.show()
            keyframe_room_page.fix_enhance.hdr_effect.edge_strength.set_value(20)
            time.sleep(DELAY_TIME * 2)
            keyframe_room_page.fix_enhance.hdr_effect.edge_radius.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.21.0_Fix_Enhance_HDR_Effect_EdgeRadius_Add_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.21.0_Fix_Enhance_HDR_Effect_EdgeRadius_Add_Keyframe.png',
                        preview_result)
            case.result = image_result

        # color enhancement previous keyframe
        with uuid('3d5346a2-a840-4357-8524-2cd4665cf059') as case:
            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            keyframe_room_page.fix_enhance.hdr_effect.edge_radius.add_remove_keyframe()
            keyframe_room_page.fix_enhance.hdr_effect.edge_radius.previous_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.21.1_Fix_Enhance_HDR_Effect_EdgeRadius_Previous_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.21.1_Fix_Enhance_HDR_Effect_EdgeRadius_Previous_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement next keyframe
        with uuid('e8ca4e53-0d09-47d3-96a7-9d582bdf831f') as case:
            keyframe_room_page.fix_enhance.hdr_effect.edge_radius.next_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.21.2_Fix_Enhance_HDR_Effect_EdgeRadius_Next_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.21.2_Fix_Enhance_HDR_Effect_EdgeRadius_Next_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement set value slider
        with uuid('e148bff1-e965-41b7-a993-16d06ff2617a') as case:
            keyframe_room_page.fix_enhance.hdr_effect.edge_radius.set_slider(20)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.21.3_Fix_Enhance_HDR_Effect_EdgeRadius_Set_Slider.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.21.3_Fix_Enhance_HDR_Effect_EdgeRadius_Set_Slider.png',
                preview_result)
            case.result = image_result

        # color enhancement set value input
        with uuid('00ad7f58-0470-444c-b860-dc88cbd3f1ae') as case:
            keyframe_room_page.fix_enhance.hdr_effect.edge_radius.set_value(30)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.21.4_Fix_Enhance_HDR_Effect_EdgeRadius_Set_Value.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.21.4_Fix_Enhance_HDR_Effect_EdgeRadius_Set_Value.png',
                preview_result)
            case.result = image_result

        # color enhancement set value arrow
        with uuid('9ff0379c-d9bf-4331-a053-952ce165d474') as case:
            keyframe_room_page.fix_enhance.hdr_effect.edge_radius.click_stepper_up(times=3)
            keyframe_room_page.fix_enhance.hdr_effect.edge_radius.click_stepper_down(times=1)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.21.5_Fix_Enhance_HDR_Effect_EdgeRadius_Set_Arrow.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.21.5_Fix_Enhance_HDR_Effect_EdgeRadius_Set_Arrow.png',
                preview_result)
            case.result = image_result

        # color enhancement reset
        with uuid('4d67d399-f055-4845-b754-cc91bb45d3ce') as case:
            keyframe_room_page.fix_enhance.hdr_effect.edge_radius.reset_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.21.6_Fix_Enhance_HDR_Effect_EdgeRadius_Reset.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.21.6_Fix_Enhance_HDR_Effect_EdgeRadius_Reset.png',
                preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_22(self):
        # HDR edge balance add/remove keyframe
        with uuid('44a17c57-3aff-4dfd-8cbc-3bf434c6a67f') as case:
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.select_timeline_media(track_index=0, clip_index=0)
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.hdr_effect.edge_balance.show()
            keyframe_room_page.fix_enhance.hdr_effect.edge_strength.set_value(20)
            time.sleep(DELAY_TIME * 2)
            keyframe_room_page.fix_enhance.hdr_effect.edge_balance.add_remove_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.22.0_Fix_Enhance_HDR_Effect_EdgeBalance_Add_Keyframe.png')
            image_result = keyframe_room_page.compare(Ground_Truth_Folder + 'G1.22.0_Fix_Enhance_HDR_Effect_EdgeBalance_Add_Keyframe.png',
                        preview_result)
            case.result = image_result

        # color enhancement previous keyframe
        with uuid('0ee0e8f8-452b-4d28-be8f-b958a85fa8e4') as case:
            library_preview_page.set_library_preview_window_timecode('00_00_07_00')
            keyframe_room_page.fix_enhance.hdr_effect.edge_balance.add_remove_keyframe()
            keyframe_room_page.fix_enhance.hdr_effect.edge_balance.previous_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.22.1_Fix_Enhance_HDR_Effect_EdgeBalance_Previous_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.22.1_Fix_Enhance_HDR_Effect_EdgeBalance_Previous_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement next keyframe
        with uuid('23b6b26e-351d-43cc-a030-71d6703732aa') as case:
            keyframe_room_page.fix_enhance.hdr_effect.edge_balance.next_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.22.2_Fix_Enhance_HDR_Effect_EdgeBalance_Next_Keyframe.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.22.2_Fix_Enhance_HDR_Effect_EdgeBalance_Next_Keyframe.png',
                preview_result)
            case.result = image_result

        # color enhancement set value slider
        with uuid('5ea18d20-8bf4-4646-846e-b0899a9c28b1') as case:
            keyframe_room_page.fix_enhance.hdr_effect.edge_balance.set_slider(-50)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.22.3_Fix_Enhance_HDR_Effect_EdgeBalance_Set_Slider.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.22.3_Fix_Enhance_HDR_Effect_EdgeBalance_Set_Slider.png',
                preview_result)
            case.result = image_result

        # color enhancement set value input
        with uuid('0260e9f7-7d81-4687-abc2-62633d61e0ae') as case:
            keyframe_room_page.fix_enhance.hdr_effect.edge_balance.set_value(30)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.22.4_Fix_Enhance_HDR_Effect_EdgeBalance_Set_Value.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.22.4_Fix_Enhance_HDR_Effect_EdgeBalance_Set_Value.png',
                preview_result)
            case.result = image_result

        # color enhancement set value arrow
        with uuid('a009bccf-88c8-400c-aac7-28d2a4124676') as case:
            keyframe_room_page.fix_enhance.hdr_effect.edge_balance.click_stepper_up(times=3)
            keyframe_room_page.fix_enhance.hdr_effect.edge_balance.click_stepper_down(times=1)
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.22.5_Fix_Enhance_HDR_Effect_EdgeBalance_Set_Arrow.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.22.5_Fix_Enhance_HDR_Effect_EdgeBalance_Set_Arrow.png',
                preview_result)
            case.result = image_result

        # color enhancement reset
        with uuid('647e36c9-d558-4946-9103-ff9039b9665f') as case:
            keyframe_room_page.fix_enhance.hdr_effect.edge_balance.reset_keyframe()
            time.sleep(DELAY_TIME)
            preview_result = keyframe_room_page.snapshot(locator=L.library_preview.upper_view_region,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.22.6_Fix_Enhance_HDR_Effect_EdgeBalance_Reset.png')
            image_result = keyframe_room_page.compare(
                Ground_Truth_Folder + 'G1.22.6_Fix_Enhance_HDR_Effect_EdgeBalance_Reset.png',
                preview_result)
            case.result = image_result




    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    119a702d-06f5-48f0-a0e1-5e37093f8424
                    740da49b-cf35-4957-b957-6bfc66835ce7
                    c601e2f1-10ee-4d9e-8486-62623fa42ffc
                    c5d031fe-9853-466f-ad98-db98d319ff0c
                    6930532b-28ed-4db8-b7c3-95b1849618b2
                    a2677b22-4aac-4ccb-b991-1ad06699e052
                    7d9fa566-47f7-4374-9dce-bd10023b8549
                    a1f1bee5-1ffc-4a18-9e93-e0037ed123c7
                    6560b1f9-6f58-4953-bd90-b03dab3fc95d
                    2c03bc6f-2c16-46de-bfc4-1fc75c2f95a0
                    6e7f0044-17f4-4ac9-8386-9c66e35b01de
                    97721d7f-6aa4-4632-a6fb-8f1f599b8d21
                    c8094c31-abe5-4666-bf67-79f43a799cd2
                    d86d1d5d-891f-4c89-9093-3a3c06f2f001
                    b670cffa-dd66-4b95-9fe9-1b48ecfcb2af
                    70357974-d98b-4a33-9c97-e8c6efc70b43
                    163c25b4-6d8c-469d-af60-21d6cdeac006
                    355e4ac1-a747-4117-b28c-a6d5824e2099
                    2bfd24af-b7a1-43c0-8dea-1afbc66adf55
                    ad5cdb25-4c24-4c67-a638-d2fdf8c48bec
                    3f517560-97a5-4695-ad7a-fec213476522
                    750e96f1-052b-4ad9-861f-5c36e03c4feb
                    85a62a7d-6d46-484b-afba-63004aa64ea1
                    fbab9e72-ff72-4ec8-ac4b-ca2993d20920
                    ee91ab54-d55c-4d75-9f5c-b8b45dac5e13
                    248cea4e-1b6e-48ed-957a-0d2336d4ac0f
                    ac77edca-3c19-4663-a8e8-287db4e18cb8
                    659c6418-658e-4e42-a45d-1dd3ed0f83d5
                    0f3436d5-0739-4161-97a8-cf08e4392d4d
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'
