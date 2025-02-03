import sys, os
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
mac = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mac)
pip_designer_page = PageFactory().get_page_object('pip_designer_page', mac)
pip_room_page = PageFactory().get_page_object('pip_room_page', mac)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page', mac)
tips_area_page = PageFactory().get_page_object('tips_area_page',mac)
fix_enhance_page = PageFactory().get_page_object('fix_enhance_page',mac)
produce_page = PageFactory().get_page_object('produce_page', mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Fix Enhance_20.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Fix_Enhance_20/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Fix_Enhance_20/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Fix_Enhance_20():
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
            google_sheet_execution_log_init('Fix Enhance_20')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"Fix Enhance 20 result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        # Image > Select template "Landscape 01.jpg" to track1
        main_page.select_library_icon_view_media("Landscape 01.jpg")
        main_page.tips_area_insert_media_to_selected_track()
        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        # [O168] Enable Split Toning checkbox
        with uuid("65cacedb-7690-4a7c-870d-2a14312bb3e5") as case:
            check_result = fix_enhance_page.enhance.get_split_toning()
            # Verify default status (Disable)
            default_result = not check_result
            #ogger(default_result)

            fix_enhance_page.enhance.enable_split_toning()
            set_result = fix_enhance_page.enhance.get_split_toning()
            # Verify current status (Enable)
            case.result = default_result and set_result

        # [O170] Highlights > Hue > Default value=0
        with uuid("e428d1ba-cb78-4e1d-9d7f-2f19eda8b6ad") as case:
            check_result = fix_enhance_page.enhance.split_toning.highlights.hue.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # [O169] Color > Select color
        with uuid("e102e281-b0d2-42cd-8bd2-274bf28f7a51") as case:
            check_result = fix_enhance_page.enhance.split_toning.highlights.set_color(150, 100)
            time.sleep(DELAY_TIME)
            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'O169_preview.png')

            # logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O169_preview.png', current_image)
            case.result = check_preview and check_result

        # [O171] Highlights > Hue > Set value by drag slider
        with uuid("b6f18b00-6d5f-41d9-84fa-e7f0e35993e8") as case:
            fix_enhance_page.enhance.split_toning.highlights.hue.adjust_slider(360)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.highlights.hue.get_value()
            if check_result == '360':
                slider_result = True
            else:
                slider_result = False

            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O171_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O171_preview.png', current_image)

            # [O173] Highlights > Hue > Max = 360
            with uuid("3f40267a-bdee-4bb7-89f1-174752549b55") as case:
                check_result = fix_enhance_page.enhance.split_toning.highlights.hue.get_value()
                if check_result == '360':
                    case.result = True
                else:
                    case.result = False
            case.result = check_preview and slider_result

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        # Select template "Travel 01.jpg" to track1
        main_page.select_library_icon_view_media("Travel 01.jpg")
        main_page.tips_area_insert_media_to_selected_track()
        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        #Enable Split Toning checkbox
        fix_enhance_page.enhance.enable_split_toning()

        # [O175] Highlights > Saturation > Default value=0
        with uuid("33f6275f-418d-4a9f-80a6-08758a568adf") as case:
            check_result = fix_enhance_page.enhance.split_toning.highlights.saturation.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # Color > Select color
        fix_enhance_page.enhance.split_toning.highlights.set_color(4, 93)

        # [O174] Highlights > Hue > Up/Down arrow
        with uuid("324775f7-ad8e-4b89-9d76-479a89bd1e2a") as case:
            fix_enhance_page.enhance.split_toning.highlights.hue.click_arrow(1, 6)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.highlights.hue.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

            # [O172] Highlights > Hue > Min = 0
            with uuid("7395cc1c-a937-4008-a1f1-170ff16577d6") as case:
                check_result = fix_enhance_page.enhance.split_toning.highlights.hue.get_value()
                if check_result == '0':
                    case.result = True
                else:
                    case.result = False

        # Set Highlights > Hue = 10
        fix_enhance_page.enhance.split_toning.highlights.hue.click_arrow(0, 10)
        time.sleep(DELAY_TIME*0.5)

        # [O179] Highlights > Saturation > Up/Down arrow
        with uuid("9bc1cae0-5202-45b2-b0ad-159abcc6a256") as case:
            fix_enhance_page.enhance.split_toning.highlights.saturation.click_arrow(0, 7)
            time.sleep(DELAY_TIME)

            check_result = fix_enhance_page.enhance.split_toning.highlights.saturation.get_value()
            if check_result == '100':
                set_arrow = True
            else:
                set_arrow = False

            #logger(set_arrow)
            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O179_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O179_preview.png', current_image)

            # [O178] Highlights > Saturation > Max = 100
            with uuid("1250cc96-90af-41e9-9da5-56bbc6d19390") as case:
                check_result = fix_enhance_page.enhance.split_toning.highlights.saturation.get_value()
                if check_result == '100':
                    case.result = True
                else:
                    case.result = False
            case.result = check_preview and set_arrow

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        # Import video > Select template "shopping_mall.m2ts" to track1
        video_path = Test_Material_Folder + 'fix_enhance_20/shopping_mall.m2ts'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('shopping_mall.m2ts')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        # [O537] Video > Enable Split Toning checkbox
        with uuid("8f35b3c9-1255-4ffd-a544-5e68210615a0") as case:
            check_result = fix_enhance_page.enhance.get_split_toning()
            # Verify default status (Disable)
            default_result = not check_result
            #ogger(default_result)

            fix_enhance_page.enhance.enable_split_toning()
            set_result = fix_enhance_page.enhance.get_split_toning()
            # Verify current status (Enable)
            case.result = default_result and set_result

        # [O539] Highlights > Hue > Default value=0
        with uuid("4e4c47ab-4507-4f1d-9178-93b37344e8ee") as case:
            check_result = fix_enhance_page.enhance.split_toning.highlights.hue.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # [O538] Color > Select color
        with uuid("ac8fb7b4-ac64-4e5c-aae6-c04138df47b4") as case:
            check_result = fix_enhance_page.enhance.split_toning.highlights.set_color(60, 79)
            time.sleep(DELAY_TIME)

            current_value = fix_enhance_page.enhance.split_toning.highlights.hue.get_value()
            if current_value == '60':
                check_hue = True
            else:
                check_hue = False

            current_value = fix_enhance_page.enhance.split_toning.highlights.saturation.get_value()
            if current_value == '79':
                check_saturation = True
            else:
                check_saturation = False

            case.result = check_result and check_hue and check_saturation

        # [O540] Highlights > Hue > Set value by drag slider
        with uuid("2462c0ae-177f-4478-b665-64c5662dbd2e") as case:
            fix_enhance_page.enhance.split_toning.highlights.hue.adjust_slider(360)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.highlights.hue.get_value()
            if check_result == '360':
                slider_result = True
            else:
                slider_result = False

            main_page.set_timeline_timecode('00_00_04_10', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O540_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O540_preview.png', current_image)
            case.result = check_preview and slider_result


        # [O543] Highlights > Hue > Up/Down arrow
        with uuid("c7cad8d5-c8c2-41e6-9a4e-7e5b9d4296be") as case:
            fix_enhance_page.enhance.split_toning.highlights.hue.click_arrow(0, 3)
            time.sleep(DELAY_TIME*0.5)

            # [O542] Highlights > Hue > Max = 360
            with uuid("96d15aff-24c3-4fb6-a81d-ed2b80173c55") as case:
                check_result = fix_enhance_page.enhance.split_toning.highlights.hue.get_value()
                if check_result == '360':
                    case.result = True
                else:
                    case.result = False

            fix_enhance_page.enhance.split_toning.highlights.hue.click_arrow(1, 7)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.highlights.hue.get_value()
            if check_result == '353':
                case.result = True
            else:
                case.result = False

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        # Import video > Select template "Y man.m2ts" to track1
        video_path = Test_Material_Folder + 'fix_enhance_20/Y man.m2ts'
        time.sleep(DELAY_TIME*3)
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('Y man.m2ts')

        main_page.set_timeline_timecode('00_00_07_00', is_verify=False)
        time.sleep(DELAY_TIME)

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        #Enable Split Toning checkbox
        fix_enhance_page.enhance.enable_split_toning()

        # [O544] Highlights > Saturation > Default value=0
        with uuid("ba348ece-5b0b-4527-90a9-62a8eb6090dd") as case:
            check_result = fix_enhance_page.enhance.split_toning.highlights.saturation.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # Color > Select color
        fix_enhance_page.enhance.split_toning.highlights.set_color(2, 68)

        fix_enhance_page.enhance.split_toning.highlights.hue.click_arrow(1, 4)
        time.sleep(DELAY_TIME*0.5)
        check_result = fix_enhance_page.enhance.split_toning.highlights.hue.get_value()

        # [O541] Highlights > Hue > Min = 0
        with uuid("cd09db12-50b1-4ebd-b7e0-e3962a014a58") as case:
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # Set Hue value = 156
        fix_enhance_page.enhance.split_toning.highlights.hue.set_value(156)

        # [O545] Highlights > Saturation > Set value by drag slider
        with uuid("de420a4f-ea09-4b17-8489-3afaf0abd883") as case:
            fix_enhance_page.enhance.split_toning.highlights.saturation.adjust_slider(97)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.highlights.saturation.get_value()
            if check_result == '97':
                slider_result = True
            else:
                slider_result = False

            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O545_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O545_preview.png', current_image)
            case.result = check_preview and slider_result

        # [O547] Highlights > Saturation > Max = 100
        with uuid("92cc4842-9a53-45fb-bf49-7ba4943f5d26") as case:
            fix_enhance_page.enhance.split_toning.highlights.saturation.click_arrow(0, 4)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.highlights.saturation.get_value()
            if check_result == '100':
                case.result = True
            else:
                case.result = False

            # [O548] Highlights > Saturation > Up/Down arrow
            with uuid("a834198f-1ff7-4d21-8981-40e6fbd68e6e") as case:
                check_result = fix_enhance_page.enhance.split_toning.highlights.saturation.get_value()
                if check_result == '100':
                    case.result = True
                else:
                    case.result = False

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        # Select template "Skateboard 03.mp4" to track1
        main_page.select_library_icon_view_media("Skateboard 03.mp4")
        main_page.tips_area_insert_media_to_selected_track()
        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        #Enable Split Toning checkbox
        fix_enhance_page.enhance.enable_split_toning()

        # [O549] Highlights > Balance > Default value=0
        with uuid("05160528-1972-4ba2-b88e-391c4538fe5c") as case:
            check_result = fix_enhance_page.enhance.split_toning.balance.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # [O546] Highlights > Saturation > Min = 0
        with uuid("67c86344-c2c4-4c98-bb9f-c2ab872c3ef8") as case:
            fix_enhance_page.enhance.split_toning.highlights.saturation.click_arrow(1, 2)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.highlights.saturation.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # Color > Select color
        fix_enhance_page.enhance.split_toning.highlights.set_color(219, 66)

        # [O550] Highlights > Balance > Set value by drag slider
        with uuid("c965801f-b876-48e5-87c0-ca5d8981cfb5") as case:
            fix_enhance_page.enhance.split_toning.balance.adjust_slider(98)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.balance.get_value()
            if check_result == '98':
                slider_result = True
            else:
                slider_result = False

            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O550_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O550_preview.png', current_image)
            case.result = check_preview and slider_result

        # [O552] Highlights > Balance > Max = 100
        with uuid("376c9156-7a05-429e-be96-35a387db1724") as case:
            fix_enhance_page.enhance.split_toning.balance.click_arrow(0, 3)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.balance.get_value()
            if check_result == '100':
                case.result = True
            else:
                case.result = False

        # [O551] Highlights > Balance > Min = -100
        with uuid("e13551b7-5d4f-45ca-8786-1c161b5f4f10") as case:
            fix_enhance_page.enhance.split_toning.balance.set_value(-102)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.balance.get_value()
            if check_result == '-100':
                case.result = True
            else:
                case.result = False

        # [O553] Highlights > Balance > Up/Down arrow
        with uuid("8ea48966-8ff6-4c26-978b-a7b6e0bae1d8") as case:
            fix_enhance_page.enhance.split_toning.balance.set_value(16)
            time.sleep(DELAY_TIME*0.5)
            fix_enhance_page.enhance.split_toning.balance.click_arrow(0, 4)
            check_result = fix_enhance_page.enhance.split_toning.balance.get_value()
            if check_result == '20':
                arrow_result = True
            else:
                arrow_result = False

            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O553_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O553_preview.png', current_image)
            case.result = check_preview and arrow_result

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        # Import image > Select template "colorful.jpg" to track1
        image_path = Test_Material_Folder + 'fix_enhance_20/colorful.jpg'
        media_room_page.collection_view_right_click_import_media_files(image_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('colorful.jpg')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        #Enable Split Toning checkbox
        fix_enhance_page.enhance.enable_split_toning()

        # Color > Select color
        fix_enhance_page.enhance.split_toning.highlights.set_color(64, 90)
        time.sleep(DELAY_TIME)

        # [O176] Highlights > Saturation > Set value by drag slider
        with uuid("6c2a9f61-3570-4e5d-aa12-3215a31feb25") as case:
            fix_enhance_page.enhance.split_toning.highlights.saturation.adjust_slider(33)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.split_toning.highlights.saturation.get_value()
            logger(check_result)

            if check_result == '33':
                slider_result = True
            else:
                slider_result = False

            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O176_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O176_preview.png', current_image)
            case.result = check_preview and slider_result

        # [O177] Highlights > Saturation > Min = 0
        with uuid("8b1d0b43-7d6c-496c-ab2f-7f08f03420fe") as case:
            fix_enhance_page.enhance.split_toning.highlights.saturation.adjust_slider(-3)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.split_toning.highlights.saturation.get_value()
            logger(check_result)

            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # Color > Select color
        fix_enhance_page.enhance.split_toning.highlights.set_color(295, 59)
        time.sleep(DELAY_TIME)

        # [O180] Balance > Default value = 0
        with uuid("0928d2d5-df5c-417a-b0fc-e37d0e944a4d") as case:
            check_result = fix_enhance_page.enhance.split_toning.balance.get_value()
            if check_result == '0':
                default_result = True
            else:
                default_result = False
            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O180_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O180_upper_preview.png', current_image)
            case.result = check_preview and default_result

        # [O181] Balance > Slider
        with uuid("7c44a947-376f-41ef-ab04-13a46716c460") as case:
            fix_enhance_page.enhance.split_toning.balance.adjust_slider(102)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.split_toning.balance.get_value()
            if check_result == '100':
                case.result = True
            else:
                case.result = False

        # [O183] Balance > Max = 100
        with uuid("afb12a70-3578-4ee1-8684-786a9e24def7") as case:
            check_result = fix_enhance_page.enhance.split_toning.balance.get_value()
            if check_result == '100':
                max_result = True
            else:
                max_result = False

            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'O183_preview.png')

            # logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O183_preview.png', current_image)
            case.result = check_preview and max_result

        # [O184] Balance > Up/Down arrow
        with uuid("a0957a68-f92d-484e-bff8-e606b145a619") as case:
            fix_enhance_page.enhance.split_toning.balance.click_arrow(1, 10)
            time.sleep(DELAY_TIME)
            current_value = fix_enhance_page.enhance.split_toning.balance.get_value()
            if current_value == '90':
                check_down = True
            else:
                check_down = False

            fix_enhance_page.enhance.split_toning.balance.click_arrow(0, 4)
            time.sleep(DELAY_TIME)
            current_value = fix_enhance_page.enhance.split_toning.balance.get_value()
            if current_value == '94':
                check_up = True
            else:
                check_up = False
            case.result = check_down and check_up

        # [O182] Balance > Min = -100
        with uuid("cc7789de-4de6-426c-9642-6d3e237adf92") as case:
            fix_enhance_page.enhance.split_toning.balance.set_value(-200)
            time.sleep(DELAY_TIME)
            current_value = fix_enhance_page.enhance.split_toning.balance.get_value()
            if current_value == '-100':
                min_result = True
            else:
                min_result = False

            main_page.set_timeline_timecode('00_00_04_25', is_verify=False)
            time.sleep(DELAY_TIME*0.5)
            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'O182_preview.png')

            # logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O182_preview.png', current_image)
            case.result = check_preview and min_result

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        # Import image > Select template "hastur.jpg" to track1
        image_path = Test_Material_Folder + 'fix_enhance_20/hastur.jpg'
        media_room_page.collection_view_right_click_import_media_files(image_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('hastur.jpg')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        #Enable Split Toning checkbox
        fix_enhance_page.enhance.enable_split_toning()

        # [O186] Shadows > Hue > Default value=0
        with uuid("ea46dcef-4bc2-405c-a08f-d76d9e74497c") as case:
            check_result = fix_enhance_page.enhance.split_toning.shadow.hue.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # [O191] Shadows > Saturation > Default value=0
        with uuid("26265f51-15d3-4321-9035-602849f72f5b") as case:
            check_result = fix_enhance_page.enhance.split_toning.shadow.saturation.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '0':
                default_result = True
            else:
                default_result = False

            current_image = fix_enhance_page.snapshot(locator=L.effect_room.library,
                                                 file_name=Auto_Ground_Truth_Folder + 'O191_fix_enhance_default_setting.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O191_fix_enhance_default_setting.png', current_image)
            case.result = check_preview and default_result

        # [O185] Shadows > Color > Select color
        with uuid("170aac3b-f344-433b-8e75-1c94683ea24f") as case:
            fix_enhance_page.enhance.split_toning.shadow.set_color(304, 84)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.hue.get_value()
            if check_result == '304':
                check_hue = True
            else:
                check_hue = False

            check_result = fix_enhance_page.enhance.split_toning.shadow.saturation.get_value()
            if check_result == '84':
                check_saturation = True
            else:
                check_saturation = False

            case.result = check_hue and check_saturation

        # [O187] Shadows > Hue > Slider
        with uuid("8b535434-ba92-485e-9217-60036286b0a4") as case:
            fix_enhance_page.enhance.split_toning.shadow.hue.adjust_slider(257)
            time.sleep(DELAY_TIME*2)
            check_result = fix_enhance_page.enhance.split_toning.shadow.hue.get_value()
            if check_result == '257':
                check_slider = True
            else:
                check_slider = False

            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O187_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O187_preview.png', current_image)
            case.result = check_preview and check_slider

        main_page.set_timeline_timecode('00_00_03_20', is_verify=False)
        # [O188] Shadows > Hue > Min = 0
        with uuid("18312324-f637-4afa-929c-809202f4c06a") as case:
            fix_enhance_page.enhance.split_toning.shadow.hue.set_value(0)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.split_toning.shadow.hue.click_arrow(1,1)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.hue.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        # Insert image (Food.jpg) & Apply two effect (TV Wall + Zoom In)
        main_page.select_library_icon_view_media("Food.jpg")
        main_page.tips_area_insert_media_to_selected_track()
        time.sleep(DELAY_TIME)
        main_page.tap_EffectRoom_hotkey()
        time.sleep(DELAY_TIME*0.5)
        media_room_page.search_library('TV Wall')
        main_page.drag_media_to_timeline_playhead_position('TV Wall')
        time.sleep(DELAY_TIME*1.5)

        media_room_page.search_library_click_cancel()
        media_room_page.search_library('Zoom In')
        main_page.drag_media_to_timeline_playhead_position('Zoom In')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        #Enable Split Toning checkbox
        fix_enhance_page.enhance.enable_split_toning()

        fix_enhance_page.enhance.split_toning.shadow.set_color(113, 79)

        # [O190] Shadows > Hue > Up/Down arrow
        with uuid("579e6b46-aa14-47a6-a0dd-2624e5268c8d") as case:
            fix_enhance_page.enhance.split_toning.shadow.hue.click_arrow(0,8)
            time.sleep(DELAY_TIME*0.5)
            fix_enhance_page.enhance.split_toning.shadow.hue.click_arrow(1,2)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.hue.get_value()
            if check_result == '119':
                case.result = True
            else:
                case.result = False

        # [O195] Shadows > Saturation > Up/Down arrow
        with uuid("c5a2c850-052a-4e6d-a773-12d114951a16") as case:
            fix_enhance_page.enhance.split_toning.shadow.saturation.click_arrow(0,2)
            time.sleep(DELAY_TIME*0.5)
            fix_enhance_page.enhance.split_toning.shadow.saturation.click_arrow(1,5)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.saturation.get_value()
            if check_result == '76':
                arrow_result = True
            else:
                arrow_result = False

            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O195_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O195_preview.png', current_image)
            case.result = check_preview and arrow_result

        main_page.set_timeline_timecode('00_00_04_25', is_verify=False)
        time.sleep(DELAY_TIME*0.5)

        # [189] Shadows > Hue > Max = 360
        with uuid("7ed2a39b-4b6e-46bf-a9d3-502341000c5e") as case:
            fix_enhance_page.enhance.split_toning.shadow.hue.set_value(360)
            fix_enhance_page.enhance.split_toning.shadow.hue.click_arrow(0,3)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.hue.get_value()
            if check_result == '360':
                case.result = True
            else:
                case.result = False

        # [194] Shadows > Saturation > Max = 100
        with uuid("158be931-de00-4ad1-822b-e5cd23648a6d") as case:
            fix_enhance_page.enhance.split_toning.shadow.saturation.set_value(100)
            fix_enhance_page.enhance.split_toning.shadow.saturation.click_arrow(0,2)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.saturation.get_value()
            if check_result == '100':
                max_result = True
            else:
                max_result = False

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O194_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O194_upper_preview.png', current_image)
            case.result = check_preview and max_result

        # [192] Shadows > Saturation > Slider
        with uuid("177e56a2-d0a2-478e-beb6-7b5ead6f8337") as case:
            fix_enhance_page.enhance.split_toning.shadow.saturation.adjust_slider(50)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.saturation.get_value()
            if check_result == '50':
                case.result = True
            else:
                case.result = False

        # [193] Shadows > Saturation > Min = 0
        with uuid("da6aa583-019e-4ea4-82fa-da21e12f1eaf") as case:
            fix_enhance_page.enhance.split_toning.shadow.saturation.adjust_slider(0)
            fix_enhance_page.enhance.split_toning.shadow.saturation.click_arrow(1,2)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.saturation.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        # Import image > Select template "Y main.m2ts" to track1
        video_path = Test_Material_Folder + 'fix_enhance_20/Y man.m2ts'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('Y man.m2ts')

        main_page.set_timeline_timecode('00_00_02_02', is_verify=False)
        time.sleep(DELAY_TIME*0.5)

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        #Enable Split Toning checkbox
        fix_enhance_page.enhance.enable_split_toning()

        # [O555] Shadows > Hue > Default value=0
        with uuid("c35f1ddc-b948-4586-a6c8-4099003921cc") as case:
            check_result = fix_enhance_page.enhance.split_toning.shadow.hue.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # [O560] Shadows > Saturation > Default value=0
        with uuid("97b08969-c51b-4b81-9817-97f5c00d8cb8") as case:
            check_result = fix_enhance_page.enhance.split_toning.shadow.saturation.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '0':
                default_result = True
            else:
                default_result = False

            current_image = fix_enhance_page.snapshot(locator=L.effect_room.library,
                                                 file_name=Auto_Ground_Truth_Folder + 'O560_fix_enhance_default_setting.png')

            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O560_fix_enhance_default_setting.png', current_image)
            case.result = check_preview and default_result

        # [O554] Shadows > Color > Select color
        with uuid("df93e54c-ec9e-4e61-898c-cb8f21638887") as case:
            fix_enhance_page.enhance.split_toning.shadow.set_color(289, 75)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.hue.get_value()
            if check_result == '289':
                check_hue = True
            else:
                check_hue = False

            check_result = fix_enhance_page.enhance.split_toning.shadow.saturation.get_value()
            if check_result == '75':
                check_saturation = True
            else:
                check_saturation = False

            case.result = check_hue and check_saturation

        # [O556] Shadows > Hue > Slider
        with uuid("23ae010b-57fd-4807-bbea-bdc6ccd6af4b") as case:
            fix_enhance_page.enhance.split_toning.shadow.hue.adjust_slider(257)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.split_toning.shadow.hue.get_value()
            if check_result == '257':
                check_slider = True
            else:
                check_slider = False

            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O556_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O556_preview.png', current_image)
            case.result = check_preview and check_slider

        main_page.set_timeline_timecode('00_00_19_04', is_verify=False)
        # [O557] Shadows > Hue > Min = 0
        with uuid("17b2cf6e-97ce-4af3-b84a-b2059b6197c2") as case:
            fix_enhance_page.enhance.split_toning.shadow.hue.set_value(0)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.split_toning.shadow.hue.click_arrow(1,1)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.hue.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_10(self):
        # Insert video (Skateboard 01.mp4) & Apply effect (Double FishEye)
        main_page.select_library_icon_view_media("Skateboard 01.mp4")
        main_page.tips_area_insert_media_to_selected_track()
        time.sleep(DELAY_TIME)
        main_page.tap_EffectRoom_hotkey()
        time.sleep(DELAY_TIME*0.5)
        media_room_page.search_library('Double FishEye')
        main_page.drag_media_to_timeline_playhead_position('Double FishEye')
        time.sleep(DELAY_TIME)

        main_page.set_timeline_timecode('00_00_04_02', is_verify=False)

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        #Enable Split Toning checkbox
        fix_enhance_page.enhance.enable_split_toning()

        fix_enhance_page.enhance.split_toning.shadow.set_color(340, 45)

        # [O559] Shadows > Hue > Up/Down arrow
        with uuid("30c20ff5-6b61-4e83-9d20-bca54f7ea89f") as case:
            fix_enhance_page.enhance.split_toning.shadow.hue.click_arrow(0,2)
            time.sleep(DELAY_TIME*0.5)
            fix_enhance_page.enhance.split_toning.shadow.hue.click_arrow(1,7)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.hue.get_value()
            if check_result == '335':
                case.result = True
            else:
                case.result = False

        # [O564] Shadows > Saturation > Up/Down arrow
        with uuid("6e609523-e35c-4460-894c-d95f4db6aa0f") as case:
            fix_enhance_page.enhance.split_toning.shadow.saturation.click_arrow(0,8)
            time.sleep(DELAY_TIME*0.5)
            fix_enhance_page.enhance.split_toning.shadow.saturation.click_arrow(1,1)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.saturation.get_value()
            if check_result == '52':
                arrow_result = True
            else:
                arrow_result = False

            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O564_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O564_preview.png', current_image)
            case.result = check_preview and arrow_result

        # [O563] Shadows > Saturation > Max = 100
        with uuid("48768601-7850-49d0-a24c-5c105217e24f") as case:
            fix_enhance_page.enhance.split_toning.shadow.saturation.set_value(100)
            fix_enhance_page.enhance.split_toning.shadow.saturation.click_arrow(0,2)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.saturation.get_value()
            if check_result == '100':
                max_result = True
            else:
                max_result = False

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O563_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O563_upper_preview.png', current_image)
            case.result = check_preview and max_result

        # [O558] Shadows > Hue > Max = 360
        with uuid("05963b40-ca63-4bad-aca6-0f65a591076a") as case:
            fix_enhance_page.enhance.split_toning.shadow.hue.set_value(360)
            fix_enhance_page.enhance.split_toning.shadow.hue.click_arrow(0,3)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.hue.get_value()
            if check_result == '360':
                case.result = True
            else:
                case.result = False

        main_page.set_timeline_timecode('00_00_10_00', is_verify=False)

        # [O561] Shadows > Saturation > Slider
        with uuid("996065dd-689d-4c6a-9895-36b063e37ee3") as case:
            fix_enhance_page.enhance.split_toning.shadow.saturation.adjust_slider(86)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.saturation.get_value()
            if check_result == '86':
                case.result = True
            else:
                case.result = False

            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O561_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O561_preview.png', current_image)
            case.result = check_preview and arrow_result

        # [O562] Shadows > Saturation > Min = 0
        with uuid("a64b1d6a-e286-4613-ba69-4440142e3f2f") as case:
            fix_enhance_page.enhance.split_toning.shadow.saturation.adjust_slider(0)
            fix_enhance_page.enhance.split_toning.shadow.saturation.click_arrow(1,2)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.split_toning.shadow.saturation.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_11(self):
        # Import image > Select template "hastur.jpg" to track1
        image_path = Test_Material_Folder + 'fix_enhance_20/hastur.jpg'
        media_room_page.collection_view_right_click_import_media_files(image_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('hastur.jpg')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        # [O198] Enable HDR Effect checkbox
        with uuid("b9333829-6df8-4e85-9ab9-ea78e94d14ad") as case:
            check_result = fix_enhance_page.enhance.get_hdr_effect()
            # Verify default status (Disable)
            default_result = not check_result
            #ogger(default_result)

            fix_enhance_page.enhance.enable_hdr_effect()
            set_result = fix_enhance_page.enhance.get_hdr_effect()
            # Verify current status (Enable)
            case.result = default_result and set_result

        # [O199] Glow > Strength > Default value=50
        with uuid("18c59f7f-9f8a-44ae-9794-0251757bc774") as case:
            check_result = fix_enhance_page.enhance.hdr_effect.glow.strength.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '50':
                default_result = True
            else:
                default_result = False

            current_image = fix_enhance_page.snapshot(locator=L.effect_room.library,
                                                 file_name=Auto_Ground_Truth_Folder + 'O199_hdr_default_setting.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O199_hdr_default_setting.png', current_image)
            case.result = check_preview and default_result

        # [O204] Glow > Radius > Default value=5
        with uuid("de7b9100-428f-4d67-9e02-a92777d30e4d") as case:
            check_result = fix_enhance_page.enhance.hdr_effect.glow.radius.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '5':
                case.result = True
            else:
                case.result = False

        # [O209] Glow > Balance > Default value=0
        with uuid("f4dfd6ac-5bea-41b1-b03c-d9ec26215b44") as case:
            check_result = fix_enhance_page.enhance.hdr_effect.glow.balance.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # [O206] Glow > Radius > Min = 1
        with uuid("271f92b1-64e3-43cd-89a7-4c9b9bf9365a") as case:
            fix_enhance_page.enhance.hdr_effect.glow.radius.adjust_slider(0)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.radius.get_value()
            time.sleep(DELAY_TIME)
            logger(check_result)
            if check_result == '1':
                case.result = True
            else:
                case.result = False

        # [O205] Glow > Radius > Slider
        with uuid("989ad9d5-5a89-496a-a775-b194c6a6cf4a") as case:
            fix_enhance_page.enhance.hdr_effect.glow.radius.adjust_slider(50)
            time.sleep(DELAY_TIME*3)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.radius.get_value()
            logger(check_result)
            if check_result == '50':
                check_slider = True
            else:
                check_slider = False

            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O205_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O205_preview.png', current_image)
            case.result = check_preview and check_slider

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_12(self):
        # Import image > Select template "hastur.jpg" to track1
        image_path = Test_Material_Folder + 'fix_enhance_20/hastur.jpg'
        media_room_page.collection_view_right_click_import_media_files(image_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('hastur.jpg')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        fix_enhance_page.enhance.enable_hdr_effect()

        # [O200] HDR Effect  > Glow > Strength > Slider
        with uuid("5f2dfc95-45a6-4912-9d47-98ce8f297cc9") as case:
            fix_enhance_page.enhance.hdr_effect.glow.strength.adjust_slider(80)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.strength.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '80':
                case.result = True
            else:
                case.result = False

        # [O210] HDR Effect  > Glow > Balance > Slider
        with uuid("3bac20ba-8664-4aa2-afa9-33874574c123") as case:
            fix_enhance_page.enhance.hdr_effect.glow.balance.adjust_slider(54)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.balance.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '54':
                case.result = True
            else:
                case.result = False

        # [O215] HDR Effect  > Edge > Strength > Slider
        with uuid("6eb31f84-0851-4dd9-8b29-b35b914c2f04") as case:
            fix_enhance_page.enhance.hdr_effect.edge.strength.adjust_slider(41)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.strength.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '41':
                case.result = True
            else:
                case.result = False

        # [O223] HDR Effect  > Edge > Radius > Up/Down arrow
        with uuid("0618b4d8-215d-4073-a78d-1e443b0a9041") as case:
            fix_enhance_page.enhance.hdr_effect.edge.radius.click_arrow(0, 10)
            time.sleep(DELAY_TIME*0.5)
            fix_enhance_page.enhance.hdr_effect.edge.radius.click_arrow(1, 2)
            main_page.set_timeline_timecode('00_00_04_25', is_verify=False)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.radius.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '13':
                arrow_result= True
            else:
                arrow_result = False
            time.sleep(DELAY_TIME * 2)
            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O223_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O223_upper_preview.png', current_image)
            case.result = check_preview and arrow_result

        # [O224] HDR Effect  > Edge > Balance > Default value=0
        with uuid("f5a46e2f-5a7f-4479-9eb7-23ba57f11ade") as case:
            check_scroll_bar = fix_enhance_page.enhance.hdr_effect.drag_scroll_bar(1)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.balance.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '0':
                default_result = True
            else:
                default_result = False
            case.result = check_scroll_bar and default_result

        # [O227] HDR Effect  > Edge > Balance > Max = 100
        with uuid("2bb6a6bb-dcf0-4913-a684-109d96326430") as case:
            fix_enhance_page.enhance.hdr_effect.edge.balance.set_value(105)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.balance.get_value()
            time.sleep(DELAY_TIME*2)
            if check_result == '100':
                max_result = True
            else:
                max_result = False
            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O227_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O227_upper_preview.png', current_image)
            case.result = check_preview and max_result

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_13(self):
        # Import image > Select template "colorful.jpg" to track1
        image_path = Test_Material_Folder + 'fix_enhance_20/colorful.jpg'
        media_room_page.collection_view_right_click_import_media_files(image_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('colorful.jpg')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        fix_enhance_page.enhance.enable_hdr_effect()

        # [O201] Glow > Strength > Min=0
        with uuid("9cc36549-9038-4cc1-abf5-e0b09edd3a6e") as case:
            fix_enhance_page.enhance.hdr_effect.glow.strength.set_value(0)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.hdr_effect.glow.strength.click_arrow(1, 3)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.strength.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # [O203] Glow > Strength > Up/Down arrow
        with uuid("c79d6e91-4e81-43f9-9641-17ee9ab5dffa") as case:
            fix_enhance_page.enhance.hdr_effect.glow.strength.click_arrow(0, 12)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.hdr_effect.glow.strength.click_arrow(1, 3)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.strength.get_value()
            if check_result == '9':
                case.result = True
            else:
                case.result = False

        # [O207] Glow > Radius > Max=50
        with uuid("5f64235c-3a4e-405d-933c-1d08fef909ea") as case:
            fix_enhance_page.enhance.hdr_effect.glow.radius.set_value(50)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.hdr_effect.glow.radius.click_arrow(0, 3)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.radius.get_value()
            if check_result == '50':
                case.result = True
            else:
                case.result = False

        # [O212] Glow > Balance > Max=100
        with uuid("7d4e7fce-cc1f-436a-b182-6e147961629c") as case:
            fix_enhance_page.enhance.hdr_effect.glow.balance.set_value(100)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.hdr_effect.glow.balance.click_arrow(0, 3)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.balance.get_value()
            if check_result == '100':
                max_result = True
            else:
                max_result = False

            current_image = fix_enhance_page.snapshot(locator=L.effect_room.library,
                                                 file_name=Auto_Ground_Truth_Folder + 'O212_hdr_current_setting.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O212_hdr_current_setting.png', current_image)
            case.result = check_preview and max_result

        # [O218] Edge > Strength > Up/Down arrow
        with uuid("f8578caa-178b-48fb-af21-dcf37f38bac8") as case:
            fix_enhance_page.enhance.hdr_effect.edge.strength.click_arrow(1, 4)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.hdr_effect.edge.strength.click_arrow(0, 10)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.strength.get_value()
            if check_result == '6':
                case.result = True
            else:
                case.result = False

        # [O220] Edge > Radius > Slider
        with uuid("c211be92-df16-49a6-84bc-1eaa71c40865") as case:
            main_page.set_timeline_timecode('00_00_05_00', is_verify=False)
            time.sleep(DELAY_TIME*0.5)
            fix_enhance_page.enhance.hdr_effect.edge.radius.adjust_slider(10)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.hdr_effect.edge.radius.adjust_slider(35)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.radius.get_value()
            if check_result == '35':
                slider_result = True
            else:
                slider_result = False

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O220_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O220_upper_preview.png', current_image)
            case.result = check_preview and slider_result

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_14(self):
        # Insert image (Food.jpg) & Apply effect (Kaleidoscope)
        main_page.select_library_icon_view_media("Landscape 02.jpg")
        main_page.tips_area_insert_media_to_selected_track()
        time.sleep(DELAY_TIME)
        main_page.tap_EffectRoom_hotkey()
        time.sleep(DELAY_TIME*0.5)
        media_room_page.search_library('Kaleidoscope')
        main_page.drag_media_to_timeline_playhead_position('Kaleidoscope')
        time.sleep(DELAY_TIME)

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        #Enable HDR Effect checkbox
        fix_enhance_page.enhance.enable_hdr_effect()

        # [O214] Edge > Strength > Default is 0
        with uuid("08eb66f9-a4a5-41be-b73f-46e5fac3e390") as case:
            check_result = fix_enhance_page.enhance.hdr_effect.edge.strength.get_value()
            time.sleep(DELAY_TIME)

            if check_result == '0':
                case.result = True
            else:
                case.result = False

            fix_enhance_page.enhance.hdr_effect.edge.strength.click_arrow(0)
            time.sleep(DELAY_TIME)

        fix_enhance_page.enhance.hdr_effect.drag_scroll_bar(1)
        # [O219] Edge > Radius > Default is 5
        with uuid("efc4df1f-f92b-4fc7-8c67-5c0a1e85eb34") as case:
            check_result = fix_enhance_page.enhance.hdr_effect.edge.radius.get_value()
            time.sleep(DELAY_TIME)

            if check_result == '5':
                case.result = True
            else:
                case.result = False

        # [O221] Edge > Radius > Min = 1
        with uuid("70a8e110-bc32-4856-a3a3-2c8026c97fd8") as case:
            fix_enhance_page.enhance.hdr_effect.edge.radius.adjust_slider(0)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.radius.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '1':
                case.result = True
            else:
                case.result = False

        # [O226] Edge > Balance > Min = -100
        with uuid("5919c5de-0e3f-43ee-b22c-de7ce5ed2e9c") as case:
            set_result = fix_enhance_page.enhance.hdr_effect.edge.balance.set_value(-200)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.balance.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '-100':
                min_result = True
            else:
                min_result = False
            case.result = min_result and set_result

        # [O228] Edge > Balance > Up/Down arrow
        with uuid("87a7bb5e-bb3d-49b2-81ab-84b89ddf3385") as case:
            set_result = fix_enhance_page.enhance.hdr_effect.edge.balance.click_arrow(0, 9)
            time.sleep(DELAY_TIME)
            set_result = fix_enhance_page.enhance.hdr_effect.edge.balance.click_arrow(1, 4)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.balance.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '-95':
                arrow_result = True
            else:
                arrow_result = False

            main_page.set_timeline_timecode('00_00_03_29', is_verify=False)
            time.sleep(DELAY_TIME)

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O228_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O228_upper_preview.png', current_image)
            case.result = check_preview and arrow_result

        # [O217] Edge > Strength > Max = 80
        with uuid("0e489d06-e42c-40e8-8266-a95e6c3985ea") as case:
            fix_enhance_page.enhance.hdr_effect.edge.strength.adjust_slider(90)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.strength.get_value()
            time.sleep(DELAY_TIME)

            if check_result == '80':
                max_result = True
            else:
                max_result = False

            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O217_preview.png')
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O217_preview.png', current_image)
            case.result = check_preview and max_result

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_15(self):
        # Import image > Select template "hastur.jpg" to track1
        image_path = Test_Material_Folder + 'fix_enhance_20/hastur.jpg'
        media_room_page.collection_view_right_click_import_media_files(image_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('hastur.jpg')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        fix_enhance_page.enhance.enable_hdr_effect()

        # [O202] HDR Effect  > Glow > Strength > Max = 100
        with uuid("073a61e0-bc63-4ea9-b1f9-cd2cda22f2a9") as case:
            initial_value = fix_enhance_page.enhance.hdr_effect.glow.strength.get_value()
            time.sleep(DELAY_TIME)
            if initial_value == '50':
                initial_result = True
            else:
                initial_result = False

            fix_enhance_page.enhance.hdr_effect.glow.strength.set_value(101)
            time.sleep(DELAY_TIME)
            max_value = fix_enhance_page.enhance.hdr_effect.glow.strength.get_value()
            time.sleep(DELAY_TIME)
            if max_value == '100':
                max_result = True
            else:
                max_result = False

            case.result = initial_result and max_result

        # [O208] HDR Effect  > Glow > Radius > Up/Down arrow
        with uuid("9296c08b-9451-49d5-be50-4eb622d16923") as case:
            initial_value = fix_enhance_page.enhance.hdr_effect.glow.radius.get_value()
            time.sleep(DELAY_TIME)
            if initial_value == '5':
                initial_result = True
            else:
                initial_result = False

            fix_enhance_page.enhance.hdr_effect.glow.radius.click_arrow(1, 2)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.hdr_effect.glow.radius.click_arrow(0, 8)
            time.sleep(DELAY_TIME)
            max_value = fix_enhance_page.enhance.hdr_effect.glow.radius.get_value()
            time.sleep(DELAY_TIME)
            if max_value == '11':
                arrow_result = True
            else:
                arrow_result = False

            case.result = initial_result and arrow_result

        # [O213] HDR Effect  > Glow > Balance > Up/Down arrow
        with uuid("8cb01be7-d7a3-4bfb-8836-eb5de2cd2b90") as case:
            initial_value = fix_enhance_page.enhance.hdr_effect.glow.balance.get_value()
            time.sleep(DELAY_TIME)
            if initial_value == '0':
                initial_result = True
            else:
                initial_result = False

            fix_enhance_page.enhance.hdr_effect.glow.balance.click_arrow(1, 4)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.hdr_effect.glow.balance.click_arrow(0, 11)
            time.sleep(DELAY_TIME)
            max_value = fix_enhance_page.enhance.hdr_effect.glow.balance.get_value()
            time.sleep(DELAY_TIME)
            if max_value == '7':
                arrow_result = True
            else:
                arrow_result = False

            case.result = initial_result and arrow_result

        # [O211] Glow > Balance > Min=-100
        with uuid("21721dcc-f9f6-4be8-9002-1b97abb18dc5") as case:
            fix_enhance_page.enhance.hdr_effect.glow.balance.adjust_slider(-100)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.hdr_effect.glow.balance.click_arrow(1, 2)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.balance.get_value()
            if check_result == '-100':
                case.result = True
            else:
                case.result = False

        # [O216] Edge > Strength > Min=-20
        with uuid("d1df687e-7149-461f-994e-0c500712df36") as case:
            initial_value = fix_enhance_page.enhance.hdr_effect.edge.strength.get_value()
            time.sleep(DELAY_TIME)
            if initial_value == '0':
                initial_result = True
            else:
                initial_result = False

            fix_enhance_page.enhance.hdr_effect.edge.strength.set_value(-50)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.strength.get_value()
            if check_result == '-20':
                min_result = True
            else:
                min_result = False

            current_image = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O216_preview.png')
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O216_preview.png', current_image)

            case.result = initial_result and min_result and check_preview

        # [O222] Edge > Radius > Max = 50
        with uuid("3232dad3-08b9-4acd-a435-bafec675e9f8") as case:
            check_result = fix_enhance_page.enhance.hdr_effect.edge.radius.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '5':
                initial_result = True
            else:
                initial_result = False
            fix_enhance_page.enhance.hdr_effect.edge.radius.set_value(100)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.radius.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '50':
                max_result = True
            else:
                max_result = False
            case.result = initial_result and max_result

        fix_enhance_page.enhance.hdr_effect.drag_scroll_bar(1)

        # [O225] Edge > Balance > Slider
        with uuid("56e7b6bf-d7f9-41f3-8b5d-e042b6f65ec1") as case:
            check_result = fix_enhance_page.enhance.hdr_effect.edge.balance.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '0':
                initial_value = True
            else:
                initial_value = False

            fix_enhance_page.enhance.hdr_effect.edge.balance.set_value(49)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.balance.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '49':
                set_result = True
            else:
                set_result = False

            main_page.set_timeline_timecode('00_00_02_00', is_verify=False)
            time.sleep(DELAY_TIME)

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O225_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O225_upper_preview.png', current_image)
            case.result = check_preview and initial_value and set_result

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_16(self):
        # Set aspect ratio to 4:3
        main_page.set_project_aspect_ratio_4_3()
        time.sleep(DELAY_TIME)
        # Import video > Select template "Pool - Fix.mpg" to track1
        video_path = Test_Material_Folder + 'fix_enhance_20/Pool - Fix.mpg'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('Pool - Fix.mpg')

        main_page.set_timeline_timecode('00_00_05_00', is_verify=False)
        time.sleep(DELAY_TIME)

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        # [O439] Enable Video Denoise checkbox
        with uuid("ff2eddc6-4341-408b-b463-5f3600f2cf91") as case:
            check_result = fix_enhance_page.fix.get_video_denoise()
            # Verify default status (Disable)
            default_result = not check_result
            #ogger(default_result)

            fix_enhance_page.fix.enable_video_denoise()
            set_result = fix_enhance_page.fix.get_video_denoise()
            # Verify current status (Enable)
            case.result = default_result and set_result

        # [O441] Denoise Degree > Slider
        with uuid("1cbf0af1-3286-4479-9b2f-f1189cf888a6") as case:
            initial_value = fix_enhance_page.fix.video_denoise.degree.get_value()
            time.sleep(DELAY_TIME)
            if initial_value == '50':
                check_initial = True
            else:
                check_initial = False

            fix_enhance_page.fix.video_denoise.degree.adjust_slider(81)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.fix.video_denoise.degree.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '81':
                set_result = True
            else:
                set_result = False
            case.result = check_initial and set_result

        # [O445] Compare video qualities in split preview
        with uuid("6e1cbfdf-4e56-47e6-8e7b-1d1a7c6ce519") as case:
            set_result = fix_enhance_page.set_check_compare_in_split_preview(value=True)
            time.sleep(DELAY_TIME)

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O445_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O445_upper_preview.png', current_image)

            # Disable split preview
            fix_enhance_page.set_check_compare_in_split_preview(value=False)
            time.sleep(DELAY_TIME)

            current_library = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O445_preview.png')
            check_library_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O445_preview.png', current_library)

            case.result = check_preview and check_library_preview and set_result

        # [O444] Denoise Degree > Up/Down arrow
        with uuid("5a13ebb6-c01a-4c0f-ae4e-d25058e51e25") as case:
            fix_enhance_page.fix.video_denoise.degree.click_arrow(0, 5)
            time.sleep(DELAY_TIME)
            fix_enhance_page.fix.video_denoise.degree.click_arrow(1, 3)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.fix.video_denoise.degree.get_value()
            if check_result == '83':
                case.result = True
            else:
                case.result = False

        # [O442] Denoise Degree > Set to 0 by keyboard inputting
        with uuid("eb686cf0-e876-4c83-8d97-b59a8cd703d0") as case:
            fix_enhance_page.fix.video_denoise.degree.set_value(0)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.fix.video_denoise.degree.get_value()
            if check_result == '0':
                set_result = True
            else:
                set_result = False

            current_preview = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O442_preview.png')
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O442_preview.png', current_preview)

            case.result = check_preview and set_result

        # [O440] Denoise Degree > "+ / -" button
        with uuid("f301785f-8ba9-42ed-a11c-ab64a55ba29e") as case:
            fix_enhance_page.fix.video_denoise.degree.click_plus(7)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.fix.video_denoise.degree.get_value()
            if check_result == '7':
                up_result = True
            else:
                up_result = False

            fix_enhance_page.fix.video_denoise.degree.click_minus(2)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.fix.video_denoise.degree.get_value()
            if check_result == '5':
                down_result = True
            else:
                down_result = False
            case.result = up_result and down_result

        # [O443] Denoise Degree > Set to 100 by keyboard inputting
        with uuid("d4a9a1a2-9116-4d11-b323-0dd76738b05c") as case:
            fix_enhance_page.fix.video_denoise.degree.set_value(100)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.fix.video_denoise.degree.get_value()
            if check_result == '100':
                set_result = True
            else:
                set_result = False

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O443_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O443_upper_preview.png', current_image)

            case.result = check_preview and set_result

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_17(self):
        # Import video > Select template "mountain.mp4" to track1
        video_path = Test_Material_Folder + 'fix_enhance_20/mountain.mp4'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('mountain.mp4')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        # [O567] Enable HDR Effect checkbox
        with uuid("94179700-c14b-4bcc-9acf-07c1e422568d") as case:
            check_result = fix_enhance_page.enhance.get_hdr_effect()
            # Verify default status (Disable)
            default_result = not check_result
            #ogger(default_result)

            fix_enhance_page.enhance.enable_hdr_effect()
            set_result = fix_enhance_page.enhance.get_hdr_effect()
            # Verify current status (Enable)
            case.result = default_result and set_result


        # [O568] Glow > Strength > Default is 50
        with uuid("ec206e0e-bee6-4554-9ff9-175d5dcc71ca") as case:
            check_result = fix_enhance_page.enhance.hdr_effect.glow.strength.get_value()
            time.sleep(DELAY_TIME)

            if check_result == '50':
                case.result = True
            else:
                case.result = False

        # [O583] Edge > Strength > Default is 0
        with uuid("0e5aeaf2-35cd-48af-96eb-69552443039c") as case:
            check_result = fix_enhance_page.enhance.hdr_effect.edge.strength.get_value()
            time.sleep(DELAY_TIME)

            if check_result == '0':
                case.result = True
            else:
                case.result = False
            fix_enhance_page.enhance.hdr_effect.edge.strength.click_arrow(0)
            time.sleep(DELAY_TIME)

        # [O588] Edge > Radius > Default is 5
        with uuid("3ed8b0ab-ed15-4612-8fd9-78689c07ecb0") as case:
            check_result = fix_enhance_page.enhance.hdr_effect.edge.radius.get_value()
            time.sleep(DELAY_TIME)

            if check_result == '5':
                case.result = True
            else:
                case.result = False

        # [O591] Edge > Radius > Max = 50
        with uuid("eca6c1cc-a9ab-477b-b0cc-54e4e4f01da1") as case:
            fix_enhance_page.enhance.hdr_effect.edge.radius.set_value(55)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.radius.get_value()
            time.sleep(DELAY_TIME)

            if check_result == '50':
                max_result = True
            else:
                max_result = False

            current_image = fix_enhance_page.snapshot(locator=L.effect_room.library,
                                                 file_name=Auto_Ground_Truth_Folder + 'O591_hdr_parameter_settings.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O591_hdr_parameter_settings.png', current_image)
            case.result = check_preview and max_result

        # [O584] Edge > Strength > Slider
        with uuid("fee509cc-8f48-41d7-8392-fa9634127e00") as case:
            fix_enhance_page.enhance.hdr_effect.edge.strength.adjust_slider(43)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.strength.get_value()
            time.sleep(DELAY_TIME)

            if check_result == '43':
                slider_result = True
            else:
                slider_result = False

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O584_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O584_upper_preview.png', current_image)
            case.result = check_preview and slider_result

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_18(self):
        # Import video > Select template "mountain.mp4" to track1
        video_path = Test_Material_Folder + 'fix_enhance_20/mountain.mp4'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('mountain.mp4')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        main_page.set_timeline_timecode('00_00_10_09', is_verify=False)

        #Enable HDR Effect checkbox
        fix_enhance_page.enhance.enable_hdr_effect()

        # [O573] Glow > Radius > Default is 5
        with uuid("9058de7a-7d21-4e03-84fa-e772a99002e6") as case:
            check_result = fix_enhance_page.enhance.hdr_effect.glow.radius.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '5':
                case.result = True
            else:
                case.result = False

        # [O578] Glow > Balance > Default is 0
        with uuid("97fde503-7f6c-4817-b4b4-2a74b266f1f0") as case:
            check_result = fix_enhance_page.enhance.hdr_effect.glow.balance.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # [O572] Glow > Strength > Up/Down arrow
        with uuid("6de36e71-da5c-41bd-80c8-bee5f111e8e3") as case:
            fix_enhance_page.enhance.hdr_effect.glow.strength.set_value(70)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.hdr_effect.glow.strength.click_arrow(1, 2)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.hdr_effect.glow.strength.click_arrow(0, 4)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.strength.get_value()
            if check_result == '72':
                case.result = True
            else:
                case.result = False

        # [O585] Edge > Strength > Min = -20
        with uuid("61b3785b-b6fa-4891-8398-6ed3a1180956") as case:
            fix_enhance_page.enhance.hdr_effect.edge.strength.set_value(-50)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.strength.get_value()
            time.sleep(DELAY_TIME)

            if check_result == '-20':
                min_result = True
            else:
                min_result = False

            current_image = fix_enhance_page.snapshot(locator=L.effect_room.library,
                                                 file_name=Auto_Ground_Truth_Folder + 'O585_hdr_parameter_settings.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O585_hdr_parameter_settings.png', current_image)
            case.result = check_preview and min_result

        fix_enhance_page.enhance.hdr_effect.drag_scroll_bar(1)
        # [O593] Edge > Balance > Default is 0
        with uuid("b6ab323f-3f6b-4a6b-a547-e0d6ca07f966") as case:
            check_result = fix_enhance_page.enhance.hdr_effect.edge.balance.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # [O596] Edge > Balance > MAX = 100
        with uuid("04c18e03-e43a-4e50-bdbc-12befecca732") as case:
            fix_enhance_page.enhance.hdr_effect.edge.balance.set_value(100)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.hdr_effect.edge.balance.click_arrow(0, 2)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.balance.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '100':
                max_result = True
            else:
                max_result = False

            current_preview = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O596_preview.png')
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O596_preview.png', current_preview)

            case.result = check_preview and max_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_19(self):
        # Import image > Select template "hastur.jpg" to track1
        image_path = Test_Material_Folder + 'fix_enhance_20/hastur.jpg'
        media_room_page.collection_view_right_click_import_media_files(image_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('hastur.jpg')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        # [O120] Enable Color Adjustment checkbox
        with uuid("63f3499b-3f98-40cd-9ebe-232497de42df") as case:
            check_result = fix_enhance_page.enhance.get_color_adjustment()
            # Verify default status (Disable)
            default_result = not check_result
            #ogger(default_result)

            fix_enhance_page.enhance.enable_color_adjustment()
            set_result = fix_enhance_page.enhance.get_color_adjustment()
            # Verify current status (Enable)
            case.result = default_result and set_result

        # [O121] Exposure > Default value=100
        with uuid("7e8e9b8c-5720-4ead-9e82-12b99ce10e7e") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            if check_result == '100':
                case.result = True
            else:
                case.result = False

        # [O126] Brightness > Default value=0
        with uuid("5ddec5b2-603c-4d73-988f-c46d9266b587") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.brightness.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # [O131] Contrast > Default value=0
        with uuid("0481c7d7-3ad1-4be3-8c20-c11e1bad2fd6") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.contrast.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # [O123] Exposure > Set to 0 by keyboard inputting
        with uuid("cf6919b6-eb90-4720-86ba-2f26d9e42c18") as case:
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(0)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # [O127] Brightness > Slider
        with uuid("2d6e991b-fa3e-4c12-b7d8-7cec7de6c0e3") as case:
            fix_enhance_page.enhance.color_adjustment.brightness.adjust_slider(82)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.brightness.get_value()
            if check_result == '82':
                case.result = True
            else:
                case.result = False

        # [O135] Contrast > Up/Down arrow
        with uuid("50a1eedf-f924-4284-90cb-ae4749677b4f") as case:
            fix_enhance_page.enhance.color_adjustment.contrast.click_arrow(0, 10)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.color_adjustment.contrast.click_arrow(1, 2)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.contrast.get_value()
            if check_result == '8':
                arrow_result = True
            else:
                arrow_result = False

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O135_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O135_upper_preview.png', current_image, similarity =0.75)
            case.result = check_preview and arrow_result

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_20(self):
        # Import image > Select template "colorful.jpg" to track1
        image_path = Test_Material_Folder + 'fix_enhance_20/colorful.jpg'
        media_room_page.collection_view_right_click_import_media_files(image_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('colorful.jpg')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        # Enable Color Adjustment checkbox
        fix_enhance_page.enhance.enable_color_adjustment()

        # [O136] Hue > Default value=100
        with uuid("bdb9efaa-ae78-4cd5-a489-643e86545fb5") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.hue.get_value()
            if check_result == '100':
                case.result = True
            else:
                case.result = False

        # [O137] Hue > Slider
        with uuid("504ea93d-47b3-483f-b5f4-db9a4b72cd40") as case:
            fix_enhance_page.enhance.color_adjustment.hue.adjust_slider(150)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.hue.get_value()
            if check_result == '150':
                slider_result = True
            else:
                slider_result = False
            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O137_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O137_upper_preview.png', current_image)
            case.result = check_preview and slider_result

        # [O141] Saturation > Default value=100
        with uuid("bdd606e6-db3b-4d61-8fff-d55a8828a107") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.saturation.get_value()
            if check_result == '100':
                case.result = True
            else:
                case.result = False

        # [O145] Saturation > Up/Down arrow
        with uuid("29196787-1a3d-4f33-8c62-e875fcfa5e26") as case:
            fix_enhance_page.enhance.color_adjustment.saturation.click_arrow(1, 5)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.color_adjustment.saturation.click_arrow(0, 11)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.saturation.get_value()
            if check_result == '106':
                case.result = True
            else:
                case.result = False

        # [O129] Brightness > Set to 100 by keyboard inputting
        with uuid("9298db82-a705-421e-9150-968838a879aa") as case:
            fix_enhance_page.enhance.color_adjustment.brightness.set_value(100)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.brightness.get_value()
            if check_result == '100':
                case.result = True
            else:
                case.result = False

        # [O130] Brightness > Up/Down arrow
        with uuid("d2b8be81-7255-4d10-8480-963b40b452ec") as case:
            fix_enhance_page.enhance.color_adjustment.brightness.click_arrow(1, 9)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.color_adjustment.brightness.click_arrow(0, 3)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.color_adjustment.brightness.click_arrow(0, 1)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.brightness.get_value()
            if check_result == '95':
                case.result = True
            else:
                case.result = False

        # [O133] Contrast > Set to -100 by keyboard inputting
        with uuid("c4f5a647-b9d3-41a2-8425-1c88365d0f4a") as case:
            fix_enhance_page.enhance.color_adjustment.contrast.set_value(-100)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.contrast.get_value()
            if check_result == '-100':
                set_result = True
            else:
                set_result = False

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O133_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O133_upper_preview.png', current_image)
            case.result = check_preview and set_result

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_21(self):
        # Insert image (Food.jpg) & Apply effect (Kaleidoscope)
        main_page.select_library_icon_view_media("Landscape 02.jpg")
        main_page.tips_area_insert_media_to_selected_track()
        time.sleep(DELAY_TIME)

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        # Enable Color Adjustment checkbox
        fix_enhance_page.enhance.enable_color_adjustment()

        # [O151] Highlight healing > Default value=0
        with uuid("fa5085b8-a1ec-4d12-88dd-2b7d8f123a27") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.highlight_healing.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # [O146] Vibrancy > Default value=0
        with uuid("cbb30b12-d778-4402-bec1-09210ddecd33") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.vibrancy.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # [O155] Shadow > Default value=0
        with uuid("049a61e0-c94d-4b16-bfa5-d1faa8587d3f") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.shadow.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        main_page.set_timeline_timecode('00_00_03_01', is_verify=False)
        time.sleep(DELAY_TIME)
        # [O159] Sharpness > Default value=0
        with uuid("76da2dab-390f-493d-9227-454df1b69172") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.sharpness.get_value()
            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # [O160] Sharpness > Slider
        with uuid("eb768121-116d-45cb-86db-d5290c8f0d9e") as case:
            fix_enhance_page.enhance.color_adjustment.sharpness.adjust_slider(172)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.sharpness.get_value()
            if check_result == '172':
                case.result = True
            else:
                case.result = False

        # [O158] Shadow > Up/Down arrow
        with uuid("d3254ce5-44fd-4388-b824-fefb02d24007") as case:
            fix_enhance_page.enhance.color_adjustment.shadow.click_arrow(0, 6)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.color_adjustment.shadow.click_arrow(1, 3)
            time.sleep(DELAY_TIME)
            fix_enhance_page.enhance.color_adjustment.shadow.click_arrow(0, 5)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.shadow.get_value()
            if check_result == '8':
                case.result = True
            else:
                case.result = False

        # [O164] Compare video qualities in split preview
        with uuid("a4ccf8d5-6f24-493a-88d6-e7f66e0e2c49") as case:
            set_result = fix_enhance_page.set_check_compare_in_split_preview(value=True)
            time.sleep(DELAY_TIME)

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O164_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O164_upper_preview.png', current_image)

            case.result = set_result and check_preview

        main_page.set_timeline_timecode('00_00_00_00', is_verify=False)
        time.sleep(DELAY_TIME*2)
        # [O622] Render preview
        with uuid("daedb221-fb41-4b1d-8032-69e32001dd9c") as case:
            timeline_operation_page.click_view_entire_video_btn()

            timeline_operation_page.edit_timeline_render_preview()

            time.sleep(DELAY_TIME*2)
            current_render_preview = timeline_operation_page.snapshot_timeline_render_clip(track_index=0, clip_index=0,
                                                 file_name=Auto_Ground_Truth_Folder + 'O622_render_preview.png')
            check_render_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O622_render_preview.png', current_render_preview)

            current_preview = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O622_preview.png')
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O622_preview.png', current_preview)

            case.result = check_preview and check_render_preview

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_22(self):
        # Import video > Select template "shopping_mall.m2ts" to track1
        video_path = Test_Material_Folder + 'fix_enhance_20/shopping_mall.m2ts'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('shopping_mall.m2ts')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        fix_enhance_page.enhance.enable_hdr_effect()

        # [O574] HDR Effect  > Glow > Radius > Slider
        with uuid("3f4524c7-6dda-4987-b602-9b802d246388") as case:
            fix_enhance_page.enhance.hdr_effect.glow.radius.adjust_slider(35)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.radius.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '35':
                case.result = True
            else:
                case.result = False

        # [O571] HDR Effect  > Glow > Strength > Max = 100
        with uuid("f4825681-0b92-40d9-af24-f2590be9342a") as case:
            fix_enhance_page.enhance.hdr_effect.glow.strength.adjust_slider(105)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.strength.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '100':
                case.result = True
            else:
                case.result = False

        # [O582] HDR Effect  > Glow > Balance > Up/Down arrow
        with uuid("22be9a5e-ed65-474c-b3db-20cc0f2ac53c") as case:
            fix_enhance_page.enhance.hdr_effect.glow.balance.set_value(65)
            time.sleep(DELAY_TIME*0.5)
            fix_enhance_page.enhance.hdr_effect.glow.balance.click_arrow(1, 2)
            time.sleep(DELAY_TIME*0.5)
            fix_enhance_page.enhance.hdr_effect.glow.balance.click_arrow(0, 4)
            time.sleep(DELAY_TIME*0.5)
            check_value = fix_enhance_page.enhance.hdr_effect.glow.balance.get_value()
            time.sleep(DELAY_TIME)
            if check_value == '67':
                case.result = True
            else:
                case.result = False

        main_page.set_timeline_timecode('00_00_09_01', is_verify=False)
        time.sleep(DELAY_TIME)

        # [O589] HDR Effect  > Edge > Radius > Slider
        with uuid("028ff4f5-92bd-40ac-bfa9-074f62e00fa4") as case:
            fix_enhance_page.enhance.hdr_effect.edge.strength.click_arrow(0,2)
            time.sleep(DELAY_TIME*0.5)

            fix_enhance_page.enhance.hdr_effect.edge.radius.adjust_slider(39)
            time.sleep(DELAY_TIME*0.5)

            check_value = fix_enhance_page.enhance.hdr_effect.edge.radius.get_value()
            time.sleep(DELAY_TIME)
            if check_value == '39':
                slider_result = True
            else:
                slider_result = False

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O589_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O589_upper_preview.png', current_image)

            case.result = check_preview and slider_result

        # [O595] HDR Effect  > Edge > Balance > Min = -100
        with uuid("838b9b16-014f-45ed-a84a-6ad9952bca76") as case:
            fix_enhance_page.enhance.hdr_effect.drag_scroll_bar(1)
            time.sleep(DELAY_TIME * 0.5)

            fix_enhance_page.enhance.hdr_effect.edge.balance.set_value(-105)
            time.sleep(DELAY_TIME*0.5)

            check_value = fix_enhance_page.enhance.hdr_effect.edge.balance.get_value()
            time.sleep(DELAY_TIME)
            if check_value == '-100':
                case.result = True
            else:
                case.result = False

        # [O597] HDR Effect  > Edge > Balance > Up/Down arrow
        with uuid("08784d3f-63c6-491e-9bcc-2394af775f7a") as case:
            fix_enhance_page.enhance.hdr_effect.edge.balance.click_arrow(0, 10)
            time.sleep(DELAY_TIME*0.5)
            fix_enhance_page.enhance.hdr_effect.edge.balance.click_arrow(1, 2)
            time.sleep(DELAY_TIME*0.5)
            check_value = fix_enhance_page.enhance.hdr_effect.edge.balance.get_value()
            time.sleep(DELAY_TIME)
            if check_value == '-92':
                arrow_result = True
            else:
                arrow_result = False

            current_preview = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O597_preview.png')
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O597_preview.png', current_preview)

            case.result = check_preview and arrow_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_23(self):
        # Import video > Select template "mountain.mp4" to track1
        video_path = Test_Material_Folder + 'fix_enhance_20/mountain.mp4'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('mountain.mp4')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        # [O268] White Balance  > White calibration > i button
        with uuid("47fbcbed-ba9b-4b5e-b8e9-544c0b2d7e86") as case:
            # Enter (White Balance)
            fix_enhance_page.fix.switch_to_white_balance()

            # Click (Calibration) button
            fix_enhance_page.fix.white_balance.click_white_calibrate_button()

            # Click i button
            main_page.exist_click(L.fix_enhance.fix.white_balance.white_calibration.btn_i)
            time.sleep(DELAY_TIME*3)
            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O268_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O268_upper_preview.png', current_image)

            # close i button window

            main_page.press_esc_key()
            time.sleep(DELAY_TIME*0.5)
            # Close (White calibration) window
            check_close_result = fix_enhance_page.fix.white_balance.white_calibration.click_close()

            case.result = check_preview and check_close_result

            # Disable (White balance)
            fix_enhance_page.fix.enable_white_balance(value=False)

        fix_enhance_page.enhance.enable_hdr_effect()

        # [O569] HDR Effect  > Glow > Strength > Slider
        with uuid("82495f41-7d3d-4afe-b288-b2790390fef8") as case:
            default_value = fix_enhance_page.enhance.hdr_effect.glow.strength.get_value()
            if default_value == '50':
                initial_value = True
            else:
                initial_value = False
            fix_enhance_page.enhance.hdr_effect.glow.strength.adjust_slider(72)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.strength.get_value()
            time.sleep(DELAY_TIME)
            if check_result == '72':
                set_slider = True
            else:
                set_slider = False
            case.result = initial_value and set_slider

        # [O570] HDR Effect  > Glow > Strength > Min = 0
        with uuid("dae032e3-dac8-4493-841c-450540b79450") as case:
            fix_enhance_page.enhance.hdr_effect.glow.strength.set_value(0)
            fix_enhance_page.enhance.hdr_effect.glow.strength.click_arrow(1,3)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.strength.get_value()

            if check_result == '0':
                case.result = True
            else:
                case.result = False

        # Set Glow > Strength = 88
        fix_enhance_page.enhance.hdr_effect.glow.strength.adjust_slider(88)

        # [O575] HDR Effect  > Glow > Radius > Min = 1
        with uuid("09d36456-3b30-42d2-b3a7-0f87e5f1ee6a") as case:
            default_value = fix_enhance_page.enhance.hdr_effect.glow.radius.get_value()
            if default_value == '5':
                initial_value = True
            else:
                initial_value = False
            fix_enhance_page.enhance.hdr_effect.glow.radius.click_arrow(1,6)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.radius.get_value()

            if check_result == '1':
                min_result = True
            else:
                min_result = False

            case.result = initial_value and min_result

        # [O581] HDR Effect  > Glow > Balance > Max = 100
        with uuid("52c131d5-2615-4e5a-88d2-369e0c4ef917") as case:
            fix_enhance_page.enhance.hdr_effect.glow.balance.set_value(105)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.hdr_effect.glow.balance.get_value()
            if check_result == '100':
                max_value = True
            else:
                max_value = False

            time.sleep(DELAY_TIME*0.5)
            current_preview = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O581_preview.png')
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O581_preview.png', current_preview)

            case.result = max_value and check_preview

        # [O586] HDR Effect  > Edge > Strength > Max = 80
        with uuid("47b00b03-2ce4-4f7d-99c0-84f0e6ef41b0") as case:
            fix_enhance_page.enhance.hdr_effect.edge.strength.set_value(90)
            time.sleep(DELAY_TIME*0.5)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.strength.get_value()
            if check_result == '80':
                case.result = True
            else:
                case.result = False

        # [O590] HDR Effect  > Edge > Radius > Min = 1
        with uuid("e1c3bd3f-d190-4bc9-a482-dc03f2739ae3") as case:
            default_value = fix_enhance_page.enhance.hdr_effect.edge.radius.get_value()
            if default_value == '5':
                default_result = True
            else:
                default_result = False

            fix_enhance_page.enhance.hdr_effect.edge.radius.set_value(0)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.radius.get_value()
            if check_result == '1':
                min_result = True
            else:
                min_result = False

            time.sleep(DELAY_TIME * 2)
            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O590_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O590_upper_preview.png', current_image)

            case.result = default_result and min_result and check_preview

        main_page.set_timeline_timecode('00_00_10_01', is_verify=False)
        time.sleep(DELAY_TIME)

        fix_enhance_page.enhance.hdr_effect.drag_scroll_bar(1)
        # [O594] Edge > Balance > Slider
        with uuid("531d05ae-5318-48ae-b67d-4689711f6070") as case:
            check_result = fix_enhance_page.enhance.hdr_effect.edge.balance.get_value()
            if check_result == '0':
                default_result = True
            else:
                default_result = False

            fix_enhance_page.enhance.hdr_effect.edge.balance.adjust_slider(43)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.balance.get_value()
            if check_result == '43':
                slider_result = True
            else:
                slider_result = False
            case.result = default_result and slider_result

        # [O592] HDR Effect  > Edge > Radius > Up/Down arrow
        with uuid("d15bcf29-546a-47bb-8d88-9ba1bd3d8c02") as case:
            fix_enhance_page.enhance.hdr_effect.edge.radius.click_arrow(0,11)
            time.sleep(DELAY_TIME * 0.5)
            fix_enhance_page.enhance.hdr_effect.edge.radius.click_arrow(1, 2)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.hdr_effect.edge.radius.get_value()
            if check_result == '10':
                arrow_result = True
            else:
                arrow_result = False

            time.sleep(DELAY_TIME * 2)
            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O592_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O592_upper_preview.png', current_image)

            case.result = arrow_result and check_preview

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_24(self):
        # Import image > Select template "hastur.jpg" to track1
        image_path = Test_Material_Folder + 'fix_enhance_20/hastur.jpg'
        media_room_page.collection_view_right_click_import_media_files(image_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('hastur.jpg')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        # Enable Color Adjustment
        fix_enhance_page.enhance.enable_color_adjustment()

        # [O122] Exposure > slider
        with uuid("9389ee7e-aba5-4400-89b0-a91e086ac6ac") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            if check_result == '100':
                default_value = True
            else:
                default_value = False
            time.sleep(DELAY_TIME*0.5)
            fix_enhance_page.enhance.color_adjustment.exposure.adjust_slider(24)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            if check_result == '24':
                check_slider = True
            else:
                check_slider = False
            case.result = default_value and check_slider

        # [O128] Brightness > Set to -100 by keyboard inputting
        with uuid("7a083fdf-3e29-427d-bddf-5a43ecfc0685") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.brightness.get_value()
            if check_result == '0':
                default_value = True
            else:
                default_value = False

            time.sleep(DELAY_TIME * 0.5)
            fix_enhance_page.enhance.color_adjustment.brightness.set_value(-100)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.brightness.get_value()
            if check_result == '-100':
                min_value = True
            else:
                min_value = False

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O128_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O128_upper_preview.png', current_image, similarity =0.75)

            case.result = default_value and min_value and check_preview

        # [O125] Exposure > Set Exposure adjustmen by Up/Down arrow
        with uuid("2d17b5a3-00c7-4389-9730-65ebe4f8ebd5") as case:
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(158)
            time.sleep(DELAY_TIME * 0.5)
            fix_enhance_page.enhance.color_adjustment.exposure.click_arrow(0,10)
            time.sleep(DELAY_TIME * 0.5)
            fix_enhance_page.enhance.color_adjustment.exposure.click_arrow(1, 3)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            if check_result == '165':
                case.result = True
            else:
                case.result = False

        # [O140] Hue > Up/Down arrow
        with uuid("ae4d33db-8cad-4809-b481-1ba694480476") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.hue.get_value()
            if check_result == '100':
                default_value = True
            else:
                default_value = False

            time.sleep(DELAY_TIME * 0.5)
            fix_enhance_page.enhance.color_adjustment.hue.click_arrow(0,5)
            time.sleep(DELAY_TIME * 0.5)
            fix_enhance_page.enhance.color_adjustment.hue.click_arrow(1, 13)
            time.sleep(DELAY_TIME * 2)
            check_result = fix_enhance_page.enhance.color_adjustment.hue.get_value()
            if check_result == '92':
                arrow_result = True
            else:
                arrow_result = False
            case.result = default_value and arrow_result

        # [O139] Hue > Set to 200 by keyboard inputting
        with uuid("9bf27615-7015-40d3-9255-8c5b24cf975a") as case:
            fix_enhance_page.enhance.color_adjustment.hue.set_value(200)
            fix_enhance_page.enhance.color_adjustment.hue.click_arrow(0,2)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.color_adjustment.hue.get_value()
            if check_result == '200':
                set_result = True
            else:
                set_result = False

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O139_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O139_upper_preview.png', current_image)

            case.result = set_result and check_preview

        # [O156] Shadow > slider
        with uuid("a4afaa0a-9d5c-4130-8377-384e0b53107e") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.shadow.get_value()
            if check_result == '0':
                default_value = True
            else:
                default_value = False
            time.sleep(DELAY_TIME*0.5)
            fix_enhance_page.enhance.color_adjustment.shadow.adjust_slider(81)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.shadow.get_value()
            if check_result == '81':
                check_slider = True
            else:
                check_slider = False
            case.result = default_value and check_slider

        # [O144] Saturation > Set to 200 by keyboard inputting
        with uuid("988c2e99-9a04-4846-91e8-4ba6c6f37d78") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.saturation.get_value()
            if check_result == '100':
                default_value = True
            else:
                default_value = False

            fix_enhance_page.enhance.color_adjustment.saturation.set_value(200)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.color_adjustment.saturation.get_value()
            if check_result == '200':
                set_result = True
            else:
                set_result = False

            case.result = default_value and set_result
        # [O161] Sharpness > Set to 100 by keyboard inputting
        with uuid("c481d00d-2794-4318-add8-7edc1cd310b2") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.sharpness.get_value()
            if check_result == '0':
                default_value = True
            else:
                default_value = False
            time.sleep(DELAY_TIME*0.5)
            fix_enhance_page.enhance.color_adjustment.sharpness.set_value(100)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.sharpness.get_value()
            if check_result == '100':
                set_result = True
            else:
                set_result = False

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O161_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O161_upper_preview.png', current_image)

            case.result = default_value and set_result and check_preview

        # [O149] Vibrancy > Set to 100 by keyboard inputting
        with uuid("0f572a24-c3cf-40e1-a209-f70fbcfe4151") as case:
            fix_enhance_page.enhance.color_adjustment.vibrancy.set_value(100)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.color_adjustment.vibrancy.get_value()
            if check_result == '100':
                case.result = True
            else:
                case.result = False

        # [O623] Produce
        with uuid("06ff1aac-758c-40ea-9e74-4da60181520a") as case:
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 1280 x 720/30p (16 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

                # Get produced file name
                explore_file = produce_page.get_produced_filename()

                # Start : produce
                produce_page.click_start()
                for x in range(15):
                    check_result = produce_page.check_produce_complete()
                    if check_result is True:
                        break
                    else:
                        time.sleep(DELAY_TIME)

                # Back to Edit
                produce_page.click_back_to_edit()
                time.sleep(DELAY_TIME * 2)

                # Verify : Can find the produced file in Media Room
                verify_step1 = main_page.select_library_icon_view_media(explore_file)

                # Verify 2 : Set timecode to (00:00:02:12)
                main_page.set_timeline_timecode('00_00_02_12', is_verify=False)
                time.sleep(DELAY_TIME)
                current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'O623_produce_library_preview.png')
                verify_step2 = produce_page.compare(Ground_Truth_Folder + 'O623_produce_library_preview.png', current_image, similarity=0.85)
                time.sleep(DELAY_TIME * 2)
                case.result = verify_step1 and verify_step2
                # Remove the produced file
                main_page.select_library_icon_view_media(explore_file)
                media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_25(self):
        # Import image > Select template "colorful.jpg" to track1
        image_path = Test_Material_Folder + 'fix_enhance_20/colorful.jpg'
        media_room_page.collection_view_right_click_import_media_files(image_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('colorful.jpg')

        tips_area_page.click_fix_enhance()
        result = fix_enhance_page.is_in_fix_enhance()
        if not result:
            raise Exception

        # Enable Color Adjustment
        fix_enhance_page.enhance.enable_color_adjustment()

        # [O143] Saturation > Set to 0 by keyboard inputting
        with uuid("86cbab8a-c946-4ed8-a5ff-d9c730959ee4") as case:
            fix_enhance_page.enhance.color_adjustment.saturation.set_value(0)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.color_adjustment.saturation.get_value()
            if check_result == '0':
                set_result = True
            else:
                set_result = False

            time.sleep(DELAY_TIME*0.5)
            current_preview = fix_enhance_page.snapshot(locator=main_page.area.preview.main,
                                                 file_name=Auto_Ground_Truth_Folder + 'O143_preview.png')
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O143_preview.png', current_preview)

            case.result = set_result and check_preview

        # Set value to 154
        fix_enhance_page.enhance.color_adjustment.saturation.set_value(154)

        # [O147] Vibrancy > slider
        with uuid("7e1798e9-6718-4378-ae73-d8f6b1f3f9c5") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.vibrancy.get_value()
            if check_result == '0':
                default_value = True
            else:
                default_value = False

            fix_enhance_page.enhance.color_adjustment.vibrancy.adjust_slider(-75)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.color_adjustment.vibrancy.get_value()
            if check_result == '-75':
                slider_value = True
            else:
                slider_value = False

            case.result = default_value and slider_value

        # [O150] Vibrancy > Up/Down arrow
        with uuid("4a781a86-738a-4f8d-bed2-f2f706ce4683") as case:
            fix_enhance_page.enhance.color_adjustment.vibrancy.click_arrow(0, 6)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.color_adjustment.vibrancy.get_value()
            if check_result == '-69':
                plus_result = True
            else:
                plus_result = False

            fix_enhance_page.enhance.color_adjustment.vibrancy.click_arrow(1, 2)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.color_adjustment.vibrancy.get_value()
            if check_result == '-71':
                minus_result = True
            else:
                minus_result = False

            case.result = plus_result and minus_result

        # [O152] Highlight healing > Slider
        with uuid("eb9e45cd-6948-472e-bbbc-e04b0f69eb62") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.highlight_healing.get_value()
            if check_result == '0':
                default_value = True
            else:
                default_value = False

            fix_enhance_page.enhance.color_adjustment.highlight_healing.adjust_slider(88)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.color_adjustment.highlight_healing.get_value()
            if check_result == '88':
                slider_result = True
            else:
                slider_result = False

            case.result = default_value and slider_result

        # [O162] Sharpness > Up/Down arrow
        with uuid("306f9d09-9dfa-4fe2-b1a9-5efacbdfb091") as case:
            fix_enhance_page.enhance.color_adjustment.sharpness.click_arrow(0, 4)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.color_adjustment.sharpness.get_value()
            if check_result == '4':
                first_result = True
            else:
                first_result = False
            time.sleep(DELAY_TIME*0.5)
            fix_enhance_page.enhance.color_adjustment.sharpness.set_value(80)
            time.sleep(DELAY_TIME*0.5)
            fix_enhance_page.enhance.color_adjustment.sharpness.click_arrow(1,5)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.color_adjustment.sharpness.get_value()
            if check_result == '75':
                set_result = True
            else:
                set_result = False

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O162_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O162_upper_preview.png', current_image)

            case.result = first_result and set_result and check_preview

        # [O148] Vibrancy > Set to -100 by keyboard inputting
        with uuid("07d1104a-2fa9-4a36-b46b-88bd4c3fec4e") as case:
            fix_enhance_page.enhance.color_adjustment.vibrancy.adjust_slider(-100)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.color_adjustment.vibrancy.get_value()
            if check_result == '-100':
                case.result = True
            else:
                case.result = False

        # [O124] Exposure > Set to 200 by keyboard inputting
        with uuid("7c232f60-7aa7-45d3-b46f-5c7df607b641") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            if check_result == '100':
                default_value = True
            else:
                default_value = False
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(200)
            time.sleep(DELAY_TIME)
            check_result = fix_enhance_page.enhance.color_adjustment.exposure.get_value()
            if check_result == '200':
                set_result = True
            else:
                set_result = False

            case.result = default_value and set_result

        # [O132] Contrast > Slider
        with uuid("f9246f17-6645-4897-818c-ef820fefbc18") as case:
            check_result = fix_enhance_page.enhance.color_adjustment.contrast.get_value()
            if check_result == '0':
                default_value = True
            else:
                default_value = False

            fix_enhance_page.enhance.color_adjustment.contrast.adjust_slider(77)
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.color_adjustment.contrast.get_value()
            if check_result == '77':
                slider_result = True
            else:
                slider_result = False

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O132_upper_preview.png')

            #logger(current_image)
            check_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O132_upper_preview.png', current_image)

            case.result = default_value and slider_result and check_preview

        # [O619] Undo/Redo
        with uuid("c4cd50b9-fa61-46a9-904a-07128b5ed45d") as case:
            main_page.click_undo()
            time.sleep(DELAY_TIME * 0.5)
            check_result = fix_enhance_page.enhance.color_adjustment.contrast.get_value()
            if check_result == '0':
                undo_result = True
            else:
                undo_result = False

            main_page.click_redo()
            time.sleep(DELAY_TIME * 2)

            current_image = fix_enhance_page.snapshot(locator=L.library_preview.upper_view_region,
                                                 file_name=Auto_Ground_Truth_Folder + 'O619_upper_preview.png')

            #logger(current_image)
            check_redo_preview = fix_enhance_page.compare(Ground_Truth_Folder + 'O132_upper_preview.png', current_image)

            case.result = undo_result and check_redo_preview