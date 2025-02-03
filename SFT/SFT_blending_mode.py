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
# Modify locator to hardcode_0408
#from pages.locator.hardcode_0408 import locator as L

#for update_report_info
from globals import *



# read PDR cap >>
app = SimpleNamespace(**PDR_cap)
# read PDR cap <<

# create driver & page >>
mac = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mac)
#base_page = PageFactory().get_page_object('base_page', mac)
effect_room_page = PageFactory().get_page_object('effect_room_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page',mac)
pip_room_page = PageFactory().get_page_object('pip_room_page',mac)
tips_area_page = PageFactory().get_page_object('tips_area_page',mac)
timeline_operation_page = PageFactory().get_page_object('tips_area_page',mac)
keyframe_room_page = PageFactory().get_page_object('keyframe_room_page',mac)
playback_window_page = PageFactory().get_page_object('playback_window_page',mac)
blending_mode_page = PageFactory().get_page_object('blending_mode_page',mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Blending Mode.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<



# For Ground Truth / Test Material folder
#======= (Mac Mini)
Ground_Truth_Folder = app.ground_truth_root + '/Blending_Mode/' #'/Users/cl/Desktop/AT/PDR_SFT_fromSVN/SFT/GroundTruth/Color_LUT/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Blending_Mode/' #'/Users/cl/Desktop/AT/PDR_SFT_fromSVN/SFT/ATGroundTruth/Color_LUT/'
Test_Material_Folder = app.testing_material #'/Users/cl/Desktop/AT/PDR_SFT_fromSVN/Material/'

#======= (iMac27")
#Ground_Truth_Folder = '/Users/qadf-imac27/Desktop/AT/SFT/GroundTruth/Color_LUT/'
#Auto_Ground_Truth_Folder = '/Users/qadf-imac27/Desktop/AT/SFT/ATGroundTruth/Color_LUT/'
#Test_Material_Folder = '/Users/qadf-imac27/Desktop/AT/Material/'

#======= (Ernesto)
#Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto/SFT/GroundTruth/Media_Room/'
#Auto_Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto/SFT/ATGroundTruth/Media_Room/'
#Test_Material_Folder = '/Users/clt/Desktop/Ernesto/Material/'


DELAY_TIME = 1



'''
@pytest.fixture(scope="module", autouse= True)
def init():
    yield
    report.export()
    report.show()
'''




class Test_Blending_Mode():

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
        print('setup class - enter')
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('Blending_Mode')


    @classmethod
    def teardown_class(cls):

        #print('teardown_class - export report')
        #report.export()
        #print(
            #f"mask designer result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        #update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           #report.get_ovinfo('skip'),
                           #report.get_ovinfo('duration'))
        #report.show()
        logger('teardown_class - export report')
        report.export()
        logger(
            f"Blending Mode result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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


    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_1_1(self):
        #7/15
        with uuid("0e880262-12c9-4f3c-ba51-51c06f6d5251") as case:
            # case1.1.1 : Enter Blending Mode dialog via tools
            # select a photo and insert to track1
            time.sleep(8)
            #main_page.enter_room(0)
            #time.sleep(DELAY_TIME*2)
            main_page.insert_media('Landscape 01.jpg')
            time.sleep(DELAY_TIME*3)

            # select track2 and then inserting another photo to timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            main_page.insert_media('Sport 01.jpg')
            timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            #click_tools = tips_area_page.tools.click_btn()
            #logger(click_tools)
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # click keyboard hotkey [ESC] to exit Blending mode dialogue
            tips_area_page.press_esc_key()

            # check result
            case.result = blending_mode_diag

        #8/5
        with uuid("d9ea79ee-3a2e-4bea-9a74-5391a10d40e3") as case:
            # case1.1.2 : Enter Blending Mode via context menu

            # select track2 and then inserting another photo to timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            #main_page.insert_media('Sport 01.jpg')
            timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
            logger(timeline_media)

            # Check applied blending mode via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Darken')
            logger(context_menu)

            # snapshot for context menu
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                              file_name=Auto_Ground_Truth_Folder + 'G1.1.2_SetBlendingMode_Darken.png')
            logger(preview_wnd)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G1.1.2_SetBlendingMode_Darken.png',
                                                        preview_wnd)
            logger(compare_result1)

            case.result = compare_result1
            logger(case.result)

        # 8/13
        with uuid("0d5916b5-29af-4e4b-a64f-d97fa27b91a3") as case:
            # case2.1.27 : Enter Blending Mode dialog and then [Cancel]

            # select track2 and target photo on timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            #main_page.insert_media('Sport 01.jpg')
            timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            # click_tools = tips_area_page.tools.click_btn()
            # logger(click_tools)
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Hue"
            blending_mode_1 = blending_mode_page.set_blending_mode('Hue')
            logger(blending_mode_1)
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.27_SetBlendingMode_Hue.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.27_SetBlendingMode_Hue.png',
                                                     preview_wnd)
            logger(compare_result)

            # click [Cancel] to exit Blending mode dialogue
            blending_mode_page.click_cancel()
            time.sleep(DELAY_TIME*3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.27_SetBlendingMode_Hue_cancel.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.27_SetBlendingMode_Hue_cancel.png',
                                                    preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1


    @exception_screenshot
    def test1_1_1_2(self):
        #7/15
        with uuid("a6ca128f-83ac-4db2-8937-aabae5c53e82") as case:
            # case2.1.1 : 1st time to enter Blending mode dialogue and the default is set to "Normal"
            # select a photo and insert to track1
            time.sleep(8)
            #main_page.enter_room(0)
            #time.sleep(DELAY_TIME*2)
            main_page.insert_media('Landscape 01.jpg')
            time.sleep(DELAY_TIME*3)

            # select track2 and then inserting another photo to timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            main_page.insert_media('Sport 01.jpg')
            timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            #click_tools = tips_area_page.tools.click_btn()
            #logger(click_tools)
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)
            time.sleep(DELAY_TIME * 3)
            blending_mode_diag1 = tips_area_page.snapshot(locator=L.tips_area.window.blending_mode,
                                     file_name=Auto_Ground_Truth_Folder + 'G2.1.1_Blending_mode.png')

            logger(blending_mode_diag1)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.1_Blending_mode.png', blending_mode_diag1)
            logger(compare_result)

            with uuid("fa4f54dc-5d8d-468e-9d5a-daf3409e5ecb") as case:
                # case2.1.28 : Click [ESC] to close "Blending Mode" dialogue
                # click keyboard hotkey [ESC] to exit Blending mode dialogue
                dialogue = L.tips_area.window.blending_mode
                logger(dialogue)
                tips_area_page.press_esc_key()
                time.sleep(2)
                if tips_area_page.is_exist(dialogue) == False:
                    case.result = True
                else:
                    case.result = False

            # check result
            case.result = blending_mode_diag and compare_result
            logger(case.result)

        # 8/13
        with uuid("2a28c1ea-8006-472b-ac23-9dad832c3cb0") as case:
            # case2.1.4 : Enter Blending Mode dialog and set to "Darken"

            # select track2 and target photo on timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            #main_page.insert_media('Sport 01.jpg')
            timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Hue"
            blending_mode = blending_mode_page.set_blending_mode('Darken')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.4_SetBlendingMode_Darken.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.4_SetBlendingMode_Darken.png',
                                                     preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.4_SetBlendingMode_Darken_Applied.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.4_SetBlendingMode_Darken_Applied.png',
                                                    preview_wnd1)
            logger(compare_result1)

            #8/13
            with uuid("190b3b62-9622-4a16-b01c-8fd267c40808") as case:
                # case2.1.2 : 2nd time to Enter "Blending Mode" dialogue and should keep previous setting
                # Enter Blending mode via tools
                blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
                logger(blending_mode_diag)
                time.sleep(3)

                # snapshot
                Bledning_diag = tips_area_page.snapshot(locator=L.blending_mode.main_window,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.1.2_Check_BlendingModeDialogue.png')
                logger(Bledning_diag)
                compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.2_Check_BlendingModeDialogue.png',
                                                        Bledning_diag)
                logger(compare_result2)

                # click keyboard hotkey [ESC] to exit Blending mode dialogue
                tips_area_page.press_esc_key()

                case.result = compare_result2

            # check result
            case.result = compare_result and compare_result1

        # 8/19
        with uuid("0ea214d1-7086-4ed5-bffe-b85e764d2924") as case:
            # case2.1.3 : Enter Blending Mode dialog and set to "Normal"

            # select track2 and target photo on timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            # main_page.insert_media('Sport 01.jpg')
            timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Normal"
            blending_mode = blending_mode_page.set_blending_mode('Normal')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.1.3_SetBlendingMode_Normal.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.3_SetBlendingMode_Normal.png',
                                                        preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                       file_name=Auto_Ground_Truth_Folder + 'G2.1.3_SetBlendingMode_Normal_Applied.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.3_SetBlendingMode_Normal_Applied.png',
                    preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1

        # 8/19
        with uuid("3e7f8e11-cc49-46ce-b557-9f37cf30dad2") as case:
            # case2.1.5 : Enter Blending Mode dialog and set to "Multiply"

            # select track2 and target photo on timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            # main_page.insert_media('Sport 01.jpg')
            timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Multiply"
            blending_mode = blending_mode_page.set_blending_mode('Multiply')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.1.5_SetBlendingMode_Multiply.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.5_SetBlendingMode_Multiply.png',
                                                        preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                       file_name=Auto_Ground_Truth_Folder + 'G2.1.5_SetBlendingMode_Multiply_Applied.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.5_SetBlendingMode_Multiply_Applied.png',
                    preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1

        # 8/19
        with uuid("faa241fd-b090-40cc-a8c6-5d77b4db8192") as case:
            # case2.1.6 : Enter Blending Mode dialog and set to "Lighten"

            # select track2 and target photo on timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            # main_page.insert_media('Sport 01.jpg')
            timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Lighten"
            blending_mode = blending_mode_page.set_blending_mode('Lighten')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.6_SetBlendingMode_Lighten.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.6_SetBlendingMode_Lighten.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.6_SetBlendingMode_Lighten_Applied.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.6_SetBlendingMode_Lighten_Applied.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1

        # 8/19
        with uuid("c0f8ab17-3ff1-4f27-be14-87ceb326c316") as case:
            # case2.1.7 : Enter Blending Mode dialog and set to "Screen"

            # select track2 and target photo on timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            # main_page.insert_media('Sport 01.jpg')
            timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Screen"
            blending_mode = blending_mode_page.set_blending_mode('Screen')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.7_SetBlendingMode_Screen.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.7_SetBlendingMode_Screen.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.7_SetBlendingMode_Screen_Applied.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.7_SetBlendingMode_Screen_Applied.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1

        # 8/19
        with uuid("8d691f8f-a6f0-4b84-893a-c30ffefb0cd3") as case:
            # case2.1.8 : Enter Blending Mode dialog and set to "Overlay"

            # select track2 and target photo on timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            # main_page.insert_media('Sport 01.jpg')
            timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Overlay"
            blending_mode = blending_mode_page.set_blending_mode('Overlay')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.8_SetBlendingMode_Overlay.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.8_SetBlendingMode_Overlay.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.8_SetBlendingMode_Overlay_Applied.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.8_SetBlendingMode_Overlay_Applied.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1

        # 8/19
        with uuid("f817dc37-d0d2-461d-bfac-8b1c412ce729") as case:
            # case2.1.9 : Enter Blending Mode dialog and set to "Difference"

            # select track2 and target photo on timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            # main_page.insert_media('Sport 01.jpg')
            timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Difference"
            blending_mode = blending_mode_page.set_blending_mode('Difference')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.9_SetBlendingMode_Difference.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.9_SetBlendingMode_Difference.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.9_SetBlendingMode_Difference_Applied.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.9_SetBlendingMode_Difference_Applied.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1

        # 8/19
        with uuid("99a2bde2-05bd-4cf3-a3de-432bd68901c1") as case:
            # case2.1.10 : Enter Blending Mode dialog and set to "Hue"

            # select track2 and target photo on timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            # main_page.insert_media('Sport 01.jpg')
            timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Hue"
            blending_mode = blending_mode_page.set_blending_mode('Hue')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.10_SetBlendingMode_Hue.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.10_SetBlendingMode_Hue.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.10_SetBlendingMode_Hue_Applied.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.10_SetBlendingMode_Hue_Applied.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1




    @exception_screenshot
    def test1_1_1_3(self):
        #7/16
        with uuid("b0523549-7f09-4f84-b1fd-2c82e824ba8c") as case:
            # case2.2.1 : Check if default ticked setting is "Normal" in context menu
            time.sleep(8)
            #main_page.enter_room(0)
            #time.sleep(DELAY_TIME*2)
            main_page.insert_media('Landscape 01.jpg')
            time.sleep(DELAY_TIME*3)

            # select track2 and then inserting another photo to timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            main_page.insert_media('Sport 01.jpg')
            timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
            logger(timeline_media)

            # Check applied blending mode via context menu
            #click_tools = tips_area_page.tools.click_btn()
            #logger(click_tools)
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode')
            logger(context_menu)

            # send right key to submenu
            main_page.keyboard.right()
            time.sleep(DELAY_TIME * 3)

            # snapshot for context menu
            context_menu_snap1 = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                              file_name=Auto_Ground_Truth_Folder + 'G2.2.3_Menu_BlendingMode_Normal.png')
            logger(context_menu_snap1)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.3_Menu_BlendingMode_Normal.png',
                                                        context_menu_snap1)
            logger(compare_result1)

            with uuid("38a39e5a-b40f-46ea-80ac-413d8804a4c1") as case:
                # case2.1.3 : Check default is ticked on "Normal"
                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.3_preview_window_BlendingMode_Normal.png')
                logger(preview_status)
                compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.3_preview_window_BlendingMode_Normal.png',
                                                          preview_status)
                logger(compare_result2)

                case.result = compare_result1 and compare_result2

            with uuid("9c46123e-8a57-4eff-90cf-5b754d5e3265") as case:
                # case2.2.4 : Check real time preview for "Darken"
                # send right key to submenu
                main_page.keyboard.down()
                time.sleep(DELAY_TIME * 2)

                # snapshot for context menu
                context_menu_snap1 = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                             file_name=Auto_Ground_Truth_Folder + 'G2.2.4_Menu_BlendingMode_Darken.png')
                logger(context_menu_snap1)
                compare_result3 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.4_Menu_BlendingMode_Darken.png',
                                                         context_menu_snap1)
                logger(compare_result3)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.4_preview_window_BlendingMode_Darken.png')
                logger(preview_status)
                compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.4_preview_window_BlendingMode_Darken.png',
                                                          preview_status)
                logger(compare_result2)

                case.result = compare_result3 and compare_result2

            with uuid("b648087a-7740-47a6-aec6-f01c240902f8") as case:
                # case2.2.5 : Check real time preview for "Multiply"
                # send right key to submenu
                main_page.keyboard.down()
                time.sleep(DELAY_TIME * 2)

                # snapshot for context menu
                context_menu_snap1 = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                             file_name=Auto_Ground_Truth_Folder + 'G2.2.5_Menu_BlendingMode_Multiply.png')
                logger(context_menu_snap1)
                compare_result3 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.5_Menu_BlendingMode_Multiply.png',
                                                         context_menu_snap1)
                logger(compare_result3)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.5_preview_window_BlendingMode_Multiply.png')
                logger(preview_status)
                compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.5_preview_window_BlendingMode_Multiply.png',
                                                          preview_status)
                logger(compare_result2)

                case.result = compare_result3 and compare_result2

            with uuid("f8f0e21a-6305-489e-9c4a-f80122720daa") as case:
                # case2.2.6 : Check real time preview for "Lighten"
                # send right key to submenu
                main_page.keyboard.down()
                time.sleep(DELAY_TIME * 2)

                # snapshot for context menu
                context_menu_snap1 = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                             file_name=Auto_Ground_Truth_Folder + 'G2.2.6_Menu_BlendingMode_Lighten.png')
                logger(context_menu_snap1)
                compare_result3 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.6_Menu_BlendingMode_Lighten.png',
                                                         context_menu_snap1)
                logger(compare_result3)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.6_preview_window_BlendingMode_Lighten.png')
                logger(preview_status)
                compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.6_preview_window_BlendingMode_Lighten.png',
                                                          preview_status)
                logger(compare_result2)

                case.result = compare_result3 and compare_result2

            with uuid("d9c0083e-692d-4771-9c87-df065fe2e833") as case:
                # case2.2.7 : Check real time preview for "Screen"
                # send right key to submenu
                main_page.keyboard.down()
                time.sleep(DELAY_TIME * 2)

                # snapshot for context menu
                context_menu_snap1 = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                             file_name=Auto_Ground_Truth_Folder + 'G2.2.7_Menu_BlendingMode_Screen.png')
                logger(context_menu_snap1)
                compare_result3 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.7_Menu_BlendingMode_Screen.png',
                                                         context_menu_snap1)
                logger(compare_result3)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.7_preview_window_BlendingMode_Screen.png')
                logger(preview_status)
                compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.7_preview_window_BlendingMode_Screen.png',
                                                          preview_status)
                logger(compare_result2)

                case.result = compare_result3 and compare_result2

            with uuid("2033c0e3-2dad-4bf3-88fb-962c6601d136") as case:
                # case2.2.8 : Check real time preview for "Overlay"
                # send right key to submenu
                main_page.keyboard.down()
                time.sleep(DELAY_TIME * 2)

                # snapshot for context menu
                context_menu_snap1 = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                             file_name=Auto_Ground_Truth_Folder + 'G2.2.8_Menu_BlendingMode_Overlay.png')
                logger(context_menu_snap1)
                compare_result3 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.8_Menu_BlendingMode_Overlay.png',
                                                         context_menu_snap1)
                logger(compare_result3)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.8_preview_window_BlendingMode_Overlay.png')
                logger(preview_status)
                compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.8_preview_window_BlendingMode_Overlay.png',
                                                          preview_status)
                logger(compare_result2)

                case.result = compare_result3 and compare_result2

            with uuid("253057ad-6956-4a32-baf7-54abc044025d") as case:
                # case2.2.9 : Check real time preview for "Difference"
                # send right key to submenu
                main_page.keyboard.down()
                time.sleep(DELAY_TIME * 2)

                # snapshot for context menu
                context_menu_snap1 = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                             file_name=Auto_Ground_Truth_Folder + 'G2.2.9_Menu_BlendingMode_Difference.png')
                logger(context_menu_snap1)
                compare_result3 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.9_Menu_BlendingMode_Difference.png',
                                                         context_menu_snap1)
                logger(compare_result3)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.9_preview_window_BlendingMode_Difference.png')
                logger(preview_status)
                compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.9_preview_window_BlendingMode_Difference.png',
                                                          preview_status)
                logger(compare_result2)

                case.result = compare_result3 and compare_result2

            with uuid("7da5c501-55f9-451f-a2ac-cff99ca872b9") as case:
                # case2.2.10 : Check real time preview for "Hue"
                # send right key to submenu
                main_page.keyboard.down()
                time.sleep(DELAY_TIME * 2)

                # snapshot for context menu
                context_menu_snap1 = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                             file_name=Auto_Ground_Truth_Folder + 'G2.2.10_Menu_BlendingMode_Hue.png')
                logger(context_menu_snap1)
                compare_result3 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.10_Menu_BlendingMode_Hue.png',
                                                         context_menu_snap1)
                logger(compare_result3)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.10_preview_window_BlendingMode_Hue.png')
                logger(preview_status)
                compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.10_preview_window_BlendingMode_Hue.png',
                                                          preview_status)
                logger(compare_result2)

                # Click [Enter] to apply blending mode
                main_page.keyboard.enter()

                case.result = compare_result3 and compare_result2

            with uuid("d7582952-5445-4290-bd96-b35af2547c3b") as case:
                # case2.2.2 : Check if the selected blending mode is kept as previous one
                main_page.timeline_select_track(2)
                timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media)
                # right click on timeline clip
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode')
                logger(context_menu)

                # send right key to submenu
                #main_page.keyboard.down()
                time.sleep(DELAY_TIME * 2)

                # snapshot for context menu
                context_menu_snap1 = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                             file_name=Auto_Ground_Truth_Folder + 'G2.2.2_Menu_BlendingMode_KeepPevious.png')
                logger(context_menu_snap1)
                compare_result3 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.2_Menu_BlendingMode_KeepPevious.png',
                                                         context_menu_snap1)
                logger(compare_result3)

                case.result = compare_result3

            case.result = compare_result1


    @exception_screenshot
    def test1_1_1_4(self):
        #7/23
        with uuid("177c0804-f660-476b-b0a7-5d2a3b7ee5fe") as case:
            # case2.2.11 : Check if Blending mode "Normal" is applied to "Photo" correctly
            time.sleep(5)
            #main_page.enter_room(0)
            #time.sleep(DELAY_TIME*2)
            main_page.insert_media('Landscape 01.jpg')
            time.sleep(DELAY_TIME*3)

            # select track2 and then inserting another photo to timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            main_page.insert_media('Sport 01.jpg')
            timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
            logger(timeline_media)

            # Check applied blending mode via context menu
            #click_tools = tips_area_page.tools.click_btn()
            #logger(click_tools)
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Normal')
            logger(context_menu)

            # snapshot for context menu
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                              file_name=Auto_Ground_Truth_Folder + 'G2.2.11_preview_window_BlendingMode_Normal.png')
            logger(preview_wnd)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.11_preview_window_BlendingMode_Normal.png',
                                                        preview_wnd)
            logger(compare_result1)

            case.result = compare_result1 #and preview_wnd
            logger(case.result)

            with uuid("20f2ff99-0d8c-4d82-8d6e-db2c07c266cd") as case:
                # case2.1.12 : Check default is ticked on "Darken"

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media)

                # Change applied blending mode to "Darken" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Darken')
                logger(context_menu)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.12_preview_window_BlendingMode_Darken.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.12_preview_window_BlendingMode_Darken.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            with uuid("385139a5-1923-4a5a-81c7-da586415439b") as case:
                # case2.1.13 : Check default is ticked on "Multiply"

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media)

                # Change applied blending mode to "Multiply" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Multiply')
                logger(context_menu)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.13_preview_window_BlendingMode_Multiply.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.13_preview_window_BlendingMode_Multiply.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            with uuid("f4a8cf27-a27a-46ee-b68a-c73e8224b06c") as case:
                # case2.1.14 : Check default is ticked on "Lighten"

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media)

                # Change applied blending mode to "Lighten" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Lighten')
                logger(context_menu)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.14_preview_window_BlendingMode_Lighten.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.14_preview_window_BlendingMode_Lighten.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            with uuid("e9f99b53-f542-4393-9722-a8be74c12822") as case:
                # case2.1.15 : Check default is ticked on "Screen"

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media)

                # Change applied blending mode to "Screen" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Screen')
                logger(context_menu)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.15_preview_window_BlendingMode_Screen.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.15_preview_window_BlendingMode_Screen.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            with uuid("3c3e8c1c-8a85-426b-9053-8aa69d38b4c4") as case:
                # case2.1.16 : Check default is ticked on "Overlay"

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media)

                # Change applied blending mode to "Overlay" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Overlay')
                logger(context_menu)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.16_preview_window_BlendingMode_Overlay.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.16_preview_window_BlendingMode_Overlay.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            with uuid("03d9af34-106d-4da9-9f91-12398033dfdf") as case:
                # case2.1.17 : Check default is ticked on "Difference"

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media)

                # Change applied blending mode to "Difference" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Difference')
                logger(context_menu)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.17_preview_window_BlendingMode_Difference.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.17_preview_window_BlendingMode_Difference.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            with uuid("c74ea43f-6944-4819-92f0-33672057120e") as case:
                # case2.1.18 : Check default is ticked on "Hue"

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media)

                # Change applied blending mode to "Hue" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Hue')
                logger(context_menu)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.18_preview_window_BlendingMode_Hue.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.18_preview_window_BlendingMode_Hue.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            #8/5
            with uuid("dd52112d-ea02-46ac-86f6-ee3ae1ece4aa") as case:
                # case2.2.27 (L66) : Check blending mode "Normal" with crossfade

                # select track1 and select photo to timeline
                select_track = main_page.timeline_select_track(1)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Landscape 01.jpg', 0)
                logger(timeline_media)

                # seek to 00:00:02:00
                set_timecode = main_page.set_timeline_timecode('00_00_02_00')
                logger(set_timecode)

                # insert video to track1
                #main_page.insert_media('Skateboard 01.jpg')
                main_page.select_library_icon_view_media('Skateboard 01.mp4')
                main_page.tips_area_insert_media_to_selected_track(option=3)

                # select track2 and select photo on timeline
                select_track1 = main_page.timeline_select_track(2)
                logger(select_track1)
                timeline_media1 = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media1)

                # Change applied blending mode to "Normal" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Normal')
                logger(context_menu)

                # seek to 00:00:04:00 which has applied crossfade
                set_timecode1 = main_page.set_timeline_timecode('00_00_04_00')
                logger(set_timecode1)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.27_preview_window_BlendingMode_Normal.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.27_preview_window_BlendingMode_Normal.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            #8/5
            with uuid("69240227-d974-4063-97db-42ce66e38ace") as case:
                # case2.2.28 (L67) : Check blending mode "Darken" with crossfade

                # select track2 and select photo on timeline
                select_track2 = main_page.timeline_select_track(2)
                logger(select_track2)
                timeline_media1 = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media1)

                # Change applied blending mode to "Normal" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Darken')
                logger(context_menu)

                # seek to 00:00:04:00 which has applied crossfade
                set_timecode1 = main_page.set_timeline_timecode('00_00_04_00')
                logger(set_timecode1)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.28_preview_window_BlendingMode_Darken.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.28_preview_window_BlendingMode_Darken.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            # 8/5
            with uuid("7f87c660-7e35-4c9d-894a-fc3c7054d489") as case:
                # case2.2.29 (L68) : Check blending mode "Multiply" with crossfade

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media)

                # Change applied blending mode to "Multiply" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Multiply')
                logger(context_menu)

                # seek to 00:00:04:00 which has applied crossfade
                set_timecode1 = main_page.set_timeline_timecode('00_00_04_00')
                logger(set_timecode1)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.29_preview_window_BlendingMode_Multiply.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.29_preview_window_BlendingMode_Multiply.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            # 8/5
            with uuid("c7d9a637-5bd3-46ba-9ba3-ac20fa778306") as case:
                # case2.2.30 : Check blending mode "Lighten" with crossfade

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media)

                # Change applied blending mode to "Lighten" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Lighten')
                logger(context_menu)

                # seek to 00:00:04:00 which has applied crossfade
                set_timecode1 = main_page.set_timeline_timecode('00_00_04_00')
                logger(set_timecode1)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.30_preview_window_BlendingMode_Lighten.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.30_preview_window_BlendingMode_Lighten.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            # 8/5
            with uuid("a721569c-1b3d-42b5-91ae-40083b4bdb0a") as case:
                # case2.2.31 : Check blending mode "Screen" with crossfade

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media)

                # Change applied blending mode to "Screen" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Screen')
                logger(context_menu)

                # seek to 00:00:04:00 which has applied crossfade
                set_timecode1 = main_page.set_timeline_timecode('00_00_04_00')
                logger(set_timecode1)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.31_preview_window_BlendingMode_Screen.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.31_preview_window_BlendingMode_Screen.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            with uuid("d6cb653c-22e9-472b-8f62-c9ff595b97f9") as case:
                # case2.2.32 : Check blending mode "Overlay" with crossfade

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media)

                # Change applied blending mode to "Overlay" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Overlay')
                logger(context_menu)

                # seek to 00:00:04:00 which has applied crossfade
                set_timecode1 = main_page.set_timeline_timecode('00_00_04_00')
                logger(set_timecode1)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.32_preview_window_BlendingMode_Overlay.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.32_preview_window_BlendingMode_Overlay.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            # 8/5
            with uuid("6aef9b05-5193-4a88-bbe1-94fc5fad783a") as case:
                # case2.2.33 : Check blending mode "Difference" with crossfade

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media)

                # Change applied blending mode to "Difference" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Difference')
                logger(context_menu)

                # seek to 00:00:04:00 which has applied crossfade
                set_timecode1 = main_page.set_timeline_timecode('00_00_04_00')
                logger(set_timecode1)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.33_preview_window_BlendingMode_Difference.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.33_preview_window_BlendingMode_Difference.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            #8/5
            with uuid("abab3a6e-9ada-4618-8536-7b10afcd8e45") as case:
                # case2.2.34 : Check blending mode "Hue" with crossfade

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Sport 01.jpg', 0)
                logger(timeline_media)

                # Change applied blending mode to "Hue" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Hue')
                logger(context_menu)

                # seek to 00:00:04:00 which has applied crossfade
                set_timecode1 = main_page.set_timeline_timecode('00_00_04_00')
                logger(set_timecode1)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.34_preview_window_BlendingMode_Hue.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.34_preview_window_BlendingMode_Hue.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result




    @exception_screenshot
    def test1_1_1_5(self):
        #7/23
        with uuid("3e2c3de3-dea6-4105-86d0-e09ec5a63ba2") as case:
            # case2.2.19 : Check if Blending mode "Normal" is applied to "Video" correctly
            time.sleep(5)
            #main_page.enter_room(0)
            #time.sleep(DELAY_TIME*2)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME*3)

            # select track2 and then inserting another photo to timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            main_page.insert_media('Skateboard 02.mp4')
            timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media)

            # Check applied blending mode via context menu
            #click_tools = tips_area_page.tools.click_btn()
            #logger(click_tools)
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Normal')
            logger(context_menu)

            # snapshot for context menu
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                              file_name=Auto_Ground_Truth_Folder + 'G2.2.19_preview_window_BlendingMode_Normal.png')
            logger(preview_wnd)
            compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.19_preview_window_BlendingMode_Normal.png',
                                                        preview_wnd)
            logger(compare_result1)

            case.result = compare_result1 and preview_wnd
            logger(case.result)

            with uuid("c50e977f-9af2-4f20-820a-4992b5d1d998") as case:
                # case2.2.20 : Check default is ticked on "Darken"

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
                logger(timeline_media)

                # Change applied blending mode to "Darken" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Darken')
                logger(context_menu)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.20_preview_window_BlendingMode_Darken.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.20_preview_window_BlendingMode_Darken.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            with uuid("445412d8-b87d-462a-adbb-dc1229ea11ea") as case:
                # case2.2.21 : Check default is ticked on "Multiply"

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
                logger(timeline_media)

                # Change applied blending mode to "Multiply" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Multiply')
                logger(context_menu)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.21_preview_window_BlendingMode_Multiply.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.21_preview_window_BlendingMode_Multiply.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            with uuid("74ce007b-1c31-44ed-b343-4ff5c9e7f8d1") as case:
                # case2.2.22 : Check default is ticked on "Lighten"

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
                logger(timeline_media)

                # Change applied blending mode to "Lighten" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Lighten')
                logger(context_menu)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.22_preview_window_BlendingMode_Lighten.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.22_preview_window_BlendingMode_Lighten.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            with uuid("e39d7428-bb35-4ff9-9701-3a96fec8e72b") as case:
                # case2.2.23 : Check default is ticked on "Screen"

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
                logger(timeline_media)

                # Change applied blending mode to "Screen" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Screen')
                logger(context_menu)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.23_preview_window_BlendingMode_Screen.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.23_preview_window_BlendingMode_Screen.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            with uuid("80ed21ad-c9b4-4433-b84e-0eae24729616") as case:
                # case2.2.24 : Check default is ticked on "Overlay"

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
                logger(timeline_media)

                # Change applied blending mode to "Overlay" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Overlay')
                logger(context_menu)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.24_preview_window_BlendingMode_Overlay.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.24_preview_window_BlendingMode_Overlay.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            with uuid("594ecb13-bd51-4de5-a729-63145b23db32") as case:
                # case2.2.25 : Check default is ticked on "Difference"

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
                logger(timeline_media)

                # Change applied blending mode to "Difference" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Difference')
                logger(context_menu)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.25_preview_window_BlendingMode_Difference.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.25_preview_window_BlendingMode_Difference.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            with uuid("6b7eca17-7be4-442b-9c8e-78479d82a193") as case:
                # case2.2.26 : Check default is ticked on "Hue"

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
                logger(timeline_media)

                # Change applied blending mode to "Hue" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Hue')
                logger(context_menu)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G2.2.26_preview_window_BlendingMode_Hue.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.2.26_preview_window_BlendingMode_Hue.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            #8/5
            with uuid("7f331889-eeaf-408a-9dc4-1cb8706dcef6") as case:
                # case3.1.5 : Opacity > Set "Fade in and Fade out"

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
                logger(timeline_media)

                # "Enable fade-in and fade-out" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Edit Video', 'Enable Fade-in and Fade-out')
                logger(context_menu)

                # seek to 00:00:01:12 which has applied crossfade
                set_timecode1 = main_page.set_timeline_timecode('00_00_01_12')
                logger(set_timecode1)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G3.1.5_Opacity_Apply_FadeIn-Out.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.5_Opacity_Apply_FadeIn-Out.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            #8/5
            with uuid("efe9c4df-183d-41b6-8609-6c6ba5bd4fbd") as case:
                # case3.1.4 : Undo & Redo "Enable Fade-in and Fade-out"

                # undo & snapshot
                undo1 = main_page.click_undo()
                logger(undo1)

                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G3.1.4_Undo_Apply_FadeIn-Out.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.4_Undo_Apply_FadeIn-Out.png',
                                                        preview_status)
                logger(compare_result)

                # Redo & snapshot
                redo1 = main_page.click_redo()
                logger(redo1)

                preview_status1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G3.1.4_Redo_Apply_FadeIn-Out.png')
                logger(preview_status1)
                compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.4_Redo_Apply_FadeIn-Out.png',
                                                        preview_status1)
                logger(compare_result1)

                case.result = compare_result and compare_result1


            #8/6
            with uuid("c8d456f4-fbfe-47a0-b82a-f50f4d023a7f") as case:
                # case3.1.6 : Restore to original opacity

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                #main_page.insert_media('Sport 01.jpg')
                timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
                logger(timeline_media)

                # "Enable fade-in and fade-out" via context menu
                # click_tools = tips_area_page.tools.click_btn()
                # logger(click_tools)
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Edit Video', 'Restore to Original Opacity Level')
                logger(context_menu)

                # seek to 00:00:01:12 which has applied crossfade
                set_timecode1 = main_page.set_timeline_timecode('00_00_01_12')
                logger(set_timecode1)


                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G3.1.6_Restore_Opacity.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.6_Restore_Opacity.png',
                                                          preview_status)
                logger(compare_result)

                case.result = compare_result

            # 8/6
            with uuid("9cfdc329-fcbc-47bb-8ade-5e401e465398") as case:
                # case3.1.1 : Add keyframe

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
                logger(timeline_media)

                # Enter keyframe room
                current_result = tips_area_page.click_keyframe()
                logger(current_result)

                # unfold "clip attribute" and drag scrollbar
                #tips_area_page.set_category_fold_enable(clip, 1)
                keyframe_room_page.clip_attributes.unfold_tab(1)
                keyframe_room_page.drag_scroll_bar(0.5)
                keyframe_room_page.clip_attributes.opacity.show()

                # set opacity to 15
                keyframe_room_page.clip_attributes.opacity.set_value(15)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main ,
                                                           file_name=Auto_Ground_Truth_Folder + 'G3.1.1_Set_Opacity_15_preview.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.1_Set_Opacity_15_preview.png',
                                                          preview_status)
                logger(compare_result)

                # snapshot for keyframe room
                keyframe_setting_page = tips_area_page.snapshot(locator=L.keyframe_room.main_window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G3.1.1_Set_Opacity_15_ks.png')
                logger(keyframe_setting_page)
                compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.1_Set_Opacity_15_ks.png',
                                                          keyframe_setting_page)
                logger(compare_result1)

                case.result = compare_result and compare_result1

            # 8/13
            with uuid("47c1d747-f4e6-4a8d-a92d-8abf08c7e568") as case:
                # case3.1.2 : Modify keyframe for opacity

                # seek to 00:00:04:00
                set_timecode = main_page.set_timeline_timecode('00_00_04_00')
                logger(set_timecode)

                # set opacity to 88 to add another keyframe
                keyframe_room_page.clip_attributes.opacity.set_value(88)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main ,
                                                           file_name=Auto_Ground_Truth_Folder + 'G3.1.2_Set_Opacity_88_preview.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.2_Set_Opacity_88_preview.png',
                                                          preview_status)
                logger(compare_result)

                # snapshot for keyframe room
                keyframe_setting_page = tips_area_page.snapshot(locator=L.keyframe_room.main_window,
                                                                file_name=Auto_Ground_Truth_Folder + 'G3.1.2_Set_Opacity_88_ks.png')
                logger(keyframe_setting_page)
                compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.2_Set_Opacity_88_ks.png',
                                                         keyframe_setting_page)
                logger(compare_result1)

                # seek back to 00:00:01:12 which has applied keyframe
                set_timecode1 = main_page.set_timeline_timecode('00_00_01_12')
                logger(set_timecode1)

                # Modify opacity from 15 to 40
                keyframe_room_page.clip_attributes.opacity.set_value(40)

                # snapshot for playback window
                preview_status1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G3.1.2_Modify_Opacity_to_40_preview.png')
                logger(preview_status1)
                compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.2_Modify_Opacity_to_40_preview.png',
                                                        preview_status1)
                logger(compare_result2)

                # snapshot for keyframe room
                keyframe_setting_page1 = tips_area_page.snapshot(locator=L.keyframe_room.main_window,
                                                                file_name=Auto_Ground_Truth_Folder + 'G3.1.2_Modify_Opacity_40_ks.png')
                logger(keyframe_setting_page1)
                compare_result3 = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.2_Modify_Opacity_40_ks.png',
                                                         keyframe_setting_page1)
                logger(compare_result3)

                case.result = compare_result and compare_result1 and compare_result2 and compare_result3

            # 8/13
            with uuid("e48406f2-fb0e-48c1-a232-ac865b4eb2b8") as case:
                # case3.1.3 : Remove keyframe from opacity

                # seek to 00:00:04:00
                set_timecode = main_page.set_timeline_timecode('00_00_04_00')
                logger(set_timecode)

                # Remove keyframe from 00_00_04_00
                keyframe_room_page.clip_attributes.opacity.add_remove_keyframe()

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G3.1.3_Remove_Keyframe_Preview.png')
                logger(preview_status)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.3_Remove_Keyframe_Preview.png',
                                                        preview_status)
                logger(compare_result)

                # snapshot for keyframe room
                keyframe_setting_page = tips_area_page.snapshot(locator=L.keyframe_room.main_window,
                                                                file_name=Auto_Ground_Truth_Folder + 'G3.1.3_Remove_Keyframe.png')
                logger(keyframe_setting_page)
                compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.3_Remove_Keyframe.png',
                                                         keyframe_setting_page)
                logger(compare_result1)

                case.result = compare_result and compare_result1

            # 8/13
            with uuid("73b84c8a-351a-430a-89e9-a70d6cc93ac2") as case:
                # case3.2.2 : Add Volume keyframe

                # select track2 and select photo to timeline
                select_track = main_page.timeline_select_track(2)
                logger(select_track)
                timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
                logger(timeline_media)

                # Enter "Volume" keyframe via context menu
                main_page.right_click()
                context_menu = main_page.select_right_click_menu('Edit Clip Keyframe', 'Volume')
                logger(context_menu)

                # set volume to 50 (max = 12)
                keyframe_room_page.volume.set_value(50)

                # snapshot for keyframe room
                keyframe_setting_page = tips_area_page.snapshot(locator=L.keyframe_room.main_window,
                                                                file_name=Auto_Ground_Truth_Folder + 'G3.2.2_Add_Volume_Keyframe.png')
                logger(keyframe_setting_page)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G3.2.2_Add_Volume_Keyframe.png',
                                                         keyframe_setting_page)
                logger(compare_result)

                # 8/13
                with uuid("a15be60c-3c76-41e1-a73d-2c5b08a61c91") as case:
                    # case3.2.1 : Apply Volume keyframe

                    # seek to 00:00:00:00
                    set_timecode = main_page.set_timeline_timecode('00_00_00_00')
                    logger(set_timecode)

                    # set volume to 5 (max = 12)
                    keyframe_room_page.volume.set_value(5)

                    # snapshot for keyframe room and timeline
                    keyframe_setting_page1 = tips_area_page.snapshot(locator=L.keyframe_room.main_window,
                                                                    file_name=Auto_Ground_Truth_Folder + 'G3.2.1_Set_Volume_Keyframe.png')
                    logger(keyframe_setting_page1)
                    compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G3.2.1_Set_Volume_Keyframe.png',
                                                            keyframe_setting_page1)
                    logger(compare_result1)

                    timeline_status = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                                file_name=Auto_Ground_Truth_Folder + 'G3.2.1_Set_Volume_Keyframe_timeline_workspace.png')
                    logger(timeline_status)

                    compare_result2 = tips_area_page.compare(
                        Ground_Truth_Folder + 'G3.2.1_Set_Volume_Keyframe_timeline_workspace.png',
                        timeline_status)
                    logger(compare_result2)

                    case.result = compare_result1 and compare_result2

                case.result = compare_result

            # 8/13
            with uuid("e53ca6b0-170c-4e3f-8d0e-37aed7037b52") as case:
                # case3.2.5 : Undo + Redo Volume keyframe

                # undo the change
                main_page.click_undo()

                # snapshot for keyframe room and timeline
                keyframe_setting_page = tips_area_page.snapshot(locator=L.keyframe_room.main_window,
                                                                file_name=Auto_Ground_Truth_Folder + 'G3.2.5_Undo_Volume_Keyframe.png')
                logger(keyframe_setting_page)
                compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G3.2.5_Undo_Volume_Keyframe.png',
                                                        keyframe_setting_page)
                logger(compare_result)

                timeline_status = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                            file_name=Auto_Ground_Truth_Folder + 'G3.2.5_Undo_Volume_Keyframe_timeline_workspace.png')
                logger(timeline_status)

                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G3.2.5_Undo_Volume_Keyframe_timeline_workspace.png',
                    timeline_status)
                logger(compare_result1)


                # redo the change
                main_page.click_redo()

                # snapshot for keyframe room and timeline
                keyframe_setting_page1 = tips_area_page.snapshot(locator=L.keyframe_room.main_window,
                                                                file_name=Auto_Ground_Truth_Folder + 'G3.2.5_Redo_Volume_Keyframe.png')
                logger(keyframe_setting_page1)
                compare_result2 = tips_area_page.compare(Ground_Truth_Folder + 'G3.2.5_Redo_Volume_Keyframe.png',
                                                        keyframe_setting_page1)
                logger(compare_result2)

                timeline_status = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                            file_name=Auto_Ground_Truth_Folder + 'G3.2.5_Redo_Volume_Keyframe_timeline_workspace.png')
                logger(timeline_status)

                compare_result3 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G3.2.5_Redo_Volume_Keyframe_timeline_workspace.png',
                    timeline_status)
                logger(compare_result3)

                case.result = compare_result and compare_result1 and compare_result2 and compare_result3

            # 8/13
            with uuid("2bc36f52-05ad-4662-8b62-be995cc67764") as case:
                # case3.2.3 : Modify Volume keyframe

                # seek to 00:00:04:00
                set_timecode = main_page.set_timeline_timecode('00_00_04_00')
                logger(set_timecode)

                # set volume to -2 (max = 12)
                keyframe_room_page.volume.set_value(-2)

                # snapshot for keyframe room and timeline
                keyframe_setting_page1 = tips_area_page.snapshot(locator=L.keyframe_room.main_window,
                                                                 file_name=Auto_Ground_Truth_Folder + 'G3.2.3_Modify_Volume_Keyframe.png')
                logger(keyframe_setting_page1)
                compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G3.2.3_Modify_Volume_Keyframe.png',
                                                         keyframe_setting_page1)
                logger(compare_result1)

                timeline_status = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                          file_name=Auto_Ground_Truth_Folder + 'G3.2.3_Modify_Volume_Keyframe_timeline_workspace.png')
                logger(timeline_status)

                compare_result2 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G3.2.3_Modify_Volume_Keyframe_timeline_workspace.png',
                    timeline_status)
                logger(compare_result2)

                case.result = compare_result1 and compare_result2

            # 8/13
            with uuid("825c1a4e-f902-4e79-9640-98598267366d") as case:
                # case3.2.4 : Remove Volume keyframe

                # seek to 00:00:04:00
                set_timecode = main_page.set_timeline_timecode('00_00_04_00')
                logger(set_timecode)

                # Remove target volume keyframe
                keyframe_room_page.volume.add_remove_keyframe()

                # snapshot for keyframe room and timeline
                keyframe_setting_page1 = tips_area_page.snapshot(locator=L.keyframe_room.main_window,
                                                                 file_name=Auto_Ground_Truth_Folder + 'G3.2.4_Remove_Volume_Keyframe.png')
                logger(keyframe_setting_page1)
                compare_result1 = tips_area_page.compare(Ground_Truth_Folder + 'G3.2.4_Remove_Volume_Keyframe.png',
                                                         keyframe_setting_page1)
                logger(compare_result1)

                timeline_status = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                          file_name=Auto_Ground_Truth_Folder + 'G3.2.4_Remove_Volume_Keyframe_timeline_workspace.png')
                logger(timeline_status)

                compare_result2 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G3.2.4_Remove_Volume_Keyframe_timeline_workspace.png',
                    timeline_status)
                logger(compare_result2)

                case.result = compare_result1 and compare_result2

    @exception_screenshot
    def test1_1_1_6(self):
        #8/20
        with uuid("0623df59-98cd-4404-a676-4099347235f1") as case:
            # case2.1.12 : Check if Blending mode "Darken" is applied to "Video" via blending mode dialogue
            time.sleep(5)
            #main_page.enter_room(0)
            #time.sleep(DELAY_TIME*2)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME*3)

            # select track2 and then inserting another photo to timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            main_page.insert_media('Skateboard 02.mp4')
            timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Darken"
            blending_mode = blending_mode_page.set_blending_mode('Darken')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.12_SetBlendingMode_Darken_video.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.12_SetBlendingMode_Darken_video.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.12_SetBlendingMode_Darken_Applied_to_video.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.12_SetBlendingMode_Darken_Applied_to_video.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1

        #8/20
        with uuid("d8cf2911-c0d3-4310-a06a-39f0e889f9d7") as case:
            # case2.1.11 : Check if Blending mode "Normal" is applied to "Video" via blending mode dialogue

            # select track2 and then inserting another photo to timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Normal"
            blending_mode = blending_mode_page.set_blending_mode('Normal')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.11_SetBlendingMode_Normal_video.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.11_SetBlendingMode_Normal_video.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.11_SetBlendingMode_Normal_Applied_to_video.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.11_SetBlendingMode_Normal_Applied_to_video.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1

        #8/20
        with uuid("7d7c666b-6950-422f-9f0c-c916f1cf4acf") as case:
            # case2.1.13 : Check if Blending mode "Multiply" is applied to "Video" via blending mode dialogue

            # select track2 and then inserting another photo to timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Multiply"
            blending_mode = blending_mode_page.set_blending_mode('Multiply')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.13_SetBlendingMode_Multiply_video.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.13_SetBlendingMode_Multiply_video.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.13_SetBlendingMode_Multiply_Applied_to_video.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.13_SetBlendingMode_Multiply_Applied_to_video.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result

        #8/27
        with uuid("2e5b2e4a-11fe-4362-bc01-ee9b6300c6c7") as case:
            # case2.1.14 : Check if Blending mode "Lighten" is applied to "Video" via blending mode dialogue

            # select track2 and then inserting another photo to timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Lighten"
            blending_mode = blending_mode_page.set_blending_mode('Lighten')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.14_SetBlendingMode_Lighten_video.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.14_SetBlendingMode_Lighten_video.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.14_SetBlendingMode_Lighten_Applied_to_video.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.14_SetBlendingMode_Lighten_Applied_to_video.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result

        #8/27
        with uuid("889578fd-ecf0-4ed8-afd7-13b12369cec9") as case:
            # case2.1.15 : Check if Blending mode "Screen" is applied to "Video" via blending mode dialogue

            # select track2 and then inserting another photo to timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Screen"
            blending_mode = blending_mode_page.set_blending_mode('Screen')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.15_SetBlendingMode_Screen_video.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.15_SetBlendingMode_Screen_video.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.15_SetBlendingMode_Screen_Applied_to_video.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.15_SetBlendingMode_Screen_Applied_to_video.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result

        #8/27
        with uuid("1d8ff934-0ad9-452b-8fab-ab5dfdf237bd") as case:
            # case2.1.16 : Check if Blending mode "Overlay" is applied to "Video" via blending mode dialogue

            # select track2 and then inserting another photo to timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Overlay"
            blending_mode = blending_mode_page.set_blending_mode('Overlay')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.16_SetBlendingMode_Overlay_video.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.16_SetBlendingMode_Overlay_video.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.16_SetBlendingMode_Overlay_Applied_to_video.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.16_SetBlendingMode_Overlay_Applied_to_video.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result

        #8/27
        with uuid("d38db418-9d26-432d-b827-1ea88267b5ae") as case:
            # case2.1.17 : Check if Blending mode "Difference" is applied to "Video" via blending mode dialogue

            # select track2 and then inserting another photo to timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Difference"
            blending_mode = blending_mode_page.set_blending_mode('Difference')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.17_SetBlendingMode_Difference_video.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.17_SetBlendingMode_Difference_video.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.17_SetBlendingMode_Difference_Applied_to_video.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.17_SetBlendingMode_Difference_Applied_to_video.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result

        #8/27
        with uuid("7c834da2-049d-4bc0-a06f-25371602170f") as case:
            # case2.1.18 : Check if Blending mode "Hue" is applied to "Video" via blending mode dialogue

            # select track2 and then inserting another photo to timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Hue"
            blending_mode = blending_mode_page.set_blending_mode('Hue')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.18_SetBlendingMode_Hue_video.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.18_SetBlendingMode_Hue_video.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.18_SetBlendingMode_Hue_Applied_to_video.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.17_SetBlendingMode_Hue_Applied_to_video.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result

    @exception_screenshot
    def test1_1_1_7(self):
        #8/27
        with uuid("644d0e0c-06de-408e-9281-ba09c6337db6") as case:
            # case2.1.19 : Check if Blending mode "Darken" is applied to "crossfade" area via blending mode dialogue

            time.sleep(5)
            # main_page.enter_room(0)
            # time.sleep(DELAY_TIME*2)
            main_page.insert_media('Landscape 01.jpg')
            time.sleep(DELAY_TIME * 3)

            # select track2 and then inserting another photo to timeline
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            main_page.insert_media('Skateboard 02.mp4')
            timeline_media = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media)


            # select track1 and select photo to timeline
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            # main_page.insert_media('Sport 01.jpg')
            timeline_media = timeline_operation_page.select_timeline_media('Landscape 01.jpg', 0)
            logger(timeline_media)

            # seek to 00:00:02:00
            set_timecode = main_page.set_timeline_timecode('00_00_02_00')
            logger(set_timecode)

            # insert video to track1
            # main_page.insert_media('Skateboard 01.jpg')
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.tips_area_insert_media_to_selected_track(option=3)

            # select track2 and select video on timeline
            select_track2 = main_page.timeline_select_track(2)
            logger(select_track2)
            timeline_media1 = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media1)

            # seek to 00:00:04:00 (crossfade)
            set_timecode = main_page.set_timeline_timecode('00_00_04_00')
            logger(set_timecode)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Darken"
            blending_mode = blending_mode_page.set_blending_mode('Darken')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.19_SetBlendingMode_Darken_crossfade.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.19_SetBlendingMode_Darken_crossfade.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.19_SetBlendingMode_Darken_applied to_crossfade.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.19_SetBlendingMode_Darken_applied to_crossfade.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result


        #8/27
        with uuid("849e5cd1-ed60-4218-ae2c-a672e887f5ad") as case:
            # case2.1.20 : Check if Blending mode "Normal" is applied to "crossfade" area via blending mode dialogue

            # select track2 and select video on timeline
            select_track2 = main_page.timeline_select_track(2)
            logger(select_track2)
            timeline_media1 = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media1)

            # seek to 00:00:04:00 (crossfade)
            set_timecode = main_page.set_timeline_timecode('00_00_04_00')
            logger(set_timecode)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Normal"
            blending_mode = blending_mode_page.set_blending_mode('Normal')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.20_SetBlendingMode_Normal_crossfade.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.20_SetBlendingMode_Normal_crossfade.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.20_SetBlendingMode_Normal_applied to_crossfade.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.20_SetBlendingMode_Normal_applied to_crossfade.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result


        #8/27
        with uuid("4fc6cf1d-6841-4584-966f-bdea7ca7cc3e") as case:
            # case2.1.21 : Check if Blending mode "Multiply" is applied to "crossfade" area via blending mode dialogue

            # select track2 and select video on timeline
            select_track2 = main_page.timeline_select_track(2)
            logger(select_track2)
            timeline_media1 = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media1)

            # seek to 00:00:04:00 (crossfade)
            set_timecode = main_page.set_timeline_timecode('00_00_04_00')
            logger(set_timecode)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Multiply"
            blending_mode = blending_mode_page.set_blending_mode('Multiply')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.21_SetBlendingMode_Multiply_crossfade.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.21_SetBlendingMode_Multiply_crossfade.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.21_SetBlendingMode_Multiply_applied to_crossfade.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.21_SetBlendingMode_Multiply_applied to_crossfade.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result

        #8/27
        with uuid("ecffdb5e-842b-4e13-af0d-7656ca8433b8") as case:
            # case2.1.22 : Check if Blending mode "Lighten" is applied to "crossfade" area via blending mode dialogue

            # select track2 and select video on timeline
            select_track2 = main_page.timeline_select_track(2)
            logger(select_track2)
            timeline_media1 = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media1)

            # seek to 00:00:04:00 (crossfade)
            set_timecode = main_page.set_timeline_timecode('00_00_04_00')
            logger(set_timecode)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Lighten"
            blending_mode = blending_mode_page.set_blending_mode('Lighten')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.22_SetBlendingMode_Ligthen_crossfade.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.22_SetBlendingMode_Lighten_crossfade.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.22_SetBlendingMode_Lighten_applied to_crossfade.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.22_SetBlendingMode_Lighten_applied to_crossfade.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result

        #8/27
        with uuid("6cc0002a-5c94-441c-aab1-14ceab3501ae") as case:
            # case2.1.23 : Check if Blending mode "Screen" is applied to "crossfade" area via blending mode dialogue

            # select track2 and select video on timeline
            select_track2 = main_page.timeline_select_track(2)
            logger(select_track2)
            timeline_media1 = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media1)

            # seek to 00:00:04:00 (crossfade)
            set_timecode = main_page.set_timeline_timecode('00_00_04_00')
            logger(set_timecode)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Screen"
            blending_mode = blending_mode_page.set_blending_mode('Screen')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.23_SetBlendingMode_Screen_crossfade.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.23_SetBlendingMode_Screen_crossfade.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.23_SetBlendingMode_Screen_applied to_crossfade.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.23_SetBlendingMode_Screen_applied to_crossfade.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result

        #9/1
        with uuid("2ea10b89-1a9e-4156-8793-27699591dd17") as case:
            # case2.1.24 : Check if Blending mode "Overlay" is applied to "overlay" area via blending mode dialogue

            # select track2 and select video on timeline
            select_track2 = main_page.timeline_select_track(2)
            logger(select_track2)
            timeline_media1 = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media1)

            # seek to 00:00:04:00 (crossfade)
            set_timecode = main_page.set_timeline_timecode('00_00_04_00')
            logger(set_timecode)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Overlay"
            blending_mode = blending_mode_page.set_blending_mode('Overlay')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.24_SetBlendingMode_Overlay_crossfade.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.24_SetBlendingMode_Overlay_crossfade.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.24_SetBlendingMode_Overlay_applied to_crossfade.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.24_SetBlendingMode_Overlay_applied to_crossfade.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result

        #9/1
        with uuid("dc868217-cbcd-424b-9102-32e629897e58") as case:
            # case2.1.25 : Check if Blending mode "Difference" is applied to "overlay" area via blending mode dialogue

            # select track2 and select video on timeline
            select_track2 = main_page.timeline_select_track(2)
            logger(select_track2)
            timeline_media1 = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media1)

            # seek to 00:00:04:00 (crossfade)
            set_timecode = main_page.set_timeline_timecode('00_00_04_00')
            logger(set_timecode)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Difference"
            blending_mode = blending_mode_page.set_blending_mode('Difference')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.25_SetBlendingMode_Difference_crossfade.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.25_SetBlendingMode_Difference_crossfade.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.25_SetBlendingMode_Difference_applied to_crossfade.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.25_SetBlendingMode_Difference_applied to_crossfade.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result

        #9/1
        with uuid("617b6d4f-7bea-4f36-927e-20973d09adf9") as case:
            # case2.1.26 : Check if Blending mode "Hue" is applied to "overlay" area via blending mode dialogue

            # select track2 and select video on timeline
            select_track2 = main_page.timeline_select_track(2)
            logger(select_track2)
            timeline_media1 = timeline_operation_page.select_timeline_media('Skateboard 02.mp4', 0)
            logger(timeline_media1)

            # seek to 00:00:04:00 (crossfade)
            set_timecode = main_page.set_timeline_timecode('00_00_04_00')
            logger(set_timecode)

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Hue"
            blending_mode = blending_mode_page.set_blending_mode('Hue')
            logger(blending_mode)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.26_SetBlendingMode_Hue_crossfade.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.26_SetBlendingMode_Hue_crossfade.png',
                                                    preview_wnd)
            logger(compare_result)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd1 = tips_area_page.snapshot(locator=L.playback_window.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.26_SetBlendingMode_Hue_applied to_crossfade.png')
            logger(preview_wnd1)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.26_SetBlendingMode_Hue_applied to_crossfade.png',
                preview_wnd1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result