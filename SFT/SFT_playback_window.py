import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time, inspect, datetime, pytest, re, configparser
os.chdir(os.path.dirname(__file__))
from types import SimpleNamespace

from ATFramework import MyReport, logger
from ATFramework.drivers.driver_factory import DriverFactory
from pages.page_factory import PageFactory
from configs.app_config import *
# import pages.media_room_page
from pages.locator import locator as L

#for update_report_info
from globals import *



# read PDR cap >>
app = SimpleNamespace(**PDR_cap)
# read PDR cap <<

# create driver & page >>
mac = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mac)
#base_page = PageFactory().get_page_object('base_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page',mac)
library_preview_page = PageFactory().get_page_object('library_preview_page',mac)
mask_designer_page = PageFactory().get_page_object('mask_designer_page', mac)
effect_room_page = PageFactory().get_page_object('effect_room_page', mac)
pip_room_page = PageFactory().get_page_object('pip_room_page', mac)
particle_room_page = PageFactory().get_page_object('particle_room_page',mac)
title_room_page = PageFactory().get_page_object('title_room_page',mac)
transition_room_page = PageFactory().get_page_object('trainsition_room_page',mac)
playback_window_page = PageFactory().get_page_object('playback_window_page',mac)
preferences_page = PageFactory().get_page_object('preferences_page',mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Playback Window.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<


# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Playback_Window/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Playback_Window/'
Test_Material_Folder = app.testing_material

#Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto_MacAT/SFT/GroundTruth/Playback_Window/'
#Auto_Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto_MacAT/SFT/ATGroundTruth/Playback_Window/'
#Test_Material_Folder = '/Users/clt/Desktop/Ernesto_MacAT/Material/'

DELAY_TIME = 1


class Test_Playback_Window():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME*3)
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
            google_sheet_execution_log_init('Playback_Window')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"mask designer result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
    def test1_1_5_1(self):
        # preview window
        with uuid("e4a145f3-65b3-45be-b135-ee64269b5632") as case:
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                              file_name=Auto_Ground_Truth_Folder + 'G5.1.0_PlaybackWindow.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.1.0_PlaybackWindow.png', preview_result)
            case.result = image_result

        # set preview window slider
        with uuid("d8e879e3-9993-4369-aac7-5724d05c96be") as case:
            with uuid("665482c6-7c86-4cb6-912a-6140bce17452") as case:
                main_page.select_library_icon_view_media('Skateboard 02.mp4')
                time.sleep(DELAY_TIME * 4)
                playback_window_page.set_timeline_sliderbar(0.8)
                preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                             file_name=Auto_Ground_Truth_Folder + 'G5.1.1_PlaybackWindowSetSlider.png')
                image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.1.1_PlaybackWindowSetSlider.png',
                                                          preview_result)
                case.result = image_result

        # set preview window timecode
        with uuid("894a879f-cc1e-4129-ae00-369a1129ee40") as case:
            with uuid("ee89262a-9317-4ab3-a253-6a763ca27965") as case:
                main_page.select_library_icon_view_media('Skateboard 02.mp4')
                time.sleep(DELAY_TIME * 4)
                playback_window_page.set_timecode_slidebar('00_00_05_00')
                time.sleep(DELAY_TIME)
                preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                             file_name=Auto_Ground_Truth_Folder + 'G5.1.2_PlaybackWindowSetTimecode.png')
                image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.1.2_PlaybackWindowSetTimecode.png',
                                                          preview_result)
                case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_2(self):
        # set to 400%
        with uuid("ab7b4229-789c-43ff-ae58-ba6d2a1fd8ea") as case:
            main_page.insert_media("Skateboard 01.mp4")
            playback_window_page.Viewer_Zoom_dropdown_menu('400%')
            time.sleep(DELAY_TIME)
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.2.0_PlaybackWindowSet400.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.2.0_PlaybackWindowSet400.png',
                                                      preview_result)
            case.result = image_result

        # set to 300%
        with uuid("845b39cf-09ea-4a32-9589-4ececd6d5df6") as case:
            playback_window_page.Viewer_Zoom_dropdown_menu('300%')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.2.1_PlaybackWindowSet300.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.2.1_PlaybackWindowSet300.png',
                                                      preview_result)
            case.result = image_result

        # set to 200%
        with uuid("d0aca3ae-abfa-4b84-9f64-8c8185cf63d4") as case:
            playback_window_page.Viewer_Zoom_dropdown_menu('200%')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.2.2_PlaybackWindowSet200.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.2.2_PlaybackWindowSet200.png',
                                                      preview_result)
            case.result = image_result

        # set to 100%
        with uuid("ace6854c-237e-4ed9-ba6a-4d617e4bdf61") as case:
            playback_window_page.Viewer_Zoom_dropdown_menu('100%')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.2.3_PlaybackWindowSet100.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.2.3_PlaybackWindowSet100.png',
                                                      preview_result)
            case.result = image_result

        # set to 75%
        with uuid("846c1874-2bb8-4fec-abe1-88a4cd28ad33") as case:
            playback_window_page.Viewer_Zoom_dropdown_menu('75%')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.2.4_PlaybackWindowSet75.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.2.4_PlaybackWindowSet75.png',
                                                      preview_result)
            case.result = image_result

        # set to 50%
        with uuid("a4ff8298-3065-4a7e-83d4-9e2981123a49") as case:
            playback_window_page.Viewer_Zoom_dropdown_menu('50%')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.2.5_PlaybackWindowSet50.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.2.5_PlaybackWindowSet50.png',
                                                      preview_result)
            case.result = image_result

        # set to 25%
        with uuid("fa42362e-a2e1-4bfb-a70e-7d19ab674933") as case:
            playback_window_page.Viewer_Zoom_dropdown_menu('25%')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.2.6_PlaybackWindowSet25.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.2.6_PlaybackWindowSet25.png',
                                                      preview_result)
            case.result = image_result

        # set to 10%
        with uuid("5ff6fda4-0e1e-479d-b99e-67f7c72354a0") as case:
            playback_window_page.Viewer_Zoom_dropdown_menu('10%')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.2.7_PlaybackWindowSet10.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.2.7_PlaybackWindowSet10.png',
                                                      preview_result)
            case.result = image_result

        # set to fit
        with uuid("58d9eb84-0f6b-4591-b5d4-cfbb038db02d") as case:
            playback_window_page.Viewer_Zoom_dropdown_menu('Fit')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.2.8_PlaybackWindowSetFit.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.2.8_PlaybackWindowSetFit.png',
                                                      preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_3(self):
        # play
        with uuid("f6f5f3cc-5704-4c63-8504-98c35621fe3e") as case:
            main_page.select_library_icon_view_media("Skateboard 01.mp4")
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.operation.pause,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.3.0_Play.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.3.0_Play.png',
                                                      preview_result)
            case.result = image_result

        # pause hotkey
        with uuid("06ca2890-d7bc-4c9d-ad1e-7bee17ca6c01") as case:
            with uuid("24f870f9-decb-477b-a163-3c8bda27ae27") as case:
                playback_window_page.press_space_key()
                time.sleep(DELAY_TIME)
                preview_result = mask_designer_page.snapshot(locator=L.playback_window.operation.play,
                                                             file_name=Auto_Ground_Truth_Folder + 'G5.3.1_Pause.png')
                image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.3.1_Pause.png',
                                                          preview_result)
                case.result = image_result

        # stop
        with uuid("4d6e192f-5ac8-4e10-a78e-5485a4547baf") as case:
            playback_window_page.Edit_Timeline_PreviewOperation('Stop')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.3.2_Stop.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.3.2_Stop.png',
                                                      preview_result)
            case.result = image_result

        # next frame
        with uuid("726a12de-8cc9-4a30-ba2e-4bec1141972d") as case:
            playback_window_page.Edit_Timeline_PreviewOperation('Next_Frame')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.3.3_NextFrame.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.3.3_NextFrame.png',
                                                      preview_result)
            case.result = image_result

        # previous frame
        with uuid("2a0a5fbf-d5c9-491f-bc79-1407a9c82d73") as case:
            playback_window_page.Edit_Timeline_PreviewOperation('Previous_Frame')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.3.4_PreviousFrame.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.3.4_PreviousFrame.png',
                                                      preview_result)
            case.result = image_result

        # next frame hotkey
        with uuid("cdb27e4a-f924-46ee-9667-46f52a944320") as case:
            playback_window_page.tap_NextFrame_hotkey()
            time.sleep(DELAY_TIME)
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.3.5_NextFrameHotkey.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.3.5_NextFrameHotkey.png',
                                                      preview_result)
            case.result = image_result

        # stop hotkey
        with uuid("6ab878a3-56b2-4271-84ee-02557ea1a78c") as case:
            playback_window_page.tap_Stop_hotkey()
            time.sleep(DELAY_TIME)
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.3.6_StopHotkey.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.3.5_NextFrameHotkey.png',
                                                      preview_result)
            case.result = image_result

        # fast forward
        with uuid("bb3411d2-9dab-4628-b8a7-f73ef30c2547") as case:
            with uuid("1959eb51-c212-4b77-bec2-52ef98265854") as case:
                with uuid("8389e80c-640f-48d5-8d05-5c93c69d3b6b") as case:
                    with uuid("93b4d137-073d-4fb3-8ac6-3f1af546083d") as case:
                        with uuid("2c287718-cede-4c46-b6bb-b140e5e85478") as case:
                            playback_window_page.Edit_Timeline_PreviewOperation('Fast_Forward')
                            time.sleep(DELAY_TIME)
                            playback_window_page.Edit_Timeline_PreviewOperation('Fast_Forward')
                            time.sleep(DELAY_TIME)
                            playback_window_page.Edit_Timeline_PreviewOperation('Fast_Forward')
                            time.sleep(DELAY_TIME)
                            playback_window_page.tap_FastForward_hotkey()
                            time.sleep(DELAY_TIME)
                            case.result = True

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_4(self):
        # snapshot
        with uuid("f90e8bea-3d40-4347-bd32-8ca3d10a6385") as case:
            main_page.select_library_icon_view_media("Skateboard 01.mp4")
            playback_window_page.Edit_TimelinePreview_ClickTakeSnapshot()
            playback_window_page.Edit_SaveAsSanpshot_FileName(Auto_Ground_Truth_Folder + 'G5.4.0_Snapshot.jpg')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G5.4.0_Snapshot.jpg',
                                                     Auto_Ground_Truth_Folder + 'G5.4.0_Snapshot.jpg')
            case.result = compare_result

        # snapshot hotkey
        with uuid("ca114aa8-b0ee-47e7-b105-4bb2cf791680") as case:
            playback_window_page.tap_Snapshot_hotkey()
            time.sleep(DELAY_TIME)
            playback_window_page.Edit_SaveAsSanpshot_FileName(Auto_Ground_Truth_Folder + 'G5.4.1_Snapshot.jpg')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G5.4.1_Snapshot.jpg',
                                                     Auto_Ground_Truth_Folder + 'G5.4.1_Snapshot.jpg')
            case.result = compare_result



    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_5(self):
        # set to Ultra HD
        with uuid("5d9bbbb7-b644-4198-9b5e-a4dacd3a64d4") as case:
            main_page.insert_media("Skateboard 01.mp4")
            playback_window_page.Edit_TimelinePreview_SetPreviewQuality('Ultra HD')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.5.0_UltraHD.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.5.0_UltraHD.png',
                                                      preview_result)
            case.result = image_result

        # set to Full HD
        with uuid("28ffc392-a540-4d4b-b88c-1ecf09547b2b") as case:
            playback_window_page.Edit_TimelinePreview_SetPreviewQuality('Full HD')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.5.1_FullHD.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.5.1_FullHD.png',
                                                      preview_result)
            case.result = image_result

        # set to Low
        with uuid("fe26d4fb-b90b-4e2a-a4df-12e780b6c3d8") as case:
            playback_window_page.Edit_TimelinePreview_SetPreviewQuality('Low')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.5.2_Low.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.5.2_Low.png',
                                                      preview_result)
            case.result = image_result

        # set to Normal
        with uuid("7136312c-e567-461e-86d2-4f738b4a9b3d") as case:
            playback_window_page.Edit_TimelinePreview_SetPreviewQuality('Normal')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.5.3_Normal.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.5.3_Normal.png',
                                                      preview_result)
            case.result = image_result

        # set to High
        with uuid("6bd248c6-8d75-4311-b67a-0d3f25dda1a9") as case:
            playback_window_page.Edit_TimelinePreview_SetPreviewQuality('High')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.5.4_High.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.5.4_High.png',
                                                      preview_result)
            case.result = image_result

        # set to HD
        with uuid("696097af-afe1-49c5-949b-29d568d70b83") as case:
            playback_window_page.Edit_TimelinePreview_SetPreviewQuality('HD')
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.5.5_HD.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.5.5_HD.png',
                                                      preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_6(self):
        # set grid line 10x10
        with uuid("7bd11589-6210-41ea-ad41-c6495dacf232") as case:
            time.sleep(DELAY_TIME)
            main_page.insert_media("Skateboard 01.mp4")
            time.sleep(DELAY_TIME)
            playback_window_page.Edit_Timeline_Grid_line_format(10)
            time.sleep(DELAY_TIME)
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.6.0_GridLine10x10.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.6.0_GridLine10x10.png',
                                                      preview_result)
            case.result = image_result

        # set grid line 9x9
        with uuid("4e006759-c7e4-4965-9c9d-2e216a670398") as case:
            time.sleep(DELAY_TIME)
            playback_window_page.Edit_Timeline_Grid_line_format(9)
            time.sleep(DELAY_TIME)
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.6.1_GridLine9x9.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.6.1_GridLine9x9.png',
                                                      preview_result)
            case.result = image_result

        # set grid line 8x8
        with uuid("ca3ddce5-7c43-46b4-b7a6-1d04b7bd7687") as case:
            time.sleep(DELAY_TIME)
            playback_window_page.Edit_Timeline_Grid_line_format(8)
            time.sleep(DELAY_TIME)
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.6.2_GridLine8x8.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.6.2_GridLine8x8.png',
                                                      preview_result)
            case.result = image_result

        # set grid line 7x7
        with uuid("585881aa-f528-4ae8-89ae-441262737346") as case:
            time.sleep(DELAY_TIME)
            playback_window_page.Edit_Timeline_Grid_line_format(7)
            time.sleep(DELAY_TIME)
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.6.3_GridLine7x7.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.6.3_GridLine7x7.png',
                                                      preview_result)
            case.result = image_result

        # set grid line 6x6
        with uuid("b799eb4b-15d7-4d9a-9edb-bf4e9759b4ee") as case:
            time.sleep(DELAY_TIME)
            playback_window_page.Edit_Timeline_Grid_line_format(6)
            time.sleep(DELAY_TIME)
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.6.4_GridLine6x6.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.6.4_GridLine6x6.png',
                                                      preview_result)
            case.result = image_result

        # set grid line 5x5
        with uuid("e5651ace-ab7d-4e9a-8518-c884bb7f94a8") as case:
            time.sleep(DELAY_TIME)
            playback_window_page.Edit_Timeline_Grid_line_format(5)
            time.sleep(DELAY_TIME)
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.6.5_GridLine5x5.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.6.5_GridLine5x5.png',
                                                      preview_result)
            case.result = image_result

        # set grid line 4x4
        with uuid("9daa05b6-8921-41b8-a033-474ca5c292ff") as case:
            time.sleep(DELAY_TIME)
            playback_window_page.Edit_Timeline_Grid_line_format(4)
            time.sleep(DELAY_TIME)
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.6.6_GridLine4x4.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.6.6_GridLine4x4.png',
                                                      preview_result)
            case.result = image_result

        # set grid line 3x3
        with uuid("1bdf1052-d3b0-4577-b6fe-6bf049296f62") as case:
            time.sleep(DELAY_TIME)
            playback_window_page.Edit_Timeline_Grid_line_format(3)
            time.sleep(DELAY_TIME)
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.6.7_GridLine3x3.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.6.7_GridLine3x3.png',
                                                      preview_result)
            case.result = image_result

        # set grid line 2x2
        with uuid("437f4372-80f6-46d8-a1f0-970404c51d83") as case:
            time.sleep(DELAY_TIME)
            playback_window_page.Edit_Timeline_Grid_line_format(2)
            time.sleep(DELAY_TIME)
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.6.8_GridLine2x2.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.6.8_GridLine2x2.png',
                                                      preview_result)
            case.result = image_result

        # set grid line None
        with uuid("81bf6a26-801f-43ef-994f-f11715035907") as case:
            time.sleep(DELAY_TIME)
            playback_window_page.Edit_Timeline_Grid_line_format(1)
            time.sleep(DELAY_TIME)
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.6.9_GridLineNone.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.6.9_GridLineNone.png',
                                                      preview_result)
            case.result = image_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_7(self):
        # undock
        with uuid("3462cb42-35c1-4f7b-8674-1e188fd312d6") as case:
            main_page.insert_media("Skateboard 01.mp4")
            playback_window_page.Edit_TimelinePreview_ClickUnDock()
            time.sleep(DELAY_TIME)
            library_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                      file_name=Auto_Ground_Truth_Folder + 'G5.7.0_Undock.png')
            compare_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.7.0_Undock.png',
                                                     library_result)
            case.result = compare_result

        # minimize
        with uuid("5775d9e3-5d2a-4d89-9200-53034c3ec9a2") as case:
            playback_window_page.Edit_TImelinePreview_ClickMinimize()
            time.sleep(DELAY_TIME)
            library_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.7.1_Minimize.png')
            compare_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.7.1_Minimize.png',
                                                          library_result)
            case.result = compare_result

        # show timeline preview
        with uuid("da511a2b-56b4-4098-acc0-ace62f11e326") as case:
            playback_window_page.Edit_TimelinePreview_ClickShowTimelinePreview()
            time.sleep(DELAY_TIME)
            library_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.7.2_ShowTimelinePreview.png')
            compare_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.7.2_ShowTimelinePreview.png',
                                                          library_result)
            case.result = compare_result

        # maximize / restore down
        with uuid("68050910-3b43-4fc9-92e8-5b88dc9554cc") as case:
            playback_window_page.Edit_TimelinePreview_ClickMaximize_RestoreDown()
            time.sleep(DELAY_TIME)
            library_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.7.3_Maximize.png')
            compare_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.7.3_Maximize.png',
                                                          library_result)
            case.result = compare_result
            playback_window_page.Edit_TimelinePreview_ClickMaximize_RestoreDown()

        # dock
        with uuid("80be242f-d60e-46b7-b4c8-a48bfb9cfc81") as case:
            playback_window_page.Edit_TimelinePreview_ClickDock()
            time.sleep(DELAY_TIME)
            library_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.7.4_Dock.png')
            compare_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.7.4_Dock.png',
                                                          library_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_8(self):
        # double click enter full screen
        with uuid("3462cb42-35c1-4f7b-8674-1e188fd312d6") as case:
            main_page.insert_media("Skateboard 01.mp4")
            playback_window_page.Edit_TimelinePreview_ClickUnDock()
            playback_window_page.Edit_TimelinePreview_DoubleClick_EnterFullScreen()
            time.sleep(DELAY_TIME * 4)
            library_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.8.0_DoubleClickEnterFullScreen.png')
            compare_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.8.0_DoubleClickEnterFullScreen.png',
                                                          library_result)
            case.result = compare_result
            playback_window_page.press_esc_key()

        # enter full screen
        with uuid("dae28834-67f2-4e83-8a82-e7c59af702d0") as case:
            playback_window_page.Edit_TImelinePreview_ClickViewFullScreen()
            time.sleep(DELAY_TIME * 4)
            library_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.8.1_EnterFullScreen.png')
            compare_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.8.1_EnterFullScreen.png',
                                                          library_result)
            case.result = compare_result
            playback_window_page.press_esc_key()

        # hotkey to enter full screen
        with uuid("b0268a28-9448-4739-a732-2f6830ec0bf4") as case:
            playback_window_page.EnterFullScreen_hotkey()
            time.sleep(DELAY_TIME * 4)
            library_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.8.2_EnterFullScreenByHotkey.png')
            compare_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.8.2_EnterFullScreenByHotkey.png',
                                                          library_result)
            case.result = compare_result
            playback_window_page.press_esc_key()
            playback_window_page.Edit_TimelinePreview_ClickDock()


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_9(self):
        # right click play
        with uuid("8e54f997-99b7-4d97-b7b5-0752fef45848") as case:
            main_page.select_library_icon_view_media("Skateboard 01.mp4")
            time.sleep(DELAY_TIME)
            current_result = playback_window_page.context.click_play_pause()
            time.sleep(DELAY_TIME * 2)
            playback_window_page.context.click_play_pause()
            case.result = current_result

        # right click stop
        with uuid("ea1ffc17-56b3-4aa0-81a1-d2e58714c7c4") as case:
            current_result = playback_window_page.context.click_stop()
            case.result = current_result

        # right click next frame
        with uuid("17236d4b-3a15-4aee-9861-4d285da00194") as case:
            current_result = playback_window_page.context.click_next_frame()
            case.result = current_result

        # right click previous frame
        with uuid("91d38960-eb28-4964-a6f1-ae757a9064ca") as case:
            current_result = playback_window_page.context.click_next_frame()
            case.result = current_result

        # right click fast forward
        with uuid("73d96279-06ae-4d26-8336-5289cebd7d4f") as case:
            with uuid("5daacef4-385f-417b-b363-630854372ad8") as case:
                with uuid("d5f08302-60ef-4b01-b0dc-90f664393dd1") as case:
                    with uuid("0d8ec559-c136-40a4-bf89-3aa19595a3f3") as case:
                        current_result = playback_window_page.context.click_fastforward()
                        playback_window_page.context.click_fastforward()
                        playback_window_page.context.click_fastforward()
                        playback_window_page.context.click_fastforward()
                        case.result = current_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_10(self):
        # right click Ultra HD
        with uuid("2aaac657-70bf-4d0a-96e0-e98387b4d987") as case:
            main_page.insert_media("Skateboard 01.mp4")
            playback_window_page.context.click_quality_ultra_hd()
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.10.0_RightClickUltraHD.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.10.0_RightClickUltraHD.png',
                                                      preview_result)
            case.result = image_result

        # right click Full HD
        with uuid("29f084a1-cd82-4e47-8bba-fa0de897f660") as case:
            playback_window_page.context.click_quality_full_hd()
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.10.1_RightClickFullHD.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.10.1_RightClickFullHD.png',
                                                      preview_result)
            case.result = image_result

        # right click Low
        with uuid("75b9d9b0-5802-4464-8843-4826b6d39152") as case:
            playback_window_page.context.click_quality_low()
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.10.2_RightClickLow.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.10.2_RightClickLow.png',
                                                      preview_result)
            case.result = image_result

        # right click Normal
        with uuid("3099cae9-ecd9-471b-97aa-43922b55ff45") as case:
            playback_window_page.context.click_quality_normal()
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.10.3_RightClickNormal.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.10.3_RightClickNormal.png',
                                                      preview_result)
            case.result = image_result

        # right click High
        with uuid("3ce338b3-a222-4009-9586-c849218fa459") as case:
            playback_window_page.context.click_quality_high()
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.10.4_RightClickHigh.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.10.4_RightClickHigh.png',
                                                      preview_result)
            case.result = image_result

        # right click HD
        with uuid("b41469c7-7724-4cf4-b7ff-524794e2da2d") as case:
            playback_window_page.context.click_quality_hd()
            preview_result = mask_designer_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.10.5_RightClickHD.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G5.10.5_RightClickHD.png',
                                                      preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_11(self):
        # right click next second
        with uuid("c12e6a35-cad0-4d2d-9b73-cefdff1465d6") as case:
            main_page.insert_media("Skateboard 01.mp4")
            playback_window_page.context.click_next_sec()
            preview_result = playback_window_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.11.0_RightClickNextSecond.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.11.0_RightClickNextSecond.png',
                                                      preview_result)
            case.result = image_result

        # right click previous second
        with uuid("bd2ec1a0-1e72-47a0-8d1d-4c64e3e8e155") as case:
            playback_window_page.context.click_previous_sec()
            preview_result = playback_window_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G5.11.1_RightClickPreviousSecond.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.11.1_RightClickPreviousSecond.png',
                                                      preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_12(self):
        # right click modify
        with uuid("bea868ad-4a23-4e75-9832-b4352224c24c") as case:
            main_page.insert_media("Skateboard 01.mp4")
            playback_window_page.context.click_edit_modify()
            time.sleep(DELAY_TIME)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.12.0_RightClickModify.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.12.0_RightClickModify.png',
                                                        preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_13(self):
        # right click trim
        with uuid("d8296b44-5f90-40d4-91e2-b88902a7a84c") as case:
            main_page.insert_media("Skateboard 01.mp4")
            playback_window_page.context.click_edit_trim()
            time.sleep(DELAY_TIME)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.13.0_RightClickTrim.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.13.0_RightClickTrim.png',
                                                        preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_14(self):
        # right click fix enhance
        with uuid("7a69a1fa-bf11-4b27-8677-3c689c433c66") as case:
            main_page.insert_media("Skateboard 01.mp4")
            playback_window_page.context.click_edit_fix_enhance()
            time.sleep(DELAY_TIME)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.14.0_RightClickFixEnhance.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.14.0_RightClickFixEnhance.png',
                                                        preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_15(self):
        # right click Pan and Zoom
        with uuid("4b035674-0d91-4930-bedf-127e763109cd") as case:
            main_page.insert_media("Food.jpg")
            playback_window_page.context.click_edit_pan_and_zoom()
            time.sleep(DELAY_TIME * 8)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.15.0_RightClickPanAndZoom.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.15.0_RightClickPanAndZoom.png',
                                                        preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_16(self):
        # right click 400%
        with uuid("249034a2-0fc4-4373-b523-38a82bff47f6") as case:
            main_page.insert_media("Skateboard 01.mp4")
            playback_window_page.context.click_zoom_400()
            time.sleep(DELAY_TIME)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.16.0_RightClick400.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.16.0_RightClick400.png',
                                                        preview_result)
            case.result = image_result

        # right click 300%
        with uuid("28623ca0-1241-49dc-bcbf-3f3776c6f680") as case:
            playback_window_page.context.click_zoom_300()
            time.sleep(DELAY_TIME)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.16.1_RightClick300.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.16.1_RightClick300.png',
                                                        preview_result)
            case.result = image_result

        # right click 200%
        with uuid("91fee5cf-49ad-46dc-891c-4a2f2894d866") as case:
            playback_window_page.context.click_zoom_200()
            time.sleep(DELAY_TIME)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.16.2_RightClick200.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.16.2_RightClick200.png',
                                                        preview_result)
            case.result = image_result

        # right click 100%
        with uuid("3a6276fe-a792-4230-bd8d-231a8b2fc589") as case:
            playback_window_page.context.click_zoom_100()
            time.sleep(DELAY_TIME)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.16.3_RightClick100.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.16.3_RightClick100.png',
                                                        preview_result)
            case.result = image_result

        # right click 75%
        with uuid("8fa92cb9-1a8e-42c0-8b31-3795f4608a9a") as case:
            playback_window_page.context.click_zoom_75()
            time.sleep(DELAY_TIME)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.16.4_RightClick75.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.16.4_RightClick75.png',
                                                        preview_result)
            case.result = image_result

        # right click 50%
        with uuid("9e31c6e1-adec-41ea-9a54-d4474981fabd") as case:
            playback_window_page.context.click_zoom_50()
            time.sleep(DELAY_TIME)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.16.5_RightClick50.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.16.5_RightClick50.png',
                                                        preview_result)
            case.result = image_result

        # right click 25%
        with uuid("ad90ec92-1ec6-4222-bc83-3d145f840e9b") as case:
            playback_window_page.context.click_zoom_25()
            time.sleep(DELAY_TIME)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.16.6_RightClick25.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.16.6_RightClick25.png',
                                                        preview_result)
            case.result = image_result

        # right click 10%
        with uuid("a9480ee5-280c-4a35-9f7e-893a777df929") as case:
            playback_window_page.context.click_zoom_10()
            time.sleep(DELAY_TIME)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.16.7_RightClick10.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.16.7_RightClick10.png',
                                                        preview_result)
            case.result = image_result

        # right click fit
        with uuid("6eb4dccc-5e19-415b-b861-e18317cc1876") as case:
            playback_window_page.context.click_zoom_fit()
            time.sleep(DELAY_TIME)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.16.8_RightClickFit.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.16.8_RightClickFit.png',
                                                        preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_17(self):
        # right click undock dock
        with uuid("249034a2-0fc4-4373-b523-38a82bff47f6") as case:
            main_page.insert_media("Skateboard 01.mp4")
            playback_window_page.context.click_dock_undock_preview_window()
            time.sleep(DELAY_TIME)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.17.0_RightClickUndock.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.17.0_RightClickUndock.png',
                                                        preview_result)
            case.result = image_result
            playback_window_page.context.click_dock_undock_preview_window()

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_18(self):
        # volume meter in library gray out
        with uuid("e42edb8f-bd50-4805-9d8f-ac33cd58fce8") as case:
            with uuid("42603494-f348-46eb-8bb9-b747a85ff039") as case:
                with uuid("bda755df-b886-44d3-9c05-bb799fa0dba1") as case:
                    time.sleep(DELAY_TIME * 4)
                    main_page.top_menu_bar_view_show_timeline_preview_volume_meter()
                    time.sleep(DELAY_TIME * 4)
                    main_page.select_library_icon_view_media("Skateboard 01.mp4")
                    time.sleep(DELAY_TIME)
                    preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                                   file_name=Auto_Ground_Truth_Folder + 'G5.18.0_VolumeMeterInLibrary.png')
                    image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.18.0_VolumeMeterInLibrary.png',
                                                                preview_result)
                    case.result = image_result

        # volume meter timeline
        with uuid("ec075772-6e96-4550-9cd4-02d7e87cf1a3") as case:
            main_page.insert_media("Skateboard 01.mp4")
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.18.1_VolumeMeterTimeline.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.18.1_VolumeMeterTimeline.png',
                                                        preview_result)
            case.result = image_result

        # volume meter 5.1ch
        with uuid("eae33b7d-f69b-4346-8981-5050d71ad6fa") as case:
            main_page.click_set_user_preferences()
            preferences_page.general.audio_channels_set_51_surround()
            preferences_page.click_ok()
            time.sleep(DELAY_TIME)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.18.2_VolumeMeter51.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.18.2_VolumeMeter51.png',
                                                        preview_result)
            case.result = image_result
            main_page.click_set_user_preferences()
            preferences_page.general.audio_channels_set_stereo()
            preferences_page.click_ok()

        # volume meter relaunch
        with uuid("6b0aeff5-cc3a-42aa-9727-262407d51c36") as case:
            main_page.close_app()
            main_page.start_app()
            time.sleep(DELAY_TIME * 8)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.18.3_VolumeMeterRelaunchPDR.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.18.3_VolumeMeterRelaunchPDR.png',
                                                        preview_result)
            case.result = image_result


        # volume meter close
        with uuid("c39ac2ff-eccb-4c0f-be53-6231f24cbc89") as case:
            main_page.top_menu_bar_view_show_timeline_preview_volume_meter()
            time.sleep(DELAY_TIME * 8)
            preview_result = playback_window_page.snapshot(locator=L.library_preview.upper_view_region,
                                                           file_name=Auto_Ground_Truth_Folder + 'G5.18.4_VolumeMeterClose.png')
            image_result = playback_window_page.compare(Ground_Truth_Folder + 'G5.18.4_VolumeMeterClose.png',
                                                        preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_5_19(self):
        # full screen mode play
        with uuid("2e5b06e8-b7bb-4130-aa5f-8018dec11889") as case:
            main_page.insert_media("Skateboard 01.mp4")
            playback_window_page.Edit_TimelinePreview_ClickUnDock()
            time.sleep(DELAY_TIME * 2)
            playback_window_page.Edit_TImelinePreview_ClickViewFullScreen()
            time.sleep(DELAY_TIME * 2)
            playback_window_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            playback_window_page.press_space_key()
            case.result = True

        # full screen mode stop
        with uuid("18e351b0-ec6d-4a02-8738-9528f354d8b7") as case:
            time.sleep(DELAY_TIME * 2)
            playback_window_page.tap_Stop_hotkey()
            time.sleep(DELAY_TIME * 2)
            case.result = True

        # full screen mode next frame
        with uuid("71c660fd-f4c0-40ab-b975-18011cf7b084") as case:
            time.sleep(DELAY_TIME * 2)
            playback_window_page.tap_NextFrame_hotkey()
            time.sleep(DELAY_TIME * 2)
            case.result = True

        # full screen mode fast forward
        with uuid("99c5dbf6-d35e-413c-805a-2eac0075b3eb") as case:
            time.sleep(DELAY_TIME * 2)
            playback_window_page.tap_NextFrame_hotkey()
            time.sleep(DELAY_TIME * 2)
            case.result = True
            playback_window_page.tap_Stop_hotkey()
            time.sleep(DELAY_TIME * 2)

        # full screen mode esc
        with uuid("e2fe9192-b511-4ace-9e0e-c28dea66bd09") as case:
            playback_window_page.press_esc_key()
            case.result = True
            time.sleep(DELAY_TIME * 2)
            playback_window_page.Edit_TimelinePreview_ClickDock()


    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    cc5899da-36ed-4bc1-a696-e17f99666d50
                    ea8bb882-f300-43c2-80d2-7cb5927e44bb
                    ea330263-b58b-4d3d-8908-00b32a0e83c2
                    c39ac2ff-eccb-4c0f-be53-6231f24cbc89
                    21e3eddc-d38a-4400-9779-713784562b66
                    8d48c6eb-ca54-4a6f-aef4-e164bcb323f6
                    b27e1631-60a9-46e4-adfe-fa1bd07534b9
                    161f7bdd-061f-4f6a-8484-b9a2a443b718
                    3dc5a750-99f0-4d36-bd80-54c477dab3c6
                    591cfca9-ed3a-41e9-838d-97707003e26d
                    bd112d62-b264-4d7a-8afb-033d8e34c748
                    8f09b5aa-0c89-4c23-b064-82f726b6f04d
                    235b5e96-8b82-447d-b43f-11d1be80dd72
                    1ea609e7-98b4-4d19-9966-615e3d8de400
                ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"











































