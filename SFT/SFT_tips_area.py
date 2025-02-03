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
    def test1_1_6_1(self):
        # insert image to timeline
        with uuid("7a949456-9954-4adc-a3c3-42ea6b5c2d99") as case:
            main_page.select_library_icon_view_media('Food.jpg')
            tips_area_page.click_TipsArea_btn_insert()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G6.1.0_InsertImageToTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.1.0_InsertImageToTimeline.png',
                                                     image_result)
            case.result = compare_result

        # split disabled
        with uuid("b04d3d65-59cb-49cb-b860-fce6b914ded4") as case:
            with uuid("66578e91-c8f5-4903-af7a-43467485a794") as case:
                current_result = tips_area_page.get_btn_split_status()
                case.result = not current_result

        # split image
        with uuid("ecf9a70b-fd63-4765-91b7-342c1a0cc6cf") as case:
            with uuid("f0220d14-ece0-4b61-94f4-fcf04e60d8db") as case:
                playback_window_page.set_timecode_slidebar('00_00_02_00')
                tips_area_page.click_TipsArea_btn_split()
                image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                       file_name=Auto_Ground_Truth_Folder + 'G6.1.2_ImageSplit.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.1.2_ImageSplit.png',
                                                        image_result)
                case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_2(self):
        # insert video to timeline
        with uuid("2e1948cb-379e-4137-8553-c50b54242c10") as case:
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            tips_area_page.click_TipsArea_btn_insert()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G6.2.0_InsertVideoToTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.2.0_InsertVideoToTimeline.png',
                                                     image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_3(self):
        # insert audio to timeline
        with uuid("b22042a4-8115-48d1-84ff-6fb0737937c3") as case:
            main_page.select_library_icon_view_media('Speaking Out.mp3')
            tips_area_page.click_TipsArea_btn_insert()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G6.3.0_InsertAudioToTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.3.0_InsertAudioToTimeline.png',
                                                     image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_4(self):
        # insert effect to timeline effect track
        with uuid("5cb95ed3-49f3-46a9-8878-20db8c83e9c0") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(3)
            main_page.select_library_icon_view_media('Beating')
            tips_area_page.click_TipsArea_btn_add_to_effect_track()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G6.4.0_InsertEffectToTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.4.0_InsertEffectToTimeline.png',
                                                     image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_5(self):
        # insert pip object to timeline
        with uuid("73d0bbde-bf9a-4ced-91ab-ae2478c356ad") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            main_page.select_library_icon_view_media('Dialog_03')
            tips_area_page.click_TipsArea_btn_insert()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G6.5.0_InsertPiPToTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.5.0_InsertPiPToTimeline.png',
                                                     image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_6(self):
        # insert particle to timeline
        with uuid("6bfe7dcc-f90f-4873-8f9b-679ca564f15f") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(5)
            main_page.select_library_icon_view_media('Maple')
            tips_area_page.click_TipsArea_btn_insert()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G6.6.0_InsertParticleToTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.6.0_InsertParticleToTimeline.png',
                                                     image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_7(self):
        # insert title to timeline
        with uuid("07f418ae-c7d5-433a-8b44-85896f7abc23") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            main_page.select_library_icon_view_media('Clover_01')
            tips_area_page.click_TipsArea_btn_insert()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G6.7.0_InsertTitleToTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.7.0_InsertTitleToTimeline.png',
                                                     image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_8(self):
        # insert my favorite transition to timeline clips prefix
        with uuid("6d1e4497-db54-4501-8f65-a20149bf5220") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            tips_area_page.click_TipsArea_btn_insert()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            tips_area_page.click_TipsArea_btn_insert(1)
            main_page.enter_room(2)
            main_page.select_library_icon_view_media('Blur')
            time.sleep(DELAY_TIME * 4)
            transition_room_page.select_RightClickMenu_Addto('My Favorites')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_apply_favorite_transition(0)
            time.sleep(DELAY_TIME)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G6.8.0_InsertMyFavoritesTransitionToTimelineClipsPrefix.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.8.0_InsertMyFavoritesTransitionToTimelineClipsPrefix.png',
                                                     image_result)
            case.result = compare_result

        # insert my favorite transition to timeline clips postfix
        with uuid("8367cf4a-b0a7-4b65-9bdf-37cdf231b701") as case:
            main_page.select_library_icon_view_media('Blur')
            tips_area_page.click_TipsArea_btn_apply_favorite_transition(1)
            time.sleep(DELAY_TIME)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.8.1_InsertMyFavoritesTransitionToTimelineClipsPostfix.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.8.1_InsertMyFavoritesTransitionToTimelineClipsPostfix.png',
                                                    image_result)
            case.result = compare_result

        # insert my favorite transition to timeline clips cross
        with uuid("1c504c16-1bd1-4393-a23f-a13ad94004c0") as case:
            main_page.select_library_icon_view_media('Blur')
            tips_area_page.click_TipsArea_btn_apply_favorite_transition(2)
            time.sleep(DELAY_TIME)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.8.2_InsertMyFavoritesTransitionToTimelineClipsCross.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.8.2_InsertMyFavoritesTransitionToTimelineClipsCross.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_8a(self):
        # insert my favorite transition to timeline clips prefix
        with uuid("295afe77-f64f-4dc7-96b4-9c6a33fdb1c2") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            tips_area_page.click_TipsArea_btn_insert()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            tips_area_page.click_TipsArea_btn_insert(1)
            main_page.enter_room(2)
            main_page.select_library_icon_view_media('Blur')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.click_TipsArea_btn_apply_favorite_transition(3)
            time.sleep(DELAY_TIME)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.8.3_InsertMyFavoritesTransitionToTimelineClipsOverlap.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.8.3_InsertMyFavoritesTransitionToTimelineClipsOverlap.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_9(self):
        # insert fading transition to timeline clips prefix
        with uuid("4eb9f8bd-58ff-431a-94f7-199e763c0651") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            tips_area_page.click_TipsArea_btn_insert()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            tips_area_page.click_TipsArea_btn_insert(1)
            main_page.enter_room(2)
            main_page.select_library_icon_view_media('Blur')
            tips_area_page.click_TipsArea_btn_apply_fading_transition(0)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G6.9.0_InsertFadingTransitionToTimelineClipsPrefix.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.9.0_InsertFadingTransitionToTimelineClipsPrefix.png',
                                                     image_result)
            case.result = compare_result

        # insert fading transition to timeline clips postfix
        with uuid("b76b9805-d37e-45a2-bd1f-2d99d1d56d20") as case:
            main_page.select_library_icon_view_media('Blur')
            tips_area_page.click_TipsArea_btn_apply_fading_transition(1)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.9.1_InsertFadingTransitionToTimelineClipsPostfix.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.9.1_InsertFadingTransitionToTimelineClipsPostfix.png',
                                                    image_result)
            case.result = compare_result

        # insert fading transition to timeline clips cross
        with uuid("3d553ea0-4fe8-4ded-8d2d-6a3e58ff47e6") as case:
            main_page.select_library_icon_view_media('Blur')
            tips_area_page.click_TipsArea_btn_apply_fading_transition(2)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.9.2_InsertFadingTransitionToTimelineClipsCross.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.9.2_InsertFadingTransitionToTimelineClipsCross.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_9a(self):
        # insert fading transition to timeline clips overlap
        with uuid("3cacfdd9-ecfc-464a-813f-90af131dc8a3") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            tips_area_page.click_TipsArea_btn_insert()
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            tips_area_page.click_TipsArea_btn_insert(1)
            main_page.enter_room(2)
            main_page.select_library_icon_view_media('Blur')
            tips_area_page.click_TipsArea_btn_apply_fading_transition(3)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.9.3_InsertFadingTransitionToTimelineClipsOverlap.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.9.3_InsertFadingTransitionToTimelineClipsOverlap.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_10(self):
        # image crop
        with uuid("2a61e45a-76fd-4a58-8e73-15fa3e169ee5") as case:
            main_page.insert_media('Food.jpg')
            current_result = tips_area_page.click_TipsArea_btn_Crop_Image()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_11(self):
        # image duration
        with uuid("cf554d23-dd4e-45c7-a724-051a13e17e59") as case:
            main_page.insert_media('Food.jpg')
            current_result = tips_area_page.click_TipsArea_btn_Duration()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_12(self):
        # image PiP Designer
        with uuid("f0ffd876-fd01-46e1-b6f7-9c9b0bc543f7") as case:
            main_page.insert_media('Food.jpg')
            current_result = tips_area_page.tools.select_PiP_Designer()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_13(self):
        # image mask Designer
        with uuid("b547315c-45fa-4667-88dd-a492df8f323e") as case:
            main_page.insert_media('Food.jpg')
            current_result = tips_area_page.tools.select_Mask_Designer()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_14(self):
        # image blending mode
        with uuid("32f1abc6-9d8a-413d-b0a9-71027e75d82a") as case:
            main_page.insert_media('Food.jpg')
            current_result = tips_area_page.tools.select_Blending_Mode()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_15(self):
        # image pan and zoom
        with uuid("ef88d86f-ec2f-421e-85ee-72d20ab784af") as case:
            main_page.insert_media('Food.jpg')
            current_result = tips_area_page.tools.select_Pan_Zoom()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_16(self):
        # image fix enhance
        with uuid("d534130b-a6c8-49ec-aa39-662b0170a9e3") as case:
            main_page.insert_media('Food.jpg')
            current_result = tips_area_page.click_fix_enhance()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_17(self):
        # image keyframe room
        with uuid("32561c9b-0ba8-43ea-94ab-8ef6e2f2df0d") as case:
            main_page.insert_media('Food.jpg')
            current_result = tips_area_page.click_keyframe()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_18(self):
        # image cut
        with uuid("1ecfe23e-835d-4bd2-b76b-33f7bd8610e3") as case:
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.cut()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.18.0_ImageCut.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.18.0_ImageCut.png',
                                                    image_result)
            case.result = compare_result

        # image paste
        with uuid("e4f03710-3810-4f8d-84fe-48f2a9c3b68a") as case:
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.18.1_ImagePaste.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.18.1_ImagePaste.png',
                                                    image_result)
            case.result = compare_result

        # image select all
        with uuid("da51ea30-5c72-4d98-906e-b7aebff67aa1") as case:
            tips_area_page.more_features.select_all()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.18.2_ImageSelectAll.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.18.2_ImageSelectAll.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_19(self):
        # image copy
        with uuid("e1bfb995-b7a3-4f76-830d-ffe07ff7d93c") as case:
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.copy()
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.19.0_ImageCopy.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.19.0_ImageCopy.png',
                                                    image_result)
            case.result = compare_result

        # image remove
        with uuid("fc0e268b-8f4b-4ed6-9435-5534517a89e8") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.remove(1)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.19.1_ImageRemove.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.19.1_ImageRemove.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_20(self):
        # image copy attributes
        with uuid("0ea98c68-8c37-4072-b9fe-305a5a015a56") as case:
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.copy_keyframe_attributes()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.20.0_ImageCopyAttributes.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.20.0_ImageCopyAttributes.png',
                                                    image_result)
            case.result = compare_result

        # image paste attributes
        with uuid("55138e2a-5ea5-48b6-a376-4d794a0b9d37") as case:
            tips_area_page.more_features.paste_keyframe_attributes()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.20.1_ImagePasteAttributes.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.20.1_ImagePasteAttributes.png',
                                                    image_result)
            case.result = compare_result

        # image link unlink gray
        with uuid("68660acc-5813-477f-93e2-c9a555c28e54") as case:
            current_result = tips_area_page.more_features.get_link_unlink_status()
            case.result = not current_result

        # image group ungroup gray
        with uuid("f74912e4-3305-4c94-a76a-363eca22b784") as case:
            current_result = tips_area_page.more_features.get_group_ungroup_status()
            case.result = not current_result

        # image edit video gray
        with uuid("6b1cb80e-ea6a-4ad9-afc9-87de79fe424d") as case:
            current_result = tips_area_page.more_features.get_edit_video_status()
            case.result = not current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_21(self):
        # image edit image crop image
        with uuid("7e71d6e1-845c-44af-8b06-fd998e72587d") as case:
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.edit_image_CropImage()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_22(self):
        # image edit image pan and zoom
        with uuid("ad7c79b2-add5-4d4e-8024-429cd4a6e3d5") as case:
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.edit_image_PanZoom()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_23(self):
        # image edit image fix enhance
        with uuid("1cb1518a-3567-4520-afab-eafeb0d4ef61") as case:
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.edit_image_FixEnhance()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_24(self):
        # image edit image restore disabled
        with uuid("c1f7d78b-e72c-4475-b907-96f240420964") as case:
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_image_restore_opacity_status()
            case.result = not current_result

        # image edit image enable fade in and fade out
        with uuid("cd7eaf16-e24b-470a-a40c-0aac588f7e77") as case:
            tips_area_page.more_features.edit_image_enable_fade_feature()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.24.1_ImageEditImageEnableFadeInOut.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.24.1_ImageEditImageEnableFadeInOut.png',
                                                    image_result)
            case.result = compare_result

        # image edit image restore
        with uuid("79b954a7-d756-43f3-88cf-1648af0435a2") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.edit_image_restore_opacity()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.24.2_ImageEditImageRestore.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.24.2_ImageEditImageRestore.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_25(self):
        # image Set Clip Attributes Set Duration
        with uuid("3b86099c-7a8b-4c24-8742-41158a382466") as case:
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.click_clip_attributes_duration()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_26(self):
        # image Set Clip Attributes stretch mode
        with uuid("58c4299a-f4f8-4dbd-a76d-05caa4c24d33") as case:
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.click_clip_attributes_stretch_mode()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_27(self):
        # image Set Clip Attributes blending mode
        with uuid("d69f5289-1b67-41a3-8ff2-76087f440633") as case:
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.set_attributes_blending_mode(4)
            image_result = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.27.0_ImageSetClipAttributesBlendingMode.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.27.0_ImageSetClipAttributesBlendingMode.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_28(self):
        # image change alias
        with uuid("be7ab9c1-9651-435b-b6f6-86187af8d647") as case:
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.click_change_alias()
            tips_area_page.more_features.set_alias('1234')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.28.0_ImageChangeAlias.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.28.0_ImageChangeAlias.png',
                                                    image_result)
            case.result = compare_result

        # image reset alias
        with uuid("f38db060-cd1b-4dea-ba78-6f685215f593") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.click_reset_alias()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.28.1_ImageResetAlias.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.28.1_ImageResetAlias.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_29(self):
        # image view properties
        with uuid("0a1032b6-2ee9-4bd3-b3be-8c83602b0564") as case:
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.view_properties()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_30(self):
        # image reset allundock disable
        with uuid("328bb6d6-5758-4285-82cb-49f180a801ae") as case:
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_reset_all_undock_windows_status()
            case.result = not current_result

        # image undock timeline
        with uuid("59760aa7-b7d9-442f-ba9f-fd6e98dace52") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.30.1_ImageUndockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.30.1_ImageUndockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # image dock timeline
        with uuid("8a98d5d9-26f8-49d9-b6dd-5c35bbb017b0") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(False)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.30.2_ImagedockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.30.2_ImagedockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # image reset all undock
        with uuid("10f5e74f-0077-4ee3-bd77-ea5f42e9c7fa") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            tips_area_page.more_features.reset_all_undock_windows()
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.30.3_ImageResetAllUndock.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.30.3_ImageResetAllUndock.png',
                                                    image_result)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_31(self):
        # video split disabled
        with uuid("ff47c2db-e44d-43a2-b703-744483ecb94e") as case:
            with uuid("7fedb123-2181-4d31-8686-28c33e43483a") as case:
                main_page.insert_media('Skateboard 01.mp4')
                time.sleep(DELAY_TIME * 4)
                current_result = tips_area_page.get_btn_split_status()
                case.result = not current_result

        # split video
        with uuid("16445b97-34b5-409e-8148-b6dc766dda59") as case:
            with uuid("89c89600-9907-4a15-9ab5-f695c83a5780") as case:
                playback_window_page.set_timecode_slidebar('00_00_03_00')
                tips_area_page.click_TipsArea_btn_split()
                time.sleep(DELAY_TIME * 4)
                image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                       file_name=Auto_Ground_Truth_Folder + 'G6.31.1_VideoSplit.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.31.1_VideoSplit.png',
                                                        image_result)
                case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_32(self):
        # video trim
        with uuid("6d00354d-00af-4b67-bb40-dc7f845d9e31") as case:
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.click_TipsArea_btn_Trim('Video')
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_33(self):
        # video PiP Designer
        with uuid("204e790e-d954-4a99-b715-253122ed1310") as case:
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.tools.select_PiP_Designer()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_34(self):
        # video Mask Designer
        with uuid("8e32a4fd-9b11-44f2-84e6-684532286851") as case:
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.tools.select_Mask_Designer()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_35(self):
        # video crop zoom pan
        with uuid("6093ca49-7b35-4451-91a9-d5ef649d8e53") as case:
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.tools.select_CropZoomPan()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_36(self):
        # video video speed
        with uuid("36eebc33-6341-4ddb-934f-c72ab572d941") as case:
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.tools.select_VideoSpeed()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_37(self):
        # video video in reverse
        with uuid("b24e835c-9dc1-11eb-a8b3-0242ac130003") as case:
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.tools.select_Video_in_Reverse()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_38(self):
        # video blending mode
        with uuid("e0bbdeb9-ab70-4977-ad1d-a7a484b62597") as case:
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.tools.select_Blending_Mode()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_39(self):
        # video audio editor
        with uuid("961a2249-4b5f-422c-98e0-83a27e829f0d") as case:
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.tools.select_Audio_Editor()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_40(self):
        # video fix enhance
        with uuid("b312ebb1-e3b6-4418-872b-b8acd3573320") as case:
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.click_fix_enhance()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_41(self):
        # video keyframe room
        with uuid("15182edb-14c6-47d8-9b2b-c5bf0e763774") as case:
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.click_keyframe()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_42(self):
        # video cut
        with uuid("ac6b696f-5dad-4754-9c44-805fae0b0f67") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.cut()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.42.0_VideoCut.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.42.0_VideoCut.png',
                                                    image_result)
            case.result = compare_result

        # video paste
        with uuid("6760e7c2-1465-4209-a084-cc0440552d44") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.42.1_VideoPaste.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.42.1_VideoPaste.png',
                                                    image_result)
            case.result = compare_result

        # video select all
        with uuid("255994fe-edf8-4995-8575-e8a8a9d166ab") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.select_all()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.42.2_VideoSelectAll.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.42.2_VideoSelectAll.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_43(self):
        # video copy
        with uuid("f09e6430-c0da-497f-af8d-b3b8488faece") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.copy()
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.43.0_VideoCopy.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.43.0_VideoCopy.png',
                                                    image_result)
            case.result = compare_result

        # video remove
        with uuid("3855f628-2bc6-47df-9144-5fc52ee184da") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.remove(1)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.43.1_VideoRemove.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.43.1_VideoRemove.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_44(self):
        # video copy attributes
        with uuid("16df0ebc-fb45-466b-808b-d763e7f9eb7c") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.copy_keyframe_attributes()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.44.0_VideoCopyAttributes.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.44.0_VideoCopyAttributes.png',
                                                    image_result)
            case.result = compare_result

        # video paste attributes
        with uuid("456b7f09-619c-491e-a380-f39bc8b38aec") as case:
            tips_area_page.more_features.paste_keyframe_attributes()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.44.1_VideoPasteAttributes.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.44.1_VideoPasteAttributes.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_45(self):
        # video link unlink
        with uuid("6eff36dd-cb7a-4c3e-85d1-2d4d040d6f42") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.link_unlink_video_audio()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.45.0_VideoLinkUnlink.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.45.0_VideoLinkUnlink.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_46(self):
        # video group ungroup gray
        with uuid("729a0d8a-e731-44ce-833a-fb251f1485e3") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_group_ungroup_status()
            case.result = not current_result

        # video mute clip unselect
        with uuid("5404fea3-9cd8-47b4-8a49-ad997b78a918") as case:
            with uuid("005369bc-0ddb-4632-ab96-86007a44a1ee") as case:
                current_result = not tips_area_page.more_features.get_mute_clip_tick_status()
                image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                       file_name=Auto_Ground_Truth_Folder + 'G6.46.1_VideoMuteClipUnselect.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.46.1_VideoMuteClipUnselect.png',
                                                        image_result)
                case.result = compare_result and current_result

        # video mute clip select
        with uuid("607895ce-d169-4189-bbf1-8542fcca7528") as case:
            with uuid("005369bc-0ddb-4632-ab96-86007a44a1ee") as case:
                tips_area_page.more_features.mute_clip()
                current_result = tips_area_page.more_features.get_mute_clip_tick_status()
                image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                       file_name=Auto_Ground_Truth_Folder + 'G6.46.2_VideoMuteClipSelect.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.46.2_VideoMuteClipSelect.png',
                                                        image_result)
                case.result = compare_result and current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_47(self):
        # video restore volume gray
        with uuid("ad5a6e6c-5a06-4ae4-98c2-d5313363e54e") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_restore_original_volume_status()
            case.result = not current_result

        # video remove all clip marker gray
        with uuid("c5db9e2f-18ce-45e4-8f93-73a962edfc02") as case:
            current_result = tips_area_page.more_features.get_remove_all_clip_markers_status()
            case.result = not current_result

        # video normalize audio gray
        with uuid("58f7a855-371e-4fe2-b0a3-aaf6f0a246c8") as case:
            current_result = tips_area_page.more_features.get_normalize_audio_status()
            case.result = not current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_48(self):
        # video Trim
        with uuid("2fb90546-b8cb-4f2e-b7a5-f04507be5e04") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.edit_video_trim()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_49(self):
        # video fix enhance
        with uuid("3b8acce5-4e20-4760-b077-5da3b9ce9fd3") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.edit_video_FixEnhance()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_50(self):
        # video restore opacity level gray
        with uuid("4cd3fc9d-6b36-4b96-84bb-154e8b1d94fe") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_video_restore_opacity_status()
            case.result = not current_result

        # video fade in fade out
        with uuid("4cd3fc9d-6b36-4b96-84bb-154e8b1d94fe") as case:
            tips_area_page.more_features.edit_video_enable_fade_feature()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.50.1_VideoFadeInFadeOut.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.50.1_VideoFadeInFadeOut.png',
                                                    image_result)
            case.result = compare_result

        # video restore opacity level
        with uuid("fabd827d-b2b4-485d-9cb0-8e4cc3ca1a0c") as case:
            time.sleep(DELAY_TIME)
            tips_area_page.more_features.edit_video_restore_opacity()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.50.2_VideoRestoreOpacityLevel.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.50.2_VideoRestoreOpacityLevel.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_51(self):
        # video video collage gray
        with uuid("5047e524-4caa-43d7-bc18-79a64691852e") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_restore_original_volume_status()
            case.result = not current_result

        # video edit image gray
        with uuid("89e1bbd8-e924-45ac-99d2-d3169029ecc9") as case:
            current_result = tips_area_page.more_features.get_edit_image_status()
            case.result = not current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_52(self):
        # video set clip attributes set aspect ratio
        with uuid("2ed38080-379e-45d9-b332-bebf35ba5a7f") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.set_attributes_aspect_ratio()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_53(self):
        # video set clip attributes blending mode
        with uuid("9fdb7f10-b210-471c-b14e-fb5c24493243") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.set_attributes_blending_mode(3)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.53.0_VideoBlendingMode.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.53.0_VideoBlendingMode.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_54(self):
        # video change alias
        with uuid("8ca108f3-f0af-4925-8c6f-247bb4280cc3") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.click_change_alias()
            time.sleep(DELAY_TIME)
            tips_area_page.more_features.set_alias('abcd')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.54.0_VideoChangeAlias.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.54.0_VideoChangeAlias.png',
                                                    image_result)
            case.result = compare_result

        # video reset alias
        with uuid("c14d1df4-cc6b-43c5-bb84-02e33e96e578") as case:
            time.sleep(DELAY_TIME)
            tips_area_page.more_features.click_reset_alias()
            time.sleep(DELAY_TIME)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.54.1_VideoResetAlias.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.54.1_VideoResetAlias.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_55(self):
        # video view properties
        with uuid("61d5dc08-374a-44f4-a4af-891f631c8485") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.view_properties()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_56(self):
        # video reset all undock disable
        with uuid("c6578bf0-0328-48f3-b0d4-30e5d192e81b") as case:
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_reset_all_undock_windows_status()
            case.result = not current_result

        # video undock timeline
        with uuid("57d5c961-5626-4e48-9225-f1bbfb474e8c") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.56.1_VideoUndockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.56.1_VideoUndockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # video dock timeline
        with uuid("886c029d-61c0-4a1f-851c-754f7b91a698") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(False)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.56.2_VideoDockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.56.2_VideoDockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # video reset all undock
        with uuid("131f24fd-1912-4d3a-9767-3f2e74d3b7db") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            tips_area_page.more_features.reset_all_undock_windows()
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.56.3_VideoResetAllUndock.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.56.3_VideoResetAllUndock.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_57(self):
        # audio split disabled
        with uuid("f9678a24-b972-4bd6-9cf9-37c24a0cbcf4") as case:
            with uuid("04fcad1d-8a63-434a-a32c-2a1ed2f1b321") as case:
                time.sleep(DELAY_TIME * 4)
                main_page.insert_media('Mahoroba.mp3')
                time.sleep(DELAY_TIME * 4)
                current_result = tips_area_page.get_btn_split_status()
                case.result = not current_result

        # split audio
        with uuid("a7415a72-30e6-4f76-866d-b712737b1661") as case:
            with uuid("a0ea6001-bbed-4605-a463-32725f9afaa6") as case:
                playback_window_page.set_timecode_slidebar('00_01_03_00')
                tips_area_page.click_TipsArea_btn_split()
                image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                       file_name=Auto_Ground_Truth_Folder + 'G6.57.1_AudioSplit.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.57.1_AudioSplit.png',
                                                        image_result)
                case.result = compare_result

        # audio select all
        with uuid("19a4e062-c44b-413a-8ded-4eaa634160f2") as case:
            tips_area_page.more_features.select_all()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.57.2_AudioSelectAll.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.57.2_AudioSelectAll.png',
                                                    image_result)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_58(self):
        # audio trim
        with uuid("d2fdfd3c-2771-40ee-a850-ce2bb8a7b610") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.click_TipsArea_btn_Trim('Audio')
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_59(self):
        # audio tools audio speed
        with uuid("2b5a25a8-9dd1-11eb-a8b3-0242ac130003") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.tools.select_Audio_Speed()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_60(self):
        # audio tools audio reverse
        with uuid("de035c06-5866-4955-a5ea-247289b176c1") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.tools.select_Audio_in_Reverse()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_61(self):
        # audio tools audio editor
        with uuid("925a7bb8-5e60-4745-9166-74016cbce8ef") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.tools.select_Audio_Editor()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_62(self):
        # audio fix enhance
        with uuid("461eed2f-3e09-47bb-86a3-f00a0445a4e8") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.click_fix_enhance()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_63(self):
        # audio keyframe room
        with uuid("859712bb-48d1-4c62-8376-5bdf3dcd8ef5") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.click_keyframe()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_64(self):
        # audio cut
        with uuid("efd57c10-e8dd-4f48-b3ea-e2f7553bbd81") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.cut()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.64.0_AudioCut.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.64.0_AudioCut.png',
                                                    image_result)
            case.result = compare_result

        # audio paste
        with uuid("0d4ef3d8-3503-49ff-9470-9642239ab3fe") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.64.1_AudioPaste.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.64.1_AudioPaste.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_65(self):
        # audio copy
        with uuid("3b571076-935e-4b2b-a984-ca1c1641ad68") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.copy()
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.65.0_AudioCopy.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.65.0_AudioCopy.png',
                                                    image_result)
            case.result = compare_result

        # audio remove
        with uuid("1d09133b-cb4d-4b2e-82bd-97514c993caf") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.remove(1)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.65.1_AudioRemove.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.65.1_AudioRemove.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_66(self):
        # audio copy attributes
        with uuid("16957e6e-1504-43fb-9fd5-cb3374ba9464") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.copy_keyframe_attributes()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.66.0_AudioCopyAttributes.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.66.0_AudioCopyAttributes.png',
                                                    image_result)
            case.result = compare_result

        # audio paste attributes
        with uuid("1858d456-5726-49f7-b225-ef4d973b518e") as case:
            tips_area_page.more_features.paste_keyframe_attributes()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.66.1_AudioPasteAttributes.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.66.1_AudioPasteAttributes.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_67(self):
        # audio link unlink gray
        with uuid("98a8ab81-2489-44b0-9738-e0476d3dc366") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_link_unlink_status()
            case.result = not current_result

        # audio group ungroup gray
        with uuid("b76e527d-cdc1-417f-80b3-16262d610d05") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_group_ungroup_status()
            case.result = not current_result

        # audio unselect mute clip
        with uuid("47ed95e9-5478-4b9a-ae77-da46a1e6b459") as case:
            with uuid("d888be38-9425-4466-b304-fc72f71b6436") as case:
                current_result = not tips_area_page.more_features.get_mute_clip_tick_status()
                image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                       file_name=Auto_Ground_Truth_Folder + 'G6.67.2_AudioMuteClipUnselect.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.67.2_AudioMuteClipUnselect.png',
                                                        image_result)
                case.result = compare_result and current_result

        # audio mute clip select
        with uuid("6df9ba88-35f5-4420-bfd2-1ab2f5e0a604") as case:
            with uuid("65b9ea88-13e2-46c9-9cae-30ffb0378514") as case:
                tips_area_page.more_features.mute_clip()
                current_result = tips_area_page.more_features.get_mute_clip_tick_status()
                image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G6.67.3_AudioMuteClipSelect.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.67.3_AudioMuteClipSelect.png',
                                                       image_result)
                case.result = compare_result and current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_68(self):
        # audio restore volume gray
        with uuid("3bc5adcb-4a79-4a09-8f96-5c931c4773cb") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_restore_original_volume_status()
            case.result = not current_result

        # audio remove all clip marker gray
        with uuid("af2007b6-fb22-4df4-a60b-bef744f7885f") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_remove_all_clip_markers_status()
            case.result = not current_result

        # audio normalize gray
        with uuid("726a98b1-851b-4df4-8a58-f90d6f30d05b") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_normalize_audio_status()
            case.result = not current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_69(self):
        # audio change alias
        with uuid("bf179f41-5f49-433d-9d26-8991779b877f") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.click_change_alias()
            time.sleep(DELAY_TIME)
            tips_area_page.more_features.set_alias('xyz')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.69.0_AudioChangeAlias.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.69.0_AudioChangeAlias.png',
                                                    image_result)
            case.result = compare_result

        # audio reset alias
        with uuid("19add754-d9ef-42d4-888d-dcd259653722") as case:
            time.sleep(DELAY_TIME)
            tips_area_page.more_features.click_reset_alias()
            time.sleep(DELAY_TIME)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.69.1_AudioResetAlias.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.69.1_AudioResetAlias.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_70(self):
        # audio view properties
        with uuid("94ab1838-db9c-4629-bc1f-747f5d23383c") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.view_properties()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_71(self):
        # audio reset all undock disable
        with uuid("6c1bbeff-d943-4ec0-8bfd-c09eb3539854") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.insert_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_reset_all_undock_windows_status()
            case.result = not current_result

        # audio undock timeline
        with uuid("0ed8a4dd-3913-40a6-8db5-225ff8eba27a") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.71.1_AudioUndockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.71.1_AudioUndockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # audio dock timeline
        with uuid("30296815-4b11-4665-8167-9dfb8800f9fb") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(False)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.71.2_AudioDockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.71.2_AudioDockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # audio reset all undock
        with uuid("2386b9d0-0b38-40b3-855e-b56e3f26e1f1") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            tips_area_page.more_features.reset_all_undock_windows()
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.71.3_AudioResetAllUndock.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.71.3_AudioResetAllUndock.png',
                                                    image_result)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_72(self):
        # effect split gray
        with uuid("b377c735-115b-49f5-ad45-b93a28a4d1ae") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(3)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Abstractionism')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_add_to_effect_track()
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.get_btn_split_status()
            case.result = not current_result

        # effect split
        with uuid("99f048d3-3ea5-47e0-925c-ae8af6f63601") as case:
            playback_window_page.set_timecode_slidebar('00_00_03_00')
            tips_area_page.click_TipsArea_btn_split()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.72.1_EffectSplit.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.72.1_EffectSplit.png',
                                                    image_result)
            case.result = compare_result

        # effect select all
        with uuid("770299ae-0b77-4adb-9c6d-d524e1ec672b") as case:
            tips_area_page.more_features.select_all()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.72.2_EffectSelectAll.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.72.2_EffectSelectAll.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_73(self):
        # effect duration
        with uuid("dbf40279-ceae-43b5-9cd8-57ebdf9acf2d") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(3)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Abstractionism')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_add_to_effect_track()
            current_result = tips_area_page.click_TipsArea_btn_Duration()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_74(self):
        # effect modify
        with uuid("c6c41565-113e-4a73-9361-df9f9d8bc46d") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(3)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Abstractionism')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_add_to_effect_track()
            current_result = tips_area_page.click_TipsArea_btn_Modify('Effect')
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_75(self):
        # effect keyframe room
        with uuid("7f32f0d3-7894-4894-8ed6-5d0e51343296") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(3)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Abstractionism')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_add_to_effect_track()
            current_result = tips_area_page.click_keyframe()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_76(self):
        # effect cut
        with uuid("a28d10f4-534a-4df5-8a89-8c2ef507011b") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(3)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Abstractionism')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_add_to_effect_track()
            tips_area_page.more_features.cut()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.76.0_EffectCut.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.76.0_EffectCut.png',
                                                    image_result)
            case.result = compare_result

            # effect paste
        with uuid("789b26bb-f44e-4b78-a569-6d1b3a73fd21") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Abstractionism')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_add_to_effect_track()
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.76.1_EffectPaste.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.76.1_EffectPaste.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_77(self):
        # effect copy
        with uuid("36842aca-9571-42c5-86a5-c3becfc22ca3") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(3)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Abstractionism')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_add_to_effect_track()
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.copy()
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.77.0_EffectCopy.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.77.0_EffectCopy.png',
                                                    image_result)
            case.result = compare_result

        # effect remove
        with uuid("90726504-f5c2-4f54-8eea-cf537c671c0b") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.remove(1)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.77.1_EffectRemove.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.77.1_EffectRemove.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_78(self):
        # effect group ungroup gray
        with uuid("b7fe5b2a-ec22-4f19-97b5-baad3db821df") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(3)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Abstractionism')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_add_to_effect_track()
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_group_ungroup_status()
            case.result = not current_result

        # effect more feature split gray
        with uuid("7bcabc4c-908f-423a-9103-61d9ac12dde0") as case:
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.more_features.get_split_status()
            case.result = not current_result

        # effect more feature split
        with uuid("8b493d1b-30a6-434f-aca0-acae5d4575d7") as case:
            playback_window_page.set_timecode_slidebar('00_00_02_00')
            tips_area_page.click_TipsArea_btn_split()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.78.2_EffectSplit.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.78.2_EffectSplit.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_79(self):
        # effect more feature edit effect
        with uuid("f8d23848-5cbb-46f5-a498-ae726bbec7c0") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(3)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Abstractionism')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_add_to_effect_track()
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.edit_effect()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_80(self):
        # effect more feature duration
        with uuid("c2dd2d03-b5e3-4788-b6b9-710ca18ee724") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(3)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Abstractionism')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_add_to_effect_track()
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.click_set_duration()
            case.result = current_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_81(self):
        # effect reset all undock disable
        with uuid("5db54130-b775-4f02-9def-c34d10dfba5c") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(3)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Abstractionism')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_add_to_effect_track()
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_reset_all_undock_windows_status()
            case.result = not current_result

        # effect undock timeline
        with uuid("91172811-daf2-4de6-9634-ac8125cc7bd2") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.81.1_EffectUndockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.81.1_EffectUndockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # effect dock timeline
        with uuid("d2b4bd44-9c05-416e-8081-c5e26a350143") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(False)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.81.2_EffectDockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.81.2_EffectDockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # effect reset all undock
        with uuid("8b01ab67-243f-44c1-87e3-8a986e47d445") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            tips_area_page.more_features.reset_all_undock_windows()
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.81.3_EffectResetAllUndock.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.81.3_EffectResetAllUndock.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_82(self):
        # pip split gray
        with uuid("957a5b60-e99e-4be5-8c62-415d0ae200d0") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            current_result = tips_area_page.get_btn_split_status()
            case.result = not current_result

        # pip split
        with uuid("93588e35-2feb-42d7-90b6-6fcd067c51ff") as case:
            playback_window_page.set_timecode_slidebar('00_00_02_00')
            tips_area_page.click_TipsArea_btn_split()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.82.1_PiPSplit.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.82.1_PiPSplit.png',
                                                    image_result)
            case.result = compare_result

        # pip select all
        with uuid("1430b80c-637d-44e0-bf44-9e9b5aa6aa6d") as case:
            tips_area_page.more_features.select_all()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.82.2_PiPSelectAll.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.82.2_PiPSelectAll.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_83(self):
        # pip duration
        with uuid("68981394-ec9d-4afa-a234-d6ed68e1dfdd") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            current_result = tips_area_page.click_TipsArea_btn_Duration()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_84(self):
        # pip pip designer
        with uuid("cf778148-5dfd-401c-939e-f168953f08ff") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.tools.select_PiP_Designer()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_85(self):
        # pip mask designer
        with uuid("db621e23-e429-4e38-9494-dcc319e8a4e3") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.tools.select_Mask_Designer()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_86(self):
        # pip blending effect
        with uuid("f668fb0c-2893-4092-8b66-c24efab7f7b3") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.tools.select_Blending_Mode()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_87(self):
        # pip fix enhance
        with uuid("6f78e3a3-25e3-4ac9-9ceb-db593e9cd95d") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.click_fix_enhance()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_88(self):
        # pip keyframe
        with uuid("28dc28f3-1979-4d26-b508-d0ec34f1a683") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.click_keyframe()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_89(self):
        # pip cut
        with uuid("df65054d-19fa-4988-a3ae-68b7320d3696") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            tips_area_page.more_features.cut()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.89.0_PiPCut.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.89.0_PiPCut.png',
                                                    image_result)
            case.result = compare_result

            # pip paste
        with uuid("ab97abf2-e843-4597-b49a-8589df337b88") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.89.1_PiPPaste.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.89.1_PiPPaste.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_90(self):
        # pip copy
        with uuid("81c3d4d1-daa3-4fce-8c4a-18ea3c097174") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.copy()
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.90.0_PiPCopy.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.90.0_PiPCopy.png',
                                                    image_result)
            case.result = compare_result

        # pip remove
        with uuid("66e1d2fe-13e6-4bcd-be45-13d089e6796d") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.remove(1)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.90.1_PiPRemove.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.90.1_PiPRemove.png',
                                                    image_result)
            case.result = compare_result

    @exception_screenshot
    def test1_1_6_91(self):
        # pip copy attributes
        with uuid("92593286-c447-44da-a40b-8f01fd907720") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.copy_keyframe_attributes()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.91.0_PiPCopyAttributes.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.91.0_PiPCopyAttributes.png',
                                                    image_result)
            case.result = compare_result

        # pip paste attributes
        with uuid("86c8da77-d480-4deb-b561-81abcdb982a0") as case:
            tips_area_page.more_features.paste_keyframe_attributes()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.91.1_PiPPasteAttributes.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.91.1_PiPPasteAttributes.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_92(self):
        # pip link unlink gray
        with uuid("9051b5d8-de13-47c2-a84d-351fe944cef9") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            current_result = tips_area_page.more_features.get_link_unlink_status()
            case.result = not current_result

        # pip group ungroup gray
        with uuid("75c59dc9-6a65-4c3e-81c0-7ffa04092e70") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_group_ungroup_status()
            case.result = not current_result

        # pip edit video trim gray
        with uuid("0978ada3-5945-4f91-a839-60441de74742") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_edit_video_trim_status()
            case.result = not current_result

        # pip more feature split gray
        with uuid("8260c22e-f047-4e6a-8cc4-9c0789bee8ee") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_split_status()
            case.result = not current_result

        # pip more feature split
        with uuid("4366a526-06de-40c1-92ea-3316a5373328") as case:
            playback_window_page.set_timecode_slidebar('00_00_02_00')
            tips_area_page.click_TipsArea_btn_split()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.92.1_PiPSplit.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.92.1_PiPSplit.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_93(self):
        # pip fix enhance
        with uuid("1d0b9158-0a9b-4549-91bb-282328fb1153") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            current_result = tips_area_page.more_features.edit_video_FixEnhance()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_94(self):
        # pip video collage gray
        with uuid("788de8fe-1f8a-4e5b-acd0-08f60a832204") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            current_result = tips_area_page.more_features.get_edit_in_video_collage_status()
            case.result = not current_result

        # pip restore opacity gray
        with uuid("d75230d7-614f-4c41-bbbb-f16915a55bfd") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_video_restore_opacity_status()
            case.result = not current_result

        # pip enable fade in fade out
        with uuid("ac4baa2e-cc13-420b-8b7f-e3f327520fe2") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.edit_video_enable_fade_feature()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.94.2_PiPFadeInFadeOut.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.94.2_PiPFadeInFadeOut.png',
                                                    image_result)
            case.result = compare_result

        # pip restore opacity
        with uuid("0411d3ef-e894-4885-895c-a27e6f585b4a") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.edit_video_restore_opacity()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.94.3_PiPRestoreOpacity.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.94.3_PiPRestoreOpacity.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_95(self):
        # pip edit image gray
        with uuid("cad21048-644d-47c6-8e02-2e70d68e21f2") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            current_result = tips_area_page.more_features.get_edit_image_status()
            case.result = not current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_96(self):
        # pip Set Clip Attributes Set Duration
        with uuid("127ca99a-3925-4246-b59f-7995c07bbdd3") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            current_result = tips_area_page.more_features.click_clip_attributes_duration()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_97(self):
        # pip Set Clip Attributes Set Blending Mode
        with uuid("1e6a1675-8a47-446f-a568-c5bbd5a04145") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            tips_area_page.more_features.set_attributes_blending_mode(3)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.97.0_PiPBlendingMode.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.97.0_PiPBlendingMode.png',
                                                    image_result)
            case.result = compare_result

