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
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="PiP Designer_20.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Pip_Designer_20/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Pip_Designer_20/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Pip_Designer_20():
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
            google_sheet_execution_log_init('Pip Designer_20')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"Pip Designer 20 result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        # Enter Pip Room
        main_page.enter_room(4)
        pip_room_page.check_in_Pip_room()
        time.sleep(DELAY_TIME*2)

        # Select template "Wedding 2"
        main_page.select_LibraryRoom_category('Romance')
        main_page.select_library_icon_view_media("Wedding 2")

        # Add to timeline
        main_page.right_click()
        main_page.select_right_click_menu("Add to Timeline")

        # Enter pip designer
        timeline_operation_page.select_timeline_media(0, 0)
        main_page.double_click()
        result = pip_designer_page.get_title()
        if result != 'Wedding 2':
            logger('Not enter pip designer now.')
            raise Exception

        # enter Advance mode > Motion tab
        pip_designer_page.switch_mode('Advanced')
        pip_designer_page.advanced.switch_to_motion()
        pip_designer_page.advanced.unfold_path_menu()

        # [M332] Motion > Default path
        with uuid("7536c52a-e280-491d-a457-fb7607366e17") as case:
            pip_designer_page.path.select_category(option='default')
            time.sleep(DELAY_TIME)
            pip_designer_page.path.select_template(9)
            time.sleep(DELAY_TIME)

            # Verify 1: Timecode (00:00:04:13)
            pip_designer_page.set_timecode('00_00_04_13')
            time.sleep(DELAY_TIME)
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M332_default_template_9.png')

            #logger(current_image)
            check_temp_9 = pip_designer_page.compare(Ground_Truth_Folder + 'M332_default_template_9.png', current_image)

            pip_designer_page.path.select_template(18)
            time.sleep(DELAY_TIME)
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M332_default_template_18.png')

            #logger(current_image)
            check_temp_18 = pip_designer_page.compare(Ground_Truth_Folder + 'M332_default_template_18.png', current_image)

            case.result = check_temp_9 and check_temp_18

        # [M334] Motion > Save Custom path
        with uuid("8b61f9e8-e0ea-49b3-8fc4-fa1fd525078d") as case:
            # On canvas preview: Drag node to custom shape
            x,y = main_page.exist(L.shape_designer.canvas_object_shape).AXPosition
            size_w, size_h = main_page.exist(L.shape_designer.canvas_object_shape).AXSize
            new_x = x + 5
            new_y = y + (size_h*0.5)

            main_page.mouse.move(x, new_y)
            time.sleep(DELAY_TIME*0.5)
            main_page.drag_mouse((x, new_y), (new_x, new_y))
            time.sleep(DELAY_TIME*0.5)

            # click custom button
            check_result = pip_designer_page.path.click_save_custom_btn()
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M334.png')

            #logger(current_image)
            check_preview = pip_designer_page.compare(Ground_Truth_Folder + 'M334.png', current_image)
            case.result = check_result and check_preview

        # [M499] After play ending of image sequence > Stay at the last frame
        with uuid("4cb61b28-9ba7-4556-8a2a-875c768e79da") as case:
            pip_designer_page.simple_timeline.click_image_track()
            pip_designer_page.simple_timeline.set_image_seq_ends('last')
            time.sleep(DELAY_TIME*0.5)
            pip_designer_page.click_ok()

            # Change duration to 7s then check result
            main_page.tips_area_click_set_length_of_selected_clip('00_00_07_00')

            # Enter Pip Designer
            timeline_operation_page.select_timeline_media(0, 0)
            main_page.double_click()
            pip_designer_page.advanced.switch_to_motion()

            # Verify : Timecode (00:00:06:00)
            time.sleep(DELAY_TIME*2)
            pip_designer_page.set_timecode('00_00_06_00')
            time.sleep(DELAY_TIME)
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M499.png')

            #logger(current_image)
            check_preview = pip_designer_page.compare(Ground_Truth_Folder + 'M499.png', current_image)
            case.result = check_preview

        # [M501] After play ending of image sequence > Stop playback
        with uuid("df56b069-af42-48cb-b08c-16650529ec95") as case:
            pip_designer_page.simple_timeline.click_image_track()
            pip_designer_page.simple_timeline.set_image_seq_ends('stop')
            time.sleep(DELAY_TIME)

            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M501.png')

            #logger(current_image)
            check_preview = pip_designer_page.compare(Ground_Truth_Folder + 'M501.png', current_image)
            case.result = check_preview

        # [M333] 4.2 Motion > Custom path
        with uuid("7b44abe8-4ae7-4b29-a87a-0848f1a5e90c") as case:
            pip_designer_page.path.select_template(3)
            pip_designer_page.path.select_category(option='custom')
            time.sleep(DELAY_TIME)
            result = pip_designer_page.path.select_template(2)
            case.result = result

        # [M335] 4.2 Motion > Remove Custom Path
        with uuid("0266354f-9a4c-4a3a-a52d-91ef7af6c33d") as case:
            check_result = pip_designer_page.path.remove_custom_template(2)
            time.sleep(DELAY_TIME*2)

            current_image = pip_designer_page.snapshot(locator=L.pip_designer.path.area_path_outline_row,
                                                 file_name=Auto_Ground_Truth_Folder + 'M335.png')

            #logger(current_image)
            check_preview = pip_designer_page.compare(Ground_Truth_Folder + 'M335.png', current_image)
            case.result = check_result and check_preview

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        # Enter Pip Room
        main_page.enter_room(4)
        pip_room_page.check_in_Pip_room()

        main_page.select_LibraryRoom_category('General')
        time.sleep(DELAY_TIME*2)

        # Select template "Dialog_03"
        main_page.select_library_icon_view_media("Dialog_03")

        # Add to timeline
        main_page.right_click()
        main_page.select_right_click_menu("Add to Timeline")

        # Enter pip designer
        timeline_operation_page.select_timeline_media(0, 0)
        main_page.double_click()
        result = pip_designer_page.get_title()
        if result != 'Dialog_03':
            logger('Not enter pip designer now.')
            raise Exception

        # enter Advance mode > Motion tab
        pip_designer_page.switch_mode('Advanced')
        pip_designer_page.advanced.switch_to_motion()
        pip_designer_page.advanced.unfold_path_menu()

        # [M331] Motion > All Paths
        with uuid("c0f9b824-e0df-430b-bc8f-099bd88c6ae4") as case:
            pip_designer_page.path.select_category(option='all')
            time.sleep(DELAY_TIME)
            pip_designer_page.path.select_template(24)
            time.sleep(DELAY_TIME)

            # Verify 1: Timecode (00:00:01:20)
            pip_designer_page.set_timecode('00_00_01_20')
            time.sleep(DELAY_TIME)
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M331_default_template_24.png')

            #logger(current_image)
            check_temp_24 = pip_designer_page.compare(Ground_Truth_Folder + 'M331_default_template_24.png', current_image)
            case.result = check_temp_24

        # [M432] 6.2 Keyframe > Position > Right-click menu > Linear > Default is linear
        with uuid("e8f2d89a-3928-4593-becb-ddd9627df7f6") as case:
            pip_designer_page.click_specific_keyframe(2)
            time.sleep(DELAY_TIME)
            result = pip_designer_page.simple_timeline.right_click_menu.get_linear_status()
            if result:
                case.result = True
            else:
                case.result = False

        # [M433] 6.2 Keyframe > Position > Right-click menu > Linear > Keyframe icon
        with uuid("583bed85-1518-49de-b2de-c1ff97d8fd97") as case:
            pip_designer_page.drag_simple_timeline_track_to_lager()
            time.sleep(DELAY_TIME)
            pip_designer_page.drag_keyframe_scroll_bar(1)
            time.sleep(DELAY_TIME * 1.5)
            pos_locator = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRoleDescription': 'outline'}
            current_image = pip_designer_page.snapshot(locator=pos_locator,
                                                 file_name=Auto_Ground_Truth_Folder + 'M433_pos_keyframe_icon.png')

            #logger(current_image)
            check_result = pip_designer_page.compare(Ground_Truth_Folder + 'M433_pos_keyframe_icon.png', current_image)
            case.result = check_result

        # [M434] 6.2 Keyframe > Position > Right-click menu > Hold > Able to change to Hold keyframe
        with uuid("02d58b6a-46f2-40c5-96d0-d5fafd3f82e6") as case:
            pip_designer_page.drag_keyframe_scroll_bar(0)
            time.sleep(DELAY_TIME * 1.5)
            pip_designer_page.click_specific_keyframe(2)
            check_result = pip_designer_page.simple_timeline.right_click_menu.set_linear_hold('hold')

            # Verify preview : Timecode (00:00:04:00)
            pip_designer_page.set_timecode('00_00_04_00')
            time.sleep(DELAY_TIME)
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M434_preview.png')

            #logger(current_image)
            check_preview = pip_designer_page.compare(Ground_Truth_Folder + 'M434_preview.png', current_image)
            case.result = check_result and check_preview

        # [M435] 6.2 Keyframe > Position > Right-click menu > Hold > Keyframe icon
        with uuid("74fbcb01-39ab-4585-a917-2ebfe6f3b091") as case:
            pos_locator = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRoleDescription': 'outline'}
            current_image = pip_designer_page.snapshot(locator=pos_locator,
                                                 file_name=Auto_Ground_Truth_Folder + 'M435_pos_keyframe_icon.png')

            #logger(current_image)
            check_result = pip_designer_page.compare(Ground_Truth_Folder + 'M435_pos_keyframe_icon.png', current_image)
            case.result = check_result

        # [M436] 6.2 Keyframe > Position > Right-click menu > Hold > Ease in disable
        with uuid("4ceb5862-de2c-407f-a7b3-409964a583e7") as case:
            pip_designer_page.set_timecode('00_00_05_00')
            time.sleep(DELAY_TIME)
            pip_designer_page.click_specific_keyframe(3)
            pos = main_page.mouse.position()
            main_page.mouse.move(pos[0] - 5, pos[1])
            time.sleep(DELAY_TIME*0.5)
            result = pip_designer_page.simple_timeline.right_click_menu.get_ease_in_status()

            if result == None:
                case.result = True
            else:
                case.result = False

        # [M437] 6.2 Keyframe > Position > Right-click menu > Hold > Ease out disable
        with uuid("e1ef1a5d-8784-40c2-b6fb-74d609091cb9") as case:
            pip_designer_page.click_specific_keyframe(2)
            result = pip_designer_page.simple_timeline.right_click_menu.get_ease_out_status()

            if result == None:
                case.result = True
            else:
                case.result = False

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        # Select template "Landscape 01.jpg" to track1
        main_page.select_library_icon_view_media("Landscape 01.jpg")
        main_page.tips_area_insert_media_to_selected_track()
        main_page.timeline_select_track(2)

        # Enter Pip Room
        main_page.enter_room(4)
        pip_room_page.check_in_Pip_room()

        main_page.select_LibraryRoom_category('General')
        time.sleep(DELAY_TIME*2)

        # Select template "Dialog_04" to track2
        main_page.select_library_icon_view_media("Dialog_04")
        main_page.tips_area_insert_media_to_selected_track()

        # Enter pip designer
        timeline_operation_page.select_timeline_media(2, 0)
        main_page.double_click()
        result = pip_designer_page.get_title()
        if result != 'Dialog_04':
            logger('Not enter pip designer now.')
            raise Exception

        # enter Advance mode > Properties tab
        pip_designer_page.switch_mode('Advanced')
        pip_designer_page.advanced.switch_to_properties()

        # [M447] 6.2 Keyframe > Scale > Right-click menu > Linear > Default is linear
        with uuid("46caa267-3dc5-4be3-97c1-5b52a3792a38") as case:
            pip_designer_page.click_specific_keyframe(5)
            result = pip_designer_page.simple_timeline.right_click_menu.get_linear_status()
            if result:
                case.result = True
            else:
                case.result = False

        # [M448] 6.2 Keyframe > Scale > Right-click menu > Linear > Keyframe icon
        with uuid("44856067-3adb-4c6e-942b-e4bda8f053e3") as case:
            pip_designer_page.drag_simple_timeline_track_to_lager()
            time.sleep(DELAY_TIME)
            pip_designer_page.drag_keyframe_scroll_bar(1)
            time.sleep(DELAY_TIME * 1.5)
            simple_timeline_locator = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRoleDescription': 'outline'}
            current_image = pip_designer_page.snapshot(locator=simple_timeline_locator,
                                                 file_name=Auto_Ground_Truth_Folder + 'M448_scale_keyframe_icon.png')

            #logger(current_image)
            check_result = pip_designer_page.compare(Ground_Truth_Folder + 'M448_scale_keyframe_icon.png', current_image)
            case.result = check_result


        # [M449] 6.2 Keyframe > Scale > Right-click menu > Hold > Able to change to Hold keyframe
        with uuid("e8ad76c7-0dab-42d8-8729-b97ea913883b") as case:
            pip_designer_page.drag_keyframe_scroll_bar(0)
            time.sleep(DELAY_TIME*1.5)
            pip_designer_page.click_specific_keyframe(5)
            check_result = pip_designer_page.simple_timeline.right_click_menu.set_linear_hold('hold')

            pip_designer_page.express_mode.unfold_properties_object_setting_tab()
            pip_designer_page.input_scale_width_value('2')
            case.result = check_result

        # [M450] 6.2 Keyframe > Scale > Right-click menu > Hold > Keyframe icon is correct and preview is correct
        with uuid("e076fdab-7c39-494f-a668-6e46acc1109d") as case:
            # Verify preview : Timecode (00:00:01:20)
            pip_designer_page.set_timecode('00_00_01_20')
            time.sleep(DELAY_TIME)
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M450_preview.png')

            #logger(current_image)
            check_preview = pip_designer_page.compare(Ground_Truth_Folder + 'M450_preview.png', current_image)
            case.result = check_preview

        # [M451] 6.2 Keyframe > Scale > Right-click menu > Hold > Ease in disable
        with uuid("8bbd8128-916e-4c89-9933-e4639307a4e0") as case:
            pip_designer_page.click_specific_keyframe(6)
            result = pip_designer_page.simple_timeline.right_click_menu.get_ease_in_status()

            if result == None:
                case.result = True
            else:
                case.result = False

        # [M452] 6.2 Keyframe > Scale > Right-click menu > Hold > Ease out disable
        with uuid("f98d16ee-a7d1-473a-9c04-5320b4a514cd") as case:
            pip_designer_page.click_specific_keyframe(5)
            result = pip_designer_page.simple_timeline.right_click_menu.get_ease_out_status()

            if result == None:
                case.result = True
            else:
                case.result = False

    # 4 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        # Select template "Sport 01.jpg" to track1
        main_page.select_library_icon_view_media("Sport 01.jpg")
        main_page.tips_area_insert_media_to_selected_track()
        main_page.timeline_select_track(2)

        # Enter Pip Room
        main_page.enter_room(4)
        pip_room_page.check_in_Pip_room()

        main_page.select_LibraryRoom_category('General')
        time.sleep(DELAY_TIME*2)

        # Select template "Dialog_03" to track2
        main_page.select_library_icon_view_media("Dialog_03")
        main_page.tips_area_insert_media_to_selected_track()

        # Enter pip designer
        timeline_operation_page.select_timeline_media(2, 0)
        main_page.double_click()
        result = pip_designer_page.get_title()
        if result != 'Dialog_03':
            logger('Not enter pip designer now.')
            raise Exception

        # enter Advance mode > Properties tab
        pip_designer_page.switch_mode('Advanced')
        pip_designer_page.advanced.switch_to_properties()

        # [M462] 6.2 Keyframe > Opacity > Right-click menu > Linear > Default is linear
        with uuid("ae86b80d-f62d-43a0-94a8-92eb162e0a9d") as case:
            pip_designer_page.click_specific_keyframe(9)
            result = pip_designer_page.simple_timeline.right_click_menu.get_linear_status()
            if result:
                case.result = True
            else:
                case.result = False

        # [M463] 6.2 Keyframe > Opacity > Right-click menu > Linear > Keyframe icon
        with uuid("b9a34acb-fd0b-40a4-abfa-7048229824fe") as case:
            pip_designer_page.drag_simple_timeline_track_to_lager()
            time.sleep(DELAY_TIME)
            pip_designer_page.drag_keyframe_scroll_bar(1)
            time.sleep(DELAY_TIME * 1.5)
            simple_timeline_locator = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRoleDescription': 'outline'}
            current_image = pip_designer_page.snapshot(locator=simple_timeline_locator,
                                                 file_name=Auto_Ground_Truth_Folder + 'M463_opacity_keyframe_icon.png')

            #logger(current_image)
            check_result = pip_designer_page.compare(Ground_Truth_Folder + 'M463_opacity_keyframe_icon.png', current_image)
            case.result = check_result

        # [M464] 6.2 Keyframe > Opacity > Right-click menu > Hold > Able to change to Hold keyframe
        with uuid("d040c710-83c2-4f8c-8407-651d90fb76c8") as case:
            pip_designer_page.drag_keyframe_scroll_bar(0)
            time.sleep(DELAY_TIME * 1.5)
            pip_designer_page.click_specific_keyframe(9)
            check_result = pip_designer_page.simple_timeline.right_click_menu.set_linear_hold('hold')

            pip_designer_page.express_mode.unfold_properties_object_setting_tab()
            pip_designer_page.drag_properties_scroll_bar(0.3)
            pip_designer_page.express_mode.drag_object_setting_opacity_slider(40)
            case.result = check_result

        # [M465] 6.2 Keyframe > Opacity > Right-click menu > Hold > Keyframe icon is correct and preview is correct
        with uuid("d7cd49c6-2715-4813-82e1-fecdd957a9a4") as case:
            # Verify preview : Timecode (00:00:02:21)
            pip_designer_page.set_timecode('00_00_02_21')
            time.sleep(DELAY_TIME)
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M465_preview.png')

            #logger(current_image)
            check_preview = pip_designer_page.compare(Ground_Truth_Folder + 'M465_preview.png', current_image)
            case.result = check_preview

    # 2 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        media_room_page.enter_color_boards()
        main_page.click_library_details_view()
        media_room_page.sound_clips_select_media("254, 241, 12")
        main_page.click_library_icon_view()
        #main_page.select_library_icon_view_media("94,32,73")
        main_page.tips_area_insert_media_to_selected_track()
        # Change duration to 7s then check result
        main_page.tips_area_click_set_length_of_selected_clip('00_00_07_00')

        main_page.timeline_select_track(2)

        # Enter Pip Room
        main_page.enter_room(4)
        pip_room_page.check_in_Pip_room()
        time.sleep(DELAY_TIME*2)

        # Select template "Wedding 2"
        main_page.select_LibraryRoom_category('Romance')
        main_page.select_library_icon_view_media("Wedding 2")

        # Add to timeline
        main_page.right_click()
        main_page.select_right_click_menu("Add to Timeline")

        # Change duration to 7s then check result
        main_page.tips_area_click_set_length_of_selected_clip('00_00_07_00')

        # Enter pip designer
        timeline_operation_page.select_timeline_media(2, 0)
        main_page.double_click()
        result = pip_designer_page.get_title()
        if result != 'Wedding 2':
            logger('Not enter pip designer now.')
            raise Exception

        # Unfold Object setting
        pip_designer_page.express_mode.unfold_properties_object_setting_tab()
        time.sleep(DELAY_TIME)

        # enter Advance mode > Motion tab
        pip_designer_page.switch_mode('Advanced')

        # [M498] 6.3 After play ending of image sequence > Keep loop playback (Default)
        with uuid("a2ae4c65-528a-4623-894b-99cd9861c696") as case:
            # Verify : Timecode (00:00:06:10)
            time.sleep(DELAY_TIME)
            pip_designer_page.set_timecode('00_00_06_10')
            time.sleep(DELAY_TIME)
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                       file_name=Auto_Ground_Truth_Folder + 'M498.png')

            # logger(current_image)
            check_preview = pip_designer_page.compare(Ground_Truth_Folder + 'M498.png', current_image)

            result = pip_designer_page.simple_timeline.get_image_seq_ends()
            if result == 'Loop Playback':
                check_result = True
            else:
                check_result = False

            time.sleep(DELAY_TIME)

            case.result = check_result and check_preview

        # [M500] 6.3 After play ending of image sequence > Stay at the first frame
        with uuid("6f3843ce-42e3-48b3-8b43-21ceedd8e944") as case:
            pip_designer_page.drag_simple_timeline_track_to_lager()
            time.sleep(DELAY_TIME)

            check_result = pip_designer_page.simple_timeline.set_image_seq_ends('first')
            time.sleep(DELAY_TIME)
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                       file_name=Auto_Ground_Truth_Folder + 'M500.png')

            # logger(current_image)
            check_preview = pip_designer_page.compare(Ground_Truth_Folder + 'M500.png', current_image)
            case.result = check_result and check_preview

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        # Select template "Sport 01.jpg" to track1
        main_page.select_library_icon_view_media("Travel 01.jpg")
        main_page.tips_area_insert_media_to_selected_track()

        # Enter pip designer
        timeline_operation_page.select_timeline_media(0, 0)
        main_page.double_click()
        result = pip_designer_page.get_title()
        if result != 'Travel 01':
            logger('Not enter pip designer now.')
            raise Exception

        # enter Advance mode > Properties tab
        pip_designer_page.switch_mode('Advanced')
        pip_designer_page.advanced.switch_to_properties()

        pip_designer_page.express_mode.unfold_properties_object_setting_tab()
        pip_designer_page.drag_properties_scroll_bar(0.8)

        # add 1st keyframe of rotation
        pip_designer_page.add_remove_rotation_current_keyframe()

        # Go to time code 2s & add 2nd keyframe of rotation
        pip_designer_page.set_timecode('00_00_02_00')
        pip_designer_page.input_rotation_degree_value(170)
        pip_designer_page.drag_simple_timeline_track_to_lager()

        # Go to time code 4s & add 3rd keyframe of rotation
        pip_designer_page.set_timecode('00_00_04_00')
        pip_designer_page.input_rotation_degree_value(240)



        # [M475] 6.2 Keyframe > Rotation > Right-click menu > Linear > Default is linear
        with uuid("7a38a431-d461-44c1-b674-cadb0074bb6b") as case:
            pip_designer_page.click_specific_keyframe(1)
            result = pip_designer_page.simple_timeline.right_click_menu.get_linear_status()
            if result:
                case.result = True
            else:
                case.result = False

        # [M476] 6.2 Keyframe > Rotation > Right-click menu > Linear > Keyframe icon
        with uuid("5ceb2b3d-6a9c-4ea8-9fdb-3935bf9cc7a3") as case:
            pip_designer_page.set_timecode('00_00_03_00')
            time.sleep(DELAY_TIME)
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M476_preview.png')

            #logger(current_image)
            check_result = pip_designer_page.compare(Ground_Truth_Folder + 'M476_preview.png', current_image)
            case.result = check_result

        # [M477] 6.2 Keyframe > Rotation > Right-click menu > Hold > Able to change to Hold keyframe
        with uuid("c7bee6ba-3ef6-4c0e-b4eb-c435ee8a4869") as case:
            pip_designer_page.click_specific_keyframe(1)
            check_result = pip_designer_page.simple_timeline.right_click_menu.set_linear_hold('hold')
            case.result = check_result

        # [M478] 6.2 Keyframe > Rotation > Right-click menu > Hold > Keyframe icon is correct and preview is correct
        with uuid("4869430e-24c0-41bf-b65f-9c9f4e890086") as case:
            # Verify preview : Timecode (00:00:03:00)
            pip_designer_page.set_timecode('00_00_03_00')
            time.sleep(DELAY_TIME)
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M478_preview.png')

            #logger(current_image)
            check_preview = pip_designer_page.compare(Ground_Truth_Folder + 'M478_preview.png', current_image)
            case.result = check_preview

        # [M479] 6.2 Keyframe > Rotation > Right-click menu > Hold > Ease in disable
        with uuid("a45190ac-bfbf-4a34-8b25-39285bec5cea") as case:
            pip_designer_page.click_specific_keyframe(0)
            result = pip_designer_page.simple_timeline.right_click_menu.get_ease_in_status()

            if result == None:
                case.result = True
            else:
                case.result = False

        # [M480] 6.2 Keyframe > Rotation > Right-click menu > Hold > Ease out disable
        with uuid("faab6d15-30fe-4eff-b0b7-1c7320048870") as case:
            pip_designer_page.click_specific_keyframe(1)
            result = pip_designer_page.simple_timeline.right_click_menu.get_ease_out_status()

            if result == None:
                case.result = True
            else:
                case.result = False

    # 5 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        # Select template "Travel 01.jpg" to track1
        main_page.select_library_icon_view_media("Travel 01.jpg")
        main_page.tips_area_insert_media_to_selected_track()

        # Enter pip designer
        timeline_operation_page.select_timeline_media(0, 0)
        main_page.double_click()
        result = pip_designer_page.get_title()
        if result != 'Travel 01':
            logger('Not enter pip designer now.')
            raise Exception

        # enter Advance mode > Properties tab
        pip_designer_page.switch_mode('Advanced')
        pip_designer_page.advanced.switch_to_properties()
        pip_designer_page.express_mode.unfold_properties_object_setting_tab()
        pip_designer_page.drag_properties_scroll_bar(0.8)

        # add 1st keyframe of rotation
        pip_designer_page.add_remove_rotation_current_keyframe()

        # Go to time code 2s & add 2nd keyframe of rotation
        pip_designer_page.set_timecode('00_00_02_00')
        pip_designer_page.input_rotation_degree_value(170)

        # Go to time code 4s & add 3rd keyframe of rotation
        pip_designer_page.set_timecode('00_00_04_00')
        pip_designer_page.input_rotation_degree_value(250)

        # Go to Motion tab > Set Path
        pip_designer_page.advanced.switch_to_motion()
        pip_designer_page.advanced.unfold_path_menu()
        pip_designer_page.path.select_template(6)
        pip_designer_page.advanced.unfold_path_menu(0)
        pip_designer_page.drag_keyframe_scroll_bar(0.62)

        # Enable (Motion Blur) checkbox
        pip_designer_page.motion_blur.set_checkbox()
        pip_designer_page.advanced.unfold_motion_blur_menu()

        # [M345] 4.2 Motion Blur > Blur length > Default value (1.00)
        with uuid("62024066-6d8f-4808-87d0-f3128e2bd4d0") as case:
            check_value = pip_designer_page.motion_blur.length.get_value()
            logger(check_value)
            if check_value == '1.00':
                check_default = True
            else:
                check_default = False

            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M345_preview.png')

            #logger(current_image)
            check_preview = pip_designer_page.compare(Ground_Truth_Folder + 'M345_preview.png', current_image)
            case.result = check_preview and check_default

        # [M346] 4.2 Motion Blur > Blur length > Minimum value (0)
        with uuid("cc36a543-a096-4de2-a47f-d252d1583dc1") as case:
            pip_designer_page.motion_blur.length.set_value(0)
            time.sleep(DELAY_TIME*0.5)
            check_value = pip_designer_page.motion_blur.length.get_value()
            logger(check_value)
            if check_value == '0.00':
                case.result = True
            else:
                case.result = False

        # [M348] 4.2 Motion Blur > Blur length > Adjust by Slider
        with uuid("d727e4e3-108d-4311-a85a-fb454c63f0d4") as case:
            pip_designer_page.motion_blur.length.adjust_slider(1.9)
            time.sleep(DELAY_TIME*0.5)
            check_value = pip_designer_page.motion_blur.length.get_value()
            logger(check_value)
            if check_value == '1.90':
                check_result = True
            else:
                check_result = False

            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M348_preview.png')

            #logger(current_image)
            check_preview = pip_designer_page.compare(Ground_Truth_Folder + 'M348_preview.png', current_image)
            case.result = check_preview and check_result

        # [M347] 4.2 Motion Blur > Blur length > Maximum value (2.00)
        with uuid("562f93f5-68bf-4009-9dfe-17a33ec2a418") as case:
            pip_designer_page.motion_blur.length.set_value(2)
            time.sleep(DELAY_TIME*0.5)
            check_value = pip_designer_page.motion_blur.length.get_value()
            logger(check_value)
            if check_value == '2.00':
                case.result = True
            else:
                case.result = False

            # [M349] 4.2 Motion Blur > Blur length > Adjust by Input
            with uuid("1c0f7e04-d46a-40fb-9605-2782fcccc8df") as case:
                if check_value == '2.00':
                    case.result = True
                else:
                    case.result = False

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        # Select template "Food.jpg" to track1
        main_page.select_library_icon_view_media("Food.jpg")
        main_page.tips_area_insert_media_to_selected_track()

        # Enter pip designer
        timeline_operation_page.select_timeline_media(0, 0)
        main_page.double_click()
        result = pip_designer_page.get_title()
        if result != 'Food':
            logger('Not enter pip designer now.')
            raise Exception

        # enter Advance mode > Properties tab
        pip_designer_page.switch_mode('Advanced')
        pip_designer_page.advanced.switch_to_properties()
        pip_designer_page.express_mode.unfold_properties_object_setting_tab()
        pip_designer_page.drag_properties_scroll_bar(0.8)

        # add 1st keyframe of rotation
        pip_designer_page.add_remove_rotation_current_keyframe()

        # Go to time code 2s & add 2nd keyframe of rotation
        pip_designer_page.set_timecode('00_00_02_00')
        pip_designer_page.input_rotation_degree_value(175)

        # Go to time code 4s & add 3rd keyframe of rotation
        pip_designer_page.set_timecode('00_00_04_00')
        pip_designer_page.input_rotation_degree_value(280)

        # Go to Motion tab > Set Path
        pip_designer_page.advanced.switch_to_motion()
        pip_designer_page.advanced.unfold_path_menu()
        pip_designer_page.path.select_template(3)
        pip_designer_page.advanced.unfold_path_menu(0)
        pip_designer_page.drag_keyframe_scroll_bar(0.62)

        # Enable (Motion Blur) checkbox
        pip_designer_page.motion_blur.set_checkbox()
        pip_designer_page.advanced.unfold_motion_blur_menu()

        #  Set slider to 1.9
        pip_designer_page.motion_blur.length.adjust_slider(2)
        time.sleep(DELAY_TIME*0.5)
        # [M350] 4.2 Motion Blur > Blur length > Adjust arrow button
        with uuid("ca24222c-ddb3-4cbd-b529-cb43c0be11bd") as case:
            pip_designer_page.motion_blur.length.click_arrow(1,6)
            time.sleep(DELAY_TIME*0.5)
            check_value = pip_designer_page.motion_blur.length.get_value()
            if check_value == '1.94':
                check_down = True
            else:
                check_down = False

            pip_designer_page.motion_blur.length.click_arrow(0,5)
            time.sleep(DELAY_TIME*0.5)
            check_value = pip_designer_page.motion_blur.length.get_value()
            if check_value == '1.99':
                check_up = True
            else:
                check_up = False
            case.result = check_down and check_up

        # [M351] 4.2 Motion Blur > Blur density > Default value
        with uuid("0a541e22-dae6-41da-98e4-29ba632550d1") as case:
            check_value = pip_designer_page.motion_blur.density.get_value()
            if check_value == '16':
                case.result = True
            else:
                case.result = False

        # [M352] 4.2 Motion Blur > Blur density > Minimum value (2)
        with uuid("4045bb5a-b849-4b6b-9a6e-a9babc71effc") as case:
            pip_designer_page.motion_blur.density.set_value(2)

            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M352_preview.png')

            #logger(current_image)
            check_preview = pip_designer_page.compare(Ground_Truth_Folder + 'M352_preview.png', current_image)
            check_value = pip_designer_page.motion_blur.density.get_value()
            if check_value == '2':
                check_result = True
            else:
                check_result = False
            case.result = check_preview and check_result

            # [M355] 4.2 Motion Blur > Blur density > Adjust by Input
            with uuid("a09eb96a-e143-4f6f-b106-ca4c001a5387") as case:
                check_value = pip_designer_page.motion_blur.density.get_value()
                if check_value == '2':
                    case.result = True
                else:
                    case.result = False

        # Go to time code 2s
        pip_designer_page.set_timecode('00_00_02_00')

        # [M356] 4.2 Motion Blur > Blur density > Adjust arrow button
        with uuid("b9326e03-3864-47fa-b945-545541f1b0c7") as case:
            pip_designer_page.motion_blur.density.click_arrow(0, 8)
            time.sleep(DELAY_TIME*0.5)
            pip_designer_page.motion_blur.density.click_arrow(1, 2)
            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M356_preview.png')

            #logger(current_image)
            check_preview = pip_designer_page.compare(Ground_Truth_Folder + 'M356_preview.png', current_image)
            check_value = pip_designer_page.motion_blur.density.get_value()
            if check_value == '8':
                check_result = True
            else:
                check_result = False
            case.result = check_preview and check_result

        # [M354] 4.2 Motion Blur > Blur density > Adjust by Slider
        with uuid("7fcd9f42-0e92-4dd1-bd80-7055af2a2772") as case:
            pip_designer_page.motion_blur.density.adjust_slider(32)
            check_value = pip_designer_page.motion_blur.density.get_value()
            if check_value == '32':
                case.result = True
            else:
                case.result = False

        # [M353] 4.2 Motion Blur > Blur density > Maximum value (32)
        with uuid("8e97e4fa-0317-43c1-b840-1271d2a03338") as case:
            check_value = pip_designer_page.motion_blur.density.get_value()
            if check_value == '32':
                check_result = True
            else:
                check_result = False

            current_image = pip_designer_page.snapshot(locator=L.pip_designer.designer_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'M353_preview.png')

            #logger(current_image)
            check_preview = pip_designer_page.compare(Ground_Truth_Folder + 'M353_preview.png', current_image)
            case.result = check_preview and check_result