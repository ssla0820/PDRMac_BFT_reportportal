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
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
keyframe_room_page = PageFactory().get_page_object('keyframe_room_page', mwc)


# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Fix Enhance.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder - Setup for Overall Project
Ground_Truth_Folder = app.ground_truth_root + '/Fix_Enhance/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Fix_Enhance/'
Test_Material_Folder = app.testing_material

# For Ground Truth / Test Material folder - Setup for Duncan personal testing
# Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/GroundTruth/Title_Room/'
# Auto_Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/ATGroundTruth/Title_Room/'
# Test_Material_Folder = '/Users/cl/Desktop/Duncan/Material/'

DELAY_TIME = 1

class Test_Fix_Enhance():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
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
            google_sheet_execution_log_init('Fix_Enhance')

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

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_2_1(self):
        with uuid("b340e7f7-2285-4655-8d84-b28e4d8cf846") as case:
            # 1.2.1 White Balance - Enable White Balance checkbox - Apply the settings of White Balance
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Landscape 01.jpg')
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            fix_enhance_page.fix.enable_white_balance()
            # Compare image of preview window
            current_result = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-2-1_Enable_WB_checkbox.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-1_Enable_WB_checkbox.png', current_result)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("51f14e5f-2955-492a-88d3-50512a620363") as case:
            # 1.2.2 Select Color temperature and Tint - Apply the settings of Color temperature and Tint if White Balance checkbox enabled
            fix_enhance_page.fix.white_balance.color_temperature.set_value(30)
            fix_enhance_page.fix.white_balance.tint.set_value(90)
            # Compare image of preview window
            current_result = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-2-2_Apply_Settings_WB_Tint.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-2_Apply_Settings_WB_Tint.png', current_result)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_2_3(self):
        with uuid("db5374e0-55aa-4622-a120-cade951730af") as case:
            # 1.2.3 Color temperature and Tint - Color temperature - Default value=50
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Landscape 01.jpg')
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            # Snapshot image of preview window before WB is ticked
            before_result = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-2-3_Before.png')
            # Snapshot image of preview window after WB is ticked
            fix_enhance_page.fix.enable_white_balance()
            after_result = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-2-3_After.png')
            compare_result = media_room_page.compare(before_result, after_result)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("ebbc29a8-0034-445a-82b0-f58a774d02d0") as case:
            # 1.2.4 Color temperature and Tint - Color temperature - Slider
            # Adjust color temperature to 90 by slider
            fix_enhance_page.fix.white_balance.set_color_temperature_slider(90)
            current_image = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-2-4_ColorTemperature_Slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-4_ColorTemperature_Slider.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("42a4c9c4-18d5-4e46-816c-44f2c4abc314") as case:
            # 1.2.5 Color temperature and Tint - Color temperature - Set to 1 by keyboard inputting
            fix_enhance_page.fix.white_balance.color_temperature.set_value(1)
            result = fix_enhance_page.fix.white_balance.get_color_temperature_value()
            logger(f"{result= }")
            if not result == '1':
                case.result = False
            else:
                case.result = True

        with uuid("5d76aca8-eb50-4b1c-9843-eb9641e808d8") as case:
            # 1.2.6 Color temperature and Tint - Color temperature - Set to 100 by keyboard inputting
            fix_enhance_page.fix.white_balance.color_temperature.set_value(100)
            result = fix_enhance_page.fix.white_balance.get_color_temperature_value()
            logger(f"{result= }")
            if not result == '100':
                case.result = False
            else:
                case.result = True

        with uuid("29ce8cf0-22eb-49d2-bc1c-666d2b6c91e9") as case:
            # 1.2.7 Color temperature and Tint - Color temperature - Up/Down arrow
            # Press down
            fix_enhance_page.fix.white_balance.click_color_temperature_arrow(option="down")
            # Press up
            fix_enhance_page.fix.white_balance.click_color_temperature_arrow(option="up")
            result = fix_enhance_page.fix.white_balance.get_color_temperature_value()
            logger(f"{result= }")
            if not result == '100':
                case.result = False
            else:
                case.result = True

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_2_8(self):
        with uuid("db5374e0-55aa-4622-a120-cade951730af") as case:
            # 1.2.8 Color temperature and Tint - Color temperature - Default value=50
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Landscape 02.jpg')
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            # Snapshot image of preview window before WB is ticked
            before_result = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-2-8_Before.png')
            # Snapshot image of preview window after WB is ticked
            fix_enhance_page.fix.enable_white_balance()
            after_result = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-2-8_After.png')
            compare_result = media_room_page.compare(before_result, after_result)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("ebbc29a8-0034-445a-82b0-f58a774d02d0") as case:
            # 1.2.9 Color temperature and Tint - Color temperature - Slider
            # Adjust color temperature to 90 by slider
            fix_enhance_page.fix.white_balance.set_tint_slider(90)
            current_image = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-2-9_Tint_Slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-9_Tint_Slider.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("42a4c9c4-18d5-4e46-816c-44f2c4abc314") as case:
            # 1.2.10 Color temperature and Tint - Color temperature - Set to 1 by keyboard inputting
            fix_enhance_page.fix.white_balance.tint.set_value(1)
            result = fix_enhance_page.fix.white_balance.get_tint_value()
            logger(f"{result= }")
            if not result == '1':
                case.result = False
            else:
                case.result = True

        with uuid("5d76aca8-eb50-4b1c-9843-eb9641e808d8") as case:
            # 1.2.11 Color temperature and Tint - Color temperature - Set to 100 by keyboard inputting
            fix_enhance_page.fix.white_balance.tint.set_value(100)
            result = fix_enhance_page.fix.white_balance.get_tint_value()
            logger(f"{result= }")
            if not result == '100':
                case.result = False
            else:
                case.result = True

        with uuid("29ce8cf0-22eb-49d2-bc1c-666d2b6c91e9") as case:
            # 1.2.12 Color temperature and Tint - Color temperature - Up/Down arrow
            # Press down
            fix_enhance_page.fix.white_balance.click_tint_arrow(option="down")
            # Press up
            fix_enhance_page.fix.white_balance.click_tint_arrow(option="up")
            result = fix_enhance_page.fix.white_balance.get_tint_value()
            logger(f"{result= }")
            if not result == '100':
                case.result = False
            else:
                case.result = True

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_2_13(self):
        with uuid("126407cc-adf8-41c2-87af-e1b272f4c29d") as case:
            # 1.2.13 Select White calibration - Apply the settings of White calibration if White Balance checkbox enabled
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Landscape 02.jpg')
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            fix_enhance_page.fix.enable_white_balance()
            # Change white balance value first
            fix_enhance_page.fix.white_balance.tint.set_value(80)
            # Tick Apply the settings of White calibration
            fix_enhance_page.fix.white_balance.set_radio_button(option=1)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-2-13_White_Calibration.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-13_White_Calibration.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("b2ed6891-5557-487e-afbe-4c7f9ca3f799") as case:
            # 1.2.14 Click White calibration button - Enter White calibration setting dialog
            case.result = fix_enhance_page.fix.white_balance.click_white_calibrate_button()

        with uuid("7988af1a-6dac-4da6-bb7f-54c0a6364b79") as case:
            # 1.2.15 White calibration - (i) button - Show What is White Calibration? Dialog
            case.result = fix_enhance_page.fix.white_balance.white_calibration.click_i_button()

        with uuid("b6151426-5f21-49d4-9aad-fc5560eb1de7") as case:
            # 1.2.16 White calibration - Select color in Original window - The "Selected color would become what you choose
            # Select color in original window
            pos = fix_enhance_page.get_mouse_pos()
            logger(f"{pos= }")
            fix_enhance_page.mouse.move(550, 370)
            time.sleep(2)
            main_page.mouse.click()
            # Snapshot two parts to show the original preview and applied preview
            current_image = fix_enhance_page.snapshot(locator = L.fix_enhance.fix.white_balance.white_calibration.frame, file_name=Auto_Ground_Truth_Folder + '1-2-16_TwoParts.png')
            compare_result = fix_enhance_page.compare(Ground_Truth_Folder + '1-2-16_TwoParts.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("165c60d5-6e16-4c5f-8b2d-e318b0860149") as case:
            # 1.2.17 White calibration - Select color in Original window - The Calibrated window would become the calibrated result
            # Snapshot two parts to show the original preview and applied preview
            current_image = fix_enhance_page.snapshot(locator = L.fix_enhance.fix.white_balance.white_calibration.frame, file_name=Auto_Ground_Truth_Folder + '1-2-17_TwoParts.png')
            compare_result = fix_enhance_page.compare(Ground_Truth_Folder + '1-2-17_TwoParts.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("165c60d5-6e16-4c5f-8b2d-e318b0860149") as case:
            # 1.2.18 White calibration - [OK] - Apply settings
            fix_enhance_page.fix.white_balance.white_calibration.click_ok()
            current_image = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-2-18_Apply_White_Calibration.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-18_Apply_White_Calibration.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("165c60d5-6e16-4c5f-8b2d-e318b0860149") as case:
            # 1.2.19 White calibration - [Cancel] - Remove all the settings
            fix_enhance_page.fix.white_balance.click_white_calibrate_button()
            fix_enhance_page.mouse.move(305, 305)
            time.sleep(10)
            main_page.mouse.click()
            fix_enhance_page.fix.white_balance.white_calibration.click_cancel()
            current_image = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-2-18_Cancel_White_Calibration.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-2-18_Cancel_White_Calibration.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("06771037-e5a9-4bd1-897f-efff94f6fc1c") as case:
            # 1.2.20 Compare video qualities in split preview - The preview splits to two parts to show the original preview and applied preview
            current_image = fix_enhance_page.snapshot(locator = L.fix_enhance.fix.white_balance.white_calibration.frame, file_name=Auto_Ground_Truth_Folder + '1-2-20_TwoParts.png')
            compare_result = fix_enhance_page.compare(Ground_Truth_Folder + '1-2-20_TwoParts.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_3_1(self):
        with uuid("d1bfd4cd-bb4c-4c1d-a0f4-92239cc1dd6e") as case:
            # 1.3.1 Lens Correction - Checkbox - Unselect (default) - Won't Apply the settings of Lens Correction
            time.sleep(5)
            main_page.insert_media('Landscape 02.jpg')
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            # Tick lens correction option
            fix_enhance_page.fix.enable_lens_correction()
            # Default is unselected and verify preview window is no changed
            current_image = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-1_Unselect.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-1_Unselect.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_3_2(self):
        with uuid("7bf7cb1b-0c5d-4e69-9ac7-68b7e93bad73") as case:
            # 1.3.2 Lens Correction - Checkbox - Select - Build-in lens profile for selected clip - Apply the lens correction automatically
            time.sleep(5)
            main_page.insert_media('Landscape 02.jpg')
            time.sleep(5)
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            # Tick lens correction option - GoPro HERO7 Black (Wide)
            fix_enhance_page.fix.enable_lens_correction()
            fix_enhance_page.fix.lens_correction.select_marker_type('GoPro')
            fix_enhance_page.fix.lens_correction.select_model_type(18)
            # Default is unselected and verify preview window is no changed
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-2_Select_Build-in.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-2_Select_Build-in.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("74049f38-b5b3-4689-8524-ed7d116de4e7") as case:
            # 1.3.3 Lens Correction - Checkbox - Select - No Build-in lens profile for selected clip - Won't Apply the lens correction automatically
            fix_enhance_page.fix.enable_lens_correction(value=False)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-3_Select_Unselect.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-3_Select_Unselect.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("db28da39-c333-4ee9-b5c4-63e91132c64b") as case:
            # 1.3.4 Import Lens Profile	- via [Import Lens Profile] button - After importing, profile will add into Maker/Model list correctly
            fix_enhance_page.fix.enable_lens_correction()
            fix_enhance_page.fix.lens_correction.import_lens_profile(app.testing_material + '/Fix_Enhance/GoProHero4_SuperView.pdlcp')
            fix_enhance_page.fix.enable_lens_correction()
            fix_enhance_page.fix.lens_correction.select_marker_type('GoPro')
            fix_enhance_page.fix.lens_correction.select_model_type(5)
            current_image = fix_enhance_page.snapshot(locator = L.fix_enhance.fix.lens_correction.menu_model, file_name=Auto_Ground_Truth_Folder + '1-3-4_Model.png')
            compare_result = fix_enhance_page.compare(Ground_Truth_Folder + '1-3-4_Model.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("bea2c4e3-1cb8-4629-ba29-dd42ba83ef5e") as case:
            # 1.3.6 Import existed profile- No duplicate profile existed
            current_image = fix_enhance_page.snapshot(locator = L.fix_enhance.fix.lens_correction.menu_model, file_name=Auto_Ground_Truth_Folder + '1-3-6_Model.png')
            compare_result = fix_enhance_page.compare(Ground_Truth_Folder + '1-3-6_Model.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("d16c6ee2-f015-4268-ae47-0cd6c0de154f") as case:
            # 1.3.7 [Download More Lens Profile] button	- Link to DZ download website directly
            case.result = fix_enhance_page.fix.lens_correction.download_lens_profile()

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_3_8(self):
        with uuid("d16c6ee2-f015-4268-ae47-0cd6c0de154f") as case:
            # 1.3.8 Maker and Model - None - Model is disabled and No profile can be applied
            time.sleep(5)
            main_page.insert_media('Landscape 02.jpg')
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            # Tick lens correction option - GoPro HERO7 Black (Wide)
            fix_enhance_page.fix.enable_lens_correction()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-8_None.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-8_None.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0756e5a2-a5c7-446d-87f1-eac188a77fc6") as case:
            # 1.3.9 Maker and Model - Asus - Clip is fixed correctly after apply the profile
            fix_enhance_page.fix.lens_correction.select_marker_type('ASUS')
            fix_enhance_page.fix.lens_correction.select_model_type(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-9_Asus.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-9_Asus.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0756e5a2-a5c7-446d-87f1-eac188a77fc6") as case:
            # 1.3.10 Maker and Model - DJI - Clip is fixed correctly after apply the profile
            fix_enhance_page.fix.lens_correction.select_marker_type('DJI')
            fix_enhance_page.fix.lens_correction.select_model_type(2)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-10_DJI.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-10_DJI.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0756e5a2-a5c7-446d-87f1-eac188a77fc6") as case:
            # 1.3.11 Maker and Model - ELECOM - Clip is fixed correctly after apply the profile
            fix_enhance_page.fix.lens_correction.select_marker_type('ELECOM')
            fix_enhance_page.fix.lens_correction.select_model_type(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-11_ELECOM.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-11_ELECOM.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0756e5a2-a5c7-446d-87f1-eac188a77fc6") as case:
            # 1.3.12 Maker and Model - Garmin - Clip is fixed correctly after apply the profile
            fix_enhance_page.fix.lens_correction.select_marker_type('Garmin')
            fix_enhance_page.fix.lens_correction.select_model_type(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-12_Garmin.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-12_Garmin.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0756e5a2-a5c7-446d-87f1-eac188a77fc6") as case:
            # 1.3.13 Maker and Model - GoPro - Clip is fixed correctly after apply the profile
            fix_enhance_page.fix.lens_correction.select_marker_type('GoPro')
            fix_enhance_page.fix.lens_correction.select_model_type(15)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-13_GoPro.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-13_GoPro.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0756e5a2-a5c7-446d-87f1-eac188a77fc6") as case:
            # 1.3.14 Maker and Model - HTC - Model is disabled and No profile can be applied
            fix_enhance_page.fix.lens_correction.select_marker_type('HTC')
            fix_enhance_page.fix.lens_correction.select_model_type(0)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-14_HTC.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-14_HTC.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0756e5a2-a5c7-446d-87f1-eac188a77fc6") as case:
            # 1.3.15 Maker and Model - JVC - Model is disabled and No profile can be applied
            fix_enhance_page.fix.lens_correction.select_marker_type('JVC')
            fix_enhance_page.fix.lens_correction.select_model_type(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-15_JVC.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-15_JVC.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0756e5a2-a5c7-446d-87f1-eac188a77fc6") as case:
            # 1.3.16 Maker and Model - Liquid Image - Model is disabled and No profile can be applied
            fix_enhance_page.fix.lens_correction.select_marker_type('Liquid Image')
            fix_enhance_page.fix.lens_correction.select_model_type(0)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-16_LiquidImage.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-16_LiquidImage.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0756e5a2-a5c7-446d-87f1-eac188a77fc6") as case:
            # 1.3.17 Maker and Model - Olympus - Clip is fixed correctly after apply the profile
            fix_enhance_page.fix.lens_correction.select_marker_type('Olympus')
            fix_enhance_page.fix.lens_correction.select_model_type(0)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-17_Olympus.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-17_Olympus.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0756e5a2-a5c7-446d-87f1-eac188a77fc6") as case:
            # 1.3.18 Maker and Model - Panasonic - Clip is fixed correctly after apply the profile
            fix_enhance_page.fix.lens_correction.select_marker_type('Panasonic')
            fix_enhance_page.fix.lens_correction.select_model_type(2)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-18_Panasonic.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-18_Panasonic.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0756e5a2-a5c7-446d-87f1-eac188a77fc6") as case:
            # 1.3.19 Maker and Model - Polaroid - Model is disabled and No profile can be applied
            fix_enhance_page.fix.lens_correction.select_marker_type('Polaroid')
            fix_enhance_page.fix.lens_correction.select_model_type(0)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-18_Polaroid.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-19_Polaroid.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0756e5a2-a5c7-446d-87f1-eac188a77fc6") as case:
            # 1.3.20 Maker and Model - RICOH - Model is disabled and No profile can be applied
            fix_enhance_page.fix.lens_correction.select_marker_type('RICOH')
            fix_enhance_page.fix.lens_correction.select_model_type(4)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-20_RICOH.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-20_RICOH.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0756e5a2-a5c7-446d-87f1-eac188a77fc6") as case:
            # 1.3.21 Maker and Model - Rollei - Model is disabled and No profile can be applied
            fix_enhance_page.fix.lens_correction.select_marker_type('Rollei')
            fix_enhance_page.fix.lens_correction.select_model_type(0)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-21_Rollei.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-21_Rollei.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0756e5a2-a5c7-446d-87f1-eac188a77fc6") as case:
            # 1.3.22 Maker and Model - Sony - Model is disabled and No profile can be applied
            fix_enhance_page.fix.lens_correction.select_marker_type('Sony')
            fix_enhance_page.fix.lens_correction.select_model_type(10)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-22_Sony.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-22_Sony.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_3_23(self):
        with uuid("3b52ebc8-769f-45ec-a858-c139760e5e0e") as case:
            # 1.3.23 Fisheye distortion - Number - Default 0 - No fix apply on clip
            time.sleep(5)
            main_page.insert_media('Landscape 02.jpg')
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick lens correction option
            fix_enhance_page.fix.enable_lens_correction()
            # Check if default value of fisheye distortion is 0
            check_value = fix_enhance_page.fix.lens_correction.fisheye_distortion.get_value()
            if not check_value == '0':
                result = False
            else:
                result = True
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-23_before.png')
            fix_enhance_page.fix.lens_correction.fisheye_distortion.set_value(0)
            time.sleep(1)
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-23_before.png', current_image)
            logger(f"{compare_result= }")
            case.result = result and compare_result

        with uuid("cd67f952-b982-45f8-87a1-0c59e436658f") as case:
            # 1.3.24 Fisheye distortion - Number - max 100 - Show correct fix on preview screen correctly
            fix_enhance_page.fix.lens_correction.fisheye_distortion.set_value(100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-24_max.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-24_max.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("4bc36448-9b57-46b5-8aa4-73a55a716434") as case:
            # 1.3.25 Fisheye distortion - Number - min -100 - Show correct fix on preview screen correctly
            fix_enhance_page.fix.lens_correction.fisheye_distortion.set_value(-100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-25_min.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-25_min.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("ea05eff5-5130-408f-8b01-5fa5a9114d14") as case:
            # 1.3.26 Fisheye distortion - Adjustment - "+ /" button - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.fisheye_distortion.click_arrow(opt = "up", times=10)
            fix_enhance_page.fix.lens_correction.fisheye_distortion.click_arrow(opt = "down", times=10)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-26_button.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-26_button.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("53969d39-b67a-4825-869d-20ae2e8e0cb9") as case:
            # 1.3.27 Fisheye distortion - Adjustment - Slider - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.fisheye_distortion.adjust_slider(80)
            fix_enhance_page.fix.lens_correction.fisheye_distortion.adjust_slider(-80)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-27_slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-27_slider.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("151a8b06-94ce-4dfd-abeb-82b1ba0a16b0") as case:
            # 1.3.28 Fisheye distortion - Adjustment - keyboard inputting - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.fisheye_distortion.set_value(-50)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-28_keyboard.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-28_keyboard.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("1737c424-904c-4301-8ee8-d88f72a8ec49") as case:
            # 1.3.29 Fisheye distortion - Adjustment - Up/Down arrow- Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.fisheye_distortion.click_plus()
            fix_enhance_page.fix.lens_correction.fisheye_distortion.click_minus()
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-29_plus_minus.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-29_plus_minus.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result


    #@pytest.mark.skip
    @exception_screenshot
    def test_1_3_30(self):
        with uuid("c2e57eb5-4c9d-4706-b247-026abbf49ae0") as case:
            # 1.3.30 Vignette Removal - Vignette amount - Default 0 - No fix apply on clip
            time.sleep(5)
            main_page.insert_media('Landscape 02.jpg')
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick lens correction option
            fix_enhance_page.fix.enable_lens_correction()
            # Check if default value of Vignette Removal is 0
            check_value = fix_enhance_page.fix.lens_correction.vignette_amount.get_value()
            if not check_value == '0':
                result = False
            else:
                result = True
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-30_before.png')
            fix_enhance_page.fix.lens_correction.vignette_amount.set_value(0)
            time.sleep(1)
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-30_before.png', current_image)
            logger(f"{compare_result= }")
            case.result = result and compare_result
            case.result = compare_result

        with uuid("0c3146f3-f6ce-4353-af4f-68e93691ae1d") as case:
            # 1.3.31 Vignette Removal - Number - max 100 - Show correct fix on preview screen correctly
            fix_enhance_page.fix.lens_correction.vignette_amount.set_value(100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-31_max.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-31_max.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("3839536a-aac4-4c19-9025-bebd1705241c") as case:
            # 1.3.32 Vignette Removal - Number - min 0 - Show correct fix on preview screen correctly
            fix_enhance_page.fix.lens_correction.vignette_amount.set_value(0)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-32_min.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-32_min.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("4f882ab2-fb34-4326-8ea0-5442219f7be6") as case:
            # 1.3.33 Vignette Removal - Adjustment - "+ /" button - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_amount.click_arrow(opt = "up", times=10)
            fix_enhance_page.fix.lens_correction.vignette_amount.click_arrow(opt = "down", times=10)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-33_button.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-33_button.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("ccda8b7d-049c-4e1a-89e1-c28f97902213") as case:
            # 1.3.34 Vignette Removal - Adjustment - Slider - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_amount.adjust_slider(80)
            fix_enhance_page.fix.lens_correction.vignette_amount.adjust_slider(-80)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-34_slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-34_slider.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("1ffd0a24-0534-4501-9ef7-bb784b62683c") as case:
            # 1.3.35 Vignette Removal - Adjustment - keyboard inputting - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_amount.set_value(-50)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-35_keyboard.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-35_keyboard.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("fd629e6b-78d1-4030-8614-3d2c83f8af11") as case:
            # 1.3.36 Vignette Removal - Adjustment - Up/Down arrow- Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_amount.click_plus()
            fix_enhance_page.fix.lens_correction.vignette_amount.click_minus()
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-36_plus_minus.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-36_plus_minus.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result


    #@pytest.mark.skip
    @exception_screenshot
    def test_1_3_37(self):
        with uuid("2a3b7580-7c22-4751-922e-7de29a9e2f21") as case:
            # 1.3.37 Vignette Removal - Vignette midpoint - Disable (default) - When Vignette amount is 0
            time.sleep(5)
            main_page.insert_media('Landscape 02.jpg')
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick lens correction option
            fix_enhance_page.fix.enable_lens_correction()
            # Check if default of Vignette Midpoint is disabled
            current_image = fix_enhance_page.snapshot(locator = L.fix_enhance.fix.lens_correction.value_vignette_midpoint, file_name=Auto_Ground_Truth_Folder + '1-3-37_Disable.png')
            compare_result = fix_enhance_page.compare(Ground_Truth_Folder + '1-3-37_Disable.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("9f55c107-00a8-421a-b18c-c1e368c0c711") as case:
            # 1.3.38 Vignette Removal - Vignette Midpoint - Default 50 - Show correct fix on preview screen correctly
            # Adjust vignette amount to 1 fist
            fix_enhance_page.fix.lens_correction.vignette_amount.set_value(1)
            # Verify default value of vignette midpoint
            check_value = fix_enhance_page.fix.lens_correction.vignette_midpoint.get_value()
            if not check_value == '50':
                result = False
            else:
                result = True
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-38_before.png')
            # Verify result after setting to 50 for vignette midpoint
            fix_enhance_page.fix.lens_correction.vignette_amount.set_value(50)
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-38_before.png', current_image)
            logger(f"{compare_result= }")
            case.result = result and compare_result
            case.result = compare_result

        with uuid("da2b5955-cdac-4e82-abc8-8d748940c901") as case:
            # 1.3.39 Vignette Removal - Vignette Midpoint - Number - max 100 - Show correct fix on preview screen correctly
            fix_enhance_page.fix.lens_correction.vignette_midpoint.set_value(100)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-39_max.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-39_max.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("bf7816c4-619a-4aee-b5d1-2f4fdcaff66d") as case:
            # 1.3.40 Vignette Removal - Vignette Midpoint - Number - min 0 - Show correct fix on preview screen correctly
            fix_enhance_page.fix.lens_correction.vignette_midpoint.set_value(0)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-40_min.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-40_min.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("b20f12c1-95a3-4f53-b769-52ec0b5a7daf") as case:
            # 1.3.41 Vignette Removal - Vignette Midpoint - Adjustment - "+ /" button - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_midpoint.click_arrow(opt = "up", times=10)
            fix_enhance_page.fix.lens_correction.vignette_midpoint.click_arrow(opt = "down", times=10)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-41_button.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-41_button.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("3d72afc6-daf1-4e89-a6aa-922daedb9506") as case:
            # 1.3.42 Vignette Removal - Vignette Midpoint - Adjustment - Slider - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_midpoint.adjust_slider(80)
            fix_enhance_page.fix.lens_correction.vignette_midpoint.adjust_slider(-80)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-42_slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-42_slider.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("c26cecb1-56b1-486a-b4d2-0bf9b8d1f2e4") as case:
            # 1.3.43 Vignette Removal - Vignette Midpoint - Adjustment - keyboard inputting - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_midpoint.set_value(-50)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-43_keyboard.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-43_keyboard.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("3cfd7729-08b3-4203-897c-9c343c008d67") as case:
            # 1.3.44 Vignette Removal - Vignette Midpoint - Adjustment - Up/Down arrow- Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_midpoint.click_plus()
            fix_enhance_page.fix.lens_correction.vignette_midpoint.click_minus()
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-3-44_plus_minus.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-3-44_plus_minus.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result



    # =========================================

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_2_1(self):
        with uuid("414760e8-01b6-410c-8ccf-70c583f71d06") as case:
            # 2.2.1 White Balance - Enable White Balance checkbox - Apply the settings of White Balance
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Skateboard 01.mp4')
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            fix_enhance_page.fix.enable_white_balance()
            # Compare image of preview window
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '2-2-1_Enable_WB_checkbox.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-2-1_Enable_WB_checkbox.png',
                                                     current_result)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("f5ea2781-3b1a-4bcb-a98c-471107bbaf3c") as case:
            # 2.2.2 Select Color temperature and Tint - Apply the settings of Color temperature and Tint if White Balance checkbox enabled
            fix_enhance_page.fix.white_balance.color_temperature.set_value(30)
            fix_enhance_page.fix.white_balance.tint.set_value(90)
            # Compare image of preview window
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '2-2-2_Apply_Settings_WB_Tint.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-2-2_Apply_Settings_WB_Tint.png',
                                                     current_result)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_2_3(self):
        with uuid("07721efe-8872-4b66-896a-d2a888706c46") as case:
            # 2.2.3 Color temperature and Tint - Color temperature - Default value=50
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Skateboard 01.mp4')
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            # Snapshot image of preview window before WB is ticked
            before_result = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + '2-2-3_Before.png')
            # Snapshot image of preview window after WB is ticked
            fix_enhance_page.fix.enable_white_balance()
            after_result = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                    file_name=Auto_Ground_Truth_Folder + '2-2-3_After.png')
            compare_result = media_room_page.compare(before_result, after_result)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("3372a380-1391-49c7-9707-30867b8ec852") as case:
            # 2.2.4 Color temperature and Tint - Color temperature - Slider
            # Adjust color temperature to 90 by slider
            fix_enhance_page.fix.white_balance.set_color_temperature_slider(90)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + '2-2-4_ColorTemperature_Slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-2-4_ColorTemperature_Slider.png',
                                                     current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("7186164c-19d7-4d30-a9ce-d67289873375") as case:
            # 2.2.5 Color temperature and Tint - Color temperature - Set to 1 by keyboard inputting
            fix_enhance_page.fix.white_balance.color_temperature.set_value(1)
            result = fix_enhance_page.fix.white_balance.get_color_temperature_value()
            logger(f"{result= }")
            if not result == '1':
                case.result = False
            else:
                case.result = True

        with uuid("489feb9f-4616-4253-94e4-9653f4bf73db") as case:
            # 2.2.6 Color temperature and Tint - Color temperature - Set to 100 by keyboard inputting
            fix_enhance_page.fix.white_balance.color_temperature.set_value(100)
            time.sleep(1)
            result = fix_enhance_page.fix.white_balance.get_color_temperature_value()
            logger(f"{result= }")
            if not result == '100':
                case.result = False
            else:
                case.result = True

        with uuid("51978fdf-976f-4ea6-8c6d-cbf9ea60ce83") as case:
            # 2.2.7 Color temperature and Tint - Color temperature - Up/Down arrow
            # Press down
            fix_enhance_page.fix.white_balance.click_color_temperature_arrow(option="down")
            # Press up
            fix_enhance_page.fix.white_balance.click_color_temperature_arrow(option="up")
            result = fix_enhance_page.fix.white_balance.get_color_temperature_value()
            logger(f"{result= }")
            if not result == '100':
                case.result = False
            else:
                case.result = True

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_2_8(self):
        with uuid("16b17ad0-d2e8-453d-9063-6b518e4680c3") as case:
            # 2.2.8 Color temperature and Tint - Color temperature - Default value=50
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Skateboard 02.mp4')
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            # Snapshot image of preview window before WB is ticked
            before_result = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + '2-2-8_Before.png')
            # Snapshot image of preview window after WB is ticked
            fix_enhance_page.fix.enable_white_balance()
            after_result = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                    file_name=Auto_Ground_Truth_Folder + '2-2-8_After.png')
            compare_result = media_room_page.compare(before_result, after_result)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("d1bc1c78-fae4-4176-9ecc-81e83c0f679e") as case:
            # 2.2.9 Color temperature and Tint - Color temperature - Slider
            # Adjust color temperature to 90 by slider
            fix_enhance_page.fix.white_balance.set_tint_slider(90)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + '2-2-9_Tint_Slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-2-9_Tint_Slider.png',
                                                     current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("b8001529-5a0e-4570-8270-3740a14cb43e") as case:
            # 2.2.10 Color temperature and Tint - Color temperature - Set to 1 by keyboard inputting
            fix_enhance_page.fix.white_balance.tint.set_value(1)
            time.sleep(1)
            result = fix_enhance_page.fix.white_balance.get_tint_value()
            logger(f"{result= }")
            if not result == '1':
                case.result = False
            else:
                case.result = True

        with uuid("299fb468-3066-4aa6-977b-977e6ad95727") as case:
            # 2.2.11 Color temperature and Tint - Color temperature - Set to 100 by keyboard inputting
            fix_enhance_page.fix.white_balance.tint.set_value(100)
            time.sleep(1)
            result = fix_enhance_page.fix.white_balance.get_tint_value()
            logger(f"{result= }")
            if not result == '100':
                case.result = False
            else:
                case.result = True

        with uuid("9929fd59-2e0f-4cdb-9e7b-dcc7a7eeabf0") as case:
            # 2.2.12 Color temperature and Tint - Color temperature - Up/Down arrow
            # Press down
            fix_enhance_page.fix.white_balance.click_tint_arrow(option="down")
            # Press up
            fix_enhance_page.fix.white_balance.click_tint_arrow(option="up")
            result = fix_enhance_page.fix.white_balance.get_tint_value()
            logger(f"{result= }")
            if not result == '100':
                case.result = False
            else:
                case.result = True

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_2_13(self):
        with uuid("56654c6c-9866-4560-82c9-8bb15f88107c") as case:
            # 2.2.13 Select White calibration - Apply the settings of White calibration if White Balance checkbox enabled
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Skateboard 01.mp4')
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            fix_enhance_page.fix.enable_white_balance()
            # Change white balance value first
            fix_enhance_page.fix.white_balance.tint.set_value(80)
            # Tick Apply the settings of White calibration
            fix_enhance_page.fix.white_balance.set_radio_button(option=1)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + '2-2-13_White_Calibration.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-2-13_White_Calibration.png',
                                                     current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("c456c377-367f-46d7-933a-e8577607a1c1") as case:
            # 2.2.14 Click White calibration button - Enter White calibration setting dialog
            case.result = fix_enhance_page.fix.white_balance.click_white_calibrate_button()

        with uuid("47fbcbed-ba9b-4b5e-b8e9-544c0b2d7e86") as case:
            # 2.2.15 White calibration - (i) button - Show What is White Calibration? Dialog
            case.result = fix_enhance_page.fix.white_balance.white_calibration.click_i_button()

        with uuid("8bb76e40-6705-488b-896e-fe8face7cee4") as case:
            # 2.2.16 White calibration - Select color in Original window - The "Selected color would become what you choose
            # Select color in original window
            pos = fix_enhance_page.get_mouse_pos()
            logger(f"{pos= }")
            fix_enhance_page.mouse.move(550, 370)
            time.sleep(2)
            main_page.mouse.click()
            # Snapshot two parts to show the original preview and applied preview
            current_image = fix_enhance_page.snapshot(
                locator=L.fix_enhance.fix.white_balance.white_calibration.frame,
                file_name=Auto_Ground_Truth_Folder + '2-2-16_TwoParts.png')
            compare_result_a = fix_enhance_page.compare(Ground_Truth_Folder + '2-2-16_TwoParts.png',
                                                      current_image)
            logger(f"{compare_result= }")

            # 2.2.16-b White calibration - Select color in Original window - The Calibrated window would become the calibrated result
            # Snapshot two parts to show the original preview and applied preview
            current_image = fix_enhance_page.snapshot(
                locator=L.fix_enhance.fix.white_balance.white_calibration.frame,
                file_name=Auto_Ground_Truth_Folder + '2-2-17_TwoParts.png')
            compare_result_b = fix_enhance_page.compare(Ground_Truth_Folder + '2-2-17_TwoParts.png',
                                                      current_image)
            logger(f"{compare_result= }")
            case.result = compare_result_a and compare_result_a

        with uuid("e29e47d9-f2a3-4fab-b1b4-f293571ba244") as case:
            # 2.2.17 White calibration - [OK] - Apply settings
            fix_enhance_page.fix.white_balance.white_calibration.click_ok()
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + '2-2-17_Apply_White_Calibration.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-2-17_Apply_White_Calibration.png',
                                                     current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("8af4429e-001e-4fc1-8629-2ca81e693ef6") as case:
            # 2.2.18 White calibration - [Cancel] - Remove all the settings
            fix_enhance_page.fix.white_balance.click_white_calibrate_button()
            fix_enhance_page.mouse.move(305, 305)
            time.sleep(10)
            main_page.mouse.click()
            fix_enhance_page.fix.white_balance.white_calibration.click_cancel()
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + '2-2-18_Cancel_White_Calibration.png')
            compare_result = media_room_page.compare(
                Ground_Truth_Folder + '2-2-18_Cancel_White_Calibration.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("5d5ad31a-4975-4895-bfe4-12940675b259") as case:
            # 2.2.19 Compare video qualities in split preview - The preview splits to two parts to show the original preview and applied preview
            current_image = fix_enhance_page.snapshot(
                locator=L.fix_enhance.fix.white_balance.white_calibration.frame,
                file_name=Auto_Ground_Truth_Folder + '2-2-19_TwoParts.png')
            compare_result = fix_enhance_page.compare(Ground_Truth_Folder + '2-2-19_TwoParts.png',
                                                      current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_4_1(self):
        with uuid("6a8f6624-4f03-4793-8708-ca1d640a6e44") as case:
            # 2.4.1 Lens Correction - Checkbox - Unselect (default) - Won't Apply the settings of Lens Correction
            time.sleep(5)
            main_page.set_project_aspect_ratio_4_3()
            media_room_page.import_media_file(app.testing_material + '/Fix_Enhance/GoProHero7.mp4')
            media_room_page.high_definition_video_confirm_dialog_click_no()
            main_page.insert_media('GoProHero7.MP4')
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            # Tick lens correction option
            fix_enhance_page.fix.enable_lens_correction()
            # Default is unselected and verify preview window is no changed
            current_image = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-1_Unselect.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-1_Unselect.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_4_2(self):
        with uuid("8354a1ad-2e30-42d6-93b0-c2a16fac8391") as case:
            # 2.4.2 Lens Correction - Checkbox - Select - Build-in lens profile for selected clip - Apply the lens correction automatically
            time.sleep(5)
            main_page.set_project_aspect_ratio_4_3()
            media_room_page.import_media_file(app.testing_material + '/Fix_Enhance/GoProHero7.mp4')
            main_page.insert_media('GoProHero7.MP4')
            main_page.set_timeline_timecode('00_00_02_28', is_verify=False)
            time.sleep(5)
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            # Tick lens correction option - GoPro HERO7 Black (Wide)
            fix_enhance_page.fix.enable_lens_correction()
            fix_enhance_page.fix.lens_correction.select_marker_type('GoPro')
            fix_enhance_page.fix.lens_correction.select_model_type(18)
            # Default is unselected and verify preview window is no changed
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-2_Select_Build-in.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-2_Select_Build-in.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("5ad8f068-2d6a-4334-967d-fe5b1b8e39cb") as case:
            # 2.4.3 Lens Correction - Checkbox - Select - No Build-in lens profile for selected clip - Won't Apply the lens correction automatically
            fix_enhance_page.fix.enable_lens_correction(value=False)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-3_Select_Unselect.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-3_Select_Unselect.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("d63e37ed-02f8-48da-9559-f81e43f1c7e9") as case:
            # 2.4.4 Import Lens Profile	- via [Import Lens Profile] button - After importing, profile will add into Maker/Model list correctly
            fix_enhance_page.fix.enable_lens_correction()
            fix_enhance_page.fix.lens_correction.import_lens_profile(app.testing_material + '/Fix_Enhance/GoProHero4_SuperView.pdlcp')
            fix_enhance_page.fix.enable_lens_correction()
            fix_enhance_page.fix.lens_correction.select_marker_type('GoPro')
            fix_enhance_page.fix.lens_correction.select_model_type(5)
            current_image = fix_enhance_page.snapshot(locator = L.fix_enhance.fix.lens_correction.menu_model, file_name=Auto_Ground_Truth_Folder + '2-4-4_Model.png')
            compare_result = fix_enhance_page.compare(Ground_Truth_Folder + '2-4-4_Model.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("dad0f99e-6601-431b-b8bf-0d7fd2bb115d") as case:
            # 2.4.6 Import existed profile- No duplicate profile existed
            current_image = fix_enhance_page.snapshot(locator = L.fix_enhance.fix.lens_correction.menu_model, file_name=Auto_Ground_Truth_Folder + '2-4-6_Model.png')
            compare_result = fix_enhance_page.compare(Ground_Truth_Folder + '2-4-6_Model.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("18669f2c-a61f-4125-b21b-42b520e72624") as case:
            # 2.4.7 [Download More Lens Profile] button	- Link to DZ download website directly
            case.result = fix_enhance_page.fix.lens_correction.download_lens_profile()

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_4_8(self):
        with uuid("1e8cea5f-caa6-4ae6-99ec-ee37f5e88791") as case:
            # 2.4.8 Maker and Model - None - Model is disabled and No profile can be applied
            time.sleep(5)
            main_page.set_project_aspect_ratio_4_3()
            media_room_page.import_media_file(app.testing_material + '/Fix_Enhance/GoProHero7.mp4')
            main_page.insert_media('GoProHero7.MP4')
            main_page.set_timeline_timecode('00_00_02_28', is_verify=False)
            tips_area_page.click_fix_enhance()
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            # Tick lens correction option - GoPro HERO7 Black (Wide)
            fix_enhance_page.fix.enable_lens_correction()
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-8_None.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-8_None.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("1d4425a2-94be-4ffc-b5e4-7ae65026b275") as case:
            # 2.4.9 Maker and Model - Asus - Clip is fixed correctly after apply the profile
            fix_enhance_page.fix.lens_correction.select_marker_type('ASUS')
            fix_enhance_page.fix.lens_correction.select_model_type(1)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-9_Asus.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-9_Asus.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("89ea9503-0e99-4ed7-ae29-f867e51df258") as case:
            # 2.4.10 Maker and Model - DJI - Clip is fixed correctly after apply the profile
            fix_enhance_page.fix.lens_correction.select_marker_type('DJI')
            fix_enhance_page.fix.lens_correction.select_model_type(2)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-10_DJI.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-10_DJI.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("d6a5823e-ce01-4301-8b62-5aeb3499be77") as case:
            # 2.4.11 Maker and Model - ELECOM - Clip is fixed correctly after apply the profile
            fix_enhance_page.fix.lens_correction.select_marker_type('ELECOM')
            fix_enhance_page.fix.lens_correction.select_model_type(1)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-11_ELECOM.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-11_ELECOM.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("8c1cc57f-5a9a-479e-9e70-8a43fee78d40") as case:
            # 2.4.12 Maker and Model - Garmin - Clip is fixed correctly after apply the profile
            fix_enhance_page.fix.lens_correction.select_marker_type('Garmin')
            fix_enhance_page.fix.lens_correction.select_model_type(1)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-12_Garmin.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-12_Garmin.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("d77b5a21-4296-480b-bf9e-2235b904ef54") as case:
            # 2.4.13 Maker and Model - GoPro - Clip is fixed correctly after apply the profile
            fix_enhance_page.fix.lens_correction.select_marker_type('GoPro')
            fix_enhance_page.fix.lens_correction.select_model_type(15)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-13_GoPro.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-13_GoPro.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("cac7858e-325f-46b7-ab74-1bd501db3281") as case:
            # 2.4.14 Maker and Model - HTC - Model is disabled and No profile can be applied
            fix_enhance_page.fix.lens_correction.select_marker_type('HTC')
            fix_enhance_page.fix.lens_correction.select_model_type(0)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-14_HTC.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-14_HTC.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("9bf52a41-1791-4ddb-9b70-fb7c1a0d3aa1") as case:
            # 2.4.15 Maker and Model - JVC - Model is disabled and No profile can be applied
            fix_enhance_page.fix.lens_correction.select_marker_type('JVC')
            fix_enhance_page.fix.lens_correction.select_model_type(1)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-15_JVC.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-15_JVC.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("597973cb-fc60-4da2-9d19-3ea807c17b94") as case:
            # 2.4.16 Maker and Model - Liquid Image - Model is disabled and No profile can be applied
            fix_enhance_page.fix.lens_correction.select_marker_type('Liquid Image')
            fix_enhance_page.fix.lens_correction.select_model_type(0)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-16_LiquidImage.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-16_LiquidImage.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("a2cc268c-2d74-4113-8b7a-7d0041bd066c") as case:
            # 2.4.17 Maker and Model - Olympus - Clip is fixed correctly after apply the profile
            fix_enhance_page.fix.lens_correction.select_marker_type('Olympus')
            fix_enhance_page.fix.lens_correction.select_model_type(0)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-17_Olympus.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-17_Olympus.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("70308915-f40c-420c-836c-2e85b6547d59") as case:
            # 2.4.18 Maker and Model - Panasonic - Clip is fixed correctly after apply the profile
            fix_enhance_page.fix.lens_correction.select_marker_type('Panasonic')
            fix_enhance_page.fix.lens_correction.select_model_type(2)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-18_Panasonic.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-18_Panasonic.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("aefd89d7-d20b-462f-b41d-55ea027b0f06") as case:
            # 2.4.19 Maker and Model - Polaroid - Model is disabled and No profile can be applied
            fix_enhance_page.fix.lens_correction.select_marker_type('Polaroid')
            fix_enhance_page.fix.lens_correction.select_model_type(0)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-18_Polaroid.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-19_Polaroid.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("0785c7dd-3351-4cc6-a341-c993fdf3983c") as case:
            # 2.4.20 Maker and Model - RICOH - Model is disabled and No profile can be applied
            fix_enhance_page.fix.lens_correction.select_marker_type('RICOH')
            fix_enhance_page.fix.lens_correction.select_model_type(4)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-20_RICOH.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-20_RICOH.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("b3ba6320-db4d-416c-b3ca-48176ef9cb33") as case:
            # 2.4.21 Maker and Model - Rollei - Model is disabled and No profile can be applied
            fix_enhance_page.fix.lens_correction.select_marker_type('Rollei')
            fix_enhance_page.fix.lens_correction.select_model_type(0)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-21_Rollei.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-21_Rollei.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("303ed176-b3a3-47d4-b62c-d32825b8d957") as case:
            # 2.4.22 Maker and Model - Sony - Model is disabled and No profile can be applied
            fix_enhance_page.fix.lens_correction.select_marker_type('Sony')
            fix_enhance_page.fix.lens_correction.select_model_type(10)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-22_Sony.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-22_Sony.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_4_23(self):
        with uuid("869d4312-3afa-40a8-8bdd-12eb41978870") as case:
            # 2.4.23 Fisheye distortion - Number - Default 0 - No fix apply on clip
            time.sleep(5)
            main_page.set_project_aspect_ratio_4_3()
            media_room_page.import_media_file(app.testing_material + '/Fix_Enhance/GoProHero7.mp4')
            main_page.insert_media('GoProHero7.MP4')
            main_page.set_timeline_timecode('00_00_02_28', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick lens correction option
            fix_enhance_page.fix.enable_lens_correction()
            # Check if default value of fisheye distortion is 0
            check_value = fix_enhance_page.fix.lens_correction.fisheye_distortion.get_value()
            if not check_value == '0':
                result = False
            else:
                result = True
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-23_before.png')
            fix_enhance_page.fix.lens_correction.fisheye_distortion.set_value(0)
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-23_before.png', current_image)
            logger(f"{compare_result= }")
            case.result = result and compare_result

        with uuid("b2baabd9-1776-405f-9290-c60360c6a57f") as case:
            # 2.4.24 Fisheye distortion - Number - max 100 - Show correct fix on preview screen correctly
            fix_enhance_page.fix.lens_correction.fisheye_distortion.set_value(100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-24_max.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-24_max.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("d1c9a241-30bd-4ab2-acff-1c1fff26928b") as case:
            # 2.4.25 Fisheye distortion - Number - min -100 - Show correct fix on preview screen correctly
            fix_enhance_page.fix.lens_correction.fisheye_distortion.set_value(-100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-25_min.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-25_min.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("7be8363e-ccc0-4dcc-b870-7ee067219ada") as case:
            # 2.4.26 Fisheye distortion - Adjustment - "+ /" button - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.fisheye_distortion.click_arrow(opt = "up", times=10)
            fix_enhance_page.fix.lens_correction.fisheye_distortion.click_arrow(opt = "down", times=10)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-26_button.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-26_button.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("80cf513e-3c9f-4528-b69b-d0b8664257af") as case:
            # 2.4.27 Fisheye distortion - Adjustment - Slider - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.fisheye_distortion.adjust_slider(80)
            fix_enhance_page.fix.lens_correction.fisheye_distortion.adjust_slider(-80)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-27_slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-27_slider.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("7f59c177-68f4-4f3a-aa70-942ac719b259") as case:
            # 2.4.28 Fisheye distortion - Adjustment - keyboard inputting - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.fisheye_distortion.set_value(-50)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-28_keyboard.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-28_keyboard.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("c4484c29-ab5e-40e7-8ccf-f0f9d2bc62b7") as case:
            # 2.4.29 Fisheye distortion - Adjustment - Up/Down arrow- Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.fisheye_distortion.click_plus()
            fix_enhance_page.fix.lens_correction.fisheye_distortion.click_minus()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-29_plus_minus.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-29_plus_minus.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result


    #@pytest.mark.skip
    @exception_screenshot
    def test_2_4_30(self):
        with uuid("cf0cfa02-89b8-4229-8347-9848477786b7") as case:
            # 2.4.30 Vignette Removal - Vignette amount - Default 0 - No fix apply on clip
            time.sleep(5)
            main_page.set_project_aspect_ratio_4_3()
            media_room_page.import_media_file(app.testing_material + '/Fix_Enhance/GoProHero7.mp4')
            main_page.insert_media('GoProHero7.MP4')
            main_page.set_timeline_timecode('00_00_02_28', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick lens correction option
            fix_enhance_page.fix.enable_lens_correction()
            # Check if default value of Vignette Removal is 0
            check_value = fix_enhance_page.fix.lens_correction.vignette_amount.get_value()
            if not check_value == '0':
                result = False
            else:
                result = True
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-30_before.png')
            fix_enhance_page.fix.lens_correction.vignette_amount.set_value(0)
            time.sleep(1)
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-30_before.png', current_image)
            logger(f"{compare_result= }")
            case.result = result and compare_result
            case.result = compare_result

        with uuid("70f609e0-4ee6-47f0-96c1-70629a201685") as case:
            # 2.4.31 Vignette Removal - Number - max 100 - Show correct fix on preview screen correctly
            fix_enhance_page.fix.lens_correction.vignette_amount.set_value(100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-31_max.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-31_max.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("35a09d88-4649-444b-9926-fe3f6006798b") as case:
            # 2.4.32 Vignette Removal - Number - min 0 - Show correct fix on preview screen correctly
            fix_enhance_page.fix.lens_correction.vignette_amount.set_value(0)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-32_min.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-32_min.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("53f50002-7b10-4069-83bd-bb857a6625b3") as case:
            # 2.4.33 Vignette Removal - Adjustment - "+ /" button - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_amount.click_arrow(opt = "up", times=10)
            fix_enhance_page.fix.lens_correction.vignette_amount.click_arrow(opt = "down", times=10)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-33_button.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-33_button.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("bffacc37-03ce-4dc1-9b75-290b533f50b7") as case:
            # 2.4.34 Vignette Removal - Adjustment - Slider - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_amount.adjust_slider(80)
            fix_enhance_page.fix.lens_correction.vignette_amount.adjust_slider(-80)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-34_slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-34_slider.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("6e062864-e6d8-4843-a97d-c6f7cca4f880") as case:
            # 2.4.35 Vignette Removal - Adjustment - keyboard inputting - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_amount.set_value(-50)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-35_keyboard.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-35_keyboard.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("4f15c4bd-d570-495e-839d-ceb8bd32f6ee") as case:
            # 2.4.36 Vignette Removal - Adjustment - Up/Down arrow- Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_amount.click_plus()
            fix_enhance_page.fix.lens_correction.vignette_amount.click_minus()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-36_plus_minus.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-36_plus_minus.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result


    #@pytest.mark.skip
    @exception_screenshot
    def test_2_4_37(self):
        with uuid("61b0b383-3e66-47d3-a944-1a577d3f6f1f") as case:
            # 2.4.37 Vignette Removal - Vignette midpoint - Disable (default) - When Vignette amount is 0
            time.sleep(5)
            main_page.set_project_aspect_ratio_4_3()
            media_room_page.import_media_file(app.testing_material + '/Fix_Enhance/GoProHero7.mp4')
            main_page.insert_media('GoProHero7.MP4')
            main_page.set_timeline_timecode('00_00_02_28', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick lens correction option
            fix_enhance_page.fix.enable_lens_correction()
            # Check if default of Vignette Midpoint is disabled
            current_image = fix_enhance_page.snapshot(locator = L.fix_enhance.fix.lens_correction.value_vignette_midpoint, file_name=Auto_Ground_Truth_Folder + '2-4-37_Disable.png')
            compare_result = fix_enhance_page.compare(Ground_Truth_Folder + '2-4-37_Disable.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("54ba9b93-9657-4e88-8991-24c403a00153") as case:
            # 2.4.38 Vignette Removal - Vignette Midpoint - Default 50 - Show correct fix on preview screen correctly
            # Adjust vignette amount to 1 fist
            fix_enhance_page.fix.lens_correction.vignette_amount.set_value(1)
            # Verify default value of vignette midpoint
            check_value = fix_enhance_page.fix.lens_correction.vignette_midpoint.get_value()
            if not check_value == '50':
                result = False
            else:
                result = True
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-38_before.png')
            # Verify result after setting to 50 for vignette midpoint
            fix_enhance_page.fix.lens_correction.vignette_amount.set_value(50)
            time.sleep(1)
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-38_before.png', current_image)
            logger(f"{compare_result= }")
            case.result = result and compare_result
            case.result = compare_result

        with uuid("7f550e60-0c1b-4262-a7c7-0fbf028aa8a7") as case:
            # 2.4.39 Vignette Removal - Vignette Midpoint - Number - max 100 - Show correct fix on preview screen correctly
            fix_enhance_page.fix.lens_correction.vignette_midpoint.set_value(100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-39_max.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-39_max.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("9106efbc-7a4b-4797-bf63-1f01b13bfd21") as case:
            # 2.4.40 Vignette Removal - Vignette Midpoint - Number - min 0 - Show correct fix on preview screen correctly
            fix_enhance_page.fix.lens_correction.vignette_midpoint.set_value(0)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-40_min.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-40_min.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("772da30f-9f27-4007-b8b4-ed5fe302e398") as case:
            # 2.4.41 Vignette Removal - Vignette Midpoint - Adjustment - "+ /" button - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_midpoint.click_arrow(opt = "up", times=10)
            fix_enhance_page.fix.lens_correction.vignette_midpoint.click_arrow(opt = "down", times=10)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-41_button.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-41_button.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("f0598c9d-f63a-47e7-8605-7171410a982b") as case:
            # 2.4.42 Vignette Removal - Vignette Midpoint - Adjustment - Slider - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_midpoint.adjust_slider(80)
            fix_enhance_page.fix.lens_correction.vignette_midpoint.adjust_slider(-80)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-42_slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-42_slider.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("05e2d1ae-31f9-4928-989b-fe3f2a6f214b") as case:
            # 2.4.43 Vignette Removal - Vignette Midpoint - Adjustment - keyboard inputting - Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_midpoint.set_value(-50)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-43_keyboard.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-43_keyboard.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("79956aa0-d455-4ac6-af07-0f5009328fe5") as case:
            # 2.4.44 Vignette Removal - Vignette Midpoint - Adjustment - Up/Down arrow- Number adjustment and fix apply on preview directly
            fix_enhance_page.fix.lens_correction.vignette_midpoint.click_plus()
            fix_enhance_page.fix.lens_correction.vignette_midpoint.click_minus()
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-4-44_plus_minus.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-4-44_plus_minus.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result


    #@pytest.mark.skip
    @exception_screenshot
    def test_2_3_1(self):
        with uuid("c180d0c3-3def-4bea-8b1e-8103f926e265") as case:
            # 2.3.1 Video Stabilizer - Video Stabilizer checkbox - Tick - Single video - Apply the settings of Video Stabilizer, default level is 50
            time.sleep(5)
            main_page.set_project_aspect_ratio_4_3()
            media_room_page.import_media_file(app.testing_material + '/Fix_Enhance/GoProHero7.mp4')
            #media_room_page.high_definition_video_confirm_dialog_click_no()
            main_page.insert_media('GoProHero7.MP4')
            main_page.set_timeline_timecode('00_00_02_28', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick video stabilizer option
            fix_enhance_page.fix.enable_video_stabilizer()
            # Check default value of video stabilizer
            check_value = fix_enhance_page.fix.video_stabilizer.correction_level.get_value()
            logger(f"{check_value= }")
            if not check_value == '50':
                result = False
            else:
                result = True
            # Snapshot when apply default value of video stabilizer
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-3-1_Apply_VS_Default.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-3-1_Apply_VS_Default.png', current_image)
            logger(f"{compare_result= }")
            case.result = check_value and compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_3_2(self):
        with uuid("82ff407b-3e01-4232-a8dc-376a72cb8351") as case:
            # 2.3.2 Video Stabilizer - Video Stabilizer checkbox - Tick - Multiple video - Apply the settings of Video Stabilizer, default level is 50
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            # Import 2 clips into timeline
            main_page.insert_media('Skateboard 01.mp4')
            media_room_page.hover_library_media('Skateboard 02.mp4')
            main_page.drag_media_to_timeline_clip('Skateboard 01.mp4', 0, 1, 1)
            # Select all clips in timeline
            timeline_operation_page.select_multiple_timeline_media(media1_track_index=0, media1_clip_index=0, media2_track_index=0, media2_clip_index=1)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick video stabilizer option
            fix_enhance_page.fix.enable_video_stabilizer()
            # Snapshot when apply default value of video stabilizer
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-3-2_Apply_VS_Multiple.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-3-2_Apply_VS_Multiple.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_3_3(self):
        with uuid("1c571164-aa5d-4e89-8a44-06616799f3da") as case:
            # 2.3.3 Video Stabilizer - Video Stabilizer checkbox - UnTick - No fix applied
            time.sleep(5)
            main_page.set_project_aspect_ratio_4_3()
            media_room_page.import_media_file(app.testing_material + '/Fix_Enhance/GoProHero7.mp4')
            #media_room_page.high_definition_video_confirm_dialog_click_no()
            main_page.insert_media('GoProHero7.MP4')
            main_page.set_timeline_timecode('00_00_02_28', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick and untick video stabilizer option
            fix_enhance_page.fix.enable_video_stabilizer()
            fix_enhance_page.fix.enable_video_stabilizer(value=False)
            # Snapshot when untick video stabilizer
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-3-3_Untick.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-3-3_Untick.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_3_4(self):
        with uuid("00502774-0cab-424e-aead-1431760de174") as case:
            # 2.3.4 Video Stabilizer - Apply Video Stabilizer to correct shaky video - [+] and [-] button - Set Video Stabilizer level by + / - button
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            media_room_page.import_media_file(app.testing_material + '/Fix_Enhance/shaky.MTS')
            main_page.insert_media('shaky.MTS')
            main_page.set_timeline_timecode('00_00_01_11', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick video stabilizer option
            fix_enhance_page.fix.enable_video_stabilizer()
            # Adjust [+] and [-] button
            fix_enhance_page.fix.video_stabilizer.correction_level.click_minus(times=5)
            fix_enhance_page.fix.video_stabilizer.correction_level.click_arrow(times=10)
            time.sleep(1)
            # Snapshot when apply default value of video stabilizer
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-3-4_Apply_VS_Multiple.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-3-4_Apply_VS_Multiple.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("b5672bb3-79f7-409c-8172-153541cbfbe0") as case:
            # 2.3.5 Video Stabilizer - Apply Video Stabilizer to correct shaky video - Slider - Set Video Stabilizer level by slider
            fix_enhance_page.fix.video_stabilizer.correction_level.adjust_slider(75)
            time.sleep(2)
            # Snapshot after adjustment
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-3-5_Slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-3-5_Slider.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("49f7ccdb-b0e2-457e-b94c-91247f738b1a") as case:
            # 2.3.6 Video Stabilizer - Apply Video Stabilizer to correct shaky video - Set to 1 by keyboard inputting - Set Video Stabilizer level to 1
            time.sleep(1)
            fix_enhance_page.fix.video_stabilizer.correction_level.set_value(1)
            time.sleep(2)
            # Snapshot after adjustment
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-3-6_Set_1.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-3-6_Set_1.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("acc091d4-e4e3-4b88-b59c-b9adae924d13") as case:
            # 2.3.7 Video Stabilizer - Apply Video Stabilizer to correct shaky video - Set to 100 by keyboard inputting - Set Video Stabilizer level to 100
            time.sleep(1)
            fix_enhance_page.fix.video_stabilizer.correction_level.set_value(100)
            time.sleep(2)
            # Snapshot after adjustment
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-3-7_Set_100.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-3-7_Set_100.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("701799a5-770e-4982-af20-f1df8969a024") as case:
            # 2.3.8 Video Stabilizer - Apply Video Stabilizer to correct shaky video - Up/Down arrow - Set Video Stabilizer level by Up/Down arrow
            time.sleep(1)
            fix_enhance_page.fix.video_stabilizer.correction_level.click_arrow(opt = "up", times=17)
            fix_enhance_page.fix.video_stabilizer.correction_level.click_arrow(opt = "down", times=15)
            time.sleep(2)
            # Snapshot after adjustment
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-3-8_Updown.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-3-8_Updown.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_3_12(self):
        with uuid("c565c5f1-7c26-444d-ac47-1525de925d95") as case:
            # 2.3.12 Video Stabilizer - Compare video qualities in split preview - The preview splits to two parts to show the original preview and applied preview
            # PDR 19.6.2922 may crash after ticking "Compare with split preview" option
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            media_room_page.import_media_file(app.testing_material + '/Fix_Enhance/shaky.MTS')
            main_page.insert_media('shaky.MTS')
            main_page.set_timeline_timecode('00_00_01_11', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick video stabilizer option
            fix_enhance_page.fix.enable_video_stabilizer()
            # Tick "Compare with split preview" option
            fix_enhance_page.set_check_compare_in_split_preview(value=True)
            time.sleep(1)
            # Snapshot when apply default value of video stabilizer
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-3-12_Split.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-3-12_Split.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("f081461f-e07c-415c-a4f8-7da111b0d65a") as case:
            # 2.3.14 Video Stabilizer - [Reset] - Parameter change will restore to default value directly if clicking
            # change value of video_stabilizer
            fix_enhance_page.fix.video_stabilizer.correction_level.set_value(100)
            # click reset button
            fix_enhance_page.click_reset()
            time.sleep(2)
            # Snapshot and compare with default value of video stabilizer
            current_image = keyframe_room_page.snapshot(locator=keyframe_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-3-14_Reset.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-3-12_Split.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("39f9c2d5-3fdb-4217-a652-86511e2188e0") as case:
            # 2.3.15 Video Stabilizer - [Keyframe] - Switch to Keyframe room
            # click keyframe button
            fix_enhance_page.click_keyframe()
            # verify if enter keyframe room
            keyframe_result = keyframe_room_page.is_enter_keyframe_settings()
            logger(f"{keyframe_result = }")
            case.result = keyframe_result

        with uuid("2255aa82-2e97-49b5-bf6a-dda1563ad725") as case:
            # 2.3.17 Video Stabilizer - Preview - Video is fixed after apply video stabilizer
            # click fix enhance button
            tips_area_page.click_fix_enhance()
            # Tick video stabilizer option
            fix_enhance_page.fix.enable_video_stabilizer()
            # Snapshot 1st video frame to check the fixed result
            main_page.set_timeline_timecode('00_00_10_29', is_verify=False)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-3-17_1st.png')
            compare_result_1 = media_room_page.compare(Ground_Truth_Folder + '2-3-17_1st.png', current_image)
            logger(f"{compare_result= }")
            # Snapshot 2nd video frame to check the fixed result
            main_page.set_timeline_timecode('00_00_12_04', is_verify=False)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-3-17_2nd.png')
            compare_result_2 = media_room_page.compare(Ground_Truth_Folder + '2-3-17_2nd.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # Snapshot 3rd video frame to check the fixed result
            main_page.set_timeline_timecode('00_00_13_08', is_verify=False)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-3-17_3rd.png')
            compare_result_3 = media_room_page.compare(Ground_Truth_Folder + '2-3-17_3rd.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result_1 and compare_result_2 and compare_result_3

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_3_16(self):
        with uuid("5f3ed231-a95e-42b5-a115-2adf5686a468") as case:
            # 2.3.16 Video Stabilizer - [Apply to All] - Apply fix to other video at the same track correctly
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            # Import 2 clips into timeline
            main_page.insert_media('Skateboard 01.mp4')
            media_room_page.hover_library_media('Skateboard 02.mp4')
            main_page.drag_media_to_timeline_clip('Skateboard 01.mp4', 0, 1, 1)
            # Select all clips in timeline
            timeline_operation_page.select_multiple_timeline_media(media1_track_index=0, media1_clip_index=0, media2_track_index=0, media2_clip_index=1)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick video stabilizer option
            fix_enhance_page.fix.enable_video_stabilizer()
            # Tick [Apply to All] button
            fix_enhance_page.click_apply_to_all()
            # Snapshot when apply default value of video stabilizer
            current_image = timeline_operation_page.snapshot(locator=L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + '2-3-16_Apply_All.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-3-16_Apply_All.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result

        with uuid("7fae6843-de59-4851-915a-4063c216c0a1") as case:
            # 2.3.18 Video Stabilizer - Undo/Redo - Parameter and preview displays correctly
            # Snapshot for video_stabilizer = "50"
            original_50_img = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-3-18_before_50_img.png')
            # input "80" for video_stabilizer
            fix_enhance_page.fix.video_stabilizer.correction_level.set_value(80)
            time.sleep(1)
            # Snapshot for video_stabilizer = 80
            after_80_img = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-3-18_after_80_img.png')
            # click undo button
            main_page.click_undo()
            # Verify if result is back to video_stabilizer = "50"
            compare_result_1 = media_room_page.compare(Ground_Truth_Folder + '2-3-18_before_50_img.png', original_50_img)
            logger(f"{compare_result_1= }")
            # click redo button
            main_page.click_redo()
            # Verify if result is back to video_stabilizer = "80"
            compare_result_2 = media_room_page.compare(Ground_Truth_Folder + '2-3-18_after_80_img.png', after_80_img)
            logger(f"{compare_result_2= }")
            case.result = compare_result_1 and compare_result_2
            main_page.save_project("Fix_Enhance_01", app.testing_material + '/Fix_Enhance/SaveProject')

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_3_21(self):
        with uuid("944c9288-c0ad-4aae-8b68-3c8c7a107411") as case:
            # 2.3.21 Video Stabilizer - Project - Save then open - Fix keeps and preview is correct after open project
            time.sleep(5)
            main_page.tap_OpenProject_hotkey()
            main_page.handle_open_project_dialog(app.testing_material + '/Fix_Enhance/SaveProject/Fix_Enhance_01.pds')
            main_page.handle_merge_media_to_current_library_dialog()
            time.sleep(2)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-3-21_Save.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-3-18_after_80_img.png', current_image)
            case.result = compare_result
            #main_page.top_menu_bar_file_pack_project_materials(app.testing_material + '/Fix_Enhance/PackProject/PackProject.pdk')
            #time.sleep(5)
    '''
    # @pytest.mark.skip
    @exception_screenshot
    def test_2_3_22(self):
        with uuid("508b622c-e1e3-4da1-9b8c-a3c700105f46") as case:
            # 2.3.22 Video Stabilizer - Project - Pack then open - Fix keeps and preview is correct after open project
            time.sleep(5)
            main_page.tap_OpenProject_hotkey()
            main_page.handle_open_project_dialog(app.testing_material + '/Fix_Enhance/PackProject/PackProject.pdk', app.testing_material + '/Fix_Enhance/PackProject/UnZip')
            main_page.handle_merge_media_to_current_library_dialog()
            time.sleep(4)
            media_room_page.high_definition_video_confirm_dialog_click_no()
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-3-22_Pack.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-3-18_after_80_img', current_image)
            case.result = compare_result
    '''

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_6_1(self):
        with uuid("8d35b9cd-7810-446a-9686-c6f318bba9bd") as case:
            # 2.6.1 Audio Denoise - Enable Audio Denoise checkbox - Apply the settings of Audio Denoise, default degree is 50 Stationary noise
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            # Import clip into timeline
            main_page.insert_media('Skateboard 01.mp4')
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick audio denoise option
            fix_enhance_page.fix.enable_audio_denoise()
            # Verify default value of degree is 50
            check_value = fix_enhance_page.fix.audio_denoise.degree.get_value()
            logger(f"{check_value= }")
            if not check_value == '50':
                result = False
            else:
                result = True
            case.result = result

        with uuid("0a84bca6-3158-40e5-8c3e-a6f983412ef3") as case:
            # 2.6.2 Audio Denoise - Noise type - Stationary noise - Denoise the Stationary noise
            # Check if switch to "Stationary noise" noise type
            # 1=Stationary noise, 2=Wind noise, 3=Clicking noise
            fix_enhance_page.fix.audio_denoise.set_noise_type(0)
            time.sleep(5)
            noise_type = fix_enhance_page.fix.audio_denoise.get_noise_type()
            logger(f"{noise_type= }")
            if not noise_type == 'Stationary noise':
                result = False
            else:
                result = True
            case.result = result

        with uuid("3aefc35e-95d1-4b49-a57b-f65ea1989526") as case:
            # 2.6.3 Audio Denoise - Noise type - Wind noise - Denoise the Wind noise
            # Check if switch to "Wind noise" noise type
            fix_enhance_page.fix.audio_denoise.set_noise_type(1)
            time.sleep(5)
            noise_type = fix_enhance_page.fix.audio_denoise.get_noise_type()
            logger(f"{noise_type= }")
            if not noise_type == 'Wind noise':
                result = False
            else:
                result = True
            case.result = result

        with uuid("cd3aacbf-4327-4fed-8550-48bbc11d4b66") as case:
            # 2.6.5 Audio Denoise - Degree - "+ / -" button - Set Audio Denoise degree by + / - button
            fix_enhance_page.fix.audio_denoise.degree.click_arrow(opt = "up", times=8)
            fix_enhance_page.fix.audio_denoise.degree.click_arrow(opt = "down", times=7)
            # Verify if degree value is 51
            degree_value = fix_enhance_page.fix.audio_denoise.degree.get_value()
            logger(f"{degree_value= }")
            if not degree_value == '51':
                result = False
            else:
                result = True
            case.result = result

        with uuid("276a3cf5-15de-44b0-b44c-25581f143daa") as case:
            # 2.6.6 Audio Denoise - Degree - Slider - Set Audio Denoise degree by slider - Set Audio Denoise degree by slider
            fix_enhance_page.fix.audio_denoise.degree.adjust_slider(55)
            # Verify if degree value is 55
            degree_value = fix_enhance_page.fix.audio_denoise.degree.get_value()
            logger(f"{degree_value= }")
            if not degree_value == '55':
                result = False
            else:
                result = True
            case.result = result

        with uuid("ab8b575c-2594-4ef1-abd3-d03d71b5c7ea") as case:
            # 2.6.7 Audio Denoise - Degree - Set to 1 by keyboard inputting - Set Audio Denoise degree to 1
            fix_enhance_page.fix.audio_denoise.degree.set_value(1)
            # Verify if degree value is 1
            degree_value = fix_enhance_page.fix.audio_denoise.degree.get_value()
            logger(f"{degree_value= }")
            if not degree_value == '1':
                result = False
            else:
                result = True
            case.result = result

        with uuid("a82994e1-4616-44a4-9725-4a07dccae457") as case:
            # 2.6.8 Audio Denoise - Degree - Set to 100 by keyboard inputting - Set Audio Denoise degree to 100
            fix_enhance_page.fix.audio_denoise.degree.set_value(100)
            # Verify if degree value is 100
            degree_value = fix_enhance_page.fix.audio_denoise.degree.get_value()
            logger(f"{degree_value= }")
            if not degree_value == '100':
                result = False
            else:
                result = True
            case.result = result

        with uuid("94b842e6-72ff-4444-a6b5-6f400693b4f1") as case:
            # 2.6.9 Audio Denoise - Degree - Up/Down arrow - Set Audio Denoise degree by Up/Down arrow
            fix_enhance_page.fix.audio_denoise.degree.set_value(60)
            fix_enhance_page.fix.audio_denoise.degree.click_minus(times=5)
            fix_enhance_page.fix.audio_denoise.degree.click_plus(times=6)
            # Verify if degree value is 61
            degree_value = fix_enhance_page.fix.audio_denoise.degree.get_value()
            logger(f"{degree_value= }")
            if not degree_value == '61':
                result = False
            else:
                result = True
            case.result = result

    """
        with uuid("0954ed2e-3982-4d1d-ae3f-136483a60a58") as case:
            # 2.6.4 Audio Denoise - Noise type - Clicking noise - Denoise the Clicking noise
            # Check if switch to "Clicking noise" noise type
            fix_enhance_page.fix.audio_denoise.set_noise_type(2)
            noise_type = fix_enhance_page.fix.audio_denoise.get_noise_type()
            logger(f"{noise_type= }")
            if not noise_type == 'Clicking noise':
                result = False
            else:
                result = True
            case.result = result
    """

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_9_1(self):
        with uuid("b1b62bbf-517c-4766-a724-52d8e37b6b63") as case:
            # 2.9.1 Color Adjustment - Enable Color Adjustment checkbox	- Apply the settings of Color Adjustment
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            # Import clip into timeline
            main_page.insert_media('Skateboard 03.mp4')
            # Seek to specific timecode
            main_page.set_timeline_timecode('00_00_05_11', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick color adjustment option
            case.result = fix_enhance_page.enhance.switch_to_color_adjustment()
            logger(f"{case.result= }")

        with uuid("fa795975-ecac-471b-b2b3-320f6f8dedda") as case:
            # 2.9.2 Color Adjustment - Exposure	- Default value=100 - No Exposure adjustment applied
            # Click Reset button
            fix_enhance_page.click_reset()
            # Snapshot original status for reference
            original_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-2_Original.png')
            # Change Exposure setting to 100
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(100)
            # Snapshot to verify if effect applied
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-2_Apply.png')
            compare_result = media_room_page.compare(original_image, current_image)
            case.result = compare_result

        with uuid("1baae1ae-abf8-4a5b-8845-b62565d5f903") as case:
            # 2.9.3 Color Adjustment - Exposure	- Slider - Set Exposure adjustment by slider
            # Change Exposure setting by slider
            fix_enhance_page.enhance.color_adjustment.exposure.adjust_slider(180)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-3_Slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-3_Slider.png', current_image)
            case.result = compare_result

        with uuid("c89be476-c7cf-4597-b3c9-0cfc5bb0d459") as case:
            # 2.9.4 Color Adjustment - Exposure	- Set to 0 by keyboard inputting - Set Exposure adjustment to 0
            # Change Exposure setting by keyboard
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(0)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-4_Exposure_0.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-4_Exposure_0.png', current_image)
            case.result = compare_result

        with uuid("b59408a2-2402-4d0a-a6cf-cbf591891e0d") as case:
            # 2.9.5 Color Adjustment - Exposure	- Set to 200 by keyboard inputting - Set Exposure adjustment to 200
            # Change Exposure setting by keyboard
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(200)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-5_Exposure_200.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-5_Exposure_200.png', current_image)
            case.result = compare_result

        with uuid("a7ea5798-b8e2-4b4c-951c-fffdbf686cbb") as case:
            # 2.9.6 Color Adjustment - Up/Down arrow - Set Exposure adjustment by Up/Down arrow
            # Change Exposure setting by up/down arrow
            fix_enhance_page.enhance.color_adjustment.exposure.click_arrow(opt = "down", times=20)
            fix_enhance_page.enhance.color_adjustment.exposure.click_arrow(opt = "up", times=1)
            # Check if Exposure setting is 181
            current_value = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            logger(f"{current_value= }")
            if not current_value == '181':
                result = False
            else:
                result = True
            # Snapshot to verify if effect applied
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-6_Exposure_181.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-6_Exposure_181.png', current_image)
            case.result = compare_result and result

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_9_7(self):
        with uuid("a71cd786-9e9d-4e16-8e6b-405b10186c24") as case:
            # 2.9.7 Color Adjustment - Brightness - Default value = 0 - No Brightness adjustment applied
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            # Import clip into timeline
            main_page.insert_media('Skateboard 03.mp4')
            # Seek to specific timecode
            main_page.set_timeline_timecode('00_00_04_11', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick color adjustment option
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Snapshot original status for reference
            original_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-7_Original.png')
            # Change Exposure setting to 100
            fix_enhance_page.enhance.color_adjustment.brightness.set_value(0)
            # Snapshot to verify if effect applied
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-7_Apply.png')
            compare_result = media_room_page.compare(original_image, current_image)
            case.result = compare_result

        with uuid("dc4decdd-2406-477a-bfb7-679518239964") as case:
            # 2.9.8 Color Adjustment - Brightness - Slider - Set Brightness adjustment by slider
            # Change Brightness setting by slider
            fix_enhance_page.enhance.color_adjustment.brightness.adjust_slider(50)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-8_Slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-8_Slider.png', current_image)
            case.result = compare_result

        with uuid("73d16962-5351-4abe-8550-7dd5e7367ecf") as case:
            # 2.9.9 Color Adjustment - Brightness - Set to -100 by keyboard inputting - Set Brightness adjustment to -100
            # Change Brightness setting by keyboard
            fix_enhance_page.enhance.color_adjustment.brightness.set_value(-100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-9_Brightness_-100.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-9_Brightness_-100.png', current_image)
            case.result = compare_result

        with uuid("2d4ba12f-a8f7-42e6-8e72-4d68cf1fc062") as case:
            # 2.9.10 Color Adjustment - Brightness - Set to 100 by keyboard inputting - Set Brightness adjustment to 100
            # Change Brightness setting by keyboard
            fix_enhance_page.enhance.color_adjustment.brightness.set_value(100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-10_Brightness_100.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-10_Brightness_100.png', current_image)
            case.result = compare_result

        with uuid("e9c95954-2be2-4be4-8041-182264d46ede") as case:
            # 2.9.11 Color Adjustment - Up/Down arrow - Set Brightness adjustment by Up/Down arrow
            # Change Brightness setting by up/down arrow
            fix_enhance_page.enhance.color_adjustment.brightness.click_arrow(opt = "down", times=20)
            fix_enhance_page.enhance.color_adjustment.brightness.click_arrow(opt = "up", times=1)
            # Check if Brightness setting is 81
            current_value = fix_enhance_page.enhance.color_adjustment.brightness.get_value()
            logger(f"{current_value= }")
            if not current_value == '81':
                result = False
            else:
                result = True
            # Snapshot to verify if effect applied
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-11_Brightness_81.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-11_Brightness_81.png', current_image)
            case.result = compare_result and result

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_9_12(self):
        with uuid("f3d9fb94-9664-4f9a-92b0-8836df16b33a") as case:
            # 2.9.12 Color Adjustment - Contrast - Default value = 0 - No Contrast adjustment applied
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            # Import clip into timeline
            main_page.insert_media('Skateboard 03.mp4')
            # Seek to specific timecode
            main_page.set_timeline_timecode('00_00_03_11', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick color adjustment option
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Snapshot original status for reference
            original_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-12_Original.png')
            # Change Contrast setting to 100
            fix_enhance_page.enhance.color_adjustment.contrast.set_value(0)
            # Snapshot to verify if effect applied
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-12_Apply.png')
            compare_result = media_room_page.compare(original_image, current_image)
            case.result = compare_result

        with uuid("48848dfc-a995-4b73-91d2-9903dd46dffc") as case:
            # 2.9.13 Color Adjustment - Contrast - Slider - Set Contrast adjustment by slider
            # Change Contrast setting by slider
            fix_enhance_page.enhance.color_adjustment.contrast.adjust_slider(50)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-13_Slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-13_Slider.png', current_image)
            case.result = compare_result

        with uuid("466c0ac2-c544-4359-9db3-4f10b07b221b") as case:
            # 2.9.14 Color Adjustment - Contrast - Set to -100 by keyboard inputting - Set Contrast adjustment to -100
            # Change Contrast setting by keyboard
            fix_enhance_page.enhance.color_adjustment.contrast.set_value(-100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-14_Contrast_0.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-14_Contrast_0.png', current_image)
            case.result = compare_result

        with uuid("a1756f74-feac-4d3c-85fa-27bc73c63703") as case:
            # 2.9.15 Color Adjustment - Contrast - Set to 100 by keyboard inputting - Set Contrast adjustment to 100
            # Change Contrast setting by keyboard
            fix_enhance_page.enhance.color_adjustment.contrast.set_value(100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-15_Contrast_100.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-15_Contrast_100.png', current_image)
            case.result = compare_result

        with uuid("7252bf7f-e5dd-4ba5-8577-7d4f8d7c7522") as case:
            # 2.9.16 Color Adjustment - Up/Down arrow - Set Contrast adjustment by Up/Down arrow
            # Change Contrast setting by up/down arrow
            fix_enhance_page.enhance.color_adjustment.contrast.click_arrow(opt = "down", times=20)
            fix_enhance_page.enhance.color_adjustment.contrast.click_arrow(opt = "up", times=5)
            # Check if Contrast setting is 85
            current_value = fix_enhance_page.enhance.color_adjustment.contrast.get_value()
            logger(f"{current_value= }")
            if not current_value == '85':
                result = False
            else:
                result = True
            # Snapshot to verify if effect applied
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-16_Contrast_85.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-16_Contrast_85.png', current_image)
            case.result = compare_result and result


    # @pytest.mark.skip
    @exception_screenshot
    def test_2_9_17(self):
        with uuid("65e1c579-dbe7-4881-ba46-d653f8468b0f") as case:
            # 2.9.17 Color Adjustment - Hue - Default value = 100 - No Hue adjustment applied
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            # Import clip into timeline
            main_page.insert_media('Skateboard 03.mp4')
            # Seek to specific timecode
            main_page.set_timeline_timecode('00_00_02_11', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick color adjustment option
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Snapshot original status for reference
            original_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-17_Original.png')
            # Change Hue setting to 100
            fix_enhance_page.enhance.color_adjustment.hue.set_value(100)
            # Snapshot to verify if effect applied
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-17_Apply.png')
            compare_result = media_room_page.compare(original_image, current_image)
            case.result = compare_result

        with uuid("da7f09b8-d4b0-45fa-b58b-0ff8579b77df") as case:
            # 2.9.18 Color Adjustment - Hue - Slider - Set Hue adjustment by slider
            # Change Hue setting by slider
            fix_enhance_page.enhance.color_adjustment.hue.adjust_slider(50)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-18_Slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-18_Slider.png', current_image)
            case.result = compare_result

        with uuid("c311ecda-52ba-41ab-af6c-aab70e9913f3") as case:
            # 2.9.19 Color Adjustment - Hue - Set to 0 by keyboard inputting - Set Hue adjustment to 0
            # Change Hue setting by keyboard
            fix_enhance_page.enhance.color_adjustment.hue.set_value(0)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-19_Hue_0.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-19_Hue_0.png', current_image)
            case.result = compare_result

        with uuid("e2639308-afab-44c3-a7e7-8182da8df649") as case:
            # 2.9.20 Color Adjustment - Hue - Set to 200 by keyboard inputting - Set Hue adjustment to 200
            # Change Hue setting by keyboard
            fix_enhance_page.enhance.color_adjustment.hue.set_value(200)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-20_Hue_200.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-20_Hue_200.png', current_image)
            case.result = compare_result

        with uuid("0aeb9896-01b9-4707-ba17-c1c914f431e9") as case:
            # 2.9.21 Color Adjustment - Up/Down arrow - Set Hue adjustment by Up/Down arrow
            # Change Hue setting by up/down arrow
            fix_enhance_page.enhance.color_adjustment.hue.click_arrow(opt = "down", times=20)
            fix_enhance_page.enhance.color_adjustment.hue.click_arrow(opt = "up", times=5)
            # Check if Hue setting is 85
            current_value = fix_enhance_page.enhance.color_adjustment.hue.get_value()
            logger(f"{current_value= }")
            if not current_value == '185':
                result = False
            else:
                result = True
            # Snapshot to verify if effect applied
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-21_Hue_185.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-21_Hue_185.png', current_image)
            case.result = compare_result and result


    # @pytest.mark.skip
    @exception_screenshot
    def test_2_9_22(self):
        with uuid("8eabbcac-0884-42c8-960e-52efc037acf7") as case:
            # 2.9.22 Color Adjustment - saturation - Default value = 100 - No saturation adjustment applied
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            # Import clip into timeline
            main_page.insert_media('Skateboard 03.mp4')
            # Seek to specific timecode
            main_page.set_timeline_timecode('00_00_01_11', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick color adjustment option
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Snapshot original status for reference
            original_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-22_Original.png')
            # Change saturation setting to 100
            fix_enhance_page.enhance.color_adjustment.saturation.set_value(100)
            # Snapshot to verify if effect applied
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-22_Apply.png')
            compare_result = media_room_page.compare(original_image, current_image)
            case.result = compare_result

        with uuid("b32cbb77-4688-4c7d-8b2c-f60ba787a6b1") as case:
            # 2.9.23 Color Adjustment - saturation - Slider - Set saturation adjustment by slider
            # Change saturation setting by slider
            fix_enhance_page.enhance.color_adjustment.saturation.adjust_slider(50)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-23_Slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-23_Slider.png', current_image)
            case.result = compare_result

        with uuid("8b4a575a-6f8c-41eb-be44-d7dc479787ca") as case:
            # 2.9.24 Color Adjustment - saturation - Set to 0 by keyboard inputting - Set saturation adjustment to 0
            # Change saturation setting by keyboard
            fix_enhance_page.enhance.color_adjustment.saturation.set_value(0)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-24_saturation_0.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-24_saturation_0.png', current_image)
            case.result = compare_result

        with uuid("160abd60-882f-4ea7-bf32-042c61c7f3b1") as case:
            # 2.9.25 Color Adjustment - saturation - Set to 200 by keyboard inputting - Set saturation adjustment to 200
            # Change saturation setting by keyboard
            fix_enhance_page.enhance.color_adjustment.saturation.set_value(200)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-25_saturation_200.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-25_saturation_200.png', current_image)
            case.result = compare_result

        with uuid("181edb9f-a89b-411b-94ff-b12c41a63ccf") as case:
            # 2.9.26 Color Adjustment - Up/Down arrow - Set saturation adjustment by Up/Down arrow
            # Change saturation setting by up/down arrow
            fix_enhance_page.enhance.color_adjustment.saturation.click_arrow(opt = "down", times=20)
            fix_enhance_page.enhance.color_adjustment.saturation.click_arrow(opt = "up", times=5)
            # Check if saturation setting is 85
            current_value = fix_enhance_page.enhance.color_adjustment.saturation.get_value()
            logger(f"{current_value= }")
            if not current_value == '185':
                result = False
            else:
                result = True
            # Snapshot to verify if effect applied
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-26_saturation_185.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-26_saturation_185.png', current_image)
            case.result = compare_result and result

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_9_27(self):
        with uuid("5fefb746-28e5-4c16-9b4c-dfca4f26d95d") as case:
            # 2.9.27 Color Adjustment - vibrancy - Default value = 0 - No vibrancy adjustment applied
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            # Import clip into timeline
            main_page.insert_media('Skateboard 03.mp4')
            # Seek to specific timecode
            main_page.set_timeline_timecode('00_00_01_11', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick color adjustment option
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Snapshot original status for reference
            original_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-27_Original.png')
            # Change vibrancy setting to 100
            fix_enhance_page.enhance.color_adjustment.vibrancy.set_value(0)
            # Snapshot to verify if effect applied
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-27_Apply.png')
            compare_result = media_room_page.compare(original_image, current_image)
            case.result = compare_result

        with uuid("cb854a5b-8127-48e4-b185-e102c282e8b5") as case:
            # 2.9.28 Color Adjustment - vibrancy - Slider - Set vibrancy adjustment by slider
            # Change vibrancy setting by slider
            fix_enhance_page.enhance.color_adjustment.vibrancy.adjust_slider(50)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-28_Slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-28_Slider.png', current_image)
            case.result = compare_result

        with uuid("4d0b9aa8-1fd0-43f4-8ee0-e88b11ebbdca") as case:
            # 2.9.29 Color Adjustment - vibrancy - Set to -100 by keyboard inputting - Set vibrancy adjustment to -100
            # Change vibrancy setting by keyboard
            fix_enhance_page.enhance.color_adjustment.vibrancy.set_value(-100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-29_vibrancy_-100.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-29_vibrancy_-100.png', current_image)
            case.result = compare_result

        with uuid("dca116d8-a408-4268-a193-dc2aa5bdf29c") as case:
            # 2.9.30 Color Adjustment - vibrancy - Set to 100 by keyboard inputting - Set vibrancy adjustment to 100
            # Change vibrancy setting by keyboard
            fix_enhance_page.enhance.color_adjustment.vibrancy.set_value(100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-30_vibrancy_100.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-30_vibrancy_100.png', current_image)
            case.result = compare_result

        with uuid("a17f70d0-da1c-43fa-a987-5082dda378de") as case:
            # 2.9.31 Color Adjustment - Up/Down arrow - Set vibrancy adjustment by Up/Down arrow
            # Change vibrancy setting by up/down arrow
            fix_enhance_page.enhance.color_adjustment.vibrancy.click_arrow(opt = "down", times=20)
            fix_enhance_page.enhance.color_adjustment.vibrancy.click_arrow(opt = "up", times=5)
            # Check if vibrancy setting is 85
            current_value = fix_enhance_page.enhance.color_adjustment.vibrancy.get_value()
            logger(f"{current_value= }")
            if not current_value == '85':
                result = False
            else:
                result = True
            # Snapshot to verify if effect applied
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-31_vibrancy_85.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-31_vibrancy_85.png', current_image)
            case.result = compare_result and result

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_9_32(self):
        with uuid("aa5afcfd-47ba-42fa-9289-ca245342d2f4") as case:
            # 2.9.32 Color Adjustment - highlight healing - Default value = 0 - No highlight healing adjustment applied
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            # Import clip into timeline
            main_page.insert_media('Skateboard 03.mp4')
            # Seek to specific timecode
            main_page.set_timeline_timecode('00_00_01_11', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick color adjustment option
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Snapshot original status for reference
            original_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-32_Original.png')
            # Change highlight healing setting to 100
            fix_enhance_page.enhance.color_adjustment.highlight_healing.set_value(0)
            # Snapshot to verify if effect applied
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-32_Apply.png')
            compare_result = media_room_page.compare(original_image, current_image)
            case.result = compare_result

        with uuid("2f91fc8e-7945-47f4-b0b1-90b2ca3fa214") as case:
            # 2.9.33 Color Adjustment - highlight healing - Slider - Set highlight healing adjustment by slider
            # Change highlight healing setting by slider
            fix_enhance_page.enhance.color_adjustment.highlight_healing.adjust_slider(50)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-33_Slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-33_Slider.png', current_image)
            case.result = compare_result

        with uuid("8ec5acea-e596-47e2-bd41-446f3c386ede") as case:
            # 2.9.34 Color Adjustment - highlight healing - Set to 100 by keyboard inputting - Set highlight healing adjustment to 100
            # Change highlight healing setting by keyboard
            fix_enhance_page.enhance.color_adjustment.highlight_healing.set_value(100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-34_highlight_healing_100.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-34_highlight_healing_100.png', current_image)
            case.result = compare_result

        with uuid("5ce20dac-554c-4f0a-a248-739409bf6882") as case:
            # 2.9.35 Color Adjustment - Up/Down arrow - Set highlight healing adjustment by Up/Down arrow
            # Change highlight healing setting by up/down arrow
            fix_enhance_page.enhance.color_adjustment.highlight_healing.click_arrow(opt = "down", times=20)
            fix_enhance_page.enhance.color_adjustment.highlight_healing.click_arrow(opt = "up", times=5)
            # Check if highlight healing setting is 85
            current_value = fix_enhance_page.enhance.color_adjustment.highlight_healing.get_value()
            logger(f"{current_value= }")
            if not current_value == '85':
                result = False
            else:
                result = True
            # Snapshot to verify if effect applied
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-35_highlight_healing_85.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-35_highlight_healing_85.png', current_image)
            case.result = compare_result and result

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_9_36(self):
        with uuid("2be2ab5a-7ffe-4fca-97d8-8d97ba8048a3") as case:
            # 2.9.36 Color Adjustment - shadow - Default value = 0 - No shadow adjustment applied
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            # Import clip into timeline
            main_page.insert_media('Skateboard 03.mp4')
            # Seek to specific timecode
            main_page.set_timeline_timecode('00_00_09_11', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick color adjustment option
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Snapshot original status for reference
            original_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-36_Original.png')
            # Change shadow setting to 100
            fix_enhance_page.enhance.color_adjustment.shadow.set_value(0)
            # Snapshot to verify if effect applied
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-36_Apply.png')
            compare_result = media_room_page.compare(original_image, current_image)
            case.result = compare_result

        with uuid("bce7ebdb-6414-4141-84a8-327973794604") as case:
            # 2.9.37 Color Adjustment - shadow - Slider - Set shadow adjustment by slider
            # Change shadow setting by slider
            fix_enhance_page.enhance.color_adjustment.shadow.adjust_slider(50)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-37_Slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-37_Slider.png', current_image)
            case.result = compare_result

        with uuid("63513a51-83f9-4d0f-8edc-92401ef2086f") as case:
            # 2.9.38 Color Adjustment - shadow - Set to 100 by keyboard inputting - Set shadow adjustment to 100
            # Change shadow setting by keyboard
            fix_enhance_page.enhance.color_adjustment.shadow.set_value(100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-38_shadow_100.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-38_shadow_100.png', current_image)
            case.result = compare_result

        with uuid("0e570885-2d2f-4c26-a046-9d452e3b1371") as case:
            # 2.9.39 Color Adjustment - Up/Down arrow - Set shadow adjustment by Up/Down arrow
            # Change shadow setting by up/down arrow
            fix_enhance_page.enhance.color_adjustment.shadow.click_arrow(opt="down", times=20)
            fix_enhance_page.enhance.color_adjustment.shadow.click_arrow(opt="up", times=5)
            # Check if shadow setting is 85
            current_value = fix_enhance_page.enhance.color_adjustment.shadow.get_value()
            logger(f"{current_value= }")
            if not current_value == '85':
                result = False
            else:
                result = True
            # Snapshot to verify if effect applied
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-39_shadow_85.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-39_shadow_85.png', current_image)
            case.result = compare_result and result
            
    @exception_screenshot
    def test_2_9_40(self):
        with uuid("bcb0d253-7256-46e8-8c8c-ac645e232b7d") as case:
            # 2.9.40 Color Adjustment - sharpness - Default value = 0 - No sharpness adjustment applied
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            # Import clip into timeline
            main_page.insert_media('Skateboard 03.mp4')
            # Seek to specific timecode
            main_page.set_timeline_timecode('00_00_05_20', is_verify=False)
            tips_area_page.click_fix_enhance()
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            # Verify if in "Fix Enhance" page
            logger(f"{is_in_fix_enhance= }")
            # Tick color adjustment option
            fix_enhance_page.enhance.switch_to_color_adjustment()
            # Snapshot original status for reference
            original_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-40_Original.png')
            # Change sharpness setting to 100
            fix_enhance_page.enhance.color_adjustment.sharpness.set_value(0)
            # Snapshot to verify if effect applied
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-40_Apply.png')
            compare_result = media_room_page.compare(original_image, current_image)
            case.result = compare_result

        with uuid("1ae1b4ca-4366-401c-8a43-1b3e596dbf86") as case:
            # 2.9.41 Color Adjustment - sharpness - Slider - Set sharpness adjustment by slider
            # Change sharpness setting by slider
            fix_enhance_page.enhance.color_adjustment.sharpness.adjust_slider(50)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-41_Slider.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-41_Slider.png', current_image)
            case.result = compare_result

        with uuid("3aca129d-1371-4315-b81c-a2a1129775d5") as case:
            # 2.9.42 Color Adjustment - sharpness - Set to 100 by keyboard inputting - Set sharpness adjustment to 100
            # Change sharpness setting by keyboard
            fix_enhance_page.enhance.color_adjustment.sharpness.set_value(100)
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-42_sharpness_100.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-42_sharpness_100.png', current_image)
            case.result = compare_result

        with uuid("208bb004-d1e7-4ad9-9caa-44d73c365a2c") as case:
            # 2.9.43 Color Adjustment - Up/Down arrow - Set sharpness adjustment by Up/Down arrow
            # Change sharpness setting by up/down arrow
            fix_enhance_page.enhance.color_adjustment.sharpness.click_arrow(opt="down", times=20)
            fix_enhance_page.enhance.color_adjustment.sharpness.click_arrow(opt="up", times=5)
            # Check if sharpness setting is 85
            current_value = fix_enhance_page.enhance.color_adjustment.sharpness.get_value()
            logger(f"{current_value= }")
            if not current_value == '85':
                result = False
            else:
                result = True
            # Snapshot to verify if effect applied
            time.sleep(1)
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-43_sharpness_85.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-43_sharpness_85.png', current_image)
            case.result = compare_result and result

        with uuid("84180073-231e-4ea9-9e9d-ab8e0dc1f8ad") as case:
            # 2.9.45 Color Adjustment - Compare video qualities in split preview - The preview splits to two parts to show the original preview and applied preview
            # Tick "Compare with split preview" option
            fix_enhance_page.set_check_compare_in_split_preview(value=True)
            time.sleep(1)
            # Snapshot when apply default value of video stabilizer
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-45_Split.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-45_Split.png', current_image)
            logger(f"{compare_result= }")
            case.result = compare_result
            # UnTick "Compare with split preview" option
            fix_enhance_page.set_check_compare_in_split_preview(value=False)
            time.sleep(1)

        with uuid("da9ce14b-93f6-472f-a8c0-49453964a7e5") as case:
            # 2.9.44 Color Adjustment - Reset - Reset to default
            # Adjust other slider's setting then click reset button
            fix_enhance_page.enhance.color_adjustment.shadow.set_value(55)
            fix_enhance_page.enhance.color_adjustment.highlight_healing.set_value(30)
            fix_enhance_page.enhance.color_adjustment.vibrancy.set_value(10)
            fix_enhance_page.enhance.color_adjustment.saturation.set_value(30)
            fix_enhance_page.enhance.color_adjustment.hue.set_value(30)
            fix_enhance_page.enhance.color_adjustment.contrast.set_value(-30)
            fix_enhance_page.enhance.color_adjustment.brightness.set_value(10)
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(110)
            # Click reset button
            fix_enhance_page.click_reset()
            time.sleep(1)
            # Snapshot with original photo
            current_image = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '2-9-44_Reset.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '2-9-40_Original.png', current_image)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    8b3f7c8f-5ff0-43fe-b57c-972fd28d83f9
                    d21b283b-beb8-4afa-9dd0-2540eb05dd75
                    01be9e16-5145-4e2b-9f7b-d2b0fb221eaf
                    cda8717d-73fd-4fea-83f9-1893c3e12073
                    29402e83-3586-4a3d-871f-cbe415c57e0e
                    041a3ce4-c01e-4e40-b6e7-a14ba0a3dee8
                    4f29c6e6-c788-4bfd-8eb6-184b351bb077
                    d3ac4305-66bd-4ce9-85cf-d231c455fa2d
                    0954ed2e-3982-4d1d-ae3f-136483a60a58
                    852c4cf3-82f8-4dfd-810e-34931d428156
                    558293e8-efc4-4e9e-9cde-c23838bc09fd
                    d50a1175-b1bb-463e-8bff-64c642500ae7
                    92d786ef-a7d2-41c2-b6a9-0e2d23ec5865
                    8b106dcc-d8ab-4917-aa1c-7f877c19ef03
                    17e876f4-fcd1-4d5a-9a5c-12f79647dc37
                    1d034e25-e577-426f-9d54-27d6bb4b3a9a
                    fd3199c9-a869-4e4c-88c2-286be9ec2065
                    c541b6b6-e64a-4549-b8bf-697a06436e26
                    2839dad1-6467-46ad-a036-e5640fa3b174
                    4945645a-0020-4861-960f-51c87b7d1d1a
                    bb9e7252-8001-4c68-b4ad-4300cc89a9f2
                    42ac4a73-7f0e-45b7-a799-c011f5b7dee7
                    9e097dc6-79d2-4b60-9e58-6f87d0755d0f
                    63f3499b-3f98-40cd-9ebe-232497de42df
                    7e8e9b8c-5720-4ead-9e82-12b99ce10e7e
                    9389ee7e-aba5-4400-89b0-a91e086ac6ac
                    cf6919b6-eb90-4720-86ba-2f26d9e42c18
                    7c232f60-7aa7-45d3-b46f-5c7df607b641
                    2d17b5a3-00c7-4389-9730-65ebe4f8ebd5
                    5ddec5b2-603c-4d73-988f-c46d9266b587
                    2d6e991b-fa3e-4c12-b7d8-7cec7de6c0e3
                    7a083fdf-3e29-427d-bddf-5a43ecfc0685
                    9298db82-a705-421e-9150-968838a879aa
                    d2b8be81-7255-4d10-8480-963b40b452ec
                    0481c7d7-3ad1-4be3-8c20-c11e1bad2fd6
                    f9246f17-6645-4897-818c-ef820fefbc18
                    c4f5a647-b9d3-41a2-8425-1c88365d0f4a
                    3b8df7ce-3ba2-4338-a785-d2a02f6192c9
                    50a1eedf-f924-4284-90cb-ae4749677b4f
                    bdb9efaa-ae78-4cd5-a489-643e86545fb5
                    504ea93d-47b3-483f-b5f4-db9a4b72cd40
                    9bad7be2-268e-493a-82da-cbfb8878c628
                    9bf27615-7015-40d3-9255-8c5b24cf975a
                    ae4d33db-8cad-4809-b481-1ba694480476
                    bdd606e6-db3b-4d61-8fff-d55a8828a107
                    84a00013-bf2a-4633-b774-2584c86c748e
                    86cbab8a-c946-4ed8-a5ff-d9c730959ee4
                    988c2e99-9a04-4846-91e8-4ba6c6f37d78
                    29196787-1a3d-4f33-8c62-e875fcfa5e26
                    cbb30b12-d778-4402-bec1-09210ddecd33
                    7e1798e9-6718-4378-ae73-d8f6b1f3f9c5
                    07d1104a-2fa9-4a36-b46b-88bd4c3fec4e
                    0f572a24-c3cf-40e1-a209-f70fbcfe4151
                    4a781a86-738a-4f8d-bed2-f2f706ce4683
                    fa5085b8-a1ec-4d12-88dd-2b7d8f123a27
                    eb9e45cd-6948-472e-bbbc-e04b0f69eb62
                    ae628996-4132-449d-b708-2a300b70292c
                    44de4a85-822e-4205-beaa-f5d0b505b58a
                    049a61e0-c94d-4b16-bfa5-d1faa8587d3f
                    a4afaa0a-9d5c-4130-8377-384e0b53107e
                    1627437a-f61a-4484-aeca-124eabcaaf06
                    d3254ce5-44fd-4388-b824-fefb02d24007
                    76da2dab-390f-493d-9227-454df1b69172
                    eb768121-116d-45cb-86db-d5290c8f0d9e
                    c481d00d-2794-4318-add8-7edc1cd310b2
                    306f9d09-9dfa-4fe2-b1a9-5efacbdfb091
                    b791285a-63cb-4ce5-8def-9508eac81028
                    a4ccf8d5-6f24-493a-88d6-e7f66e0e2c49
                    b32080fa-4b84-4caa-a47a-9d4e35c13bdb
                    837f63f2-014c-43f7-bda9-9c0c6bbf08d0
                    d9be4e35-2279-4907-9835-0515e9ce9b6b
                    4d6de7d9-1d53-4d24-90df-5b51f1469c5e
                    f0667c90-cfe5-4c07-9d80-8982dc666174
                    24987db7-8a71-446c-971b-f2f3df2bcb47
                    8c79c2da-e618-4b61-8b9f-83cc07e6a4dc
                    6344dc44-46fe-4d24-9b99-15772cd34c6a
                    65e9bde5-8d6e-4680-8647-dc51ce162d4d
                    4e8ba33f-e795-4c8e-838b-3379d5dd14ab
                    f233643c-ad2c-4f75-8347-3c446de8bf09
                    30ce0778-75f4-418c-b2a9-74d8aed233d0
                    9f6df2a4-b584-4377-9ab0-55beaafb55e0
                    2f5690d4-3bf3-4be9-b6cb-9e03c787572b
                    f434d517-dc98-4729-b683-29bc9739c338
                    ae0ea08d-79ea-4152-b94e-b65bc663544d
                    b301f7c4-30e2-4a86-8e8f-6fc4e02b3b32
                    0278acd4-e159-4660-bcd2-bf8ac3926ddc
                    83f45596-5ac1-493c-9e3a-171cb4170836
                    7c81c727-b4de-462b-bde1-c9ceef83bba3
                    571c59d4-3b12-4430-8d98-e3677d05ceb8
                    e729c814-cd54-4800-80ab-ee1448824805
                    695c7caf-803a-4de4-a935-5ee92879f776
                    2ae92ba1-db3c-4ad9-9589-ada0fcbf442a
                    7eaf6d54-20d7-4712-8966-e174347ff8e8
                    65cacedb-7690-4a7c-870d-2a14312bb3e5
                    e102e281-b0d2-42cd-8bd2-274bf28f7a51
                    e428d1ba-cb78-4e1d-9d7f-2f19eda8b6ad
                    b6f18b00-6d5f-41d9-84fa-e7f0e35993e8
                    7395cc1c-a937-4008-a1f1-170ff16577d6
                    3f40267a-bdee-4bb7-89f1-174752549b55
                    324775f7-ad8e-4b89-9d76-479a89bd1e2a
                    33f6275f-418d-4a9f-80a6-08758a568adf
                    6c2a9f61-3570-4e5d-aa12-3215a31feb25
                    8b1d0b43-7d6c-496c-ab2f-7f08f03420fe
                    1250cc96-90af-41e9-9da5-56bbc6d19390
                    9bc1cae0-5202-45b2-b0ad-159abcc6a256
                    0928d2d5-df5c-417a-b0fc-e37d0e944a4d
                    7c44a947-376f-41ef-ab04-13a46716c460
                    cc7789de-4de6-426c-9642-6d3e237adf92
                    afb12a70-3578-4ee1-8684-786a9e24def7
                    a0957a68-f92d-484e-bff8-e606b145a619
                    170aac3b-f344-433b-8e75-1c94683ea24f
                    ea46dcef-4bc2-405c-a08f-d76d9e74497c
                    8b535434-ba92-485e-9217-60036286b0a4
                    18312324-f637-4afa-929c-809202f4c06a
                    7ed2a39b-4b6e-46bf-a9d3-502341000c5e
                    579e6b46-aa14-47a6-a0dd-2624e5268c8d
                    26265f51-15d3-4321-9035-602849f72f5b
                    177e56a2-d0a2-478e-beb6-7b5ead6f8337
                    da6aa583-019e-4ea4-82fa-da21e12f1eaf
                    158be931-de00-4ad1-822b-e5cd23648a6d
                    c5a2c850-052a-4e6d-a773-12d114951a16
                    b9333829-6df8-4e85-9ab9-ea78e94d14ad
                    18c59f7f-9f8a-44ae-9794-0251757bc774
                    5f2dfc95-45a6-4912-9d47-98ce8f297cc9
                    9cc36549-9038-4cc1-abf5-e0b09edd3a6e
                    073a61e0-bc63-4ea9-b1f9-cd2cda22f2a9
                    719ef287-abec-4183-bc1d-9e40f1d16c32
                    c79d6e91-4e81-43f9-9641-17ee9ab5dffa
                    de7b9100-428f-4d67-9e02-a92777d30e4d
                    989ad9d5-5a89-496a-a775-b194c6a6cf4a
                    271f92b1-64e3-43cd-89a7-4c9b9bf9365a
                    5f64235c-3a4e-405d-933c-1d08fef909ea
                    b38cd043-a70e-438d-9a8e-131b830cffcc
                    9296c08b-9451-49d5-be50-4eb622d16923
                    f4dfd6ac-5bea-41b1-b03c-d9ec26215b44
                    3bac20ba-8664-4aa2-afa9-33874574c123
                    21721dcc-f9f6-4be8-9002-1b97abb18dc5
                    7d4e7fce-cc1f-436a-b182-6e147961629c
                    2592588c-95ca-40b2-b981-3d6561703c64
                    8cb01be7-d7a3-4bfb-8836-eb5de2cd2b90
                    08eb66f9-a4a5-41be-b73f-46e5fac3e390
                    6eb31f84-0851-4dd9-8b29-b35b914c2f04
                    d1df687e-7149-461f-994e-0c500712df36
                    0e489d06-e42c-40e8-8266-a95e6c3985ea
                    30f1375f-8a80-4d11-89b4-daf5d24d7f43
                    f8578caa-178b-48fb-af21-dcf37f38bac8
                    efc4df1f-f92b-4fc7-8c67-5c0a1e85eb34
                    c211be92-df16-49a6-84bc-1eaa71c40865
                    70a8e110-bc32-4856-a3a3-2c8026c97fd8
                    3232dad3-08b9-4acd-a435-bafec675e9f8
                    bed5d160-3409-4bcf-a688-9760b704d4ce
                    0618b4d8-215d-4073-a78d-1e443b0a9041
                    f5a46e2f-5a7f-4479-9eb7-23ba57f11ade
                    56e7b6bf-d7f9-41f3-8b5d-e042b6f65ec1
                    5919c5de-0e3f-43ee-b22c-de7ce5ed2e9c
                    2bb6a6bb-dcf0-4913-a684-109d96326430
                    f6ae497e-4ffc-431e-ae5d-c19dab0c6d9e
                    87a7bb5e-bb3d-49b2-81ab-84b89ddf3385
                    01be9e16-5145-4e2b-9f7b-d2b0fb221eaf
                    cda8717d-73fd-4fea-83f9-1893c3e12073
                    29402e83-3586-4a3d-871f-cbe415c57e0e
                    041a3ce4-c01e-4e40-b6e7-a14ba0a3dee8
                    fc0dcbad-021c-4663-a5df-36bf3b484780
                    b5e6ba18-077f-426f-8adb-42df0e05cbf4
                    8a9ecfc2-c65c-49f8-9451-fe3ed0e0e3fc
                    183b8c20-d0cf-4fb2-a354-1f2af185ee97
                    598804f2-819f-42a8-a915-25787e231173
                    4780008e-f2a4-42b9-a983-7c53725b8ab3
                    a9809b53-d66b-4071-b9fb-d5b3b0c3ca6b
                    cc0890fd-e6a2-4707-8b38-87d73cea2ec0
                    0cc30cdb-dbd6-40f1-ba8f-6cdae7eaad0c
                    6f687b35-abe9-4bb9-a0dc-08fc17f60fcb
                    63ae1a4d-86a4-4ee7-933c-366c9028c46b
                    482750da-dc4d-4d9b-a8b4-122c47a7f28e
                    6acf9275-5474-4e43-9b21-3869d6422f30
                    a4bf4941-037e-4b13-ab59-b217f976b83e
                    40b75eb0-f7ee-4357-9c4a-1d1f82e884d0
                    fd1086dd-7cc4-4ed4-a278-f4ab79ac4018
                    52362ae4-c7cc-4140-98c3-b5889631c2ee
                    5e10bcec-bebf-4061-8706-eb2ed708b0e3
                    8f32c5fd-e6f3-4b6f-a0ae-e31cb0be5b42
                    7751eb5a-7e78-43ae-9c44-044ca2d2f9b4
                    6c88b035-5cb2-4152-9202-8d11602cafb8
                    dceb5723-b272-4c0a-a99e-bbbc6ac95583
                    64eed0c3-dff1-40b5-a8ab-2660460c0b8c
                    f03091f1-d69f-4d3e-8a9a-02889b250859
                    3fb9edab-c3c2-4bfc-bffb-581b1f8a49b0
                    0199b268-2835-43a1-badf-127e9f1a20d2
                    37fe6e88-2202-4113-8bfa-cd90ed0cfdb4
                    a8fe2928-89b0-4028-9e80-e7d8d31b7202
                    12f02eb7-0a32-4c46-b83a-49e85920e0ae
                    fe8b2591-7805-4e53-a86a-6d26f517a5af
                    bd663114-a745-4d54-bd11-d27a779fd931
                    f33e03b0-b5d7-4c37-8c11-3bb4416b3f93
                    5b0b10d7-f5dd-4951-ba3e-abf9d827d184
                    d3a325ee-6c4a-4996-a71a-2e815cfbfc04
                    d7ec4fb0-b6e7-457e-898f-35c516fe8b14
                    728f6833-626c-4e8f-b7ab-25a01ea54311
                    959d347c-44b7-481e-8cd3-acc4f96a2f07
                    1314b1b5-8ba0-4166-a8a7-4f4e86d58dc7
                    825ac1c8-f3c8-4cb0-a988-bbda3ff93144
                    a26c36c0-26dd-4d23-b0cb-6027565d17cd
                    54e6fb8a-431b-4c34-b851-2bd5f6a69cba
                    7ee400b6-4abe-49dd-93ce-b168b9cdc7b9
                    8bdcca47-1392-4622-830a-c08b199df58a
                    8ed30779-eb8e-49c7-9815-a2b5b12b23db
                    0a18cad8-a879-4e2c-b72a-2cb0b31a7444
                    a2f08730-bae3-4a00-bec2-7771735d4cfa
                    2aa2c09f-fd1a-4e00-9620-ebd820139ef3
                    a2765733-88fb-404d-986f-0be8cb6f856e
                    8493b9d0-05c1-4ec8-953f-7598e41d773d
                    5a824e34-f7b7-4e69-9146-dd9edc26a7c6
                    08eb2f95-988c-49ce-b6ea-5f07c7f1653b
                    fb2bef24-f22a-4a60-b6e9-fc591eb87b79
                    5b9c07ef-f0d8-41a3-b57a-33cefe92b54b
                    9c3a6695-9456-4d08-ba98-9d624d21e515
                    57d0cc20-3d53-44f8-9a5a-131acae295f9
                    4c57a037-bbf8-4455-892e-7a59c6fa9b46
                    ff2eddc6-4341-408b-b463-5f3600f2cf91
                    f301785f-8ba9-42ed-a11c-ab64a55ba29e
                    1cbf0af1-3286-4479-9b2f-f1189cf888a6
                    eb686cf0-e876-4c83-8d97-b59a8cd703d0
                    d4a9a1a2-9116-4d11-b323-0dd76738b05c
                    5a13ebb6-c01a-4c0f-ae4e-d25058e51e25
                    6e1cbfdf-4e56-47e6-8e7b-1d1a7c6ce519
                    213be16e-3e89-43b5-99b8-b99586e39fe9
                    b21efc96-d1e3-4001-a5b0-5be2c81ce7ce
                    44736c65-744d-4a32-bbe7-640b2e4f98a2
                    4cdde1fc-d0ce-4898-b49e-d9aada0ac500
                    b9928c06-e363-4ec3-b3b3-36435c960edc
                    465ce9ba-9f3e-4661-8acd-1692ef5ef259
                    6b095276-8583-4ca0-8706-5d76a6418be0
                    c388b125-a0af-40dc-8627-96bbce068a28
                    97509b41-f3cb-42e2-bdd0-ca138c94ba56
                    6299bb58-d483-4a93-910f-d695279539d9
                    2ed3144e-f763-4206-867a-6ce21d9480ba
                    3ab62845-fcab-4078-9634-fa732e02259c
                    f788b8c9-e4f7-4b06-bf1b-0adbf4fa965a
                    2533a1fd-9bf6-440d-a926-7d9017f32322
                    385491bc-2a03-462a-b480-fc2d9e1ed327
                    8d5388aa-f2d8-4b9d-b660-651ccf380ed0
                    fab91780-1028-4534-b87f-3c5acc1f886a
                    7ef86791-be37-408c-af4a-020c29603f67
                    d9717ca6-43b0-4b2b-b4cf-8636d0fcb7ff
                    5a5a20ad-5d0c-4cd7-84aa-067129b93f74
                    c84e77c9-bf32-4e7b-b4a6-f20d28caeb78
                    a96aeb49-cabc-48e0-a68b-0ad7c2455d65
                    3abd39b3-a3bb-4307-8666-7bab65b1314c
                    4e41d3f7-6736-4433-aeea-53a5601b7c93
                    f8028142-d6e3-480c-8671-75251d5730a5
                    8f35b3c9-1255-4ffd-a544-5e68210615a0
                    ac8fb7b4-ac64-4e5c-aae6-c04138df47b4
                    4e4c47ab-4507-4f1d-9178-93b37344e8ee
                    2462c0ae-177f-4478-b665-64c5662dbd2e
                    cd09db12-50b1-4ebd-b7e0-e3962a014a58
                    96d15aff-24c3-4fb6-a81d-ed2b80173c55
                    c7cad8d5-c8c2-41e6-9a4e-7e5b9d4296be
                    ba348ece-5b0b-4527-90a9-62a8eb6090dd
                    de420a4f-ea09-4b17-8489-3afaf0abd883
                    67c86344-c2c4-4c98-bb9f-c2ab872c3ef8
                    92cc4842-9a53-45fb-bf49-7ba4943f5d26
                    a834198f-1ff7-4d21-8981-40e6fbd68e6e
                    05160528-1972-4ba2-b88e-391c4538fe5c
                    c965801f-b876-48e5-87c0-ca5d8981cfb5
                    e13551b7-5d4f-45ca-8786-1c161b5f4f10
                    376c9156-7a05-429e-be96-35a387db1724
                    8ea48966-8ff6-4c26-978b-a7b6e0bae1d8
                    df93e54c-ec9e-4e61-898c-cb8f21638887
                    c35f1ddc-b948-4586-a6c8-4099003921cc
                    23ae010b-57fd-4807-bbea-bdc6ccd6af4b
                    17b2cf6e-97ce-4af3-b84a-b2059b6197c2
                    05963b40-ca63-4bad-aca6-0f65a591076a
                    30c20ff5-6b61-4e83-9d20-bca54f7ea89f
                    97b08969-c51b-4b81-9817-97f5c00d8cb8
                    996065dd-689d-4c6a-9895-36b063e37ee3
                    a64b1d6a-e286-4613-ba69-4440142e3f2f
                    48768601-7850-49d0-a24c-5c105217e24f
                    6e609523-e35c-4460-894c-d95f4db6aa0f
                    94179700-c14b-4bcc-9acf-07c1e422568d
                    ec206e0e-bee6-4554-9ff9-175d5dcc71ca
                    82495f41-7d3d-4afe-b288-b2790390fef8
                    dae032e3-dac8-4493-841c-450540b79450
                    f4825681-0b92-40d9-af24-f2590be9342a
                    f9acc98b-a951-4e61-a949-287c95e3caa2
                    6de36e71-da5c-41bd-80c8-bee5f111e8e3
                    9058de7a-7d21-4e03-84fa-e772a99002e6
                    3f4524c7-6dda-4987-b602-9b802d246388
                    09d36456-3b30-42d2-b3a7-0f87e5f1ee6a
                    149c5bf6-684a-4c98-9197-ccf4d66d1af4
                    28825aa7-ab91-44b3-bd51-68b8af894ef2
                    a46feb77-c202-437d-8e58-95ba3bef6fce
                    97fde503-7f6c-4817-b4b4-2a74b266f1f0
                    2abdc9fd-094e-4c1d-a0a4-402150bbaa41
                    30c43f9f-1937-4d37-b77f-3c420f75a1ff
                    52c131d5-2615-4e5a-88d2-369e0c4ef917
                    209ae862-dc89-4104-a398-261c343f8b49
                    22be9a5e-ed65-474c-b3db-20cc0f2ac53c
                    0e5aeaf2-35cd-48af-96eb-69552443039c
                    fee509cc-8f48-41d7-8392-fa9634127e00
                    61b3785b-b6fa-4891-8398-6ed3a1180956
                    47b00b03-2ce4-4f7d-99c0-84f0e6ef41b0
                    78d54a47-81be-4a19-ab1d-85b094af2164
                    d7a38529-7ee8-49de-8e4e-f0084438995b
                    3ed8b0ab-ed15-4612-8fd9-78689c07ecb0
                    028ff4f5-92bd-40ac-bfa9-074f62e00fa4
                    e1c3bd3f-d190-4bc9-a482-dc03f2739ae3
                    eca6c1cc-a9ab-477b-b0cc-54e4e4f01da1
                    171d18ad-b19c-49e2-b990-9460de605f94
                    d15bcf29-546a-47bb-8d88-9ba1bd3d8c02
                    b6ab323f-3f6b-4a6b-a547-e0d6ca07f966
                    531d05ae-5318-48ae-b67d-4689711f6070
                    838b9b16-014f-45ed-a84a-6ad9952bca76
                    04c18e03-e43a-4e50-bdbc-12befecca732
                    564cbfac-b03f-41ce-87e9-e93891d8589b
                    08784d3f-63c6-491e-9bcc-2394af775f7a
                ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"