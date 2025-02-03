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
video_speed_page = PageFactory().get_page_object('video_speed_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Video Speed.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Video_Speed/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Video_Speed/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

# @pytest.fixture(scope="module", autouse= True)
# def init():
#     yield
#     main_page.close_app()
#     report.export()
#     report.show()


class Test_Video_Speed():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        main_page.insert_media("Skateboard 01.mp4")

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
            google_sheet_execution_log_init('Video_Speed')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"video speed result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        with uuid("41679eec-5122-4ded-beb2-158fe9360670") as case:
            # Insert Skateboard 01.mp4 > Enter Video Speed designer
            # 1.1.1. Mouse click enter Video Speed designer
            main_page.tap_TipsArea_Tools_menu('Video Speed')

            set_check_result = L.video_speed.preview

            if not video_speed_page.exist(locator=set_check_result):
                case.result = False
            else:
                case.result = True

        with uuid("3f34b5a2-4cfc-4129-a40c-f2f8a29be69e") as case:
            # 2.1.1. Caption bar > Module
            set_check_result = video_speed_page.exist(L.video_speed.text_window_title).AXValue

            if not set_check_result == 'Video Speed Designer  |  Skateboard 01':
                case.result = False
            else:
                case.result = True

        with uuid("b5043a6a-f673-4f5a-89f9-cf08c9198f30") as case:
            # 2.1.2. Caption bar > File name
            set_check_result = video_speed_page.exist(L.video_speed.text_window_title).AXValue

            if not set_check_result == 'Video Speed Designer  |  Skateboard 01':
                case.result = False
            else:
                case.result = True

        with uuid("0e3d7091-fb51-46ac-9bb4-32ce0cbbfad4") as case:
            # 2.1.3.1. Caption bar > Window control > Maximize/Restore down
            video_speed_page.Edit_VideoSpeedDesigner_Click_Maximize_btn()
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'video_speed_2_1_3_1.png'

            ground_truth = Ground_Truth_Folder + 'video_speed_2_1_3_1.png'
            current_preview = video_speed_page.snapshot(
                locator=L.video_speed.main, file_name=image_full_path)

            check_result_1 = video_speed_page.compare(ground_truth, current_preview)

            video_speed_page.Edit_VideoSpeedDesigner_Click_Restore_btn()
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'video_speed_2_1_3_2.png'

            ground_truth = Ground_Truth_Folder + 'video_speed_2_1_3_2.png'
            current_preview = video_speed_page.snapshot(
                locator=L.video_speed.main, file_name=image_full_path)

            check_result_2 = video_speed_page.compare(ground_truth, current_preview)
            case.result = check_result_1 and check_result_2

        with uuid("07a07595-adba-412f-9e1c-2d2801c6a3fd") as case:
            # 2.1.3.2. Caption bar > Window control > X button
            video_speed_page.Edit_VideoSpeedDesigner_Click_Close_btn()
            time.sleep(DELAY_TIME)

            set_check_result = video_speed_page.exist(L.video_speed.text_window_title)

            if not set_check_result:
                case.result = True
            else:
                case.result = False

            # video_speed_page.Edit_VideoSpeedDesigner_ClickCancel()

        with uuid("d10de289-099c-4d7c-9ef3-89f67fdfc59d") as case:
            # Insert Skateboard 01.mp4, Skateboard 02.mp4 > Enter Video Speed designer
            main_page.select_library_icon_view_media("Skateboard 02.mp4")
            main_page.tips_area_insert_media_to_selected_track(option=1)

            with main_page.keyboard.pressed(main_page.keyboard.key.cmd, 'a'):
                pass
            # 1.1.2. Mouse click enter Video Speed designer
            main_page.tap_TipsArea_Tools_menu('Video Speed')
            time.sleep(DELAY_TIME)

            set_check_result = video_speed_page.exist(L.video_speed.video_speed.main).AXTitle

            if not set_check_result == 'Video Speed':
                case.result = False
            else:
                case.result = True
            video_speed_page.Edit_VideoSpeed_ClickOK()

        with uuid('55c34dff-8e0e-4841-8d24-856ab0a4082c') as case:
            # 1.2. Timeline
            # 1.2.1. Hotkey - Control + Drag video edge > for single video
            # Quick to adjust video speed from timeline
            main_page.close_and_restart_app()
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.drag_to_change_speed(
                track_index=0, clip_index=0, mode='Last', direction='Right', ratio=1)

            image_full_path = Auto_Ground_Truth_Folder + 'video_speed_1_2_1_1.png'
            ground_truth = Ground_Truth_Folder + 'video_speed_1_2_1_1.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.click_undo()

        with uuid('d4bdcf47-0654-4483-a164-7cc815f7dc9d') as case:
            # 1.2. Timeline
            # 1.2.1. Hotkey - Control + Drag video edge > for multiple videos(different track)
            # Quick to adjust video speed from timeline
            main_page.select_library_icon_view_media("Skateboard 02.mp4")
            main_page.tips_area_insert_media_to_selected_track(option=1)

            timeline_operation_page.deselect_clip(track_index=0, last_clip_index=1, movement=100)
            timeline_operation_page.drag_single_media_to_other_track(
                track_index=0, clip_index=0, distance=0, track_num=2)
            timeline_operation_page.select_multiple_timeline_media(
                media1_track_index=2, media1_clip_index=0, media2_track_index=0, media2_clip_index=0)
            timeline_operation_page.drag_to_change_speed(
                track_index=0, clip_index=0, mode='Last', direction='Right', ratio=1)

            image_full_path = Auto_Ground_Truth_Folder + 'video_speed_1_2_1_2.png'
            ground_truth = Ground_Truth_Folder + 'video_speed_1_2_1_2.png'
            current_preview = timeline_operation_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)

            check_result = timeline_operation_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid("115d41ba-6ae9-49cd-9244-3462df244bfa") as case:
            # 2.2.1. Original video length > Display video length
            main_page.tap_TipsArea_Tools_menu('Video Speed')
            time.sleep(DELAY_TIME)
            video_timecode = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_OriginalVideoLength()

            if not video_timecode == '00;00;10;00':
                case.result = False
            else:
                case.result = True

        with uuid("f9bb3192-25ab-47a7-8891-0d8b1e8e4ef2") as case:
            # 2.2.2. New video duration input box > input directly
            current_result = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_SetValue('00_00_05_00')
            case.result = current_result

        with uuid('58a7d4fe-f70a-4145-a901-b85b8296b7c7') as case:
            # 2.2.2. New video duration input box > speed multiplier would be update correctly
            current_speed_multiplier = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_GetValue()

            if not current_speed_multiplier == '2.000':
                case.result = False
            else:
                case.result = True

        with uuid('b38ebf29-3280-4413-835c-c10aa088fe1f') as case:
            # 2.2.2. New video duration input box > More button > Up button
            for i in range(5):
                check_result = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_ArrowButton('Up')

            case.result = check_result

        with uuid('0af6b31a-a0e7-4893-96be-59695405a182') as case:
            # 2.2.2. New video duration input box > More button >speed multiplier would be update correctly
            current_speed_multiplier = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_GetValue()

            if not current_speed_multiplier == '1.935':
                case.result = False
            else:
                case.result = True

        with uuid('9cbcbaec-6ef7-485a-8f26-e329e5d9c597') as case:
            # 2.2.2. New video duration input box > less button > down button
            for i in range(5):
                check_result = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_ArrowButton('Down')

            case.result = check_result

        with uuid('4a2df9d5-5538-4c4d-8f05-4a8aa1fb29d4') as case:
            # 2.2.2. New video duration input box > less button >speed multiplier would be update correctly
            current_speed_multiplier = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_GetValue()

            if not current_speed_multiplier == '2.000':
                case.result = False
            else:
                case.result = True

        with uuid('f909660c-ce05-405d-896d-0a87f7d55d6a') as case:
            # 2.2.3. Speed Multiplier (slider) > Random (0.101~99.999)
            check_result = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_DragSlider(70.0)

            case.result = check_result

        with uuid('11a0b368-3f2d-4811-be89-a74eadc17a17') as case:
            # 2.2.3. Speed Multiplier (slider) > Random > New video duration information would be updated correctly
            time.sleep(DELAY_TIME)
            current_speed_multiplier = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_GetValue()

            if not current_speed_multiplier == '8.200':
                case.result = False
            else:
                case.result = True

        with uuid('90bd87da-082d-460c-82e2-fc105f85ec94') as case:
            # 2.2.3. Speed Multiplier (slider) > Min or Max > Min: 0.100
            video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_DragSlider(0.0)

            current_speed_multiplier = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_GetValue()

            if not current_speed_multiplier == '0.100':
                case.result = False
            else:
                case.result = True

        with uuid('fd1e75b3-8fce-4c7c-b883-b0127b44b7cb') as case:
            # 2.2.3. Speed Multiplier (slider) > Min or Max > Max: 100.00
            check_result = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_DragSlider(100.0)

            case.result = check_result

        with uuid('3e82f25d-9834-4622-8abd-4f7023e2d551') as case:
            # 2.2.3. Speed Multiplier (slider) > Min or Max > New video duration information would be updated correctly
            current_speed_multiplier = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_GetValue()

            if not current_speed_multiplier == '100.000':
                case.result = False
            else:
                case.result = True

        with uuid('a0358495-be33-4f45-8439-f9506391a8c2') as case:
            # 2.2.4. Speed Multiplier (input box) > input directly > can input multiplier directly
            check_result = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_SetValue(2)

            case.result = check_result

        with uuid('b4f5cee0-b0a6-49ad-a29b-a28c8b34eda8') as case:
            # 2.2.4. Speed Multiplier (input box) > input directly > new video duration would be updated correctly
            current_new_duration = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_NewVideoLength_GetValue()

            if not current_new_duration == '00;00;05;00':
                case.result = False
            else:
                case.result = True

        with uuid('c8a69668-d379-442b-bbb4-474f9a823462') as case:
            # 2.2.4. Speed Multiplier (input box) > more button > click more button to increase multiplier value
            for i in range(50):
                check_result = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_ArrowButton('Up')

            case.result = check_result

        with uuid('25d9bb74-c7f1-4731-bb49-f07ece7ecba7') as case:
            # 2.2.4. Speed Multiplier (input box) > more button > new video duration would be updated correctly
            current_new_duration = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_NewVideoLength_GetValue()

            if not current_new_duration == '00;00;04;26':
                case.result = False
            else:
                case.result = True

        with uuid('393a10ab-5b25-4e0c-a614-2a57b65c6ca8') as case:
            # 2.2.4. Speed Multiplier (input box) > less button > click less button to decrease multiplier value
            for i in range(50):
                check_result = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_ArrowButton('Down')

            case.result = check_result

        with uuid('4f01d536-e746-42b6-86c8-ffd75b8947cb') as case:
            # 2.2.4. Speed Multiplier (input box) > less button > new video duration would be updated correctly
            current_new_duration = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_NewVideoLength_GetValue()

            if not current_new_duration == '00;00;05;00':
                case.result = False
            else:
                case.result = True

        with uuid('bbb08672-34a7-406f-824d-f176d5582630') as case:
            # 2.2.5. Switch to [Selected Range] Tab > speed applied > pop-out warning 'if you continue, the changes you made to the video
            video_speed_page.Edit_VideoSpeedDesigner_SelectTab('Selected Range')
            check_result = video_speed_page.Edit_Question_dlg_ClickButton('Cancel')

            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid('5e046c2d-4487-4655-a2f7-99496b41ef39') as case:
            # 2.2.5. Switch to [Selected Range] Tab > no speed applied > switch to [Select Range] tab directly without warning
            main_page.tap_TipsArea_Tools_menu('Video Speed')
            time.sleep(DELAY_TIME * 2)
            video_speed_page.Edit_VideoSpeedDesigner_SelectTab('Selected Range')
            time.sleep(DELAY_TIME)
            check_result = video_speed_page.exist(locator=L.video_speed.i_button)

            case.result = check_result

        with uuid('580998c8-2b69-4b90-bb6e-1fdfb6fe99ea') as case:
            # 2.3.1. Selected Range Tab > i button for create a time shift
            # pop-out dialog to explain how to use time shift
            check_result = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_Click_i_Button()
            case.result = check_result

            video_speed_page.Edit_VideoSpeedDesigner_SelectRange_i_Click_Close_btn()

        with uuid('4e7f5488-e24a-4b4e-9498-a82cb11df30a') as case:
            # 2.3.2. Selected Range Tab > Create time shift button > Single region
            # create the time shift, which is indicated in orange on the timeline
            video_speed_page.VideoSpeedDesigner_SelectRange_Click_Upper_CreateTimeShift_btn()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_speed_2_3_2_1.png'

            ground_truth = Ground_Truth_Folder + 'video_speed_2_3_2_1.png'
            current_preview = video_speed_page.snapshot(
                locator=L.video_speed.main, file_name=image_full_path)

            check_result = video_speed_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('61233337-1f10-4000-83f9-4233ba483b4d') as case:
            # 2.3.3. Selected Range Tab > Duration input box > input directly
            # Can input video duration into input box directly
            current_result = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_Duration_SetValue('00_00_02_16')
            case.result = current_result

        with uuid('708fa231-6f49-4241-9ffd-1ef86a1c8e57') as case:
            # 2.3.3. Selected Range Tab > Duration input box > input directly
            # Speed multiplier would be updated correctly
            current_speed_multiplier = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_GetValue()

            if not current_speed_multiplier == '0.500':
                case.result = False
            else:
                case.result = True

        with uuid('a4ada197-c1ab-4205-9505-d7fb4aaa3fd8') as case:
            # 2.3.3. Selected Range Tab > Duration input box > more button
            # click more button to increase video duration
            for i in range(44):
                check_result = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_Duration_ArrowButton('Up')

            case.result = check_result

        with uuid('8b8ffea7-31b8-4a04-9769-065090a22672') as case:
            # 2.3.3. Selected Range Tab > Duration input box > more button
            # Speed multiplier would be updated correctly
            current_speed_multiplier = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_GetValue()

            if not current_speed_multiplier == '0.317':
                case.result = False
            else:
                case.result = True

        with uuid('aad74de9-3d02-4eb9-9ee4-ce51c2f3ec57') as case:
            # 2.3.3. Selected Range Tab > Duration input box > less button
            # click less button to decrease video duration
            for i in range(44):
                check_result = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_Duration_ArrowButton('Down')

            case.result = check_result

        with uuid('91e73105-c18e-4a2c-85de-0b4180ebef6b') as case:
            # 2.3.3. Selected Range Tab > Duration input box > less button
            # Speed multiplier would be updated correctly
            current_speed_multiplier = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_GetValue()

            if not current_speed_multiplier == '0.500':
                case.result = False
            else:
                case.result = True

        with uuid('bb90b350-b2e1-44d2-beb1-d7c66e7e2c7e') as case:
            # 2.3.4. Selected Range Tab > Speed Multiplier (slider) > Random
            # Change video speed after dragging slider
            check_result = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_DragSlider(70.0)

            case.result = check_result

        with uuid('98a700bd-fc58-431c-8710-dffb68243ff5') as case:
            # 2.3.4. Selected Range Tab > Speed Multiplier (slider) > 0.101~99.999
            # Video duration information would be updated correctly
            time.sleep(DELAY_TIME)
            current_speed_multiplier = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_GetValue()

            if not current_speed_multiplier == '8.200':
                case.result = False
            else:
                case.result = True

        with uuid('28483568-4bf7-42c1-9c16-9c854fdfff07') as case:
            # 2.3.4. Selected Range Tab > Speed Multiplier (slider) > Min or Max
            # Min: 0.100
            video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_DragSlider(0.0)

            current_speed_multiplier = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_GetValue()

            if not current_speed_multiplier == '0.100':
                case.result = False
            else:
                case.result = True

        with uuid('03375daf-930c-4970-8ea9-b1c83259821c') as case:
            # 2.3.4. Selected Range Tab > Speed Multiplier (slider) > Min or Max
            # Max: 100.00
            check_result = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_DragSlider(100.0)

            case.result = check_result

        with uuid('fa41cf2f-8f2e-4aeb-98c2-ac540a5e9f6a') as case:
            # 2.3.4. Selected Range Tab > Speed Multiplier (slider) > Min or Max
            # Video duration information would be updated correctly
            current_speed_multiplier = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_GetValue()

            if not current_speed_multiplier == '38.000':
                case.result = False
            else:
                case.result = True

        with uuid('ac7dce69-b459-4773-89ed-4a92b7fc9fa7') as case:
            # 2.3.5. Selected Range Tab > Speed Multiplier(input box) > input directly
            # Can input multiplier directly
            check_result = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_SetValue(0.25)

            case.result = check_result

        with uuid('0cf37842-ca52-4c17-82b6-96b122694d8c') as case:
            # 2.3.5. Selected Range Tab > Speed Multiplier(input box) > input directly
            # video duration would be updated correctly
            current_new_duration = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_VideoLength_GetValue()

            if not current_new_duration == '00;00;05;02':
                case.result = False
            else:
                case.result = True

        with uuid('f380ffec-195f-4cab-a2bc-f1014fd1e926') as case:
            # 2.3.5. Selected Range Tab > Speed Multiplier(input box) > more button
            # Click more button to increase multiplier value
            for i in range(50):
                check_result = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_ArrowButton('Up')

            case.result = check_result

        with uuid('987cb5d1-8db0-4838-bf7a-98380bd74a97') as case:
            # 2.3.5. Selected Range Tab > Speed Multiplier(input box) > more button
            # video duration would be updated correctly
            current_new_duration = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_VideoLength_GetValue()

            if not current_new_duration == '00;00;04;07':
                case.result = False
            else:
                case.result = True

        with uuid('2426b6a1-e15a-4676-8324-520b688a2fbd') as case:
            # 2.3.5. Selected Range Tab > Speed Multiplier(input box) > less button
            # click less button to decrease multiplier value
            for i in range(50):
                check_result = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_ArrowButton('Down')

            case.result = check_result

        with uuid('cb65281b-39ff-420a-8935-1e46223a0199') as case:
            # 2.3.5. Selected Range Tab > Speed Multiplier(input box) > less button
            # video duration would be updated correctly
            current_new_duration = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_VideoLength_GetValue()

            if not current_new_duration == '00;00;05;02':
                case.result = False
            else:
                case.result = True

        with uuid('f9bdd974-fdd6-47c5-8667-0c177ca1a10e') as case:
            # 2.3.6. Selected Range Tab > Ease in checkbox > Tick
            # Change of speed at the beginning of the time shift to gradually speed up/slow down to the specified speed
            video_speed_page.Edit_VideoSpeedDesigner_SelectRange_EaseIn_SetCheck()
            time.sleep(DELAY_TIME)
            current_new_duration = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_VideoLength_GetValue()

            if not current_new_duration == '00;00;03;17':
                case.result = False
            else:
                case.result = True

        with uuid('e2757704-c0c0-442a-81ec-34d1e2c22075') as case:
            # 2.3.6. Selected Range Tab > Ease in checkbox > Un-tick
            # not apply ease in
            video_speed_page.Edit_VideoSpeedDesigner_SelectRange_EaseIn_SetCheck(0)
            time.sleep(DELAY_TIME)
            current_new_duration = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_VideoLength_GetValue()

            if not current_new_duration == '00;00;05;02':
                case.result = False
            else:
                case.result = True

        with uuid('aa655697-5be1-4693-a99e-26815cccab3e') as case:
            # 2.3.7. Selected Range Tab > Ease out checkbox > Tick
            # the video to gradually return to the original video speed at the end of the time shift
            video_speed_page.Edit_VideoSpeedDesigner_SelectRange_EaseOut_SetCheck()
            time.sleep(DELAY_TIME)
            current_new_duration = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_VideoLength_GetValue()

            if not current_new_duration == '00;00;03;17':
                case.result = False
            else:
                case.result = True

        with uuid('54db59e6-5b59-4d0f-a6f8-1b88cf58ad55') as case:
            # 2.3.7. Selected Range Tab > Ease out checkbox > Un-Tick
            # not apply ease out
            video_speed_page.Edit_VideoSpeedDesigner_SelectRange_EaseOut_SetCheck(False)
            time.sleep(DELAY_TIME)
            current_new_duration = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_VideoLength_GetValue()

            if not current_new_duration == '00;00;05;02':
                case.result = False
            else:
                case.result = True

        with uuid('680e0e4a-799c-498f-aed3-00fce711c575') as case:
            # 2.3.6. Selected Range Tab > Ease in checkbox > disable
            # if duration is less than 2 sec. checkbox will disable
            video_speed_page.Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_SetValue(1)
            time.sleep(DELAY_TIME)

            check_result = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_EaseIn_IsEnabled()
            if not check_result:
                case.result = True
            else:
                case.result = False

        with uuid('4bbbc86c-fa92-402d-be1a-668004789868') as case:
            # 2.3.7. Selected Range Tab > Ease out checkbox > disable
            # if duration is less than 2 sec. checkbox will disable
            check_result = video_speed_page.Edit_VideoSpeedDesigner_SelectRange_EaseOut_IsEnabled()
            if not check_result:
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid('23061f45-08dd-4ddb-8002-0e02f573b4bf') as case:
            # 2.4.1. Playback > Preview control > play/pause button
            # video preview shows normally
            main_page.tap_TipsArea_Tools_menu('Video Speed')
            video_speed_page.VideoSpeedDesigner_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 5)
            video_speed_page.VideoSpeedDesigner_PreviewOperation('Play')

            ground_truth = Ground_Truth_Folder + 'video_speed_2_4_1_1.png'

            check_result = video_speed_page.check_VideoSpeedDesigner_preveiw(ground_truth, similarity=0.95)
            case.result = check_result

        with uuid('c6f5a77f-b334-468c-aba5-0d46130bf929') as case:
            # 2.4.1. Playback > Preview control > stop button
            # can stay at the frame while clicking stop button
            video_speed_page.VideoSpeedDesigner_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 2)
            video_speed_page.VideoSpeedDesigner_PreviewOperation('Stop')
            time.sleep(DELAY_TIME)
            ground_truth = Ground_Truth_Folder + 'video_speed_2_4_1_2.png'

            check_result = video_speed_page.check_VideoSpeedDesigner_preveiw(ground_truth, similarity=0.95)
            case.result = check_result

        with uuid('91594fbb-926d-48be-88ad-2dcb14a676b7') as case:
            # 2.4.1. Playback > Preview control > next frame button
            # check the preview shows as next frame after clicking
            # time.sleep(DELAY_TIME * 3)
            for i in range(10):
                video_speed_page.VideoSpeedDesigner_PreviewOperation('Next_Frame')
            time.sleep(DELAY_TIME)
            ground_truth = Ground_Truth_Folder + 'video_speed_2_4_1_4.png'

            check_result = video_speed_page.check_VideoSpeedDesigner_preveiw(ground_truth, similarity=0.95)
            case.result = check_result

        with uuid('db2a17ba-0410-42e4-bc62-ae98d90431de') as case:
            # 2.4.1. Playback > Preview control > previous frame button
            # check the preview shows as previous frame after clicking
            # time.sleep(DELAY_TIME * 3)
            for i in range(10):
                video_speed_page.VideoSpeedDesigner_PreviewOperation('Previous_Frame')
            time.sleep(DELAY_TIME)
            ground_truth = Ground_Truth_Folder + 'video_speed_2_4_1_3.png'

            check_result = video_speed_page.check_VideoSpeedDesigner_preveiw(ground_truth, similarity=0.95)
            case.result = check_result

        with uuid('ed4bbe79-e0cc-4a04-8edc-137be84da297') as case:
            # 2.4.1. Playback > Preview control > fast forward button
            # video preview shows in selected speed
            # time.sleep(DELAY_TIME * 3)
            check_result = video_speed_page.VideoSpeedDesigner_PreviewOperation('Fast_Forward')
            time.sleep(DELAY_TIME * 6)
            # waiting for FF verify function

            case.result = check_result

        with uuid('dc618f18-d2f3-42a9-bda4-deb21ee3483d') as case:
            # 2.4.1. Playback > Preview control > timecode display/input box
            # seek frame via timecode directly
            # time.sleep(DELAY_TIME * 3)
            video_speed_page.set_VideoSpeedDesigner_timecode('00_00_05_00')
            time.sleep(DELAY_TIME)
            ground_truth = Ground_Truth_Folder + 'video_speed_2_4_1_5.png'

            check_result = video_speed_page.check_VideoSpeedDesigner_preveiw(ground_truth, similarity=0.95)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid('940c0dd1-ce56-48b4-a221-aefccb8b941f') as case:
            # 2.5.1. Frame panel > continue video frame
            # show video frame correctly
            # time.sleep(DELAY_TIME * 3)
            main_page.tap_TipsArea_Tools_menu('Video Speed')
            video_speed_page.Edit_VideoSpeedDesigner_SelectTab('Selected Range')
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'video_speed_2_5_1_1.png'
            ground_truth = Ground_Truth_Folder + 'video_speed_2_5_1_1.png'

            current_preview = video_speed_page.snapshot(
                locator=L.video_speed.main, file_name=image_full_path)

            check_result = video_speed_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('1468a6f5-42f6-4fd0-8874-dfa516e23d77') as case:
            # 2.5.2. Frame panel > create time shift button
            # create the time shift, which is indicated in orange on the timeline
            # time.sleep(DELAY_TIME * 3)
            video_speed_page.VideoSpeedDesigner_SelectRange_Click_lower_CreateTimeShift_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'video_speed_2_5_2_1.png'
            ground_truth = Ground_Truth_Folder + 'video_speed_2_5_2_1.png'

            current_preview = video_speed_page.snapshot(
                locator=L.video_speed.main, file_name=image_full_path)

            check_result = video_speed_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('ab84353d-6066-42fb-85f2-05479fdb85ae') as case:
            # 2.5.4. Frame panel > Remove button
            # remove the selected time shift
            # time.sleep(DELAY_TIME * 3)
            video_speed_page.Edit_VideoSpeedDesigner_Click_Remove_btn()

            image_full_path = Auto_Ground_Truth_Folder + 'video_speed_2_5_4_1.png'
            ground_truth = Ground_Truth_Folder + 'video_speed_2_5_4_1.png'

            current_preview = video_speed_page.snapshot(
                locator=L.video_speed.main, file_name=image_full_path)

            check_result = video_speed_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('e95b8f0b-9683-42a6-b15b-609ffa2aee42') as case:
            # 2.5.6. Frame panel > timeline ruler > zoom in
            # resize timeline scale
            # time.sleep(DELAY_TIME * 3)
            for i in range(20):
                check_result = video_speed_page.Edit_VideoSpeedDesigner_Click_ZoomIn_btn()

            case.result = check_result

        with uuid('7c4422b7-dfec-481d-8244-4b4620006265') as case:
            # 2.5.6. Frame panel > timeline ruler > zoom in
            # continue thumbnail updates correctly
            time.sleep(DELAY_TIME * 3)
            image_full_path = Auto_Ground_Truth_Folder + 'video_speed_2_5_6_1.png'
            ground_truth = Ground_Truth_Folder + 'video_speed_2_5_6_1.png'

            current_preview = video_speed_page.snapshot(
                locator=L.video_speed.main, file_name=image_full_path)

            check_result = video_speed_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('bed180a6-fcde-411a-a4ba-b2c6cfb162e4') as case:
            # 2.5.6. Frame panel > timeline ruler > zoom out
            # resize timeline scale
            # time.sleep(DELAY_TIME * 3)
            for i in range(10):
                check_result = video_speed_page.Edit_VideoSpeedDesigner_Click_ZoomOut_btn()

            case.result = check_result

        with uuid('d6919cdd-dd20-4748-88aa-2600e6c02148') as case:
            # 2.5.6. Frame panel > timeline ruler > zoom out
            # continue thumbnail updates correctly
            time.sleep(DELAY_TIME * 3)
            image_full_path = Auto_Ground_Truth_Folder + 'video_speed_2_5_6_2.png'
            ground_truth = Ground_Truth_Folder + 'video_speed_2_5_6_2.png'

            current_preview = video_speed_page.snapshot(
                locator=L.video_speed.main, file_name=image_full_path)

            check_result = video_speed_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('8d85ddd8-1ea2-4454-b163-479a6bf5c906') as case:
            # 2.5.5. Frame panel > view entire movie button
            # auto fit your current project in the timeline area if you want to view the entire movie
            # time.sleep(DELAY_TIME * 3)
            video_speed_page.Edit_VideoSpeedDesigner_Click_ViewEntireMovie()

            image_full_path = Auto_Ground_Truth_Folder + 'video_speed_2_5_5_1.png'
            ground_truth = Ground_Truth_Folder + 'video_speed_2_5_5_1.png'

            current_preview = video_speed_page.snapshot(
                locator=L.video_speed.main, file_name=image_full_path)

            check_result = video_speed_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid('887f647e-95ef-413d-be59-aadd7eef3f4a') as case:
            # 2.6.1. Confirmation > Reset > Disable
            # should disable before change speed
            main_page.tap_TipsArea_Tools_menu('Video Speed')
            time.sleep(DELAY_TIME)
            check_result = video_speed_page.select_range.reset.is_enabled()
            if not check_result:
                case.result = True
            else:
                case.result = False
            video_speed_page.Edit_VideoSpeedDesigner_EntireClip_OriginalVideoLength()

        with uuid('021833b9-aadc-4e42-b294-30706f6211b4') as case:
            # 2.6.1. Confirmation > Reset > Enable
            # should enable after change speed
            video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_SetValue(2.000)
            time.sleep(DELAY_TIME)
            check_result = video_speed_page.Edit_VideoSpeedDesigner_ClickReset()

            case.result = check_result

        with uuid('186a6811-4eba-42b2-92af-0c74a05ba03f') as case:
            # 2.6.2. Confirmation > Cancel
            # leave designer w/o saving change
            check_result = video_speed_page.Edit_VideoSpeedDesigner_ClickCancel()

            case.result = check_result
            video_speed_page.Edit_Question_dlg_ClickButton('No')

        with uuid('c69f1942-93b0-42de-a798-f4ff01ec1503') as case:
            # 2.6.3. Confirmation > OK
            # leave designer and saving change
            main_page.tap_TipsArea_Tools_menu('Video Speed')
            video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_SetValue(2.000)
            video_speed_page.Edit_VideoSpeedDesigner_ClickOK()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_speed_2_6_3_1.png'
            ground_truth = Ground_Truth_Folder + 'video_speed_2_6_3_1.png'

            current_preview = video_speed_page.snapshot(
                locator=L.main.timeline.track_unit, file_name=image_full_path)

            check_result = video_speed_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        with uuid('9f168b0b-140d-4cb1-b4a0-cdf1f1f9230c') as case:
            # 3. Video Speed(Multiple videos)
            # 3.1.1. Adjustment > New video duration
            # Adjust by input timecode > set duration correctly
            # Insert Skateboard 01.mp4, Skateboard 02.mp4 > Enter Video Speed designer
            main_page.select_library_icon_view_media("Skateboard 02.mp4")
            main_page.tips_area_insert_media_to_selected_track(option=1)

            with main_page.keyboard.pressed(main_page.keyboard.key.cmd, 'a'):
                pass
            # Mouse click enter Video Speed designer
            main_page.tap_TipsArea_Tools_menu('Video Speed')
            time.sleep(DELAY_TIME)
            video_speed_page.Edit_VideoSpeed_Reset_GetStatus()
            video_speed_page.Edit_VideoSpeed_EntireClip_NewVideoDuration_SetValue('00_00_20_00')

            current_speed_multiplier = video_speed_page.Edit_VideoSpeed_EntireClip_SpeedMultiplier_GetValue()

            if not current_speed_multiplier == '0.500':
                case.result = False
            else:
                case.result = True

        with uuid('00461978-9638-4239-9271-ce2263816cd1') as case:
            # 3.1.1. Adjustment > New video duration
            # Adjust by Up/Down > set duration correctly
            # New video duration input box > More button > Up button
            for i in range(30):
                video_speed_page.Edit_VideoSpeed_EntireClip_NewVideoDuration_ArrowButton('Up')
                with main_page.keyboard.pressed(main_page.keyboard.key.enter):
                    pass

            # New video duration input box > less button > down button
            for i in range(10):
                video_speed_page.Edit_VideoSpeed_EntireClip_NewVideoDuration_ArrowButton('Down')
                with main_page.keyboard.pressed(main_page.keyboard.key.enter):
                    pass

            # New video duration input box > less button >speed multiplier would be update correctly
            current_speed_multiplier = video_speed_page.Edit_VideoSpeed_EntireClip_SpeedMultiplier_GetValue()

            if not current_speed_multiplier == '0.484':
                case.result = False
            else:
                case.result = True

        with uuid('bb170b24-77b9-4584-bb95-094239962f3b') as case:
            # 3.1.2. Adjustment > Speed multiplier
            # Adjust by Slider > set duration correctly
            video_speed_page.Edit_VideoSpeed_EntireClip_SpeedMultiplier_DragSlider(70.0)

            # New video speed multiplier information would be updated correctly
            time.sleep(DELAY_TIME)
            current_speed_multiplier = video_speed_page.Edit_VideoSpeed_EntireClip_SpeedMultiplier_GetValue()

            if not current_speed_multiplier == '8.200':
                case.result = False
            else:
                case.result = True

        with uuid('b4ce561c-45b6-4f9b-92e7-799a207ad55b') as case:
            # 3.1.2. Adjustment > Speed multiplier
            # Adjust by input no. > set duration correctly
            video_speed_page.Edit_VideoSpeed_EntireClip_SpeedMultiplier_SetValue(2)

            # new video duration would be updated correctly
            time.sleep(DELAY_TIME * 3)
            current_new_duration = video_speed_page.Edit_VideoSpeed_EntireClip_NewVideoDuration_GetValue()

            if not current_new_duration == '00;00;05;00':
                case.result = False
            else:
                case.result = True

            video_speed_page.Edit_VideoSpeed_ClickCancel()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        with uuid('581e450d-844e-4b92-911c-74d007696c8f') as case:
            # 3.2.1. Confirmation > Reset > Disable
            # should disable before change speed
            # Insert Skateboard 01.mp4, Skateboard 02.mp4 > Enter Video Speed designer
            main_page.select_library_icon_view_media("Skateboard 02.mp4")
            main_page.tips_area_insert_media_to_selected_track(option=1)

            with main_page.keyboard.pressed(main_page.keyboard.key.cmd, 'a'):
                pass
            # Mouse click enter Video Speed designer
            main_page.tap_TipsArea_Tools_menu('Video Speed')
            time.sleep(DELAY_TIME)
            check_result = video_speed_page.Edit_VideoSpeed_Reset_GetStatus()
            if not check_result:
                case.result = True
            else:
                case.result = False

        with uuid('f810ae97-bc81-42c3-9ccb-1faa1118f290') as case:
            # 3.2.1. Confirmation > Reset > Enable
            # should enable after change speed
            video_speed_page.Edit_VideoSpeed_EntireClip_SpeedMultiplier_SetValue(2.000)
            check_result = video_speed_page.Edit_VideoSpeed_ClickReset()

            case.result = check_result

        with uuid('9329fad5-9e68-4bd9-8425-b547a48485d6') as case:
            # 3.2.2. Confirmation > Cancel
            # leave designer w/o saving change
            check_result = video_speed_page.Edit_VideoSpeed_ClickCancel()

            case.result = check_result

        with uuid('27ca3b22-fdec-4587-b06b-38407edc2176') as case:
            # 3.2.3. Confirmation > OK
            # leave designer and saving change
            main_page.tap_TipsArea_Tools_menu('Video Speed')
            video_speed_page.Edit_VideoSpeed_EntireClip_SpeedMultiplier_SetValue(2.000)
            video_speed_page.Edit_VideoSpeed_ClickOK()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'video_speed_3_2_3_1.png'
            ground_truth = Ground_Truth_Folder + 'video_speed_3_2_3_1.png'

            current_preview = video_speed_page.snapshot(
                locator=L.main.timeline.track_unit, file_name=image_full_path)

            check_result = video_speed_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    7523a6f1-5d6f-461e-b4ca-cfd30b58af62
                    48bab60b-3a42-4b4a-8460-b0996a443d7d
                    8c7da941-9e65-4f97-a5bf-00e7ec3856f0
                    e99fa7d1-8050-4199-ad05-13bc4cdba7ed
                    731307bd-852d-4bd3-a2c6-31b9627a231a
                    7c94e029-bcff-423c-8cd1-d0dc7e310d04
                    c956935e-616e-470b-b3c2-e629a3a5104a
                    6b691890-c0ce-40b1-a5d0-bc66d35d9a7b
                    d7c0be3f-8bbb-4571-8687-0fde647a0d6b
                    7c90bf73-547e-4318-91ad-55ec2baa1945
                    50be366a-72f1-4e1b-ac45-eb370dd73d5f
                    cbec5e08-4ad4-4e1f-925c-2a71ad44a905
                    7d1cbe2d-2b82-4b1a-9776-c6445f22240c
                    567ddaee-1aca-4d1c-93bc-bcc16a463064
                    e408133d-a5ce-4fa4-ab14-b536143dd350
                    eef42992-bba8-4691-9fae-d8fbfdc1306f
                    70a3972e-0041-43bf-9e73-001d1059b940
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'