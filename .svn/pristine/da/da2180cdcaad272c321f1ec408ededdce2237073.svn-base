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
report = MyReport("MyReport", driver=mwc, html_name="Mask Designer_02.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Mask_Designer_02/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Mask_Designer_02/'
Test_Material_Folder = app.testing_material

# Ground_Truth_Folder = '/Users/qadf/Desktop/AT/M4_Leo/SFT/GroundTruth/Mask_Designer_02/'
# Auto_Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto_MacAT/SFT/ATGroundTruth/Mask_Designer_02/'
# Test_Material_Folder = '/Users/qadf/Desktop/AT/M4_Leo/Material/'

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
            google_sheet_execution_log_init('Mask_Designer')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"media room result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')},"
            f"{report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
    def test_1_1_1(self):
        with uuid("91dc1c06-cb55-40e1-bb5a-54120d7af563") as case:
            # Insert Food.jpg to timeline > Enter Mask Designer
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 5)

            # 3.1.1 Category > Linear Mask > Default Setting
            mask_designer_page.Edit_MaskDesigner_ClickFullScreen()
            time.sleep(DELAY_TIME)
            mask_designer_page.MaskDesigner_Apply_template(3)
            time.sleep(DELAY_TIME)

            mask_designer_highlight = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_property.content,
                file_name=Auto_Ground_Truth_Folder + "M311_linear_default_highlight.png")
            compare_result_template = mask_designer_page.compare(Ground_Truth_Folder +
                                                                 "M311_linear_default_highlight.png",
                                                                 mask_designer_highlight)

            mask_designer_page.drag_Mask_Settings_Scroll_Bar(1.0)
            time.sleep(DELAY_TIME)

            mask_designer_settings = mask_designer_page.snapshot(
                locator=L.mask_designer.settings.content,
                file_name=Auto_Ground_Truth_Folder + "M311_linear_default_settings.png")
            compare_result_settings = mask_designer_page.compare(Ground_Truth_Folder +
                                                                 "M311_linear_default_settings.png",
                                                                 mask_designer_settings)

            mask_designer_preview = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M311_linear_default_preview.png")
            compare_result_preview = mask_designer_page.compare(Ground_Truth_Folder +
                                                                "M311_linear_default_preview.png",
                                                                mask_designer_preview)

            logger(compare_result_template)
            logger(compare_result_settings)
            logger(compare_result_preview)

            test_result = compare_result_template and compare_result_settings and compare_result_preview
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("bd6146ad-367c-4c69-ae1f-9135a151b58c") as case:
            # 3.1.1 Category > Linear Mask > Position adjustment
            mask_designer_page.object_settings.set_position_x(0.75)
            mask_designer_page.object_settings.set_position_y(0.25)

            position_x = mask_designer_page.Get_MaskDesigner_ObjectSetting_PositionX_Value()
            position_y = mask_designer_page.Get_MaskDesigner_ObjectSetting_PositionY_Value()

            mask_designer_preview = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M311_linear_position_adjust_preview.png")
            compare_result_preview = mask_designer_page.compare(Ground_Truth_Folder +
                                                                "M311_linear_position_adjust_preview.png",
                                                                mask_designer_preview)

            logger(position_x)
            logger(position_y)
            logger(compare_result_preview)

            if position_x != "0.75" or position_y != "0.25" or not compare_result_preview:
                case.result = False
            else:
                case.result = True

        with uuid("2d804c2b-c024-4d6f-a975-90c21404cd16") as case:
            # 3.1.1 Category > Linear Mask > Rotation adjustment
            mask_designer_page.object_settings.set_rotation(90)

            rotation_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_Rotation_Value()

            mask_designer_preview = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M311_linear_Rotation_adjust_preview.png")
            compare_result_preview = mask_designer_page.compare(Ground_Truth_Folder +
                                                                "M311_linear_Rotation_adjust_preview.png",
                                                                mask_designer_preview)

            logger(rotation_value)
            logger(compare_result_preview)

            if rotation_value != "90.00" or not compare_result_preview:
                case.result = False
            else:
                case.result = True

        with uuid("5cf05c54-06ae-42df-91f3-d026748bbeb7") as case:
            # 3.1.1 Category > Linear Mask > Move out of Canvas
            mask_designer_page.move_object_out_of_canvas()
            time.sleep(DELAY_TIME)

            mask_designer_preview = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M311_linear_MoveOutOfCanvas_preview.png")
            compare_result_preview = mask_designer_page.compare(Ground_Truth_Folder +
                                                                "M311_linear_MoveOutOfCanvas_preview.png",
                                                                mask_designer_preview, similarity=0.8)
            logger(compare_result_preview)

            test_result = compare_result_preview
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("274e76cb-a199-4a79-991c-9cb25dc420c6") as case:
            # 3.1.1 Category > Linear Mask > Move within Canvas
            mask_designer_page.tap_MaskDesigner_Undo_btn()
            time.sleep(DELAY_TIME)
            mask_designer_page.move_object_on_canvas()
            time.sleep(DELAY_TIME)

            mask_designer_preview = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M311_linear_MoveOnCanvas_preview.png")
            compare_result_preview = mask_designer_page.compare(Ground_Truth_Folder +
                                                                "M311_linear_MoveOnCanvas_preview.png",
                                                                mask_designer_preview)

            logger(compare_result_preview)

            test_result = compare_result_preview
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("3b7231c2-2571-4e0d-ac7b-4d4794dd653a") as case:
            # 3.1.1 Category > Linear Mask > Keyframe setting
            # add keyframe
            mask_designer_page.object_settings.position.click_add_remove_keyframe()
            time.sleep(DELAY_TIME)

            mask_designer_add = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_designer_window,
                file_name=Auto_Ground_Truth_Folder + "M311_linear_keyframe_add.png")
            compare_result_add = mask_designer_page.compare(Ground_Truth_Folder +
                                                            "M311_linear_keyframe_add.png",
                                                            mask_designer_add)
            # remove keyframe
            mask_designer_page.object_settings.position.click_add_remove_keyframe()
            time.sleep(DELAY_TIME)

            mask_designer_remove = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_designer_window,
                file_name=Auto_Ground_Truth_Folder + "M311_linear_keyframe_remove.png")
            compare_result_remove = mask_designer_page.compare(Ground_Truth_Folder +
                                                               "M311_linear_keyframe_remove.png",
                                                               mask_designer_remove, similarity=0.8)

            logger(compare_result_add)
            logger(compare_result_remove)

            test_result = compare_result_add and compare_result_remove
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("da7fc654-30f7-4e7a-9def-402d2b18330f") as case:
            # 3.1.1 Category > Mask switch
            mask_designer_page.drag_Mask_Settings_Scroll_Bar(0.0)
            time.sleep(DELAY_TIME)
            mask_designer_page.MaskDesigner_Apply_template(0)
            time.sleep(DELAY_TIME)
            mask_designer_page.MaskDesigner_Apply_template(5)
            time.sleep(DELAY_TIME)

            mask_designer_highlight = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_property.content,
                file_name=Auto_Ground_Truth_Folder + "M311_mask_switch_highlight.png")
            compare_result_template = mask_designer_page.compare(Ground_Truth_Folder +
                                                                 "M311_mask_switch_highlight.png",
                                                                 mask_designer_highlight)

            mask_designer_preview = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M311_mask_switch_preview.png")
            compare_result_preview = mask_designer_page.compare(Ground_Truth_Folder +
                                                                "M311_mask_switch_preview.png",
                                                                mask_designer_preview)

            logger(compare_result_template)
            logger(compare_result_preview)

            test_result = compare_result_template and compare_result_preview
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("bd398444-07bc-438f-bf0c-4efbd09d84a7") as case:
            # 3.1.1 Category > Mask switch > Undo & Redo
            mask_designer_page.tap_MaskDesigner_Undo_btn()
            time.sleep(DELAY_TIME)

            mask_designer_highlight_undo = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_property.content,
                file_name=Auto_Ground_Truth_Folder + "M311_mask_switch_highlight_undo.png")
            compare_result_template_undo = mask_designer_page.compare(Ground_Truth_Folder +
                                                                      "M311_mask_switch_highlight_undo.png",
                                                                      mask_designer_highlight_undo)

            mask_designer_preview_undo = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M311_mask_switch_preview_undo.png")
            compare_result_preview_undo = mask_designer_page.compare(Ground_Truth_Folder +
                                                                     "M311_mask_switch_preview_undo.png",
                                                                     mask_designer_preview_undo)

            mask_designer_page.tap_MaskDesigner_Redo_btn()
            time.sleep(DELAY_TIME)

            mask_designer_highlight_redo = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_property.content,
                file_name=Auto_Ground_Truth_Folder + "M311_mask_switch_highlight_redo.png")
            compare_result_template_redo = mask_designer_page.compare(Ground_Truth_Folder +
                                                                      "M311_mask_switch_highlight_redo.png",
                                                                      mask_designer_highlight_redo)

            mask_designer_preview_redo = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M311_mask_switch_preview_redo.png")
            compare_result_preview_redo = mask_designer_page.compare(Ground_Truth_Folder +
                                                                     "M311_mask_switch_preview_redo.png",
                                                                     mask_designer_preview_redo)

            logger(compare_result_template_undo)
            logger(compare_result_preview_undo)
            logger(compare_result_template_redo)
            logger(compare_result_preview_redo)

            result_1 = compare_result_template_undo and compare_result_preview_undo
            result_2 = compare_result_template_redo and compare_result_preview_redo
            test_result = result_1 and result_2
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("3b8a48c0-ab4e-4c4c-83f6-8637bbb0969e") as case:
            # 3.1.1 Category > Parallel Mask > Default Setting
            mask_designer_page.drag_Mask_Settings_Scroll_Bar(0.0)
            time.sleep(DELAY_TIME)
            mask_designer_page.MaskDesigner_Apply_template(0)
            time.sleep(DELAY_TIME)
            mask_designer_page.MaskDesigner_Apply_template(5)
            time.sleep(DELAY_TIME)

            mask_designer_highlight = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_property.content,
                file_name=Auto_Ground_Truth_Folder + "M311_parallel_default_highlight.png")
            compare_result_template = mask_designer_page.compare(Ground_Truth_Folder +
                                                                 "M311_parallel_default_highlight.png",
                                                                 mask_designer_highlight)

            mask_designer_page.drag_Mask_Settings_Scroll_Bar(1.0)
            time.sleep(DELAY_TIME)

            mask_designer_settings = mask_designer_page.snapshot(
                locator=L.mask_designer.settings.content,
                file_name=Auto_Ground_Truth_Folder + "M311_parallel_default_settings.png")
            compare_result_settings = mask_designer_page.compare(Ground_Truth_Folder +
                                                                 "M311_parallel_default_settings.png",
                                                                 mask_designer_settings)

            mask_designer_preview = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M311_parallel_default_preview.png")
            compare_result_preview = mask_designer_page.compare(Ground_Truth_Folder +
                                                                "M311_parallel_default_preview.png",
                                                                mask_designer_preview)

            logger(compare_result_template)
            logger(compare_result_settings)
            logger(compare_result_preview)

            test_result = compare_result_template and compare_result_settings and compare_result_preview
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("b24c212b-152e-4932-ace0-c5184e952f15") as case:
            # 3.1.1 Category > Parallel Mask > Position adjustment
            mask_designer_page.object_settings.set_position_x(0.75)
            mask_designer_page.object_settings.set_position_y(0.25)

            position_x = mask_designer_page.Get_MaskDesigner_ObjectSetting_PositionX_Value()
            position_y = mask_designer_page.Get_MaskDesigner_ObjectSetting_PositionY_Value()

            mask_designer_preview = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M311_parallel_position_adjust_preview.png")
            compare_result_preview = mask_designer_page.compare(Ground_Truth_Folder +
                                                                "M311_parallel_position_adjust_preview.png",
                                                                mask_designer_preview)

            logger(position_x)
            logger(position_y)
            logger(compare_result_preview)

            if position_x != "0.75" or position_y != "0.25" or not compare_result_preview:
                case.result = False
            else:
                case.result = True

        with uuid("e40f931e-104d-4516-b306-753bfa114d27") as case:
            # 3.1.1 Category > Parallel Mask > Rotation adjustment
            mask_designer_page.object_settings.set_rotation(90)

            rotation_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_Rotation_Value()

            mask_designer_preview = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M311_parallel_Rotation_adjust_preview.png")
            compare_result_preview = mask_designer_page.compare(Ground_Truth_Folder +
                                                                "M311_parallel_Rotation_adjust_preview.png",
                                                                mask_designer_preview)

            logger(rotation_value)
            logger(compare_result_preview)

            if rotation_value != "90.00" or not compare_result_preview:
                case.result = False
            else:
                case.result = True

        with uuid("31bd7f4e-d3bb-46b3-b0a1-0e530a615739") as case:
            # 3.1.1 Category > Parallel Mask > Keyframe setting
            # add keyframe
            mask_designer_page.object_settings.position.click_add_remove_keyframe()
            time.sleep(DELAY_TIME)

            mask_designer_add = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_designer_window,
                file_name=Auto_Ground_Truth_Folder + "M311_parallel_keyframe_add.png")
            compare_result_add = mask_designer_page.compare(Ground_Truth_Folder +
                                                            "M311_parallel_keyframe_add.png",
                                                            mask_designer_add, similarity=0.8)
            # remove keyframe
            mask_designer_page.object_settings.position.click_add_remove_keyframe()
            time.sleep(DELAY_TIME)

            mask_designer_remove = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_designer_window,
                file_name=Auto_Ground_Truth_Folder + "M311_parallel_keyframe_remove.png")
            compare_result_remove = mask_designer_page.compare(Ground_Truth_Folder +
                                                               "M311_parallel_keyframe_remove.png",
                                                               mask_designer_remove, similarity=0.8)

            logger(compare_result_add)
            logger(compare_result_remove)

            test_result = compare_result_add and compare_result_remove
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("67622a99-55d3-44b4-a2fe-1c382b4aff18") as case:
            # 3.1.1 Category > Parallel Mask > with invert
            mask_designer_page.drag_Mask_Settings_Scroll_Bar(0.0)
            time.sleep(DELAY_TIME)
            mask_designer_page.Edit_MaskDesigner_Invert_mask_SetCheck(True)
            time.sleep(DELAY_TIME)

            mask_designer = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_designer_window,
                file_name=Auto_Ground_Truth_Folder + "M311_parallel_invert.png")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder +
                                                        "M311_parallel_invert.png",
                                                        mask_designer, similarity=0.8)

            logger(compare_result)

            test_result = compare_result
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("ccb524cb-022f-42cb-83d4-c3d15e5f3bfb") as case:
            # 3.1.1 Category > Parallel Mask > Max Range
            # cancel maintain aspect ratio
            mask_designer_page.drag_Mask_Settings_Scroll_Bar(1.0)
            mask_designer_page.object_settings.set_scale_ratio(False)
            mask_designer_page.object_settings.set_scale_width(6.000)
            mask_designer_page.object_settings.click_scale_width_arrow("up", 1)

            mask_designer_page.object_settings.set_scale_height(6.000)
            mask_designer_page.object_settings.click_scale_height_arrow("up", 1)

            width_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_ScaleWidth_Value()
            height_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_ScaleHigh_Value()

            logger(width_value)
            logger(height_value)

            if width_value != "6.000" or height_value != "6.000":
                case.result = False
            else:
                case.result = True

        with uuid("889b7557-3591-476a-8ad5-825198ee8b14") as case:
            # 3.1.1 Category > Parallel Mask > Min Range
            mask_designer_page.object_settings.set_scale_width(0.001)
            mask_designer_page.object_settings.click_scale_width_arrow("down", 1)

            mask_designer_page.object_settings.set_scale_height(0.001)
            mask_designer_page.object_settings.click_scale_height_arrow("down", 1)

            width_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_ScaleWidth_Value()
            height_value = mask_designer_page.Get_MaskDesigner_ObjectSetting_ScaleHigh_Value()

            # restore down dialog size
            mask_designer_page.Edit_MaskDesigner_ClickRestoreScreen()
            time.sleep(DELAY_TIME)

            logger(width_value)
            logger(height_value)

            if width_value != "0.001" or height_value != "0.001":
                case.result = False
            else:
                case.result = True

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid("7e09ccb3-d332-4e0f-9074-73cc4d3f37ab") as case:
            # Insert Food.jpg to timeline > Enter Mask Designer
            main_page.insert_media("Food.jpg")
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 5)

            # maximize dialog size
            mask_designer_page.Edit_MaskDesigner_ClickFullScreen()
            time.sleep(DELAY_TIME)

            # 3.1.4 Create a brush mask
            mask_designer_page.click_create_brush_mask_btn()
            time.sleep(DELAY_TIME)
            enter = mask_designer_page.is_enter_brush_mask_designer()
            if not enter:
                case.result = False
            else:
                case.result = True

            # close brush mask dialog
            mask_designer_page.brush_mask.click_close_btn()
            time.sleep(DELAY_TIME)

        with uuid("527e3787-c726-42c4-aa6b-6782e67f29df") as case:
            # 3.1.5 Create a selection mask > Enable > 1st
            mask_designer_page.click_create_selection_mask_btn()
            time.sleep(DELAY_TIME)

            mask_designer = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_designer_window,
                file_name=Auto_Ground_Truth_Folder + "M315_enable_1st.png")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder +
                                                        "M315_enable_1st.png",
                                                        mask_designer)

            logger(compare_result)

            test_result = compare_result
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("59c41bd1-c78f-4021-a39e-ae961f4e6974") as case:
            # 3.1.5 Create a selection mask > Enable > 2nd
            mask_designer = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_designer_window,
                file_name=Auto_Ground_Truth_Folder + "M315_enable_2nd.png")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder +
                                                        "M315_enable_2nd.png",
                                                        mask_designer)

            logger(compare_result)

            test_result = compare_result
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("27da4450-c8ce-47b4-b68c-23bca1be7b9f") as case:
            # 3.1.5 Create a selection mask > Before complete range selection
            mask_designer = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_designer_window,
                file_name=Auto_Ground_Truth_Folder + "M315_before_selection.png")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder +
                                                        "M315_before_selection.png",
                                                        mask_designer)

            logger(compare_result)

            test_result = compare_result
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("14424525-c009-4c34-9def-4c5401c953c9") as case:
            # 3.1.5 Create a selection mask > De-select Selection Mask button > Before selection mask region
            # disable selection mask
            mask_designer_page.click_create_selection_mask_btn()
            time.sleep(DELAY_TIME)

            mask_designer = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_designer_window,
                file_name=Auto_Ground_Truth_Folder + "M315_deselect_before.png")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder +
                                                        "M315_deselect_before.png",
                                                        mask_designer)

            logger(compare_result)

            test_result = compare_result
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("47012fb7-df50-432a-87f1-0be0c5c1e647") as case:
            # 3.1.5 Create a selection mask > Set selection mask region > Set selection point
            # enable selection mask
            mask_designer_page.click_create_selection_mask_btn()
            time.sleep(DELAY_TIME)
            mask_designer_page.draw_triangle_on_canvas()
            time.sleep(DELAY_TIME)

            mask_designer = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_designer_window,
                file_name=Auto_Ground_Truth_Folder + "M315_select_DrawOnCanvas.png")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder +
                                                        "M315_select_DrawOnCanvas.png",
                                                        mask_designer)

            logger(compare_result)

            test_result = compare_result
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("125aadad-9d0f-4238-be69-d5070eba21b4") as case:
            # 3.1.5 Create a selection mask > Set selection mask region > Remove selection point (from context menu)
            # Right click at selection point
            mask_designer_page.right_click()
            mask_designer_page.select_right_click_menu(0)

            mask_designer = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M315_select_remove_selection_point.png")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder +
                                                        "M315_select_remove_selection_point.png",
                                                        mask_designer)

            logger(compare_result)

            test_result = compare_result
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("cdba79e3-f1f6-4c88-b0a4-1e777c84309e") as case:
            # 3.1.5 Create a selection mask > De-select Selection Mask button > Complete selection mask region
            # disable selection mask
            mask_designer_page.click_create_selection_mask_btn()
            time.sleep(DELAY_TIME)

            mask_designer = mask_designer_page.snapshot(
                locator=L.mask_designer.mask_designer_window,
                file_name=Auto_Ground_Truth_Folder + "M315_deselect_complete.png")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder +
                                                        "M315_deselect_complete.png",
                                                        mask_designer)

            logger(compare_result)

            test_result = compare_result
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("c731cd17-28ce-4bed-9083-862ed288c821") as case:
            # 3.1.5 Create a selection mask > Set selection mask region > Create handle after create selection mask
            # enable selection mask
            mask_designer_page.click_create_selection_mask_btn()
            time.sleep(DELAY_TIME)

            mask_designer = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M315_select_ShowHandle.png")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder +
                                                        "M315_select_ShowHandle.png",
                                                        mask_designer)

            logger(compare_result)

            test_result = compare_result
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("a442c87b-18b8-446a-bd53-57e6d17583e5") as case:
            # 3.1.5 Create a selection mask > Set selection mask region > Add selection point on mask edge

            mask_designer = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M315_select_AddPointAtEdge.png")
            compare_result = mask_designer_page.compare(Ground_Truth_Folder +
                                                        "M315_select_AddPointAtEdge.png",
                                                        mask_designer)

            logger(compare_result)

            test_result = compare_result
            if test_result is False:
                case.result = False
            else:
                case.result = True

        with uuid("3be75baf-606f-4b10-b3fe-c16b27d332dc") as case:
            # 3.1.5 Create a selection mask > Set selection mask region > Undo / Redo

            mask_designer_page.tap_MaskDesigner_Undo_btn()

            mask_designer_undo = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M315_select_undo.png")
            compare_result_undo = mask_designer_page.compare(Ground_Truth_Folder +
                                                             "M315_select_undo.png",
                                                             mask_designer_undo)

            mask_designer_page.tap_MaskDesigner_Redo_btn()

            mask_designer_redo = mask_designer_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + "M315_select_redo.png")
            compare_result_redo = mask_designer_page.compare(Ground_Truth_Folder +
                                                             "M315_select_redo.png",
                                                             mask_designer_redo)

            logger(compare_result_undo)
            logger(compare_result_redo)

            test_result = compare_result_undo and compare_result_redo
            if test_result is False:
                case.result = False
            else:
                case.result = True

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''

                ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"
