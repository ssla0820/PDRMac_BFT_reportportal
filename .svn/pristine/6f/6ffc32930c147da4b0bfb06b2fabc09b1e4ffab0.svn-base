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
transition_room_page = PageFactory().get_page_object('transition_room_page',mac)
playback_window_page = PageFactory().get_page_object('playback_window_page',mac)
preferences_page = PageFactory().get_page_object('preferences_page',mac)
tips_area_page = PageFactory().get_page_object('tips_area_page',mac)
video_collage_designer_page = PageFactory().get_page_object('video_collage_designer_page',mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Tips Area.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<


# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Tips_Area/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Tips_Area/'
Test_Material_Folder = app.testing_material

#Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto_MacAT_Trunk/SFT/GroundTruth/Tips_Area/'
#Auto_Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto_MacAT_Trunk/SFT/ATGroundTruth/Tips_Area/'
#Test_Material_Folder = '/Users/clt/Desktop/Ernesto_MacAT_Trunk/Material/'

DELAY_TIME = 1

class Test_Tips_Area():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        yield mac
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
            google_sheet_execution_log_init('Tips_Area')

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
    def test1_1_6_129(self):
        # color board video collage gray
        with uuid("d21aa077-4c1d-440c-bfc3-d8b0e85c4464") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.more_features.get_edit_in_video_collage_status()
            case.result = not current_result

        # color board restore opacity gray
        with uuid("c0cbe786-f986-4aba-92b8-40ef3f6c334e") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_video_restore_opacity_status()
            case.result = not current_result

        # color board edit image gray
        with uuid("c0cbe786-f986-4aba-92b8-40ef3f6c334e") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_edit_image_status()
            case.result = not current_result

        # color board set clip attributes duration
        with uuid("c0cbe786-f986-4aba-92b8-40ef3f6c334e") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.click_clip_attributes_duration()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_130(self):
        # color board change alias
        with uuid("8126ca9b-3ac0-4753-a296-75dcf1650fe5") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            tips_area_page.more_features.click_change_alias()
            tips_area_page.more_features.set_alias('abcde')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.130.0_ColorBoardChangeAlias.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.130.0_ColorBoardChangeAlias.png',
                                                    image_result)
            case.result = compare_result

        # color board reset alias
        with uuid("d957d891-528f-4cca-b62a-f1ca3b53b8f4") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.click_reset_alias()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.130.1_ColorBoardResetAlias.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.130.1_ColorBoardResetAlias.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_131(self):
        # color board reset all undock disable
        with uuid("f48aa9dd-4eaa-423c-9429-1a99fceff0b0") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.more_features.get_reset_all_undock_windows_status()
            case.result = not current_result

        # color board undock timeline
        with uuid("edf4b36a-e4cd-4fbb-b65b-b77e8b0094b7") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.131.1_ColorBoardUndockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.131.1_ColorBoardUndockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # color board dock timeline
        with uuid("71cb5e6f-36d0-4ba6-8c31-790f9929c0e1") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(False)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.131.2_ColorBoardDockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.131.2_ColorBoardDockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # color board reset all undock
        with uuid("4cec9628-8f71-4a04-b003-b7d0307f7509") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            tips_area_page.more_features.reset_all_undock_windows()
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.131.3_ColorBoardResetAllUndock.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.131.3_ColorBoardResetAllUndock.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_132(self):
        # video collage split gray
        with uuid("8c97e9c3-d5f6-4081-9eec-d2caf0b4fe24") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_plugins_video_collage_designer()
            time.sleep(DELAY_TIME * 4)
            video_collage_designer_page.click_ok()
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.get_btn_split_status()
            case.result = not current_result

        # video collage split
        with uuid("970875d3-df32-4933-b7aa-273914c3e824") as case:
            playback_window_page.set_timecode_slidebar('00_00_01_00')
            tips_area_page.click_TipsArea_btn_split()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.132.1_VideoCollageSplit.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.132.1_VideoCollageSplit.png',
                                                    image_result)
            case.result = compare_result

        # video collage select all
        with uuid("a3ba6068-d12c-4b7d-ae63-4f87c4353e51") as case:
            tips_area_page.more_features.select_all()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.132.2_VideoCollageSelectAll.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.132.2_VideoCollageSelectAll.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_133(self):
        # video collage video collage designer
        with uuid("26011069-0cf3-4cc1-844e-b895823485f5") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_plugins_video_collage_designer()
            time.sleep(DELAY_TIME * 4)
            video_collage_designer_page.click_ok()
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.click_TipsArea_btn_VideoCollage()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_134(self):
        # video collage cut
        with uuid("4609beb6-1142-4255-8e72-ae0686a963bc") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_plugins_video_collage_designer()
            time.sleep(DELAY_TIME * 4)
            video_collage_designer_page.click_ok()
            time.sleep(DELAY_TIME)
            tips_area_page.more_features.cut()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.134.0_VideoCollageCut.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.134.0_VideoCollageCut.png',
                                                    image_result)
            case.result = compare_result

        # video collage paste
        with uuid("3d2ad2de-bef6-4ea0-ab9a-f3ee9dc44ee9") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_plugins_video_collage_designer()
            time.sleep(DELAY_TIME * 4)
            video_collage_designer_page.click_ok()
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.134.1_VideoCollagePaste.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.134.1_VideoCollagePaste.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_135(self):
        # video collage copy
        with uuid("0c77504d-5214-438d-9e98-15faeefd9cc7") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_plugins_video_collage_designer()
            time.sleep(DELAY_TIME * 4)
            video_collage_designer_page.click_ok()
            time.sleep(DELAY_TIME)
            tips_area_page.more_features.copy()
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.135.0_VideoCollageCopy.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.135.0_VideoCollageCopy.png',
                                                    image_result)
            case.result = compare_result

        # video collage remove
        with uuid("47c53d37-5f89-4025-ad43-14256fc4706b") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.remove(1)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.135.1_VideoCollageRemove.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.135.1_VideoCollageRemove.png',
                                                    image_result)
            case.result = compare_result

    @exception_screenshot
    def test1_1_6_136(self):
        # video collage more feature split gray
        with uuid("c379be8f-ae0f-4c6a-b4f1-584a8c86f5a7") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_plugins_video_collage_designer()
            time.sleep(DELAY_TIME * 4)
            video_collage_designer_page.click_ok()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.more_features.get_split_status()
            case.result = not current_result

        # video collage more feature link unlink gray
        with uuid("e054e1fa-0357-4e72-9753-737ee2b75ce6") as case:
            current_result = tips_area_page.more_features.get_link_unlink_status()
            case.result = not current_result

        # video collage group ungroup gray
        with uuid("30c51221-c648-41df-b2c6-2495179915dd") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_group_ungroup_status()
            case.result = not current_result

        # video collage more feature split
        with uuid("01bca5c3-b9ee-4549-addb-8559bc3ccf49") as case:
            playback_window_page.set_timecode_slidebar('00_00_01_00')
            tips_area_page.click_TipsArea_btn_split()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.136.1_VideoCollageSplit.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.136.1_VideoCollageSplit.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_137(self):
        # video collage more feature trim gray
        with uuid("f58f0d52-1e25-43f5-b520-0ce20b108698") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_plugins_video_collage_designer()
            time.sleep(DELAY_TIME * 4)
            video_collage_designer_page.click_ok()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.more_features.get_edit_video_trim_status()
            case.result = not current_result

        # video collage more feature fix enhance gray
        with uuid("b6985147-5277-4c3f-91aa-22ef79cab407") as case:
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.more_features.get_edit_video_fixenhance_status()
            case.result = not current_result

        # video collage more feature Enable Fade in and Fade out and Restore to Original opacity Level and vedio collage designer gray
        with uuid("e152857d-5cbb-4288-af67-0c25f9166058") as case:
            with uuid("eecbe85c-7d43-4a3e-a45c-355d89879433") as case:
                with uuid("92dda2b2-80a4-411b-8378-1e31dfaeb04a") as case:
                    time.sleep(DELAY_TIME)
                    current_result = tips_area_page.more_features.get_edit_video_status()
                    case.result = not current_result

        # video collage edit image gray
        with uuid("1be30508-bec5-4ae2-b6d4-272a0f18323c") as case:
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.more_features.get_edit_image_status()
            case.result = not current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_138(self):
        # video collage change alias
        with uuid("e7cb4996-7183-4418-a2d4-22bf4f139b77") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_plugins_video_collage_designer()
            time.sleep(DELAY_TIME * 4)
            video_collage_designer_page.click_ok()
            time.sleep(DELAY_TIME)
            tips_area_page.more_features.click_change_alias()
            tips_area_page.more_features.set_alias('abcde')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.138.0_VideoCollageChangeAlias.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.138.0_VideoCollageChangeAlias.png',
                                                    image_result)
            case.result = compare_result

        # video collage reset alias
        with uuid("546231ae-9397-48b5-947b-dc172f1cf31c") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.click_reset_alias()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.138.1_VideoCollageResetAlias.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.138.1_VideoCollageResetAlias.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_139(self):
        # video collage reset all undock disable
        with uuid("86fbc6e2-26e4-4d94-8787-5c9b5a9e7bd5") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_plugins_video_collage_designer()
            time.sleep(DELAY_TIME * 4)
            video_collage_designer_page.click_ok()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.more_features.get_reset_all_undock_windows_status()
            case.result = not current_result

        # video collage undock timeline
        with uuid("68c835df-18b3-428d-837d-3eeb3656a2ab") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.139.1_VideoCollageUndockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.139.1_VideoCollageUndockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # video collage dock timeline
        with uuid("95f9bf50-95c8-47b0-af40-93538aad7365") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(False)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.139.2_VideoCollageDockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.139.2_VideoCollageDockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # video collage reset all undock
        with uuid("566d5537-7008-42db-addd-545370ccd17e") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            tips_area_page.more_features.reset_all_undock_windows()
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.139.3_VideoCollageResetAllUndock.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.139.3_VideoCollageResetAllUndock.png',
                                                    image_result)
            case.result = compare_result
























