import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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
download_from_cl_dz_page = PageFactory().get_page_object('download_from_cl_dz_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
transition_room_page = PageFactory().get_page_object('transition_room_page', mwc)
title_designer_page = PageFactory().get_page_object('title_designer_page', mwc)
crop_zoom_pan_page = PageFactory().get_page_object('crop_zoom_pan_page', mwc)
pan_zoom_page = PageFactory().get_page_object('pan_zoom_page', mwc)
timeline_page = PageFactory().get_page_object('timeline_operation_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
particle_designer_page = PageFactory().get_page_object('particle_designer_page', mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)
mask_designer_page = PageFactory().get_page_object('mask_designer_page', mwc)
gettyimage_page = PageFactory().get_page_object('gettyimage_page', mwc)
library_preview_page = PageFactory().get_page_object('library_preview_page', mwc)
shape_designer_page = PageFactory().get_page_object('shape_designer_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Shape Designer.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Shape_Designer/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Shape_Designer/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Shape_Designer():
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
            google_sheet_execution_log_init('Shape_Designer')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"shape designer result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
    def test1_1_8_1(self):
        # entry PiP Room New template
        with uuid("607981b2-a3a8-4dba-816d-785eae7d174f") as case:
            with uuid("43a0ffa7-38d6-403b-ae3b-e94db30ef71b") as case:
                main_page.enter_room(4)
                pip_room_page.click_CreateNewShape_btn()
                time.sleep(DELAY_TIME * 3)
                preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                             file_name=Auto_Ground_Truth_Folder + 'G8.1.0_Shape_Designer_NewCreate.png')
                image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.1.0_Shape_Designer_NewCreate.png',
                    preview_result)
                case.result = image_result

        # restore down
        with uuid("5cc51fc3-b1d8-4c73-92a3-7fc7bf855f1c") as case:
            shape_designer_page.click_restore_btn()
            time.sleep(DELAY_TIME * 3)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G8.1.1_Shape_Designer_Maximize.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.1.1_Shape_Designer_Maximize.png',
                    preview_result)
            case.result = image_result

        # click esc to close
        with uuid("f87624f7-79ed-4384-adf8-d908d213fda7") as case:
            time.sleep(DELAY_TIME * 3)

            shape_designer_page.press_esc_key()
            time.sleep(DELAY_TIME * 3)
            shape_designer_elem = main_page.exist(L.shape_designer.designer_window)
            if shape_designer_elem:
                case.result = False
            else:
                case.result = True


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_8_2(self):
        # entry PiP Room modify template
        with uuid("432d9bbb-af16-4ebf-905b-10f412b09e3f") as case:
            with uuid("48a4a4f2-01e6-4e97-acb1-d0ac844fe542") as case:
                main_page.enter_room(4)
                time.sleep(DELAY_TIME * 3)
                pip_room_page.select_LibraryRoom_category('Shape')
                pip_room_page.hover_library_media('Shape 001')
                pip_room_page.left_click()
                pip_room_page.click_ModifySelectedPiP_btn()
                time.sleep(DELAY_TIME * 3)
                preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                              file_name=Auto_Ground_Truth_Folder + 'G8.2.0_Shape_Designer_Modify_btn.png')
                image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.2.0_Shape_Designer_Modify_btn.png',
                                                           preview_result)
                case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_8_3(self):
        # entry PiP Room double click to modify template
        with uuid("432d9bbb-af16-4ebf-905b-10f412b09e3f") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 3)
            pip_room_page.select_LibraryRoom_category('Shape')
            pip_room_page.hover_library_media('Shape 001')
            pip_room_page.left_click()
            pip_room_page.double_click()
            time.sleep(DELAY_TIME * 3)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.3.0_Shape_Designer_DoubleClick_Modify.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.3.0_Shape_Designer_DoubleClick_Modify.png',
                                                        preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_8_4(self):
        # entry PiP Room right click menu to modify template
        with uuid("00b7e30b-53c1-4db9-a84e-a873ce71dea6") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 3)
            pip_room_page.select_LibraryRoom_category('Shape')
            pip_room_page.hover_library_media('Shape 001')
            pip_room_page.right_click()
            pip_room_page.select_right_click_menu("Modify Template")
            time.sleep(DELAY_TIME * 3)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.4.0_Shape_Designer_RightClick_Modify.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.4.0_Shape_Designer_RightClick_Modify.png',
                                                        preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_8_5(self):
        # tips area tools to enter shape designer
        with uuid("87af8082-b8ca-4211-a978-0e3827d93b36") as case:
            with uuid("c6936e43-6b26-445a-a7e5-e51f4a8b10a8") as case:
                main_page.enter_room(4)
                time.sleep(DELAY_TIME * 3)
                pip_room_page.select_LibraryRoom_category('Shape')
                pip_room_page.hover_library_media('Shape 001')
                pip_room_page.right_click()
                pip_room_page.select_right_click_menu("Add to Timeline")
                tips_area_page.tools.select_Shape_Designer()
                time.sleep(DELAY_TIME * 3)
                preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                                file_name=Auto_Ground_Truth_Folder + 'G8.5.0_Shape_Designer_Timeline_Tools_Modify.png')
                image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.5.0_Shape_Designer_Timeline_Tools_Modify.png',
                                                            preview_result)
                case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_8_6(self):
        # tips area more features to enter shape designer
        with uuid("92c626f8-9d86-4488-b88b-761c471abf59") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 3)
            pip_room_page.select_LibraryRoom_category('Shape')
            pip_room_page.hover_library_media('Shape 001')
            pip_room_page.right_click()
            pip_room_page.select_right_click_menu("Add to Timeline")
            tips_area_page.more_features.edit_Shape_Designer()
            time.sleep(DELAY_TIME * 3)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.6.0_Shape_Designer_Timeline_MoreFeatures_Modify.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.6.0_Shape_Designer_Timeline_MoreFeatures_Modify.png',
                                                            preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_8_7(self):
        # hotkey f2 to enter shape designer
        with uuid("3aa32fa3-ebd1-4fe8-8d87-64938a07918c") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 3)
            pip_room_page.select_LibraryRoom_category('Shape')
            pip_room_page.hover_library_media('Shape 001')
            pip_room_page.right_click()
            pip_room_page.select_right_click_menu("Add to Timeline")
            particle_designer_page.press_hotkey_enter_designer()
            time.sleep(DELAY_TIME * 3)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.7.0_Shape_Designer_Timeline_Hotkey_Modify.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.7.0_Shape_Designer_Timeline_Hotkey_Modify.png',
                                                            preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_8_8(self):
        # timeline right click to enter shape designer
        with uuid("045aa197-dc50-47f6-83af-ce1ee3964830") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 3)
            pip_room_page.select_LibraryRoom_category('Shape')
            pip_room_page.hover_library_media('Shape 001')
            pip_room_page.right_click()
            pip_room_page.select_right_click_menu("Add to Timeline")
            timeline_page.select_timeline_media(track_index=0, clip_index=0)
            timeline_operation_page.right_click()
            timeline_operation_page.select_right_click_menu('Edit in Shape Designer...')
            time.sleep(DELAY_TIME * 3)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.8.0_Shape_Designer_Timeline_RightClick_Modify.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.8.0_Shape_Designer_Timeline_RightClick_Modify.png',
                                                            preview_result)
            case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_8_9(self):
        # timeline double click to enter shape designer
        with uuid("b0b735ef-9e7c-4ea8-bf3f-77d3d9b8cd7e") as case:
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 3)
            pip_room_page.select_LibraryRoom_category('Shape')
            pip_room_page.hover_library_media('Shape 001')
            pip_room_page.right_click()
            pip_room_page.select_right_click_menu("Add to Timeline")
            timeline_page.select_timeline_media(track_index=0, clip_index=0)
            timeline_operation_page.double_click()
            time.sleep(DELAY_TIME * 3)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.9.0_Shape_Designer_Timeline_DoubleClick_Modify.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.9.0_Shape_Designer_Timeline_DoubleClick_Modify.png',
                                                            preview_result)
            case.result = image_result

        # shape designer x to close
        with uuid("57de5769-edbf-4e4a-b7e2-5af5a898cb81") as case:
            shape_designer_page.click_close_btn()
            time.sleep(DELAY_TIME * 3)
            preview_result = shape_designer_page.snapshot(locator=L.library_preview.upper_view_region,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.9.1_Shape_Designer_X.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.9.1_Shape_Designer_X.png',
                                                       preview_result)
            case.result = image_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_8_10(self):
        # shape designer unfold shape type
        with uuid("c4557be4-f4c1-4302-b06d-f84a944871ca") as case:
            main_page.enter_room(4)
            pip_room_page.click_CreateNewShape_btn()
            time.sleep(DELAY_TIME * 3)
            shape_designer_page.properties.unfold_shape_type()
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.10.0_Shape_Designer_Unfold_ShapeType.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.10.0_Shape_Designer_Unfold_ShapeType.png',
                preview_result)
            case.result = image_result

        # shape designer unfold shape preset
        with uuid("aab8313e-7295-4a26-87c8-5699f98b8504") as case:
            shape_designer_page.properties.unfold_shape_preset()
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.10.1_Shape_Designer_Unfold_ShapePreset.png')
            image_result = shape_designer_page.compare(
                Ground_Truth_Folder + 'G8.10.1_Shape_Designer_Unfold_ShapePreset.png',
                preview_result)
            case.result = image_result

        # shape designer unfold shape fill
        with uuid("54e51f7a-8b24-4d1c-82b8-5ef76ec6fa9c") as case:
            shape_designer_page.properties.unfold_shape_fill()
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.10.2_Shape_Designer_Unfold_ShapeFill.png')
            image_result = shape_designer_page.compare(
                Ground_Truth_Folder + 'G8.10.2_Shape_Designer_Unfold_ShapeFill.png',
                preview_result)
            case.result = image_result

        # shape designer unfold shape outline
        with uuid("f4c9d921-b1c7-4776-9bd1-ce411c415a8b") as case:
            shape_designer_page.properties.unfold_shape_outline()
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.10.3_Shape_Designer_Unfold_ShapeOutline.png')
            image_result = shape_designer_page.compare(
                Ground_Truth_Folder + 'G8.10.3_Shape_Designer_Unfold_ShapeOutline.png',
                preview_result)
            case.result = image_result

        # shape designer unfold shadow
        with uuid("6ad1cc6b-701b-4cf9-8050-4d46a955214c") as case:
            shape_designer_page.properties.unfold_shadow()
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.10.4_Shape_Designer_Unfold_Shadow.png')
            image_result = shape_designer_page.compare(
                Ground_Truth_Folder + 'G8.10.4_Shape_Designer_Unfold_Shadow.png',
                preview_result)
            case.result = image_result

        # shape designer unfold title
        with uuid("94fdccb9-e18c-4209-9edc-7b92ed6b765d") as case:
            shape_designer_page.properties.unfold_title()
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.10.5_Shape_Designer_Unfold_Title.png')
            image_result = shape_designer_page.compare(
                Ground_Truth_Folder + 'G8.10.5_Shape_Designer_Unfold_Title.png',
                preview_result)
            case.result = image_result

        # shape designer remember folder status
        with uuid("0ea85d8d-76f1-4a65-833a-e72b86166a40") as case:
            with uuid("a46a67b4-38dc-4f12-a3c3-48b49b6eac57") as case:
                with uuid("a96a494a-24a7-4ac5-9b27-c8a364929899") as case:
                    with uuid("da61a499-cc0f-4158-a73b-439dd85d76bd") as case:
                        with uuid("7f7d1a1e-f292-496f-b33b-7f00f63a5f38") as case:
                            shape_designer_page.click_close_btn()
                            time.sleep(DELAY_TIME * 3)
                            pip_room_page.click_CreateNewShape_btn()
                            time.sleep(DELAY_TIME * 3)
                            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.10.6_Shape_Designer_Remember_Fold.png')
                            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.10.6_Shape_Designer_Remember_Fold.png',
                                                            preview_result)
                            case.result = image_result

        # shape designer fold shape type
        with uuid("08f4b576-8205-4a57-b09b-93f66751536f") as case:
            shape_designer_page.properties.unfold_shape_type(0)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.10.7_Shape_Designer_Fold_ShapeType.png')
            image_result = shape_designer_page.compare(
                Ground_Truth_Folder + 'G8.10.7_Shape_Designer_Fold_ShapeType.png',
                preview_result)
            case.result = image_result

        # shape designer fold shape preset
        with uuid("b36133f2-6d70-445a-b1c4-95ffd09953f1") as case:
            shape_designer_page.properties.unfold_shape_preset(0)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.10.8_Shape_Designer_Fold_ShapePreset.png')
            image_result = shape_designer_page.compare(
                Ground_Truth_Folder + 'G8.10.8_Shape_Designer_Fold_ShapePreset.png',
                preview_result)
            case.result = image_result

        # shape designer fold shape fill
        with uuid("93ce05ca-6af6-4fdd-9d22-9a24a186d7a4") as case:
            shape_designer_page.properties.unfold_shape_fill(0)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.10.9_Shape_Designer_Fold_ShapeFill.png')
            image_result = shape_designer_page.compare(
                Ground_Truth_Folder + 'G8.10.9_Shape_Designer_Fold_ShapeFill.png',
                preview_result)
            case.result = image_result

        # shape designer fold shape outline
        with uuid("3ac63d52-bd18-400e-9a6c-26effc326a5e") as case:
            shape_designer_page.properties.unfold_shape_outline(0)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.10.10_Shape_Designer_Fold_ShapeOutline.png')
            image_result = shape_designer_page.compare(
                Ground_Truth_Folder + 'G8.10.10_Shape_Designer_Fold_ShapeOutline.png',
                preview_result)
            case.result = image_result

        # shape designer fold shadow
        with uuid("7dd5148e-4530-48a7-8bcb-fff090cc41c4") as case:
            shape_designer_page.properties.unfold_shadow(0)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.10.11_Shape_Designer_Fold_Shadow.png')
            image_result = shape_designer_page.compare(
                Ground_Truth_Folder + 'G8.10.11_Shape_Designer_Fold_Shadow.png',
                preview_result)
            case.result = image_result

        # shape designer fold title
        with uuid("aa6d9fc5-2008-4b33-bb6d-3778cf2da8b7") as case:
            shape_designer_page.properties.unfold_title(0)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.10.12_Shape_Designer_Fold_Title.png')
            image_result = shape_designer_page.compare(
                Ground_Truth_Folder + 'G8.10.12_Shape_Designer_Fold_Title.png',
                preview_result)
            case.result = image_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_8_11(self):
        # shape designer keyframe tab object settings unfold
        with uuid("9815dcb2-296f-4a1b-88a9-0249a8d5d944") as case:
            main_page.enter_room(4)
            pip_room_page.click_CreateNewShape_btn()
            time.sleep(DELAY_TIME * 3)
            shape_designer_page.click_keyframe_tab()
            time.sleep(DELAY_TIME * 2)
            shape_designer_page.keyframe.object_settings.unfold_menu()
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.11.0_Shape_Designer_Keyframe_Unfold_ObjectSettings.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.11.0_Shape_Designer_Keyframe_Unfold_ObjectSettings.png',
                preview_result)
            case.result = image_result

        # shape designer keyframe tab object settings fold
        with uuid("cd4a577d-ef6e-400b-8f45-7708ab1c1281") as case:
            shape_designer_page.keyframe.object_settings.unfold_menu(0)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.11.1_Shape_Designer_Keyframe_Fold_ObjectSettings.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.11.1_Shape_Designer_Keyframe_Fold_ObjectSettings.png',
                preview_result)
            case.result = image_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_8_12(self):
        # shape designer shape type select 1
        with uuid("c87db17b-54df-434f-8525-47d4221d0a47") as case:
            main_page.enter_room(4)
            pip_room_page.click_CreateNewShape_btn()
            time.sleep(DELAY_TIME * 3)
            shape_designer_page.properties.unfold_shape_type()
            shape_designer_page.properties.shape_type.drag_scroll_bar(0)
            shape_designer_page.properties.shape_type.apply_type(1)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.12.0_Shape_Designer_Select_ShapeType1.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.12.0_Shape_Designer_Select_ShapeType1.png',
                preview_result)
            case.result = image_result

        # shape designer undo
        with uuid("0e3f1b5f-1592-4cf5-8316-315b543dc2c4") as case:
            with uuid("d60dc610-47cc-4273-8d82-504eb8a86678") as case:
                shape_designer_page.click_undo()
                preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                              file_name=Auto_Ground_Truth_Folder + 'G8.12.1_Shape_Designer_Undo.png')
                image_result = shape_designer_page.compare(
                    Ground_Truth_Folder + 'G8.12.1_Shape_Designer_Undo.png',
                    preview_result)
                case.result = image_result

        # shape designer redo
        with uuid("6d95631d-5218-4168-94e7-bd05033c118f") as case:
            with uuid("eadc62e0-4d4b-4c54-b3ff-6125faf756df") as case:
                shape_designer_page.click_redo()
                preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                              file_name=Auto_Ground_Truth_Folder + 'G8.12.2_Shape_Designer_Redo.png')
                image_result = shape_designer_page.compare(
                    Ground_Truth_Folder + 'G8.12.2_Shape_Designer_Redo.png',
                    preview_result)
                case.result = image_result

        # shape designer hotkey undo
        with uuid("a723596c-6bd7-4f46-b685-355525986a71") as case:
            shape_designer_page.tap_Undo_hotkey()
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.12.3_Shape_Designer_UndoHotkey.png')
            image_result = shape_designer_page.compare(
                Ground_Truth_Folder + 'G8.12.3_Shape_Designer_UndoHotkey.png',
                preview_result)
            case.result = image_result

        # shape designer hotkey redo
        with uuid("d891234f-d4cd-4503-af76-4dd5b9845a0a") as case:
            shape_designer_page.tap_Redo_hotkey()
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                          file_name=Auto_Ground_Truth_Folder + 'G8.12.4_Shape_Designer_RedoHotkey.png')
            image_result = shape_designer_page.compare(
                Ground_Truth_Folder + 'G8.12.4_Shape_Designer_RedoHotkey.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 2
        with uuid("2a9620f6-e43f-4989-bed7-632b37545b05") as case:
            shape_designer_page.properties.shape_type.apply_type(2)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.12.5_Shape_Designer_Select_ShapeType2.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.12.5_Shape_Designer_Select_ShapeType2.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 3, linear to linear
        with uuid("38a419ab-7d85-424c-91e7-86c6fb8e1dec") as case:
            with uuid("e8b65fa0-1018-4718-9b19-3ff84ec8ccf7") as case:
                shape_designer_page.properties.shape_type.apply_type(3)
                preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.12.6_Shape_Designer_Select_ShapeType3.png')
                image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.12.6_Shape_Designer_Select_ShapeType3.png',
                    preview_result)
                case.result = image_result

        # shape designer shape type select 4
        with uuid("ca640f3c-29cb-4b92-a74f-65cea95105a2") as case:
            shape_designer_page.properties.shape_type.apply_type(4)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.12.7_Shape_Designer_Select_ShapeType4.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.12.7_Shape_Designer_Select_ShapeType4.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 5
        with uuid("aa205ee1-4b41-4534-9b0b-32d92212cc51") as case:
            shape_designer_page.properties.shape_type.apply_type(5)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.12.8_Shape_Designer_Select_ShapeType5.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.12.8_Shape_Designer_Select_ShapeType5.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 6
        with uuid("14763836-bab5-43d3-a13c-931ac72e3357") as case:
            shape_designer_page.properties.shape_type.apply_type(6)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.12.9_Shape_Designer_Select_ShapeType6.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.12.9_Shape_Designer_Select_ShapeType6.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 7
        with uuid("74968ddd-ec5d-47c4-ba07-c3f90a92da66") as case:
            shape_designer_page.properties.shape_type.apply_type(7)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.12.10_Shape_Designer_Select_ShapeType7.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.12.10_Shape_Designer_Select_ShapeType7.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 8
        with uuid("5990fc54-fef2-4dbf-8451-f9041885936e") as case:
            shape_designer_page.properties.shape_type.apply_type(8)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.12.11_Shape_Designer_Select_ShapeType8.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.12.11_Shape_Designer_Select_ShapeType8.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 10, linear to general
        with uuid("5990fc54-fef2-4dbf-8451-f9041885936e") as case:
            with uuid("0a37b93c-4ef0-490a-a4e8-8d5f886901fb") as case:
                shape_designer_page.properties.shape_type.apply_type(10)
                preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                                file_name=Auto_Ground_Truth_Folder + 'G8.12.12_Shape_Designer_Select_ShapeType10.png')
                image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.12.12_Shape_Designer_Select_ShapeType10.png',
                    preview_result)
                case.result = image_result


        # shape designer shape type select 9, general to linear
        with uuid("eb849961-75da-447a-a379-5117ea82f30b") as case:
            with uuid("6990de9b-601c-48df-988e-7d7b2cad81da") as case:
                shape_designer_page.properties.shape_type.apply_type(9)
                preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                                file_name=Auto_Ground_Truth_Folder + 'G8.12.13_Shape_Designer_Select_ShapeType9.png')
                image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.12.13_Shape_Designer_Select_ShapeType9.png',
                    preview_result)
                case.result = image_result

        # shape designer shape type select line shape fill and title gray out
        with uuid("820f9aa0-6961-4536-8eb7-c7096cd9c345") as case:
            with uuid("de384bfb-28d2-4068-806d-2fae30c1abf7") as case:
                shape_designer_page.properties.unfold_title()
                preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                              file_name=Auto_Ground_Truth_Folder + 'G8.12.14_Shape_Designer_Select_ShapeType_GrayOut.png')
                image_result = shape_designer_page.compare(
                    Ground_Truth_Folder + 'G8.12.14_Shape_Designer_Select_ShapeType_GrayOut.png',
                    preview_result)
                case.result = image_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_8_13(self):
        # shape designer shape type select 11
        with uuid("c87db17b-54df-434f-8525-47d4221d0a47") as case:
            main_page.enter_room(4)
            pip_room_page.click_CreateNewShape_btn()
            time.sleep(DELAY_TIME * 3)
            shape_designer_page.properties.unfold_shape_type()
            shape_designer_page.properties.shape_type.drag_scroll_bar(0)
            shape_designer_page.properties.shape_type.drag_scroll_bar(0.3)
            shape_designer_page.properties.shape_type.apply_type(11)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.13.0_Shape_Designer_Select_ShapeType11.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.0_Shape_Designer_Select_ShapeType11.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 12, general to general
        with uuid("72903a27-808e-4489-8472-8b6eea3bffae") as case:
            with uuid("bf47d787-f1f5-460e-a85a-154e63ffa585") as case:
                shape_designer_page.properties.shape_type.apply_type(12)
                preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                              file_name=Auto_Ground_Truth_Folder + 'G8.13.1_Shape_Designer_Select_ShapeType12.png')
                image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.1_Shape_Designer_Select_ShapeType12.png',
                    preview_result)
                case.result = image_result

        # shape designer shape type select 13
        with uuid("b8b4cb23-958c-4d1c-9cdc-d7340325bd66") as case:
            shape_designer_page.properties.shape_type.apply_type(13)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.13.2_Shape_Designer_Select_ShapeType13.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.2_Shape_Designer_Select_ShapeType13.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 14
        with uuid("f7f8687f-aaa8-4c92-aef7-a18d867809c8") as case:
            shape_designer_page.properties.shape_type.apply_type(14)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G8.13.3_Shape_Designer_Select_ShapeType14.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.3_Shape_Designer_Select_ShapeType14.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 15
        with uuid("60119835-917f-45a9-ac38-b189fb2f0e99") as case:
            shape_designer_page.properties.shape_type.apply_type(15)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G8.13.4_Shape_Designer_Select_ShapeType15.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.4_Shape_Designer_Select_ShapeType15.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 16
        with uuid("a93efdac-2fb2-497e-aaf9-6478faf28ec0") as case:
            shape_designer_page.properties.shape_type.apply_type(16)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G8.13.5_Shape_Designer_Select_ShapeType16.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.5_Shape_Designer_Select_ShapeType16.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 17
        with uuid("4afd7500-4766-43d8-bc54-3078a9012b8f") as case:
            shape_designer_page.properties.shape_type.apply_type(17)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G8.13.6_Shape_Designer_Select_ShapeType17.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.6_Shape_Designer_Select_ShapeType17.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 18
        with uuid("ad4c9024-69bf-4511-8407-97676982fad8") as case:
            shape_designer_page.properties.shape_type.apply_type(18)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G8.13.7_Shape_Designer_Select_ShapeType18.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.7_Shape_Designer_Select_ShapeType18.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 19
        with uuid("b26aaabe-8c12-4782-9227-29158d5535ac") as case:
            shape_designer_page.properties.shape_type.apply_type(19)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G8.13.8_Shape_Designer_Select_ShapeType19.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.8_Shape_Designer_Select_ShapeType19.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 20
        with uuid("5dc6a872-e042-4ea5-a2f9-04714a5e6f62") as case:
            shape_designer_page.properties.shape_type.apply_type(20)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G8.13.9_Shape_Designer_Select_ShapeType20.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.9_Shape_Designer_Select_ShapeType20.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 21
        with uuid("f8e3850f-500d-42de-ac6e-24a1d3170b48") as case:
            shape_designer_page.properties.shape_type.drag_scroll_bar(0)
            shape_designer_page.properties.shape_type.drag_scroll_bar(0.6)
            shape_designer_page.properties.shape_type.apply_type(21)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G8.13.10_Shape_Designer_Select_ShapeType21.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.10_Shape_Designer_Select_ShapeType21.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 22
        with uuid("034667c8-e064-4780-8ce8-fb381f015e5d") as case:
            shape_designer_page.properties.shape_type.apply_type(22)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G8.13.11_Shape_Designer_Select_ShapeType22.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.11_Shape_Designer_Select_ShapeType22.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 23
        with uuid("f55fc58e-7894-4bcc-a785-44edf8be55b1") as case:
            shape_designer_page.properties.shape_type.apply_type(23)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G8.13.12_Shape_Designer_Select_ShapeType23.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.12_Shape_Designer_Select_ShapeType23.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 24
        with uuid("642a02df-2883-4077-a6e8-d6a6e8ea5c57") as case:
            shape_designer_page.properties.shape_type.apply_type(24)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G8.13.13_Shape_Designer_Select_ShapeType24.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.13_Shape_Designer_Select_ShapeType24.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 25
        with uuid("d99ca180-7a6a-4416-8437-4df406ba9dca") as case:
            shape_designer_page.properties.shape_type.apply_type(25)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G8.13.14_Shape_Designer_Select_ShapeType25.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.14_Shape_Designer_Select_ShapeType25.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 26
        with uuid("6bd06afc-87fc-41f2-ac00-b07bb8906d69") as case:
            shape_designer_page.properties.shape_type.apply_type(26)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G8.13.15_Shape_Designer_Select_ShapeType26.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.15_Shape_Designer_Select_ShapeType26.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 27
        with uuid("825bf186-6ba8-4a6c-86cd-6785e2c6fdd7") as case:
            shape_designer_page.properties.shape_type.apply_type(27)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G8.13.16_Shape_Designer_Select_ShapeType27.png')
            image_result = shape_designer_page.compare(Ground_Truth_Folder + 'G8.13.16_Shape_Designer_Select_ShapeType27.png',
                preview_result)
            case.result = image_result

        # shape designer shape type select 28
        with uuid("588f8417-7a1f-4453-add4-f8d5c8ef60b1") as case:
            shape_designer_page.properties.shape_type.apply_type(28)
            preview_result = shape_designer_page.snapshot(locator=L.shape_designer.designer_window,
                                                    file_name=Auto_Ground_Truth_Folder + 'G8.13.17_Shape_Designer_Select_ShapeType28.png')
            image_result = shape_designer_page.compare(
                Ground_Truth_Folder + 'G8.13.17_Shape_Designer_Select_ShapeType28.png',
                preview_result)
            case.result = image_result




















