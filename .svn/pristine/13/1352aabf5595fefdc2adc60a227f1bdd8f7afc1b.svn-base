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
mwc = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mwc)
mask_designer_page = PageFactory().get_page_object('mask_designer_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Mask Designer.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Mask_Designer/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Mask_Designer/'
Test_Material_Folder = app.testing_material

#Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto_MacAT/SFT/GroundTruth/Mask_Designer/'
#Auto_Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto_MacAT/SFT/ATGroundTruth/Mask_Designer/'
#Test_Material_Folder = '/Users/clt/Desktop/Ernesto_MacAT/Material/'

DELAY_TIME = 1

# @pytest.fixture(scope="module", autouse= True)
# def init():
#     yield
#     main_page.close_app()
#     report.export()
#     report.show()

class Test_Mask_Designer():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        # main_page.insert_media("Food.jpg")
        # main_page.tap_TipsArea_Tools_menu(1)
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
            google_sheet_execution_log_init('Mask_Designer')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"media room result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        with uuid("ece315e7-9169-4c6a-a0f7-0db4c20f8ebe") as case:
            # Insert Food.jpg to timeline > Enter Mask Designer
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME*4)
            # Apply template (6th)
            mask_designer_page.MaskDesigner_Apply_template(5)

            # 3.1.5 Invert Mask > Check [G103]
            SetCheck_result = mask_designer_page.Edit_MaskDesigner_Invert_mask_SetCheck(check=True)
            time.sleep(DELAY_TIME)

            image_full_path_1 = Auto_Ground_Truth_Folder+"G103_1.png"
            image_full_path_2 = Auto_Ground_Truth_Folder+"G103_2.png"
            if L.mask_designer.take_preview_pic:
                current_invert_mask = mask_designer_page.snapshot(locator=L.mask_designer.mask_property.invert_mask, file_name=image_full_path_1)
                current_preview = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=image_full_path_2)
                logger(f"{current_invert_mask=}")
                #logger(f"{current_preview=}")
                case.result = SetCheck_result
            else:
                check_invert_mask = mask_designer_page.compare(image_full_path_1, mask_designer_page.image.screenshot())
                check_preview = mask_designer_page.compare(image_full_path_2, mask_designer_page.image.screenshot())
                case.result = SetCheck_result and check_invert_mask and check_preview

        with uuid("da03e0ff-b6c8-44a9-b32a-1097c5302c48") as case:
            # 3.1.5 Invert Mask > Uncheck [G102]
            SetCheck_result = mask_designer_page.Edit_MaskDesigner_Invert_mask_SetCheck(check=False)
            time.sleep(DELAY_TIME)

            image_full_path_1 = Auto_Ground_Truth_Folder+"G102_1.png"
            image_full_path_2 = Auto_Ground_Truth_Folder+"G102_2.png"
            if L.mask_designer.take_preview_pic:
                current_invert_mask = mask_designer_page.snapshot(locator=L.mask_designer.mask_property.invert_mask, file_name=image_full_path_1)
                current_preview = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=image_full_path_2)
                logger(f"{current_invert_mask=}")
                case.result = SetCheck_result
            else:
                check_invert_mask = mask_designer_page.compare(image_full_path_1, mask_designer_page.image.screenshot())
                check_preview = mask_designer_page.compare(image_full_path_2, mask_designer_page.image.screenshot())
                case.result = SetCheck_result and check_invert_mask and check_preview

        with uuid("46e26a24-875f-419e-8f27-01e36f809104") as case:
            # 3.1.1 Category > All Mask [F85]
            time.sleep(DELAY_TIME*2)

            # not sure the locator > manually get Ground Truth Image
            logger('line102')
            mask_tab_preview = mask_designer_page.snapshot(locator=L.mask_designer.mask_designer_window, file_name=Auto_Ground_Truth_Folder+"F85_1.png")
            compare_result1 = mask_designer_page.compare(Ground_Truth_Folder+'F85_1.png', mask_tab_preview)
            logger(compare_result1)
            mask_designer_page.drag_Mask_Properties_Scroll_Bar(0.26)
            time.sleep(DELAY_TIME)
            mask_designer_page.drag_Mask_Properties_Scroll_Bar(0.52)
            time.sleep(DELAY_TIME)
            mask_designer_page.drag_Mask_Properties_Scroll_Bar(0.79)
            time.sleep(DELAY_TIME)
            mask_designer_page.drag_Mask_Properties_Scroll_Bar(1)
            time.sleep(DELAY_TIME)

            mask_tab_preview = mask_designer_page.snapshot(locator=L.mask_designer.mask_designer_window, file_name=Auto_Ground_Truth_Folder+"F85_2.png")
            compare_result2 = mask_designer_page.compare(Ground_Truth_Folder+'F85_2.png', mask_tab_preview)
            logger(compare_result1)
            logger(compare_result2)

            test_result = compare_result1 and compare_result2
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("b496fdb6-3d58-4ed5-818d-86dceca2ff78") as case:
            time.sleep(DELAY_TIME*2)
            # 3.1.6 Feather radius > Adjustment > Slider [G107]
            slider_result = mask_designer_page.Edit_MaskDesigner_Feather_radius_Slider(10)
            # Assertion Error

            # compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G107_1.png',
            #                                             mask_designer_page.image.screenshot())

            image_full_path_1 = Auto_Ground_Truth_Folder + "G107_1.png"
            image_full_path_2 = Auto_Ground_Truth_Folder + "G107_2.png"

            if L.mask_designer.take_preview_pic:
                current_slider = mask_designer_page.snapshot(locator=L.mask_designer.mask_property.feather_slider,
                                                             file_name=image_full_path_1)
                current_preview = mask_designer_page.snapshot(locator=L.mask_designer.preview_window,
                                                              file_name=image_full_path_2)
                logger(f"{current_slider=}")
                case.result = slider_result
            else:
                check_slider = mask_designer_page.compare(image_full_path_1, mask_designer_page.image.screenshot())
                check_preview = mask_designer_page.compare(image_full_path_2, mask_designer_page.image.screenshot())
                case.result = slider_result and check_slider and check_preview

        with uuid("525cf07b-bcc0-4522-8187-b6a4481065a8") as case:
            # 1.3.4 [Cancel] button > Have editing > Confirmation = No [G30]
            time.sleep(DELAY_TIME*2)
            cancel_result = mask_designer_page.Edit_MaskDesigner_ClickCancel(1)
            time.sleep(DELAY_TIME)
            #compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G30_1.png',
            #                                            mask_designer_page.image.screenshot())
            if not mask_designer_page.exist(L.mask_designer.mask_property.category):
                case.result = cancel_result
            else:
                case.result = False


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid("8398dd62-97b4-4632-afba-067dc21c7f0a") as case:
            # Insert Food.jpg to timeline track1
            main_page.insert_media("Food.jpg")
            time.sleep(DELAY_TIME*2)
            # Insert Skateboard 01.mp4 to timeline track2 > Enter Mask Designer
            main_page.timeline_select_track(2)
            time.sleep(DELAY_TIME*2)
            main_page.insert_media("Skateboard 01.mp4")
            # 3.1.1 Category > Default Mask [F86]

            # add Skateboard 01.mp4 to timeline track2
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME*3)
            mask_designer_page.MaskDesigner_Select_category(1)

            current_default_value = mask_designer_page.exist(L.mask_designer.mask_property.category).AXTitle
            if current_default_value == 'Default Masks':
                case.result = True
            else:
                case.result = False

        with uuid("ee87c82a-896a-4ba5-a3d9-b1565b220fe9") as case:
            time.sleep(DELAY_TIME)
            # Apply template (4th)
            mask_designer_page.MaskDesigner_Apply_template(3)

            # 1.2.4 Only show the selected track > Check [G18]
            SetCheck_result = mask_designer_page.Edit_MaskDesigner_Only_Show_Selected_track_SetCheck(check_it=True)
            time.sleep(DELAY_TIME)
            #compare_result = mask_designer_page.image.search(Ground_Truth_Folder + 'G18_1.png',
            #                                             mask_designer_page.image.screenshot())
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G18_1.png')
            logger(f"{current_image=}")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G18_1.png', current_image)
            #logger(SetCheck_result)# 12:01 wait check
            #logger(compare_result)
            case.result = SetCheck_result and compare_result

        with uuid("53764fd7-b0bd-4016-9d76-ce2174ddc4f1") as case:
            # 2.2 Edit > Undo > Click item [G41]
            time.sleep(DELAY_TIME*2)
            mask_designer_page.tap_MaskDesigner_Undo_btn()
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G41_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G41_1.png', current_image)
            case.result = compare_result

        with uuid("684a1418-4877-4d0f-bf79-44957743ed0f") as case:
            # 2.2 Edit > Redo > Click item [G43]
            time.sleep(DELAY_TIME)
            mask_designer_page.tap_MaskDesigner_Redo_btn()
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G43_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G43_1.png', current_image)
            case.result = compare_result

        with uuid("677a4032-ab5f-464a-8c65-26cf99524206") as case:
            time.sleep(DELAY_TIME)
            # 1.2.4 Only show the selected track > Uncheck [G17]
            SetCheck_result = mask_designer_page.Edit_MaskDesigner_Only_Show_Selected_track_SetCheck(check_it=False)
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G17_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G17_1.png', current_image)
            case.result = compare_result
            mask_designer_page.Edit_MaskDesigner_ClickCancel(0)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid("67446d24-31d3-4409-b125-e3c64ce58468") as case:
            with uuid("2c78ed2e-a770-4297-9482-32fc88ab3e5e") as case:
                # Insert Food.jpg to timeline > Enter Mask Designer
                main_page.insert_media("Food.jpg")
                main_page.tap_TipsArea_Tools_menu(1)
                time.sleep(DELAY_TIME*4)

                # 3.1.2 Category > Create a Image > Type > jpg/jpeg [G91]
                # 3.1.2 Category > Create a Image > Type > horizontal [G98]
                mask_designer_page.Edit_MaskDesigner_CreateImageMask(Test_Material_Folder + '03 image/Horizontal.jpg')

                current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G91_1.png')
                #logger(f"{current_image}")
                compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G91_1.png', current_image)
                case.result = compare_result
            case.result = compare_result

        with uuid("747083d1-bd0e-482a-a1e4-272c11be4965") as case:
            time.sleep(DELAY_TIME)

            # 3.1.2 Category > Create a Image > Type > bmp [G92]
            mask_designer_page.Edit_MaskDesigner_CreateImageMask(Test_Material_Folder+'03 image/02.bmp')

            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G92_1.png')
            #logger(f"{current_image}")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G92_1.png', current_image)
            case.result = compare_result

        with uuid("24d59902-7cb0-4bd5-9f07-6f296994dad0") as case:
            time.sleep(DELAY_TIME)

            # 3.1.2 Category > Create a Image > Type > png [G93]
            mask_designer_page.Edit_MaskDesigner_CreateImageMask(Test_Material_Folder+'03 image/03.png')
            time.sleep(DELAY_TIME*2)
            check_result = mask_designer_page.MaskDesigner_Select_Mask_Alpha_Channel()
            time.sleep(DELAY_TIME*2)

            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G93_1.png')
            #logger(f"{current_image}")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G93_1.png', current_image)
            case.result = compare_result

        with uuid("7850a36e-8fa7-4946-816c-361c18238e89") as case:
            time.sleep(DELAY_TIME*2)
            # 3.1.2 Category > Create a Image > Type > tif [G94]
            mask_designer_page.Edit_MaskDesigner_CreateImageMask(Test_Material_Folder+'03 image/04.tif')
            time.sleep(DELAY_TIME*2)

            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G94_1.png')
            # logger(f"{current_image}")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G94_1.png', current_image)
            case.result = compare_result

        with uuid("07ddbd8d-9e0d-487d-9cf8-9ba95498f357") as case:
            time.sleep(DELAY_TIME*2)
            # 3.1.2 Category > Create a Image > Type > gif [G95]
            mask_designer_page.Edit_MaskDesigner_CreateImageMask(Test_Material_Folder+'03 image/05.gif')
            time.sleep(DELAY_TIME*2)
            check_result = mask_designer_page.MaskDesigner_Select_Mask_Alpha_Channel()
            time.sleep(DELAY_TIME*4)

            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G95_1.png')
            # logger(f"{current_image}")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G95_1.png', current_image)
            case.result = check_result and compare_result

        with uuid("ef95622e-58ad-407a-9de8-6a5e7f0edf54") as case:
            time.sleep(DELAY_TIME*2)
            # 3.1.2 Category > Create a Image > Type > RAW file [G96]
            mask_designer_page.Edit_MaskDesigner_CreateImageMask(Test_Material_Folder+'03 image/05RAW.CRW')
            time.sleep(DELAY_TIME*2)
            mask_designer_page.Edit_MaskDesigner_ClickCancel(0)
            time.sleep(DELAY_TIME*2)

            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G96_1.png')
            # logger(f"{current_image}")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G96_1.png', current_image)
            case.result = compare_result

        with uuid("fbfc6f42-7f7e-4bee-a734-2396b4972912") as case:
            time.sleep(DELAY_TIME*3)
            # 3.1.2 Category > Create a Image > Type > HEIC [G97]
            mask_designer_page.Edit_MaskDesigner_CreateImageMask(Test_Material_Folder+'03 image/IMG_0751.HEIC')
            time.sleep(DELAY_TIME*2)

            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G97_1.png')
            # logger(f"{current_image}")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G97_1.png', current_image)
            case.result = compare_result

        with uuid("cf0a236b-37a2-42b2-9b57-9a000265ee73") as case:
            time.sleep(DELAY_TIME*2)
            # 3.1.2 Category > Create a Image > Type > virtical [G99]
            mask_designer_page.Edit_MaskDesigner_CreateImageMask(Test_Material_Folder+'03 image/Vertical.jpg')
            time.sleep(DELAY_TIME*2)

            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G99_1.png')
            # logger(f"{current_image}")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G99_1.png', current_image)
            case.result = compare_result
            mask_designer_page.Edit_MaskDesigner_ClickCancel(0)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid("cb1446d5-2848-498b-aadd-7e1b7e25a92b") as case:
            # Insert Food.jpg to timeline > Enter Mask Designer
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME*2)
            # 3.1.1 Category > Custom Masks > Create & Show [G87]
            mask_designer_page.MaskDesigner_Select_category(2)
            time.sleep(DELAY_TIME*2)

            current_category_value = mask_designer_page.exist(L.mask_designer.mask_property.category).AXTitle
            if current_category_value == 'Custom Masks':
                case.result = True
            else:
                case.result = False

        with uuid("4fffad84-e91a-483c-ad14-cf0fe5f3adf1") as case:
            time.sleep(DELAY_TIME*2)
            # 3.1.1 Category > Custom Masks > Remove Mask [G88]
            for x in range(8):
                remove_result = mask_designer_page.Edit_MaskDesigner_RemoveCustomMask(1)
                time.sleep(DELAY_TIME*2)
                if not remove_result:
                    case.result = False
                    break
            case.result = True


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid("135e53b9-30f7-4a9b-b95f-03f0a5aeb4e8") as case:
            # Insert Food.jpg to timeline > Enter Mask Designer
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME*4)
            # if Mask Designer exist
            if mask_designer_page.exist(L.mask_designer.mask_property.category):
                case.result = True
            else:
                case.result = False

        with uuid("bd52a163-a7a2-455d-9a11-976e6c66663e") as case:
            with uuid("3a8e0637-208b-4db7-91b9-5c779e72b7fd") as case:
                mask_designer_page.MaskDesigner_Apply_template(4)
                # Feather radius value to max 100 [G109]
                input_result = mask_designer_page.Edit_MaskDesigner_Feather_radius_InputValue(100)
                time.sleep(DELAY_TIME)
                current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G109_1.png')
                current_input = mask_designer_page.snapshot(locator=L.mask_designer.mask_property.feather_group, file_name=Auto_Ground_Truth_Folder + 'G109_2.png')
                logger(f"{current_input=}")
                compare_result1 = mask_designer_page.compare(Ground_Truth_Folder + 'G109_1.png', current_image)
                logger(compare_result1)
                compare_result2 = mask_designer_page.compare(Ground_Truth_Folder + 'G109_2.png', current_input)
                logger(compare_result2)
                case.result = compare_result1 and compare_result2

        with uuid("7b86d658-b6e5-4edc-a631-46d59f93d681") as case:
            # Feather radius value to min 0 [G110]
            input_result = mask_designer_page.Edit_MaskDesigner_Feather_radius_InputValue(0)

            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G110_1.png')
            current_value = mask_designer_page.Get_MaskDesigner_Feather_radius_CurrentValue()

            if float(current_value) == 0:
                compare_result2 = True
            else:
                compare_result2 = False

            logger(f"{current_input=}")
            compare_result1 = mask_designer_page.compare(Ground_Truth_Folder + 'G110_1.png', current_image)

            case.result = compare_result1 and compare_result2

        with uuid("0d1be6c5-1a70-4a1a-aac8-7f1756ea7be5") as case:
            # Feather radius value arrow up and down [G111]
            click_result = mask_designer_page.Edit_MaskDesigner_Feather_radius_ArrowButton("up")
            time.sleep(DELAY_TIME)
            current_value = mask_designer_page.Get_MaskDesigner_Feather_radius_CurrentValue()
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G111_1.png')
            time.sleep(DELAY_TIME)
            compare_result3 = mask_designer_page.compare(Ground_Truth_Folder + 'G111_1.png', current_image)
            logger(current_value)
            if float(current_value) == 1:
                compare_result1 = True
            else:
                compare_result1 = False

            logger(compare_result1)
            time.sleep(DELAY_TIME)
            click_result = mask_designer_page.Edit_MaskDesigner_Feather_radius_ArrowButton("down")
            time.sleep(DELAY_TIME)
            current_value = mask_designer_page.Get_MaskDesigner_Feather_radius_CurrentValue()
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G111_1.png')
            time.sleep(DELAY_TIME)
            compare_result4 = mask_designer_page.compare(Ground_Truth_Folder + 'G111_1.png', current_image)
            logger(current_value)
            if float(current_value) == 0:
                compare_result2 = True
            else:
                compare_result2 = False
            logger(compare_result2)
            case.result = compare_result1 and compare_result2 and compare_result3 and compare_result4

        with uuid("34f68801-bdac-4775-ab7d-fdd599a19e51") as case:
            with uuid("161250ac-e451-41fd-80de-1a8f12d4631c") as case:
                # check the default position X and Y
                current_value_x = mask_designer_page.Get_MaskDesigner_ObjectSetting_PositionX_Value()
                current_value_y = mask_designer_page.Get_MaskDesigner_ObjectSetting_PositionY_Value()

                if float(current_value_x) == 0.500:
                    compare_result_x = True
                else:
                    compare_result_x = False

                if float(current_value_y) == 0.500:
                    compare_result_y = True
                else:
                    compare_result_y = False
                case.result = compare_result_x and compare_result_y

        with uuid("ba6ad4f8-9184-4335-b8f4-bb0e9996f4cc") as case:
            with uuid("7d8f4ab5-068d-48ce-9750-54ed61de2cea") as case:
                # position X set to min -10 by input [G112]
                mask_designer_page.drag_Mask_Settings_Scroll_Bar(0.5)
                input_result_x = mask_designer_page.object_settings.set_position_x(-10)
                time.sleep(DELAY_TIME)
                current_value_x = mask_designer_page.Get_MaskDesigner_ObjectSetting_PositionX_Value()
                logger(current_value_x)
                if float(current_value_x) == -10:
                    compare_result_x = True
                else:
                    compare_result_x = False
                current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G112_1.png')
                time.sleep(DELAY_TIME)
                compare_result_image = mask_designer_page.compare(Ground_Truth_Folder + 'G112_1.png', current_image)

                case.result = compare_result_x and compare_result_image

        with uuid("2dfb63f8-f5ee-4771-ad31-c5f869434410") as case:
            # position X set to max 10 [G114]
            input_result_x = mask_designer_page.object_settings.set_position_x(10)
            time.sleep(DELAY_TIME)
            current_value_x = mask_designer_page.Get_MaskDesigner_ObjectSetting_PositionX_Value()
            logger(current_value_x)
            if float(current_value_x) == 10:
                compare_result_x = True
            else:
                compare_result_x = False
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G114_1.png')
            time.sleep(DELAY_TIME)
            compare_result_image = mask_designer_page.compare(Ground_Truth_Folder + 'G114_1.png', current_image)

            case.result = compare_result_x and compare_result_image

        with uuid("074170ce-f765-439d-b041-c6001c847e03") as case:
            # click cancel then Yes [G116]
            time.sleep(DELAY_TIME * 2)
            cancel_result = mask_designer_page.Edit_MaskDesigner_ClickCancel(0)
            time.sleep(DELAY_TIME)
            # compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G116_1.png',
            #                                            mask_designer_page.image.screenshot())
            if not mask_designer_page.exist(L.mask_designer.mask_property.category):
                case.result = cancel_result
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid("3937d423-1a03-4181-acb9-0233e4449d94") as case:
            # Insert Skateboard 01.mp4 to timeline > Enter Mask Designer
            main_page.insert_media("Skateboard 01.mp4")
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 4)
            # if Mask Designer exist
            if mask_designer_page.exist(L.mask_designer.mask_property.category):
                case.result = True
            else:
                case.result = False

        with uuid("f7649a17-ee69-4bc2-8ed0-02cb1374b08c") as case:
            # check if default feather was 0
            mask_designer_page.MaskDesigner_Apply_template(5)
            current_value = mask_designer_page.Get_MaskDesigner_Feather_radius_CurrentValue()
            if float(current_value) == 0:
                case.result = True
            else:
                case.result = False

        with uuid("7a1cd758-6fc2-4334-bdbd-6d7a65adb864") as case:
            with uuid("b809ebb7-f6f5-46ba-a19f-f211125cd5b3") as case:
                # position Y set to min -10 by input [G113]

                mask_designer_page.drag_Mask_Settings_Scroll_Bar(0.5)
                time.sleep(DELAY_TIME)
                input_result_y = mask_designer_page.object_settings.set_position_y(-10)
                time.sleep(DELAY_TIME)
                current_value_y = mask_designer_page.Get_MaskDesigner_ObjectSetting_PositionX_Value()
                if float(current_value_y) == -10.000:
                    compare_result_y = True
                else:
                    compare_result_y = False
                current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G113_1.png')
                time.sleep(DELAY_TIME)
                compare_result_image = mask_designer_page.compare(Ground_Truth_Folder + 'G113_1.png', current_image)

                case.result = compare_result_image

        with uuid("d1e31f95-bc4e-4a28-855c-2f0f1560f602") as case:
            # position Y set to max 10 [G115]
            input_result_x = mask_designer_page.object_settings.set_position_y(10)
            time.sleep(DELAY_TIME)
            current_value_y = mask_designer_page.Get_MaskDesigner_ObjectSetting_PositionY_Value()
            if float(current_value_y) == 10.000:
                compare_result_y = True
            else:
                compare_result_y = False
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G115_1.png')
            time.sleep(DELAY_TIME)
            compare_result_image = mask_designer_page.compare(Ground_Truth_Folder + 'G115_1.png', current_image)

            case.result = compare_result_y and compare_result_image

        with uuid("074170ce-f765-439d-b041-c6001c847e03") as case:
            # click cancel then Cancel [G117]
            time.sleep(DELAY_TIME * 2)
            cancel_result = mask_designer_page.Edit_MaskDesigner_ClickCancel(2)
            time.sleep(DELAY_TIME)
            # compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G117_1.png',
            #                                            mask_designer_page.image.screenshot())
            if mask_designer_page.exist(L.mask_designer.mask_property.category):
                case.result = cancel_result
            else:
                case.result = False

        with uuid("e27f487e-f1ab-4e0c-a148-019112b1a651") as case:
            # use arrow to adjust position X [G118]
            time.sleep(DELAY_TIME * 2)
            click_result1 = mask_designer_page.object_settings.click_position_x_arrow("up")
            time.sleep(DELAY_TIME)
            current_value1 = mask_designer_page.Get_MaskDesigner_ObjectSetting_PositionX_Value()
            time.sleep(DELAY_TIME)
            if float(current_value1) == 0.501:
                click_result3 = click_result1
            else:
                click_result3 = False

            current_image1 = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G118_1.png')
            time.sleep(DELAY_TIME)
            compare_result1 = mask_designer_page.compare(Ground_Truth_Folder + 'G118_1.png', current_image1)

            click_result2 = mask_designer_page.object_settings.click_position_x_arrow("down")
            time.sleep(DELAY_TIME)
            current_value2 = mask_designer_page.Get_MaskDesigner_ObjectSetting_PositionX_Value()
            time.sleep(DELAY_TIME)
            if float(current_value2) == 0.500:
                click_result4 = click_result2
            else:
                click_result4 = False

            current_image2 = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G118_2.png')
            time.sleep(DELAY_TIME)
            compare_result2 = mask_designer_page.compare(Ground_Truth_Folder + 'G118_2.png', current_image2)
            case.result = compare_result1 and click_result3 and compare_result2 and click_result4

        with uuid("fee1c1bc-e102-4ec9-98f6-d8dabac87f43") as case:
            # use arrow to adjust position Y [G119]
            time.sleep(DELAY_TIME * 2)
            click_result1 = mask_designer_page.object_settings.click_position_y_arrow("down")
            time.sleep(DELAY_TIME)
            current_value1 = mask_designer_page.Get_MaskDesigner_ObjectSetting_PositionY_Value()
            time.sleep(DELAY_TIME)
            if float(current_value1) == 9.999:
                click_result3 = click_result1
            else:
                click_result3 = False

            current_image1 = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G119_1.png')
            time.sleep(DELAY_TIME)
            compare_result1 = mask_designer_page.compare(Ground_Truth_Folder + 'G119_1.png', current_image1)

            click_result2 = mask_designer_page.object_settings.click_position_y_arrow("up")
            time.sleep(DELAY_TIME)
            current_value2 = mask_designer_page.Get_MaskDesigner_ObjectSetting_PositionY_Value()
            time.sleep(DELAY_TIME)
            if float(current_value2) == 10.000:
                click_result4 = click_result2
            else:
                click_result4 = False

            current_image2 = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G119_2.png')
            time.sleep(DELAY_TIME)
            compare_result2 = mask_designer_page.compare(Ground_Truth_Folder + 'G119_2.png', current_image2)
            mask_designer_page.Edit_MaskDesigner_ClickCancel(0)
            case.result = compare_result1 and compare_result2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        with uuid("7af094f8-fa04-4acc-a4c8-5dd8ba3707cb") as case:
            # Insert Food.jpg to timeline > Enter Mask Designer
            # Enter then close without editing
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 4)
            cancel_result = mask_designer_page.Edit_MaskDesigner_ClickCancel(None)
            time.sleep(DELAY_TIME * 2)
            if not mask_designer_page.exist(L.mask_designer.mask_property.category):
                case.result = cancel_result
            else:
                case.result = False

        with uuid("7c0230b5-c5d4-4fc9-ad18-7b400a773b55") as case:
            # Enter Masdk Designer
            # Check default Scale Width
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 2)
            mask_designer_page.MaskDesigner_Apply_template(6)
            mask_designer_page.drag_Mask_Settings_Scroll_Bar(0.5)
            time.sleep(DELAY_TIME * 2)

            current_result = mask_designer_page.Get_MaskDesigner_ObjectSetting_ScaleWidth_Value()
            logger(current_result)
            time.sleep(DELAY_TIME)
            if float(current_result) == 0.750:
                case.result = True
            else:
                case.result = False


        with uuid("498841ce-7d61-4de7-b4ca-deb16c40ab55") as case:
            # Enter Masdk Designer
            # Check default Scale Height

            time.sleep(DELAY_TIME * 4)
            current_result = mask_designer_page.Get_MaskDesigner_ObjectSetting_ScaleHigh_Value()
            time.sleep(DELAY_TIME)
            if float(current_result) == 1:
                case.result = True
            else:
                case.result = False

        with uuid("85bc16a5-4e33-4646-9f10-188cbab4ccc5") as case:
            with uuid("3ce5230f-4cc3-45d8-823d-c77ca83fc8d9") as case:
                # Enter Masdk Designer
                # Set Scale Width to min by slider [G120]
                time.sleep(DELAY_TIME * 4)
                current_result = mask_designer_page.object_settings.set_scale_width_slider(0.001)
                time.sleep(DELAY_TIME)
                current_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_ScaleWidth_Value()
                if float(current_value) == 0.001:
                    slider_result = True
                else:
                    slider_result = False
                current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G120_1.png')
                image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G120_1.png', current_image)
                case.result = slider_result and image_result

        with uuid("07562b0e-aa75-4c00-8652-7da2475f6a8c") as case:
            # Set Scale Width adjust by arrow [G121]
            time.sleep(DELAY_TIME * 4)
            current_result = mask_designer_page.object_settings.click_scale_width_arrow("up")
            time.sleep(DELAY_TIME)
            current_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_ScaleWidth_Value()
            if float(current_value) == 0.002:
                arrow_result = current_result
            else:
                arrow_result = False
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G121_1.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G121_1.png', current_image)
            case.result = arrow_result and image_result


        with uuid("26451639-c862-4146-ae99-520af0f1db84") as case:
            with uuid("cc32993c-3b01-438c-8030-9ace2f26889d") as case:
                with uuid("9a685e23-adc2-4d77-9b65-6bcadd0b8cd4") as case:
                    # Set Scale Width to min by input value with Maintain aspect ratio unchecked[G122]
                    time.sleep(DELAY_TIME * 4)
                    check_result = mask_designer_page.object_settings.set_scale_ratio(False)
                    time.sleep(DELAY_TIME)
                    current_result = mask_designer_page.object_settings.set_scale_width(6)
                    time.sleep(DELAY_TIME)
                    current_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_ScaleWidth_Value()
                    if float(current_value) == 6.000:
                        slider_result = True
                    else:
                        slider_result = False
                    current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G122_1.png')
                    image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G122_1.png', current_image)
                    case.result = slider_result and image_result


        with uuid("fa602976-1ebf-4a19-9638-ba9d70ce02d4") as case:
            with uuid("89414f33-53d9-499e-a073-0915ad34da28") as case:
                with uuid("1641e543-5781-4920-aef8-9fe4e8c3b7c7") as case:
                    # Set Maintain aspect ratio checked and set Scale height to max 6 by value[G123]
                    time.sleep(DELAY_TIME * 4)
                    check_result = mask_designer_page.object_settings.set_scale_ratio(True)
                    time.sleep(DELAY_TIME)
                    current_result = mask_designer_page.object_settings.set_scale_height(6)
                    current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G123_1.png')
                    image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G123_1.png', current_image)
                    case.result = current_result and image_result
                    mask_designer_page.Edit_MaskDesigner_ClickCancel(0)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        with uuid("eee71231-bfb7-46eb-8f4f-34091e92a138") as case:
            # put Food.jpg to timeline -> Enter Mask Designer
            # click X button to exit
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 4)
            current_result = mask_designer_page.Edit_MaskDesigner_CloseWindow()
            time.sleep(DELAY_TIME)
            if not mask_designer_page.exist(L.mask_designer.mask_property.category):
                case.result = current_result
            else:
                case.result = False

        with uuid("d7df1a19-1638-49bf-8850-c83bf0b438c0") as case:
            # put Food.jpg to timeline -> Enter Mask Designer
            # click maximize window then restore [G124]
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 4)
            current_result1 = mask_designer_page.Edit_MaskDesigner_ClickFullScreen()
            time.sleep(DELAY_TIME)
            current_image1 = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G124_1.png')
            image_result1 = mask_designer_page.compare(Ground_Truth_Folder + 'G124_1.png', current_image1)
            current_result2 = mask_designer_page.Edit_MaskDesigner_ClickRestoreScreen()
            current_image2 = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G124_2.png')
            image_result2 = mask_designer_page.compare(Ground_Truth_Folder + 'G124_2.png', current_image2)
            case.result = image_result1 and image_result2

        with uuid("f53ece9b-f827-4568-aac1-c367581f6259") as case:
            with uuid("0a62aa70-dd1f-4103-80d4-8a1aa5013849") as case:
                # adjust Scale height to min 0.001 by slider [G125]
                time.sleep(DELAY_TIME * 4)
                mask_designer_page.MaskDesigner_Apply_template(2)
                mask_designer_page.drag_Mask_Settings_Scroll_Bar(0.75)
                slider_value = mask_designer_page.object_settings.set_scale_height_slider(0.001)
                time.sleep(DELAY_TIME)
                current_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_ScaleHigh_Value()
                if float(current_value) == 0.001:
                    slider_result = True
                else:
                    slider_result = False

                current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G125_1.png')
                image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G125_1.png', current_image)
                case.result = slider_result and image_result

        with uuid("003bf704-bccc-407c-b4c4-5e4114f6331f") as case:
            # adjust Scale height by arrow [G126]
            time.sleep(DELAY_TIME * 4)
            arrow_result = mask_designer_page.object_settings.click_scale_height_arrow("up")
            time.sleep(DELAY_TIME)
            current_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_ScaleHigh_Value()
            if float(current_value) == 0.002:
                current_result = arrow_result
            else:
                current_result = False

            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G126_1.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G126_1.png', current_image)
            case.result = current_result and image_result

        with uuid("d38822e4-aab2-45ca-8d17-ec0f74c28359") as case:
            # check opacity default value
            time.sleep(DELAY_TIME * 4)
            current_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_Opacity_Value()
            if current_value == '100%':
                case.result = True
            else:
                case.result = False
            mask_designer_page.Edit_MaskDesigner_ClickCancel(0)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        with uuid("829fa749-22df-474e-b01e-d8c2685d7d79") as case:
            with uuid("829fa749-22df-474e-b01e-d8c2685d7d79") as case:
                # put Food.jpg to timeline -> Enter Mask Designer
                # adjust Opacity to 0 by slider [G127]
                main_page.insert_media("Food.jpg")
                main_page.tap_TipsArea_Tools_menu(1)
                time.sleep(DELAY_TIME * 4)
                mask_designer_page.MaskDesigner_Apply_template(6)
                mask_designer_page.drag_Mask_Settings_Scroll_Bar(0.80)
                slider_value = mask_designer_page.object_settings.set_opacity_slider(0)
                time.sleep(DELAY_TIME)
                current_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_Opacity_Value()
                if current_value == '0%':
                    slider_result = slider_value
                else:
                    slider_result = False
                current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G127_1.png')
                image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G127_1.png', current_image)
                case.result = slider_result and image_result

        with uuid("2aa5fa6c-ec60-409b-9334-4a655f26798d") as case:
            # adjust opacity by arrow [G128]
            time.sleep(DELAY_TIME * 4)
            arrow_value = mask_designer_page.object_settings.click_opacity_arrow("up")
            current_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_Opacity_Value()
            if current_value == '1%':
                arrow_result = arrow_value
            else:
                arrow_result = False

            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G128_1.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G128_1.png', current_image)
            case.result = arrow_result and image_result


        with uuid("219655b0-8da8-48bc-b73e-a5cf738d775b") as case:
            with uuid("bd920535-7edd-4b06-80f0-2d67ec85dfc4") as case:
                # adjust Opacity to max 100 by value [G129]
                time.sleep(DELAY_TIME * 4)
                input_value = mask_designer_page.object_settings.set_opacity(100)
                time.sleep(DELAY_TIME)
                current_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_Opacity_Value()
                if current_value == '100%':
                    input_result = input_value
                else:
                    input_result = False
                current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G129_1.png')
                image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G129_1.png', current_image)
                case.result = input_result and image_result

        with uuid("53de95a7-5aa0-4ab6-85f2-50de12de747b") as case:
            # check rotation default
            time.sleep(DELAY_TIME * 4)
            current_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_Rotation_Value()
            if float(current_value) == 0.00:
                case.result = True
            else:
                case.result = False
            mask_designer_page.Edit_MaskDesigner_ClickCancel(0)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_10(self):
        with uuid("a2f4f64a-e4ef-40a0-8216-975010852a85") as case:
            with uuid("ecb38f57-0b8d-4a06-81d8-b755f7f66e4c") as case:
                # insert Food.jpg to timeline -> Enter Mask Designer
                # adjust rotation to min -9999 by input [G130]
                main_page.insert_media("Food.jpg")
                main_page.tap_TipsArea_Tools_menu(1)
                time.sleep(DELAY_TIME * 4)
                mask_designer_page.MaskDesigner_Apply_template(1)
                mask_designer_page.drag_Mask_Settings_Scroll_Bar(0.90)
                input_result = mask_designer_page.object_settings.set_rotation(-9999)
                input_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_Rotation_Value()
                if input_value == -9999.00:
                    current_result = input_result
                else:
                    current_result = False
                current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G130_1.png')
                image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G130_1.png', current_image)
                case.result = image_result

        with uuid("4c352be6-ff7d-4209-9d45-7aa3ef617fd3") as case:
            # adjust rotation to max 9999 by input [G131]
            time.sleep(DELAY_TIME * 4)
            input_result = mask_designer_page.object_settings.set_rotation(9999)
            input_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_Rotation_Value()
            if input_value == 9999.00:
                current_result = input_result
            else:
                current_result = False
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G131_1.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G131_1.png', current_image)
            case.result = image_result


        with uuid("39e19a60-41d7-48d4-b2a3-41c6e3a2a062") as case:
            # adjust rotation by arrow [G132]
            time.sleep(DELAY_TIME * 4)
            arrow_result = mask_designer_page.object_settings.click_rotation_arrow("down")
            arrow_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_Rotation_Value()
            if arrow_value == 9998.99:
                current_result = arrow_result
            else:
                current_result = False
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G132_1.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G132_1.png', current_image)
            case.result = image_result

        with uuid("4a3f91e1-a4e9-475d-9c4e-733b8bea66ce") as case:
            # View Undo [G136]
            time.sleep(DELAY_TIME * 2)
            mask_designer_page.tap_MaskDesigner_Undo_btn()
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G136_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G136_1.png', current_image)
            case.result = compare_result

        with uuid("b831def1-f296-4c8a-9e84-1099941c02b8") as case:
            # View Redo [G137]
            time.sleep(DELAY_TIME * 2)
            mask_designer_page.tap_MaskDesigner_Redo_btn()
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G137_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G137_1.png', current_image)
            case.result = compare_result

        with uuid("dbc57333-af91-4530-92cb-275d8570dbd2") as case:
            # Click OK [G133]
            time.sleep(DELAY_TIME * 4)
            mask_designer_page.Edit_MaskDesigner_ClickOK()
            time.sleep(DELAY_TIME)
            if not mask_designer_page.exist(L.mask_designer.mask_property.category):
                current_result = True
            else:
                current_result = False
            time.sleep(DELAY_TIME)
            timelinepreview_img = mask_designer_page.snapshot(locator=mask_designer_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'G133_1.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G133_1.png', timelinepreview_img)
            logger(f"{timelinepreview_img=}")
            case.result = current_result and image_result

        with uuid("dd29424c-8abe-4540-9dad-46a3eac9c398") as case:
            # Modify timeline clip Tools -> Mask Designer [G134]
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 4)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G134_1.png')
            case.result = mask_designer_page.compare(Ground_Truth_Folder + 'G134_1.png', current_image)

        with uuid("8485df90-3055-4afd-8379-d99301db814e") as case:
            # Click OK [G135]
            time.sleep(DELAY_TIME * 4)
            mask_designer_page.Edit_MaskDesigner_ClickOK()
            time.sleep(DELAY_TIME)
            if not mask_designer_page.exist(L.mask_designer.mask_property.category):
                current_result = True
            else:
                current_result = False
            time.sleep(DELAY_TIME)
            timelinepreview_img = mask_designer_page.snapshot(locator=mask_designer_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'G135_1.png')
            image_result = mask_designer_page.compare(Ground_Truth_Folder + 'G135_1.png', timelinepreview_img)
            logger(f"{timelinepreview_img=}")
            case.result = current_result and image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_11(self):
        with uuid("6c0888f1-1470-43b5-b123-61b5811ec80a") as case:
            # insert Skateboard 01.mp4 to timeline -> Enter Mask Designer
            # Click Zoom In canvas [G138]
            main_page.insert_media("Skateboard 01.mp4")
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 4)
            mask_designer_page.MaskDesigner_Apply_template(1)
            time.sleep(DELAY_TIME)
            current_result = mask_designer_page.Edit_MaskDesigner_ClickZoomIn()
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G138_1.png')
            logger(f"{current_image=}")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G138_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("f2b70983-a8d0-4502-bce3-98ec7ceb86e8") as case:
            # Click Zoom Out canvas [G139]
            time.sleep(DELAY_TIME * 4)
            current_result = mask_designer_page.Edit_MaskDesigner_ClickZoomOut()
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G139_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G139_1.png', current_image)
            case.result = current_result and compare_result


        with uuid("bb250fe1-f77a-46b4-976d-6f0ace6abeec") as case:
            # Set Viewer to Fit [G140]
            time.sleep(DELAY_TIME * 4)
            current_result = mask_designer_page.Viewer_Zoom_dropdown_menu("Fit")
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G140_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G140_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("d579f62f-26a4-4cbb-9ab2-210d5e9e187a") as case:
            # Set Viewer to 10% [G141]
            time.sleep(DELAY_TIME * 4)
            current_result = mask_designer_page.Viewer_Zoom_dropdown_menu("10%")
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G141_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G141_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("d2947068-fc2d-4740-934f-66a9817c223d") as case:
            # Set Viewer to 25% [G142]
            time.sleep(DELAY_TIME * 4)
            current_result = mask_designer_page.Viewer_Zoom_dropdown_menu("25%")
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G142_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G142_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("5f503224-a4aa-4f0c-9dcb-61d1f1143e43") as case:
            # Set Viewer to 50% [G143]
            time.sleep(DELAY_TIME * 4)
            current_result = mask_designer_page.Viewer_Zoom_dropdown_menu("50%")
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G143_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G143_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("6281b525-b575-4ab7-bf39-4d6026b1b2c4") as case:
            # Set Viewer to 75% [G144]
            time.sleep(DELAY_TIME * 4)
            current_result = mask_designer_page.Viewer_Zoom_dropdown_menu("75%")
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G144_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G144_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("c8220955-0f95-42bd-b9fe-58b70fe6408f") as case:
            # Set Viewer to 100% [G145]
            time.sleep(DELAY_TIME * 4)
            current_result = mask_designer_page.Viewer_Zoom_dropdown_menu("100%")
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G145_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G145_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("f9017b2d-c799-421a-9fc4-7779ae5cfd8e") as case:
            # Set Viewer to 200% [G146]
            time.sleep(DELAY_TIME * 4)
            current_result = mask_designer_page.Viewer_Zoom_dropdown_menu("200%")
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G146_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G146_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("4b4756b7-03c8-4212-81a0-5fd84c57957b") as case:
            # Set Viewer to 300% [G147]
            time.sleep(DELAY_TIME * 4)
            current_result = mask_designer_page.Viewer_Zoom_dropdown_menu("300%")
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G147_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G147_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("59c1debe-5ca6-43ce-8cde-6e3b1843b86d") as case:
            # Set Viewer to 400% [G148]
            time.sleep(DELAY_TIME * 4)
            current_result = mask_designer_page.Viewer_Zoom_dropdown_menu("400%")
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G148_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G148_1.png', current_image)
            case.result = current_result and compare_result
            mask_designer_page.Edit_MaskDesigner_ClickCancel(0)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_12(self):
        with uuid("171ad8c3-5d14-4a10-b723-ea644822ffc3") as case:
            # Play [G149]
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 4)
            mask_designer_page.MaskDesigner_Apply_template(7)
            time.sleep(DELAY_TIME)
            current_result = mask_designer_page.Edit_MaskDesigner_PreviewOperation("play")
            time.sleep(DELAY_TIME)
            #current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview.pause, file_name=Auto_Ground_Truth_Folder + 'G149_1.png')
            #logger(current_image)
            #compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G149_1.png', current_image)
            case.result = current_result


        with uuid("386cd35f-cdf2-40f3-8938-82e6af44127e") as case:
            # Stop [G150]
            current_result = mask_designer_page.Edit_MaskDesigner_PreviewOperation("stop")
            time.sleep(DELAY_TIME)
            current_image1 = mask_designer_page.snapshot(locator=L.mask_designer.preview.stop, file_name=Auto_Ground_Truth_Folder + 'G150_1.png')
            logger(current_image1)
            compare_result1 = mask_designer_page.compare(Ground_Truth_Folder + 'G150_1.png', current_image1)
            current_image2 = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G150_2.png')
            compare_result2 = mask_designer_page.compare(Ground_Truth_Folder + 'G150_2.png', current_image2)
            case.result = current_result and compare_result1 and compare_result2

        with uuid("46aac7a0-f635-4634-8728-b185a3b46795") as case:
            # Next frame [G151]
            current_result = mask_designer_page.Edit_MaskDesigner_PreviewOperation("next_frame")
            time.sleep(DELAY_TIME)

            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G151_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G151_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("793435f6-fd89-4e58-a3e7-550c88469315") as case:
            # Previous frame [G152]
            current_result = mask_designer_page.Edit_MaskDesigner_PreviewOperation("previous_frame")
            time.sleep(DELAY_TIME)

            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G152_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G152_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("bcb99764-9c6f-4441-9bd6-805fa95cee44") as case:
            # Fast forward [G153]
            current_result = mask_designer_page.Edit_MaskDesigner_PreviewOperation("fast_forward")
            time.sleep(DELAY_TIME)

            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G153_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G153_1.png', current_image)
            case.result = current_result and compare_result
            mask_designer_page.Edit_MaskDesigner_PreviewOperation("stop")

        with uuid("b382ae27-732e-4291-b10e-12080fad311b") as case:
            with uuid("1d3cf955-25d1-4828-84e3-d638d58da4a8") as case:
                # input timecode [G154]
                current_result = mask_designer_page.set_MaskDesigner_timecode("00_00_02_00")
                time.sleep(DELAY_TIME)
                current_image1 = mask_designer_page.snapshot(locator=L.mask_designer.timecode, file_name=Auto_Ground_Truth_Folder + 'G154_1.png')
                compare_result1 = mask_designer_page.compare(Ground_Truth_Folder + 'G154_1.png', current_image1)
                current_image2 = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G154_2.png')
                compare_result2 = mask_designer_page.compare(Ground_Truth_Folder + 'G154_2.png', current_image2)
                case.result = compare_result1 and compare_result2
                mask_designer_page.Edit_MaskDesigner_ClickCancel(0)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_13(self):
        with uuid("f5dccc0d-d9f6-4659-8c92-4516b60f9bdc") as case:
            # untick snap
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME)
            case.result = mask_designer_page.set_snap_ref_line(False)

        with uuid("6a56e262-84bd-4066-897e-6010912ca561") as case:
            # tick snap
            time.sleep(DELAY_TIME)
            case.result = mask_designer_page.set_snap_ref_line(True)

        with uuid("cd0a22d3-89a2-447e-a47e-d087e0d7fab0") as case:
            # set grid line 10x10 [G155]
            time.sleep(DELAY_TIME)
            current_result = mask_designer_page.set_grid_line(9)
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G155_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G155_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("85ea6332-73b0-4948-91c6-20d820b7f605") as case:
            # set grid line 9x9 [G156]
            time.sleep(DELAY_TIME)
            current_result = mask_designer_page.set_grid_line(8)
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G156_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G156_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("6772923c-b5e6-4ba4-b486-cf9fd39a8d6a") as case:
            # set grid line 8x8 [G157]
            time.sleep(DELAY_TIME)
            current_result = mask_designer_page.set_grid_line(7)
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G157_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G157_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("a04679ef-a49e-43dc-a20b-9f89f8f15a10") as case:
            # set grid line 7x7 [G158]
            time.sleep(DELAY_TIME)
            current_result = mask_designer_page.set_grid_line(6)
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G158_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G158_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("f9d8deb1-9d8d-4c22-8b0c-bf75978b908e") as case:
            # set grid line 6x6 [G159]
            time.sleep(DELAY_TIME)
            current_result = mask_designer_page.set_grid_line(5)
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G159_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G159_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("aad55216-13a3-436e-a888-7b8d7427c32c") as case:
            # set grid line 5x5 [G160]
            time.sleep(DELAY_TIME)
            current_result = mask_designer_page.set_grid_line(4)
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G160_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G160_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("ec10d263-c13c-4de3-b960-abb88978dd6e") as case:
            # set grid line 4x4 [G161]
            time.sleep(DELAY_TIME)
            current_result = mask_designer_page.set_grid_line(3)
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G161_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G161_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("9913e387-040d-4f97-8875-c5fcae1f4ab0") as case:
            # set grid line 3x3 [G162]
            time.sleep(DELAY_TIME)
            current_result = mask_designer_page.set_grid_line(2)
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G162_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G162_1.png', current_image)
            case.result = current_result and compare_result

        with uuid("523a0d4d-723b-4790-a788-26998b6dfb60") as case:
            # set grid line 2x2 [G163]
            time.sleep(DELAY_TIME)
            current_result = mask_designer_page.set_grid_line(1)
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G163_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G163_1.png', current_image)
            case.result = current_result and compare_result


        with uuid("65b38d0c-159f-421c-b2aa-30415f4c5d4a") as case:
            # set grid line None [G164]
            time.sleep(DELAY_TIME)
            current_result = mask_designer_page.set_grid_line(0)
            time.sleep(DELAY_TIME)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G164_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G164_1.png', current_image)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_14(self):
        with uuid("e94e2278-2629-4a6f-9c2c-4886309666e5") as case:
            # Undo by hotkey [G165]
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME)
            mask_designer_page.MaskDesigner_Apply_template(9)
            time.sleep(DELAY_TIME)
            mask_designer_page.object_settings.set_opacity(70)
            time.sleep(DELAY_TIME)
            with mask_designer_page.keyboard.pressed(mask_designer_page.keyboard.key.cmd, "z"): pass

            time.sleep(DELAY_TIME * 4)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G165_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G165_1.png', current_image)
            case.result = compare_result

        with uuid("1c2053f9-2521-4eb9-9710-0b8e60c2272a") as case:
            # Redo by hotkey [G166]

            time.sleep(DELAY_TIME)
            with mask_designer_page.keyboard.pressed(mask_designer_page.keyboard.key.cmd,mask_designer_page.keyboard.key.shift, "z"): pass

            time.sleep(DELAY_TIME * 4)
            current_image = mask_designer_page.snapshot(locator=L.mask_designer.preview_window, file_name=Auto_Ground_Truth_Folder + 'G166_1.png')
            compare_result = mask_designer_page.compare(Ground_Truth_Folder + 'G166_1.png', current_image)
            case.result = compare_result

        with uuid("9826664a-223a-4474-ba4c-0b143b2a7f85") as case:
            # Save As then Cancel
            time.sleep(DELAY_TIME)
            current_result1 = mask_designer_page.Edit_MaskDesigner_ClickSaveAs()
            time.sleep(DELAY_TIME)
            current_result2 = mask_designer_page.save_as.click_cancel()
            case.result = current_result1 and current_result2

        with uuid("f9bd121f-748c-43c1-bd90-710942327856") as case:
            # Save As then OK
            time.sleep(DELAY_TIME)
            current_result1 = mask_designer_page.Edit_MaskDesigner_ClickSaveAs()
            time.sleep(DELAY_TIME)
            current_result2 = mask_designer_page.save_as.input_name("1a")
            time.sleep(DELAY_TIME)
            current_result3 = mask_designer_page.save_as.click_ok
            case.result = current_result1 and current_result2 and current_result3
            #mask_designer_page.Edit_MaskDesigner_ClickCancel(0)

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    f9bd121f-748c-43c1-bd90-710942327856
                    30cdb620-bf91-46fb-9026-321a0adccc3f
                    07daa8c1-8fac-42b5-92f5-d69ec300531c
                    b2262ca9-e74c-4c92-9608-da9ffb649858
                    b7f64226-6cef-4a9c-b03f-9874ea9d1dfe
                ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"
