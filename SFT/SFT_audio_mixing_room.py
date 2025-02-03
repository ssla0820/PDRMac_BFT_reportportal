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
audio_mixing_room_page = PageFactory().get_page_object('audio_mixing_room_page', mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Audio Mixing Room.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Audio_Mixing_Room/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Audio_Mixing_Room/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Audio_Mixing_Room():
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

    @classmethod
    def setup_class(cls):
        main_page.clear_cache()
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('Audio_Mixing_Room')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"audio mixing room result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number,
                                                     report.get_ovinfo('na'),
                                                     report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        with uuid('a692b4f4-f1b0-4ed4-bf32-dd0e739746d3') as case:
            # 1. General
            # 1.1. Enter Audio Mixing Room
            # 1.1.1. Mouse click enter
            # enter audio mixing room
            main_page.insert_media('Mahoroba.mp3')
            main_page.select_library_icon_view_media("Skateboard 01.mp4")
            main_page.tips_area_insert_media_to_selected_track(option=1)

            main_page.enter_room(6)
            check_result = audio_mixing_room_page.exist(L.audio_mixing_room.audio_mixing_track)
            if not check_result:
                case.result = False
            else:
                case.result = True

        with uuid('f804885a-dc0a-45dc-96a0-b3f5c10539ef') as case:
            # 1.2. Tracks
            # 1.2.1. Audio Tracks
            # show audio x
            case.result = check_result

        with uuid('77466d44-4713-49ff-bb37-9536da62b21d') as case:
            # 2. Function
            # 2.1. Audio Track
            # 2.1.1. dB Meter
            # show as the audio wave
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 5)
            playback_window_page.Edit_Timeline_PreviewOperation('Pause')

            image_full_path = Auto_Ground_Truth_Folder + 'audio_mixing_room_2_1_1_1.png'
            ground_truth = Ground_Truth_Folder + 'audio_mixing_room_2_1_1_1.png'
            current_preview = audio_mixing_room_page.snapshot(
                locator=L.audio_mixing_room.audio_mixing_track, file_name=image_full_path)

            check_result = audio_mixing_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('3f0007c1-bbfb-47c5-a892-6882dd0626c3') as case:
            # 2.1. Audio Track
            # 2.1.3. Video Volume > Slider > Default
            # default is +0.0 dB
            volume_value = audio_mixing_room_page.exist(L.audio_mixing_room.audio_volume_slider).AXValue
            if not volume_value == 67:
                check_result_1 = False
            else:
                check_result_1 = True

            volume_db_value = audio_mixing_room_page.get_volume_db_value(0)
            if not volume_db_value == '+0.0':
                check_result_2 = False
            else:
                check_result_2 = True

            case.result = check_result_1 and check_result_2

        with uuid('22ffe47d-1581-4b32-abcf-8b142a535ca4') as case:
            # 2.1. Audio Track
            # 2.1.3. Video Volume > Slider > Max
            # max is +12.0 dB
            audio_mixing_room_page.set_audio_volume(0, 100)

            volume_db_value = audio_mixing_room_page.get_volume_db_value(0)
            if not volume_db_value == '+12.0':
                check_result = False
            else:
                check_result = True
            case.result = check_result

        with uuid('37beb083-ea8d-410d-aadb-39de4b66291d') as case:
            # 2.1. Audio Track
            # 2.1.3. Video Volume > Slider > Max
            # the audio track clip keyframe would change to max
            image_full_path = Auto_Ground_Truth_Folder + 'audio_mixing_room_2_1_3_1.png'
            ground_truth = Ground_Truth_Folder + 'audio_mixing_room_2_1_3_1.png'
            current_preview = audio_mixing_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = audio_mixing_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('0c87ecd2-2132-4610-bef3-cc165cfb1e33') as case:
            # 2.1. Audio Track
            # 2.1.3. Video Volume > Slider > Min
            # min is -oo
            audio_mixing_room_page.set_audio_volume(0, 0)

            volume_db_value = audio_mixing_room_page.get_volume_db_value(0)
            if not volume_db_value == '-∞':
                check_result = False
            else:
                check_result = True
            case.result = check_result

        with uuid('8a4e35f2-f871-497a-8c5d-6033f1eaa3ea') as case:
            # 2.1. Audio Track
            # 2.1.3. Video Volume > Slider > Min
            # the audio track clip keyframe would change to min
            image_full_path = Auto_Ground_Truth_Folder + 'audio_mixing_room_2_1_3_2.png'
            ground_truth = Ground_Truth_Folder + 'audio_mixing_room_2_1_3_2.png'
            current_preview = audio_mixing_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = audio_mixing_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('7e92083a-e9d2-497e-a63b-27df2cdbf736') as case:
            # 2.1. Audio Track
            # 2.1.3. Video Volume > Input
            # the slider change as input value
            audio_mixing_room_page.set_audio_volume(0, 90)

            volume_db_value = audio_mixing_room_page.get_volume_db_value(0)
            if not volume_db_value == '+9.7':
                check_result = False
            else:
                check_result = True
            case.result = check_result

        with uuid('b6531d5e-9f72-4a8e-b60d-088f1996e942') as case:
            # 2.1. Audio Track
            # 2.1.3. Video Volume > Input
            # the voice track clip keyframe would change as input value
            image_full_path = Auto_Ground_Truth_Folder + 'audio_mixing_room_2_1_3_3.png'
            ground_truth = Ground_Truth_Folder + 'audio_mixing_room_2_1_3_3.png'
            current_preview = audio_mixing_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = audio_mixing_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('9eb57f28-280c-4f64-ba2d-f06af4cf35fd') as case:
            # 2.1. Audio Track
            # 2.1.4. Audio Gain > Default
            # default is 50
            gain_value = audio_mixing_room_page.exist(L.audio_mixing_room.audio_gain).AXValue
            if not gain_value == 50:
                check_result = False
            else:
                check_result = True
            case.result = check_result

        with uuid('d091d1ef-b76c-4d4d-b627-62354aa74987') as case:
            # 2.1. Audio Track
            # 2.1.4. Audio Gain > Max
            # max is 100
            audio_mixing_room_page.set_audio_gain(0, 100)

            audio_gain = audio_mixing_room_page.exist(L.audio_mixing_room.audio_gain).AXValue
            if not audio_gain == 100:
                check_result = False
            else:
                check_result = True
            case.result = check_result

        with uuid('a8220989-41dd-40c7-8d38-6a5d5a92179d') as case:
            # 2.1. Audio Track
            # 2.1.2. Volume peak indicator
            # becomes red when the volume peak is out of range
            image_full_path = Auto_Ground_Truth_Folder + 'audio_mixing_room_2_1_2_1.png'
            ground_truth = Ground_Truth_Folder + 'audio_mixing_room_2_1_2_1.png'
            current_preview = audio_mixing_room_page.snapshot(
                locator=L.audio_mixing_room.audio_mixing_track, file_name=image_full_path)

            check_result = audio_mixing_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('f87feaf5-9d64-47c5-9d0d-ecea90b57f0d') as case:
            # 2.1. Audio Track
            # 2.1.4. Audio Gain > Max
            # the track gain would change to max
            image_full_path = Auto_Ground_Truth_Folder + 'audio_mixing_room_2_1_4_1.png'
            ground_truth = Ground_Truth_Folder + 'audio_mixing_room_2_1_4_1.png'
            current_preview = audio_mixing_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = audio_mixing_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('06a37271-c22c-4507-9b62-2d7ec6735292') as case:
            # 2.1. Audio Track
            # 2.1.4. Audio Gain > Min
            # min is 0
            audio_mixing_room_page.set_audio_gain(0, 0)

            audio_gain = audio_mixing_room_page.exist(L.audio_mixing_room.audio_gain).AXValue
            if not audio_gain == 0:
                check_result = False
            else:
                check_result = True
            case.result = check_result

        with uuid('7f7190ec-14c6-4500-917d-988b4543eb5d') as case:
            # 2.1. Audio Track
            # 2.1.4. Audio Gain > Min
            # the track gain would change to min
            image_full_path = Auto_Ground_Truth_Folder + 'audio_mixing_room_2_1_4_2.png'
            ground_truth = Ground_Truth_Folder + 'audio_mixing_room_2_1_4_2.png'
            current_preview = audio_mixing_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = audio_mixing_room_page.compare(ground_truth, current_preview)
            case.result = check_result

            audio_mixing_room_page.set_audio_gain(0, 50)

        with uuid('732db6f4-8d5e-43fb-8b83-3a6f0ed03610') as case:
            # 2.1. Audio Track
            # 2.1.5. Keyframe > Previous Keyframe
            # select previous keyframe
            audio_mixing_room_page.click_previous_keyframe(0)
            time.sleep(DELAY_TIME)
            volume_db_value = audio_mixing_room_page.get_volume_db_value(0)
            if not volume_db_value == '+0.0':
                case.result = False
            else:
                case.result = True

        with uuid('08e48a15-be50-453f-828b-1d56b1792a1f') as case:
            # 2.1. Audio Track
            # 2.1.6. Fade > Fade in
            # the voice track clip keyframe start to fade in at this point
            audio_mixing_room_page.click_fade_in(0)

            image_full_path = Auto_Ground_Truth_Folder + 'audio_mixing_room_2_1_6_1.png'
            ground_truth = Ground_Truth_Folder + 'audio_mixing_room_2_1_6_1.png'
            current_preview = audio_mixing_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = audio_mixing_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('35662a9e-2c8f-4a7e-8c51-6924769330da') as case:
            # 2.1. Audio Track
            # 2.1.5. Keyframe > Next Keyframe
            # select next keyframe
            audio_mixing_room_page.click_next_keyframe(0)
            time.sleep(DELAY_TIME)

            volume_db_value = audio_mixing_room_page.get_volume_db_value(0)
            if not volume_db_value == '+9.7':
                case.result = False
            else:
                case.result = True

            audio_mixing_room_page.click_next_keyframe(0)

        with uuid('7a0bfd55-2ca5-4e70-8b33-abecdf5a6367') as case:
            # 2.1. Audio Track
            # 2.1.6. Fade > Fade out
            # the voice track clip keyframe start to fade out at this point
            audio_mixing_room_page.click_next_keyframe(0)
            audio_mixing_room_page.click_fade_out(0)

            image_full_path = Auto_Ground_Truth_Folder + 'audio_mixing_room_2_1_6_2.png'
            ground_truth = Ground_Truth_Folder + 'audio_mixing_room_2_1_6_2.png'
            current_preview = audio_mixing_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = audio_mixing_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('aeb198cc-b515-44a5-949b-1ee4073e2744') as case:
            # 2.1. Audio Track
            # 2.1.7. Normalize
            # normalize the voice track audio clips
            audio_mixing_room_page.click_normalize(0)

            image_full_path = Auto_Ground_Truth_Folder + 'audio_mixing_room_2_1_7_1.png'
            ground_truth = Ground_Truth_Folder + 'audio_mixing_room_2_1_7_1.png'
            current_preview = audio_mixing_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = audio_mixing_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('653c14b7-116a-46f7-bb74-37515b6c31e3') as case:
            # 2.1. Audio Track
            # 2.1.5. Keyframe > Add/Remove Keyframe
            # add/remove keyframe at current position
            main_page.set_timeline_timecode('00_00_30_00')
            audio_mixing_room_page.click_keyframe_control(0)

            image_full_path = Auto_Ground_Truth_Folder + 'audio_mixing_room_2_1_5_1.png'
            ground_truth = Ground_Truth_Folder + 'audio_mixing_room_2_1_5_1.png'
            current_preview = audio_mixing_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = audio_mixing_room_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    6dcb9b5e-7d91-4494-9e6f-fab368135fb8
                    7a00f2d0-e1ad-41ed-956d-0a22e59eced5
                    799d07d2-fe91-4c0f-b933-9208d04358d9
                    79f927ff-0562-4b6d-8eb8-91fd8b11e1ca
                ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"


