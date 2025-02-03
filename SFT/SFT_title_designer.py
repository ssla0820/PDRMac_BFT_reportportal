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
title_designer_page = PageFactory().get_page_object('title_designer_page',mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Title Designer.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<


# For Ground Truth / Test Material folder
#Ground_Truth_Folder = app.ground_truth_root + '/Title_Designer/'
#Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Title_Designer/'
#Test_Material_Folder = app.testing_material

Ground_Truth_Folder = '/Users/RDUC/Desktop/Ernesto/SFT/GroundTruth/Title_Designer/'
Auto_Ground_Truth_Folder = '/Users/RDUC/Desktop/Ernesto/SFT/ATGroundTruth/Title_Designer/'
Test_Material_Folder = '/Users/RDUC/Desktop/Ernesto/Material/'

DELAY_TIME = 1

class Test_Title_Designer():
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
            google_sheet_execution_log_init('Title_Designer')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"title designer result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
    def test1_1_7_1(self):
        # title room new create button
        with uuid("c5b7d346-4511-4266-aa61-0f19cc0c29ff") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            current_result = title_room_page.click_CreateNewTitle_btn()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_2(self):
        # title room modify select button
        with uuid("640ac6fa-024f-4e49-ba6a-31e3df43bde6") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Clover_01')
            time.sleep(DELAY_TIME)
            current_result = title_room_page.click_ModifySelectedTitle_btn()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_3(self):
        # title room double click to modify
        with uuid("4c592d50-628d-4e14-8e04-21325aca55f0") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Clover_01')
            time.sleep(DELAY_TIME)
            title_room_page.double_click()
            time.sleep(DELAY_TIME * 4)
            current_result = title_room_page.check_enter_title_designer()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_4(self):
        # title room right click menu modify
        with uuid("01a08072-61b5-46f6-b4bc-d1281d607982") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            main_page.select_library_icon_view_media('Clover_01')
            time.sleep(DELAY_TIME)
            current_result = title_room_page.select_RightClickMenu_ModifyTemplate()
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_5(self):
        # title designer maximize window
        with uuid("96abf2df-20b4-4796-b103-39ee42a9b229") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            title_room_page.click_CreateNewTitle_btn()
            title_designer_page.click_maximize_btn()
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.5.0_TitleDesignerMaximize.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.5.0_TitleDesignerMaximize.png',
                                                    image_result)
            case.result = compare_result

        # title designer restore down window
        with uuid("dad3eb78-1e83-4a97-8488-0b457cdf94c7") as case:
            time.sleep(DELAY_TIME * 4)
            title_designer_page.click_maximize_btn()
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.5.1_TitleDesignerRestoreDown.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.5.1_TitleDesignerRestoreDown.png',
                                                    image_result)
            case.result = compare_result

        # title designer close window
        with uuid("1f016958-ab34-4b21-9040-432b472dd98e") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = title_designer_page.click_close_btn()
            case.result = current_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_6(self):
        # title designer insert title
        with uuid("3a0bbbd5-0def-4040-8da9-778f51bf2098") as case:
            with uuid("437df26b-35ea-4037-be55-60fa6e81ccf9") as case:
                time.sleep(DELAY_TIME * 4)
                main_page.enter_room(1)
                time.sleep(DELAY_TIME * 4)
                title_room_page.click_CreateNewTitle_btn()
                time.sleep(DELAY_TIME * 4)
                title_designer_page.insert_title('aaABC123')
                time.sleep(DELAY_TIME * 4)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.6.0_TitleDesignerInsertTitle.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.6.0_TitleDesignerInsertTitle.png',
                                                        image_result)
                case.result = compare_result

        # title designer undo
        with uuid("a14f684a-9716-4095-ae02-27f4271bfc9a") as case:
            title_designer_page.click_undo_btn()
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.6.1_TitleDesignerUndo.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.6.1_TitleDesignerUndo.png',
                                                    image_result)
            case.result = compare_result

        # title designer redo
        with uuid("fb621447-1952-4fad-a11b-0c0ac158786f") as case:
            title_designer_page.click_redo_btn()
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.6.2_TitleDesignerRedo.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.6.2_TitleDesignerRedo.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_7(self):
        # title designer advance mode
        with uuid("5729fbf0-311b-4f0a-8ecb-91ce6bce99a1") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            title_room_page.click_CreateNewTitle_btn()
            time.sleep(DELAY_TIME * 4)
            title_designer_page.switch_mode(2)
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.7.0_TitleDesignerAdvanceMode.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.7.0_TitleDesignerAdvanceMode.png',
                                                    image_result)
            case.result = compare_result

        # title designer express mode
        with uuid("e5714df0-c300-42d1-b95f-e574cee2fba6") as case:
            time.sleep(DELAY_TIME * 4)
            title_designer_page.switch_mode(1)
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.7.1_TitleDesignerExpressMode.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.7.1_TitleDesignerExpressMode.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_8(self):
        # title designer zoom in
        with uuid("0a243c42-7772-4b70-9e87-348bb1c0e4d5") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            title_room_page.click_CreateNewTitle_btn()
            time.sleep(DELAY_TIME * 4)
            title_designer_page.click_zoom_in()
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.8.0_TitleDesignerZoomIn.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.8.0_TitleDesignerZoomIn.png',
                                                    image_result)
            case.result = compare_result

        # title designer zoom out
        with uuid("3295e9db-ee42-405d-a59c-b3947a759594") as case:
            time.sleep(DELAY_TIME * 4)
            title_designer_page.click_zoom_out()
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.8.1_TitleDesignerZoomOut.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.8.1_TitleDesignerZoomOut.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_9(self):
        # title designer 400%
        with uuid("27164fc3-1ff9-4e4d-84f6-3e379b73f1cf") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            title_room_page.click_CreateNewTitle_btn()
            time.sleep(DELAY_TIME * 4)
            title_designer_page.click_viewer_zoom_menu('400%')
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.9.0_TitleDesigner400.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.9.0_TitleDesigner400.png',
                                                    image_result)
            case.result = compare_result

        # title designer 300%
        with uuid("c7d3af85-e449-4eee-aa3e-274d4db76e4a") as case:
            time.sleep(DELAY_TIME * 4)
            title_designer_page.click_viewer_zoom_menu('300%')
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.9.1_TitleDesigner300.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.9.1_TitleDesigner300.png',
                                                    image_result)
            case.result = compare_result

        # title designer 200%
        with uuid("4d767b7e-8108-489f-874f-e3128aeb1802") as case:
            time.sleep(DELAY_TIME * 4)
            title_designer_page.click_viewer_zoom_menu('200%')
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.9.2_TitleDesigner200.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.9.2_TitleDesigner200.png',
                                                    image_result)
            case.result = compare_result

        # title designer 100%
        with uuid("f011ad25-3c21-45a4-a01b-8637096b26ff") as case:
            time.sleep(DELAY_TIME * 4)
            title_designer_page.click_viewer_zoom_menu('100%')
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.9.3_TitleDesigner100.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.9.3_TitleDesigner100.png',
                                                    image_result)
            case.result = compare_result

        # title designer 75%
        with uuid("f4de13dc-b7de-4a18-bc34-f89d74319c62") as case:
            time.sleep(DELAY_TIME * 4)
            title_designer_page.click_viewer_zoom_menu('75%')
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.9.4_TitleDesigner75.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.9.4_TitleDesigner75.png',
                                                    image_result)
            case.result = compare_result

        # title designer 50%
        with uuid("231c7bf0-c49e-4ea2-a559-373ed54dd22f") as case:
            time.sleep(DELAY_TIME * 4)
            title_designer_page.click_viewer_zoom_menu('50%')
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.9.5_TitleDesigner50.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.9.5_TitleDesigner50.png',
                                                    image_result)
            case.result = compare_result

        # title designer 25%
        with uuid("72cbcad4-b2c8-4f3f-b532-75632fd9b688") as case:
            time.sleep(DELAY_TIME * 4)
            title_designer_page.click_viewer_zoom_menu('25%')
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.9.6_TitleDesigner25.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.9.6_TitleDesigner25.png',
                                                    image_result)
            case.result = compare_result

        # title designer 10%
        with uuid("5b1cd306-e8d1-4e28-b8d0-282387cf2298") as case:
            time.sleep(DELAY_TIME * 4)
            title_designer_page.click_viewer_zoom_menu('10%')
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.9.7_TitleDesigner10.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.9.7_TitleDesigner10.png',
                                                    image_result)
            case.result = compare_result

        # title designer Fit
        with uuid("584e6b52-4561-40e5-86af-83e9a19bd9a8") as case:
            time.sleep(DELAY_TIME * 4)
            title_designer_page.click_viewer_zoom_menu('Fit')
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.9.8_TitleDesignerFit.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.9.8_TitleDesignerFit.png',
                                                    image_result)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_10(self):
        # title designer play/pause
        with uuid("87faec2a-cad3-4c9e-9230-d1d6790f39da") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            title_room_page.click_CreateNewTitle_btn()
            time.sleep(DELAY_TIME * 4)
            current_result = title_designer_page.click_preview_operation('Play')
            case.result = current_result

        # title designer stop
        with uuid("d56267d0-023f-4bec-b937-66801e31bfbe") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = title_designer_page.click_preview_operation('Stop')
            case.result = current_result

        # title designer Next frame
        with uuid("4d648642-72c4-4aef-8d56-2d3542bd807b") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = title_designer_page.click_preview_operation('Next_Frame')
            case.result = current_result

        # title designer Previous frame
        with uuid("31618df6-3bfc-4a7b-b0d5-599943b24d2c") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = title_designer_page.click_preview_operation('Previous_Frame')
            case.result = current_result

        # title designer fast forward
        with uuid("ab3f0d58-5fa6-45d5-b996-d79e69f8e7b7") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = title_designer_page.click_preview_operation('Fast_Foward')
            case.result = current_result

        # title designer timecode
        with uuid("4d74da5c-e4d8-403f-822b-dc1f5ee0c223") as case:
            time.sleep(DELAY_TIME * 4)
            title_designer_page.set_timecode('00_00_03_00')
            time.sleep(DELAY_TIME * 4)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.10.5_TitleDesignerTimecode.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.10.5_TitleDesignerTimecode.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_11(self):
        # title designer char preset
        with uuid("ff5751f2-3a11-45fc-ab5c-d73c3156152a") as case:
            with uuid("2b018c9c-e1c9-4823-8c51-1af434e8b15f") as case:
                time.sleep(DELAY_TIME * 4)
                main_page.enter_room(1)
                time.sleep(DELAY_TIME * 4)
                title_room_page.click_CreateNewTitle_btn()
                time.sleep(DELAY_TIME * 4)
                title_designer_page.apply_character_presets(4, 1)
                time.sleep(DELAY_TIME * 4)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.11.0_TitleDesignerCharacterPreset.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.11.0_TitleDesignerCharacterPreset.png',
                                                        image_result)
                case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_12(self):
        # title designer font type
        with uuid("3782ed4a-7e0d-403b-8ffc-5d6f16fdef1d") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME)
            title_room_page.click_CreateNewTitle_btn()
            time.sleep(DELAY_TIME)
            title_designer_page.set_font_type('Optima')
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.12.0_TitleDesignerFontType.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.12.0_TitleDesignerFontType.png',
                                                    image_result)
            case.result = compare_result

        # title designer font size
        with uuid("4e606fdb-2e20-4296-bb5b-1f4ffdbebbbc") as case:
            title_designer_page.set_font_size('24')
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.12.1_TitleDesignerFontSize.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.12.1_TitleDesignerFontSize.png',
                                                    image_result)
            case.result = compare_result

        # title designer font face color
        with uuid("11389ab7-da57-4866-9784-446a52aec55f") as case:
            title_designer_page.set_font_face_color('100', '75', '200')
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.12.2_TitleDesignerFontFaceColor.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.12.2_TitleDesignerFontFaceColor.png',
                                                    image_result)
            case.result = compare_result

        # title designer line spacing
        with uuid("908df224-09dd-402c-b9c0-a37377ededd5") as case:
            title_designer_page.set_line_spacing_amount('5')
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.12.3_TitleDesignerLineSpacing.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.12.3_TitleDesignerLineSpacing.png',
                                                    image_result)
            case.result = compare_result

        # title designer text spacing
        with uuid("9a9e3e9d-a554-4496-a263-84579e335995") as case:
            title_designer_page.set_text_spacing_amount('8')
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.12.4_TitleDesignerTextSpacing.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.12.4_TitleDesignerTextSpacing.png',
                                                    image_result)
            case.result = compare_result

        # title designer kerning
        with uuid("78bf3056-8813-467e-b513-fb926df1b934") as case:
            title_designer_page.set_kerning_check(1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.12.5_TitleDesignerKerning.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.12.5_TitleDesignerKerning.png',
                                                    image_result)
            case.result = compare_result

        # title designer bold
        with uuid("7eca4743-4c63-4181-bd5f-604e05eebde4") as case:
            title_designer_page.click_bold_btn()
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.12.6_TitleDesignerBold.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.12.6_TitleDesignerBold.png',
                                                    image_result)
            case.result = compare_result

        # title designer italic
        with uuid("b07c5b18-79b8-47d2-b97b-2c8c0326245f") as case:
            title_designer_page.click_italic_btn()
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.12.7_TitleDesignerItalic.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.12.7_TitleDesignerItalic.png',
                                                    image_result)
            case.result = compare_result

        # title designer align right
        with uuid("ec7ac69c-1386-4f50-a9b0-bba6eec48a7c") as case:
            title_designer_page.set_align(3)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.12.8_TitleDesignerAlignRight.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.12.8_TitleDesignerAlignRight.png',
                                                    image_result)
            case.result = compare_result

        # title designer align center
        with uuid("f54d1e02-4470-4766-a45d-12de42a9404e") as case:
            title_designer_page.set_align(2)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.12.9_TitleDesignerAlignCenter.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.12.9_TitleDesignerAlignCenter.png',
                                                    image_result)
            case.result = compare_result

        # title designer align left
        with uuid("d09ca4e6-0e8b-4e80-b0b8-0f48b4d911cc") as case:
            title_designer_page.set_align(1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.12.10_TitleDesignerAlignLeft.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.12.10_TitleDesignerAlignLeft.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_13(self):
        # title designer font face untick
        with uuid("84e6d98d-7ebe-48c0-9701-d832f560043a") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME)
            title_room_page.click_CreateNewTitle_btn()
            time.sleep(DELAY_TIME)
            title_designer_page.set_check_font_face(0)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.13.0_TitleDesignerFontFaceUntick.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.13.0_TitleDesignerFontFaceUntick.png',
                                                    image_result)
            case.result = compare_result

        # title designer font face tick
        with uuid("a9142749-5764-46d9-bcea-d4c2a60ee092") as case:
            title_designer_page.set_check_font_face(1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.13.1_TitleDesignerFontFaceTick.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.13.1_TitleDesignerFontFaceTick.png',
                                                    image_result)
            case.result = compare_result

        # title designer font face blur default
        with uuid("12aad65a-4b0f-4731-a6ba-10f64b5ebf48") as case:
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.13.2_TitleDesignerFontFaceBlurDefault.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.13.2_TitleDesignerFontFaceBlurDefault.png',
                                                    image_result)
            case.result = compare_result

        # title designer font face blur slider and max
        with uuid("52d76114-4e96-446a-b435-334ac2f1d591") as case:
            with uuid("1fe8924b-3042-4ae5-a098-47511a6b0b8e") as case:
                title_designer_page.drag_font_face_blur_slider(20)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.13.3_TitleDesignerFontFaceBlurSlider.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.13.3_TitleDesignerFontFaceBlurSlider.png',
                                                        image_result)
                case.result = compare_result

        # title designer font face blur input and min
        with uuid("30e6771a-2b96-4af6-b33d-ca414950c069") as case:
            with uuid("4f4022bc-81ee-4518-92dc-e3aa04bf3386") as case:
                title_designer_page.input_font_face_blur_value('0')
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.13.4_TitleDesignerFontFaceBlurInput.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.13.4_TitleDesignerFontFaceBlurInput.png',
                                                        image_result)
                case.result = compare_result

        # title designer font face blur arrow
        with uuid("b10308c5-3fe2-4c46-ab20-ba947f5cad00") as case:
            title_designer_page.click_font_face_blur_arrow_btn(0)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.13.5_TitleDesignerFontFaceBlurArrow.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.13.5_TitleDesignerFontFaceBlurArrow.png',
                                                    image_result)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_14(self):
        # title designer font face opacity default
        with uuid("ab9ebc7b-90ac-4cb9-ad68-040b3635aaf2") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME)
            title_room_page.click_CreateNewTitle_btn()
            time.sleep(DELAY_TIME)
            title_designer_page.set_check_font_face(1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.14.0_TitleDesignerFontFaceOpacityDefault.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.14.0_TitleDesignerFontFaceOpacityDefault.png',
                                                    image_result)
            case.result = compare_result

        # title designer font face opacity slider min
        with uuid("24c61483-8d64-4eab-a573-27dbbec98c4e") as case:
            with uuid("aa2887d1-9c47-4034-b7ca-942fa4da28d4") as case:
                title_designer_page.drag_font_face_opacity_slider(0)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.14.1_TitleDesignerFontFaceOpacitySlider.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.14.1_TitleDesignerFontFaceOpacitySlider.png',
                                                        image_result)
                case.result = compare_result

        # title designer font face opacity input max
        with uuid("0fa9d46a-041b-4fa3-aa87-ef74f592d9f9") as case:
            with uuid("ba856d3e-b1d2-4082-bb54-b923aef9af9f") as case:
                title_designer_page.input_font_face_opacity_value('1000')
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.14.2_TitleDesignerFontFaceOpacityInput.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.14.2_TitleDesignerFontFaceOpacityInput.png',
                                                        image_result)
                case.result = compare_result

        # title designer font face opacity arrow
        with uuid("c61e452f-695b-4d7b-8888-18bd5c037b27") as case:
            title_designer_page.click_font_face_opacity_arrow_btn(1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.14.3_TitleDesignerFontFaceOpacityArrow.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.14.3_TitleDesignerFontFaceOpacityArrow.png',
                                                    image_result)
            case.result = compare_result

        # title designer font face fill type uniform
        with uuid("373d2506-2325-41e5-a38e-38cd1652a5b4") as case:
            title_designer_page.apply_font_face_uniform_color('60', '70', '80')
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.14.4_TitleDesignerFontFaceFillTypeUniform.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.14.4_TitleDesignerFontFaceFillTypeUniform.png',
                                                    image_result)
            case.result = compare_result

        # title designer font face fill type 2 color gradient
        with uuid("54528614-a4dc-4b31-8603-30b3d856c3b8") as case:
            title_designer_page.apply_font_face_2_color('20', '30', '40', '50', '60', '70')
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.14.5_TitleDesignerFontFaceFillType2Color.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.14.5_TitleDesignerFontFaceFillType2Color.png',
                                                    image_result)
            case.result = compare_result

        # title designer font face fill type 4 color gradient
        with uuid("b478d12b-9b02-4476-9518-8513478ecde3") as case:
            title_designer_page.apply_font_face_4_color('20', '30', '40', '50', '60', '70', '55', '75', '120', '45', '170', '200')
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.14.6_TitleDesignerFontFaceFillType4Color.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.14.6_TitleDesignerFontFaceFillType4Color.png',
                                                    image_result)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_15(self):
        # title designer border untick
        with uuid("ae795198-7cab-4420-a5ce-d155dca9e00c") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME)
            title_room_page.click_CreateNewTitle_btn()
            time.sleep(DELAY_TIME)
            title_designer_page.set_check_border(0)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.15.0_TitleDesignerBorderUntick.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.15.0_TitleDesignerBorderUntick.png',
                                                    image_result)
            case.result = compare_result

        # title designer border tick
        with uuid("c0163532-0565-47c2-aaba-74b57288bf71") as case:
            title_designer_page.set_check_border(1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.15.1_TitleDesignerBorderTick.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.15.1_TitleDesignerBorderTick.png',
                                                    image_result)
            case.result = compare_result

        # title designer border size default
        with uuid("14502754-845f-41b1-9f68-4fed18fb2f15") as case:
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.15.2_TitleDesignerBorderSizeDefault.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.15.2_TitleDesignerBorderSizeDefault.png',
                                                    image_result)
            case.result = compare_result

        # title designer border size slider max
        with uuid("c119a5d2-196e-4239-8beb-006e1bd9e631") as case:
            with uuid("6a806a0b-59c6-45c2-8902-b411af2ca925") as case:
                title_designer_page.drag_border_size_slider(10, 0)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.15.3_TitleDesignerBorderSizeSlider.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.15.3_TitleDesignerBorderSizeSlider.png',
                                                        image_result)
                case.result = compare_result

        # title designer border size input min
        with uuid("45590173-cadc-46f4-88d9-f48c80810138") as case:
            with uuid("2c979109-3631-4f53-864e-b1c41d04562a") as case:
                title_designer_page.input_border_size_value('10', 0)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.15.4_TitleDesignerBorderSizeInput.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.15.4_TitleDesignerBorderSizeInput.png',
                                                        image_result)
                case.result = compare_result

        # title designer border size arrow
        with uuid("2961a17b-462a-4a5b-ad3a-db9748581b31") as case:
            title_designer_page.click_size_value_arrow_btn(0)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.15.5_TitleDesignerBorderSizeArrow.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.15.5_TitleDesignerBorderSizeArrow.png',
                                                    image_result)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_16(self):
        # title designer border blur default
        with uuid("3e63aa6b-3856-4cfc-be98-6354b4a75425") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME)
            title_room_page.click_CreateNewTitle_btn()
            time.sleep(DELAY_TIME)
            title_designer_page.set_check_border(1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.16.0_TitleDesignerBorderBlurDefault.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.16.0_TitleDesignerBorderBlurDefault.png',
                                                    image_result)
            case.result = compare_result

        # title designer border blur slider max
        with uuid("8eb552a2-9a3c-432c-b6b8-72a8aafc01b9") as case:
            with uuid("f07e2181-b273-4b65-b230-d58080e7164b") as case:
                title_designer_page.drag_border_blur_slider(20, 0)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.16.1_TitleDesignerBorderBlurSlider.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.16.1_TitleDesignerBorderBlurSlider.png',
                                                        image_result)
                case.result = compare_result

        # title designer border blur input min
        with uuid("7866be43-2948-4603-8a05-b68d06b1d048") as case:
            with uuid("91ef962a-d410-4eb0-a484-604a738ab0eb") as case:
                title_designer_page.input_border_blur_value('0', 0)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.16.2_TitleDesignerBorderBlurInput.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.16.2_TitleDesignerBorderBlurInput.png',
                                                        image_result)
                case.result = compare_result

        # title designer border blur arrow
        with uuid("0613691d-d8c4-41ab-8785-50f0e923bd67") as case:
            title_designer_page.click_border_blur_arrow_btn(0, 0)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.16.3_TitleDesignerBorderBlurArrow.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.16.3_TitleDesignerBorderBlurArrow.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_17(self):
        # title designer border opacity default
        with uuid("d0f8b767-3f80-4899-a06d-361d813f82e5") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME)
            title_room_page.click_CreateNewTitle_btn()
            time.sleep(DELAY_TIME)
            title_designer_page.set_check_border(1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.17.0_TitleDesignerBorderOpacityDefault.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.17.0_TitleDesignerBorderOpacityDefault.png',
                                                    image_result)
            case.result = compare_result

        # title designer border opacity slider min
        with uuid("1443c97f-6d47-4c11-9a16-e3c569de3041") as case:
            with uuid("cf35a65f-761a-4736-8706-0f8fd8ccc52a") as case:
                title_designer_page.drag_border_opacity_slider(0, 0)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.17.1_TitleDesignerBorderOpacitySlider.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.17.1_TitleDesignerBorderOpacitySlider.png',
                                                        image_result)
                case.result = compare_result

        # title designer border opacity input max
        with uuid("042fdea5-36fc-4fbf-8a46-25eb83c1f383") as case:
            with uuid("c2a568fa-1446-4627-826d-021753050811") as case:
                title_designer_page.input_border_opacity_value('1000', 0)
                time.sleep(DELAY_TIME * 4)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.17.2_TitleDesignerBorderOpacityInput.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.17.2_TitleDesignerBorderOpacityInput.png',
                                                        image_result)
                case.result = compare_result

        # title designer border opacity arrow
        with uuid("c1155447-3c75-464d-aba6-b6334511f241") as case:
            title_designer_page.click_border_opacity_value_arrow_btn(1, 0)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.17.3_TitleDesignerBorderOpacityArrow.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.17.3_TitleDesignerBorderOpacityArrow.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_18(self):
        # title designer animation tab in animation effect category
        with uuid("9250be89-8dce-43c8-93c3-62137191415b") as case:
            with uuid("84e86589-26d6-4541-9892-def9ef81974b") as case:
                time.sleep(DELAY_TIME * 4)
                main_page.enter_room(1)
                time.sleep(DELAY_TIME)
                title_room_page.click_CreateNewTitle_btn()
                time.sleep(DELAY_TIME)
                title_designer_page.switch_mode(2)
                title_designer_page.click_animation_tab()
                title_designer_page.unfold_animation_in_animation_tab()
                title_designer_page.select_animation_in_animation_effect(2,2)
                time.sleep(DELAY_TIME * 4)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.18.0_TitleDesignerAnimationTabInAnimationEffectCategory.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.18.0_TitleDesignerAnimationTabInAnimationEffectCategory.png',
                                                        image_result)
                case.result = compare_result

        # title designer animation tab out animation effect category and effect
        with uuid("f17cbb2c-e569-48dc-8d88-ad74c1f5ecd7") as case:
            with uuid("72f27f46-e325-4306-9902-c2b39e9cac86") as case:
                title_designer_page.unfold_animation_in_animation_tab(0)
                title_designer_page.unfold_animation_out_animation_tab()
                title_designer_page.select_animation_out_animation_effect(2,2)
                time.sleep(DELAY_TIME * 4)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.18.1_TitleDesignerAnimationTabOutAnimationEffectCategory.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.18.1_TitleDesignerAnimationTabOutAnimationEffectCategory.png',
                                                        image_result)
                case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_19(self):
        # title designer edit image chroma key enable
        with uuid("15068ba7-98ad-447c-81de-98b034f88d5a") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME)
            title_room_page.click_CreateNewTitle_btn()
            time.sleep(DELAY_TIME)
            title_designer_page.switch_mode(2)
            title_designer_page.click_insert_image_btn()
            title_designer_page.insert_image(Test_Material_Folder + '1.jpg')
            title_designer_page.apply_chromakey()
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.19.0_TitleDesignerEditImageChromaKeyEnable.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.19.0_TitleDesignerEditImageChromaKeyEnable.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image chroma key add new key
        with uuid("e94fcb7e-4402-48c8-bb2b-8f9380b1f064") as case:
            title_designer_page.click_chromakey_add_new_key()
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.19.1_TitleDesignerEditImageChromaKeyAddNewKey.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.19.1_TitleDesignerEditImageChromaKeyAddNewKey.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image chroma key delete key
        with uuid("106f5d12-7df5-41f7-ae3c-de9053b98174") as case:
            title_designer_page.click_chromakey_remove_btn(1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.19.2_TitleDesignerEditImageChromaKeyRemoveKey.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.19.2_TitleDesignerEditImageChromaKeyRemoveKey.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image chroma key default
        with uuid("8b73ab9d-a247-440f-b425-540c5d75d5e5") as case:
            with uuid("eee2f356-0938-490e-8de3-4e400c2fe972") as case:
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.19.3_TitleDesignerEditImageChromaKeyDefault.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.19.3_TitleDesignerEditImageChromaKeyDefault.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image chroma key color range input value min
        with uuid("9ed29e07-dc37-466b-96ee-2b465482c258") as case:
            with uuid("3fee999e-4f49-448a-a95e-e8624444c9d8") as case:
                title_designer_page.input_chromakey_color_range_value('0')
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.19.4_TitleDesignerEditImageChromaKeyColorRangeInputValue.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.19.4_TitleDesignerEditImageChromaKeyColorRangeInputValue.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image chroma key color range slider max
        with uuid("1b43c676-df96-4927-a779-e0b88f734e0c") as case:
            with uuid("4c1da2fb-a0bf-47f6-a3c0-cfb364bead11") as case:
                title_designer_page.drag_chromakey_color_range_slider('60')
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.19.5_TitleDesignerEditImageChromaKeyColorRangeSlider.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.19.5_TitleDesignerEditImageChromaKeyColorRangeSlider.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image chroma key color range arrow
        with uuid("d5d219b9-c467-4eca-8f5d-1cf5ca317f4c") as case:
            title_designer_page.click_chromakey_color_range_arrow_btn(1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.19.6_TitleDesignerEditImageChromaKeyColorRangeArrowDown.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.19.6_TitleDesignerEditImageChromaKeyColorRangeArrowDown.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image chroma key denoise input value min
        with uuid("e646d412-044f-4faa-b9ce-a854251ff508") as case:
            with uuid("f1aaaac7-52f3-4b8e-8c25-c6db68ca4e18") as case:
                title_designer_page.input_chromakey_denoise_value('0')
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.19.7_TitleDesignerEditImageChromaKeyDenoiseInputValue.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.19.7_TitleDesignerEditImageChromaKeyDenoiseInputValue.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image chroma key denoise slider max
        with uuid("434f2ae4-e66b-475a-b402-acf5510fbf5a") as case:
            with uuid("321f41f2-9e63-4a68-8ff5-d1600fb24517") as case:
                title_designer_page.drag_chromakey_denoise_slider('100')
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.19.8_TitleDesignerEditImageChromaKeyDenoiseSlider.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.19.8_TitleDesignerEditImageChromaKeyDenoiseSlider.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image chroma key color range arrow
        with uuid("00d11822-051a-42b9-b896-c5a8be13c505") as case:
            title_designer_page.click_chromakey_denoise_arrow_btn(1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.19.9_TitleDesignerEditImageChromaKeyDenoiseArrowDown.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.19.9_TitleDesignerEditImageChromaKeyDenoiseArrowDown.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image chroma key add two new key
        with uuid("43800d73-12c5-4849-95c5-8e95c52f16a6") as case:
            title_designer_page.click_chromakey_add_new_key()
            title_designer_page.drag_object_vertical_slider(0.5)
            title_designer_page.click_chromakey_add_new_key()
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.19.10_TitleDesignerEditImageChromaKeyAddTwoNewKey.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.19.10_TitleDesignerEditImageChromaKeyAddTwoNewKey.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_20(self):
        # title designer edit image border default disable
        with uuid("1315e5ee-3d45-4acb-b07c-decab9cd3936") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME)
            title_room_page.click_CreateNewTitle_btn()
            time.sleep(DELAY_TIME)
            title_designer_page.switch_mode(2)
            title_designer_page.click_insert_image_btn()
            title_designer_page.insert_image(Test_Material_Folder + '1.jpg')
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.20.0_TitleDesignerEditImageBorderDisable.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.20.0_TitleDesignerEditImageBorderDisable.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image border enable
        with uuid("05fbc6d8-0b0e-4777-8d60-c2d59389ab76") as case:
            title_designer_page.apply_border(1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.20.1_TitleDesignerEditImageBorderEnable.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.20.1_TitleDesignerEditImageBorderEnable.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image border default
        with uuid("fee47cd4-a82a-4a16-b3d0-bbe1c6c717ec") as case:
            with uuid("6ca10173-554b-433f-acdd-2aa473159282") as case:
                with uuid("9db239e9-65c0-49b3-b96a-a3e78017fcba") as case:
                    with uuid("15772436-a312-4e9c-83e3-95a10ef1486d") as case:
                        title_designer_page.apply_border_uniform_color('30','30','30',1)
                        image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                               file_name=Auto_Ground_Truth_Folder + 'G7.20.2_TitleDesignerEditImageBorderDefault.png')
                        compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.20.2_TitleDesignerEditImageBorderDefault.png',
                                                                image_result)
                        case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_21(self):
        # title designer edit image border size slider min
        with uuid("f77894d9-387d-44d0-bec8-f9741dfcfe47") as case:
            with uuid("c9b0a905-7cd6-417d-b6cc-b5f1bc86fa82") as case:
                time.sleep(DELAY_TIME * 4)
                main_page.enter_room(1)
                time.sleep(DELAY_TIME)
                title_room_page.click_CreateNewTitle_btn()
                time.sleep(DELAY_TIME)
                title_designer_page.switch_mode(2)
                title_designer_page.click_insert_image_btn()
                title_designer_page.insert_image(Test_Material_Folder + '1.jpg')
                title_designer_page.apply_border(1)
                title_designer_page.drag_border_size_slider(0,1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.21.0_TitleDesignerEditImageBorderSizeSlider.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.21.0_TitleDesignerEditImageBorderSizeSlider.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image border size input max
        with uuid("f77894d9-387d-44d0-bec8-f9741dfcfe47") as case:
            with uuid("c9b0a905-7cd6-417d-b6cc-b5f1bc86fa82") as case:
                title_designer_page.input_border_size_value('10',1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.21.1_TitleDesignerEditImageBorderSizeInput.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.21.1_TitleDesignerEditImageBorderSizeInput.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image border size arrow
        with uuid("674624f9-5768-45bc-b9f9-96293b0bca11") as case:
            title_designer_page.click_size_value_arrow_btn(1, 1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.21.2_TitleDesignerEditImageBorderSizeArrow.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.21.2_TitleDesignerEditImageBorderSizeArrow.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_22(self):
        # title designer edit image border blur slider max
        with uuid("c813dfc1-443b-4842-9d4b-ac306b968f5d") as case:
            with uuid("6e32e511-f782-4a93-a644-be3cb7ed9efc") as case:
                time.sleep(DELAY_TIME * 4)
                main_page.enter_room(1)
                time.sleep(DELAY_TIME)
                title_room_page.click_CreateNewTitle_btn()
                time.sleep(DELAY_TIME)
                title_designer_page.switch_mode(2)
                title_designer_page.click_insert_image_btn()
                title_designer_page.insert_image(Test_Material_Folder + '1.jpg')
                title_designer_page.apply_border(1)
                title_designer_page.drag_border_blur_slider(20,1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.22.0_TitleDesignerEditImageBorderBlurSlider.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.22.0_TitleDesignerEditImageBorderBlurSlider.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image border blur input min
        with uuid("8eb8597d-fcd4-4b7d-83f5-4f3408f59a57") as case:
            with uuid("d7217e87-f44f-438a-806c-8936e38a2330") as case:
                title_designer_page.input_border_blur_value('0',1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.22.1_TitleDesignerEditImageBorderBlurInput.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.22.1_TitleDesignerEditImageBorderBlurInput.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image border blur arrow
        with uuid("9f68e339-cca3-414a-94f0-c84ac3d303c8") as case:
            title_designer_page.click_border_blur_arrow_btn(0, 1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.22.2_TitleDesignerEditImageBorderBlurArrow.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.22.2_TitleDesignerEditImageBorderBlurArrow.png',
                                                    image_result)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_23(self):
        # title designer edit image border opacity slider min
        with uuid("20c393e6-d130-42a2-841a-ee232eae4c55") as case:
            with uuid("a89d85ed-786a-4eff-8a98-6d46750ba59b") as case:
                time.sleep(DELAY_TIME * 4)
                main_page.enter_room(1)
                time.sleep(DELAY_TIME)
                title_room_page.click_CreateNewTitle_btn()
                time.sleep(DELAY_TIME)
                title_designer_page.switch_mode(2)
                title_designer_page.click_insert_image_btn()
                title_designer_page.insert_image(Test_Material_Folder + '1.jpg')
                title_designer_page.apply_border(1)
                title_designer_page.drag_border_opacity_slider(0,1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.23.0_TitleDesignerEditImageBorderOpacitySlider.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.23.0_TitleDesignerEditImageBorderOpacitySlider.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image border blur input max
        with uuid("1f81fc99-f934-403f-a0e0-31d1528a5a78") as case:
            with uuid("bfc54efb-86c1-4ec3-be6e-71482edc71ca") as case:
                title_designer_page.input_border_opacity_value('1000',1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.23.1_TitleDesignerEditImageBorderOpacityInput.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.23.1_TitleDesignerEditImageBorderOpacityInput.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image border blur arrow
        with uuid("96831de3-0982-4dd8-b32a-04946f4a05cc") as case:
            title_designer_page.click_border_opacity_value_arrow_btn(1, 1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.23.2_TitleDesignerEditImageBorderOpacityArrow.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.23.2_TitleDesignerEditImageBorderOpacityArrow.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image border 2 color
        with uuid("6bf67a0e-f9d6-4fd4-82ea-894766af6cf4") as case:
            title_designer_page.apply_border_2_color('120','150','80','30','200','180', 1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.23.3_TitleDesignerEditImageBorder2Color.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.23.3_TitleDesignerEditImageBorder2Color.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image border 4 color
        with uuid("2ca37c97-70d0-4046-83e7-935762788bbe") as case:
            title_designer_page.apply_border_4_color('120','150','80','30','200','180','20','50','90','220','0','0', 1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.23.4_TitleDesignerEditImageBorder4Color.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.23.4_TitleDesignerEditImageBorder4Color.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_24(self):
        # title designer edit image shadow default untick
        with uuid("94e96018-9083-436d-849d-45243b076b6b") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME)
            title_room_page.click_CreateNewTitle_btn()
            time.sleep(DELAY_TIME)
            title_designer_page.switch_mode(2)
            title_designer_page.click_insert_image_btn()
            title_designer_page.insert_image(Test_Material_Folder + '1.jpg')
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.24.0_TitleDesignerEditImageShadowDefaultUntick.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.24.0_TitleDesignerEditImageShadowDefaultUntick.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image shadow tick
        with uuid("7e8c23a1-5345-4f00-bf7f-00b21c359177") as case:
            title_designer_page.apply_shadow(1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.24.1_TitleDesignerEditImageShadowTick.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.24.1_TitleDesignerEditImageShadowTick.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image shadow apply shadow to object only
        with uuid("12aeeae4-dea9-427e-b61d-0354dd450e52") as case:
            title_designer_page.apply_shadow_to(4,1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.24.2_TitleDesignerEditImageShadowApplyShadowToObjectOnly.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.24.2_TitleDesignerEditImageShadowApplyShadowToObjectOnly.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image shadow default
        with uuid("0302ef8c-eb72-41e2-b569-df3392e0af0c") as case:
            with uuid("9158f525-ba2d-47cb-9e3e-d855f59a7a1c") as case:
                with uuid("1b33cdd5-487f-4d13-a7c2-e5c786277ffe") as case:
                    image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                           file_name=Auto_Ground_Truth_Folder + 'G7.24.3_TitleDesignerEditImageShadowDefault.png')
                    compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.24.3_TitleDesignerEditImageShadowDefault.png',
                                                            image_result)
                    case.result = compare_result

        # title designer edit image shadow apply shadow to border only
        with uuid("c3a61fbe-09c9-4db1-be56-e836a5f780b2") as case:
            title_designer_page.apply_shadow_to(2,1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.24.4_TitleDesignerEditImageShadowApplyShadowToBorderOnly.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.24.4_TitleDesignerEditImageShadowApplyShadowToBorderOnly.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image shadow apply shadow to object and border
        with uuid("29128ee7-7892-49fd-94d9-2ec5ff4d3a36") as case:
            title_designer_page.apply_shadow_to(3,1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.24.5_TitleDesignerEditImageShadowApplyShadowToObjectAndBorder.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.24.5_TitleDesignerEditImageShadowApplyShadowToObjectAndBorder.png',
                                                    image_result)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_25(self):
        # title designer edit image shadow distance slider max
        with uuid("c8719a1f-1aee-4edd-9903-dfd44257ec2a") as case:
            with uuid("e3f363a7-e20a-489e-a1c9-b148a2fbf8b3") as case:
                time.sleep(DELAY_TIME * 4)
                main_page.enter_room(1)
                time.sleep(DELAY_TIME)
                title_room_page.click_CreateNewTitle_btn()
                time.sleep(DELAY_TIME)
                title_designer_page.switch_mode(2)
                title_designer_page.click_insert_image_btn()
                title_designer_page.insert_image(Test_Material_Folder + '1.jpg')
                title_designer_page.apply_shadow(1)
                title_designer_page.drag_shadow_distance_slider(100,1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.25.0_TitleDesignerEditImageShadowDistanceSlider.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.25.0_TitleDesignerEditImageShadowDistanceSlider.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image shadow distance value min
        with uuid("b196f538-bc1a-4c7c-a443-d5c3137fc758") as case:
            with uuid("ae4c8cdc-67e5-4760-89f8-7494dee8db5f") as case:
                title_designer_page.input_shadow_distance_value('0',1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.25.1_TitleDesignerEditImageShadowDistanceValue.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.25.1_TitleDesignerEditImageShadowDistanceValue.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image shadow distance arrow
        with uuid("f3b04fba-f0cd-4c6e-b101-0dafa6b2bdc7") as case:
            title_designer_page.click_shadow_distance_arrow_btn(0,1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.25.2_TitleDesignerEditImageShadowDistanceArrow.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.25.2_TitleDesignerEditImageShadowDistanceArrow.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_26(self):
        # title designer edit image shadow blur slider max
        with uuid("2e59d5ea-4b72-4b8d-8bb2-0a0b49a6461e") as case:
            with uuid("26ca3f6f-da31-4105-bb9c-9f396b346f24") as case:
                time.sleep(DELAY_TIME * 4)
                main_page.enter_room(1)
                time.sleep(DELAY_TIME)
                title_room_page.click_CreateNewTitle_btn()
                time.sleep(DELAY_TIME)
                title_designer_page.switch_mode(2)
                title_designer_page.click_insert_image_btn()
                title_designer_page.insert_image(Test_Material_Folder + '1.jpg')
                title_designer_page.apply_shadow(1)
                title_designer_page.drag_shadow_blur_slider(20,1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.26.0_TitleDesignerEditImageShadowBlurSlider.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.26.0_TitleDesignerEditImageShadowBlurSlider.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image shadow blur value min
        with uuid("2ecca4bb-d02a-4637-a840-55e9938c6bc4") as case:
            with uuid("28aadada-28f8-4871-b3d4-a85316842ae9") as case:
                title_designer_page.input_shadow_blur_value('0',1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.26.1_TitleDesignerEditImageShadowBlurValue.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.26.1_TitleDesignerEditImageShadowBlurValue.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image shadow blur arrow
        with uuid("2de2cdd4-7aad-4dec-acef-77f8aa48a5e7") as case:
            title_designer_page.click_shadow_blur_arrow_btn(0,1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.26.2_TitleDesignerEditImageShadowBlurArrow.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.26.2_TitleDesignerEditImageShadowBlurArrow.png',
                                                    image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_7_27(self):
        # title designer edit image shadow opacity slider min
        with uuid("6b2ef703-a348-4407-acff-57e2c0e55cbd") as case:
            with uuid("8f996ed1-fbc4-495c-9f3e-d6f3c6e8d128") as case:
                time.sleep(DELAY_TIME * 4)
                main_page.enter_room(1)
                time.sleep(DELAY_TIME)
                title_room_page.click_CreateNewTitle_btn()
                time.sleep(DELAY_TIME)
                title_designer_page.switch_mode(2)
                title_designer_page.click_insert_image_btn()
                title_designer_page.insert_image(Test_Material_Folder + '1.jpg')
                title_designer_page.apply_shadow(1)
                title_designer_page.drag_shadow_opacity_slider(0,1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.27.0_TitleDesignerEditImageShadowOpacitySlider.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.27.0_TitleDesignerEditImageShadowOpacitySlider.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image shadow opacity value max
        with uuid("b92e8b28-f754-4113-a28a-5edb8905d13e") as case:
            with uuid("d9d46bb5-98f9-4692-92bc-f40e16573865") as case:
                title_designer_page.input_shadow_opacity_value('1000',1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.27.1_TitleDesignerEditImageShadowOpacityValue.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.27.1_TitleDesignerEditImageShadowOpacityValue.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image shadow opacity arrow
        with uuid("f80f5fe6-e2ea-4f13-9f84-0d3826da796f") as case:
            title_designer_page.click_shadow_opacity_arrow_btn(1,1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.27.2_TitleDesignerEditImageShadowOpacityArrow.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.27.2_TitleDesignerEditImageShadowOpacityArrow.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image shadow shadow color
        with uuid("54ad7ff9-51b8-40b0-92de-546b7ef64c79") as case:
            title_designer_page.set_shadow_fill_shadow_color('80','120','150',1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.27.3_TitleDesignerEditImageShadowShadowColor.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.27.3_TitleDesignerEditImageShadowShadowColor.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image flip untick
        with uuid("74548a73-ae3f-4038-8c9f-f9b5e17c345a") as case:
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.27.4_TitleDesignerEditImageFlipUntick.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.27.4_TitleDesignerEditImageFlipUntick.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image flip tick upside down
        with uuid("30fcb9f3-0fe2-482f-9a7b-e3b1d5dcf167") as case:
            with uuid("41670ed4-1f1b-461d-b2fc-342eda4f3ca7") as case:
                title_designer_page.apply_flip(1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.27.5_TitleDesignerEditImageFlipUpsideDown.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.27.5_TitleDesignerEditImageFlipUpsideDown.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image flip left to right
        with uuid("b69d0128-3531-41e2-8b02-c53bbd9c550e") as case:
            title_designer_page.set_flip_apply_type(2)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.27.6_TitleDesignerEditImageFlipLeftToRight.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.27.6_TitleDesignerEditImageFlipLeftToRight.png',
                                                    image_result)
            case.result = compare_result

    @exception_screenshot
    def test1_1_7_28(self):
        # title designer edit image fade default
        with uuid("d8bf40c5-ab65-49f7-ac4e-86fc8c2ce4a5") as case:
            with uuid("3ffe5b48-9854-4dbe-9d2a-adea4fc783d3") as case:
                with uuid("4a00ddd1-3fd9-481a-a2a7-fbaba52091e0") as case:
                    time.sleep(DELAY_TIME * 4)
                    main_page.enter_room(1)
                    time.sleep(DELAY_TIME)
                    title_room_page.click_CreateNewTitle_btn()
                    time.sleep(DELAY_TIME)
                    title_designer_page.switch_mode(2)
                    title_designer_page.click_insert_image_btn()
                    title_designer_page.insert_image(Test_Material_Folder + '1.jpg')
                    image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                           file_name=Auto_Ground_Truth_Folder + 'G7.28.0_TitleDesignerEditImageFadeDefault.png')
                    compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.28.0_TitleDesignerEditImageFadeDefault.png',
                                                            image_result)
                    case.result = compare_result

        # title designer edit image fade untick
        with uuid("30fcb9f3-0fe2-482f-9a7b-e3b1d5dcf167") as case:
            title_designer_page.apply_fade(0)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.28.1_TitleDesignerEditImageFadeUntick.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.28.1_TitleDesignerEditImageFadeUntick.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image fade in untick
        with uuid("8474f6aa-88d3-436c-acdf-052b82cea766") as case:
            title_designer_page.apply_fade(1)
            title_designer_page.set_fade_enable_fade_in(0)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.28.2_TitleDesignerEditImageFadeInUntick.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.28.2_TitleDesignerEditImageFadeInUntick.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image fade out untick
        with uuid("c12f32d4-c0b8-47f2-92b0-5af3f36244b8") as case:
            title_designer_page.set_fade_enable_fade_out(0)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.28.3_TitleDesignerEditImageFadeOutUntick.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.28.3_TitleDesignerEditImageFadeOutUntick.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image object settings X arrow
        with uuid("27845199-567d-4c99-90ce-e5acbd3fc3f1") as case:
            with uuid("27845199-567d-4c99-90ce-e5acbd3fc3f1") as case:
                title_designer_page.click_object_setting_x_position_arrow_btn(0)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.28.4_TitleDesignerEditImageObjectSettingsXArrow.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.28.4_TitleDesignerEditImageObjectSettingsXArrow.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image object settings X input min
        with uuid("28304c92-05d7-4736-823c-77614f8cbe02") as case:
            with uuid("54404160-d82e-4c4d-b197-3df780d71116") as case:
                title_designer_page.input_object_setting_x_position_value('-2',1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.28.5_TitleDesignerEditImageObjectSettingsXInput.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.28.5_TitleDesignerEditImageObjectSettingsXInput.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image object settings Y input max
        with uuid("d35b78a7-aa11-46a1-94b6-210db1987efd") as case:
            with uuid("bf1ae484-c8fe-4fa2-84f3-7e46ec7f5dc5") as case:
                title_designer_page.input_object_setting_y_position_value('2',1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.28.6_TitleDesignerEditImageObjectSettingsYInput.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.28.6_TitleDesignerEditImageObjectSettingsYInput.png',
                                                        image_result)
                case.result = compare_result

        # title designer edit image object settings default
        with uuid("4df469f6-5373-4fc4-b718-98ed36b50c89") as case:
            with uuid("f6f44868-0af0-49dd-a166-70bf27d1867e") as case:
                with uuid("20989034-780b-4e3a-a0c2-d4602ee16951") as case:
                    title_designer_page.input_object_setting_x_position_value('0', 1)
                    title_designer_page.input_object_setting_y_position_value('0', 1)
                    image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                           file_name=Auto_Ground_Truth_Folder + 'G7.28.7_TitleDesignerEditImageObjectSettingsDefault.png')
                    compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.28.7_TitleDesignerEditImageObjectSettingsDefault.png',
                                                            image_result)
                    case.result = compare_result

    @exception_screenshot
    def test1_1_7_29(self):
        # title designer edit image object settings scale width input max
        with uuid("605682ed-9c37-4f40-be50-2f9cb9602409") as case:
            with uuid("642b1ac0-af2b-4163-8a27-ce1312a82e13") as case:
                with uuid("62d4a824-fa77-4b05-9af1-8975697be609") as case:
                    time.sleep(DELAY_TIME * 4)
                    main_page.enter_room(1)
                    time.sleep(DELAY_TIME)
                    title_room_page.click_CreateNewTitle_btn()
                    time.sleep(DELAY_TIME)
                    title_designer_page.switch_mode(2)
                    title_designer_page.click_insert_image_btn()
                    title_designer_page.insert_image(Test_Material_Folder + '1.jpg')
                    title_designer_page.input_object_setting_scale_width_value('10',1)
                    image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                           file_name=Auto_Ground_Truth_Folder + 'G7.29.0_TitleDesignerEditImageObjectSettingsScaleWidthInput.png')
                    compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.29.0_TitleDesignerEditImageObjectSettingsScaleWidthInput.png',
                                                            image_result)
                    case.result = compare_result

        # title designer edit image object settings scale height arrow maintain aspect ratio untick
        with uuid("68dd9337-9afb-4e52-9af8-7aa744217731") as case:
            with uuid("a3c08b66-c9f8-449a-b1e2-7ad8e3fed9a2") as case:
                with uuid("345ef3b3-4d96-4a4f-a44e-8f564eb9bb0d") as case:
                    title_designer_page.set_check_object_setting_scale_maintain_aspect_ratio(0)
                    title_designer_page.click_object_setting_scale_height_arrow_btn(1)
                    image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                           file_name=Auto_Ground_Truth_Folder + 'G7.29.1_TitleDesignerEditImageObjectSettingsScaleHeightArrow.png')
                    compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.29.1_TitleDesignerEditImageObjectSettingsScaleHeightArrow.png',
                                                            image_result)
                    case.result = compare_result

        # title designer edit image object settings scale width min
        with uuid("2732a28e-5da1-4e82-873a-7f51f136a51e") as case:
            title_designer_page.set_check_object_setting_scale_maintain_aspect_ratio(1)
            title_designer_page.input_object_setting_scale_width_value('0.2',1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.29.2_TitleDesignerEditImageObjectSettingsScaleWidthMin.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.29.2_TitleDesignerEditImageObjectSettingsScaleWidthMin.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image object settings opacity slider min
        with uuid("596a5f7f-a68c-4f8c-a394-9849216cd148") as case:
            with uuid("fc1a5769-4ded-4733-ad4e-779b81e3241c") as case:
                title_designer_page.drag_object_setting_opacity_slider(0)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.29.3_TitleDesignerEditImageObjectSettingsOpacitySliderMin.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.29.3_TitleDesignerEditImageObjectSettingsOpacitySliderMin.png',
                                                         image_result)
                case.result = compare_result

        # title designer edit image object settings opacity input max
        with uuid("e65d9928-ae92-4303-b78a-1a90cabd4697") as case:
            with uuid("ee8b3056-9ef1-449c-8426-adedb38bdd5d") as case:
                title_designer_page.input_object_setting_opacity_value('1000',1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.29.4_TitleDesignerEditImageObjectSettingsOpacityInputMax.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.29.4_TitleDesignerEditImageObjectSettingsOpacityInputMax.png',
                                                         image_result)
                case.result = compare_result

        # title designer edit image object settings opacity arrow
        with uuid("bdca4274-7850-42d5-9451-a440e3a23f23") as case:
            title_designer_page.click_object_setting_opacity_arrow_btn(1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.29.5_TitleDesignerEditImageObjectSettingsOpacityArrow.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.29.5_TitleDesignerEditImageObjectSettingsOpacityArrow.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image object settings rotation input max
        with uuid("62b6f923-47cf-41d2-9685-9d7243140365") as case:
            with uuid("1f299783-b157-4ec4-bd65-c7afa930ba16") as case:
                title_designer_page.input_object_setting_rotation_value('9999',1)
                image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                       file_name=Auto_Ground_Truth_Folder + 'G7.29.6_TitleDesignerEditImageObjectSettingsRotationInputMax.png')
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.29.6_TitleDesignerEditImageObjectSettingsRotationInputMax.png',
                                                         image_result)
                case.result = compare_result

        # title designer edit image object settings rotation arrow
        with uuid("cae7a5a0-54cd-4032-8b48-8c5371df72aa") as case:
            title_designer_page.click_object_setting_rotation_arrow_btn(1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.29.7_TitleDesignerEditImageObjectSettingsRotationArrow.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.29.7_TitleDesignerEditImageObjectSettingsRotationArrow.png',
                                                    image_result)
            case.result = compare_result

        # title designer edit image object settings rotation input min
        with uuid("fe54d5ba-2825-495a-8bea-9fb13ed8fdcc") as case:
            title_designer_page.input_object_setting_rotation_value('-9999',1)
            image_result = tips_area_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                   file_name=Auto_Ground_Truth_Folder + 'G7.29.8_TitleDesignerEditImageObjectSettingsRotationInputMin.png')
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G7.29.8_TitleDesignerEditImageObjectSettingsRotationInputMin.png',
                                                    image_result)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    f07b4488-adce-4d03-b061-f068a0448d67
                    d1ffe741-4ded-4c4d-9cfa-560d6a110c2a
                    0523149d-bcc6-4c92-84c5-b82e34f4f81e
                    7c2baa6c-0681-4f0b-9035-37898dee2f3d
                    adddd7f9-afe4-4430-aac8-49dd794cd443
                    41cb99bf-5a0e-424b-bef8-afb8cbfcf5e2
                    5f3ec935-214d-4f39-8638-e8b5d380d5bd
                    07cf9ea0-f43d-4a79-a017-01cefde197c7
                    6e34c34b-0679-47a5-acb7-9da2b7ccd870
                    41396e90-8149-4634-9ea8-069d2f4bea15
                    38b09950-5e49-4c7e-a097-c357bfdbb4c4
                    57894f24-2ab2-4bf6-a2ba-2087015eeb5f
                    ff5f47d7-7db8-4d86-8eb2-68621fc27f7b
                    879024d8-1662-47ff-9b68-1c27e92ae9e4
                    3abdc9b7-b472-4c72-af02-f42aa35e1e2d
                    659e6324-d7f4-4423-af42-2a48c08d2abb
                    c4b39d75-ab0d-4b6d-9d4a-1ce550507af3
                    62b6f923-47cf-41d2-9685-9d7243140365
                    cae7a5a0-54cd-4032-8b48-8c5371df72aa
                    fe54d5ba-2825-495a-8bea-9fb13ed8fdcc
                    1f299783-b157-4ec4-bd65-c7afa930ba16
                    6a851bf5-f45c-43e4-a0c6-06dbf921f91f
                    a371feb5-f11e-43f1-a992-568ecb7c4d41
                    710f2d67-bd7c-400e-8064-f035bad876d5
                    483ddd2d-3da1-4d42-a2eb-1e72f9a58cad
                    bce9b67b-ae86-4867-aa3d-118028981924
                    402e96fa-96c7-4cc4-9d70-8dd63f8a5725
                    06cbf136-dc28-4859-980d-6ae0e2bdcc2d
                    6be5af4f-3811-4e0e-bc46-b8e852690c97
                    0dde6326-7e0a-404a-83f7-a4d218066d5d
                    62138efd-6d13-424f-b543-d968d725c21f
                    37629f67-aad6-4d0b-9bb9-72b7fc61c537
                    0993defb-6995-4c69-8dd2-2a9688bcc83a
                    d8a324a6-fe9c-4457-9863-8e2bca828d11
                    8ccafdaa-3fa8-43fd-8278-1acf5287b713
                    04735055-c071-4bdb-a34e-5384a08d5cbc
                    23d38bfb-9fdb-4acc-b531-f4f9e08cdd94
                    870d0432-afc1-4d72-b493-511da036ced5
                    9608baf8-7540-4f48-aaf2-69ac3de5f668
                    54fa0377-262c-4928-9fa3-f65ecc7a2191
                    bffcc08c-9d0c-4c5e-90de-daa33ef573bc
                    87fdb3f6-2be8-4177-ac2f-4eb7e13a6d3d
                    6e5dc0da-ce9c-4344-91d0-6763e4106f08
                    80c1417c-d866-412f-adb5-67e447716298
                    1bd1be17-d481-45fb-ae43-cf2ec50112c5
                    065c931e-15da-4ce3-a772-53024acd10d7
                    8755ce38-6519-4edf-afaf-16f3f8ae56ed
                    13db729b-7945-4131-9238-764985e77f5b
                    6e4984c6-a187-44d8-b7ab-e75654520d80
                    97116791-b019-4afc-93db-a15f1ded9a9d
                    6695ce05-9f18-412b-beda-55a87da0a776
                    5bae1dc4-0c6c-48df-9a6e-a16ba7042ce5
                    cea4edf4-b890-4d80-b622-7183e659a4fe
                    8e81d0c5-56a3-415d-bd32-9eb0ddc7306b
                    c63223cd-ecd0-4cf3-b977-cc74459513f2
                    5959ada2-46b1-4e4d-8052-e2618947c3e4
                    792e9682-3775-4ba6-8569-0df48a3ad6dd
                    508d580f-21b1-4540-8316-9baa790ed8e5
                    325efb3f-0be1-457f-a8a1-306a58e36cab
                    23fd5849-ba25-4f3c-b5e7-1e05d3b6d649
                    43e29596-cf2a-47f9-9478-6aaabe3b63be
                    6f0c9cc6-24c0-431d-8899-eae7c3c46f89
                    cd743115-d736-4095-a181-5db429bced43
                    e8209410-1de8-4612-ba4b-2159a80634e5
                    7709329c-ea11-4785-8309-00c3141b003c
                    188391f2-b9b6-4249-ad18-8f81b8dc4b3c
                    30585fa1-50b0-4c6e-bda5-dcb2696d11d9
                    2a0f104c-ffe2-46c7-bb53-ec21934a777c
                    cd9e3821-aa44-4c68-a499-8043530bad4b
                    b36cf589-f062-4048-b23d-b08d62249c3d
                    b13b85dc-fa74-4db8-9947-6fc478468a91
                    f9204087-afff-48ba-bbd5-db8188673b84
                    522c4708-67c8-420b-a2e7-08d39379ad08
                    36845d4a-01bc-4d0e-9e3f-e58809a36e72
                    c193a7b4-22cf-4bac-88af-bbe6751d9ede
                    ad213c50-a2b7-49c7-ae27-f553340f20d7
                    aebebd43-fa65-4312-9889-e1f2a759a55c
                    d8e7f0b6-9d5b-4184-82b8-7cf35c1c60b0
                    b3ad3c3e-cbe4-4aa1-ae42-92d3c305138c
                    46c3c22d-9705-4969-9857-e2652234da52
                    6e7c559d-db23-4cd2-a793-2540dd866f1d
                    cab9ca79-4a01-4475-ab34-57322fda2732
                    c2e0f5be-0624-4a21-aebe-d347dbd6ec3a
                    91762335-9ea7-4527-9b70-d0b6c47fc87f
                    350d2001-6bd1-4a05-bbf8-1eed5b65af6c
                    2387aa3c-a940-410f-8941-591ec8060019
                    1e4a48e5-bbe5-40c5-ab30-c8ee9d89d48e
                    6e57b614-576b-445f-9df7-75fde85e6209
                    fae2735e-8600-46d8-b324-83d30f66597b
                    ecf0d309-1116-4205-a789-66b2a1e10204
                    d3a51e98-35fd-4bf1-b07b-03697a4752a1
                    fc4e4a00-3598-4e97-ba59-b554e0b36535
                    aa291a02-6406-4f77-81b8-b9423b7a923d
                ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"


