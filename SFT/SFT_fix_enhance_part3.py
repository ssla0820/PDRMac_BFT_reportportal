import sys, os

from SFT.globals import update_report_info, get_enable_case_execution_log, google_sheet_execution_log_init, \
    google_sheet_execution_log_update_result

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
base_page = PageFactory().get_page_object('base_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
fix_enhance_page = PageFactory().get_page_object('fix_enhance_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)


# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Fix Enhance_part3.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder - Setup for Overall Project
Ground_Truth_Folder = app.ground_truth_root + '/Fix_Enhance_part3/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Fix_Enhance_part3/'
Test_Material_Folder = app.testing_material

# For Ground Truth / Test Material folder - Setup for Duncan personal testing
# Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/GroundTruth/Title_Room/'
# Auto_Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/ATGroundTruth/Title_Room/'
# Test_Material_Folder = '/Users/cl/Desktop/Duncan/Material/'

DELAY_TIME = 1

class Test_Fix_Enhance_3():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME*4)
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
            google_sheet_execution_log_init('Fix_Enhance_2_3')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"test case template result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
    def test_1_1_1(self):
        with uuid("7e8e9b8c-5720-4ead-9e82-12b99ce10e7e") as case:
            # 1.7 Color Adjustment
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Food.jpg')
            tips_area_page.click_fix_enhance()
            fix_enhance_page.is_in_fix_enhance()
            """
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(is_in_fix_enhance)
            """
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Verify Default Exposure = 100
            current_value = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            logger(current_value)
            if current_value == '100':
                exposure_result = True
            else:
                exposure_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H121_CA_Exposure(100).png')
            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H121_CA_Exposure(100).png', current_image)
            case.result = compare_result and exposure_result

        with uuid("2d17b5a3-00c7-4389-9730-65ebe4f8ebd5") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Adjust Exposure by Up and Down arrow
            fix_enhance_page.enhance.color_adjustment.exposure.click_arrow(opt="up", times=2)

            # Verify Up x 2
            current_value = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            logger(current_value)
            if current_value == '102':
                exposure_up_result = True
            else:
                exposure_up_result = False

            fix_enhance_page.enhance.color_adjustment.exposure.click_arrow(opt="down", times=2)

            # Verify Down x 2
            current_value = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            logger(current_value)
            time.sleep(1)
            if current_value == '100':
                exposure_down_result = True
            else:
                exposure_down_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H125_CA_Exposure(up_down).png')
            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H125_CA_Exposure(up_down).png',
                                                     current_image)
            case.result = compare_result and exposure_up_result and exposure_down_result

        with uuid("9389ee7e-aba5-4400-89b0-a91e086ac6ac") as case:
            # Switch to Color Adjustment > Adjust Exposure Slider
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Adjust Exposure = 80 by drag slider
            fix_enhance_page.enhance.color_adjustment.exposure.adjust_slider(80)

            # Verify Exposure Slider = 80
            current_value = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            logger(current_value)
            if current_value == '80':
                exposure_result = True
            else:
                exposure_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H122_CA_Exposure(slider80).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H122_CA_Exposure(slider80).png',
                                                     current_image)
            case.result = compare_result and exposure_result

        with uuid("cf6919b6-eb90-4720-86ba-2f26d9e42c18") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Set Exposure = 0 by keyboard inputting
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(0)

            # Verify Exposure = 0
            current_value = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            logger(current_value)
            if current_value == '0':
                exposure_min_result = True
            else:
                exposure_min_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H123_CA_Exposure(0).png')
            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H123_CA_Exposure(0).png', current_image)
            case.result = compare_result and exposure_min_result

        with uuid("7c232f60-7aa7-45d3-b46f-5c7df607b641") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Set Exposure = 200 by keyboard inputting
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(200)

            # Verify Exposure = 200
            current_value = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            logger(current_value)
            if current_value == '200':
                exposure_max_result = True
            else:
                exposure_max_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H124_CA_Exposure(200).png')
            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H124_CA_Exposure(200).png', current_image)
            case.result = compare_result and exposure_max_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid("5ddec5b2-603c-4d73-988f-c46d9266b587") as case:
            # 1.7 Color Adjustment
            main_page.insert_media('Food.jpg')
            tips_area_page.click_fix_enhance()
            fix_enhance_page.is_in_fix_enhance()
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Verify Default Brightness = 0
            current_value = fix_enhance_page.enhance.color_adjustment.brightness.get_value()
            logger(current_value)
            if current_value == '0':
                brightness_result = True
            else:
                brightness_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H126_CA_Brightness(0).png')
            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H126_CA_Brightness(0).png', current_image)
            case.result = compare_result and brightness_result

        with uuid("d2b8be81-7255-4d10-8480-963b40b452ec") as case:
            # Switch to Color Adjustment > Adjust Brightness by Up and Down arrow
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Adjust Up x 2
            fix_enhance_page.enhance.color_adjustment.brightness.click_arrow(opt="up", times=2)
            # Verify Up x 2
            current_value = fix_enhance_page.enhance.color_adjustment.brightness.get_value()
            logger(current_value)
            if current_value == '2':
                brightness_up_result = True
            else:
                brightness_up_result = False

            # Adjust Down x 2
            fix_enhance_page.enhance.color_adjustment.brightness.click_arrow(opt="down", times=2)
            # Verify Down x 2
            current_value = fix_enhance_page.enhance.color_adjustment.brightness.get_value()
            logger(current_value)
            time.sleep(1)
            if current_value == '0':
                brightness_down_result = True
            else:
                brightness_down_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H130_CA_Brightness(up_down).png')
            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H130_CA_Brightness(up_down).png',
                                                     current_image)
            case.result = compare_result and brightness_up_result and brightness_down_result

        with uuid("2d6e991b-fa3e-4c12-b7d8-7cec7de6c0e3") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Adjust Brightness Slider = -60
            fix_enhance_page.enhance.color_adjustment.brightness.adjust_slider(-60)

            # Verify Brightness = -60
            current_value = fix_enhance_page.enhance.color_adjustment.brightness.get_value()
            logger(current_value)
            if current_value == '-60':
                brightness_result = True
            else:
                brightness_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H127_CA_Brightness(slider-60).png')
            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H127_CA_Brightness(slider-60).png',
                                                     current_image)
            case.result = compare_result and brightness_result

        with uuid("7a083fdf-3e29-427d-bddf-5a43ecfc0685") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Set Exposure = -100 by keyboard inputting
            fix_enhance_page.enhance.color_adjustment.brightness.set_value(-100)

            # Verify Exposure = -100
            current_value = fix_enhance_page.enhance.color_adjustment.brightness.get_value()
            logger(current_value)
            if current_value == '-100':
                brightness_min_result = True
            else:
                brightness_min_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H128_CA_Brightness(-100).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H128_CA_Brightness(-100).png',
                                                     current_image)
            case.result = compare_result and brightness_min_result

        with uuid("9298db82-a705-421e-9150-968838a879aa") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Set Brightness = 100 by keyboard inputting
            fix_enhance_page.enhance.color_adjustment.brightness.set_value(100)

            # Verify Exposure = 100
            current_value = fix_enhance_page.enhance.color_adjustment.brightness.get_value()
            logger(current_value)
            if current_value == '100':
                brightness_max_result = True
            else:
                brightness_max_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H129_CA_Brightness(100).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H129_CA_Brightness(100).png', current_image)
            case.result = compare_result and brightness_max_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid("0481c7d7-3ad1-4be3-8c20-c11e1bad2fd6") as case:
            # 1.7 Color Adjustment
            main_page.insert_media('Food.jpg')
            tips_area_page.click_fix_enhance()
            fix_enhance_page.is_in_fix_enhance()
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Verify Default Contrast = 0
            current_value = fix_enhance_page.enhance.color_adjustment.contrast.get_value()
            logger(current_value)
            if current_value == '0':
                contrast_result = True
            else:
                contrast_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H131_CA_Contrast(0).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H131_CA_Contrast(0).png', current_image)
            case.result = compare_result and contrast_result

        with uuid("50a1eedf-f924-4284-90cb-ae4749677b4f") as case:
            # Switch to Color Adjustment > Adjust Contrast by Up and Down arrow
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Adjust Up x 2
            fix_enhance_page.enhance.color_adjustment.contrast.click_arrow(opt="up", times=2)
            # Verify Up x 2
            current_value = fix_enhance_page.enhance.color_adjustment.contrast.get_value()
            logger(current_value)
            if current_value == '2':
                contrast_up_result = True
            else:
                contrast_up_result = False

            # Adjust Down x 2
            fix_enhance_page.enhance.color_adjustment.contrast.click_arrow(opt="down", times=2)
            # Verify Down x 2
            current_value = fix_enhance_page.enhance.color_adjustment.contrast.get_value()
            logger(current_value)
            time.sleep(1)
            if current_value == '0':
                contrast_down_result = True
            else:
                contrast_down_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H135_CA_Contrast(up_down).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H135_CA_Contrast(up_down).png',
                                                     current_image)
            case.result = compare_result and contrast_up_result and contrast_down_result

        with uuid("f9246f17-6645-4897-818c-ef820fefbc18") as case:
            # Switch to Color Adjustment > Adjust Contrast Slider
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Adjust Contrast Slider = 90
            fix_enhance_page.enhance.color_adjustment.contrast.adjust_slider(90)

            # Verify default Contrast = 90
            current_value = fix_enhance_page.enhance.color_adjustment.contrast.get_value()
            logger(current_value)
            if current_value == '90':
                contrast_min_result = True
            else:
                contrast_min_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H132_CA_Contrast(slider90).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H132_CA_Contrast(slider90).png',
                                                     current_image)
            case.result = compare_result and contrast_min_result

        with uuid("c4f5a647-b9d3-41a2-8425-1c88365d0f4a") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Set Contrast = -100 by keyboard inputting
            fix_enhance_page.enhance.color_adjustment.contrast.set_value(-100)

            # Verify Contrast = -100
            current_value = fix_enhance_page.enhance.color_adjustment.contrast.get_value()
            logger(current_value)
            if current_value == '-100':
                contrast_min_result = True
            else:
                contrast_min_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H133_CA_Contrast(-100).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H133_CA_Contrast(-100).png', current_image)
            case.result = compare_result and contrast_min_result

        with uuid("3b8df7ce-3ba2-4338-a785-d2a02f6192c9") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Set Contrast = 100 by keyboard inputting
            fix_enhance_page.enhance.color_adjustment.contrast.set_value(100)

            # Verify Contrast = 100
            current_value = fix_enhance_page.enhance.color_adjustment.contrast.get_value()
            logger(current_value)
            if current_value == '100':
                contrast_max_result = True
            else:
                contrast_max_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H133_CA_Contrast(-100).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H133_CA_Contrast(-100).png', current_image)
            case.result = compare_result and contrast_max_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid("bdb9efaa-ae78-4cd5-a489-643e86545fb5") as case:
            # 1.7 Color Adjustment
            main_page.insert_media('Food.jpg')
            tips_area_page.click_fix_enhance()
            fix_enhance_page.is_in_fix_enhance()
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Verify Default Hue = 100
            current_value = fix_enhance_page.enhance.color_adjustment.hue.get_value()
            logger(current_value)
            if current_value == '100':
                hue_result = True
            else:
                hue_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H136_CA_Hue(100).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H136_CA_Hue(100).png', current_image)
            case.result = compare_result and hue_result

        with uuid("ae4d33db-8cad-4809-b481-1ba694480476") as case:
            # Switch to Color Adjustment > Adjust Hue by Up and Down arrow
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Adjust Up x 2
            fix_enhance_page.enhance.color_adjustment.hue.click_arrow(opt="up", times=2)
            # Verify Up x 2
            current_value = fix_enhance_page.enhance.color_adjustment.hue.get_value()
            logger(current_value)
            if current_value == '102':
                hue_up_result = True
            else:
                hue_up_result = False

            # Adjust Down x 2
            fix_enhance_page.enhance.color_adjustment.hue.click_arrow(opt="down", times=2)
            # Verify Down x 2
            current_value = fix_enhance_page.enhance.color_adjustment.hue.get_value()
            logger(current_value)
            time.sleep(1)
            if current_value == '100':
                hue_down_result = True
            else:
                hue_down_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H140_CA_Hue(up_down).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H140_CA_Hue(up_down).png', current_image)
            case.result = compare_result and hue_up_result and hue_down_result

        with uuid("504ea93d-47b3-483f-b5f4-db9a4b72cd40") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Adjust Hue Slider = 20
            fix_enhance_page.enhance.color_adjustment.hue.adjust_slider(20)

            # Verify Hue = 20
            current_value = fix_enhance_page.enhance.color_adjustment.hue.get_value()
            logger(current_value)
            if current_value == '20':
                hue_down_result = True
            else:
                hue_down_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H140_CA_Hue(slider).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H140_CA_Hue(slider).png', current_image)
            case.result = compare_result and hue_down_result

        with uuid("9bad7be2-268e-493a-82da-cbfb8878c628") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Set Hue = 0 by keyboard inputting
            fix_enhance_page.enhance.color_adjustment.hue.set_value(0)

            # Verify Hue = 0
            current_value = fix_enhance_page.enhance.color_adjustment.hue.get_value()
            logger(current_value)
            if current_value == '0':
                hue_min_result = True
            else:
                hue_min_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H138_CA_Hue(0).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H138_CA_Hue(0).png', current_image)
            case.result = compare_result and hue_min_result

        with uuid("9bf27615-7015-40d3-9255-8c5b24cf975a") as case:
            # Switch to Color Adjustment > Set Hue = 200 by keyboard inputting
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Set Hue = 200 by keyboard inputting
            fix_enhance_page.enhance.color_adjustment.hue.set_value(200)

            # Verify Hue = 200
            current_value = fix_enhance_page.enhance.color_adjustment.hue.get_value()
            logger(current_value)
            if current_value == '200':
                hue_max_result = True
            else:
                hue_max_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H139_CA_Hue(200).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H139_CA_Hue(200).png', current_image)
            case.result = compare_result and hue_max_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid("bdd606e6-db3b-4d61-8fff-d55a8828a107") as case:
            # 1.7 Color Adjustment
            main_page.insert_media('Food.jpg')
            tips_area_page.click_fix_enhance()
            fix_enhance_page.is_in_fix_enhance()

            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Verify default Saturation = 100
            current_value = fix_enhance_page.enhance.color_adjustment.saturation.get_value()
            logger(current_value)
            if current_value == '100':
                saturation_result = True
            else:
                saturation_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H141_CA_Saturation(100).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H141_CA_Saturation(100).png', current_image)
            case.result = compare_result and saturation_result

        with uuid("29196787-1a3d-4f33-8c62-e875fcfa5e26") as case:
            # Switch to Color Adjustment > Adjust Saturation by Up and Down arrow
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Adjust Up x 2
            fix_enhance_page.enhance.color_adjustment.saturation.click_arrow(opt="up", times=2)
            # Verify Up x 2
            current_value = fix_enhance_page.enhance.color_adjustment.saturation.get_value()
            logger(current_value)
            if current_value == '102':
                saturation_up_result = True
            else:
                saturation_up_result = False

            # Adjust Down x 2
            fix_enhance_page.enhance.color_adjustment.saturation.click_arrow(opt="down", times=2)
            # Verify Down x 2
            current_value = fix_enhance_page.enhance.color_adjustment.saturation.get_value()
            logger(current_value)
            time.sleep(1)
            if current_value == '100':
                saturation_down_result = True
            else:
                saturation_down_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H145_CA_Saturation(up_down).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H145_CA_Saturation(up_down).png',
                                                     current_image)
            case.result = compare_result and saturation_up_result and saturation_down_result

        with uuid("84a00013-bf2a-4633-b774-2584c86c748e") as case:
            # Switch to Color Adjustment > Adjust Saturation Slider
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Adjust Saturation Slider = 40
            fix_enhance_page.enhance.color_adjustment.saturation.adjust_slider(40)

            # Verify Saturation = 40
            current_value = fix_enhance_page.enhance.color_adjustment.saturation.get_value()
            logger(current_value)
            if current_value == '40':
                saturation_down_result = True
            else:
                saturation_down_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H142_CA_Saturation(slider40).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H142_CA_Saturation(slider40).png',
                                                     current_image)
            case.result = compare_result and saturation_up_result and saturation_down_result

        with uuid("86cbab8a-c946-4ed8-a5ff-d9c730959ee4") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Set Saturation = 0 by keyboard inputting
            fix_enhance_page.enhance.color_adjustment.saturation.set_value(0)

            # Verify Saturation = 0
            current_value = fix_enhance_page.enhance.color_adjustment.saturation.get_value()
            logger(current_value)
            if current_value == '0':
                saturation_min_result = True
            else:
                saturation_min_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H143_CA_Saturation(0).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H143_CA_Saturation(0).png', current_image)
            case.result = compare_result and saturation_min_result

        with uuid("988c2e99-9a04-4846-91e8-4ba6c6f37d78") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            #  Set Saturation = 200 by keyboard inputting
            fix_enhance_page.enhance.color_adjustment.saturation.set_value(200)

            # Verify Saturation = 200
            current_value = fix_enhance_page.enhance.color_adjustment.saturation.get_value()
            logger(current_value)
            if current_value == '200':
                saturation_min_result = True
            else:
                saturation_min_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H144_CA_Saturation(200).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H144_CA_Saturation(200).png', current_image)
            case.result = compare_result and saturation_min_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid("cbb30b12-d778-4402-bec1-09210ddecd33") as case:
            # 1.7 Color Adjustment
            main_page.insert_media('Food.jpg')
            tips_area_page.click_fix_enhance()
            fix_enhance_page.is_in_fix_enhance()
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Verify Default Vibrancy = 100
            current_value = fix_enhance_page.enhance.color_adjustment.vibrancy.get_value()
            logger(current_value)
            if current_value == '0':
                vibrancy_result = True
            else:
                vibrancy_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H146_CA_Vibrancy(0).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H146_CA_Vibrancy(0).png', current_image)
            case.result = compare_result and vibrancy_result

        with uuid("4a781a86-738a-4f8d-bed2-f2f706ce4683") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Adjust Vibrancy by Up and Down arrow
            fix_enhance_page.enhance.color_adjustment.vibrancy.click_arrow(opt="up", times=2)
            # Verify Up x 2
            current_value = fix_enhance_page.enhance.color_adjustment.vibrancy.get_value()
            logger(current_value)
            if current_value == '2':
                vibrancy_up_result = True
            else:
                vibrancy_up_result = False

            fix_enhance_page.enhance.color_adjustment.vibrancy.click_arrow(opt="down", times=2)
            # Verify Down x 2
            current_value = fix_enhance_page.enhance.color_adjustment.vibrancy.get_value()
            logger(current_value)
            time.sleep(1)
            if current_value == '0':
                vibrancy_down_result = True
            else:
                vibrancy_down_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H146_CA_Vibrancy(0)_2.png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H146_CA_Vibrancy(0)_2.png', current_image)
            case.result = compare_result and vibrancy_up_result and vibrancy_down_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        with uuid("7e1798e9-6718-4378-ae73-d8f6b1f3f9c5") as case:

            main_page.close_and_restart_app()
            time.sleep(3)

            # 1.7 Color Adjustment
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Food.jpg')
            tips_area_page.click_fix_enhance()
            fix_enhance_page.is_in_fix_enhance()
            """
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(is_in_fix_enhance)
            """
            # Switch to Color Adjustment > Adjust Vibrancy Slider
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Adjust Vibrancy Slider = -50
            fix_enhance_page.enhance.color_adjustment.vibrancy.adjust_slider(-50)

            # Verify Vibrancy = -50
            current_value = fix_enhance_page.enhance.color_adjustment.vibrancy.get_value()
            logger(current_value)
            if current_value == '-50':
                vibrancy_result = True
            else:
                vibrancy_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'H147_CA_Vibrancy(slider-50).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H147_CA_Vibrancy(slider-50).png', current_image)
            case.result = compare_result and vibrancy_result


        with uuid("07d1104a-2fa9-4a36-b46b-88bd4c3fec4e") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Set Vibrancy = -100 by keyboard inputting
            fix_enhance_page.enhance.color_adjustment.vibrancy.set_value(-100)

            # Verify Vibrancy = -100
            current_value = fix_enhance_page.enhance.color_adjustment.vibrancy.get_value()
            logger(current_value)
            if current_value == '-100':
                vibrancy_min_result = True
            else:
                vibrancy_min_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'H148_CA_Vibrancy(-100).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H148_CA_Vibrancy(-100).png', current_image)
            case.result = compare_result and vibrancy_min_result


        with uuid("0f572a24-c3cf-40e1-a209-f70fbcfe4151") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Set Vibrancy = 100 by keyboard inputting
            fix_enhance_page.enhance.color_adjustment.vibrancy.set_value(100)

            # Verify Vibrancy = 100
            current_value = fix_enhance_page.enhance.color_adjustment.vibrancy.get_value()
            logger(current_value)
            if current_value == '100':
                vibrancy_max_result = True
            else:
                vibrancy_max_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H149_CA_Vibrancy(100).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H149_CA_Vibrancy(100).png', current_image)
            case.result = compare_result and vibrancy_max_result


    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        with uuid("fa5085b8-a1ec-4d12-88dd-2b7d8f123a27") as case:
            # 1.7 Color Adjustment
            main_page.insert_media('Food.jpg')
            tips_area_page.click_fix_enhance()
            fix_enhance_page.is_in_fix_enhance()
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Verify Default Highlight Healing = 0
            current_value = fix_enhance_page.enhance.color_adjustment.highlight_healing.get_value()
            logger(current_value)
            if current_value == '0':
                highlight_healing_default_min_result = True
            else:
                highlight_healing_default_min_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H151_CA_Highlight_Healing(0).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H151_CA_Highlight_Healing(0).png', current_image)
            case.result = compare_result and highlight_healing_default_min_result


        with uuid("44de4a85-822e-4205-beaa-f5d0b505b58a") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Adjust Highlight Healing by Up x 2
            fix_enhance_page.enhance.color_adjustment.highlight_healing.click_arrow(opt="up", times=2)
            # Verify Up x 2
            current_value = fix_enhance_page.enhance.color_adjustment.highlight_healing.get_value()
            logger(current_value)
            if current_value == '2':
                highlight_healing_up_result = True
            else:
                highlight_healing_up_result = False

            # Adjust Highlight Healing by Down x 2
            fix_enhance_page.enhance.color_adjustment.highlight_healing.click_arrow(opt="down", times=2)
            # Verify Down x 2
            current_value = fix_enhance_page.enhance.color_adjustment.highlight_healing.get_value()
            logger(current_value)
            time.sleep(1)
            if current_value == '0':
                highlight_healing_down_result = True
            else:
                highlight_healing_down_result = False

            case.result = highlight_healing_up_result and highlight_healing_down_result

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H154_CA_Highlight_Healing(up_down).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H154_CA_Highlight_Healing(up_down).png', current_image)
            case.result = compare_result and highlight_healing_up_result and highlight_healing_down_result


        with uuid("eb9e45cd-6948-472e-bbbc-e04b0f69eb62") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Adjust Highlight Healing Slider = 75
            fix_enhance_page.enhance.color_adjustment.highlight_healing.adjust_slider(75)

            # Verify Highlight Healing = 75
            current_value = fix_enhance_page.enhance.color_adjustment.highlight_healing.get_value()
            logger(current_value)
            if current_value == '75':
                highlight_healing_slider_result = True
            else:
                highlight_healing_slider_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H152_CA_Highlight_Healing(slider75).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H152_CA_Highlight_Healing(slider75).png', current_image)
            case.result = compare_result and highlight_healing_slider_result


        with uuid("ae628996-4132-449d-b708-2a300b70292c") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Set Highlight Healing = 100 by keyboard inputting
            fix_enhance_page.enhance.color_adjustment.highlight_healing.set_value(100)
            # Verify Highlight Healing = 100
            current_value = fix_enhance_page.enhance.color_adjustment.highlight_healing.get_value()
            logger(current_value)
            if current_value == '100':
                highlight_healing_result = True
            else:
                highlight_healing_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H153_CA_Highlight_Healing(100).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H153_CA_Highlight_Healing(100).png', current_image)
            case.result = compare_result and highlight_healing_result


    @exception_screenshot
    def test_1_1_9(self):
        with uuid("049a61e0-c94d-4b16-bfa5-d1faa8587d3f") as case:
            # 1.7 Color Adjustment
            main_page.insert_media('Food.jpg')
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            fix_enhance_page.is_in_fix_enhance()
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Verify default Shadow = 0
            current_value = fix_enhance_page.enhance.color_adjustment.shadow.get_value()
            logger(current_value)
            if current_value == '0':
                shadow_default_min_result = True
            else:
                shadow_default_min_result = False


            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H155_CA_Shadow(0).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H155_CA_Shadow(0).png', current_image)
            case.result = compare_result and shadow_default_min_result


        with uuid("d3254ce5-44fd-4388-b824-fefb02d24007") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Adjust Shadow by Up x 2
            fix_enhance_page.enhance.color_adjustment.shadow.click_arrow(opt="up", times=2)
            # Verify Up x 2
            current_value = fix_enhance_page.enhance.color_adjustment.shadow.get_value()
            logger(current_value)
            if current_value == '2':
                shadow_up_result = True
            else:
                shadow_up_result = False

            # Adjust Shadow by Down x 2
            fix_enhance_page.enhance.color_adjustment.shadow.click_arrow(opt="down", times=2)
            # Verify Down x 2
            current_value = fix_enhance_page.enhance.color_adjustment.shadow.get_value()
            logger(current_value)
            time.sleep(1)
            if current_value == '0':
                shadow_down_result = True
            else:
                shadow_down_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H158_CA_Shadow(up_down).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H158_CA_Shadow(up_down).png', current_image)
            case.result = compare_result and shadow_up_result and shadow_down_result


        with uuid("a4afaa0a-9d5c-4130-8377-384e0b53107e") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Adjust Shadow Slider = 30
            fix_enhance_page.enhance.color_adjustment.shadow.adjust_slider(30)

            # Verify Shadow = 30
            current_value = fix_enhance_page.enhance.color_adjustment.shadow.get_value()
            logger(current_value)
            if current_value == '30':
                shadow_slider_result = True
            else:
                shadow_slider_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H156_CA_Shadow(slider30).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H156_CA_Shadow(slider30).png', current_image)
            case.result = compare_result and shadow_slider_result


        with uuid("1627437a-f61a-4484-aeca-124eabcaaf06") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Set Shadow = 100 by keyboard inputting
            fix_enhance_page.enhance.color_adjustment.shadow.set_value(100)

            # Verify Shadow = 100
            current_value = fix_enhance_page.enhance.color_adjustment.shadow.get_value()
            logger(current_value)
            if current_value == '100':
                shadow_max_result = True
            else:
                shadow_max_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H157_CA_Shadow(100).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H157_CA_Shadow(100).png', current_image)
            case.result = compare_result and shadow_max_result


    @exception_screenshot
    def test_1_1_10(self):
        with uuid("76da2dab-390f-493d-9227-454df1b69172") as case:
            # 1.7 Color Adjustment
            main_page.insert_media('Food.jpg')
            tips_area_page.click_fix_enhance()
            fix_enhance_page.is_in_fix_enhance()
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Verify Default Sharpness = 0
            current_value = fix_enhance_page.enhance.color_adjustment.sharpness.get_value()
            logger(current_value)
            if current_value == '0':
                sharpness_default_min_result = True
            else:
                sharpness_default_min_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H159_CA_Sharpness(0).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H159_CA_Sharpness(0).png', current_image)
            case.result = compare_result and sharpness_default_min_result


        with uuid("306f9d09-9dfa-4fe2-b1a9-5efacbdfb091") as case:
            # Switch to Color Adjustment > Adjust Sharpness by Up and Down arrow
            fix_enhance_page.enhance.switch_to_color_adjustment()

            # Adjust Sharpness by Up x2
            fix_enhance_page.enhance.color_adjustment.sharpness.click_arrow(opt = "up", times=2)
            # Verify Up x 2
            current_value = fix_enhance_page.enhance.color_adjustment.sharpness.get_value()
            logger(current_value)
            if current_value == '2':
                sharpness_up_result = True
            else:
                sharpness_up_result = False

            # Adjust Sharpness by Down x2
            fix_enhance_page.enhance.color_adjustment.sharpness.click_arrow(opt = "down", times=2)
            # Verify Down x 2
            current_value = fix_enhance_page.enhance.color_adjustment.sharpness.get_value()
            logger(current_value)
            time.sleep(1)
            if current_value == '0':
                sharpness_down_result = True
            else:
                sharpness_down_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H159_CA_Sharpness(0)_2.png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H159_CA_Sharpness(0)_2.png', current_image)
            case.result = compare_result and sharpness_up_result and sharpness_down_result



        with uuid("eb768121-116d-45cb-86db-d5290c8f0d9e") as case:
            # Switch to Color Adjustment > Adjust Sharpness Slider
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Adjust Sharpness Slider = 55
            fix_enhance_page.enhance.color_adjustment.sharpness.adjust_slider(55)

            # Verify Sharpness = 55
            current_value = fix_enhance_page.enhance.color_adjustment.sharpness.get_value()
            logger(current_value)
            if current_value == '55':
                sharpness_slider_result = True
            else:
                sharpness_slider_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H160_CA_Sharpness(slider55).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H160_CA_Sharpness(slider55).png', current_image)
            case.result = compare_result and sharpness_slider_result


        with uuid("c481d00d-2794-4318-add8-7edc1cd310b2") as case:
            # Switch to Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Set Sharpness = 100 by keyboard inputting
            fix_enhance_page.enhance.color_adjustment.sharpness.set_value(100)

            # Verify Sharpness = 100
            current_value = fix_enhance_page.enhance.color_adjustment.sharpness.get_value()
            logger(current_value)
            if current_value == '100':
                sharpness_max_result = True
            else:
                sharpness_max_result = False

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H161_CA_Sharpness(100).png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H161_CA_Sharpness(100).png',
                                                     current_image)
            case.result = compare_result and sharpness_max_result


    @exception_screenshot
    def test_1_1_11(self):
        with uuid("63f3499b-3f98-40cd-9ebe-232497de42df") as case:
            # 1.7 Color Adjustment
            main_page.insert_media('Food.jpg')
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(is_in_fix_enhance)

            # Switch to Color Adjustment > Adjust Exposure Slider
            fix_enhance_page.enhance.switch_to_color_adjustment()
            fix_enhance_page.enhance.color_adjustment.exposure.adjust_slider(80)

            # Switch to Color Adjustment > Adjust Brightness Slider
            fix_enhance_page.enhance.switch_to_color_adjustment()
            fix_enhance_page.enhance.color_adjustment.brightness.adjust_slider(-60)

            # Switch to Color Adjustment > Adjust Contrast Slider
            fix_enhance_page.enhance.switch_to_color_adjustment()
            fix_enhance_page.enhance.color_adjustment.contrast.adjust_slider(90)

            # Switch to Color Adjustment > Adjust Hue Slider
            fix_enhance_page.enhance.switch_to_color_adjustment()
            fix_enhance_page.enhance.color_adjustment.hue.adjust_slider(20)

            # Switch to Color Adjustment > Adjust Saturation Slider
            fix_enhance_page.enhance.switch_to_color_adjustment()
            fix_enhance_page.enhance.color_adjustment.saturation.adjust_slider(40)

            # Switch to Color Adjustment > Adjust Vibrancy Slider
            fix_enhance_page.enhance.switch_to_color_adjustment()
            fix_enhance_page.enhance.color_adjustment.vibrancy.adjust_slider(-50)

            # Switch to Color Adjustment > Adjust Highlight Healing Slider
            fix_enhance_page.enhance.switch_to_color_adjustment()
            fix_enhance_page.enhance.color_adjustment.highlight_healing.adjust_slider(75)

            # Switch to Color Adjustment > Adjust Shadow Slider
            fix_enhance_page.enhance.switch_to_color_adjustment()
            fix_enhance_page.enhance.color_adjustment.shadow.adjust_slider(30)

            # Switch to Color Adjustment > Adjust Sharpness Slider
            fix_enhance_page.enhance.switch_to_color_adjustment()
            fix_enhance_page.enhance.color_adjustment.sharpness.adjust_slider(55)
            time.sleep(2)

            # Untick Color Adjustment checkbox
            fix_enhance_page.enhance.enable_color_adjustment(value=False)

            # Tick Color Adjustment checkbox
            fix_enhance_page.enhance.enable_color_adjustment()

            # Verify Color Adjustment checkbox
            checkbox_result = fix_enhance_page.enhance.get_color_adjustment()
            time.sleep(2)

            # Snapshot image of Color Adjustment checkbox ticked
            after_result = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                    file_name=Auto_Ground_Truth_Folder + 'H120_CA_Checked.png')

            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H120_CA_Checked.png', after_result)
            case.result = compare_result and checkbox_result

            """
            # For Color Adjustment Unchecked
            case.result = (not checkbox_result) and image_result
            """

            """
            # For Color Adjustment Unchecked * return value = False
            checkbox_result = fix_enhance_page.enhance.get_color_adjustment()
            if current_value == 'False':
                result = True
            else:
                result = False
            """

        with uuid("b791285a-63cb-4ce5-8def-9508eac81028") as case:

            # Reset Color Adjustment
            fix_enhance_page.click_reset()
            time.sleep(3)

            # Verify default Exposure value
            current_value = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            logger(current_value)
            if current_value == '100':
                exposure_result = True
            else:
                exposure_result = False

            # Verify default Brightness value
            current_value = fix_enhance_page.enhance.color_adjustment.brightness.get_value()
            logger(current_value)
            if current_value == '0':
                brightness_result = True
            else:
                brightness_result = False

            # Verify default Contrast value
            current_value = fix_enhance_page.enhance.color_adjustment.contrast.get_value()
            logger(current_value)
            if current_value == '0':
                contrast_result = True
            else:
                contrast_result = False

            # Verify default Hue value
            current_value = fix_enhance_page.enhance.color_adjustment.hue.get_value()
            logger(current_value)
            if current_value == '100':
                hue_result = True
            else:
                hue_result = False

            # Verify default Saturation value
            current_value = fix_enhance_page.enhance.color_adjustment.saturation.get_value()
            logger(current_value)
            if current_value == '100':
                saturation_result = True
            else:
                saturation_result = False

            # Verify default Vibrancy value
            current_value = fix_enhance_page.enhance.color_adjustment.vibrancy.get_value()
            logger(current_value)
            if current_value == '0':
                vibrancy_result = True
            else:
                vibrancy_result = False

            # Verify default Highlight_Healing value
            current_value = fix_enhance_page.enhance.color_adjustment.highlight_healing.get_value()
            logger(current_value)
            if current_value == '0':
                highlight_healing_result = True
            else:
                highlight_healing_result = False

            # Verify default Shadow value
            current_value = fix_enhance_page.enhance.color_adjustment.shadow.get_value()
            logger(current_value)
            if current_value == '0':
                shadow_result = True
            else:
                shadow_result = False

            # Verify default Sharpness value
            current_value = fix_enhance_page.enhance.color_adjustment.sharpness.get_value()
            logger(current_value)
            if current_value == '0':
                sharpness_result = True
            else:
                sharpness_result = False

            # Snapshot image of Reset to compare with "Original"
            after_result = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                    file_name=Auto_Ground_Truth_Folder + 'H163_CA_Reset.png')
            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H163_CA_Reset.png', after_result)

            case.result = compare_result and exposure_result and brightness_result and contrast_result and saturation_result and vibrancy_result and highlight_healing_result and shadow_result and sharpness_result


        with uuid("a4ccf8d5-6f24-493a-88d6-e7f66e0e2c49") as case:

            # Undo
            main_page.click_undo()
            time.sleep(1)

            # Tick "Compare with split preview" option
            fix_enhance_page.set_check_compare_in_split_preview(value=True)
            time.sleep(3)

            # Check Current testing image to be Original image or NOT
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'H164_CA_SplitPreview.png')

            # Compare result
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'H164_CA_SplitPreview.png', current_image)
            case.result = compare_result
