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
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page',mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Title Designer4.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Title_Designer_v20/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Title_Designer_v20/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1


class Test_Title_Designer_4():  # Title Designer_4.html
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME * 4)
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
            google_sheet_execution_log_init('Title_Designer_4')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"title designer 4 result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        # 2/22
        with uuid('db545089-fd1c-4e6f-9a64-687ce7ec80d7') as case:
            # session 1.5 : In title room (Basic mode) > Object Tab
            # case1.5.6.1.3 : Backdrop > Apply Backdrop > Untick / Disable (Default)
            # Insert clip w/ title to different track
            time.sleep(7)
            main_page.insert_media('Skateboard 01.mp4')
            main_page.enter_room(1)
            title_room_page.click_CreateNewTitle_btn()

            # Maximize window
            title_designer_page.click_maximize_btn()

            # Verify if in "Title Designer" page with
            current_title = title_designer_page.get_title_text_content()
            logger(f"{current_title= }")
            if not current_title == 'My Title':
                logger('Failed to enter Title Designer Page!')
                raise Exception

            # 2/27
            # Check backdrop checkbox default status
            check_backdrop_checkbox_status = title_designer_page.backdrop.get_checkbox_status()
            logger(f"{check_backdrop_checkbox_status= }")
            if check_backdrop_checkbox_status == False:
                backdrop_default_untick = True
                logger(f"{backdrop_default_untick = }")
            else:
                backdrop_default_untick = False
                logger(f"{backdrop_default_untick = }")

            with uuid('6687dbb0-d4c4-4428-9b8c-0fd2f3aadc50') as case:
                # session 1.5 : In title room > Object Tab
                # case1.5.6.1.1 : Backdrop > Apply Backdrop > Tick / Enable
                # Enable backdrop
                check_box_status = title_designer_page.backdrop.set_checkbox(1)
                logger(f"{check_box_status= }")

                # Check backdrop checkbox status
                check_backdrop_checkbox_status1 = title_designer_page.backdrop.get_checkbox_status()
                logger(f"{check_backdrop_checkbox_status1= }")
                if check_backdrop_checkbox_status1 == True:
                    backdrop_ticked = True
                    logger(f"{backdrop_ticked = }")

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.title_designer.area.frame_preview,
                        file_name=Auto_Ground_Truth_Folder + 'G1.5.6.1.1_Title_Designer_Apply_Backdrop.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G1.5.6.1.1_Title_Designer_Apply_Backdrop.png',
                        preview_wnd)
                    logger(compare_result)

                case.result = compare_result and backdrop_ticked

            case.result = backdrop_default_untick
        ''' # skip
        # 2/22
        with uuid('153fb9ec-07e8-4bb1-b779-8ab0081dfaac') as case:
            # session 1.5 : In title room > Object Tab
            # case1.5.6.1.3 : Backdrop > Apply Backdrop > Untick
            # Disable backdrop
            check_box_status = title_designer_page.backdrop.set_checkbox(0)
            logger(f"{check_box_status= }")

            # Check backdrop checkbox status
            check_backdrop_checkbox_status1 = title_designer_page.backdrop.get_checkbox_status()
            logger(f"{check_backdrop_checkbox_status= }")
            if check_backdrop_checkbox_status == False:
                backdrop_unticked = True
                logger(f"{backdrop_unticked = }")
            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.6.1.3_Title_Designer_Disable_Backdrop.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.6.1.3_Title_Designer_Disable_Backdrop.png',
                preview_wnd)
            logger(compare_result)

            case.result = compare_result and backdrop_unticked
        '''
        # 2/27
        with uuid('d316d7b9-c96f-424c-9188-ca431b0f0e00') as case:
            # session 1.5 : In title room > Object Tab
            # case1.5.6.2.1 : Backdrop > Backdrop type > Solid background bar
            # Enable backdrop
            check_box_status = title_designer_page.backdrop.set_checkbox(1)
            logger(f"{check_box_status= }")
            
            # unfold backdrop
            title_designer_page.backdrop.set_unfold_tab()
            time.sleep(DELAY_TIME * 1)

            # Check default setting and select "Solid background bar"
            get_backdrop_type = title_designer_page.backdrop.get_type()
            logger(f"{get_backdrop_type= }")
            if get_backdrop_type == 2:
                # switch to "Solid background bar"
                switch_type = title_designer_page.backdrop.set_type(1)
                logger(f"{switch_type= }")
                get_backdrop_type1 = title_designer_page.backdrop.get_type()
                logger(f"{get_backdrop_type1= }")
                if get_backdrop_type1 == 1:
                    result = True
                    logger(f"{result= }")
                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.title_designer.area.frame_preview,
                        file_name=Auto_Ground_Truth_Folder + 'G1.5.6.2.1_Title_Designer_Backdrop_Solid_background_bar.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G1.5.6.2.1_Title_Designer_Backdrop_Solid_background_bar.png',
                        preview_wnd)
                    logger(compare_result)
                else:
                    #raise Exception
                    result = False
                    logger(f"{result= }")

                with uuid('664f9e89-369f-4649-af2c-809f909232a6') as case:
                    # check if Width is disabled after select 'Solid background bar'
                    check_width_disable = title_designer_page.backdrop.check_width_disable()
                    logger(f"{check_width_disable= }")
                    if check_width_disable == True:
                        case.result = True
                    else:
                        case.result = False

                with uuid('43f320a5-8773-4006-9978-eabb1c6d483b') as case:
                    # check if offsetX is disabled after select 'Solid background bar'
                    check_offset_x_disable = title_designer_page.backdrop.check_offset_x_disable()
                    logger(f"{check_offset_x_disable= }")
                    if check_offset_x_disable == True:
                        case.result = True
                    else:
                        case.result = False

                with uuid('c7ec47a5-daa6-4036-955e-858c8efe6b2b') as case:
                    # check if Curve radius is disabled after select 'Solid background bar'
                    check_curve_radius_disable = title_designer_page.backdrop.check_curve_radius_disable()
                    logger(f"{check_curve_radius_disable= }")
                    if check_curve_radius_disable == True:
                        case.result = True
                    else:
                        case.result = False

            case.result = result and compare_result

        # 2/27
        with uuid('16113128-eb2c-4000-a7d9-14feebf40e15') as case:
            # session 1.5 : In title room > Object Tab
            # case1.5.6.2.2.1 : Backdrop > Backdrop type > Fit with title > Ellipse
            # Switch to "Fit with title"
            check_box_status = title_designer_page.backdrop.set_checkbox(1)
            logger(f"{check_box_status= }")

            get_backdrop_type = title_designer_page.backdrop.get_type()
            logger(f"{get_backdrop_type= }")
            if get_backdrop_type == 1:
                # switch type
                switch_type = title_designer_page.backdrop.set_type(2, 1)
                logger(f"{switch_type= }")
                get_backdrop_type = title_designer_page.backdrop.get_type()
                logger(f"{get_backdrop_type= }")
                if get_backdrop_type == 2:
                    result = True
                    logger(f"{result= }")
                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.title_designer.area.frame_preview,
                        file_name=Auto_Ground_Truth_Folder + 'G1.5.6.2.2.1_Title_Designer_Backdrop_Fit_with_title_Ellipse.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G1.5.6.2.2.1_Title_Designer_Backdrop_Fit_with_title_Ellipse.png',
                        preview_wnd)
                    logger(compare_result)
                else:
                    result = False
                    logger(f"{result= }")

                with uuid('22df9da3-8a55-4e87-b580-a4724caf916a') as case:
                    # check if Curve radius is disabled after select "Ellipse" of "Fit with Title"
                    check_curve_radius_disable = title_designer_page.backdrop.check_curve_radius_disable()
                    logger(f"{check_curve_radius_disable= }")
                    if check_curve_radius_disable == True:
                        case.result = True
                    else:
                        case.result = False

            case.result = result and compare_result

        # 2/27
        with uuid('b0a62916-f527-4568-bb5e-365505da3725') as case:
            # session 1.5 : In title room > Object Tab
            # case1.5.6.2.3.1 : Backdrop > Backdrop type > Fit with title > Rectangle
            # Switch to "Rectangle" of "Fit with title"
            get_backdrop_type = title_designer_page.backdrop.get_type()
            logger(f"{get_backdrop_type= }")
            if get_backdrop_type == 2:
                # switch type to "Rectangle"
                switch_type = title_designer_page.backdrop.set_type(2, 2)
                logger(f"{switch_type= }")
                get_backdrop_type = title_designer_page.backdrop.get_type()
                logger(f"{get_backdrop_type= }")
                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G1.5.6.2.3.1_Title_Designer_Backdrop_Fit_with_title_Rectangle.png')
                logger(preview_wnd)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.5.6.2.3.1_Title_Designer_Backdrop_Fit_with_title_Rectangle.png',
                    preview_wnd)
                logger(compare_result)

                with uuid('328115bd-fede-42fa-a1f4-6fbaec8d097f') as case:
                    # check if Curve radius is disabled after select "Rectangle" of "Fit with Title"
                    check_curve_radius_disable = title_designer_page.backdrop.check_curve_radius_disable()
                    logger(f"{check_curve_radius_disable= }")
                    if check_curve_radius_disable == True:
                        case.result = True
                    else:
                        case.result = False

            case.result = compare_result

        # 3/3
        with uuid('91892fef-7223-4164-b388-c128ae811440') as case:
            # session 1.5 : In title room > Object Tab
            # case1.5.6.2.5.1 : Backdrop > Backdrop type > Fit with title > Rounded Rectangle
            # Switch to "Rounded Rectangle" of "Fit with title"
            get_backdrop_type = title_designer_page.backdrop.get_type()
            logger(f"{get_backdrop_type= }")
            if get_backdrop_type == 2:
                # switch type to "Rounded Rectangle"
                switch_type = title_designer_page.backdrop.set_type(2, 4)
                logger(f"{switch_type= }")
                get_backdrop_type = title_designer_page.backdrop.get_type()
                logger(f"{get_backdrop_type= }")
                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G1.5.6.2.5.1_Title_Designer_Backdrop_Fit_with_title_Rounded_Rectangle.png')
                logger(preview_wnd)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.5.6.2.5.1_Title_Designer_Backdrop_Fit_with_title_Rounded_Rectangle.png',
                    preview_wnd)
                logger(compare_result)

                with uuid('be23d20d-5c41-46d2-a1d6-2de536b78383') as case:
                    # check if Curve radius is disabled after select "Rounded Rectangle" of "Fit with Title"
                    check_curve_radius_disable = title_designer_page.backdrop.check_curve_radius_disable()
                    logger(f"{check_curve_radius_disable= }")
                    if check_curve_radius_disable == True:
                        case.result = True
                    else:
                        case.result = False

            case.result = compare_result

        # 3/3
        with uuid('deeea4a3-0a0e-42f0-a938-7e768ed6eb44') as case:
            # session 1.5 : In title room > Object Tab
            # case1.5.6.2.4 : Backdrop > Backdrop type > Fit with title > Curve-edged Rectangle (Default)
            # Switch to "Curve-edged Rectangle" of "Fit with title"
            get_backdrop_type = title_designer_page.backdrop.get_type()
            logger(f"{get_backdrop_type= }")
            if get_backdrop_type == 2:
                # switch type to "Rounded Rectangle"
                switch_type = title_designer_page.backdrop.set_type(2, 3)
                logger(f"{switch_type= }")
                get_backdrop_type = title_designer_page.backdrop.get_type()
                logger(f"{get_backdrop_type= }")
                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G1.5.6.2.5.1_Title_Designer_Backdrop_Fit_with_title_Rounded_Rectangle.png')
                logger(preview_wnd)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G1.5.6.2.5.1_Title_Designer_Backdrop_Fit_with_title_Rounded_Rectangle.png',
                    preview_wnd)
                logger(compare_result)

            # Click [OK] to apply all settings
            title_designer_page.click_ok()
            time.sleep(DELAY_TIME * 2)
            title_designer_page.save_as_name('New_template')
            title_designer_page.exist_click(L.title_designer.save_as_template.btn_ok)

            # Select track1
            time.sleep(DELAY_TIME * 2)
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # insert new created title to track2
            main_page.select_library_icon_view_media('New_template')
            #main_page.insert_media('New_template')
            main_page.tips_area_insert_media_to_selected_track(-1)

            # snapshot for playback window
            preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'G1.5.6.2.5.1_Preview_Window.png')
            logger(preview_status)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.5.6.2.5.1_Preview_Window.png',
                preview_status)
            logger(compare_result1)

            case.result = compare_result and compare_result1

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        # 3/4
        with uuid('153fb9ec-07e8-4bb1-b779-8ab0081dfaac') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.1.3 : Backdrop > Apply Backdrop > Untick / Disable (Default)
            # Insert clip w/ title to different track
            time.sleep(5)
            main_page.insert_media('Skateboard 01.mp4')
            main_page.enter_room(1)
            title_room_page.click_CreateNewTitle_btn()

            # Maximize window
            title_designer_page.click_maximize_btn()

            # switch to "Advance Mode"
            title_designer_page.switch_mode(2)

            # Verify if in "Title Designer" page with
            current_title = title_designer_page.get_title_text_content()
            logger(f"{current_title= }")
            if not current_title == 'My Title':
                logger('Failed to enter Title Designer Page!')
                raise Exception

            # 3/4
            # Check backdrop checkbox default status
            check_backdrop_checkbox_status = title_designer_page.backdrop.get_checkbox_status()
            logger(f"{check_backdrop_checkbox_status= }")
            if check_backdrop_checkbox_status == False:
                backdrop_default_untick = True
                logger(f"{backdrop_default_untick = }")
            else:
                backdrop_default_untick = False
                logger(f"{backdrop_default_untick = }")

            with uuid('38ec1d92-cdd3-4d4d-9df9-0eac986e89bb') as case:
                # session 2.6 : Object tab (Advance mode) > Object Tab
                # case2.6.6.1.1 : Backdrop > Apply Backdrop > Tick / Enable
                # Enable backdrop
                check_box_status = title_designer_page.backdrop.set_checkbox(1)
                logger(f"{check_box_status= }")

                # Check backdrop checkbox status
                check_backdrop_checkbox_status1 = title_designer_page.backdrop.get_checkbox_status()
                logger(f"{check_backdrop_checkbox_status1= }")
                if check_backdrop_checkbox_status1 == True:
                    backdrop_ticked = True
                    logger(f"{backdrop_ticked = }")

                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.title_designer.area.frame_preview,
                        file_name=Auto_Ground_Truth_Folder + 'G2.6.6.1.1_Title_Designer_Advance_Apply_Backdrop.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G2.6.6.1.1_Title_Designer_Advance_Apply_Backdrop.png',
                        preview_wnd, similarity=0.85)
                    logger(compare_result)

                case.result = compare_result and backdrop_ticked

            case.result = backdrop_default_untick
        ''' # skip
        # 3/4
        with uuid('153fb9ec-07e8-4bb1-b779-8ab0081dfaac') as case:
            # session 2.6 : In title room > Object Tab
            # case2.6.6.1.3 : Backdrop > Apply Backdrop > Untick
            # Disable backdrop
            check_box_status = title_designer_page.backdrop.set_checkbox(0)
            logger(f"{check_box_status= }")

            # Check backdrop checkbox status
            check_backdrop_checkbox_status1 = title_designer_page.backdrop.get_checkbox_status()
            logger(f"{check_backdrop_checkbox_status= }")
            if check_backdrop_checkbox_status == False:
                backdrop_unticked = True
                logger(f"{backdrop_unticked = }")
            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.6.1.3_Title_Designer_Advance_Disable_Backdrop.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.6.1.3_Title_Designer_Advance_Disable_Backdrop.png',
                preview_wnd)
            logger(compare_result)

            case.result = compare_result and backdrop_unticked
        '''
        # 3/4
        with uuid('187140b0-ff1b-4a30-a015-f1bffb964b9d') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.2.1 : Backdrop > Backdrop type > Solid background bar
            # Enable backdrop
            check_box_status = title_designer_page.backdrop.set_checkbox(1)
            logger(f"{check_box_status= }")

            # unfold backdrop
            title_designer_page.backdrop.set_unfold_tab()
            time.sleep(DELAY_TIME * 1)

            # Check default setting and select "Solid background bar"
            get_backdrop_type = title_designer_page.backdrop.get_type()
            logger(f"{get_backdrop_type= }")
            if get_backdrop_type == 2:
                # switch to "Solid background bar"
                switch_type = title_designer_page.backdrop.set_type(1)
                logger(f"{switch_type= }")
                get_backdrop_type1 = title_designer_page.backdrop.get_type()
                logger(f"{get_backdrop_type1= }")
                if get_backdrop_type1 == 1:
                    result = True
                    logger(f"{result= }")
                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.title_designer.area.frame_preview,
                        file_name=Auto_Ground_Truth_Folder + 'G2.6.6.2.1_Title_Designer_Advance_Backdrop_Solid_background_bar.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G2.6.6.2.1_Title_Designer_Advance_Backdrop_Solid_background_bar.png',
                        preview_wnd, similarity=0.85)
                    logger(compare_result)
                else:
                    # raise Exception
                    result = False
                    logger(f"{result= }")

                with uuid('90b990f1-8d38-4caf-8a93-0e421303279e') as case:
                    # check if Width is disabled after select 'Solid background bar'
                    check_width_disable = title_designer_page.backdrop.check_width_disable()
                    logger(f"{check_width_disable= }")
                    if check_width_disable == True:
                        case.result = True
                    else:
                        case.result = False

                with uuid('74186e7d-21bc-416e-8994-60ed260e6120') as case:
                    # check if offsetX is disabled after select 'Solid background bar'
                    check_offset_x_disable = title_designer_page.backdrop.check_offset_x_disable()
                    logger(f"{check_offset_x_disable= }")
                    if check_offset_x_disable == True:
                        case.result = True
                    else:
                        case.result = False

                with uuid('81fdbc18-65a2-4319-9df1-eeb79efe2a41') as case:
                    # check if Curve radius is disabled after select 'Solid background bar'
                    check_curve_radius_disable = title_designer_page.backdrop.check_curve_radius_disable()
                    logger(f"{check_curve_radius_disable= }")
                    if check_curve_radius_disable == True:
                        case.result = True
                    else:
                        case.result = False

            case.result = result and compare_result

        # 3/4
        with uuid('ac07ed54-c477-41e8-bb33-3f526bfcd450') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.2.2.1 : Backdrop > Backdrop type > Fit with title > Ellipse
            # Switch to "Fit with title"
            check_box_status = title_designer_page.backdrop.set_checkbox(1)
            logger(f"{check_box_status= }")

            get_backdrop_type = title_designer_page.backdrop.get_type()
            logger(f"{get_backdrop_type= }")
            if get_backdrop_type == 1:
                # switch to "Solid background bar"
                switch_type = title_designer_page.backdrop.set_type(2, 1)
                logger(f"{switch_type= }")
                get_backdrop_type = title_designer_page.backdrop.get_type()
                logger(f"{get_backdrop_type= }")
                if get_backdrop_type == 2:
                    result = True
                    logger(f"{result= }")
                    # snapshot
                    preview_wnd = tips_area_page.snapshot(
                        locator=L.title_designer.area.frame_preview,
                        file_name=Auto_Ground_Truth_Folder + 'G2.6.6.2.2.1_Title_Designer_Advance_Backdrop_Fit_with_title_Ellipse.png')
                    logger(preview_wnd)
                    compare_result = tips_area_page.compare(
                        Ground_Truth_Folder + 'G2.6.6.2.2.1_Title_Designer_Advance_Backdrop_Fit_with_title_Ellipse.png',
                        preview_wnd)
                    logger(compare_result)
                else:
                    result = False
                    logger(f"{result= }")

                with uuid('2bfa77ba-9b41-46a5-a9c1-4ce303068fee') as case:
                    # check if Curve radius is disabled after select "Ellipse" of "Fit with Title"
                    check_curve_radius_disable = title_designer_page.backdrop.check_curve_radius_disable()
                    logger(f"{check_curve_radius_disable= }")
                    if check_curve_radius_disable == True:
                        case.result = True
                    else:
                        case.result = False

            case.result = result and compare_result

        # 3/4
        with uuid('2531cdc6-5c95-4e9b-9d0b-d55d20430ca9') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.2.3.1 : Backdrop > Backdrop type > Fit with title > Rectangle
            # Switch to "Rectangle" of "Fit with title"
            get_backdrop_type = title_designer_page.backdrop.get_type()
            logger(f"{get_backdrop_type= }")
            if get_backdrop_type == 2:
                # switch type to "Rectangle"
                switch_type = title_designer_page.backdrop.set_type(2, 2)
                logger(f"{switch_type= }")
                get_backdrop_type = title_designer_page.backdrop.get_type()
                logger(f"{get_backdrop_type= }")
                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.2.3.1_Title_Designer_Advance_Backdrop_Fit_with_title_Rectangle.png')
                logger(preview_wnd)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.2.3.1_Title_Designer_Advance_Backdrop_Fit_with_title_Rectangle.png',
                    preview_wnd)
                logger(compare_result)

                with uuid('b456fe81-bf16-4d5d-8932-2e8f6f446643') as case:
                    # check if Curve radius is disabled after select "Rectangle" of "Fit with Title"
                    check_curve_radius_disable = title_designer_page.backdrop.check_curve_radius_disable()
                    logger(f"{check_curve_radius_disable= }")
                    if check_curve_radius_disable == True:
                        case.result = True
                    else:
                        case.result = False

            case.result = compare_result

        # 3/4
        with uuid('c12e8162-9000-401f-b182-2e6d2a4b9063') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.2.5.1 : Backdrop > Backdrop type > Fit with title > Rounded Rectangle
            # Switch to "Rounded Rectangle" of "Fit with title"
            get_backdrop_type = title_designer_page.backdrop.get_type()
            logger(f"{get_backdrop_type= }")
            if get_backdrop_type == 2:
                # switch type to "Rounded Rectangle"
                switch_type = title_designer_page.backdrop.set_type(2, 4)
                logger(f"{switch_type= }")
                get_backdrop_type = title_designer_page.backdrop.get_type()
                logger(f"{get_backdrop_type= }")
                time.sleep(DELAY_TIME * 2)
                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.2.5.1_Title_Designer_Advance_Backdrop_Fit_with_title_Rounded_Rectangle.png')
                logger(preview_wnd)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.2.5.1_Title_Designer_Advance_Backdrop_Fit_with_title_Rounded_Rectangle.png',
                    preview_wnd)
                logger(compare_result)

                with uuid('28b2d494-f2ff-45fe-8f4a-01a0799117c7') as case:
                    # check if Curve radius is disabled after select "Rounded Rectangle" of "Fit with Title"
                    check_curve_radius_disable = title_designer_page.backdrop.check_curve_radius_disable()
                    logger(f"{check_curve_radius_disable= }")
                    if check_curve_radius_disable == True:
                        case.result = True
                    else:
                        case.result = False

            case.result = compare_result

        # 3/4
        with uuid('41712fd3-8936-441f-8b9a-9cb0136c763f') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.2.4 : Backdrop > Backdrop type > Fit with title > Curve-edged Rectangle (Default)
            # Switch to "Curve-edged Rectangle" of "Fit with title"
            get_backdrop_type = title_designer_page.backdrop.get_type()
            logger(f"{get_backdrop_type= }")
            if get_backdrop_type == 2:
                # switch type to "Rounded Rectangle"
                switch_type = title_designer_page.backdrop.set_type(2, 3)
                logger(f"{switch_type= }")
                get_backdrop_type = title_designer_page.backdrop.get_type()
                logger(f"{get_backdrop_type= }")
                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.2.4_Title_Designer_Advance_Backdrop_Fit_with_title_Curve-edged_Rectangle.png')
                logger(preview_wnd)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.2.4_Title_Designer_Advance_Backdrop_Fit_with_title_Curve-edged_Rectangle.png',
                    preview_wnd)
                logger(compare_result)

            # Click [OK] to apply all settings
            title_designer_page.click_ok()
            time.sleep(DELAY_TIME * 2)
            title_designer_page.save_as_name('New_template_1')
            title_designer_page.exist_click(L.title_designer.save_as_template.btn_ok)

            # Select track1
            time.sleep(DELAY_TIME * 2)
            select_track = main_page.timeline_select_track(2)
            logger(select_track)
            time.sleep(DELAY_TIME * 2)

            # insert new created title to track2
            main_page.select_library_icon_view_media('New_template_1')
            #main_page.insert_media('New_template_1')
            main_page.right_click()
            main_page.select_right_click_menu('Add to Timeline')
            time.sleep(DELAY_TIME * 2)

            # snapshot for playback window
            preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'G2.6.6.2.5.1_Preview_Window.png')
            logger(preview_status)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.6.2.5.1_Preview_Window.png',
                preview_status)
            logger(compare_result1)

            case.result = compare_result and compare_result1

        # 3/8
        with uuid('bbf5a53b-b407-4b3e-967d-ed9c15ce856c') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.3.1 : Backdrop > Fill Type > Uniform Color
            # select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # Cut "Food.jpg" and leave gap
            main_page.select_timeline_media('My Title')

            # Enter title designer
            tips_area_page.click_TipsArea_btn_Designer('title')
            time.sleep(DELAY_TIME * 3)

            # Switch "Fill Type" to "Uniform Color"
            fill_type = title_designer_page.backdrop.set_fill_type(1)
            logger(f"{fill_type= }")

            apply_uniform_color_result = title_designer_page.backdrop.apply_uniform_color('#fcf803')
            logger(f"{apply_uniform_color_result= }")

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.6.3.1_Title_Designer_Advance_Backdrop_Apply_Uniform_Color.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.6.3.1_Title_Designer_Advance_Backdrop_Apply_Uniform_Color.png',
                preview_wnd)
            logger(compare_result)

            case.result = apply_uniform_color_result and compare_result

        # 3/8
        with uuid('a6cf4bd6-dacc-4b88-81a6-63f8da2cef41') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.3.2 : Backdrop > Fill Type > Uniform Color - Select color
            case.result = compare_result

        # 3/10
        with uuid('4aeeceda-90cf-4f1a-8641-8cda6242fe13') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.4.1 : Backdrop > Fill Type > 2 Color Gradient
            # Switch "Fill Type" to "2 Color Gradient"
            fill_type = title_designer_page.backdrop.set_fill_type(2)
            logger(f"{fill_type= }")
            time.sleep(DELAY_TIME * 2)

            with uuid('484fbe13-a4ca-4897-a71e-2a29904e2d64') as case:
                # case2.6.6.4.2 : 2 Color Gradient - Begin color
                # change begin color
                title_designer_page.backdrop.apply_gradient_begin('#347842')

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.4.2_Title_Designer_Advance_Backdrop_Apply_2_Color_Gradient.png')
                logger(preview_wnd)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.4.2_Title_Designer_Advance_Backdrop_Apply_2_Color_Gradient.png',
                    preview_wnd)
                logger(compare_result)

                case.result = compare_result

            with uuid('60dcc709-30ae-4898-b035-1bb86f410842') as case:
                # case2.6.6.4.3 : 2 Color Gradient - End color
                # change end color
                title_designer_page.backdrop.apply_gradient_end('#d83a88')

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.4.3_Title_Designer_Advance_Backdrop_Apply_2_Color_Gradient_end.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.4.3_Title_Designer_Advance_Backdrop_Apply_2_Color_Gradient_end.png',
                    preview_wnd)
                logger(compare_result1)

                case.result = compare_result1

                # Click [OK] to apply all settings
                title_designer_page.click_ok()
                #time.sleep(DELAY_TIME * 2)

                # save as new template --> skip below actions as the changes will be applied to customized title template directly
                #title_designer_page.save_as_name('New_template_2')
                #title_designer_page.exist_click(L.title_designer.save_as_template.btn_ok)
                time.sleep(DELAY_TIME * 3)

                # snapshot for playback window
                preview_status = tips_area_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G2.6.6.4_Preview_Window.png')
                logger(preview_status)
                compare_result2 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.4_Preview_Window.png',
                    preview_status)
                logger(compare_result2)

            case.result = compare_result and compare_result1 and compare_result2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        # 3/10
        with uuid('e23a3e5c-057a-49e1-9d55-c845b8e0c609') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.5.1 : Backdrop > Fill Type > Image
            # Create new title
            time.sleep(5)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(2)
            main_page.enter_room(1)
            title_room_page.click_CreateNewTitle_btn()

            # Maximize window
            title_designer_page.click_maximize_btn()

            # switch to "Advance Mode"
            title_designer_page.switch_mode(2)

            # Verify if in "Title Designer" page with
            current_title = title_designer_page.get_title_text_content()
            logger(f"{current_title= }")
            if not current_title == 'My Title':
                logger('Failed to enter Title Designer Page!')
                raise Exception

            # Check backdrop checkbox default status
            check_backdrop_checkbox_status = title_designer_page.backdrop.get_checkbox_status()
            logger(f"{check_backdrop_checkbox_status= }")
            if check_backdrop_checkbox_status == False:
                backdrop_default_untick = True
                logger(f"{backdrop_default_untick = }")
            else:
                backdrop_default_untick = False
                logger(f"{backdrop_default_untick = }")

            # Enable backdrop
            check_box_status = title_designer_page.backdrop.set_checkbox(1)
            logger(f"{check_box_status= }")

            # unfold backdrop
            title_designer_page.backdrop.set_unfold_tab()
            time.sleep(DELAY_TIME * 1)

            # switch backdrop type to Ellipse
            switch_backdrop_type = title_designer_page.backdrop.set_type(2, 1)
            logger(f"{switch_backdrop_type= }")

            # switch fill type to 'Image'
            fill_type = title_designer_page.backdrop.set_fill_type(3, Test_Material_Folder + 'Title_Designer_v20/005.jpg')
            logger(f"{fill_type= }")
            time.sleep(DELAY_TIME * 2)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.6.5.1_Title_Designer_Advance_Backdrop_Apply_Image.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.6.5.1_Title_Designer_Advance_Backdrop_Apply_Image.png',
                preview_wnd)
            logger(compare_result)

            # 3/10
            with uuid('83d5ef16-cefd-4bf5-b4bd-b4a21f1210de') as case:
                # case2.6.6.5.2 : Thumbnail
                # snapshot thumbnail
                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.backdrop.image.thumbnail_image,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.5.2_Title_Designer_Advance_Backdrop_Image_Thumbnail.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.5.2_Title_Designer_Advance_Backdrop_Image_Thumbnail.png',
                    preview_wnd)
                logger(compare_result1)

                case.result = compare_result1

            # 3/10
            with uuid('9f0adf21-d628-4cd4-bcf4-859fc33a146e') as case:
                # case2.6.6.5.5 : Fill Type - Image > Flip upside down
                # Tick "Flip upside down"
                title_designer_page.backdrop.image.flip_upside_down.set_checkbox(1)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.5.5_Title_Designer_Advance_Backdrop_Image_FlipUpsideDown.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.5.5_Title_Designer_Advance_Backdrop_Image_FlipUpsideDown.png',
                    preview_wnd, similarity=0.85)
                logger(compare_result1)

                case.result = compare_result1

            # 3/10
            with uuid('e2b90d21-526e-4f25-b0c1-e0db72ee31d6') as case:
                # case2.6.6.5.6 : Fill Type - Image > Flip left to right
                # Tick "Flip left to right"
                title_designer_page.backdrop.image.flip_left_right.set_checkbox(1)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.5.6_Title_Designer_Advance_Backdrop_Image_FlipLeftRight.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.5.6_Title_Designer_Advance_Backdrop_Image_FlipLeftRight.png',
                    preview_wnd, similarity=0.85)
                logger(compare_result1)

                case.result = compare_result1

            # 3/10
            with uuid('f31b1340-5197-48fe-8d25-505d185aaa26') as case:
                # case2.6.6.5.7 : Fill Type - Image > solid background bar type
                # switch to "Solid background bar"
                switch_type = title_designer_page.backdrop.set_type(1)
                logger(f"{switch_type= }")

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.5.7_Title_Designer_Advance_Backdrop_Image_with_SolidBackgroundBar.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.5.7_Title_Designer_Advance_Backdrop_Image_with_SolidBackgroundBar.png',
                    preview_wnd)
                logger(compare_result1)

                case.result = compare_result1

            # switch to "Fill Type"
            switch_type = title_designer_page.backdrop.set_type(2)
            logger(f"{switch_type= } , {compare_result} , {compare_result1}")
            case.result = compare_result and compare_result1

        # 3/10
        with uuid('b937ce90-81f0-43e0-8320-d799add08f37') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.6.1 : Width > Default value
            width_default_value = title_designer_page.backdrop.width.value.get_value()
            logger(f"{width_default_value= }")

            if width_default_value == '1.00':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result


        # 3/10
        with uuid('e51df796-86cb-4d06-9bfd-047c5642797d') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.7.1 : Height > Default value
            height_default_value = title_designer_page.backdrop.height.value.get_value()
            logger(f"{height_default_value= }")

            if height_default_value == '1.00':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result

        # 3/18
        with uuid('9325ace4-1608-4524-b0fd-75897ccbef8f') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.8.1 : Maintain Aspect Ratio > Tick (Default)
            default_check_status = title_designer_page.backdrop.get_maintain_aspect_ratio()
            logger(f"{default_check_status= }")

            if default_check_status == True:
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            # adjust width
            set_width = title_designer_page.backdrop.width.value.set_value('0.5')
            time.sleep(DELAY_TIME)
            logger(f"{set_width= }")
            width_value = title_designer_page.backdrop.width.value.get_value()
            logger(f"{width_value= }")
            height_value = title_designer_page.backdrop.height.value.get_value()
            logger(f"{height_value= }")

            if width_value == '0.50' and height_value == '0.50':
                result1 = True
                logger(f"{result1= }")
            else:
                result1 = False
                logger(f"{result1= }")

            # set width back to 1.00
            title_designer_page.backdrop.width.value.set_value('1.00')

            case.result = result and result1

        # 3/18
        with uuid('d91536d7-723b-4c1b-b8a0-63748d907c94') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.8.2 : Maintain Aspect Ratio > untick
            # untick maintain aspect ratio
            tick_status = title_designer_page.backdrop.set_maintain_aspect_ratio(0)
            logger(f"{tick_status= }")

            new_tick_status = title_designer_page.backdrop.get_maintain_aspect_ratio()
            logger(f"{new_tick_status= }")

            if new_tick_status == False:
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            # adjust width
            set_width = title_designer_page.backdrop.width.value.set_value('0.7')
            time.sleep(DELAY_TIME)
            logger(f"{set_width= }")
            width_value = title_designer_page.backdrop.width.value.get_value()
            logger(f"{width_value= }")
            height_value = title_designer_page.backdrop.height.value.get_value()
            logger(f"{height_value= }")

            if width_value == '0.70' and height_value == '1.00':
                result1 = True
                logger(f"{result1= }")

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.8.2_Title_Designer_Advance_Backdrop_untick_maintain_aspect_ratio.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.8.2_Title_Designer_Advance_Backdrop_untick_maintain_aspect_ratio.png',
                    preview_wnd, similarity=0.85)
                logger(compare_result1)

            else:
                result1 = False
                logger(f"{result1= }")

            time.sleep(DELAY_TIME)

            # set width to default
            set_width = title_designer_page.backdrop.width.value.set_value('1.0')
            time.sleep(DELAY_TIME)
            logger(f"{set_width= }")

            # tick maintain aspect ratio
            tick_status1 = title_designer_page.backdrop.set_maintain_aspect_ratio(1)
            logger(f"{tick_status1= }")

            case.result = compare_result1 and result and result1

        # 3/16
        with uuid('2ab8e738-2312-4b2b-a046-2232eb7a4e5e') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.6.6 : Width > Min
            drag_slider = title_designer_page.backdrop.width.value.adjust_slider(0.20)
            logger(f"{drag_slider= }")
            width_min_value = title_designer_page.backdrop.width.value.get_value()
            logger(f"{width_min_value= }")

            if width_min_value == '0.20':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result

        # 3/16
        with uuid('ffa2d34c-8920-4d69-8bec-853ef022b0f1') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.6.7 : Width > Max
            set_value = title_designer_page.backdrop.width.value.set_value(2.00)
            logger(f"{set_value= }")
            width_max_value = title_designer_page.backdrop.width.value.get_value()
            logger(f"{width_max_value= }")

            if width_max_value == '2.00':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result


        # 3/10
        with uuid('d3beb048-38dd-416b-9c08-3607a42d775c') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.6.2 : Width > Slider
            # set value by slider
            drag_slider = title_designer_page.backdrop.width.value.adjust_slider(0.79)
            logger(f"{drag_slider= }")
            width_value = title_designer_page.backdrop.width.value.get_value()
            logger(f"{width_value= }")

            if width_value != '1.00':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result

        # 3/10
        with uuid('e65b793e-f0ec-42ed-a8c7-2bbf302768a5') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.6.3 : Width > Input Value
            # set input value
            input_value = title_designer_page.backdrop.width.value.set_value(1.3)
            logger(f"{input_value= }")

            width_value = title_designer_page.backdrop.width.value.get_value()
            logger(f"{width_value= }")

            if width_value == '1.30':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result

        # 3/10
        with uuid('c88a08b5-a065-4ac8-9bab-84dd5843a617') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.6.4 : Width > Adjust Value by click arrow
            # set input value
            new_value = title_designer_page.backdrop.width.value.click_arrow('up', 8)
            logger(f"{new_value= }")

            width_value = title_designer_page.backdrop.width.value.get_value()
            logger(f"{width_value= }")

            if width_value == '1.38':
                result1 = True
                logger(f"{result1= }")
            else:
                result1 = False
                logger(f"{result1= }")

            new_value1 = title_designer_page.backdrop.width.value.click_arrow('down', 5)
            logger(f"{new_value1= }")

            width_value = title_designer_page.backdrop.width.value.get_value()
            logger(f"{width_value= }")

            if width_value == '1.33':
                result2 = True
                logger(f"{result2= }")

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.6.4_Title_Designer_Advance_Backdrop_Image_with_new_width.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.6.4_Title_Designer_Advance_Backdrop_Image_with_new_width.png',
                    preview_wnd)
                logger(compare_result1)

            else:
                result2 = False
                logger(f"{result2= }")

            case.result = result1 and result2 and compare_result1

        # 3/16
        with uuid('2a75b95f-60a2-40d0-909b-fadf33fde0e2') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.7.2 : Height > Slider
            # set value by slider
            drag_slider = title_designer_page.backdrop.height.value.adjust_slider(0.99)
            logger(f"{drag_slider= }")
            height_value = title_designer_page.backdrop.height.value.get_value()
            logger(f"{height_value= }")

            if height_value == '0.99':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result

        # 3/16
        with uuid('df7f1390-616f-4c1c-8cf0-6050dff18cba') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.7.3 : Height > Input Value
            # set input value
            input_value = title_designer_page.backdrop.height.value.set_value(1.60)
            logger(f"{input_value= }")

            height_value = title_designer_page.backdrop.height.value.get_value()
            logger(f"{height_value= }")

            if height_value == '1.60':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result

        # 3/16
        with uuid('061b6153-e7b1-481c-8a39-a92616aae85e') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.7.4 : Height > Adjust Value by click arrow
            # set input value
            new_value = title_designer_page.backdrop.height.value.click_arrow('up', 5)
            logger(f"{new_value= }")

            height_value = title_designer_page.backdrop.height.value.get_value()
            logger(f"{height_value= }")

            if height_value == '1.65':
                result1 = True
                logger(f"{result1= }")
            else:
                result1 = False
                logger(f"{result1= }")

            new_value1 = title_designer_page.backdrop.height.value.click_arrow('down', 6)
            logger(f"{new_value1= }")

            height_value = title_designer_page.backdrop.height.value.get_value()
            logger(f"{height_value= }")

            if height_value == '1.59':
                result2 = True
                logger(f"{result2= }")

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.7.4_Title_Designer_Advance_Backdrop_Image_with_new_height.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.7.4_Title_Designer_Advance_Backdrop_Image_with_new_height.png',
                    preview_wnd)
                logger(compare_result1)

            else:
                result2 = False
                logger(f"{result2= }")

            case.result = result1 and result2 and compare_result1

        # 3/18
        with uuid('963d9524-0d31-4014-bc09-cb4d8772c078') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.9.1 : Opacity > Default value
            opacity_default_value = title_designer_page.backdrop.opacity.value.get_value()
            logger(f"{opacity_default_value= }")

            if opacity_default_value == '70':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            # scroll down
            drag_scroll_bar = title_designer_page.drag_object_vertical_slider(0.9)
            logger(f"{drag_scroll_bar= }")

            case.result = result

        # 3/18
        with uuid('66bce4c5-91a8-4426-875b-53df06103461') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.9.2 : opacity > Slider
            # set value by slider
            drag_slider = title_designer_page.backdrop.opacity.value.adjust_slider(10)
            logger(f"{drag_slider= }")
            opacity_value = title_designer_page.backdrop.opacity.value.get_value()
            logger(f"{opacity_value= }")

            if opacity_value == '10':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result

        # 3/18
        with uuid('1736bcb2-f80a-4cdf-958d-38cc20c43c45') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.9.3 : Opacity > Input Value
            # set input value
            input_value = title_designer_page.backdrop.opacity.value.set_value(30)
            logger(f"{input_value= }")

            opacity_value = title_designer_page.backdrop.opacity.value.get_value()
            logger(f"{opacity_value= }")

            if opacity_value == '30':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result

        # 3/18
        with uuid('8e94c276-a2ba-4d25-baa8-2dea708f3eae') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.9.4 : opacity > Adjust Value by click arrow
            # set input value
            new_value = title_designer_page.backdrop.opacity.value.click_arrow('up', 8)
            logger(f"{new_value= }")

            opacity_value = title_designer_page.backdrop.opacity.value.get_value()
            logger(f"{opacity_value= }")

            if opacity_value == '38':
                result1 = True
                logger(f"{result1= }")
            else:
                result1 = False
                logger(f"{result1= }")

            new_value1 = title_designer_page.backdrop.opacity.value.click_arrow('down', 5)
            logger(f"{new_value1= }")

            opacity_value = title_designer_page.backdrop.opacity.value.get_value()
            logger(f"{opacity_value= }")

            if opacity_value == '33':
                result2 = True
                logger(f"{result2= }")

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.9.4_Title_Designer_Advance_Backdrop_Image_with_new_opacity.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.9.4_Title_Designer_Advance_Backdrop_Image_with_new_opacity.png',
                    preview_wnd)
                logger(compare_result1)

            else:
                result2 = False
                logger(f"{result2= }")

            case.result = result1 and result2 and compare_result1

        # 3/18
        with uuid('2f2b2e1f-29a9-4a36-b2ea-4166b1dfc3df') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.10.1 : Offset - X > Default value
            offsetx_default_value = title_designer_page.backdrop.offset_x.value.get_value()
            logger(f"{offsetx_default_value= }")

            if offsetx_default_value == '0.000':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result

        # 3/18
        with uuid('e16b9ff5-515e-4f7b-b13b-46ce3bdce70d') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.10.2 : Offset - X > Input Value
            # set input value
            input_value = title_designer_page.backdrop.offset_x.value.set_value(0.357)
            logger(f"{input_value= }")

            offsetx_value = title_designer_page.backdrop.offset_x.value.get_value()
            logger(f"{offsetx_value= }")

            if offsetx_value == '0.357':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result

        # 3/18
        with uuid('4df1122d-a558-4520-9c8f-527663e6d78b') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.10.3 : offset - Y > Adjust Value by click arrow
            # set input value
            new_value = title_designer_page.backdrop.offset_x.value.click_arrow('up', 20)
            logger(f"{new_value= }")

            offsetx_value = title_designer_page.backdrop.offset_x.value.get_value()
            logger(f"{offsetx_value= }")

            if offsetx_value == '0.377':
                result1 = True
                logger(f"{result1= }")
            else:
                result1 = False
                logger(f"{result1= }")

            new_value1 = title_designer_page.backdrop.offset_x.value.click_arrow('down', 2)
            logger(f"{new_value1= }")

            offsetx_value = title_designer_page.backdrop.offset_x.value.get_value()
            logger(f"{offsetx_value= }")

            if offsetx_value == '0.375':
                result2 = True
                logger(f"{result2= }")

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.10.3_Title_Designer_Advance_Backdrop_Image_with_new_offsetX.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.10.3_Title_Designer_Advance_Backdrop_Image_with_new_offsetX.png',
                    preview_wnd, similarity=0.85)
                logger(compare_result1)

            else:
                result2 = False
                logger(f"{result2= }")

            case.result = result1 and result2 and compare_result1

        # 3/18
        with uuid('669e0d59-6153-4c55-aa68-039023ef6c0f') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.11.1 : Offset - Y > Default value
            offsety_default_value = title_designer_page.backdrop.offset_y.value.get_value()
            logger(f"{offsety_default_value= }")

            if offsety_default_value == '0.000':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result

        # 3/18
        with uuid('474b5682-c8f5-48c0-b787-9138e51b96d3') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.11.2 : Offset - Y > Input Value
            # set input value
            input_value = title_designer_page.backdrop.offset_y.value.set_value(0.200)
            logger(f"{input_value= }")

            offsety_value = title_designer_page.backdrop.offset_y.value.get_value()
            logger(f"{offsety_value= }")

            if offsety_value == '0.200':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result

        # 3/18
        with uuid('203edbfd-09c7-4bc4-b569-6d0d5a0074d4') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.11.3 : offset-Y > Adjust Value by click arrow
            # set input value
            new_value = title_designer_page.backdrop.offset_y.value.click_arrow('up', 15)
            logger(f"{new_value= }")

            offsety_value = title_designer_page.backdrop.offset_y.value.get_value()
            logger(f"{offsety_value= }")

            if offsety_value == '0.215':
                result1 = True
                logger(f"{result1= }")
            else:
                result1 = False
                logger(f"{result1= }")

            new_value1 = title_designer_page.backdrop.offset_y.value.click_arrow('down', 5)
            logger(f"{new_value1= }")

            offsety_value = title_designer_page.backdrop.offset_y.value.get_value()
            logger(f"{offsety_value= }")

            if offsety_value == '0.210':
                result2 = True
                logger(f"{result2= }")

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.11.3_Title_Designer_Advance_Backdrop_Image_with_new_offsetY.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.11.3_Title_Designer_Advance_Backdrop_Image_with_new_offsetY.png',
                    preview_wnd, similarity=0.85)
                logger(compare_result1)

            else:
                result2 = False
                logger(f"{result2= }")

            case.result = result1 and result2 and compare_result1

        # 3/18
        with uuid('4fbfdbc1-ab6a-4059-9016-44e5f6cb5703') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.12.1 : Curve Radius > Default value
            # scroll up
            drag_scroll_bar = title_designer_page.drag_object_vertical_slider(0.5)
            logger(f"{drag_scroll_bar= }")

            # switch to curve-edged Rectangle
            switch_type = title_designer_page.backdrop.set_type(2, 3)
            logger(f"{switch_type= }")
            get_backdrop_type = title_designer_page.backdrop.get_type()
            logger(f"{get_backdrop_type= }")

            # scroll down
            drag_scroll_bar = title_designer_page.drag_object_vertical_slider(0.9)
            logger(f"{drag_scroll_bar= }")

            curve_radius_default_value = title_designer_page.backdrop.curve_radius.value.get_value()
            logger(f"{curve_radius_default_value= }")

            if curve_radius_default_value == '0.400':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result

        # 3/18
        with uuid('6fc45912-2ec4-4ab1-9840-67bfd130d121') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.12.2 : curve radius > Slider
            # set value by slider
            drag_slider = title_designer_page.backdrop.curve_radius.value.adjust_slider(0.201)
            logger(f"{drag_slider= }")
            curve_radius_value = title_designer_page.backdrop.curve_radius.value.get_value()
            logger(f"{curve_radius_value= }")

            if curve_radius_value == '0.201':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result

        # 3/18
        with uuid('a7012de2-6e30-42d1-9779-22bfcdff0386') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.12.3 : curve radius > Input Value
            # set input value
            input_value = title_designer_page.backdrop.curve_radius.value.set_value(0.705)
            logger(f"{input_value= }")

            curve_radius_value = title_designer_page.backdrop.curve_radius.value.get_value()
            logger(f"{curve_radius_value= }")

            if curve_radius_value == '0.705':
                result = True
                logger(f"{result= }")
            else:
                result = False
                logger(f"{result= }")

            case.result = result

        # 3/18
        with uuid('940f9324-fc1f-4417-acd4-43a1722e38bd') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.6.12.4 : curve radius > Adjust Value by click arrow
            # set input value
            new_value = title_designer_page.backdrop.curve_radius.value.click_arrow('up', 8)
            logger(f"{new_value= }")

            curve_radius_value = title_designer_page.backdrop.curve_radius.value.get_value()
            logger(f"{curve_radius_value= }")

            if curve_radius_value == '0.713':
                result1 = True
                logger(f"{result1= }")
            else:
                result1 = False
                logger(f"{result1= }")

            new_value1 = title_designer_page.backdrop.curve_radius.value.click_arrow('down', 3)
            logger(f"{new_value1= }")

            curve_radius_value = title_designer_page.backdrop.curve_radius.value.get_value()
            logger(f"{curve_radius_value= }")

            if curve_radius_value == '0.710':
                result2 = True
                logger(f"{result2= }")

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.6.12.4_Title_Designer_Advance_Backdrop_Image_with_new_curve_radius.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.6.12.4_Title_Designer_Advance_Backdrop_Image_with_new_curve_radius.png',
                    preview_wnd, similarity=0.85)
                logger(compare_result1)

            else:
                result2 = False
                logger(f"{result2= }")

            case.result = result1 and result2 and compare_result1

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        # 3/25
        with uuid('c0a0e270-387e-4122-9920-ffc822560c8d') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.1.1 : Special Effect > Fire > Preview
            # Enter Title Designer with default title
            time.sleep(7)
            main_page.insert_media('Skateboard 01.mp4')
            main_page.enter_room(1)
            main_page.drag_media_to_timeline_playhead_position('Default', track_no=2)
            main_page.select_timeline_media('My Title')
            timeline_operation_page.double_click()
            time.sleep(3)

            # Maximize window
            title_designer_page.click_maximize_btn()

            # switch to "Advance Mode"
            title_designer_page.switch_mode(2)

            # Verify if in "Title Designer" page with
            current_title = title_designer_page.get_title_text_content()
            logger(f"{current_title= }")
            if not current_title == 'My Title':
                logger('Failed to enter Title Designer Page!')
                raise Exception

            # Check backdrop checkbox default status
            check_backdrop_checkbox_status = title_designer_page.backdrop.get_checkbox_status()
            logger(f"{check_backdrop_checkbox_status= }")
            if check_backdrop_checkbox_status == False:
                backdrop_default_untick = True
                logger(f"{backdrop_default_untick = }")
            else:
                backdrop_default_untick = False
                logger(f"{backdrop_default_untick = }")

            # Enable backdrop
            check_box_status = title_designer_page.backdrop.set_checkbox(1)
            logger(f"{check_box_status= }")

            # unfold special effect
            title_designer_page.special_effects.set_unfold_tab(1)
            time.sleep(DELAY_TIME * 2)

            # Select "No Effect"
            title_designer_page.special_effects.apply_effect(0)

            # Select "Fire"
            title_designer_page.special_effects.apply_effect(1)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.1.1_Title_Designer_Advance_Special_Effect_Fire_Preview.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.1.1_Title_Designer_Advance_Special_Effect_Fire_Preview.png',
                preview_wnd)
            logger(f"{compare_result=}")

            with uuid('9d6852df-9b1e-448b-aa58-ee105617243b') as case:
                # session 2.6 : Object tab (Advance mode) > Object Tab
                # case2.6.9.1.2 : Special Effect > Fire > Looks
                # scroll down
                drag_scroll_bar = title_designer_page.drag_object_vertical_slider(1)
                logger(f"{drag_scroll_bar= }")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(2)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.1.2_Title_Designer_Advance_Special_Effect_Fire_Looks2.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.1.2_Title_Designer_Advance_Special_Effect_Fire_Looks2.png',
                    preview_wnd)
                logger(f"{compare_result1=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(3)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.1.2_Title_Designer_Advance_Special_Effect_Fire_Looks3.png')
                logger(preview_wnd)
                compare_result2 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.1.2_Title_Designer_Advance_Special_Effect_Fire_Looks3.png',
                    preview_wnd)
                logger(f"{compare_result2=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(4)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.1.2_Title_Designer_Advance_Special_Effect_Fire_Looks4.png')
                logger(preview_wnd)
                compare_result3 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.1.2_Title_Designer_Advance_Special_Effect_Fire_Looks4.png',
                    preview_wnd)
                logger(f"{compare_result3=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(5)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.1.2_Title_Designer_Advance_Special_Effect_Fire_Looks5.png')
                logger(preview_wnd)
                compare_result4 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.1.2_Title_Designer_Advance_Special_Effect_Fire_Looks5.png',
                    preview_wnd)
                logger(f"{compare_result4=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(6)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.1.2_Title_Designer_Advance_Special_Effect_Fire_Looks6.png')
                logger(preview_wnd)
                compare_result5 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.1.2_Title_Designer_Advance_Special_Effect_Fire_Looks6.png',
                    preview_wnd)
                logger(f"{compare_result5=}")

                case.result = compare_result1 and compare_result2 and compare_result3 and compare_result4 and compare_result5

            case.result = compare_result

        # 3/25
        with uuid('f91831eb-dbaf-4f21-b24a-7780996f22db') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.1.3.4 : Special Effect > Fire > Size > Able to adjust keyframe value
            # Seek to 00:02:00
            time.sleep(DELAY_TIME * 1)
            title_designer_page.set_timecode('00_00_02_00')

            # add keyframe
            title_designer_page.special_effects.size.keyframe.click_add_remove()
            #title_designer_page.keyframe.press(L.IDC_KEYFRAMEROOM_BTN_ADDREMOVE_KEYFRAME)
            time.sleep(DELAY_TIME * 1)

            # Adjust size
            title_designer_page.special_effects.size.value.set_value(149)
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.1.3.4_Title_Designer_Advance_Special_Effect_Fire_Adjust_Size.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.1.3.4_Title_Designer_Advance_Special_Effect_Fire_Adjust_Size.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 3/25
        with uuid('7fcc7cdd-b13d-46ef-bfd2-b9c4e7228e4d') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.1.4 : Special Effect > Fire > Density
            # Adjust density
            title_designer_page.special_effects.density.set_value(151)
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.1.4_Title_Designer_Advance_Special_Effect_Fire_Adjust_Density.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.1.4_Title_Designer_Advance_Special_Effect_Fire_Adjust_Density.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 3/25
        with uuid('44ebc032-56c7-4d28-a069-7195870f3fec') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.1.6 : Special Effect > Fire > Undo/Redo
            # Undo
            title_designer_page.click_undo_btn()
            time.sleep(DELAY_TIME * 5)

            # Adjust density
            density_value = title_designer_page.special_effects.density.get_value()
            logger(f"{density_value= }")

            if density_value == '375':
                result = True
                logger(f"{result=}")

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.1.6_Title_Designer_Advance_Special_Effect_Fire_undo.png')
                logger(preview_wnd)
                compare_result = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.1.6_Title_Designer_Advance_Special_Effect_Fire_undo.png',
                    preview_wnd)
                logger(f"{compare_result=}")

            else:
                result = False
                logger(f"{result=}")

            case.result = result and compare_result

        # 3/25
        with uuid('a4908860-d0d1-471b-96c3-4e8148631900') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.2.1 : Special Effect > Lights > Preview

            time.sleep(5)
            # Select "Lights"
            title_designer_page.special_effects.apply_effect(2)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.2.1_Title_Designer_Advance_Special_Effect_Lights_Preview.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.2.1_Title_Designer_Advance_Special_Effect_Lights_Preview.png',
                preview_wnd)
            logger(f"{compare_result=}")

            with uuid('e0ea9e6f-a41c-43fd-92c7-4df46d15ef5d') as case:
                # session 2.6 : Object tab (Advance mode) > Object Tab
                # case2.6.9.2.2 : Special Effect > Lights > Looks
                # scroll down
                drag_scroll_bar = title_designer_page.drag_object_vertical_slider(1)
                logger(f"{drag_scroll_bar= }")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(2)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.2.2_Title_Designer_Advance_Special_Effect_Lights_Looks2.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.2.2_Title_Designer_Advance_Special_Effect_Lights_Looks2.png',
                    preview_wnd)
                logger(f"{compare_result1=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(3)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.2.2_Title_Designer_Advance_Special_Effect_Lights_Looks3.png')
                logger(preview_wnd)
                compare_result2 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.2.2_Title_Designer_Advance_Special_Effect_Lights_Looks3.png',
                    preview_wnd)
                logger(f"{compare_result2=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(4)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.2.2_Title_Designer_Advance_Special_Effect_Lights_Looks4.png')
                logger(preview_wnd)
                compare_result3 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.2.2_Title_Designer_Advance_Special_Effect_Lights_Looks4.png',
                    preview_wnd)
                logger(f"{compare_result3=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(5)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.2.2_Title_Designer_Advance_Special_Effect_Lights_Looks5.png')
                logger(preview_wnd)
                compare_result4 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.2.2_Title_Designer_Advance_Special_Effect_Lights_Looks5.png',
                    preview_wnd)
                logger(f"{compare_result4=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(6)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.2.2_Title_Designer_Advance_Special_Effect_Lights_Looks6.png')
                logger(preview_wnd)
                compare_result5 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.2.2_Title_Designer_Advance_Special_Effect_Lights_Looks6.png',
                    preview_wnd)
                logger(f"{compare_result5=}")

                case.result = compare_result1 and compare_result2 and compare_result3 and compare_result4 and compare_result5

            case.result = compare_result

        # 3/25
        with uuid('bbfbfc78-3ffa-43a6-ba3e-519505dc5253') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.2.3.4 : Special Effect > Lights > Tail Size > Able to adjust keyframe value
            # Seek to 00:01:15
            time.sleep(DELAY_TIME * 1)
            title_designer_page.set_timecode('00_00_01_15')

            # add keyframe
            title_designer_page.special_effects.tail_size.keyframe.click_add_remove()
            time.sleep(DELAY_TIME * 1)

            # Adjust size
            title_designer_page.special_effects.tail_size.value.set_value(140)
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.2.3.4_Title_Designer_Advance_Special_Effect_Lights_Adjust_Tail_Size.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.2.3.4_Title_Designer_Advance_Special_Effect_Lights_Adjust_Tail_Size.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 3/25
        with uuid('7ee9382a-d72f-4916-a24e-cd5768d84485') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.2.4.4 : Special Effect > Lights > Tail Color > Able to adjust keyframe value
            # add keyframe
            title_designer_page.special_effects.tail_color.keyframe.click_add_remove()
            time.sleep(DELAY_TIME * 1)

            # Adjust size
            title_designer_page.special_effects.tail_color.set_color('#FBCE29')
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.2.4.4_Title_Designer_Advance_Special_Effect_Lights_Adjust_Tail_Color.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.2.4.4_Title_Designer_Advance_Special_Effect_Lights_Adjust_Tail_Color.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 3/25
        with uuid('bf6d153b-b330-42d8-8ef9-44b4e2995e36') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.2.5.4 : Special Effect > Lights > Head Size > Able to adjust keyframe value
            # add keyframe
            title_designer_page.special_effects.head_size.keyframe.click_add_remove()
            time.sleep(DELAY_TIME * 1)

            # Adjust size
            title_designer_page.special_effects.head_size.value.set_value(93)
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.2.5.4_Title_Designer_Advance_Special_Effect_Lights_Adjust_Head_Size.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.2.5.4_Title_Designer_Advance_Special_Effect_Lights_Adjust_Head_Size.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result
        # 3/25
        with uuid('fdf1e34f-bcfd-4e6a-8029-512fbc9468a7') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.2.6.4 : Special Effect > Lights > Head Color > Able to adjust keyframe value
            # add keyframe
            title_designer_page.special_effects.head_color.keyframe.click_add_remove()
            time.sleep(DELAY_TIME * 1)

            # seek to another time frame
            #time.sleep(DELAY_TIME * 1)
            title_designer_page.set_timecode('00_00_03_15')

            # Adjust size
            title_designer_page.special_effects.head_color.set_color('#E169E6')
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.2.6.4_Title_Designer_Advance_Special_Effect_Lights_Adjust_Head_Color.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.2.6.4_Title_Designer_Advance_Special_Effect_Lights_Adjust_Head_Color.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 3/30
        with uuid('5abab394-9980-4c2c-a3bc-f7d03702fa16') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.3.1 : Special Effect > Lightning > Preview
            time.sleep(DELAY_TIME)
            # Select "Lights"
            title_designer_page.special_effects.apply_effect(3)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.3.1_Title_Designer_Advance_Special_Effect_Lightning_Preview.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.3.1_Title_Designer_Advance_Special_Effect_Lightning_Preview.png',
                preview_wnd)
            logger(f"{compare_result=}")

            with uuid('319daf65-1056-4c16-bf97-a7f304d8ed78') as case:
                # session 2.6 : Object tab (Advance mode) > Object Tab
                # case2.6.9.3.2 : Special Effect > Lightning > Looks
                # scroll down
                drag_scroll_bar = title_designer_page.drag_object_vertical_slider(1)
                logger(f"{drag_scroll_bar= }")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(2)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.3.2_Title_Designer_Advance_Special_Effect_Lightning_Looks2.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.3.2_Title_Designer_Advance_Special_Effect_Lightning_Looks2.png',
                    preview_wnd)
                logger(f"{compare_result1=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(3)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.3.2_Title_Designer_Advance_Special_Effect_Lightning_Looks3.png')
                logger(preview_wnd)
                compare_result2 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.3.2_Title_Designer_Advance_Special_Effect_Lightning_Looks3.png',
                    preview_wnd)
                logger(f"{compare_result2=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(4)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.3.2_Title_Designer_Advance_Special_Effect_Lightning_Looks4.png')
                logger(preview_wnd)
                compare_result3 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.3.2_Title_Designer_Advance_Special_Effect_Lightning_Looks4.png',
                    preview_wnd)
                logger(f"{compare_result3=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(5)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.3.2_Title_Designer_Advance_Special_Effect_Lightning_Looks5.png')
                logger(preview_wnd)
                compare_result4 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.3.2_Title_Designer_Advance_Special_Effect_Lightning_Looks5.png',
                    preview_wnd)
                logger(f"{compare_result4=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(6)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.3.2_Title_Designer_Advance_Special_Effect_Lightning_Looks6.png')
                logger(preview_wnd)
                compare_result5 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.3.2_Title_Designer_Advance_Special_Effect_Lightning_Looks6.png',
                    preview_wnd)
                logger(f"{compare_result5=}")

                case.result = compare_result1 and compare_result2 and compare_result3 and compare_result4 and compare_result5

            case.result = compare_result

        # 3/30
        with uuid('e3f4710b-74aa-4a63-8846-cd6c189a539c') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.2.3.4 : Special Effect > Lightning > Size > Able to adjust keyframe value
            # Seek to 00:01:15
            time.sleep(DELAY_TIME * 1)
            title_designer_page.set_timecode('00_00_02_15')

            # add keyframe
            title_designer_page.special_effects.size.keyframe.click_add_remove()
            time.sleep(DELAY_TIME * 1)

            # Adjust size
            title_designer_page.special_effects.size.value.set_value(102)
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.3.3.4_Title_Designer_Advance_Special_Effect_Lightning_Adjust_Size.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.3.3.4_Title_Designer_Advance_Special_Effect_Lightning_Adjust_Size.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 3/30
        with uuid('177d2448-3c4d-4f0a-9c57-98e63bc226a3') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.3.6.4 : Special Effect > Lightning > Color > Able to adjust keyframe value
            # add keyframe
            title_designer_page.special_effects.color.keyframe.click_add_remove()
            time.sleep(DELAY_TIME * 1)

            # seek to another time frame
            #time.sleep(DELAY_TIME * 1)
            title_designer_page.set_timecode('00_00_03_15')

            # Adjust size
            title_designer_page.special_effects.color.set_color('#65219C')
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.3.6.4_Title_Designer_Advance_Special_Effect_Lightning_Adjust_Color.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.3.6.4_Title_Designer_Advance_Special_Effect_Lightning_Adjust_Color.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 3/30
        with uuid('c3df1e95-00d5-4cc6-adbf-ff67ced0e9a3') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.3.6.4 : Special Effect > Lightning > Length > Able to adjust keyframe value
            # add keyframe
            title_designer_page.special_effects.length.keyframe.click_add_remove()
            time.sleep(DELAY_TIME * 1)

            # seek to another time frame
            #time.sleep(DELAY_TIME * 1)
            title_designer_page.set_timecode('00_00_03_15')

            # Adjust length
            title_designer_page.special_effects.length.value.set_value(75)
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.3.6.4_Title_Designer_Advance_Special_Effect_Lights_Adjust_Length.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.3.6.4_Title_Designer_Advance_Special_Effect_Lights_Adjust_Length.png',
                preview_wnd)
            logger(f"{compare_result=}")

            # click [OK] to save the modification
            title_designer_page.click_ok()

            # seek via preview window
            time.sleep(DELAY_TIME)
            set_timecode = main_page.set_timeline_timecode('00_00_03_02')
            logger(set_timecode)

            # snapshot preview window
            time.sleep(DELAY_TIME * 2)
            preview_window = tips_area_page.snapshot(locator=L.playback_window.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'G2.6.9.3.6.4_Timeline_Preview_Window.png')
            logger(preview_window)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.3.6.4_Timeline_Preview_Window.png', preview_window)
            logger(compare_result1)

            case.result = compare_result and compare_result1

   # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        # 3/30
        with uuid('428ef8cc-2cb8-4f7c-871e-fa7d80dfc5c8') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.4.1 : Special Effect > LED Sign > Preview
            # Enter Title Designer with default title
            time.sleep(5)
            main_page.insert_media('Skateboard 01.mp4')
            main_page.enter_room(1)
            main_page.drag_media_to_timeline_playhead_position('Default', track_no=2)
            main_page.select_timeline_media('My Title')
            timeline_operation_page.double_click()
            time.sleep(3)

            # Maximize window
            title_designer_page.click_maximize_btn()

            # switch to "Advance Mode"
            title_designer_page.switch_mode(2)

            # Verify if in "Title Designer" page with
            current_title = title_designer_page.get_title_text_content()
            logger(f"{current_title= }")
            if not current_title == 'My Title':
                logger('Failed to enter Title Designer Page!')
                raise Exception

            # Enable backdrop
            check_box_status = title_designer_page.backdrop.set_checkbox(1)
            logger(f"{check_box_status= }")

            # Set timecode
            title_designer_page.set_timecode('00_00_01_15')

            # Enable shadow
            check_box_status = title_designer_page.set_check_shadow(1)
            logger(f"{check_box_status= }")

            # unfold special effect
            title_designer_page.special_effects.set_unfold_tab(1)
            time.sleep(DELAY_TIME * 2)

            # Select "No Effect"
            title_designer_page.special_effects.apply_effect(0)

            # Select "Fire"
            title_designer_page.special_effects.apply_effect(4)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.4.1_Title_Designer_Advance_Special_Effect_LED_Preview.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.4.1_Title_Designer_Advance_Special_Effect_LED_Preview.png',
                preview_wnd)
            logger(f"{compare_result=}")

            with uuid('1cef1a81-ce4c-44b2-9102-177207f15f5c') as case:
                # session 2.6 : Object tab (Advance mode) > Object Tab
                # case2.6.9.4.2 : Special Effect > LED Sign > Looks
                # scroll down
                drag_scroll_bar = title_designer_page.drag_object_vertical_slider(1)
                logger(f"{drag_scroll_bar= }")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(2)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.4.2_Title_Designer_Advance_Special_Effect_LED_Looks2.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.4.2_Title_Designer_Advance_Special_Effect_LED_Looks2.png',
                    preview_wnd)
                logger(f"{compare_result1=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(3)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.4.2_Title_Designer_Advance_Special_Effect_LED_Looks3.png')
                logger(preview_wnd)
                compare_result2 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.4.2_Title_Designer_Advance_Special_Effect_LED_Looks3.png',
                    preview_wnd)
                logger(f"{compare_result2=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(4)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.4.2_Title_Designer_Advance_Special_Effect_LED_Looks4.png')
                logger(preview_wnd)
                compare_result3 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.4.2_Title_Designer_Advance_Special_Effect_LED_Looks4.png',
                    preview_wnd)
                logger(f"{compare_result3=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(5)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.4.2_Title_Designer_Advance_Special_Effect_LED_Looks5.png')
                logger(preview_wnd)
                compare_result4 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.4.2_Title_Designer_Advance_Special_Effect_LED_Looks5.png',
                    preview_wnd)
                logger(f"{compare_result4=}")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(6)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.4.2_Title_Designer_Advance_Special_Effect_LED_Looks6.png')
                logger(preview_wnd)
                compare_result5 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.4.2_Title_Designer_Advance_Special_Effect_LED_Looks6.png',
                    preview_wnd)
                logger(f"{compare_result5=}")

                case.result = compare_result1 and compare_result2 and compare_result3 and compare_result4 and compare_result5

            case.result = compare_result

        # 3/30
        with uuid('1f1ece3e-72b9-4964-95b0-063317367ed8') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.4.3.4 : Special Effect > LED Sign > Size > Able to adjust keyframe value
            # Seek to 00:01:15
            time.sleep(DELAY_TIME * 1)
            title_designer_page.set_timecode('00_00_02_15')

            # add keyframe
            title_designer_page.special_effects.size.keyframe.click_add_remove()
            time.sleep(DELAY_TIME * 1)

            # Adjust size
            title_designer_page.special_effects.size.value.set_value(107)
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.4.3.4_Title_Designer_Advance_Special_Effect_LED_Adjust_Size.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.4.3.4_Title_Designer_Advance_Special_Effect_LED_Adjust_Size.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 3/30
        with uuid('41a64e00-e3cf-4fa5-b061-a600924788ef') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.4.6.4 : Special Effect > LED Sign > Color > Able to adjust keyframe value
            # add keyframe
            title_designer_page.special_effects.color.keyframe.click_add_remove()
            time.sleep(DELAY_TIME * 1)

            # seek to another time frame
            #time.sleep(DELAY_TIME * 1)
            title_designer_page.set_timecode('00_00_03_20')

            # Adjust size
            title_designer_page.special_effects.color.set_color('#6020F4')
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.4.6.4_Title_Designer_Advance_Special_Effect_LED_Adjust_Color.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.4.6.4_Title_Designer_Advance_Special_Effect_LED_Adjust_Color.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 3/30
        with uuid('524b5b4c-c5f6-45ca-8d61-db9cce6c6c40') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.4.4 : Special Effect > LED Sign > Density
            # Adjust density
            title_designer_page.special_effects.density.set_value(70)
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.4.4_Title_Designer_Advance_Special_Effect_LED_Adjust_Density.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.4.4_Title_Designer_Advance_Special_Effect_LED_Adjust_Density.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 3/30
        with uuid('fc896317-056e-497b-bd1c-315ce48d18b4') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.5.1 : Special Effect > Neon Sign > Preview
            time.sleep(DELAY_TIME)
            # Select "Neon Sign"
            title_designer_page.special_effects.apply_effect(5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.5.1_Title_Designer_Advance_Special_Effect_Neo_Preview.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.5.1_Title_Designer_Advance_Special_Effect_Neo_Preview.png',
                preview_wnd)
            logger(f"{compare_result=}")

            with uuid('b800c0c5-69e7-4dd2-a556-dbe150a76b49') as case:
                # session 2.6 : Object tab (Advance mode) > Object Tab
                # case2.6.9.5.2 : Special Effect > Neon Sign > Looks
                # scroll down
                drag_scroll_bar = title_designer_page.drag_object_vertical_slider(1)
                logger(f"{drag_scroll_bar= }")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(2)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.5.2_Title_Designer_Advance_Special_Effect_Neon_Looks2.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.5.2_Title_Designer_Advance_Special_Effect_Neon_Looks2.png',
                    preview_wnd)
                logger(f"{compare_result1=}")

                # Switch to different look3
                title_designer_page.special_effects.set_look_menu(3)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.5.2_Title_Designer_Advance_Special_Effect_Neon_Looks3.png')
                logger(preview_wnd)
                compare_result2 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.5.2_Title_Designer_Advance_Special_Effect_Neon_Looks3.png',
                    preview_wnd)
                logger(f"{compare_result2=}")

                # Switch to different look4
                title_designer_page.special_effects.set_look_menu(4)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.5.2_Title_Designer_Advance_Special_Effect_Neon_Looks4.png')
                logger(preview_wnd)
                compare_result3 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.5.2_Title_Designer_Advance_Special_Effect_Neon_Looks4.png',
                    preview_wnd)
                logger(f"{compare_result3=}")

                # Switch to different look5
                title_designer_page.special_effects.set_look_menu(5)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.5.2_Title_Designer_Advance_Special_Effect_Neon_Looks5.png')
                logger(preview_wnd)
                compare_result4 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.5.2_Title_Designer_Advance_Special_Effect_Neon_Looks5.png',
                    preview_wnd)
                logger(f"{compare_result4=}")

                # Switch to different look6
                title_designer_page.special_effects.set_look_menu(6)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.5.2_Title_Designer_Advance_Special_Effect_Neon_Looks6.png')
                logger(preview_wnd)
                compare_result5 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.5.2_Title_Designer_Advance_Special_Effect_Neon_Looks6.png',
                    preview_wnd)
                logger(f"{compare_result5=}")

                case.result = compare_result1 and compare_result2 and compare_result3 and compare_result4 and compare_result5

            case.result = compare_result

        # 3/30
        with uuid('40548a58-672f-4a70-a761-acd072394f6b') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.5.3.4 : Special Effect > Neon Sign > Size > Able to adjust keyframe value
            # Seek to 00:02:20
            time.sleep(DELAY_TIME * 1)
            title_designer_page.set_timecode('00_00_02_20')

            # add keyframe
            title_designer_page.special_effects.size.keyframe.click_add_remove()
            time.sleep(DELAY_TIME * 1)

            # Adjust size
            title_designer_page.special_effects.size.value.set_value(35)
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.5.3.4_Title_Designer_Advance_Special_Effect_Neon_Adjust_Size.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.5.3.4_Title_Designer_Advance_Special_Effect_Neon_Adjust_Size.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 4/7
        with uuid('f36bbe7e-a68b-4358-8801-ea2b4af6e5f3') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.5.4.4 : Special Effect > Neon Sign > Color > Able to adjust keyframe value
            # add keyframe
            title_designer_page.special_effects.color.keyframe.click_add_remove()
            time.sleep(DELAY_TIME * 1)

            # seek to another time frame
            #time.sleep(DELAY_TIME * 1)
            title_designer_page.set_timecode('00_00_03_20')

            # Adjust size
            title_designer_page.special_effects.color.set_color('#6F20FC')
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.5.4.4_Title_Designer_Advance_Special_Effect_Neon_Adjust_Color.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.5.4.4_Title_Designer_Advance_Special_Effect_Neon_Adjust_Color.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 4/7
        with uuid('69d9e0c6-8946-403a-8d0c-f6189824015f') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.6.1 : Special Effect > Electric Wave > Preview
            time.sleep(DELAY_TIME * 5)
            # Select "Electric Wave"
            #title_designer_page.special_effects.apply_effect(6)
            title_designer_page.special_effects.apply_effect(6)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.6.1_Title_Designer_Advance_Special_Effect_EW_Preview.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.6.1_Title_Designer_Advance_Special_Effect_EW_Preview.png',
                preview_wnd)
            logger(f"{compare_result=}")

            with uuid('84c8e511-2458-4721-8927-dc0645fe616f') as case:
                # session 2.6 : Object tab (Advance mode) > Object Tab
                # case2.6.9.6.2 : Special Effect > Electric Wave > Looks
                # scroll down
                drag_scroll_bar = title_designer_page.drag_object_vertical_slider(1)
                logger(f"{drag_scroll_bar= }")

                # Switch to different look2
                title_designer_page.special_effects.set_look_menu(2)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.6.2_Title_Designer_Advance_Special_Effect_EW_Looks2.png')
                logger(preview_wnd)
                compare_result1 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.6.2_Title_Designer_Advance_Special_Effect_EW_Looks2.png',
                    preview_wnd)
                logger(f"{compare_result1=}")

                # Switch to different look3
                title_designer_page.special_effects.set_look_menu(3)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.6.2_Title_Designer_Advance_Special_Effect_EW_Looks3.png')
                logger(preview_wnd)
                compare_result2 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.6.2_Title_Designer_Advance_Special_Effect_EW_Looks3.png',
                    preview_wnd)
                logger(f"{compare_result2=}")

                # Switch to different look4
                title_designer_page.special_effects.set_look_menu(4)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.6.2_Title_Designer_Advance_Special_Effect_EW_Looks4.png')
                logger(preview_wnd)
                compare_result3 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.6.2_Title_Designer_Advance_Special_Effect_EW_Looks4.png',
                    preview_wnd)
                logger(f"{compare_result3=}")

                # Switch to different look5
                title_designer_page.special_effects.set_look_menu(5)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.6.2_Title_Designer_Advance_Special_Effect_EW_Looks5.png')
                logger(preview_wnd)
                compare_result4 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.6.2_Title_Designer_Advance_Special_Effect_EW_Looks5.png',
                    preview_wnd)
                logger(f"{compare_result4=}")

                # Switch to different look6
                title_designer_page.special_effects.set_look_menu(6)
                time.sleep(DELAY_TIME * 1)

                # snapshot
                preview_wnd = tips_area_page.snapshot(
                    locator=L.title_designer.area.frame_preview,
                    file_name=Auto_Ground_Truth_Folder + 'G2.6.9.6.2_Title_Designer_Advance_Special_Effect_EW_Looks6.png')
                logger(preview_wnd)
                compare_result5 = tips_area_page.compare(
                    Ground_Truth_Folder + 'G2.6.9.6.2_Title_Designer_Advance_Special_Effect_EW_Looks6.png',
                    preview_wnd)
                logger(f"{compare_result5=}")

                case.result = compare_result1 and compare_result2 and compare_result3 and compare_result4 and compare_result5

            case.result = compare_result

        # 4/7
        with uuid('733669a9-9b61-445f-8349-7d79d9dbe16a') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.6.3.4 : Special Effect > Electric Wave > Size > Able to adjust keyframe value
            # Seek to 00:02:25
            time.sleep(DELAY_TIME * 1)
            title_designer_page.set_timecode('00_00_02_25')

            # add keyframe
            title_designer_page.special_effects.size.keyframe.click_add_remove()
            time.sleep(DELAY_TIME * 1)

            # Adjust size
            title_designer_page.special_effects.size.value.set_value(181)
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.6.3.4_Title_Designer_Advance_Special_Effect_EW_Adjust_Size.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.6.3.4_Title_Designer_Advance_Special_Effect_EW_Adjust_Size.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 4/7
        with uuid('9d90a1fc-c7e5-430d-96a7-8f2350411da5') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.6.4.4 : Special Effect > Electric Wave > Color > Able to adjust keyframe value
            # add keyframe
            title_designer_page.special_effects.color.keyframe.click_add_remove()
            time.sleep(DELAY_TIME * 1)

            # seek to another time frame
            #time.sleep(DELAY_TIME * 1)
            title_designer_page.set_timecode('00_00_01_12')

            # Adjust size
            title_designer_page.special_effects.color.set_color('#D3A0FC')
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.6.4.4_Title_Designer_Advance_Special_Effect_EW_Adjust_Color.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.6.4.4_Title_Designer_Advance_Special_Effect_EW_Adjust_Color.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 4/7
        with uuid('2ea183e3-e475-473d-89e2-225697d90d41') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.6.6.4 : Special Effect > Electric Wave > Length > Able to adjust keyframe value
            # Seek to 00:02:25
            time.sleep(DELAY_TIME * 1)
            title_designer_page.set_timecode('00_00_02_25')

            # add keyframe
            title_designer_page.special_effects.length.keyframe.click_add_remove()
            time.sleep(DELAY_TIME * 1)

            # Adjust length
            title_designer_page.special_effects.length.value.set_value(147)
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.6.6.4_Title_Designer_Advance_Special_Effect_EW_Adjust_Length.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.6.6.4_Title_Designer_Advance_Special_Effect_EW_Adjust_Length.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 4/7
        with uuid('44ec909c-b83a-4bb2-bf78-d19547c129f9') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.6.7.4 : Special Effect > Electric Wave > Period > Able to adjust keyframe value
            # Seek to 00:02:27
            time.sleep(DELAY_TIME * 1)
            title_designer_page.set_timecode('00_00_02_27')

            # add keyframe
            title_designer_page.special_effects.period.keyframe.click_add_remove()
            time.sleep(DELAY_TIME * 1)

            # Adjust period
            title_designer_page.special_effects.period.value.set_value(40)
            time.sleep(DELAY_TIME * 5)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.6.7.4_Title_Designer_Advance_Special_Effect_EW_Adjust_Period.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.6.7.4_Title_Designer_Advance_Special_Effect_EW_Adjust_Period.png',
                preview_wnd)
            logger(f"{compare_result=}")

            case.result = compare_result

        # 4/15
        with uuid('c359ad1b-eddd-4d39-ac6e-ffc6617ca842') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.6.8.1 : Special Effect > Electric Wave > Co-exist > keyframe of object settings
            # Seek and unfold Object Settings
            time.sleep(DELAY_TIME * 1)
            title_designer_page.set_timecode('00_00_01_27')
            time.sleep(DELAY_TIME * 2)
            title_designer_page.unfold_object_object_setting_tab()

            # add keyframe with position
            title_designer_page.click_object_setting_position_add_keyframe_control()
            time.sleep(DELAY_TIME * 1)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.6.8.1_Title_Designer_Advance_Reset_Special_Effect_Warning.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.6.8.1_Title_Designer_Advance_Reset_Special_Effect_Warning.png',
                preview_wnd)
            logger(f"{compare_result=}")

            # click [ESC] to discard change
            #title_designer_page.press_esc_key()

            case.result = compare_result

        # 4/15
        with uuid('a758b9c3-97fc-4258-8a58-c0ea10b179ce') as case:
            # session 2.6 : Object tab (Advance mode) > Object Tab
            # case2.6.9.6.8.2 : Special Effect > Electric Wave > Co-exist > In/Out animation tab
            # Switch to [Animation] tab
            time.sleep(DELAY_TIME * 1)
            title_designer_page.click_animation_tab()
            time.sleep(DELAY_TIME * 2)

            # select one of effect
            title_designer_page.select_animation_in_animation_effect(1, 3)
            time.sleep(DELAY_TIME * 1)

            # snapshot
            preview_wnd = tips_area_page.snapshot(
                locator=L.title_designer.area.frame_preview,
                file_name=Auto_Ground_Truth_Folder + 'G2.6.9.6.8.2_Title_Designer_Advance_Reset_Special_Effect_Warning1.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.6.9.6.8.2_Title_Designer_Advance_Reset_Special_Effect_Warning1.png',
                preview_wnd)
            logger(f"{compare_result=}")

            # click [ESC] to discard change
            title_designer_page.press_esc_key()

            case.result = compare_result

        # 4/15
        with uuid('68d98843-dad0-4a62-baa2-7cd3df0aabfb') as case:
            # session 2.7 : Animation tab (Advance mode) > Animation Tab
            # case2.7.3.1 : Motion blur > Apply motion blur
            # fold in-animation
            time.sleep(DELAY_TIME * 1)
            title_designer_page.unfold_animation_in_animation_tab(0)
            time.sleep(DELAY_TIME * 1)

            # tick checkbox of motion blur
            title_designer_page.motion_blur.set_checkbox(1)

            # unfold motion blur
            title_designer_page.motion_blur.set_unfold(1)

            # get checkbox status
            checkbox_status = title_designer_page.motion_blur.get_checkbox_status()
            logger(f"{checkbox_status=}")

            case.result = checkbox_status

        # 4/15
        with uuid('764f4e9f-0e35-45d3-8e13-863dd627deb6') as case:
            # session 2.7 : Animation tab (Advance mode) > Animation Tab
            # case2.7.3.2.1 : Motion blur > Blur_length > slider
            # adjust blur length by slider
            result = title_designer_page.motion_blur.blur_length.adjust_slider(1.26)
            logger(f"{result=}")

            case.result = result

        # 4/15
        with uuid('fb638d8b-2ac6-47cc-b363-0f7c0f3f984c') as case:
            # session 2.7 : Animation tab (Advance mode) > Animation Tab
            # case2.7.3.2.2 : Motion blur > Blur_length > input value
            # adjust blur length by input value
            result = title_designer_page.motion_blur.blur_length.set_value(0.60)
            logger(f"{result=}")

            case.result = result

