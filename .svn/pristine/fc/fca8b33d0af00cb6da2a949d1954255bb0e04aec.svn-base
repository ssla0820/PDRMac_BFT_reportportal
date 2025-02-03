import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time, inspect, datetime, pytest, re, configparser
os.chdir(os.path.dirname(__file__))
from types import SimpleNamespace

from ATFramework.pages.base_page import BasePage
from ATFramework import MyReport, logger
from ATFramework.drivers.driver_factory import DriverFactory
from pages.page_factory import PageFactory
from configs.app_config import *
# import pages.media_room_page
from pages.locator import locator as L
# Modify locator to hardcode_0408
#from pages.locator.hardcode_0408 import locator as L

#for update_report_info
from globals import *


# read PDR cap >>
app = SimpleNamespace(**PDR_cap)
# read PDR cap <<

# create driver & page >>
mwc = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
effect_room_page = PageFactory().get_page_object('effect_room_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
transition_room_page = PageFactory().get_page_object('transition_room_page', mwc)
video_speed_page = PageFactory().get_page_object('video_speed_page', mwc)
#blending_mode_page = PageFactory().get_page_object('blending_mode_page',mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page',mwc)
produce_page = PageFactory().get_page_object('produce_page',mwc)
video_collage_designer_page = PageFactory().get_page_object('video_collage_designer_page',mwc)
trim_page = PageFactory().get_page_object('trim_page',mwc)
fix_enhance_page = PageFactory().get_page_object('fix_enhance_page',mwc)
crop_zoom_pan_page = PageFactory().get_page_object('crop_zoom_pan_page',mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Crop Zoom Pan.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Crop_Zoom_Pan/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Crop_Zoom_Pan/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Crop_Zoom_Pan():
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
            google_sheet_execution_log_init('Test_Crop_Zoom_Pan')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"Crop Zoom Pan result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        #11/9
        with uuid('7c3e88bb-9113-4c6c-9c8f-a439a1cb20a1') as case:
            # session 1 : General > Entry Point
            # case1.1 : Tools > Crop/Zoom/Pan
            # select one of library media and insert to track1
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.insert_media('Skateboard 01.mp4')

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('Skateboard 01.mp4')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME*7)

            # snapshot for crop/zoom/pan window
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G1.1_Crop_Zoom_Pan_Page.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1_Crop_Zoom_Pan_Page.png', crop_zoom_pan_window)
            logger(compare_result)

            # exit crop_zoom_pan_window by ESC key
            #trim_page.press_esc_key()

            # 11/9
            with uuid('621e0aad-4558-4f5d-a0bc-fdc73190e6ca') as case:
                # case1.2.1.2.1 : Maximize the Crop/Zoom/Pan dialogue
                # click Maximize button to enlarge Crop/Zoom/Pan page
                crop_zoom_pan_page.click_maximize_btn()
                time.sleep(DELAY_TIME*2)

                # snapshot for crop/zoom/pan window
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                               file_name=Auto_Ground_Truth_Folder + 'G1.2.1.2.1_Maximize_Crop_Zoom_Pan.png')
                logger(crop_zoom_pan_window)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.2.1.2.1_Maximize_Crop_Zoom_Pan.png', crop_zoom_pan_window)
                logger(compare_result1)

                case.result = compare_result1

            # 11/9
            with uuid('c00215b8-61dc-472c-b2f4-a99dcb3c44f0') as case:
                # case1.2.1.2.1 : Restore the Crop/Zoom/Pan dialogue
                # click Maximize button again to restore Crop/Zoom/Pan page
                crop_zoom_pan_page.click_maximize_btn()
                time.sleep(DELAY_TIME * 2)

                # snapshot for crop/zoom/pan window
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                               file_name=Auto_Ground_Truth_Folder + 'G1.2.1.2.2_Restore_Crop_Zoom_Pan.png')
                logger(crop_zoom_pan_window)
                compare_result2 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.2.1.2.2_Restore_Crop_Zoom_Pan.png', crop_zoom_pan_window)
                logger(compare_result2)

                case.result = compare_result2

            case.result = compare_result

        # 11/11
        with uuid('8191792c-827d-430a-9bcf-ea986f7cd693') as case:
            # session 1 : General > General Function
            # case1.2.3.1 : Show current timecode
            timecode = crop_zoom_pan_page.get_timecode()
            logger(timecode)

            if timecode == '00;00;00;00':
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            if result:
                # snapshot for crop/zoom/pan window
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                                file_name=Auto_Ground_Truth_Folder + 'G1.2.3.1_Crop_Zoom_Pan_Preview.png')
                logger(crop_zoom_pan_window)
                compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G1.2.3.1_Crop_Zoom_Pan_Preview.png', crop_zoom_pan_window)
                logger(compare_result)

            case.result = result and compare_result

        # 11/11
        with uuid('fa0c8bb1-1ac2-43c3-8c7c-e99045983eb3') as case:
            # session 1 : General > General Function
            # case1.2.3.2 : Input timecode
            timecode = crop_zoom_pan_page.set_timecode('00_00_03_10')
            logger(timecode)

            timecode = crop_zoom_pan_page.get_timecode()
            logger(timecode)

            if timecode == '00;00;03;10':
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            if result:
                # snapshot for crop/zoom/pan window
                time.sleep(DELAY_TIME*2)
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                                file_name=Auto_Ground_Truth_Folder + 'G1.2.3.2_Crop_Zoom_Pan_Preview_after_set_timecode.png')
                logger(crop_zoom_pan_window)
                compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G1.2.3.2_Crop_Zoom_Pan_Preview_after_set_timecode.png', crop_zoom_pan_window)
                logger(compare_result)

            case.result = result and compare_result

        # 11/11
        with uuid('f7e4325f-02b9-4c1f-9add-2ea2f829611d') as case:
            # session 1 : General > General Function
            # case1.2.4.3.9 : Toggle TV safe zone and grid lines on/off > Grid Lines = 9
            # switch grid line from 'None' to '9'
            crop_zoom_pan_page.select_grid_lines_format(9)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.4.3.9_Crop_Zoom_Pan_Grid_line_9.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.4.3.9_Crop_Zoom_Pan_Grid_line_9.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result



        # 11/11
        with uuid('bc192dd1-0010-42dd-b63d-3a8d3690cf10') as case:
            # session 1 : General > General Function
            # case1.2.5.6 : Viewer Zoom > Set to 100%
            # set preview to 100%
            set_zoom_menu = crop_zoom_pan_page.click_viewer_zoom_menu('100%')
            logger(set_zoom_menu)
            get_zoom_menu = crop_zoom_pan_page.get_viewer_setting()
            logger(get_zoom_menu)

            if get_zoom_menu == '100%':
                test_result = True
                logger(test_result)
            else:
                test_result = False
                logger(test_result)

            if test_result:
                # snapshot for crop/zoom/pan window
                time.sleep(DELAY_TIME * 2)
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G1.2.5.6_Crop_Zoom_Pan_Zoom_In_100.png')
                logger(crop_zoom_pan_window)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.2.5.6_Crop_Zoom_Pan_Zoom_In_100.png', crop_zoom_pan_window)
                logger(compare_result)

            case.result = test_result and compare_result

        # 11/11
        with uuid('efb9d1a5-3062-4829-8b61-3e885e9880f6') as case:
            # session 1 : General > General Function
            # case1.2.4.3.5 : Toggle TV safe zone and grid lines on/off > Grid Lines = 5
            # switch grid line from 'None' to '5'
            crop_zoom_pan_page.select_grid_lines_format(5)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.4.3.5_Crop_Zoom_Pan_Grid_line_5.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.4.3.5_Crop_Zoom_Pan_Grid_line_5.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 11/11
        with uuid('6b4e29c9-66e4-46bc-8096-1c7b393fdcb5') as case:
            # session 1 : General > General Function
            # case1.2.5.7 : Viewer Zoom > Set to 200%
            # set preview to 200%
            set_zoom_menu = crop_zoom_pan_page.click_viewer_zoom_menu('200%')
            logger(set_zoom_menu)
            get_zoom_menu = crop_zoom_pan_page.get_viewer_setting()
            logger(get_zoom_menu)

            if get_zoom_menu == '200%':
                test_result = True
                logger(test_result)
            else:
                test_result = False
                logger(test_result)

            if test_result:
                # snapshot for crop/zoom/pan window
                time.sleep(DELAY_TIME * 2)
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G1.2.5.7_Crop_Zoom_Pan_Zoom_In_200.png')
                logger(crop_zoom_pan_window)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.2.5.7_Crop_Zoom_Pan_Zoom_In_200.png', crop_zoom_pan_window)
                logger(compare_result)

            case.result = test_result and compare_result

        # 11/11
        with uuid('a68e824a-421c-4e32-b48f-78184d754de0') as case:
            # session 1 : General > General Function
            # case1.2.4.3.2 : Toggle TV safe zone and grid lines on/off > Grid Lines = 2
            # switch grid line from 'None' to '2'
            crop_zoom_pan_page.select_grid_lines_format(2)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.4.3.2_Crop_Zoom_Pan_Grid_line_2.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.4.3.2_Crop_Zoom_Pan_Grid_line_2.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 11/11
        with uuid('1bc1a4b8-ee55-43f3-b100-8ef70afef9c6') as case:
            # session 1 : General > General Function
            # case1.2.5.4 : Viewer Zoom > Set to 50%
            # set preview to 50%
            set_zoom_menu = crop_zoom_pan_page.click_viewer_zoom_menu('50%')
            logger(set_zoom_menu)
            get_zoom_menu = crop_zoom_pan_page.get_viewer_setting()
            logger(get_zoom_menu)

            if get_zoom_menu == '50%':
                test_result = True
                logger(test_result)
            else:
                test_result = False
                logger(test_result)

            if test_result:
                # snapshot for crop/zoom/pan window
                time.sleep(DELAY_TIME * 2)
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G1.2.5.4_Crop_Zoom_Pan_Zoom_In_50.png')
                logger(crop_zoom_pan_window)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.2.5.4_Crop_Zoom_Pan_Zoom_In_50.png', crop_zoom_pan_window)
                logger(compare_result)

            case.result = test_result and compare_result

        # 11/18
        with uuid('f5eec63c-fd65-4dcd-8b56-70d960dc4a2a') as case:
            # session 1 : General > General Function
            # case1.2.4.3.7 : Toggle TV safe zone and grid lines on/off > Grid Lines = 7
            # switch grid line to '7'
            crop_zoom_pan_page.select_grid_lines_format(7)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.4.3.7_Crop_Zoom_Pan_Grid_line_7.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.4.3.7_Crop_Zoom_Pan_Grid_line_7.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 11/18
        with uuid('246f45ba-198c-48c9-86a2-f7c560f3728b') as case:
            # session 1 : General > General Function
            # case1.2.5.9 : Viewer Zoom > Set to 400%
            # set preview to 50%
            set_zoom_menu = crop_zoom_pan_page.click_viewer_zoom_menu('400%')
            logger(set_zoom_menu)
            get_zoom_menu = crop_zoom_pan_page.get_viewer_setting()
            logger(get_zoom_menu)

            if get_zoom_menu == '400%':
                test_result = True
                logger(test_result)
            else:
                test_result = False
                logger(test_result)

            if test_result:
                # snapshot for crop/zoom/pan window
                time.sleep(DELAY_TIME * 2)
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G1.2.5.9_Crop_Zoom_Pan_Zoom_In_400.png')
                logger(crop_zoom_pan_window)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.2.5.9_Crop_Zoom_Pan_Zoom_In_400.png', crop_zoom_pan_window)
                logger(compare_result)

            case.result = test_result and compare_result

        # 11/18
        with uuid('2b00f2dc-1241-4556-a164-668c589ab0f8') as case:
            # session 1 : General > General Function
            # case1.2.4.3.4 : Toggle TV safe zone and grid lines on/off > Grid Lines = 4
            # switch grid line to '4'
            crop_zoom_pan_page.select_grid_lines_format(4)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.4.3.4_Crop_Zoom_Pan_Grid_line_4.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.4.3.4_Crop_Zoom_Pan_Grid_line_4.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 11/18
        with uuid('2dc34043-f338-4f51-b02e-3e0cd508a786') as case:
            # session 1 : General > General Function
            # case1.2.5.3 : Viewer Zoom > Set to 25%
            # set preview to 25%
            set_zoom_menu = crop_zoom_pan_page.click_viewer_zoom_menu('25%')
            logger(set_zoom_menu)
            get_zoom_menu = crop_zoom_pan_page.get_viewer_setting()
            logger(get_zoom_menu)

            if get_zoom_menu == '25%':
                test_result = True
                logger(test_result)
            else:
                test_result = False
                logger(test_result)

            if test_result:
                # snapshot for crop/zoom/pan window
                time.sleep(DELAY_TIME * 2)
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G1.2.5.3_Crop_Zoom_Pan_Zoom_In_25.png')
                logger(crop_zoom_pan_window)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.2.5.3_Crop_Zoom_Pan_Zoom_In_25.png', crop_zoom_pan_window)
                logger(compare_result)

            case.result = test_result and compare_result

        # 11/18
        with uuid('26ce5e8d-5aeb-4a08-8017-4df0182a5952') as case:
            # session 1 : General > General Function
            # case1.2.4.3.6 : Toggle TV safe zone and grid lines on/off > Grid Lines = 6
            # switch grid line to '6'
            crop_zoom_pan_page.select_grid_lines_format(6)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.4.3.6_Crop_Zoom_Pan_Grid_line_6.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.4.3.6_Crop_Zoom_Pan_Grid_line_6.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 11/18
        with uuid('ccfdce59-4de3-465c-a534-c9dd992386d4') as case:
            # session 1 : General > General Function
            # case1.2.5.8 : Viewer Zoom > Set to 300%
            # set preview to 300%
            set_zoom_menu = crop_zoom_pan_page.click_viewer_zoom_menu('300%')
            logger(set_zoom_menu)
            get_zoom_menu = crop_zoom_pan_page.get_viewer_setting()
            logger(get_zoom_menu)

            if get_zoom_menu == '300%':
                test_result = True
                logger(test_result)
            else:
                test_result = False
                logger(test_result)

            if test_result:
                # snapshot for crop/zoom/pan window
                time.sleep(DELAY_TIME * 2)
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G1.2.5.8_Crop_Zoom_Pan_Zoom_In_300.png')
                logger(crop_zoom_pan_window)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.2.5.8_Crop_Zoom_Pan_Zoom_In_300.png', crop_zoom_pan_window)
                logger(compare_result)

            case.result = test_result and compare_result

        # 11/18
        with uuid('96b0b56d-836a-416e-a25f-5801990d241d') as case:
            # session 1 : General > General Function
            # case1.2.4.3.3 : Toggle TV safe zone and grid lines on/off > Grid Lines = 3
            # switch grid line to '3'
            crop_zoom_pan_page.select_grid_lines_format(3)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.4.3.3_Crop_Zoom_Pan_Grid_line_3.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.4.3.3_Crop_Zoom_Pan_Grid_line_3.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 11/18
        with uuid('fe82c9a0-6a21-4714-9864-78188976b9e1') as case:
            # session 1 : General > General Function
            # case1.2.5.2 : Viewer Zoom > Set to 10%
            # set preview to 10%
            set_zoom_menu = crop_zoom_pan_page.click_viewer_zoom_menu('10%')
            logger(set_zoom_menu)
            get_zoom_menu = crop_zoom_pan_page.get_viewer_setting()
            logger(get_zoom_menu)

            if get_zoom_menu == '10%':
                test_result = True
                logger(test_result)
            else:
                test_result = False
                logger(test_result)

            if test_result:
                # snapshot for crop/zoom/pan window
                time.sleep(DELAY_TIME * 2)
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G1.2.5.2_Crop_Zoom_Pan_Zoom_In_10.png')
                logger(crop_zoom_pan_window)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.2.5.2_Crop_Zoom_Pan_Zoom_In_10.png', crop_zoom_pan_window)
                logger(compare_result)

            case.result = test_result and compare_result








        # 11/11
        with uuid('cad66fdc-aa57-4273-9aad-58567c0dbe97') as case:
            # session 1 : General > General Function
            # case1.2.1.3 : Close "Crop/Zoom/Pan" windows
            # Click [Close] to close "crop/zoom/pan"
            crop_zoom_pan_page.close_window()
            check_result = crop_zoom_pan_page.is_not_exist(L.crop_zoom_pan.window)
            logger(check_result)

            case.result = check_result


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        #11/18
        with uuid('519d1b19-9bb7-4167-ac8f-a0db7d95577c') as case:
            # session 1 : General > General Function
            # case1.2.2.2 : Playback Panel > Stop
            # select one of library media and insert to track1
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            main_page.insert_media('Skateboard 02.mp4')

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('Skateboard 02.mp4')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME*7)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 3)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.preview,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.2.2_BeforePlayback.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.2.2_BeforePlayback.png', crop_zoom_pan_window)
            logger(compare_result)

            # Playback
            playback_func = crop_zoom_pan_page.preview_operation('Play')
            logger(playback_func)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 3)
            crop_zoom_pan_play = tips_area_page.snapshot(locator=L.crop_zoom_pan.preview,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.2.2_StartPlayback.png')
            compare_result1 = tips_area_page.compare(crop_zoom_pan_play, crop_zoom_pan_window)
            logger(compare_result1)

            # check if start playback correctly
            if compare_result1 == False:
                playback_function = True
                logger(playback_function)
            else:
                playback_function = False
                logger(playback_function)

            # Stop playback
            crop_zoom_pan_page.preview_operation('Stop')

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.preview,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.2.2_StopPlayback.png')
            logger(crop_zoom_pan_window)
            compare_result2 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.2.2_StopPlayback.png', crop_zoom_pan_window)
            logger(compare_result2)

            case.result = compare_result and playback_function and compare_result2

        #11/18
        with uuid('51beb1b9-0a63-441f-b73d-1133f0f365aa') as case:
            # session 1 : General > General Function
            # case1.2.2.4 : Playback Panel > Next frame
            # seek video by set timecode
            crop_zoom_pan_page.set_timecode('00_00_06_04')
            time.sleep(DELAY_TIME*2)

            # Go to next frame
            crop_zoom_pan_page.preview_operation('Next_Frame')

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME*2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.2.4_NextFrame.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.2.4_NextFrame.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        #11/18
        with uuid('c66ab551-9a21-4d95-83df-5e346a31bb8b') as case:
            # session 1 : General > General Function
            # case1.2.2.3 : Playback Panel > Previous frame
            # seek video by set timecode
            #crop_zoom_pan_page.set_timecode(00_00_06_01)
            #time.sleep(DELAY_TIME)

            # Go to previous frame
            crop_zoom_pan_page.preview_operation('Previous_Frame')

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.2.3_PreviousFrame.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.2.3_PreviousFrame.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        #11/18
        with uuid('61819403-2ffb-438f-a755-ab98b9a78aa1') as case:
            # session 2 : Crop/Zoom
            # case2.1.1 : Select Aspect Ratio > 4:3
            # set aspect ratio to 4:3
            crop_zoom_pan_page.set_AspectRatio_4_3()

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 3)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.1.1_AspectRation_4_3.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.1_AspectRation_4_3.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 11/18
        with uuid('5a695a42-8a4d-43c5-89e1-26b3ef4a173e') as case:
            # session 1 : General > General Function
            # case1.2.4.3.8 : Toggle TV safe zone and grid lines on/off > Grid Lines = 8
            # switch grid line from 'None' to '8'
            crop_zoom_pan_page.select_grid_lines_format(8)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.4.3.8_Crop_Zoom_Pan_Grid_line_8.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.4.3.8_Crop_Zoom_Pan_Grid_line_8.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 11/18
        with uuid('5747bfda-1f3f-4f79-b701-0021abce1deb') as case:
            # session 1 : General > General Function
            # case1.2.5.9 : Viewer Zoom > Set to 800%
            # set preview to 800%
            set_zoom_menu = crop_zoom_pan_page.click_viewer_zoom_menu('800%')
            logger(set_zoom_menu)
            get_zoom_menu = crop_zoom_pan_page.get_viewer_setting()
            logger(get_zoom_menu)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.5.9_Crop_Zoom_Pan_Zoom_In_800.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.5.9_Crop_Zoom_Pan_Zoom_In_800.png', crop_zoom_pan_window)
            logger(compare_result)

            if get_zoom_menu == '800%':
                test_result = True
                logger(test_result)
            else:
                test_result = False
                logger(test_result)

            case.result = test_result and compare_result

        # 11/18
        with uuid('8c032ed5-c014-4c9a-a775-0348bb162cce') as case:
            # session 1 : General > General Function
            # case1.2.5.1 : Viewer Zoom > Set to Fit
            # set preview to Fit
            set_zoom_menu = crop_zoom_pan_page.click_viewer_zoom_menu('Fit')
            logger(set_zoom_menu)
            get_zoom_menu = crop_zoom_pan_page.get_viewer_setting()
            logger(get_zoom_menu)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.5.1_Crop_Zoom_Pan_Zoom_In_Fit.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.5.1_Crop_Zoom_Pan_Zoom_In_Fit.png', crop_zoom_pan_window)
            logger(compare_result)

            if get_zoom_menu == 'Fit':
                test_result = True
                logger(test_result)
            else:
                test_result = False
                logger(test_result)

            case.result = test_result and compare_result

        # 11/18
        with uuid('bba2a032-26db-4734-8e6f-a6e737250b85') as case:
            # session 2 : Crop/zoom
            # case2.2.1.2 : Crop 4:3 area with non 4:3 clip
            # adjust width / height by value
            #crop_zoom_pan_page.set_scale_width(0.530) --> exception
            crop_zoom_pan_page.set_scale_width_slider(0.2)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.1.2_Crop_4-3_area_Non_4-3_clip.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.2.1.2_Crop_4-3_area_Non_4-3_clip.png', crop_zoom_pan_window)
            logger(compare_result)

            # seek to early time frame
            crop_zoom_pan_page.set_timecode('00_00_03_00')
            time.sleep(DELAY_TIME)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.1.2_Crop_4-3_area_Non_4-3_clip_seek.png')
            logger(crop_zoom_pan_window)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.2.1.2_Crop_4-3_area_Non_4-3_clip_seek.png', crop_zoom_pan_window)
            logger(compare_result1)

            # click [Ok] to apply all settings
            crop_zoom_pan_page.click_ok()
            time.sleep(DELAY_TIME*2)

            # seek to specific time code
            time.sleep(DELAY_TIME)
            set_timecode = main_page.set_timeline_timecode('00_00_03_20')
            logger(set_timecode)
            time.sleep(DELAY_TIME * 2)

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.2.1.2_Crop_4-3_area_Non_4-3_clip_timeline_preview.png')
            logger(preview_wnd)
            compare_result2 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.2.1.2_Crop_4-3_area_Non_4-3_clip_timeline_preview.png',
                preview_wnd)
            logger(compare_result2)

            case.result = compare_result and compare_result1 and compare_result2

        # 11/18
        with uuid('1119f43d-0db9-4ea4-aa71-99cd6c9c1eee') as case:
            # session 2 : Crop/zoom
            # case2.1.2 : set aspect ratio to 16:9
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('Skateboard 02.mp4')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 8)

            # set aspect ratio to 16:9
            crop_zoom_pan_page.set_AspectRatio_16_9()
            time.sleep(DELAY_TIME)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 5)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.1.2_AspectRation_16_9.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.2_AspectRation_16_9.png', crop_zoom_pan_window)
            logger(compare_result)

            # press Enter
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_page.press_enter_key()

            # snapshot for applied result
            time.sleep(DELAY_TIME * 5)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.1.2_AspectRation_16_9_applied.png')
            logger(crop_zoom_pan_window)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.2_AspectRation_16_9_applied.png', crop_zoom_pan_window)
            logger(compare_result1)

            case.result = compare_result and compare_result1

        # 11/18
        with uuid('051fccfc-718c-4ccb-9dbc-3a56459664e3') as case:
            # session 2 : Crop/zoom
            # case2.2.2.1 : Crop 16:9 area with 16:9 clip
            # seek to early time frame
            crop_zoom_pan_page.set_timecode('00_00_07_00')
            time.sleep(DELAY_TIME)

            # adjust width / height by value
            # crop_zoom_pan_page.set_scale_width(0.530) --> exception
            crop_zoom_pan_page.set_scale_width_slider(0.3)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                               file_name=Auto_Ground_Truth_Folder + 'G2.2.2.1_Crop_16-9_area_16-9_clip.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.2.2.1_Crop_16-9_area_16-9_clip.png', crop_zoom_pan_window)
            logger(compare_result)

            # seek to early time frame
            crop_zoom_pan_page.set_timecode('00_00_03_00')
            time.sleep(DELAY_TIME)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.2.2.1_Crop_16-9_area_16-9_clip_seek.png')
            logger(crop_zoom_pan_window)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.2.2.1_Crop_16-9_area_16-9_clip_seek.png', crop_zoom_pan_window)
            logger(compare_result1)

            # click [Ok] to apply all settings
            crop_zoom_pan_page.click_ok()
            time.sleep(DELAY_TIME * 2)

            # seek to specific time code
            time.sleep(DELAY_TIME)
            set_timecode = main_page.set_timeline_timecode('00_00_03_20')
            logger(set_timecode)

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.2.2.1_Crop_16-9_area_16-9_clip_timeline_preview.png')
            logger(preview_wnd)
            compare_result2 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.2.2.1_Crop_16-9_area_16-9_clip_timeline_preview.png',
                preview_wnd)
            logger(compare_result2)

            case.result = compare_result and compare_result1 and compare_result2

        # 11/21
        with uuid('5aa70ab6-05d0-4256-a87c-25c3575a5e92') as case:
            # session 2 : Crop/zoom
            # case2.1.4 : set aspect ratio to 1:1
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('Skateboard 02.mp4')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 8)

            # set aspect ratio to 4:3
            crop_zoom_pan_page.set_AspectRatio_1_1()

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 3)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.1.4_AspectRation_1_1.png')
            time.sleep(DELAY_TIME)
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.4_AspectRation_1_1.png', crop_zoom_pan_window, similarity=0.9)
            logger(compare_result)

            # press Enter
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_page.press_enter_key()

            # snapshot for applied result
            time.sleep(DELAY_TIME * 5)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.1.4_AspectRation_1_1_applied.png')
            logger(crop_zoom_pan_window)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.4_AspectRation_1_1_applied.png', crop_zoom_pan_window)
            logger(compare_result1)

            case.result = compare_result and compare_result1

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        #11/25
        with uuid('9688b708-4e5a-460e-8fa9-4b7e17efeae8') as case:
            # session 2 : Crop/Zoom
            # case2.2.1 : Crop > Crop 4:3 Area
            # import 4:3 video and insert to track1
            time.sleep(DELAY_TIME * 5)
            main_page.set_project_aspect_ratio_4_3()
            import_media = media_room_page.import_media_file(Test_Material_Folder + 'Crop_Zoom_Pan/DV-AVI_720x480_4_3_24.4Mbps_LPCM.AVI')
            logger(import_media)
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media('DV-AVI_720x480_4_3_24.4Mbps_LPCM.AVI')
            main_page.insert_media('DV-AVI_720x480_4_3_24.4Mbps_LPCM.AVI')

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('DV-AVI_720x480_4_3_24.4Mbps_LPCM.AVI')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # set aspect ratio to 4:3
            crop_zoom_pan_page.set_AspectRatio_4_3()

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.1.1_Crop_4-3_area_4-3_clip.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.2.1.1_Crop_4-3_area_4-3_clip.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 11/25
        with uuid('6e20838c-f3e7-403f-8f4c-27c7257ab872') as case:
            # session 2 : Crop/Zoom
            # case2.2.4 : Crop 16:9 area > on non 16:9 video
            # set aspect ratio to 16:9
            crop_zoom_pan_page.set_AspectRatio_16_9()

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                               file_name=Auto_Ground_Truth_Folder + 'G2.2.2.2_Crop_16-9_area_Non_16-9_clip.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.2.2.2_Crop_16-9_area_Non_16-9_clip.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 11/25
        with uuid('0d16a5f0-ffc9-4e33-b628-e209c9d5c1ed') as case:
            # session 1 : General > General Function
            # case1.2.5.11 : Viewer Zoom > Set to 1600%
            # set preview to 1600%
            set_zoom_menu = crop_zoom_pan_page.click_viewer_zoom_menu('1600%')
            logger(set_zoom_menu)
            get_zoom_menu = crop_zoom_pan_page.get_viewer_setting()
            logger(get_zoom_menu)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.5.11_Crop_Zoom_Pan_Zoom_In_1600.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.5.11_Crop_Zoom_Pan_Zoom_In_1600.png', crop_zoom_pan_window)
            logger(compare_result)

            if get_zoom_menu == '1600%':
                test_result = True
                logger(test_result)
            else:
                test_result = False
                logger(test_result)

            # switch zoom menu to 'Fit'
            #set_zoom_menu1 = crop_zoom_pan_page.click_viewer_zoom_menu('Fit')
            #logger(set_zoom_menu1)

            case.result = test_result and compare_result







    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        #11/25
        with uuid('6bc31ea6-85c6-46ee-a032-693312159cdb') as case:
            # session 2 : Crop/Zoom
            # case2.2.1 : Crop > Crop 9:16 Area
            # import 9:16 video and insert to track1
            time.sleep(DELAY_TIME * 5)
            main_page.set_project_aspect_ratio_9_16()
            import_media = media_room_page.import_media_file(Test_Material_Folder + 'Crop_Zoom_Pan/9_16.MOV')
            logger(import_media)
            media_room_page.high_definition_video_confirm_dialog_click_no()
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media('9_16.MOV')
            main_page.insert_media('9_16.MOV')

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('9_16.MOV')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # set aspect ratio to 4:3
            #crop_zoom_pan_page.set_AspectRatio_9_16()

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.3.1_Crop_9-16_area_9-16_clip.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.2.3.1_Crop_9-16_area_9-16_clip.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 11/25
        with uuid('6ce2e613-4f71-4ef1-9b87-da1c189f7171') as case:
            # session 2 : Crop/Zoom
            # case2.2.4 : Crop 1:1 area > on non 1:1 video
            # set aspect ratio to 1:1
            crop_zoom_pan_page.set_AspectRatio_1_1()

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                               file_name=Auto_Ground_Truth_Folder + 'G2.2.4.2_Crop_1-1_area_Non_1-1_clip.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.2.4.2_Crop_1-1_area_Non_1-1_clip.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 11/25
        with uuid('05c45825-72d2-4b02-a5ff-69c9d8cc9f21') as case:
            # session 1 : General > General Function
            # case1.2.5.5 : Viewer Zoom > Set to 75%
            # set preview to 75%
            set_zoom_menu = crop_zoom_pan_page.click_viewer_zoom_menu('75%')
            logger(set_zoom_menu)
            get_zoom_menu = crop_zoom_pan_page.get_viewer_setting()
            logger(get_zoom_menu)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.2.5.5_Crop_Zoom_Pan_Zoom_In_75.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.5.5_Crop_Zoom_Pan_Zoom_In_75.png', crop_zoom_pan_window)
            logger(compare_result)

            if get_zoom_menu == '75%':
                test_result = True
                logger(test_result)
            else:
                test_result = False
                logger(test_result)

            # switch zoom menu to 'Fit'
            #set_zoom_menu1 = crop_zoom_pan_page.click_viewer_zoom_menu('Fit')
            #logger(set_zoom_menu1)

            case.result = test_result and compare_result

        # 11/25
        with uuid('7c908a67-47bb-48a9-b299-0c245eca5bf6') as case:
            # session 1 : General > General Function
            # case1.2.4.3.10 : Toggle TV safe zone and grid lines on/off > Grid Lines = 10
            # switch grid line from 'None' to '10'
            crop_zoom_pan_page.select_grid_lines_format(10)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G1.2.4.3.10_Crop_Zoom_Pan_Grid_line_10.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.4.3.10_Crop_Zoom_Pan_Grid_line_10.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 11/25
        with uuid('ce132acb-93f0-4904-aa5d-ec04965dd11d') as case:
            # session 2 : Crop/Zoom
            # case2.3.1 : Object adjustment on the Selection box > Size
            # adjust width and height (unable to edit on screen by AT currently)
            resize = crop_zoom_pan_page.set_scale_width('0.72')
            logger(resize)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.3.1_Crop_Zoom_Pan_resize_by_width.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.3.1_Crop_Zoom_Pan_resize_by_width.png', crop_zoom_pan_window)
            logger(compare_result)

            resize1 = crop_zoom_pan_page.set_scale_height('0.62')
            logger(resize1)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window1 = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.3.1_Crop_Zoom_Pan_resize_by_height.png')
            logger(crop_zoom_pan_window1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.3.1_Crop_Zoom_Pan_resize_by_height.png', crop_zoom_pan_window1)
            logger(compare_result1)

            case.result = compare_result and compare_result1

        # 11/25
        with uuid('09f4dc9b-1aa1-4829-aaea-ff58c885de12') as case:
            # session 1 : General > General Function
            # case1.2.4.3.1 : Toggle TV safe zone and grid lines on/off > Grid Lines = 'None'
            # switch grid line to 'None'
            crop_zoom_pan_page.select_grid_lines_format(1)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                       file_name=Auto_Ground_Truth_Folder + 'G1.2.4.3.1_Crop_Zoom_Pan_Grid_line_None.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.2.4.3.1_Crop_Zoom_Pan_Grid_line_None.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result



    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        #11/25
        with uuid('695b4369-b6ad-4512-a973-e4a1d1b317f8') as case:
            # session 2 : Crop/Zoom
            # case2.2.4 : Crop > Crop 1:1 Area
            # import 1:1 video and insert to track1
            time.sleep(DELAY_TIME * 5)
            main_page.set_project_aspect_ratio_1_1()
            import_media = media_room_page.import_media_file(Test_Material_Folder + 'Crop_Zoom_Pan/1_1Video_Samsung_S10_hevc.mp4')
            logger(import_media)
            media_room_page.high_definition_video_confirm_dialog_click_no()
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media('1_1Video_Samsung_S10_hevc.mp4')
            main_page.insert_media('1_1Video_Samsung_S10_hevc.mp4')

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('1_1Video_Samsung_S10_hevc.mp4')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # set aspect ratio to 1:1
            #crop_zoom_pan_page.set_AspectRatio_1_1()

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.4.1_Crop_1-1_area_1-1_clip.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.2.4.1_Crop_1-1_area_1-1_clip.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 11/25
        with uuid('5ae5843c-0983-4f59-9a2f-cd7767973aa6') as case:
            # session 2 : Crop/Zoom
            # case2.2.3 : Crop 9:16 area > on non 9:16 video
            # set aspect ratio to 9:16
            crop_zoom_pan_page.set_AspectRatio_9_16()
            aspect_ratio = crop_zoom_pan_page.get_current_AspectRatio()
            logger(aspect_ratio)

            if aspect_ratio == '9:16':
                result1 = True
                logger(result1)
            else:
                result1 = False
                logger(result1)

            with uuid('9178b73f-41ec-4d80-bd41-2d922c9d6ff9') as case:
                # snapshot for crop/zoom/pan window
                time.sleep(DELAY_TIME * 2)
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                               file_name=Auto_Ground_Truth_Folder + 'G2.2.3.2_Crop_9-16_area_Non_9-16_clip.png')
                logger(crop_zoom_pan_window)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.2.3.2_Crop_9-16_area_Non_9-16_clip.png', crop_zoom_pan_window)
                logger(compare_result)

                case.result = compare_result

            case.result = result1


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        #11/26
        with uuid('e8bae531-e026-4477-b4e4-7cbde9d90193') as case:
            # session 2 : Crop/Zoom
            # case2.6.1 : Reset button
            # import 16:9 video and insert to track1
            time.sleep(DELAY_TIME * 5)
            main_page.set_project_aspect_ratio_16_9()
            time.sleep(DELAY_TIME * 2)
            import_media = media_room_page.import_media_file(Test_Material_Folder + 'Crop_Zoom_Pan/AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')
            logger(import_media)
            media_room_page.high_definition_video_confirm_dialog_click_no()
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')
            main_page.insert_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Select track1
            time.sleep(DELAY_TIME * 2)
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # check [Reset] button status
            reset_btn = crop_zoom_pan_page.get_reset_status()
            logger(reset_btn)

            if reset_btn == False:
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 4)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.6.1_Crop_room_pan_Reset_btn_default_status.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.1_Crop_room_pan_Reset_btn_default_status.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = result and compare_result

        # 11/26
        with uuid('5198b175-0449-4c88-ae7a-104ff4391950') as case:
            # session 2 : Crop/Zoom
            # case2.6.2.1 : Reset button > Modify aspect ratio
            # set aspect ratio to 4:3
            crop_zoom_pan_page.set_AspectRatio_4_3()
            aspect_ratio = crop_zoom_pan_page.get_current_AspectRatio()
            logger(aspect_ratio)

            if aspect_ratio == '4:3':
                result1 = True
                logger(result1)
            else:
                result1 = False
                logger(result1)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.6.2.1_Switch_to_4-3_Before_Reset.png')
            logger(crop_zoom_pan_window)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.2.1_Switch_to_4-3_Before_Reset.png', crop_zoom_pan_window)
            logger(compare_result1)

            # click [Reset] button
            crop_zoom_pan_page.click_reset()

            aspect_ratio1 = crop_zoom_pan_page.get_current_AspectRatio()
            logger(aspect_ratio1)

            if aspect_ratio1 == '16:9':
                result2 = True
                logger(result2)
            else:
                result2 = False
                logger(result2)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.6.2.1_Switch_to_4-3_Then_Reset.png')
            logger(crop_zoom_pan_window)
            compare_result2 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.2.1_Switch_to_4-3_Then_Reset.png', crop_zoom_pan_window)
            logger(compare_result2)

            case.result = result1 and result2 and compare_result1 and compare_result2

        # 11/26
        with uuid('d375a2cd-b478-49ba-be2b-be246640e9cb') as case:
            # session 2 : Crop/Zoom
            # case2.6.2.2 : Reset button > Modify aspect ratio
            # set aspect ratio to 9:16
            crop_zoom_pan_page.set_AspectRatio_9_16()
            aspect_ratio = crop_zoom_pan_page.get_current_AspectRatio()
            logger(aspect_ratio)

            if aspect_ratio == '9:16':
                result1 = True
                logger(result1)
            else:
                result1 = False
                logger(result1)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.6.2.2_Switch_to_9-16_Before_Reset.png')
            logger(crop_zoom_pan_window)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.2.2_Switch_to_9-16_Before_Reset.png', crop_zoom_pan_window)
            logger(compare_result1)

            # click [Reset] button
            crop_zoom_pan_page.click_reset()

            aspect_ratio1 = crop_zoom_pan_page.get_current_AspectRatio()
            logger(aspect_ratio1)

            if aspect_ratio1 == '16:9':
                result2 = True
                logger(result2)
            else:
                result2 = False
                logger(result2)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.6.2.2_Switch_to_9-16_Then_Reset.png')
            logger(crop_zoom_pan_window)
            compare_result2 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.2.2_Switch_to_9-16_Then_Reset.png', crop_zoom_pan_window)
            logger(compare_result2)

            case.result = result1 and result2 and compare_result1 and compare_result2

        # 11/26
        with uuid('ca256f51-8c42-43fb-9b55-fcbf76c12d76') as case:
            # session 2 : Crop/Zoom
            # case2.6.2.3 : Reset button > Modify aspect ratio
            # set aspect ratio to 1:1
            crop_zoom_pan_page.set_AspectRatio_1_1()
            aspect_ratio = crop_zoom_pan_page.get_current_AspectRatio()
            logger(aspect_ratio)

            if aspect_ratio == '1:1':
                result1 = True
                logger(result1)
            else:
                result1 = False
                logger(result1)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.6.2.3_Switch_to_1-1_Before_Reset.png')
            logger(crop_zoom_pan_window)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.2.3_Switch_to_1-1_Before_Reset.png', crop_zoom_pan_window)
            logger(compare_result1)

            # click [Reset] button
            crop_zoom_pan_page.click_reset()

            aspect_ratio1 = crop_zoom_pan_page.get_current_AspectRatio()
            logger(aspect_ratio1)

            if aspect_ratio1 == '16:9':
                result2 = True
                logger(result2)
            else:
                result2 = False
                logger(result2)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.6.2.3_Switch_to_1-1_Then_Reset.png')
            logger(crop_zoom_pan_window)
            compare_result2 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.2.3_Switch_to_1-1_Then_Reset.png', crop_zoom_pan_window)
            logger(compare_result2)

            case.result = result1 and result2 and compare_result1 and compare_result2

        # 11/26
        with uuid('3433f05d-d2ba-4fbb-9d53-13941521ec8f') as case:
            # session 2 : Crop/Zoom
            # case2.6.2.4 : Reset button > Modify aspect ratio
            # set aspect ratio to Freeform
            crop_zoom_pan_page.set_AspectRatio_Freeform()
            aspect_ratio = crop_zoom_pan_page.get_current_AspectRatio()
            logger(aspect_ratio)

            if aspect_ratio == 'Freeform':
                result1 = True
                logger(result1)
            else:
                result1 = False
                logger(result1)

            adjust_width = crop_zoom_pan_page.set_scale_width('0.90')
            logger(adjust_width)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.6.2.4_Switch_to_Freeform_Before_Reset.png')
            logger(crop_zoom_pan_window)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.2.4_Switch_to_Freeform_Before_Reset.png', crop_zoom_pan_window)
            logger(compare_result1)

            # apply all changes to check result on timeline
            crop_zoom_pan_page.click_ok()
            time.sleep(DELAY_TIME*2)

            # snapshot for timeline preview screen
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.6.2.4_Freeform_Timeline_Preview.png')
            logger(crop_zoom_pan_window)
            compare_result2 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.2.4_Freeform_Timeline_Preview.png', crop_zoom_pan_window)
            logger(compare_result2)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # click [Reset] button
            crop_zoom_pan_page.click_reset()

            aspect_ratio1 = crop_zoom_pan_page.get_current_AspectRatio()
            logger(aspect_ratio1)

            if aspect_ratio1 == '16:9':
                result2 = True
                logger(result2)
            else:
                result2 = False
                logger(result2)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.6.2.4_Switch_to_Freeform_Then_Reset.png')
            logger(crop_zoom_pan_window)
            compare_result3 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.2.4_Switch_to_Freeform_Then_Reset.png', crop_zoom_pan_window)
            logger(compare_result3)

            case.result = result1 and result2 and compare_result1 and compare_result2 and compare_result3

        # 11/26
        with uuid('bd190dc9-72aa-4ae9-a0df-e2033d69f43d') as case:
            # session 2 : Crop/Zoom
            # case2.6.6 : Undo
            # Undo last step
            crop_zoom_pan_page.click_undo()

            # check aspect ratio after undo
            aspect_ratio = crop_zoom_pan_page.get_current_AspectRatio()
            logger(aspect_ratio)

            if aspect_ratio == 'Freeform':
                result1 = True
                logger(result1)
            else:
                result1 = False
                logger(result1)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.6.6_Undo.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.6_Undo.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = result1 and compare_result

        # 11/26
        with uuid('31f519cf-d85f-466d-9741-2fb7ef6bbfb9') as case:
            # session 2 : Crop/Zoom
            # case2.6.7 : Redo
            # Undo last step
            redo_operation = crop_zoom_pan_page.click_redo()
            logger(redo_operation)

            # check aspect ratio after redo
            aspect_ratio = crop_zoom_pan_page.get_current_AspectRatio()
            logger(aspect_ratio)

            if aspect_ratio == '16:9':
                result1 = True
                logger(result1)
            else:
                result1 = False
                logger(result1)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.6.7_Redo.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.7_Redo.png', crop_zoom_pan_window)
            logger(compare_result)

            # Undo last step
            undo_operation = crop_zoom_pan_page.click_undo()
            logger(undo_operation)

            # apply all changes to check result on timeline
            #crop_zoom_pan_page.click_ok()
            #time.sleep(DELAY_TIME * 2)

            case.result = result1 and compare_result
        '''
        # 11/26
        with uuid('5b1ec26f-95b4-48c5-9930-8d7a88b726ad') as case:
            # session 2 : Crop/Zoom
            # case2.6.3 : Add keyframe > Reset
            # Undo last step
            crop_zoom_pan_page.click_redo()

            # seek by timecode and then add keyframe
            crop_zoom_pan_page.set_timecode('00_00_06_04')
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_page.keyframe.add()

            # adjust width
            crop_zoom_pan_page.set_scale_width('0.7')

            # seek by timecode
            crop_zoom_pan_page.set_timecode('00_00_04_15')
            time.sleep(DELAY_TIME * 2)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.6.3_add_keyframe.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.3_add_keyframe.png', crop_zoom_pan_window)
            logger(compare_result)

            # click [Reset] button
            crop_zoom_pan_page.click_reset()

            aspect_ratio1 = crop_zoom_pan_page.get_current_AspectRatio()
            logger(aspect_ratio1)

            if aspect_ratio1 == '16:9':
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 5)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.6.3_Add_Keyframe_Then_Reset.png')
            logger(crop_zoom_pan_window)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.3_Add_Keyframe_Then_Reset.png', crop_zoom_pan_window)
            logger(compare_result1)

            case.result = result and compare_result and compare_result1
        '''

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        #12/4
        with uuid('5f54bb5f-0113-4e58-b701-19714f4127e4') as case:
            # session 2 : Crop/zoom
            # case2.1.5 : set aspect ratio to Freeform
            time.sleep(DELAY_TIME * 5)
            import_media = media_room_page.import_media_file(
                Test_Material_Folder + 'Crop_Zoom_Pan/AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')
            logger(import_media)
            media_room_page.high_definition_video_confirm_dialog_click_no()
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')
            main_page.insert_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # set aspect ratio to Freeform
            crop_zoom_pan_page.set_AspectRatio_Freeform()

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.1.5_AspectRation_Freeform.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.5_AspectRation_Freeform.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 12/4
        with uuid('2e7a7abc-634f-4d75-9c13-60b128b7f434') as case:
            # session 2 : Crop/zoom
            # case2.2.5.1 : Crop freeform area with non 16:9 clip
            # adjust width / height by value
            #crop_zoom_pan_page.set_scale_width(0.530) --> exception
            crop_zoom_pan_page.set_scale_width_slider(0.3)
            crop_zoom_pan_page.set_scale_height_slider(0.5)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.5.1_Crop_Freeform_area_free_area.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.2.5.1_Crop_Freeform_area_free_area.png', crop_zoom_pan_window)
            logger(compare_result)

            # seek to early time frame
            crop_zoom_pan_page.set_timecode('00_00_03_00')
            time.sleep(DELAY_TIME)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.5.1_Crop_Freeform_area_free_area_seek.png')
            logger(crop_zoom_pan_window)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.2.5.1_Crop_Freeform_area_free_area_seek.png', crop_zoom_pan_window)
            logger(compare_result1)

            # click [Ok] to apply all settings
            crop_zoom_pan_page.click_ok()
            time.sleep(DELAY_TIME*2)

            # seek to specific time code
            time.sleep(DELAY_TIME)
            set_timecode = main_page.set_timeline_timecode('00_00_03_20')
            logger(set_timecode)

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.2.5.1_Crop_Freeform_area_free_area_timeline_preview.png')
            logger(preview_wnd)
            compare_result2 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.2.5.1_Crop_Freeform_area_free_area_timeline_preview.png',
                preview_wnd)
            logger(compare_result2)

            case.result = compare_result and compare_result1 and compare_result2

        # 12/4
        with uuid('267baa53a-9c94-4430-8e24-3fb3d8afd592') as case:
            # session 2 : Crop/zoom
            # case2.4.1 : Add Keyframe at current location
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # check if current time code is 00:00:03:20
            timecode = crop_zoom_pan_page.get_timecode()
            logger(timecode)
            if timecode == '00;00;03;20':
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            # Go to next frame (add this step to work-around bug. we need to remove it after bug is solved.)
            crop_zoom_pan_page.preview_operation('Next_Frame')

            # add keyframe at current location
            add_keyframe = crop_zoom_pan_page.keyframe.add() # bug is found : add keyframe... isn't enabled in this case
            logger(add_keyframe)

            # set rotation degree
            crop_zoom_pan_page.set_rotation('50')

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.4.1_Add_Keyframe_At_Current_Location.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.4.1_Add_Keyframe_At_Current_Location.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = add_keyframe and result and compare_result
            case.fail_log = "*Bug Code: VDE213607-0002*"

        # 12/4
        with uuid('157462f4-7121-4afd-b202-11f63bfcc0b2') as case:
            # session 2 : Crop/zoom
            # case2.4.2 : Remove Keyframe at current location
            # seek by timecode
            crop_zoom_pan_page.set_timecode('00_00_03_21')
            time.sleep(DELAY_TIME * 2)

            # remove keyframe at current location
            remove_keyframe = crop_zoom_pan_page.keyframe.remove()
            logger(remove_keyframe)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.4.2_Remove_Keyframe_At_Current_Location.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.4.2_Remove_Keyframe_At_Current_Location.png', crop_zoom_pan_window)
            logger(compare_result)

            # add keyframe at current location
            add_keyframe = crop_zoom_pan_page.keyframe.add()
            logger(add_keyframe)

            # set rotation degree
            crop_zoom_pan_page.set_rotation('45')

            case.result = remove_keyframe and compare_result

        # 12/4
        with uuid('77aea94d-bffc-4dbc-acdd-17a1f6ea6148') as case:
            # session 2 : Crop/zoom
            # case2.4.3 : Select Previous Keyframe
            # seek by timecode
            #crop_zoom_pan_page.set_timecode('00_00_03_21')
            #time.sleep(DELAY_TIME * 2)

            # select previous keyframe
            crop_zoom_pan_page.keyframe.select_previous()

            # get timecode
            timecode = crop_zoom_pan_page.get_timecode()
            logger(timecode)
            if timecode == '00;00;00;00':
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.4.3_Select_Previous_Keyframe.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.4.3_Select_Previous_Keyframe.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = result and compare_result

        # 12/4
        with uuid('6a3eca4b-6f37-4db0-94be-020185b0e313') as case:
            # session 2 : Crop/zoom
            # case2.4.4 : Select Next Keyframe
            # seek by timecode
            #crop_zoom_pan_page.set_timecode('00_00_03_21')
            #time.sleep(DELAY_TIME * 2)

            # select next keyframe
            crop_zoom_pan_page.keyframe.select_next()

            # get timecode
            timecode = crop_zoom_pan_page.get_timecode()
            logger(timecode)
            if timecode == '00;00;03;21':
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            if result:
                # snapshot for crop/zoom/pan window
                time.sleep(DELAY_TIME * 2)
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                                file_name=Auto_Ground_Truth_Folder + 'G2.4.4_Select_Next_Keyframe.png')
                logger(crop_zoom_pan_window)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.4.4_Select_Next_Keyframe.png', crop_zoom_pan_window)
                logger(compare_result)

            case.result = result and compare_result

        # 12/4
        with uuid('ca53dd88-6e58-457f-bc63-2c8b24423c67') as case:
            # session 2 : Crop/zoom
            # case2.4.5.1 : Duplicate previous keyframe
            # seek by timecode
            crop_zoom_pan_page.set_timecode('00_00_05_15')
            time.sleep(DELAY_TIME * 2)

            # duplicate previous keyframe
            crop_zoom_pan_page.keyframe.duplicate_previous()

            # snapshot for crop/zoom/pan window
            main_page.move_mouse_to_0_0()
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.4.5.1_Duplicate_Previous_Keyframe.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.4.5.1_Duplicate_Previous_Keyframe.png', crop_zoom_pan_window)
            logger(compare_result)

            # adjust width
            crop_zoom_pan_page.set_scale_width('0.8')

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.4.5.1_Adjust_width.png')
            logger(crop_zoom_pan_window)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.4.5.1_Adjust_width.png', crop_zoom_pan_window)
            logger(compare_result1)

            case.result = compare_result and compare_result1

        # 12/4
        with uuid('baa697d3-caf0-418b-bd9f-fc1584dd9a23') as case:
            # session 2 : Crop/zoom
            # case2.4.5.2 : Duplicate next keyframe
            # seek by timecode
            crop_zoom_pan_page.set_timecode('00_00_04_05')
            time.sleep(DELAY_TIME * 2)

            # duplicate previous keyframe
            crop_zoom_pan_page.keyframe.duplicate_previous()

            # snapshot for crop/zoom/pan window
            main_page.move_mouse_to_0_0()
            time.sleep(DELAY_TIME * 3)

            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.4.5.2_Duplicate_Next_Keyframe.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.4.5.2_Duplicate_Next_Keyframe.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 12/4
        with uuid('643eade1-9f81-44b0-83e3-1b6c8a1fcc49') as case:
            # session 2 : Crop/zoom
            # case2.2.5.2 : Crop with size change and rotate
            # seek by timecode
            crop_zoom_pan_page.set_timecode('00_00_10_05')
            time.sleep(DELAY_TIME * 2)

            # adjust width
            crop_zoom_pan_page.set_scale_width('0.8')

            # set rotation degree
            crop_zoom_pan_page.set_rotation('120')

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.5.2_Adjust_width_and_rotation.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.2.5.2_Adjust_width_and_rotation.png', crop_zoom_pan_window)
            logger(compare_result)

            case.result = compare_result

        # 12/4
        with uuid('2a87c9c2-f326-4eec-93aa-62d940456ef1') as case:
            # session 2 : Crop/zoom
            # case2.4.6 : Keyframe with rotate, move, and size change
            # seek by timecode
            set_time = crop_zoom_pan_page.set_timecode('00_00_20_00')
            logger(set_time)
            time.sleep(DELAY_TIME * 2)

            # adjust width
            crop_zoom_pan_page.set_scale_width('1.0')
            time.sleep(DELAY_TIME)

            # set rotation degree
            crop_zoom_pan_page.set_rotation('180')
            time.sleep(DELAY_TIME)

            # adjust position by value
            crop_zoom_pan_page.set_position_x('0.7')
            time.sleep(DELAY_TIME)
            crop_zoom_pan_page.set_position_y('0.6')
            time.sleep(DELAY_TIME)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.4.6_keyframe_rotation_position change.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.4.6_keyframe_rotation_position change.png', crop_zoom_pan_window)
            logger(compare_result)

            # seek by timecode
            crop_zoom_pan_page.set_timecode('00_00_16_00')
            time.sleep(DELAY_TIME * 2)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.4.6_Seek_to_16th_sec.png')
            logger(crop_zoom_pan_window)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.4.6_Seek_to_16th_sec.png', crop_zoom_pan_window)
            logger(compare_result1)

            case.result = compare_result and compare_result1

        # 12/5
        with uuid('d7ee34e4-6454-4b83-b6f6-4aaf941a2674') as case:
            # session 2 : Crop/Zoom
            # case2.3.5 : Undo
            # Undo last step
            exe_undo = crop_zoom_pan_page.click_undo()
            logger(exe_undo)
            time.sleep(DELAY_TIME)

            # check timecode
            timecode = crop_zoom_pan_page.get_timecode()
            logger(timecode)
            if timecode == '00;00;20;00':
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            if result:
                # snapshot for crop/zoom/pan window
                time.sleep(DELAY_TIME * 2)
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                                file_name=Auto_Ground_Truth_Folder + 'G2.3.5_Undo_Editing.png')
                logger(crop_zoom_pan_window)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.3.5_Undo_Editing.png', crop_zoom_pan_window)
                logger(compare_result)

            case.result = result and compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        #12/10
        with uuid('49a56d2e-159b-4881-9efd-0e975ff18246') as case:
            # session 2 : Crop/zoom
            # case.2.5.1 : Rotation Settings > Custom Settings (360~-360)
            time.sleep(DELAY_TIME * 5)
            import_media = media_room_page.import_media_file(
                Test_Material_Folder + 'Crop_Zoom_Pan/AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')
            logger(import_media)
            media_room_page.high_definition_video_confirm_dialog_click_no()
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')
            main_page.insert_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # set rotation to 220
            rotation_degree = crop_zoom_pan_page.set_rotation('220')
            logger(rotation_degree)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.5.1_rotation_degree_220.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.5.1_rotation_degree_220.png', crop_zoom_pan_window)
            logger(compare_result)

            # set rotation to -220
            rotation_degree = crop_zoom_pan_page.set_rotation('-220')
            logger(rotation_degree)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.5.1_rotation_degree_-220.png')
            logger(crop_zoom_pan_window)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.5.1_rotation_degree_-220.png', crop_zoom_pan_window)
            logger(compare_result1)

            case.result = compare_result and compare_result1

        #12/10
        with uuid('db31d023-9962-4932-a762-73a4bab5ee24') as case:
            # session 2 : Crop/zoom
            # case.2.5.2 : Rotation Settings > ▲/▼ button
            for i in range(2):
                crop_zoom_pan_page.click_rotation_arrow('up')

            rotation_degree = crop_zoom_pan_page.get_rotation()
            logger(rotation_degree)
            if rotation_degree == '-218':
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            if result:
                # snapshot for crop/zoom/pan window
                time.sleep(DELAY_TIME * 2)
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.5.2_rotation_up_arrow.png')
                logger(crop_zoom_pan_window)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.5.2_rotation_up_arrow.png', crop_zoom_pan_window)
                logger(compare_result1)

            for i in range (5):
                crop_zoom_pan_page.click_rotation_arrow('down')

            rotation_degree1 = crop_zoom_pan_page.get_rotation()
            logger(rotation_degree1)
            if rotation_degree1 == '-223':
                result1 = True
                logger(result1)
            else:
                result1 = False
                logger(result1)

            if result1:
                # snapshot for crop/zoom/pan window
                time.sleep(DELAY_TIME * 2)
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                                file_name=Auto_Ground_Truth_Folder + 'G2.5.2_rotation_down_arrow.png')
                logger(crop_zoom_pan_window)
                compare_result2 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.5.2_rotation_down_arrow.png', crop_zoom_pan_window)
                logger(compare_result2)

            case.result = compare_result1 and compare_result2 and result and result1

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        #1/15
        with uuid('5b1ec26f-95b4-48c5-9930-8d7a88b726ad') as case:
            # session 2 : Crop/Zoom
            # case2.6.3 : Apply Keyframe > Click Reset button
            # import 16:9 video and insert to track1
            time.sleep(DELAY_TIME * 5)
            main_page.set_project_aspect_ratio_16_9()
            import_media = media_room_page.import_media_file(Test_Material_Folder + 'Crop_Zoom_Pan/AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')
            logger(import_media)
            media_room_page.high_definition_video_confirm_dialog_click_no()
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')
            main_page.insert_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # Seek > Adjust parameters to apply keyframe
            crop_zoom_pan_page.set_timecode('00_00_13_00')
            time.sleep(DELAY_TIME * 2)
            rotation = crop_zoom_pan_page.set_rotation('130')
            logger(rotation)
            time.sleep(DELAY_TIME * 2)

            # snapshot
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.6.3_apply_keyframe_before_reset.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.3_apply_keyframe_before_reset.png', crop_zoom_pan_window)
            logger(compare_result)

            # check [Reset] button status
            reset_btn = crop_zoom_pan_page.get_reset_status()
            logger(reset_btn)

            if reset_btn == True:
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            # click [Reset] button
            click_reset = crop_zoom_pan_page.click_reset()
            logger(click_reset)
            time.sleep(DELAY_TIME * 2)

            if click_reset:
                # snapshot
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.6.3_apply_keyframe_after_reset.png')
                logger(crop_zoom_pan_window)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.3_apply_keyframe_after_reset.png', crop_zoom_pan_window)
                logger(compare_result1)

            case.result = result and compare_result and compare_result1

        #1/15
        with uuid('6a85cb6b-dba4-4135-92c1-17821b99ab1f') as case:
            # session 2 : Crop/Zoom
            # case2.6.4 : Modify Keyframe > Click Reset button
            # undo last step
            crop_zoom_pan_page.click_undo()
            time.sleep(DELAY_TIME*2)

            # Seek > modify parameters to adjust keyframe
            crop_zoom_pan_page.set_timecode('00_00_13_00')
            time.sleep(DELAY_TIME * 2)
            rotation = crop_zoom_pan_page.set_rotation('190')
            logger(rotation)
            time.sleep(DELAY_TIME * 2)

            # snapshot
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.6.4_modify_keyframe_before_reset.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.4_modify_keyframe_before_reset.png', crop_zoom_pan_window)
            logger(compare_result)

            # check [Reset] button status
            reset_btn = crop_zoom_pan_page.get_reset_status()
            logger(reset_btn)

            if reset_btn == True:
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            # click [Reset] button
            click_reset = crop_zoom_pan_page.click_reset()
            logger(click_reset)
            time.sleep(DELAY_TIME * 2)

            if click_reset:
                # snapshot
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.6.4_modify_keyframe_after_reset.png')
                logger(crop_zoom_pan_window)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.4_modify_keyframe_after_reset.png', crop_zoom_pan_window)
                logger(compare_result1)

            case.result = result and compare_result1


        #1/15
        with uuid('b0acf0b5-7ef4-49b3-9637-31f5df148bbb') as case:
            # session 2 : Crop/Zoom
            # case2.6.5 : Remove all Keyframe > Check Reset button
            # undo last step
            crop_zoom_pan_page.click_undo()
            time.sleep(DELAY_TIME*2)

            # modify keyframe
            # Seek > Adjust parameters to apply keyframe
            crop_zoom_pan_page.set_timecode('00_00_13_00')
            time.sleep(DELAY_TIME * 2)
            remove_keyframe = crop_zoom_pan_page.keyframe.remove()
            logger(remove_keyframe)
            time.sleep(DELAY_TIME * 2)

            # check [Reset] button status
            reset_btn = crop_zoom_pan_page.get_reset_status()
            logger(reset_btn)

            if reset_btn == False:
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            if result:
                # snapshot
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.reset,
                                                                file_name=Auto_Ground_Truth_Folder + 'G2.6.5_Check_Reset_Button_after_Remove_all_keyframe.png')
                logger(crop_zoom_pan_window)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.5_Check_Reset_Button_after_Remove_all_keyframe.png', crop_zoom_pan_window)
                logger(compare_result)

            case.result = result and compare_result

        # 1/15
        with uuid('781f170a-4480-4bf6-b145-1295f2c2333f') as case:
            # session 2 : Crop/Zoom
            # case2.6.8 : Do some editing and Click "OK" > Enter Crop/Zoom/Pan dialog again > Click Reset button
            # undo last step
            crop_zoom_pan_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # click [OK] to leave crop & zoom & pan page
            crop_zoom_pan_page.click_ok()
            time.sleep(DELAY_TIME * 2)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # check [Reset] button status
            reset_btn = crop_zoom_pan_page.get_reset_status()
            logger(reset_btn)

            if reset_btn == True:
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            # click [Reset] button
            click_reset = crop_zoom_pan_page.click_reset()
            logger(click_reset)
            time.sleep(DELAY_TIME * 2)

            if click_reset:
                # snapshot
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.6.8_Reset_btn_Status_After_re-enter_Crop_Zoom_Pan.png')
                logger(crop_zoom_pan_window)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.8_Reset_btn_Status_After_re-enter_Crop_Zoom_Pan.png', crop_zoom_pan_window)
                logger(compare_result)

            # click [OK] to leave crop & zoom & pan page
            crop_zoom_pan_page.click_ok()
            time.sleep(DELAY_TIME * 2)

            case.result = result and compare_result

        # 1/15
        with uuid('3fbc0263-a4f3-4b52-9b66-ee2248ae2f56') as case:
            # session 2 : Crop/Zoom
            # case2.6.9 : Do some editing and Click "Cancel" > Enter Crop/Zoom/Pan dialog again > Check Reset button
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # Seek > Adjust parameters to apply keyframe
            crop_zoom_pan_page.set_timecode('00_00_11_00')
            time.sleep(DELAY_TIME * 2)
            rotation = crop_zoom_pan_page.set_rotation('120')
            logger(rotation)
            time.sleep(DELAY_TIME * 2)

            # click [Cancel] to leave crop & zoom & pan page
            crop_zoom_pan_page.click_cancel()
            time.sleep(DELAY_TIME * 2)

            # press [Enter]
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 2)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # check [Reset] button status
            reset_btn = crop_zoom_pan_page.get_reset_status()
            logger(reset_btn)

            if reset_btn == True:
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            if result:
                # snapshot
                crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.reset,
                                                                file_name=Auto_Ground_Truth_Folder + 'G2.6.9_Check_Reset_Button_after_re-enter_Crop_Zoom_Pan.png')
                logger(crop_zoom_pan_window)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9_Check_Reset_Button_after_re-enter_Crop_Zoom_Pan.png',
                    crop_zoom_pan_window)
                logger(compare_result)

            case.result = result and compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_10(self):
        #1/15
        with uuid('c7f0aab1-f9c4-4982-b415-1bf61f31d1ad') as case:
            # session 2 : Crop/Zoom
            # case2.7 : Cancel/OK/X button
            # case2.7.2.1 : Without editing > Click [Cancel]
            # import 16:9 video and insert to track1
            time.sleep(DELAY_TIME * 5)
            main_page.set_project_aspect_ratio_16_9()
            import_media = media_room_page.import_media_file(Test_Material_Folder + 'Crop_Zoom_Pan/AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')
            logger(import_media)
            media_room_page.high_definition_video_confirm_dialog_click_no()
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')
            main_page.insert_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # Click [Cancel]
            cancel_result = crop_zoom_pan_page.click_cancel()
            logger(cancel_result)
            time.sleep(DELAY_TIME * 2)

            # check if crop_zoom_pan is still alive
            if crop_zoom_pan_page.is_not_exist(L.crop_zoom_pan.window) == True:
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            case.result = result

        # 1/15
        with uuid('644f3534-63f0-4dff-91c5-8d9ccd5daa32') as case:
            # session 2 : Crop/Zoom
            # case2.7 : Cancel/OK/X button
            # case2.7.3.1 : Without editing > Click [X]
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # Click [Close] to close "crop/zoom/pan"
            crop_zoom_pan_page.close_window()
            time.sleep(DELAY_TIME * 2)
            check_result = crop_zoom_pan_page.is_not_exist(L.crop_zoom_pan.window)
            logger(check_result)

            # check if crop_zoom_pan is still alive
            if crop_zoom_pan_page.is_not_exist(L.crop_zoom_pan.window) == True:
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            case.result = result

        # 1/15
        with uuid('52e1835b-8114-4bdd-966a-df1c650f6f3b') as case:
            # session 2 : Crop/Zoom
            # case2.7 : Cancel/OK/X button
            # case2.7.2.2 : Editing in crop/zoom/pan > Click [Cancel]
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # Seek > rotate object
            crop_zoom_pan_page.set_timecode('00_00_13_00')
            time.sleep(DELAY_TIME * 2)
            rotation = crop_zoom_pan_page.set_rotation('190')
            logger(rotation)
            time.sleep(DELAY_TIME * 3)

            # Click [Cancel]
            cancel_result = crop_zoom_pan_page.click_cancel()
            logger(cancel_result)
            time.sleep(DELAY_TIME * 2)

            # snapshot
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.reset,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.7.2.2_Click_Cancel_After_Editing.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.7.2.2_Click_Cancel_After_Editing.png',
                crop_zoom_pan_window)
            logger(compare_result)

            #click [Enter]
            main_page.press_enter_key()
            time.sleep(DELAY_TIME*2)

            case.result = compare_result

        # 1/15
        with uuid('ac09441e-169d-4f2d-be0f-fd9c959c3df8') as case:
            # session 2 : Crop/Zoom
            # case2.7 : Cancel/OK/X button
            # case2.7.3.2 : Editing in crop/zoom/pan > Click [X]
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # Seek > rotate object
            crop_zoom_pan_page.set_timecode('00_00_10_00')
            time.sleep(DELAY_TIME * 2)
            rotation = crop_zoom_pan_page.set_rotation('100')
            logger(rotation)
            time.sleep(DELAY_TIME * 2)

            # Click [Cancel]
            cancel_result = crop_zoom_pan_page.click_cancel()
            logger(cancel_result)
            time.sleep(DELAY_TIME * 2)

            # snapshot
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.reset,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.7.3.2_Click_X_After_Editing.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.7.3.2_Click_X_After_Editing.png',
                crop_zoom_pan_window)
            logger(compare_result)

            # click [Enter]
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 2)

            case.result = compare_result

        # 1/15
        with uuid('3ec9fe07-63d6-4165-9dc8-198034394c2f') as case:
            # session 2 : Crop/Zoom
            # case2.7 : Cancel/OK/X button
            # case2.7.1 : Editing in crop/zoom/pan > Click [OK]
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 7)

            # Seek > rotate object
            crop_zoom_pan_page.set_timecode('00_00_00_00')
            time.sleep(DELAY_TIME * 2)
            rotation = crop_zoom_pan_page.set_rotation('-80')
            logger(rotation)
            time.sleep(DELAY_TIME * 2)

            # Click [OK]
            apply_result = crop_zoom_pan_page.click_ok()
            logger(apply_result)
            time.sleep(DELAY_TIME * 2)

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.7.1_Apply_Rotation.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.7.1_Apply_Rotation.png', preview_wnd, similarity=0.85)
            logger(compare_result)

            case.result = compare_result