# @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_98(self):
        # pip change alias
        with uuid("114ea627-3029-441b-b10c-a9a28e1fdc39") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.click_change_alias()
            tips_area_page.more_features.set_alias('ab12')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.98.0_PiPChangeAlias.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.98.0_PiPChangeAlias.png',
                                                    image_result)
            case.result = compare_result

        # pip reset alias
        with uuid("f7a6d684-886c-4847-9d3c-9ffda6ad101d") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.click_reset_alias()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.98.1_PiPResetAlias.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.98.1_PiPResetAlias.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_99(self):
        # pip reset all undock disable
        with uuid("d93c62b2-6b9f-4997-aeaf-44a12e274874") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Dialog_06')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_reset_all_undock_windows_status()
            case.result = not current_result

        # pip undock timeline
        with uuid("c7b7e62a-b97c-457d-b2ae-f56b6030918b") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.99.1_PiPUndockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.99.1_PiPUndockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # pip dock timeline
        with uuid("17a069c0-d7e7-40be-88ed-d451861d03c3") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(False)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.99.2_PiPDockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.99.2_PiPDockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # pip reset all undock
        with uuid("7534f53d-cea0-40f7-8957-d50635d6d0a4") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            tips_area_page.more_features.reset_all_undock_windows()
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.99.3_PiPResetAllUndock.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.99.3_PiPResetAllUndock.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_100(self):
        # particle split gray
        with uuid("e43a14c6-3541-4ea3-9b14-d4e1fa78f424") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(5)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Maple')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            current_result = tips_area_page.get_btn_split_status()
            case.result = not current_result

        # particle split
        with uuid("4a051d99-86fd-443c-b026-4b14530693d7") as case:
            playback_window_page.set_timecode_slidebar('00_00_02_00')
            tips_area_page.click_TipsArea_btn_split()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.100.1_ParticleSplit.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.100.1_ParticleSplit.png',
                                                    image_result)
            case.result = compare_result

        # particle select all
        with uuid("d8ca7147-2a67-468c-bc1b-777ec88dde4a") as case:
            tips_area_page.more_features.select_all()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.100.2_ParticleSelectAll.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.100.2_ParticleSelectAll.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_101(self):
        # particle duration
        with uuid("37cc68aa-5a08-4881-bd92-c4adff293b50") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(5)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Maple')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            current_result = tips_area_page.click_TipsArea_btn_Duration()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_102(self):
        # particle particle designer
        with uuid("1c805311-0122-43fd-9597-f3abcea0e1ff") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(5)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Maple')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.click_TipsArea_btn_Designer('particle')
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_103(self):
        # particle cut
        with uuid("5e2f540e-2f5f-487b-990e-e5494d43adfb") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(5)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Maple')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            tips_area_page.more_features.cut()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.103.0_ParticleCut.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.103.0_ParticleCut.png',
                                                    image_result)
            case.result = compare_result

        # particle paste
        with uuid("7568ebff-0004-4bbf-88e9-3c472a72eb78") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Maple')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.103.1_ParticlePaste.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.103.1_ParticlePaste.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_104(self):
        # particle copy
        with uuid("57704653-cbe8-4ae6-9f96-83ee63428b64") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(5)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Maple')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.copy()
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.104.0_ParticleCopy.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.104.0_ParticleCopy.png',
                                                    image_result)
            case.result = compare_result

        # particle remove
        with uuid("ca550134-958d-4d76-bfd3-74be8c98c203") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.remove(1)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.104.1_ParticleRemove.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.104.1_ParticleRemove.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_105(self):
        # particle more feature split gray
        with uuid("2b6c874e-0677-4478-816e-5e6042631931") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(5)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Maple')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.more_features.get_split_status()
            case.result = not current_result

        # particle more feature link unlink gray
        with uuid("fca056d2-eba6-4cf8-b8d7-226a24b52580") as case:
            current_result = tips_area_page.more_features.get_link_unlink_status()
            case.result = not current_result

        # particle group ungroup gray
        with uuid("70bca743-961d-459c-8ac7-1b13eff079fa") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_group_ungroup_status()
            case.result = not current_result

        # particle more feature split
        with uuid("ec4d5d23-6568-45d2-9a6c-f8a189fc4869") as case:
            playback_window_page.set_timecode_slidebar('00_00_02_00')
            tips_area_page.click_TipsArea_btn_split()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.105.1_ParticleSplit.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.105.1_ParticleSplit.png',
                                                    image_result)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_106(self):
        # particle more feature duration
        with uuid("b63e1650-e831-469b-9d56-e89a7d2a8913") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(5)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Maple')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.click_set_duration()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_107(self):
        # particle reset all undock disable
        with uuid("186a2eb0-56d7-446d-846e-03bebbe7d2ff") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(5)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Maple')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_reset_all_undock_windows_status()
            case.result = not current_result

        # particle undock timeline
        with uuid("a63d7f93-9348-4533-aaa5-c12da42ae969") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.107.1_ParticleUndockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.107.1_ParticleUndockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # particle dock timeline
        with uuid("77472655-8e31-45c0-974f-0f694f0feecf") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(False)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.107.2_ParticleDockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.107.2_ParticleDockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # particle reset all undock
        with uuid("a5d21c3e-903f-4fb1-a84d-ff6a4f5400e6") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            tips_area_page.more_features.reset_all_undock_windows()
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.107.3_ParticleResetAllUndock.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.107.3_ParticleResetAllUndock.png',
                                                    image_result)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_108(self):
        # title split gray
        with uuid("1478a8b0-3d11-46cc-bd54-f9de5b5fe287") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Clover_01')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            current_result = tips_area_page.get_btn_split_status()
            case.result = not current_result

        # title split
        with uuid("3bed273e-8b3f-4e1c-901b-7c7dbf9a06d7") as case:
            playback_window_page.set_timecode_slidebar('00_00_02_00')
            tips_area_page.click_TipsArea_btn_split()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.108.1_TitleSplit.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.108.1_TitleSplit.png',
                                                    image_result)
            case.result = compare_result

        # title select all
        with uuid("4c615da6-9998-469f-afba-154c8868dc31") as case:
            tips_area_page.more_features.select_all()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.108.2_TitleSelectAll.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.108.2_TitleSelectAll.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_109(self):
        # title duration
        with uuid("dcb3e614-1679-4f9c-bb88-130e85c4b3ff") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Clover_01')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            current_result = tips_area_page.click_TipsArea_btn_Duration()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_110(self):
        # title title designer
        with uuid("a1ba5d48-c37d-4320-bedc-9d2a9adc03f0") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Clover_01')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.click_TipsArea_btn_Designer('title')
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_111(self):
        # title cut
        with uuid("555f5542-f0f2-4e41-b3e5-114172d8dcef") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Clover_01')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            tips_area_page.more_features.cut()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.111.0_TitleCut.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.111.0_TitleCut.png',
                                                    image_result)
            case.result = compare_result

        # title paste
        with uuid("97631eae-fefd-44b4-a087-6d7cc0d08722") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Clover_01')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.111.1_TitlePaste.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.111.1_TitlePaste.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_112(self):
        # title copy
        with uuid("70632f2d-677c-4546-bf41-a590ad6ac144") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Clover_01')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            tips_area_page.more_features.copy()
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.112.0_TitleCopy.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.112.0_TitleCopy.png',
                                                    image_result)
            case.result = compare_result

        # title remove
        with uuid("ce01e9dd-75cc-4c5b-80ba-5ed4933c4389") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.remove(1)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.112.1_TitleRemove.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.112.1_TitleRemove.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_113(self):
        # title more feature split gray
        with uuid("726627df-a2fd-412a-abce-d1c99e5a270e") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Clover_01')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.more_features.get_split_status()
            case.result = not current_result

        # title more feature link unlink gray
        with uuid("e5cf7ff3-b856-4e3c-bc93-0341dd557109") as case:
            current_result = tips_area_page.more_features.get_link_unlink_status()
            case.result = not current_result

        # title group ungroup gray
        with uuid("a0780182-2297-480c-8c01-d294ea2d6354") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_group_ungroup_status()
            case.result = not current_result

        # title more feature split
        with uuid("7439d8b1-5b41-41c7-a46f-41ffc8bac806") as case:
            playback_window_page.set_timecode_slidebar('00_00_02_00')
            tips_area_page.click_TipsArea_btn_split()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.105.1_ParticleSplit.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.105.1_ParticleSplit.png',
                                                    image_result)
            case.result = compare_result



    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_114(self):
        # title more feature title designer
        with uuid("f56eb659-9e8e-4ca3-a304-354224c908d1") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Clover_01')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.edit_title()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_115(self):
        # title more feature duration
        with uuid("4bffc987-bed9-4a33-a7ef-0bb3322cfe6d") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Clover_01')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.click_set_duration()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_116(self):
        # title reset all undock disable
        with uuid("4142e349-c0ad-4f02-b75c-24e13813d06e") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Clover_01')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_reset_all_undock_windows_status()
            case.result = not current_result

        # title undock timeline
        with uuid("a4aa672b-2b02-4a01-8d1f-7fdb22c04c8b") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.116.1_TitleUndockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.116.1_TitleUndockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # title dock timeline
        with uuid("e990a764-ed4f-4a15-b657-5c4195257d19") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(False)
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.116.2_TitleDockTimeline.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.116.2_TitleDockTimeline.png',
                                                    image_result)
            case.result = compare_result

        # title reset all undock
        with uuid("cff38015-59e2-48c2-8810-d0fc022fd48a") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.dock_undock_timeline_window(True)
            tips_area_page.more_features.reset_all_undock_windows()
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.116.3_TitleResetAllUndock.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.116.3_TitleResetAllUndock.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_117(self):
        # color board split gray
        with uuid("43c8f935-8acb-4e4b-9678-d64b2f5548b9") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            current_result = tips_area_page.get_btn_split_status()
            case.result = not current_result

        # color board split
        with uuid("f4ec841f-5dc9-412f-8a99-62ecf1f96633") as case:
            playback_window_page.set_timecode_slidebar('00_00_02_00')
            tips_area_page.click_TipsArea_btn_split()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.117.1_ColorBoardSplit.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.117.1_ColorBoardSplit.png',
                                                    image_result)
            case.result = compare_result

        # color board select all
        with uuid("4724eb54-3cb5-406d-b4a5-00f934f1decd") as case:
            tips_area_page.more_features.select_all()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.117.2_ColorBoardSelectAll.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.117.2_ColorBoardSelectAll.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_118(self):
        # color board duration
        with uuid("dcb3e614-1679-4f9c-bb88-130e85c4b3ff") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            current_result = tips_area_page.click_TipsArea_btn_Duration()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_119(self):
        # color board PiP Designer
        with uuid("0f2762dd-051b-4b17-91fe-f0744713fcd7") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.tools.select_PiP_Designer()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_120(self):
        # color board Mask Designer
        with uuid("d6b427ae-ec88-4fa5-8fb7-a68011a9e771") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.tools.select_Mask_Designer()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_121(self):
        # color board keyframe room
        with uuid("eed2d568-c434-427a-813f-1760fc346cf3") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.click_keyframe()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_122(self):
        # color board color change
        with uuid("f26b7cb3-07b4-4032-aa34-19b18af301ee") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_ChangeColor('05364A')
            image_result = tips_area_page.snapshot(locator=L.library_preview.upper_view_region,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.122.0_ColorBoardChangeColor.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.122.0_ColorBoardChangeColor.png',
                                                    image_result)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_123(self):
        # color board cut
        with uuid("2ceba0c8-676a-434b-a7f8-139fde8be170") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            tips_area_page.more_features.cut()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.123.0_ColorBoardCut.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.123.0_ColorBoardCut.png',
                                                    image_result)
            case.result = compare_result

        # color board paste
        with uuid("9d2f9a4c-1fb5-4a2e-9f56-f86e828c7ea4") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.123.1_ColorBoardPaste.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.123.1_ColorBoardPaste.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_124(self):
        # color board copy
        with uuid("90f6abec-0c82-4354-ba36-0499aa566f69") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            tips_area_page.more_features.copy()
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.paste('Insert')
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.124.0_ColorBoardCopy.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.124.0_ColorBoardCopy.png',
                                                    image_result)
            case.result = compare_result

        # color board remove
        with uuid("398b2d01-80ef-45ff-8054-a7a135065710") as case:
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.remove(1)
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.124.1_ColorBoardRemove.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.124.1_ColorBoardRemove.png',
                                                    image_result)
            case.result = compare_result

    @exception_screenshot
    def test1_1_6_125(self):
        # color board copy attributes
        with uuid("de60397f-edf2-4b12-a9c5-30a6ab53d2e5") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME * 4)
            tips_area_page.more_features.copy_keyframe_attributes()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.125.0_ColorBoardCopyAttributes.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.125.0_ColorBoardCopyAttributes.png',
                                                    image_result)
            case.result = compare_result

        # color board paste attributes
        with uuid("dac5a007-992b-493f-8404-83f02bcdc6e7") as case:
            tips_area_page.more_features.paste_keyframe_attributes()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.125.1_ColorBoardPasteAttributes.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.125.1_ColorBoardPasteAttributes.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_126(self):
        # color board link unlink gray
        with uuid("fb5607b5-afe3-4e60-b6f0-4f1a1d02ff45") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_link_unlink_status()
            case.result = not current_result

        # color board group ungroup gray
        with uuid("20a5cee7-5193-41ab-9328-2d512076abf3") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = tips_area_page.more_features.get_group_ungroup_status()
            case.result = not current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_127(self):
        # color board more feature split gray
        with uuid("04c47ae3-5af0-4166-9c1b-d41fe8109e16") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.more_features.get_split_status()
            case.result = not current_result

        # color board more feature split
        with uuid("46bd2fd8-d1cc-4d86-a5e2-171a391ffba7") as case:
            playback_window_page.set_timecode_slidebar('00_00_02_00')
            tips_area_page.click_TipsArea_btn_split()
            image_result = tips_area_page.snapshot(locator=tips_area_page.area.timeline,
                                                   file_name=Auto_Ground_Truth_Folder + 'G6.127.1_ColorBoardSplit.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G6.127.1_ColorBoardSplit.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_6_128(self):
        # color board more feature trim gray
        with uuid("04c47ae3-5af0-4166-9c1b-d41fe8109e16") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('51,53,128')
            time.sleep(DELAY_TIME)
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.more_features.get_edit_video_trim_status()
            case.result = not current_result

        # color board more feature fix enhance gray
        with uuid("ef225fa3-a83b-46b3-abd8-ef4d7c416095") as case:
            time.sleep(DELAY_TIME)
            current_result = tips_area_page.more_features.get_edit_video_fixenhance_status()
            case.result = not current_result

'''
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

'''






















