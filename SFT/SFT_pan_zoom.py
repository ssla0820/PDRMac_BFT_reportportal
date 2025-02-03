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
transition_room_page = PageFactory().get_page_object('trainsition_room_page', mac)
playback_window_page = PageFactory().get_page_object('playback_window_page', mac)
preferences_page = PageFactory().get_page_object('preferences_page', mac)
pan_zoom_page = PageFactory().get_page_object('pan_zoom_page', mac)
tips_area_page = PageFactory().get_page_object('tips_area_page', mac)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Pan & Zoom.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<


# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/pan_zoom/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/pan_zoom/'
Test_Material_Folder = app.testing_material

#Ground_Truth_Folder = '/Users/cl/Desktop/Ernesto_MacAT_M3/SFT/ground_truth/pan_zoom/'
#Auto_Ground_Truth_Folder = '/Users/cl/Desktop/Ernesto_MacAT_M3/SFT/auto_ground_truth/pan_zoom/'
#Test_Material_Folder = '/Users/cl/Desktop/Ernesto_MacAT/Material/'

DELAY_TIME = 1


class Test_Pan_Zoom():
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
            google_sheet_execution_log_init('Pan_Zoom')

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
        # Tools -> Pan & Zoom
        with uuid("c3792d76-1d6b-48e8-81fe-1f34be5cbf38") as case:
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            time.sleep(DELAY_TIME * 4)
            case.result = pan_zoom_page.is_enter_pan_zoom()

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_2(self):
        # More Features -> Edit Image -> Pan & Zoom
        with uuid("73bf2a7a-b011-448b-990c-d17cd594edf1") as case:
            main_page.insert_media("Food.jpg")
            tips_area_page.more_features.edit_image_PanZoom()
            time.sleep(DELAY_TIME * 4)
            case.result = pan_zoom_page.is_enter_pan_zoom()

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_3(self):
        # Right click menu -> Edit Image -> Pan & Zoom
        with uuid("9c181b70-8d9b-4bd5-a8d4-7af375485c78") as case:
            main_page.insert_media("Food.jpg")
            timeline_operation_page.select_timeline_media(0,0)
            timeline_operation_page.right_click()
            timeline_operation_page.select_right_click_menu('Edit Image')
            timeline_operation_page.select_right_click_menu('Pan & Zoom')
            time.sleep(DELAY_TIME * 4)
            case.result = pan_zoom_page.is_enter_pan_zoom()

        # motion designer disable
        with uuid("314d1eb3-95b4-4f68-9f45-953d5e39d775") as case:
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.btn_motion_designer,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.1_Motion_Designer_Button.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.3.1_Motion_Designer_Button.png', preview_result)
            case.result = image_result

        # click i button
        with uuid("b4e31200-e9a6-499b-9423-273863b23389") as case:
            case.result = pan_zoom_page.click_i_button()

        # select a style
        with uuid("c14afca8-b756-4bf6-b75e-9ca0032ff5b3") as case:
            with uuid("c38e1ffe-d31d-4e7f-b307-97f6fad4c92c") as case:
                pan_zoom_page.apply_motion_style(4)
                if pan_zoom_page.get_applied_style_name() == 'Vertical Down':
                    result = True
                else:
                    result = False
                preview_result = pan_zoom_page.snapshot(locator=L.playback_window.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.3.3_Apply_Style.png')
                image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.3.3_Apply_Style.png',
                                                     preview_result)
                case.result = image_result and result

        # change style
        with uuid("97ea7a60-8cb7-42fd-af6b-11e48bc55d15") as case:
            pan_zoom_page.apply_motion_style(5)
            preview_result = pan_zoom_page.snapshot(locator=L.playback_window.main,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.4_Change_Style.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.3.4_Change_Style.png',
                                                 preview_result)
            case.result = image_result

        # reset style
        with uuid("0c2daf3b-67ec-4f39-8941-7fa4d13a6626") as case:
            pan_zoom_page.click_reset()
            preview_result = pan_zoom_page.snapshot(locator=L.playback_window.main,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.3.5_Reset_Style.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.3.5_Reset_Style.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_4(self):
        # Apply to All
        with uuid("9a562409-e6c1-499e-9c82-b35b7f37b44c") as case:
            main_page.insert_media("Food.jpg")
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            tips_area_page.click_TipsArea_btn_insert(1)
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            time.sleep(DELAY_TIME * 4)
            pan_zoom_page.apply_motion_style(6)
            pan_zoom_page.click_apply_to_all()
            preview_result = pan_zoom_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.4.0_Apply_To_All.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.4.0_Apply_To_All.png',preview_result, similarity=0.9)
            case.result = image_result

        # close
        with uuid("5a60fe5b-6c46-4c7a-a4b6-c36d2a086807") as case:
            pan_zoom_page.click_close()
            preview_result = pan_zoom_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.4.1_Close.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.4.1_Close.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_5(self):
        # Click User Define
        with uuid("065f4d03-cf9a-45fd-b3fb-09daca2e1c84") as case:
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            time.sleep(DELAY_TIME * 4)
            case.result = pan_zoom_page.apply_user_defined_style()

        # Motion Designer caption
        with uuid("a93e8bf4-aa79-4d9d-b95c-9742bc274f3e") as case:
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.5.1_Motion_Designer_Caption.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.5.1_Motion_Designer_Caption.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer maximize
        with uuid("18c84b49-e27e-45a4-930c-cd59ac88ece7") as case:
            pan_zoom_page.magic_motion_designer.click_maximize()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.5.2_Motion_Designer_Maximize.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.5.2_Motion_Designer_Maximize.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer restore down
        with uuid("c433d528-d843-4cf8-a5a4-7cbc6f5ba358") as case:
            pan_zoom_page.magic_motion_designer.click_maximize()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.5.3_Motion_Designer_Restore_Down.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.5.3_Motion_Designer_Restore_Down.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer close
        with uuid("73aaebb0-c15e-4eab-8478-77511c4c16b0") as case:
            pan_zoom_page.magic_motion_designer.click_close()
            case.result = not pan_zoom_page.magic_motion_designer.is_enter()

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_6(self):
        # Motion Designer button
        with uuid("32de8186-1580-4bcc-85b2-da1f079b286c") as case:
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            time.sleep(DELAY_TIME * 4)
            pan_zoom_page.apply_motion_style(7)
            pan_zoom_page.click_motion_designer()
            time.sleep(DELAY_TIME * 3)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.6.0_Motion_Designer.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.6.0_Motion_Designer.png',
                                                 preview_result)
            case.result = image_result

        # play
        with uuid("192d23bd-d87b-43a2-8774-b2d1eaede9c6") as case:
            pan_zoom_page.magic_motion_designer.preview_operation.click_play()
            case.result = True

        # stop
        with uuid("55ecdc40-e45e-4a5a-8864-2e76904fb8d3") as case:
            pan_zoom_page.magic_motion_designer.preview_operation.click_stop()
            case.result = True

        # next frame
        with uuid("3c8ee77c-f3bb-4990-9b35-bb43f217dec7") as case:
            pan_zoom_page.magic_motion_designer.preview_operation.click_go_to_next_frame()
            case.result = True

        # previous frame
        with uuid("57efa29a-3e8d-4200-b4f0-e44d27110dfa") as case:
            pan_zoom_page.magic_motion_designer.preview_operation.click_go_to_previous_frame()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.6.4_Motion_Designer_Preview_Operation.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.6.4_Motion_Designer_Preview_Operation.png',
                                                 preview_result)
            case.result = image_result

        # snap ref line
        with uuid("61386b83-739d-4c16-beda-f10dd00a94c3") as case:
            result1 = pan_zoom_page.magic_motion_designer.apply_snap_ref_line(0)
            result2 = pan_zoom_page.magic_motion_designer.apply_snap_ref_line(1)
            case.result = result1 and result2

        # grid line 10
        with uuid("11d376fc-7e2a-4594-abf4-5967409bd01a") as case:
            pan_zoom_page.magic_motion_designer.select_grid_lines_format(10)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.6.6_Motion_Designer_Grid_Line_10.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.6.6_Motion_Designer_Grid_Line_10.png',
                                                 preview_result)
            case.result = image_result

        # grid line 9
        with uuid("52521031-27e0-41ec-8f29-3ff856957761") as case:
            pan_zoom_page.magic_motion_designer.select_grid_lines_format(9)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.6.7_Motion_Designer_Grid_Line_9.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.6.7_Motion_Designer_Grid_Line_9.png',
                                                 preview_result)
            case.result = image_result

        # grid line 8
        with uuid("2e445095-4fa4-4144-a310-98a21fbfb04a") as case:
            pan_zoom_page.magic_motion_designer.select_grid_lines_format(8)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.6.8_Motion_Designer_Grid_Line_8.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.6.8_Motion_Designer_Grid_Line_8.png',
                                                 preview_result)
            case.result = image_result

        # grid line 7
        with uuid("0529176d-faea-429c-9a42-ded8f9b3acfa") as case:
            pan_zoom_page.magic_motion_designer.select_grid_lines_format(7)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.6.9_Motion_Designer_Grid_Line_7.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.6.9_Motion_Designer_Grid_Line_7.png',
                                                 preview_result)
            case.result = image_result

        # grid line 6
        with uuid("50d33f2e-ffdd-4cbd-8195-e06acd7e10c5") as case:
            pan_zoom_page.magic_motion_designer.select_grid_lines_format(6)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.6.10_Motion_Designer_Grid_Line_6.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.6.10_Motion_Designer_Grid_Line_6.png',
                                                 preview_result)
            case.result = image_result

        # grid line 5
        with uuid("44c38e20-d924-4aef-b60b-c3cb04c7e0cc") as case:
            pan_zoom_page.magic_motion_designer.select_grid_lines_format(5)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.6.11_Motion_Designer_Grid_Line_5.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.6.11_Motion_Designer_Grid_Line_5.png',
                                                 preview_result)
            case.result = image_result

        # grid line 4
        with uuid("6239c8b2-bc45-44ca-9990-1df4806ed11c") as case:
            pan_zoom_page.magic_motion_designer.select_grid_lines_format(4)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.6.12_Motion_Designer_Grid_Line_4.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.6.12_Motion_Designer_Grid_Line_4.png',
                                                 preview_result)
            case.result = image_result

        # grid line 3
        with uuid("15f3502e-d314-4cb0-bd35-709880870a0c") as case:
            pan_zoom_page.magic_motion_designer.select_grid_lines_format(3)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.6.13_Motion_Designer_Grid_Line_3.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.6.13_Motion_Designer_Grid_Line_3.png',
                                                 preview_result)
            case.result = image_result

        # grid line 2
        with uuid("bd8e9490-b571-49b6-ac74-0070e2acf696") as case:
            pan_zoom_page.magic_motion_designer.select_grid_lines_format(2)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.6.14_Motion_Designer_Grid_Line_2.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.6.14_Motion_Designer_Grid_Line_2.png',
                                                 preview_result)
            case.result = image_result

        # grid line None
        with uuid("b52993e8-b272-4722-9f68-282cbc01b9de") as case:
            pan_zoom_page.magic_motion_designer.select_grid_lines_format(1)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.6.15_Motion_Designer_Grid_Line_None.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.6.15_Motion_Designer_Grid_Line_None.png',
                                                 preview_result)
            case.result = image_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_7(self):
        # Motion Designer viewer 1600%
        with uuid("3aee2ee3-9f5f-4d71-9c51-da6fcddac190") as case:
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            time.sleep(DELAY_TIME * 4)
            pan_zoom_page.apply_motion_style(7)
            pan_zoom_page.click_motion_designer()
            time.sleep(DELAY_TIME * 2)
            pan_zoom_page.magic_motion_designer.select_viewer_zoom("1600%")
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.7.0_Motion_Designer_Viewer_Zoom_1600.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.7.0_Motion_Designer_Viewer_Zoom_1600.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer viewer 800%
        with uuid("03030535-8958-4f86-b3d7-f593e8f94791") as case:
            pan_zoom_page.magic_motion_designer.select_viewer_zoom("800%")
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.7.1_Motion_Designer_Viewer_Zoom_800.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.7.1_Motion_Designer_Viewer_Zoom_800.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer viewer 400%
        with uuid("e52dfb30-f026-4303-a5b7-bd9c2d2f8bdd") as case:
            pan_zoom_page.magic_motion_designer.select_viewer_zoom("400%")
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.7.2_Motion_Designer_Viewer_Zoom_400.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.7.2_Motion_Designer_Viewer_Zoom_400.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer viewer 300%
        with uuid("3680356e-b2f8-4fc8-8eb5-d1a1ab70d6f8") as case:
            pan_zoom_page.magic_motion_designer.select_viewer_zoom("300%")
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.7.3_Motion_Designer_Viewer_Zoom_300.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.7.3_Motion_Designer_Viewer_Zoom_300.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer viewer 200%
        with uuid("157919b3-bfa6-4210-9605-575a37d76812") as case:
            pan_zoom_page.magic_motion_designer.select_viewer_zoom("200%")
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.7.4_Motion_Designer_Viewer_Zoom_200.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.7.4_Motion_Designer_Viewer_Zoom_200.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer viewer 100%
        with uuid("a964f15e-8a48-4226-9f91-afe690cec0b4") as case:
            pan_zoom_page.magic_motion_designer.select_viewer_zoom("100%")
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.7.5_Motion_Designer_Viewer_Zoom_100.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.7.5_Motion_Designer_Viewer_Zoom_100.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer viewer 75%
        with uuid("04640fd9-e61d-449b-808a-0585520ec49d") as case:
            pan_zoom_page.magic_motion_designer.select_viewer_zoom("75%")
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.7.6_Motion_Designer_Viewer_Zoom_75.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.7.6_Motion_Designer_Viewer_Zoom_75.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer viewer 50%
        with uuid("6fcbe5ef-8a14-4813-b138-45f479117011") as case:
            pan_zoom_page.magic_motion_designer.select_viewer_zoom("50%")
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.7.7_Motion_Designer_Viewer_Zoom_50.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.7.7_Motion_Designer_Viewer_Zoom_50.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer viewer 25%
        with uuid("bbb5bf0b-2779-4565-bd82-eb14caa49832") as case:
            pan_zoom_page.magic_motion_designer.select_viewer_zoom("25%")
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.7.8_Motion_Designer_Viewer_Zoom_25.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.7.8_Motion_Designer_Viewer_Zoom_25.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer viewer 10%
        with uuid("58aff17b-833c-4eb7-9277-8965ce13932e") as case:
            pan_zoom_page.magic_motion_designer.select_viewer_zoom("10%")
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.7.9_Motion_Designer_Viewer_Zoom_10.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.7.9_Motion_Designer_Viewer_Zoom_10.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer viewer Fit
        with uuid("2d41af0e-089b-4a84-b6d8-c46db176f31d") as case:
            pan_zoom_page.magic_motion_designer.select_viewer_zoom("Fit")
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.7.10_Motion_Designer_Viewer_Zoom_Fit.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.7.10_Motion_Designer_Viewer_Zoom_Fit.png',
                                                 preview_result)
            case.result = image_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_8(self):
        # Motion Designer add keyframe
        with uuid("fa91810b-34ef-4d1f-9fbf-1397801089ef") as case:
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            time.sleep(DELAY_TIME * 4)
            pan_zoom_page.apply_motion_style(10)
            pan_zoom_page.click_motion_designer()
            time.sleep(DELAY_TIME * 2)
            pan_zoom_page.magic_motion_designer.set_timecode("00_00_02_00")
            pan_zoom_page.magic_motion_designer.keyframe.add()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.8.0_Motion_Designer_Add_keyframe.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.8.0_Motion_Designer_Add_keyframe.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer select previous keyframe and position X/Y change
        with uuid("5bbbea6b-500b-4662-9ecf-bcd81a09d619") as case:
            with uuid("d375be24-2f56-4965-9d4b-b6ca8fbd2faf") as case:
                with uuid("7f122797-6105-4008-980b-825fbde91171") as case:
                    pan_zoom_page.magic_motion_designer.keyframe.select_previous()
                    preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G1.8.1_Motion_Designer_Select_Previous_keyframe.png')
                    image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.8.1_Motion_Designer_Select_Previous_keyframe.png',
                                                         preview_result)
                    case.result = image_result

        # Motion Designer select next keyframe
        with uuid("a2ff5678-992c-4540-8f26-bf2891c90300") as case:
            pan_zoom_page.magic_motion_designer.keyframe.select_next()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.8.2_Motion_Designer_Select_Next_keyframe.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.8.2_Motion_Designer_Select_Next_keyframe.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer duplicate next keyframe
        with uuid("859146b9-beb2-4786-b78c-8a575d834922") as case:
            pan_zoom_page.magic_motion_designer.keyframe.duplicate_next()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.8.3_Motion_Designer_Duplicate_Next_keyframe.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.8.3_Motion_Designer_Duplicate_Next_keyframe.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer duplicate previous keyframe
        with uuid("ff50d7d1-dab3-445d-bd48-399cb0028e7c") as case:
            pan_zoom_page.magic_motion_designer.keyframe.duplicate_previous()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.8.4_Motion_Designer_Duplicate_Previous_keyframe.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.8.4_Motion_Designer_Duplicate_Previous_keyframe.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer drag keyframe
        with uuid("25146af9-b3f3-42bf-9205-d8e1d91e0dec") as case:
            pan_zoom_page.magic_motion_designer.keyframe.drag_node(2, 10)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.8.5_Motion_Designer_Drag_keyframe.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.8.5_Motion_Designer_Drag_keyframe.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer remove keyframe
        with uuid("b7e1cbb9-6f2f-4b46-8997-a31aadeaa98a") as case:
            pan_zoom_page.magic_motion_designer.keyframe.remove()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.8.6_Motion_Designer_Remove_keyframe.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.8.6_Motion_Designer_Remove_keyframe.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_9(self):
        # Motion Designer default aspect ratio
        with uuid("2a0cee66-ccc6-4c33-927e-fc63c7599a87") as case:
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            time.sleep(DELAY_TIME * 4)
            pan_zoom_page.apply_motion_style(7)
            pan_zoom_page.click_motion_designer()
            time.sleep(DELAY_TIME * 2)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                            file_name=Auto_Ground_Truth_Folder + 'G1.9.0_Motion_Designer_Default_Aspect_Ratio.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.9.0_Motion_Designer_Default_Aspect_Ratio.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer set aspect ratio 4:3
        with uuid("388aec3a-3286-44c5-b618-f9dd50054b8e") as case:
            pan_zoom_page.magic_motion_designer.set_aspect_ratio_4_3('ok')
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                            file_name=Auto_Ground_Truth_Folder + 'G1.9.1_Motion_Designer_Set_Aspect_Ratio_4_3.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.9.1_Motion_Designer_Set_Aspect_Ratio_4_3.png',
                                                preview_result)
            case.result = image_result

        # Motion Designer set aspect ratio 9:16
        with uuid("c04481db-50d1-496b-9e55-e885de5a77af") as case:
            pan_zoom_page.magic_motion_designer.set_aspect_ratio_9_16()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                            file_name=Auto_Ground_Truth_Folder + 'G1.9.2_Motion_Designer_Set_Aspect_Ratio_9_16.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.9.2_Motion_Designer_Set_Aspect_Ratio_9_16.png',
                                                preview_result)
            case.result = image_result

        # Motion Designer set aspect ratio 1:1
        with uuid("6875b46f-9c75-4038-8847-b77cc285badf") as case:
            pan_zoom_page.magic_motion_designer.set_aspect_ratio_1_1()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                            file_name=Auto_Ground_Truth_Folder + 'G1.9.3_Motion_Designer_Set_Aspect_Ratio_1_1.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.9.3_Motion_Designer_Set_Aspect_Ratio_1_1.png',
                                                preview_result)
            case.result = image_result

        # Motion Designer set aspect ratio freeform
        with uuid("2b13f275-2f94-444e-a81b-8b5626773250") as case:
            pan_zoom_page.magic_motion_designer.set_aspect_ratio_freeform()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                            file_name=Auto_Ground_Truth_Folder + 'G1.9.4_Motion_Designer_Set_Aspect_Ratio_Freeform.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.9.4_Motion_Designer_Set_Aspect_Ratio_Freeform.png',
                                                preview_result)
            case.result = image_result

        # Motion Designer set aspect ratio 16:9
        with uuid("937c81af-04ad-43c2-8029-32e0d88f1b45") as case:
            pan_zoom_page.magic_motion_designer.set_aspect_ratio_16_9()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                            file_name=Auto_Ground_Truth_Folder + 'G1.9.5_Motion_Designer_Set_Aspect_Ratio_16_9.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.9.5_Motion_Designer_Set_Aspect_Ratio_16_9.png',
                                                preview_result)
            case.result = image_result



    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_10(self):
        # Motion Designer position x input value
        with uuid("42a5c7b1-fced-40d7-a6cb-26e0ba3a2b57") as case:
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            time.sleep(DELAY_TIME * 4)
            pan_zoom_page.apply_motion_style(7)
            pan_zoom_page.click_motion_designer()
            time.sleep(DELAY_TIME * 2)
            pan_zoom_page.magic_motion_designer.position_x.set_value(0.3)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                            file_name=Auto_Ground_Truth_Folder + 'G1.10.0_Motion_Designer_Set_PositionX_Value.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.10.0_Motion_Designer_Set_PositionX_Value.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer position y input value
        with uuid("27555b0f-1c60-4b82-a12b-feadd8926f40") as case:
            pan_zoom_page.magic_motion_designer.position_y.set_value(0.3)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                            file_name=Auto_Ground_Truth_Folder + 'G1.10.1_Motion_Designer_Set_PositionY_Value.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.10.1_Motion_Designer_Set_PositionY_Value.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer position x arrow
        with uuid("10748aac-6617-4ad0-9c0c-4e713aea9ead") as case:
            pan_zoom_page.magic_motion_designer.position_x.click_stepper_up(3)
            pan_zoom_page.magic_motion_designer.position_x.click_stepper_down(1)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                            file_name=Auto_Ground_Truth_Folder + 'G1.10.2_Motion_Designer_Set_PositionX_Arrow.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.10.2_Motion_Designer_Set_PositionX_Arrow.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer position y arrow
        with uuid("523a5800-c0ab-4b4a-9217-3bdb79742756") as case:
            pan_zoom_page.magic_motion_designer.position_y.click_stepper_up(3)
            pan_zoom_page.magic_motion_designer.position_y.click_stepper_down(1)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                            file_name=Auto_Ground_Truth_Folder + 'G1.10.3_Motion_Designer_Set_PositionY_Arrow.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.10.3_Motion_Designer_Set_PositionY_Arrow.png',
                                                 preview_result)
            case.result = image_result



    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_11(self):
        # Motion Designer position drag preview
        with uuid("74de8102-b20e-4257-982a-3fa62d2f53a2") as case:
            with uuid("9447150f-2631-40a7-b549-68df5fca59e5") as case:
                with uuid("d93e6729-f054-4ba9-a38b-e7e4f71235f9") as case:
                    with uuid("25dac472-acdd-4068-ab01-8f44eb918678") as case:
                        with uuid("c940f827-3de9-4706-ae98-b73052a8e993") as case:
                            with uuid("47043f40-c4f5-4c54-a779-4509874707f0") as case:
                                with uuid("916e8c62-080c-47d2-9a11-42c64eca682d") as case:

                                    main_page.insert_media("Food.jpg")
                                    main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
                                    time.sleep(DELAY_TIME * 4)
                                    pan_zoom_page.apply_motion_style(7)
                                    pan_zoom_page.click_motion_designer()
                                    time.sleep(DELAY_TIME * 2)
                                    pan_zoom_page.magic_motion_designer.move_preview_object(-40)
                                    preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                                            file_name=Auto_Ground_Truth_Folder + 'G1.11.0_Motion_Designer_Set_Position_Drag_Preview.png')
                                    image_result = pan_zoom_page.compare(
                                        Ground_Truth_Folder + 'G1.11.0_Motion_Designer_Set_Position_Drag_Preview.png',
                                        preview_result)
                                    case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_12(self):
        # Motion Designer scale width input
        with uuid("966acce0-59e1-4cf1-a764-d6a55196f7ea") as case:
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            time.sleep(DELAY_TIME * 4)
            pan_zoom_page.apply_motion_style(7)
            pan_zoom_page.click_motion_designer()
            time.sleep(DELAY_TIME * 2)
            pan_zoom_page.magic_motion_designer.scale_width.set_value(0.6)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.12.0_Motion_Designer_Scale_Width_Input.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.12.0_Motion_Designer_Scale_Width_Input.png',
                    preview_result)
            case.result = image_result

        # Motion Designer scale height input
        with uuid("589a7694-3af2-40a7-baf8-e9fdfc8be521") as case:
            pan_zoom_page.magic_motion_designer.scale_height.set_value(0.4)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.12.1_Motion_Designer_Scale_Height_Input.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.12.1_Motion_Designer_Scale_Height_Input.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer scale width slider
        with uuid("b9084120-65b5-49d3-b3a6-66998a260968") as case:
            pan_zoom_page.magic_motion_designer.scale_width.set_slider(1.2)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.12.2_Motion_Designer_Scale_Width_Slider.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.12.2_Motion_Designer_Scale_Width_Slider.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer scale height slider
        with uuid("5d235d2e-f1e1-46c5-aa35-5c2137b4a6ac") as case:
            pan_zoom_page.magic_motion_designer.scale_height.set_slider(0.8)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.12.3_Motion_Designer_Scale_Height_Slider.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.12.3_Motion_Designer_Scale_Height_Slider.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer scale width arrow
        with uuid("cc088dde-5aef-42c8-a9b7-eec45a7d5c4b") as case:
            pan_zoom_page.magic_motion_designer.scale_width.click_stepper_up(3)
            pan_zoom_page.magic_motion_designer.scale_width.click_stepper_down(1)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.12.4_Motion_Designer_Scale_Width_Arrow.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.12.4_Motion_Designer_Scale_Width_Arrow.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer scale height arrow
        with uuid("e5ae1065-a98e-436e-9dd6-f55b93461384") as case:
            pan_zoom_page.magic_motion_designer.scale_height.click_stepper_up(3)
            pan_zoom_page.magic_motion_designer.scale_height.click_stepper_down(1)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.12.5_Motion_Designer_Scale_Height_Arrow.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.12.5_Motion_Designer_Scale_Height_Arrow.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer scale width and height drag preview
        with uuid("23525c39-c975-4aff-9fbb-a002aaeb3312") as case:
            with uuid("a645bf35-89eb-4a60-a86f-e9c9e31882d2") as case:
                pan_zoom_page.magic_motion_designer.resize_crop_region_from_upper_right()
                preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.12.6_Motion_Designer_Scale_Drag_Preview.png')
                image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.12.6_Motion_Designer_Scale_Drag_Preview.png',
                                                     preview_result)
                case.result = image_result

        # Motion Designer scale width and height Value changes between keyframes
        with uuid("945fe0f6-a09e-4f04-8909-f3e861ce98cf") as case:
            with uuid("1faf5510-032d-4ea4-b396-a4b5e0015f95") as case:
                pan_zoom_page.magic_motion_designer.set_timecode("00_00_02_00")
                preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.12.7_Motion_Designer_Scale_Value_Change.png')
                image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.12.7_Motion_Designer_Scale_Value_Change.png',
                                                     preview_result)
                case.result = image_result

        # Motion Designer maintain aspect ratio
        with uuid("8f3881b6-b14b-43ff-ad88-10707aaabeb4") as case:
            pan_zoom_page.magic_motion_designer.set_aspect_ratio_freeform()
            pan_zoom_page.magic_motion_designer.scale_height.set_slider(0.5)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.12.8_Motion_Designer_Maintain_Aspect_Ratio.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.12.8_Motion_Designer_Maintain_Aspect_Ratio.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_13(self):
        # Motion Designer rotation drag preview
        with uuid("61669ef5-e156-4e33-bc88-ccf9b7e59658") as case:
            with uuid("401990b8-6b0d-4c01-beed-c433765b321d") as case:
                main_page.insert_media("Food.jpg")
                main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
                time.sleep(DELAY_TIME * 4)
                pan_zoom_page.apply_motion_style(7)
                pan_zoom_page.click_motion_designer()
                time.sleep(DELAY_TIME * 2)
                pan_zoom_page.magic_motion_designer.drag_preview_object_rotate_clockwise(170)
                preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.13.0_Motion_Designer_Rotation_Drag_Preview.png')
                image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.13.0_Motion_Designer_Rotation_Drag_Preview.png',
                        preview_result)
                case.result = image_result

        # Motion Designer rotation input
        with uuid("66e8067b-c460-4779-bc43-e410b8497b03") as case:
            with uuid("5df95c5b-733f-4dad-9e6f-ce0e8086b3d7") as case:
                pan_zoom_page.magic_motion_designer.rotation.set_value(150)
                preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.13.1_Motion_Designer_Rotation_Input.png')
                image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.13.1_Motion_Designer_Rotation_Input.png',
                                                     preview_result)
                case.result = image_result

        # Motion Designer rotation arrow
        with uuid("5a455608-cbde-4f1d-9f2b-14b93e7834b7") as case:
            with uuid("4edadb53-68db-4f4e-8717-38e08b397f22") as case:
                pan_zoom_page.magic_motion_designer.rotation.click_stepper_up(3)
                pan_zoom_page.magic_motion_designer.rotation.click_stepper_down(1)
                preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.13.2_Motion_Designer_Rotation_Arrow.png')
                image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.13.2_Motion_Designer_Rotation_Arrow.png',
                                                     preview_result)
                case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_14(self):
        # Motion Designer rotation value change
        with uuid("d0620ce7-823a-43e9-bd8a-c2fa4c0a8488") as case:
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            time.sleep(DELAY_TIME * 4)
            pan_zoom_page.apply_motion_style(13)
            pan_zoom_page.click_motion_designer()
            time.sleep(DELAY_TIME * 2)
            pan_zoom_page.magic_motion_designer.set_timecode("00_00_02_00")
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.14.0_Motion_Designer_Rotation_Value_Change.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.14.0_Motion_Designer_Rotation_Value_Change.png',
                    preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_15(self):
        # Motion Designer resize crop region top center
        with uuid("b10e97b2-1180-4ff2-8392-4554ab4e54ba") as case:
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            time.sleep(DELAY_TIME * 4)
            pan_zoom_page.apply_motion_style(7)
            pan_zoom_page.click_motion_designer()
            time.sleep(DELAY_TIME * 2)
            pan_zoom_page.magic_motion_designer.resize_crop_region_from_upper_middle()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.15.0_Motion_Designer_Resize_Upper_Middle.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.15.0_Motion_Designer_Resize_Upper_Middle.png',
                    preview_result)
            case.result = image_result

        # Motion Designer undo
        with uuid("5e294d8b-ac2e-431e-a32a-10e2926b277d") as case:
            pan_zoom_page.magic_motion_designer.click_undo()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.15.1_Motion_Designer_Undo.png')
            image_result = pan_zoom_page.compare(
                Ground_Truth_Folder + 'G1.15.1_Motion_Designer_Undo.png',
                preview_result)
            case.result = image_result

        # Motion Designer redo
        with uuid("447a3763-b2ea-4b4b-a87f-78d37ada0508") as case:
            pan_zoom_page.magic_motion_designer.click_redo()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.15.2_Motion_Designer_Redo.png')
            image_result = pan_zoom_page.compare(
                Ground_Truth_Folder + 'G1.15.2_Motion_Designer_Redo.png',
                preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_16(self):
        # Motion Designer resize crop region top left
        with uuid("5137f370-fbba-4182-aeef-d65817c1673b") as case:
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            time.sleep(DELAY_TIME * 4)
            pan_zoom_page.apply_motion_style(7)
            pan_zoom_page.click_motion_designer()
            time.sleep(DELAY_TIME * 2)
            pan_zoom_page.magic_motion_designer.resize_crop_region_from_upper_left()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.16.0_Motion_Designer_Resize_Upper_Left.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.16.0_Motion_Designer_Resize_Upper_Left.png',
                    preview_result)
            case.result = image_result

        # Motion Designer resize crop region top right
        with uuid("3d86644c-f5c2-40fa-abff-7d797dbaf57b") as case:
            pan_zoom_page.magic_motion_designer.resize_crop_region_from_upper_right()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.16.1_Motion_Designer_Resize_Upper_Right.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.16.1_Motion_Designer_Resize_Upper_Right.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer resize crop region left center
        with uuid("5c0ad386-6267-438a-b3b4-8c3e430b5aa9") as case:
            pan_zoom_page.magic_motion_designer.resize_crop_region_from_middle_left()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.16.2_Motion_Designer_Resize_Left_Center.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.16.2_Motion_Designer_Resize_Left_Center.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer resize crop region right center
        with uuid("9d9a5aa3-8d41-4d8a-9e31-675e7fa2d4d7") as case:
            pan_zoom_page.magic_motion_designer.resize_crop_region_from_middle_right()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.16.3_Motion_Designer_Resize_Right_Center.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.16.3_Motion_Designer_Resize_Right_Center.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer resize crop region bottom left
        with uuid("1ab58be4-a0a7-45e1-9c49-7dd9595a3e87") as case:
            pan_zoom_page.magic_motion_designer.resize_crop_region_from_lower_left()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.16.4_Motion_Designer_Resize_Bottom_Left.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.16.4_Motion_Designer_Resize_Bottom_Left.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer resize crop region bottom center
        with uuid("b221d9c7-fb5f-4b02-8bac-3f418a5a829c") as case:
            pan_zoom_page.magic_motion_designer.resize_crop_region_from_lower_middle()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.16.5_Motion_Designer_Resize_Bottom_Center.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.16.5_Motion_Designer_Resize_Bottom_Center.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer resize crop region bottom right
        with uuid("5f439749-ffdf-465d-b45f-69c2e4dd929c") as case:
            pan_zoom_page.magic_motion_designer.resize_crop_region_from_lower_right()
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.16.6_Motion_Designer_Resize_Bottom_Right.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.16.6_Motion_Designer_Resize_Bottom_Right.png',
                                                 preview_result)
            case.result = image_result

        # Motion Designer OK
        with uuid("acff73df-9a03-42a9-8237-3d01dc574936") as case:
            pan_zoom_page.magic_motion_designer.click_ok()
            time.sleep(DELAY_TIME * 2)
            preview_result1 = pan_zoom_page.snapshot(locator=L.playback_window.main,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.16.7_Motion_Designer_OK_1.png')
            image_result1 = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.16.7_Motion_Designer_OK_1.png',
                                                 preview_result1)
            preview_result2 = pan_zoom_page.snapshot(locator=pan_zoom_page.area.timeline,
                                                     file_name=Auto_Ground_Truth_Folder + 'G1.16.7_Motion_Designer_OK_2.png')
            image_result2 = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.16.7_Motion_Designer_OK_2.png',
                                                  preview_result2)
            case.result = image_result1 and image_result2

        # Main page undo
        with uuid("f8122a1b-ee8a-4f29-bc22-9679bf2858b0") as case:
            main_page.click_undo()
            preview_result = pan_zoom_page.snapshot(locator=L.playback_window.main,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.16.8_Timeline_Undo.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.16.8_Timeline_Undo.png',
                                                 preview_result)
            case.result = image_result

        # Main page redo
        with uuid("5900eec7-fb6d-4db0-b9a1-22ee1f59563a") as case:
            main_page.click_redo()
            preview_result = pan_zoom_page.snapshot(locator=L.playback_window.main,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.16.9_Timeline_Redo.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.16.9_Timeline_Redo.png',
                                                 preview_result)
            case.result = image_result

        # timeline split
        with uuid("bee82309-4a22-4c5c-96f7-1d0fadf3ac7a") as case:
            timeline_operation_page.timeline_click_zoomin_btn()
            playback_window_page.set_timecode_slidebar('00_00_01_00')
            tips_area_page.click_TipsArea_btn_split()
            preview_result = pan_zoom_page.snapshot(locator=pan_zoom_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.16.10_Timeline_Split.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.16.10_Timeline_Split.png',
                                                 preview_result)
            case.result = image_result

        # Pan and Zoom i button
        with uuid("6b27a762-0a75-41bd-a31e-8b6832e93f19") as case:
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            time.sleep(DELAY_TIME * 4)
            result = pan_zoom_page.click_i_button()
            case.result = result

        # Motion Designer re-enter
        with uuid("1cb38fdc-b902-4767-b620-f7af627ada45") as case:
            time.sleep(DELAY_TIME * 4)
            pan_zoom_page.click_motion_designer()
            time.sleep(DELAY_TIME * 4)
            preview_result = pan_zoom_page.snapshot(locator=L.pan_zoom.magic_motion_designer.main_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.16.12_Motion_Designer_Re-Enter.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.16.12_Motion_Designer_Re-Enter.png',
                                                 preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_1_17(self):
        # Apply all selected images
        with uuid("935b81e7-5183-47b9-b947-73b61807b86a") as case:
            main_page.insert_media("Food.jpg")
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            tips_area_page.click_TipsArea_btn_insert(1)
            pan_zoom_page.tap_SelectAll_hotkey()
            main_page.tap_TipsArea_Tools_menu("Pan & Zoom")
            time.sleep(DELAY_TIME * 4)
            pan_zoom_page.apply_motion_style(6)
            preview_result = pan_zoom_page.snapshot(locator=pan_zoom_page.area.timeline,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.17.0_Apply_on_all_selected_images.png')
            image_result = pan_zoom_page.compare(Ground_Truth_Folder + 'G1.17.0_Apply_on_all_selected_images.png',
                                                 preview_result)
            case.result = image_result
