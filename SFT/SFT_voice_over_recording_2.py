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
base_page = PageFactory().get_page_object('base_page', mwc)
title_designer_page = PageFactory().get_page_object('title_designer_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
voice_over_recording_page = PageFactory().get_page_object('voice_over_recording_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)


# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Voice-Over Recording Room_2.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Voice_Over_Recording_2/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Voice_Over_Recording_2/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1


class Test_Voice_Over_Recording_2():
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
            google_sheet_execution_log_init('Voice_Over_Recording_2')

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

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_1_1(self):
        with uuid('e16cb9f3-9298-4701-b473-5a37502836e2') as case:

            # 2.1.1.1 - Device - Audio Device - Click drop down list and select
            time.sleep(5)
            voice_over_recording_page.tap_VoiceRecordRoom_hotkey()
            # Verify if in "Voice Over" page
            is_in_voice_over = voice_over_recording_page.check_in_voice_over_recording_room()
            logger(f"{is_in_voice_over= }")
            if is_in_voice_over is not True:
                logger('Failed to enter Voice over page!')
                raise Exception
            # Enter Audio Setup page
            voice_over_recording_page.click_device_btn()
            # Please install this tool on AT server first (https://rogueamoeba.com/loopback/)
            # Due to MacOS12 cannot support Loopback Audio (Only MacOS10.15 support)
            #voice_over_recording_page.set_audio_setup_select_audio_device('Loopback Audio')
            voice_over_recording_page.click_audio_setup_ok_btn()
            # Enter Audio Setup page
            voice_over_recording_page.click_device_btn()
            # Snapshot current result
            time.sleep(DELAY_TIME)
            #current_image = voice_over_recording_page.snapshot(locator=L.voice_over_recording.menu_audio_device, file_name=Auto_Ground_Truth_Folder + '2-1-1-1_SelectDevice.png')
            #compare_result = voice_over_recording_page.compare(Ground_Truth_Folder + '2-1-1-1_SelectDevice.png', current_image)
            #logger(f"{compare_result= }")
            #case.result = compare_result

            # Check if AT platform has this audio device
            case.result = voice_over_recording_page.set_audio_setup_select_audio_device('External Microphone')
            

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_1_2(self):
        with uuid('0dec4eb5-5fb2-4bb4-aa3f-5d0f6c27e4ea') as case:
            # 2.1.1.2 - Device - Input Volume - Default
            time.sleep(5)
            voice_over_recording_page.tap_VoiceRecordRoom_hotkey()
            # Verify if in "Voice Over" page
            is_in_voice_over = voice_over_recording_page.check_in_voice_over_recording_room()
            logger(f"{is_in_voice_over= }")
            if is_in_voice_over is not True:
                logger('Failed to enter Voice over page!')
                raise Exception
            # Enter Audio Setup page`
            voice_over_recording_page.click_device_btn()
            voice_over_recording_page.set_audio_setup_audio_drag_input_volume(100)
            voice_over_recording_page.click_audio_setup_ok_btn()
            voice_over_recording_page.click_device_btn()
            time.sleep(DELAY_TIME)
            current_image = voice_over_recording_page.snapshot(locator=L.voice_over_recording.window_audio_setup, file_name=Auto_Ground_Truth_Folder + '2-1-1-2_Default.png')
            compare_result = voice_over_recording_page.compare(Ground_Truth_Folder + '2-1-1-2_Default.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid('ef08db9e-0928-48d5-834d-4cb19ed9ead6') as case:
            # 2.1.1.3 - Device - Input Volume - Max
            # Enter Audio Setup page
            voice_over_recording_page.set_audio_setup_audio_drag_input_volume(100)
            voice_over_recording_page.click_audio_setup_ok_btn()
            voice_over_recording_page.click_device_btn()
            time.sleep(DELAY_TIME)
            current_image2 = voice_over_recording_page.snapshot(locator=L.voice_over_recording.window_audio_setup, file_name=Auto_Ground_Truth_Folder + '2-1-1-3_Max.png')
            compare_result = voice_over_recording_page.compare(Ground_Truth_Folder + '2-1-1-3_Max.png', current_image2)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid('47d69da3-0709-4cec-933e-e748cabc3111') as case:
            # 2.1.1.4 - Device - Input Volume - Min
            # Enter Audio Setup page
            voice_over_recording_page.set_audio_setup_audio_drag_input_volume(0)
            voice_over_recording_page.click_audio_setup_ok_btn()
            voice_over_recording_page.click_device_btn()
            time.sleep(DELAY_TIME)
            current_image3 = voice_over_recording_page.snapshot(locator=L.voice_over_recording.window_audio_setup, file_name=Auto_Ground_Truth_Folder + '2-1-1-4_Min.png')
            compare_result = voice_over_recording_page.compare(Ground_Truth_Folder + '2-1-1-4_Min.png', current_image3)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid('a5b7068f-54cb-4e85-8ddd-2a246ddb3d04') as case:
            # 2.1.1.7 - Device - Input Volume - OK
            current_image4 =media_room_page.snapshot(locator=L.media_room.library_frame, file_name=Auto_Ground_Truth_Folder + '2-1-1-7_OK.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-1-1-7_OK.png', current_image4)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid('c4b77b75-b6de-4b80-b528-238917f5cf21') as case:
            # 2.1.1.8 - Device - Input Volume - Close
            case.result = voice_over_recording_page.click_audio_setup_close_btn()

        with uuid('6593a43b-9764-4181-b9a2-44b7a61562cf') as case:
            # 2.1.1.6 - Device - Input Volume - Mixer
            # Enter Audio Setup page
            voice_over_recording_page.click_device_btn()
            voice_over_recording_page.click_audio_setup_mixer_btn()
            case.result = voice_over_recording_page.click_audio_setup_ok_btn()

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_4_1(self):
        with uuid('7a172da3-d168-402f-a7de-f4f08c2aee52') as case:
            # 2.1.4.1 - Preferences - Time limit - hour
            time.sleep(5)
            voice_over_recording_page.tap_VoiceRecordRoom_hotkey()
            # Verify if in "Voice Over" page
            is_in_voice_over = voice_over_recording_page.check_in_voice_over_recording_room()
            logger(f"{is_in_voice_over= }")
            if is_in_voice_over is not True:
                logger('Failed to enter Voice over page!')
                raise Exception
            # Enter Preferences page
            voice_over_recording_page.click_preferences_btn()
            voice_over_recording_page.set_check_recording_preferences_timelimit()
            # Enter Set hour as 12\
            voice_over_recording_page.set_timelimit_hour(12)
            current_result1 = voice_over_recording_page.get_timelimit_hour()
            if not current_result1 == '12':
                current_result1 = False
            else:
                current_result1 = True
            logger(f"{current_result1= }")
            # Enter Set hour as 0
            voice_over_recording_page.set_timelimit_hour(0)
            current_result2 = voice_over_recording_page.get_timelimit_hour()
            if not current_result2 == '0':
                current_result2 = False
            else:
                current_result2 = True
            logger(f"{current_result2= }")
            case.result = current_result1 and current_result2

        with uuid('0a1eeb54-2ffe-4d9e-aac4-44d780a31b1b') as case:
            # 2.1.4.2 - Preferences - Time limit - minutes
            # Enter Set min as 0
            voice_over_recording_page.set_timelimit_min(0)
            current_result1 = voice_over_recording_page.get_timelimit_min()
            if not current_result1 == '0':
                current_result1 = False
            else:
                current_result1 = True
            logger(f"{current_result1= }")
            # Enter Set hour as 59
            voice_over_recording_page.set_timelimit_min(59)
            current_result2 = voice_over_recording_page.get_timelimit_min()
            if not current_result2 == '59':
                current_result2 = False
            else:
                current_result2 = True
            logger(f"{current_result2= }")
            case.result = current_result1 and current_result2

        with uuid('9df9357e-23f7-44de-abc4-8799a830709c') as case:
            # 2.1.4.3 - Preferences - Time limit - sec
            # Enter Set sec as 0
            voice_over_recording_page.set_timelimit_sec(0)
            current_result1 = voice_over_recording_page.get_timelimit_sec()
            if not current_result1 == '0':
                current_result1 = False
            else:
                current_result1 = True
            logger(f"{current_result1= }")
            # Enter Set sec as 59
            voice_over_recording_page.set_timelimit_sec(59)
            current_result2 = voice_over_recording_page.get_timelimit_sec()
            if not current_result2 == '59':
                current_result2 = False
            else:
                current_result2 = True
            logger(f"{current_result2= }")
            case.result = current_result1 and current_result2

        with uuid('7fd16ab8-393c-48fa-8ad2-7d222351bc2a') as case:
            # 2.1.4.4 - Preferences - Add a 3 second delay before recording
            # Can be ticked/ un-ticked
            current_result1 = voice_over_recording_page.set_check_recording_preferences_delay_3s(bCheck=1)
            current_result2 = voice_over_recording_page.set_check_recording_preferences_delay_3s(bCheck=0)
            case.result = current_result1 and current_result2

        with uuid('13488799-5dea-4901-9ac2-b9df22258ffa') as case:
            # 2.1.4.5 - Preferences - Auto fade-in at beginning of recording
            # Can be ticked/ un-ticked
            current_result3 = voice_over_recording_page.set_check_recording_preferences_auto_fade_in(bCheck=1)
            current_result4 = voice_over_recording_page.set_check_recording_preferences_auto_fade_in(bCheck=0)
            case.result = current_result3 and current_result4

        with uuid('be3b1fb7-9bb7-4931-b8a5-d3f748b64808') as case:
            # 2.1.4.6 - Preferences - Auto fade-out at beginning of recording
            # Can be ticked/ un-ticked
            current_result5 = voice_over_recording_page.set_check_recording_preferences_auto_fade_out(bCheck=1)
            current_result6 = voice_over_recording_page.set_check_recording_preferences_auto_fade_out(bCheck=0)
            case.result = current_result5 and current_result6

        with uuid('45543f7c-4363-4049-be7a-bb7ece8b5508') as case:
            # 2.1.4.7 - Preferences - OK
            # Apply and save all the settings
            voice_over_recording_page.set_check_recording_preferences_timelimit(bCheck=1)
            voice_over_recording_page.set_check_recording_preferences_delay_3s(bCheck=1)
            voice_over_recording_page.set_check_recording_preferences_auto_fade_in(bCheck=1)
            voice_over_recording_page.set_check_recording_preferences_auto_fade_out(bCheck=1)
            voice_over_recording_page.click_recording_preferences_ok()
            voice_over_recording_page.click_preferences_btn()
            time.sleep(DELAY_TIME)
            current_image = media_room_page.snapshot(locator=L.voice_over_recording.window_recording_preference, file_name=Auto_Ground_Truth_Folder + '2-1-4-6_OK.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-1-4-6_OK.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid('a40d02d2-917b-4686-ab9a-ea9a6f37f3ed') as case:
            # 2.1.4.7 - Preferences - Cancel
            # Discard adjusted settings and close dialogue
            voice_over_recording_page.set_check_recording_preferences_timelimit(bCheck=0)
            voice_over_recording_page.set_check_recording_preferences_delay_3s(bCheck=0)
            voice_over_recording_page.set_check_recording_preferences_auto_fade_in(bCheck=0)
            voice_over_recording_page.set_check_recording_preferences_auto_fade_out(bCheck=0)
            voice_over_recording_page.click_recording_preferences_ok()
            voice_over_recording_page.click_preferences_btn()
            voice_over_recording_page.set_check_recording_preferences_timelimit(bCheck=1)
            voice_over_recording_page.set_check_recording_preferences_delay_3s(bCheck=1)
            voice_over_recording_page.set_check_recording_preferences_auto_fade_in(bCheck=1)
            voice_over_recording_page.set_check_recording_preferences_auto_fade_out(bCheck=1)
            voice_over_recording_page.click_recording_preferences_cancel()
            voice_over_recording_page.click_preferences_btn()
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-1-4-6_OK.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_5_1(self):
        with uuid('c7368f70-e24b-4800-865b-2e157c009d35') as case:
            # 2.1.5.1 - Record button - No image/audio/video clip on timeline
            # Record button is enabled
            time.sleep(5)
            voice_over_recording_page.tap_VoiceRecordRoom_hotkey()
            # Verify if in "Voice Over" page
            is_in_voice_over = voice_over_recording_page.check_in_voice_over_recording_room()
            logger(f"{is_in_voice_over= }")
            if is_in_voice_over is not True:
                logger('Failed to enter Voice over page!')
                raise Exception

            voice_over_recording_page.click_device_btn()
            voice_over_recording_page.set_audio_setup_audio_drag_input_volume(93)
            voice_over_recording_page.click_audio_setup_ok_btn()
            time.sleep(5)
            current_library = media_room_page.snapshot(locator=L.media_room.library_frame, file_name=Auto_Ground_Truth_Folder + '2-1-5-1_Library.png')
            current_timeline = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1-5-1_Timeline.png')
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + '2-1-5-1_Library.png', current_library)
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + '2-1-5-1_Timeline.png', current_timeline)
            logger(f"{compare_result1= }")
            logger(f"{compare_result2= }")
            case.result = compare_result1 and compare_result2

        with uuid('6eceb8ca-9d40-4294-85c5-8998cd0d6856') as case:
            # 2.1.5.2 - Record button - Have image/audio/video clip on timeline
            # Record button is enabled and record for 5 sec
            voice_over_recording_page.click_record_btn(recording_time=5)
            time.sleep(5)
            current_result = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1-5-2_Timeline.png')
            compare_result = timeline_operation_page.compare(Ground_Truth_Folder + '2-1-5-2_Timeline.png', current_result, similarity=0.9)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_6_1(self):
        with uuid('4a22a907-d122-4262-acfc-0d69295e2753') as case:
            # 2.1.6.1 "Mute all tracks when recording" option - Default - Default value: Un-tick
            time.sleep(5)
            voice_over_recording_page.tap_VoiceRecordRoom_hotkey()
            # Verify if in "Voice Over" page
            is_in_voice_over = voice_over_recording_page.check_in_voice_over_recording_room()
            logger(f"{is_in_voice_over= }")
            if is_in_voice_over is not True:
                logger('Failed to enter Voice over page!')
                raise Exception
            time.sleep(5)
            # "Mute all tracks when recording" option - Default - Default value: Un-tick
            current_result = voice_over_recording_page.get_mute_all_track_value()
            logger(f"{current_result= }")
            if not current_result == 0:
                current_result = False
            else:
                current_result = True
            case.result = current_result

        with uuid('70f7ab7b-2d43-438c-a092-2ad61b6cf3df') as case:
            # 2.1.6.2 "Mute all tracks when recording" option - Before Recording - Can be ticked/ un-ticked
            voice_over_recording_page.set_check_mute_all_track(1)
            current_result2 = voice_over_recording_page.get_mute_all_track_value()
            logger(f"{current_result2= }")
            if not current_result2 == 1:
                current_result2 = False
            else:
                current_result2 = True
            case.result = current_result2
            voice_over_recording_page.set_check_mute_all_track(0)
            time.sleep(DELAY_TIME)

        with uuid('45019607-f2e7-4606-9fef-2a83ae8a9097') as case:
            # 2.1.6.3 "Mute all tracks when recording" option - Tick checkbox While Recording - All tracks are mute
            # Record button is enabled and record for 5 sec
            voice_over_recording_page.click_record_btn(recording_time=5)
            current_result = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-1-6-3_Timeline.png')
            compare_result3 = timeline_operation_page.compare(Ground_Truth_Folder + '2-1-6-3_Timeline.png', current_result, similarity=0.9)
            logger(f"{compare_result3= }")
            case.result = compare_result3

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    a0972f8a-98d9-44b1-b6f1-a52fcc01e876
                    1ee8363a-508d-4a36-b4ef-a22f323c31c6
                    5922c949-e9fb-4e27-b640-1e1cc084e266
                    # 2.1.6.4 Grey out while recording
                    738f11c8-f73f-4959-8c73-004357cfca0b
                    # 2.2.1 
                    0bb5898d-be75-4009-a497-5784ba88101b
                    70d24ac4-f4d0-4845-abf4-bf5db35249f3
                    33ed22b1-7e76-4f3a-b623-2fbb0566805a
                    # 2.2.2
                    b5704e99-c67d-4f23-819b-407be8b6f5af
                    1a05ab66-098d-428d-b8b4-2b27d1a3d633
                    # 3.1
                    d80a6528-82b6-4148-95ec-5736829776e9
                    54751c36-367d-4944-a4ec-1e6fefd80839
                    53f6a3b5-0599-4422-b5c0-a18da3ccac1d
                    3f4f2e65-da1b-44f1-8f68-ac8df5c47c5d
                    # 3.2
                    44bd8f1e-c0cc-4d61-bf8d-19a8700b48d0
                    e855c5d7-3f67-4776-a766-5dce259c4a0c
                    7bfecff9-d161-4d61-a71d-78e345e5f7e1
                    16a0de67-673f-49da-82fa-78dbd9d6e7cd
                    d4b678ec-06e1-412e-9398-22cb9f52bf96
                    dfbf82a1-68b1-4079-995f-5509c9712ef8
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'

