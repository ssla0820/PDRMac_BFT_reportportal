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
base_page = PageFactory().get_page_object('base_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page', mac)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mac)
playback_window_page = PageFactory().get_page_object('playback_window_page', mac)
precut_page = PageFactory().get_page_object('precut_page', mac)
tips_area_page = PageFactory().get_page_object('tips_area_page', mac)
library_preview_page = PageFactory().get_page_object('library_preview_page', mac)
title_designer_page = PageFactory().get_page_object('title_designer_page', mac)

# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Motion Graphics Title_v2.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
#Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/GroundTruth/Pre_Cut/'
#Auto_Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/ATGroundTruth/Pre_Cut/'
#Test_Material_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/'
Ground_Truth_Folder = app.ground_truth_root + '/Motion_graphics/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Motion_graphics/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Motion_Graphics():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME*4)
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
            google_sheet_execution_log_init('Motion_graphics')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"Motion Graphics result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        with uuid("ebb3f6df-ec29-4206-aa00-3a2015d622bc") as case:
            # [H62] Play or pause the preview
            main_page.enter_room(1)
            main_page.select_library_icon_view_media('Motion Graphics 001')
            main_page.tips_area_insert_media_to_selected_track()
            tips_area_page.click_TipsArea_btn_Designer("Title")
            time.sleep(2)
            main_page.press_enter_key()
            if title_designer_page.click_preview_operation("Play") == True:
                check1 = True
            else:
                check1 = False
            time.sleep(1)
            if title_designer_page.click_preview_operation("Pause") == True:
                check2 = True
            else:
                check2 = False
            case.result = check1 and check2

        with uuid("65bb20fb-967e-4409-b3b1-570113f68ddf") as case:
            # [H64] Go to previous frame
            if title_designer_page.click_preview_operation("Previous_Frame") == True:
                check2 = True
            else:
                check2 = False
            case.result = check2

        with uuid("3943bf43-d1f0-45da-8be7-767372386dc0") as case:
            # [H65] Go to next frame
            if title_designer_page.click_preview_operation("Next_Frame") == True:
                check2 = True
            else:
                check2 = False
            case.result = check2

        with uuid("5cc0780f-08e3-4287-91d7-c5e9bf8d501d") as case:
            # [H66] Fast forward preview (2x,4x,8x,16x)
            if title_designer_page.click_preview_operation("Fast_Forward") == True:
                check2 = True
            else:
                check2 = False
            case.result = check2

        with uuid("5b6dce0c-bc6c-4f46-80d2-faf158f82385") as case:
            # [H63] Stop preview
            if title_designer_page.click_preview_operation("Stop") == True:
                check2 = True
            else:
                check2 = False
            case.result = check2

        with uuid("95cdd00b-58e5-4ae1-8c90-e255210ea350") as case:
            # [H67] Display correct timecode
            if main_page.exist(locator=L.title_designer.area.timecode).AXValue == '00;00;00;00':
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid("2b79fdac-ee86-4469-ac45-a5a58a99126b") as case:
            # [H69] Select different title track correctly
            main_page.enter_room(1)
            main_page.select_library_icon_view_media('Motion Graphics 001')
            main_page.tips_area_insert_media_to_selected_track()
            tips_area_page.click_TipsArea_btn_Designer("Title")
            time.sleep(2)
            main_page.press_enter_key()
            main_page.exist_click(L.title_designer.title.btn_title)
            if title_designer_page.mgt.select_title_track("PowerDirector") == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("234fe143-1663-4f24-b6e3-e676b68007d5") as case:
            # [H78] Select font from dropdown menu
            if title_designer_page.mgt.apply_font_type("Arial") == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("531d0668-5015-41e4-a8cb-7ddc0a258d94") as case:
            # [H79] Set font bold setting
            if title_designer_page.mgt.click_bold_btn() == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("72e950df-588c-4b3f-94b4-cc0d801bbc84") as case:
            # [H80] Set font italic setting
            if title_designer_page.mgt.click_italic_btn() == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("61b422c7-70a9-4c78-8657-46e75ac36e0c") as case:
            # [H81] Open color selector window
            if title_designer_page.mgt.apply_font_face_color("FFFFFF") == True:
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            case.result = check_in_pos

    def test_1_1_3(self):
        with uuid("cb5cdabe-ee93-4114-8722-2e134c8d79af") as case:
            # [H70] Input text from textbox on designer top-left
            main_page.enter_room(1)
            main_page.select_library_icon_view_media('Motion Graphics 001')
            main_page.tips_area_insert_media_to_selected_track()
            tips_area_page.click_TipsArea_btn_Designer("Title")
            time.sleep(2)
            main_page.press_enter_key()
            main_page.exist_click(L.title_designer.title.btn_title)
            title_designer_page.mgt.select_title_track("PowerDirector")
            if title_designer_page.mgt.input_title_text("A") == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("8dd0b798-0a69-42c2-afeb-49c942ca07ac") as case:
            # [H71] Input multiple lines text
            if title_designer_page.mgt.input_title_text("A\nB") == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("75ca0614-655f-4374-9681-11298855430a") as case:
            # [H72] Input unicode text
            if title_designer_page.mgt.input_title_text("Δ") == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("2359a7e6-94a6-4d89-87c4-fae7ed2e0ff2") as case:
            # [H73] Input unicode text + normal text together and displays fine
            if title_designer_page.mgt.input_title_text("ΔB") == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("3e6ac88a-fc6e-4e72-bdd3-476366855615") as case:
            # [H74] Input special symbols as text (!,@,#,$,*….)
            if title_designer_page.mgt.input_title_text("!,@,#,$,*") == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("84217281-2b15-4f7f-8263-dfa44297532b") as case:
            # [H75] Able to Input extra long text and display correctly
            if title_designer_page.mgt.input_title_text("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("29ca3003-dd08-4684-a2d1-8c367e80801f") as case:
            # [H76] Other text and graphics color are normal in preview
            main_page.exist_click(L.title_designer.title.edittext_title_text)
            main_page.tap_SelectAll_hotkey()
            main_page.press_backspace_key()
            title_designer_page.mgt.input_title_text("A")
            if title_designer_page.mgt.select_title_track("") == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("9c5929c4-0e13-4e38-89bf-5089a0f46c2f") as case:
            # [H77] Hoktey can work
            title_designer_page.mgt.select_title_track("By Cyberlink")
            main_page.exist_click(L.title_designer.title.edittext_title_text)
            main_page.tap_SelectAll_hotkey()
            main_page.tap_Cut_hotkey()
            if title_designer_page.mgt.select_title_track("") == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

    def test_1_2_1(self):
        with uuid("9bfe114d-08f0-4bca-b83d-dc3731add235") as case:
            # [H91] Group no. is correct as template.
            main_page.enter_room(1)
            main_page.select_library_icon_view_media('Motion Graphics 001')
            main_page.tips_area_insert_media_to_selected_track()
            tips_area_page.click_TipsArea_btn_Designer("Title")
            time.sleep(2)
            main_page.press_enter_key()
            main_page.exist_click(L.title_designer.motion_graphic_title.btn_graphics_color)
            if title_designer_page.mgt.apply_graphics_color(3, "34DCE6") == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("8631e135-ff6e-4733-9672-6b941c380856") as case:
            # [H92] Default color is correct
            if title_designer_page.mgt.get_graphics_color(1) == "34DCE7":
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("01726d8e-a199-4588-8298-b6cae1b43a4b") as case:
            # [H93] Open color selector window
            title_designer_page.mgt.apply_graphics_color(1, "34DCE6")
            if title_designer_page.mgt.get_graphics_color(1) == "34DCE6":
                check_in_pos = True
            else:
                check_in_pos = False
            main_page.press_esc_key()
            case.result = check_in_pos

    def test_1_3_1(self):
        with uuid("d7952f75-677e-42ab-8974-a0c374f22c30") as case:
            # [H103] Set position X axis value (-2.000~2.000)
            main_page.enter_room(1)
            main_page.select_library_icon_view_media('Motion Graphics 001')
            main_page.tips_area_insert_media_to_selected_track()
            tips_area_page.click_TipsArea_btn_Designer("Title")
            time.sleep(2)
            main_page.press_enter_key()
            main_page.exist_click(L.title_designer.motion_graphic_title.btn_object_setting)
            title_designer_page.mgt.set_position_x_value("1")
            if title_designer_page.mgt.get_position_x_value() == "1.000":
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("db32a353-30b6-45dd-be59-95ed4ab362b0") as case:
            # [H104] Set position Y axis value (-2.000~2.000)
            title_designer_page.mgt.set_position_y_value("1")
            if title_designer_page.mgt.get_position_y_value() == "1.000":
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("24099712-2cbd-4df5-b0e4-ed6beecdc370") as case:
            # [H105] position adjust by ▲/▼ button
            title_designer_page.mgt.click_position_x_arrow_btn(0, 2)
            if title_designer_page.mgt.get_position_x_value() == "1.002":
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("0249110d-ca27-4db6-b0ae-85aefe673483") as case:
            # [H106] position adjust by input value
            if title_designer_page.mgt.set_position_y_value("-1") == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("a8866c40-7f73-4c0c-a7c0-956608649d12") as case:
            # [H107] Set width (0.2 ~ 10)
            title_designer_page.mgt.set_scale_width_value("7")
            if title_designer_page.mgt.get_scale_width_value() == "7.00":
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("c06c1043-f3d3-4298-9689-2dab01f2d0a1") as case:
            # [H109] Maintain aspect ratio after tick
            if title_designer_page.mgt.click_maintain_aspect_ratio(0) == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("fbed6d3a-cfbb-4641-906f-930c4ce67dab") as case:
            # [H108] Set Height (0.2 ~ 10)
            title_designer_page.mgt.set_scale_height_value("6")
            if title_designer_page.mgt.get_scale_height_value() == "6.00":
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("58ff77c7-523c-4ab0-9b6a-7b8edfbe1de5") as case:
            # [H110] scale adjust by ▲/▼ button
            title_designer_page.mgt.click_scale_width_arrow_btn(0,2)
            if title_designer_page.mgt.get_scale_width_value() == "7.02":
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("1f9276d4-3b0a-40a3-ac3e-4a4e01818009") as case:
            # [H111] scale Adjust by input value
            if title_designer_page.mgt.set_scale_height_value("7") == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("dc4f80fc-1ce5-4c27-93b9-f494946e23e1") as case:
            # [H112] scale Adjust by slide bar
            title_designer_page.mgt.drag_scale_width_slider("3")
            if title_designer_page.mgt.get_scale_width_value() == "3.00":
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("a2e0c688-7ad9-43b4-bc1d-8bd0beffa025") as case:
            # [H113] Set rotation value ( -9999 ~ 9999)
            title_designer_page.mgt.set_rotation_value("900")
            if title_designer_page.mgt.get_rotation_value() == "900.00":
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("e5bd8605-85c1-4d04-a298-84a7bb84ba11") as case:
            # [H114] angle Adjust by Input value
            if title_designer_page.mgt.set_rotation_value("900") == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("65b65055-3be8-48a4-b12d-97990196fca9") as case:
            # [H115] angle Adjust by ▲/▼ button
            title_designer_page.mgt.click_rotation_arrow_btn(0, 2)
            if title_designer_page.mgt.get_rotation_value() == "900.02":
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

        with uuid("d0ea5cc6-f4d2-40d7-b68f-1b49d5276616") as case:
            # [H116] Fold/Unfold status should keep at next entry
            if title_designer_page.mgt.unfold_title_tab(1) == True:
                check_in_pos = True
            else:
                check_in_pos = False
            case.result = check_in_pos

