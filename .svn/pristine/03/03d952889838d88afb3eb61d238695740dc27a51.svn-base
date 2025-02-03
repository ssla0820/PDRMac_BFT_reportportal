import sys, os

from SFT.globals import get_enable_case_execution_log, google_sheet_execution_log_init, update_report_info, \
    google_sheet_execution_log_update_result

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

# for update_report_info
from globals import *

# read PDR cap >>
app = SimpleNamespace(**PDR_cap)
# read PDR cap <<

# create driver & page >>
mac = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mac)
# base_page = PageFactory().get_page_object('base_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page', mac)
library_preview_page = PageFactory().get_page_object('library_preview_page', mac)
mask_designer_page = PageFactory().get_page_object('mask_designer_page', mac)
effect_room_page = PageFactory().get_page_object('effect_room_page', mac)
pip_room_page = PageFactory().get_page_object('pip_room_page', mac)
particle_room_page = PageFactory().get_page_object('particle_room_page', mac)
title_room_page = PageFactory().get_page_object('title_room_page', mac)
transition_room_page = PageFactory().get_page_object('transition_room_page', mac)
playback_window_page = PageFactory().get_page_object('playback_window_page', mac)
preferences_page = PageFactory().get_page_object('preferences_page', mac)
pan_zoom_page = PageFactory().get_page_object('pan_zoom_page', mac)
tips_area_page = PageFactory().get_page_object('tips_area_page', mac)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mac)
produce_page = PageFactory().get_page_object('produce_page', mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Range Selection.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<


# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/range_selection/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/range_selection/'
Test_Material_Folder = app.testing_material

#Ground_Truth_Folder = '/Users/cl/Desktop/Ernesto_MacAT_M3/SFT/ground_truth/range_selection/'
#Auto_Ground_Truth_Folder = '/Users/cl/Desktop/Ernesto_MacAT_M3/SFT/auto_ground_truth/range_selection/'
#Test_Material_Folder = '/Users/cl/Desktop/Ernesto_MacAT/Material/'

DELAY_TIME = 1



class Test_Range_Selection():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME * 3)
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
            google_sheet_execution_log_init('Range_Selection')

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
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number,
                                                     report.get_ovinfo('na'),
                                                     report.get_ovinfo('skip'),
                                                     report.get_ovinfo('duration'))
        report.show()

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_1(self):
        # Range selection mark in and mark out
        with uuid("654bee3d-bc65-48ff-8bfb-03483a6ee0bc") as case:
            with uuid("3b76d640-94ee-4793-a7ca-2a74ee06e40b") as case:
                main_page.insert_media("Skateboard 01.mp4")
                timeline_operation_page.timeline_click_zoomin_btn()
                time.sleep(DELAY_TIME)
                timeline_operation_page.timeline_click_zoomin_btn()
                time.sleep(DELAY_TIME)
                timeline_operation_page.timeline_click_zoomin_btn()
                time.sleep(DELAY_TIME)
                timeline_operation_page.set_range_markin_markout(30,180)
                preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.1.0_Range_Select_Mark_In_Out.png')
                image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.1.0_Range_Select_Mark_In_Out.png',
                                                     preview_result)
                case.result = image_result

        # Range selection copy
        with uuid("e94c89d3-4470-458a-9008-ef415e095705") as case:
            case.result = tips_area_page.click_TipsArea_btn_Copy()

        # Range selection cut
        with uuid("690b557a-72a3-49da-92ad-341ae18a1ba3") as case:
            tips_area_page.click_TipsArea_btn_Cut()
            time.sleep(DELAY_TIME * 2)
            preview_result = timeline_operation_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.1.2_Range_Select_Cut.png')
            image_result = timeline_operation_page.compare(Ground_Truth_Folder + 'G1.1.2_Range_Select_Cut.png',
                                                    preview_result)
            case.result = image_result

        # Range selection paste
        with uuid("732a4715-917b-48ff-a04e-562f3783b643") as case:
            tips_area_page.click_TipsArea_btn_Paste()
            time.sleep(DELAY_TIME * 2)
            preview_result = timeline_operation_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.1.3_Range_Select_Paste.png')
            image_result = timeline_operation_page.compare(Ground_Truth_Folder + 'G1.1.3_Range_Select_Paste.png',
                                                    preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_2(self):
        # Range selection hotkey copy
        with uuid("93267f9c-11f9-4e08-8291-c12ca8b5b525") as case:
            main_page.insert_media("Skateboard 01.mp4")
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.set_range_markin_markout(30, 180)
            main_page.tap_Copy_hotkey()
            time.sleep(DELAY_TIME * 2)
            case.result = True

        # Range selection hotkey cut
        with uuid("3daddc9c-f4f7-47cc-92f4-965825b91abf") as case:
            with uuid("b84b1014-a24b-4434-b402-4e830d965496") as case:
                with uuid("bf863ebd-32ad-4a5e-967d-f25c03481647") as case:
                    main_page.tap_Cut_hotkey()
                    time.sleep(DELAY_TIME * 2)
                    preview_result = timeline_operation_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                            file_name=Auto_Ground_Truth_Folder + 'G1.2.1_Range_Select_Cut_Hotkey.png')
                    image_result = timeline_operation_page.compare(Ground_Truth_Folder + 'G1.2.1_Range_Select_Cut_Hotkey.png',
                                                         preview_result)
                    case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_3(self):
        # Range selection remove
        with uuid("20da53be-814e-46fd-afa2-5993a75e4d27") as case:
            main_page.insert_media("Skateboard 01.mp4")
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_Remove()
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.0_Range_Select_Remove.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.3.0_Range_Select_Remove.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_4(self):
        # Range selection right click menu copy
        with uuid("413a2ced-e22f-49f8-8938-d9c2565d1b49") as case:
            main_page.insert_media("Skateboard 01.mp4")
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Copy')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.4.0_Range_Select_RightClickMenu_Copy.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.4.0_Range_Select_RightClickMenu_Copy.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_5(self):
        # Range selection right click menu cut and leave gap
        with uuid("45b243cc-ba68-48f7-8444-a0a1dfb3cab2") as case:
            main_page.insert_media("Skateboard 01.mp4")
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Cut','Cut and Leave Gap')
            time.sleep(DELAY_TIME * 2)
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.5.0_Range_Select_RightClickMenu_CutAndLeaveGap.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.5.0_Range_Select_RightClickMenu_CutAndLeaveGap.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_6(self):
        # Range selection right click menu cut and fill gap
        with uuid("5a192574-ecfd-41b1-9105-ee220a7a342e") as case:
            main_page.insert_media("Skateboard 01.mp4")
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Cut','Cut and Fill Gap')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.6.0_Range_Select_RightClickMenu_CutAndFillGap.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.6.0_Range_Select_RightClickMenu_CutAndFillGap.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_7(self):
        # Range selection right click menu cut fill gap and move all clip
        with uuid("863a62ee-2373-4060-88cd-dd6c7114f267") as case:
            main_page.insert_media("Skateboard 01.mp4")
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Cut','Cut, Fill Gap, and Move All Clips')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.7.0_Range_Select_RightClickMenu_CutFillGapAndMoveAll.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.7.0_Range_Select_RightClickMenu_CutFillGapAndMoveAll.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_8(self):
        # Range selection right click menu remove and leave gap
        with uuid("bb7c939e-879e-493d-a07f-75e99ef01b67") as case:
            main_page.insert_media("Skateboard 01.mp4")
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Remove','Remove and Leave Gap')
            time.sleep(DELAY_TIME*2)
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.8.0_Range_Select_RightClickMenu_RemoveAndLeaveGap.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.8.0_Range_Select_RightClickMenu_RemoveAndLeaveGap.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_9(self):
        # Range selection right click menu remove and fill gap
        with uuid("4cbd2dc8-62df-41d7-b21b-7d421bef99b6") as case:
            main_page.insert_media("Skateboard 01.mp4")
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Remove','Remove and Fill Gap')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.9.0_Range_Select_RightClickMenu_RemoveAndFillGap.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.9.0_Range_Select_RightClickMenu_RemoveAndFillGap.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_10(self):
        # Range selection right click menu remove and fill gap
        with uuid("fde9990b-211a-4df9-b31b-e768ffae0081") as case:
            main_page.insert_media("Skateboard 01.mp4")
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Remove','Remove, Fill Gap, and Move All Clips')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.10.0_Range_Select_RightClickMenu_RemoveFillGapAndMoveAllClips.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.10.0_Range_Select_RightClickMenu_RemoveFillGapAndMoveAllClips.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_11(self):
        # Range selection hotkey remove
        with uuid("7b60f0ff-00e8-454f-8e0d-a1ec86708baa") as case:
            with uuid("7c6e6c28-df54-4100-9147-bcbce8670d66") as case:
                with uuid("89f53c30-3077-45c8-9e26-4a8c6e11c685") as case:
                    main_page.insert_media("Skateboard 01.mp4")
                    timeline_operation_page.set_range_markin_markout(30, 180)
                    timeline_operation_page.timeline_click_zoomin_btn()
                    time.sleep(DELAY_TIME)
                    timeline_operation_page.timeline_click_zoomin_btn()
                    time.sleep(DELAY_TIME)
                    timeline_operation_page.timeline_click_zoomin_btn()
                    time.sleep(DELAY_TIME)
                    main_page.tap_Remove_hotkey()
                    time.sleep(DELAY_TIME * 2)
                    preview_result = timeline_operation_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                                      file_name=Auto_Ground_Truth_Folder + 'G1.11.0_Range_Select_Remove_Hotkey.png')
                    image_result = timeline_operation_page.compare(
                        Ground_Truth_Folder + 'G1.11.0_Range_Select_Remove_Hotkey.png',
                        preview_result)
                    case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_12(self):
        # Range selection right click menu loop playback
        with uuid("fedfc1ed-b761-4540-bb5d-fa60345d88c1") as case:
            main_page.insert_media("Skateboard 01.mp4")
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Loop Playback')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.12.0_Range_Select_RightClickMenu_LoopPlayback.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.12.0_Range_Select_RightClickMenu_LoopPlayback.png',
                                                 preview_result)
            case.result = image_result

        # Range selection right click menu lock range
        with uuid("685cdca4-f95d-4491-9c25-eace59a1783e") as case:
            timeline_operation_page.right_click_range_select_menu('Lock Range')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.12.1_Range_Select_RightClickMenu_LockRange.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.12.1_Range_Select_RightClickMenu_LockRange.png',
                                                 preview_result)
            case.result = image_result

        # Range selection right click menu produce range
        with uuid("da98e668-7d18-4903-8b4a-831ca8f31606") as case:
            timeline_operation_page.right_click_range_select_menu('Export Range')
            time.sleep(DELAY_TIME * 5)
            preview_result = pan_zoom_page.snapshot(locator=L.produce.btn_start_produce,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.12.2_Range_Select_RightClickMenu_ProduceRange.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.12.2_Range_Select_RightClickMenu_ProduceRange.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_13(self):
        # Range selection lock range
        with uuid("c7107547-d1ed-4a56-8e37-6d44b8c31a4a") as case:
            main_page.insert_media("Skateboard 01.mp4")
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_Lock_Range()
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.13.0_Range_Select_LockRange.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.13.0_Range_Select_LockRange.png',
                                                 preview_result)
            case.result = image_result

        # Range selection produce range
        with uuid("8bca1f64-4917-4b89-9783-733e6ad4aa34") as case:
            tips_area_page.click_TipsArea_btn_Produce_Range()
            preview_result = pan_zoom_page.snapshot(locator=L.produce.btn_start_produce,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.13.1_Range_Select_ProduceRange.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.13.1_Range_Select_ProduceRange.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_14(self):
        # Range selection render preview
        with uuid("d484f4ab-b2ef-4f33-8652-1295d835f0d9") as case:
            main_page.insert_media("Skateboard 01.mp4")
            timeline_operation_page.set_range_markin_markout(10,240)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.edit_timeline_render_preview()
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.14.0_Range_Select_RenderPreview.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.14.0_Range_Select_RenderPreview.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_15(self):
        # Media with effect Range selection right click menu copy
        with uuid("73ed2fd5-7481-4ec4-8032-1cdf4af6c8b3") as case:
            main_page.insert_media("Skateboard 01.mp4")
            main_page.enter_room(3)
            effect_room_page.apply_effect_to_video('Aberration',0,0)
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Copy')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.15.0_MediaEffect_Range_Select_RightClickMenu_Copy.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.15.0_MediaEffect_Range_Select_RightClickMenu_Copy.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_16(self):
        # Media with effect Range selection right click menu cut and leave gap
        with uuid("8dadae6f-716f-4ff8-bac7-ab1a7e3cfcec") as case:
            main_page.insert_media("Skateboard 01.mp4")
            main_page.enter_room(3)
            effect_room_page.apply_effect_to_video('Aberration',0,0)
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Cut','Cut and Leave Gap')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.16.0_MediaEffect_Range_Select_RightClickMenu_CutAndLeaveGap.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.16.0_MediaEffect_Range_Select_RightClickMenu_CutAndLeaveGap.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_17(self):
        # Media with effect Range selection right click menu cut and fill gap
        with uuid("47ec53c5-edb1-4c1b-8fa5-8f1a9449f853") as case:
            main_page.insert_media("Skateboard 01.mp4")
            main_page.enter_room(3)
            effect_room_page.apply_effect_to_video('Aberration',0,0)
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Cut','Cut and Fill Gap')
            time.sleep(DELAY_TIME*2)
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.17.0_MediaEffect_Range_Select_RightClickMenu_CutAndFillGap.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.17.0_MediaEffect_Range_Select_RightClickMenu_CutAndFillGap.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_18(self):
        # Media with effect Range selection right click menu cut fill gap and move all clips
        with uuid("5441163a-7b82-41e0-aad2-76b3160253d7") as case:
            main_page.insert_media("Skateboard 01.mp4")
            main_page.enter_room(3)
            main_page.timeline_select_track(1)
            effect_room_page.apply_effect_to_video('Aberration',0,0)
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Cut','Cut, Fill Gap, and Move All Clips')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.18.0_MediaEffect_Range_Select_RightClickMenu_CutFillGapAndMoveAllClips.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.18.0_MediaEffect_Range_Select_RightClickMenu_CutFillGapAndMoveAllClips.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_19(self):
        # Media with effect Range selection hotkey copy
        with uuid("426ae485-bf34-44b9-92dc-07c33ccba923") as case:
            main_page.insert_media("Skateboard 01.mp4")
            main_page.enter_room(3)
            main_page.timeline_select_track(1)
            effect_room_page.apply_effect_to_video('Aberration', 0, 0)
            timeline_operation_page.set_range_markin_markout(30, 180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            main_page.tap_Copy_hotkey()
            time.sleep(DELAY_TIME * 2)
            case.result = True

        # Media with effect Range selection hotkey cut
        with uuid("8d4dd061-3e59-4dd5-912e-30b229b3a17a") as case:
            with uuid("6565e753-b2e7-4b5c-b37a-2c708e627c0e") as case:
                with uuid("9c75399e-008f-4fea-8e9b-c4f717d0fad6") as case:
                    main_page.tap_Cut_hotkey()
                    time.sleep(DELAY_TIME * 2)
                    preview_result = timeline_operation_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                                      file_name=Auto_Ground_Truth_Folder + 'G1.19.0_MediaEffect_Range_Select_Cut_Hotkey.png')
                    image_result = timeline_operation_page.compare(
                        Ground_Truth_Folder + 'G1.19.0_MediaEffect_Range_Select_Cut_Hotkey.png',
                        preview_result)
                    case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_20(self):
        # Media with effect Range selection right click menu remove and leave gap
        with uuid("ced7a904-8acb-4c6f-bb78-d96cbb8da2f4") as case:
            main_page.insert_media("Skateboard 01.mp4")
            main_page.enter_room(3)
            main_page.timeline_select_track(1)
            effect_room_page.apply_effect_to_video('Aberration',0,0)
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            time.sleep(3)
            timeline_operation_page.right_click_range_select_menu('Remove','Remove and Leave Gap')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.20.0_MediaEffect_Range_Select_RightClickMenu_RemoveAndLeaveGap.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.20.0_MediaEffect_Range_Select_RightClickMenu_RemoveAndLeaveGap.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_21(self):
        # Media with effect Range selection right click menu remove and fill gap
        with uuid("8f417dc9-ddd0-40f1-9986-779ad8b4f89e") as case:
            main_page.insert_media("Skateboard 01.mp4")
            main_page.enter_room(3)
            time.sleep(DELAY_TIME*2)
            main_page.timeline_select_track(1)
            effect_room_page.apply_effect_to_video('Aberration',0,0)

            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Remove','Remove and Fill Gap')
            time.sleep(DELAY_TIME*2)
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.21.0_MediaEffect_Range_Select_RightClickMenu_RemoveAndFillGap.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.21.0_MediaEffect_Range_Select_RightClickMenu_RemoveAndFillGap.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_22(self):
        # Media with effect Range selection right click menu remove fill gap and move all clips
        with uuid("4110612c-b7c4-48ff-a154-03215d48628a") as case:
            main_page.insert_media("Skateboard 01.mp4")
            main_page.enter_room(3)
            time.sleep(DELAY_TIME * 2)
            main_page.timeline_select_track(1)
            effect_room_page.apply_effect_to_video('Aberration',0,0)
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Remove','Remove, Fill Gap, and Move All Clips')
            time.sleep(DELAY_TIME * 2)
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.22.0_MediaEffect_Range_Select_RightClickMenu_RemoveFillGapAndMoveAllClips.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.22.0_MediaEffect_Range_Select_RightClickMenu_RemoveFillGapAndMoveAllClips.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_23(self):
        # Media with effect Range selection hotkey remove
        with uuid("1583011c-aa77-4bd6-85df-6f2c228ed126") as case:
            with uuid("1933aede-6980-44c4-b5d2-77ccd5ba7fd9") as case:
                with uuid("f843e839-2adb-4b73-8c76-30eaa90307e2") as case:
                    main_page.insert_media("Skateboard 01.mp4")
                    main_page.enter_room(3)
                    time.sleep(DELAY_TIME * 2)
                    main_page.timeline_select_track(1)
                    timeline_operation_page.timeline_click_zoomin_btn()
                    time.sleep(DELAY_TIME)
                    timeline_operation_page.timeline_click_zoomin_btn()
                    time.sleep(DELAY_TIME)
                    timeline_operation_page.timeline_click_zoomin_btn()
                    time.sleep(DELAY_TIME)

                    effect_room_page.apply_effect_to_video('Aberration', 0, 0)
                    time.sleep(DELAY_TIME)
                    timeline_operation_page.set_range_markin_markout(30, 180)
                    time.sleep(DELAY_TIME * 2)
                    main_page.tap_Remove_hotkey()
                    time.sleep(DELAY_TIME * 3)
                    preview_result = timeline_operation_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                                      file_name=Auto_Ground_Truth_Folder + 'G1.23.0_MediaEffect_Range_Select_Remove_Hotkey.png')
                    image_result = timeline_operation_page.compare(
                        Ground_Truth_Folder + 'G1.23.0_MediaEffect_Range_Select_Remove_Hotkey.png',
                        preview_result)
                    case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_24(self):
        # Media with effect Range selection right click menu loop playback
        with uuid("46497707-c7d5-42e5-a4e0-f476e1f730fc") as case:
            main_page.insert_media("Skateboard 01.mp4")
            main_page.enter_room(3)
            effect_room_page.apply_effect_to_video('Aberration', 0, 0)
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Loop Playback')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.24.0_MediaEffect_Range_Select_RightClickMenu_LoopPlayback.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.24.0_MediaEffect_Range_Select_RightClickMenu_LoopPlayback.png',
                                                 preview_result)
            case.result = image_result

        # Media with effect Range selection right click menu lock range
        with uuid("05f9dabf-04ba-443b-b6a2-b7c03ee1b19f") as case:
            timeline_operation_page.right_click_range_select_menu('Lock Range')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.24.1_MediaEffect_Range_Select_RightClickMenu_LockRange.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.24.1_MediaEffect_Range_Select_RightClickMenu_LockRange.png',
                                                 preview_result)
            case.result = image_result

        # Media with effect Range selection right click menu produce range
        with uuid("12682d06-35c2-48f5-87d3-6fe04ee67ff6") as case:
            timeline_operation_page.right_click_range_select_menu('Export Range')
            time.sleep(DELAY_TIME * 5)
            preview_result = pan_zoom_page.snapshot(locator=L.produce.btn_start_produce,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.24.2_MediaEffect_Range_Select_RightClickMenu_ProduceRange.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.24.2_MediaEffect_Range_Select_RightClickMenu_ProduceRange.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_25(self):
        # Media with effect Range selection COPY
        with uuid("c3f3cbee-b64d-40bb-81cd-0bd9f3a6a73e") as case:
            main_page.insert_media("Skateboard 01.mp4")
            main_page.enter_room(3)
            effect_room_page.apply_effect_to_video('Aberration', 0, 0)
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_Copy()
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.25.0_MediaEffect_Range_Select_Copy.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.25.0_MediaEffect_Range_Select_Copy.png',
                                                 preview_result)
            case.result = image_result

        # Media with effect Range selection render preview
        with uuid("5fd5075f-3403-4a9c-aa03-1d1fda268ca2") as case:
            timeline_operation_page.edit_timeline_render_preview()
            time.sleep(DELAY_TIME)
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.25.1_MediaEffect_Range_Select_RenderPreview.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.25.1_MediaEffect_Range_Select_RenderPreview.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_26(self):
        # Media with effect Range selection Cut
        with uuid("e1ee37da-59de-4ac2-acbb-6f19525c9010") as case:
            main_page.insert_media("Skateboard 01.mp4")
            main_page.enter_room(3)
            effect_room_page.apply_effect_to_video('Aberration', 0, 0)
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_Cut()
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.26.0_MediaEffect_Range_Select_Cut.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.26.0_MediaEffect_Range_Select_Cut.png',
                                                 preview_result)
            case.result = image_result

        # Media with effect Range selection Paste
        with uuid("2cc54027-14c3-4536-b11c-0728e1cfecdd") as case:
            tips_area_page.click_TipsArea_btn_Paste()
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.26.1_MediaEffect_Range_Select_Paste.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.26.1_MediaEffect_Range_Select_Paste.png',
                                                 preview_result)
            case.result = image_result



    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_27(self):
        # Media with effect Range selection Remove
        with uuid("b5bd4259-0d0d-49c8-baed-95bd735e7e20") as case:
            main_page.insert_media("Skateboard 01.mp4")
            main_page.enter_room(3)
            time.sleep(DELAY_TIME*2)
            effect_room_page.apply_effect_to_video('Aberration', 0, 0)
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_Remove()
            time.sleep(DELAY_TIME*2)
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.27.0_MediaEffect_Range_Select_Remove.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.27.0_MediaEffect_Range_Select_Remove.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_28(self):
        # Media with effect Range selection lock range
        with uuid("3a2b72ca-e97f-4da4-88aa-78a21ad74459") as case:
            main_page.insert_media("Skateboard 01.mp4")
            main_page.enter_room(3)
            effect_room_page.apply_effect_to_video('Aberration', 0, 0)
            timeline_operation_page.set_range_markin_markout(30,180)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_Lock_Range()
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.28.0_MediaEffect_Range_Select_LockRange.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.28.0_MediaEffect_Range_Select_LockRange.png',
                                                 preview_result)
            case.result = image_result

        # Media with effect Range selection produce range
        with uuid("d8de1d3e-bf2b-4057-8429-97dc37662b69") as case:
            tips_area_page.click_TipsArea_btn_Produce_Range()
            time.sleep(DELAY_TIME)
            produce_page.click_edit()
            time.sleep(DELAY_TIME)
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.28.1_MediaEffect_Range_Select_ProduceRange.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.28.1_MediaEffect_Range_Select_ProduceRange.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_29(self):
        # PiP Range selection right click menu copy
        with uuid("c50a75af-440c-4ce3-90c2-f4c7fc3367cc") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 2)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME * 2)
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30,120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Copy')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.29.0_PiP_Range_Select_RightClickMenu_Copy.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.29.0_PiP_Range_Select_RightClickMenu_Copy.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_30(self):
        # PiP Range selection right click menu cut and leave gap
        with uuid("624cf414-0edd-4625-bd0f-d6095051fc98") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 2)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME * 2)
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30,120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Cut','Cut and Leave Gap')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.30.0_PiP_Range_Select_RightClickMenu_CutAndLeaveGap.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.30.0_PiP_Range_Select_RightClickMenu_CutAndLeaveGap.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_31(self):
        # PiP Range selection right click menu cut and fill gap
        with uuid("f2f21578-118f-4b8a-9417-3d62b5497e9b") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 2)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME * 2)
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30, 120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Cut','Cut and Fill Gap')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.31.0_PiP_Range_Select_RightClickMenu_CutAndFillGap.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.31.0_PiP_Range_Select_RightClickMenu_CutAndFillGap.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_32(self):
        # PiP Range selection right click menu cut fill gap and move all clips
        with uuid("1269d7fa-b322-44f4-b2ee-cb596e4ed373") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 2)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME * 2)
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30, 120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Cut','Cut, Fill Gap, and Move All Clips')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.32.0_PiP_Range_Select_RightClickMenu_CutFillGapAndMoveAllClips.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.32.0_PiP_Range_Select_RightClickMenu_CutFillGapAndMoveAllClips.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_33(self):
        # PiP Range selection hotkey copy
        with uuid("1d2f2a45-e049-4cc3-9f88-b5525ec90f10") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 2)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME * 2)
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30, 120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            main_page.tap_Copy_hotkey()
            time.sleep(DELAY_TIME * 2)
            case.result = True

        # PiP Range selection hotkey cut
        with uuid("b1d330c5-abdb-43b5-8db5-8f710e1edcd3") as case:
            with uuid("38f3d044-291e-49d2-8322-5f36b55005c0") as case:
                with uuid("3c58afc0-1b6d-4991-b34d-0705a856e0c2") as case:
                    main_page.tap_Cut_hotkey()
                    time.sleep(DELAY_TIME * 2)
                    preview_result = timeline_operation_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                                      file_name=Auto_Ground_Truth_Folder + 'G1.33.0_PiP_Range_Select_Cut_Hotkey.png')
                    image_result = timeline_operation_page.compare(
                        Ground_Truth_Folder + 'G1.33.0_PiP_Range_Select_Cut_Hotkey.png',
                        preview_result)
                    case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_34(self):
        # PiP Range selection right click menu remove and leave gap
        with uuid("c369b1d1-adce-4143-b846-bd04671d3c3c") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 2)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME * 2)
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30, 120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Remove','Remove and Leave Gap')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.34.0_PiP_Range_Select_RightClickMenu_RemoveAndLeaveGap.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.34.0_PiP_Range_Select_RightClickMenu_RemoveAndLeaveGap.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_35(self):
        # PiP Range selection right click menu remove and fill gap
        with uuid("77d187b9-b544-4708-a554-2c3c5cefb51e") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 2)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME * 2)
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30, 120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Remove','Remove and Fill Gap')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.35.0_PiP_Range_Select_RightClickMenu_RemoveAndFillGap.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.35.0_PiP_Range_Select_RightClickMenu_RemoveAndFillGap.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_36(self):
        # PiP Range selection right click menu remove fill gap and move all clips
        with uuid("f3fd3be8-70be-4aa0-b0bd-59c2a2670b99") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 2)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME * 2)
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30, 120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Remove','Remove, Fill Gap, and Move All Clips')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.36.0_PiP_Range_Select_RightClickMenu_RemoveFillGapAndMoveAllClips.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.36.0_PiP_Range_Select_RightClickMenu_RemoveFillGapAndMoveAllClips.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_37(self):
        # PiP Range selection hotkey remove
        with uuid("e9f09efe-f6c1-479e-b9b8-c078b28c1606") as case:
            with uuid("413903c1-8ab8-4326-8059-d7cae9a1fd21") as case:
                with uuid("4c5de068-f152-4381-ad8e-01f06a5e929b") as case:
                    main_page.enter_room(4)
                    time.sleep(DELAY_TIME * 2)
                    main_page.select_LibraryRoom_category('General')
                    time.sleep(DELAY_TIME * 2)
                    pip_room_page.hover_library_media('Dialog_03')
                    pip_room_page.select_RightClickMenu_AddToTimeline()
                    timeline_operation_page.set_range_markin_markout(30, 120)
                    timeline_operation_page.timeline_click_zoomin_btn()
                    time.sleep(DELAY_TIME)
                    timeline_operation_page.timeline_click_zoomin_btn()
                    time.sleep(DELAY_TIME)
                    timeline_operation_page.timeline_click_zoomin_btn()
                    time.sleep(DELAY_TIME)
                    main_page.tap_Remove_hotkey()
                    time.sleep(DELAY_TIME * 2)
                    preview_result = timeline_operation_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                                      file_name=Auto_Ground_Truth_Folder + 'G1.37.0_PiP_Range_Select_Remove_Hotkey.png')
                    image_result = timeline_operation_page.compare(
                        Ground_Truth_Folder + 'G1.37.0_PiP_Range_Select_Remove_Hotkey.png',
                        preview_result)
                    case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_38(self):
        # PiP Range selection right click menu loop playback
        with uuid("8a70c398-4364-4a12-ba4a-e86f2adc7780") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME*5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME * 2)
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30, 120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Loop Playback')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.38.0_PiP_Range_Select_RightClickMenu_LoopPlayback.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.38.0_PiP_Range_Select_RightClickMenu_LoopPlayback.png',
                                                 preview_result)
            case.result = image_result

        # PiP Range selection right click menu lock range
        with uuid("e96c5496-2346-48de-b1db-6ecff11d5bc9") as case:
            timeline_operation_page.right_click_range_select_menu('Lock Range')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.38.1_PiP_Range_Select_RightClickMenu_LockRange.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.38.1_PiP_Range_Select_RightClickMenu_LockRange.png',
                                                 preview_result)
            case.result = image_result

        # PiP Range selection right click menu produce range
        with uuid("28ae94a5-a1ec-4214-a011-dba17077f45b") as case:
            timeline_operation_page.right_click_range_select_menu('Export Range')
            time.sleep(DELAY_TIME * 5)
            preview_result = pan_zoom_page.snapshot(locator=L.produce.btn_start_produce,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.38.2_PiP_Range_Select_RightClickMenu_ProduceRange.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.38.2_PiP_Range_Select_RightClickMenu_ProduceRange.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_39(self):
        # PiP Range selection COPY
        with uuid("9b4a0b9f-f005-47cb-96ea-387627c2ddcc") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME*5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME * 2)
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30, 120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_Copy()
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.39.0_PiP_Range_Select_Copy.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.39.0_PiP_Range_Select_Copy.png',
                                                 preview_result)
            case.result = image_result

        # PiP Range selection render preview
        with uuid("f873fc48-4824-4a4b-a78a-e5162ec8a69f") as case:
            timeline_operation_page.edit_timeline_render_preview()
            time.sleep(DELAY_TIME)
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.39.1_PiP_Range_Select_RenderPreview.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.39.1_PiP_Range_Select_RenderPreview.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_40(self):
        # PiP Range selection Cut
        with uuid("32c163b6-db09-4f9d-803c-b209ce51a390") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME*5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME * 2)
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30, 120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_Cut()
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.40.0_PiP_Range_Select_Cut.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.40.0_PiP_Range_Select_Cut.png',
                                                 preview_result)
            case.result = image_result

        # PiP Range selection Paste
        with uuid("9621eda6-5068-44f3-befc-616a1ee01b87") as case:
            tips_area_page.click_TipsArea_btn_Paste()
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.40.1_PiP_Range_Select_Paste.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.40.1_PiP_Range_Select_Paste.png',
                                                 preview_result)
            case.result = image_result



    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_41(self):
        # PiP Range selection Remove
        with uuid("2774d537-84e6-424e-9f02-be8b06c570d1") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME*5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME * 2)
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30, 120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_Remove()
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.41.0_PiP_Range_Select_Remove.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.41.0_PiP_Range_Select_Remove.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_42(self):
        # PiP Range selection lock range
        with uuid("38fb1760-52d9-491b-b350-6a2e4639d518") as case:
            main_page.enter_room(4)
            main_page.select_LibraryRoom_category('General')
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30, 120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_Lock_Range()
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.42.0_PiP_Range_Select_LockRange.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.42.0_PiP_Range_Select_LockRange.png',
                                                 preview_result)
            case.result = image_result

        # PiP Range selection produce range
        with uuid("faf02dfd-81b0-4909-907b-4ee3f76682cb") as case:
            tips_area_page.click_TipsArea_btn_Produce_Range()
            time.sleep(DELAY_TIME)
            produce_page.click_edit()
            time.sleep(DELAY_TIME)
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.42.1_PiP_Range_Select_ProduceRange.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.42.1_PiP_Range_Select_ProduceRange.png',
                                                 preview_result)
            case.result = image_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_43(self):
        # Particle Range selection right click menu copy
        with uuid("07b2fc90-27e2-497e-b212-106e5f17505b") as case:
            time.sleep(DELAY_TIME * 5)
            main_page.enter_room(5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            particle_room_page.hover_library_media('Maple')
            particle_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30,120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Copy')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.43.0_Particle_Range_Select_RightClickMenu_Copy.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.43.0_Particle_Range_Select_RightClickMenu_Copy.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_44(self):
        # Particle Range selection right click menu cut and leave gap
        with uuid("5d64292f-f57c-4f4a-baed-d16854a734fe") as case:
            time.sleep(DELAY_TIME * 5)
            main_page.enter_room(5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            particle_room_page.hover_library_media('Maple')
            particle_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30, 120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Cut','Cut and Leave Gap')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.44.0_Particle_Range_Select_RightClickMenu_CutAndLeaveGap.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.44.0_Particle_Range_Select_RightClickMenu_CutAndLeaveGap.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_45(self):
        # Particle Range selection right click menu cut and fill gap
        with uuid("d036dc6e-227c-447c-aa63-20a7b47c9a9b") as case:
            time.sleep(DELAY_TIME * 5)
            main_page.enter_room(5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            particle_room_page.hover_library_media('Maple')
            particle_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30, 120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Cut','Cut and Fill Gap')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.45.0_Particle_Range_Select_RightClickMenu_CutAndFillGap.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.45.0_Particle_Range_Select_RightClickMenu_CutAndFillGap.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_46(self):
        # Particle Range selection right click menu cut fill gap and move all clips
        with uuid("70e6ff90-461d-40c4-b9ee-a135a735d2d3") as case:
            time.sleep(DELAY_TIME * 5)
            main_page.enter_room(5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            particle_room_page.hover_library_media('Maple')
            particle_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30, 120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.right_click_range_select_menu('Cut','Cut, Fill Gap, and Move All Clips')
            preview_result = pan_zoom_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.46.0_Particle_Range_Select_RightClickMenu_CutFillGapAndMoveAllClips.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.46.0_Particle_Range_Select_RightClickMenu_CutFillGapAndMoveAllClips.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_47(self):
        # Particle Range selection hotkey copy
        with uuid("acf83751-c241-44db-b1c8-60d862eb5eee") as case:
            time.sleep(DELAY_TIME * 5)
            main_page.enter_room(5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            particle_room_page.hover_library_media('Maple')
            particle_room_page.select_RightClickMenu_AddToTimeline()
            timeline_operation_page.set_range_markin_markout(30, 120)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            timeline_operation_page.timeline_click_zoomin_btn()
            time.sleep(DELAY_TIME)
            main_page.tap_Copy_hotkey()
            time.sleep(DELAY_TIME * 2)
            case.result = True

        # Particle Range selection hotkey cut
        with uuid("c23f540d-2b4c-469c-a747-1a404524198d") as case:
            with uuid("f015f60c-b24c-4a4e-9b49-b97a345a23ed") as case:
                with uuid("36db5c1c-7783-4069-9a91-4fdebe374c87") as case:
                    main_page.tap_Cut_hotkey()
                    time.sleep(DELAY_TIME * 2)
                    preview_result = timeline_operation_page.snapshot(locator=timeline_operation_page.area.timeline,
                                                                      file_name=Auto_Ground_Truth_Folder + 'G1.47.0_Particle_Range_Select_Cut_Hotkey.png')
                    image_result = timeline_operation_page.compare(
                        Ground_Truth_Folder + 'G1.47.0_Particle_Range_Select_Cut_Hotkey.png',
                        preview_result)
                    case.result = image_result








































































