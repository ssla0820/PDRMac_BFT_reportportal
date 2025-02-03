import sys, os

import pages.mask_designer_page

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
tips_area_page = PageFactory().get_page_object('tips_area_page',mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Mask Designerv20.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Mask_Designer_v20/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Mask_Designer_v20/'
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

class Test_Mask_Designer_v20():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME * 3)
        # main_page.insert_media("Food.jpg")
        # main_page.tap_TipsArea_Tools_menu(1)
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
            google_sheet_execution_log_init('Mask_Designer_v20')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"Mask Designer v20 result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()

    def drag_tool_on_canvas_from_upper_right_down (self):
        el_canvas = self.exist(L.mask_designer.mask_property.brush_mask_designer.preview_area)
        pos_canvas = el_canvas.AXPosition
        size_canvas = el_canvas.AXSize
        time.sleep(1)
        pos_middle_x = pos_canvas[0] + size_canvas[0] * 0.2
        pos_middle_y = pos_canvas[1] + size_canvas[1] * 0.2
        self.drag_mouse((pos_middle_x + 150, pos_middle_y - 150), (pos_middle_x, pos_middle_y))
        self.drag_mouse((pos_middle_x - 50, pos_middle_y + 120), (pos_middle_x, pos_middle_y))

        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        # 2/11
        with uuid("c5d6b628-d0cb-40a3-9c2c-251bfc5e967d") as case:
            # session 5.1 : Brush Mask Designer > Caption bar
            # case5.1.2.1.1 : Caption bar > Edit > Undo > Click item
            # Insert jpg to timeline > Enter Mask Designer
            main_page.select_library_icon_view_media('Sport 01.jpg')
            main_page.insert_media("Sport 01.jpg")
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME*4)

            # Enter brush mask designer
            mask_designer_page.click_create_brush_mask_btn()
            time.sleep(DELAY_TIME * 2)
            enter_brush_mask_designer = mask_designer_page.is_enter_brush_mask_designer()
            logger(enter_brush_mask_designer)
            if enter_brush_mask_designer:
                # Increase width of tool and then draw on canvas
                # mask_designer_page.brush_mask.width.set_value('60') # will cause a bug that unable to undo /redo by hotkey after operating by the page function
                mask_designer_page.brush_mask.width.adjust_slider(60)
                mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_middle()
                mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_left()
                mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_right()
                time.sleep(DELAY_TIME * 2)

                # snapshot
                preview_wnd = tips_area_page.snapshot(locator=L.mask_designer.mask_property.brush_mask_designer.preview_area,
                                                      file_name=Auto_Ground_Truth_Folder + 'G5.1.2.1.1_Brush_Mask_Designer_Preview.png')
                logger(preview_wnd)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G5.1.2.1.1_Brush_Mask_Designer_Preview.png',
                    preview_wnd)
                logger(compare_result)

                # undo
                mask_designer_page.brush_mask.click_undo()
                time.sleep(DELAY_TIME * 1)

                # snapshot#2
                preview_wnd = tips_area_page.snapshot(
                    locator=L.mask_designer.mask_property.brush_mask_designer.preview_area,
                    file_name=Auto_Ground_Truth_Folder + 'G5.1.2.1.1_Brush_Mask_Designer_Preview_after_undo.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G5.1.2.1.1_Brush_Mask_Designer_Preview_after_undo.png',
                    preview_wnd)
                logger(compare_result1)

            # 2/11
            with uuid("629c1813-7601-48fa-b024-0b5dd901e57a") as case:
                # case5.1.2.2.1 : Caption bar > Edit > Redo > Click item
                # Redo
                time.sleep(DELAY_TIME * 1)
                mask_designer_page.brush_mask.click_redo()
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.mask_designer.mask_property.brush_mask_designer.preview_area,
                    file_name=Auto_Ground_Truth_Folder + 'G5.1.2.2.1_Brush_Mask_Designer_Preview_after_redo.png')
                logger(preview_wnd)
                compare_result_redo = tips_area_page.compare(
                    Ground_Truth_Folder + 'G5.1.2.2.1_Brush_Mask_Designer_Preview_after_redo.png',
                    preview_wnd)
                logger(compare_result_redo)

                case.result = compare_result_redo

            # 2/11
            with uuid("73dfc207-da67-4b8c-85a2-cdc2da301a93") as case:
                # case5.1.2.1.2 : Caption bar > Edit > Undo > Hotkey
                # Undo by hotkey
                time.sleep(DELAY_TIME * 2)
                mask_designer_page.tap_Undo_hotkey()
                #mask_designer_page.keyboard.pressed(mask_designer_page.brush_mask.keyboard.key.cmd, "z")
                time.sleep(DELAY_TIME * 2)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.mask_designer.mask_property.brush_mask_designer.preview_area,
                    file_name=Auto_Ground_Truth_Folder + 'G5.1.2.1.2_Brush_Mask_Designer_Preview_after_undo_by_hotkey.png')
                logger(preview_wnd)
                compare_result_undo_hk = tips_area_page.compare(
                    Ground_Truth_Folder + 'G5.1.2.1.2_Brush_Mask_Designer_Preview_after_undo_by_hotkey.png',
                    preview_wnd)
                logger(compare_result_undo_hk)

                case.result = compare_result_undo_hk

            # 2/11
            with uuid("22585893-e6fc-4245-a1ed-d3aaa222db06") as case:
                # case5.1.2.2.2 : Caption bar > Edit > Redo > Hotkey
                # Undo by hotkey
                time.sleep(DELAY_TIME * 1)
                mask_designer_page.tap_Redo_hotkey()
                #mask_designer_page.keyboard.pressed(mask_designer_page.keyboard.key.cmd,
                                                    #mask_designer_page.keyboard.key.shift, "z")
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.mask_designer.mask_property.brush_mask_designer.preview_area,
                    file_name=Auto_Ground_Truth_Folder + 'G5.1.2.2.2_Brush_Mask_Designer_Preview_after_redo_by_hotkey.png')
                logger(preview_wnd)
                compare_result_redo_hk = tips_area_page.compare(
                    Ground_Truth_Folder + 'G5.1.2.2.2_Brush_Mask_Designer_Preview_after_redo_by_hotkey.png',
                    preview_wnd)
                logger(compare_result_redo_hk)

                case.result = compare_result_redo_hk

            # 2/11
            with uuid("b88bce2f-0235-4756-9cc9-0fd489d70dd7") as case:
                # case5.1.2.3.1 : Caption bar > Edit > Reset the canvas
                # click [Reset] button
                mask_designer_page.brush_mask.click_reset()
                time.sleep(DELAY_TIME * 1)
                mask_designer_page.brush_mask.reset_dialog.click_ok()
                #time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.mask_designer.mask_property.brush_mask_designer.window,
                    file_name=Auto_Ground_Truth_Folder + 'G5.1.2.3.1_Brush_Mask_Designer_Preview_after_reset.png')
                logger(preview_wnd)
                compare_result_reset = tips_area_page.compare(
                    Ground_Truth_Folder + 'G5.1.2.3.1_Brush_Mask_Designer_Preview_after_reset.png',
                    preview_wnd, similarity=0.8)
                logger(compare_result_reset)

                case.result = compare_result_reset

            # 2/11
            with uuid("f691ffc6-a950-434d-81d4-30e136672231") as case:
                # case5.1.7 : Caption bar > Maximize / Restore down
                # maximize brush mask designer
                mask_designer_page.brush_mask.click_max_restore_btn()
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.mask_designer.mask_property.brush_mask_designer.window,
                    file_name=Auto_Ground_Truth_Folder + 'G5.1.7_Brush_Mask_Designer_Maximize.png')
                logger(preview_wnd)
                compare_result_maximize = tips_area_page.compare(
                    Ground_Truth_Folder + 'G5.1.7_Brush_Mask_Designer_Maximize.png',
                    preview_wnd)
                logger(compare_result_maximize)

                # restore the window
                mask_designer_page.brush_mask.click_max_restore_btn()
                time.sleep(DELAY_TIME * 1)

                case.result = compare_result_maximize

            # 2/11
            with uuid("bdd6e7ef-0205-42f8-a9e4-8d1f1c7f3c00") as case:
                # case5.1.8 : Caption bar > Close
                # Close brush mask designer
                mask_designer_page.brush_mask.click_close_btn()
                time.sleep(DELAY_TIME * 2)

                close_brush_mask_designer = mask_designer_page.is_not_exist(L.mask_designer.mask_property.brush_mask_designer.window)
                logger(close_brush_mask_designer)
                if close_brush_mask_designer:
                    case.result = True
                else:
                    case.result = False

            case.result = compare_result and compare_result1

  # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        # 2/16
        with uuid("a81ae02a-8807-4339-929a-b122cfc0e611") as case:
            # session 5.2 : Brush Mask Designer > Tools
            # case5.2.1.2 : Pen Style > Flat
            # Import animated png (GIF) into media room > Enter Mask Designer
            time.sleep(DELAY_TIME * 5)
            main_page.set_project_aspect_ratio_9_16()
            import_media = media_room_page.import_media_file(
                Test_Material_Folder + 'Mask_Designer_v20/9-16.gif')
            logger(import_media)
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('9-16.gif')
            main_page.insert_media("9-16.gif")
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME*4)

            # Enter brush mask designer
            mask_designer_page.click_create_brush_mask_btn()
            time.sleep(DELAY_TIME * 2)
            enter_brush_mask_designer = mask_designer_page.is_enter_brush_mask_designer()
            logger(enter_brush_mask_designer)
            if enter_brush_mask_designer:
                # Switch pen tool to "Flat"
                # mask_designer_page.brush_mask.width.set_value('60') # will cause a bug that unable to undo /redo by hotkey after operating by the page function
                mask_designer_page.brush_mask.tools.set_flat()

                with uuid("c6b03798-c86f-420d-97d5-c53ef26c6fe5") as case:
                    # Case 5.2.2.1.1 : Width > Value > Default(20)
                    width = mask_designer_page.brush_mask.width.get_value()
                    logger(width)
                    if width == '20':
                        case.result = True
                    else:
                        case.result = False

                with uuid("3bfb20d7-e1a9-4002-aba6-897e1b712090") as case:
                    # Case 5.2.3.1.1 : Transparency of tracing paper > Value > Default(50)
                    transparency = mask_designer_page.brush_mask.transparency.get_value()
                    logger(transparency)
                    if transparency == '50%':
                        case.result = True
                    else:
                        case.result = False

                with uuid("eed5bb6c-9b65-4977-a6f0-ea98f4ca5cdc") as case:
                    # Case 5.2.2.2.1 : Width > Adjustment > By slide (20) -> (60)
                    mask_designer_page.brush_mask.width.adjust_slider(60)
                    mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_middle()
                    #mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_left()
                    time.sleep(DELAY_TIME * 2)
                    new_width = mask_designer_page.brush_mask.width.get_value()
                    logger(new_width)
                    if new_width == '60':
                        case.result = True
                    else:
                        case.result = False

                # snapshot
                preview_wnd = tips_area_page.snapshot(locator=L.mask_designer.mask_property.brush_mask_designer.preview_area,
                                                      file_name=Auto_Ground_Truth_Folder + 'G5.2.1.2_Brush_Mask_Designer_Flat.png')
                logger(preview_wnd)
                compare_result_flat = tips_area_page.compare(
                    Ground_Truth_Folder + 'G5.2.1.2_Brush_Mask_Designer_Flat.png',
                    preview_wnd, similarity=0.8)
                logger(compare_result_flat)

                # 2/16
                with uuid("46f438e6-38cf-424c-8032-6d9d7d38183b") as case:
                    # session 5.2 : Brush Mask Designer > Tools
                    # Case 5.2.2.2.1 : Width > Adjustment > By ▲/▼
                    # click [Arrow up] for 10 times
                    mask_designer_page.brush_mask.width.set_arrow(0,10)
                    new_width = mask_designer_page.brush_mask.width.get_value()
                    logger(new_width)
                    if new_width == '70':
                        result1 = True
                        logger(result1)
                    else:
                        result1 = False
                        logger(result1)

                    # click [Arrow down] for 5 times
                    mask_designer_page.brush_mask.width.set_arrow(1, 5)
                    new_width_1 = mask_designer_page.brush_mask.width.get_value()
                    logger(new_width_1)
                    if new_width_1 == '65':
                        # draw on canvas
                        mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_left()
                        # snapshot
                        preview_wnd = tips_area_page.snapshot(
                            locator=L.mask_designer.mask_property.brush_mask_designer.preview_area,
                            file_name=Auto_Ground_Truth_Folder + 'G5.2.2.2.2_Brush_Mask_Designer_Width_Reduce_Value_By_Arrow.png')
                        logger(preview_wnd)
                        compare_result_arrow = tips_area_page.compare(
                            Ground_Truth_Folder + 'G5.2.2.2.2_Brush_Mask_Designer_Width_Reduce_Value_By_Arrow.png',
                            preview_wnd, similarity=0.8)
                        logger(compare_result_arrow)
                        result2 = compare_result_arrow
                        logger(result2)
                    else:
                        result2 = False
                        logger(result2)

                    case.result = result1 and result2


                # 2/16
                with uuid("24a7b648-8436-4d36-8835-052520ce2416") as case:
                    # session 5.2 : Brush Mask Designer > Tools
                    # case5.2.1.1 : Pen Style > Round
                    mask_designer_page.brush_mask.tools.set_round()
                    mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_right()
                    #self.drag_tool_on_canvas_from_upper_right_down()
                    time.sleep(DELAY_TIME * 2)

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.preview_area,
                        file_name=Auto_Ground_Truth_Folder + 'G5.2.1.1_Brush_Mask_Designer_Round.png')
                    logger(preview_wnd)
                    compare_result_round = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.2.1.1_Brush_Mask_Designer_Round.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result_round)

                    case.result = compare_result_round

                # 2/16
                with uuid("c416a8f9-a0ce-41b0-b624-fe1a53495ba3") as case:
                    # session 5.2 : Brush Mask Designer > Tools
                    # case5.2.1.4 : Pen Style > Eraser
                    mask_designer_page.brush_mask.tools.set_eraser()
                    #mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_right()
                    #self.drag_tool_on_canvas_from_upper_right_down()
                    time.sleep(DELAY_TIME * 2)

                    # 2/16
                    with uuid("a4343755-18c2-463c-94ed-ce81020d03eb") as case:
                        # session 5.2 : Brush Mask Designer > Tools
                        # Case 5.2.2.2.2 : Width > Adjustment > By input value
                        #
                        mask_designer_page.brush_mask.width.set_value(80)
                        new_width = mask_designer_page.brush_mask.width.get_value()
                        logger(new_width)
                        if new_width == '80':
                            result1 = True
                            logger(result1)

                            # draw on canvas
                            #self.drag_tool_on_canvas_from_upper_right_down()
                            mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_right()

                            # snapshot
                            preview_wnd = tips_area_page.snapshot(
                                locator=L.mask_designer.mask_property.brush_mask_designer.preview_area,
                                file_name=Auto_Ground_Truth_Folder + 'G5.2.1.1_Brush_Mask_Designer_Round.png')
                            logger(preview_wnd)
                            compare_result_round = tips_area_page.compare(
                                Ground_Truth_Folder + 'G5.2.1.1_Brush_Mask_Designer_Round.png',
                                preview_wnd, similarity=0.8)
                            logger(compare_result_round)

                        else:
                            result1 = False
                            logger(result1)

                        case.result = result1 and compare_result_round

                    case.result = compare_result_round

                # 2/16
                with uuid("fd3f24d7-d7cf-4c42-b146-d45fa4a0f948") as case:
                    # session 5.2 : Brush Mask Designer > Tools
                    # Case 5.2.3.2.1 : Transparency of tracing paper > Adjustment > By slider
                    mask_designer_page.brush_mask.transparency.adjust_slider(70)
                    # mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_middle()
                    # mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_left()
                    time.sleep(DELAY_TIME * 2)
                    new_width = mask_designer_page.brush_mask.transparency.get_value()
                    logger(new_width)
                    if new_width == '70%':
                        case.result = True
                    else:
                        case.result = False

                # 2/16
                with uuid("9a144c7d-66a9-4440-b89b-f06530206961") as case:
                    # session 5.2 : Brush Mask Designer > Tools
                    # Case 5.2.3.2.3 : Transparency of tracing paper > Adjustment > By ▲/▼
                    # click [Arrow up] for 5 times
                    mask_designer_page.brush_mask.transparency.set_arrow(0, 5)
                    new_width = mask_designer_page.brush_mask.transparency.get_value()
                    logger(new_width)
                    if new_width == '75%':
                        result1 = True
                        logger(result1)
                    else:
                        result1 = False
                        logger(result1)

                    # click [Arrow down] for 5 times
                    mask_designer_page.brush_mask.transparency.set_arrow(1, 5)
                    new_width_1 = mask_designer_page.brush_mask.transparency.get_value()
                    logger(new_width_1)
                    if new_width_1 == '70%':
                        # draw on canvas
                        mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_left()
                        # snapshot
                        preview_wnd = tips_area_page.snapshot(
                            locator=L.mask_designer.mask_property.brush_mask_designer.preview_area,
                            file_name=Auto_Ground_Truth_Folder + 'G5.2.3.2.3_Brush_Mask_Designer_Transparency_Reduce_Value_By_Arrow.png')
                        logger(preview_wnd)
                        compare_result_arrow1 = tips_area_page.compare(
                            Ground_Truth_Folder + 'G5.2.3.2.3_Brush_Mask_Designer_Transparency_Reduce_Value_By_Arrow.png',
                            preview_wnd, similarity=0.8)
                        logger(compare_result_arrow1)
                        result2 = compare_result_arrow1
                        logger(result2)
                    else:
                        result2 = False
                        logger(result2)

                    case.result = result1 and result2

            case.result = compare_result_flat

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        # 2/16
        with uuid("f1029b10-53b0-4f9d-8890-76cd1b284e56") as case:
            # session 5.2 : Brush Mask Designer > Tools
            # case5.2.1.3 : Pen Style > Smart brush
            # Import animated png (GIF) into media room > Enter Mask Designer
            time.sleep(DELAY_TIME * 5)
            main_page.set_project_aspect_ratio_1_1()
            import_media = media_room_page.import_media_file(
                Test_Material_Folder + 'Mask_Designer_v20/1_1_S10_hevc.mp4')
            logger(import_media)
            time.sleep(DELAY_TIME * 2)
            media_room_page.high_definition_video_confirm_dialog_click_no()
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('1_1_S10_hevc.mp4')
            main_page.insert_media("1_1_S10_hevc.mp4")
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 4)

            # Enter brush mask designer
            mask_designer_page.click_create_brush_mask_btn()
            time.sleep(DELAY_TIME * 2)
            enter_brush_mask_designer = mask_designer_page.is_enter_brush_mask_designer()
            logger(enter_brush_mask_designer)
            if enter_brush_mask_designer:
                # Switch pen tool to "Smart brush"
                # mask_designer_page.brush_mask.width.set_value('60') # will cause a bug that unable to undo /redo by hotkey after operating by the page function
                mask_designer_page.brush_mask.tools.set_smart_brush()

                # switch brush mode (need new page function)

                # 2/16
                with uuid("06a5a326-f6c4-4cba-8e36-9a34054b306a") as case:
                    # session 5.2 : Brush Mask Designer > Tools
                    # Case 5.2.2.1.2 : Width > Value > Min(4)
                    mask_designer_page.brush_mask.width.adjust_slider(0)
                    new_width = mask_designer_page.brush_mask.width.get_value()
                    logger(new_width)
                    if new_width == '4':
                        result1 = True
                        logger(result1)

                        # draw on canvas
                        mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_right()

                        # snapshot
                        preview_wnd = tips_area_page.snapshot(
                            locator=L.mask_designer.mask_property.brush_mask_designer.preview_area,
                            file_name=Auto_Ground_Truth_Folder + 'G5.2.2.1.2_Brush_Mask_Designer_Minimize_SmartBrush.png')
                        logger(preview_wnd)
                        compare_result_brush = tips_area_page.compare(
                            Ground_Truth_Folder + 'G5.2.2.1.2_Brush_Mask_Designer_Minimize_SmartBrush.png',
                            preview_wnd, similarity=0.8)
                        logger(compare_result_brush)

                    else:
                        result1 = False
                        logger(result1)

                    case.result = result1 and compare_result_brush

                # 2/16
                with uuid("33415c9b-350a-41b7-a595-f801d26ff407") as case:
                    # session 5.2 : Brush Mask Designer > Tools
                    # Case 5.2.2.1.3 : Width > Value > Max(100)
                    mask_designer_page.brush_mask.width.adjust_slider(100)
                    new_width = mask_designer_page.brush_mask.width.get_value()
                    logger(new_width)
                    if new_width == '100':
                        result1 = True
                        logger(result1)

                        # draw on canvas
                        mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_left()

                        # snapshot
                        preview_wnd = tips_area_page.snapshot(
                            locator=L.mask_designer.mask_property.brush_mask_designer.preview_area,
                            file_name=Auto_Ground_Truth_Folder + 'G5.2.2.1.3_Brush_Mask_Designer_Max_SmartBrush.png')
                        logger(preview_wnd)
                        compare_result_brush = tips_area_page.compare(
                            Ground_Truth_Folder + 'G5.2.2.1.3_Brush_Mask_Designer_Max_SmartBrush.png',
                            preview_wnd, similarity=0.8)
                        logger(compare_result_brush)

                    else:
                        result1 = False
                        logger(result1)

                    case.result = result1 and compare_result_brush

                # 2/16
                with uuid("4f79906b-1e84-4566-b868-54c059d1a4b3") as case:
                    # session 5.2 : Brush Mask Designer > Tools
                    # Case 5.2.3.2.2 : Transparency of tracing paper > Adjustment > By input value
                    mask_designer_page.brush_mask.transparency.set_value(30)
                    new_tracing_paper_of_transparency = mask_designer_page.brush_mask.transparency.get_value()
                    logger(new_tracing_paper_of_transparency)
                    if new_tracing_paper_of_transparency == '30%':
                        result1 = True
                        logger(result1)
                        # snapshot
                        preview_wnd = tips_area_page.snapshot(
                            locator=L.mask_designer.mask_property.brush_mask_designer.preview_area,
                            file_name=Auto_Ground_Truth_Folder + 'G5.2.3.2.2_Brush_Mask_Designer_SmartBrush_Transparency.png')
                        logger(preview_wnd)
                        compare_result_brush1 = tips_area_page.compare(
                            Ground_Truth_Folder + 'G5.2.3.2.2_Brush_Mask_Designer_SmartBrush_Transparency.png',
                            preview_wnd, similarity=0.8)
                        logger(compare_result_brush1)
                        case.result = result1 and compare_result_brush1
                    else:
                        case.result = False

                # 2/16
                with uuid("b23adcab-f54c-4531-bef6-7289dbef6bd2") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # Case 5.3.2.1.1 : Zoom > Zoom button > [-] button
                    mask_designer_page.brush_mask.click_zoom_out(1) # switch to 45%
                    time.sleep(DELAY_TIME * 2)

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.2.1.1_Brush_Mask_Designer_Zoom_Out.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.2.1.1_Brush_Mask_Designer_Zoom_Out.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result)

                    case.result = compare_result

                # 2/16
                with uuid("0f4b10b1-4e0f-4200-9d14-41a188ae2200") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # Case 5.3.2.1.2 : Zoom > Zoom button > [+] button
                    mask_designer_page.brush_mask.click_zoom_in(3) # switch to 75%
                    time.sleep(DELAY_TIME * 2)

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.2.1.2_Brush_Mask_Designer_Zoom_In.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.2.1.2_Brush_Mask_Designer_Zoom_In.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result)

                    case.result = compare_result

                # 2/16
                with uuid("4478bda6-3a54-46d0-bedc-cead7c1fd976") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # Case 5.3.1.2 : Control button > Undo
                    mask_designer_page.brush_mask.click_undo()
                    time.sleep(DELAY_TIME * 2)

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.1.2_Brush_Mask_Designer_Undo.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.1.2_Brush_Mask_Designer_Undo.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result)

                    case.result = compare_result

                # 2/16
                with uuid("851414b4-7ad6-40c6-93d7-f624458d0b7d") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # Case 5.3.1.3 : Control button > Redo
                    mask_designer_page.brush_mask.click_redo()
                    time.sleep(DELAY_TIME * 2)

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.1.3_Brush_Mask_Designer_Redo.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.1.3_Brush_Mask_Designer_Redo.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result)

                    case.result = compare_result

                # 2/16
                with uuid("b565ef93-2a01-4052-bdf3-5cfb7d382b9b") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # Case 5.3.2.2.1 : Zoom > Zoom menu > Fit
                    mask_designer_page.brush_mask.click_viewer_zoom_menu('Fit')
                    time.sleep(DELAY_TIME * 2)

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.2.2.1_Brush_Mask_Designer_Zoom_Menu_Fit.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.2.2.1_Brush_Mask_Designer_Zoom_Menu_Fit.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result)

                    case.result = compare_result

                # 2/16
                with uuid("e32f02c7-4dac-41b6-9384-8eb534658bfa") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # Case 5.3.2.2.3 : Zoom > Zoom menu > 25%
                    mask_designer_page.brush_mask.click_viewer_zoom_menu('25%')
                    time.sleep(DELAY_TIME * 2)

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.2.2.3_Brush_Mask_Designer_Zoom_Menu_25%.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.2.2.3_Brush_Mask_Designer_Zoom_Menu_25%.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result)

                    case.result = compare_result

                # 2/18
                with uuid("e6e7ec42-f2c6-4e24-bf17-46291c423270") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # Case 5.3.2.2.5 : Zoom > Zoom menu > 75%
                    mask_designer_page.brush_mask.click_viewer_zoom_menu('75%')
                    time.sleep(DELAY_TIME * 2)

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.2.2.5_Brush_Mask_Designer_Zoom_Menu_75%.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.2.2.5_Brush_Mask_Designer_Zoom_Menu_75%.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result)

                    case.result = compare_result

                # 2/18
                with uuid("e63d5ddf-7745-458d-8c56-bbcca0e801d8") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # Case 5.3.2.2.7 : Zoom > Zoom menu > 200%
                    mask_designer_page.brush_mask.click_viewer_zoom_menu('200%')
                    time.sleep(DELAY_TIME * 2)

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.2.2.7_Brush_Mask_Designer_Zoom_Menu_200%.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.2.2.7_Brush_Mask_Designer_Zoom_Menu_200%.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result)

                    case.result = compare_result

                # 2/18
                with uuid("0d769031-c071-4ca5-97d2-572e07c28b2b") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # Case 5.3.2.2.9 : Zoom > Zoom menu > 400%
                    mask_designer_page.brush_mask.click_viewer_zoom_menu('400%')
                    time.sleep(DELAY_TIME * 2)

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.2.2.9_Brush_Mask_Designer_Zoom_Menu_400%.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.2.2.9_Brush_Mask_Designer_Zoom_Menu_400%.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result)

                    case.result = compare_result

                case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        # 2/22
        with uuid("bb98fb8e-75c3-49fe-a55f-8a942005206d") as case:
            # session 5.3 : Brush Mask Designer > Canvas
            # case5.3.3.3 : Preview Control > Set timecode
            # import 16:9 video and insert to track1
            time.sleep(DELAY_TIME * 5)
            main_page.set_project_aspect_ratio_16_9()
            import_media = media_room_page.import_media_file(
                Test_Material_Folder + 'Crop_Zoom_Pan/AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')
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
            time.sleep(DELAY_TIME * 1)
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 4)

            # Enter brush mask designer
            mask_designer_page.click_create_brush_mask_btn()
            time.sleep(DELAY_TIME * 2)
            enter_brush_mask_designer = mask_designer_page.is_enter_brush_mask_designer()
            logger(enter_brush_mask_designer)
            if enter_brush_mask_designer:
                # set timecode
                set_timecode = mask_designer_page.brush_mask.set_timecode('00_00_29_13')
                logger(set_timecode)
                time.sleep(DELAY_TIME * 2)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.mask_designer.mask_property.brush_mask_designer.window,
                    file_name=Auto_Ground_Truth_Folder + 'G5.3.3.3_Brush_Mask_Designer_After_Seeking.png')
                logger(preview_wnd)
                compare_result0 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G5.3.3.3_Brush_Mask_Designer_After_Seeking.png',
                    preview_wnd, similarity=0.8)
                logger(compare_result0)

                # get timecode
                get_timecode = mask_designer_page.brush_mask.get_timecode_slidebar()
                logger(get_timecode)

                if get_timecode == '00;00;29;13':
                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.3.3_Brush_Mask_Designer_Set_Timecode.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.3.3_Brush_Mask_Designer_Set_Timecode.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result)
                else:
                    case.result = False

                # 2/22
                with uuid("0ab4080e-03ad-4205-abb1-d9aeea0643c3") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # case5.3.3.1 : Preview Control > Previous frame
                    check_result = mask_designer_page.brush_mask.click_previous_frame(3)
                    logger(check_result)
                    time.sleep(DELAY_TIME * 2)
                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.3.1_Brush_Mask_Designer_Previous_Frame.png')
                    logger(preview_wnd)
                    compare_result1 = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.3.1_Brush_Mask_Designer_Previous_Frame.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result1)

                    case.result = compare_result1

                # 2/22
                with uuid("c1262c1c-3d86-491f-a8ed-2badc1fde1d7") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # Case 5.3.2.2.2 : Zoom > Zoom menu > 10%
                    mask_designer_page.brush_mask.click_viewer_zoom_menu('10%')
                    time.sleep(DELAY_TIME * 2)

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.2.2.2_Brush_Mask_Designer_Zoom_Menu_10%.png')
                    logger(preview_wnd)
                    compare_result1 = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.2.2.2_Brush_Mask_Designer_Zoom_Menu_10%.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result1)

                    case.result = compare_result1

                # 2/22
                with uuid("42170343-e78b-4ee2-8a69-03aaa041487c") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # Case 5.3.2.2.4 : Zoom > Zoom menu > 50%
                    mask_designer_page.brush_mask.click_viewer_zoom_menu('50%')
                    time.sleep(DELAY_TIME * 2)

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.2.2.4_Brush_Mask_Designer_Zoom_Menu_50%.png')
                    logger(preview_wnd)
                    compare_result1 = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.2.2.4_Brush_Mask_Designer_Zoom_Menu_50%.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result1)

                    case.result = compare_result1

                # 2/22
                with uuid("082b94d5-06d6-4ea0-8ddc-6eab08be626d") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # Case 5.3.2.2.6 : Zoom > Zoom menu > 100%
                    mask_designer_page.brush_mask.click_viewer_zoom_menu('100%')
                    time.sleep(DELAY_TIME * 2)

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.2.2.6_Brush_Mask_Designer_Zoom_Menu_100%.png')
                    logger(preview_wnd)
                    compare_result1 = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.2.2.6_Brush_Mask_Designer_Zoom_Menu_100%.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result1)

                    case.result = compare_result1

                # 2/22
                with uuid("e8123b5c-fda0-479b-abe5-0f64cdc83cdc") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # Case 5.3.2.2.8 : Zoom > Zoom menu > 300%
                    mask_designer_page.brush_mask.click_viewer_zoom_menu('300%')
                    time.sleep(DELAY_TIME * 2)

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.2.2.8_Brush_Mask_Designer_Zoom_Menu_300%.png')
                    logger(preview_wnd)
                    compare_result1 = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.2.2.8_Brush_Mask_Designer_Zoom_Menu_300%.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result1)

                    # switch back to 'Fit'
                    time.sleep(DELAY_TIME * 1)
                    mask_designer_page.brush_mask.click_viewer_zoom_menu('Fit')

                    case.result = compare_result1

                # 2/22
                with uuid("e1ef69dd-43e1-4900-84a2-405f709dbb56") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # case5.3.3.2 : Preview Control > Next frame
                    check_result = mask_designer_page.brush_mask.click_next_frame(2)
                    logger(check_result)
                    time.sleep(DELAY_TIME * 2)
                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.mask_designer.mask_property.brush_mask_designer.window,
                        file_name=Auto_Ground_Truth_Folder + 'G5.3.3.2_Brush_Mask_Designer_Next_Frame.png')
                    logger(preview_wnd)
                    compare_result2 = tips_area_page.compare(
                        Ground_Truth_Folder + 'G5.3.3.2_Brush_Mask_Designer_Next_Frame.png',
                        preview_wnd, similarity=0.8)
                    logger(compare_result2)

                    case.result = compare_result2

                # 2/22
                with uuid("77bc53dd-8a9a-47a6-b4cc-b1cf43000361") as case:
                    # session 5.3 : Brush Mask Designer > Canvas
                    # Case 5.3.1.1 : Control button > Reset button
                    # Set brush width
                    mask_designer_page.brush_mask.width.set_value(70)
                    new_width = mask_designer_page.brush_mask.width.get_value()
                    logger(new_width)
                    if new_width == '70':
                        result1 = True
                        logger(result1)
                        # draw on canvas
                        mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_right()
                        # snapshot
                        preview_wnd = tips_area_page.snapshot(
                            locator=L.mask_designer.mask_property.brush_mask_designer.window,
                            file_name=Auto_Ground_Truth_Folder + 'G5.3.1.1_Brush_Mask_Designer_Draw.png')
                        logger(preview_wnd)
                        compare_result3 = tips_area_page.compare(
                            Ground_Truth_Folder + 'G5.3.1.1_Brush_Mask_Designer_Draw.png',
                            preview_wnd, similarity=0.8)
                        logger(compare_result3)
                        # reset
                        mask_designer_page.brush_mask.click_reset()
                        time.sleep(DELAY_TIME * 1)
                        main_page.press_enter_key()
                        time.sleep(DELAY_TIME * 1)
                        # snapshot
                        preview_wnd = tips_area_page.snapshot(
                            locator=L.mask_designer.mask_property.brush_mask_designer.window,
                            file_name=Auto_Ground_Truth_Folder + 'G5.3.1.1_Brush_Mask_Designer_Reset.png')
                        logger(preview_wnd)
                        compare_result4 = tips_area_page.compare(
                            Ground_Truth_Folder + 'G5.3.1.1_Brush_Mask_Designer_Reset.png',
                            preview_wnd, similarity=0.8)
                        logger(compare_result4)

                    case.result = compare_result3 and compare_result4

                # 2/22
                with uuid("e47112c8-a52f-4da3-a25c-feee557a8f8d") as case:
                    # session 5.4 : Brush Mask Designer > Confirmation
                    # Case 5.4.2 : Confirmation > Cancel button
                    # click [Cancel] button to leave brush mask designer directly
                    mask_designer_page.brush_mask.click_cancel_btn()
                    time.sleep(DELAY_TIME * 1)
                    enter_brush_mask_designer = mask_designer_page.is_enter_brush_mask_designer()
                    logger(enter_brush_mask_designer)
                    if enter_brush_mask_designer == False:
                        # Return True if quit brush mask designer correctly
                        test_result1 = True
                        logger(test_result1)

                        # Enter brush mask designer again
                        mask_designer_page.click_create_brush_mask_btn()
                        time.sleep(DELAY_TIME * 2)
                        enter_brush_mask_designer = mask_designer_page.is_enter_brush_mask_designer()
                        logger(enter_brush_mask_designer)

                        # Draw on canvas and then click [Cancel]
                        mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_right()
                        time.sleep(DELAY_TIME)
                        mask_designer_page.brush_mask.click_cancel_btn()
                        time.sleep(DELAY_TIME * 2)

                        # Handle confirmation dialogue by click [Yes] to save editing result
                        mask_designer_page.brush_mask.close_dialog.click_yes()
                        time.sleep(DELAY_TIME)

                        # snapshot
                        preview_wnd = tips_area_page.snapshot(
                            locator=L.mask_designer.preview_window,
                            file_name=Auto_Ground_Truth_Folder + 'G5.4.2_Brush_Mask_Designer_Confirmation_Yes.png')
                        logger(preview_wnd)
                        compare_result5 = tips_area_page.compare(
                            Ground_Truth_Folder + 'G5.4.2_Brush_Mask_Designer_Confirmation_Yes.png',
                            preview_wnd)
                        logger(compare_result5)

                    else:
                        test_result1 = False
                        logger(test_result1)

                    case.result = test_result1 and compare_result5

                # 2/22
                with uuid("bbe59541-9ecc-460c-adef-0a0aecb673eb") as case:
                    # session 5.4 : Brush Mask Designer > Confirmation
                    # Case 5.4.1 : Confirmation > OK button
                    # click [OK] button to save editing and leave brush mask designer directly
                    # Enter brush mask designer again
                    mask_designer_page.click_create_brush_mask_btn()
                    time.sleep(DELAY_TIME * 2)
                    enter_brush_mask_designer = mask_designer_page.is_enter_brush_mask_designer()
                    logger(enter_brush_mask_designer)
                    if enter_brush_mask_designer:
                        # Draw on canvas and then click [OK]
                        mask_designer_page.brush_mask.drag_tool_on_canvas_from_upper_left()
                        time.sleep(DELAY_TIME)
                        mask_designer_page.brush_mask.click_ok_btn()
                        time.sleep(DELAY_TIME * 2)
                        # check if brush mask designer closed correctly
                        enter_brush_mask_designer = mask_designer_page.is_enter_brush_mask_designer()
                        logger(enter_brush_mask_designer)
                        if enter_brush_mask_designer == False:
                            # snapshot
                            preview_wnd = tips_area_page.snapshot(
                                locator=L.mask_designer.preview_window,
                                file_name=Auto_Ground_Truth_Folder + 'G5.4.1_Brush_Mask_Designer_After_Click_OK.png')
                            logger(preview_wnd)
                            compare_result6 = tips_area_page.compare(
                                Ground_Truth_Folder + 'G5.4.1_Brush_Mask_Designer_After_Click_OK.png',
                                preview_wnd)
                            logger(compare_result6)
                            case.result = compare_result6
                        else:
                            case.result = False

            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        # 2/22
        with uuid("b14c99d7-de8d-49d5-ab87-f0dfe06c2d65") as case:
            # session 6.1 : Motion > Path
            # case 6.1.1.1 : Category > All path
            # import 16:9 video and insert to track1
            time.sleep(DELAY_TIME * 5)
            main_page.set_project_aspect_ratio_16_9()
            import_media = media_room_page.import_media_file(
                Test_Material_Folder + 'Crop_Zoom_Pan/AVC(16_9, 1920x1056, 23.976)_AAC(6ch).mov')
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
            time.sleep(DELAY_TIME * 1)
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 4)

            # Apply one of mask template to clip
            mask_designer_page.MaskDesigner_Apply_template(8)
            time.sleep(DELAY_TIME)

            # select [Motion] tab
            mask_designer_page.switch_to_motion()

            # get category
            category = mask_designer_page.motion.get_current_category()
            logger(category)
            if category == 'All Paths':
                result = True
                logger(result)

                # apply specific template
                mask_designer_page.motion.select_path_template(9)
                time.sleep(DELAY_TIME)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.mask_designer.property_frame,
                    file_name=Auto_Ground_Truth_Folder + 'G6.1.1.1_Mask_Designer_Motion_Tab_All_Paths.png')
                logger(preview_wnd)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G6.1.1.1_Mask_Designer_Motion_Tab_All_Paths.png',
                    preview_wnd)
                logger(compare_result)
            else:
                result = False
                logger(result)

            case.result = result and compare_result



        # 2/22
        with uuid("97aa2a65-69f0-4c84-b165-e3af2e5458b8") as case:
            # session 6.1 : Motion > Path
            # case 6.1.2.1 : Custom Path > Save
            # click [Save modified mask motion...] button
            click_save_mask_btn = mask_designer_page.motion.click_save_custom_btn()
            logger(click_save_mask_btn)
            time.sleep(DELAY_TIME)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.mask_designer.property_frame,
                file_name=Auto_Ground_Truth_Folder + 'G6.1.2.1_Mask_Designer_Motion_Tab_Save_Modified_Mask_Motion.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G6.1.2.1_Mask_Designer_Motion_Tab_Save_Modified_Mask_Motion.png',
                preview_wnd)
            logger(compare_result)

            case.result = compare_result

        # 2/22
        with uuid("03d79014-8219-4244-9033-ebada7026882") as case:
            # session 6.1 : Motion > Path
            # case 6.1.1.2 : Category > Default Paths
            # Switch category to "Default Paths"
            mask_designer_page.motion.select_category('default')
            time.sleep(DELAY_TIME * 1)

            # get category
            category = mask_designer_page.motion.get_current_category()
            logger(category)
            if category == 'Default Paths':
                result = True
                logger(result)
                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.mask_designer.property_frame,
                    file_name=Auto_Ground_Truth_Folder + 'G6.1.1.2_Mask_Designer_Motion_Tab_Default_Paths.png')
                logger(preview_wnd)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G6.1.1.2_Mask_Designer_Motion_Tab_Default_Paths.png',
                    preview_wnd)
                logger(compare_result)
            else:
                result = False
                logger(result)

            case.result = result and compare_result

        # 2/22
        with uuid("76f5c39c-1e18-45a6-af41-2a62cbb733bf") as case:
            # session 6.1 : Motion > Path
            # case 6.1.1.3 : Category > Custom Paths
            # Switch category to "Custom Paths"
            mask_designer_page.motion.select_category('custom')
            time.sleep(DELAY_TIME * 1)

            # get category
            category = mask_designer_page.motion.get_current_category()
            logger(category)
            if category == 'Custom Paths':
                result = True
                logger(result)
                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.mask_designer.property_frame,
                    file_name=Auto_Ground_Truth_Folder + 'G6.1.1.3_Mask_Designer_Motion_Tab_Custom_Paths.png')
                logger(preview_wnd)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G6.1.1.3_Mask_Designer_Motion_Tab_Custom_Paths.png',
                    preview_wnd)
                logger(compare_result)
            else:
                result = False
                logger(result)

            case.result = result and compare_result

        # 2/22
        with uuid("b3b12a33-5928-497f-9142-4745dee376d1") as case:
            # session 6.1 : Motion > Path
            # case 6.1.2.2 : Custom Path > Remove
            # Select custom mask motion object
            mask_designer_page.motion.select_path_template(2)
            time.sleep(DELAY_TIME)

            # Right click on the mask and then remove it
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Remove Path')
            logger(context_menu)
            time.sleep(DELAY_TIME * 2)

            # snapshot1
            preview_wnd = tips_area_page.snapshot(
                locator=L.mask_designer.property_frame,
                file_name=Auto_Ground_Truth_Folder + 'G6.1.2.2_Mask_Designer_Motion_Tab_Remove_Template_Warning.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G6.1.2.2_Mask_Designer_Motion_Tab_Remove_Template_Warning.png',
                preview_wnd)
            logger(compare_result)

            # Confirm to remove template
            time.sleep(DELAY_TIME * 1)
            main_page.press_enter_key()
            time.sleep(DELAY_TIME * 2)

            # snapshot2
            preview_wnd = tips_area_page.snapshot(
                locator=L.mask_designer.property_frame,
                file_name=Auto_Ground_Truth_Folder + 'G6.1.2.2_Mask_Designer_Motion_Tab_Remove_Template.png')
            logger(preview_wnd)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G6.1.2.2_Mask_Designer_Motion_Tab_Remove_Template.png',
                preview_wnd)
            logger(compare_result1)

            case.result = compare_result and compare_result1

        # 2/22
        with uuid("e2bc6935-da7e-4df2-9bab-91c9783c874d") as case:
            # session 6.2 : Motion > Manual Adjustment
            # case 6.2.1 : Manual adjustment on Canvas
            # Drag and drop to adjust path on canvas correctly
            mask_designer_page.adjust_object_on_canvas_resize(10, 30)
            time.sleep(DELAY_TIME * 1)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + 'G6.2.1_Mask_Designer_Motion_Tab_Adjust_On_Canvas.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G6.2.1_Mask_Designer_Motion_Tab_Adjust_On_Canvas.png',
                preview_wnd)
            logger(compare_result)

            # seek
            mask_designer_page.set_MaskDesigner_timecode("00_00_07_29")
            time.sleep(DELAY_TIME * 2)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.mask_designer.preview_window,
                file_name=Auto_Ground_Truth_Folder + 'G6.2.1_Mask_Designer_Motion_Tab_Adjust_On_Canvas_1.png')
            logger(preview_wnd)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G6.2.1_Mask_Designer_Motion_Tab_Adjust_On_Canvas_1.png',
                preview_wnd)
            logger(compare_result1)

            case.result = compare_result and compare_result1

