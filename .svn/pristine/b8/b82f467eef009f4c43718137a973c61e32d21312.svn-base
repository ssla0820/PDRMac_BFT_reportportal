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
title_designer_page = PageFactory().get_page_object('title_designer_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Title Designer2.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Title_Designer_2/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Title_Designer_2/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1


class Test_Title_Designer_2():  # Title Designer2.html columns(119~625)
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
            google_sheet_execution_log_init('Title_Designer_2')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"title designer 2 result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number,
                                                     report.get_ovinfo('na'),
                                                     report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        with uuid('0bc99273-d8d0-489f-a439-f1266d3e1458') as case:
            # 1. In Title Room (Basic mode)
            # 1.5. Object Tab
            # 1.5.4. Border > Fill Type > Uniform Color
            # select color
            main_page.enter_room(1)
            title_room_page.click_CreateNewTitle_btn()
            title_designer_page.unfold_object_border_tab(unfold=1)
            title_designer_page.set_check_border(bCheck=1)
            check_result_1 = title_room_page.check_enter_title_designer()

            title_designer_page.apply_border_uniform_color('255', '0', '0')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_4_1.png', 'Object')

            check_result_3 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_4_2.png', 'Preview')
            case.result = check_result_1 and check_result_2 and check_result_3

        with uuid('671e1dc0-7e26-43cc-a478-a294a8777816') as case:
            # 1.5. Object Tab
            # 1.5.4. Border > Fill Type > 2 Color Gradient
            # select color
            title_designer_page.apply_border_2_color('0', '255', '0', '0', '0', '255')

            check_result_1 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_4_3.png', 'Object')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_4_4.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('3edf489e-3f7e-4b36-a715-f505a5427553') as case:
            # 1.5. Object Tab
            # 1.5.4. Border > Fill Type > 4 Color Gradient
            # select color
            title_designer_page.apply_border_4_color(
                '0', '255', '0', '0', '0', '255', '255', '0', '0', '255', '255', '255')

            check_result_1 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_4_5.png', 'Object')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_4_6.png', 'Preview')
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid('5f4e241f-75f0-475c-a880-fac7d64fa179') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Checkbox > Untick (Default)
            # untick to dis-apply settings
            main_page.enter_room(1)
            title_room_page.click_CreateNewTitle_btn()

            check_status = title_designer_page.exist(L.title_designer.shadow.chx_shadow).AXValue
            check_result_1 = False if not check_status == 0 else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_1.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('82e277ef-3273-4e4f-870d-bad5cddf3a66') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Checkbox > Tick
            # tick to apply settings
            title_designer_page.set_check_shadow(bCheck=1)

            check_status = title_designer_page.exist(L.title_designer.shadow.chx_shadow).AXValue
            check_result_1 = False if not check_status == 1 else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_2.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('6ed1c84b-edd6-4845-8672-8b6dc0216dc5') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Apply shadow to > Text and Border
            # display shadow as selected setting
            title_designer_page.set_check_border(bCheck=1)
            title_designer_page.set_check_shadow(bCheck=1)
            title_designer_page.unfold_object_shadow_tab(unfold=1)
            title_designer_page.apply_shadow_to(index=0)

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_3.png', 'Preview')

        with uuid('90022909-7cbe-475c-bc86-b513448ce0f8') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Apply shadow to > Text Only
            # display shadow as selected setting
            title_designer_page.apply_shadow_to(index=1)

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_4.png', 'Preview')

        with uuid('64e15746-4175-4dfa-9c97-109c3b0d6998') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Apply shadow to > Border Only
            # display shadow as selected setting
            title_designer_page.apply_shadow_to(index=2)

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_5.png', 'Preview')

            title_designer_page.apply_shadow_to(index=0)  # restore to default setting

        with uuid('26dee390-da3c-43ec-8608-e9eddb6f3171') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Distance > Default value
            # default value should be 3
            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_distance).AXValue

            case.result = False if not check_value == '3.0' else True

        with uuid('ee9e28df-18b2-4e2c-8c61-6032b1bdcaa7') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Distance > Min
            # minimal value should be 0.0
            title_designer_page.drag_shadow_distance_slider('0')

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_distance).AXValue
            check_result_1 = False if not check_value == '0.0' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_6.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('1ef8c0b4-8145-4cb5-87cf-fd3bd375185b') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Distance > Max
            # max value should be 100
            title_designer_page.drag_shadow_distance_slider('100')

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_distance).AXValue
            check_result_1 = False if not check_value == '100.0' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_7.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('ccc7aa26-1647-48fc-a54e-0880e8b7f11b') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Distance > Slider
            # use slider to set value
            case.result = check_result_1 and check_result_2

        with uuid('b00695b5-9521-4894-9d82-7dc72bb969c8') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Distance > Input value
            # direct input to set value
            title_designer_page.input_shadow_distance_value('20')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_8.png', 'Preview')

        with uuid('085e1348-0a53-4eec-b344-975f2c89ea74') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Distance > ^/v button
            # use buttons to set value
            for number_of_clicks in range(3):
                title_designer_page.click_shadow_distance_arrow_btn(index=0)
            for number_of_clicks in range(2):
                title_designer_page.click_shadow_distance_arrow_btn(index=1)

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_distance).AXValue
            case.result = False if not check_value == '20.1' else True

        with uuid('202a5d1f-6125-4146-8766-803b187d1546') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Blur > Default value
            # default value should be 0
            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_blur).AXValue

            case.result = False if not check_value == '0' else True

        with uuid('94419af8-864f-4bd1-872f-b61193ee55ba') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Blur > Min
            # minimal value should be 0
            title_designer_page.drag_shadow_blur_slider('0')

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_blur).AXValue
            check_result_1 = False if not check_value == '0' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_9.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('c6cecd94-cdf2-4862-ba95-9b1b73d7ace7') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Blur > Max
            # max value should be 20
            title_designer_page.drag_shadow_blur_slider('100')

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_blur).AXValue
            check_result_1 = False if not check_value == '20' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_10.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('3048fd8d-901a-4b05-9bb3-ea60251bf1b9') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Blur > Slider
            # use slider to set value
            case.result = check_result_1 and check_result_2

        with uuid('a8b25314-9c99-4120-9be6-fab9d975f5de') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Blur > Input value
            # direct input to set value
            title_designer_page.input_shadow_blur_value('5')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_11.png', 'Preview')

        with uuid('e9f0fe74-fb28-4f81-8a21-11ff5333f69a') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Blur > ^/v button
            # use buttons to set value
            for number_of_clicks in range(3):
                title_designer_page.click_shadow_blur_arrow_btn(index=0)
            for number_of_clicks in range(2):
                title_designer_page.click_shadow_blur_arrow_btn(index=1)

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_blur).AXValue
            case.result = False if not check_value == '6' else True

        with uuid('70809d27-5a51-43a8-8016-b664b66673da') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Opacity > Default value
            # default value should be 100%
            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_opacity).AXValue

            case.result = False if not check_value == '100%' else True

        with uuid('08126905-c8ef-47dd-b3f6-552ef623b67c') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Opacity > Min
            # minimal value should be 0
            title_designer_page.drag_shadow_opacity_slider('0')

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_opacity).AXValue
            check_result_1 = False if not check_value == '0%' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_12.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('12b03740-4116-4d29-8bf0-5b03c9a07af1') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Opacity > Max
            # max value should be 100%
            title_designer_page.drag_shadow_opacity_slider('100')

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_opacity).AXValue
            check_result_1 = False if not check_value == '100%' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_13.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('8b469c01-a86c-4e58-aec6-30434fa6ff47') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Opacity > Slider
            # use slider to set value
            case.result = check_result_1 and check_result_2

        with uuid('61218c7a-ff79-4538-90f8-c65bed8617e1') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Opacity > Input value
            # direct input to set value
            title_designer_page.input_shadow_opacity_value('90')

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_opacity).AXValue
            check_result_1 = False if not check_value == '90%' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_14.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('b0f43bb9-d696-4c10-9237-947413d18c06') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Opacity > ^/v button
            # use buttons to set value
            title_designer_page.drag_shadow_opacity_slider('90')
            for number_of_clicks in range(3):
                title_designer_page.click_shadow_opacity_arrow_btn(index=0)
            for number_of_clicks in range(2):
                title_designer_page.click_shadow_opacity_arrow_btn(index=1)

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_opacity).AXValue
            case.result = False if not check_value == '91%' else True

        with uuid('993e48af-cb8c-4380-8815-b5d3b4be5af5') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Fill Shadow > Select color
            # open color selector to select color
            title_designer_page.set_shadow_fill_shadow_color(red='255', green='0', blue='0')

            check_result_1 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_15.png', 'Object')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_18.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('1dc74b52-d889-4c32-afea-e74b7cb63ae4') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Fill Shadow > On / Off
            # tick to apply fill shadow
            title_designer_page.set_check_shadow_fill_shadow(bCheck=1)
            check_result_1 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_16.png', 'Preview')

            title_designer_page.set_check_shadow_fill_shadow(bCheck=0)
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_1_5_5_17.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('41396e90-8149-4634-9ea8-069d2f4bea15') as case:
            # 1.5. Object Tab
            # 1.5.5. Shadow > Shadow direction > Set direction
            # set shadow direction
            case.result = None
            case.fail_log = "*AT limitation*"

        with uuid('e7671d5e-2561-4bb8-a088-83fe23874169') as case:
            # 1.6. Save template
            # 1.6.4. [Cancel] button
            # pop close confirm dialog if have unsaved edit
            check_result = title_designer_page.click_cancel(option=2)
            case.result = check_result

        with uuid('1cc82dc2-467f-4506-a05a-f6b0f6ba1fe9') as case:
            # 1.6. Save template
            # 1.6.2. [Save as] button
            # pop save as dialog and keep designer open after save
            title_designer_page.save_as_name('1234')
            title_designer_page.exist_click(L.title_designer.save_as_template.btn_ok)

            check_title_name = title_designer_page.get_title()
            case.result = False if not check_title_name == '1234' else True

        with uuid('8ec038ce-d7db-4d3a-b27a-40310094c94b') as case:
            # 1.6. Save template
            # 1.6.5. [Save As Template] dialog > [Cancel] button
            # cancel and close dialog
            title_designer_page.save_as_name('1111')
            title_designer_page.save_as_click_cancel()

            check_title_name = title_designer_page.get_title()
            case.result = False if not check_title_name == '1234' else True

        with uuid('32ef69f7-a65a-46c9-9a7d-65e1fa7b0ccf') as case:
            # 1.6. Save template
            # 1.6.5. [Save As Template] dialog > [Enter a name] textbox
            # input template name
            case.result = title_designer_page.save_as_name('123456')

        with uuid('e706ba41-dc16-4fb2-9f86-c90443c60cab') as case:
            # 1.6. Save template
            # 1.6.5. [Save As Template] dialog > Thumbnail slider
            # drag slider to set thumbnail
            case.result = title_designer_page.save_as_set_slider(0.2)

        with uuid('4b760932-0b31-4a59-bfa6-afdb20fe5018') as case:
            # 1.6. Save template
            # 1.6.5. [Save As Template] dialog > [OK] button
            # save with entered name and selected thumbnail
            title_designer_page.exist_click(L.title_designer.save_as_template.btn_ok)

            check_title_name = title_designer_page.get_title()
            case.result = False if not check_title_name == '123456' else True

        with uuid('ca899edc-d495-4c99-b8f9-1643561d3d08') as case:
            # 1.6. Save template
            # 1.6.3. [OK] button
            # pop save as dialog and close designer after save
            title_designer_page.click_ok()

            check_result = title_designer_page.exist(L.title_designer.main_window)
            case.result = True if not check_result else False

        with uuid('55bd6570-71dc-45b3-ab8d-7be7e2db4306') as case:
            # 1.6. Save template
            # 1.6.6. Check Template in Title Room > Name
            # show as saved name
            case.result = main_page.select_library_icon_view_media('123456')

        with uuid('591bbc75-c95b-4da5-acfa-282b88140fb6') as case:
            # 1.6. Save template
            # 1.6.6. Check Template in Title Room > Thumbnail
            # show as saved thumbnail
            image_full_path = Auto_Ground_Truth_Folder + 'title_designer_1_6_6_1.png'
            ground_truth = Ground_Truth_Folder + 'title_designer_1_6_6_1.png'
            current_preview = title_designer_page.snapshot(
                locator=L.base.Area.library_icon_view, file_name=image_full_path)
            check_result = title_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('d943260e-f40d-427a-a80d-05de072b9193') as case:
            # 1.6. Save template
            # 1.6.6. Check Template in Title Room > Preview
            # show preview correctly when select
            image_full_path = Auto_Ground_Truth_Folder + 'title_designer_1_6_6_2.png'
            ground_truth = Ground_Truth_Folder + 'title_designer_1_6_6_2.png'
            current_preview = title_designer_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result = title_designer_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('9b4401dc-137c-4d75-9152-513587b521f0') as case:
            # 2. Timeline editing (switch to Advanced mode)
            # 2.1. Add saved template to timeline
            # 2.1.1. Drag to timeline
            # Add template to selected position correctly
            # Pop ripple editing menu if needed
            main_page.enter_room(0)
            main_page.insert_media('Skateboard 01.mp4')
            main_page.enter_room(1)
            main_page.drag_media_to_timeline_playhead_position('1234', track_no=2)

            case.result = main_page.select_timeline_media('My Title')
            main_page.click_undo()

        with uuid('434e0056-a7cc-4934-a3b3-abedc8acc2a5') as case:
            # 2.1. Add saved template to timeline
            # 2.1.2. Right Click Menu > Add to Timeline
            # Add template to selected position correctly
            # Pop ripple editing menu if needed
            main_page.hover_library_media('1234')
            title_room_page.select_RightClickMenu_AddToTimeline()

            case.result = main_page.select_timeline_media('My Title')
            main_page.click_undo()

        with uuid('62eae51d-1406-4c78-8bf6-f8c82b947c89') as case:
            # 2.1. Add saved template to timeline
            # 2.1.3. Tips Area > Insert on selected track
            # Add template to selected position correctly
            # Pop ripple editing menu if needed
            main_page.select_library_icon_view_media('1234')
            main_page.tips_area_insert_media_to_selected_track()

            case.result = main_page.select_timeline_media('My Title')

        with uuid('2ff58d4c-af3f-4524-beea-8a42407da414') as case:
            # 2.2. Entry Point
            # 2.2.1. Timeline > Right click menu > Edit Title...
            # launch designer with selected template
            timeline_operation_page.right_click()
            timeline_operation_page.select_right_click_menu('Edit Title...')

            check_result = title_designer_page.is_exist(L.title_designer.main_window)
            case.result = False if not check_result else True

            title_designer_page.press_esc_key()

        with uuid('4c498b1e-db03-4af5-9817-310cd93c515b') as case:
            # 2.2. Entry Point
            # 2.2.1. Timeline > Double click template
            # launch designer with selected template
            main_page.select_timeline_media('My Title')
            timeline_operation_page.double_click()

            check_result = title_designer_page.is_exist(L.title_designer.main_window)
            case.result = False if not check_result else True

            title_designer_page.press_esc_key()

        with uuid('3fc5e5d6-13bd-42c0-90ae-ed72facbeb8e') as case:
            # 2.2. Entry Point
            # 2.2.2. Tips Area > [Designer] button
            # launch designer with selected template
            main_page.tips_area_click_designer()

            check_result = title_designer_page.is_exist(L.title_designer.main_window)
            case.result = False if not check_result else True

            title_designer_page.press_esc_key()

        with uuid('6c1ef0ad-4ca9-429e-b922-6cb80c8ff2b4') as case:
            # 2.2. Entry Point
            # 2.2.2. Tips Area > More feature button > Edit Title...
            # launch designer with selected template
            main_page.tips_area_click_more_feature()
            timeline_operation_page.select_right_click_menu('Edit Title...')

            check_result = title_designer_page.is_exist(L.title_designer.main_window)
            case.result = False if not check_result else True

        with uuid('6cc5eeb9-37f3-4b38-ac3c-53a50aaa37fb') as case:
            # 2.2. Entry Point
            # 2.2.3. Basic Mode to Advanced Mode
            title_designer_page.switch_mode(2)
            object_status_1 = title_designer_page.is_exist(L.title_designer.btn_animation)
            object_status_2 = title_designer_page.is_exist(L.title_designer.btn_clip_timecode)
            check_result_1 = object_status_1 and object_status_2

            title_designer_page.switch_mode(1)
            object_status_3 = not (title_designer_page.is_exist(L.title_designer.btn_animation))
            object_status_4 = not (title_designer_page.is_exist(L.title_designer.btn_clip_timecode))
            check_result_2 = object_status_3 and object_status_4

            case.result = check_result_1 and check_result_2

            title_designer_page.switch_mode(2)  # switch to advanced mode

        with uuid('5f3a6340-5590-4f3a-8ff2-528b3e6093b5') as case:
            # 2.3. Designer Menu Bar
            # 2.3.1. Caption
            # should display "Title Designer" and the text in 1st title track
            get_window_title = title_designer_page.get_full_title()
            case.result = False if not get_window_title == 'Title Designer | My Title' else True

        with uuid('45879eca-09ce-419d-ae4f-f5ab885a0f63') as case:
            # 2.3. Designer Menu Bar
            # 2.3.3. [Edit] button > Undo
            # undo last action
            title_designer_page.set_font_face_color(red='0', green='0', blue='255')
            title_designer_page.click_menu_bar_edit(index=1)  # undo

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_3_3_1.png', 'designer window')

        with uuid('814d8746-5e1e-4071-9d38-a77f1d36f9b5') as case:
            # 2.3. Designer Menu Bar
            # 2.3.3. [Edit] button > Redo
            # redo last undo action
            title_designer_page.click_menu_bar_edit(index=2)  # redo

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_3_3_2.png', 'designer window')

        with uuid('1c9b4f96-12a3-4410-8091-febcd975a0ba') as case:
            # 2.3. Designer Menu Bar
            # 2.3.3. [Edit] button > Cut
            # cut selected object
            title_designer_page.click_menu_bar_edit(index=3)  # cut

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_3_3_3.png', 'designer window')

            title_designer_page.click_menu_bar_edit(index=1)  # undo

        with uuid('137dc5bc-11d8-4403-9376-a4518f8f87e3') as case:
            # 2.3. Designer Menu Bar
            # 2.3.3. [Edit] button > Copy
            # copy selected object
            title_designer_page.click_menu_bar_edit(index=4)  # copy

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_3_3_4.png', 'designer window')

        with uuid('6c40c679-53ce-44c4-949a-80b36758ded9') as case:
            # 2.3. Designer Menu Bar
            # 2.3.3. [Edit] button > Remove
            # remove selected object
            title_designer_page.click_menu_bar_edit(index=6)  # remove

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_3_3_5.png', 'designer window')

        with uuid('fc5a3087-62bd-4a7a-908a-a2eb6ebc79c0') as case:
            # 2.3. Designer Menu Bar
            # 2.3.3. [Edit] button > Paste
            # paste cut or copied object
            title_designer_page.click_menu_bar_edit(index=5)  # paste

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_3_3_6.png', 'designer window')

        with uuid('467dd142-fd8e-48ca-a697-a37281c9f945') as case:
            # 2.3. Designer Menu Bar
            # 2.3.3. [Edit] button > Select All
            # select all object
            title_designer_page.click_menu_bar_edit(index=7)  # select all

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_3_3_7.png', 'designer window')

        with uuid('e7202f78-31f8-46a9-9a79-0fb32cb3258c') as case:
            # 2.3. Designer Menu Bar
            # 2.3.8. Maximize / Restore Down > Maximize
            # maximize window size
            title_designer_page.click_maximize_btn()

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_3_8_1.png', 'designer window')

        with uuid('18b8ec85-0924-41d2-b024-a9080d315dc0') as case:
            # 2.3. Designer Menu Bar
            # 2.3.8. Maximize / Restore Down > Restore Down
            # restore to original window size
            title_designer_page.click_maximize_btn()

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_3_8_2.png', 'designer window')

        with uuid('4210576e-79d3-483e-a708-e179011e1058') as case:
            # 2.3. Designer Menu Bar
            # 2.3.9. Close > Close
            # close designer
            title_designer_page.save_as_name('12345')
            title_designer_page.exist_click(L.title_designer.save_as_template.btn_ok)
            title_designer_page.click_close_btn()

            check_result = title_designer_page.is_exist(L.title_designer.main_window)
            case.result = True if not check_result else False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid('19706794-5603-4380-a702-3c37fb0010bc') as case:
            # 2.4. Control bar
            # 2.4.1. [Insert Title] button
            # insert a new title
            main_page.enter_room(1)
            title_room_page.click_CreateNewTitle_btn()
            title_designer_page.switch_mode(2)  # advanced mode
            title_designer_page.press_backspace_key()  # delete default title text
            check_result_1 = title_designer_page.insert_title('auto test')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_1_1.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('263b7959-cab6-4005-bae3-34ce82df7460') as case:
            # 2.4. Control bar
            # 2.4.2. [Insert Particle] button
            # open import particle dialog
            check_result_1 = title_designer_page.click_insert_particle_btn()

            check_result_2 = title_designer_page.is_exist(L.title_designer.particle.window_insert_particle)
            case.result = check_result_1 and check_result_2

        with uuid('487b1ff5-0b2f-480c-870c-06373420e5bd') as case:
            # 2.4. Control bar
            # 2.4.3. Import Particle dialog > Sort
            # sort by type dropdown menu
            title_designer_page.exist_click(L.title_designer.particle.chx_particle_menu)
            title_designer_page.exist_click(L.title_designer.particle.option_custom)
            title_designer_page.exist_click(L.title_designer.particle.chx_particle_menu)
            title_designer_page.exist_click(L.title_designer.particle.option_general)
            title_designer_page.exist_click(L.title_designer.particle.chx_particle_menu)
            title_designer_page.exist_click(L.title_designer.particle.option_downloaded)
            title_designer_page.exist_click(L.title_designer.particle.chx_particle_menu)
            title_designer_page.exist_click(L.title_designer.particle.option_all_content)

            image_full_path = Auto_Ground_Truth_Folder + 'title_designer_2_4_3_1.png'
            ground_truth = Ground_Truth_Folder + 'title_designer_2_4_3_1.png'
            current_preview = title_designer_page.snapshot(
                locator=L.title_designer.particle.window_insert_particle, file_name=image_full_path)
            check_result = title_designer_page.compare(ground_truth, current_preview)

            case.result = check_result

        with uuid('2e68b17a-effc-41d0-a73f-8b12f6459302') as case:
            # 2.4. Control bar
            # 2.4.3. Import Particle dialog > Preview
            # play preview when select template
            title_designer_page.exist_click({'AXIdentifier': 'EntityCollectionViewItem', 'index': 0})
            check_result_1 = title_designer_page.exist(L.title_designer.particle.btn_ok).AXEnabled

            image_full_path = Auto_Ground_Truth_Folder + 'title_designer_2_4_3_2.png'
            ground_truth = Ground_Truth_Folder + 'title_designer_2_4_3_2.png'
            current_preview = title_designer_page.snapshot(
                locator=L.title_designer.particle.window_insert_particle, file_name=image_full_path)
            check_result_2 = title_designer_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('e5853346-0ebc-4cb7-96e6-9cfd7d67b74b') as case:
            # 2.4. Control bar
            # 2.4.3. Import Particle dialog > [Cancel] button
            # cancel and close dialog
            title_designer_page.exist_click(
                {'AXIdentifier': 'IDC_TITLE_IMPORT_PARTICLE_BTN_CANCEL', 'AXTitle': 'Cancel'})

            check_result = title_designer_page.is_exist(L.title_designer.particle.window_insert_particle)
            case.result = True if not check_result else False

        with uuid('8e55e9c7-8344-464d-8e0b-981de115e13c') as case:
            # 2.4. Control bar
            # 2.4.3. Import Particle dialog > [OK] button
            # select a particle template and click to add to title
            title_designer_page.click_insert_particle_btn()
            # all contents, 1st particle
            check_result_1 = title_designer_page.insert_particle(menu_index=0, particle_index=0)

            title_designer_page.set_timecode('00_00_03_00')
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_3_3.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('f641e69d-1a32-462c-a84f-87bb809969b8') as case:
            # 2.4. Control bar
            # 2.4.3. Import Particle dialog > x button
            # click to close dialog
            title_designer_page.click_insert_particle_btn()
            title_designer_page.exist_click({'AXIdentifier': 'EntityCollectionViewItem', 'index': 0})
            title_designer_page.click_close_btn()

            check_result = title_designer_page.is_exist(L.title_designer.particle.window_insert_particle)
            case.result = True if not check_result else False

        with uuid('abdb33c5-d9ff-40d0-a69b-7783e604deca') as case:
            # 2.4. Control bar
            # 2.4.5. [Insert Image] button
            # open import image dialog
            title_designer_page.click_insert_image_btn()
            time.sleep(DELAY_TIME)

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_5_1.png', 'designer window')

            title_designer_page.press_esc_key()

        with uuid('d935011c-19c5-4958-9272-26b56128d20d') as case:
            # 2.4. Control bar
            # 2.4.6. [Insert background] button > Select import image
            # open import image dialog
            title_designer_page.click_insert_background_btn()
            time.sleep(DELAY_TIME)

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_6_1.png', 'designer window')

        with uuid('15bcb5d9-7c7c-4014-98b2-66cf0c6be6ba') as case:
            # 2.4. Control bar
            # 2.4.6. [Insert background] button > Background Media Adjustment settings > Stretch
            # set background adjustment type
            title_designer_page.insert_background(Test_Material_Folder + 'lake_001.jpg')

            check_result_1 = title_designer_page.insert_background_adjust_setting(index=0)  # stretch

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_6_2.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('6a8dc989-525d-4684-9aed-494694d81aca') as case:
            # 2.4. Control bar
            # 2.4.6. [Insert background] button > Background Media Adjustment settings > Letterbox
            # set background adjustment type
            title_designer_page.click_insert_background_btn()
            title_designer_page.insert_background(Test_Material_Folder + 'lake_001.jpg')
            check_result_1 = title_designer_page.insert_background_adjust_setting(index=1)  # letterbox, locator error

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_6_3.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('50840c67-42b8-4b39-98f7-366aac0bf777') as case:
            # 2.4. Control bar
            # 2.4.6. [Insert background] button > Background Media Adjustment settings > Crop
            # set background adjustment type
            title_designer_page.click_insert_background_btn()
            title_designer_page.insert_background(Test_Material_Folder + 'lake_001.jpg')
            check_result_1 = title_designer_page.insert_background_adjust_setting(index=2)  # crop, locator error

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_6_4.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('75bb0f97-d676-4407-bfbf-070aa6ec6694') as case:
            # 2.4. Control bar
            # 2.4.7. [Delete background] button
            # remove inserted background
            check_result_1 = title_designer_page.click_delete_background_btn()
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_7_1.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('1c4f5a5a-5cde-4d46-a553-a9b9569b1c5b') as case:
            # 2.4. Control bar
            # 2.4.8. [Undo] button
            # undo last action
            check_result_1 = title_designer_page.click_undo_btn()
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_8_1.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('be381478-a665-40ba-8492-b20711c5b37f') as case:
            # 2.4. Control bar
            # 2.4.9. [Redo] button
            # Redo last undo action
            check_result_1 = title_designer_page.click_redo_btn()
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_9_1.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('a1863831-db3d-422a-b790-8ee46f61caa2') as case:
            # 2.4. Control bar
            # 2.4.11. Zoom > [Zoom in] button
            # zoom in preview after click
            title_designer_page.click_zoom_in(times=3)

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_11_1.png', 'Preview')

        with uuid('c9a9876a-2a49-471e-88bb-4880528ca63f') as case:
            # 2.4. Control bar
            # 2.4.11. Zoom > [Zoom out] button
            # zoom out preview after click
            title_designer_page.click_zoom_out(times=4)

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_11_2.png', 'Preview')

        with uuid('5a751b77-36b1-4089-bec4-3f61f7fe2f58') as case:
            # 2.4. Control bar
            # 2.4.12. Viewer Zoom dropdown menu > 10%
            # set preview zoom to selected zoom
            title_designer_page.click_viewer_zoom_menu(value='10%')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_12_1.png', 'Preview')

        with uuid('ef5da168-ad14-4484-be92-1e9492cef61b') as case:
            # 2.4. Control bar
            # 2.4.12. Viewer Zoom dropdown menu > 25%
            # set preview zoom to selected zoom
            title_designer_page.click_viewer_zoom_menu(value='25%')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_12_2.png', 'Preview')

        with uuid('36710f3f-8f37-4c60-a43f-d366d281562e') as case:
            # 2.4. Control bar
            # 2.4.12. Viewer Zoom dropdown menu > 50%
            # set preview zoom to selected zoom
            title_designer_page.click_viewer_zoom_menu(value='50%')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_12_3.png', 'Preview')

        with uuid('ed215a0c-d8fa-4e3f-b813-06672b3491c8') as case:
            # 2.4. Control bar
            # 2.4.12. Viewer Zoom dropdown menu > 75%
            # set preview zoom to selected zoom
            title_designer_page.click_viewer_zoom_menu(value='75%')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_12_4.png', 'Preview')

        with uuid('3c145889-fad2-4cf1-8279-862ce8fab9e9') as case:
            # 2.4. Control bar
            # 2.4.12. Viewer Zoom dropdown menu > 100%
            # set preview zoom to selected zoom
            title_designer_page.click_viewer_zoom_menu(value='100%')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_12_5.png', 'Preview')

        with uuid('85140955-02a4-4d70-be01-c83fe3a83b4a') as case:
            # 2.4. Control bar
            # 2.4.12. Viewer Zoom dropdown menu > 200%
            # set preview zoom to selected zoom
            title_designer_page.click_viewer_zoom_menu(value='200%')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_12_6.png', 'Preview')

        with uuid('7b2fcbbe-8901-4856-ba73-fd22604b29d9') as case:
            # 2.4. Control bar
            # 2.4.12. Viewer Zoom dropdown menu > 300%
            # set preview zoom to selected zoom
            title_designer_page.click_viewer_zoom_menu(value='300%')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_12_7.png', 'Preview')

        with uuid('1b13c856-db50-4224-8bc7-a3b332fdd653') as case:
            # 2.4. Control bar
            # 2.4.12. Viewer Zoom dropdown menu > 400%
            # set preview zoom to selected zoom
            title_designer_page.click_viewer_zoom_menu(value='400%')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_12_8.png', 'Preview')

        with uuid('4e5fddbd-395d-452f-b164-1c609615022d') as case:
            # 2.4. Control bar
            # 2.4.12. Viewer Zoom dropdown menu > Fit
            # set preview zoom to selected zoom
            title_designer_page.click_viewer_zoom_menu(value='Fit')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_12_9.png', 'Preview')

        with uuid('d79d4ab2-5cf7-4056-b4aa-d027d843a4c4') as case:
            # 2.4. Control bar
            # 2.4.13. Playback controls > Play/Pause
            # play or pause preview
            title_designer_page.click_preview_operation('Play')
            check_result_1 = title_designer_page.exist(L.title_designer.operation.btn_pause).AXEnabled
            time.sleep(DELAY_TIME * 3)

            title_designer_page.click_preview_operation('Pause')
            check_result_2 = title_designer_page.exist(L.title_designer.operation.btn_play).AXEnabled
            case.result = check_result_1 and check_result_2

        with uuid('0837877b-d256-4a9b-be52-7d067a929e6d') as case:
            # 2.4. Control bar
            # 2.4.13. Playback controls > Next Frame
            # go to next frame
            old_timecode = title_designer_page.find(L.title_designer.area.timecode).AXValue
            old_timecode_list = list(old_timecode)
            old_timecode_list[10] = int(old_timecode_list[10]) + 3
            if old_timecode_list[10] > 9:
                old_timecode_list[10] = str(int(old_timecode_list[10]) - 10)
                old_timecode_list[9] = int(old_timecode_list[9]) + 1
                if old_timecode_list[9] > 2:
                    old_timecode_list[9] = str(int(old_timecode_list[9]) - 3)
                    old_timecode_list[7] = str(int(old_timecode_list[7]) + 1)
                old_timecode_list[9] = str(int(old_timecode_list[9]))
            else:
                old_timecode_list[10] = str(int(old_timecode_list[10]))

            new_timecode = ''.join(old_timecode_list)
            for number_of_clicks in range(3):
                title_designer_page.click_preview_operation('Next_Frame')

            current_timecode = title_designer_page.find(L.title_designer.area.timecode).AXValue
            case.result = False if not current_timecode == new_timecode else True

            logger('old_timecode = ' + old_timecode)
            logger('new_timecode = ' + new_timecode)
            logger('current_timecode = ' + current_timecode)

        with uuid('7865f96d-5396-44fd-8b75-76a05eb3b32c') as case:
            # 2.4. Control bar
            # 2.4.13. Playback controls > Previous Frame
            # go to previous frame
            old_timecode = title_designer_page.find(L.title_designer.area.timecode).AXValue
            old_timecode_list = list(old_timecode)
            old_timecode_list[10] = int(old_timecode_list[10]) - 2
            if old_timecode_list[10] < 1:
                old_timecode_list[10] = str(int(old_timecode_list[10]) + 10)
                if old_timecode_list[9] == '0':
                    old_timecode_list[9] = int(old_timecode_list[9]) + 2
                    if old_timecode_list[9] == 2:
                        old_timecode_list[9] = str(int(old_timecode_list[9]))
                        old_timecode_list[7] = str(int(old_timecode_list[7]) - 1)
                elif old_timecode_list[9] != '0':
                    old_timecode_list[9] = str(int(old_timecode_list[9]) - 1)
                old_timecode_list[9] = str(int(old_timecode_list[9]))
            else:
                old_timecode_list[10] = str(int(old_timecode_list[10]))

            new_timecode = ''.join(old_timecode_list)
            for number_of_clicks in range(2):
                title_designer_page.click_preview_operation('Previous_Frame')

            current_timecode = title_designer_page.find(L.title_designer.area.timecode).AXValue
            case.result = False if not current_timecode == new_timecode else True

            logger('old_timecode = ' + old_timecode)
            logger('new_timecode = ' + new_timecode)
            logger('current_timecode = ' + current_timecode)

        with uuid('109b2da5-886a-4561-a439-b958774dce2b') as case:
            # 2.4. Control bar
            # 2.4.13. Playback controls > Stop
            # stop preview
            title_designer_page.click_preview_operation('Stop')

            current_timecode = title_designer_page.find(L.title_designer.area.timecode).AXValue
            case.result = False if not current_timecode == '00;00;00;00' else True

        with uuid('04e6e277-7b5b-444c-b4c8-414c2afeaabf') as case:
            # 2.4. Control bar
            # 2.4.13. Playback controls > Timecode
            # display correct timecode
            case.result = False if not current_timecode == '00;00;00;00' else True

        with uuid('63481a2b-7b59-4907-b7a8-d4adbbf9dd7f') as case:
            # 2.4. Control bar
            # 2.4.13. Playback controls > Fast Forward
            # fast forward preview (2x, 4x, 8x, 16x)
            title_designer_page.click_preview_operation('Fast_Forward')  # FFx2
            check_result_1 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_13_1.png', 'Preview')
            time.sleep(DELAY_TIME * 5.5)

            for number_of_clicks in range(2):  # FFx4
                title_designer_page.click_preview_operation('Fast_Forward')
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_13_2.png', 'Preview')
            time.sleep(DELAY_TIME * 3.5)

            for number_of_clicks in range(3):  # FFx8
                title_designer_page.click_preview_operation('Fast_Forward')
            check_result_3 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_13_3.png', 'Preview')
            time.sleep(DELAY_TIME * 2)

            for number_of_clicks in range(4):  # FFx16
                title_designer_page.click_preview_operation('Fast_Forward')
            check_result_4 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_13_4.png', 'Preview')
            time.sleep(DELAY_TIME * 1.5)

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid('aae08066-3830-45a7-80a9-399021740e12') as case:
            # 2.4. Control bar
            # 2.4.19. Right Click Menu > Insert New Title
            # insert a new title
            main_page.insert_media('Food.jpg')
            main_page.select_library_icon_view_media("Landscape 01.jpg")
            main_page.tips_area_insert_media_to_selected_track(option=1)
            main_page.select_timeline_media('Food.jpg')
            main_page.enter_room(1)
            main_page.drag_media_to_timeline_playhead_position('Default', track_no=2)
            main_page.select_timeline_media('My Title')
            timeline_operation_page.double_click()
            title_designer_page.switch_mode(2)  # advanced mode
            title_designer_page.press_backspace_key()  # delete default title text

            title_designer_page.right_click(L.title_designer.area.frame_video_preview)
            title_designer_page.select_right_click_menu('Insert New Title')
            title_designer_page.keyboard.send('auto test')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_19_1.png', 'Preview')

        with uuid('172c675b-eccc-4734-93a5-7dee51020b98') as case:
            # 2.4. Control bar
            # 2.4.19. Right Click Menu > Copy
            # copy selected object
            title_designer_page.right_click(L.title_designer.area.view_title)
            title_designer_page.select_right_click_menu('Copy')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_19_2.png', 'Preview')

        with uuid('443ce137-2045-429b-97ed-c4f7ff213578') as case:
            # 2.4. Control bar
            # 2.4.19. Right Click Menu > Cut
            # cut selected object
            title_designer_page.right_click(L.title_designer.area.view_title)
            title_designer_page.select_right_click_menu('Cut')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_19_3.png', 'Preview')

        with uuid('d138d6f9-2afa-4db0-ae12-7b9e80fc200e') as case:
            # 2.4. Control bar
            # 2.4.19. Right Click Menu > Paste
            # paste cut or copied object
            title_designer_page.right_click(L.title_designer.area.frame_video_preview)
            title_designer_page.select_right_click_menu('Paste')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_19_4.png', 'Preview')

        with uuid('d6b0fb64-8e90-40c8-8750-b708e837c6bd') as case:
            # 2.4. Control bar
            # 2.4.19. Right Click Menu > Delete
            # remove selected object
            title_designer_page.right_click(L.title_designer.area.view_title)
            title_designer_page.select_right_click_menu('Delete')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_19_5.png', 'Preview')

            title_designer_page.click_undo_btn()

        with uuid('0e24852d-b0d0-4882-b14b-ec58bf4ef46a') as case:
            # 2.4. Control bar
            # 2.4.19. Right Click Menu > Align to > Left
            # align object(Text & Image)s
            title_designer_page.right_click(L.title_designer.area.view_title)
            title_designer_page.select_right_click_menu('Align to', 'Left')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_19_6.png', 'Preview')

        with uuid('af564339-9dc5-4eca-877c-331f2f2dc984') as case:
            # 2.4. Control bar
            # 2.4.19. Right Click Menu > Align to > Right
            # align object(Text & Image)s
            title_designer_page.right_click(L.title_designer.area.view_title)
            title_designer_page.select_right_click_menu('Align to', 'Right')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_19_7.png', 'Preview')

        with uuid('345bfaf2-a23d-4fe4-a58d-bffe45b64591') as case:
            # 2.4. Control bar
            # 2.4.19. Right Click Menu > Align to > Top
            # align object(Text & Image)s
            title_designer_page.right_click(L.title_designer.area.view_title)
            title_designer_page.select_right_click_menu('Align to', 'Top')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_19_8.png', 'Preview')

        with uuid('aed4257f-fcfb-4c35-9d30-ddae5ce01c51') as case:
            # 2.4. Control bar
            # 2.4.19. Right Click Menu > Align to > Bottom
            # align object(Text & Image)s
            title_designer_page.right_click(L.title_designer.area.view_title)
            title_designer_page.select_right_click_menu('Align to', 'Bottom')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_19_9.png', 'Preview')

        with uuid('fbcddea1-4204-4270-89a6-86483b833463') as case:
            # 2.4. Control bar
            # 2.4.19. Right Click Menu > Align to > Horizontal Center
            # align object(Text & Image)s
            title_designer_page.right_click(L.title_designer.area.view_title)
            title_designer_page.select_right_click_menu('Align to', 'Horizontal Center')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_19_10.png', 'Preview')

        with uuid('95cd7b68-e5bb-4cc9-bf2a-8cd30002df63') as case:
            # 2.4. Control bar
            # 2.4.19. Right Click Menu > Align to > Vertical Center
            # align object(Text & Image)s
            title_designer_page.right_click(L.title_designer.area.view_title)
            title_designer_page.select_right_click_menu('Align to', 'Vertical Center')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_19_11.png', 'Preview')

        with uuid('46f2cd4e-96eb-492d-b4bb-7fa83bde4e73') as case:
            # 2.4. Control bar
            # 2.4.15. [Align object(Text & Image)s] button > Align Left > Align to Canvas
            # Align object (Text & Image)
            title_designer_page.click_align_object_btn()
            title_designer_page.select_right_click_menu('Align Left')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_15_1.png', 'Preview')

        with uuid('46512f82-bc59-4bc1-b476-f986e712152f') as case:
            # 2.4. Control bar
            # 2.4.15. [Align object(Text & Image)s] button > Align Right > Align Selected Objects
            # Align object (Text & Image)
            title_designer_page.click_align_object_btn()
            title_designer_page.select_right_click_menu('Align Right')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_15_2.png', 'Preview')

        with uuid('2f1c7258-8e38-4dd8-b6b8-98c978e4bc1d') as case:
            # 2.4. Control bar
            # 2.4.15. [Align object(Text & Image)s] button > Align Top > Align to Canvas
            # Align object (Text & Image)
            title_designer_page.click_align_object_btn()
            title_designer_page.select_right_click_menu('Align Top')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_15_3.png', 'Preview')

        with uuid('795b268f-b6dc-4937-a8e4-93da4b25801c') as case:
            # 2.4. Control bar
            # 2.4.15. [Align object(Text & Image)s] button > Align Bottom > Align Selected Objects
            # Align object (Text & Image)
            title_designer_page.click_align_object_btn()
            title_designer_page.select_right_click_menu('Align Bottom')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_15_4.png', 'Preview')

        with uuid('4f89ae42-cd4f-4f9d-b067-f0b46ecf3157') as case:
            # 2.4. Control bar
            # 2.4.15. [Align object(Text & Image)s] button > Horizontal Center > Align to Canvas
            # Align object (Text & Image)
            title_designer_page.click_align_object_btn()
            title_designer_page.select_right_click_menu('Horizontal Center')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_15_5.png', 'Preview')

        with uuid('832f7785-bba6-461f-bb69-3c860f52763a') as case:
            # 2.4. Control bar
            # 2.4.15. [Align object(Text & Image)s] button > Vertical Center > Align Selected Objects
            # Align object (Text & Image)
            title_designer_page.click_align_object_btn()
            title_designer_page.select_right_click_menu('Vertical Center')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_15_6.png', 'Preview')

        with uuid('9c6d6675-4295-4c90-a408-1fe8cfceb089') as case:
            # 2.4. Control bar
            # 2.4.16. Toggle TV safe zone and grid lines on/off > Snap to Reference Lines
            # object will snap after select
            title_designer_page.select_grid_lines_format(2)  # 2x2 grid lines
            title_designer_page.apply_snap_ref_line(bApply=0)

            title_pos = title_designer_page.get_position(L.title_designer.area.view_title)
            title_designer_page.drag_mouse((title_pos['x'] + 20, title_pos['y']),
                                           (title_pos['x'] + 20, title_pos['y'] + (title_pos['h'] / 2) - 3))

            check_result_1 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_16_1.png', 'Preview')
            title_designer_page.click_undo_btn()

            title_designer_page.apply_snap_ref_line(bApply=1)

            title_pos = title_designer_page.get_position(L.title_designer.area.view_title)
            title_designer_page.drag_mouse((title_pos['x'] + 20, title_pos['y']),
                                           (title_pos['x'] + 20, title_pos['y'] + (title_pos['h'] / 2) - 3))

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_16_2.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('db83e7bc-3cb5-4b20-9316-4c2d4a991709') as case:
            # 2.4. Control bar
            # 2.4.16. Toggle TV safe zone and grid lines on/off > Grid Lines > 2 x 2
            # show grid lines
            case.result = check_result_1

        with uuid('b46d08f7-8dff-41a1-9221-51aa619d74e5') as case:
            # 2.4. Control bar
            # 2.4.18. Modify object on Canvas > Move
            # move object by drag
            case.result = check_result_2

        with uuid('713566dc-11c4-4f99-904c-66165370b557') as case:
            # 2.4. Control bar
            # 2.4.18. Modify object on Canvas > Resize
            # resize object by drag edges
            title_pos = title_designer_page.get_position(L.title_designer.area.view_title)
            title_designer_page.drag_mouse((title_pos['x'], title_pos['y']),
                                           (title_pos['x'] - 20, title_pos['y'] - 20))

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_18_1.png', 'Preview')

            title_designer_page.click_undo_btn()

        with uuid('a7454300-ad16-4693-be36-01b48fc5a83b') as case:
            # 2.4. Control bar
            # 2.4.19. Right Click Menu > Insert New Image...
            # open import image dialog
            title_designer_page.right_click(L.title_designer.area.frame_preview)
            title_designer_page.select_right_click_menu('Insert New Image...')
            title_designer_page.select_file(Test_Material_Folder + 'lake_001.jpg')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_19_12.png', 'Preview')

            title_designer_page.click_undo_btn()

        with uuid('bcf73cd4-3547-4d24-ba18-2d887c05bd4a') as case:
            # 2.4. Control bar
            # 2.4.19. Right Click Menu > Insert New Particle...
            # open import particle dialog
            title_designer_page.right_click(L.title_designer.area.frame_video_preview)
            title_designer_page.select_right_click_menu('Insert New Particle...')
            title_designer_page.insert_particle(menu_index=0, particle_index=0)
            title_designer_page.set_timecode('00_00_03_00')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_19_13.png', 'Preview')

        with uuid('f1d37b8b-e54e-45b7-b928-9188c9b35d91') as case:
            # 2.4. Control bar
            # 2.4.16. Toggle TV safe zone and grid lines on/off > Grid Lines > 3 x 3
            # show grid lines
            check_result_1 = title_designer_page.select_grid_lines_format(3)  # 3x3 grid lines

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_16_3.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('cf584a19-d732-4176-ab87-7f00fcd3c2cb') as case:
            # 2.4. Control bar
            # 2.4.16. Toggle TV safe zone and grid lines on/off > Grid Lines > 4 x 4
            # show grid lines
            check_result_1 = title_designer_page.select_grid_lines_format(4)  # 4x4 grid lines

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_16_4.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('5f910939-64b9-4f88-9597-f8158b5d88ca') as case:
            # 2.4. Control bar
            # 2.4.16. Toggle TV safe zone and grid lines on/off > Grid Lines > 5 x 5
            # show grid lines
            check_result_1 = title_designer_page.select_grid_lines_format(5)  # 5x5 grid lines

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_16_5.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('bb911dee-baa6-4a02-9fff-4892cd77d0b6') as case:
            # 2.4. Control bar
            # 2.4.16. Toggle TV safe zone and grid lines on/off > Grid Lines > 6 x 6
            # show grid lines
            check_result_1 = title_designer_page.select_grid_lines_format(6)  # 6x6 grid lines

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_16_6.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('9f8960df-7349-43a6-9d1e-7be731c1fc46') as case:
            # 2.4. Control bar
            # 2.4.16. Toggle TV safe zone and grid lines on/off > Grid Lines > 7 x 7
            # show grid lines
            check_result_1 = title_designer_page.select_grid_lines_format(7)  # 7x7 grid lines

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_16_7.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('6d4494d9-393b-4834-9c6e-a10a0af3ea18') as case:
            # 2.4. Control bar
            # 2.4.16. Toggle TV safe zone and grid lines on/off > Grid Lines > 8 x 8
            # show grid lines
            check_result_1 = title_designer_page.select_grid_lines_format(8)  # 8x8 grid lines

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_16_8.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('7e98f3f2-241e-41c5-8ab4-5b98a2f4d320') as case:
            # 2.4. Control bar
            # 2.4.16. Toggle TV safe zone and grid lines on/off > Grid Lines > 9 x 9
            # show grid lines
            check_result_1 = title_designer_page.select_grid_lines_format(9)  # 9x9 grid lines

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_16_9.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('4c4c65b4-10e8-41c5-8424-7b8dd55aa8ad') as case:
            # 2.4. Control bar
            # 2.4.16. Toggle TV safe zone and grid lines on/off > Grid Lines > 10 x 10
            # show grid lines
            check_result_1 = title_designer_page.select_grid_lines_format(10)  # 10x10 grid lines

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_16_10.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('79e089d4-fcc1-4b31-bcdb-52c336f71fa5') as case:
            # 2.4. Control bar
            # 2.4.16. Toggle TV safe zone and grid lines on/off > Grid Lines > None
            # no grid line
            check_result_1 = title_designer_page.select_grid_lines_format(1)  # none grid line

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_4_16_11.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('56ad9555-c207-4a1a-b174-072b82e285f0') as case:
            # 2.4. Control bar
            # 2.4.17. Timecode Mode > Movie Timecode
            # show timecode with movie mode
            title_designer_page.switch_timecode_mode(mode=2)  # switch to movie mode

            current_timecode = title_designer_page.exist(L.title_designer.area.timecode).AXValue
            case.result = False if not current_timecode == '00;00;08;00' else True

        with uuid('7a97a38a-2c82-4b0d-8fe0-ea8f5ddc13c3') as case:
            # 2.4. Control bar
            # 2.4.17. Timecode Mode > Clip Timecode
            # show timecode with clip mode
            title_designer_page.switch_timecode_mode(mode=1)  # switch to clip mode

            current_timecode = title_designer_page.exist(L.title_designer.area.timecode).AXValue
            case.result = False if not current_timecode == '00;00;03;00' else True

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid('d2c7f837-f299-4364-a331-6e1ff9a6575b') as case:
            # 2.5. Input Title
            # 2.5.1. Input Title > From preview canvas
            # input text directly on canvas
            main_page.enter_room(1)
            title_room_page.click_CreateNewTitle_btn()
            title_designer_page.switch_mode(2)  # advanced mode
            title_designer_page.press_backspace_key()  # delete default title text
            title_designer_page.double_click(L.title_designer.area.frame_video_preview)
            title_designer_page.keyboard.send('Title 1')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_5_1_1.png', 'Preview')

        with uuid('52e1405f-7be8-43bf-8b46-fa35d907a233') as case:
            # 2.5. Input Title
            # 2.5.1. Input Title > From edit box (upper left)
            # input text from textbox on designer top-left
            title_designer_page.exist_click(L.title_designer.area.edittext_text_content)
            title_designer_page.keyboard.send('許功蓋')

            check_result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_5_1_2.png', 'Preview')
            case.result = check_result

        with uuid('24c5930c-76f9-4b3c-a907-2c8ad04ef0b5') as case:
            # 2.5. Input Title
            # 2.5.1. Input Title > Unicode
            # input unicode text
            case.result = check_result

        with uuid('6cc5de1e-52f7-491a-b698-85274940f61e') as case:
            # 2.5. Input Title
            # 2.5.1. Input Title > Multiple lines
            # input multiple lines text
            with title_designer_page.keyboard.pressed(main_page.keyboard.key.enter):
                pass
            title_designer_page.keyboard.send('~!@#$%^&*()')

            check_result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_5_1_3.png', 'Preview')
            case.result = check_result

        with uuid('6ac79855-021a-4041-b86e-ce71f930642d') as case:
            # 2.5. Input Title
            # 2.5.1. Input Title > Special symbols
            # input special symbols as text (!@#$...)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid('972cc116-57ad-4598-8ef5-58f6cec67403') as case:
            # 2.6. Object Tab
            # 2.6.1. Character Presets > Select a preset
            # apply preset to title
            main_page.enter_room(1)
            title_room_page.click_CreateNewTitle_btn()
            title_designer_page.switch_mode(2)  # advanced mode
            title_designer_page.click_object_tab()
            title_designer_page.unfold_object_character_presets_tab(unfold=1)
            title_designer_page.exist_click(L.title_designer.area.edittext_text_content)  # input multiple lines title
            with title_designer_page.keyboard.pressed(main_page.keyboard.key.enter):
                pass
            title_designer_page.keyboard.send('My Title 1')
            # workaround, de-activate in title edit box
            title_pos = title_designer_page.get_position(L.title_designer.area.view_title)
            title_designer_page.drag_mouse((title_pos['x'], title_pos['y']), (title_pos['x'], title_pos['y']))
            title_designer_page.apply_character_presets(index=12, character_type=1)  # no.13 preset, default list

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_1_1.png', 'Preview')

        with uuid('ccb58acf-e3d9-4e7e-9c7c-82d4006256c5') as case:
            # 2.6. Object Tab
            # 2.6.1. Character Presets > Save currently as preset button
            # save current font settings as a custom preset
            title_designer_page.save_as_new_preset()

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_1_2.png', 'Object')

        with uuid('f4c811cb-8650-4e2c-946f-2474d9acbe3f') as case:
            # 2.6. Object Tab
            # 2.6.1. Character Presets > Type Filter
            # sort by type dropdown menu
            title_designer_page.exist_click(L.title_designer.character_presets.cbx_character_types)
            title_designer_page.exist_click(L.title_designer.character_presets.option_default)

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_1_3.png', 'Object')

            title_designer_page.unfold_object_character_presets_tab(unfold=0)  # unfold character presets

        with uuid('728f085d-44d4-4634-9701-77e2f3eb1c4b') as case:
            # 2.6. Object Tab
            # 2.6.2. Font/Paragraph > Font Type
            # select font from dropdown menu
            title_designer_page.unfold_object_font_paragraph_tab(unfold=1)
            check_result_1 = title_designer_page.set_font_type('Arial')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_2_1.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('4654c205-6a9c-4d00-aad8-1bb53adb38ae') as case:
            # 2.6. Object Tab
            # 2.6.2. Font/Paragraph > Font Size
            # select or input font size
            check_result_1 = title_designer_page.set_font_size('55')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_2_2.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('b33d3b22-521b-40e8-a9dd-1c4edadd5e01') as case:
            # 2.6. Object Tab
            # 2.6.2. Font/Paragraph > Font color
            # open color selector to select color
            check_result_1 = title_designer_page.set_font_face_color(red='0', green='0', blue='240')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_2_3.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('07526b81-f4ff-41f9-ab06-f22832ad04bf') as case:
            # 2.6. Object Tab
            # 2.6.2. Font/Paragraph > Line Spacing
            # select or input value
            check_result_1 = title_designer_page.set_line_spacing_amount('5')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_2_4.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('8fd079b5-fe59-4127-bb2d-e162ad942c66') as case:
            # 2.6. Object Tab
            # 2.6.2. Font/Paragraph > Text Spacing
            # select or input value
            check_result_1 = title_designer_page.set_text_spacing_amount('5')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_2_5.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('c828af7a-6482-46a4-8d7c-cf47ec0b9471') as case:
            # 2.6. Object Tab
            # 2.6.2. Font/Paragraph > Kerning
            # apply kerning effect to title after select
            check_result_1 = title_designer_page.set_kerning_check(bCheck=1)

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_2_6.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('eeee331c-4a9c-4658-b2e9-95767e02c759') as case:
            # 2.6. Object Tab
            # 2.6.2. Font/Paragraph > Bold
            # set font bold setting
            check_result_1 = title_designer_page.click_bold_btn()

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_2_7.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('dcddd0fc-2508-4905-8549-7561d1e9a218') as case:
            # 2.6. Object Tab
            # 2.6.2. Font/Paragraph > Italic
            # set font italic setting
            check_result_1 = title_designer_page.click_italic_btn()

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_2_8.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('afce256a-9bdc-4c38-b783-8f1c3cd5b929') as case:
            # 2.6. Object Tab
            # 2.6.2. Font/Paragraph > Align Center
            # align center after select
            check_result_1 = title_designer_page.set_align(2)  # Align center

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_2_9.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('944bf1eb-de56-42e1-90e4-e9d8d0f9d1a6') as case:
            # 2.6. Object Tab
            # 2.6.2. Font/Paragraph > Align Right
            # align right after select
            check_result_1 = title_designer_page.set_align(3)  # align right

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_2_10.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('6216bdab-880a-4e4b-a1b0-f904b342a290') as case:
            # 2.6. Object Tab
            # 2.6.2. Font/Paragraph > Align Left
            # align left after select
            check_result_1 = title_designer_page.set_align(1)  # align left

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_2_11.png', 'designer window')
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        with uuid('90ea8c5d-5fda-49b2-a58b-674d3a1a21dd') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Blur > Default value
            # default value should be 0
            main_page.enter_room(1)
            title_room_page.click_CreateNewTitle_btn()
            title_designer_page.switch_mode(2)  # advanced mode
            title_designer_page.click_object_tab()
            default_setting_check = title_designer_page.exist(L.title_designer.font_face.chx_font_face).AXValue
            title_designer_page.unfold_object_font_face_tab(unfold=1)
            default_value_check = title_designer_page.exist(L.title_designer.font_face.edittext_blur).AXValue

            check_result_1 = False if not default_value_check == '0' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_1.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('6a7dd0db-b801-4e54-a747-4835dbce6999') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Blur > Max
            # max value should be 20
            title_designer_page.drag_font_face_blur_slider(value='100')

            current_value = title_designer_page.exist(L.title_designer.font_face.edittext_blur).AXValue
            check_result_1 = False if not current_value == '20' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_2.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('ff00b0ae-caad-414f-bb3c-2946849bad84') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Blur > Min
            # minimal value should be 0
            title_designer_page.drag_font_face_blur_slider(value='0')

            current_value = title_designer_page.exist(L.title_designer.font_face.edittext_blur).AXValue
            check_result_1 = False if not current_value == '0' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_3.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('a9cb5a23-b35d-414a-a5e4-1002d9b304b6') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Blur > Slider
            # use slider to set value
            case.result = check_result_1 and check_result_2

        with uuid('a8526ce1-9907-4569-a55b-cc3aafe10366') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Blur > Input value
            # direct input to set value
            title_designer_page.input_font_face_blur_value(value='10')

            current_value = title_designer_page.exist(L.title_designer.font_face.edittext_blur).AXValue
            check_result_1 = False if not current_value == '10' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_4.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('1e1cf25b-3de6-430a-ad3d-9c16777bd509') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Blur > ^/v button
            # use buttons to set value
            for number_of_clicks in range(3):
                title_designer_page.click_font_face_blur_arrow_btn(option=0)  # click up arrow btn

            current_value = title_designer_page.exist(L.title_designer.font_face.edittext_blur).AXValue
            check_result_1 = False if not current_value == '13' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_5.png', 'Preview')

            for number_of_clicks in range(4):
                title_designer_page.click_font_face_blur_arrow_btn(option=1)  # click down arrow btn

            current_value = title_designer_page.exist(L.title_designer.font_face.edittext_blur).AXValue
            check_result_3 = False if not current_value == '9' else True
            check_result_4 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_6.png', 'Preview')

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('1356b91e-2353-4165-b0c5-65bdb9f0163f') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Opacity > Default value
            # default value should be 100%
            default_value_check = title_designer_page.exist(L.title_designer.font_face.edittext_opacity).AXValue
            check_result_1 = False if not default_value_check == '100%' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_7.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('3a85a783-561e-4144-88cd-c03d5f31f407') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Opacity > Min
            # minimal value should be 0%
            title_designer_page.drag_font_face_opacity_slider(value='0')

            current_value = title_designer_page.exist(L.title_designer.font_face.edittext_opacity).AXValue
            check_result_1 = False if not current_value == '0%' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_8.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('30f7a220-2880-47dd-a6c6-2a6dcfc4f53e') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Opacity > Max
            # max value should be 100%
            title_designer_page.drag_font_face_opacity_slider(value='100')

            current_value = title_designer_page.exist(L.title_designer.font_face.edittext_opacity).AXValue
            check_result_1 = False if not current_value == '100%' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_9.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('e785372d-3a53-4343-abf5-2e1437d65221') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Opacity > Slider
            # use slider to set value
            case.result = check_result_1 and check_result_2

        with uuid('12fe0304-5568-4bee-8a43-9491ad2122e2') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Opacity > Input value
            # direct input to set value
            title_designer_page.input_font_face_opacity_value(value='90')

            current_value = title_designer_page.exist(L.title_designer.font_face.edittext_opacity).AXValue
            check_result_1 = False if not current_value == '90%' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_10.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('8330a00f-f8e6-4ade-b3dc-5a4d12f79def') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Opacity > ^/v button
            # use buttons to set value
            title_designer_page.drag_font_face_opacity_slider(value='95')
            for number_of_clicks in range(3):
                title_designer_page.click_font_face_opacity_arrow_btn(option=0)  # click up arrow btn

            current_value = title_designer_page.exist(L.title_designer.font_face.edittext_opacity).AXValue
            check_result_1 = False if not current_value == '98%' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_11.png', 'Preview')

            for number_of_clicks in range(4):
                title_designer_page.click_font_face_opacity_arrow_btn(option=1)  # click down arrow btn

            current_value = title_designer_page.exist(L.title_designer.font_face.edittext_opacity).AXValue
            check_result_3 = False if not current_value == '94%' else True
            check_result_4 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_12.png', 'Preview')

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('ffb8484b-0058-4ae4-9a04-70d824add3e0') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Fill Type > Uniform Color
            # select color
            check_result_1 = title_designer_page.apply_font_face_uniform_color(red='255', green='0', blue='0')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_13.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('a2d13b97-ad10-40e4-8f17-15eb667fa1a6') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Fill Type > 2 Color Gradient
            # select color
            check_result_1 = title_designer_page.apply_font_face_2_color(red1='255', green1='255', blue1='255',
                                                                         red2='0', green2='255', blue2='0')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_14.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('6b7fedcc-aea4-401b-9325-e967084316dc') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Fill Type > 4 Color Gradient
            # select color
            check_result_1 = title_designer_page.apply_font_face_4_color(red1='0', green1='0', blue1='255',
                                                                         red2='255', green2='0', blue2='0',
                                                                         red3='0', green3='255', blue3='0',
                                                                         red4='255', green4='255', blue4='255')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_15.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('4cc305f8-e86e-48d3-a832-42f8c6f1943c') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Apply Font Face > Untick
            # untick to disapply font face settings
            check_result_1 = title_designer_page.set_check_font_face(bCheck=0)
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_16.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('7d1234fd-c6e9-453f-9cb6-98c7e1048e6d') as case:
            # 2.6. Object Tab
            # 2.6.3. Font Face > Apply Font Face > Tick(Default)
            # tick to apply font face settings
            title_designer_page.set_check_font_face(bCheck=1)

            check_result_1 = False if not default_setting_check == 1 else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_3_17.png', 'designer window')
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        with uuid('3736e5d7-dd11-4551-bb4f-fab908253a3f') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Size > Default value
            # default value should be 3
            main_page.enter_room(1)
            title_room_page.click_CreateNewTitle_btn()
            title_designer_page.switch_mode(2)  # advanced mode
            title_designer_page.click_object_tab()
            default_setting_check = title_designer_page.exist(L.title_designer.border.chx_border).AXValue
            title_designer_page.unfold_object_border_tab(unfold=1)
            title_designer_page.set_check_border(bCheck=1)
            default_value_check = title_designer_page.exist(L.title_designer.border.edittext_size).AXValue

            check_result_1 = False if not default_value_check == '3' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_1.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('5d5171b0-aad2-4fe5-86d6-c08b613d5f48') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Size > Min
            # minimal value should be 0
            title_designer_page.drag_border_size_slider(value='0')

            current_value = title_designer_page.exist(L.title_designer.border.edittext_size).AXValue
            check_result_1 = False if not current_value == '0' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_2.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('c850618b-f07e-426a-94ad-f1959a3d8683') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Size > Max
            # max value should be 10
            title_designer_page.drag_border_size_slider(value='100')

            current_value = title_designer_page.exist(L.title_designer.border.edittext_size).AXValue
            check_result_1 = False if not current_value == '10' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_3.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('3bc39710-bb28-4b4e-8b52-2ff7b89ccdf5') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Size > Slider
            # use slider to set value
            case.result = check_result_1 and check_result_2

        with uuid('6c6694b1-72ce-463f-9cfd-77cbc8f27c90') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Size > Input value
            # direct input to set value
            title_designer_page.input_border_size_value(value='5')

            current_value = title_designer_page.exist(L.title_designer.border.edittext_size).AXValue
            check_result_1 = False if not current_value == '5' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_4.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('a139390c-5584-4887-a335-543ebde0990c') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Size > ^/v button
            # use buttons to set value
            for number_of_clicks in range(3):
                title_designer_page.click_size_value_arrow_btn(value=0)  # click up arrow btn

            current_value = title_designer_page.exist(L.title_designer.border.edittext_size).AXValue
            check_result_1 = False if not current_value == '8' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_5.png', 'Preview')

            for number_of_clicks in range(4):
                title_designer_page.click_size_value_arrow_btn(value=1)  # click down arrow btn

            current_value = title_designer_page.exist(L.title_designer.border.edittext_size).AXValue
            check_result_3 = False if not current_value == '4' else True
            check_result_4 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_6.png', 'Preview')

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('b443bfb1-c452-4ecd-9c3c-2893d1718966') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Blur > Default value
            # default value should be 0
            default_value_check = title_designer_page.exist(L.title_designer.border.edittext_blur).AXValue

            check_result_1 = False if not default_value_check == '0' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_7.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('9e26e9eb-4938-4618-8d7c-94c44b2df6fd') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Blur > Max
            # max value should be 20
            title_designer_page.drag_border_blur_slider(value='100')

            current_value = title_designer_page.exist(L.title_designer.border.edittext_blur).AXValue
            check_result_1 = False if not current_value == '20' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_8.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('5adbd1db-4cc0-449a-8e4b-548aff769e35') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Blur > Min
            # minimal value should be 0
            title_designer_page.drag_border_blur_slider(value='0')

            current_value = title_designer_page.exist(L.title_designer.border.edittext_blur).AXValue
            check_result_1 = False if not current_value == '0' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_9.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('a98dff12-de4d-4ed8-b7d6-b2947cff3b68') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Blur > Slider
            # use slider to set value
            case.result = check_result_1 and check_result_2

        with uuid('4550ab2a-906c-4210-ae66-f4e61db41ce7') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Blur > Input value
            # direct input to set value
            title_designer_page.input_border_blur_value(value='3')

            current_value = title_designer_page.exist(L.title_designer.border.edittext_blur).AXValue
            check_result_1 = False if not current_value == '3' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_10.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('e5c718c5-3eba-46f0-8784-b87b99e0261b') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Blur > ^/v button
            # use buttons to set value
            for number_of_clicks in range(3):
                title_designer_page.click_border_blur_arrow_btn(value=0)  # click up arrow btn

            current_value = title_designer_page.exist(L.title_designer.border.edittext_blur).AXValue
            check_result_1 = False if not current_value == '6' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_11.png', 'Preview')

            for number_of_clicks in range(4):
                title_designer_page.click_border_blur_arrow_btn(value=1)  # click down arrow btn

            current_value = title_designer_page.exist(L.title_designer.border.edittext_blur).AXValue
            check_result_3 = False if not current_value == '2' else True
            check_result_4 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_12.png', 'Preview')

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('8459a879-a0bf-43d7-8aab-c48c91eeb5c2') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Opacity > Default value
            # default value should be 100%
            default_value_check = title_designer_page.exist(L.title_designer.border.edittext_opacity).AXValue

            check_result_1 = False if not default_value_check == '100%' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_13.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('dcd3d1ae-084c-439f-8572-dadb1d9f2708') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Opacity > Min
            # minimal value should be 0%
            title_designer_page.drag_border_opacity_slider(value='0')

            current_value = title_designer_page.exist(L.title_designer.border.edittext_opacity).AXValue
            check_result_1 = False if not current_value == '0%' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_14.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('ef869857-0cd5-4236-9168-c1173322d717') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Opacity > Max
            # max value should be 100%
            title_designer_page.drag_border_opacity_slider(value='100')

            current_value = title_designer_page.exist(L.title_designer.border.edittext_opacity).AXValue
            check_result_1 = False if not current_value == '100%' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_15.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('2e08b699-3e95-4a9b-a993-0abb92bb7e13') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Opacity > Slider
            # use slider to set value
            case.result = check_result_1 and check_result_2

        with uuid('dc48860c-7e83-47ac-861a-ccdd5b7c7356') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Opacity > Input value
            # direct input to set value
            title_designer_page.input_border_opacity_value(value='90')

            current_value = title_designer_page.exist(L.title_designer.border.edittext_opacity).AXValue
            check_result_1 = False if not current_value == '90%' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_16.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('4797a9e9-8fee-4ec5-91d4-d9ec5456b164') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Opacity > ^/v button
            # use buttons to set value
            title_designer_page.drag_border_opacity_slider(value='95')
            for number_of_clicks in range(3):
                title_designer_page.click_border_opacity_value_arrow_btn(value=0)  # click up arrow btn

            current_value = title_designer_page.exist(L.title_designer.border.edittext_opacity).AXValue
            check_result_1 = False if not current_value == '98%' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_17.png', 'Preview')

            for number_of_clicks in range(4):
                title_designer_page.click_border_opacity_value_arrow_btn(value=1)  # click down arrow btn

            current_value = title_designer_page.exist(L.title_designer.border.edittext_opacity).AXValue
            check_result_3 = False if not current_value == '94%' else True
            check_result_4 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_18.png', 'Preview')

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('147c4d44-b86f-406a-b2f3-84ab8aafdbb4') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Fill Type > Uniform Color
            # select color
            check_result_1 = title_designer_page.apply_border_uniform_color(red='255', green='0', blue='0')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_19.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('b3abedb8-c23f-4e26-aa84-75efb85504b7') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Fill Type > 2 Color Gradient
            # select color
            check_result_1 = title_designer_page.apply_border_2_color(red1='255', green1='255', blue1='255',
                                                                      red2='0', green2='255', blue2='0')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_20.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('b5d3348a-7c95-4396-aa07-9759c043c103') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Fill Type > 4 Color Gradient
            # select color
            check_result_1 = title_designer_page.apply_border_4_color(red1='0', green1='0', blue1='255',
                                                                      red2='255', green2='0', blue2='0',
                                                                      red3='0', green3='255', blue3='0',
                                                                      red4='255', green4='255', blue4='255')

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_21.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('43ed0b3c-1164-404a-9cbf-f4b4831fa6b7') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Apply Border > Untick (Default)
            # untick to disapply settings
            title_designer_page.set_check_border(bCheck=0)

            check_result_1 = False if not default_setting_check == 0 else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_22.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('eb18d94c-d6f7-4c39-835b-53eabb9c49cf') as case:
            # 2.6. Object Tab
            # 2.6.4. Border > Apply Border > Tick
            # tick to apply settings
            check_result_1 = title_designer_page.set_check_border(bCheck=1)
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_4_23.png', 'designer window')
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        with uuid('0c042bcf-d1da-4f85-9d57-7e4736fa025c') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Checkbox > Untick (Default)
            # untick to dis-apply settings
            main_page.enter_room(1)
            title_room_page.click_CreateNewTitle_btn()
            title_designer_page.switch_mode(mode=2)  # switch to advanced mode
            title_designer_page.click_object_tab()
            default_setting_check = title_designer_page.exist(L.title_designer.shadow.chx_shadow).AXValue

            check_result_1 = False if not default_setting_check == 0 else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_1.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('c22a1813-a297-4874-ac27-cc3b4a66965a') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Checkbox > Tick
            # tick to apply settings
            title_designer_page.unfold_object_shadow_tab(unfold=1)
            title_designer_page.set_check_shadow(bCheck=1)

            check_status = title_designer_page.exist(L.title_designer.shadow.chx_shadow).AXValue
            check_result_1 = False if not check_status == 1 else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_2.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('26aea84f-f660-41c8-aeb2-9e3037ba9d58') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Apply shadow to > Text and Border
            # display shadow as selected setting
            title_designer_page.unfold_object_shadow_tab(unfold=0)
            title_designer_page.set_check_border(bCheck=1)
            title_designer_page.set_check_shadow(bCheck=1)
            title_designer_page.unfold_object_shadow_tab(unfold=1)
            title_designer_page.apply_shadow_to(index=0)

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_3.png', 'Preview')

        with uuid('f065e920-14b8-457d-ba0c-f1523db28a05') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Apply shadow to > Text Only
            # display shadow as selected setting
            title_designer_page.apply_shadow_to(index=1)

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_4.png', 'Preview')

        with uuid('9a71adaf-ee6d-4d72-bf70-2f9636c4fb79') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Apply shadow to > Border Only
            # display shadow as selected setting
            title_designer_page.apply_shadow_to(index=2)

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_5.png', 'Preview')

            title_designer_page.apply_shadow_to(index=0)  # restore to default setting

        with uuid('b178166e-b78c-456f-889d-ddbad6f90e21') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Distance > Default value
            # default value should be 3.0
            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_distance).AXValue

            case.result = False if not check_value == '3.0' else True

        with uuid('de61321a-dce5-4f41-9fa8-4e092cad4e61') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Distance > Min
            # minimal value should be 0.0
            title_designer_page.drag_shadow_distance_slider('0')

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_distance).AXValue
            check_result_1 = False if not check_value == '0.0' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_6.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('a310721e-8c1d-45d7-bd23-4396b24e33a9') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Distance > Max
            # max value should be 100
            title_designer_page.drag_shadow_distance_slider('100')

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_distance).AXValue
            check_result_1 = False if not check_value == '100.0' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_7.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('5dd4032c-04b5-4bb5-88e8-b7283add8a4c') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Distance > Slider
            # use slider to set value
            case.result = check_result_1 and check_result_2

        with uuid('8adeb943-497e-4df8-96d8-57f700f9e3f5') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Distance > Input value
            # direct input to set value
            title_designer_page.input_shadow_distance_value('20')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_8.png', 'Preview')

        with uuid('74679c4a-6521-4a85-9746-b9056be482a3') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Distance > ^/v button
            # use buttons to set value
            for number_of_clicks in range(3):
                title_designer_page.click_shadow_distance_arrow_btn(index=0)
            for number_of_clicks in range(2):
                title_designer_page.click_shadow_distance_arrow_btn(index=1)

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_distance).AXValue
            case.result = False if not check_value == '20.1' else True

        with uuid('3babadc2-4e19-487d-a493-c9b075ce7be5') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Blur > Default value
            # default value should be 0
            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_blur).AXValue

            case.result = False if not check_value == '0' else True

        with uuid('7632e42e-9156-47f0-8f1f-954b767b927a') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Blur > Min
            # minimal value should be 0
            title_designer_page.drag_shadow_blur_slider('0')

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_blur).AXValue
            check_result_1 = False if not check_value == '0' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_9.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('7818bf77-9c58-459b-972d-7967f0cd6a0c') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Blur > Max
            # max value should be 20
            title_designer_page.drag_shadow_blur_slider('100')

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_blur).AXValue
            check_result_1 = False if not check_value == '20' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_10.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('0d7d9bd4-fae4-44f8-857f-958e40e079c8') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Blur > Slider
            # use slider to set value
            case.result = check_result_1 and check_result_2

        with uuid('50e355dc-a6da-4743-986a-3612f385409f') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Blur > Input value
            # direct input to set value
            title_designer_page.input_shadow_blur_value('5')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_11.png', 'Preview')

        with uuid('82a61047-f9ed-4c61-9a03-6199062713a6') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Blur > ^/v button
            # use buttons to set value
            for number_of_clicks in range(3):
                title_designer_page.click_shadow_blur_arrow_btn(index=0)
            for number_of_clicks in range(2):
                title_designer_page.click_shadow_blur_arrow_btn(index=1)

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_blur).AXValue
            case.result = False if not check_value == '6' else True

        with uuid('6a6bee09-eb19-41b6-a9a1-e3bb78574285') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Opacity > Default value
            # default value should be 100%
            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_opacity).AXValue

            case.result = False if not check_value == '100%' else True

        with uuid('fc92aceb-9e9b-4dae-82e3-b5f927661618') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Opacity > Min
            # minimal value should be 0%
            title_designer_page.drag_shadow_opacity_slider('0')

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_opacity).AXValue
            check_result_1 = False if not check_value == '0%' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_12.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('7b4613df-887a-4784-a0bc-d4d885b325e4') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Opacity > Max
            # max value should be 100%
            title_designer_page.drag_shadow_opacity_slider('100')

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_opacity).AXValue
            check_result_1 = False if not check_value == '100%' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_13.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('588e8bd2-169f-49bd-bd54-5c84e52d6f60') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Opacity > Slider
            # use slider to set value
            case.result = check_result_1 and check_result_2

        with uuid('3a08347c-32d1-41b1-8b1d-dd07c32de935') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Opacity > Input value
            # direct input to set value
            title_designer_page.input_shadow_opacity_value('90')

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_opacity).AXValue
            check_result_1 = False if not check_value == '90%' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_14.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('b2294f0c-fb90-4065-893d-6600eb469be5') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Opacity > ^/v button
            # use buttons to set value
            title_designer_page.drag_shadow_opacity_slider('90')
            for number_of_clicks in range(3):
                title_designer_page.click_shadow_opacity_arrow_btn(index=0)
            for number_of_clicks in range(2):
                title_designer_page.click_shadow_opacity_arrow_btn(index=1)

            check_value = title_designer_page.exist(L.title_designer.shadow.edittext_opacity).AXValue
            case.result = False if not check_value == '91%' else True

        with uuid('bb7806b4-e22b-42ec-a73e-2b1ddb88b12d') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Fill Shadow > Select color
            # open color selector to select color
            title_designer_page.set_shadow_fill_shadow_color(red='255', green='0', blue='0')

            case.result = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_15.png', 'Object')

        with uuid('682be521-c79c-4ba1-baae-8a8e864890e6') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Fill Shadow > On / Off
            # tick to apply fill shadow
            title_designer_page.set_check_shadow_fill_shadow(bCheck=1)
            check_result_1 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_16.png', 'Preview')

            title_designer_page.set_check_shadow_fill_shadow(bCheck=0)
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_5_17.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('1b9821fa-e18d-43a3-8e3c-1ca78cabd4e4') as case:
            # 2.6. Object Tab
            # 2.6.5. Shadow > Shadow direction > Set direction
            # set shadow direction
            case.result = None
            case.fail_log = "*AT limitation*"

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_1(self):
        with uuid('c6e70e31-8fbd-4203-8531-1c7e7f896de5') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position > X
            # Set position X axis value (-2.000~2.000)
            main_page.enter_room(1)
            title_room_page.click_CreateNewTitle_btn()
            title_designer_page.switch_mode(2)  # advanced mode
            title_designer_page.click_object_tab()
            title_designer_page.unfold_object_object_setting_tab(unfold=1)

            title_designer_page.click_object_setting_position_add_keyframe_control()
            check_result_1 = title_designer_page.input_object_setting_x_position_value('0.200')  # keyframe 00;00;00;00
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_1.png', 'designer window')
            case.result = check_result_1 and check_result_2

            ease_in_no_keyframe_status = title_designer_page.exist(
                L.title_designer.object_setting.chx_ease_in).AXEnabled
            ease_out_no_keyframe_status = title_designer_page.exist(
                L.title_designer.object_setting.chx_ease_out).AXEnabled

        with uuid('2874f41c-b35c-4195-b31f-8808712f2559') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position > Y
            # Set position Y axis value (-2.000~2.000)
            check_result_1 = title_designer_page.input_object_setting_y_position_value('0.200')  # keyframe 00;00;00;00
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_2.png', 'designer window')
            case.result = check_result_1 and check_result_2

        with uuid('b61e2a33-1344-4863-b4ad-f9eabcb99ed5') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position > Adjust by Up/Down icon
            # Value can adjust correctly
            title_designer_page.set_timecode('00_00_05_00')  # keyframe 00;00;05;00
            title_designer_page.click_object_setting_position_add_keyframe_control()
            title_designer_page.input_object_setting_x_position_value('0.499')
            for number_of_clicks in range(3):
                title_designer_page.click_object_setting_x_position_arrow_btn(index=0)  # click up arrow btn
            for number_of_clicks in range(2):
                title_designer_page.click_object_setting_x_position_arrow_btn(index=1)  # click down arrow btn
            current_value_x = title_designer_page.exist(L.title_designer.object_setting.edittext_position_x).AXValue
            check_result_1 = False if not current_value_x == '0.500' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_3.png', 'designer window')

            title_designer_page.input_object_setting_y_position_value('0.499')
            for number_of_clicks in range(3):
                title_designer_page.click_object_setting_y_position_arrow_btn(index=0)  # click up arrow btn
            for number_of_clicks in range(2):
                title_designer_page.click_object_setting_y_position_arrow_btn(index=1)  # click down arrow btn
            current_value_y = title_designer_page.exist(L.title_designer.object_setting.edittext_position_y).AXValue
            check_result_3 = False if not current_value_y == '0.500' else True
            check_result_4 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_4.png', 'designer window')

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('c8133fe9-1a18-495a-8841-eac6428b1131') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position > Adjust by Input
            # Value can adjust correctly
            title_designer_page.set_timecode('00_00_07_00')  # keyframe 00;00;07;00
            add_keyframe_result = title_designer_page.click_object_setting_position_add_keyframe_control()

            title_designer_page.set_timecode('00_00_10_00')  # keyframe 00;00;10;00
            title_designer_page.click_object_setting_position_add_keyframe_control()
            check_result_1 = title_designer_page.input_object_setting_x_position_value('0.800')
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_5.png', 'designer window')

            check_result_3 = title_designer_page.input_object_setting_y_position_value('0.800')
            check_result_4 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_6.png', 'designer window')

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('83ddd194-14b8-4e39-8e2c-fa3731301763') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position > Previous/Next keyframe
            # Seek to previous/next keyframe
            title_designer_page.click_object_setting_position_previous_keyframe()
            remove_keyframe_result = title_designer_page.click_object_setting_position_add_keyframe_control()
            check_result_1 = title_designer_page.click_object_setting_position_next_keyframe()
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_7.png', 'designer window')

            check_result_3 = title_designer_page.click_object_setting_position_previous_keyframe()
            check_result_4 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_8.png', 'designer window')

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('875db2cc-8771-4ee0-8ad8-05d968a6e3f5') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position > Add/Remove keyframe
            # Add or remove keyframe on current timecode
            case.result = add_keyframe_result and remove_keyframe_result

        with uuid('9fd6680f-40b4-43fb-b7e9-0097e82c036c') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position>Ease in/ Ease out > (?) button
            # Link to ease function video tutorial page (Hide when no keyframe)
            case.result = title_designer_page.click_object_setting_tutorial_btn()

        with uuid('a5b03db2-f39e-4404-82f1-0b752ba6bcfd') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position>Ease in/ Ease out > Ease In
            # Apply ease in effect to motion (Hide when no keyframe)
            # no keyframe
            check_result_1 = True if not ease_in_no_keyframe_status else False
            # with keyframe
            check_result_2 = title_designer_page.set_check_object_setting_position_ease_in(bCheck=1)

            case.result = check_result_1 and check_result_2

        with uuid('78477d37-70a6-4776-942b-450ee052117f') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position>Ease in/ Ease out > Ease Out
            # Apply ease out effect to motion (Hide when no keyframe)
            check_result_1 = True if not ease_out_no_keyframe_status else False
            # with keyframe
            check_result_2 = title_designer_page.set_check_object_setting_position_ease_out(bCheck=1)

            case.result = check_result_1 and check_result_2

        with uuid('e87259f5-2139-433d-8f23-47c6d1dcfc8b') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position>Ease in/ Ease out > Default value
            # Default value should be 0.4
            ease_in_default_value_check = title_designer_page.exist(L.title_designer.object_setting.
                                                                    edittext_position_ease_in).AXValue
            check_result_1 = False if not ease_in_default_value_check == '0.40' else True

            ease_out_default_value_check = title_designer_page.exist(L.title_designer.object_setting.
                                                                     edittext_position_ease_out).AXValue
            check_result_2 = False if not ease_out_default_value_check == '0.40' else True

            case.result = check_result_1 and check_result_2

        with uuid('77c68e1f-028f-4b3e-a9a3-1735d7e1e5d0') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position>Ease in/ Ease out > Min
            # Minimal value should be 0.01
            title_designer_page.drag_object_setting_position_ease_in_slider(value='0')
            current_value_ease_in = title_designer_page.exist(
                L.title_designer.object_setting.edittext_position_ease_in).AXValue
            check_result_1 = False if not current_value_ease_in == '0.01' else True

            title_designer_page.drag_object_setting_position_ease_out_slider(value='0')
            current_value_ease_out = title_designer_page.exist(
                L.title_designer.object_setting.edittext_position_ease_out).AXValue
            check_result_2 = False if not current_value_ease_out == '0.01' else True

            case.result = check_result_1 and check_result_2

        with uuid('2e293e2f-ec59-4683-a440-643d8275f939') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position>Ease in/ Ease out > Adjust by slide bar
            # Value can adjust correctly
            case.result = check_result_1 and check_result_2

        with uuid('048da7d3-0f56-41a2-a120-50fa6065fb97') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position>Ease in/ Ease out > Max
            # Max value should be 1.00
            title_designer_page.drag_object_setting_position_ease_in_slider(value='100')
            current_value_ease_in = title_designer_page.exist(
                L.title_designer.object_setting.edittext_position_ease_in).AXValue
            check_result_1 = False if not current_value_ease_in == '1.00' else True

            title_designer_page.drag_object_setting_position_ease_out_slider(value='100')
            current_value_ease_out = title_designer_page.exist(
                L.title_designer.object_setting.edittext_position_ease_out).AXValue
            check_result_2 = False if not current_value_ease_out == '1.00' else True

            case.result = check_result_1 and check_result_2

        with uuid('59c42e03-c97c-4133-8dfa-61e83ceaf4d6') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position>Ease in/ Ease out > Adjust by Input
            # Value can adjust correctly
            check_result_1 = title_designer_page.input_object_setting_position_ease_in_value(value='0.50')
            check_result_2 = title_designer_page.input_object_setting_position_ease_out_value(value='0.50')

            title_designer_page.set_timecode('00_00_03_00')
            current_value_x = title_designer_page.exist(L.title_designer.object_setting.edittext_position_x).AXValue
            current_value_y = title_designer_page.exist(L.title_designer.object_setting.edittext_position_y).AXValue
            check_result_3 = False if not (current_value_x == '0.447' and current_value_y == '0.447') else True

            case.result = check_result_1 and check_result_2 and check_result_3

            title_designer_page.click_object_setting_position_next_keyframe()

        with uuid('ad775c5f-3f35-4bf6-8815-e6bdb30225e3') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position>Ease in/ Ease out > Adjust by Up/Down icon
            # Value can adjust correctly
            for number_of_clicks in range(2):
                title_designer_page.click_object_setting_position_ease_in_arrow_btn(index=0)
            for number_of_clicks in range(3):
                title_designer_page.click_object_setting_position_ease_in_arrow_btn(index=1)
            current_value_ease_in = title_designer_page.exist(
                L.title_designer.object_setting.edittext_position_ease_in).AXValue
            check_result_1 = False if not current_value_ease_in == '0.49' else True

            for number_of_clicks in range(2):
                title_designer_page.click_object_setting_position_ease_out_arrow_btn(index=0)
            for number_of_clicks in range(3):
                title_designer_page.click_object_setting_position_ease_out_arrow_btn(index=1)
            current_value_ease_out = title_designer_page.exist(
                L.title_designer.object_setting.edittext_position_ease_out).AXValue
            check_result_2 = False if not current_value_ease_out == '0.49' else True

            case.result = check_result_1 and check_result_2

        with uuid('f4052362-a53e-4456-a7f9-bc5a2272587e') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Position > Reset Keyframe
            # reset position keyframe
            check_result_1 = title_designer_page.click_object_setting_position_reset_keyframe_control()
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_9.png', 'designer window')

            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_2(self):
        with uuid('0e6eeca0-8fea-43a7-843a-8f8fc3114cd7') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale > Default value
            # Default value should be 1.00
            main_page.enter_room(1)
            title_room_page.click_CreateNewTitle_btn()
            title_designer_page.switch_mode(2)  # advanced mode
            title_designer_page.click_object_tab()
            title_designer_page.unfold_object_object_setting_tab(unfold=1)

            width_default_value = title_designer_page.exist(
                L.title_designer.object_setting.edittext_scale_width).AXValue
            check_result_1 = False if not width_default_value == '1.00' else True

            height_default_value = title_designer_page.exist(
                L.title_designer.object_setting.edittext_scale_height).AXValue
            check_result_2 = False if not height_default_value == '1.00' else True

            case.result = check_result_1 and check_result_2

        with uuid('cd5829f1-10f6-4e90-9679-71c59f1db3f3') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale > Max
            # Max value should be 10.00
            title_designer_page.exist(L.title_designer.object_setting.slider_width).AXValue = 100
            max_width = title_designer_page.exist(L.title_designer.object_setting.edittext_scale_width).AXValue
            check_result_1 = False if not max_width == '10.00' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_10.png', 'Preview')

            max_height = title_designer_page.exist(L.title_designer.object_setting.edittext_scale_height).AXValue
            check_result_3 = False if not max_height == '10.00' else True
            check_result_4 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_11.png', 'Preview')

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('b45f1b6d-e1ef-4c25-a8ab-6bb0414770ab') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale > Min
            # Minimal value should be 0.20
            title_designer_page.exist(L.title_designer.object_setting.slider_width).AXValue = 0
            min_width = title_designer_page.exist(L.title_designer.object_setting.edittext_scale_width).AXValue
            check_result_1 = False if not min_width == '0.20' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_12.png', 'Preview')

            min_height = title_designer_page.exist(L.title_designer.object_setting.edittext_scale_height).AXValue
            check_result_3 = False if not min_height == '0.20' else True
            check_result_4 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_13.png', 'Preview')

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('c98277d0-51ba-4ffe-aafa-2f76c4cfc8f7') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale > Add/Remove keyframe
            # Add or remove keyframe on current timecode
            # keyframe 00;00;00;00
            check_result_1 = title_designer_page.click_object_setting_scale_add_keyframe_control()
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_14.png', 'Preview')

            case.result = check_result_1 and check_result_2

            ease_in_no_keyframe_status = title_designer_page.exist(
                L.title_designer.object_setting.chx_scale_ease_in).AXEnabled
            ease_out_no_keyframe_status = title_designer_page.exist(
                L.title_designer.object_setting.chx_scale_ease_out).AXEnabled

        with uuid('c8fe54bb-4fa6-4305-936c-5e9fdd0329d2') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale > Width
            # Set width
            title_designer_page.set_timecode('00_00_05_00')  # keyframe 00;00;05;00
            title_designer_page.click_object_setting_scale_add_keyframe_control()
            check_result_1 = title_designer_page.input_object_setting_scale_width_value('1.35')
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_15.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('8eee27ed-cb41-41fe-ab49-afd43a554f5b') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale > Height
            # Set height
            title_designer_page.set_timecode('00_00_07_00')  # keyframe 00;00;07;00
            title_designer_page.click_object_setting_scale_add_keyframe_control()
            check_result_1 = title_designer_page.input_object_setting_scale_height_value('1.81')
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_16.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('d962d1c1-ecec-4bfc-9e21-128e09de30f2') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale > Previous/Next keyframe
            # Seek to previous/next keyframe
            title_designer_page.set_timecode('00_00_10_00')  # keyframe 00;00;10;00
            title_designer_page.click_object_setting_scale_add_keyframe_control()
            title_designer_page.input_object_setting_scale_width_value('2.50')

            check_result_1 = title_designer_page.click_object_setting_scale_previous_keyframe()
            title_designer_page.click_object_setting_scale_add_keyframe_control()  # remove keyframe
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_17.png', 'Preview')

            check_result_3 = title_designer_page.click_object_setting_scale_next_keyframe()
            check_result_4 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_18.png', 'Preview')

            title_designer_page.click_object_setting_scale_previous_keyframe()

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('a0cf71cc-6592-46d9-bf4c-3826eb1cf525') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale > Maintain Aspect Ratio
            # Maintain aspect ratio after tick
            # uncheck maintain aspect ratio
            check_result_1 = title_designer_page.set_check_object_setting_scale_maintain_aspect_ratio(bCheck=0)

            title_designer_page.exist(L.title_designer.object_setting.slider_width).AXValue = 1.5
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_19.png', 'Preview')

            title_designer_page.input_object_setting_scale_height_value('0.80')
            check_result_3 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_20.png', 'Preview')

            case.result = check_result_1 and check_result_2 and check_result_3

        with uuid('a8f4d937-55b5-4b67-98b7-94a574cb4f4c') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale>Ease in/ Ease out > Ease In
            # Apply ease in effect to motion (Hide when no keyframe)
            # no keyframe
            check_result_1 = True if not ease_in_no_keyframe_status else False
            # with keyframe
            check_result_2 = title_designer_page.set_check_object_setting_scale_ease_in(bCheck=1)

            case.result = check_result_1 and check_result_2

        with uuid('46cb73fa-b901-4ae4-8665-587d1cc0ac6e') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale>Ease in/ Ease out > Ease Out
            # Apply ease out effect to motion (Hide when no keyframe)
            check_result_1 = True if not ease_out_no_keyframe_status else False
            # with keyframe
            check_result_2 = title_designer_page.set_check_object_setting_scale_ease_out(bCheck=1)

            case.result = check_result_1 and check_result_2

        with uuid('17adf457-57c4-401c-abad-e4317e421a2a') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale>Ease in/ Ease out > Default value
            # Default value should be 0.4
            ease_in_default_value_check = title_designer_page.exist(L.title_designer.object_setting.
                                                                    edittext_scale_ease_in).AXValue
            check_result_1 = False if not ease_in_default_value_check == '0.40' else True

            ease_out_default_value_check = title_designer_page.exist(L.title_designer.object_setting.
                                                                     edittext_scale_ease_out).AXValue  # RD hardcode bug
            check_result_2 = False if not ease_out_default_value_check == '0.40' else True

            case.result = check_result_1 and check_result_2

        with uuid('56b06d01-12bd-42ec-89a6-0b735144b3bd') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale>Ease in/ Ease out > Min
            # Minimal value should be 0.01
            title_designer_page.drag_object_setting_scale_ease_in_slider(value='0')
            current_value_ease_in = title_designer_page.exist(
                L.title_designer.object_setting.edittext_scale_ease_in).AXValue
            check_result_1 = False if not current_value_ease_in == '0.01' else True

            title_designer_page.drag_object_setting_scale_ease_out_slider(value='0')
            current_value_ease_out = title_designer_page.exist(
                L.title_designer.object_setting.edittext_scale_ease_out).AXValue
            check_result_2 = False if not current_value_ease_out == '0.01' else True

            case.result = check_result_1 and check_result_2

        with uuid('d019c58b-670c-4028-ab33-afb88e6856ba') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale>Ease in/ Ease out > Adjust by slide bar
            # Value can adjust correctly
            case.result = check_result_1 and check_result_2

        with uuid('2de284c2-c733-4fd8-b9c1-21c4594293fa') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale>Ease in/ Ease out > Max
            # Max value should be 1
            title_designer_page.drag_object_setting_scale_ease_in_slider(value='100')
            current_value_ease_in = title_designer_page.exist(
                L.title_designer.object_setting.edittext_scale_ease_in).AXValue
            check_result_1 = False if not current_value_ease_in == '1.00' else True

            title_designer_page.drag_object_setting_scale_ease_out_slider(value='100')
            current_value_ease_out = title_designer_page.exist(
                L.title_designer.object_setting.edittext_scale_ease_out).AXValue
            check_result_2 = False if not current_value_ease_out == '1.00' else True

            case.result = check_result_1 and check_result_2

        with uuid('3d0980f4-cddf-4d29-af16-9783ee8d50aa') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale>Ease in/ Ease out > Adjust by Input
            # Value can adjust correctly
            check_result_1 = title_designer_page.input_object_setting_scale_ease_in_value(value='0.50')
            check_result_2 = title_designer_page.input_object_setting_scale_ease_out_value(value='0.50')

            title_designer_page.set_timecode('00_00_03_00')
            current_value_width = title_designer_page.exist(
                L.title_designer.object_setting.edittext_scale_width).AXValue
            current_value_height = title_designer_page.exist(
                L.title_designer.object_setting.edittext_scale_height).AXValue
            check_result_3 = False if not (current_value_width == '1.27' and current_value_height == '0.69') else True

            case.result = check_result_1 and check_result_2 and check_result_3

            title_designer_page.click_object_setting_scale_next_keyframe()

        with uuid('08ee86ad-4bc5-4ed1-9012-37c1c8cc02b3') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale>Ease in/ Ease out > Adjust by Up/Down icon
            # Value can adjust correctly
            for number_of_clicks in range(2):
                title_designer_page.click_object_setting_scale_ease_in_arrow_btn(index=0)
            for number_of_clicks in range(3):
                title_designer_page.click_object_setting_scale_ease_in_arrow_btn(index=1)
            current_value_ease_in = title_designer_page.exist(
                L.title_designer.object_setting.edittext_scale_ease_in).AXValue
            check_result_1 = False if not current_value_ease_in == '0.49' else True

            for number_of_clicks in range(2):
                title_designer_page.click_object_setting_scale_ease_out_arrow_btn(index=0)
            for number_of_clicks in range(3):
                title_designer_page.click_object_setting_scale_ease_out_arrow_btn(index=1)
            current_value_ease_out = title_designer_page.exist(
                L.title_designer.object_setting.edittext_scale_ease_out).AXValue
            check_result_2 = False if not current_value_ease_out == '0.49' else True

            case.result = check_result_1 and check_result_2

        with uuid('5ea7a3b7-6afb-48b9-92c6-9f8b49930bab') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Scale > Reset Keyframe
            # Reset scale keyframe
            check_result_1 = title_designer_page.click_object_setting_scale_reset_keyframe_control()
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_21.png', 'designer window')

            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_3(self):
        with uuid('72a71446-6dd3-4892-9537-246834a34dc6') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Opacity > Default value
            # Default value should be 100%
            main_page.enter_room(1)
            title_room_page.click_CreateNewTitle_btn()
            title_designer_page.switch_mode(2)  # advanced mode
            title_designer_page.click_object_tab()
            title_designer_page.unfold_object_object_setting_tab(unfold=1)
            opacity_default_value = title_designer_page.exist(
                L.title_designer.object_setting.edittext_opacity).AXValue

            case.result = False if not opacity_default_value == '100%' else True

        with uuid('6362e7d8-ffea-4bb0-ab6f-3c407043240b') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Opacity > Min
            # Minimal value should be 0%
            title_designer_page.drag_object_setting_opacity_slider(value=0)
            min_opacity = title_designer_page.exist(L.title_designer.object_setting.edittext_opacity).AXValue
            check_result_1 = False if not min_opacity == '0%' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_22.png', 'Preview')
            case.result = check_result_1 and check_result_2

        with uuid('d3471a84-8c64-4357-974d-f103c06385af') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Opacity > Slider
            # Use slider to set value
            case.result = check_result_1 and check_result_2

        with uuid('46c6d54b-5642-429f-b5a0-2ac33e7373ff') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Opacity > Max
            # Max value should be 100%
            title_designer_page.drag_object_setting_opacity_slider(value=100)
            max_opacity = title_designer_page.exist(L.title_designer.object_setting.edittext_opacity).AXValue
            check_result_1 = False if not max_opacity == '100%' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_23.png', 'Preview')
            case.result = check_result_1 and check_result_2

            # keyframe 00;00;00;00
            add_opacity_keyframe = title_designer_page.click_object_setting_opacity_add_keyframe_control()

        with uuid('ef47ecc6-0a5b-444f-8259-7a661af888da') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Opacity > Input value
            # Direct input to set value
            title_designer_page.set_timecode('00_00_05_00')  # keyframe 00;00;05;00
            title_designer_page.click_object_setting_opacity_add_keyframe_control()
            title_designer_page.input_object_setting_opacity_value('90')

            check_value = title_designer_page.exist(L.title_designer.object_setting.edittext_opacity).AXValue
            check_result_1 = False if not check_value == '90%' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_24.png', 'Preview')

            case.result = check_result_1 and check_result_2

            title_designer_page.set_timecode('00_00_07_00')  # keyframe 00;00;07;00
            title_designer_page.click_object_setting_opacity_add_keyframe_control()
            title_designer_page.input_object_setting_opacity_value('70')

            title_designer_page.set_timecode('00_00_10_00')  # keyframe 00;00;10;00
            title_designer_page.click_object_setting_opacity_add_keyframe_control()
            title_designer_page.input_object_setting_opacity_value('98')

        with uuid('cf7e01eb-f2ab-4967-b8a4-a116bfdbfefc') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Opacity > Previous/Next keyframe
            # Seek to previous/next keyframe
            check_result_1 = title_designer_page.click_object_setting_opacity_previous_keyframe()
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_25.png', 'Preview')

            remove_opacity_keyframe = title_designer_page.click_object_setting_opacity_add_keyframe_control()

            check_result_3 = title_designer_page.click_object_setting_opacity_next_keyframe()
            check_result_4 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_26.png', 'Preview')

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

            title_designer_page.click_object_setting_opacity_previous_keyframe()

        with uuid('50a54228-66b3-4d33-851f-2fc0c82cb7e0') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Opacity > Add/Remove keyframe
            # Add or remove keyframe on current timecode
            case.result = add_opacity_keyframe and remove_opacity_keyframe

        with uuid('91f80e6a-bf84-4752-ba70-023e16d84473') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Opacity > ▲/▼ button
            # Use buttons to set value
            title_designer_page.drag_object_setting_opacity_slider(value=90)
            for number_of_clicks in range(3):
                title_designer_page.click_object_setting_opacity_arrow_btn(index=0)
            for number_of_clicks in range(2):
                title_designer_page.click_object_setting_opacity_arrow_btn(index=1)

            check_value = title_designer_page.exist(L.title_designer.object_setting.edittext_opacity).AXValue
            case.result = False if not check_value == '91%' else True

        with uuid('51419b0b-a65e-4d22-9b4a-f1a6de4b8044') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Opacity > Reset Keyframe
            # Reset opacity keyframe
            check_result_1 = title_designer_page.click_object_setting_opacity_reset_keyframe_control()
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_27.png', 'designer window')

            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_4(self):
        with uuid('e2d997ab-fe2d-4796-b50c-85e4d3cd5ac1') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation > Default value
            # Default value should be 0.00
            main_page.enter_room(1)
            title_room_page.click_CreateNewTitle_btn()
            title_designer_page.switch_mode(2)  # advanced mode
            title_designer_page.click_object_tab()
            title_designer_page.unfold_object_object_setting_tab(unfold=1)
            rotation_default_value = title_designer_page.exist(
                L.title_designer.object_setting.edittext_rotation).AXValue

            case.result = False if not rotation_default_value == '0.00' else True

        with uuid('f198418f-76c5-4f07-a341-43adc78e2e3f') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation > Min
            # Minimal value should be -9999
            title_designer_page.input_object_setting_rotation_value('-100000')

            min_rotation = title_designer_page.exist(L.title_designer.object_setting.edittext_rotation).AXValue
            check_result_1 = False if not min_rotation == '-9999.00' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_28.png', 'Preview')

            case.result = check_result_1 and check_result_2

        with uuid('f92ebeff-75ea-4bf9-8e6f-237bc2fef53e') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation > Max
            # Max value should be 9999
            title_designer_page.input_object_setting_rotation_value('100000')

            min_rotation = title_designer_page.exist(L.title_designer.object_setting.edittext_rotation).AXValue
            check_result_1 = False if not min_rotation == '9999.00' else True

            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_29.png', 'Preview')

            case.result = check_result_1 and check_result_2

            title_designer_page.input_object_setting_rotation_value('0')

            check_result_3 = title_designer_page.click_object_setting_rotation_add_keyframe_control()  # 00;00;00;00
            check_result_4 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_30.png', 'Preview')

            add_rotation_keyframe = check_result_3 and check_result_4

            title_designer_page.set_timecode('00_00_05_00')  # 00;00;05;00
            title_designer_page.click_object_setting_rotation_add_keyframe_control()
            title_designer_page.input_object_setting_rotation_value('270')

            title_designer_page.set_timecode('00_00_07_00')  # 00;00;07;00
            title_designer_page.click_object_setting_rotation_add_keyframe_control()
            title_designer_page.input_object_setting_rotation_value('-200')

            title_designer_page.set_timecode('00_00_10_00')  # 00;00;10;00
            title_designer_page.click_object_setting_rotation_add_keyframe_control()
            title_designer_page.input_object_setting_rotation_value('540')

        with uuid('b6342426-6b17-4fcb-a207-ffa376d1e63b') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation > Input value
            # Direct input to set value
            case.result = check_result_1 and check_result_2

        with uuid('80606cd7-7871-43d2-8082-2354e16e640d') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation > Previous/Next keyframe
            # Seek to previous/next keyframe
            title_designer_page.click_object_setting_rotation_previous_keyframe()
            current_value = title_designer_page.exist(L.title_designer.object_setting.edittext_rotation).AXValue
            check_result_1 = False if not current_value == '-200.00' else True
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_31.png', 'Preview')

            title_designer_page.drag_object_vertical_slider(1.0)  # drag object vertical slider to bottom
            check_result_3 = title_designer_page.click_object_setting_rotation_add_keyframe_control()
            check_result_4 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_32.png', 'Preview')
            remove_rotation_keyframe = check_result_3 and check_result_4

            ease_in_status_without_keyframe = title_designer_page.exist(
                L.title_designer.object_setting.slider_rotation_ease_in).AXEnabled
            ease_out_status_without_keyframe = title_designer_page.exist(
                L.title_designer.object_setting.slider_rotation_ease_out).AXEnabled

            title_designer_page.click_object_setting_rotation_next_keyframe()
            current_value = title_designer_page.exist(L.title_designer.object_setting.edittext_rotation).AXValue
            check_result_5 = False if not current_value == '540.00' else True
            check_result_6 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_33.png', 'Preview')

            title_designer_page.click_object_setting_rotation_previous_keyframe()

            case.result = check_result_1 and check_result_2 and check_result_5 and check_result_6

        with uuid('97ca135c-1ab2-4796-bdee-e2b58784496a') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation > Add/Remove keyframe
            # Add or remove keyframe on current timecode
            case.result = add_rotation_keyframe and remove_rotation_keyframe

        with uuid('ff5f47d7-7db8-4d86-8eb2-68621fc27f7b') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation > Slider
            # Use slider to set value
            # v2922, no rotation slider
            case.result = None
            case.fail_log = '*SKIP by AT*'

        with uuid('040f7e31-032f-41d5-ab83-0224b41f507f') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation > ▲/▼ button
            # Use buttons to set value
            for number_of_clicks in range(3):
                title_designer_page.click_object_setting_rotation_arrow_btn(index=0)
            for number_of_clicks in range(2):
                title_designer_page.click_object_setting_rotation_arrow_btn(index=1)

            check_value = title_designer_page.exist(L.title_designer.object_setting.edittext_rotation).AXValue
            case.result = False if not check_value == '270.01' else True

        with uuid('312bb654-b838-4a3c-80bc-5ce3f6ed2685') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation>Ease in/ Ease out > Ease In
            # Apply ease in effect to motion (Hide when no keyframe)
            title_designer_page.drag_object_vertical_slider(1.0)
            # no keyframe
            check_result_1 = True if not ease_in_status_without_keyframe else False
            # with keyframe
            check_result_2 = title_designer_page.set_check_object_setting_rotation_ease_in(bCheck=1)

            case.result = check_result_1 and check_result_2

        with uuid('4e17035f-895f-477c-9a09-21eaf77a5515') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation>Ease in/ Ease out > Ease Out
            # Apply ease out effect to motion (Hide when no keyframe)
            # no keyframe
            check_result_1 = True if not ease_out_status_without_keyframe else False
            # with keyframe
            check_result_2 = title_designer_page.set_check_object_setting_rotation_ease_out(bCheck=1)

            case.result = check_result_1 and check_result_2

        with uuid('152356b2-4f53-49f2-ae2f-f21e2a842a2d') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation>Ease in/ Ease out > Default value
            # Default value should be 0.4
            ease_in_default_value_check = title_designer_page.exist(L.title_designer.object_setting.
                                                                    edittext_rotation_ease_in).AXValue
            check_result_1 = False if not ease_in_default_value_check == '0.40' else True

            ease_out_default_value_check = title_designer_page.exist(L.title_designer.object_setting.
                                                                     edittext_rotation_ease_out).AXValue
            check_result_2 = False if not ease_out_default_value_check == '0.40' else True

            case.result = check_result_1 and check_result_2

        with uuid('7ba08966-0527-4cc9-8633-19e6b69d1aa3') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation>Ease in/ Ease out > Min
            # Minimal value should be 0.01
            title_designer_page.drag_object_setting_rotation_ease_in_slider(value='0')
            current_value_ease_in = title_designer_page.exist(
                L.title_designer.object_setting.edittext_rotation_ease_in).AXValue
            check_result_1 = False if not current_value_ease_in == '0.01' else True

            title_designer_page.drag_object_setting_rotation_ease_out_slider(value='0')
            current_value_ease_out = title_designer_page.exist(
                L.title_designer.object_setting.edittext_rotation_ease_out).AXValue
            check_result_2 = False if not current_value_ease_out == '0.01' else True

            case.result = check_result_1 and check_result_2

        with uuid('0ddf3bcc-3e8a-4757-9a50-81126e0fd9ad') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation>Ease in/ Ease out > Adjust by slide bar
            # Value can adjust correctly
            case.result = check_result_1 and check_result_2

        with uuid('5968b2da-e57e-44f8-b4e0-8d576eca8c85') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation>Ease in/ Ease out > Max
            # Max value should be 1.00
            title_designer_page.drag_object_setting_rotation_ease_in_slider(value='100')
            current_value_ease_in = title_designer_page.exist(
                L.title_designer.object_setting.edittext_rotation_ease_in).AXValue
            check_result_1 = False if not current_value_ease_in == '1.00' else True

            title_designer_page.drag_object_setting_rotation_ease_out_slider(value='100')
            current_value_ease_out = title_designer_page.exist(
                L.title_designer.object_setting.edittext_rotation_ease_out).AXValue
            check_result_2 = False if not current_value_ease_out == '1.00' else True

            case.result = check_result_1 and check_result_2

        with uuid('bd4c7329-f836-446b-b484-68ea232d23f9') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation>Ease in/ Ease out > Adjust by Input
            # Value can adjust correctly
            check_result_1 = title_designer_page.input_object_setting_rotation_ease_in_value(value='0.50')
            check_result_2 = title_designer_page.input_object_setting_rotation_ease_out_value(value='0.50')

            title_designer_page.set_timecode('00_00_03_00')
            current_rotation_value = title_designer_page.exist(
                L.title_designer.object_setting.edittext_rotation).AXValue

            check_result_3 = False if not current_rotation_value == '221.92' else True

            case.result = check_result_1 and check_result_2 and check_result_3

            title_designer_page.click_object_setting_rotation_next_keyframe()

        with uuid('ccc3585a-205b-4815-9cff-723deb80f3ad') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation>Ease in/ Ease out > Adjust by Up/Down icon
            # Value can adjust correctly
            for number_of_clicks in range(2):
                title_designer_page.click_object_setting_rotation_ease_in_arrow_btn(index=0)
            for number_of_clicks in range(3):
                title_designer_page.click_object_setting_rotation_ease_in_arrow_btn(index=1)
            current_value_ease_in = title_designer_page.exist(
                L.title_designer.object_setting.edittext_rotation_ease_in).AXValue
            check_result_1 = False if not current_value_ease_in == '0.49' else True

            for number_of_clicks in range(2):
                title_designer_page.click_object_setting_rotation_ease_out_arrow_btn(index=0)
            for number_of_clicks in range(3):
                title_designer_page.click_object_setting_rotation_ease_out_arrow_btn(index=1)
            current_value_ease_out = title_designer_page.exist(
                L.title_designer.object_setting.edittext_rotation_ease_out).AXValue
            check_result_2 = False if not current_value_ease_out == '0.49' else True

            case.result = check_result_1 and check_result_2

        with uuid('e93ebf41-dc5f-4d9a-8291-e15723808d43') as case:
            # 2.6. Object Tab
            # 2.6.9. Object Settings > Rotation > Reset Keyframe
            # Reset Rotation keyframe
            check_result_1 = title_designer_page.click_object_setting_rotation_reset_keyframe_control()
            check_result_2 = title_designer_page.check_title_designer_page(
                Ground_Truth_Folder + 'title_designer_2_6_9_34.png', 'designer window')

            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    c5b7d346-4511-4266-aa61-0f19cc0c29ff
                    640ac6fa-024f-4e49-ba6a-31e3df43bde6
                    4c592d50-628d-4e14-8e04-21325aca55f0
                    01a08072-61b5-46f6-b4bc-d1281d607982
                    2b567599-9119-4715-96cd-c088a9eb6f4c
                    a45a8215-1859-406c-8691-e3a7b66e4cce
                    a2ce173c-514a-46c7-8a60-11abd9bd7b8d
                    96abf2df-20b4-4796-b103-39ee42a9b229
                    dad3eb78-1e83-4a97-8488-0b457cdf94c7
                    1f016958-ab34-4b21-9040-432b472dd98e
                    3a0bbbd5-0def-4040-8da9-778f51bf2098
                    a14f684a-9716-4095-ae02-27f4271bfc9a
                    fb621447-1952-4fad-a11b-0c0ac158786f
                    e5714df0-c300-42d1-b95f-e574cee2fba6
                    5729fbf0-311b-4f0a-8ecb-91ce6bce99a1
                    0a243c42-7772-4b70-9e87-348bb1c0e4d5
                    3295e9db-ee42-405d-a59c-b3947a759594
                    584e6b52-4561-40e5-86af-83e9a19bd9a8
                    5b1cd306-e8d1-4e28-b8d0-282387cf2298
                    72cbcad4-b2c8-4f3f-b532-75632fd9b688
                    231c7bf0-c49e-4ea2-a559-373ed54dd22f
                    f4de13dc-b7de-4a18-bc34-f89d74319c62
                    f011ad25-3c21-45a4-a01b-8637096b26ff
                    4d767b7e-8108-489f-874f-e3128aeb1802
                    c7d3af85-e449-4eee-aa3e-274d4db76e4a
                    27164fc3-1ff9-4e4d-84f6-3e379b73f1cf
                    87faec2a-cad3-4c9e-9230-d1d6790f39da
                    d56267d0-023f-4bec-b937-66801e31bfbe
                    31618df6-3bfc-4a7b-b0d5-599943b24d2c
                    4d648642-72c4-4aef-8d56-2d3542bd807b
                    ab3f0d58-5fa6-45d5-b996-d79e69f8e7b7
                    4d74da5c-e4d8-403f-822b-dc1f5ee0c223
                    e44dc5ab-07d3-4783-9920-4265345556ca
                    925654cb-2d22-4f63-ac31-d81dfcf970e3
                    ed453141-db85-420f-b42d-311cc6ca3667
                    41f2ec7d-4e70-45d8-bff1-e262f556c18b
                    cb75debb-f001-4ad5-ac9c-c43b5c92edb4
                    db8627ce-dcb4-40ed-9bd5-5ccd390678aa
                    ee21e785-927b-42e5-8f92-ce1feb8be010
                    b86e4916-7f81-480a-849f-26b080539566
                    027e7bdb-85e4-49fe-905e-b2a9b76ea01a
                    d6d16387-4af1-4169-a46e-28ef8b3498a7
                    30cd3f4e-9f53-4a91-bacc-7e58b9d5ae9e
                    b719396c-590a-42dc-8335-7664151c6093
                    f07b4488-adce-4d03-b061-f068a0448d67
                    d1ffe741-4ded-4c4d-9cfa-560d6a110c2a
                    0523149d-bcc6-4c92-84c5-b82e34f4f81e
                    7c2baa6c-0681-4f0b-9035-37898dee2f3d
                    adddd7f9-afe4-4430-aac8-49dd794cd443
                    41cb99bf-5a0e-424b-bef8-afb8cbfcf5e2
                    5f3ec935-214d-4f39-8638-e8b5d380d5bd
                    07cf9ea0-f43d-4a79-a017-01cefde197c7
                    437df26b-35ea-4037-be55-60fa6e81ccf9
                    6e34c34b-0679-47a5-acb7-9da2b7ccd870
                    4c03f2b7-95fb-4803-9634-0c24f461f5cc
                    4f471855-b84a-4671-a7b8-fd617b589015
                    2b018c9c-e1c9-4823-8c51-1af434e8b15f
                    b19cb6fc-f7f5-4c84-b262-37ceab88340e
                    ff5751f2-3a11-45fc-ab5c-d73c3156152a
                    3782ed4a-7e0d-403b-8ffc-5d6f16fdef1d
                    4e606fdb-2e20-4296-bb5b-1f4ffdbebbbc
                    11389ab7-da57-4866-9784-446a52aec55f
                    908df224-09dd-402c-b9c0-a37377ededd5
                    9a9e3e9d-a554-4496-a263-84579e335995
                    78bf3056-8813-467e-b513-fb926df1b934
                    7eca4743-4c63-4181-bd5f-604e05eebde4
                    b07c5b18-79b8-47d2-b97b-2c8c0326245f
                    d09ca4e6-0e8b-4e80-b0b8-0f48b4d911cc
                    f54d1e02-4470-4766-a45d-12de42a9404e
                    ec7ac69c-1386-4f50-a9b0-bba6eec48a7c
                    a9142749-5764-46d9-bcea-d4c2a60ee092
                    84e6d98d-7ebe-48c0-9701-d832f560043a
                    52d76114-4e96-446a-b435-334ac2f1d591
                    30e6771a-2b96-4af6-b33d-ca414950c069
                    b10308c5-3fe2-4c46-ab20-ba947f5cad00
                    12aad65a-4b0f-4731-a6ba-10f64b5ebf48
                    4f4022bc-81ee-4518-92dc-e3aa04bf3386
                    1fe8924b-3042-4ae5-a098-47511a6b0b8e
                    24c61483-8d64-4eab-a573-27dbbec98c4e
                    0fa9d46a-041b-4fa3-aa87-ef74f592d9f9
                    c61e452f-695b-4d7b-8888-18bd5c037b27
                    ab9ebc7b-90ac-4cb9-ad68-040b3635aaf2
                    aa2887d1-9c47-4034-b7ca-942fa4da28d4
                    ba856d3e-b1d2-4082-bb54-b923aef9af9f
                    373d2506-2325-41e5-a38e-38cd1652a5b4
                    54528614-a4dc-4b31-8603-30b3d856c3b8
                    b478d12b-9b02-4476-9518-8513478ecde3
                    c0163532-0565-47c2-aaba-74b57288bf71
                    ae795198-7cab-4420-a5ce-d155dca9e00c
                    c119a5d2-196e-4239-8beb-006e1bd9e631
                    45590173-cadc-46f4-88d9-f48c80810138
                    2961a17b-462a-4a5b-ad3a-db9748581b31
                    14502754-845f-41b1-9f68-4fed18fb2f15
                    2c979109-3631-4f53-864e-b1c41d04562a
                    6a806a0b-59c6-45c2-8902-b411af2ca925
                    8eb552a2-9a3c-432c-b6b8-72a8aafc01b9
                    7866be43-2948-4603-8a05-b68d06b1d048
                    0613691d-d8c4-41ab-8785-50f0e923bd67
                    3e63aa6b-3856-4cfc-be98-6354b4a75425
                    91ef962a-d410-4eb0-a484-604a738ab0eb
                    f07e2181-b273-4b65-b230-d58080e7164b
                    1443c97f-6d47-4c11-9a16-e3c569de3041
                    042fdea5-36fc-4fbf-8a46-25eb83c1f383
                    c1155447-3c75-464d-aba6-b6334511f241
                    d0f8b767-3f80-4899-a06d-361d813f82e5
                    cf35a65f-761a-4736-8706-0f8fd8ccc52a
                    c2a568fa-1446-4627-826d-021753050811
                    41396e90-8149-4634-9ea8-069d2f4bea15
                    6687dbb0-d4c4-4428-9b8c-0fd2f3aadc50
                    db545089-fd1c-4e6f-9a64-687ce7ec80d7
                    d316d7b9-c96f-424c-9188-ca431b0f0e00
                    664f9e89-369f-4649-af2c-809f909232a6
                    43f320a5-8773-4006-9978-eabb1c6d483b
                    c7ec47a5-daa6-4036-955e-858c8efe6b2b
                    16113128-eb2c-4000-a7d9-14feebf40e15
                    22df9da3-8a55-4e87-b580-a4724caf916a
                    328115bd-fede-42fa-a1f4-6fbaec8d097f
                    deeea4a3-0a0e-42f0-a938-7e768ed6eb44
                    91892fef-7223-4164-b388-c128ae811440
                    68c60080-768f-4c2a-9d20-8807a475cd9e
                    12ddda06-b613-4d75-9888-650abae3a9dd
                    45931913-46c2-4a9b-a46a-2583895759f4
                    ab1af6e4-3780-45e8-9efb-b3a331f05696
                    459dc1dc-e671-4477-a577-a4f58825a45c
                    00e7726a-b14f-4505-8d4e-b99aa9292d63
                    44e62b5e-7a2f-4551-b823-a322936fd5a3
                    c771920d-e607-41d2-9c35-639fa42f3265
                    ec4ed9d5-c2fa-4977-9868-34c829742cf6
                    cf6551b0-73b5-4d3b-a9cd-c6654626bbdb
                    c26c1ffd-c58c-4c08-a708-9428f9c002bd
                    4ba2d6a2-b8b1-4993-a5cd-ca6e7e540fc1
                    5c463958-41cf-4de1-8306-d0d7dd1375bd
                    d45a63f6-f193-4946-8a56-4b53f689eb35
                    af9d19f8-4056-4677-a94a-acc00bb62b4b
                    6704083f-9eec-4a63-be77-e379ae15f29b
                    3d909880-072c-486e-a03b-1d89675cc91c
                    d62123f9-7884-4f61-8da2-2bce74ac021b
                    d6e9f659-beac-4e60-a45a-44512e6c1e6a
                    fe1371bb-29de-4ac2-af58-6c394f6d64de
                    b52ef451-e056-4581-8b34-ce9da9b557a9
                    efbb82c9-ba7b-4799-bd26-5ce6f36ee222
                    3465c4a1-4c47-484d-8977-e63b0d1734ae
                    432144aa-1f40-4fb9-9f45-a99c5358106f
                    146b5dbc-0456-42f0-8163-e6043ff20189
                    c03c8188-316e-4b25-93c8-18524a60b326
                    0efba9ec-cf70-4053-974a-0dd2ee01ab4c
                    2874a168-3154-42d4-8bb4-48dd28109d60
                    0f7cd437-a868-49a0-91b8-a4accdc9baaa
                    8bda1afa-eb9f-41dd-a00c-97e2c461bca5
                    6e23ef8c-0ae3-486a-976d-4005c46c12f0
                    2497d50e-7b59-4ec4-ac0c-18e7032d79f5
                    9b4d68bb-0790-4750-8908-8ab45cd9d922
                    374ef42f-4738-4569-8791-678a4fedc4ed
                    ff6a8f48-5ea6-4490-9a74-f6102657d29c
                    86a3ed16-56ae-48c0-9b4b-632b1321d50a
                    38b09950-5e49-4c7e-a097-c357bfdbb4c4
                    57894f24-2ab2-4bf6-a2ba-2087015eeb5f
                    4c08f0e0-7435-46ed-87b1-ea37846204ef
                    7164d836-4918-4b66-be1d-88d1ee28cf5b
                    a24e7d2b-f832-4011-8536-7fa7ec6b70b3
                    54a6560e-b0f4-4dbb-8996-1d40b8b57af2
                    c77cd294-2a14-4665-b7f3-03507bca9550
                    7a328904-b0bf-43fd-8b11-bb18ef0cbd05
                    6f9dffc7-72d2-4afb-acee-ca57fb4ea730
                    a111cd37-92ab-4f90-b947-ce60282a5a8a
                    529cfb97-326c-49ed-b072-68a50869e74e
                    9c22c1f7-89b6-47e5-8528-4544b789093c
                    55513f4e-a065-43df-92d8-1388903c1231
                    64dcefae-4c63-4ece-b6f3-ef8ab49807aa
                    116b9352-d6cb-404f-a92c-fc4ca41401ae
                    44ba60f4-c6f6-40ce-be2c-8c10f01c6ce9
                    3ec3d103-612c-4043-b7d7-b1839078f31f
                    8ac8e742-1249-4c72-847a-e953e8a94aaf
                    121e9e89-d2d0-4452-86da-31036b49e0da
                    a67f8f7b-7f9f-4aec-9846-a676e26aa4f3
                    d5909d41-51f7-4b7f-b23f-8cf248a27f7f
                    5e5a3eaa-18a9-4987-812c-066ebdd4542b
                    a50958b0-4272-4bf4-acbb-098d9cd97a0e
                    4fba059d-dea9-4fb2-9dd1-d341ad46ab4f
                    0d27d176-f6a6-4dca-b043-598fdca399f1
                    8f1eb4ae-23c1-42aa-bc70-445c5a6a33fb
                    f4872a76-e88f-4567-aad7-e30d32f9acae
                    dc071af0-2869-4c6a-810a-ee392ffe0630
                    f27b2102-c461-41b5-a17a-d96244e504d2
                    22a06de3-5e47-4fb6-8145-92edea508f8e
                    2716e9e2-9100-4341-a3de-5b7e293c4667
                    d9c26d30-003a-462c-b615-21af00d289f4
                    4e9a132e-264d-4d7a-971f-39d9a7f3edd4
                    9dfd0e52-00f5-42f0-acf9-c08ac71c09a9
                    064d4df7-bc6e-46f6-a790-086c6d06d439
                    5269c4cd-99ca-46f0-b443-8033122437b1
                    2c89d8c9-7650-47d0-b73b-777301e5e876
                    f759dabf-af3b-4fd0-a65d-4b9652ebae87
                    6777d4c3-971c-4f9d-9310-c01317d58bae
                    27a1a6b4-717f-4728-9fab-5ef46723c608
                    7d5e329b-8b6a-4ac5-ba83-a3c316d23ae2
                    74e46a2e-6350-4e97-9dd6-f9f489ce8c77
                    22d0db67-7da9-478b-a3bd-b69045af0b9f
                    93902a73-8016-4f36-a35d-66fbc75c2df2
                    70a9202f-9eb2-40c9-8166-f456a702086c
                    2f02c48c-163d-47af-a58c-eb77c6328919
                    23fd45f3-5a65-44fc-8b10-c13908d1178d
                    c5e45944-269d-44c2-bfd7-98054b4aca9c
                    fc594731-e79d-444f-86c2-ee581c3068dc
                    f4f590a7-ca3e-4124-a934-696792a71a7b
                    05886fee-59e2-49e4-ad1b-d75c3564731e
                    50e519ef-03a8-4690-b752-99ee4db34b94
                    fd477e24-0a82-45df-9a62-d463bc5233d9
                    bf282ee8-a77b-4472-bece-50814b438abc
                    453d084e-4367-4130-8960-7af6862e31c8
                    8f9de7c2-ec60-4e39-bcd7-eb655b2f7013
                    ab1a20a1-5bde-4798-b19f-fd9dc003d694
                    877d5700-2b6f-4b44-b1a9-2d886969f6de
                    1f292bde-09e6-4dfc-8960-de33fed4a5b6
                    c31d8947-cf3d-4e1e-90e7-57cee855ce08
                    bfe5edf0-3e5a-4fa7-a981-75c6cede4e2d
                    ed89b4ab-e9af-4635-b611-1548098134d0
                    6c64451a-9060-4a74-9d9f-a4722c40dc2d
                    1ff72490-daac-49af-95be-41ebd938fa3a
                    6fabfabe-0fe0-4cb7-b3c1-2d4a1bdf278f
                    822f0530-e29b-4a99-baf7-9bc8cdb38edf
                    4408b58e-cf01-4b18-9687-cdeb1625e9d7
                    1b9821fa-e18d-43a3-8e3c-1ca78cabd4e4
                    38ec1d92-cdd3-4d4d-9df9-0eac986e89bb
                    66b07a91-d12e-4cc5-a2f9-d334c4d53233
                    153fb9ec-07e8-4bb1-b779-8ab0081dfaac
                    187140b0-ff1b-4a30-a015-f1bffb964b9d
                    90b990f1-8d38-4caf-8a93-0e421303279e
                    74186e7d-21bc-416e-8994-60ed260e6120
                    81fdbc18-65a2-4319-9df1-eeb79efe2a41
                    ac07ed54-c477-41e8-bb33-3f526bfcd450
                    2bfa77ba-9b41-46a5-a9c1-4ce303068fee
                    2531cdc6-5c95-4e9b-9d0b-d55d20430ca9
                    b456fe81-bf16-4d5d-8932-2e8f6f446643
                    41712fd3-8936-441f-8b9a-9cb0136c763f
                    c12e8162-9000-401f-b182-2e6d2a4b9063
                    28b2d494-f2ff-45fe-8f4a-01a0799117c7
                    bbf5a53b-b407-4b3e-967d-ed9c15ce856c
                    a6cf4bd6-dacc-4b88-81a6-63f8da2cef41
                    4aeeceda-90cf-4f1a-8641-8cda6242fe13
                    484fbe13-a4ca-4897-a71e-2a29904e2d64
                    60dcc709-30ae-4898-b035-1bb86f410842
                    9ae667fe-acd2-4d68-9598-370de5ac464a
                    e23a3e5c-057a-49e1-9d55-c845b8e0c609
                    83d5ef16-cefd-4bf5-b4bd-b4a21f1210de
                    d88b7306-9622-48f5-b68f-ea11d54e09a7
                    aae51de9-1bcb-4f3e-9bac-4a02cbcf72b3
                    9f0adf21-d628-4cd4-bcf4-859fc33a146e
                    e2b90d21-526e-4f25-b0c1-e0db72ee31d6
                    f31b1340-5197-48fe-8d25-505d185aaa26
                    b937ce90-81f0-43e0-8320-d799add08f37
                    d3beb048-38dd-416b-9c08-3607a42d775c
                    e65b793e-f0ec-42ed-a8c7-2bbf302768a5
                    c88a08b5-a065-4ac8-9bab-84dd5843a617
                    2b7c233a-33fb-464b-ae12-778b0605096f
                    2ab8e738-2312-4b2b-a046-2232eb7a4e5e
                    ffa2d34c-8920-4d69-8bec-853ef022b0f1
                    e51df796-86cb-4d06-9bfd-047c5642797d
                    2a75b95f-60a2-40d0-909b-fadf33fde0e2
                    df7f1390-616f-4c1c-8cf0-6050dff18cba
                    061b6153-e7b1-481c-8a39-a92616aae85e
                    1ee1a5fb-2eda-4940-9ac5-52e641c209a4
                    535509cf-b3d4-4a73-8255-c3e232b43893
                    a9e40c01-e5b7-4333-be05-927a4d0ae953
                    9325ace4-1608-4524-b0fd-75897ccbef8f
                    d91536d7-723b-4c1b-b8a0-63748d907c94
                    963d9524-0d31-4014-bc09-cb4d8772c078
                    66bce4c5-91a8-4426-875b-53df06103461
                    1736bcb2-f80a-4cdf-958d-38cc20c43c45
                    8e94c276-a2ba-4d25-baa8-2dea708f3eae
                    ddb42fd9-25df-4597-8471-c61a9f39880f
                    61fc2272-96ab-4d4a-b0ae-3c49b3fe0bf4
                    ccd3c885-c30d-4abd-8805-5ab2f0fe99b1
                    2f2b2e1f-29a9-4a36-b2ea-4166b1dfc3df
                    e16b9ff5-515e-4f7b-b13b-46ce3bdce70d
                    4df1122d-a558-4520-9c8f-527663e6d78b
                    1b852bbe-88ea-46eb-b7a6-12bdc509dbc2
                    e688f69a-c9bc-4452-aec8-119214ac995f
                    8cad3732-b3c5-4ebd-809d-6f6c9019084c
                    80e2d78d-7249-4d5c-b2e5-f89015b2104a
                    ca87b27b-7d15-4597-8219-fa04a6d1017b
                    6fdbbfb3-0dbf-479d-a5e0-68243f95296a
                    e25db376-7578-460e-9afb-39a1753fa629
                    7eb4643f-ec81-43af-8368-d0c6c2cddb2f
                    ddcaebaf-0378-466c-ae00-cf55971cc8ef
                    d85c870a-bb3f-4a32-a59a-e8ffb7bd61ec
                    e3f3c884-a475-4023-a301-650920ae7c6c
                    ece66c3c-10a4-41a0-9c83-ef2f8ee15fb4
                    099e9b74-45af-41c8-aa59-775ac0033c36
                    dcc74ab8-d486-4df8-9166-a999cf5a1f06
                    222f8b93-43ab-4ee1-b05f-04846adea42b
                    d9cfb254-3207-4774-99e8-d62abc4ae465
                    4f325179-f84f-41ac-b560-f9025cd8db26
                    31c75d2b-71c3-4128-8599-9024468cecd8
                    e3bcef1b-f65e-4240-ac12-eff40c8107f4
                    9d6868b4-c3f4-4043-83ec-77646f4c62ff
                    8c1ef759-be45-4725-a318-a02e57daf264
                    f3c4b3a7-a3b3-48e2-90db-77905488c0e1
                    264583bb-aeb2-4dac-bf45-f28b7b9bcc3c
                    e72a6db0-9ee5-4d86-b758-a7481d0d705a
                    e6e126ea-14a4-42e0-9435-161cd7230568
                    f73ccf49-99e4-4e1a-8c0d-35343625b746
                    ad541bd2-b45b-41bb-b3e0-4f7a9ffb0b71
                    c8384ce1-5186-4a73-86ed-6570c6f3ebed
                    fe090979-a81a-4a1c-9cb3-89b98af90328
                    ff5f47d7-7db8-4d86-8eb2-68621fc27f7b
                    19364c72-e8d7-42e4-bc2d-94ffa91b2240
                    c0a0e270-387e-4122-9920-ffc822560c8d
                    9d6852df-9b1e-448b-aa58-ee105617243b
                    5baf986e-988a-47da-977a-6ae996b9ff69
                    9c8ef55a-bf5b-48a2-ab0a-badc9db1f2c1
                    1931a2b0-c6dc-46e7-a196-054a27c674db
                    f91831eb-dbaf-4f21-b24a-7780996f22db
                    7fcc7cdd-b13d-46ef-bfd2-b9c4e7228e4d
                    a06d237d-d1ed-4a08-9f87-7d1ad2338791
                    e5820c41-8633-4023-a31a-32759b9bd295
                    a21d64b9-7c0c-42d1-a249-a7aba8e1d6db
                    44ebc032-56c7-4d28-a069-7195870f3fec
                    a4908860-d0d1-471b-96c3-4e8148631900
                    e0ea9e6f-a41c-43fd-92c7-4df46d15ef5d
                    516963d1-3fb7-45c9-81a4-760887437030
                    b9ce2d3a-7b33-4729-8ea7-5aa0fa8068ce
                    6f157110-4da9-48e1-a60b-1223c0cad4eb
                    bbfbfc78-3ffa-43a6-ba3e-519505dc5253
                    5bb521c1-8a7d-4fd0-ae83-2c48c7f007dd
                    9250be89-8dce-43c8-93c3-62137191415b
                    84e86589-26d6-4541-9892-def9ef81974b
                    f17cbb2c-e569-48dc-8d88-ad74c1f5ecd7
                    72f27f46-e325-4306-9902-c2b39e9cac86
                    68d98843-dad0-4a62-baa2-7cd3df0aabfb
                    764f4e9f-0e35-45d3-8e13-863dd627deb6
                    fb638d8b-2ac6-47cc-b363-0f7c0f3f984c
                    fc29b969-bd2f-40d1-a25f-8e2d3b9363c0
                    91baff01-def7-4a20-b5aa-9c03b177782e
                    93658b0e-ed74-40b3-8cff-fa2005928f92
                    41b7163c-2f0e-4929-8b07-9d798ee1f546
                    413ad649-5c69-4458-9b7b-874d81d241dd
                    1d76e6f1-063e-492f-a670-4acffc01bbc9
                    c5e55efe-f87a-4245-9d6b-6b5d6884212a
                    d204ebb2-ae7a-4f79-ba38-ffd543a6a915
                    159c5a23-54cd-432d-bf4c-acc1fa10b7f1
                    282db381-c959-4a84-af9c-41de10bdd5bc
                    348a3001-9ec2-471a-bb3a-92cde69441be
                    13945729-489d-4470-87e8-cf7ddfb95142
                    350559ef-fb9e-4086-8c22-7c7a08ae1e1c
                    8e82c5c7-8276-4e53-a571-9a67207f134f
                    a6c35dd7-15e3-47b4-84aa-b1450252e61d
                    cd655a9d-62dc-4130-8656-0a753b6485e2
                    135273bf-3eec-454d-a8ea-28c560b1bed9
                    c86535df-cab1-4151-a95c-3d6d2eb15ebe
                    969ae430-9a78-4ab1-af18-c299e626fe43
                    879024d8-1662-47ff-9b68-1c27e92ae9e4
                    876d2f5e-2b90-46b2-9c9b-4e19cc75860b
                    5dc01975-045a-4ffd-9544-9234b13b9fc8
                    89c03554-46ca-49d7-a298-20f27463dce4
                    7c9c2533-8d95-4fdf-8928-df15a44bf7a3
                    f28eb1de-90a2-4a8a-9a8a-1763c77930af
                    97488fec-8f04-4b35-b81d-ca6903c28181
                    9713a337-e32d-43fd-aadd-ae6a22c60f13
                    dd04a7fa-bf76-4ea4-9dad-fa4bde626930
                    5191611e-0931-4cc5-b8fd-7eb20c1082fe
                    66e003d1-ec48-4b3f-9ddf-2e51e13351b5
                    e4272280-1ea1-49f9-8d54-237ca04b27ae
                    15068ba7-98ad-447c-81de-98b034f88d5a
                    3abdc9b7-b472-4c72-af02-f42aa35e1e2d
                    106f5d12-7df5-41f7-ae3c-de9053b98174
                    659e6324-d7f4-4423-af42-2a48c08d2abb
                    8b73ab9d-a247-440f-b425-540c5d75d5e5
                    3fee999e-4f49-448a-a95e-e8624444c9d8
                    4c1da2fb-a0bf-47f6-a3c0-cfb364bead11
                    1b43c676-df96-4927-a779-e0b88f734e0c
                    9ed29e07-dc37-466b-96ee-2b465482c258
                    d5d219b9-c467-4eca-8f5d-1cf5ca317f4c
                    eee2f356-0938-490e-8de3-4e400c2fe972
                    f1aaaac7-52f3-4b8e-8c25-c6db68ca4e18
                    321f41f2-9e63-4a68-8ff5-d1600fb24517
                    434f2ae4-e66b-475a-b402-acf5510fbf5a
                    e646d412-044f-4faa-b9ce-a854251ff508
                    00d11822-051a-42b9-b896-c5a8be13c505
                    e94fcb7e-4402-48c8-bb2b-8f9380b1f064
                    43800d73-12c5-4849-95c5-8e95c52f16a6
                    05fbc6d8-0b0e-4777-8d60-c2d59389ab76
                    1315e5ee-3d45-4acb-b07c-decab9cd3936
                    f77894d9-387d-44d0-bec8-f9741dfcfe47
                    d7e77f56-853c-4cab-b4e2-9744ce6f6d2c
                    674624f9-5768-45bc-b9f9-96293b0bca11
                    68436535-8761-4977-a49f-5fb216c300e4
                    fee47cd4-a82a-4a16-b3d0-bbe1c6c717ec
                    c9b0a905-7cd6-417d-b6cc-b5f1bc86fa82
                    66825968-e4b3-4e76-b07d-7eb67d458816
                    c813dfc1-443b-4842-9d4b-ac306b968f5d
                    8eb8597d-fcd4-4b7d-83f5-4f3408f59a57
                    9f68e339-cca3-414a-94f0-c84ac3d303c8
                    1f913850-e78e-49d6-ab1d-3717397df590
                    6ca10173-554b-433f-acdd-2aa473159282
                    d7217e87-f44f-438a-806c-8936e38a2330
                    6e32e511-f782-4a93-a644-be3cb7ed9efc
                    20c393e6-d130-42a2-841a-ee232eae4c55
                    1f81fc99-f934-403f-a0e0-31d1528a5a78
                    96831de3-0982-4dd8-b32a-04946f4a05cc
                    94e35c7c-1b5d-4a7b-a935-0717c156e901
                    9db239e9-65c0-49b3-b96a-a3e78017fcba
                    a89d85ed-786a-4eff-8a98-6d46750ba59b
                    bfc54efb-86c1-4ec3-be6e-71482edc71ca
                    15772436-a312-4e9c-83e3-95a10ef1486d
                    6bf67a0e-f9d6-4fd4-82ea-894766af6cf4
                    2ca37c97-70d0-4046-83e7-935762788bbe
                    7e8c23a1-5345-4f00-bf7f-00b21c359177
                    94e96018-9083-436d-849d-45243b076b6b
                    29128ee7-7892-49fd-94d9-2ec5ff4d3a36
                    12aeeae4-dea9-427e-b61d-0354dd450e52
                    c3a61fbe-09c9-4db1-be56-e836a5f780b2
                    c8719a1f-1aee-4edd-9903-dfd44257ec2a
                    b196f538-bc1a-4c7c-a443-d5c3137fc758
                    f3b04fba-f0cd-4c6e-b101-0dafa6b2bdc7
                    8ef42287-35ef-446c-bae5-8bd850a18211
                    0302ef8c-eb72-41e2-b569-df3392e0af0c
                    ae4c8cdc-67e5-4760-89f8-7494dee8db5f
                    e3f363a7-e20a-489e-a1c9-b148a2fbf8b3
                    2e59d5ea-4b72-4b8d-8bb2-0a0b49a6461e
                    2ecca4bb-d02a-4637-a840-55e9938c6bc4
                    2de2cdd4-7aad-4dec-acef-77f8aa48a5e7
                    1659cdcd-44ca-470d-b2ce-ca7430fdcedc
                    9158f525-ba2d-47cb-9e3e-d855f59a7a1c
                    28aadada-28f8-4871-b3d4-a85316842ae9
                    26ca3f6f-da31-4105-bb9c-9f396b346f24
                    6b2ef703-a348-4407-acff-57e2c0e55cbd
                    b92e8b28-f754-4113-a28a-5edb8905d13e
                    f80f5fe6-e2ea-4f13-9f84-0d3826da796f
                    d7f21e15-81b7-4c2f-8156-6fa1ba638ad1
                    1b33cdd5-487f-4d13-a7c2-e5c786277ffe
                    8f996ed1-fbc4-495c-9f3e-d6f3c6e8d128
                    d9d46bb5-98f9-4692-92bc-f40e16573865
                    4210871f-cb6f-4412-a617-6400a1dd875d
                    54ad7ff9-51b8-40b0-92de-546b7ef64c79
                    528cf25f-95e5-4bb7-a987-7a7352512767
                    d638ced9-76de-49ad-bf10-c166bcc4675c
                    87ffd593-f96e-4532-a41a-b98925fff683
                    a940f495-1bc9-426f-ad22-aa5b9f7adb6e
                    fcbe8eaf-af78-4add-9f3c-dd8f1e86ad1d
                    f02aa75b-52ab-42a3-8291-0b73cec2ebbf
                    80831c44-26bd-4bd4-950e-6afeeab415a3
                    d1576b0d-962f-43d8-b6cd-4dfa478631c8
                    6b6c5dfe-f74e-4124-8991-f3567395bb23
                    a02396bf-2cbb-4187-a685-4bf3eebc074a
                    6236fd38-c850-4b3d-89dd-9994bb163cc4
                    bf69024c-82de-44f7-9efe-719ce06ac116
                    c38e28de-0809-4e63-9c7e-9780c8fd6c12
                    dfe7b125-b2e7-4189-838c-17058f6ded4e
                    dbfd9fee-f9a5-4939-8c29-5cbbecb33a6d
                    c50b447b-bfbb-40f1-ab5d-a416b5578c65
                    3d7aca77-07b7-4cc8-bef8-27e4575aaf24
                    a2c1676a-e9e7-4257-8543-823f3e35d268
                    6ddeb4c2-1807-4c36-8dd6-0f470bc90a45
                    2667e654-0d25-4c97-ba94-eaabc412325c
                    33630820-80dc-4482-9be9-d04a0a0b5d95
                    9bb645ef-ab6f-45c2-a67a-ce98eeb29358
                    3f76b07a-3955-4e9b-a784-0be4d141fab4
                    d0af45c4-1a59-45ae-85ff-326b58e62a96
                    427d7d6e-9a3a-4538-b803-163883be7c2f
                    3fcbf20b-3732-41bb-bb83-3e47eca37c78
                    30fcb9f3-0fe2-482f-9a7b-e3b1d5dcf167
                    74548a73-ae3f-4038-8c9f-f9b5e17c345a
                    41670ed4-1f1b-461d-b2fc-342eda4f3ca7
                    b69d0128-3531-41e2-8b02-c53bbd9c550e
                    d8bf40c5-ab65-49f7-ac4e-86fc8c2ce4a5
                    23ef4ed9-d204-4939-9412-447f440fc52e
                    3ffe5b48-9854-4dbe-9d2a-adea4fc783d3
                    8474f6aa-88d3-436c-acdf-052b82cea766
                    4a00ddd1-3fd9-481a-a2a7-fbaba52091e0
                    c12f32d4-c0b8-47f2-92b0-5af3f36244b8
                    27845199-567d-4c99-90ce-e5acbd3fc3f1
                    d35b78a7-aa11-46a1-94b6-210db1987efd
                    28304c92-05d7-4736-823c-77614f8cbe02
                    91b1852e-7be2-420a-ae15-9c4408f1750e
                    54404160-d82e-4c4d-b197-3df780d71116
                    bf1ae484-c8fe-4fa2-84f3-7e46ec7f5dc5
                    605682ed-9c37-4f40-be50-2f9cb9602409
                    68dd9337-9afb-4e52-9af8-7aa744217731
                    642b1ac0-af2b-4163-8a27-ce1312a82e13
                    a3c08b66-c9f8-449a-b1e2-7ad8e3fed9a2
                    c4b39d75-ab0d-4b6d-9d4a-1ce550507af3
                    4df469f6-5373-4fc4-b718-98ed36b50c89
                    2732a28e-5da1-4e82-873a-7f51f136a51e
                    62d4a824-fa77-4b05-9af1-8975697be609
                    345ef3b3-4d96-4a4f-a44e-8f564eb9bb0d
                    596a5f7f-a68c-4f8c-a394-9849216cd148
                    e65d9928-ae92-4303-b78a-1a90cabd4697
                    bdca4274-7850-42d5-9451-a440e3a23f23
                    f6f44868-0af0-49dd-a166-70bf27d1867e
                    fc1a5769-4ded-4733-ad4e-779b81e3241c
                    ee8b3056-9ef1-449c-8426-adedb38bdd5d
                    7650981d-773c-4db3-a65b-cb4e4836d5d5
                    62b6f923-47cf-41d2-9685-9d7243140365
                    cae7a5a0-54cd-4032-8b48-8c5371df72aa
                    20989034-780b-4e3a-a0c2-d4602ee16951
                    fe54d5ba-2825-495a-8bea-9fb13ed8fdcc
                    1f299783-b157-4ec4-bd65-c7afa930ba16
                    6a851bf5-f45c-43e4-a0c6-06dbf921f91f
                    a371feb5-f11e-43f1-a992-568ecb7c4d41
                    710f2d67-bd7c-400e-8064-f035bad876d5
                    483ddd2d-3da1-4d42-a2eb-1e72f9a58cad
                    bce9b67b-ae86-4867-aa3d-118028981924
                    402e96fa-96c7-4cc4-9d70-8dd63f8a5725
                    06cbf136-dc28-4859-980d-6ae0e2bdcc2d
                    6be5af4f-3811-4e0e-bc46-b8e852690c97
                    0dde6326-7e0a-404a-83f7-a4d218066d5d
                    62138efd-6d13-424f-b543-d968d725c21f
                    37629f67-aad6-4d0b-9bb9-72b7fc61c537
                    0993defb-6995-4c69-8dd2-2a9688bcc83a
                    d8a324a6-fe9c-4457-9863-8e2bca828d11
                    8ccafdaa-3fa8-43fd-8278-1acf5287b713
                    04735055-c071-4bdb-a34e-5384a08d5cbc
                    23d38bfb-9fdb-4acc-b531-f4f9e08cdd94
                    870d0432-afc1-4d72-b493-511da036ced5
                    9608baf8-7540-4f48-aaf2-69ac3de5f668
                    54fa0377-262c-4928-9fa3-f65ecc7a2191
                    bffcc08c-9d0c-4c5e-90de-daa33ef573bc
                    87fdb3f6-2be8-4177-ac2f-4eb7e13a6d3d
                    6e5dc0da-ce9c-4344-91d0-6763e4106f08
                    80c1417c-d866-412f-adb5-67e447716298
                    1bd1be17-d481-45fb-ae43-cf2ec50112c5
                    065c931e-15da-4ce3-a772-53024acd10d7
                    8755ce38-6519-4edf-afaf-16f3f8ae56ed
                    13db729b-7945-4131-9238-764985e77f5b
                    6e4984c6-a187-44d8-b7ab-e75654520d80
                    97116791-b019-4afc-93db-a15f1ded9a9d
                    6695ce05-9f18-412b-beda-55a87da0a776
                    5bae1dc4-0c6c-48df-9a6e-a16ba7042ce5
                    cea4edf4-b890-4d80-b622-7183e659a4fe
                    8e81d0c5-56a3-415d-bd32-9eb0ddc7306b
                    c63223cd-ecd0-4cf3-b977-cc74459513f2
                    5959ada2-46b1-4e4d-8052-e2618947c3e4
                    792e9682-3775-4ba6-8569-0df48a3ad6dd
                    508d580f-21b1-4540-8316-9baa790ed8e5
                    325efb3f-0be1-457f-a8a1-306a58e36cab
                    23fd5849-ba25-4f3c-b5e7-1e05d3b6d649
                    43e29596-cf2a-47f9-9478-6aaabe3b63be
                    9097cf40-8243-4d3c-9cd3-0389f1e3d4ee
                    6f0c9cc6-24c0-431d-8899-eae7c3c46f89
                    42ed6ad6-38ee-499b-b71d-1d7874cc23e5
                    8d58ebd2-41bd-44f3-ba01-5009da2a41e5
                    cd743115-d736-4095-a181-5db429bced43
                    e8209410-1de8-4612-ba4b-2159a80634e5
                    5806d653-0a38-48d8-985f-1fc8835595a6
                    f8565f67-ed83-4d5f-bef7-eda60a3df8c2
                    7709329c-ea11-4785-8309-00c3141b003c
                    188391f2-b9b6-4249-ad18-8f81b8dc4b3c
                    30585fa1-50b0-4c6e-bda5-dcb2696d11d9
                    2a0f104c-ffe2-46c7-bb53-ec21934a777c
                    cd9e3821-aa44-4c68-a499-8043530bad4b
                    b36cf589-f062-4048-b23d-b08d62249c3d
                    b13b85dc-fa74-4db8-9947-6fc478468a91
                    f9204087-afff-48ba-bbd5-db8188673b84
                    522c4708-67c8-420b-a2e7-08d39379ad08
                    36845d4a-01bc-4d0e-9e3f-e58809a36e72
                    c193a7b4-22cf-4bac-88af-bbe6751d9ede
                    ad213c50-a2b7-49c7-ae27-f553340f20d7
                    aebebd43-fa65-4312-9889-e1f2a759a55c
                    d8e7f0b6-9d5b-4184-82b8-7cf35c1c60b0
                    b3ad3c3e-cbe4-4aa1-ae42-92d3c305138c
                    01554b19-23cb-4580-8249-b7595231fa7c
                    b3afc46f-8a4e-4561-97f7-0fe348c8ba23
                    dd2020a4-6386-49d2-b6e4-17bc4c79a631
                    46c3c22d-9705-4969-9857-e2652234da52
                    fbf53ac1-0acb-4d4c-855c-724bcd2419c9
                    26b560f3-d1fb-40c6-8323-1fdffffe3843
                    6e7c559d-db23-4cd2-a793-2540dd866f1d
                    5e9620d2-859b-410a-86c5-092b3a847738
                    255af9c1-3ad8-4539-b183-8b74b23963e9
                    cab9ca79-4a01-4475-ab34-57322fda2732
                    c2e0f5be-0624-4a21-aebe-d347dbd6ec3a
                    91762335-9ea7-4527-9b70-d0b6c47fc87f
                    350d2001-6bd1-4a05-bbf8-1eed5b65af6c
                    2387aa3c-a940-410f-8941-591ec8060019
                    1e4a48e5-bbe5-40c5-ab30-c8ee9d89d48e
                    6e57b614-576b-445f-9df7-75fde85e6209
                    fae2735e-8600-46d8-b324-83d30f66597b
                    ecf0d309-1116-4205-a789-66b2a1e10204
                    94319f73-bf93-422d-a757-49644aaa1e77
                    5ee00b8d-3006-4e87-a53b-b1e09cf1661c
                    77aeae8e-2b24-4465-834a-3f8433c54023
                    14f33730-b67a-4499-928f-dd3e4abb38bd
                    ec4da57b-4065-4e20-979f-1b93c6a01edd
                    d375b848-13b6-4913-b933-feec657e0420
                    a73a8b1d-1c65-4041-b79c-a8da90ba1c6e
                    7cc4e681-a523-4949-b80c-6fd11467b91e
                    62008583-e1cf-4cf7-97ff-9db5ff6cabc5
                    eeee611a-ba89-40d2-a5d0-d7f8a1fbb9ce
                    b775d274-63ef-40bb-b5c0-12198b13ab6a
                    22bd3ac1-1e7f-437b-b9ba-4b6d980f6a7d
                    a62b5d7f-494c-4be3-b880-5116a70e7502
                    6f9f4d9d-6be4-449e-9eef-5c15472ccf1e
                    38082345-66c8-453e-a6c4-dfa7e250b234
                    48dd3f56-9425-44e6-b607-aa89388a029c
                    5afd849c-48c8-48ad-a542-ecdde730ed8a
                    d57faefc-408f-4b86-aee9-d6dc73f934fd
                    c64cfd4a-d883-4a22-9564-1e155e560ed0
                    f8f03179-7cf2-413c-8bd1-453632f404b5
                    6a043f22-d70c-4631-96e2-2fa4f83519bc
                    f940c90e-36d5-4955-900b-fbb0ab64b87c
                    8857e3a5-c4b1-4733-8db9-f0712dcbb320
                    9131f544-1cc5-4fbe-86fd-b60b14f26283
                    8c1d68ae-3c99-48db-b96f-51c506267008
                    8ab38260-388c-4a99-9c0f-aec663026fe9
                    dfb65bce-6368-40e3-8fcd-ecb7f316b3fc
                    728795c2-8a45-4bde-bc53-2954b473554c
                    69f66746-645a-41e5-9826-06d7c311c6e9
                    75cff78b-0736-4072-b811-b99eb4dd73ca
                    396d586b-6096-4ee9-932f-e25ef9a7ea15
                    434de788-cfa5-496b-80dc-8adf55c0aa45
                    768a2c45-f066-4bb7-9da9-a22be4f9411f
                    8239b092-64d8-4198-b2d0-e2d34cddacb8
                    80a7f243-7821-4baa-b95c-1af60ff30633
                    a614bd43-7a4d-4ca2-b04d-d6f747957e95
                    f207c2ec-3345-4da8-93e9-44f1b7328652
                    ebed11f5-8119-45a6-be02-673de5e2e781
                    9267fa79-8dea-446e-ba9d-af304960d6ec
                    2fd01b3a-abb9-4e5c-86e2-948901d3660e
                    9d5014e6-0a3b-4459-9f48-5cb6d4f3e091
                    d9a2ed03-4e70-4e35-a9c8-3cbfb812dfe1
                    ba34e80a-546f-4ecb-8e15-d7a23fcaf2f0
                    e1c464b0-ff55-4ed4-b497-8cfc5cfd1f97
                    bbb9f664-e890-4a5c-bcbe-7fa92d9662bb
                    9f3ef74f-8830-4749-b2ab-fa321f33e08a
                    c676b11e-b8f8-479c-9b86-4c505841b3d0
                    661edba2-c58e-4132-b0d3-79bb2af3062f
                    907e5878-2060-485f-a549-5e0574110f2b
                    efe8df07-2470-4cae-9137-0d509aa2061c
                    738a75e9-be89-4234-90f6-bf3503b67bf9
                    c275e961-ce4a-4a75-b6e3-fd86fb60cef6
                    33b7c15c-3f7f-438a-8728-8dd0e9c8eae3
                    6a915683-6c1f-480a-b9ef-9cc54a119e88
                    66229b39-8af1-4696-a7f4-e2ca8abfdd23
                    077830d9-449b-434e-8e82-7d0ce6688a6a
                    66504ce4-ca38-4061-85b8-2845dc0d8945
                    c590e44c-e5d6-4343-a8ef-02b61353005c
                    b4be1859-b0f7-4738-8367-fd2d05220718
                    bf6e7ea8-1e8f-45d8-810e-bc1400e98187
                    9a4fefa5-437b-44eb-a7a1-cdba6cdd2f24
                    64f43e76-6780-4d71-99c4-cabcc9f617b4
                    16db6941-5ab2-4b45-b68c-b7c8a349ef33
                    39aed0c3-dfb4-4c80-81f3-58bbed6e2efd
                    8ece0352-e78f-46d0-9afc-7fc39f159055
                    10f35e11-a5e8-49c9-9abe-9e03e1d70650
                    a67208f3-99bf-4129-8c8c-4685706ecd3b
                    6ff409b1-dfc6-4d31-ba83-9c48f08a7f6d
                    67c7b311-cc2a-49ec-bfc3-53f6c7ddc3ce
                    e91fb817-7cf1-4fb3-b9c8-9ab41173dee1
                    2a7b4f5e-e7e8-4e13-9adc-22e2b242bf91
                    5227bbbf-53c3-45c2-b783-acc5f9fbc137
                    33d47f91-6d37-498a-b3a1-55b2c8c656ad
                    67525246-e264-4daf-9300-3fbc98f2b8e3
                    962efcc7-7633-4538-97f1-a288fb065157
                    d802f8ab-3dd3-4dd7-9b45-ecfcfd8ebe52
                    21f1c4a8-8c0b-4a19-93cd-3511e5f10b98
                    2b41e915-786d-4d41-aeea-bd6ce85daf10
                    aba98574-38ac-4ebb-8ee8-1097faa8d4fd
                    bd5e9152-f721-4f94-91b7-ede15b06764b
                    e8f574da-09c6-454c-add9-f6140919442d
                    2f9d3993-5b05-48bd-ac14-b6c134f04fb9
                    64281e92-2ed6-4a16-83b2-05973b281ec4
                    ae67bf71-74e8-4202-b3cc-8905414be496
                    9ae9b348-5b5a-484f-8841-1e66aad365e7
                    5ade5771-da02-4cd2-a82b-53a3d5fb4f1f
                    4fa9a30a-7a97-4181-ae6a-9c49b7c362ad
                    c0579467-80f9-402d-96a8-3a2862777343
                    876fc43a-5299-44d1-af63-4503496d4db2
                    1863c325-3ff6-4e5e-ba10-00b654a02746
                    0509599a-82a8-41fb-accb-26606a1de508
                    398f8e7d-4759-43d5-b71a-11f7ffc85734
                    7a661b12-e700-4435-b8c4-1dfd6f262c31
                    b26bf4c1-132e-48f5-9cfd-d2aeb1968a62
                    5550115b-d9d1-4a81-b48d-4317a74bc35d
                    5d8a2920-0d00-4d79-a645-6c09e47266ea
                    ad79cbb1-29b7-45dd-ae63-8e47f6393a3b
                    9092fb20-5854-4074-b25a-fb495907b220
                    93ed87b8-df0e-4789-8d71-28e69ba6262c
                    81102ae0-efcf-4322-b485-c798433264fe
                    f3be233b-3915-4580-98f4-35685f50bceb
                    e0c53fd7-b548-4a97-b17f-aa6e8c468e3d
                    33b4498c-f99c-42b7-9e01-77f7261b8b3e
                    f930835d-8ded-484f-9b18-4131424a9471
                    b18c2045-c22b-4b78-b8d7-28505872a51e
                    058f17ed-95a2-40fd-8c43-74f9582681b1
                    940eed66-fc56-42b5-bcf3-5cfe1c866d8d
                    9ec7a834-daae-4c3c-982f-5dfa4922064a
                    cdfe40a4-8e57-47ec-9c4c-1cf155afa348
                    6a26ca11-a95b-4608-a6bc-aa57595f28af
                    0b51610f-0d21-4094-b1b2-54e2ef22f97e
                    dc172907-da60-42fe-be99-0dfb6bacf126
                    257d7919-91c8-4f42-9e39-bea24e3e5af4
                    431b0dbc-98f9-4f73-b1ee-3351832b5857
                    fd44af25-9f4f-4c61-8956-f7dfd7c3e0cd
                    f1cb1181-a41f-4e91-9ec5-247084491145
                    e880a920-6b8c-4d80-aed4-c37a6335808d
                    b0bc771e-6386-4382-8637-a018707dad05
                    c12a60bf-194a-42ee-bdd6-e9226a89e7b7
                    990a316e-e79a-4bae-bfc9-b30990e2564a
                    ee3d1ace-b7e8-4699-9154-c0d1a75498c0
                    ceaf8102-2685-4b91-840e-69bdc917849d
                    863bbd49-3417-491a-acb5-12b2db51fa7b
                    43c50e1c-9e67-4c6e-8575-dc39080c9ffb
                    dcd83cd8-e9f7-4b25-a82e-c38151a2d16d
                    59c40dfa-2ff5-4415-9bf2-e9dee60890bc
                    4d892fbb-260e-4b01-a50b-f459bed0c319
                    18729392-8284-4ec9-a048-d0b0db5528ea
                    dbb8aafd-63b5-470d-8843-dc87dd883bd0
                    f8b363fa-4b57-4e82-ad7a-2e0df2b8f7fd
                    94149e7e-5e49-44bc-8a9c-90234ae591d1
                    187308dd-9602-4f05-a56f-1c3b506a92c8
                    e8d580fb-7fe2-42e6-91a7-1a0155bb96b3
                    d3a51e98-35fd-4bf1-b07b-03697a4752a1
                    fc4e4a00-3598-4e97-ba59-b554e0b36535
                    009eff8d-227d-4ed8-aa71-260612408acb
                    aa291a02-6406-4f77-81b8-b9423b7a923d
                    5308ab1f-1519-4ca0-ab29-437e404a9dff
                    3c99e3fb-0a27-4c3f-90da-4eb2a5bfbf06
                    44b025ab-bffd-4974-9655-a8f84bdbd967
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'

